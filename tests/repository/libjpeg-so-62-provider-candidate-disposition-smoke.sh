#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
FIXTURE=$(mktemp -d "$TMP_BASE/libjpeg-so-62-disposition-smoke.XXXXXX")
cleanup(){ chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }; trap cleanup EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
CHECK="$FIXTURE/tools/docs/check-libjpeg-so-62-provider-candidate-disposition"
TABLE=experiments/glibc/selected-obsidian-provider-authority/review/libjpeg-so-62-provider-candidate-disposition.tsv
bash "$CHECK" "$FIXTURE" >/dev/null
restore(){ git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"; }
mutate(){ python3 - "$FIXTURE/$TABLE" "$1" "$2" <<'PY'
from pathlib import Path
import csv,sys
p=Path(sys.argv[1]); rows=list(csv.DictReader(p.open(),delimiter='\t')); rows[0][sys.argv[2]]=sys.argv[3]
with p.open('w',newline='') as f: w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
}
mutate required_lookup_identity libjpeg.so.8
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'libjpeg smoke: SONAME-8 requirement accepted' >&2; exit 1; fi
restore
mutate disposition ACCEPT_EXISTING_SONAME_8_PROVIDER
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'libjpeg smoke: SONAME-8 provider substitution accepted' >&2; exit 1; fi
restore
mutate expected_compatibility_concrete_member libjpeg.so.62.3.0
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'libjpeg smoke: oracle concrete filename accepted as pinned source output' >&2; exit 1; fi
restore
mutate prohibited_inference ALLOW_SONAME_ALIAS_TO_LIBJPEG_SO_8
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'libjpeg smoke: alias bridge accepted' >&2; exit 1; fi
restore
mutate authority_effect PROVIDER_COMPOSITION_TARGET_AND_ACTIVATION_ACCEPTED
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'libjpeg smoke: authority broadening accepted' >&2; exit 1; fi
restore
sed -i '2d' "$FIXTURE/$TABLE"
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'libjpeg smoke: missing disposition row accepted' >&2; exit 1; fi
echo 'libjpeg.so.62 provider-candidate disposition smoke: PASS'
