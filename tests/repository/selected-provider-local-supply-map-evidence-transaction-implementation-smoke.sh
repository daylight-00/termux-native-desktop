#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
CHECK="$ROOT/tools/docs/check-selected-provider-local-supply-map-evidence-transaction-implementation-review"
SOURCE="$ROOT/experiments/glibc/selected-obsidian-provider-authority/implementation/selected_provider_local_supply_map_evidence_transaction_candidate.py"
FIXTURE="$ROOT/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-implementation-synthetic-fixture.json"
TMP_ROOT=${TMPDIR:-"${HOME:-$ROOT}/.cache"}
mkdir -p "$TMP_ROOT"
TMP=$(mktemp -d "$TMP_ROOT/lsme-implementation-smoke.XXXXXX")
trap 'rm -rf "$TMP"' EXIT
"$CHECK"
python3 "$SOURCE" --repo-root "$ROOT" --fixture "$FIXTURE" --case success >/dev/null
set +e
python3 "$SOURCE" --repo-root "$ROOT" --fixture "$FIXTURE" --case discovery-attempt >"$TMP/discovery.json"
rc=$?
set -e
[ "$rc" -eq 2 ]
python3 - "$TMP/discovery.json" <<'PY2'
import json,sys
from pathlib import Path
r=json.loads(Path(sys.argv[1]).read_text())
assert r['failure_id']=='LSME-FAIL-005'
assert r['current_provider_read_count']==0
assert r['current_write_count']==0
assert r['current_live_authority_count']==0
assert r['provider_paths_opened']==[]
PY2
cp -a "$ROOT" "$TMP/live-path"
python3 - "$TMP/live-path" <<'PY2'
import json,sys
from pathlib import Path
root=Path(sys.argv[1]);p=root/'experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-implementation-synthetic-fixture.json'
d=json.loads(p.read_text());d['coordinate_receipt']['rows'][0]['absolute_canonical_path']='/data/data/com.termux/files/usr/glibc/lib/live.so';p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PY2
if "$TMP/live-path/tools/docs/check-selected-provider-local-supply-map-evidence-transaction-implementation-review" >"$TMP/live-path.log" 2>&1;then echo 'implementation-smoke: FAIL: live path accepted' >&2;exit 1;fi
echo 'implementation-smoke: PASS: live path rejected'
cp -a "$ROOT" "$TMP/read-widen"
sed -i $'s/current_provider_read_count\t0/current_provider_read_count\t1/' "$TMP/read-widen/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-implementation-metadata.tsv"
if "$TMP/read-widen/tools/docs/check-selected-provider-local-supply-map-evidence-transaction-implementation-review" >"$TMP/read-widen.log" 2>&1;then echo 'implementation-smoke: FAIL: read widening accepted' >&2;exit 1;fi
echo 'implementation-smoke: PASS: read widening rejected'
cp -a "$ROOT" "$TMP/failure-gap"
python3 - "$TMP/failure-gap" <<'PY2'
import json,sys
from pathlib import Path
root=Path(sys.argv[1]);p=root/'experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-implementation-negative-cases.json'
d=json.loads(p.read_text());d['cases'].pop();d['case_count']=17;p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PY2
if "$TMP/failure-gap/tools/docs/check-selected-provider-local-supply-map-evidence-transaction-implementation-review" >"$TMP/failure-gap.log" 2>&1;then echo 'implementation-smoke: FAIL: failure gap accepted' >&2;exit 1;fi
echo 'implementation-smoke: PASS: failure gap rejected'
echo 'implementation-smoke: all checks passed'
