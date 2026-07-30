#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
TREE=$(git -C "$ROOT" write-tree)
TMP=$(mktemp -d -p "$(dirname "$ROOT")" owner-activation-review.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
git -C "$ROOT" archive "$TREE" | tar -xf - -C "$TMP"
CHECK="$TMP/tools/docs/check-selected-provider-local-supply-live-authority-transaction-owner-activation-decision-review"
python3 "$CHECK" >/dev/null
ROW="$TMP/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-owner-activation-decision-review.tsv"
python3 - "$ROW" <<'PY2'
from pathlib import Path
p=Path(__import__('sys').argv[1]);s=p.read_text();p.write_text(s.replace('ONE_NON_EXECUTING_EXACT_INPUT_SET_REVIEW_TRANSACTION_ONLY','LIVE_EXECUTION_AUTHORIZED',1))
PY2
if python3 "$CHECK" >/dev/null 2>&1; then echo 'mutation execution widening accepted' >&2; exit 1; fi
git -C "$ROOT" show "$TREE:$([ -n "$ROOT" ] && echo experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-owner-activation-decision-review.tsv)" > "$ROW"
python3 - "$ROW" <<'PY2'
from pathlib import Path
p=Path(__import__('sys').argv[1]);s=p.read_text();p.write_text(s.replace('NOT_SUPPLIED_NOT_AUTHORIZED','SUPPLIED_AUTHORIZED',1))
PY2
if python3 "$CHECK" >/dev/null 2>&1; then echo 'mutation input inference accepted' >&2; exit 1; fi
echo 'owner activation decision review smoke: PASS'
