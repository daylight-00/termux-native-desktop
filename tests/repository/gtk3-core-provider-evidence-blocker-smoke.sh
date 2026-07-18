#!/usr/bin/env bash
set -euo pipefail
ROOT=${1:-$(git rev-parse --show-toplevel)}
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
TMP=$(mktemp -d "$TMP_BASE/gtk3-core-blocker-smoke.XXXXXX"); trap 'rm -rf "$TMP"' EXIT
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
"$TMP/tools/docs/check-gtk3-core-provider-evidence-blocker" >/dev/null
python3 - "$TMP" <<'PY2'
from pathlib import Path
p=Path(__import__('sys').argv[1])/'experiments/glibc/selected-obsidian-provider-authority/review/gtk3-core-provider-evidence-blocker.tsv'
p.write_text(p.read_text().replace('OPEN_BLOCKED_NO_GLIBC_CANDIDATE','ACCEPTED_BOUNDED_PROVIDER'))
PY2
if "$TMP/tools/docs/check-gtk3-core-provider-evidence-blocker" >/dev/null 2>&1; then
 echo 'gtk3-core-blocker-smoke: FAIL: authority widening was accepted' >&2; exit 1
fi
echo 'gtk3-core-blocker-smoke: PASS: authority widening is rejected'
