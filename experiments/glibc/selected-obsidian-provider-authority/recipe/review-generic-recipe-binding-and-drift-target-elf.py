#!/usr/bin/env python3
"""Review the bounded generic recipe-binding and drift-target ELF receipt.

This reviewer validates source lineage, cached artifact identity, recipe-file
manifests and drift-target ELF observations without accepting build provenance,
adaptation semantics, final provider authority or target population.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, NoReturn

EXPECTED_IDENTITIES = 37
EXPECTED_DRIFT_ROWS = 15
EXPECTED_ARTIFACTS = 34
EXPECTED_SELECTED_ARTIFACTS = 29
EXPECTED_RECIPE_ROOTS = 28
EXPECTED_RECIPE_FILES = 84
EXPECTED_SOURCE_HEAD = "fd2ae25e04f3ea26d6c7b4678020814889331d86"
EXPECTED_SOURCE_TREE = "e502a4c18ab9092ec119e3a498a0bf192ef60e6f"
EXPECTED_SOURCE_ORIGIN = "https://github.com/termux-pacman/glibc-packages.git"
NEXT_STATE = "DEFINE_BOUNDED_GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_REVIEW_SET"

REVIEW_POLICY = "LINEAGE_ADAPTATION_AND_OBJECT_EVIDENCE_ONLY_NOT_AUTHORITY"
ALLOWED_ADAPTATION_TOKENS = {
    "PATCH_FILE",
    "SUBPACKAGE_SCRIPT",
    "LAYOUT_OR_HOOK",
    "EXTRA_CONFIGURE_ARGS",
    "CUSTOM_TERMUX_STEP",
    "TERMUX_PREFIX_REFERENCE",
    "BUILD_IN_SRC",
    "PACKAGE_REVISION",
}
MATERIAL_DELTA_TOKENS = {"PATCH_FILE", "CUSTOM_TERMUX_STEP", "LAYOUT_OR_HOOK"}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"generic recipe binding and drift target ELF receipt review: FAIL: {message}")


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


def bytes_sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


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


def adaptation_state(value: str) -> tuple[str, set[str]]:
    if value == "NONE_DECLARED":
        return "NO_EXPLICIT_DELTA_TOKEN_OBSERVED_SEMANTIC_REVIEW_OPEN", set()
    tokens = value.split(";")
    if tokens != sorted(set(tokens)) or any(token not in ALLOWED_ADAPTATION_TOKENS for token in tokens):
        fail(f"invalid adaptation token set: {value}")
    token_set = set(tokens)
    if token_set & MATERIAL_DELTA_TOKENS:
        return "MATERIAL_RECIPE_DELTA_EVIDENCE_SEMANTIC_REVIEW_REQUIRED", token_set
    return "CONFIGURATION_OR_PACKAGING_DELTA_EVIDENCE_SEMANTIC_REVIEW_REQUIRED", token_set


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules", required=True, type=Path)
    parser.add_argument("--binding-receipt", required=True, type=Path)
    parser.add_argument("--drift-receipt", required=True, type=Path)
    parser.add_argument("--artifact-verification", required=True, type=Path)
    parser.add_argument("--artifact-registry", required=True, type=Path)
    parser.add_argument("--recipe-inventory", required=True, type=Path)
    parser.add_argument("--source-state", required=True, type=Path)
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--source-receipt-archive", required=True)
    parser.add_argument("--source-receipt-sha256", required=True)
    parser.add_argument("--expected-identities", type=int, default=EXPECTED_IDENTITIES)
    parser.add_argument("--expected-drift-rows", type=int, default=EXPECTED_DRIFT_ROWS)
    parser.add_argument("--expected-artifacts", type=int, default=EXPECTED_ARTIFACTS)
    parser.add_argument("--expected-selected-artifacts", type=int, default=EXPECTED_SELECTED_ARTIFACTS)
    parser.add_argument("--expected-recipe-roots", type=int, default=EXPECTED_RECIPE_ROOTS)
    parser.add_argument("--expected-recipe-files", type=int, default=EXPECTED_RECIPE_FILES)
    parser.add_argument("--expected-source-head", default=EXPECTED_SOURCE_HEAD)
    parser.add_argument("--expected-source-tree", default=EXPECTED_SOURCE_TREE)
    parser.add_argument("--expected-source-origin", default=EXPECTED_SOURCE_ORIGIN)
    parser.add_argument("--next-state", default=NEXT_STATE)
    args = parser.parse_args()

    if args.out.exists() or args.out.is_symlink():
        fail(f"refusing existing output: {args.out}")
    if not valid_sha256(args.source_receipt_sha256):
        fail("invalid source receipt SHA-256")

    rules = read_tsv(args.rules)
    binding = read_tsv(args.binding_receipt)
    drift = read_tsv(args.drift_receipt)
    artifact_verification = read_tsv(args.artifact_verification)
    artifact_registry = read_tsv(args.artifact_registry)
    recipe_inventory = read_tsv(args.recipe_inventory)
    source_state = read_tsv(args.source_state)
    summary_rows = read_tsv(args.summary)

    required_rule_fields = {
        "evidence_row_id", "capability_partition", "identity_label", "expected_artifact_id",
        "expected_artifact_package", "expected_artifact_version", "expected_artifact_sha256",
        "expected_soname_alias", "expected_member_receipt_review_state", "expected_alias_member_path",
        "expected_alias_target_member_path", "expected_recipe_root", "expected_recipe_tree",
        "expected_recipe_resolved_full_version", "expected_recipe_source_url_raw",
        "expected_recipe_source_sha256", "expected_recipe_file_manifest_sha256",
        "expected_drift_target_input_state", "receipt_review_policy", "authority_state",
    }
    require_fields(rules, required_rule_fields, "review rules")
    if len(rules) != args.expected_identities:
        fail(f"review rule denominator {len(rules)} != {args.expected_identities}")
    rule_ids = [row["evidence_row_id"] for row in rules]
    if len(rule_ids) != len(set(rule_ids)):
        fail("duplicate evidence_row_id in review rules")
    if any(row["receipt_review_policy"] != REVIEW_POLICY or row["authority_state"] != "CANDIDATE_ONLY" for row in rules):
        fail("review policy or authority stop state drifted")
    rule_by_id = {row["evidence_row_id"]: row for row in rules}

    required_binding_fields = {
        "evidence_row_id", "capability_partition", "identity_label", "member_receipt_review_state",
        "artifact_id", "artifact_package", "artifact_version", "artifact_sha256", "recipe_root",
        "recipe_tree", "recipe_resolved_full_version", "recipe_source_url_raw", "recipe_source_sha256",
        "recipe_file_manifest_sha256", "adaptation_evidence_tokens", "recipe_lineage_candidate_state",
        "artifact_to_recipe_binding_state", "termux_android_adaptation_state",
        "drift_target_elf_review_state", "final_provider_state", "target_population_state",
    }
    require_fields(binding, required_binding_fields, "recipe binding receipt")
    if len(binding) != args.expected_identities or {row["evidence_row_id"] for row in binding} != set(rule_ids):
        fail("recipe binding receipt identity denominator/set mismatch")
    binding_by_id = {row["evidence_row_id"]: row for row in binding}

    required_drift_fields = {
        "evidence_row_id", "identity_label", "artifact_id", "artifact_package", "expected_soname_alias",
        "alias_member_path", "target_member_path", "target_member_size", "target_member_mode_octal",
        "target_member_sha256", "elf_parse_state", "elf_class", "elf_data", "elf_machine",
        "observed_soname", "drift_target_elf_review_state", "object_member_evidence_state",
        "artifact_to_recipe_binding_state", "termux_android_adaptation_state", "final_provider_state",
        "target_population_state",
    }
    require_fields(drift, required_drift_fields, "drift target receipt")
    if len(drift) != args.expected_drift_rows:
        fail(f"drift receipt denominator {len(drift)} != {args.expected_drift_rows}")
    drift_ids = [row["evidence_row_id"] for row in drift]
    if len(drift_ids) != len(set(drift_ids)):
        fail("duplicate evidence_row_id in drift receipt")
    drift_by_id = {row["evidence_row_id"]: row for row in drift}

    required_artifact_fields = {
        "artifact_id", "package", "version", "architecture", "actual_size", "actual_sha256",
        "control_identity_state", "package_operation_performed",
    }
    require_fields(artifact_verification, required_artifact_fields, "artifact verification receipt")
    require_fields(
        artifact_registry,
        {"artifact_id", "package", "version", "architecture", "artifact_size", "artifact_sha256"},
        "artifact registry",
    )
    if len(artifact_verification) != args.expected_artifacts or len(artifact_registry) != args.expected_artifacts:
        fail("artifact verification/registry denominator mismatch")
    artifact_registry_by_id = {row["artifact_id"]: row for row in artifact_registry}
    if len(artifact_registry_by_id) != args.expected_artifacts:
        fail("duplicate artifact ID in artifact registry")
    if {row["artifact_id"] for row in artifact_verification} != set(artifact_registry_by_id):
        fail("artifact verification identity set differs from registry")
    for row in artifact_verification:
        expected = artifact_registry_by_id[row["artifact_id"]]
        if [row["package"], row["version"], row["architecture"]] != [expected["package"], expected["version"], expected["architecture"]]:
            fail(f"artifact control identity drift: {row['artifact_id']}")
        if row["actual_size"] != expected["artifact_size"] or row["actual_sha256"] != expected["artifact_sha256"]:
            fail(f"artifact byte identity drift: {row['artifact_id']}")
        if row["control_identity_state"] != "EXACT_PACKAGE_VERSION_ARCHITECTURE_MATCH" or row["package_operation_performed"] != "NO":
            fail(f"artifact verification promoted or mutated package state: {row['artifact_id']}")

    required_source_fields = {"head", "tree", "origin", "is_shallow", "is_bare", "worktree_state", "fsck_state"}
    require_fields(source_state, required_source_fields, "source repository state")
    if len(source_state) != 1:
        fail("source repository state must contain one row")
    source = source_state[0]
    if source["head"] != args.expected_source_head or source["tree"] != args.expected_source_tree or source["origin"] != args.expected_source_origin:
        fail("source repository identity mismatch")
    if source["is_shallow"] != "false" or source["is_bare"] != "false" or source["worktree_state"] != "CLEAN" or source["fsck_state"] != "PASS":
        fail("source repository cleanliness/integrity state mismatch")

    required_inventory_fields = {"recipe_root", "path", "mode", "blob_oid", "size", "content_sha256"}
    require_fields(recipe_inventory, required_inventory_fields, "recipe file inventory")
    if len(recipe_inventory) != args.expected_recipe_files:
        fail(f"recipe file denominator {len(recipe_inventory)} != {args.expected_recipe_files}")
    inventory_keys = [(row["recipe_root"], row["path"]) for row in recipe_inventory]
    if len(inventory_keys) != len(set(inventory_keys)):
        fail("duplicate recipe inventory path")
    inventory_by_root: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in recipe_inventory:
        if not valid_oid(row["blob_oid"]) or not valid_sha256(row["content_sha256"]):
            fail(f"invalid recipe blob/hash identity: {row['path']}")
        try:
            size = int(row["size"])
        except ValueError:
            fail(f"invalid recipe file size: {row['path']}")
        if size < 0 or not re.fullmatch(r"[0-7]{6}", row["mode"]):
            fail(f"invalid recipe file metadata: {row['path']}")
        inventory_by_root[row["recipe_root"]].append(row)
    expected_roots = {row["expected_recipe_root"] for row in rules}
    if len(expected_roots) != args.expected_recipe_roots or set(inventory_by_root) != expected_roots:
        fail("recipe root denominator/set mismatch")
    manifest_by_root: dict[str, str] = {}
    for root, rows in inventory_by_root.items():
        ordered = sorted(rows, key=lambda row: row["path"])
        payload = "".join(
            f"{row['path']}\t{row['blob_oid']}\t{row['size']}\t{row['content_sha256']}\n"
            for row in ordered
        ).encode()
        manifest_by_root[root] = bytes_sha256(payload)

    summary = {row["field"]: row["value"] for row in summary_rows}
    required_summary = {
        "source_repository_head": args.expected_source_head,
        "source_repository_tree": args.expected_source_tree,
        "review_identity_rows": str(args.expected_identities),
        "unique_recipe_roots": str(args.expected_recipe_roots),
        "selected_rule_artifacts": str(args.expected_selected_artifacts),
        "verified_cached_artifacts": str(args.expected_artifacts),
        "recipe_family_version_aligned_rows": str(args.expected_identities),
        "drift_target_elf_rows": str(args.expected_drift_rows),
        "drift_target_expected_soname_confirmed": str(args.expected_drift_rows),
        "expected_alias_absent_correct_candidate_required": "1" if args.expected_identities == EXPECTED_IDENTITIES else summary.get("expected_alias_absent_correct_candidate_required", ""),
        "artifact_to_recipe_bindings_accepted": "0",
        "termux_android_adaptations_accepted": "0",
        "final_provider_decisions_accepted": "0",
        "target_rows_populated": "0",
        "next_state": "REVIEW_BOUNDED_GENERIC_RECIPE_BINDING_AND_DRIFT_TARGET_ELF_RECEIPT",
    }
    for field, expected in required_summary.items():
        if summary.get(field) != expected:
            fail(f"collector summary mismatch for {field}: {summary.get(field)!r} != {expected!r}")

    selected_artifact_ids = {row["expected_artifact_id"] for row in rules}
    if len(selected_artifact_ids) != args.expected_selected_artifacts:
        fail("selected artifact denominator drifted")

    output: list[dict[str, object]] = []
    counts: Counter[str] = Counter()
    adaptation_counts: Counter[str] = Counter()
    for rule in sorted(rules, key=lambda row: row["evidence_row_id"]):
        evidence_id = rule["evidence_row_id"]
        row = binding_by_id[evidence_id]
        comparisons = {
            "capability_partition": rule["capability_partition"],
            "identity_label": rule["identity_label"],
            "member_receipt_review_state": rule["expected_member_receipt_review_state"],
            "artifact_id": rule["expected_artifact_id"],
            "artifact_package": rule["expected_artifact_package"],
            "artifact_version": rule["expected_artifact_version"],
            "artifact_sha256": rule["expected_artifact_sha256"],
            "recipe_root": rule["expected_recipe_root"],
            "recipe_tree": rule["expected_recipe_tree"],
            "recipe_resolved_full_version": rule["expected_recipe_resolved_full_version"],
            "recipe_source_url_raw": rule["expected_recipe_source_url_raw"],
            "recipe_source_sha256": rule["expected_recipe_source_sha256"],
            "recipe_file_manifest_sha256": rule["expected_recipe_file_manifest_sha256"],
        }
        for field, expected in comparisons.items():
            if row[field] != expected:
                fail(f"binding receipt drift for {evidence_id} field {field}")
        if manifest_by_root[row["recipe_root"]] != row["recipe_file_manifest_sha256"]:
            fail(f"recipe file manifest cannot be reproduced for {evidence_id}")
        if row["recipe_lineage_candidate_state"] != "PINNED_RECIPE_FAMILY_VERSION_ALIGNED_CANDIDATE":
            fail(f"recipe lineage state drift for {evidence_id}")
        if row["artifact_to_recipe_binding_state"] != "OPEN_NO_BUILD_ATTESTATION":
            fail(f"artifact-to-recipe binding was promoted for {evidence_id}")
        if row["termux_android_adaptation_state"] != "PINNED_RECIPE_ADAPTATION_EVIDENCE_INVENTORIED_REVIEW_OPEN":
            fail(f"adaptation state was promoted for {evidence_id}")
        if row["final_provider_state"] != "UNRESOLVED" or row["target_population_state"] != "BLOCKED":
            fail(f"final authority or target population was promoted for {evidence_id}")

        adaptation_review, _tokens = adaptation_state(row["adaptation_evidence_tokens"])
        adaptation_counts[adaptation_review] += 1
        drift_row = drift_by_id.get(evidence_id)
        member_state = row["member_receipt_review_state"]
        expected_input_state = rule["expected_drift_target_input_state"]
        expected_input_by_member = {
            "EXACT_CONCRETE_MEMBER_AND_EXPECTED_SONAME_OBSERVED": "NOT_REQUIRED_EXACT_MEMBER_ALREADY_OBSERVED",
            "EXPECTED_SONAME_ALIAS_SYMLINK_PRESENT_CONCRETE_FILENAME_DRIFT": "PENDING_READ_ONLY_TARGET_ELF_INSPECTION",
            "EXPECTED_SONAME_ALIAS_NOT_OBSERVED_DIFFERENT_FAMILY_MEMBERS_PRESENT": "NOT_APPLICABLE_EXPECTED_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED",
        }
        if expected_input_by_member.get(member_state) != expected_input_state:
            fail(f"review rule drift-target input state is inconsistent for {evidence_id}")
        drift_path = drift_hash = drift_soname = "-"
        if member_state == "EXACT_CONCRETE_MEMBER_AND_EXPECTED_SONAME_OBSERVED":
            if row["drift_target_elf_review_state"] != "NOT_REQUIRED_EXACT_MEMBER_ALREADY_OBSERVED" or drift_row is not None:
                fail(f"unexpected drift target evidence for exact row {evidence_id}")
            object_state = "EXACT_MEMBER_EXPECTED_SONAME_CANDIDATE_CONFIRMED"
            concrete_policy = "NOT_APPLICABLE_EXACT_CONCRETE_MEMBER"
            eligibility = "OBJECT_MEMBER_EVIDENCE_COMPLETE_BUILD_AND_ADAPTATION_REVIEW_REQUIRED"
        elif member_state == "EXPECTED_SONAME_ALIAS_SYMLINK_PRESENT_CONCRETE_FILENAME_DRIFT":
            if drift_row is None:
                fail(f"missing drift target receipt for {evidence_id}")
            expected_drift = {
                "identity_label": rule["identity_label"],
                "artifact_id": rule["expected_artifact_id"],
                "artifact_package": rule["expected_artifact_package"],
                "expected_soname_alias": rule["expected_soname_alias"],
                "alias_member_path": rule["expected_alias_member_path"].removeprefix("./"),
                "target_member_path": rule["expected_alias_target_member_path"].removeprefix("./"),
            }
            for field, expected in expected_drift.items():
                if drift_row[field] != expected:
                    fail(f"drift target receipt mismatch for {evidence_id} field {field}")
            if (
                row["drift_target_elf_review_state"] != "DRIFT_TARGET_ELF_EXPECTED_SONAME_CONFIRMED"
                or drift_row["drift_target_elf_review_state"] != "DRIFT_TARGET_ELF_EXPECTED_SONAME_CONFIRMED"
                or drift_row["elf_parse_state"] != "ELF_SONAME_PARSED"
                or drift_row["elf_class"] != "ELF64"
                or drift_row["elf_data"] != "LITTLE"
                or drift_row["elf_machine"] != "183"
                or drift_row["observed_soname"] != rule["expected_soname_alias"]
                or not valid_sha256(drift_row["target_member_sha256"])
            ):
                fail(f"drift target ELF evidence incomplete or mismatched for {evidence_id}")
            if (
                drift_row["object_member_evidence_state"] != "OBSERVED_CANDIDATE_NOT_AUTHORITY_ACCEPTED"
                or drift_row["artifact_to_recipe_binding_state"] != "OPEN_NO_BUILD_ATTESTATION"
                or drift_row["termux_android_adaptation_state"] != "OPEN_REVIEW_REQUIRED"
                or drift_row["final_provider_state"] != "UNRESOLVED"
                or drift_row["target_population_state"] != "BLOCKED"
            ):
                fail(f"drift target receipt promoted authority for {evidence_id}")
            object_state = "DRIFT_TARGET_ELF_EXPECTED_SONAME_CANDIDATE_CONFIRMED"
            concrete_policy = "OPEN_EXPECTED_SONAME_MATCH_ONLY_CONCRETE_FILENAME_DRIFT_NOT_ACCEPTED"
            eligibility = "OBJECT_MEMBER_EVIDENCE_COMPLETE_BUILD_ADAPTATION_AND_DRIFT_REVIEW_REQUIRED"
            drift_path = drift_row["target_member_path"]
            drift_hash = drift_row["target_member_sha256"]
            drift_soname = drift_row["observed_soname"]
        elif member_state == "EXPECTED_SONAME_ALIAS_NOT_OBSERVED_DIFFERENT_FAMILY_MEMBERS_PRESENT":
            if row["drift_target_elf_review_state"] != "NOT_APPLICABLE_EXPECTED_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED" or drift_row is not None:
                fail(f"alias-absent row has invalid drift state for {evidence_id}")
            object_state = "EXPECTED_SONAME_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED"
            concrete_policy = "BLOCKED_EXPECTED_ALIAS_ABSENT"
            eligibility = "OBJECT_MEMBER_REQUIREMENT_UNSATISFIED"
        else:
            fail(f"unknown member receipt state for {evidence_id}: {member_state}")

        counts[object_state] += 1
        if eligibility == "OBJECT_MEMBER_REQUIREMENT_UNSATISFIED":
            next_action = "CORRECT_OBJECT_REQUIREMENT_OR_LOCATE_MATCHING_EXPECTED_SONAME_CANDIDATE"
        elif concrete_policy.startswith("OPEN_"):
            next_action = "DEFINE_BUILD_ATTESTATION_ADAPTATION_AND_CONCRETE_DRIFT_ACCEPTANCE_REQUIREMENTS"
        else:
            next_action = "DEFINE_BUILD_ATTESTATION_AND_ADAPTATION_REVIEW_REQUIREMENTS"

        output.append({
            "evidence_row_id": evidence_id,
            "capability_partition": row["capability_partition"],
            "identity_label": row["identity_label"],
            "artifact_id": row["artifact_id"],
            "artifact_package": row["artifact_package"],
            "artifact_version": row["artifact_version"],
            "artifact_sha256": row["artifact_sha256"],
            "recipe_root": row["recipe_root"],
            "recipe_tree": row["recipe_tree"],
            "recipe_resolved_full_version": row["recipe_resolved_full_version"],
            "recipe_source_url_raw": row["recipe_source_url_raw"],
            "recipe_source_sha256": row["recipe_source_sha256"],
            "recipe_file_manifest_sha256": row["recipe_file_manifest_sha256"],
            "adaptation_evidence_tokens": row["adaptation_evidence_tokens"],
            "recipe_lineage_review_state": "PINNED_RECIPE_LINEAGE_CANDIDATE_CONFIRMED",
            "artifact_build_attestation_review_state": "OPEN_NO_INDEPENDENT_BUILD_PROVENANCE_OR_BYTE_REPRODUCTION",
            "adaptation_semantic_review_state": adaptation_review,
            "member_receipt_review_state": member_state,
            "object_member_review_state": object_state,
            "drift_target_member_path": drift_path,
            "drift_target_member_sha256": drift_hash,
            "drift_target_observed_soname": drift_soname,
            "concrete_filename_policy_state": concrete_policy,
            "provider_review_eligibility_state": eligibility,
            "final_provider_state": "UNRESOLVED",
            "target_population_state": "BLOCKED",
            "next_action": next_action,
        })

    expected_object_counts = Counter({
        "EXACT_MEMBER_EXPECTED_SONAME_CANDIDATE_CONFIRMED": 21,
        "DRIFT_TARGET_ELF_EXPECTED_SONAME_CANDIDATE_CONFIRMED": 15,
        "EXPECTED_SONAME_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED": 1,
    }) if args.expected_identities == EXPECTED_IDENTITIES else counts
    if counts != expected_object_counts:
        fail(f"object-member review cardinality drift: {dict(counts)}")
    expected_adaptation_counts = Counter({
        "MATERIAL_RECIPE_DELTA_EVIDENCE_SEMANTIC_REVIEW_REQUIRED": 20,
        "CONFIGURATION_OR_PACKAGING_DELTA_EVIDENCE_SEMANTIC_REVIEW_REQUIRED": 8,
        "NO_EXPLICIT_DELTA_TOKEN_OBSERVED_SEMANTIC_REVIEW_OPEN": 9,
    }) if args.expected_identities == EXPECTED_IDENTITIES else adaptation_counts
    if adaptation_counts != expected_adaptation_counts:
        fail(f"adaptation review cardinality drift: {dict(adaptation_counts)}")

    args.out.mkdir(parents=True)
    review_path = args.out / "generic-recipe-binding-and-drift-target-receipt-review.tsv"
    review_fields = list(output[0])
    write_tsv(review_path, review_fields, output)

    metadata_path = args.out / "generic-recipe-binding-and-drift-target-receipt-metadata.tsv"
    metadata = [
        ("source_receipt_archive", args.source_receipt_archive),
        ("source_receipt_sha256", args.source_receipt_sha256),
        ("source_repository_head", source["head"]),
        ("source_repository_tree", source["tree"]),
        ("review_rules_sha256", sha256(args.rules)),
        ("binding_receipt_sha256", sha256(args.binding_receipt)),
        ("drift_receipt_sha256", sha256(args.drift_receipt)),
        ("artifact_verification_sha256", sha256(args.artifact_verification)),
        ("artifact_registry_sha256", sha256(args.artifact_registry)),
        ("recipe_file_inventory_sha256", sha256(args.recipe_inventory)),
        ("source_repository_state_sha256", sha256(args.source_state)),
        ("collector_summary_sha256", sha256(args.summary)),
        ("review_receipt_sha256", sha256(review_path)),
        ("review_identity_rows", len(output)),
        ("selected_artifacts_referenced", len(selected_artifact_ids)),
        ("verified_cached_artifacts", len(artifact_verification)),
        ("unique_recipe_roots", len(expected_roots)),
        ("recipe_file_inventory_rows", len(recipe_inventory)),
        ("exact_member_expected_soname_candidate_confirmed", counts["EXACT_MEMBER_EXPECTED_SONAME_CANDIDATE_CONFIRMED"]),
        ("drift_target_elf_expected_soname_candidate_confirmed", counts["DRIFT_TARGET_ELF_EXPECTED_SONAME_CANDIDATE_CONFIRMED"]),
        ("expected_soname_alias_absent_correct_candidate_required", counts["EXPECTED_SONAME_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED"]),
        ("material_recipe_delta_review_required", adaptation_counts["MATERIAL_RECIPE_DELTA_EVIDENCE_SEMANTIC_REVIEW_REQUIRED"]),
        ("configuration_or_packaging_delta_review_required", adaptation_counts["CONFIGURATION_OR_PACKAGING_DELTA_EVIDENCE_SEMANTIC_REVIEW_REQUIRED"]),
        ("no_explicit_delta_token_semantic_review_open", adaptation_counts["NO_EXPLICIT_DELTA_TOKEN_OBSERVED_SEMANTIC_REVIEW_OPEN"]),
        ("artifact_build_attestations_accepted", 0),
        ("termux_android_adaptations_accepted", 0),
        ("concrete_filename_drifts_accepted", 0),
        ("final_provider_decisions_accepted", 0),
        ("target_rows_populated", 0),
        ("next_state", args.next_state),
    ]
    write_tsv(metadata_path, ["field", "value"], ({"field": key, "value": value} for key, value in metadata))
    (args.out / "claim-boundary.txt").write_text(
        "Pinned recipe lineage is candidate evidence, not artifact build attestation.\n"
        "Recipe adaptation tokens identify semantic review work; they do not accept an adaptation.\n"
        "Exact or drift-target SONAME evidence remains candidate object/member evidence only.\n"
        "Concrete filename drift is not accepted by SONAME equality alone.\n"
        "No final provider authority, target population, package transaction, extraction or runtime execution is accepted.\n",
        encoding="utf-8",
    )
    (args.out / "next-state.txt").write_text(args.next_state + "\n", encoding="utf-8")
    (args.out / "review.status").write_text("PASS\n", encoding="utf-8")
    print("generic recipe binding and drift target ELF receipt review: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
