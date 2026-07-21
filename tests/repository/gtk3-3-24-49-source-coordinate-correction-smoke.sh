#!/usr/bin/env bash
set -euo pipefail
ROOT=${1:-$(git rev-parse --show-toplevel)}
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
TMP=$(mktemp -d "$TMP_BASE/gtk3-source-coordinate.XXXXXX"); trap 'rm -rf "$TMP"' EXIT
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
"$TMP/tools/docs/check-gtk3-3-24-49-source-coordinate-correction" >/dev/null
python3 - "$TMP" <<'PY2'
from pathlib import Path
root=Path(__import__('sys').argv[1])
p=root/'docs/current/ACTIVE_TASK.md'
p.write_text(p.read_text().replace('198aeace1e9e119c77f4d669bd8efdf337828ad1','7a7e86ecab67e7cf65f066dae2e02ae74d653ced'))
PY2
if "$TMP/tools/docs/check-gtk3-3-24-49-source-coordinate-correction" >/dev/null 2>&1; then
 echo 'gtk3-source-coordinate-smoke: FAIL: stale commit restoration was accepted' >&2; exit 1
fi
rm -rf "$TMP"; TMP=$(mktemp -d "$TMP_BASE/gtk3-source-coordinate.XXXXXX")
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
python3 - "$TMP" <<'PY2'
from pathlib import Path
root=Path(__import__('sys').argv[1])
p=root/'experiments/glibc/selected-obsidian-provider-authority/review/gtk3-3-24-49-source-coordinate-correction.tsv'
p.write_text(p.read_text().replace('NO_COMPOSITION_EFFECT_THREE_GAPS_RETAINED','COMPOSITION_ACCEPTED'))
PY2
if "$TMP/tools/docs/check-gtk3-3-24-49-source-coordinate-correction" >/dev/null 2>&1; then
 echo 'gtk3-source-coordinate-smoke: FAIL: composition widening was accepted' >&2; exit 1
fi
echo 'gtk3-source-coordinate-smoke: PASS: stale source restoration and authority widening are rejected'
