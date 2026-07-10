#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROBE=${PROBE:-$PREFIX/tmp/tnd-vulkan-policy-composition/glx-renderer-probe}
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/implicit-loader-debug-$(date +%Y%m%d-%H%M%S)}
LOADER_DEBUG=${VK_LOADER_DEBUG:-error,warn,info,driver}

[ -x "$PROBE" ] || {
    printf 'missing probe binary: %s\n' "$PROBE" >&2
    exit 1
}

mkdir -p "$OUT"

set +e
VULKAN_POLICY_MODE=implicit-discovery \
VK_LOADER_DEBUG="$LOADER_DEBUG" \
bash "$SCRIPT_DIR/run-zink-with-policy.sh" "$PROBE" \
    >"$OUT/probe.stdout" \
    2>"$OUT/probe.stderr"
status=$?
set -e

printf '%s\n' "$status" >"$OUT/exit-status"

awk '
    /Vulkan Loader/ ||
    /DRIVER/ ||
    /driver/ ||
    /manifest/ ||
    /\.json/ ||
    /\.so/ ||
    /failed/ ||
    /ERROR/ ||
    /WARNING/ {
        print
    }
' "$OUT/probe.stderr" \
    >"$OUT/loader-driver-summary.txt"

printf 'implicit loader debug capture: PASS\n'
printf 'workload exit status: %s\n' "$status"
printf 'output: %s\n' "$OUT"

printf '\n===== probe stdout =====\n'
cat "$OUT/probe.stdout"

printf '\n===== probe stderr =====\n'
cat "$OUT/probe.stderr"

printf '\n===== loader/driver summary =====\n'
cat "$OUT/loader-driver-summary.txt"
