#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
F=$(mktemp -d "$TMP_BASE/local-supply-issuance-production-design.XXXXXX")
trap 'rm -rf "$F"' EXIT
git -C "$ROOT" archive HEAD | tar -xf - -C "$F"
CHECK="$F/tools/docs/check-selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-review"
META="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-metadata.tsv"
RECEIPT="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-receipt-contract.json"
python3 "$CHECK" >/dev/null
sed -i 's/current_issued_token_count	0/current_issued_token_count	1/' "$META"
if python3 "$CHECK" >/dev/null 2>&1; then echo 'live token widening accepted' >&2; exit 1; fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-metadata.tsv > "$META"
sed -i 's/provider_byte_read_authorized	NO/provider_byte_read_authorized	YES/' "$META"
if python3 "$CHECK" >/dev/null 2>&1; then echo 'provider read widening accepted' >&2; exit 1; fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-metadata.tsv > "$META"
python3 - "$RECEIPT" <<'PYINNER'
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);d=json.loads(p.read_text());d['current_coordinate_row_count']=41;d['current_outputs']=[{'fabricated':True}];p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PYINNER
if python3 "$CHECK" >/dev/null 2>&1; then echo 'live coordinate output accepted' >&2; exit 1; fi
echo 'selected-provider authorization issuance/coordinate production design smoke: PASS'
