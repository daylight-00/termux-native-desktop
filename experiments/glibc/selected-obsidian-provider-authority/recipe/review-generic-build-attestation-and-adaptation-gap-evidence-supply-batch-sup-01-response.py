#!/usr/bin/env python3
"""Review the bounded SUP-01 authoritative correction response."""
from __future__ import annotations
import argparse, csv, hashlib, re
from pathlib import Path
from typing import Iterable, NoReturn

EXPECTED_HEAD = "ae7fbcb17a1834936caadabbbd56dfd628f70fe4"
EXPECTED_TREE = "d127b8fbe1e29efe9d9d58619d2f58f887ca1835"
EXPECTED_BATCH = "SUP-01"
EXPECTED_REQUEST = "SRQ-OJ-001"
EXPECTED_REQUIREMENT = "OJ-001"
EXPECTED_LANE = "GC-01"
EXPECTED_UNIT = "generic-object-acquisition:c67c0d26282d621fc99a"
EXPECTED_OBJECT = "generic-object-review:fc085dca914b298d1356"
EXPECTED_EVIDENCE = "selected:a7e42baafca8ed4717e3"
EXPECTED_PAYLOAD_SHA = "91c5d65069c6447724e1c7119dc21ac8267708465f78c30588f77dda63a7067e"
EXPECTED_MANIFEST_SHA = "7d6aefbdbae1ac46a6620912fab54056f0a5ca9f994bf63304d1b8fbdeb1d7f1"
EXPECTED_REFS = {
    "github:libjpeg-turbo/libjpeg-turbo@3.1.0:CMakeLists.txt#blob=9c4e5e2dadf57b8e421a562ff687f59aabb6a360",
    "github:libjpeg-turbo/libjpeg-turbo@3.1.0:sharedlib/CMakeLists.txt#blob=c8c92996f51ace4d61c0baac2d178ead618cab93",
    "github:termux-pacman/glibc-packages@9bdd20c1d36524a0ab016d9b71c748b0cbb20a34:gpkg/libjpeg-turbo/build.sh-diff",
    "debian:trixie:libjpeg62-turbo:arm64:1%3A2.1.5-4:files",
}
EXPECTED_BASIS = {
    "UPSTREAM_DEFAULT_V6B_ABI_USES_SONAME_62",
    "WITH_JPEG8_IS_BACKWARD_INCOMPATIBLE_AND_USES_SONAME_8",
    "DEBIAN_62_3_0_IS_PROVIDER_VERSIONED_CONCRETE_FILENAME_NOT_PERMANENT_REQUIREMENT",
}
EXPECTED_FAMILY = {"libjpeg.so", "libjpeg.so.8", "libjpeg.so.8.3.2"}
SOURCE_CLAIM = "CANDIDATE_EVIDENCE_REVIEW_REQUIRED_NO_AUTHORITY_EFFECT"
REVIEW_CLAIM = "OBJECT_REQUIREMENT_CORRECTION_ACCEPTED_PROVIDER_AUTHORITY_OPEN_NO_TARGET_EFFECT"
NEXT = "FULFILL_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02"

def fail(msg: str) -> NoReturn:
    raise SystemExit(f"SUP-01 response review: FAIL: {msg}")

def read_tsv(path: Path, fields: list[str] | None = None) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file() or path.is_symlink():
        fail(f"missing regular input: {path}")
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        actual = reader.fieldnames or []
        if not actual:
            fail(f"missing header: {path}")
        if fields is not None and actual != fields:
            fail(f"header drift: {path}")
        return actual, [{k: (v or "") for k, v in row.items()} for row in reader]

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

