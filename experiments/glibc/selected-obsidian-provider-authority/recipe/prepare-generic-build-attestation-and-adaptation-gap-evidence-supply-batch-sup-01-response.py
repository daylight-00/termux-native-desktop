#!/usr/bin/env python3
"""Prepare the bounded SUP-01 authoritative correction response.

This transaction corrects the requirement identity from a Debian-oracle concrete
filename to the stable libjpeg v6b SONAME.  It rejects the Termux candidate's
libjpeg v8 ABI as a substitute and emits candidate evidence only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path
from typing import Iterable, NoReturn

EXPECTED_HASHES = {
    "source_contracts": "97cf1d4c06f32119e14cb026532e8a107c52ba7238c09cceab894701fb967f04",
    "requirements": "900dc80c0785185b83b2fd4a1cc9428a08e8cc1afd459eb6412871a1aaf6e025",
    "objects": "c8ed9478efb239f352a77564aec42226a7ec616715bc090d607e3e74c68b098e",
    "batches": "2d97ada3d107723a0da50878209e83b2bd9791e73e0d94cd03c40fe7e65ce8a4",
    "requests": "d26fb629a05c36f012f4fd18391d1f1e3caf9a636b0a07190eb8b9f9212ee2ae",
}
BATCH_ID = "SUP-01"
REQUEST_ID = "SRQ-OJ-001"
REQUIREMENT_ID = "OJ-001"
LANE_ID = "GC-01"
ACQUISITION_UNIT_ID = "generic-object-acquisition:c67c0d26282d621fc99a"
OBJECT_REVIEW_ID = "generic-object-review:fc085dca914b298d1356"
EVIDENCE_ROW_ID = "selected:a7e42baafca8ed4717e3"
CANDIDATE_ARTIFACT_ID = "generic-artifact:e672a721d7a949048cab"
CANDIDATE_ARTIFACT_SHA256 = "e672a721d7a949048cab5c7073ef0a0c05f627b8fc691ecc2d0adea6a5a5689e"
CANDIDATE_RECIPE_ROOT = "gpkg/libjpeg-turbo"
CANDIDATE_RECIPE_TREE = "cb58a7c1d7f4a1f89d036e4c80da596c0c61234c"
SOURCE_KIND = "AUTHORITATIVE_REFERENCE"
ACQUISITION_MODE = "OPERATOR_SUPPLIED_REFERENCE_OR_BOUNDED_REFERENCE_CAPTURE"
LOCATOR_CLASS = "IMMUTABLE_DOCUMENT_REVISION_OR_CONTENT_DIGEST"
CLAIM_BOUNDARY = "CANDIDATE_EVIDENCE_REVIEW_REQUIRED_NO_AUTHORITY_EFFECT"
AUTHORITY_STATE = "OPEN_NO_ACCEPTANCE"
TARGET_STATE = "UNPOPULATED"
NEXT_STATE = "REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_01_RESPONSE"
REFERENCE_LOCATOR = ";".join([
    "github:libjpeg-turbo/libjpeg-turbo@3.1.0:CMakeLists.txt#blob=9c4e5e2dadf57b8e421a562ff687f59aabb6a360",
    "github:libjpeg-turbo/libjpeg-turbo@3.1.0:sharedlib/CMakeLists.txt#blob=c8c92996f51ace4d61c0baac2d178ead618cab93",
    "github:termux-pacman/glibc-packages@9bdd20c1d36524a0ab016d9b71c748b0cbb20a34:gpkg/libjpeg-turbo/build.sh-diff",
    "debian:trixie:libjpeg62-turbo:arm64:1%3A2.1.5-4:files",
])
PAYLOAD_FIELDS = [
    "object_review_id", "evidence_row_id", "prior_oracle_concrete_identity",
    "required_identity", "rejected_substitute_identity", "reference_locator",
    "decision_basis", "candidate_artifact_id", "candidate_artifact_sha256",
    "candidate_recipe_root", "candidate_recipe_tree", "candidate_recipe_configuration",
    "candidate_observed_family", "correction_response_state", "provider_candidate_state",
    "authority_state", "target_population_state", "claim_boundary",
]
MANIFEST_FIELDS = [
    "input_id", "acquisition_unit_id", "requirement_id", "lane_id", "scope_kind",
    "scope_id", "source_kind", "acquisition_mode", "locator_class", "source_locator",
    "relative_path", "sha256", "size_bytes", "evidence_class", "claim_boundary",
]


def fail(message: str) -> NoReturn:
    raise SystemExit(f"SUP-01 response: FAIL: {message}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.is_file() or path.is_symlink():
        fail(f"missing regular input: {path}")
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if not reader.fieldnames:
            fail(f"missing header: {path}")
        return [{k: v or "" for k, v in row.items()} for row in reader]


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def one(rows: list[dict[str, str]], key: str, value: str, label: str) -> dict[str, str]:
    matches = [row for row in rows if row.get(key) == value]
    if len(matches) != 1:
        fail(f"expected one {label}: {value}")
    return matches[0]


def verify_hash(path: Path, expected: str, label: str) -> None:
    observed = sha256(path)
    if observed != expected:
        fail(f"{label} hash drift: {observed}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-contracts", required=True, type=Path)
    parser.add_argument("--requirements", required=True, type=Path)
    parser.add_argument("--objects", required=True, type=Path)
    parser.add_argument("--batches", required=True, type=Path)
    parser.add_argument("--requests", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    if args.out.exists() or args.out.is_symlink():
        fail(f"refusing existing output: {args.out}")
    for label, path in [
        ("source_contracts", args.source_contracts), ("requirements", args.requirements),
        ("objects", args.objects), ("batches", args.batches), ("requests", args.requests),
    ]:
        verify_hash(path, EXPECTED_HASHES[label], label)

    contracts = read_tsv(args.source_contracts)
    requirements = read_tsv(args.requirements)
    objects = read_tsv(args.objects)
    batches = read_tsv(args.batches)
    requests = read_tsv(args.requests)
    contract = one(contracts, "source_kind", SOURCE_KIND, "source contract")
    requirement = one(requirements, "requirement_id", REQUIREMENT_ID, "requirement")
    unit = one(objects, "acquisition_unit_id", ACQUISITION_UNIT_ID, "object acquisition unit")
    batch = one(batches, "batch_id", BATCH_ID, "supply batch")
    request = one(requests, "request_id", REQUEST_ID, "supply request")

    expected_contract = {
        "allowed_requirements": REQUIREMENT_ID,
        "allowed_scope_kinds": "OBJECT",
        "acquisition_mode": ACQUISITION_MODE,
        "required_locator_class": LOCATOR_CLASS,
        "prohibited_inference": "NO_ABI_FAMILY_SUBSTITUTION",
        "claim_boundary": CLAIM_BOUNDARY,
        "authority_state": AUTHORITY_STATE,
    }
    for field, expected in expected_contract.items():
        if contract.get(field) != expected:
            fail(f"source contract drift: {field}")
    if requirement.get("lane_id") != LANE_ID or requirement.get("primary_source_kind") != SOURCE_KIND:
        fail("OJ-001 requirement identity/source drift")
    if requirement.get("manifest_scope_kind") != "OBJECT" or requirement.get("deliverable_contract") != "object-requirement-correction-review.tsv":
        fail("OJ-001 scope/deliverable drift")
    if requirement.get("authority_state") != AUTHORITY_STATE or requirement.get("claim_boundary") != CLAIM_BOUNDARY:
        fail("OJ-001 authority/claim promotion")
    for field, expected in {
        "object_review_id": OBJECT_REVIEW_ID,
        "evidence_row_id": EVIDENCE_ROW_ID,
        "identity_label": "libjpeg.so.62.3.0",
        "artifact_id": CANDIDATE_ARTIFACT_ID,
        "artifact_sha256": CANDIDATE_ARTIFACT_SHA256,
        "recipe_root": CANDIDATE_RECIPE_ROOT,
        "manifest_scope_kind": "OBJECT",
        "manifest_scope_id": OBJECT_REVIEW_ID,
        "final_provider_state": "UNRESOLVED",
        "authority_state": AUTHORITY_STATE,
        "target_population_state": TARGET_STATE,
    }.items():
        if unit.get(field) != expected:
            fail(f"object acquisition drift: {field}")
    if REQUIREMENT_ID not in unit.get("requirement_ids", "").split(";"):
        fail("OJ-001 not assigned to object acquisition unit")
    if batch.get("requirement_ids") != REQUIREMENT_ID or batch.get("request_state") != "REQUEST_DEFINED_NOT_ISSUED":
        fail("SUP-01 batch drift")
    if request.get("batch_id") != BATCH_ID or request.get("requirement_id") != REQUIREMENT_ID:
        fail("SRQ-OJ-001 identity drift")
    if request.get("request_state") != "REQUEST_DEFINED_NOT_ISSUED" or request.get("responses_received") != "0":
        fail("request already issued/responded or state drift")
    if request.get("authority_state") != AUTHORITY_STATE:
        fail("request authority promotion")

    acquisition_input = args.out / "acquisition-input"
    acquisition_input.mkdir(parents=True)
    payload_path = acquisition_input / "object-requirement-correction-review.tsv"
    payload = {
        "object_review_id": OBJECT_REVIEW_ID,
        "evidence_row_id": EVIDENCE_ROW_ID,
        "prior_oracle_concrete_identity": "libjpeg.so.62.3.0",
        "required_identity": "libjpeg.so.62",
        "rejected_substitute_identity": "libjpeg.so.8",
        "reference_locator": REFERENCE_LOCATOR,
        "decision_basis": "UPSTREAM_DEFAULT_V6B_ABI_USES_SONAME_62;WITH_JPEG8_IS_BACKWARD_INCOMPATIBLE_AND_USES_SONAME_8;DEBIAN_62_3_0_IS_PROVIDER_VERSIONED_CONCRETE_FILENAME_NOT_PERMANENT_REQUIREMENT",
        "candidate_artifact_id": CANDIDATE_ARTIFACT_ID,
        "candidate_artifact_sha256": CANDIDATE_ARTIFACT_SHA256,
        "candidate_recipe_root": CANDIDATE_RECIPE_ROOT,
        "candidate_recipe_tree": CANDIDATE_RECIPE_TREE,
        "candidate_recipe_configuration": "-DWITH_JPEG8=ON",
        "candidate_observed_family": "libjpeg.so;libjpeg.so.8;libjpeg.so.8.3.2",
        "correction_response_state": "PROPOSED_REQUIRED_IDENTITY_CORRECTION_REVIEW_REQUIRED",
        "provider_candidate_state": "NO_MATCHING_SONAME_62_CANDIDATE_BOUND",
        "authority_state": AUTHORITY_STATE,
        "target_population_state": TARGET_STATE,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if payload["required_identity"] == payload["rejected_substitute_identity"]:
        fail("libjpeg.so.8 substitution attempted")
    write_tsv(payload_path, PAYLOAD_FIELDS, [payload])
    payload_sha = sha256(payload_path)
    payload_size = payload_path.stat().st_size
    manifest = {
        "input_id": "sup-01-oj-001-authoritative-correction",
        "acquisition_unit_id": ACQUISITION_UNIT_ID,
        "requirement_id": REQUIREMENT_ID,
        "lane_id": LANE_ID,
        "scope_kind": "OBJECT",
        "scope_id": OBJECT_REVIEW_ID,
        "source_kind": SOURCE_KIND,
        "acquisition_mode": ACQUISITION_MODE,
        "locator_class": LOCATOR_CLASS,
        "source_locator": REFERENCE_LOCATOR,
        "relative_path": payload_path.name,
        "sha256": payload_sha,
        "size_bytes": str(payload_size),
        "evidence_class": "AUTHORITATIVE_OBJECT_REQUIREMENT_CORRECTION_RESPONSE",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = acquisition_input / "acquisition-input-manifest.tsv"
    write_tsv(manifest_path, MANIFEST_FIELDS, [manifest])
    metadata_rows = [
        {"field": "supply_batch", "value": BATCH_ID},
        {"field": "supply_request", "value": REQUEST_ID},
        {"field": "requirement", "value": REQUIREMENT_ID},
        {"field": "response_payloads", "value": "1"},
        {"field": "proposed_required_identity", "value": "libjpeg.so.62"},
        {"field": "rejected_substitute_identity", "value": "libjpeg.so.8"},
        {"field": "matching_provider_candidates_bound", "value": "0"},
        {"field": "object_corrections_accepted", "value": "0"},
        {"field": "final_provider_decisions_accepted", "value": "0"},
        {"field": "target_rows_populated", "value": "0"},
        {"field": "payload_sha256", "value": payload_sha},
        {"field": "manifest_sha256", "value": sha256(manifest_path)},
        {"field": "response_state", "value": "SUPPLY_RESPONSE_PREPARED_REVIEW_REQUIRED"},
        {"field": "next_state", "value": NEXT_STATE},
    ]
    write_tsv(args.out / "response-metadata.tsv", ["field", "value"], metadata_rows)
    (args.out / "analysis.status").write_text("PASS\n", encoding="utf-8")
    (args.out / "claim-boundary.txt").write_text(
        "Candidate authoritative correction response only. No object correction, provider authority, target population, materialization or activation is accepted.\n",
        encoding="utf-8",
    )
    (args.out / "next-state.txt").write_text(NEXT_STATE + "\n", encoding="utf-8")
    print("SUP_01_RESPONSE=PASS_BOUNDED")
    print("PROPOSED_REQUIRED_IDENTITY=libjpeg.so.62")
    print("REJECTED_SUBSTITUTE_IDENTITY=libjpeg.so.8")
    print("MATCHING_PROVIDER_CANDIDATES_BOUND=0")
    print(f"NEXT_STATE={NEXT_STATE}")


if __name__ == "__main__":
    main()
