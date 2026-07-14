#!/usr/bin/env bash
set -euo pipefail
repo=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
base="$repo/experiments/glibc/selected-obsidian-provider-authority"
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
python3 "$base/recipe/define-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-request-set.py" \
  --root-review "$base/review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-root-provenance-locator-receipt-review.tsv" \
  --source-head fb73cf6129ebefffed8c44532e18bf1a2bae411f --source-tree a338f3fa370cb59713400e61e802b515f6494fd4 --out "$tmp/out"
for f in generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-requests.tsv generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-record-contracts.tsv generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-request-set-metadata.tsv; do
 cmp "$tmp/out/$f" "$base/review/$f"
done
[[ $(awk 'END{print NR-1}' "$tmp/out/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-requests.tsv") == 28 ]]
[[ $(awk 'END{print NR-1}' "$tmp/out/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-record-contracts.tsv") == 84 ]]
! grep -v $'\tREQUEST_DEFINED_NOT_ISSUED\t' "$tmp/out/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-requests.tsv" | tail -n +2 | grep .
# Negative: locator-state drift must fail closed.
cp "$base/review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-root-provenance-locator-receipt-review.tsv" "$tmp/bad.tsv"
sed -i '0,/CONFIRMED_NO_EXISTING_CUSTODIAN_EXPORT/s//COMPLETE_CUSTODIAN_EXPORT_FOUND/' "$tmp/bad.tsv"
if python3 "$base/recipe/define-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-request-set.py" --root-review "$tmp/bad.tsv" --source-head x --source-tree y --out "$tmp/badout" >/dev/null 2>&1; then
 echo 'negative locator-state drift unexpectedly accepted' >&2; exit 1
fi
printf 'PASS\n'
