#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
FIXTURE=$(mktemp -d "$TMP_BASE/xorg-provider-smoke.XXXXXX")
cleanup() { chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }
trap cleanup EXIT HUP INT TERM

git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
bash "$FIXTURE/tools/docs/check-xorg-reference-consumed-provider-authority" >/dev/null

TABLE=experiments/glibc/selected-obsidian-provider-authority/review/xorg-reference-consumed-provider-authority.tsv

restore() { git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"; }

# Negative: exact SONAME drift must fail.
python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); lines=p.read_text().splitlines(); cols=lines[0].split('\t'); row=lines[1].split('\t')
row[cols.index('observed_soname')]='libXfixes.so.999'; lines[1]='\t'.join(row); p.write_text('\n'.join(lines)+'\n')
PY
if bash "$FIXTURE/tools/docs/check-xorg-reference-consumed-provider-authority" >/dev/null 2>&1; then
  echo 'xorg provider smoke: SONAME drift was accepted' >&2; exit 1
fi
restore

# Negative: accepted provider cannot gain target or activation effect.
python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); lines=p.read_text().splitlines(); cols=lines[0].split('\t'); row=lines[1].split('\t')
row[cols.index('authority_effect')]='PROVIDER_AUTHORITY_AND_TARGET_ACTIVATION_ACCEPTED'; lines[1]='\t'.join(row); p.write_text('\n'.join(lines)+'\n')
PY
if bash "$FIXTURE/tools/docs/check-xorg-reference-consumed-provider-authority" >/dev/null 2>&1; then
  echo 'xorg provider smoke: target or activation effect was accepted' >&2; exit 1
fi
restore

# Negative: static candidate exclusion is mandatory.
python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); lines=p.read_text().splitlines(); cols=lines[0].split('\t'); row=lines[1].split('\t')
row[cols.index('candidate_conflict_and_exclusion_result')]='ONE_DYNAMIC_CANDIDATE'; lines[1]='\t'.join(row); p.write_text('\n'.join(lines)+'\n')
PY
if bash "$FIXTURE/tools/docs/check-xorg-reference-consumed-provider-authority" >/dev/null 2>&1; then
  echo 'xorg provider smoke: missing static exclusion was accepted' >&2; exit 1
fi
restore

# Negative: a row cannot disappear.
sed -i '2d' "$FIXTURE/$TABLE"
if bash "$FIXTURE/tools/docs/check-xorg-reference-consumed-provider-authority" >/dev/null 2>&1; then
  echo 'xorg provider smoke: missing provider row was accepted' >&2; exit 1
fi

echo 'xorg reference-consumed provider authority smoke: PASS'
