#!/usr/bin/env python3
"""Review the bounded generic build-attestation/adaptation evidence receipt.

The reviewer validates the device receipt against the canonical 0147 review set.
It may confirm bounded local evidence as review input and confirm explicit gaps,
but it never accepts build provenance, adaptation semantics, filename drift,
final provider authority, or target population.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, NoReturn

EXPECTED_REQUIREMENTS = 16
EXPECTED_ROOTS = 28
EXPECTED_OBJECTS = 37
EXPECTED_RECIPE_FILES = 84
EXPECTED_SIGNALS = 74
EXPECTED_EXACT_OUTPUTS = 21
EXPECTED_DRIFT_OUTPUTS = 15
EXPECTED_BLOCKED_OUTPUTS = 1
EXPECTED_GAPS = 10
EXPECTED_FOUNDATION_ARTIFACTS = 34
EXPECTED_BRANCH = "docs/post-graphics-architecture-audit"
EXPECTED_SOURCE_HEAD = "540976e7bb8bc49e2d2ab732f8c2f75a90c3b63a"
EXPECTED_SOURCE_TREE = "bd042154b7eadd0655d52477677129fa54bfdbd1"
COLLECTOR_NEXT_STATE = "REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE_RECEIPT"
NEXT_STATE = "DEFINE_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_SET"

LOCAL_REVIEW_STATE = "LOCAL_EVIDENCE_CONFIRMED_BOUNDED_REVIEW_INPUT"
GAP_REVIEW_STATE = "EXTERNAL_SEMANTIC_POLICY_OR_CORRECTION_GAP_CONFIRMED"
AUTHORITY_STATE = "OPEN_NO_ACCEPTANCE"
TARGET_STATE = "UNPOPULATED"


def fail(message: str) -> NoReturn:
    raise SystemExit(f"generic build attestation/adaptation evidence receipt review: FAIL: {message}")


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        fail(f"missing input: {path}")
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if not reader.fieldnames:
            fail(f"missing TSV header: {path}")
        return [{key: (value or "") for key, value in row.items()} for row in reader]


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=fields,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def valid_sha256(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{64}", value))


def valid_oid(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{40}", value))


def require_fields(rows: list[dict[str, str]], fields: set[str], label: str) -> None:
    if not rows:
        fail(f"empty {label}")
    missing = fields - set(rows[0])
    if missing:
        fail(f"{label} schema missing fields: {sorted(missing)}")


def read_key_values(path: Path) -> dict[str, str]:
    if not path.is_file():
        fail(f"missing key/value input: {path}")
    result: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if "=" not in line:
            fail(f"invalid key/value line in {path}: {line}")
        key, value = line.split("=", 1)
        if not key or key in result:
            fail(f"duplicate/empty key in {path}: {key}")
        result[key] = value
    return result


def as_int(value: str, label: str) -> int:
    try:
        return int(value)
    except ValueError:
        fail(f"invalid integer for {label}: {value}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--requirements", required=True, type=Path)
    parser.add_argument("--root-review-set", required=True, type=Path)
    parser.add_argument("--object-review-set", required=True, type=Path)
    parser.add_argument("--rules", required=True, type=Path)
    parser.add_argument("--requirement-status", required=True, type=Path)
    parser.add_argument("--root-observations", required=True, type=Path)
    parser.add_argument("--recipe-file-evidence", required=True, type=Path)
    parser.add_argument("--build-script-signal-evidence", required=True, type=Path)
    parser.add_argument("--root-object-crosswalk", required=True, type=Path)
    parser.add_argument("--artifact-member-output", required=True, type=Path)
    parser.add_argument("--external-gaps", required=True, type=Path)
    parser.add_argument("--input-verification", required=True, type=Path)
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--analysis-status", required=True, type=Path)
    parser.add_argument("--claim-boundary", required=True, type=Path)
    parser.add_argument("--collector-next-state", required=True, type=Path)
    parser.add_argument("--transaction-status", required=True, type=Path)
    parser.add_argument("--final-git-state", required=True, type=Path)
    parser.add_argument("--remote-state", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--source-receipt-archive", required=True)
    parser.add_argument("--source-receipt-sha256", required=True)
    parser.add_argument("--expected-requirements", type=int, default=EXPECTED_REQUIREMENTS)
    parser.add_argument("--expected-roots", type=int, default=EXPECTED_ROOTS)
    parser.add_argument("--expected-objects", type=int, default=EXPECTED_OBJECTS)
    parser.add_argument("--expected-recipe-files", type=int, default=EXPECTED_RECIPE_FILES)
    parser.add_argument("--expected-signals", type=int, default=EXPECTED_SIGNALS)
    parser.add_argument("--expected-exact-outputs", type=int, default=EXPECTED_EXACT_OUTPUTS)
    parser.add_argument("--expected-drift-outputs", type=int, default=EXPECTED_DRIFT_OUTPUTS)
    parser.add_argument("--expected-blocked-outputs", type=int, default=EXPECTED_BLOCKED_OUTPUTS)
    parser.add_argument("--expected-gaps", type=int, default=EXPECTED_GAPS)
    parser.add_argument("--expected-foundation-artifacts", type=int, default=EXPECTED_FOUNDATION_ARTIFACTS)
    parser.add_argument("--expected-root-artifact-references", type=int, default=29)
    parser.add_argument("--expected-branch", default=EXPECTED_BRANCH)
    parser.add_argument("--expected-source-head", default=EXPECTED_SOURCE_HEAD)
    parser.add_argument("--expected-source-tree", default=EXPECTED_SOURCE_TREE)
    parser.add_argument("--next-state", default=NEXT_STATE)
    args = parser.parse_args()

    if args.out.exists() or args.out.is_symlink():
        fail(f"refusing existing output: {args.out}")
    if not valid_sha256(args.source_receipt_sha256):
        fail("invalid source receipt SHA-256")
    if not valid_oid(args.expected_source_head) or not valid_oid(args.expected_source_tree):
        fail("invalid expected source Git identity")

    transaction = read_key_values(args.transaction_status)
    if transaction != {
        "TRANSACTION": "PASS",
        "VALIDATION": "PASS",
        "EVIDENCE_COLLECTION": "PASS",
        "PUSH_AFTER_APPLY": "1",
    }:
        fail(f"transaction status mismatch: {transaction}")
    final_git = read_key_values(args.final_git_state)
    if final_git != {
        "branch": args.expected_branch,
        "head": args.expected_source_head,
        "tree": args.expected_source_tree,
    }:
        fail(f"final Git state mismatch: {final_git}")
    remote = read_key_values(args.remote_state)
    if remote.get("push_after_apply") != "1" or remote.get("remote_head_after") != args.expected_source_head:
        fail(f"remote state mismatch: {remote}")

    if args.analysis_status.read_text(encoding="utf-8").strip() != "PASS":
        fail("collector analysis status is not PASS")
    if args.collector_next_state.read_text(encoding="utf-8").strip() != COLLECTOR_NEXT_STATE:
        fail("collector next state mismatch")
    claim = args.claim_boundary.read_text(encoding="utf-8")
    for token in (
        "not build provenance or adaptation acceptance",
        "No build, package operation, maintainer script, payload extraction, network acquisition",
        "provider promotion or target population",
    ):
        if token not in claim:
            fail(f"claim boundary missing stop token: {token}")

    requirements = read_tsv(args.requirements)
    root_set = read_tsv(args.root_review_set)
    object_set = read_tsv(args.object_review_set)
    rules = read_tsv(args.rules)
    requirement_status = read_tsv(args.requirement_status)
    root_observations = read_tsv(args.root_observations)
    recipe_files = read_tsv(args.recipe_file_evidence)
    signals = read_tsv(args.build_script_signal_evidence)
    crosswalk = read_tsv(args.root_object_crosswalk)
    outputs = read_tsv(args.artifact_member_output)
    external_gaps = read_tsv(args.external_gaps)
    input_verification = read_tsv(args.input_verification)
    summary_rows = read_tsv(args.summary)

    require_fields(requirements, {
        "requirement_id", "dimension", "scope", "requirement", "acceptable_evidence",
        "blocking_or_insufficient_evidence", "authority_effect",
    }, "requirements")
    require_fields(rules, {
        "requirement_id", "expected_collection_state", "review_disposition", "evidence_class",
        "remaining_gap_class", "expected_evidence_references", "receipt_review_state",
        "authority_state", "next_action",
    }, "review rules")
    require_fields(requirement_status, {
        "requirement_id", "dimension", "scope", "requirement", "acceptable_evidence",
        "blocking_or_insufficient_evidence", "authority_effect", "collection_state",
        "evidence_references", "collection_note", "review_state", "authority_state",
    }, "requirement evidence status")

    if len(requirements) != args.expected_requirements or len(rules) != args.expected_requirements or len(requirement_status) != args.expected_requirements:
        fail("requirement denominator mismatch")
    requirement_ids = [row["requirement_id"] for row in requirements]
    if len(requirement_ids) != len(set(requirement_ids)):
        fail("duplicate canonical requirement ID")
    if {row["requirement_id"] for row in rules} != set(requirement_ids):
        fail("review rule requirement set mismatch")
    if {row["requirement_id"] for row in requirement_status} != set(requirement_ids):
        fail("receipt requirement set mismatch")
    requirement_by_id = {row["requirement_id"]: row for row in requirements}
    rule_by_id = {row["requirement_id"]: row for row in rules}
    status_by_id = {row["requirement_id"]: row for row in requirement_status}

    local_rule_ids: set[str] = set()
    gap_rule_ids: set[str] = set()
    requirement_review_rows: list[dict[str, object]] = []
    for requirement_id in requirement_ids:
        canonical = requirement_by_id[requirement_id]
        rule = rule_by_id[requirement_id]
        receipt = status_by_id[requirement_id]
        for field in (
            "dimension", "scope", "requirement", "acceptable_evidence",
            "blocking_or_insufficient_evidence", "authority_effect",
        ):
            if receipt[field] != canonical[field]:
                fail(f"requirement {requirement_id} canonical field drift: {field}")
        if receipt["collection_state"] != rule["expected_collection_state"]:
            fail(f"requirement {requirement_id} collection state mismatch")
        if receipt["evidence_references"] != rule["expected_evidence_references"]:
            fail(f"requirement {requirement_id} evidence reference mismatch")
        if receipt["review_state"] != "EVIDENCE_COLLECTED_OR_GAP_RECORDED_REVIEW_REQUIRED":
            fail(f"requirement {requirement_id} collector review state drifted")
        if receipt["authority_state"] != AUTHORITY_STATE or rule["authority_state"] != AUTHORITY_STATE:
            fail(f"requirement {requirement_id} authority promotion detected")
        if rule["review_disposition"] == "LOCAL_EVIDENCE":
            local_rule_ids.add(requirement_id)
        elif rule["review_disposition"] == "GAP":
            gap_rule_ids.add(requirement_id)
        else:
            fail(f"requirement {requirement_id} invalid review disposition")
        if rule["receipt_review_state"] not in {LOCAL_REVIEW_STATE, GAP_REVIEW_STATE}:
            fail(f"requirement {requirement_id} invalid receipt review state")
        requirement_review_rows.append({
            "requirement_id": requirement_id,
            "dimension": canonical["dimension"],
            "scope": canonical["scope"],
            "collection_state": receipt["collection_state"],
            "evidence_references": receipt["evidence_references"],
            "evidence_class": rule["evidence_class"],
            "receipt_review_state": rule["receipt_review_state"],
            "remaining_gap_class": rule["remaining_gap_class"],
            "next_action": rule["next_action"],
            "authority_state": AUTHORITY_STATE,
        })

    if len(local_rule_ids) != args.expected_requirements - args.expected_gaps or len(gap_rule_ids) != args.expected_gaps:
        fail("local/gap requirement cardinality mismatch")

    require_fields(external_gaps, {"requirement_id", "dimension", "scope", "collection_state", "gap", "next_action"}, "external gaps")
    if len(external_gaps) != args.expected_gaps or {row["requirement_id"] for row in external_gaps} != gap_rule_ids:
        fail("external gap denominator/set mismatch")
    for row in external_gaps:
        rule = rule_by_id[row["requirement_id"]]
        canonical = requirement_by_id[row["requirement_id"]]
        if row["dimension"] != canonical["dimension"] or row["scope"] != canonical["scope"]:
            fail(f"external gap canonical scope drift: {row['requirement_id']}")
        if row["collection_state"] != rule["expected_collection_state"]:
            fail(f"external gap state mismatch: {row['requirement_id']}")
        if row["next_action"] != "PROVIDE_BOUNDED_EVIDENCE_FOR_SEPARATE_RECEIPT_REVIEW":
            fail(f"external gap next action drift: {row['requirement_id']}")

    summary = {row.get("field", ""): row.get("value", "") for row in summary_rows}
    expected_summary = {
        "requirements": args.expected_requirements,
        "root_work_units": args.expected_roots,
        "object_work_units": args.expected_objects,
        "verified_foundation_artifacts": args.expected_foundation_artifacts,
        "recipe_files_collected": args.expected_recipe_files,
        "build_script_signal_rows": args.expected_signals,
        "exact_output_rows": args.expected_exact_outputs,
        "drift_output_rows": args.expected_drift_outputs,
        "blocked_object_rows": args.expected_blocked_outputs,
        "local_evidence_or_partial_evidence_requirement_rows": args.expected_requirements - args.expected_gaps,
        "external_semantic_policy_or_correction_gap_rows": args.expected_gaps,
        "artifact_build_attestations_accepted": 0,
        "termux_android_adaptations_accepted": 0,
        "concrete_filename_drifts_accepted": 0,
        "final_provider_decisions_accepted": 0,
        "target_rows_populated": 0,
        "package_operations_performed": 0,
        "maintainer_scripts_executed": 0,
        "filesystem_payload_extractions": 0,
        "network_acquisitions": 0,
    }
    for field, expected in expected_summary.items():
        if as_int(summary.get(field, ""), field) != expected:
            fail(f"summary {field} mismatch")
    if summary.get("source_manifest_before") != summary.get("source_manifest_after") or not valid_sha256(summary.get("source_manifest_before", "")):
        fail("source manifest immutability mismatch")
    if summary.get("next_state") != COLLECTOR_NEXT_STATE:
        fail("summary next state mismatch")

    require_fields(input_verification, {"input", "path", "sha256_or_state", "verification_state"}, "input verification")
    expected_inputs = {
        "requirements", "root_review_set", "object_review_set", "member_receipt_review",
        "recipe_receipt_review", "foundation_summary", "source_checkout",
    }
    if {row["input"] for row in input_verification} != expected_inputs:
        fail("input verification set mismatch")
    for row in input_verification:
        if row["input"] == "source_checkout":
            if row["verification_state"] != "PINNED_CLEAN_IMMUTABLE_PASS" or not valid_sha256(row["sha256_or_state"]):
                fail("source checkout verification mismatch")
        elif row["verification_state"] != "PASS" or not valid_sha256(row["sha256_or_state"]):
            fail(f"input verification failed: {row['input']}")

    require_fields(root_set, {
        "root_review_id", "review_tier", "recipe_root", "recipe_tree", "recipe_resolved_full_version",
        "artifact_count", "identity_count", "adaptation_evidence_tokens", "review_state",
        "authority_state", "next_action",
    }, "root review set")
    require_fields(root_observations, {
        "root_review_id", "review_tier", "recipe_root", "recipe_tree", "recipe_resolved_full_version",
        "recipe_file_count", "build_script_signal_count", "artifact_count", "identity_count",
        "adaptation_evidence_tokens", "build_provenance_collection_state",
        "recipe_inventory_collection_state", "upstream_semantic_comparison_state",
        "adaptation_classification_state", "update_rollback_state", "authority_state",
    }, "root observations")
    if len(root_set) != args.expected_roots or len(root_observations) != args.expected_roots:
        fail("root denominator mismatch")
    root_set_by_id = {row["root_review_id"]: row for row in root_set}
    root_obs_by_id = {row["root_review_id"]: row for row in root_observations}
    if len(root_set_by_id) != args.expected_roots or set(root_set_by_id) != set(root_obs_by_id):
        fail("root identity set mismatch")

    require_fields(recipe_files, {"recipe_root", "recipe_tree", "path", "mode", "blob_oid", "size", "content_sha256", "file_class", "semantic_review_state"}, "recipe file evidence")
    require_fields(signals, {"recipe_root", "recipe_tree", "path", "line_number", "signal_classes", "line_sha256", "line_text", "semantic_classification_state"}, "build script signal evidence")
    if len(recipe_files) != args.expected_recipe_files or len(signals) != args.expected_signals:
        fail("recipe file/signal denominator mismatch")
    file_counts = Counter(row["recipe_root"] for row in recipe_files)
    signal_counts = Counter(row["recipe_root"] for row in signals)
    if len({(row["recipe_root"], row["path"]) for row in recipe_files}) != len(recipe_files):
        fail("duplicate recipe file evidence row")
    if any(row["semantic_review_state"] != "NOT_PERFORMED_EVIDENCE_INVENTORY_ONLY" for row in recipe_files):
        fail("recipe file semantic acceptance detected")
    if any(row["semantic_classification_state"] != "UNCLASSIFIED_SYNTACTIC_SIGNAL_ONLY" for row in signals):
        fail("build script signal semantic classification detected")

    root_review_rows: list[dict[str, object]] = []
    for root_id in sorted(root_set_by_id):
        canonical = root_set_by_id[root_id]
        receipt = root_obs_by_id[root_id]
        for field in (
            "review_tier", "recipe_root", "recipe_tree", "recipe_resolved_full_version",
            "artifact_count", "identity_count", "adaptation_evidence_tokens",
        ):
            if receipt[field] != canonical[field]:
                fail(f"root {root_id} canonical field drift: {field}")
        if receipt["authority_state"] != AUTHORITY_STATE:
            fail(f"root {root_id} authority promotion detected")
        if receipt["build_provenance_collection_state"] != "EXTERNAL_DIGEST_BOUND_BUILD_RECORD_REQUIRED":
            fail(f"root {root_id} build provenance state drifted")
        if receipt["recipe_inventory_collection_state"] != "COMPLETE_PINNED_RECIPE_FILE_INVENTORY_COLLECTED":
            fail(f"root {root_id} recipe inventory state drifted")
        if receipt["upstream_semantic_comparison_state"] != "NOT_PERFORMED_REQUIRES_BOUNDED_SEMANTIC_REVIEW":
            fail(f"root {root_id} upstream comparison state drifted")
        if receipt["adaptation_classification_state"] != "OPEN_NO_NECESSITY_CLASSIFICATION":
            fail(f"root {root_id} adaptation classification state drifted")
        if receipt["update_rollback_state"] != "OPEN_NO_CONTINUITY_POLICY":
            fail(f"root {root_id} continuity state drifted")
        if as_int(receipt["recipe_file_count"], "recipe_file_count") != file_counts[receipt["recipe_root"]]:
            fail(f"root {root_id} recipe file count mismatch")
        if as_int(receipt["build_script_signal_count"], "build_script_signal_count") != signal_counts[receipt["recipe_root"]]:
            fail(f"root {root_id} signal count mismatch")
        semantic_state = (
            "FULL_NO_TOKEN_SEMANTIC_REVIEW_OPEN"
            if receipt["adaptation_evidence_tokens"] == "NONE_DECLARED"
            else "RECIPE_DELTA_SEMANTIC_REVIEW_OPEN"
        )
        correction_state = (
            "OBJECT_REQUIREMENT_CORRECTION_OPEN"
            if receipt["review_tier"] == "T0_OBJECT_REQUIREMENT_CORRECTION"
            else "NOT_APPLICABLE"
        )
        root_review_rows.append({
            "root_review_id": root_id,
            "review_tier": receipt["review_tier"],
            "recipe_root": receipt["recipe_root"],
            "recipe_tree": receipt["recipe_tree"],
            "recipe_resolved_full_version": receipt["recipe_resolved_full_version"],
            "recipe_file_count": receipt["recipe_file_count"],
            "build_script_signal_count": receipt["build_script_signal_count"],
            "artifact_count": receipt["artifact_count"],
            "identity_count": receipt["identity_count"],
            "recipe_inventory_review_state": "PINNED_RECIPE_FILE_AND_SIGNAL_INVENTORY_CONFIRMED",
            "build_provenance_review_state": "OPEN_EXTERNAL_DIGEST_BOUND_BUILD_RECORD_REQUIRED",
            "adaptation_semantic_review_state": semantic_state,
            "adaptation_necessity_review_state": "OPEN_CLASSIFICATION_REQUIRED",
            "continuity_policy_review_state": "OPEN_UPDATE_ROLLBACK_POLICY_REQUIRED",
            "object_correction_review_state": correction_state,
            "authority_state": AUTHORITY_STATE,
        })
    if sum(as_int(row["identity_count"], "identity_count") for row in root_observations) != args.expected_objects:
        fail("root identity total mismatch")
    if sum(as_int(row["artifact_count"], "artifact_count") for row in root_observations) != args.expected_root_artifact_references:
        fail("root artifact-reference total mismatch")

    require_fields(object_set, {
        "object_review_id", "evidence_row_id", "review_tier", "capability_partition", "identity_label",
        "artifact_id", "artifact_package", "artifact_version", "artifact_sha256", "recipe_root",
        "recipe_tree", "object_member_review_state", "review_eligibility_state", "authority_state",
        "target_population_state",
    }, "object review set")
    require_fields(crosswalk, {
        "root_review_id", "object_review_id", "evidence_row_id", "recipe_root", "identity_label",
        "artifact_id", "adaptation_evidence_tokens", "adaptation_requirement_set",
        "object_impact_evidence_state", "authority_state",
    }, "root-object crosswalk")
    require_fields(outputs, {
        "object_review_id", "evidence_row_id", "identity_label", "artifact_id", "artifact_package",
        "artifact_version", "artifact_sha256", "recipe_root", "recipe_tree", "member_path",
        "member_sha256", "observed_soname", "alias_member_path", "alias_link_target",
        "output_binding_evidence_state", "producing_build_binding_state", "authority_state",
        "target_population_state",
    }, "artifact/member output evidence")
    if len(object_set) != args.expected_objects or len(crosswalk) != args.expected_objects or len(outputs) != args.expected_objects:
        fail("object denominator mismatch")
    object_set_by_id = {row["object_review_id"]: row for row in object_set}
    crosswalk_by_id = {row["object_review_id"]: row for row in crosswalk}
    output_by_id = {row["object_review_id"]: row for row in outputs}
    if len(object_set_by_id) != args.expected_objects or set(object_set_by_id) != set(crosswalk_by_id) or set(object_set_by_id) != set(output_by_id):
        fail("object identity set mismatch")

    output_classes = Counter(row["output_binding_evidence_state"] for row in outputs)
    expected_output_classes = {
        "EXACT_MEMBER_DIGEST_AND_SONAME_OBSERVED_NOT_BUILD_ATTESTED": args.expected_exact_outputs,
        "ALIAS_TARGET_MEMBER_DIGEST_AND_SONAME_OBSERVED_NOT_BUILD_ATTESTED": args.expected_drift_outputs,
        "OBJECT_REQUIREMENT_UNSATISFIED_NO_OUTPUT_BINDING": args.expected_blocked_outputs,
    }
    if dict(output_classes) != expected_output_classes:
        fail(f"output evidence classes mismatch: {output_classes}")

    object_review_rows: list[dict[str, object]] = []
    for object_id in sorted(object_set_by_id):
        canonical = object_set_by_id[object_id]
        link = crosswalk_by_id[object_id]
        output = output_by_id[object_id]
        for field in ("evidence_row_id", "identity_label", "artifact_id", "recipe_root"):
            if link[field] != canonical[field] or output[field] != canonical[field]:
                fail(f"object {object_id} canonical field drift: {field}")
        for field in ("artifact_package", "artifact_version", "artifact_sha256", "recipe_tree"):
            if output[field] != canonical[field]:
                fail(f"object {object_id} output field drift: {field}")
        if link["root_review_id"] not in root_set_by_id or link["authority_state"] != AUTHORITY_STATE:
            fail(f"object {object_id} crosswalk state drifted")
        if link["object_impact_evidence_state"] != "ROOT_OBJECT_CROSSWALK_COLLECTED_SEMANTIC_IMPACT_REVIEW_OPEN":
            fail(f"object {object_id} impact state drifted")
        if output["producing_build_binding_state"] != "OPEN_NO_DIGEST_BOUND_BUILD_RECORD":
            fail(f"object {object_id} producing build binding promotion detected")
        if output["authority_state"] != AUTHORITY_STATE or output["target_population_state"] != TARGET_STATE:
            fail(f"object {object_id} authority/target promotion detected")

        output_class = output["output_binding_evidence_state"]
        if output_class == "EXACT_MEMBER_DIGEST_AND_SONAME_OBSERVED_NOT_BUILD_ATTESTED":
            if "EXACT_MEMBER" not in canonical["object_member_review_state"]:
                fail(f"object {object_id} exact class conflicts with review set")
            if any(output[field] == "-" for field in ("member_path", "member_sha256", "observed_soname")):
                fail(f"object {object_id} incomplete exact output evidence")
            output_review = "EXACT_MEMBER_DIGEST_AND_SONAME_CONFIRMED_REVIEW_INPUT"
            consumer_review = "NOT_APPLICABLE_NO_CONCRETE_FILENAME_DRIFT"
            drift_review = "NOT_APPLICABLE_NO_CONCRETE_FILENAME_DRIFT"
            correction_review = "NOT_APPLICABLE"
        elif output_class == "ALIAS_TARGET_MEMBER_DIGEST_AND_SONAME_OBSERVED_NOT_BUILD_ATTESTED":
            if "DRIFT_TARGET" not in canonical["object_member_review_state"]:
                fail(f"object {object_id} drift class conflicts with review set")
            if any(output[field] == "-" for field in ("member_path", "member_sha256", "observed_soname", "alias_member_path", "alias_link_target")):
                fail(f"object {object_id} incomplete drift output evidence")
            output_review = "ALIAS_TARGET_MEMBER_DIGEST_AND_SONAME_CONFIRMED_REVIEW_INPUT"
            consumer_review = "OPEN_CONSUMER_BINDING_EVIDENCE_REQUIRED"
            drift_review = "OPEN_SUCCESSOR_AND_ROLLBACK_FILENAME_POLICY_REQUIRED"
            correction_review = "NOT_APPLICABLE"
        else:
            if canonical["identity_label"] != "libjpeg.so.62.3.0" or canonical["review_tier"] != "T0_OBJECT_REQUIREMENT_CORRECTION":
                fail(f"object {object_id} unexpected blocked identity")
            if any(output[field] != "-" for field in ("member_path", "member_sha256", "observed_soname", "alias_member_path", "alias_link_target")):
                fail(f"object {object_id} blocked row contains output binding")
            output_review = "NO_OUTPUT_BINDING_OBJECT_REQUIREMENT_UNSATISFIED"
            consumer_review = "NOT_APPLICABLE_OBJECT_REQUIREMENT_UNSATISFIED"
            drift_review = "NOT_APPLICABLE_OBJECT_REQUIREMENT_UNSATISFIED"
            correction_review = "OPEN_CORRECT_REQUIREMENT_OR_LOCATE_EXACT_SONAME_CANDIDATE"

        object_review_rows.append({
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
            "member_path": output["member_path"],
            "member_sha256": output["member_sha256"],
            "observed_soname": output["observed_soname"],
            "alias_member_path": output["alias_member_path"],
            "alias_link_target": output["alias_link_target"],
            "output_evidence_review_state": output_review,
            "build_binding_review_state": "OPEN_NO_DIGEST_BOUND_PRODUCING_BUILD_RECORD",
            "adaptation_impact_review_state": "OPEN_SEMANTIC_OBJECT_IMPACT_REVIEW_REQUIRED",
            "consumer_binding_review_state": consumer_review,
            "filename_drift_policy_review_state": drift_review,
            "object_requirement_review_state": correction_review,
            "final_provider_state": "UNRESOLVED",
            "authority_state": AUTHORITY_STATE,
            "target_population_state": TARGET_STATE,
        })

    args.out.mkdir(parents=True)
    requirement_out = args.out / "generic-build-attestation-adaptation-evidence-receipt-review.tsv"
    root_out = args.out / "generic-build-attestation-adaptation-root-evidence-receipt-review.tsv"
    object_out = args.out / "generic-build-attestation-adaptation-object-evidence-receipt-review.tsv"
    metadata_out = args.out / "generic-build-attestation-adaptation-evidence-receipt-metadata.tsv"

    write_tsv(requirement_out, [
        "requirement_id", "dimension", "scope", "collection_state", "evidence_references",
        "evidence_class", "receipt_review_state", "remaining_gap_class", "next_action", "authority_state",
    ], requirement_review_rows)
    write_tsv(root_out, [
        "root_review_id", "review_tier", "recipe_root", "recipe_tree", "recipe_resolved_full_version",
        "recipe_file_count", "build_script_signal_count", "artifact_count", "identity_count",
        "recipe_inventory_review_state", "build_provenance_review_state",
        "adaptation_semantic_review_state", "adaptation_necessity_review_state",
        "continuity_policy_review_state", "object_correction_review_state", "authority_state",
    ], root_review_rows)
    write_tsv(object_out, [
        "object_review_id", "evidence_row_id", "review_tier", "capability_partition", "identity_label",
        "artifact_id", "artifact_package", "artifact_version", "artifact_sha256", "recipe_root",
        "recipe_tree", "member_path", "member_sha256", "observed_soname", "alias_member_path",
        "alias_link_target", "output_evidence_review_state", "build_binding_review_state",
        "adaptation_impact_review_state", "consumer_binding_review_state",
        "filename_drift_policy_review_state", "object_requirement_review_state",
        "final_provider_state", "authority_state", "target_population_state",
    ], object_review_rows)

    metadata_rows = [
        {"field": "source_receipt_archive", "value": args.source_receipt_archive},
        {"field": "source_receipt_sha256", "value": args.source_receipt_sha256},
        {"field": "source_repository_branch", "value": args.expected_branch},
        {"field": "source_repository_head", "value": args.expected_source_head},
        {"field": "source_repository_tree", "value": args.expected_source_tree},
        {"field": "requirements_sha256", "value": sha256(args.requirements)},
        {"field": "root_review_set_sha256", "value": sha256(args.root_review_set)},
        {"field": "object_review_set_sha256", "value": sha256(args.object_review_set)},
        {"field": "review_rules_sha256", "value": sha256(args.rules)},
        {"field": "requirement_receipt_sha256", "value": sha256(args.requirement_status)},
        {"field": "root_observations_sha256", "value": sha256(args.root_observations)},
        {"field": "artifact_member_output_sha256", "value": sha256(args.artifact_member_output)},
        {"field": "external_gaps_sha256", "value": sha256(args.external_gaps)},
        {"field": "requirement_review_sha256", "value": sha256(requirement_out)},
        {"field": "root_review_sha256", "value": sha256(root_out)},
        {"field": "object_review_sha256", "value": sha256(object_out)},
        {"field": "requirement_rows", "value": str(args.expected_requirements)},
        {"field": "local_evidence_requirement_rows", "value": str(args.expected_requirements - args.expected_gaps)},
        {"field": "gap_requirement_rows", "value": str(args.expected_gaps)},
        {"field": "root_review_rows", "value": str(args.expected_roots)},
        {"field": "object_review_rows", "value": str(args.expected_objects)},
        {"field": "exact_output_rows", "value": str(args.expected_exact_outputs)},
        {"field": "drift_output_rows", "value": str(args.expected_drift_outputs)},
        {"field": "blocked_object_rows", "value": str(args.expected_blocked_outputs)},
        {"field": "artifact_build_attestations_accepted", "value": "0"},
        {"field": "termux_android_adaptations_accepted", "value": "0"},
        {"field": "concrete_filename_drifts_accepted", "value": "0"},
        {"field": "final_provider_decisions_accepted", "value": "0"},
        {"field": "target_rows_populated", "value": "0"},
        {"field": "next_state", "value": args.next_state},
    ]
    write_tsv(metadata_out, ["field", "value"], metadata_rows)
    print("generic build attestation/adaptation evidence receipt review: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
