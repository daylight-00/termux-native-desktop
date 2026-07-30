#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-$(dirname "$ROOT")}
mkdir -p "$TMP_BASE"
F=$(mktemp -d "$TMP_BASE/live-authority-production-implementation-acceptance.XXXXXX")
trap 'rm -rf "$F"' EXIT
TREE=$(git -C "$ROOT" write-tree)
git -C "$ROOT" archive "$TREE" | tar -xf - -C "$F"
CHECK="$F/tools/docs/check-selected-provider-local-supply-live-authority-transaction-production-implementation-boundary-acceptance"
ACC="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-production-implementation-boundary-acceptance.tsv"
META="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-production-implementation-metadata.tsv"
python3 "$CHECK" >/dev/null
python3 - "$ACC" <<'PY2'
import csv,sys
from pathlib import Path
p=Path(sys.argv[1])
with p.open(newline='',encoding='utf-8') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
    fields=list(rows[0])
rows[0]['accepted_current_selected_provider_read_count']='1'
with p.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n')
    w.writeheader(); w.writerows(rows)
PY2
if python3 "$CHECK" >/dev/null 2>&1; then echo 'selected-provider read widening accepted' >&2; exit 1; fi
git -C "$ROOT" show "$TREE":experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-production-implementation-boundary-acceptance.tsv > "$ACC"
python3 - "$ACC" <<'PY2'
import csv,sys
from pathlib import Path
p=Path(sys.argv[1])
with p.open(newline='',encoding='utf-8') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
    fields=list(rows[0])
rows[0]['provider_open_gate_state']='OPEN_AUTHORIZED'
with p.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n')
    w.writeheader(); w.writerows(rows)
PY2
if python3 "$CHECK" >/dev/null 2>&1; then echo 'provider-open authority widening accepted' >&2; exit 1; fi
git -C "$ROOT" show "$TREE":experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-production-implementation-boundary-acceptance.tsv > "$ACC"
sed -i $'s/project_replay_write_count\t0/project_replay_write_count\t1/' "$META"
if python3 "$CHECK" >/dev/null 2>&1; then echo 'project replay widening accepted' >&2; exit 1; fi
echo 'selected-provider local-supply live-authority transaction production implementation boundary acceptance smoke: PASS'
