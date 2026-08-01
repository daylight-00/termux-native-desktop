#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
CHECK="$ROOT/tools/docs/check-selected-provider-local-supply-map-production-boundary-acceptance"
"$CHECK" >/dev/null
TMP=$(mktemp -d "${TMPDIR:-/tmp}/map-production-acceptance-smoke.XXXXXX")
trap 'rm -rf "$TMP"' EXIT
cp -a "$ROOT/." "$TMP/repo"
python3 - "$TMP/repo/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-production-boundary-acceptance.tsv" <<'PY2'
from pathlib import Path
import sys
p=Path(sys.argv[1]);s=p.read_text();p.write_text(s.replace('	NO	NO	NO	NO	NO	NO	await-explicit-owner-decision', '	YES	NO	NO	NO	NO	NO	await-explicit-owner-decision',1))
PY2
if "$TMP/repo/tools/docs/check-selected-provider-local-supply-map-production-boundary-acceptance" >/dev/null 2>&1; then
 echo 'local-supply map production acceptance smoke: FAIL: target-population authority mutation accepted' >&2; exit 1
fi
echo 'local-supply map production acceptance smoke: PASS'
