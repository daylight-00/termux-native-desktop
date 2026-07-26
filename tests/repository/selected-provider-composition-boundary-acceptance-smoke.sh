#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
FIXTURE=$(mktemp -d "$TMP_BASE/composition-acceptance-smoke.XXXXXX")
trap 'rm -rf "$FIXTURE"' EXIT

git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
bash "$FIXTURE/tools/docs/check-selected-provider-composition-boundary-acceptance" >/dev/null
TABLE=experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-boundary-acceptance.tsv

python3 - "$FIXTURE/$TABLE" <<'PYONE'
from pathlib import Path
import sys
path = Path(sys.argv[1])
text = path.read_text()
text = text.replace('\t0\t0\t0\tEXACT_41_MEMBER', '\t1\t0\t0\tEXACT_41_MEMBER', 1)
path.write_text(text)
PYONE
if bash "$FIXTURE/tools/docs/check-selected-provider-composition-boundary-acceptance" >/dev/null 2>&1; then
  echo 'composition acceptance smoke: active gap accepted' >&2
  exit 1
fi

git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"
python3 - "$FIXTURE/$TABLE" <<'PYTWO'
from pathlib import Path
import sys
path = Path(sys.argv[1])
path.write_text(path.read_text().replace('NOT_AUTHORIZED', 'AUTHORIZED', 1))
PYTWO
if bash "$FIXTURE/tools/docs/check-selected-provider-composition-boundary-acceptance" >/dev/null 2>&1; then
  echo 'composition acceptance smoke: target population widened' >&2
  exit 1
fi

echo 'selected provider composition boundary acceptance smoke: PASS'
