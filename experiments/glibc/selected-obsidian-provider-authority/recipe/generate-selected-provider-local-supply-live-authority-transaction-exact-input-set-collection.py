#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path("experiments/glibc/selected-obsidian-provider-authority")
REVIEW = BASE / "review"
IMPLEMENTATION = BASE / "implementation"
SOURCE = IMPLEMENTATION / "selected_provider_local_supply_live_authority_transaction_exact_input_set_collection_candidate.py"
PLAN = REVIEW / "selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-isolated-fixture-plan.json"
NEGATIVE = REVIEW / "selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-negative-cases.json"
COVERAGE = REVIEW / "selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-coverage.tsv"
SUCCESS = REVIEW / "selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-isolated-success.json"
METADATA = REVIEW / "selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-metadata.tsv"


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    spec = importlib.util.spec_from_file_location("exact_input_set_collection_generator", path)
    if spec is None or spec.loader is None:
        raise SystemExit("unable to load collection implementation")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output-root", type=Path, default=Path("."))
    args = parser.parse_args()
    repo = args.repo_root.resolve(); output = args.output_root.resolve()
    source = repo / SOURCE
    module = load(source)
    module.verify_source_digests(repo)
    plan = module.build_isolated_fixture_plan(repo)
    negative = module.build_negative_cases()
    coverage = module.build_coverage_rows(repo)
    with tempfile.TemporaryDirectory(prefix="lsla-collection-generate-", dir=repo.parent) as temp:
        manifest = module.materialize_isolated_fixture(plan, Path(temp) / "fixture", "success", repo)
        success = module.normalize_result(module.execute_manifest(manifest))
    if not success.get("pass") or len(coverage) != 20:
        raise SystemExit("exact input-set collection generation failed")

    output_source = output / SOURCE
    output_source.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != output_source.resolve(): shutil.copyfile(source, output_source)
    for relative, value in ((PLAN, plan), (NEGATIVE, negative), (SUCCESS, success)):
        path = output / relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(canonical(value))
    write_tsv(output / COVERAGE, [
        "coverage_kind", "source_id", "sequence", "input_class", "collection_action",
        "isolated_case", "current_state", "authority_effect",
    ], coverage)
    metadata = {
        "schema_version": "1",
        "collection_review_id": module.REVIEW_ID,
        "candidate_state": module.SUCCESS_DECISION,
        "collection_acceptance_gate": module.ACCEPTANCE_GATE,
        "owner_activation_acceptance_id": module.OWNER_ACCEPTANCE_ID,
        "implementation_source_sha256": sha(output_source),
        "isolated_fixture_plan_sha256": sha(output / PLAN),
        "negative_cases_sha256": sha(output / NEGATIVE),
        "collection_coverage_sha256": sha(output / COVERAGE),
        "isolated_success_sha256": sha(output / SUCCESS),
        "input_contract_coverage_count": "20",
        "isolated_success_case_count": "1",
        "isolated_negative_case_count": "20",
        "isolated_document_role_count": "5",
        "isolated_coordinate_row_count": "41",
        "isolated_coordinate_metadata_field_count": "10",
        "isolated_document_open_count": "5",
        "isolated_document_read_count": "5",
        "isolated_provider_lstat_count": "41",
        "isolated_replay_lstat_count": "1",
        "isolated_repository_metadata_capture_count": "2",
        "isolated_remote_metadata_capture_count": "1",
        "isolated_executor_identity_capture_count": "1",
        "isolated_envelope_write_count": "2",
        "selected_provider_open_count": "0",
        "selected_provider_read_count": "0",
        "provider_byte_count": "0",
        "project_replay_open_count": "0",
        "project_replay_read_count": "0",
        "project_replay_write_count": "0",
        "current_live_document_count": "0",
        "current_execution_authorization_count": "0",
        "current_local_supply_map_count": "0",
        "current_live_authority_count": "0",
        "provider_open_gate_armed": "NO",
        "accepted_transaction_count": "1",
        "consumed_transaction_count": "0",
        "remaining_transaction_count": "1",
        "execution_mode": module.EXECUTION_MODE,
        "live_input_set_accepted": "NO",
        "execution_authorized": "NO",
        "next_action": "review-and-accept-non-executing-selected-provider-local-supply-live-authority-transaction-exact-input-set-collection-candidate-boundary",
        "authority_effect": "PRODUCTION_CAPABLE_ISOLATED_FIXTURE_COLLECTION_SEALING_CANDIDATE_20_INPUTS_1_SUCCESS_20_FAIL_CLOSED_5_DOCUMENT_READS_41_PROVIDER_LSTATS_1_REPLAY_LSTAT_2_ENVELOPE_WRITES_ZERO_PROVIDER_CONTENT_REPLAY_OR_LIVE_AUTHORITY",
        "prohibited_inference": "CANDIDATE_REVIEW_DOES_NOT_CONSUME_OWNER_TRANSACTION_ACCEPT_LIVE_INPUTS_DISCOVER_PROVIDER_PATHS_OPEN_OR_READ_PROVIDER_CONTENT_OPEN_READ_OR_WRITE_PROJECT_REPLAY_EXECUTE_OR_ARM_PROVIDER_GATE",
    }
    write_tsv(output / METADATA, ["key", "value"], [{"key": k, "value": v} for k, v in metadata.items()])


if __name__ == "__main__":
    main()
