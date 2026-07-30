#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
CHECK=tools/docs/check-selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-review
SOURCE=experiments/glibc/selected-obsidian-provider-authority/implementation/selected_provider_local_supply_live_authority_transaction_exact_input_set_collection_candidate.py
SUCCESS=experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-isolated-success.json
METADATA=experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-metadata.tsv
TREE=$(git -C "$ROOT" write-tree)
TMP_BASE=${TND_TEST_TMPDIR:-$(dirname "$ROOT")}; mkdir -p "$TMP_BASE"
TMP=$(mktemp -d "$TMP_BASE/exact-input-set-collection.XXXXXX"); trap 'rm -rf "$TMP"' EXIT
FIXTURE="$TMP/repository"; mkdir -p "$FIXTURE"
git -C "$ROOT" archive "$TREE" | tar -xf - -C "$FIXTURE"

python3 - "$FIXTURE/$SUCCESS" <<'PY'
import json,sys
p=sys.argv[1]; v=json.load(open(p)); v['selected_provider_open_count']=1
open(p,'w').write(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n')
PY
if (cd "$FIXTURE" && python3 "$CHECK") >/dev/null 2>&1; then echo "mutation selected-provider open widening was not rejected" >&2; exit 1; fi

git -C "$ROOT" show "$TREE:$SUCCESS" > "$FIXTURE/$SUCCESS"
printf '\nimport selected_provider_local_supply_live_authority_transaction_production_candidate\n' >> "$FIXTURE/$SOURCE"
if (cd "$FIXTURE" && python3 "$CHECK") >/dev/null 2>&1; then echo "mutation accepted production implementation import was not rejected" >&2; exit 1; fi

git -C "$ROOT" show "$TREE:$SOURCE" > "$FIXTURE/$SOURCE"
python3 - "$FIXTURE/$METADATA" <<'PY'
import sys
p=sys.argv[1]; s=open(p).read().replace('consumed_transaction_count\t0','consumed_transaction_count\t1').replace('remaining_transaction_count\t1','remaining_transaction_count\t0')
open(p,'w').write(s)
PY
if (cd "$FIXTURE" && python3 "$CHECK") >/dev/null 2>&1; then echo "mutation premature owner transaction consumption was not rejected" >&2; exit 1; fi

echo "exact input-set collection smoke: PASS: selected-provider open, accepted implementation import and premature transaction consumption widening rejected"
