#!/usr/bin/env bash
set -euo pipefail

PROJECT_REPO=${PROJECT_REPO:-$(CDPATH= cd -- "$(dirname -- "$0")/../../../.." && pwd)}
BASE="$PROJECT_REPO/experiments/glibc/selected-obsidian-provider-authority"
OUT=${OUT:-$BASE/work/results/generic-build-attestation-and-adaptation-evidence}
SOURCE_REPO=${GENERIC_SOURCE_REPO:-$BASE/work/source/termux-pacman-glibc-packages}
ARTIFACT_CACHE=${GENERIC_ARTIFACT_CACHE:-$BASE/work/artifacts/generic-artifact-member-inventory}
FOUNDATION="$OUT/foundation-recipe-binding-and-drift-target"
FOUNDATION_COLLECTOR="$BASE/recipe/collect-generic-recipe-binding-and-drift-target-elf.py"
COLLECTOR="$BASE/recipe/collect-generic-build-attestation-and-adaptation-evidence.py"

for command in git python3 dpkg-deb sha256sum; do
    command -v "$command" >/dev/null 2>&1 || { printf 'missing required command: %s\n' "$command" >&2; exit 2; }
done
for path in "$FOUNDATION_COLLECTOR" "$COLLECTOR"; do
    [ -f "$path" ] || { printf 'missing required input: %s\n' "$path" >&2; exit 2; }
done
[ -d "$SOURCE_REPO/.git" ] || { printf 'missing pinned source checkout: %s\n' "$SOURCE_REPO" >&2; exit 2; }
[ -d "$ARTIFACT_CACHE" ] || { printf 'missing verified artifact cache: %s\n' "$ARTIFACT_CACHE" >&2; exit 2; }
[ ! -e "$OUT" ] && [ ! -L "$OUT" ] || { printf 'refusing existing output: %s\n' "$OUT" >&2; exit 2; }
mkdir -p "$OUT"

PROJECT_REPO="$PROJECT_REPO" \
OUT="$FOUNDATION" \
GENERIC_SOURCE_REPO="$SOURCE_REPO" \
GENERIC_ARTIFACT_CACHE="$ARTIFACT_CACHE" \
python3 "$FOUNDATION_COLLECTOR"

PROJECT_REPO="$PROJECT_REPO" \
OUT="$OUT/evidence" \
GENERIC_EVIDENCE_FOUNDATION_OUT="$FOUNDATION" \
GENERIC_SOURCE_REPO="$SOURCE_REPO" \
python3 "$COLLECTOR"

cp "$OUT/evidence/analysis.status" "$OUT/analysis.status"
cp "$OUT/evidence/claim-boundary.txt" "$OUT/claim-boundary.txt"
cp "$OUT/evidence/next-state.txt" "$OUT/next-state.txt"
cp "$OUT/evidence/summary.tsv" "$OUT/summary.tsv"
printf 'GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE=PASS\n'
printf 'OUTPUT=%s\n' "$OUT"
