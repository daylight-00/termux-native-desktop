#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
TREE=$(git -C "$ROOT" write-tree)
TMP=$(mktemp -d -p "$(dirname "$ROOT")" envelope-prep.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
git -C "$ROOT" archive "$TREE" | tar -xf - -C "$TMP"
CHECK="$TMP/tools/docs/check-selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-envelope-preparation-review"
SCHEMA="$TMP/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-envelope-preparation-schema.json"
python3 "$CHECK" >/dev/null
restore(){ git -C "$ROOT" show "$TREE:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-envelope-preparation-schema.json" > "$SCHEMA"; }
python3 - "$SCHEMA" <<'PY1'
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);x=json.loads(p.read_text());x['envelope_generated']=True;p.write_text(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n')
PY1
if python3 "$CHECK" >/dev/null 2>&1; then echo 'mutation generated envelope accepted' >&2; exit 1; fi
restore
python3 - "$SCHEMA" <<'PY2'
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);x=json.loads(p.read_text());x['accepted_boundaries']['consumed_transaction_count']=1;x['accepted_boundaries']['remaining_transaction_count']=0;p.write_text(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n')
PY2
if python3 "$CHECK" >/dev/null 2>&1; then echo 'mutation owner consumption accepted' >&2; exit 1; fi
restore
python3 - "$SCHEMA" <<'PY3'
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);x=json.loads(p.read_text());x['authority_counts']['selected_provider_opens']=1;p.write_text(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n')
PY3
if python3 "$CHECK" >/dev/null 2>&1; then echo 'mutation provider authority accepted' >&2; exit 1; fi
echo 'exact input-set envelope preparation smoke: PASS'
