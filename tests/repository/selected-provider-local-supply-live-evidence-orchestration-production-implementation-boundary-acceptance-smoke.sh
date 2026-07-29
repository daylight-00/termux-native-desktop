#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-$(dirname "$ROOT")};mkdir -p "$TMP_BASE";F=$(mktemp -d "$TMP_BASE/live-evidence-orchestration-acceptance.XXXXXX");trap 'rm -rf "$F"' EXIT
git -C "$ROOT" archive HEAD | tar -xf - -C "$F"
CHECK="$F/tools/docs/check-selected-provider-local-supply-live-evidence-orchestration-production-implementation-boundary-acceptance"
ACC="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-evidence-orchestration-production-implementation-boundary-acceptance.tsv"
python3 "$CHECK" >/dev/null
python3 - "$ACC" <<'PY2'
import csv,sys
from pathlib import Path
p=Path(sys.argv[1])
with p.open(newline='',encoding='utf-8') as f:
    r=list(csv.DictReader(f,delimiter='\t'));fields=list(r[0])
r[0]['accepted_selected_provider_open_count']='1'
with p.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(r)
PY2
if python3 "$CHECK" >/dev/null 2>&1; then echo 'selected-provider open widening accepted' >&2;exit 1;fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-evidence-orchestration-production-implementation-boundary-acceptance.tsv > "$ACC"
python3 - "$ACC" <<'PY2'
import csv,sys
from pathlib import Path
p=Path(sys.argv[1])
with p.open(newline='',encoding='utf-8') as f:
    r=list(csv.DictReader(f,delimiter='\t'));fields=list(r[0])
r[0]['owner_authorization_issuance_state']='AUTHORIZED'
with p.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(r)
PY2
if python3 "$CHECK" >/dev/null 2>&1; then echo 'live authority widening accepted' >&2;exit 1;fi
echo 'selected-provider local-supply live-evidence orchestration production implementation boundary acceptance smoke: PASS'
