#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
TREE=$(git -C "$ROOT" write-tree)
TMP=$(mktemp -d -p "$(dirname "$ROOT")" exact-input-set-collection-acceptance.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
git -C "$ROOT" archive "$TREE" | tar -xf - -C "$TMP"
CHECK="$TMP/tools/docs/check-selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-boundary-acceptance"
ACC="$TMP/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-boundary-acceptance.tsv"
python3 "$CHECK" >/dev/null
restore(){ git -C "$ROOT" show "$TREE:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-boundary-acceptance.tsv" > "$ACC"; }
python3 - "$ACC" <<'PY1'
from pathlib import Path
p=Path(__import__('sys').argv[1]);s=p.read_text();p.write_text(s.replace('	0	0	0	0	1	0	1	','	1	0	0	0	1	0	1	',1))
PY1
if python3 "$CHECK" >/dev/null 2>&1; then echo 'mutation selected-provider authority widening accepted' >&2; exit 1; fi
restore
python3 - "$ACC" <<'PY2'
from pathlib import Path
p=Path(__import__('sys').argv[1]);s=p.read_text();p.write_text(s.replace('	1	0	1	SELECTED-', '	1	1	0	SELECTED-',1))
PY2
if python3 "$CHECK" >/dev/null 2>&1; then echo 'mutation owner transaction consumption accepted' >&2; exit 1; fi
restore
python3 - "$ACC" <<'PY3'
from pathlib import Path
p=Path(__import__('sys').argv[1]);s=p.read_text();p.write_text(s.replace('NOT_SUPPLIED_NOT_AUTHORIZED','SUPPLIED_AUTHORIZED',1))
PY3
if python3 "$CHECK" >/dev/null 2>&1; then echo 'mutation inferred live input accepted' >&2; exit 1; fi
echo 'exact input-set collection acceptance smoke: PASS'
