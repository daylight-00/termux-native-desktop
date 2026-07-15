#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
FIXTURE=$(mktemp -d "$TMP_BASE/pango-provider-smoke.XXXXXX")
cleanup(){ chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }; trap cleanup EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
CHECK="$FIXTURE/tools/docs/check-pango-reference-consumed-provider-authority"
TABLE=experiments/glibc/selected-obsidian-provider-authority/review/pango-reference-consumed-provider-authority.tsv
POLICY=experiments/glibc/selected-obsidian-provider-authority/review/pango-concrete-filename-continuity-policy.tsv
bash "$CHECK" "$FIXTURE" >/dev/null
restore_table(){ git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"; }
restore_policy(){ git -C "$ROOT" show HEAD:"$POLICY" > "$FIXTURE/$POLICY"; }
mutate_table(){ python3 - "$FIXTURE/$TABLE" "$1" "$2" <<'PY'
from pathlib import Path
import csv,sys
p=Path(sys.argv[1]); rows=list(csv.DictReader(p.open(),delimiter='\t')); rows[0][sys.argv[2]]=sys.argv[3]
with p.open('w',newline='') as f: w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
}
mutate_policy(){ python3 - "$FIXTURE/$POLICY" "$1" "$2" "$3" <<'PY'
from pathlib import Path
import csv,sys
p=Path(sys.argv[1]); rows=list(csv.DictReader(p.open(),delimiter='\t'))
for r in rows:
 if r['policy_id']==sys.argv[2]: r[sys.argv[3]]=sys.argv[4]
with p.open('w',newline='') as f: w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
}
mutate_table observed_sonames 'libpango-1.0.so.999;libpangoft2-1.0.so.0;libpangocairo-1.0.so.0'
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'pango smoke: SONAME drift accepted' >&2; exit 1; fi
restore_table
mutate_table observed_alias_targets 'libpango-1.0.so.0.5600.3;libpangoft2-1.0.so.0.5400.0;libpangocairo-1.0.so.0.5400.0'
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'pango smoke: wrong alias target accepted' >&2; exit 1; fi
restore_table
mutate_policy PANGO-CF-002 decision ACCEPT_ORACLE_FILENAME_AS_TARGET_AUTHORITY
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'pango smoke: oracle filename authority accepted' >&2; exit 1; fi
restore_policy
mutate_policy PANGO-CF-004 required_invariant MIXED_GENERATION_FAMILY_ALLOWED
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'pango smoke: mixed-generation rollback accepted' >&2; exit 1; fi
restore_policy
mutate_table authority_effect COMPLETE_GTK_COMPOSITION_TARGET_AND_ACTIVATION_ACCEPTED
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'pango smoke: authority broadening accepted' >&2; exit 1; fi
restore_table
sed -i '2d' "$FIXTURE/$TABLE"
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'pango smoke: missing provider row accepted' >&2; exit 1; fi
echo 'pango reference-consumed provider authority smoke: PASS'
