#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
FIXTURE=$(mktemp -d "$TMP_BASE/libtasn1-provider-smoke.XXXXXX")
cleanup() { chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }
trap cleanup EXIT HUP INT TERM

git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
bash "$FIXTURE/tools/docs/check-libtasn1-reference-consumed-provider-authority" >/dev/null

TABLE=experiments/glibc/selected-obsidian-provider-authority/review/libtasn1-reference-consumed-provider-authority.tsv
restore() { git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"; }

python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); lines=p.read_text().splitlines(); c=lines[0].split('\t'); r=lines[1].split('\t')
r[c.index('observed_soname')]='libtasn1.so.999'; lines[1]='\t'.join(r); p.write_text('\n'.join(lines)+'\n')
PY
if bash "$FIXTURE/tools/docs/check-libtasn1-reference-consumed-provider-authority" >/dev/null 2>&1; then
  echo 'libtasn1 provider smoke: provider SONAME drift was accepted' >&2; exit 1
fi
restore

python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); lines=p.read_text().splitlines(); c=lines[0].split('\t'); r=lines[1].split('\t')
r[c.index('consumer_observed_soname')]='libgnutls.so.999'; lines[1]='\t'.join(r); p.write_text('\n'.join(lines)+'\n')
PY
if bash "$FIXTURE/tools/docs/check-libtasn1-reference-consumed-provider-authority" >/dev/null 2>&1; then
  echo 'libtasn1 provider smoke: consumer SONAME drift was accepted' >&2; exit 1
fi
restore

python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); lines=p.read_text().splitlines(); c=lines[0].split('\t'); r=lines[1].split('\t')
v=r[c.index('candidate_conflict_and_exclusion_result')]
r[c.index('candidate_conflict_and_exclusion_result')]=v.replace(';INCLUDED_MINITASN1_FALLBACK_NOT_SELECTED','')
lines[1]='\t'.join(r); p.write_text('\n'.join(lines)+'\n')
PY
if bash "$FIXTURE/tools/docs/check-libtasn1-reference-consumed-provider-authority" >/dev/null 2>&1; then
  echo 'libtasn1 provider smoke: included fallback ambiguity was accepted' >&2; exit 1
fi
restore

python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); lines=p.read_text().splitlines(); c=lines[0].split('\t'); r=lines[1].split('\t')
r[c.index('authority_effect')]='PROVIDER_COMPOSITION_TARGET_AND_ACTIVATION_ACCEPTED'
lines[1]='\t'.join(r); p.write_text('\n'.join(lines)+'\n')
PY
if bash "$FIXTURE/tools/docs/check-libtasn1-reference-consumed-provider-authority" >/dev/null 2>&1; then
  echo 'libtasn1 provider smoke: target or activation effect was accepted' >&2; exit 1
fi
restore

sed -i '2d' "$FIXTURE/$TABLE"
if bash "$FIXTURE/tools/docs/check-libtasn1-reference-consumed-provider-authority" >/dev/null 2>&1; then
  echo 'libtasn1 provider smoke: missing provider row was accepted' >&2; exit 1
fi

echo 'libtasn1 reference-consumed provider authority smoke: PASS'
