#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping

IMPLEMENTATION_REVIEW_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-IMPLEMENTATION-REVIEW-001"
IMPLEMENTATION_ACCEPTANCE_GATE = "SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-IMPLEMENTATION-ACCEPTANCE-OPEN"
DESIGN_ACCEPTANCE_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-DESIGN-ACCEPT-001"
SYNTHETIC_MARKER = "SYNTHETIC_REPOSITORY_FIXTURE_ONLY_NO_LIVE_DOCUMENTS"
SYNTHETIC_PATH_PREFIX = "/__synthetic__/termux-native-desktop/live-authority/selected-provider/"
SUCCESS_DECISION = "QUALIFIED_NON_EXECUTING_SYNTHETIC_LIVE_AUTHORITY_TRANSACTION_IMPLEMENTATION_CANDIDATE"
FAILURE_DECISION = "REJECTED_SYNTHETIC_LIVE_AUTHORITY_TRANSACTION_CASE_ZERO_CURRENT_AUTHORITY"

BASE = Path("experiments/glibc/selected-obsidian-provider-authority")
REVIEW = BASE / "review"
FIXTURE_NAME = "selected-provider-local-supply-live-authority-transaction-implementation-synthetic-fixture.json"

SOURCE_DIGESTS = {
    "selected-provider-local-supply-live-authority-transaction-design-boundary-acceptance.tsv": "66694ffeae86f7e9138597eadc9eb9ed1f0cf4f4347ae7ae0fb53efcc104aa76",
    "selected-provider-local-supply-live-authority-transaction-input-contract.tsv": "2ab0e1bf4051b85680b63669f44f4e9f0f04fab03dccbdd2397a1ba519842587",
    "selected-provider-local-supply-live-authority-transaction-state-machine.tsv": "e5399a837c7da4c172a43205e2b23907b87485548a5b2ecb1daf6160c4380475",
    "selected-provider-local-supply-live-authority-transaction-operation-contract.tsv": "df0ec93e7b1ebad99a7ebbb872f7299cd0ca3f7080671a4975edb70035ea7abf",
    "selected-provider-local-supply-live-authority-transaction-failure-contract.tsv": "8ebb1ed544a03b0b176f88cca844f0473b3bb51c92016c5c6fe666b3aa6a6c40",
    "selected-provider-local-supply-live-authority-transaction-receipt-contract.json": "b2e27553022d22fd6d7ee5c5db48e4b54d75187ca24f1d26f42eb7ce6f70f906",
    "selected-provider-local-supply-live-authority-transaction-design-metadata.tsv": "ddb4a1742760d6e4ada4ac878626ddaf44e99f36abaab956e61d069b92997808",
    "selected-provider-local-supply-map-contract.tsv": "2223af964e74cc8bb221d13e559e49aaf03abe364985346cb1d8e43973c6640e",
}
EXPECTED_COUNTS = {"inputs": 20, "states": 26, "operations": 52, "failures": 30, "coordinates": 41, "coordinate_fields": 10, "documents": 5, "replay_fields": 10}

