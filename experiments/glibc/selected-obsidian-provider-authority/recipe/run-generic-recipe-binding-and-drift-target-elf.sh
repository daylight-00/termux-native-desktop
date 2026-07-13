#!/usr/bin/env bash
set -euo pipefail

PROJECT_REPO=${PROJECT_REPO:-$(CDPATH= cd -- "$(dirname -- "$0")/../../../.." && pwd)}
BASE="$PROJECT_REPO/experiments/glibc/selected-obsidian-provider-authority"
OUT=${OUT:-$BASE/work/results/generic-recipe-binding-and-drift-target-elf}
SOURCE_REPO=${GENERIC_SOURCE_REPO:-$BASE/work/source/termux-pacman-glibc-packages}
ARTIFACT_CACHE=${GENERIC_ARTIFACT_CACHE:-$BASE/work/artifacts/generic-artifact-member-inventory}
COLLECTOR="$BASE/recipe/collect-generic-recipe-binding-and-drift-target-elf.py"
RULES=${GENERIC_RECIPE_DRIFT_RULES:-$BASE/review/generic-recipe-binding-and-drift-target-rules.tsv}
ARTIFACTS=${GENERIC_COMPARISON_ARTIFACTS:-$BASE/review/generic-artifact-member-comparison-artifacts.tsv}

for command in git python3 dpkg-deb sha256sum; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 2
    }
done
for path in "$COLLECTOR" "$RULES" "$ARTIFACTS"; do
    [ -f "$path" ] || { printf 'missing required input: %s\n' "$path" >&2; exit 2; }
done
[ -d "$SOURCE_REPO/.git" ] || { printf 'missing pinned source checkout: %s\n' "$SOURCE_REPO" >&2; exit 2; }
[ -d "$ARTIFACT_CACHE" ] || { printf 'missing verified artifact cache: %s\n' "$ARTIFACT_CACHE" >&2; exit 2; }
[ ! -e "$OUT" ] && [ ! -L "$OUT" ] || { printf 'refusing existing output: %s\n' "$OUT" >&2; exit 2; }

PROJECT_REPO="$PROJECT_REPO" \
OUT="$OUT" \
GENERIC_SOURCE_REPO="$SOURCE_REPO" \
GENERIC_ARTIFACT_CACHE="$ARTIFACT_CACHE" \
GENERIC_RECIPE_DRIFT_RULES="$RULES" \
GENERIC_COMPARISON_ARTIFACTS="$ARTIFACTS" \
python3 "$COLLECTOR"

printf 'GENERIC_RECIPE_BINDING_AND_DRIFT_TARGET_ELF=PASS\n'
printf 'OUTPUT=%s\n' "$OUT"
