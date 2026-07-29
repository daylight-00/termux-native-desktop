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
SOURCE_NAME = "selected_provider_local_supply_live_evidence_orchestration_production_candidate.py"
PLAN_NAME = "selected-provider-local-supply-live-evidence-orchestration-production-implementation-isolated-fixture-plan.json"
NEGATIVE_NAME = "selected-provider-local-supply-live-evidence-orchestration-production-implementation-negative-cases.json"
COVERAGE_NAME = "selected-provider-local-supply-live-evidence-orchestration-production-implementation-coverage.tsv"
SUCCESS_NAME = "selected-provider-local-supply-live-evidence-orchestration-production-implementation-isolated-fixture-success.json"
METADATA_NAME = "selected-provider-local-supply-live-evidence-orchestration-production-implementation-metadata.tsv"
SOURCE_DIGESTS = {
    "selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-boundary-acceptance.tsv": "5b3628f2612e0e3ee51001cb80b3c43a76262fd182b500e31b32abb6f7b8bb69",
    "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-boundary-acceptance.tsv": "b108bd0955883e67bc4baab37b22af8c405fabba7b109d1830a8812404e83758",
    "selected-provider-local-supply-map-evidence-transaction-implementation-boundary-acceptance.tsv": "cc8974480536c3a656b1bc1eff7f7c7250c53cf24fe3b160a61aedc948fb8df6",
    "selected-provider-local-supply-evidence-owner-authorization-token-schema.json": "27d11e8bb8de3238b49aef77757f0328a2269a156f55fdcbdddcf4dcb4fd411b",
    "selected-provider-local-supply-evidence-coordinate-receipt-schema.json": "b94c25994ecc26e402607b9e61c0cee796c74b15435bc168a18821def9096f83",
    "selected-provider-local-supply-evidence-live-input-adapter-contract.json": "2e80bcb77b97b5ecc52304a9ef3693b123cb13dc74a7bc9c94dc1be557e82213",
    "selected-provider-local-supply-evidence-execution-authorization-schema.json": "91cd60dbc10fd0d0d1e644011b1d5f4f06e903744e81982dc088264836757a20",
    "selected-provider-local-supply-map-contract.tsv": "2223af964e74cc8bb221d13e559e49aaf03abe364985346cb1d8e43973c6640e",
    "selected-provider-local-supply-map-validation-contract.tsv": "0df8d9c7ddc28098ee220ee634a139b04aaa3d241bd36b2a4eb57ef8fbc41198",
    "selected-provider-local-supply-map-evidence-transaction-receipt-contract.json": "1fb99dbbc3581af9b77a52d34e2c6d25a51b245952491d4cf034b67e5ffd7dcd",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("live_evidence_orchestration_candidate", path)
    if spec is None or spec.loader is None:
        raise SystemExit("unable to load production orchestration candidate")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = ["coverage_kind", "source_id", "sequence", "implementation_symbol", "enforcement_layer", "isolated_case", "selected_provider_effect", "authority_effect"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


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
    repo = args.repo_root.resolve(); output = args.output_root.resolve()
    review = repo / REVIEW
    for name, digest in SOURCE_DIGESTS.items():
        if sha(review / name) != digest:
            raise SystemExit(f"accepted source digest mismatch: {name}")
    source = repo / IMPLEMENTATION / SOURCE_NAME
    module = load_module(source)
    plan = module.build_isolated_fixture_plan(repo)
    coverage = module.build_coverage_rows()
    negatives = module.build_negative_cases()
    if len(coverage) != 118:
        raise SystemExit(f"coverage cardinality mismatch: {len(coverage)}")
    if negatives.get("case_count") != 28:
        raise SystemExit("negative case cardinality mismatch")
    temp_parent = repo.parent
    with tempfile.TemporaryDirectory(prefix="leo-generator-", dir=temp_parent) as temp:
        manifest = module.materialize_isolated_fixture(plan, Path(temp) / "fixture", "success")
        success = module.normalize_result(module.execute_manifest(manifest))
        if not success.get("pass") or success.get("row_count") != 41:
            raise SystemExit(f"isolated fixture success failed: {success}")
    for case in negatives["cases"]:
        with tempfile.TemporaryDirectory(prefix="leo-negative-", dir=temp_parent) as temp:
            manifest = module.materialize_isolated_fixture(plan, Path(temp) / "fixture", case["case"])
            result = module.execute_manifest(manifest)
            if result.get("failure_id") != case["expected_failure_id"]:
                raise SystemExit(f"negative case mismatch: {case['case']}: {result}")
            if result.get("selected_provider_paths_opened") != 0 or result.get("selected_provider_files_read") != 0:
                raise SystemExit(f"selected provider effect in negative case: {case['case']}")
            if result.get("candidate_filesystem_write_count") != 0 or result.get("live_authority_count") != 0:
                raise SystemExit(f"authority widening in negative case: {case['case']}")

    destination_source = output / IMPLEMENTATION / SOURCE_NAME
    destination_source.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != destination_source.resolve():
        shutil.copyfile(source, destination_source)
    plan_path = output / REVIEW / PLAN_NAME
    negative_path = output / REVIEW / NEGATIVE_NAME
    coverage_path = output / REVIEW / COVERAGE_NAME
    success_path = output / REVIEW / SUCCESS_NAME
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_bytes(canonical(plan))
    negative_path.write_bytes(canonical(negatives))
    write_tsv(coverage_path, coverage)
    success_path.write_bytes(canonical(success))

    metadata = {
        "schema_version": "1",
        "implementation_review_id": module.REVIEW_ID,
        "candidate_state": module.CANDIDATE_STATE,
        "implementation_acceptance_gate": module.ACCEPTANCE_GATE,
        "implementation_source_sha256": sha(destination_source),
        "isolated_fixture_plan_sha256": sha(plan_path),
        "negative_cases_sha256": sha(negative_path),
        "implementation_coverage_sha256": sha(coverage_path),
        "isolated_fixture_success_sha256": sha(success_path),
        "explicit_input_coverage_count": "18",
        "state_coverage_count": "24",
        "operation_coverage_count": "48",
        "failure_coverage_count": "28",
        "total_coverage_count": "118",
        "inherited_issuance_implementation_coverage_count": "88",
        "inherited_adapter_implementation_coverage_count": "164",
        "inherited_evidence_implementation_coverage_count": "78",
        "inherited_total_semantic_coverage_count": "330",
        "isolated_success_case_count": "1",
        "isolated_negative_case_count": "28",
        "isolated_coordinate_row_count": "41",
        "isolated_coordinate_row_field_count": "10",
        "isolated_fixture_open_count": "41",
        "isolated_fixture_read_count": "41",
        "selected_provider_open_count": "0",
        "selected_provider_read_count": "0",
        "candidate_filesystem_write_count": "0",
        "persistent_replay_write_count": "0",
        "in_memory_replay_tuple_consumed": "1",
        "current_live_authority_count": "0",
        "local_supply_map_produced": "NO",
        "execution_mode": module.ISOLATED_MARKER,
        "production_surfaces": "EXPLICIT_CANONICAL_DOCUMENTS_DIGEST_REPOSITORY_REMOTE_EXECUTOR_TIME_REPLAY_FIRST_OPEN_COMPONENT_LSTAT_O_NOFOLLOW_FSTAT_STREAMING_SHA256_ELF64_AARCH64_DT_SONAME_WHOLE_MAP_PROTECTED_STATE",
        "selected_provider_path_policy": "DENY_ALL_CURRENT_CANDIDATE_EXECUTIONS",
        "accepted_synthetic_cli_invocation": "FORBIDDEN_NOT_IMPORTED_NOT_INVOKED",
        "live_to_synthetic_rewrite": "FORBIDDEN",
        "replay_persistence": "MEMORY_ONLY_TEST_INTERFACE_NO_PERSISTENT_WRITE",
        "live_execution_authorized": "NO",
        "owner_authorization_issuance_authorized": "NO",
        "coordinate_receipt_production_authorized": "NO",
        "execution_authorization_issuance_authorized": "NO",
        "provider_byte_read_authorized": "NO_SELECTED_PROVIDER_ISOLATED_FIXTURE_ONLY",
        "generation_root_creation_authorized": "NO",
        "target_population_authorized": "NO",
        "materialization_authorized": "NO",
        "publication_authorized": "NO",
        "deployment_authorized": "NO",
        "activation_authorized": "NO",
        "update_boundary": "ANY_SOURCE_FIXTURE_PLAN_COVERAGE_SERIALIZATION_FILESYSTEM_SURFACE_OUTPUT_SCOPE_OR_AUTHORITY_CHANGE_REQUIRES_NEW_PRODUCTION_IMPLEMENTATION_REVIEW",
        "rollback_boundary": "REMOVE_UNACCEPTED_CANDIDATE_ONLY_NO_SELECTED_PROVIDER_PATH_OPEN_READ_WRITE_OR_LIVE_AUTHORITY_EXISTS",
        "next_action": "review-and-accept-non-executing-selected-provider-local-supply-live-evidence-orchestration-production-implementation-candidate-boundary",
        "authority_effect": "PRODUCTION_CAPABLE_ORCHESTRATION_CANDIDATE_118_COVERAGE_1_SUCCESS_28_FAIL_CLOSED_41_ISOLATED_FILE_OPENS_READS_ZERO_SELECTED_PROVIDER_OPENS_READS_ZERO_FILESYSTEM_WRITES_ZERO_LIVE_AUTHORITY",
        "prohibited_inference": "CANDIDATE_REVIEW_DOES_NOT_AUTHORIZE_LIVE_DOCUMENTS_SELECTED_PROVIDER_PATHS_PROVIDER_BYTES_REPLAY_PERSISTENCE_LOCAL_MAP_PRODUCTION_GENERATION_ROOT_POPULATION_MATERIALIZATION_PUBLICATION_DEPLOYMENT_OR_ACTIVATION",
    }
    for name, digest in SOURCE_DIGESTS.items():
        metadata[f"accepted_source_sha256::{name}"] = digest
    write_metadata(output / REVIEW / METADATA_NAME, metadata)


if __name__ == "__main__":
    main()
