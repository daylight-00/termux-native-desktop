#!/usr/bin/env bash
set -euo pipefail
ROOT=${1:-$(git rev-parse --show-toplevel)}
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
TMP=$(mktemp -d "$TMP_BASE/libxdamage-candidate-review.XXXXXX"); trap 'rm -rf "$TMP"' EXIT
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
"$TMP/tools/docs/check-libxdamage-production-recipe-candidate-result-review" >/dev/null
printf '\ntermux_step_pre_configure() { :; }\n' >> "$TMP/experiments/glibc/selected-obsidian-provider-authority/candidates/libxdamage-glibc/gpkg/libxdamage/build.sh"
if "$TMP/tools/docs/check-libxdamage-production-recipe-candidate-result-review" >/dev/null 2>&1; then
 echo 'libxdamage-candidate-review-smoke: FAIL: private harness leakage was accepted' >&2; exit 1
fi
echo 'libxdamage-candidate-review-smoke: PASS: exact candidate hashes and production/harness separation are enforced'
