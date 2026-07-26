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
p=Path(sys.argv[1]);s=p.read_text().replace('composition_decision\tREVIEWED_COMPLETE_PROVIDER_SET_TARGET_MANIFEST_NOT_ACCEPTED','composition_decision\tACCEPTED');p.write_text(s)
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
printf 'COMP-GAP-999\tselected:fake\tfake.so.1\tfake.so.1\tfake.so.1\tfake\t1\tNONE_REVIEWED_ROOT\tFAKE_GAP\tFAKE\tFAKE\tFAKE\tBLOCKS_COMPOSITION_ACCEPTANCE_AND_TARGET_MANIFEST_GENERATION\n' >> "$FIXTURE/$GAPS"
if bash "$FIXTURE/tools/docs/check-selected-provider-composition-review" >/dev/null 2>&1; then echo 'composition smoke: reintroduced active gap accepted' >&2; exit 1; fi
echo 'selected provider composition review smoke: PASS'
