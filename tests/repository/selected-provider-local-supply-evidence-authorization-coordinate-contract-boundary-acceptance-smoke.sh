#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
F=$(mktemp -d "$TMP_BASE/local-supply-auth-coordinate-acceptance.XXXXXX")
trap 'rm -rf "$F"' EXIT
git -C "$ROOT" archive HEAD | tar -xf - -C "$F"
CHECK="$F/tools/docs/check-selected-provider-local-supply-evidence-authorization-coordinate-contract-boundary-acceptance"
ACC="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-coordinate-contract-boundary-acceptance.tsv"
TOKEN="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-owner-authorization-token-schema.json"
COORD="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-coordinate-receipt-schema.json"
python3 "$CHECK" >/dev/null
sed -i 's/NOT_ISSUED_SEPARATE_OWNER_DECISION_AND_TRANSACTION_REQUIRED/ISSUED/' "$ACC"
if python3 "$CHECK" >/dev/null 2>&1; then echo 'live token issuance widening accepted' >&2; exit 1; fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-coordinate-contract-boundary-acceptance.tsv > "$ACC"
python3 - "$TOKEN" <<'PYINNER'
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);d=json.loads(p.read_text());d['current_token_count']=1;d['current_token']={'fabricated':True};p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PYINNER
if python3 "$CHECK" >/dev/null 2>&1; then echo 'candidate live token accepted' >&2; exit 1; fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-owner-authorization-token-schema.json > "$TOKEN"
python3 - "$COORD" <<'PYINNER'
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);d=json.loads(p.read_text());d['current_receipt_count']=1;d['current_coordinate_row_count']=1;d['current_rows']=[{'fabricated':True}];p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PYINNER
if python3 "$CHECK" >/dev/null 2>&1; then echo 'candidate live coordinate accepted' >&2; exit 1; fi
echo 'selected-provider local-supply authorization/coordinate contract boundary acceptance smoke: PASS'
