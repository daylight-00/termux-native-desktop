#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"; F=$(mktemp -d "$TMP_BASE/pixman-budget-smoke.XXXXXX"); trap 'rm -rf "$F"' EXIT
git -C "$ROOT" archive HEAD | tar -xf - -C "$F"
python3 "$F/tools/docs/check-selected-target-pixman-size-resource-budget-intervention-review" >/dev/null
META="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-target-resource-budget-metadata.tsv"
sed -i 's/target_population_authorized\tNO/target_population_authorized\tYES/' "$META"
if python3 "$F/tools/docs/check-selected-target-pixman-size-resource-budget-intervention-review" >/dev/null 2>&1; then echo population widening accepted >&2; exit 1; fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-target-resource-budget-metadata.tsv > "$META"
sed -i 's/pixman_member_size_bytes\t460920/pixman_member_size_bytes\t152856/' "$META"
if python3 "$F/tools/docs/check-selected-target-pixman-size-resource-budget-intervention-review" >/dev/null 2>&1; then echo package size substitution accepted >&2; exit 1; fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-target-resource-budget-metadata.tsv > "$META"
sed -i 's/receipt_overhead_budget_bytes\t1048576/receipt_overhead_budget_bytes\t44332/' "$META"
if python3 "$F/tools/docs/check-selected-target-pixman-size-resource-budget-intervention-review" >/dev/null 2>&1; then echo unreserved receipt overhead accepted >&2; exit 1; fi
echo 'selected target Pixman size/resource/intervention review smoke: PASS'
