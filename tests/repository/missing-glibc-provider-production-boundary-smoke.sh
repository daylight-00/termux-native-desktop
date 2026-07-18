#!/usr/bin/env bash
set -euo pipefail
ROOT=${1:-$(git rev-parse --show-toplevel)}
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
TMP=$(mktemp -d "$TMP_BASE/missing-provider-production-boundary-smoke.XXXXXX"); trap 'rm -rf "$TMP"' EXIT
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
"$TMP/tools/docs/check-missing-glibc-provider-production-boundary" >/dev/null
python3 - "$TMP" <<'PY2'
from pathlib import Path
p=Path(__import__('sys').argv[1])/'experiments/glibc/selected-obsidian-provider-authority/review/missing-glibc-provider-production-boundary.tsv'
p.write_text(p.read_text().replace('NO_BUILD_AUTHORIZATION','AUTHORIZED_FOR_BUILD'))
PY2
if "$TMP/tools/docs/check-missing-glibc-provider-production-boundary" >/dev/null 2>&1; then
 echo 'missing-provider-production-boundary-smoke: FAIL: libSELinux build widening was accepted' >&2; exit 1
fi
echo 'missing-provider-production-boundary-smoke: PASS: libSELinux build widening is rejected'
