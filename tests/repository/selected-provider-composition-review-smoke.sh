#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"; FIXTURE=$(mktemp -d "$TMP_BASE/provider-composition.XXXXXX")
cleanup(){ chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }; trap cleanup EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
bash "$FIXTURE/tools/docs/check-selected-provider-composition-review" >/dev/null
META=experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-metadata.tsv
restore(){ git -C "$ROOT" show HEAD:"$META" > "$FIXTURE/$META"; }
python3 - "$FIXTURE/$META" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]);s=p.read_text().replace('composition_decision\tREVIEWED_BLOCKED_INCOMPLETE','composition_decision\tACCEPTED');p.write_text(s)
PY
if bash "$FIXTURE/tools/docs/check-selected-provider-composition-review" >/dev/null 2>&1; then echo 'composition smoke: incomplete set accepted' >&2; exit 1; fi
restore
python3 - "$FIXTURE/$META" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]);s=p.read_text().replace('target_manifest_allowed\tNO','target_manifest_allowed\tYES');p.write_text(s)
PY
if bash "$FIXTURE/tools/docs/check-selected-provider-composition-review" >/dev/null 2>&1; then echo 'composition smoke: target generation widened' >&2; exit 1; fi
restore
GAPS=experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-gaps.tsv
sed -i '2d' "$FIXTURE/$GAPS"
if bash "$FIXTURE/tools/docs/check-selected-provider-composition-review" >/dev/null 2>&1; then echo 'composition smoke: missing gap accepted' >&2; exit 1; fi
echo 'selected provider composition review smoke: PASS'
