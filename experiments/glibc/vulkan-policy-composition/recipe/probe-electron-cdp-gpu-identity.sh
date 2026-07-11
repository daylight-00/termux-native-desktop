#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
APP=${APP:?set APP to the extracted Electron application directory}
ENTRYPOINT=${ENTRYPOINT:?set ENTRYPOINT to the Electron executable}
LAUNCHER=${LAUNCHER:?set LAUNCHER to the promoted application launcher}
APP_LABEL=${APP_LABEL:-Electron}
PYTHON=${PYTHON:-$PREFIX/bin/python}
QUERY_HELPER=${QUERY_HELPER:-$SCRIPT_DIR/query-cdp-system-info.py}
USER_DATA_DIR=${USER_DATA_DIR:?set USER_DATA_DIR to an isolated application data directory}
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/electron-cdp-gpu-identity-$(date +%Y%m%d-%H%M%S)}
DURATION_SECONDS=${DURATION_SECONDS:-30}
POLL_SLEEP_SECONDS=${POLL_SLEEP_SECONDS:-0.1}
CONTROL_GL_GPU=${CONTROL_GL_GPU:-1}
VULKAN_POLICY_MODE=${VULKAN_POLICY_MODE:-explicit-freedreno}

for command in awk date pgrep readlink sort tr sed grep cp mv rm wc sleep; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

[ -x "$ENTRYPOINT" ] || {
    printf 'missing %s entrypoint: %s\n' "$APP_LABEL" "$ENTRYPOINT" >&2
    exit 1
}

[ -x "$LAUNCHER" ] || {
    printf 'missing %s launcher: %s\n' "$APP_LABEL" "$LAUNCHER" >&2
    exit 1
}

[ -x "$PYTHON" ] || {
    printf 'missing Python interpreter: %s\n' "$PYTHON" >&2
    exit 1
}

[ -f "$QUERY_HELPER" ] || {
    printf 'missing CDP query helper: %s\n' "$QUERY_HELPER" >&2
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

if [ "${LIBGL_ALWAYS_SOFTWARE+x}" = x ]; then
    printf 'LIBGL_ALWAYS_SOFTWARE must be unset for this probe\n' >&2
    exit 2
fi

existing=$(pgrep -af "$APP/" || true)
if [ -n "$existing" ]; then
    printf 'existing %s processes detected; close them before the probe:\n' "$APP_LABEL" >&2
    printf '%s\n' "$existing" >&2
    exit 1
fi

mkdir -p "$OUT" "$USER_DATA_DIR"
ACTIVE_PORT_FILE="$USER_DATA_DIR/DevToolsActivePort"
STALE_ACTIVE_PORT=

if [ -e "$ACTIVE_PORT_FILE" ]; then
    STALE_ACTIVE_PORT="$OUT/DevToolsActivePort.preexisting"
    mv "$ACTIVE_PORT_FILE" "$STALE_ACTIVE_PORT"
fi

printf 'app: %s\n' "$APP" | tee "$OUT/app-path.txt"
printf 'entrypoint: %s\n' "$ENTRYPOINT" | tee "$OUT/entrypoint-path.txt"
printf 'launcher: %s\n' "$LAUNCHER" | tee "$OUT/launcher-path.txt"
printf 'user data dir: %s\n' "$USER_DATA_DIR" | tee "$OUT/user-data-dir.txt"
printf 'duration seconds: %s\n' "$DURATION_SECONDS" | tee "$OUT/duration.txt"
printf 'poll sleep seconds: %s\n' "$POLL_SLEEP_SECONDS" | tee "$OUT/poll-sleep.txt"
printf 'GL_GPU=%s\n' "$CONTROL_GL_GPU" | tee "$OUT/mode.txt"
printf 'VULKAN_POLICY_MODE=%s\n' "$VULKAN_POLICY_MODE" | tee -a "$OUT/mode.txt"

GL_GPU="$CONTROL_GL_GPU" \
VULKAN_POLICY_MODE="$VULKAN_POLICY_MODE" \
"$LAUNCHER" \
    --user-data-dir "$USER_DATA_DIR" \
    --remote-debugging-address=127.0.0.1 \
    --remote-debugging-port=0 \
    >"$OUT/launch.stdout" \
    2>"$OUT/launch.stderr" &
LAUNCH_PID=$!
printf '%s\n' "$LAUNCH_PID" >"$OUT/launch.pid"
printf 'launch pid: %s\n' "$LAUNCH_PID"

OBSERVED_PIDS=("$LAUNCH_PID")
GPU_PID=

read_cmdline() {
    local pid=$1
    [ -r "/proc/$pid/cmdline" ] || return 1
    tr '\0' ' ' <"/proc/$pid/cmdline" 2>/dev/null
}

pid_still_belongs_to_probe() {
    local pid=$1 cmdline
    cmdline=$(read_cmdline "$pid" || true)
    [ -n "$cmdline" ] || return 1
    case "$cmdline" in
        *"$APP/"*|*"$USER_DATA_DIR"*) return 0 ;;
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

    mapfile -t remaining < <(pgrep -f "$APP/|$USER_DATA_DIR" 2>/dev/null | sort -n || true)
    for pid in "${remaining[@]:-}"; do
        if pid_still_belongs_to_probe "$pid"; then
            kill -TERM "$pid" 2>/dev/null || true
        fi
    done

    sleep 1

    mapfile -t remaining < <(pgrep -f "$APP/|$USER_DATA_DIR" 2>/dev/null | sort -n || true)
    for pid in "${remaining[@]:-}"; do
        if pid_still_belongs_to_probe "$pid"; then
            kill -KILL "$pid" 2>/dev/null || true
        fi
    done

    if [ -f "$ACTIVE_PORT_FILE" ]; then
        cp "$ACTIVE_PORT_FILE" "$OUT/DevToolsActivePort.final" 2>/dev/null || true
        rm -f "$ACTIVE_PORT_FILE"
    fi

    if [ -n "$STALE_ACTIVE_PORT" ] && [ -f "$STALE_ACTIVE_PORT" ]; then
        mv "$STALE_ACTIVE_PORT" "$ACTIVE_PORT_FILE"
    fi
}
trap cleanup EXIT

