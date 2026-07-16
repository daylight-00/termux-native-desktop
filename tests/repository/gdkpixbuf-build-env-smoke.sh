#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP=${TND_TEST_TMPDIR:-$(mktemp -d)}
CASE="$TMP/repo"
BACKUP="$TMP/backup"
mkdir -p "$CASE" "$BACKUP"
git -C "$ROOT" archive HEAD | tar -x -C "$CASE"
for rel in \
  packages/gdkpixbuf-glibc/build-env/pyproject.toml \
  packages/gdkpixbuf-glibc/build-env/uv.lock \
  packages/gdkpixbuf-glibc/README.md; do
  mkdir -p "$BACKUP/$(dirname "$rel")"
  cp "$CASE/$rel" "$BACKUP/$rel"
done

"$CASE/tools/docs/check-gdkpixbuf-build-env" >/dev/null

expect_fail() {
  local label=$1 rel=$2
  if "$CASE/tools/docs/check-gdkpixbuf-build-env" >/dev/null 2>&1; then
    echo "expected failure: $label" >&2
    exit 1
  fi
  cp "$BACKUP/$rel" "$CASE/$rel"
}

python3 - "$CASE/packages/gdkpixbuf-glibc/build-env/pyproject.toml" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text(); s=s.replace('    "meson==1.11.1",\n', '    "meson==1.11.1",\n    "ninja==1.13.0",\n'); p.write_text(s)
PY
expect_fail "binary Ninja added to uv project" packages/gdkpixbuf-glibc/build-env/pyproject.toml

sed -i 's/meson-1.11.1-py3-none-any.whl/meson-1.11.1-manylinux_aarch64.whl/' "$CASE/packages/gdkpixbuf-glibc/build-env/uv.lock"
expect_fail "Meson wheel loses pure-Python tag" packages/gdkpixbuf-glibc/build-env/uv.lock

sed -i 's/Ninja remains a native Termux host/Ninja moves into the uv environment/' "$CASE/packages/gdkpixbuf-glibc/README.md"
expect_fail "package boundary moves Ninja into uv" packages/gdkpixbuf-glibc/README.md

printf 'gdkpixbuf build env smoke: PASS\n'
