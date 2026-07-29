#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-$(dirname "$ROOT")}
mkdir -p "$TMP_BASE"
F=$(mktemp -d "$TMP_BASE/live-authority-design-acceptance.XXXXXX")
trap 'rm -rf "$F"' EXIT
TREE=$(git -C "$ROOT" write-tree)
git -C "$ROOT" archive "$TREE" | tar -xf - -C "$F"
CHECK="$F/tools/docs/check-selected-provider-local-supply-live-authority-transaction-design-boundary-acceptance"
ACC="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-design-boundary-acceptance.tsv"
python3 "$CHECK" >/dev/null
python3 - "$ACC" <<'PY2'
import csv, sys
from pathlib import Path
p = Path(sys.argv[1])
with p.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
    fields = list(rows[0])
rows[0]['accepted_current_selected_provider_read_count'] = '1'
with p.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
PY2
if python3 "$CHECK" >/dev/null 2>&1; then
  echo 'selected-provider read widening accepted' >&2
  exit 1
fi
git -C "$ROOT" show "$TREE":experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-design-boundary-acceptance.tsv > "$ACC"
python3 - "$ACC" <<'PY2'
import csv, sys
from pathlib import Path
p = Path(sys.argv[1])
with p.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
    fields = list(rows[0])
rows[0]['replay_registry_state'] = 'OPENED_WRITTEN'
with p.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
PY2
if python3 "$CHECK" >/dev/null 2>&1; then
  echo 'replay authority widening accepted' >&2
  exit 1
fi
echo 'selected-provider local-supply live-authority transaction design boundary acceptance smoke: PASS'
