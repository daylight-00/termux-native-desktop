#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
"$ROOT/tools/docs/check-fribidi-bounded-provider-authority"
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
TMP=$(mktemp -d "$TMP_BASE/fribidi-provider-smoke.XXXXXX")
trap 'rm -rf "$TMP"' EXIT
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
python3 - "$TMP" <<'PY'
from pathlib import Path
import csv
import sys

p = Path(sys.argv[1]) / 'experiments/glibc/selected-obsidian-provider-authority/review/fribidi-bounded-provider-authority.tsv'
with p.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='\t')
    fields = reader.fieldnames
    rows = list(reader)
rows[0]['project_owned_adaptation_boundary'] = 'CUSTOM_TERMUX_STEP_MATERIAL_RUNTIME_PATCH'
with p.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
PY
if "$TMP/tools/docs/check-fribidi-bounded-provider-authority" >/dev/null 2>&1; then
  echo 'fribidi smoke: semantic widening mutation accepted' >&2
  exit 1
fi
echo 'fribidi smoke: PASS'
