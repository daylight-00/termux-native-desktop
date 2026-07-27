#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
F=$(mktemp -d "$TMP_BASE/local-supply-issuance-coordinate-design-acceptance.XXXXXX")
trap 'rm -rf "$F"' EXIT
git -C "$ROOT" archive HEAD | tar -xf - -C "$F"
CHECK="$F/tools/docs/check-selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-boundary-acceptance"
ACC="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-boundary-acceptance.tsv"
META="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-metadata.tsv"
RECEIPT="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-receipt-contract.json"
python3 "$CHECK" >/dev/null
sed -i 's/NOT_AUTHORIZED_SEPARATE_EXPLICIT_OWNER_DECISION_AND_TRANSACTION_REQUIRED/AUTHORIZED/' "$ACC"
if python3 "$CHECK" >/dev/null 2>&1; then
  echo 'owner issuance authority widening accepted' >&2
  exit 1
fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-boundary-acceptance.tsv > "$ACC"
sed -i 's/current_live_authority_count	0/current_live_authority_count	1/' "$META"
if python3 "$CHECK" >/dev/null 2>&1; then
  echo 'candidate live authority accepted' >&2
  exit 1
fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-metadata.tsv > "$META"
python3 - "$RECEIPT" <<'PYINNER'
import json,sys
from pathlib import Path
p=Path(sys.argv[1])
d=json.loads(p.read_text())
d['current_provider_read_count']=1
p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PYINNER
if python3 "$CHECK" >/dev/null 2>&1; then
  echo 'candidate provider read accepted' >&2
  exit 1
fi
echo 'selected-provider local-supply authorization issuance/coordinate production design boundary acceptance smoke: PASS'
