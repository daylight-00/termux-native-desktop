#!/usr/bin/env bash
set -euo pipefail

PROJECT_REPO=${PROJECT_REPO:-$(CDPATH= cd -- "$(dirname -- "$0")/../../../.." && pwd)}
BASE="$PROJECT_REPO/experiments/glibc/selected-obsidian-provider-authority"
REVIEW="$BASE/review"
OUT=${OUT:-$BASE/work/results/generic-build-attestation-and-adaptation-gap-evidence-acquisition}
INPUT_ROOT=${GENERIC_GAP_ACQUISITION_INPUT_ROOT:-$HOME/.cache/hw-t-evidence/termux-native-desktop/generic-build-attestation-adaptation-gap-acquisition-input}
ACQUIRER="$BASE/recipe/acquire-generic-build-attestation-and-adaptation-gap-evidence.py"

for command in python3 sha256sum; do
    command -v "$command" >/dev/null 2>&1 || { printf 'missing required command: %s\n' "$command" >&2; exit 2; }
done
[ -f "$ACQUIRER" ] || { printf 'missing acquirer: %s\n' "$ACQUIRER" >&2; exit 2; }
[ ! -e "$OUT" ] && [ ! -L "$OUT" ] || { printf 'refusing existing output: %s\n' "$OUT" >&2; exit 2; }

PYTHONDONTWRITEBYTECODE=1 python3 "$ACQUIRER" \
  --source-contracts "$REVIEW/generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv" \
  --lanes "$REVIEW/generic-build-attestation-adaptation-gap-evidence-acquisition-lanes.tsv" \
  --requirements "$REVIEW/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv" \
  --roots "$REVIEW/generic-build-attestation-adaptation-root-gap-evidence-acquisition-set.tsv" \
  --objects "$REVIEW/generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv" \
  --input-root "$INPUT_ROOT" \
  --out "$OUT"

printf 'GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUIRER=PASS\n'
printf 'OUTPUT=%s\n' "$OUT"
printf 'EVIDENCE_ROOT=%s\n' "$OUT/evidence-root"
