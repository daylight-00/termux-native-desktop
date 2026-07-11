#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

export VK_LOADER_DEBUG=${VK_LOADER_DEBUG:-all}

printf 'VK_LOADER_DEBUG=%s\n' "$VK_LOADER_DEBUG" >&2

exec \
    "$SCRIPT_DIR/launch-obsidian-with-policy.sh" \
    "$@"
