#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"; TMP=$(mktemp -d "$TMP_BASE/freetype-provider-smoke.XXXXXX")
trap 'chmod -R u+w "$TMP" 2>/dev/null || true; rm -rf "$TMP"' EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
TND_SKIP_GENERATED_DRIFT=1 bash "$TMP/tools/docs/check-freetype-bounded-provider-authority" >/dev/null
python3 - "$TMP" <<'PY'
from pathlib import Path
import csv,sys
p=Path(sys.argv[1])/'experiments/glibc/selected-obsidian-provider-authority/review/freetype-bounded-provider-authority.tsv'
with p.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0])
rows[0]['project_owned_adaptation_boundary']='EXTRA_CONFIGURE_ARGS_ENABLE_UNREVIEWED_RUNTIME_FEATURE'
with p.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
PY
if TND_SKIP_GENERATED_DRIFT=1 bash "$TMP/tools/docs/check-freetype-bounded-provider-authority" >/dev/null 2>&1; then
 echo 'freetype-provider-smoke: FAIL: widened configure semantics accepted' >&2; exit 1
fi
echo 'freetype-provider-smoke: PASS'
