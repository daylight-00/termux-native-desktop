#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
FIXTURE=$(mktemp -d "$TMP_BASE/libjpeg-result-review-smoke.XXXXXX")
cleanup(){ chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }; trap cleanup EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
CHECK="$FIXTURE/tools/docs/check-libjpeg-so-62-compatibility-provider-candidate-result-review"
TABLE=experiments/glibc/selected-obsidian-provider-authority/review/libjpeg-so-62-compatibility-provider-candidate-result-review.tsv
bash "$CHECK" "$FIXTURE" >/dev/null
restore(){ git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"; }
mutate(){ python3 - "$FIXTURE/$TABLE" "$1" "$2" <<'PY'
from pathlib import Path
import csv,sys
p=Path(sys.argv[1]); rows=list(csv.DictReader(p.open(),delimiter='\t')); rows[0][sys.argv[2]]=sys.argv[3]
with p.open('w',newline='') as f: w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
}
mutate candidate_decision ACCEPTED_PROVIDER
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'libjpeg result smoke: first candidate accepted' >&2; exit 1; fi
restore
mutate dt_runpath_state ABSENT
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'libjpeg result smoke: blocking runpath erased' >&2; exit 1; fi
restore
mutate candidate_sha256 0000000000000000000000000000000000000000000000000000000000000000
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'libjpeg result smoke: candidate digest drift accepted' >&2; exit 1; fi
restore
mutate authority_effect PROVIDER_AUTHORITY_ACCEPTED
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'libjpeg result smoke: authority broadening accepted' >&2; exit 1; fi
restore
sed -i 's/add CMAKE_SKIP_RPATH=ON/add CMAKE_SKIP_RPATH=OFF/' "$FIXTURE/docs/evidence/libjpeg-so-62-compatibility-provider-candidate-result-review.md"
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'libjpeg result smoke: corrected build contract weakened' >&2; exit 1; fi
echo 'libjpeg.so.62 compatibility-provider candidate result review smoke: PASS'
