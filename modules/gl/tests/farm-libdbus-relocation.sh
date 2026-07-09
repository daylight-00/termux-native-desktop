#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

DBUS_LINK=${DBUS_LINK:-$HOME/gl/lib/libdbus-1.so.3}
LDD=${LDD:-$PREFIX/glibc/bin/ldd}

[ -e "$DBUS_LINK" ] || { echo "missing farm libdbus: $DBUS_LINK" >&2; exit 1; }
[ -x "$LDD" ] || { echo "missing glibc ldd: $LDD" >&2; exit 1; }

DBUS=$(readlink -f "$DBUS_LINK")
out=$(mktemp)
trap 'rm -f "$out"' EXIT

set +e
env LD_PRELOAD= "$LDD" -r "$DBUS" >"$out" 2>&1
status=$?
set -e

cat "$out"

if grep -q 'undefined symbol:' "$out"; then
    printf 'farm libdbus relocation: FAIL\n' >&2
    exit 1
fi

[ "$status" -eq 0 ] || {
    printf 'farm libdbus relocation: FAIL (ldd status %s)\n' "$status" >&2
    exit "$status"
}

printf 'farm libdbus relocation: PASS\n'
