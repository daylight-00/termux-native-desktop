#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

APP=${APP:-$HOME/gl/apps/vscode}
LAUNCHER=${LAUNCHER:-$HOME/projects/termux-native-desktop/experiments/glibc/vulkan-policy-composition/recipe/launch-vscode-with-policy.sh}
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-process-handoff-$(date +%Y%m%d-%H%M%S)}
DURATION_SECONDS=${DURATION_SECONDS:-12}
POLL_SLEEP_SECONDS=${POLL_SLEEP_SECONDS:-0.1}
CONTROL_GL_GPU=${CONTROL_GL_GPU:-1}
VULKAN_POLICY_MODE=${VULKAN_POLICY_MODE:-explicit-freedreno}

for command in awk date pgrep sort tr; do
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
printf 'sample\ttimestamp\tlaunch_alive\tpid\tppid\tclass\tcmdline\n' >"$OUT/process-topology.tsv"
printf 'sample\ttimestamp\tlaunch_alive\n' >"$OUT/launch-state.tsv"

printf 'app: %s\n' "$APP" | tee "$OUT/app-path.txt"
printf 'launcher: %s\n' "$LAUNCHER" | tee "$OUT/launcher-path.txt"
printf 'duration seconds: %s\n' "$DURATION_SECONDS" | tee "$OUT/duration.txt"
printf 'poll sleep seconds: %s\n' "$POLL_SLEEP_SECONDS" | tee "$OUT/poll-sleep.txt"
printf 'GL_GPU=%s\n' "$CONTROL_GL_GPU" | tee "$OUT/mode.txt"
printf 'VULKAN_POLICY_MODE=%s\n' "$VULKAN_POLICY_MODE" | tee -a "$OUT/mode.txt"

GL_GPU="$CONTROL_GL_GPU" \
VULKAN_POLICY_MODE="$VULKAN_POLICY_MODE" \
"$LAUNCHER" \
    >"$OUT/launch.stdout" \
    2>"$OUT/launch.stderr" &
LAUNCH_PID=$!
printf '%s\n' "$LAUNCH_PID" >"$OUT/launch.pid"
printf 'launch pid: %s\n' "$LAUNCH_PID"

declare -A OBSERVED_PIDS=()
OBSERVED_PIDS["$LAUNCH_PID"]=1

classify_cmdline() {
    local pid=$1 cmdline=$2

    if [ "$pid" = "$LAUNCH_PID" ]; then
        printf 'launch-wrapper\n'
        return 0
    fi

    case "$cmdline" in
        *--type=renderer*) printf 'renderer\n' ;;
        *--type=utility*) printf 'utility\n' ;;
        *--type=gpu-process*) printf 'gpu\n' ;;
        *--type=zygote*) printf 'zygote\n' ;;
        *chrome_crashpad_handler*) printf 'crashpad\n' ;;
        *resources/app/out/cli.js*) printf 'node-cli\n' ;;
        *"$APP/bin/code"*) printf 'cli-wrapper\n' ;;
        *"$APP/code"*) printf 'electron-main-candidate\n' ;;
        *) printf 'app-related\n' ;;
    esac
}

app_pid_snapshot() {
    pgrep -f "$APP/" 2>/dev/null | sort -n || true
}

pid_still_belongs_to_probe() {
    local pid=$1 cmdline

    [ -r "/proc/$pid/cmdline" ] || return 1
    cmdline=$(tr '\0' ' ' <"/proc/$pid/cmdline" 2>/dev/null || true)

    case "$cmdline" in
        *"$APP/"*) return 0 ;;
        *) return 1 ;;
    esac
}

cleanup() {
    local pid

    for pid in "${!OBSERVED_PIDS[@]}"; do
        if pid_still_belongs_to_probe "$pid"; then
            kill -TERM "$pid" 2>/dev/null || true
        fi
    done

    sleep 1

    for pid in "${!OBSERVED_PIDS[@]}"; do
        if pid_still_belongs_to_probe "$pid"; then
            kill -KILL "$pid" 2>/dev/null || true
        fi
    done
}
trap cleanup EXIT

started=$SECONDS
deadline=$((started + DURATION_SECONDS))
sample=0

while (( SECONDS < deadline )); do
    sample=$((sample + 1))
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%S.%NZ)

    launch_alive=0
    [ -d "/proc/$LAUNCH_PID" ] && launch_alive=1
    printf '%s\t%s\t%s\n' \
        "$sample" "$timestamp" "$launch_alive" \
        >>"$OUT/launch-state.tsv"

    mapfile -t app_pids < <(app_pid_snapshot)
    for pid in "${app_pids[@]:-}"; do
        [ -r "/proc/$pid/status" ] || continue
        [ -r "/proc/$pid/cmdline" ] || continue

        ppid=$(awk '/^PPid:/ { print $2; exit }' "/proc/$pid/status" 2>/dev/null || true)
        cmdline=$(tr '\0' ' ' <"/proc/$pid/cmdline" 2>/dev/null || true)
        [ -n "$ppid" ] || continue
        [ -n "$cmdline" ] || continue

        class=$(classify_cmdline "$pid" "$cmdline")
        OBSERVED_PIDS["$pid"]=1
        printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
            "$sample" "$timestamp" "$launch_alive" \
            "$pid" "$ppid" "$class" "$cmdline" \
            >>"$OUT/process-topology.tsv"
    done

    sleep "$POLL_SLEEP_SECONDS"
done

printf '\n===== launch-root state transitions =====\n'
awk -F '\t' '
    NR == 1 { next }
    !seen || $3 != previous {
        print
        previous = $3
        seen = 1
    }
' "$OUT/launch-state.tsv"

printf '\n===== process identity/parent transitions =====\n'
printf 'timestamp\tpid\tppid\tclass\tcmdline\n'
awk -F '\t' '
    NR == 1 { next }
    {
        state = $5 "\t" $6
        if (!($4 in previous) || previous[$4] != state) {
            print $2 "\t" $4 "\t" $5 "\t" $6 "\t" $7
            previous[$4] = state
        }
    }
' "$OUT/process-topology.tsv"

printf '\n===== launch stderr =====\n'
sed -n '1,160p' "$OUT/launch.stderr" || true

printf '\nprobe complete\n'
printf 'evidence: %s\n' "$OUT"
