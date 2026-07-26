#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}};mkdir -p "$TMP_BASE";W=$(mktemp -d "$TMP_BASE/target-accept.XXXXXX");trap 'rm -rf "$W"' EXIT
git -C "$ROOT" archive HEAD | tar -xf - -C "$W"
python3 "$W/tools/docs/check-selected-target-manifest-boundary-acceptance" >/dev/null
A="$W/experiments/glibc/selected-obsidian-provider-authority/review/selected-target-manifest-boundary-acceptance.tsv"
sed -i 's/NOT_REVIEWED_NOT_LIFTED/LIFTED/' "$A"
if python3 "$W/tools/docs/check-selected-target-manifest-boundary-acceptance" >/dev/null 2>&1;then echo 'target acceptance smoke: intervention widening accepted' >&2;exit 1;fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-target-manifest-boundary-acceptance.tsv > "$A"
M="$W/experiments/glibc/selected-obsidian-provider-authority/review/selected-target-manifest.tsv"
sed -i '0,/UNPOPULATED_SCHEMA_ONLY/s//AUTHORIZED/' "$M"
if python3 "$W/tools/docs/check-selected-target-manifest-boundary-acceptance" >/dev/null 2>&1;then echo 'target acceptance smoke: population widening accepted' >&2;exit 1;fi
echo 'selected target manifest boundary acceptance smoke: PASS'
