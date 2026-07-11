#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

APP=${APP:-$HOME/gl/apps/vscode}
LAUNCHER=${LAUNCHER:-$HOME/projects/termux-native-desktop/experiments/glibc/vulkan-policy-composition/recipe/launch-vscode-with-policy.sh}
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-policy-env-boundary-$(date +%Y%m%d-%H%M%S)}
DURATION_SECONDS=${DURATION_SECONDS:-15}
POLL_SLEEP_SECONDS=${POLL_SLEEP_SECONDS:-0.1}
CONTROL_GL_GPU=${CONTROL_GL_GPU:-1}
VULKAN_POLICY_MODE=${VULKAN_POLICY_MODE:-explicit-freedreno}
VK_LOADER_DEBUG_VALUE=${VK_LOADER_DEBUG_VALUE:-all}

for command in awk date pgrep readlink sort tr grep sed wc; do
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
printf 'timestamp\tpid\tppid\tclass\targv0\tcmdline\n' >"$OUT/processes.tsv"
printf 'timestamp\tpid\tclass\tstate\tentry_count\tselected_key_count\n' >"$OUT/process-environment-summary.tsv"
printf 'timestamp\tpid\tclass\tkey\tvalue\n' >"$OUT/process-environment-selected.tsv"
printf 'timestamp\tpid\tclass\tfd\ttarget\n' >"$OUT/process-stdio-fds.tsv"
printf 'sample\ttimestamp\tmain_seen\tzygote_seen\tgpu_seen\n' >"$OUT/observation-state.tsv"

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
declare -A CAPTURED=()
MAIN_SEEN=0
ZYGOTE_SEEN=0
GPU_SEEN=0

read_cmdline() {
    local pid=$1
    [ -r "/proc/$pid/cmdline" ] || return 1
    { tr '\0' ' ' <"/proc/$pid/cmdline"; } 2>/dev/null
}

read_argv0() {
    local pid=$1
    [ -r "/proc/$pid/cmdline" ] || return 1
    { tr '\0' '\n' <"/proc/$pid/cmdline" | sed -n '1p'; } 2>/dev/null
}

classify_cmdline() {
    local pid=$1 cmdline=$2 argv0=$3

    if [ "$pid" = "$LAUNCH_PID" ]; then
        printf 'launch-wrapper\n'
        return 0
    fi

    case "$cmdline" in
        *resources/app/out/cli.js*) printf 'node-cli\n' ;;
        *--type=gpu-process*) printf 'gpu\n' ;;
        *--type=renderer*) printf 'renderer\n' ;;
        *--type=utility*) printf 'utility\n' ;;
        *--type=zygote*) printf 'zygote\n' ;;
        *chrome_crashpad_handler*) printf 'crashpad\n' ;;
        *)
            if [ "$argv0" = "$APP/code" ] && [[ "$cmdline" != *" --type="* ]]; then
                printf 'main\n'
            elif [[ "$cmdline" == *"$APP/bin/code"* ]]; then
                printf 'cli-wrapper\n'
            else
                printf 'helper\n'
            fi
            ;;
    esac
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
    local timestamp=$1 pid=$2 class=$3 raw stderr_file entry_count selected_count
    raw="$OUT/.environ-$pid.raw"
    stderr_file="$OUT/.environ-$pid.stderr"

    if [ ! -r "/proc/$pid/environ" ]; then
        printf '%s\t%s\t%s\tUNREADABLE\t0\t0\n' \
            "$timestamp" "$pid" "$class" \
            >>"$OUT/process-environment-summary.tsv"
        return 1
    fi

    if ! { tr '\0' '\n' <"/proc/$pid/environ" >"$raw"; } 2>"$stderr_file"; then
        printf '%s\t%s\t%s\tREAD_FAILED\t0\t0\n' \
            "$timestamp" "$pid" "$class" \
            >>"$OUT/process-environment-summary.tsv"
        return 1
    fi

    entry_count=$(awk 'NF { count++ } END { print count + 0 }' "$raw")

    selected_count=0
    while IFS= read -r line; do
        [ -n "$line" ] || continue
        key=${line%%=*}
        value=${line#*=}
        printf '%s\t%s\t%s\t%s\t%s\n' \
            "$timestamp" "$pid" "$class" "$key" "$value" \
            >>"$OUT/process-environment-selected.tsv"
        selected_count=$((selected_count + 1))
    done < <(
        grep -E '^(VK_LOADER_DEBUG|VK_DRIVER_FILES|VK_ICD_FILENAMES|TND_EXPERIMENT_VULKAN_POLICY|LD_LIBRARY_PATH|LD_PRELOAD|LIBGL_ALWAYS_SOFTWARE|MESA_LOADER_DRIVER_OVERRIDE)=' "$raw" \
            | sort \
            || true
    )

    printf '%s\t%s\t%s\tREAD_OK\t%s\t%s\n' \
        "$timestamp" "$pid" "$class" "$entry_count" "$selected_count" \
        >>"$OUT/process-environment-summary.tsv"
}

