#!/usr/bin/env python3
"""Define bounded evidence-acquisition work units from the reviewed 0152 receipt.

This repository-side planning transaction does not acquire evidence. It maps the
six open closure lanes, sixteen requirements, twenty-eight pinned recipe roots,
and thirty-seven named objects to deterministic acquisition contracts that are
compatible with the strict manifest consumed by the 0151 collector.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter
from pathlib import Path
from typing import Iterable, NoReturn

EXPECTED_LANES = 6
EXPECTED_REQUIREMENTS = 16
EXPECTED_ROOTS = 28
EXPECTED_OBJECTS = 37
EXPECTED_DIRECT_GAPS = 10
EXPECTED_LOCAL_FOUNDATIONS = 6
EXPECTED_SOURCE_CONTRACTS = 10
AUTHORITY_STATE = "OPEN_NO_ACCEPTANCE"
TARGET_STATE = "UNPOPULATED"
ACQUISITION_STATE = "ACQUISITION_WORK_UNIT_DEFINED_NOT_EXECUTED"
NEXT_STATE = "IMPLEMENT_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUIRER"
SOURCE_NEXT_STATE = "DEFINE_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUISITION_SET"
CLAIM_BOUNDARY = "CANDIDATE_EVIDENCE_REVIEW_REQUIRED_NO_AUTHORITY_EFFECT"

SOURCE_CONTRACTS = [
    {
        "source_kind": "AUTHORITATIVE_REFERENCE",
        "acquisition_role": "OBJECT_REQUIREMENT_CORRECTION",
        "allowed_requirements": "OJ-001",
        "allowed_scope_kinds": "OBJECT",
        "acquisition_mode": "OPERATOR_SUPPLIED_REFERENCE_OR_BOUNDED_REFERENCE_CAPTURE",
        "required_locator_class": "IMMUTABLE_DOCUMENT_REVISION_OR_CONTENT_DIGEST",
        "required_integrity_fields": "source_locator;sha256;size_bytes",
        "payload_contract": "AUTHORITATIVE_REQUIRED_IDENTITY_AND_DECISION_BASIS",
        "prohibited_inference": "NO_ABI_FAMILY_SUBSTITUTION",
    },
    {
        "source_kind": "IMMUTABLE_BUILD_RECORD",
        "acquisition_role": "PRODUCING_BUILD_PROVENANCE",
        "allowed_requirements": "BA-001;BA-002;BA-003",
        "allowed_scope_kinds": "ROOT",
        "acquisition_mode": "IMPORT_EXISTING_IMMUTABLE_BUILDER_RECORD",
        "required_locator_class": "BUILDER_RUN_ID_AND_IMMUTABLE_RECORD_LOCATOR",
        "required_integrity_fields": "source_locator;sha256;size_bytes",
        "payload_contract": "ARTIFACT_DIGEST_RECIPE_TREE_INVOCATION_ENVIRONMENT_AND_OUTPUT_BINDING",
        "prohibited_inference": "NO_REPOSITORY_COLOCATION_OR_VERSION_ONLY_PROVENANCE",
    },
    {
        "source_kind": "SIGNED_PROVENANCE",
        "acquisition_role": "SIGNED_BUILD_PROVENANCE",
        "allowed_requirements": "BA-001;BA-002;BA-003;BA-004",
        "allowed_scope_kinds": "ROOT",
        "acquisition_mode": "IMPORT_SIGNED_PROVENANCE_ENVELOPE",
        "required_locator_class": "SIGNATURE_IDENTITY_AND_VERIFIABLE_ENVELOPE_LOCATOR",
        "required_integrity_fields": "source_locator;sha256;size_bytes",
        "payload_contract": "DIGEST_BOUND_SOURCE_RECIPE_BUILD_AND_OUTPUT_STATEMENT",
        "prohibited_inference": "NO_UNSIGNED_NAME_OR_VERSION_EQUIVALENCE",
    },
    {
        "source_kind": "INDEPENDENT_REPRODUCTION",
        "acquisition_role": "INDEPENDENT_BUILD_VERIFICATION",
        "allowed_requirements": "BA-004",
        "allowed_scope_kinds": "ROOT",
        "acquisition_mode": "IMPORT_INDEPENDENT_REPRODUCTION_RECEIPT",
        "required_locator_class": "INDEPENDENT_EXECUTOR_AND_RECEIPT_LOCATOR",
        "required_integrity_fields": "source_locator;sha256;size_bytes",
        "payload_contract": "PINNED_SOURCE_RECIPE_ENVIRONMENT_OUTPUT_DIGEST_COMPARISON",
        "prohibited_inference": "NO_SAME_HOST_SELF_REPLAY_AS_INDEPENDENT_VERIFICATION",
    },
    {
        "source_kind": "OUTPUT_MANIFEST",
        "acquisition_role": "OUTPUT_TO_BUILD_LINKAGE",
        "allowed_requirements": "BA-003",
        "allowed_scope_kinds": "ROOT",
        "acquisition_mode": "IMPORT_PRODUCING_BUILD_OUTPUT_MANIFEST",
        "required_locator_class": "PRODUCING_BUILD_RUN_AND_OUTPUT_MANIFEST_LOCATOR",
        "required_integrity_fields": "source_locator;sha256;size_bytes",
        "payload_contract": "PACKAGE_AND_NAMED_MEMBER_DIGESTS_BOUND_TO_PRODUCING_BUILD",
        "prohibited_inference": "NO_RECEIPT_ONLY_MEMBER_OBSERVATION_AS_BUILD_LINK",
    },
    {
        "source_kind": "PINNED_UPSTREAM_BASELINE",
        "acquisition_role": "UPSTREAM_SEMANTIC_BASELINE",
        "allowed_requirements": "AD-001;AD-002;AD-006",
        "allowed_scope_kinds": "ROOT",
        "acquisition_mode": "ACQUIRE_OR_IMPORT_PINNED_UPSTREAM_SOURCE_BASELINE",
        "required_locator_class": "UPSTREAM_URL_REVISION_AND_DECLARED_DIGEST",
        "required_integrity_fields": "source_locator;sha256;size_bytes",
        "payload_contract": "PINNED_UPSTREAM_FILES_NEEDED_FOR_RECIPE_DELTA_REVIEW",
        "prohibited_inference": "NO_UNPINNED_LATEST_UPSTREAM_BASELINE",
    },
    {
        "source_kind": "SEMANTIC_REVIEW",
        "acquisition_role": "ADAPTATION_SEMANTIC_CLASSIFICATION",
        "allowed_requirements": "AD-001;AD-002;AD-003;AD-004;AD-006",
        "allowed_scope_kinds": "ROOT;OBJECT",
        "acquisition_mode": "AUTHOR_BOUNDED_REPOSITORY_REVIEW_RECORD",
        "required_locator_class": "REVIEW_DOCUMENT_REVISION_OR_CONTENT_DIGEST",
        "required_integrity_fields": "source_locator;sha256;size_bytes",
        "payload_contract": "DELTA_UPSTREAM_NECESSITY_AND_NAMED_OBJECT_IMPACT_CLASSIFICATION",
        "prohibited_inference": "NO_TOKEN_PRESENCE_OR_TERMUX_ORIGIN_AS_NECESSITY",
    },
    {
        "source_kind": "CONSUMER_REFERENCE",
        "acquisition_role": "CONSUMER_BINDING_EVIDENCE",
        "allowed_requirements": "CF-001;CF-002",
        "allowed_scope_kinds": "OBJECT",
        "acquisition_mode": "PASSIVE_BOUNDED_CONSUMER_REFERENCE_CAPTURE",
        "required_locator_class": "CONSUMER_IDENTITY_AND_CONTENT_DIGEST",
        "required_integrity_fields": "source_locator;sha256;size_bytes",
        "payload_contract": "CONSUMER_REFERENCE_TO_STABLE_SONAME_OR_ALIAS_IDENTITY",
        "prohibited_inference": "NO_PROVIDER_SONAME_EQUALITY_AS_CONSUMER_BINDING",
    },
    {
        "source_kind": "LOADER_POLICY",
        "acquisition_role": "LOADER_IDENTITY_POLICY",
        "allowed_requirements": "CF-001;CF-002",
        "allowed_scope_kinds": "OBJECT",
        "acquisition_mode": "IMPORT_OR_AUTHOR_BOUNDED_LOADER_POLICY_RECORD",
        "required_locator_class": "POLICY_REVISION_OR_CONTENT_DIGEST",
        "required_integrity_fields": "source_locator;sha256;size_bytes",
        "payload_contract": "STABLE_ALIAS_SONAME_AND_CONCRETE_TARGET_BINDING_RULES",
        "prohibited_inference": "NO_CURRENT_CONCRETE_FILENAME_AS_PERMANENT_ORACLE",
    },
    {
        "source_kind": "CONTINUITY_POLICY",
        "acquisition_role": "SUCCESSOR_AND_ROLLBACK_POLICY",
        "allowed_requirements": "BA-005;AD-005;CF-002;CF-003;CF-004",
        "allowed_scope_kinds": "ROOT;OBJECT",
        "acquisition_mode": "AUTHOR_BOUNDED_SUCCESSOR_AND_ROLLBACK_POLICY",
        "required_locator_class": "POLICY_REVISION_OR_CONTENT_DIGEST",
        "required_integrity_fields": "source_locator;sha256;size_bytes",
        "payload_contract": "SUCCESSOR_ROLLBACK_ATTESTATION_ADAPTATION_ALIAS_AND_TARGET_GATES",
        "prohibited_inference": "NO_CURRENT_VERSION_ONLY_CONTINUITY_CLAIM",
    },
]

REQ_PLAN = {
    "OJ-001": ("AUTHORITATIVE_CORRECTION", "OPERATOR_SUPPLIED_OR_BOUNDED_REFERENCE_REVIEW", "AUTHORITATIVE_REFERENCE", "NONE", "OBJECT", "object-requirement-correction-review.tsv", "object_review_id;evidence_row_id;required_identity;reference_locator;decision_basis", "P0"),
    "BA-001": ("PRODUCER_PROVENANCE", "IMPORT_EXISTING_PRODUCING_BUILD_RECORD", "IMMUTABLE_BUILD_RECORD", "SIGNED_PROVENANCE", "ROOT", "build-invocation-record.json", "root_review_id;artifact_sha256;recipe_tree;build_run_id;invocation", "P1"),
    "BA-002": ("PRODUCER_PROVENANCE", "IMPORT_EXISTING_PRODUCING_ENVIRONMENT_RECORD", "IMMUTABLE_BUILD_RECORD", "SIGNED_PROVENANCE", "ROOT", "build-environment-record.json", "root_review_id;build_run_id;toolchain;dependencies;environment", "P1"),
    "BA-003": ("OUTPUT_LINKAGE", "IMPORT_PRODUCING_BUILD_OUTPUT_MANIFEST", "OUTPUT_MANIFEST", "IMMUTABLE_BUILD_RECORD;SIGNED_PROVENANCE", "ROOT", "build-output-manifest.tsv", "root_review_id;build_run_id;artifact_sha256;member_path;member_sha256", "P2"),
    "BA-004": ("INDEPENDENT_VERIFICATION", "IMPORT_INDEPENDENT_REPRODUCTION_OR_SIGNED_PROVENANCE", "INDEPENDENT_REPRODUCTION", "SIGNED_PROVENANCE", "ROOT", "independent-reproduction-receipt.json", "root_review_id;recipe_tree;artifact_sha256;executor_identity;comparison_result", "P1"),
    "BA-005": ("CONTINUITY_POLICY_AUTHORING", "AUTHOR_SUCCESSOR_ROLLBACK_ATTESTATION_POLICY", "CONTINUITY_POLICY", "NONE", "ROOT", "build-attestation-continuity-policy.tsv", "root_review_id;transition_class;required_checks;rollback_checks;stop_conditions", "P5"),
    "AD-001": ("SEMANTIC_REVIEW_AUTHORING", "AUTHOR_COMPLETE_RECIPE_DELTA_INVENTORY_REVIEW", "SEMANTIC_REVIEW", "PINNED_UPSTREAM_BASELINE", "ROOT", "recipe-delta-inventory-review.tsv", "root_review_id;recipe_file;delta_class;review_disposition;evidence_reference", "P3"),
    "AD-002": ("UPSTREAM_BASELINE_AND_REVIEW", "ACQUIRE_PINNED_BASELINE_AND_AUTHOR_SEMANTIC_COMPARISON", "PINNED_UPSTREAM_BASELINE", "SEMANTIC_REVIEW", "ROOT", "upstream-semantic-comparison.tsv", "root_review_id;recipe_tree;upstream_locator;upstream_digest;delta_semantics", "P3"),
    "AD-003": ("SEMANTIC_REVIEW_AUTHORING", "AUTHOR_ANDROID_TERMUX_NECESSITY_CLASSIFICATION", "SEMANTIC_REVIEW", "NONE", "ROOT", "android-termux-necessity-review.tsv", "root_review_id;delta_id;necessity_class;platform_evidence;rejection_basis", "P3"),
    "AD-004": ("OBJECT_IMPACT_REVIEW_AUTHORING", "AUTHOR_NAMED_OBJECT_IMPACT_BINDING", "SEMANTIC_REVIEW", "NONE", "OBJECT", "object-impact-review.tsv", "object_review_id;root_review_id;delta_id;impact_class;impact_basis", "P3"),
    "AD-005": ("CONTINUITY_POLICY_AUTHORING", "AUTHOR_ADAPTATION_SUCCESSOR_ROLLBACK_POLICY", "CONTINUITY_POLICY", "NONE", "ROOT", "adaptation-continuity-policy.tsv", "root_review_id;transition_class;semantic_recheck;object_recheck;rollback_gate", "P5"),
    "AD-006": ("SEMANTIC_REVIEW_AUTHORING", "AUTHOR_FULL_NO_TOKEN_ROOT_SEMANTIC_REVIEW", "SEMANTIC_REVIEW", "PINNED_UPSTREAM_BASELINE", "ROOT", "no-token-root-semantic-review.tsv", "root_review_id;recipe_file;upstream_baseline;semantic_result;explicit_no_impact_basis", "P3"),
    "CF-001": ("CONSUMER_BINDING_COLLECTION", "CAPTURE_PASSIVE_CONSUMER_REFERENCE_OR_LOADER_POLICY", "CONSUMER_REFERENCE", "LOADER_POLICY", "OBJECT", "consumer-binding-evidence.tsv", "object_review_id;consumer_identity;reference_kind;referenced_identity;consumer_digest", "P4"),
    "CF-002": ("CONSUMER_BINDING_REVIEW", "REVIEW_ALIAS_CHAIN_WITH_CONSUMER_AND_CONTINUITY_INPUTS", "CONSUMER_REFERENCE", "LOADER_POLICY;CONTINUITY_POLICY", "OBJECT", "alias-chain-consumer-review.tsv", "object_review_id;alias_member_path;alias_link_target;observed_soname;consumer_evidence_ids", "P4"),
    "CF-003": ("CONTINUITY_POLICY_AUTHORING", "AUTHOR_SUCCESSOR_FILENAME_DRIFT_POLICY", "CONTINUITY_POLICY", "NONE", "OBJECT", "successor-filename-drift-policy.tsv", "object_review_id;stable_identity;allowed_transition;required_validation;rejection_rule", "P5"),
    "CF-004": ("CONTINUITY_POLICY_AUTHORING", "AUTHOR_ROLLBACK_FILENAME_DRIFT_POLICY", "CONTINUITY_POLICY", "NONE", "OBJECT", "rollback-filename-drift-policy.tsv", "object_review_id;stable_identity;rollback_transition;required_validation;rejection_rule", "P5"),
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"generic gap evidence acquisition set: FAIL: {message}")


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.is_file() or path.is_symlink():
        fail(f"missing regular input: {path}")
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if not reader.fieldnames:
            fail(f"missing header: {path}")
        return [{key: value or "" for key, value in row.items()} for row in reader]


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
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
    return {item for item in value.split(";") if item and item != "NONE"}


def join_set(values: Iterable[str]) -> str:
    result = sorted(set(values))
    return ";".join(result) if result else "NONE"


def unique(rows: list[dict[str, str]], key: str, label: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row.get(key, "")
        if not value or value in result:
            fail(f"{label} duplicate or empty {key}: {value!r}")
        result[value] = row
    return result


def metadata(path: Path) -> dict[str, str]:
    rows = read_tsv(path)
    if not rows or set(rows[0]) != {"field", "value"}:
        fail("source metadata header drift")
    return {row["field"]: row["value"] for row in rows}


def unit_id(prefix: str, scope_id: str, requirements: str) -> str:
    digest = hashlib.sha256(f"{scope_id}\0{requirements}".encode()).hexdigest()[:20]
    return f"{prefix}:{digest}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lanes", required=True, type=Path)
    parser.add_argument("--requirements", required=True, type=Path)
    parser.add_argument("--requirement-review", required=True, type=Path)
    parser.add_argument("--lane-review", required=True, type=Path)
    parser.add_argument("--root-review", required=True, type=Path)
    parser.add_argument("--object-review", required=True, type=Path)
    parser.add_argument("--source-metadata", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    lanes = read_tsv(args.lanes)
    requirements = read_tsv(args.requirements)
    req_review = read_tsv(args.requirement_review)
    lane_review = read_tsv(args.lane_review)
    root_review = read_tsv(args.root_review)
    object_review = read_tsv(args.object_review)
    source_meta = metadata(args.source_metadata)

    if len(lanes) != EXPECTED_LANES or len(lane_review) != EXPECTED_LANES:
        fail("lane denominator drift")
    if len(requirements) != EXPECTED_REQUIREMENTS or len(req_review) != EXPECTED_REQUIREMENTS:
        fail("requirement denominator drift")
    if len(root_review) != EXPECTED_ROOTS:
        fail("root denominator drift")
    if len(object_review) != EXPECTED_OBJECTS:
        fail("object denominator drift")
    if len(SOURCE_CONTRACTS) != EXPECTED_SOURCE_CONTRACTS:
        fail("source contract denominator drift")

    lane_by_id = unique(lanes, "lane_id", "lane set")
    lane_review_by_id = unique(lane_review, "lane_id", "lane review")
    req_by_id = unique(requirements, "requirement_id", "requirement set")
    req_review_by_id = unique(req_review, "requirement_id", "requirement review")
    if set(req_by_id) != set(REQ_PLAN) or set(req_review_by_id) != set(REQ_PLAN):
        fail("requirement identity drift")
    if set(lane_by_id) != set(lane_review_by_id):
        fail("lane identity drift")

    direct_count = 0
    local_count = 0
    requirement_rows: list[dict[str, object]] = []
    for req_id in sorted(req_by_id):
        source = req_by_id[req_id]
        review = req_review_by_id[req_id]
        plan = REQ_PLAN[req_id]
        if review["lane_id"] != source["lane_id"] or review["authority_state"] != AUTHORITY_STATE:
            fail(f"review identity or authority drift: {req_id}")
        if review["candidate_evidence_count"] != "0" or review["closure_state"] != "OPEN_EVIDENCE_REQUIRED":
            fail(f"unexpected candidate or closure state: {req_id}")
        if review["receipt_review_state"] not in {
            "LOCAL_FOUNDATION_RECONFIRMED_REVIEW_INPUT_CLOSURE_OPEN",
            "NO_CANDIDATE_EVIDENCE_GAP_CONFIRMED_OPEN",
        }:
            fail(f"unexpected receipt review state: {req_id}")
        if source["closure_class"] == "DIRECT_GAP":
            direct_count += 1
        elif source["closure_class"] == "LOCAL_FOUNDATION_COMPLETION":
            local_count += 1
        else:
            fail(f"unexpected closure class: {req_id}")
        acquisition_class, mode, primary, alternates, scope_kind, deliverable, bindings, priority = plan
        if primary not in {row["source_kind"] for row in SOURCE_CONTRACTS}:
            fail(f"unknown primary source kind: {req_id}")
        allowed = {primary} | split_set(alternates)
        contract_allowed = {
            row["source_kind"]
            for row in SOURCE_CONTRACTS
            if req_id in split_set(row["allowed_requirements"])
        }
        if not allowed <= contract_allowed:
            fail(f"source contract mismatch: {req_id} {sorted(allowed - contract_allowed)}")
        requirement_rows.append({
            "requirement_id": req_id,
            "lane_id": source["lane_id"],
            "dimension": source["dimension"],
            "scope": source["scope"],
            "closure_class": source["closure_class"],
            "receipt_review_state": review["receipt_review_state"],
            "remaining_gap_class": review["remaining_gap_class"],
            "acquisition_priority": priority,
            "acquisition_class": acquisition_class,
            "acquisition_mode": mode,
            "primary_source_kind": primary,
            "alternate_source_kinds": alternates,
            "manifest_scope_kind": scope_kind,
            "deliverable_contract": deliverable,
            "minimum_binding_fields": bindings,
            "dependency_requirement_ids": source["dependency_requirement_ids"],
            "completion_gate": review["completion_criteria"],
            "review_after_collection": "SEPARATE_GAP_CLOSURE_RECEIPT_REVIEW_REQUIRED",
            "claim_boundary": CLAIM_BOUNDARY,
            "acquisition_state": ACQUISITION_STATE,
            "authority_state": AUTHORITY_STATE,
        })
    if direct_count != EXPECTED_DIRECT_GAPS or local_count != EXPECTED_LOCAL_FOUNDATIONS:
        fail("closure class denominator drift")

    requirement_by_id = {row["requirement_id"]: row for row in requirement_rows}
    lane_rows: list[dict[str, object]] = []
    for lane_id in sorted(lane_by_id):
        source = lane_by_id[lane_id]
        review = lane_review_by_id[lane_id]
        req_ids = split_set(source["requirement_ids"])
        if req_ids != split_set(review["requirement_ids"]):
            fail(f"lane requirement drift: {lane_id}")
        lane_rows.append({
            "lane_id": lane_id,
            "priority": source["priority"],
            "lane_class": source["lane_class"],
            "scope": source["scope"],
            "requirement_ids": join_set(req_ids),
            "acquisition_classes": join_set(requirement_by_id[r]["acquisition_class"] for r in req_ids),
            "source_kinds": join_set(
                kind
                for req_id in req_ids
                for kind in ({requirement_by_id[req_id]["primary_source_kind"]} | split_set(str(requirement_by_id[req_id]["alternate_source_kinds"])))
            ),
            "acquisition_sequence": ";".join(sorted(req_ids, key=lambda r: (requirement_by_id[r]["acquisition_priority"], r))),
            "manifest_contract": "0151_STRICT_EVIDENCE_MANIFEST_COMPATIBLE",
            "completion_gate": source["completion_gate"],
            "stop_condition": source["stop_condition"],
            "acquisition_state": ACQUISITION_STATE,
            "authority_state": AUTHORITY_STATE,
        })

    root_rows: list[dict[str, object]] = []
    root_edges = 0
    for row in sorted(root_review, key=lambda item: item["root_review_id"]):
        if row["candidate_evidence_count"] != "0" or row["closure_state"] != "OPEN_EVIDENCE_REQUIRED" or row["authority_state"] != AUTHORITY_STATE:
            fail(f"root review state drift: {row['root_review_id']}")
        req_ids = split_set(row["requirement_ids"])
        if not req_ids <= set(requirement_by_id):
            fail(f"root unknown requirement: {row['root_review_id']}")
        root_edges += len(req_ids)
        root_rows.append({
            "acquisition_unit_id": unit_id("generic-root-acquisition", row["root_review_id"], join_set(req_ids)),
            "root_review_id": row["root_review_id"],
            "recipe_root": row["recipe_root"],
            "recipe_tree": row["recipe_tree"],
            "closure_lane_ids": row["closure_lane_ids"],
            "requirement_ids": join_set(req_ids),
            "source_kinds": join_set(
                kind
                for req_id in req_ids
                for kind in ({requirement_by_id[req_id]["primary_source_kind"]} | split_set(str(requirement_by_id[req_id]["alternate_source_kinds"])))
            ),
            "direct_gap_requirement_ids": row["explicit_gap_requirement_ids"],
            "local_foundation_requirement_ids": row["local_foundation_requirement_ids"],
            "manifest_scope_kind": "ROOT",
            "manifest_scope_id": row["root_review_id"],
            "acquisition_sequence": ";".join(sorted(req_ids, key=lambda r: (requirement_by_id[r]["acquisition_priority"], r))),
            "completion_gate": "ALL_ROOT_AND_DEPENDENT_OBJECT_ACQUISITION_RECORDS_COLLECTED_AND_SEPARATELY_REVIEWED",
            "acquisition_state": ACQUISITION_STATE,
            "authority_state": AUTHORITY_STATE,
        })

    object_rows: list[dict[str, object]] = []
    object_edges = 0
    for row in sorted(object_review, key=lambda item: item["object_review_id"]):
        if row["candidate_evidence_count"] != "0" or row["closure_state"] != "OPEN_EVIDENCE_REQUIRED":
            fail(f"object review state drift: {row['object_review_id']}")
        if row["authority_state"] != AUTHORITY_STATE or row["target_population_state"] != TARGET_STATE or row["final_provider_state"] != "UNRESOLVED":
            fail(f"object authority/target drift: {row['object_review_id']}")
        req_ids = split_set(row["requirement_ids"])
        if not req_ids <= set(requirement_by_id):
            fail(f"object unknown requirement: {row['object_review_id']}")
        object_edges += len(req_ids)
        object_rows.append({
            "acquisition_unit_id": unit_id("generic-object-acquisition", row["object_review_id"], join_set(req_ids)),
            "object_review_id": row["object_review_id"],
            "evidence_row_id": row["evidence_row_id"],
            "identity_label": row["identity_label"],
            "artifact_id": row["artifact_id"],
            "artifact_sha256": row["artifact_sha256"],
            "recipe_root": row["recipe_root"],
            "object_class": row["object_class"],
            "closure_lane_ids": row["closure_lane_ids"],
            "requirement_ids": join_set(req_ids),
            "source_kinds": join_set(
                kind
                for req_id in req_ids
                for kind in ({requirement_by_id[req_id]["primary_source_kind"]} | split_set(str(requirement_by_id[req_id]["alternate_source_kinds"])))
            ),
            "direct_gap_requirement_ids": row["explicit_gap_requirement_ids"],
            "local_foundation_requirement_ids": row["local_foundation_requirement_ids"],
            "manifest_scope_kind": "OBJECT",
            "manifest_scope_id": row["object_review_id"],
            "acquisition_sequence": ";".join(sorted(req_ids, key=lambda r: (requirement_by_id[r]["acquisition_priority"], r))),
            "completion_gate": "ROOT_ACQUISITION_PREREQUISITES_PLUS_OBJECT_SPECIFIC_ACQUISITION_RECORDS_SEPARATELY_REVIEWED",
            "acquisition_state": ACQUISITION_STATE,
            "final_provider_state": "UNRESOLVED",
            "authority_state": AUTHORITY_STATE,
            "target_population_state": TARGET_STATE,
        })

    if source_meta.get("next_state") != SOURCE_NEXT_STATE:
        fail(f"source metadata next-state drift: {source_meta.get('next_state')}")
    expected_meta = {
        "closure_lanes": "6",
        "requirements": "16",
        "root_work_units": "28",
        "object_work_units": "37",
        "candidate_evidence_files": "0",
        "candidate_requirements": "0",
        "local_foundation_only_requirements": "6",
        "explicit_gap_no_candidate_requirements": "10",
        "artifact_build_attestations_accepted": "0",
        "termux_android_adaptations_accepted": "0",
        "concrete_filename_drifts_accepted": "0",
        "object_corrections_accepted": "0",
        "final_provider_decisions_accepted": "0",
        "target_rows_populated": "0",
    }
    for key, value in expected_meta.items():
        if source_meta.get(key) != value:
            fail(f"source metadata drift: {key}={source_meta.get(key)!r} != {value!r}")

    out = args.out
    if out.exists():
        fail(f"output already exists: {out}")
    out.mkdir(parents=True)

    source_fields = list(SOURCE_CONTRACTS[0]) + ["claim_boundary", "authority_state"]
    source_rows = [{**row, "claim_boundary": CLAIM_BOUNDARY, "authority_state": AUTHORITY_STATE} for row in SOURCE_CONTRACTS]
    write_tsv(out / "generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv", source_fields, source_rows)
    write_tsv(out / "generic-build-attestation-adaptation-gap-evidence-acquisition-lanes.tsv", list(lane_rows[0]), lane_rows)
    write_tsv(out / "generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv", list(requirement_rows[0]), requirement_rows)
    write_tsv(out / "generic-build-attestation-adaptation-root-gap-evidence-acquisition-set.tsv", list(root_rows[0]), root_rows)
    write_tsv(out / "generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv", list(object_rows[0]), object_rows)

    produced = [
        out / "generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv",
        out / "generic-build-attestation-adaptation-gap-evidence-acquisition-lanes.tsv",
        out / "generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv",
        out / "generic-build-attestation-adaptation-root-gap-evidence-acquisition-set.tsv",
        out / "generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv",
    ]
    source_counts = Counter(row["primary_source_kind"] for row in requirement_rows)
    metadata_rows = [
        {"field": "source_receipt_review_head", "value": source_meta.get("source_head", "")},
        {"field": "source_receipt_review_tree", "value": source_meta.get("source_tree", "")},
        {"field": "closure_lane_rows", "value": str(len(lane_rows))},
        {"field": "requirement_rows", "value": str(len(requirement_rows))},
        {"field": "direct_gap_requirement_rows", "value": str(direct_count)},
        {"field": "local_foundation_completion_rows", "value": str(local_count)},
        {"field": "source_contract_rows", "value": str(len(source_rows))},
        {"field": "root_acquisition_rows", "value": str(len(root_rows))},
        {"field": "object_acquisition_rows", "value": str(len(object_rows))},
        {"field": "root_requirement_edges", "value": str(root_edges)},
        {"field": "object_requirement_edges", "value": str(object_edges)},
        {"field": "primary_source_kind_counts", "value": ";".join(f"{key}={source_counts[key]}" for key in sorted(source_counts))},
        {"field": "candidate_evidence_files_acquired", "value": "0"},
        {"field": "artifact_build_attestations_accepted", "value": "0"},
        {"field": "termux_android_adaptations_accepted", "value": "0"},
        {"field": "concrete_filename_drifts_accepted", "value": "0"},
        {"field": "object_corrections_accepted", "value": "0"},
        {"field": "final_provider_decisions_accepted", "value": "0"},
        {"field": "target_rows_populated", "value": "0"},
    ]
    for path in produced:
        metadata_rows.append({"field": f"sha256:{path.name}", "value": sha256(path)})
    for label, path in [
        ("source_lanes_sha256", args.lanes),
        ("source_requirements_sha256", args.requirements),
        ("source_requirement_review_sha256", args.requirement_review),
        ("source_lane_review_sha256", args.lane_review),
        ("source_root_review_sha256", args.root_review),
        ("source_object_review_sha256", args.object_review),
        ("source_metadata_sha256", args.source_metadata),
    ]:
        metadata_rows.append({"field": label, "value": sha256(path)})
    metadata_rows.append({"field": "next_state", "value": NEXT_STATE})
    write_tsv(out / "generic-build-attestation-adaptation-gap-evidence-acquisition-set-metadata.tsv", ["field", "value"], metadata_rows)
    (out / "analysis.status").write_text("PASS\n", encoding="utf-8")
    (out / "claim-boundary.txt").write_text(CLAIM_BOUNDARY + "\n", encoding="utf-8")
    (out / "next-state.txt").write_text(NEXT_STATE + "\n", encoding="utf-8")

    print("generic gap evidence acquisition set: PASS")
    print(f"lanes={len(lane_rows)} requirements={len(requirement_rows)} roots={len(root_rows)} objects={len(object_rows)}")
    print(f"source_contracts={len(source_rows)} root_requirement_edges={root_edges} object_requirement_edges={object_edges}")
    print("evidence_acquired=0 authority_accepted=0 target_rows=0")


if __name__ == "__main__":
    main()