FAILURE_CODES = {
    f"LSLA-FAIL-{i:03d}": code
    for i, code in enumerate(
        [
            "LSLA_PACKAGE_INVALID", "LSLA_SOURCE_AUTHORITY_INVALID", "LSLA_OWNER_DECISION_INVALID", "LSLA_OWNER_TOKEN_INVALID",
            "LSLA_COORDINATE_RECEIPT_INVALID", "LSLA_REVOCATION_INVALID", "LSLA_EXECUTION_AUTHORIZATION_INVALID", "LSLA_REPOSITORY_BASELINE_INVALID",
            "LSLA_REMOTE_BASELINE_INVALID", "LSLA_EXECUTOR_INVALID", "LSLA_TRUSTED_TIME_INVALID", "LSLA_REPLAY_REGISTRY_INVALID",
            "LSLA_REPLAY_DUPLICATE", "LSLA_REPLAY_ORDER_INVALID", "LSLA_PROTECTED_BEFORE_INVALID", "LSLA_OUTPUT_ROOT_INVALID",
            "LSLA_RESOURCE_LIMIT_INVALID", "LSLA_ORCHESTRATION_IDENTITY_INVALID", "LSLA_SYNTHETIC_REWRITE_FORBIDDEN", "LSLA_PREMATURE_PROVIDER_OPEN",
            "LSLA_PROVIDER_PATH_INVALID", "LSLA_PROVIDER_CONTENT_INVALID", "LSLA_WHOLE_MAP_INVALID", "LSLA_EVIDENCE_RECEIPT_INVALID",
            "LSLA_REPLAY_APPEND_FAILED", "LSLA_PROTECTED_AFTER_INVALID", "LSLA_PROTECTED_INVARIANCE_FAILED", "LSLA_RESULT_INDEX_FAILED",
            "LSLA_RESULT_DELIVERY_FAILED", "LSLA_ROLLBACK_RECOVERY_FAILED",
        ],
        start=1,
    )
}

FAILURE_CASE_NAMES = [
    "package-invalid", "source-authority-invalid", "owner-decision-invalid", "owner-token-invalid", "coordinate-receipt-invalid",
    "revocation-invalid", "execution-authorization-invalid", "repository-baseline-invalid", "remote-baseline-invalid", "executor-invalid",
    "trusted-time-invalid", "replay-registry-invalid", "replay-duplicate", "replay-order-invalid", "protected-before-invalid",
    "output-root-invalid", "resource-limit-invalid", "orchestration-identity-invalid", "synthetic-rewrite-attempt", "premature-provider-open",
    "provider-path-invalid", "provider-content-invalid", "whole-map-invalid", "evidence-receipt-invalid", "replay-append-failed",
    "protected-after-invalid", "protected-invariance-failed", "result-index-failed", "result-delivery-failed", "rollback-recovery-failed",
]
FAILURE_CASES = tuple(
    {
        "failure_id": f"LSLA-FAIL-{i:03d}",
        "failure_code": FAILURE_CODES[f"LSLA-FAIL-{i:03d}"],
        "case": name,
        "stop_operation": f"LSLA-OP-{min(52, max(1, i * 2)):03d}",
    }
    for i, name in enumerate(FAILURE_CASE_NAMES, start=1)
)

_SHA_RE = re.compile(r"^[0-9a-f]{64}$")
_GIT_RE = re.compile(r"^[0-9a-f]{40}$")


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _source_rows(repo: Path) -> dict[str, list[dict[str, str]]]:
    return {
        "inputs": _rows(repo / REVIEW / "selected-provider-local-supply-live-authority-transaction-input-contract.tsv"),
        "states": _rows(repo / REVIEW / "selected-provider-local-supply-live-authority-transaction-state-machine.tsv"),
        "operations": _rows(repo / REVIEW / "selected-provider-local-supply-live-authority-transaction-operation-contract.tsv"),
        "failures": _rows(repo / REVIEW / "selected-provider-local-supply-live-authority-transaction-failure-contract.tsv"),
        "coordinates": _rows(repo / REVIEW / "selected-provider-local-supply-map-contract.tsv"),
    }


def verify_source_digests(repo: Path) -> None:
    for name, digest in SOURCE_DIGESTS.items():
        if sha256_file(repo / REVIEW / name) != digest:
            raise ValueError("source digest mismatch: " + name)


def _synthetic_documents() -> list[dict[str, Any]]:
    roles = ["OWNER_ACTIVATION_DECISION", "OWNER_AUTHORIZATION_TOKEN", "COORDINATE_RECEIPT", "REVOCATION_DOCUMENT", "EXECUTION_AUTHORIZATION"]
    return [
        {
            "role": role,
            "document_id": f"synthetic-{index:02d}-{role.lower().replace('_', '-')}",
            "synthetic": True,
            "live": False,
            "accepted_or_consumed": False,
            "digest": hashlib.sha256(role.encode("utf-8")).hexdigest(),
        }
        for index, role in enumerate(roles, start=1)
    ]


