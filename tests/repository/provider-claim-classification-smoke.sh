#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
FIXTURE=$(mktemp -d "$TMP_BASE/provider-claim-smoke.XXXXXX")
cleanup() { chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }
trap cleanup EXIT HUP INT TERM

git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
bash "$FIXTURE/tools/docs/check-provider-claim-classification" >/dev/null

CLAIMS=experiments/glibc/selected-obsidian-provider-authority/review/provider-claim-classification.tsv
DISP=experiments/glibc/selected-obsidian-provider-authority/review/provider-sup-02-request-disposition.tsv

# Negative: duplicate claim identity must fail.
tail -n 1 "$FIXTURE/$CLAIMS" >> "$FIXTURE/$CLAIMS"
if bash "$FIXTURE/tools/docs/check-provider-claim-classification" >/dev/null 2>&1; then
  echo 'provider claim smoke: duplicate claim ID was accepted' >&2
  exit 1
fi
git -C "$ROOT" show HEAD:"$CLAIMS" > "$FIXTURE/$CLAIMS"

# Negative: every canonical SUP-02 request must have exactly one disposition.
sed -i '2d' "$FIXTURE/$DISP"
if bash "$FIXTURE/tools/docs/check-provider-claim-classification" >/dev/null 2>&1; then
  echo 'provider claim smoke: missing SUP-02 disposition was accepted' >&2
  exit 1
fi
git -C "$ROOT" show HEAD:"$DISP" > "$FIXTURE/$DISP"

# Negative: a current mandatory SUP-02 request cannot be reintroduced silently.
python3 - "$FIXTURE/$DISP" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1])
lines=p.read_text().splitlines()
cols=lines[0].split('\t')
row=lines[1].split('\t')
row[cols.index('disposition')]='STILL_NECESSARY'
row[cols.index('required_now')]='YES'
lines[1]='\t'.join(row)
p.write_text('\n'.join(lines)+'\n')
PY
if bash "$FIXTURE/tools/docs/check-provider-claim-classification" >/dev/null 2>&1; then
  echo 'provider claim smoke: mandatory SUP-02 request was accepted' >&2
  exit 1
fi
git -C "$ROOT" show HEAD:"$DISP" > "$FIXTURE/$DISP"

# Negative: classification cannot create provider authority.
python3 - "$FIXTURE/$CLAIMS" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1])
lines=p.read_text().splitlines()
cols=lines[0].split('\t')
row=lines[1].split('\t')
row[cols.index('authority_effect')]='PROVIDER_AUTHORITY_ACCEPTED'
lines[1]='\t'.join(row)
p.write_text('\n'.join(lines)+'\n')
PY
if bash "$FIXTURE/tools/docs/check-provider-claim-classification" >/dev/null 2>&1; then
  echo 'provider claim smoke: authority effect was accepted' >&2
  exit 1
fi

echo 'provider claim classification smoke: PASS'
