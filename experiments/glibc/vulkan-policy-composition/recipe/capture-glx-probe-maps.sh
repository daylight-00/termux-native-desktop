#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
MODE=${VULKAN_POLICY_MODE:-explicit-freedreno}
PROBE=${PROBE:-$PREFIX/tmp/tnd-vulkan-policy-composition/glx-renderer-probe}
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/maps-$MODE-$(date +%Y%m%d-%H%M%S)}
HOLD_SECONDS=${PROBE_HOLD_SECONDS:-15}

[ -x "$PROBE" ] || {
    printf 'missing probe binary: %s\n' "$PROBE" >&2
    exit 1
}

mkdir -p "$OUT"

cleanup() {
    if [ -n "${pid:-}" ] && kill -0 "$pid" 2>/dev/null; then
        kill "$pid" 2>/dev/null || true
        wait "$pid" 2>/dev/null || true
    fi
}
trap cleanup EXIT

PROBE_HOLD_SECONDS="$HOLD_SECONDS" \
VULKAN_POLICY_MODE="$MODE" \
bash "$SCRIPT_DIR/run-zink-with-policy.sh" "$PROBE" \
    >"$OUT/probe.stdout" \
    2>"$OUT/probe.stderr" &
pid=$!
printf '%s\n' "$pid" >"$OUT/pid"

ready=0
for _ in $(seq 1 100); do
    if grep -q '^GL_RENDERER=' "$OUT/probe.stdout" 2>/dev/null; then
        ready=1
        break
    fi

    if ! kill -0 "$pid" 2>/dev/null; then
        break
    fi

    sleep 0.1
done

if [ "$ready" -ne 1 ]; then
    printf 'probe did not reach renderer identity gate\n' >&2
    printf '\n===== stdout =====\n' >&2
    cat "$OUT/probe.stdout" >&2 || true
    printf '\n===== stderr =====\n' >&2
    cat "$OUT/probe.stderr" >&2 || true
    exit 1
fi

cp "/proc/$pid/maps" "$OUT/maps.txt"

awk '
    $6 ~ /^\// {
        print $6
    }
' "$OUT/maps.txt" \
    | sort -u \
    >"$OUT/mapped-paths.raw.txt"

: >"$OUT/mapped-paths.real.txt"
while IFS= read -r path; do
    [ -n "$path" ] || continue
    realpath -e "$path" 2>/dev/null || printf '%s\n' "$path"
done <"$OUT/mapped-paths.raw.txt" \
    | sort -u \
    >"$OUT/mapped-paths.real.txt"

awk '
    /libGL(X|dispatch|\.so)/ ||
    /zink/ ||
    /vulkan/ ||
    /mesa/ ||
    /dri/ ||
    /libdrm/ ||
    /kgsl/ {
        print
    }
' "$OUT/mapped-paths.real.txt" \
    >"$OUT/graphics-related-paths.txt"

wait "$pid"
pid=
trap - EXIT

printf 'GLX probe maps capture: PASS\n'
printf 'mode: %s\n' "$MODE"
printf 'output: %s\n' "$OUT"

printf '\n===== probe stdout =====\n'
cat "$OUT/probe.stdout"

printf '\n===== probe stderr =====\n'
cat "$OUT/probe.stderr"

printf '\n===== graphics-related mapped paths =====\n'
cat "$OUT/graphics-related-paths.txt"
