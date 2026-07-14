#!/usr/bin/env bash
set -euo pipefail

PROJECT_REPO=${PROJECT_REPO:-$(CDPATH= cd -- "$(dirname -- "$0")/../../../.." && pwd)}
BASE="$PROJECT_REPO/experiments/glibc/selected-obsidian-provider-authority"
ISSUANCE="$BASE/evidence-supply/requests/SUP-02/custodian-export"
ACQUIRER="$BASE/recipe/acquire-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-responses.py"
INPUT_ROOT=${SUP02_CUSTODIAN_EXPORT_RESPONSE_ROOT:-$HOME/.cache/hw-t-evidence/termux-native-desktop/sup-02-custodian-export-responses}
OUT=${OUT:-$BASE/work/results/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-acquisition}
SOURCE_HEAD=${SOURCE_HEAD:-636aad838111d37be0ab8bd8364aa5795b32256d}
SOURCE_TREE=${SOURCE_TREE:-3a20228415cb835267e34ea0c10be6297d00cdaf}

for command in python3 sha256sum; do
    command -v "$command" >/dev/null 2>&1 || { printf 'missing required command: %s\n' "$command" >&2; exit 2; }
done
[ -f "$ACQUIRER" ] || { printf 'missing acquirer: %s\n' "$ACQUIRER" >&2; exit 2; }
[ ! -e "$OUT" ] && [ ! -L "$OUT" ] || { printf 'refusing existing output: %s\n' "$OUT" >&2; exit 2; }

PYTHONDONTWRITEBYTECODE=1 python3 "$ACQUIRER" \
  --request-issuance "$ISSUANCE/custodian-export-request-issuance.tsv" \
  --record-contract-issuance "$ISSUANCE/custodian-export-record-contract-issuance.tsv" \
  --input-root "$INPUT_ROOT" \
  --source-head "$SOURCE_HEAD" \
  --source-tree "$SOURCE_TREE" \
  --out "$OUT"

printf 'OUTPUT=%s\n' "$OUT"
printf 'CANDIDATE_RESPONSE_ROOT=%s\n' "$OUT/candidate-response-root"
