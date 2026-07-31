#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
TREE=$(git -C "$ROOT" write-tree)
TMP=$(mktemp -d -p "$(dirname "$ROOT")" production-exact-input-review.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
git -C "$ROOT" archive "$TREE" | tar -xf - -C "$TMP"
CHECK="$TMP/tools/docs/check-selected-provider-local-supply-live-authority-transaction-production-exact-input-set-correction-bootstrap-review"
REVIEW="$TMP/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-production-exact-input-set-correction-bootstrap-review.tsv"
MEMBERS="$TMP/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-production-exact-input-set-correction-bootstrap-provider-members.tsv"
python3 "$CHECK" >/dev/null
cp "$REVIEW" "$REVIEW.orig"; cp "$MEMBERS" "$MEMBERS.orig"
python3 - "$REVIEW" <<'PY1'
import csv,sys
from pathlib import Path
p=Path(sys.argv[1])
with p.open(newline='',encoding='utf-8') as h: rows=list(csv.DictReader(h,delimiter='\t'))
rows[0]['consumed_transaction_count']='0'; rows[0]['remaining_transaction_count']='1'
with p.open('w',newline='',encoding='utf-8') as h:
 w=csv.DictWriter(h,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
PY1
if python3 "$CHECK" >/dev/null 2>&1; then echo 'owner accounting mutation accepted' >&2; exit 1; fi
mv "$REVIEW.orig" "$REVIEW"
python3 - "$MEMBERS" <<'PY2'
import csv,sys
from pathlib import Path
p=Path(sys.argv[1])
with p.open(newline='',encoding='utf-8') as h: rows=list(csv.DictReader(h,delimiter='\t'))
rows[0]['aarch64']='NO'
with p.open('w',newline='',encoding='utf-8') as h:
 w=csv.DictWriter(h,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
PY2
if python3 "$CHECK" >/dev/null 2>&1; then echo 'ELF mutation accepted' >&2; exit 1; fi
mv "$MEMBERS.orig" "$MEMBERS"
python3 - "$REVIEW" <<'PY3'
import csv,sys
from pathlib import Path
p=Path(sys.argv[1])
with p.open(newline='',encoding='utf-8') as h: rows=list(csv.DictReader(h,delimiter='\t'))
rows[0]['selected_provider_live_open_count']='1'
with p.open('w',newline='',encoding='utf-8') as h:
 w=csv.DictWriter(h,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
PY3
if python3 "$CHECK" >/dev/null 2>&1; then echo 'live provider authority mutation accepted' >&2; exit 1; fi
echo 'production exact input-set bootstrap review smoke: PASS'
