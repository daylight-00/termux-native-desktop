#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

BASE = Path("experiments/glibc/selected-obsidian-provider-authority")
REVIEW = BASE / "review"
IMPLEMENTATION = BASE / "implementation"
SOURCE = IMPLEMENTATION / "selected_provider_local_supply_live_authority_transaction_production_candidate.py"
PLAN = REVIEW / "selected-provider-local-supply-live-authority-transaction-production-implementation-isolated-fixture-plan.json"
NEGATIVE = REVIEW / "selected-provider-local-supply-live-authority-transaction-production-implementation-negative-cases.json"
COVERAGE = REVIEW / "selected-provider-local-supply-live-authority-transaction-production-implementation-coverage.tsv"
SUCCESS = REVIEW / "selected-provider-local-supply-live-authority-transaction-production-implementation-isolated-success.json"
METADATA = REVIEW / "selected-provider-local-supply-live-authority-transaction-production-implementation-metadata.tsv"


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    spec = importlib.util.spec_from_file_location("live_authority_production_generator", path)
    if spec is None or spec.loader is None:
        raise SystemExit("unable to load production implementation")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output-root", type=Path, default=Path("."))
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    output = args.output_root.resolve()
    source = repo / SOURCE
    module = load(source)
    module.verify_source_digests(repo)
    plan = module.build_isolated_fixture_plan(repo)
    negative = module.build_negative_cases()
    coverage = module.build_coverage_rows(repo)
    with tempfile.TemporaryDirectory(prefix="lsla-production-generate-", dir=repo.parent) as temp:
        manifest = module.materialize_isolated_fixture(plan, Path(temp) / "fixture", "success", repo)
        success = module.normalize_result(module.execute_manifest(manifest))
    if not success.get("pass") or len(coverage) != 128:
        raise SystemExit("production implementation generation failed")

    output_source = output / SOURCE
    output_source.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != output_source.resolve():
        shutil.copyfile(source, output_source)
    for relative, value in ((PLAN, plan), (NEGATIVE, negative), (SUCCESS, success)):
        path = output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(canonical(value))
    write_tsv(
        output / COVERAGE,
        [
            "coverage_kind", "source_id", "sequence", "implementation_symbol",
            "enforcement_layer", "isolated_case", "current_state", "authority_effect",
        ],
        coverage,
    )
    metadata = {
        "schema_version": "1",
        "production_implementation_review_id": module.PRODUCTION_IMPLEMENTATION_REVIEW_ID,
        "candidate_state": "QUALIFIED_NON_EXECUTING_PRODUCTION_CAPABLE_ISOLATED_FIXTURE_LIVE_AUTHORITY_TRANSACTION_IMPLEMENTATION_CANDIDATE",
        "production_implementation_acceptance_gate": module.PRODUCTION_IMPLEMENTATION_ACCEPTANCE_GATE,
        "synthetic_implementation_acceptance_id": module.SYNTHETIC_IMPLEMENTATION_ACCEPTANCE_ID,
        "implementation_source_sha256": sha(output_source),
        "isolated_fixture_plan_sha256": sha(output / PLAN),
        "negative_cases_sha256": sha(output / NEGATIVE),
        "implementation_coverage_sha256": sha(output / COVERAGE),
        "isolated_success_sha256": sha(output / SUCCESS),
        "input_coverage_count": "20",
        "state_coverage_count": "26",
        "operation_coverage_count": "52",
        "failure_coverage_count": "30",
        "total_coverage_count": "128",
        "inherited_semantic_coverage_count": "448",
        "isolated_success_case_count": "1",
        "isolated_negative_case_count": "30",
        "isolated_document_role_count": "5",
        "isolated_coordinate_row_count": "41",
        "isolated_coordinate_row_field_count": "10",
        "isolated_replay_tuple_field_count": "10",
        "isolated_document_open_count": "5",
        "isolated_document_read_count": "5",
        "isolated_replay_open_count": "1",
        "isolated_replay_read_count": "1",
        "isolated_replay_append_count": "2",
        "isolated_result_write_count": "2",
        "selected_provider_open_count": "0",
        "selected_provider_read_count": "0",
        "provider_byte_count": "0",
        "project_replay_write_count": "0",
        "current_live_document_count": "0",
        "current_execution_authorization_count": "0",
        "current_local_supply_map_count": "0",
        "current_live_authority_count": "0",
        "provider_open_gate_armed": "NO",
        "execution_mode": "ISOLATED_TEMP_AUTHORITY_DOCUMENTS_REPLAY_AND_PROVIDER_METADATA_ONLY_NO_SELECTED_PROVIDER_AUTHORITY",
        "accepted_orchestration_invocation": "FORBIDDEN_NOT_IMPORTED_NOT_INVOKED",
        "accepted_synthetic_oracle_invocation": "FORBIDDEN_NOT_IMPORTED_NOT_INVOKED",
        "owner_authorization_issuance_authorized": "NO",
        "coordinate_receipt_production_authorized": "NO",
        "execution_authorization_issuance_authorized": "NO",
        "project_replay_persistence_authorized": "NO",
        "selected_provider_open_authorized": "NO",
        "selected_provider_read_authorized": "NO",
        "provider_byte_read_authorized": "NO",
        "local_supply_map_produced": "NO",
        "generation_root_creation_authorized": "NO",
        "target_population_authorized": "NO",
        "materialization_authorized": "NO",
        "publication_authorized": "NO",
        "deployment_authorized": "NO",
        "activation_authorized": "NO",
        "update_boundary": "ANY_PRODUCTION_SOURCE_FIXTURE_DOCUMENT_REPLAY_RECEIPT_COVERAGE_SERIALIZATION_OR_AUTHORITY_CHANGE_REQUIRES_NEW_REVIEW",
        "rollback_boundary": "REMOVE_UNACCEPTED_PRODUCTION_CANDIDATE_ONLY_ISOLATED_TEMP_FIXTURES_ARE_EPHEMERAL_NO_PROJECT_REPLAY_OR_PROVIDER_STATE_EXISTS",
        "next_action": "review-and-accept-non-executing-selected-provider-local-supply-live-authority-transaction-production-implementation-candidate-boundary",
        "authority_effect": "PRODUCTION_CAPABLE_ISOLATED_FIXTURE_ONLY_128_ROW_TRANSACTION_IMPLEMENTATION_1_SUCCESS_30_FAIL_CLOSED_5_DOCUMENTS_41_COORDINATES_2_REPLAY_APPENDS_2_RESULT_WRITES_ZERO_SELECTED_PROVIDER_AND_LIVE_AUTHORITY",
        "prohibited_inference": "REVIEW_DOES_NOT_ACCEPT_OR_CONSUME_LIVE_DOCUMENTS_WRITE_PROJECT_REPLAY_STATE_ARM_PROVIDER_OPEN_GATE_OPEN_OR_READ_SELECTED_PROVIDER_PATHS_INVOKE_ORCHESTRATION_PRODUCE_A_LOCAL_MAP_CREATE_A_GENERATION_ROOT_POPULATE_MATERIALIZE_PUBLISH_DEPLOY_OR_ACTIVATE",
    }
    write_tsv(output / METADATA, ["key", "value"], [{"key": key, "value": value} for key, value in metadata.items()])


if __name__ == "__main__":
    main()
