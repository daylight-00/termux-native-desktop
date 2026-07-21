#!/usr/bin/env bash
set -euo pipefail
ROOT=${1:-$(git rev-parse --show-toplevel)}
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
TMP=$(mktemp -d "$TMP_BASE/atspi2-candidate-review.XXXXXX"); trap 'rm -rf "$TMP"' EXIT
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
"$TMP/tools/docs/check-at-spi2-core-production-recipe-candidate-result-review" >/dev/null
printf '\nTND_ISOLATED_LEAK=1\n' >> "$TMP/experiments/glibc/selected-obsidian-provider-authority/candidates/at-spi2-core-glibc/gpkg/at-spi2-core/build.sh"
if "$TMP/tools/docs/check-at-spi2-core-production-recipe-candidate-result-review" >/dev/null 2>&1; then
 echo 'atspi2-candidate-review-smoke: FAIL: private harness leakage was accepted' >&2; exit 1
fi
echo 'atspi2-candidate-review-smoke: PASS: exact candidate hashes, atomic family, disabled activation metadata, and production/harness separation are enforced'
