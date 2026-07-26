#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
F=$(mktemp -d "$TMP_BASE/materializer-design-smoke.XXXXXX")
trap 'rm -rf "$F"' EXIT
git -C "$ROOT" archive HEAD | tar -xf - -C "$F"
CHECK="$F/tools/docs/check-selected-target-materializer-runtime-preflight-design-review"
META="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-target-materializer-design-metadata.tsv"
OPS="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-target-materializer-operation-contract.tsv"
PREF="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-target-runtime-preflight-contract.tsv"
python3 "$CHECK" >/dev/null
sed -i 's/execution_authorized\tNO/execution_authorized\tYES/' "$META"
if python3 "$CHECK" >/dev/null 2>&1; then echo 'execution authority widening accepted' >&2; exit 1; fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-target-materializer-design-metadata.tsv > "$META"
sed -i 's/HARDLINK_ONLY_NO_COPY_FALLBACK/HARDLINK_OR_COPY_FALLBACK/' "$OPS"
if python3 "$CHECK" >/dev/null 2>&1; then echo 'copy fallback accepted' >&2; exit 1; fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-target-materializer-operation-contract.tsv > "$OPS"
sed -i 's/STATVFS_AVAILABLE_BYTES_AT_LEAST_59142800/STATVFS_AVAILABLE_BYTES_AT_LEAST_58000000/' "$PREF"
if python3 "$CHECK" >/dev/null 2>&1; then echo 'under-budget preflight accepted' >&2; exit 1; fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-target-runtime-preflight-contract.tsv > "$PREF"
python3 - "$OPS" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]);t=p.read_text();t=t.replace('MAT-OP-021\t21\tPUBLISH_PREVIOUS_SELECTOR','MAT-OP-021\t23\tPUBLISH_PREVIOUS_SELECTOR').replace('MAT-OP-023\t23\tWRITE_COMPLETION_RECEIPT','MAT-OP-023\t21\tWRITE_COMPLETION_RECEIPT');p.write_text(t)
PY
if python3 "$CHECK" >/dev/null 2>&1; then echo 'selector ordering drift accepted' >&2; exit 1; fi
echo 'selected-provider materializer/runtime-preflight design review smoke: PASS'
