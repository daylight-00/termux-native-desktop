#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"; F=$(mktemp -d "$TMP_BASE/coord-gen-smoke.XXXXXX"); trap 'rm -rf "$F"' EXIT
git -C "$ROOT" archive HEAD | tar -xf - -C "$F"
python3 "$F/tools/docs/check-retained-result-coordinate-generation-contract-review" >/dev/null
T="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-target-coordinate-generation-contract-metadata.tsv"
sed -i 's/population_authorized	NO/population_authorized	YES/' "$T"
if python3 "$F/tools/docs/check-retained-result-coordinate-generation-contract-review" >/dev/null 2>&1; then echo widening accepted >&2; exit 1; fi
echo 'retained result coordinate and generation contract review smoke: PASS'
