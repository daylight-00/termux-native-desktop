#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}};mkdir -p "$TMP_BASE";FIXTURE=$(mktemp -d "$TMP_BASE/local-supply-contract.XXXXXX");trap 'rm -rf "$FIXTURE"' EXIT
git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
python3 "$FIXTURE/tools/docs/check-selected-provider-local-supply-map-contract-review" >/dev/null
TABLE=experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-contract.tsv
python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]);s=p.read_text();s=s.replace('\tUNBOUND_CONTRACT_ONLY\t\t','\tUNBOUND_CONTRACT_ONLY\t/data/local/provider.so\t',1);p.write_text(s)
PY
if python3 "$FIXTURE/tools/docs/check-selected-provider-local-supply-map-contract-review" >/dev/null 2>&1;then echo 'local supply contract smoke: populated path accepted' >&2;exit 1;fi
git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"
python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]);lines=p.read_text().splitlines();p.write_text('\n'.join(lines[:-1])+'\n')
PY
if python3 "$FIXTURE/tools/docs/check-selected-provider-local-supply-map-contract-review" >/dev/null 2>&1;then echo 'local supply contract smoke: incomplete row set accepted' >&2;exit 1;fi
git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"
python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]);s=p.read_text();s=s.replace('EXISTING_AUTHORITY_DIGEST_SENTINEL','RESULT_INDEX_SHA256',1);p.write_text(s)
PY
if python3 "$FIXTURE/tools/docs/check-selected-provider-local-supply-map-contract-review" >/dev/null 2>&1;then echo 'local supply contract smoke: index-kind drift accepted' >&2;exit 1;fi
echo 'selected provider local supply map contract smoke: PASS'
