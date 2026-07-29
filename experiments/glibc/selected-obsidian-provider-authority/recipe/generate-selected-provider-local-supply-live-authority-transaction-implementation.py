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
SOURCE_NAME = "selected_provider_local_supply_live_authority_transaction_candidate.py"
FIXTURE_NAME = "selected-provider-local-supply-live-authority-transaction-implementation-synthetic-fixture.json"
NEGATIVE_NAME = "selected-provider-local-supply-live-authority-transaction-implementation-negative-cases.json"
COVERAGE_NAME = "selected-provider-local-supply-live-authority-transaction-implementation-coverage.tsv"
SUCCESS_NAME = "selected-provider-local-supply-live-authority-transaction-implementation-synthetic-success.json"
METADATA_NAME = "selected-provider-local-supply-live-authority-transaction-implementation-metadata.tsv"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("live_authority_transaction_candidate", path)
    if spec is None or spec.loader is None:
        raise SystemExit("unable to load implementation candidate")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = ["coverage_kind", "source_id", "sequence", "implementation_symbol", "enforcement_layer", "synthetic_case", "current_state", "authority_effect"]
    path.parent.mkdir(parents=True, exist_ok=True)
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
    source = repo / IMPLEMENTATION / SOURCE_NAME
    module = load_module(source)
    module.verify_source_digests(repo)
    fixture = module.build_synthetic_fixture(repo)
    negatives = module.build_negative_cases()
    coverage = module.build_coverage_rows(repo)
    success = module.execute_synthetic_case(repo, fixture, "success")
    if not success.get("pass") or len(coverage) != 128:
        raise SystemExit("synthetic implementation generation failed")

    out_source = output / IMPLEMENTATION / SOURCE_NAME
    out_source.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != out_source.resolve():
        shutil.copyfile(source, out_source)
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
        "candidate_state": "QUALIFIED_NON_EXECUTING_SYNTHETIC_LIVE_AUTHORITY_TRANSACTION_IMPLEMENTATION_CANDIDATE",
        "implementation_acceptance_gate": module.IMPLEMENTATION_ACCEPTANCE_GATE,
        "design_acceptance_id": module.DESIGN_ACCEPTANCE_ID,
        "design_acceptance_sha256": module.SOURCE_DIGESTS["selected-provider-local-supply-live-authority-transaction-design-boundary-acceptance.tsv"],
        "implementation_source_sha256": sha(out_source),
        "synthetic_fixture_sha256": sha(fixture_path),
        "synthetic_negative_cases_sha256": sha(negative_path),
        "implementation_coverage_sha256": sha(coverage_path),
        "synthetic_success_sha256": sha(success_path),
        "input_coverage_count": "20",
        "state_coverage_count": "26",
        "operation_coverage_count": "52",
        "failure_coverage_count": "30",
        "total_coverage_count": "128",
        "inherited_semantic_coverage_count": "448",
        "synthetic_success_case_count": "1",
        "synthetic_negative_case_count": "30",
        "synthetic_live_document_role_count": "5",
        "synthetic_coordinate_row_count": "41",
        "synthetic_coordinate_row_field_count": "10",
        "synthetic_replay_tuple_field_count": "10",
        "synthetic_live_document_count": "0",
        "synthetic_execution_authorization_count": "0",
        "synthetic_replay_write_count": "0",
        "synthetic_selected_provider_open_count": "0",
        "synthetic_selected_provider_read_count": "0",
        "synthetic_provider_byte_count": "0",
        "synthetic_local_supply_map_count": "0",
        "synthetic_live_authority_count": "0",
        "implementation_execution_mode": "SYNTHETIC_REPOSITORY_FIXTURE_ONLY_DOCUMENT_AND_STATE_MODEL_NO_LIVE_INPUTS_OR_EFFECTS",
        "accepted_orchestration_invocation": "FORBIDDEN_NOT_IMPORTED_NOT_INVOKED",
        "accepted_synthetic_oracle_invocation": "FORBIDDEN_NOT_IMPORTED_NOT_INVOKED",
        "owner_activation_authorized": "NO",
        "owner_authorization_issuance_authorized": "NO",
        "coordinate_receipt_production_authorized": "NO",
        "execution_authorization_issuance_authorized": "NO",
        "replay_registry_opened": "NO",
        "replay_persistence_performed": "NO",
        "provider_open_gate_armed": "NO",
        "local_path_discovery_authorized": "NO",
        "provider_byte_read_authorized": "NO",
        "local_supply_map_produced": "NO",
        "generation_root_creation_authorized": "NO",
        "target_population_authorized": "NO",
        "materialization_authorized": "NO",
        "publication_authorized": "NO",
        "deployment_authorized": "NO",
        "activation_authorized": "NO",
        "update_boundary": "ANY_IMPLEMENTATION_SOURCE_FIXTURE_COVERAGE_DOCUMENT_REPLAY_MODEL_SERIALIZATION_OR_AUTHORITY_CHANGE_REQUIRES_NEW_IMPLEMENTATION_REVIEW",
        "rollback_boundary": "REMOVE_UNACCEPTED_IMPLEMENTATION_CANDIDATE_ONLY_NO_LIVE_DOCUMENT_REPLAY_PROVIDER_OR_RUNTIME_STATE_EXISTS",
        "next_action": "review-and-accept-non-executing-selected-provider-local-supply-live-authority-transaction-implementation-candidate-boundary",
        "authority_effect": "SYNTHETIC_ONLY_128_ROW_LIVE_AUTHORITY_TRANSACTION_IMPLEMENTATION_CANDIDATE_1_SUCCESS_30_FAIL_CLOSED_5_DOCUMENT_ROLES_41_COORDINATE_ROWS_10_REPLAY_FIELDS_ZERO_CURRENT_AUTHORITY",
        "prohibited_inference": "IMPLEMENTATION_REVIEW_DOES_NOT_ACCEPT_OR_CONSUME_LIVE_DOCUMENTS_WRITE_REPLAY_STATE_ARM_PROVIDER_OPEN_GATE_OPEN_OR_READ_SELECTED_PROVIDER_PATHS_EXECUTE_ORCHESTRATION_PRODUCE_A_LOCAL_MAP_CREATE_A_GENERATION_ROOT_POPULATE_MATERIALIZE_PUBLISH_DEPLOY_OR_ACTIVATE",
    }
    write_metadata(output / REVIEW / METADATA_NAME, metadata)


if __name__ == "__main__":
    main()
