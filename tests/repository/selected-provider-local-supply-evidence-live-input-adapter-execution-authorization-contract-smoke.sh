#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
CHECK="$ROOT/tools/docs/check-selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-review"
GEN="$ROOT/experiments/glibc/selected-obsidian-provider-authority/recipe/generate-selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract.py"

"$CHECK"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/repo"
git -C "$ROOT" archive HEAD | tar -x -C "$TMP/repo"

python3 "$GEN" --repo-root "$TMP/repo" --output-root "$TMP/repro"
cmp "$TMP/repo/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-metadata.tsv" \
    "$TMP/repro/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-metadata.tsv"

cp -a "$TMP/repo" "$TMP/live-state"
sed -i 's/current_live_input_count\t0/current_live_input_count\t1/' "$TMP/live-state/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-metadata.tsv"
if "$TMP/live-state/tools/docs/check-selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-review" >"$TMP/live-state.log" 2>&1; then
  printf 'live-input-contract-smoke: FAIL: live state accepted\n' >&2; exit 1
fi
printf 'live-input-contract-smoke: PASS: live state rejected\n'

cp -a "$TMP/repo" "$TMP/rewrite"
python3 - "$TMP/rewrite" <<'PY'
from pathlib import Path
import json,sys
root=Path(sys.argv[1]);p=root/'experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-contract.json'
d=json.loads(p.read_text());d['accepted_synthetic_implementation']['live_path_rewrite_to_synthetic_namespace']='ALLOWED';p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PY
if "$TMP/rewrite/tools/docs/check-selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-review" >"$TMP/rewrite.log" 2>&1; then
  printf 'live-input-contract-smoke: FAIL: synthetic rewrite accepted\n' >&2; exit 1
fi
printf 'live-input-contract-smoke: PASS: synthetic rewrite rejected\n'

cp -a "$TMP/repo" "$TMP/claim-gap"
python3 - "$TMP/claim-gap" <<'PY'
from pathlib import Path
import json,sys
root=Path(sys.argv[1]);p=root/'experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-execution-authorization-schema.json'
d=json.loads(p.read_text());d['required_claims'].pop();d['required_claim_count']=26;p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PY
if "$TMP/claim-gap/tools/docs/check-selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-review" >"$TMP/claim-gap.log" 2>&1; then
  printf 'live-input-contract-smoke: FAIL: execution claim gap accepted\n' >&2; exit 1
fi
printf 'live-input-contract-smoke: PASS: execution claim gap rejected\n'

cp -a "$TMP/repo" "$TMP/oracle-role"
python3 - "$TMP/oracle-role" <<'PY'
from pathlib import Path
import json,sys
root=Path(sys.argv[1]);p=root/'experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-contract.json'
d=json.loads(p.read_text());d['accepted_synthetic_implementation']['live_input_invocation_authority']='ALLOWED';p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PY
if "$TMP/oracle-role/tools/docs/check-selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-review" >"$TMP/oracle-role.log" 2>&1; then
  printf 'live-input-contract-smoke: FAIL: live synthetic invocation accepted\n' >&2; exit 1
fi
printf 'live-input-contract-smoke: PASS: live synthetic invocation rejected\n'

printf 'live-input-contract-smoke: all checks passed\n'
