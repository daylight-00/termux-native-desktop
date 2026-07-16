#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"; TMP=$(mktemp -d "$TMP_BASE/gdkpixbuf-provider-review.XXXXXX"); trap 'rm -rf "$TMP"' EXIT
bash "$ROOT/tools/docs/check-gdkpixbuf-2-42-12-provider-candidate-result-review"
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
# Decision widening must fail.
python3 - "$TMP/experiments/glibc/selected-obsidian-provider-authority/review/gdkpixbuf-2-42-12-provider-candidate-result-review.tsv" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]); t=p.read_text(); p.write_text(t.replace('ACCEPTED_BOUNDED_PROVIDER','ACCEPTED_COMPLETE_COMPOSITION',1))
PY
if bash "$TMP/tools/docs/check-gdkpixbuf-2-42-12-provider-candidate-result-review" >/dev/null 2>&1; then
  echo 'gdkpixbuf provider smoke: FAIL: widened decision accepted' >&2; exit 1
fi
printf 'gdkpixbuf provider review smoke: PASS\n'
