#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
CHECK="$ROOT/tools/docs/check-selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-review"
GEN="$ROOT/experiments/glibc/selected-obsidian-provider-authority/recipe/generate-selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation.py"

"$CHECK"

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/repo"
git -C "$ROOT" archive HEAD | tar -x -C "$TMP/repo"

python3 "$GEN" --repo-root "$TMP/repo" --output-root "$TMP/repro"
cmp "$TMP/repo/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-metadata.tsv" \
    "$TMP/repro/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-metadata.tsv"

expect_reject() {
  local label=$1
  if "$TMP/repo/tools/docs/check-selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-review" >"$TMP/$label.log" 2>&1; then
    printf 'implementation-smoke: FAIL: mutation accepted: %s\n' "$label" >&2
    exit 1
  fi
  printf 'implementation-smoke: PASS: mutation rejected: %s\n' "$label"
}

cp -a "$TMP/repo" "$TMP/live-mode"
sed -i 's/SYNTHETIC_REPOSITORY_FIXTURE_ONLY/LIVE_INPUT_MODE/' "$TMP/live-mode/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-metadata.tsv"
ROOT_SAVE=$ROOT
ROOT="$TMP/live-mode"
if "$ROOT/tools/docs/check-selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-review" >"$TMP/live-mode.log" 2>&1; then
  printf 'implementation-smoke: FAIL: live mode accepted\n' >&2; exit 1
fi
printf 'implementation-smoke: PASS: live mode rejected\n'
ROOT=$ROOT_SAVE

cp -a "$TMP/repo" "$TMP/live-coordinate"
python3 - "$TMP/live-coordinate" <<'PY'
from pathlib import Path
import json,sys
root=Path(sys.argv[1]);p=root/'experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-synthetic-fixture.json'
d=json.loads(p.read_text());d['coordinate_source']['rows'][0]['absolute_canonical_path']='/data/data/com.termux/files/usr/glibc/lib/live.so';p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PY
if "$TMP/live-coordinate/tools/docs/check-selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-review" >"$TMP/live-coordinate.log" 2>&1; then
  printf 'implementation-smoke: FAIL: live coordinate accepted\n' >&2; exit 1
fi
printf 'implementation-smoke: PASS: live coordinate rejected\n'

cp -a "$TMP/repo" "$TMP/provider-read"
sed -i 's/current_provider_read_count\t0/current_provider_read_count\t1/' "$TMP/provider-read/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-metadata.tsv"
if "$TMP/provider-read/tools/docs/check-selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-review" >"$TMP/provider-read.log" 2>&1; then
  printf 'implementation-smoke: FAIL: provider read widening accepted\n' >&2; exit 1
fi
printf 'implementation-smoke: PASS: provider read widening rejected\n'

cp -a "$TMP/repo" "$TMP/failure-gap"
python3 - "$TMP/failure-gap" <<'PY'
from pathlib import Path
import json,sys
root=Path(sys.argv[1]);p=root/'experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-negative-cases.json'
d=json.loads(p.read_text());d['cases'].pop();d['case_count']=19;p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
PY
if "$TMP/failure-gap/tools/docs/check-selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-review" >"$TMP/failure-gap.log" 2>&1; then
  printf 'implementation-smoke: FAIL: failure coverage gap accepted\n' >&2; exit 1
fi
printf 'implementation-smoke: PASS: failure coverage gap rejected\n'

printf 'implementation-smoke: all checks passed\n'
