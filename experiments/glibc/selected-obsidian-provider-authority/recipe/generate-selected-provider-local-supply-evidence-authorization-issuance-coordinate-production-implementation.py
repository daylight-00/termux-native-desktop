#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path

BASE = Path("experiments/glibc/selected-obsidian-provider-authority")
REVIEW = BASE / "review"
IMPLEMENTATION = BASE / "implementation"
SOURCE_NAME = "selected_provider_local_supply_evidence_authorization_issuance_coordinate_production_candidate.py"
FIXTURE_NAME = "selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-synthetic-fixture.json"
NEGATIVE_NAME = "selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-negative-cases.json"
COVERAGE_NAME = "selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-coverage.tsv"
SUCCESS_NAME = "selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-synthetic-success.json"
METADATA_NAME = "selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-metadata.tsv"

SOURCE_DIGESTS = {
    "selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-boundary-acceptance.tsv": "bf8d2377effb02db5e89c1b388b92f1ab5c9a908df51dc310d0d7eafba270d05",
    "selected-provider-local-supply-evidence-owner-authorization-token-schema.json": "27d11e8bb8de3238b49aef77757f0328a2269a156f55fdcbdddcf4dcb4fd411b",
    "selected-provider-local-supply-evidence-coordinate-receipt-schema.json": "b94c25994ecc26e402607b9e61c0cee796c74b15435bc168a18821def9096f83",
    "selected-provider-local-supply-evidence-authorization-coordinate-validation-contract.tsv": "64a6c168e30c7a559387c27d6baa7d3bd49953d7ea304d1bd98e4043cbb57f56",
    "selected-provider-local-supply-map-contract.tsv": "2223af964e74cc8bb221d13e559e49aaf03abe364985346cb1d8e43973c6640e",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("issuance_coordinate_implementation_candidate", path)
    if spec is None or spec.loader is None:
        raise SystemExit("unable to load implementation candidate")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "coverage_kind",
        "source_id",
        "sequence",
        "implementation_symbol",
        "enforcement_layer",
        "synthetic_case",
        "current_state",
        "authority_effect",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(path: Path, values: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["key", "value"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for key, value in values.items():
            writer.writerow({"key": key, "value": value})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output-root", type=Path, default=Path("."))
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    output = args.output_root.resolve()
    review = repo / REVIEW
    for name, digest in SOURCE_DIGESTS.items():
        if sha(review / name) != digest:
            raise SystemExit(f"source digest mismatch: {name}")
    source = repo / IMPLEMENTATION / SOURCE_NAME
    module = load_module(source)
    fixture = module.build_synthetic_fixture(repo)
    negatives = module.build_negative_cases()
    coverage = module.build_coverage_rows(repo)
    success = module.execute_synthetic_case(repo, fixture, "success")
    if not success.get("pass"):
        raise SystemExit("synthetic success fixture did not pass")
    if len(coverage) != 88:
        raise SystemExit(f"coverage cardinality mismatch: {len(coverage)}")
    destination_source = output / IMPLEMENTATION / SOURCE_NAME
    destination_source.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != destination_source.resolve():
        shutil.copyfile(source, destination_source)
    fixture_path = output / REVIEW / FIXTURE_NAME
    negative_path = output / REVIEW / NEGATIVE_NAME
    coverage_path = output / REVIEW / COVERAGE_NAME
    success_path = output / REVIEW / SUCCESS_NAME
    fixture_path.parent.mkdir(parents=True, exist_ok=True)
    fixture_path.write_bytes(canonical(fixture))
    negative_path.write_bytes(canonical(negatives))
    write_tsv(coverage_path, coverage)
    success_path.write_bytes(canonical(success))
    metadata = {
        "implementation_review_id": module.IMPLEMENTATION_REVIEW_ID,
        "candidate_state": "QUALIFIED_NON_EXECUTING_SYNTHETIC_IMPLEMENTATION_CANDIDATE",
        "implementation_acceptance_gate": module.IMPLEMENTATION_ACCEPTANCE_GATE,
        "design_acceptance_id": module.DESIGN_ACCEPTANCE_ID,
        "design_acceptance_sha256": SOURCE_DIGESTS["selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-boundary-acceptance.tsv"],
        "implementation_source_sha256": sha(destination_source),
        "synthetic_fixture_sha256": sha(fixture_path),
        "synthetic_negative_cases_sha256": sha(negative_path),
        "implementation_coverage_sha256": sha(coverage_path),
        "synthetic_success_sha256": sha(success_path),
        "input_coverage_count": "14",
        "state_coverage_count": "18",
        "operation_coverage_count": "36",
        "failure_coverage_count": "20",
        "total_coverage_count": "88",
        "authorization_claim_count": "18",
        "coordinate_required_row_count": "41",
        "coordinate_required_row_field_count": "10",
        "validation_rule_count": "30",
        "synthetic_success_case_count": "1",
        "synthetic_negative_case_count": "20",
        "synthetic_coordinate_row_count": "41",
        "synthetic_provider_read_count": "0",
        "synthetic_write_count": "0",
        "current_issued_token_count": "0",
        "current_coordinate_receipt_count": "0",
        "current_coordinate_row_count": "0",
        "current_provider_read_count": "0",
        "current_live_authority_count": "0",
        "implementation_execution_mode": "SYNTHETIC_REPOSITORY_FIXTURE_ONLY",
        "owner_authorization_issuance_authorized": "NO",
        "coordinate_receipt_production_authorized": "NO",
        "local_path_discovery_authorized": "NO",
        "provider_byte_read_authorized": "NO",
        "evidence_transaction_execution_authorized": "NO",
        "local_supply_map_produced": "NO",
        "generation_root_creation_authorized": "NO",
        "target_population_authorized": "NO",
        "materialization_authorized": "NO",
        "publication_authorized": "NO",
        "deployment_authorized": "NO",
        "activation_authorized": "NO",
        "update_boundary": "ANY_IMPLEMENTATION_SOURCE_FIXTURE_COVERAGE_SERIALIZATION_VALIDATION_FAILURE_MAPPING_OUTPUT_SCOPE_OR_AUTHORITY_CHANGE_REQUIRES_NEW_IMPLEMENTATION_REVIEW",
        "rollback_boundary": "REMOVE_UNACCEPTED_IMPLEMENTATION_CANDIDATE_ONLY_NO_LIVE_AUTHORITY_EXISTS",
        "next_action": "review-and-accept-non-executing-selected-provider-local-supply-evidence-authorization-issuance-and-coordinate-receipt-production-transaction-implementation-candidate-boundary",
        "authority_effect": "SYNTHETIC_ONLY_IMPLEMENTATION_CANDIDATE_ZERO_LIVE_TOKENS_ZERO_COORDINATES_ZERO_PROVIDER_READS_ZERO_RUNTIME_EFFECT",
        "prohibited_inference": "IMPLEMENTATION_REVIEW_DOES_NOT_ISSUE_OR_ACTIVATE_TOKEN_PRODUCE_OR_ACCEPT_LIVE_COORDINATES_SEARCH_OPEN_OR_READ_PROVIDER_BYTES_EXECUTE_EVIDENCE_COLLECTION_CREATE_RUNTIME_STATE_POPULATE_MATERIALIZE_PUBLISH_DEPLOY_OR_ACTIVATE",
    }
    write_metadata(output / REVIEW / METADATA_NAME, metadata)


if __name__ == "__main__":
    main()
