#!/usr/bin/env python3
"""Define the bounded generic build-attestation and adaptation review set.

This is a repository-side planning step. It converts the reviewed 37-row
recipe/object receipt into deterministic root and object work units plus an
explicit evidence-requirement codebook. It accepts no provenance, adaptation,
filename-drift policy, provider authority, or target population.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, NoReturn

EXPECTED_OBJECTS = 37
EXPECTED_ROOTS = 28
EXPECTED_EXACT = 21
EXPECTED_DRIFT = 15
EXPECTED_UNSATISFIED = 1
NEXT_STATE = "COLLECT_BOUNDED_GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE"

REQUIREMENTS = [
    ("BA-001", "BUILD_ATTESTATION", "ROOT", "Bind the exact artifact SHA-256 to one recorded build invocation and the pinned recipe/source tree.", "Signed provenance, retained builder record, or equivalent immutable attestation naming artifact digest, source tree, recipe tree and invocation.", "Family/version alignment or repository co-location without digest-bound build provenance."),
    ("BA-002", "BUILD_ATTESTATION", "ROOT", "Record the build environment, toolchain, dependency inputs and relevant environment variables.", "Immutable environment/toolchain/dependency manifest sufficient to identify the producing build context.", "Unbounded current environment, undocumented host state, or package metadata alone."),
    ("BA-003", "BUILD_ATTESTATION", "ROOT", "Bind package outputs and named runtime members to the attested build result.", "Output manifest linking package digest and named member digests/paths to the build result.", "Receipt-only member observation with no producing-build link."),
    ("BA-004", "BUILD_ATTESTATION", "ROOT", "Provide an independent verification path for the artifact-to-recipe claim.", "Independent byte reproduction, reproducible-build comparison, or independently verifiable signed provenance.", "Single-party assertion without independent verification."),
    ("BA-005", "BUILD_ATTESTATION", "ROOT", "Define failure, update and rollback handling for attestation continuity.", "Policy showing how successor and rollback artifacts retain or re-establish the same provenance chain.", "One-off proof that cannot govern update or rollback."),
    ("AD-001", "ADAPTATION", "ROOT", "Enumerate every recipe delta and packaging hook in the pinned recipe root.", "Complete file-by-file delta inventory covering patches, custom steps, hooks, subpackages and configuration arguments.", "Token presence alone or partial recipe excerpts."),
    ("AD-002", "ADAPTATION", "ROOT", "Compare the pinned recipe behavior against the identified upstream baseline.", "Semantic comparison explaining what each delta changes relative to upstream.", "Filename/token matching without semantic interpretation."),
    ("AD-003", "ADAPTATION", "ROOT", "Classify each delta as Android/Termux-required, packaging-only, maintenance-only, optional, or unrelated.", "Reasoned classification with evidence tied to platform constraints or package behavior.", "Assuming every Termux recipe change is runtime-required adaptation."),
    ("AD-004", "ADAPTATION", "OBJECT", "Bind each accepted delta to the affected named runtime object or explicitly show no object impact.", "Object/member-level impact analysis linked to the 37 reviewed identities.", "Package-wide inference from a recipe-level change."),
    ("AD-005", "ADAPTATION", "ROOT", "Define update and rollback implications of accepted adaptations.", "Compatibility and continuity requirements for successor and rollback recipe/artifact states.", "Current-version-only reasoning."),
    ("AD-006", "ADAPTATION", "ROOT", "For roots with no explicit bounded token, perform a full semantic review rather than infer upstream equivalence.", "Complete recipe/upstream comparison showing whether any implicit or unclassified adaptation exists.", "Treating absence of collector tokens as proof of no adaptation."),
    ("CF-001", "CONCRETE_FILENAME_DRIFT", "OBJECT", "Show consumers bind to the expected SONAME or stable alias rather than the historical concrete filename.", "Consumer/reference evidence or loader-policy evidence demonstrating stable SONAME/alias binding.", "SONAME equality of the provider object alone."),
    ("CF-002", "CONCRETE_FILENAME_DRIFT", "OBJECT", "Validate the package symlink chain and concrete target across the exact current artifact.", "Exact alias-to-target chain, target digest and target SONAME bound to the reviewed artifact.", "Unversioned family inference."),
    ("CF-003", "CONCRETE_FILENAME_DRIFT", "OBJECT", "Define how successor versions may change the concrete target while preserving the accepted runtime identity.", "Explicit version-drift acceptance rule with validation gates.", "Copying the first-generation concrete filename as a permanent oracle."),
    ("CF-004", "CONCRETE_FILENAME_DRIFT", "OBJECT", "Define rollback behavior when concrete targets differ between versions.", "Rollback rule preserving alias/SONAME identity and exact artifact/member verification.", "Current-version-only acceptance."),
    ("OJ-001", "OBJECT_REQUIREMENT", "OBJECT", "Correct the required object identity or locate a candidate providing the required expected SONAME.", "Authoritative workload/reference evidence correcting the requirement, or an exact artifact/member candidate with the required SONAME.", "Substituting a different ABI family such as libjpeg.so.8 for libjpeg.so.62."),
]

FIELDS_REQUIRED = {
    "evidence_row_id", "capability_partition", "identity_label", "artifact_id",
    "artifact_package", "artifact_version", "artifact_sha256", "recipe_root",
    "recipe_tree", "recipe_resolved_full_version", "adaptation_evidence_tokens",
    "adaptation_semantic_review_state", "object_member_review_state",
    "concrete_filename_policy_state", "provider_review_eligibility_state",
    "final_provider_state", "target_population_state", "next_action",
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"generic build attestation and adaptation review set: FAIL: {message}")


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        fail(f"missing input: {path}")
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if not reader.fieldnames:
            fail(f"missing header: {path}")
        rows = [{key: (value or "") for key, value in row.items()} for row in reader]
    return rows


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


def stable_id(prefix: str, value: str) -> str:
    return f"{prefix}:{hashlib.sha256(value.encode('utf-8')).hexdigest()[:20]}"


def requirement_set(*groups: Iterable[str]) -> str:
    values = sorted({item for group in groups for item in group})
    return ";".join(values) if values else "NONE"


def classify(row: dict[str, str]) -> tuple[str, list[str], list[str], list[str], str, str]:
    adaptation = row["adaptation_semantic_review_state"]
    obj = row["object_member_review_state"]
    build = ["BA-001", "BA-002", "BA-003", "BA-004", "BA-005"]

    if adaptation == "MATERIAL_RECIPE_DELTA_EVIDENCE_SEMANTIC_REVIEW_REQUIRED":
        adapt = ["AD-001", "AD-002", "AD-003", "AD-004", "AD-005"]
        adaptation_class = "MATERIAL_RECIPE_DELTA"
    elif adaptation == "CONFIGURATION_OR_PACKAGING_DELTA_EVIDENCE_SEMANTIC_REVIEW_REQUIRED":
        adapt = ["AD-001", "AD-002", "AD-003", "AD-004"]
        adaptation_class = "CONFIGURATION_OR_PACKAGING_DELTA"
    elif adaptation == "NO_EXPLICIT_DELTA_TOKEN_OBSERVED_SEMANTIC_REVIEW_OPEN":
        adapt = ["AD-002", "AD-003", "AD-004", "AD-006"]
        adaptation_class = "NO_EXPLICIT_DELTA_TOKEN"
    else:
        fail(f"unexpected adaptation state: {adaptation}")

    if obj == "EXPECTED_SONAME_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED":
        tier = "T0_OBJECT_REQUIREMENT_CORRECTION"
        drift = []
        correction = ["OJ-001"]
        eligibility = "BLOCKED_OBJECT_REQUIREMENT_UNSATISFIED"
        next_action = "CORRECT_OBJECT_REQUIREMENT_OR_LOCATE_MATCHING_EXPECTED_SONAME_CANDIDATE"
    else:
        correction = []
        eligibility = "EVIDENCE_COLLECTION_ELIGIBLE_AUTHORITY_BLOCKED"
        if obj == "DRIFT_TARGET_ELF_EXPECTED_SONAME_CANDIDATE_CONFIRMED":
            drift = ["CF-001", "CF-002", "CF-003", "CF-004"]
            if adaptation_class == "MATERIAL_RECIPE_DELTA":
                tier = "T1_MATERIAL_DELTA_AND_DRIFT"
            elif adaptation_class == "CONFIGURATION_OR_PACKAGING_DELTA":
                tier = "T3_CONFIGURATION_OR_PACKAGING_AND_DRIFT"
            else:
                tier = "T5_NO_TOKEN_AND_DRIFT"
            next_action = "COLLECT_BUILD_ATTESTATION_ADAPTATION_AND_DRIFT_POLICY_EVIDENCE"
        elif obj == "EXACT_MEMBER_EXPECTED_SONAME_CANDIDATE_CONFIRMED":
            drift = []
            if adaptation_class == "MATERIAL_RECIPE_DELTA":
                tier = "T2_MATERIAL_DELTA_EXACT"
            elif adaptation_class == "CONFIGURATION_OR_PACKAGING_DELTA":
                tier = "T4_CONFIGURATION_OR_PACKAGING_EXACT"
            else:
                tier = "T6_NO_TOKEN_EXACT"
            next_action = "COLLECT_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE"
        else:
            fail(f"unexpected object/member state: {obj}")
    return tier, build, adapt, drift, requirement_set(correction), eligibility + ":" + next_action


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt-review", required=True, type=Path)
    parser.add_argument("--source-metadata", required=True, type=Path)
    parser.add_argument("--requirements-out", required=True, type=Path)
    parser.add_argument("--roots-out", required=True, type=Path)
    parser.add_argument("--objects-out", required=True, type=Path)
    parser.add_argument("--metadata-out", required=True, type=Path)
    parser.add_argument("--next-state", default=NEXT_STATE)
    args = parser.parse_args()

    outputs = [args.requirements_out, args.roots_out, args.objects_out, args.metadata_out]
    if any(path.exists() or path.is_symlink() for path in outputs):
        fail("refusing existing output")

    rows = read_tsv(args.receipt_review)
    if len(rows) != EXPECTED_OBJECTS:
        fail(f"object denominator {len(rows)} != {EXPECTED_OBJECTS}")
    if not FIELDS_REQUIRED.issubset(rows[0]):
        fail(f"receipt schema missing fields: {sorted(FIELDS_REQUIRED - set(rows[0]))}")
    if len({row["evidence_row_id"] for row in rows}) != EXPECTED_OBJECTS:
        fail("duplicate evidence row ID")
    if any(not re.fullmatch(r"[0-9a-f]{64}", row["artifact_sha256"]) for row in rows):
        fail("invalid artifact SHA-256")
    if any(not re.fullmatch(r"[0-9a-f]{40}", row["recipe_tree"]) for row in rows):
        fail("invalid recipe tree")
    if any(row["final_provider_state"] != "UNRESOLVED" or row["target_population_state"] != "BLOCKED" for row in rows):
        fail("authority or target population state drifted")

    source_metadata = read_tsv(args.source_metadata)
    if not source_metadata or set(source_metadata[0]) != {"field", "value"}:
        fail("invalid source metadata schema")
    source_map = {row["field"]: row["value"] for row in source_metadata}
    if source_map.get("review_identity_rows") != str(EXPECTED_OBJECTS):
        fail("source metadata denominator mismatch")
    if source_map.get("artifact_build_attestations_accepted") != "0" or source_map.get("termux_android_adaptations_accepted") != "0":
        fail("source metadata authority stop state drifted")

    requirement_rows = [
        {
            "requirement_id": rid,
            "dimension": dimension,
            "scope": scope,
            "requirement": requirement,
            "acceptable_evidence": acceptable,
            "blocking_or_insufficient_evidence": blocking,
            "authority_effect": "REVIEW_INPUT_ONLY_NO_AUTOMATIC_ACCEPTANCE",
        }
        for rid, dimension, scope, requirement, acceptable, blocking in REQUIREMENTS
    ]
    write_tsv(
        args.requirements_out,
        ["requirement_id", "dimension", "scope", "requirement", "acceptable_evidence", "blocking_or_insufficient_evidence", "authority_effect"],
        requirement_rows,
    )

    object_rows: list[dict[str, object]] = []
    by_root: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in sorted(rows, key=lambda item: item["evidence_row_id"]):
        tier, build, adapt, drift, correction, eligibility_and_action = classify(row)
        eligibility, next_action = eligibility_and_action.split(":", 1)
        object_row = {
            "object_review_id": stable_id("generic-object-review", row["evidence_row_id"]),
            "evidence_row_id": row["evidence_row_id"],
            "review_tier": tier,
            "capability_partition": row["capability_partition"],
            "identity_label": row["identity_label"],
            "artifact_id": row["artifact_id"],
            "artifact_package": row["artifact_package"],
            "artifact_version": row["artifact_version"],
            "artifact_sha256": row["artifact_sha256"],
            "recipe_root": row["recipe_root"],
            "recipe_tree": row["recipe_tree"],
            "recipe_resolved_full_version": row["recipe_resolved_full_version"],
            "adaptation_evidence_tokens": row["adaptation_evidence_tokens"],
            "object_member_review_state": row["object_member_review_state"],
            "build_attestation_requirement_set": requirement_set(build),
            "adaptation_requirement_set": requirement_set(adapt),
            "concrete_filename_requirement_set": requirement_set(drift),
            "object_correction_requirement_set": correction,
            "review_eligibility_state": eligibility,
            "authority_state": "OPEN_NO_ACCEPTANCE",
            "target_population_state": "UNPOPULATED",
            "next_action": next_action,
        }
        object_rows.append(object_row)
        by_root[row["recipe_root"]].append(object_row)

    if len(by_root) != EXPECTED_ROOTS:
        fail(f"root denominator {len(by_root)} != {EXPECTED_ROOTS}")

    root_rows: list[dict[str, object]] = []
    for root, members in sorted(by_root.items()):
        trees = {str(member["recipe_tree"]) for member in members}
        versions = {str(member["recipe_resolved_full_version"]) for member in members}
        if len(trees) != 1 or len(versions) != 1:
            fail(f"inconsistent recipe identity within root: {root}")
        tier = min((str(member["review_tier"]) for member in members), key=lambda value: int(value[1]))
        artifact_ids = sorted({str(member["artifact_id"]) for member in members})
        packages = sorted({str(member["artifact_package"]) for member in members})
        root_rows.append({
            "root_review_id": stable_id("generic-root-review", root),
            "review_tier": tier,
            "recipe_root": root,
            "recipe_tree": next(iter(trees)),
            "recipe_resolved_full_version": next(iter(versions)),
            "artifact_ids": ";".join(artifact_ids),
            "artifact_packages": ";".join(packages),
            "artifact_count": len(artifact_ids),
            "identity_count": len(members),
            "adaptation_evidence_tokens": ";".join(sorted({token for member in members for token in str(member["adaptation_evidence_tokens"]).split(";") if token and token != "NONE_DECLARED"})) or "NONE_DECLARED",
            "build_attestation_requirement_set": requirement_set(*(str(member["build_attestation_requirement_set"]).split(";") for member in members)),
            "adaptation_requirement_set": requirement_set(*(str(member["adaptation_requirement_set"]).split(";") for member in members)),
            "concrete_filename_requirement_set": requirement_set(*(str(member["concrete_filename_requirement_set"]).split(";") for member in members if member["concrete_filename_requirement_set"] != "NONE")),
            "object_correction_requirement_set": requirement_set(*(str(member["object_correction_requirement_set"]).split(";") for member in members if member["object_correction_requirement_set"] != "NONE")),
            "eligible_object_count": sum(member["review_eligibility_state"] == "EVIDENCE_COLLECTION_ELIGIBLE_AUTHORITY_BLOCKED" for member in members),
            "blocked_object_count": sum(member["review_eligibility_state"] != "EVIDENCE_COLLECTION_ELIGIBLE_AUTHORITY_BLOCKED" for member in members),
            "review_state": "REQUIREMENTS_DEFINED_EVIDENCE_NOT_COLLECTED",
            "authority_state": "OPEN_NO_ACCEPTANCE",
            "next_action": "COLLECT_ROOT_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE",
        })

    object_fields = [
        "object_review_id", "evidence_row_id", "review_tier", "capability_partition", "identity_label",
        "artifact_id", "artifact_package", "artifact_version", "artifact_sha256", "recipe_root", "recipe_tree",
        "recipe_resolved_full_version", "adaptation_evidence_tokens", "object_member_review_state",
        "build_attestation_requirement_set", "adaptation_requirement_set", "concrete_filename_requirement_set",
        "object_correction_requirement_set", "review_eligibility_state", "authority_state",
        "target_population_state", "next_action",
    ]
    root_fields = [
        "root_review_id", "review_tier", "recipe_root", "recipe_tree", "recipe_resolved_full_version",
        "artifact_ids", "artifact_packages", "artifact_count", "identity_count", "adaptation_evidence_tokens",
        "build_attestation_requirement_set", "adaptation_requirement_set", "concrete_filename_requirement_set",
        "object_correction_requirement_set", "eligible_object_count", "blocked_object_count", "review_state",
        "authority_state", "next_action",
    ]
    write_tsv(args.objects_out, object_fields, object_rows)
    write_tsv(args.roots_out, root_fields, root_rows)

    object_tiers = Counter(str(row["review_tier"]) for row in object_rows)
    root_tiers = Counter(str(row["review_tier"]) for row in root_rows)
    object_states = Counter(str(row["object_member_review_state"]) for row in object_rows)
    metadata = [
        ("source_receipt_review_sha256", sha256(args.receipt_review)),
        ("source_receipt_metadata_sha256", sha256(args.source_metadata)),
        ("requirements_sha256", sha256(args.requirements_out)),
        ("root_review_set_sha256", sha256(args.roots_out)),
        ("object_review_set_sha256", sha256(args.objects_out)),
        ("requirement_rows", str(len(requirement_rows))),
        ("root_review_rows", str(len(root_rows))),
        ("object_review_rows", str(len(object_rows))),
        ("exact_member_rows", str(object_states["EXACT_MEMBER_EXPECTED_SONAME_CANDIDATE_CONFIRMED"])),
        ("drift_target_rows", str(object_states["DRIFT_TARGET_ELF_EXPECTED_SONAME_CANDIDATE_CONFIRMED"])),
        ("unsatisfied_object_rows", str(object_states["EXPECTED_SONAME_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED"])),
    ]
    metadata.extend((f"object_tier_{tier}", str(count)) for tier, count in sorted(object_tiers.items()))
    metadata.extend((f"root_tier_{tier}", str(count)) for tier, count in sorted(root_tiers.items()))
    metadata.extend([
        ("artifact_build_attestations_accepted", "0"),
        ("termux_android_adaptations_accepted", "0"),
        ("concrete_filename_drifts_accepted", "0"),
        ("final_provider_decisions_accepted", "0"),
        ("target_rows_populated", "0"),
        ("next_state", args.next_state),
    ])
    write_tsv(args.metadata_out, ["field", "value"], ({"field": key, "value": value} for key, value in metadata))

    if len(object_rows) != EXPECTED_OBJECTS or len(root_rows) != EXPECTED_ROOTS:
        fail("output denominator mismatch")
    if object_states != Counter({
        "EXACT_MEMBER_EXPECTED_SONAME_CANDIDATE_CONFIRMED": EXPECTED_EXACT,
        "DRIFT_TARGET_ELF_EXPECTED_SONAME_CANDIDATE_CONFIRMED": EXPECTED_DRIFT,
        "EXPECTED_SONAME_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED": EXPECTED_UNSATISFIED,
    }):
        fail(f"object evidence classification mismatch: {object_states}")
    print("generic build attestation and adaptation review set: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
