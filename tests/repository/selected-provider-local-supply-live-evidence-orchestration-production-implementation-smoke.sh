#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
CHECK="$ROOT/tools/docs/check-selected-provider-local-supply-live-evidence-orchestration-production-implementation-review"
TMP_ROOT=${TMPDIR:-"${HOME:-$ROOT}/.cache"}
mkdir -p "$TMP_ROOT"
TMP=$(mktemp -d "$TMP_ROOT/leo-production-implementation-smoke.XXXXXX")
trap 'rm -rf "$TMP"' EXIT

"$CHECK"

cp -a "$ROOT" "$TMP/read-widen"
sed -i $'s/selected_provider_read_count\t0/selected_provider_read_count\t1/' \
  "$TMP/read-widen/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-evidence-orchestration-production-implementation-metadata.tsv"
if "$TMP/read-widen/tools/docs/check-selected-provider-local-supply-live-evidence-orchestration-production-implementation-review" >"$TMP/read-widen.log" 2>&1; then
  echo 'live-evidence-orchestration-smoke: FAIL: selected-provider read widening accepted' >&2
  exit 1
fi
echo 'live-evidence-orchestration-smoke: PASS: selected-provider read widening rejected'

cp -a "$ROOT" "$TMP/oracle-import"
printf '\nimport selected_provider_local_supply_map_evidence_transaction_candidate\n' >> \
  "$TMP/oracle-import/experiments/glibc/selected-obsidian-provider-authority/implementation/selected_provider_local_supply_live_evidence_orchestration_production_candidate.py"
if "$TMP/oracle-import/tools/docs/check-selected-provider-local-supply-live-evidence-orchestration-production-implementation-review" >"$TMP/oracle-import.log" 2>&1; then
  echo 'live-evidence-orchestration-smoke: FAIL: accepted synthetic CLI import accepted' >&2
  exit 1
fi
echo 'live-evidence-orchestration-smoke: PASS: accepted synthetic CLI import rejected'

cp -a "$ROOT" "$TMP/failure-gap"
python3 - "$TMP/failure-gap" <<'PY'
import json,sys
from pathlib import Path
root=Path(sys.argv[1])
p=root/'experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-evidence-orchestration-production-implementation-negative-cases.json'
d=json.loads(p.read_text()); d['cases'].pop(); d['case_count']=27
p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PY
if "$TMP/failure-gap/tools/docs/check-selected-provider-local-supply-live-evidence-orchestration-production-implementation-review" >"$TMP/failure-gap.log" 2>&1; then
  echo 'live-evidence-orchestration-smoke: FAIL: failure coverage gap accepted' >&2
  exit 1
fi
echo 'live-evidence-orchestration-smoke: PASS: failure coverage gap rejected'

echo 'live-evidence-orchestration-smoke: all checks passed'
