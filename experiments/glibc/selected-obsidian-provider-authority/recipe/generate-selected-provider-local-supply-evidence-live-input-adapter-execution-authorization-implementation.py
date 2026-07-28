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
SOURCE_NAME = "selected_provider_local_supply_evidence_live_input_adapter_execution_authorization_candidate.py"
FIXTURE_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-synthetic-fixture.json"
NEGATIVE_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-negative-cases.json"
COVERAGE_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-coverage.tsv"
SUCCESS_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-synthetic-success.json"
METADATA_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-metadata.tsv"

SOURCE_DIGESTS = {
    "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-boundary-acceptance.tsv": "2b5646bc1987b7ec01fac5c0a44cf5247b2e0850463db21956cbcac3b0547dac",
    "selected-provider-local-supply-evidence-live-input-adapter-contract.json": "2e80bcb77b97b5ecc52304a9ef3693b123cb13dc74a7bc9c94dc1be557e82213",
    "selected-provider-local-supply-evidence-execution-authorization-schema.json": "91cd60dbc10fd0d0d1e644011b1d5f4f06e903744e81982dc088264836757a20",
    "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-validation-contract.tsv": "408c213c941f8670129bf2e07da02ea06886895ee5c39e748d748b54e0993503",
    "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-state-machine.tsv": "6dcbc03906f755e836c7dd83f679b0202c6b219afcfa0afe5f254da88ed64d7b",
    "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-operation-contract.tsv": "912786adf77ef9beeaec22f3208b742a79ae3edcb33730e1267148be86266a66",
    "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-failure-contract.tsv": "a031e35872a8d2e0ad71e888a0040574bf6560b7b256ac5d7680cfb36c013e76",
    "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-receipt-contract.json": "0acb6152d3afa1397841c453d8b2cc6a72f3cbbd05bead51ee02596aafadf55b",
    "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-metadata.tsv": "ea0cfbed6e0d14a694cd1e0000acbbeecee156dd5e1923d551151c834506aa2e",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("live_input_adapter_execution_authorization_candidate", path)
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
        raise SystemExit(f"synthetic success failed: {success}")
    if len(coverage) != 164:
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
        "schema_version": "1",
        "implementation_review_id": module.IMPLEMENTATION_REVIEW_ID,
        "candidate_state": "QUALIFIED_NON_EXECUTING_SYNTHETIC_LIVE_INPUT_ADAPTER_EXECUTION_AUTHORIZATION_IMPLEMENTATION_CANDIDATE",
        "implementation_acceptance_gate": module.IMPLEMENTATION_ACCEPTANCE_GATE,
        "contract_acceptance_id": module.CONTRACT_ACCEPTANCE_ID,
        "contract_acceptance_sha256": SOURCE_DIGESTS["selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-boundary-acceptance.tsv"],
        "implementation_source_sha256": sha(destination_source),
        "synthetic_fixture_sha256": sha(fixture_path),
        "synthetic_negative_cases_sha256": sha(negative_path),
        "implementation_coverage_sha256": sha(coverage_path),
        "synthetic_success_sha256": sha(success_path),
        "explicit_input_coverage_count": "10",
        "adapter_envelope_field_coverage_count": "20",
        "execution_authorization_claim_coverage_count": "27",
        "validation_coverage_count": "37",
        "state_coverage_count": "18",
        "operation_coverage_count": "32",
        "failure_coverage_count": "20",
        "total_coverage_count": "164",
        "synthetic_success_case_count": "1",
        "synthetic_negative_case_count": "20",
        "synthetic_coordinate_row_count": "41",
        "synthetic_coordinate_row_field_count": "10",
        "synthetic_provider_read_count": "0",
        "synthetic_write_count": "0",
        "current_live_input_count": "0",
        "current_adapter_envelope_count": "0",
        "current_execution_authorization_count": "0",
        "current_provider_read_count": "0",
        "current_write_count": "0",
        "current_live_authority_count": "0",
        "implementation_execution_mode": "SYNTHETIC_REPOSITORY_FIXTURE_ONLY",
        "synthetic_implementation_role": "IMMUTABLE_SEMANTIC_AND_REGRESSION_ORACLE_ONLY_NOT_LIVE_EXECUTOR",
        "accepted_synthetic_cli_invocation": "FORBIDDEN_NOT_PERFORMED",
        "live_to_synthetic_path_rewrite": "FORBIDDEN_NOT_PERFORMED",
        "execution_replay_consumption": "VALIDATED_IN_MEMORY_ONLY_NOT_PERSISTED",
        "evidence_delegation": "NOT_EXECUTED_SEPARATE_READ_ONLY_IMPLEMENTATION_ACCEPTANCE_REQUIRED",
        "owner_authorization_issuance_authorized": "NO",
        "coordinate_receipt_production_authorized": "NO",
        "execution_authorization_issuance_authorized": "NO",
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
        "update_boundary": "ANY_IMPLEMENTATION_SOURCE_FIXTURE_COVERAGE_SERIALIZATION_VALIDATION_REPLAY_DELEGATION_OUTPUT_OR_AUTHORITY_CHANGE_REQUIRES_NEW_IMPLEMENTATION_REVIEW",
        "rollback_boundary": "REMOVE_UNACCEPTED_IMPLEMENTATION_CANDIDATE_ONLY_NO_LIVE_INPUT_PROVIDER_READ_WRITE_OR_RUNTIME_STATE_EXISTS",
        "next_action": "review-and-accept-non-executing-selected-provider-local-supply-evidence-live-input-adapter-and-execution-authorization-implementation-candidate-boundary",
        "authority_effect": "SYNTHETIC_ONLY_IMPLEMENTATION_CANDIDATE_ZERO_LIVE_INPUTS_ZERO_PROVIDER_READS_ZERO_WRITES_ZERO_LIVE_AUTHORITY",
        "prohibited_inference": "IMPLEMENTATION_REVIEW_DOES_NOT_ACCEPT_LIVE_INPUTS_ISSUE_OR_ACTIVATE_AUTHORIZATION_REWRITE_LIVE_PATHS_INVOKE_THE_ACCEPTED_SYNTHETIC_CLI_SEARCH_OPEN_OR_READ_PROVIDER_BYTES_PERSIST_REPLAY_EXECUTE_EVIDENCE_COLLECTION_CREATE_RUNTIME_STATE_POPULATE_MATERIALIZE_PUBLISH_DEPLOY_OR_ACTIVATE",
    }
    write_metadata(output / REVIEW / METADATA_NAME, metadata)


if __name__ == "__main__":
    main()
