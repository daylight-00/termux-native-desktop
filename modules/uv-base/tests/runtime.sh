#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

UV_BASE=${UV_BASE:-$HOME/uv-base}
PY="$UV_BASE/.venv/bin/python"
[ -x "$PY" ] || { echo "missing uv-base runtime: $PY" >&2; exit 1; }

version=$($PY --version 2>&1)
case "$version" in
    'Python 3.14.'*) ;;
    *) echo "unexpected uv-base Python: $version" >&2; exit 1 ;;
esac

printf 'uv-base runtime validation: PASS\n'
