#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

[ "${1:-}" = "--yes" ] || {
    echo "usage: $0 --yes" >&2
    echo "removes the generated uv-base .venv and recreates it from the lockfile" >&2
    exit 2
}

UV_BASE=${UV_BASE:-$HOME/uv-base}
rm -rf "$UV_BASE/.venv"
exec "$(dirname "$0")/sync.sh"
