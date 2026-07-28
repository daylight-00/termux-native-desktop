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
SOURCE_NAME = "selected_provider_local_supply_map_evidence_transaction_candidate.py"
FIXTURE_NAME = "selected-provider-local-supply-map-evidence-transaction-implementation-synthetic-fixture.json"
NEGATIVE_NAME = "selected-provider-local-supply-map-evidence-transaction-implementation-negative-cases.json"
COVERAGE_NAME = "selected-provider-local-supply-map-evidence-transaction-implementation-coverage.tsv"
SUCCESS_NAME = "selected-provider-local-supply-map-evidence-transaction-implementation-synthetic-success.json"
METADATA_NAME = "selected-provider-local-supply-map-evidence-transaction-implementation-metadata.tsv"
SOURCE_DIGESTS = {'selected-provider-local-supply-map-evidence-transaction-design-boundary-acceptance.tsv': '1f60ec5983807d3f0f7527b11db953bf446eed39e1e526df21ad2f6a2812f8dd', 'selected-provider-local-supply-map-evidence-transaction-input-contract.tsv': 'fbb7b3e45ad45a7bffdf8fe8b6f483233c2fe048d809f2685796ba9e60a15089', 'selected-provider-local-supply-map-evidence-transaction-state-machine.tsv': '0d6005e4b188d98f1e44b4159db0db9f75314a047de7a2b95a0e680a19ed0f40', 'selected-provider-local-supply-map-evidence-transaction-operation-contract.tsv': '4269a87f864c22ce4bc920d4ac892483211245c64cf20e50b537e2c39e32b664', 'selected-provider-local-supply-map-evidence-transaction-failure-contract.tsv': 'eb49b325251af50524e17ae5136661418c922cb2107c94d83b9c3a1f736b7adb', 'selected-provider-local-supply-map-evidence-transaction-receipt-contract.json': '1fb99dbbc3581af9b77a52d34e2c6d25a51b245952491d4cf034b67e5ffd7dcd', 'selected-provider-local-supply-map-evidence-transaction-design-metadata.tsv': 'f461ea9622f02348323996a2042756d2f0252de35e997914503546526dcd1116', 'selected-provider-local-supply-map-contract.tsv': '2223af964e74cc8bb221d13e559e49aaf03abe364985346cb1d8e43973c6640e', 'selected-provider-local-supply-map-validation-contract.tsv': '0df8d9c7ddc28098ee220ee634a139b04aaa3d241bd36b2a4eb57ef8fbc41198', 'selected-provider-local-supply-map-contract-boundary-acceptance.tsv': '5401f46120d147394932d0004a2a37c761fc6471acaeabd730b90f1e5d859cd1'}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("local_supply_map_evidence_transaction_candidate", path)
    if spec is None or spec.loader is None:
        raise SystemExit("unable to load implementation candidate")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["coverage_kind", "source_id", "sequence", "implementation_symbol", "enforcement_layer", "synthetic_case", "current_state", "authority_effect"]
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
    if len(coverage) != 78:
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
        "candidate_state": "QUALIFIED_NON_EXECUTING_SYNTHETIC_READ_ONLY_LOCAL_SUPPLY_MAP_EVIDENCE_TRANSACTION_IMPLEMENTATION_CANDIDATE",
        "implementation_acceptance_gate": module.IMPLEMENTATION_ACCEPTANCE_GATE,
        "design_acceptance_id": module.DESIGN_ACCEPTANCE_ID,
        "design_acceptance_sha256": SOURCE_DIGESTS["selected-provider-local-supply-map-evidence-transaction-design-boundary-acceptance.tsv"],
        "implementation_source_sha256": sha(destination_source),
        "synthetic_fixture_sha256": sha(fixture_path),
        "synthetic_negative_cases_sha256": sha(negative_path),
        "implementation_coverage_sha256": sha(coverage_path),
        "synthetic_success_sha256": sha(success_path),
        "input_coverage_count": "12",
        "state_coverage_count": "16",
        "operation_coverage_count": "32",
        "failure_coverage_count": "18",
        "total_coverage_count": "78",
        "inherited_validation_rule_count": "24",
        "synthetic_success_case_count": "1",
        "synthetic_negative_case_count": "18",
        "synthetic_coordinate_row_count": "41",
        "synthetic_coordinate_row_field_count": "10",
        "synthetic_provider_open_count": "0",
        "synthetic_provider_read_count": "0",
        "synthetic_write_count": "0",
        "current_authorized_coordinate_count": "0",
        "current_provider_read_count": "0",
        "current_write_count": "0",
        "current_live_authority_count": "0",
        "local_supply_map_produced": "NO",
        "implementation_execution_mode": "SYNTHETIC_REPOSITORY_FIXTURE_ONLY_TEXT_MODEL_NO_PROVIDER_OPEN_OR_READ",
        "provider_read_operations": "MODELED_ONLY_NOT_EXECUTED",
        "evidence_transaction_execution_authorized": "NO",
        "local_path_discovery_authorized": "NO",
        "provider_byte_read_authorized": "NO",
        "owner_authorization_issuance_authorized": "NO",
        "coordinate_receipt_production_authorized": "NO",
        "execution_authorization_issuance_authorized": "NO",
        "replay_persistence_performed": "NO",
        "generation_root_creation_authorized": "NO",
        "target_population_authorized": "NO",
        "materialization_authorized": "NO",
        "publication_authorized": "NO",
        "deployment_authorized": "NO",
        "activation_authorized": "NO",
        "update_boundary": "ANY_IMPLEMENTATION_SOURCE_FIXTURE_COVERAGE_SERIALIZATION_PROVIDER_READ_MODEL_OUTPUT_OR_AUTHORITY_CHANGE_REQUIRES_NEW_IMPLEMENTATION_REVIEW",
        "rollback_boundary": "REMOVE_UNACCEPTED_IMPLEMENTATION_CANDIDATE_ONLY_NO_PROVIDER_PATH_READ_WRITE_OR_RUNTIME_STATE_EXISTS",
        "next_action": "review-and-accept-non-executing-selected-provider-local-supply-map-evidence-transaction-implementation-candidate-boundary",
        "authority_effect": "SYNTHETIC_ONLY_EVIDENCE_TRANSACTION_IMPLEMENTATION_CANDIDATE_78_COVERAGE_1_SUCCESS_18_FAIL_CLOSED_41_SYNTHETIC_ROWS_ZERO_PROVIDER_OPENS_READS_WRITES_LIVE_AUTHORITY",
        "prohibited_inference": "IMPLEMENTATION_REVIEW_DOES_NOT_AUTHORIZE_LIVE_INPUTS_DISCOVERY_PROVIDER_OPEN_OR_READ_RECEIPT_PRODUCTION_LOCAL_MAP_ACCEPTANCE_REPLAY_PERSISTENCE_GENERATION_ROOT_POPULATION_MATERIALIZATION_PUBLICATION_DEPLOYMENT_OR_ACTIVATION",
    }
    write_metadata(output / REVIEW / METADATA_NAME, metadata)


if __name__ == "__main__":
    main()
