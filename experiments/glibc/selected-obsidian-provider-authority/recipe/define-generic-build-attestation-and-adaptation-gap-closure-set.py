#!/usr/bin/env python3
"""Define bounded gap-closure lanes and work units from the reviewed 0149 receipt.

This is a repository-side planning transaction. It turns the 16 reviewed
requirements, 28 pinned recipe roots, and 37 named objects into deterministic
closure lanes and work units. It collects no new evidence and accepts no build
attestation, adaptation, filename-drift policy, provider authority, or target
population.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path
from typing import Iterable, NoReturn

EXPECTED_REQUIREMENTS = 16
EXPECTED_DIRECT_GAPS = 10
EXPECTED_LOCAL_FOUNDATIONS = 6
EXPECTED_ROOTS = 28
EXPECTED_OBJECTS = 37
EXPECTED_EXACT = 21
EXPECTED_DRIFT = 15
EXPECTED_BLOCKED = 1
AUTHORITY_STATE = "OPEN_NO_ACCEPTANCE"
TARGET_STATE = "UNPOPULATED"
NEXT_STATE = "IMPLEMENT_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_COLLECTOR"
SOURCE_NEXT_STATE = "DEFINE_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_SET"
LOCAL_REVIEW_STATE = "LOCAL_EVIDENCE_CONFIRMED_BOUNDED_REVIEW_INPUT"
GAP_REVIEW_STATE = "EXTERNAL_SEMANTIC_POLICY_OR_CORRECTION_GAP_CONFIRMED"

LANES = [
    {
        "lane_id": "GC-01",
        "priority": "P0",
        "lane_class": "OBJECT_REQUIREMENT_CORRECTION",
        "scope": "OBJECT",
        "requirement_ids": "OJ-001",
        "evidence_origin": "AUTHORITATIVE_WORKLOAD_REFERENCE_OR_EXACT_CANDIDATE",
        "permitted_collection_mode": "BOUNDED_REFERENCE_REVIEW_OR_EXACT_SONAME_CANDIDATE_SEARCH",
        "completion_gate": "CORRECT_REQUIRED_IDENTITY_OR_BIND_EXACT_ARTIFACT_MEMBER_WITH_REQUIRED_SONAME",
        "stop_condition": "NO_ABI_FAMILY_SUBSTITUTION_AND_NO_PACKAGE_WIDE_INFERENCE",
    },
    {
        "lane_id": "GC-02",
        "priority": "P1",
        "lane_class": "DIGEST_BOUND_BUILD_PROVENANCE",
        "scope": "ROOT",
        "requirement_ids": "BA-001;BA-002;BA-004",
        "evidence_origin": "IMMUTABLE_BUILDER_RECORD_SIGNED_PROVENANCE_OR_INDEPENDENT_REPRODUCTION",
        "permitted_collection_mode": "BOUNDED_ARTIFACT_DIGEST_AND_PINNED_RECIPE_ROOT_PROVENANCE_REVIEW",
        "completion_gate": "DIGEST_SOURCE_RECIPE_INVOCATION_ENVIRONMENT_AND_INDEPENDENT_VERIFICATION_BOUND",
        "stop_condition": "NO_REPOSITORY_COLOCATION_OR_VERSION_ALIGNMENT_AS_PROVENANCE",
    },
    {
        "lane_id": "GC-03",
        "priority": "P2",
        "lane_class": "OUTPUT_TO_BUILD_LINK",
        "scope": "ROOT_OBJECT",
        "requirement_ids": "BA-003",
        "evidence_origin": "LOCAL_OUTPUT_RECEIPT_PLUS_PRODUCING_BUILD_RECORD",
        "permitted_collection_mode": "BIND_EXISTING_ARTIFACT_MEMBER_DIGESTS_TO_ATTESTED_BUILD_OUTPUT_MANIFEST",
        "completion_gate": "PACKAGE_AND_NAMED_MEMBER_OUTPUTS_LINKED_TO_ONE_PRODUCING_BUILD",
        "stop_condition": "NO_RECEIPT_ONLY_OUTPUT_OBSERVATION_AS_BUILD_ATTESTATION",
    },
    {
        "lane_id": "GC-04",
        "priority": "P3",
        "lane_class": "ADAPTATION_SEMANTIC_REVIEW",
        "scope": "ROOT_OBJECT",
        "requirement_ids": "AD-001;AD-002;AD-003;AD-004;AD-006",
        "evidence_origin": "PINNED_RECIPE_FILES_UPSTREAM_BASELINE_AND_OBJECT_CROSSWALK",
        "permitted_collection_mode": "BOUNDED_FILE_DELTA_UPSTREAM_SEMANTIC_NECESSITY_AND_OBJECT_IMPACT_REVIEW",
        "completion_gate": "EVERY_DELTA_CLASSIFIED_AND_BOUND_TO_NAMED_OBJECT_OR_EXPLICIT_NO_IMPACT",
        "stop_condition": "NO_TOKEN_PRESENCE_OR_TERMUX_ORIGIN_AS_RUNTIME_NECESSITY",
    },
    {
        "lane_id": "GC-05",
        "priority": "P4",
        "lane_class": "CONSUMER_BINDING_REVIEW",
        "scope": "OBJECT",
        "requirement_ids": "CF-001;CF-002",
        "evidence_origin": "EXACT_ALIAS_TARGET_RECEIPT_PLUS_BOUNDED_CONSUMER_OR_LOADER_POLICY",
        "permitted_collection_mode": "BOUNDED_REFERENCE_DYNAMIC_TAG_LOADER_POLICY_OR_PASSIVE_CONSUMER_REVIEW",
        "completion_gate": "CONSUMERS_BIND_STABLE_SONAME_OR_ALIAS_AND_CURRENT_CHAIN_REMAINS_EXACT",
        "stop_condition": "NO_PROVIDER_SONAME_EQUALITY_ALONE_AS_CONSUMER_BINDING",
    },
    {
        "lane_id": "GC-06",
        "priority": "P5",
        "lane_class": "SUCCESSOR_AND_ROLLBACK_CONTINUITY_POLICY",
        "scope": "ROOT_OBJECT",
        "requirement_ids": "BA-005;AD-005;CF-003;CF-004",
        "evidence_origin": "EXPLICIT_VERSION_TRANSITION_AND_ROLLBACK_POLICY",
        "permitted_collection_mode": "DEFINE_AND_REVIEW_BOUNDED_SUCCESSOR_ROLLBACK_VALIDATION_GATES",
        "completion_gate": "ATTESTATION_ADAPTATION_AND_FILENAME_IDENTITY_CONTINUITY_RULES_EXPLICIT",
        "stop_condition": "NO_CURRENT_VERSION_ONLY_ACCEPTANCE_OR_HISTORICAL_FILENAME_ORACLE",
    },
]

CLOSURE = {
    "BA-001": ("GC-02", "DIRECT_GAP", "EXTERNAL_IMMUTABLE_PROVENANCE", "NONE", "DIGEST_BOUND_PRODUCING_BUILD_INVOCATION_RECORDED"),
    "BA-002": ("GC-02", "DIRECT_GAP", "EXTERNAL_IMMUTABLE_PROVENANCE", "BA-001", "PRODUCING_ENVIRONMENT_TOOLCHAIN_DEPENDENCIES_AND_RELEVANT_VARIABLES_RECORDED"),
    "BA-003": ("GC-03", "LOCAL_FOUNDATION_COMPLETION", "LOCAL_OUTPUT_RECEIPT_PLUS_BUILD_RECORD", "BA-001;BA-002", "PACKAGE_AND_NAMED_MEMBER_OUTPUTS_BOUND_TO_PRODUCING_BUILD"),
    "BA-004": ("GC-02", "DIRECT_GAP", "INDEPENDENT_VERIFICATION", "BA-001;BA-002", "INDEPENDENT_REPRODUCTION_OR_INDEPENDENTLY_VERIFIABLE_PROVENANCE_RECORDED"),
    "BA-005": ("GC-06", "DIRECT_GAP", "CONTINUITY_POLICY", "BA-001;BA-002;BA-003;BA-004", "SUCCESSOR_AND_ROLLBACK_ATTESTATION_CONTINUITY_DEFINED"),
    "AD-001": ("GC-04", "LOCAL_FOUNDATION_COMPLETION", "LOCAL_RECIPE_INVENTORY", "NONE", "COMPLETE_FILE_DELTA_PATCH_HOOK_SUBPACKAGE_AND_CONFIGURATION_INVENTORY_REVIEWED"),
    "AD-002": ("GC-04", "LOCAL_FOUNDATION_COMPLETION", "PINNED_UPSTREAM_SEMANTIC_COMPARISON", "AD-001", "EVERY_RECIPE_DELTA_SEMANTICALLY_COMPARED_TO_PINNED_UPSTREAM_BASELINE"),
    "AD-003": ("GC-04", "DIRECT_GAP", "SEMANTIC_NECESSITY_CLASSIFICATION", "AD-001;AD-002", "EVERY_DELTA_CLASSIFIED_WITH_PLATFORM_OR_PACKAGE_EVIDENCE"),
    "AD-004": ("GC-04", "LOCAL_FOUNDATION_COMPLETION", "OBJECT_IMPACT_REVIEW", "AD-002;AD-003", "EVERY_REVIEWED_DELTA_BOUND_TO_NAMED_OBJECT_OR_EXPLICIT_NO_IMPACT"),
    "AD-005": ("GC-06", "DIRECT_GAP", "CONTINUITY_POLICY", "AD-002;AD-003;AD-004", "ADAPTATION_SUCCESSOR_AND_ROLLBACK_COMPATIBILITY_RULES_DEFINED"),
    "AD-006": ("GC-04", "LOCAL_FOUNDATION_COMPLETION", "FULL_NO_TOKEN_SEMANTIC_REVIEW", "AD-001;AD-002", "EVERY_NO_TOKEN_ROOT_FULLY_REVIEWED_WITHOUT_UPSTREAM_EQUIVALENCE_INFERENCE"),
    "CF-001": ("GC-05", "DIRECT_GAP", "CONSUMER_BINDING", "NONE", "BOUNDED_CONSUMER_OR_LOADER_EVIDENCE_CONFIRMS_SONAME_OR_STABLE_ALIAS_BINDING"),
    "CF-002": ("GC-05", "LOCAL_FOUNDATION_COMPLETION", "LOCAL_ALIAS_TARGET_RECEIPT_PLUS_CONSUMER_REVIEW", "CF-001;CF-003;CF-004", "EXACT_ALIAS_TARGET_CHAIN_REVIEWED_WITH_CONSUMER_AND_CONTINUITY_DEPENDENCIES"),
    "CF-003": ("GC-06", "DIRECT_GAP", "CONTINUITY_POLICY", "CF-001;CF-002", "SUCCESSOR_CONCRETE_TARGET_DRIFT_VALIDATION_POLICY_DEFINED"),
    "CF-004": ("GC-06", "DIRECT_GAP", "CONTINUITY_POLICY", "CF-001;CF-002;CF-003", "ROLLBACK_ALIAS_SONAME_AND_EXACT_MEMBER_VALIDATION_POLICY_DEFINED"),
    "OJ-001": ("GC-01", "DIRECT_GAP", "OBJECT_REQUIREMENT_CORRECTION", "NONE", "REQUIRED_IDENTITY_CORRECTED_OR_EXACT_REQUIRED_SONAME_CANDIDATE_BOUND"),
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"generic build attestation adaptation gap closure set: FAIL: {message}")


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        fail(f"missing input: {path}")
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if not reader.fieldnames:
            fail(f"missing header: {path}")
        return [{key: (value or "") for key, value in row.items()} for row in reader]


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def split_set(value: str) -> set[str]:
    if not value or value == "NONE":
        return set()
    return {item for item in value.split(";") if item}


def join_set(values: Iterable[str]) -> str:
    result = sorted(set(values))
    return ";".join(result) if result else "NONE"


def require_fields(rows: list[dict[str, str]], fields: set[str], label: str) -> None:
    if not rows:
        fail(f"empty {label}")
    missing = fields - set(rows[0])
    if missing:
        fail(f"{label} missing fields: {sorted(missing)}")


def unique_map(rows: list[dict[str, str]], field: str, label: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row[field]
        if not value or value in result:
            fail(f"{label} duplicate or empty {field}: {value!r}")
        result[value] = row
    return result


def read_metadata(path: Path) -> dict[str, str]:
    rows = read_tsv(path)
    require_fields(rows, {"field", "value"}, "source metadata")
    return {row["field"]: row["value"] for row in rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--requirements", required=True, type=Path)
    parser.add_argument("--root-review-set", required=True, type=Path)
    parser.add_argument("--object-review-set", required=True, type=Path)
    parser.add_argument("--requirement-receipt-review", required=True, type=Path)
    parser.add_argument("--root-receipt-review", required=True, type=Path)
    parser.add_argument("--object-receipt-review", required=True, type=Path)
    parser.add_argument("--source-metadata", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--next-state", default=NEXT_STATE)
    args = parser.parse_args()

    if args.out.exists() or args.out.is_symlink():
        fail(f"refusing existing output: {args.out}")

    requirements = read_tsv(args.requirements)
    root_set = read_tsv(args.root_review_set)
    object_set = read_tsv(args.object_review_set)
    req_review = read_tsv(args.requirement_receipt_review)
    root_review = read_tsv(args.root_receipt_review)
    object_review = read_tsv(args.object_receipt_review)
    source_metadata = read_metadata(args.source_metadata)

    require_fields(requirements, {"requirement_id", "dimension", "scope", "requirement", "acceptable_evidence", "blocking_or_insufficient_evidence", "authority_effect"}, "requirements")
    require_fields(req_review, {"requirement_id", "dimension", "scope", "collection_state", "evidence_references", "evidence_class", "receipt_review_state", "remaining_gap_class", "next_action", "authority_state"}, "requirement receipt review")
    require_fields(root_set, {"root_review_id", "review_tier", "recipe_root", "recipe_tree", "recipe_resolved_full_version", "artifact_ids", "artifact_count", "identity_count", "build_attestation_requirement_set", "adaptation_requirement_set", "concrete_filename_requirement_set", "object_correction_requirement_set", "authority_state"}, "root review set")
    require_fields(root_review, {"root_review_id", "review_tier", "recipe_root", "recipe_tree", "recipe_resolved_full_version", "recipe_file_count", "build_script_signal_count", "artifact_count", "identity_count", "recipe_inventory_review_state", "build_provenance_review_state", "adaptation_semantic_review_state", "adaptation_necessity_review_state", "continuity_policy_review_state", "object_correction_review_state", "authority_state"}, "root receipt review")
    require_fields(object_set, {"object_review_id", "evidence_row_id", "review_tier", "capability_partition", "identity_label", "artifact_id", "artifact_package", "artifact_version", "artifact_sha256", "recipe_root", "recipe_tree", "build_attestation_requirement_set", "adaptation_requirement_set", "concrete_filename_requirement_set", "object_correction_requirement_set", "authority_state", "target_population_state"}, "object review set")
    require_fields(object_review, {"object_review_id", "evidence_row_id", "review_tier", "capability_partition", "identity_label", "artifact_id", "artifact_package", "artifact_version", "artifact_sha256", "recipe_root", "recipe_tree", "member_path", "member_sha256", "observed_soname", "alias_member_path", "alias_link_target", "output_evidence_review_state", "build_binding_review_state", "adaptation_impact_review_state", "consumer_binding_review_state", "filename_drift_policy_review_state", "object_requirement_review_state", "final_provider_state", "authority_state", "target_population_state"}, "object receipt review")

    if len(requirements) != EXPECTED_REQUIREMENTS or len(req_review) != EXPECTED_REQUIREMENTS:
        fail("requirement denominator mismatch")
    if len(root_set) != EXPECTED_ROOTS or len(root_review) != EXPECTED_ROOTS:
        fail("root denominator mismatch")
    if len(object_set) != EXPECTED_OBJECTS or len(object_review) != EXPECTED_OBJECTS:
        fail("object denominator mismatch")

    requirement_map = unique_map(requirements, "requirement_id", "requirements")
    req_review_map = unique_map(req_review, "requirement_id", "requirement receipt review")
    if set(requirement_map) != set(CLOSURE) or set(req_review_map) != set(CLOSURE):
        fail("requirement set drift")

    direct_gap_ids: set[str] = set()
    local_ids: set[str] = set()
    requirement_rows: list[dict[str, object]] = []
    for requirement_id in requirement_map:
        canonical = requirement_map[requirement_id]
        review = req_review_map[requirement_id]
        for field in ("dimension", "scope"):
            if canonical[field] != review[field]:
                fail(f"requirement {requirement_id} canonical {field} drift")
        if review["authority_state"] != AUTHORITY_STATE:
            fail(f"requirement {requirement_id} authority promotion detected")
        lane_id, closure_class, evidence_mode, dependencies, completion = CLOSURE[requirement_id]
        expected_review_state = GAP_REVIEW_STATE if closure_class == "DIRECT_GAP" else LOCAL_REVIEW_STATE
        if review["receipt_review_state"] != expected_review_state:
            fail(f"requirement {requirement_id} review-state mismatch")
        if closure_class == "DIRECT_GAP":
            direct_gap_ids.add(requirement_id)
        else:
            local_ids.add(requirement_id)
        requirement_rows.append({
            "requirement_id": requirement_id,
            "dimension": canonical["dimension"],
            "scope": canonical["scope"],
            "source_receipt_review_state": review["receipt_review_state"],
            "source_collection_state": review["collection_state"],
            "source_evidence_references": review["evidence_references"],
            "remaining_gap_class": review["remaining_gap_class"],
            "lane_id": lane_id,
            "closure_class": closure_class,
            "evidence_mode": evidence_mode,
            "dependency_requirement_ids": dependencies,
            "completion_criteria": completion,
            "rejection_criteria": canonical["blocking_or_insufficient_evidence"],
            "closure_state": "WORK_UNIT_DEFINED_EVIDENCE_OR_REVIEW_NOT_ACCEPTED",
            "authority_state": AUTHORITY_STATE,
        })

    if len(direct_gap_ids) != EXPECTED_DIRECT_GAPS or len(local_ids) != EXPECTED_LOCAL_FOUNDATIONS:
        fail("direct-gap/local-foundation cardinality mismatch")

    lane_requirement_ids = set()
    for lane in LANES:
        lane_requirement_ids |= split_set(lane["requirement_ids"])
    if lane_requirement_ids != set(CLOSURE):
        fail("lane requirement coverage mismatch")

    root_set_map = unique_map(root_set, "root_review_id", "root review set")
    root_review_map = unique_map(root_review, "root_review_id", "root receipt review")
    if set(root_set_map) != set(root_review_map):
        fail("root ID set drift")
    root_rows: list[dict[str, object]] = []
    for root_id in sorted(root_set_map):
        canonical = root_set_map[root_id]
        review = root_review_map[root_id]
        for field in ("review_tier", "recipe_root", "recipe_tree", "recipe_resolved_full_version", "artifact_count", "identity_count"):
            if canonical[field] != review[field]:
                fail(f"root {root_id} canonical {field} drift")
        if canonical["authority_state"] != AUTHORITY_STATE or review["authority_state"] != AUTHORITY_STATE:
            fail(f"root {root_id} authority promotion detected")
        all_requirements = set()
        for field in ("build_attestation_requirement_set", "adaptation_requirement_set", "concrete_filename_requirement_set", "object_correction_requirement_set"):
            all_requirements |= split_set(canonical[field])
        if not all_requirements <= set(CLOSURE):
            fail(f"root {root_id} unknown requirement")
        root_requirements = {rid for rid in all_requirements if requirement_map[rid]["scope"] == "ROOT"}
        object_dependencies = all_requirements - root_requirements
        lanes = {CLOSURE[rid][0] for rid in all_requirements}
        prereqs = set()
        for rid in all_requirements:
            prereqs |= split_set(CLOSURE[rid][3])
        root_rows.append({
            "root_review_id": root_id,
            "review_tier": canonical["review_tier"],
            "recipe_root": canonical["recipe_root"],
            "recipe_tree": canonical["recipe_tree"],
            "recipe_resolved_full_version": canonical["recipe_resolved_full_version"],
            "artifact_ids": canonical["artifact_ids"],
            "artifact_count": canonical["artifact_count"],
            "identity_count": canonical["identity_count"],
            "recipe_file_count": review["recipe_file_count"],
            "build_script_signal_count": review["build_script_signal_count"],
            "closure_lane_ids": join_set(lanes),
            "root_requirement_set": join_set(root_requirements),
            "dependent_object_requirement_set": join_set(object_dependencies),
            "direct_gap_requirement_set": join_set(all_requirements & direct_gap_ids),
            "local_foundation_completion_set": join_set(all_requirements & local_ids),
            "prerequisite_requirement_set": join_set(prereqs),
            "completion_gate": "ALL_ROOT_REQUIREMENTS_AND_DEPENDENT_OBJECT_REQUIREMENTS_REVIEWED_IN_SEPARATE_RECEIPT",
            "work_state": "GAP_CLOSURE_WORK_UNIT_DEFINED_AUTHORITY_BLOCKED",
            "authority_state": AUTHORITY_STATE,
        })

    object_set_map = unique_map(object_set, "object_review_id", "object review set")
    object_review_map = unique_map(object_review, "object_review_id", "object receipt review")
    if set(object_set_map) != set(object_review_map):
        fail("object ID set drift")
    object_rows: list[dict[str, object]] = []
    exact_count = drift_count = blocked_count = 0
    for object_id in sorted(object_set_map):
        canonical = object_set_map[object_id]
        review = object_review_map[object_id]
        for field in ("evidence_row_id", "review_tier", "capability_partition", "identity_label", "artifact_id", "artifact_package", "artifact_version", "artifact_sha256", "recipe_root", "recipe_tree"):
            if canonical[field] != review[field]:
                fail(f"object {object_id} canonical {field} drift")
        if canonical["authority_state"] != AUTHORITY_STATE or review["authority_state"] != AUTHORITY_STATE:
            fail(f"object {object_id} authority promotion detected")
        if canonical["target_population_state"] != TARGET_STATE or review["target_population_state"] != TARGET_STATE:
            fail(f"object {object_id} target population detected")
        all_requirements = set()
        for field in ("build_attestation_requirement_set", "adaptation_requirement_set", "concrete_filename_requirement_set", "object_correction_requirement_set"):
            all_requirements |= split_set(canonical[field])
        root_requirements = {rid for rid in all_requirements if requirement_map[rid]["scope"] == "ROOT"}
        object_requirements = all_requirements - root_requirements
        lanes = {CLOSURE[rid][0] for rid in all_requirements}
        prereqs = set()
        for rid in all_requirements:
            prereqs |= split_set(CLOSURE[rid][3])

        output_state = review["output_evidence_review_state"]
        if output_state == "EXACT_MEMBER_DIGEST_AND_SONAME_CONFIRMED_REVIEW_INPUT":
            exact_count += 1
            object_class = "EXACT_MEMBER"
            completion_gate = "ROOT_BUILD_AND_ADAPTATION_CLOSURE_PLUS_OBJECT_OUTPUT_AND_IMPACT_REVIEW"
        elif output_state == "ALIAS_TARGET_MEMBER_DIGEST_AND_SONAME_CONFIRMED_REVIEW_INPUT":
            drift_count += 1
            object_class = "ALIAS_TARGET_DRIFT"
            completion_gate = "ROOT_BUILD_AND_ADAPTATION_CLOSURE_PLUS_CONSUMER_BINDING_AND_FILENAME_CONTINUITY_POLICY"
        elif output_state == "NO_OUTPUT_BINDING_OBJECT_REQUIREMENT_UNSATISFIED":
            blocked_count += 1
            object_class = "OBJECT_REQUIREMENT_BLOCKED"
            completion_gate = "CORRECT_OBJECT_REQUIREMENT_BEFORE_OTHER_AUTHORITY_REVIEW"
        else:
            fail(f"object {object_id} unexpected output review state: {output_state}")
        object_rows.append({
            "object_review_id": object_id,
            "evidence_row_id": canonical["evidence_row_id"],
            "review_tier": canonical["review_tier"],
            "capability_partition": canonical["capability_partition"],
            "identity_label": canonical["identity_label"],
            "artifact_id": canonical["artifact_id"],
            "artifact_package": canonical["artifact_package"],
            "artifact_version": canonical["artifact_version"],
            "artifact_sha256": canonical["artifact_sha256"],
            "recipe_root": canonical["recipe_root"],
            "recipe_tree": canonical["recipe_tree"],
            "member_path": review["member_path"],
            "member_sha256": review["member_sha256"],
            "observed_soname": review["observed_soname"],
            "alias_member_path": review["alias_member_path"],
            "alias_link_target": review["alias_link_target"],
            "object_class": object_class,
            "closure_lane_ids": join_set(lanes),
            "root_requirement_set": join_set(root_requirements),
            "object_requirement_set": join_set(object_requirements),
            "direct_gap_requirement_set": join_set(all_requirements & direct_gap_ids),
            "local_foundation_completion_set": join_set(all_requirements & local_ids),
            "prerequisite_requirement_set": join_set(prereqs),
            "completion_gate": completion_gate,
            "work_state": "OBJECT_REQUIREMENT_CORRECTION_WORK_UNIT_DEFINED" if object_class == "OBJECT_REQUIREMENT_BLOCKED" else "GAP_CLOSURE_WORK_UNIT_DEFINED_AUTHORITY_BLOCKED",
            "final_provider_state": "UNRESOLVED",
            "authority_state": AUTHORITY_STATE,
            "target_population_state": TARGET_STATE,
        })

    if (exact_count, drift_count, blocked_count) != (EXPECTED_EXACT, EXPECTED_DRIFT, EXPECTED_BLOCKED):
        fail(f"object class denominator mismatch: exact={exact_count} drift={drift_count} blocked={blocked_count}")

    expected_meta = {
        "requirement_rows": str(EXPECTED_REQUIREMENTS),
        "local_evidence_requirement_rows": str(EXPECTED_LOCAL_FOUNDATIONS),
        "gap_requirement_rows": str(EXPECTED_DIRECT_GAPS),
        "root_review_rows": str(EXPECTED_ROOTS),
        "object_review_rows": str(EXPECTED_OBJECTS),
        "exact_output_rows": str(EXPECTED_EXACT),
        "drift_output_rows": str(EXPECTED_DRIFT),
        "blocked_object_rows": str(EXPECTED_BLOCKED),
        "artifact_build_attestations_accepted": "0",
        "termux_android_adaptations_accepted": "0",
        "concrete_filename_drifts_accepted": "0",
        "final_provider_decisions_accepted": "0",
        "target_rows_populated": "0",
        "next_state": SOURCE_NEXT_STATE,
    }
    for field, expected in expected_meta.items():
        if source_metadata.get(field) != expected:
            fail(f"source metadata mismatch: {field}={source_metadata.get(field)!r} expected {expected!r}")

    args.out.mkdir(parents=True)
    lanes_path = args.out / "generic-build-attestation-adaptation-gap-closure-lanes.tsv"
    requirements_path = args.out / "generic-build-attestation-adaptation-gap-closure-requirements.tsv"
    roots_path = args.out / "generic-build-attestation-adaptation-root-gap-closure-set.tsv"
    objects_path = args.out / "generic-build-attestation-adaptation-object-gap-closure-set.tsv"
    metadata_path = args.out / "generic-build-attestation-adaptation-gap-closure-set-metadata.tsv"

    write_tsv(lanes_path, ["lane_id", "priority", "lane_class", "scope", "requirement_ids", "evidence_origin", "permitted_collection_mode", "completion_gate", "stop_condition"], LANES)
    write_tsv(requirements_path, ["requirement_id", "dimension", "scope", "source_receipt_review_state", "source_collection_state", "source_evidence_references", "remaining_gap_class", "lane_id", "closure_class", "evidence_mode", "dependency_requirement_ids", "completion_criteria", "rejection_criteria", "closure_state", "authority_state"], requirement_rows)
    write_tsv(roots_path, ["root_review_id", "review_tier", "recipe_root", "recipe_tree", "recipe_resolved_full_version", "artifact_ids", "artifact_count", "identity_count", "recipe_file_count", "build_script_signal_count", "closure_lane_ids", "root_requirement_set", "dependent_object_requirement_set", "direct_gap_requirement_set", "local_foundation_completion_set", "prerequisite_requirement_set", "completion_gate", "work_state", "authority_state"], root_rows)
    write_tsv(objects_path, ["object_review_id", "evidence_row_id", "review_tier", "capability_partition", "identity_label", "artifact_id", "artifact_package", "artifact_version", "artifact_sha256", "recipe_root", "recipe_tree", "member_path", "member_sha256", "observed_soname", "alias_member_path", "alias_link_target", "object_class", "closure_lane_ids", "root_requirement_set", "object_requirement_set", "direct_gap_requirement_set", "local_foundation_completion_set", "prerequisite_requirement_set", "completion_gate", "work_state", "final_provider_state", "authority_state", "target_population_state"], object_rows)

    metadata_rows = [
        {"field": "requirements_sha256", "value": sha256(args.requirements)},
        {"field": "root_review_set_sha256", "value": sha256(args.root_review_set)},
        {"field": "object_review_set_sha256", "value": sha256(args.object_review_set)},
        {"field": "requirement_receipt_review_sha256", "value": sha256(args.requirement_receipt_review)},
        {"field": "root_receipt_review_sha256", "value": sha256(args.root_receipt_review)},
        {"field": "object_receipt_review_sha256", "value": sha256(args.object_receipt_review)},
        {"field": "source_metadata_sha256", "value": sha256(args.source_metadata)},
        {"field": "closure_lanes_sha256", "value": sha256(lanes_path)},
        {"field": "closure_requirements_sha256", "value": sha256(requirements_path)},
        {"field": "root_closure_set_sha256", "value": sha256(roots_path)},
        {"field": "object_closure_set_sha256", "value": sha256(objects_path)},
        {"field": "closure_lane_rows", "value": len(LANES)},
        {"field": "requirement_rows", "value": len(requirement_rows)},
        {"field": "direct_gap_requirement_rows", "value": len(direct_gap_ids)},
        {"field": "local_foundation_completion_rows", "value": len(local_ids)},
        {"field": "root_work_units", "value": len(root_rows)},
        {"field": "object_work_units", "value": len(object_rows)},
        {"field": "exact_object_work_units", "value": exact_count},
        {"field": "drift_object_work_units", "value": drift_count},
        {"field": "blocked_object_work_units", "value": blocked_count},
        {"field": "artifact_build_attestations_accepted", "value": 0},
        {"field": "termux_android_adaptations_accepted", "value": 0},
        {"field": "concrete_filename_drifts_accepted", "value": 0},
        {"field": "final_provider_decisions_accepted", "value": 0},
        {"field": "target_rows_populated", "value": 0},
        {"field": "next_state", "value": args.next_state},
    ]
    write_tsv(metadata_path, ["field", "value"], metadata_rows)

    print("GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_SET_DEFINED_BOUNDED")
    print(f"closure_lanes={len(LANES)}")
    print(f"requirements={len(requirement_rows)}")
    print(f"direct_gaps={len(direct_gap_ids)}")
    print(f"local_foundations={len(local_ids)}")
    print(f"root_work_units={len(root_rows)}")
    print(f"object_work_units={len(object_rows)}")
    print(f"next_state={args.next_state}")


if __name__ == "__main__":
    main()
