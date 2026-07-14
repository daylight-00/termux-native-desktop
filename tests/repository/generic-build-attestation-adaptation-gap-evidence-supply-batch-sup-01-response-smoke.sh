#!/usr/bin/env bash
set -euo pipefail
root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
base="$root/experiments/glibc/selected-obsidian-provider-authority"
review="$base/review"
recipe="$base/recipe"
tracked="$base/evidence-supply/responses/SUP-01/SRQ-OJ-001"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

run_generator() {
    python3 "$recipe/prepare-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-01-response.py" \
        --source-contracts "$review/generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv" \
        --requirements "$review/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv" \
        --objects "$review/generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv" \
        --batches "$review/generic-build-attestation-adaptation-gap-evidence-supply-batches.tsv" \
        --requests "$review/generic-build-attestation-adaptation-gap-evidence-supply-requests.tsv" \
        --out "$1"
}

run_generator "$tmp/generated" >"$tmp/generator.log"
diff -ruN "$tracked" "$tmp/generated"
grep -Fx 'SUP_01_RESPONSE=PASS_BOUNDED' "$tmp/generator.log"
grep -Fx 'PROPOSED_REQUIRED_IDENTITY=libjpeg.so.62' "$tmp/generator.log"
grep -Fx 'REJECTED_SUBSTITUTE_IDENTITY=libjpeg.so.8' "$tmp/generator.log"
grep -Fx 'MATCHING_PROVIDER_CANDIDATES_BOUND=0' "$tmp/generator.log"

grep -F $'libjpeg.so.62\tlibjpeg.so.8\t' "$tmp/generated/acquisition-input/object-requirement-correction-review.tsv"
grep -F 'NO_MATCHING_SONAME_62_CANDIDATE_BOUND' "$tmp/generated/acquisition-input/object-requirement-correction-review.tsv"
! grep -F $'required_identity\tlibjpeg.so.8' "$tmp/generated/acquisition-input/object-requirement-correction-review.tsv"

python3 "$recipe/acquire-generic-build-attestation-and-adaptation-gap-evidence.py" \
    --source-contracts "$review/generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv" \
    --lanes "$review/generic-build-attestation-adaptation-gap-evidence-acquisition-lanes.tsv" \
    --requirements "$review/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv" \
    --roots "$review/generic-build-attestation-adaptation-root-gap-evidence-acquisition-set.tsv" \
    --objects "$review/generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv" \
    --input-root "$tmp/generated/acquisition-input" \
    --out "$tmp/acquired"
[ "$(awk -F '\t' '$1=="candidate_evidence_files_acquired"{print $2}' "$tmp/acquired/summary.tsv")" = 1 ]
[ "$(awk -F '\t' '$1=="candidate_requirements"{print $2}' "$tmp/acquired/summary.tsv")" = 1 ]
[ "$(awk -F '\t' '$1=="object_corrections_accepted"{print $2}' "$tmp/acquired/summary.tsv")" = 0 ]
[ "$(awk -F '\t' '$1=="final_provider_decisions_accepted"{print $2}' "$tmp/acquired/summary.tsv")" = 0 ]
[ "$(awk -F '\t' '$1=="target_rows_populated"{print $2}' "$tmp/acquired/summary.tsv")" = 0 ]
[ "$(($(wc -l < "$tmp/acquired/evidence-root/evidence-manifest.tsv") - 1))" = 1 ]

for name in source-contracts requirements objects batches requests; do
    mkdir "$tmp/tamper-$name"
    cp "$review/generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv" "$tmp/tamper-$name/source.tsv"
    cp "$review/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv" "$tmp/tamper-$name/requirements.tsv"
    cp "$review/generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv" "$tmp/tamper-$name/objects.tsv"
    cp "$review/generic-build-attestation-adaptation-gap-evidence-supply-batches.tsv" "$tmp/tamper-$name/batches.tsv"
    cp "$review/generic-build-attestation-adaptation-gap-evidence-supply-requests.tsv" "$tmp/tamper-$name/requests.tsv"
done
sed -i 's/NO_ABI_FAMILY_SUBSTITUTION/ALLOW_ABI_FAMILY_SUBSTITUTION/' "$tmp/tamper-source-contracts/source.tsv"
sed -i 's/LIBJPEG_EXPECTED_SONAME_REQUIREMENT/LIBJPEG_ABI_FAMILY_REQUIREMENT/' "$tmp/tamper-requirements/requirements.tsv"
sed -i 's/libjpeg.so.62.3.0/libjpeg.so.8.3.2/' "$tmp/tamper-objects/objects.tsv"
sed -i 's/NO_LIBJPEG_SO_8_SUBSTITUTION/ALLOW_LIBJPEG_SO_8_SUBSTITUTION/' "$tmp/tamper-batches/batches.tsv"
sed -i 's/AUTHORITATIVE_REFERENCE_REQUIRED/ABI_FAMILY_REFERENCE_ALLOWED/' "$tmp/tamper-requests/requests.tsv"
for name in source-contracts requirements objects batches requests; do
    set +e
    python3 "$recipe/prepare-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-01-response.py" \
        --source-contracts "$tmp/tamper-$name/source.tsv" \
        --requirements "$tmp/tamper-$name/requirements.tsv" \
        --objects "$tmp/tamper-$name/objects.tsv" \
        --batches "$tmp/tamper-$name/batches.tsv" \
        --requests "$tmp/tamper-$name/requests.tsv" \
        --out "$tmp/reject-$name" >/dev/null 2>&1
    rc=$?
    set -e
    [ "$rc" -ne 0 ]
done

printf '%s\n' 'generic gap evidence SUP-01 response smoke: PASS'
