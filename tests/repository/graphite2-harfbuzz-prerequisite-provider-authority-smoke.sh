#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
"$ROOT/tools/docs/check-graphite2-harfbuzz-prerequisite-provider-authority" >/dev/null
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
TMP=$(mktemp -d "$TMP_BASE/graphite2-harfbuzz-prerequisite-smoke.XXXXXX")
cleanup(){ chmod -R u+w "$TMP" 2>/dev/null || true; rm -rf "$TMP"; }; trap cleanup EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
python3 - "$TMP" <<'PY'
from pathlib import Path
import csv,sys
p=Path(sys.argv[1])/'experiments/glibc/selected-obsidian-provider-authority/review/graphite2-harfbuzz-prerequisite-provider-authority.tsv'
with p.open(newline='',encoding='utf-8') as f:r=csv.DictReader(f,delimiter='\t'); fields=r.fieldnames; rows=list(r)
rows[0]['candidate_conflict_and_exclusion_result']='UPSTREAM_BYTE_EQUIVALENCE_ACCEPTED;PERFORMANCE_EQUIVALENCE_ACCEPTED;ALL_GRAPHITE_FONTS_FUNCTIONALLY_VALIDATED_ACCEPTED;HARFBUZZ_PROVIDER_WIDENING_ACCEPTED;PACKAGE_WIDE_AUTHORITY_ACCEPTED;TARGET_POPULATION_ACCEPTED;ACTIVATION_ACCEPTED'
with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
PY
if "$TMP/tools/docs/check-graphite2-harfbuzz-prerequisite-provider-authority" >/dev/null 2>&1; then
  echo 'graphite2-harfbuzz-prerequisite-smoke: FAIL: widened Graphite2/HarfBuzz/package/functional/target authority accepted' >&2
  exit 1
fi
echo 'graphite2-harfbuzz-prerequisite-smoke: PASS'