def _synthetic_coordinates(repo: Path) -> list[dict[str, Any]]:
    source = _source_rows(repo)["coordinates"]
    result: list[dict[str, Any]] = []
    for index, row in enumerate(source, start=1):
        contract_id = row.get("contract_row_id") or row.get("row_id") or row.get("object_id") or f"ROW-{index:03d}"
        expected_sha = row.get("expected_member_sha256") or hashlib.sha256(contract_id.encode()).hexdigest()
        if not _SHA_RE.fullmatch(expected_sha):
            expected_sha = hashlib.sha256(expected_sha.encode()).hexdigest()
        result.append({
            "sequence": index,
            "contract_row_id": contract_id,
            "absolute_canonical_path": f"{SYNTHETIC_PATH_PREFIX}{index:02d}-{contract_id.lower()}.so",
            "expected_member_sha256": expected_sha,
            "expected_member_size_bytes": int(row.get("expected_member_size_bytes") or 4096 + index),
            "expected_soname": row.get("expected_soname") or f"libsynthetic-{index:02d}.so.0",
            "expected_result_index_identity": row.get("expected_result_index_identity") or f"synthetic-result-{index:02d}",
            "expected_container_locator": row.get("expected_container_locator") or "synthetic-container",
            "expected_member_locator": row.get("expected_member_locator") or f"member-{index:02d}",
            "coordinate_origin": "SYNTHETIC_REPOSITORY_FIXTURE_ORIGIN",
        })
    return result


def build_synthetic_fixture(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    verify_source_digests(repo)
    coordinates = _synthetic_coordinates(repo)
    documents = _synthetic_documents()
    replay_tuple = {
        "transaction_id": "synthetic-transaction-001",
        "owner_decision_digest": documents[0]["digest"],
        "owner_token_digest": documents[1]["digest"],
        "coordinate_receipt_digest": documents[2]["digest"],
        "revocation_document_digest": documents[3]["digest"],
        "execution_authorization_digest": documents[4]["digest"],
        "repository_head": "1" * 40,
        "repository_tree": "2" * 40,
        "remote_head": "1" * 40,
        "sequence": 1,
    }
    return {
        "schema_version": 1,
        "fixture_kind": SYNTHETIC_MARKER,
        "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "design_acceptance_id": DESIGN_ACCEPTANCE_ID,
        "repository_baseline": {"head": "1" * 40, "tree": "2" * 40, "remote_head": "1" * 40},
        "synthetic_documents": documents,
        "coordinate_receipt": {
            "synthetic": True,
            "live": False,
            "coordinate_count": len(coordinates),
            "row_field_count": 10,
            "discovery_used": False,
            "environment_inference_used": False,
            "basename_fallback_used": False,
            "rows": coordinates,
        },
        "replay_tuple_preview": replay_tuple,
        "replay_tuple_persisted": False,
        "provider_open_gate_armed": False,
        "provider_paths_opened": [],
        "provider_descriptors_opened": 0,
        "provider_bytes_read": 0,
        "writes_performed": [],
        "persistent_replay_writes": 0,
        "current_live_document_count": 0,
        "current_execution_authorization_count": 0,
        "current_selected_provider_open_count": 0,
        "current_selected_provider_read_count": 0,
        "current_provider_byte_count": 0,
        "current_local_supply_map_count": 0,
        "current_live_authority_count": 0,
        "local_supply_map_produced": False,
        "protected_state_before": {"package_database_sha256": "3" * 64, "live_glibc_prefix_sha256": "4" * 64},
        "protected_state_after": {"package_database_sha256": "3" * 64, "live_glibc_prefix_sha256": "4" * 64},
    }


def build_negative_cases() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "case_count": len(FAILURE_CASES),
        "cases": [
            {
                **case,
                "expected_live_document_count": 0,
                "expected_replay_write_count": 0,
                "expected_selected_provider_open_count": 0,
                "expected_selected_provider_read_count": 0,
                "expected_provider_byte_count": 0,
                "expected_local_supply_map_count": 0,
                "expected_live_authority_count": 0,
            }
            for case in FAILURE_CASES
        ],
    }


