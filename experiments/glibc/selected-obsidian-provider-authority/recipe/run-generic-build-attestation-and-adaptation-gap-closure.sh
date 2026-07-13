#!/usr/bin/env bash
set -euo pipefail

PROJECT_REPO=${PROJECT_REPO:-$(CDPATH= cd -- "$(dirname -- "$0")/../../../.." && pwd)}
BASE="$PROJECT_REPO/experiments/glibc/selected-obsidian-provider-authority"
OUT=${OUT:-$BASE/work/results/generic-build-attestation-and-adaptation-gap-closure}
EVIDENCE_ROOT=${GENERIC_GAP_EVIDENCE_ROOT:-$HOME/.cache/hw-t-evidence/termux-native-desktop/generic-build-attestation-adaptation-gap-closure}
COLLECTOR="$BASE/recipe/collect-generic-build-attestation-and-adaptation-gap-closure.py"

for command in python3 sha256sum; do
    command -v "$command" >/dev/null 2>&1 || { printf 'missing required command: %s\n' "$command" >&2; exit 2; }
done
[ -f "$COLLECTOR" ] || { printf 'missing collector: %s\n' "$COLLECTOR" >&2; exit 2; }
[ ! -e "$OUT" ] && [ ! -L "$OUT" ] || { printf 'refusing existing output: %s\n' "$OUT" >&2; exit 2; }

PROJECT_REPO="$PROJECT_REPO" \
OUT="$OUT" \
GENERIC_GAP_EVIDENCE_ROOT="$EVIDENCE_ROOT" \
PYTHONDONTWRITEBYTECODE=1 \
python3 "$COLLECTOR"

printf 'GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE=PASS\n'
printf 'OUTPUT=%s\n' "$OUT"
