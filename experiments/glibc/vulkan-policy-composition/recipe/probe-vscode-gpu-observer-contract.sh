#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

APP=${APP:-$HOME/gl/apps/vscode}
LAUNCHER=${LAUNCHER:-$HOME/projects/termux-native-desktop/experiments/glibc/vulkan-policy-composition/recipe/launch-vscode-with-policy.sh}
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-gpu-observer-contract-$(date +%Y%m%d-%H%M%S)}
DURATION_SECONDS=${DURATION_SECONDS:-15}
POLL_SLEEP_SECONDS=${POLL_SLEEP_SECONDS:-0.1}
CONTROL_GL_GPU=${CONTROL_GL_GPU:-1}
VULKAN_POLICY_MODE=${VULKAN_POLICY_MODE:-explicit-freedreno}
VK_LOADER_DEBUG_VALUE=${VK_LOADER_DEBUG_VALUE:-all}

for command in awk date pgrep readlink sort tr grep sed; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

[ -x "$APP/bin/code" ] || {
    printf 'missing VS Code entrypoint: %s\n' "$APP/bin/code" >&2
    exit 1
}

[ -x "$LAUNCHER" ] || {
    printf 'missing experiment launcher: %s\n' "$LAUNCHER" >&2
    exit 1
}

case "$DURATION_SECONDS" in
    ''|*[!0-9]*|0)
        printf 'DURATION_SECONDS must be a positive integer: %s\n' "$DURATION_SECONDS" >&2
        exit 2
        ;;
esac

[ "$CONTROL_GL_GPU" = 1 ] || {
    printf 'this probe requires CONTROL_GL_GPU=1\n' >&2
    exit 2
}

[ "$VULKAN_POLICY_MODE" = explicit-freedreno ] || {
    printf 'this probe requires VULKAN_POLICY_MODE=explicit-freedreno\n' >&2
    exit 2
}

if [ "${LIBGL_ALWAYS_SOFTWARE+x}" = x ]; then
    printf 'LIBGL_ALWAYS_SOFTWARE must be unset for this control\n' >&2
    exit 2
fi

existing=$(pgrep -af "$APP/" || true)
if [ -n "$existing" ]; then
    printf 'existing VS Code processes detected; close them before the probe:\n' >&2
    printf '%s\n' "$existing" >&2
    exit 1
fi

mkdir -p "$OUT"
printf 'key\tvalue\n' >"$OUT/gpu-environment.tsv"
printf 'state\tentry_count\tselected_key_count\n' >"$OUT/gpu-environment-read-state.tsv"
printf 'fd\ttarget\n' >"$OUT/gpu-stdio-fds.tsv"
printf 'timestamp\tpid\tppid\tcmdline\n' >"$OUT/gpu-process-selection.tsv"
printf 'sample\ttimestamp\tgpu_pid\tenvironment_captured\tstdio_captured\n' >"$OUT/observation-state.tsv"

printf 'app: %s\n' "$APP" | tee "$OUT/app-path.txt"
printf 'launcher: %s\n' "$LAUNCHER" | tee "$OUT/launcher-path.txt"
printf 'duration seconds: %s\n' "$DURATION_SECONDS" | tee "$OUT/duration.txt"
printf 'poll sleep seconds: %s\n' "$POLL_SLEEP_SECONDS" | tee "$OUT/poll-sleep.txt"
printf 'GL_GPU=%s\n' "$CONTROL_GL_GPU" | tee "$OUT/mode.txt"
printf 'VULKAN_POLICY_MODE=%s\n' "$VULKAN_POLICY_MODE" | tee -a "$OUT/mode.txt"
printf 'VK_LOADER_DEBUG=%s\n' "$VK_LOADER_DEBUG_VALUE" | tee -a "$OUT/mode.txt"

GL_GPU="$CONTROL_GL_GPU" \
VULKAN_POLICY_MODE="$VULKAN_POLICY_MODE" \
VK_LOADER_DEBUG="$VK_LOADER_DEBUG_VALUE" \
"$LAUNCHER" \
    >"$OUT/launch.stdout" \
    2>"$OUT/launch.stderr" &
LAUNCH_PID=$!
printf '%s\n' "$LAUNCH_PID" >"$OUT/launch.pid"
printf 'launch pid: %s\n' "$LAUNCH_PID"

OBSERVED_PIDS=("$LAUNCH_PID")
GPU_PID=
ENV_CAPTURED=0
STDIO_CAPTURED=0

read_cmdline() {
    local pid=$1
    [ -r "/proc/$pid/cmdline" ] || return 1
    { tr '\0' ' ' <"/proc/$pid/cmdline"; } 2>/dev/null
}

pid_still_belongs_to_probe() {
    local pid=$1 cmdline

    cmdline=$(read_cmdline "$pid" || true)
    [ -n "$cmdline" ] || return 1

    case "$cmdline" in
        *"$APP/"*) return 0 ;;
        *) return 1 ;;
    esac
}

cleanup() {
    local pid

    for pid in "${OBSERVED_PIDS[@]:-}"; do
        if pid_still_belongs_to_probe "$pid"; then
            kill -TERM "$pid" 2>/dev/null || true
        fi
    done

    mapfile -t remaining < <(pgrep -f "$APP/" 2>/dev/null | sort -n || true)
    for pid in "${remaining[@]:-}"; do
        if pid_still_belongs_to_probe "$pid"; then
            kill -TERM "$pid" 2>/dev/null || true
        fi
    done

    sleep 1

    mapfile -t remaining < <(pgrep -f "$APP/" 2>/dev/null | sort -n || true)
    for pid in "${remaining[@]:-}"; do
        if pid_still_belongs_to_probe "$pid"; then
            kill -KILL "$pid" 2>/dev/null || true
        fi
    done
}
trap cleanup EXIT

