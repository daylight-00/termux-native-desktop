#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}};mkdir -p "$TMP_BASE";F=$(mktemp -d "$TMP_BASE/local-supply-contract-acceptance.XXXXXX");trap 'rm -rf "$F"' EXIT
git -C "$ROOT" archive HEAD | tar -xf - -C "$F"
CHECK="$F/tools/docs/check-selected-provider-local-supply-map-contract-boundary-acceptance"
ACC="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-contract-boundary-acceptance.tsv"
CONTRACT="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-contract.tsv"
python3 "$CHECK" >/dev/null
sed -i 's/NOT_AUTHORIZED_SEPARATE_READ_ONLY_EVIDENCE_TRANSACTION_REQUIRED/AUTHORIZED/' "$ACC"
if python3 "$CHECK" >/dev/null 2>&1; then echo 'path discovery widening accepted' >&2;exit 1;fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-contract-boundary-acceptance.tsv > "$ACC"
python3 - "$CONTRACT" <<'PYINNER'
from pathlib import Path
import sys
p=Path(sys.argv[1]);s=p.read_text();p.write_text(s.replace('\tUNBOUND_CONTRACT_ONLY\t\t','\tUNBOUND_CONTRACT_ONLY\t/tmp/fabricated.so\t',1))
PYINNER
if python3 "$CHECK" >/dev/null 2>&1; then echo 'populated candidate path accepted' >&2;exit 1;fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-contract.tsv > "$CONTRACT"
sed -i 's/NOT_AUTHORIZED_SEPARATE_EXPLICIT_DECISION_REQUIRED/AUTHORIZED/' "$ACC"
if python3 "$CHECK" >/dev/null 2>&1; then echo 'execution widening accepted' >&2;exit 1;fi
echo 'selected-provider local-supply-map contract boundary acceptance smoke: PASS'
