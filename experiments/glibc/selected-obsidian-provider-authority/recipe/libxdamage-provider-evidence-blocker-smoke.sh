#!/usr/bin/env bash
set -euo pipefail
ROOT=${1:-$(git rev-parse --show-toplevel)}
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
TMP=$(mktemp -d "$TMP_BASE/libxdamage-blocker-smoke.XXXXXX"); trap 'rm -rf "$TMP"' EXIT
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
"$TMP/tools/docs/check-libxdamage-provider-evidence-blocker" >/dev/null
python3 - "$TMP" <<'PY2'
from pathlib import Path
p=Path(__import__('sys').argv[1])/'experiments/glibc/selected-obsidian-provider-authority/review/libxdamage-provider-evidence-blocker.tsv'
s=p.read_text().replace('OPEN_BLOCKED_NO_GLIBC_CANDIDATE','ACCEPTED_BOUNDED_PROVIDER')
p.write_text(s)
PY2
if "$TMP/tools/docs/check-libxdamage-provider-evidence-blocker" >/dev/null 2>&1; then
 echo 'libxdamage-blocker-smoke: FAIL: authority widening was accepted' >&2; exit 1
fi
echo 'libxdamage-blocker-smoke: PASS: authority widening is rejected'
