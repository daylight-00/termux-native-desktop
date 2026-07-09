#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

BASE=${1:-$HOME/uv-base}
EXPECTED_PROJECT=2b89a3855976ca27d81f7bda0c42b7880b52e6b74fae41c83982d115576b4355
EXPECTED_LOCK=79dab5fa4e9246ccfd72c28d569400013858723730f599a15ef6e6f566635a53

project=$(sha256sum "$BASE/pyproject.toml" | awk '{print $1}')
lock=$(sha256sum "$BASE/uv.lock" | awk '{print $1}')
[ "$project" = "$EXPECTED_PROJECT" ] || { echo "pyproject identity mismatch" >&2; exit 1; }
[ "$lock" = "$EXPECTED_LOCK" ] || { echo "lock identity mismatch" >&2; exit 1; }
printf 'uv-base definition validation: PASS\n'
