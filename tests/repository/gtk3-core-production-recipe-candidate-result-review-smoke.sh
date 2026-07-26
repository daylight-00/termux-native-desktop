#!/usr/bin/env bash
set -euo pipefail
ROOT=${1:-$(git rev-parse --show-toplevel)}
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
TMP=$(mktemp -d "$TMP_BASE/gtk3-core-candidate-review.XXXXXX"); trap 'rm -rf "$TMP"' EXIT
files=(
 docs/evidence/gtk3-core-production-recipe-candidate-result-review.md docs/evidence/gtk3-core-bounded-provider-authority.md
 experiments/glibc/selected-obsidian-provider-authority/review/gtk3-core-production-recipe-candidate-result-review.tsv
 experiments/glibc/selected-obsidian-provider-authority/review/gtk3-core-bounded-provider-authority.tsv
 experiments/glibc/selected-obsidian-provider-authority/candidates/gtk3-glibc/gpkg/gtk3/build.sh
 experiments/glibc/selected-obsidian-provider-authority/candidates/gtk3-glibc/gtk3-glibc-contribution.patch
 tools/docs/check-gtk3-core-production-recipe-candidate-result-review
)
for rel in "${files[@]}"; do mkdir -p "$TMP/$(dirname "$rel")"; cp "$ROOT/$rel" "$TMP/$rel"; done
chmod +x "$TMP/tools/docs/check-gtk3-core-production-recipe-candidate-result-review"
TND_CHECK_ROOT="$TMP" "$TMP/tools/docs/check-gtk3-core-production-recipe-candidate-result-review" >/dev/null
printf '\nTND_ISOLATED_LEAK=1\n' >> "$TMP/experiments/glibc/selected-obsidian-provider-authority/candidates/gtk3-glibc/gpkg/gtk3/build.sh"
if TND_CHECK_ROOT="$TMP" "$TMP/tools/docs/check-gtk3-core-production-recipe-candidate-result-review" >/dev/null 2>&1; then echo 'gtk3-core-candidate-review-smoke: FAIL: qualification harness leakage was accepted' >&2; exit 1; fi
echo 'gtk3-core-candidate-review-smoke: PASS'
