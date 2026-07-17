#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
"$ROOT/tools/docs/check-libcloudproviders-bounded-provider-authority"
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"; TMP=$(mktemp -d "$TMP_BASE/libcloudproviders-provider-smoke.XXXXXX"); trap 'rm -rf "$TMP"' EXIT
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
python3 - "$TMP" <<'PY'
from pathlib import Path
import csv,sys
root=Path(sys.argv[1]);p=root/'experiments/glibc/selected-obsidian-provider-authority/review/libcloudproviders-bounded-provider-authority.tsv'
rows=[]
with p.open(newline='',encoding='utf-8') as f:
 rd=csv.DictReader(f,delimiter='\t'); fields=rd.fieldnames; rows=list(rd)
rows[0]['dependency_boundary']='DBUS_SERVICES_AND_ACCOUNTS_ACCEPTED'
with p.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
PY
if "$TMP/tools/docs/check-libcloudproviders-bounded-provider-authority" >/dev/null 2>&1; then echo 'libcloudproviders smoke: widening mutation accepted' >&2; exit 1; fi
echo 'libcloudproviders smoke: PASS'
