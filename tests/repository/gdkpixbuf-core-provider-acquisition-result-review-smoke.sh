#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-/tmp}}
WORK=$(mktemp -d "$TMP_BASE/gdkpixbuf-core-acquisition-smoke.XXXXXX")
cleanup(){ rm -rf "$WORK"; }
trap cleanup EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -x -C "$WORK"
"$WORK/tools/docs/check-gdkpixbuf-core-provider-acquisition-result-review"
python3 - "$WORK" <<'PY'
from pathlib import Path
import csv,sys,subprocess
r=Path(sys.argv[1]);p=r/'experiments/glibc/selected-obsidian-provider-authority/review/gdkpixbuf-core-provider-acquisition-result-review.tsv'
rows=list(csv.DictReader(p.open(),delimiter='\t'))
rows[1]['provider_authority']='ACCEPTED'
with p.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
rc=subprocess.run([str(r/'tools/docs/check-gdkpixbuf-core-provider-acquisition-result-review')]).returncode
if rc==0: raise SystemExit('checker accepted premature provider authority')
PY
git -C "$ROOT" archive HEAD | tar -x -C "$WORK/reset" 2>/dev/null || { mkdir -p "$WORK/reset"; git -C "$ROOT" archive HEAD | tar -x -C "$WORK/reset"; }
python3 - "$WORK/reset" <<'PY'
from pathlib import Path
import csv,sys,subprocess
r=Path(sys.argv[1]);p=r/'experiments/glibc/selected-obsidian-provider-authority/review/gdkpixbuf-core-provider-acquisition-result-review-metadata.tsv'
rows=list(csv.DictReader(p.open(),delimiter='\t'))
for x in rows:
 if x['key']=='protected_state_disposition': x['value']='REAL_MUTATION'
with p.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['key','value'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
rc=subprocess.run([str(r/'tools/docs/check-gdkpixbuf-core-provider-acquisition-result-review')]).returncode
if rc==0: raise SystemExit('checker accepted false protected-state classification')
PY
printf 'gdkpixbuf-core-provider-acquisition-result-review-smoke: PASS\n'
