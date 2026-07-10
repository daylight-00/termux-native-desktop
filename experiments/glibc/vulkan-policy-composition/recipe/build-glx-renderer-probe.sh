#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SOURCE="$SCRIPT_DIR/glx-renderer-probe.c"
OUT_DIR=${OUT_DIR:-$PREFIX/tmp/tnd-vulkan-policy-composition}
BINARY=${BINARY:-$OUT_DIR/glx-renderer-probe}
CC=${CC:-$HOME/gl/toolchain/glibc-gcc}

[ -f "$SOURCE" ] || {
    printf 'missing probe source: %s\n' "$SOURCE" >&2
    exit 1
}

[ -x "$CC" ] || {
    printf 'missing glibc compiler wrapper: %s\n' "$CC" >&2
    exit 1
}

mkdir -p "$OUT_DIR"

"$CC" \
    -std=c11 \
    -O2 \
    -Wall \
    -Wextra \
    "$SOURCE" \
    -o "$BINARY" \
    -ldl

printf 'GLX renderer probe build: PASS\n'
printf 'binary: %s\n' "$BINARY"

printf '\n===== interpreter =====\n'
readelf -l "$BINARY" \
    | grep -F 'Requesting program interpreter' \
    || true

printf '\n===== NEEDED =====\n'
readelf -d "$BINARY" \
    | grep '(NEEDED)' \
    || true
