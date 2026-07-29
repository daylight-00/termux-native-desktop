#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
TMP_BASE=${TND_TEST_TMPDIR:-$(dirname "$ROOT")}
mkdir -p "$TMP_BASE"
TREE=$(git -C "$ROOT" write-tree)
WORK=$(mktemp -d "$TMP_BASE/live-authority-implementation-review.XXXXXX")
cleanup(){ rm -rf "$WORK"; }
trap cleanup EXIT
F="$WORK/repo"
mkdir -p "$F"
git -C "$ROOT" archive "$TREE" | tar -xf - -C "$F"
CHECK="$F/tools/docs/check-selected-provider-local-supply-live-authority-transaction-implementation-review"
META="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-implementation-metadata.tsv"
SOURCE="$F/experiments/glibc/selected-obsidian-provider-authority/implementation/selected_provider_local_supply_live_authority_transaction_candidate.py"
COVERAGE="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-implementation-coverage.tsv"
python3 "$CHECK" >/dev/null
python3 - "$META" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]);s=p.read_text();s=s.replace('synthetic_selected_provider_open_count\t0','synthetic_selected_provider_open_count\t1',1);p.write_text(s)
PY
if python3 "$CHECK" >/dev/null 2>&1; then echo 'smoke: metadata authority widening accepted' >&2; exit 1; fi
git -C "$ROOT" show "$TREE":experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-implementation-metadata.tsv > "$META"
python3 - "$SOURCE" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]);s=p.read_text();p.write_text(s.replace('import argparse\n','import argparse\nimport os\n',1))
PY
if python3 "$CHECK" >/dev/null 2>&1; then echo 'smoke: forbidden import accepted' >&2; exit 1; fi
git -C "$ROOT" show "$TREE":experiments/glibc/selected-obsidian-provider-authority/implementation/selected_provider_local_supply_live_authority_transaction_candidate.py > "$SOURCE"
python3 - "$COVERAGE" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]);s=p.read_text();s=s.replace('ZERO_LIVE_DOCUMENTS_REPLAY_WRITES_SELECTED_PROVIDER_OPENS_READS_PROVIDER_BYTES_LOCAL_MAPS_LIVE_AUTHORITY','LIVE_PROVIDER_OPEN_AUTHORITY',1);p.write_text(s)
PY
if python3 "$CHECK" >/dev/null 2>&1; then echo 'smoke: coverage authority widening accepted' >&2; exit 1; fi
printf 'live-authority transaction implementation smoke: PASS\n'