capture_stdio() {
    local timestamp=$1 pid=$2 class=$3 fd target

    for fd in 0 1 2; do
        if [ -e "/proc/$pid/fd/$fd" ]; then
            target=$(readlink "/proc/$pid/fd/$fd" 2>/dev/null || true)
            [ -n "$target" ] || target=UNRESOLVED
        else
            target=CLOSED_OR_UNAVAILABLE
        fi
        printf '%s\t%s\t%s\t%s\t%s\n' \
            "$timestamp" "$pid" "$class" "$fd" "$target" \
            >>"$OUT/process-stdio-fds.tsv"
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
        [ -n "$pid" ] || continue
        cmdline=$(read_cmdline "$pid" || true)
        [ -n "$cmdline" ] || continue
        argv0=$(read_argv0 "$pid" || true)
        [ -n "$argv0" ] || continue
        OBSERVED_PIDS+=("$pid")

        class=$(classify_cmdline "$pid" "$cmdline" "$argv0")
        ppid=$(awk '/^PPid:/ { print $2; exit }' "/proc/$pid/status" 2>/dev/null || true)

        case "$class" in
            main) MAIN_SEEN=1 ;;
            zygote) ZYGOTE_SEEN=1 ;;
            gpu) GPU_SEEN=1 ;;
        esac

        if [ -z "${CAPTURED[$pid]:-}" ]; then
            CAPTURED["$pid"]=1
            printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
                "$timestamp" "$pid" "${ppid:-UNKNOWN}" "$class" "$argv0" "$cmdline" \
                >>"$OUT/processes.tsv"
            capture_environment "$timestamp" "$pid" "$class" || true
            capture_stdio "$timestamp" "$pid" "$class"
        fi
    done

    printf '%s\t%s\t%s\t%s\t%s\n' \
        "$sample" "$timestamp" "$MAIN_SEEN" "$ZYGOTE_SEEN" "$GPU_SEEN" \
        >>"$OUT/observation-state.tsv"

    if [ "$MAIN_SEEN" = 1 ] && [ "$ZYGOTE_SEEN" = 1 ] && [ "$GPU_SEEN" = 1 ]; then
        break
    fi

    sleep "$POLL_SLEEP_SECONDS"
done

[ "$MAIN_SEEN" = 1 ] || {
    printf 'main process was not observed\n' >&2
    exit 1
}

[ "$ZYGOTE_SEEN" = 1 ] || {
    printf 'zygote process was not observed\n' >&2
    exit 1
}

[ "$GPU_SEEN" = 1 ] || {
    printf 'gpu process was not observed\n' >&2
    exit 1
}

for required_class in main zygote gpu; do
    if ! awk -F $'\t' -v c="$required_class" 'NR > 1 && $3 == c && $4 == "READ_OK" { found=1 } END { exit found ? 0 : 1 }' \
        "$OUT/process-environment-summary.tsv"; then
        printf 'no successful environment read for required class: %s\n' "$required_class" >&2
        exit 1
    fi
done

printf 'PASS\n' >"$OUT/probe.status"

printf '\nVS Code policy environment boundary probe: PASS\n'
printf 'evidence: %s\n' "$OUT"

printf '\n===== process environment summary =====\n'
cat "$OUT/process-environment-summary.tsv"

printf '\n===== selected environment keys =====\n'
cat "$OUT/process-environment-selected.tsv"

printf '\n===== process stdio fds =====\n'
cat "$OUT/process-stdio-fds.tsv"

printf '\n===== process identities =====\n'
cat "$OUT/processes.tsv"

printf '\n===== launch stdout bytes =====\n'
wc -c "$OUT/launch.stdout"

printf '\n===== launch stderr =====\n'
sed -n '1,160p' "$OUT/launch.stderr" || true
