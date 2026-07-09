#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ARTIFACT=${1:-$HOME/uv-base/cpython-3.14-aarch64-linux-android-for-uv.tar.gz}
EXPECTED=7083ad89661d73278c2165dfff7506a6de26c8ec9471d6621a5c06c3aa9a49be

[ -f "$ARTIFACT" ] || { echo "missing artifact: $ARTIFACT" >&2; exit 1; }
actual=$(sha256sum "$ARTIFACT" | awk '{print $1}')
[ "$actual" = "$EXPECTED" ] || {
  echo "artifact SHA-256 mismatch" >&2
  echo "expected: $EXPECTED" >&2
  echo "actual:   $actual" >&2
  exit 1
}

printf 'cpython artifact validation: PASS\n'