capture_environment() {
    local pid=$1 tmp entry_count selected_count
    tmp="$OUT/.gpu-environment.raw"

    [ -r "/proc/$pid/environ" ] || return 1

    if ! { tr '\0' '\n' <"/proc/$pid/environ" >"$tmp"; } 2>"$OUT/gpu-environment-read.stderr"; then
        printf 'READ_FAILED\t0\t0\n' >>"$OUT/gpu-environment-read-state.tsv"
        return 1
    fi

    entry_count=$(awk 'NF { count++ } END { print count + 0 }' "$tmp")

    {
        printf 'key\tvalue\n'
        grep -E '^(VK_LOADER_DEBUG|VK_DRIVER_FILES|VK_ICD_FILENAMES|TND_EXPERIMENT_VULKAN_POLICY|LD_LIBRARY_PATH|LD_PRELOAD|LIBGL_ALWAYS_SOFTWARE|MESA_LOADER_DRIVER_OVERRIDE)=' "$tmp" \
            | sort \
            | awk -F '=' '{ key=$1; sub(/^[^=]*=/, "", $0); print key "\t" $0 }' \
            || true
    } >"$OUT/gpu-environment.tsv"

    selected_count=$(( $(wc -l <"$OUT/gpu-environment.tsv") - 1 ))
    printf 'READ_OK\t%s\t%s\n' "$entry_count" "$selected_count" >>"$OUT/gpu-environment-read-state.tsv"
    return 0
}

capture_stdio() {
    local pid=$1 fd target

    printf 'fd\ttarget\n' >"$OUT/gpu-stdio-fds.tsv"
    for fd in 0 1 2; do
        if [ -e "/proc/$pid/fd/$fd" ]; then
            target=$(readlink "/proc/$pid/fd/$fd" 2>/dev/null || true)
            printf '%s\t%s\n' "$fd" "$target" >>"$OUT/gpu-stdio-fds.tsv"
        else
            printf '%s\tCLOSED_OR_UNAVAILABLE\n' "$fd" >>"$OUT/gpu-stdio-fds.tsv"
        fi
    done
}

started=$SECONDS
deadline=$((started + DURATION_SECONDS))
sample=0

while (( SECONDS < deadline )); do
    sample=$((sample + 1))
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%S.%NZ)

    mapfile -t app_pids < <(pgrep -f "$APP/" 2>/dev/null | sort -n || true)
    for pid in "${app_pids[@]:-}"; do
        cmdline=$(read_cmdline "$pid" || true)
        [ -n "$cmdline" ] || continue
        OBSERVED_PIDS+=("$pid")

        case "$cmdline" in
            *--type=gpu-process*)
                if [ -z "$GPU_PID" ]; then
                    GPU_PID=$pid
                    ppid=$(awk '/^PPid:/ { print $2; exit }' "/proc/$pid/status" 2>/dev/null || true)
                    printf '%s\t%s\t%s\t%s\n' "$timestamp" "$pid" "${ppid:-UNKNOWN}" "$cmdline" \
                        >>"$OUT/gpu-process-selection.tsv"
                    printf 'gpu pid: %s\n' "$GPU_PID"
                elif [ "$GPU_PID" != "$pid" ]; then
                    printf 'multiple gpu process identities observed: first=%s later=%s\n' "$GPU_PID" "$pid" >&2
                    exit 1
                fi
                ;;
        esac
    done

    if [ -n "$GPU_PID" ] && [ "$ENV_CAPTURED" = 0 ]; then
        if capture_environment "$GPU_PID"; then
            ENV_CAPTURED=1
        fi
    fi

    if [ -n "$GPU_PID" ] && [ "$STDIO_CAPTURED" = 0 ]; then
        capture_stdio "$GPU_PID"
        STDIO_CAPTURED=1
    fi

    printf '%s\t%s\t%s\t%s\t%s\n' \
        "$sample" "$timestamp" "${GPU_PID:-NONE}" "$ENV_CAPTURED" "$STDIO_CAPTURED" \
        >>"$OUT/observation-state.tsv"

    [ "$ENV_CAPTURED" = 1 ] && [ "$STDIO_CAPTURED" = 1 ] && break
    sleep "$POLL_SLEEP_SECONDS"
done

[ -n "$GPU_PID" ] || {
    printf 'gpu process was not observed within %s seconds\n' "$DURATION_SECONDS" >&2
    exit 1
}

[ "$ENV_CAPTURED" = 1 ] || {
    printf 'gpu environment was not captured\n' >&2
    exit 1
}

[ "$STDIO_CAPTURED" = 1 ] || {
    printf 'gpu stdio fd targets were not captured\n' >&2
    exit 1
}

printf 'PASS\n' >"$OUT/probe.status"

printf '\nVS Code GPU observer contract probe: PASS\n'
printf 'evidence: %s\n' "$OUT"

printf '\n===== gpu environment read state =====\n'
cat "$OUT/gpu-environment-read-state.tsv"

printf '\n===== gpu environment =====\n'
cat "$OUT/gpu-environment.tsv"

printf '\n===== gpu stdio fds =====\n'
cat "$OUT/gpu-stdio-fds.tsv"

printf '\n===== launch stdout bytes =====\n'
wc -c "$OUT/launch.stdout"

printf '\n===== launch stderr =====\n'
sed -n '1,160p' "$OUT/launch.stderr" || true
