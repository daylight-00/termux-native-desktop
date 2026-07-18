#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
"$ROOT/tools/docs/check-cairo-bounded-provider-authority" >/dev/null
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
TMP=$(mktemp -d "$TMP_BASE/cairo-provider-smoke.XXXXXX")
cleanup(){ chmod -R u+w "$TMP" 2>/dev/null || true; rm -rf "$TMP"; }; trap cleanup EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
python3 - "$TMP" <<'PY2'
from pathlib import Path
import csv,sys
p=Path(sys.argv[1])/'experiments/glibc/selected-obsidian-provider-authority/review/cairo-bounded-provider-authority.tsv'
with p.open(newline='',encoding='utf-8') as f:r=csv.DictReader(f,delimiter='	'); fields=r.fieldnames; rows=list(r)
rows[0]['candidate_conflict_and_exclusion_result']='PACKAGE_WIDE_AUTHORITY_ACCEPTED;CAIRO_SCRIPT_INTERPRETER_AUTHORITY_ACCEPTED;COMPLETE_COMPOSITION_ACCEPTED;TARGET_POPULATION_ACCEPTED;ACTIVATION_ACCEPTED;UPSTREAM_BYTE_EQUIVALENCE_ACCEPTED'
with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields,delimiter='	',lineterminator='\n');w.writeheader();w.writerows(rows)
PY2
if "$TMP/tools/docs/check-cairo-bounded-provider-authority" >/dev/null 2>&1; then echo 'cairo-provider-smoke: FAIL: widened Cairo/package/utility/composition authority accepted' >&2; exit 1; fi
echo 'cairo-provider-smoke: PASS'
