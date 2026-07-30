#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
CHECK=tools/docs/check-selected-provider-local-supply-live-authority-transaction-production-implementation-review
SOURCE=experiments/glibc/selected-obsidian-provider-authority/implementation/selected_provider_local_supply_live_authority_transaction_production_candidate.py
SUCCESS=experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-production-implementation-isolated-success.json
METADATA=experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-production-implementation-metadata.tsv
TREE=$(git -C "$ROOT" write-tree)
TMP_BASE=${TND_TEST_TMPDIR:-$(dirname "$ROOT")}
mkdir -p "$TMP_BASE"
TMP=$(mktemp -d "$TMP_BASE/live-authority-production-implementation.XXXXXX")
trap 'rm -rf "$TMP"' EXIT
FIXTURE="$TMP/repository"
mkdir -p "$FIXTURE"
git -C "$ROOT" archive "$TREE" | tar -xf - -C "$FIXTURE"

python3 - "$FIXTURE/$SUCCESS" <<'PYMUTATE1'
import json, sys
path=sys.argv[1]
value=json.load(open(path))
value["selected_provider_open_count"]=1
open(path,"w").write(json.dumps(value,sort_keys=True,separators=(",",":"))+"\n")
PYMUTATE1
if (cd "$FIXTURE" && python3 "$CHECK") >/dev/null 2>&1; then
  echo "mutation selected-provider-open widening was not rejected" >&2
  exit 1
fi

git -C "$ROOT" show "$TREE:$SUCCESS" > "$FIXTURE/$SUCCESS"
printf '\nimport selected_provider_local_supply_live_authority_transaction_candidate\n' >> "$FIXTURE/$SOURCE"
if (cd "$FIXTURE" && python3 "$CHECK") >/dev/null 2>&1; then
  echo "mutation accepted synthetic oracle import was not rejected" >&2
  exit 1
fi

git -C "$ROOT" show "$TREE:$SOURCE" > "$FIXTURE/$SOURCE"
python3 - "$FIXTURE/$METADATA" <<'PYMUTATE2'
import sys
path=sys.argv[1]
text=open(path).read()
text=text.replace("project_replay_write_count\t0","project_replay_write_count\t1")
open(path,"w").write(text)
PYMUTATE2
if (cd "$FIXTURE" && python3 "$CHECK") >/dev/null 2>&1; then
  echo "mutation project replay write widening was not rejected" >&2
  exit 1
fi

echo "live-authority transaction production implementation smoke: PASS: selected-provider open, accepted-oracle import and project replay-write widening rejected"
