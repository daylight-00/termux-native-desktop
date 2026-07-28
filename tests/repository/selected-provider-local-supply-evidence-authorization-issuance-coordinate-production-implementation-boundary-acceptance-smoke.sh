#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
F=$(mktemp -d "$TMP_BASE/local-supply-implementation-acceptance.XXXXXX")
trap 'rm -rf "$F"' EXIT
git -C "$ROOT" archive HEAD | tar -xf - -C "$F"
CHECK="$F/tools/docs/check-selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-boundary-acceptance"
ACC="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-boundary-acceptance.tsv"
META="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-metadata.tsv"
SUCCESS="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-synthetic-success.json"
python3 "$CHECK" >/dev/null
python3 - "$ACC" <<'PYACC'
import csv,sys
from pathlib import Path
p=Path(sys.argv[1])
with p.open(newline='',encoding='utf-8') as f:
 rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0])
rows[0]['owner_authorization_issuance_state']='AUTHORIZED'
with p.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
PYACC
if python3 "$CHECK" >/dev/null 2>&1; then echo 'owner issuance widening accepted' >&2; exit 1; fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-boundary-acceptance.tsv > "$ACC"
sed -i 's/current_live_authority_count	0/current_live_authority_count	1/' "$META"
if python3 "$CHECK" >/dev/null 2>&1; then echo 'candidate live authority accepted' >&2; exit 1; fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-metadata.tsv > "$META"
python3 - "$SUCCESS" <<'PYINNER'
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);d=json.loads(p.read_text());d['current_provider_read_count']=1;p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PYINNER
if python3 "$CHECK" >/dev/null 2>&1; then echo 'provider-read widening accepted' >&2; exit 1; fi
echo 'selected-provider local-supply issuance/coordinate implementation boundary acceptance smoke: PASS'
