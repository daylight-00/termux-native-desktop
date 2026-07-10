#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

LIBC=${LIBC:-$PREFIX/glibc/lib/libc.so.6}
[ -r "$LIBC" ] || { echo "missing libc: $LIBC" >&2; exit 1; }

symbols=$(mktemp)
trap 'rm -f "$symbols"' EXIT

readelf --dyn-syms --wide "$LIBC" >"$symbols"

if grep -qE '[[:space:]]__vsyslog_chk(@@|@)GLIBC_2\.17([[:space:]]|$)' "$symbols"; then
    printf 'glibc core ABI: PASS (__vsyslog_chk@GLIBC_2.17 exported)\n'
else
    printf 'glibc core ABI: FAIL\n' >&2
    printf 'missing export: __vsyslog_chk@GLIBC_2.17\n' >&2
    printf 'libc: %s\n' "$LIBC" >&2
    exit 1
fi