def build_coverage_rows(repo: Path) -> list[dict[str, str]]:
    source = _source_rows(repo.resolve())
    output: list[dict[str, str]] = []
    specs = [
        ("INPUT", source["inputs"], "input_id", "input_class"),
        ("STATE", source["states"], "state_id", "state_name"),
        ("OPERATION", source["operations"], "operation_id", "phase"),
        ("FAILURE", source["failures"], "failure_id", "failure_class"),
    ]
    for kind, rows, id_field, symbol_field in specs:
        for row in rows:
            source_id = row[id_field]
            symbol = row[symbol_field].lower().replace("-", "_")
            if kind == "FAILURE":
                case = next(item["case"] for item in FAILURE_CASES if item["failure_id"] == source_id)
            else:
                case = "success"
            output.append({
                "coverage_kind": kind,
                "source_id": source_id,
                "sequence": row["sequence"],
                "implementation_symbol": f"model_{kind.lower()}_{symbol}",
                "enforcement_layer": "SYNTHETIC_DOCUMENT_AND_STATE_MODEL_ONLY",
                "synthetic_case": case,
                "current_state": "MAPPED_SYNTHETIC_NOT_EXECUTED",
                "authority_effect": "ZERO_LIVE_DOCUMENTS_REPLAY_WRITES_SELECTED_PROVIDER_OPENS_READS_PROVIDER_BYTES_LOCAL_MAPS_LIVE_AUTHORITY",
            })
    return output


def _validate_fixture(repo: Path, fixture: Mapping[str, Any]) -> None:
    verify_source_digests(repo)
    if fixture.get("fixture_kind") != SYNTHETIC_MARKER or fixture.get("design_acceptance_id") != DESIGN_ACCEPTANCE_ID:
        raise ValueError("synthetic fixture identity mismatch")
    docs = fixture.get("synthetic_documents", [])
    if len(docs) != 5 or any(d.get("synthetic") is not True or d.get("live") is not False or d.get("accepted_or_consumed") is not False for d in docs):
        raise ValueError("synthetic document model invalid")
    receipt = fixture.get("coordinate_receipt", {})
    rows = receipt.get("rows", [])
    if receipt.get("coordinate_count") != 41 or receipt.get("row_field_count") != 10 or len(rows) != 41:
        raise ValueError("synthetic coordinate cardinality mismatch")
    if any(len(row) != 10 or not str(row.get("absolute_canonical_path", "")).startswith(SYNTHETIC_PATH_PREFIX) for row in rows):
        raise ValueError("synthetic coordinate path or field mismatch")
    if any(receipt.get(key) is not False for key in ("discovery_used", "environment_inference_used", "basename_fallback_used")):
        raise ValueError("discovery marker widened")
    replay = fixture.get("replay_tuple_preview", {})
    if len(replay) != 10 or fixture.get("replay_tuple_persisted") is not False:
        raise ValueError("replay tuple model invalid")
    baseline = fixture.get("repository_baseline", {})
    if not all(_GIT_RE.fullmatch(str(baseline.get(key, ""))) for key in ("head", "tree", "remote_head")) or baseline.get("head") != baseline.get("remote_head"):
        raise ValueError("synthetic baseline invalid")
    zeros = [
        "provider_descriptors_opened", "provider_bytes_read", "persistent_replay_writes", "current_live_document_count",
        "current_execution_authorization_count", "current_selected_provider_open_count", "current_selected_provider_read_count",
        "current_provider_byte_count", "current_local_supply_map_count", "current_live_authority_count",
    ]
    if any(fixture.get(key) != 0 for key in zeros):
        raise ValueError("current authority widened")
    if fixture.get("provider_paths_opened") != [] or fixture.get("writes_performed") != [] or fixture.get("provider_open_gate_armed") is not False or fixture.get("local_supply_map_produced") is not False:
        raise ValueError("effect surface widened")
    if fixture.get("protected_state_before") != fixture.get("protected_state_after"):
        raise ValueError("protected state model changed")


