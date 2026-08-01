#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
TREE=$(git -C "$ROOT" write-tree)
TMP=$(mktemp -d -p "$(dirname "$ROOT")" map-production-review.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
git -C "$ROOT" archive "$TREE" | tar -xf - -C "$TMP"
CHECK="$TMP/tools/docs/check-selected-provider-local-supply-map-production-review"
MAP="$TMP/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-production-candidate.json"
REVIEW="$TMP/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-production-review.tsv"
python3 "$CHECK" >/dev/null
cp "$MAP" "$MAP.orig"
python3 - "$MAP" <<'PY1'
import json,sys
p=sys.argv[1];d=json.load(open(p));d['rows'][0]['st_size']+=1
open(p,'w').write(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PY1
if python3 "$CHECK" >/dev/null 2>&1; then echo 'map mutation accepted' >&2; exit 1; fi
mv "$MAP.orig" "$MAP"
cp "$REVIEW" "$REVIEW.orig"
python3 - "$REVIEW" <<'PY2'
import csv,sys
p=sys.argv[1]
with open(p,newline='') as h:r=list(csv.DictReader(h,delimiter='\t'))
r[0]['remaining_transaction_count']='1'
with open(p,'w',newline='') as h:w=csv.DictWriter(h,fieldnames=r[0].keys(),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(r)
PY2
if python3 "$CHECK" >/dev/null 2>&1; then echo 'owner accounting mutation accepted' >&2; exit 1; fi
mv "$REVIEW.orig" "$REVIEW"
python3 "$CHECK" >/dev/null
echo 'local-supply map production review smoke: PASS'
