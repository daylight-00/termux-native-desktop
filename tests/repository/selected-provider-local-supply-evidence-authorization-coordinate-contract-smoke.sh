#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
F=$(mktemp -d "$TMP_BASE/local-supply-auth-coordinate.XXXXXX")
trap 'rm -rf "$F"' EXIT
git -C "$ROOT" archive HEAD | tar -xf - -C "$F"
CHECK="$F/tools/docs/check-selected-provider-local-supply-evidence-authorization-coordinate-contract-review"
TOKEN="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-owner-authorization-token-schema.json"
COORD="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-coordinate-receipt-schema.json"
META="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-coordinate-contract-metadata.tsv"
python3 "$CHECK" >/dev/null
python3 - "$TOKEN" <<'PY'
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);d=json.loads(p.read_text());d['current_token_count']=1;d['current_token']={'authorization_token_id':'fabricated'};p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PY
if python3 "$CHECK" >/dev/null 2>&1; then echo 'live token unexpectedly accepted' >&2; exit 1; fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-owner-authorization-token-schema.json > "$TOKEN"
python3 - "$COORD" <<'PY'
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);d=json.loads(p.read_text());d['current_coordinate_row_count']=1;d['current_rows']=[{'contract_row_id':'LSM-CONTRACT-001','absolute_canonical_path':'/fabricated'}];p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PY
if python3 "$CHECK" >/dev/null 2>&1; then echo 'live coordinate unexpectedly accepted' >&2; exit 1; fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-coordinate-receipt-schema.json > "$COORD"
sed -i 's/evidence_transaction_execution_authorized\tNO/evidence_transaction_execution_authorized\tYES/' "$META"
if python3 "$CHECK" >/dev/null 2>&1; then echo 'execution widening unexpectedly accepted' >&2; exit 1; fi
echo 'selected-provider local-supply evidence authorization/coordinate contract smoke: PASS'
