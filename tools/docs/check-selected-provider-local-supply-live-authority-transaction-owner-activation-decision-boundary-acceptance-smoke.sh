#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
TREE=$(git -C "$ROOT" write-tree)
TMP=$(mktemp -d -p "$(dirname "$ROOT")" owner-activation-acceptance.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
git -C "$ROOT" archive "$TREE" | tar -xf - -C "$TMP"
CHECK="$TMP/tools/docs/check-selected-provider-local-supply-live-authority-transaction-owner-activation-decision-boundary-acceptance"
ACC="$TMP/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-owner-activation-decision-boundary-acceptance.tsv"
python3 "$CHECK" >/dev/null
restore() {
  git -C "$ROOT" show "$TREE:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-owner-activation-decision-boundary-acceptance.tsv" > "$ACC"
}
python3 - "$ACC" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]);s=p.read_text();p.write_text(s.replace('ONE_NON_EXECUTING_EXACT_INPUT_SET_COLLECTION_SEALING_AND_REVIEW_TRANSACTION_ONLY','LIVE_EXECUTION_AUTHORIZED',1))
PY
if python3 "$CHECK" >/dev/null 2>&1; then echo 'mutation execution widening accepted' >&2; exit 1; fi
restore
python3 - "$ACC" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]);s=p.read_text();p.write_text(s.replace('\tNO\tNO\tNO\tNO\t0\t', '\tNO\tNO\tYES\tNO\t0\t',1))
PY
if python3 "$CHECK" >/dev/null 2>&1; then echo 'mutation provider-open widening accepted' >&2; exit 1; fi
restore
python3 - "$ACC" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]);s=p.read_text();p.write_text(s.replace('NOT_SUPPLIED_NOT_AUTHORIZED','SUPPLIED_AUTHORIZED',1))
PY
if python3 "$CHECK" >/dev/null 2>&1; then echo 'mutation inferred input accepted' >&2; exit 1; fi
echo 'owner activation decision acceptance smoke: PASS'
