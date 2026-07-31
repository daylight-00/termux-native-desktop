#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
CHECK="$ROOT/tools/docs/check-selected-provider-local-supply-live-authority-transaction-production-exact-input-set-correction-bootstrap-boundary-acceptance"
"$CHECK" >/dev/null
TMP=$(mktemp -d "${TMPDIR:-/tmp}/prod-bootstrap-acceptance-smoke.XXXXXX")
trap 'rm -rf "$TMP"' EXIT
cp -a "$ROOT/." "$TMP/repo"
python3 - "$TMP/repo/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-live-authority-transaction-production-exact-input-set-correction-bootstrap-boundary-acceptance.tsv" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text(); p.write_text(s.replace("\t0\t0\t0\t0\t0\t0\t0\tACCEPTED_EXTERNAL", "\t0\t0\t0\t0\t0\t0\t1\tACCEPTED_EXTERNAL",1))
PY
if "$TMP/repo/tools/docs/check-selected-provider-local-supply-live-authority-transaction-production-exact-input-set-correction-bootstrap-boundary-acceptance" >/dev/null 2>&1; then
  echo "production exact input-set bootstrap acceptance smoke: FAIL: authority mutation accepted" >&2; exit 1
fi
echo "production exact input-set bootstrap acceptance smoke: PASS"
