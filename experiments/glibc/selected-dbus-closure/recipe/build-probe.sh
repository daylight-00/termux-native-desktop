#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
EXPERIMENT_DIR=$(cd -- "$SCRIPT_DIR/.." && pwd)
WORK_DIR=${WORK_DIR:-$EXPERIMENT_DIR/work}
PROBE=${PROBE:-$WORK_DIR/dbus-version-probe}
SOURCE=$SCRIPT_DIR/probe.c
FARM=${FARM:-$HOME/gl/lib}

mkdir -p "$WORK_DIR"

for command in glibc-gcc readelf file; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

DBUS_LINK=$FARM/libdbus-1.so.3
[ -e "$DBUS_LINK" ] || {
    printf 'missing control provider: %s\n' "$DBUS_LINK" >&2
    exit 1
}

printf 'building probe: %s\n' "$PROBE"

glibc-gcc \
    -O2 \
    -Wall \
    -Wextra \
    -Werror \
    -o "$PROBE" \
    "$SOURCE" \
    "$DBUS_LINK" \
    -Wl,-rpath-link,"$FARM"

printf '\n===== probe identity =====\n'
file "$PROBE"
sha256sum "$PROBE"

DYNAMIC=$(mktemp)
trap 'rm -f "$DYNAMIC"' EXIT
readelf -d "$PROBE" >"$DYNAMIC"

printf '\n===== probe dynamic section =====\n'
grep -E 'NEEDED|RPATH|RUNPATH' "$DYNAMIC" || true

if grep -qE '\((RPATH|RUNPATH)\)' "$DYNAMIC"; then
    printf 'probe must not embed control farm RPATH/RUNPATH\n' >&2
    exit 1
fi

printf '\nprobe build: PASS\n'
