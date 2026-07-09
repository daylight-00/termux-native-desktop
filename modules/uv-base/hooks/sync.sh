#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

UV_BASE=${UV_BASE:-$HOME/uv-base}
PYBIN=${PYBIN:-$HOME/opt/cpython-3.14/prefix/bin/python3.14}

command -v uv >/dev/null 2>&1 || { echo 'uv is not on PATH' >&2; exit 1; }
[ -x "$PYBIN" ] || { echo "missing interpreter: $PYBIN" >&2; exit 1; }
[ -f "$UV_BASE/pyproject.toml" ] || { echo "missing project definition" >&2; exit 1; }
[ -f "$UV_BASE/uv.lock" ] || { echo "missing lockfile" >&2; exit 1; }

exec uv --project "$UV_BASE" \
    sync \
    --locked \
    --no-python-downloads \
    --python "$PYBIN"
