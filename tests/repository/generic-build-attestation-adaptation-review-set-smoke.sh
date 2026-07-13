#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
EXP="$ROOT/experiments/glibc/selected-obsidian-provider-authority"
REVIEW="$EXP/review"
RECIPE="$EXP/recipe"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

export PYTHONDONTWRITEBYTECODE=1
python3 "$RECIPE/define-generic-build-attestation-and-adaptation-review-set.py" \
  --receipt-review "$REVIEW/generic-recipe-binding-and-drift-target-receipt-review.tsv" \
  --source-metadata "$REVIEW/generic-recipe-binding-and-drift-target-receipt-metadata.tsv" \
  --requirements-out "$TMP/requirements.tsv" \
  --roots-out "$TMP/roots.tsv" \
  --objects-out "$TMP/objects.tsv" \
  --metadata-out "$TMP/metadata.tsv"

cmp "$TMP/requirements.tsv" "$REVIEW/generic-build-attestation-adaptation-review-requirements.tsv"
cmp "$TMP/roots.tsv" "$REVIEW/generic-build-attestation-adaptation-root-review-set.tsv"
cmp "$TMP/objects.tsv" "$REVIEW/generic-build-attestation-adaptation-object-review-set.tsv"
cmp "$TMP/metadata.tsv" "$REVIEW/generic-build-attestation-adaptation-review-set-metadata.tsv"

python3 - "$REVIEW" <<'PY'
import csv
import hashlib
import pathlib
import sys
from collections import Counter

review = pathlib.Path(sys.argv[1])

def read(name):
    with (review / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))

def sha(name):
    return hashlib.sha256((review / name).read_bytes()).hexdigest()

req = read("generic-build-attestation-adaptation-review-requirements.tsv")
roots = read("generic-build-attestation-adaptation-root-review-set.tsv")
objects = read("generic-build-attestation-adaptation-object-review-set.tsv")
meta_rows = read("generic-build-attestation-adaptation-review-set-metadata.tsv")
meta = {row["field"]: row["value"] for row in meta_rows}

assert len(req) == 16
assert len(roots) == 28
assert len(objects) == 37
assert len({row["requirement_id"] for row in req}) == 16
assert len({row["root_review_id"] for row in roots}) == 28
assert len({row["object_review_id"] for row in objects}) == 37
assert len({row["evidence_row_id"] for row in objects}) == 37
assert all(row["authority_effect"] == "REVIEW_INPUT_ONLY_NO_AUTOMATIC_ACCEPTANCE" for row in req)
assert all(row["review_state"] == "REQUIREMENTS_DEFINED_EVIDENCE_NOT_COLLECTED" for row in roots)
assert all(row["authority_state"] == "OPEN_NO_ACCEPTANCE" for row in roots + objects)
assert all(row["target_population_state"] == "UNPOPULATED" for row in objects)
assert sum(int(row["identity_count"]) for row in roots) == 37
assert sum(int(row["eligible_object_count"]) for row in roots) == 36
assert sum(int(row["blocked_object_count"]) for row in roots) == 1

object_tiers = Counter(row["review_tier"] for row in objects)
assert object_tiers == Counter({
    "T0_OBJECT_REQUIREMENT_CORRECTION": 1,
    "T1_MATERIAL_DELTA_AND_DRIFT": 12,
    "T2_MATERIAL_DELTA_EXACT": 8,
    "T4_CONFIGURATION_OR_PACKAGING_EXACT": 7,
    "T5_NO_TOKEN_AND_DRIFT": 3,
    "T6_NO_TOKEN_EXACT": 6,
})
root_tiers = Counter(row["review_tier"] for row in roots)
assert root_tiers == Counter({
    "T0_OBJECT_REQUIREMENT_CORRECTION": 1,
    "T1_MATERIAL_DELTA_AND_DRIFT": 8,
    "T2_MATERIAL_DELTA_EXACT": 6,
    "T4_CONFIGURATION_OR_PACKAGING_EXACT": 6,
    "T5_NO_TOKEN_AND_DRIFT": 1,
    "T6_NO_TOKEN_EXACT": 6,
})

blocked = [row for row in objects if row["review_eligibility_state"] == "BLOCKED_OBJECT_REQUIREMENT_UNSATISFIED"]
assert len(blocked) == 1
assert blocked[0]["identity_label"] == "libjpeg.so.62.3.0"
assert blocked[0]["object_correction_requirement_set"] == "OJ-001"
assert all(
    row["concrete_filename_requirement_set"] == "CF-001;CF-002;CF-003;CF-004"
    for row in objects
    if row["object_member_review_state"] == "DRIFT_TARGET_ELF_EXPECTED_SONAME_CANDIDATE_CONFIRMED"
)
assert all(
    row["build_attestation_requirement_set"] == "BA-001;BA-002;BA-003;BA-004;BA-005"
    for row in objects
)

assert meta["requirements_sha256"] == sha("generic-build-attestation-adaptation-review-requirements.tsv")
assert meta["root_review_set_sha256"] == sha("generic-build-attestation-adaptation-root-review-set.tsv")
assert meta["object_review_set_sha256"] == sha("generic-build-attestation-adaptation-object-review-set.tsv")
assert meta["requirement_rows"] == "16"
assert meta["root_review_rows"] == "28"
assert meta["object_review_rows"] == "37"
assert meta["artifact_build_attestations_accepted"] == "0"
assert meta["termux_android_adaptations_accepted"] == "0"
assert meta["concrete_filename_drifts_accepted"] == "0"
assert meta["final_provider_decisions_accepted"] == "0"
assert meta["target_rows_populated"] == "0"
assert meta["next_state"] == "COLLECT_BOUNDED_GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE"
PY

printf '%s\n' 'generic build attestation and adaptation review set smoke: PASS'
