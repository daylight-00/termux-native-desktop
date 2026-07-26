#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}};mkdir -p "$TMP_BASE";F=$(mktemp -d "$TMP_BASE/materializer-design-acceptance.XXXXXX");trap 'rm -rf "$F"' EXIT
git -C "$ROOT" archive HEAD | tar -xf - -C "$F"
CHECK="$F/tools/docs/check-selected-target-materializer-runtime-preflight-design-boundary-acceptance"
ACC="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-target-materializer-runtime-preflight-design-boundary-acceptance.tsv"
META="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-target-materializer-design-metadata.tsv"
python3 "$CHECK" >/dev/null
sed -i 's/NOT_AUTHORIZED_SEPARATE_EXPLICIT_DECISION_REQUIRED/AUTHORIZED/' "$ACC"
if python3 "$CHECK" >/dev/null 2>&1; then echo 'execution authorization widening accepted' >&2;exit 1;fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-target-materializer-runtime-preflight-design-boundary-acceptance.tsv > "$ACC"
sed -i 's/execution_authorized	NO/execution_authorized	YES/' "$META"
if python3 "$CHECK" >/dev/null 2>&1; then echo 'candidate execution widening accepted' >&2;exit 1;fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-target-materializer-design-metadata.tsv > "$META"
python3 - "$ACC" <<'PYINNER'
from pathlib import Path
import sys
p=Path(sys.argv[1]);p.write_text(p.read_text().replace('HARDLINK_ONLY_FROM_VERIFIED_CONTENT_ADDRESS_STORE_NO_COPY_FALLBACK','HARDLINK_OR_COPY_FALLBACK',1))
PYINNER
if python3 "$CHECK" >/dev/null 2>&1; then echo 'copy fallback accepted' >&2;exit 1;fi
echo 'selected-provider materializer/runtime-preflight design boundary acceptance smoke: PASS'
