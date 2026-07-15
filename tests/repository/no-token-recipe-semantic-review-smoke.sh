#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
FIXTURE=$(mktemp -d "$TMP_BASE/no-token-recipe-smoke.XXXXXX")
cleanup() { chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }
trap cleanup EXIT HUP INT TERM

git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
CHECK="$FIXTURE/tools/docs/check-no-token-recipe-semantic-review"
TABLE=experiments/glibc/selected-obsidian-provider-authority/review/no-token-recipe-semantic-review.tsv
CLAIMS=experiments/glibc/selected-obsidian-provider-authority/review/provider-claim-classification.tsv
bash "$CHECK" "$FIXTURE" >/dev/null

# Negative: exact seven-root coverage is mandatory.
sed -i '2d' "$FIXTURE/$TABLE"
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then
  echo 'no-token recipe smoke: missing root review was accepted' >&2
  exit 1
fi
git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"

# Negative: recipe blob identity must remain exact.
python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import csv,sys
p=Path(sys.argv[1]); rows=list(csv.DictReader(p.open(),delimiter='\t'))
rows[0]['recipe_manifest']='build.sh:100644:0000000000000000000000000000000000000000'
with p.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then
  echo 'no-token recipe smoke: wrong recipe blob was accepted' >&2
  exit 1
fi
git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"

# Negative: the semantic review cannot accept provider authority.
python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import csv,sys
p=Path(sys.argv[1]); rows=list(csv.DictReader(p.open(),delimiter='\t'))
rows[0]['authority_effect']='PROVIDER_AUTHORITY_ACCEPTED'
with p.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then
  echo 'no-token recipe smoke: provider authority effect was accepted' >&2
  exit 1
fi
git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"

# Negative: Pango filename drift must remain open and separate.
python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import csv,sys
p=Path(sys.argv[1]); rows=list(csv.DictReader(p.open(),delimiter='\t'))
for row in rows:
 if row['recipe_root']=='gpkg/pango': row['concrete_filename_drift_state']='NONE'
with p.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then
  echo 'no-token recipe smoke: closed Pango drift was accepted' >&2
  exit 1
fi
git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"

# Negative: generated provider claim cannot retain ADAPTATION_CLASSIFICATION.
python3 - "$FIXTURE/$CLAIMS" <<'PY'
from pathlib import Path
import csv,sys
p=Path(sys.argv[1]); rows=list(csv.DictReader(p.open(),delimiter='\t'))
for row in rows:
 if row['subject_label']=='gpkg/libxfixes' and row['claim_type']=='PROVIDER_AUTHORITY':
  row['remaining_gap']='ADAPTATION_CLASSIFICATION;'+row['remaining_gap']
with p.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then
  echo 'no-token recipe smoke: stale adaptation prerequisite was accepted' >&2
  exit 1
fi

echo 'no-token recipe semantic review smoke: PASS'
