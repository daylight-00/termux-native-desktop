#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
CHECK="$ROOT/tools/docs/check-selected-provider-local-supply-live-authority-transaction-design-review"
"$CHECK"
TMP_BASE=${TND_TEST_TMPDIR:-$(dirname "$ROOT")}
mkdir -p "$TMP_BASE"
work=$(mktemp -d "$TMP_BASE/live-authority-design-smoke.XXXXXX")
trap 'rm -rf "$work"' EXIT
mkdir -p "$work/repo"
git -C "$ROOT" archive HEAD | tar -xf - -C "$work/repo"
python3 - "$work/repo/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-design-metadata.tsv" <<'PY1'
from pathlib import Path
import csv,sys
p=Path(sys.argv[1])
with p.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f,delimiter='\t'));fields=rows[0].keys()
rows[0]['current_selected_provider_open_count']='1'
with p.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
PY1
if "$work/repo/tools/docs/check-selected-provider-local-supply-live-authority-transaction-design-review" >/dev/null 2>&1; then
 echo 'mutation current selected-provider open unexpectedly passed' >&2; exit 1
fi
rm -rf "$work/repo";mkdir -p "$work/repo";git -C "$ROOT" archive HEAD | tar -xf - -C "$work/repo"
python3 - "$work/repo/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-failure-contract.tsv" <<'PY2'
from pathlib import Path
import sys
p=Path(sys.argv[1]);lines=p.read_text().splitlines();p.write_text('\n'.join(lines[:-1])+'\n')
PY2
if "$work/repo/tools/docs/check-selected-provider-local-supply-live-authority-transaction-design-review" >/dev/null 2>&1; then
 echo 'mutation missing failure contract unexpectedly passed' >&2; exit 1
fi
printf 'live-authority transaction design smoke: PASS\n'
