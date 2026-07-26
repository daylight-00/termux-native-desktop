#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}};mkdir -p "$TMP_BASE";F=$(mktemp -d "$TMP_BASE/target-pop-supply.XXXXXX");trap 'rm -rf "$F"' EXIT
git -C "$ROOT" archive HEAD | tar -xf - -C "$F"
python3 "$F/tools/docs/check-target-population-intervention-supply-binding-review" >/dev/null
T=experiments/glibc/selected-obsidian-provider-authority/review/selected-target-population-intervention-supply-review-metadata.tsv
sed -i 's/INTERVENTION_RETAINED/BOUNDED_MATERIALIZER_DESIGN_REVIEW_AUTHORIZED/' "$F/$T"
if python3 "$F/tools/docs/check-target-population-intervention-supply-binding-review" >/dev/null 2>&1; then echo 'target population supply smoke: intervention widening accepted' >&2;exit 1;fi
git -C "$ROOT" show HEAD:"$T" > "$F/$T"
B=experiments/glibc/selected-obsidian-provider-authority/review/selected-target-supply-byte-binding-review.tsv
python3 - "$F/$B" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]);s=p.read_text();s=s.replace('BLOCKED_RESULT_COORDINATE_MISSING','QUALIFIED_READ_ONLY_BINDING_INPUT',1);p.write_text(s)
PY
if python3 "$F/tools/docs/check-target-population-intervention-supply-binding-review" >/dev/null 2>&1; then echo 'target population supply smoke: unbound result accepted' >&2;exit 1;fi
echo 'target population intervention and supply binding smoke: PASS'
