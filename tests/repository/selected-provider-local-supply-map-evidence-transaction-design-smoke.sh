#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
"$ROOT/tools/docs/check-selected-provider-local-supply-map-evidence-transaction-design-review"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
cp -a "$ROOT/." "$TMP/repo"
python3 - "$TMP/repo/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-design-metadata.tsv" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]);p.write_text(p.read_text().replace('evidence_transaction_execution_authorized\tNO','evidence_transaction_execution_authorized\tYES'))
PY
if "$TMP/repo/tools/docs/check-selected-provider-local-supply-map-evidence-transaction-design-review" >/dev/null 2>&1; then echo 'negative authority widening unexpectedly passed' >&2; exit 1; fi
rm -rf "$TMP/repo"; cp -a "$ROOT/." "$TMP/repo"
python3 - "$TMP/repo/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-receipt-contract.json" <<'PY'
from pathlib import Path
import json,sys
p=Path(sys.argv[1]);d=json.loads(p.read_text());d['current_authorized_coordinate_count']=41;p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PY
if "$TMP/repo/tools/docs/check-selected-provider-local-supply-map-evidence-transaction-design-review" >/dev/null 2>&1; then echo 'negative populated coordinate state unexpectedly passed' >&2; exit 1; fi
printf 'selected provider local supply map evidence transaction design smoke: PASS\n'
