#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
EXPERIMENT_DIR=$(cd -- "$SCRIPT_DIR/.." && pwd)
WORK_DIR=${WORK_DIR:-$EXPERIMENT_DIR/work}
PROBE=${PROBE:-$WORK_DIR/dbus-version-probe}
FARM=${FARM:-$HOME/gl/lib}
LOADER=${LOADER:-$PREFIX/glibc/lib/ld-linux-aarch64.so.1}
OUT=${OUT:-$PREFIX/tmp/selected-dbus-control-$(date +%Y%m%d-%H%M%S)}
HOLD_SECONDS=${HOLD_SECONDS:-20}

mkdir -p "$OUT"

[ -x "$PROBE" ] || "$SCRIPT_DIR/build-probe.sh"
[ -x "$LOADER" ] || { printf 'missing loader: %s\n' "$LOADER" >&2; exit 1; }
[ -e "$FARM/libdbus-1.so.3" ] || { printf 'missing control libdbus\n' >&2; exit 1; }

ROOT_PROVIDER=$(readlink -f "$FARM/libdbus-1.so.3")
CONTROL_LIBRARY_PATH="$FARM:$PREFIX/glibc/lib"

printf 'output: %s\n' "$OUT"

{
    printf '===== substrate package =====\n'
    dpkg-query -W -f='${binary:Package}\t${Version}\t${Architecture}\n' glibc

    printf '\n===== libc identity =====\n'
    sha256sum "$PREFIX/glibc/lib/libc.so.6"
    readelf -n "$PREFIX/glibc/lib/libc.so.6" | grep -A1 -B1 'Build ID' || true
} >"$OUT/substrate-identity.txt"

{
    printf 'resolved root provider: %s\n' "$ROOT_PROVIDER"
    file "$ROOT_PROVIDER"
    sha256sum "$ROOT_PROVIDER"
    readelf -n "$ROOT_PROVIDER" | grep -A1 -B1 'Build ID' || true
    readelf -d "$ROOT_PROVIDER" | grep NEEDED || true
} >"$OUT/root-provider-identity.txt"

{
    printf '===== probe ldd =====\n'
    env \
        LD_PRELOAD= \
        LD_LIBRARY_PATH="$CONTROL_LIBRARY_PATH" \
        "$PREFIX/glibc/bin/ldd" -r "$PROBE"

    printf '\n===== root provider ldd =====\n'
    env \
        LD_PRELOAD= \
        LD_LIBRARY_PATH="$CONTROL_LIBRARY_PATH" \
        "$PREFIX/glibc/bin/ldd" -r "$ROOT_PROVIDER"
} >"$OUT/control-ldd.txt" 2>&1

printf '\n===== start control probe =====\n'

DBUS_PROBE_HOLD_SECONDS=$HOLD_SECONDS \
LD_DEBUG=libs,files \
LD_PRELOAD= \
"$LOADER" \
    --library-path "$CONTROL_LIBRARY_PATH" \
    "$PROBE" \
    >"$OUT/probe.stdout" \
    2>"$OUT/loader-debug.log" &
PROBE_PID=$!

printf 'pid: %s\n' "$PROBE_PID" | tee "$OUT/probe.pid"

for _ in $(seq 1 40); do
    if [ -r "/proc/$PROBE_PID/maps" ]; then
        break
    fi
    sleep 0.25
done

if [ ! -r "/proc/$PROBE_PID/maps" ]; then
    printf 'probe maps not readable before process exit\n' >&2
    wait "$PROBE_PID" || true
    exit 1
fi

cat "/proc/$PROBE_PID/maps" >"$OUT/maps.txt"

set +e
wait "$PROBE_PID"
STATUS=$?
set -e
printf '%s\n' "$STATUS" >"$OUT/probe.status"

if [ "$STATUS" -ne 0 ]; then
    printf 'control probe failed with status %s\n' "$STATUS" >&2
    exit "$STATUS"
fi

printf '\n===== probe output =====\n'
cat "$OUT/probe.stdout"

printf '\n===== mapped provider-relevant objects =====\n'
grep -E '/gl/lib/|/glibc/lib/|/proot-distro/.*/rootfs/' "$OUT/maps.txt" \
    | awk '{print $NF}' \
    | sort -u \
    | tee "$OUT/mapped-objects.txt"

printf '\ncontrol capture: PASS\n'
printf 'evidence: %s\n' "$OUT"