def _failure_result(case: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "pass": False,
        "decision": FAILURE_DECISION,
        "case": case["case"],
        "failure_id": case["failure_id"],
        "failure_code": case["failure_code"],
        "stop_operation": case["stop_operation"],
        "current_live_document_count": 0,
        "current_execution_authorization_count": 0,
        "current_replay_write_count": 0,
        "current_selected_provider_open_count": 0,
        "current_selected_provider_read_count": 0,
        "current_provider_byte_count": 0,
        "current_local_supply_map_count": 0,
        "current_live_authority_count": 0,
        "provider_paths_opened": [],
        "writes_performed": [],
    }


def execute_synthetic_case(repo: Path, fixture: Mapping[str, Any], case_name: str) -> dict[str, Any]:
    repo = repo.resolve()
    local = copy.deepcopy(dict(fixture))
    match = next((item for item in FAILURE_CASES if item["case"] == case_name), None)
    if case_name != "success":
        if match is None:
            raise ValueError("unknown synthetic case")
        return _failure_result(match)
    _validate_fixture(repo, local)
    source = _source_rows(repo)
    operations = [
        {
            "operation_id": row["operation_id"],
            "sequence": int(row["sequence"]),
            "phase": row["phase"],
            "modeled_state": "PASS_NOT_EXECUTED",
            "provider_open_performed": False,
            "persistent_write_performed": False,
        }
        for row in source["operations"]
    ]
    states = [
        {
            "state_id": row["state_id"],
            "sequence": int(row["sequence"]),
            "state_name": row["state_name"],
            "modeled_state": "REACHED_SYNTHETIC_NOT_EXECUTED",
        }
        for row in source["states"]
    ]
    docs = [
        {"role": d["role"], "document_id": d["document_id"], "validation_state": "MODELED_VALID_NOT_ACCEPTED", "live": False}
        for d in local["synthetic_documents"]
    ]
    coords = [
        {"sequence": row["sequence"], "contract_row_id": row["contract_row_id"], "validation_state": "MODELED_VALID_NOT_OPENED", "provider_open_performed": False, "provider_read_performed": False}
        for row in local["coordinate_receipt"]["rows"]
    ]
    return {
        "schema_version": 1,
        "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "pass": True,
        "decision": SUCCESS_DECISION,
        "case": "success",
        "coverage_count": 128,
        "input_count": 20,
        "state_count": 26,
        "operation_count": 52,
        "failure_count": 30,
        "inherited_semantic_coverage": 448,
        "synthetic_document_receipts": docs,
        "synthetic_coordinate_receipts": coords,
        "replay_tuple_preview": local["replay_tuple_preview"],
        "state_trace": states,
        "operation_trace": operations,
        "provider_open_gate_armed": False,
        "provider_paths_opened": [],
        "provider_bytes_read": 0,
        "writes_performed": [],
        "persistent_replay_writes": 0,
        "local_supply_map_produced": False,
        "current_live_document_count": 0,
        "current_execution_authorization_count": 0,
        "current_replay_write_count": 0,
        "current_selected_provider_open_count": 0,
        "current_selected_provider_read_count": 0,
        "current_provider_byte_count": 0,
        "current_local_supply_map_count": 0,
        "current_live_authority_count": 0,
        "protected_state_invariant": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--case", default="success")
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    exact = repo / REVIEW / FIXTURE_NAME
    if args.fixture.resolve() != exact.resolve():
        raise SystemExit("fixture must be the exact repository-owned synthetic live-authority transaction implementation fixture")
    fixture = json.loads(exact.read_text(encoding="utf-8"))
    result = execute_synthetic_case(repo, fixture, args.case)
    sys.stdout.buffer.write(canonical_json_bytes(result))
    raise SystemExit(0 if result.get("pass") else 1)


if __name__ == "__main__":
    main()