def unique(rows: list[dict[str, str]], key: str, label: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row.get(key, "")
        if not value or value in result:
            fail(f"duplicate or empty {key} in {label}: {value!r}")
        result[value] = row
    return result

def kv_tsv(path: Path) -> dict[str, str]:
    _, rows = read_tsv(path, ["field", "value"])
    result: dict[str, str] = {}
    for row in rows:
        key = row["field"]
        if not key or key in result:
            fail(f"duplicate or empty metadata field: {key!r}")
        result[key] = row["value"]
    return result

def require(value: bool, message: str) -> None:
    if not value:
        fail(message)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-contracts", required=True, type=Path)
    parser.add_argument("--requirements", required=True, type=Path)
    parser.add_argument("--object-set", required=True, type=Path)
    parser.add_argument("--supply-batches", required=True, type=Path)
    parser.add_argument("--supply-requests", required=True, type=Path)
    parser.add_argument("--response-dir", required=True, type=Path)
    parser.add_argument("--rules", required=True, type=Path)
    parser.add_argument("--source-head", default=EXPECTED_HEAD)
    parser.add_argument("--source-tree", default=EXPECTED_TREE)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    require(re.fullmatch(r"[0-9a-f]{40}", args.source_head) is not None, "invalid source head")
    require(re.fullmatch(r"[0-9a-f]{40}", args.source_tree) is not None, "invalid source tree")
    require(args.source_head == EXPECTED_HEAD and args.source_tree == EXPECTED_TREE, "source Git identity drift")
    if args.out.exists() or args.out.is_symlink():
        fail(f"refusing existing output: {args.out}")

    _, contracts = read_tsv(args.source_contracts)
    _, requirements = read_tsv(args.requirements)
    _, objects = read_tsv(args.object_set)
    _, batches = read_tsv(args.supply_batches)
    _, requests = read_tsv(args.supply_requests)
    require([len(contracts), len(requirements), len(objects), len(batches), len(requests)] == [10, 16, 37, 6, 16], "canonical denominator drift")
    contract_i = unique(contracts, "source_kind", "source contracts")
    requirement_i = unique(requirements, "requirement_id", "requirements")
    object_i = unique(objects, "acquisition_unit_id", "objects")
    batch_i = unique(batches, "batch_id", "supply batches")
    request_i = unique(requests, "request_id", "supply requests")

    contract = contract_i.get("AUTHORITATIVE_REFERENCE") or fail("missing authoritative reference contract")
    require(contract["allowed_requirements"] == EXPECTED_REQUIREMENT, "authoritative contract requirement drift")
    require(contract["allowed_scope_kinds"] == "OBJECT", "authoritative contract scope drift")
    require(contract["acquisition_mode"] == "OPERATOR_SUPPLIED_REFERENCE_OR_BOUNDED_REFERENCE_CAPTURE", "authoritative acquisition mode drift")
    require(contract["required_locator_class"] == "IMMUTABLE_DOCUMENT_REVISION_OR_CONTENT_DIGEST", "authoritative locator class drift")
    require(contract["prohibited_inference"] == "NO_ABI_FAMILY_SUBSTITUTION", "authoritative prohibited inference drift")
    require(contract["claim_boundary"] == SOURCE_CLAIM and contract["authority_state"] == "OPEN_NO_ACCEPTANCE", "authoritative contract authority drift")

    requirement = requirement_i.get(EXPECTED_REQUIREMENT) or fail("missing OJ-001 requirement")
    require(requirement["lane_id"] == EXPECTED_LANE and requirement["manifest_scope_kind"] == "OBJECT", "OJ-001 lane/scope drift")
    require(requirement["primary_source_kind"] == "AUTHORITATIVE_REFERENCE", "OJ-001 source-kind drift")
    require(requirement["deliverable_contract"] == "object-requirement-correction-review.tsv", "OJ-001 deliverable drift")
    require(requirement["completion_gate"] == "REQUIRED_IDENTITY_CORRECTED_OR_EXACT_REQUIRED_SONAME_CANDIDATE_BOUND", "OJ-001 completion gate drift")

    batch = batch_i.get(EXPECTED_BATCH) or fail("missing SUP-01")
    require(batch["requirement_ids"] == EXPECTED_REQUIREMENT and batch["source_kinds"] == "AUTHORITATIVE_REFERENCE", "SUP-01 requirement/source drift")
    require(batch["stop_condition"] == "NO_LIBJPEG_SO_8_SUBSTITUTION_AND_NO_ABI_FAMILY_INFERENCE", "SUP-01 stop-condition drift")
    request = request_i.get(EXPECTED_REQUEST) or fail("missing SRQ-OJ-001")
    require(request["batch_id"] == EXPECTED_BATCH and request["requirement_id"] == EXPECTED_REQUIREMENT, "request identity drift")
    require(request["completion_gate"] == requirement["completion_gate"], "request completion gate drift")
    require(request["response_package_relative_path"] == "evidence-supply/responses/SUP-01/SRQ-OJ-001/", "request response path drift")

    obj = object_i.get(EXPECTED_UNIT) or fail("missing OJ-001 acquisition unit")
    require(obj["object_review_id"] == EXPECTED_OBJECT and obj["evidence_row_id"] == EXPECTED_EVIDENCE, "OJ-001 object binding drift")
    require(EXPECTED_REQUIREMENT in split_set(obj["requirement_ids"]), "OJ-001 not assigned to object unit")
    require("AUTHORITATIVE_REFERENCE" in split_set(obj["source_kinds"]), "authoritative source not assigned to object unit")
    require(obj["final_provider_state"] == "UNRESOLVED" and obj["target_population_state"] == "UNPOPULATED" and obj["authority_state"] == "OPEN_NO_ACCEPTANCE", "canonical object authority drift")

    response = args.response_dir
    manifest_path = response / "acquisition-input" / "acquisition-input-manifest.tsv"
    payload_path = response / "acquisition-input" / "object-requirement-correction-review.tsv"
    metadata_path = response / "response-metadata.tsv"
    require((response / "analysis.status").read_text(encoding="utf-8") == "PASS\n", "response analysis status drift")
    require((response / "next-state.txt").read_text(encoding="utf-8").strip() == "REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_01_RESPONSE", "response next-state drift")
    require((response / "claim-boundary.txt").read_text(encoding="utf-8").strip() == "Candidate authoritative correction response only. No object correction, provider authority, target population, materialization or activation is accepted.", "response claim-boundary drift")

    metadata = kv_tsv(metadata_path)
    expected_meta = {
        "supply_batch": EXPECTED_BATCH,
        "supply_request": EXPECTED_REQUEST,
        "requirement": EXPECTED_REQUIREMENT,
        "response_payloads": "1",
        "proposed_required_identity": "libjpeg.so.62",
        "rejected_substitute_identity": "libjpeg.so.8",
        "matching_provider_candidates_bound": "0",
        "object_corrections_accepted": "0",
        "final_provider_decisions_accepted": "0",
        "target_rows_populated": "0",
        "payload_sha256": EXPECTED_PAYLOAD_SHA,
        "manifest_sha256": EXPECTED_MANIFEST_SHA,
        "response_state": "SUPPLY_RESPONSE_PREPARED_REVIEW_REQUIRED",
        "next_state": "REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_01_RESPONSE",
    }
    require(metadata == expected_meta, f"response metadata drift: {metadata}")
    require(sha256(payload_path) == EXPECTED_PAYLOAD_SHA and sha256(manifest_path) == EXPECTED_MANIFEST_SHA, "tracked response digest drift")

    manifest_fields = ["input_id", "acquisition_unit_id", "requirement_id", "lane_id", "scope_kind", "scope_id", "source_kind", "acquisition_mode", "locator_class", "source_locator", "relative_path", "sha256", "size_bytes", "evidence_class", "claim_boundary"]
    _, manifest_rows = read_tsv(manifest_path, manifest_fields)
    require(len(manifest_rows) == 1, "expected one response manifest row")
    manifest = manifest_rows[0]
    require(manifest["input_id"] == "sup-01-oj-001-authoritative-correction", "response input id drift")
    require(manifest["acquisition_unit_id"] == EXPECTED_UNIT and manifest["scope_id"] == EXPECTED_OBJECT, "response scope binding drift")
    require(manifest["requirement_id"] == EXPECTED_REQUIREMENT and manifest["lane_id"] == EXPECTED_LANE and manifest["scope_kind"] == "OBJECT", "response requirement/lane/scope drift")
    require(manifest["source_kind"] == "AUTHORITATIVE_REFERENCE", "response source-kind drift")
    require(manifest["acquisition_mode"] == contract["acquisition_mode"] and manifest["locator_class"] == contract["required_locator_class"], "response source contract drift")
    require(manifest["relative_path"] == "object-requirement-correction-review.tsv", "response relative path drift")
    require(manifest["sha256"] == EXPECTED_PAYLOAD_SHA and int(manifest["size_bytes"]) == payload_path.stat().st_size, "response manifest integrity drift")
    require(manifest["evidence_class"] == "AUTHORITATIVE_OBJECT_REQUIREMENT_CORRECTION_RESPONSE" and manifest["claim_boundary"] == SOURCE_CLAIM, "response evidence class/claim drift")
    require(split_set(manifest["source_locator"]) == EXPECTED_REFS, "response source locator drift")

    payload_fields = ["object_review_id", "evidence_row_id", "prior_oracle_concrete_identity", "required_identity", "rejected_substitute_identity", "reference_locator", "decision_basis", "candidate_artifact_id", "candidate_artifact_sha256", "candidate_recipe_root", "candidate_recipe_tree", "candidate_recipe_configuration", "candidate_observed_family", "correction_response_state", "provider_candidate_state", "authority_state", "target_population_state", "claim_boundary"]
    _, payload_rows = read_tsv(payload_path, payload_fields)
    require(len(payload_rows) == 1, "expected one correction payload row")
    row = payload_rows[0]
    require(row["object_review_id"] == EXPECTED_OBJECT and row["evidence_row_id"] == EXPECTED_EVIDENCE, "payload object identity drift")
    require(row["prior_oracle_concrete_identity"] == "libjpeg.so.62.3.0", "prior oracle concrete identity drift")
    require(row["required_identity"] == "libjpeg.so.62", "required stable SONAME drift")
    require(row["rejected_substitute_identity"] == "libjpeg.so.8", "rejected substitute drift")
    require(split_set(row["reference_locator"]) == EXPECTED_REFS and split_set(row["decision_basis"]) == EXPECTED_BASIS, "authoritative reference or decision basis drift")
    require(row["candidate_artifact_id"] == "generic-artifact:e672a721d7a949048cab" and row["candidate_artifact_sha256"] == "e672a721d7a949048cab5c7073ef0a0c05f627b8fc691ecc2d0adea6a5a5689e", "candidate artifact drift")
    require(row["candidate_recipe_root"] == "gpkg/libjpeg-turbo" and row["candidate_recipe_tree"] == "cb58a7c1d7f4a1f89d036e4c80da596c0c61234c", "candidate recipe lineage drift")
    require(row["candidate_recipe_configuration"] == "-DWITH_JPEG8=ON", "candidate recipe configuration drift")
    family = split_set(row["candidate_observed_family"])
    require(family == EXPECTED_FAMILY and "libjpeg.so.62" not in family, "candidate observed family drift")
    require(row["correction_response_state"] == "PROPOSED_REQUIRED_IDENTITY_CORRECTION_REVIEW_REQUIRED", "correction response state drift")
    require(row["provider_candidate_state"] == "NO_MATCHING_SONAME_62_CANDIDATE_BOUND", "provider candidate state drift")
    require(row["authority_state"] == "OPEN_NO_ACCEPTANCE" and row["target_population_state"] == "UNPOPULATED" and row["claim_boundary"] == SOURCE_CLAIM, "response authority/target drift")

    args.out.mkdir(parents=True)
    review_path = args.out / "generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-response-review.tsv"
    object_path = args.out / "generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-object-review.tsv"
    metadata_out = args.out / "generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-response-review-metadata.tsv"
    review_row = {
        "review_id": "sup-01-response-review:oj-001",
        "batch_id": EXPECTED_BATCH,
        "request_id": EXPECTED_REQUEST,
        "requirement_id": EXPECTED_REQUIREMENT,
        "response_payload_count": "1",
        "authoritative_reference_state": "PINNED_IMMUTABLE_REFERENCES_VERIFIED",
        "prior_oracle_concrete_identity": "libjpeg.so.62.3.0",
        "accepted_required_identity": "libjpeg.so.62",
        "rejected_substitute_identity": "libjpeg.so.8",
        "selected_candidate_state": "WITH_JPEG8_SONAME_8_FAMILY_REJECTED",
        "correction_decision": "ACCEPT_REQUIRED_IDENTITY_AS_STABLE_SONAME_LIBJPEG_SO_62",
        "provider_candidate_state": "NO_MATCHING_SONAME_62_CANDIDATE_BOUND",
        "requirement_closure_state": "OJ_001_CLOSED_BY_REQUIRED_IDENTITY_CORRECTION",
        "final_provider_state": "UNRESOLVED",
        "authority_state": "OPEN_NO_PROVIDER_AUTHORITY_ACCEPTANCE",
        "target_population_state": "UNPOPULATED",
        "claim_boundary": REVIEW_CLAIM,
        "next_action": "FULFILL_SUP_02_PRODUCING_BUILD_PROVENANCE_AND_OUTPUT_LINKAGE",
    }
    write_tsv(review_path, list(review_row), [review_row])
    object_row = {
        "acquisition_unit_id": EXPECTED_UNIT,
        "object_review_id": EXPECTED_OBJECT,
        "evidence_row_id": EXPECTED_EVIDENCE,
        "prior_required_identity": "libjpeg.so.62.3.0",
        "accepted_required_identity": "libjpeg.so.62",
        "rejected_substitute_identity": "libjpeg.so.8",
        "candidate_artifact_id": row["candidate_artifact_id"],
        "candidate_recipe_configuration": row["candidate_recipe_configuration"],
        "candidate_observed_family": row["candidate_observed_family"],
        "object_requirement_correction_state": "ACCEPTED_STABLE_SONAME_REQUIREMENT",
        "matching_provider_candidate_state": "ABSENT_SUPPLY_STILL_REQUIRED",
        "remaining_requirement_ids": ";".join(sorted(split_set(obj["requirement_ids"]) - {EXPECTED_REQUIREMENT})) or "NONE",
        "final_provider_state": "UNRESOLVED",
        "authority_state": "OPEN_NO_PROVIDER_AUTHORITY_ACCEPTANCE",
        "target_population_state": "UNPOPULATED",
        "next_action": "KEEP_OBJECT_OPEN_AND_ADVANCE_TO_SUP_02",
    }
    write_tsv(object_path, list(object_row), [object_row])
    meta_rows = [
        ("source_head", args.source_head),
        ("source_tree", args.source_tree),
        ("source_contract_rows", 10),
        ("requirement_rows", 16),
        ("object_rows", 37),
        ("supply_batch_rows", 6),
        ("supply_request_rows", 16),
        ("response_payloads_reviewed", 1),
        ("authoritative_reference_sets_verified", 1),
        ("object_requirement_corrections_accepted", 1),
        ("requirements_closed_by_correction", 1),
        ("remaining_open_requirements", 15),
        ("matching_soname_62_provider_candidates_bound", 0),
        ("artifact_build_attestations_accepted", 0),
        ("termux_android_adaptations_accepted", 0),
        ("concrete_filename_drifts_accepted", 0),
        ("final_provider_decisions_accepted", 0),
        ("target_rows_populated", 0),
        ("response_payload_sha256", EXPECTED_PAYLOAD_SHA),
        ("response_manifest_sha256", EXPECTED_MANIFEST_SHA),
        ("rules_sha256", sha256(args.rules)),
        ("response_review_sha256", sha256(review_path)),
        ("object_review_sha256", sha256(object_path)),
        ("next_batch", "SUP-02"),
        ("next_state", NEXT),
    ]
    write_tsv(metadata_out, ["field", "value"], ({"field": k, "value": v} for k, v in meta_rows))
    (args.out / "analysis.status").write_text("PASS\n", encoding="utf-8")
    (args.out / "claim-boundary.txt").write_text(
        "The OJ-001 requirement model is corrected from provider-versioned concrete filename libjpeg.so.62.3.0 to stable SONAME libjpeg.so.62. libjpeg.so.8 remains a rejected incompatible ABI family. No matching provider candidate, final provider authority, target population, materialization or activation is accepted.\n",
        encoding="utf-8",
    )
    (args.out / "next-state.txt").write_text(NEXT + "\n", encoding="utf-8")
    print("generic build attestation/adaptation SUP-01 response review: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