started=$SECONDS
deadline=$((started + DURATION_SECONDS))
port=
browser_path=

while (( SECONDS < deadline )); do
    mapfile -t app_pids < <(pgrep -f "$APP/|$USER_DATA_DIR" 2>/dev/null | sort -n || true)
    for pid in "${app_pids[@]:-}"; do
        [ -n "$pid" ] || continue
        cmdline=$(read_cmdline "$pid" || true)
        [ -n "$cmdline" ] || continue
        OBSERVED_PIDS+=("$pid")
        case "$cmdline" in
            *--type=gpu-process*)
                [ -n "$GPU_PID" ] || GPU_PID=$pid
                ;;
        esac
    done

    if [ -s "$ACTIVE_PORT_FILE" ]; then
        port=$(sed -n '1p' "$ACTIVE_PORT_FILE" | tr -d '\r')
        browser_path=$(sed -n '2p' "$ACTIVE_PORT_FILE" | tr -d '\r')
    fi

    if [ -n "$port" ] && [ -n "$browser_path" ] && [ -n "$GPU_PID" ]; then
        break
    fi

    sleep "$POLL_SLEEP_SECONDS"
done

[ -n "$port" ] || {
    printf 'DevToolsActivePort did not provide a port within %s seconds\n' "$DURATION_SECONDS" >&2
    printf 'partial evidence: %s\n' "$OUT" >&2
    exit 1
}

[ -n "$browser_path" ] || {
    printf 'DevToolsActivePort did not provide a browser websocket path\n' >&2
    printf 'partial evidence: %s\n' "$OUT" >&2
    exit 1
}

[ -n "$GPU_PID" ] || {
    printf 'GPU process was not observed within %s seconds\n' "$DURATION_SECONDS" >&2
    printf 'partial evidence: %s\n' "$OUT" >&2
    exit 1
}

cp "$ACTIVE_PORT_FILE" "$OUT/DevToolsActivePort"
WEBSOCKET_URL="ws://127.0.0.1:${port}${browser_path}"
printf '%s\n' "$WEBSOCKET_URL" >"$OUT/websocket-url.txt"
printf '%s\n' "$GPU_PID" >"$OUT/gpu.pid"
printf 'gpu pid: %s\n' "$GPU_PID"
printf 'devtools port: %s\n' "$port"

"$PYTHON" "$QUERY_HELPER" \
    --websocket-url "$WEBSOCKET_URL" \
    --out "$OUT" \
    --timeout 10

[ -r "/proc/$GPU_PID/maps" ] || {
    printf 'GPU maps unavailable after CDP query: %s\n' "$GPU_PID" >&2
    exit 1
}

cat "/proc/$GPU_PID/maps" >"$OUT/gpu.maps"
{
    printf 'path\n'
    awk '$NF ~ /^\// { print $NF }' "$OUT/gpu.maps" \
        | sort -u \
        | grep -E 'libEGL\.so|libGLESv2\.so|libvulkan[^/]*\.so|libVkLayer|libgbm\.so|^/dev/kgsl-3d0$' \
        || true
} >"$OUT/gpu-graphics-paths.tsv"

printf 'PASS\n' >"$OUT/probe.status"

printf '\n%s CDP GPU identity probe: PASS\n' "$APP_LABEL"
printf 'evidence: %s\n' "$OUT"

printf '\n===== GPU devices =====\n'
cat "$OUT/gpu-devices.tsv"
printf '\n===== GPU aux attributes =====\n'
cat "$OUT/gpu-aux-attributes.tsv"
printf '\n===== GPU feature status =====\n'
cat "$OUT/gpu-feature-status.tsv"
printf '\n===== GPU mapped graphics paths =====\n'
cat "$OUT/gpu-graphics-paths.tsv"
printf '\n===== launch stderr =====\n'
sed -n '1,200p' "$OUT/launch.stderr" || true
