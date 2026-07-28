#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import posixpath
import re
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

SYNTHETIC_MARKER = "SYNTHETIC_REPOSITORY_FIXTURE_ONLY"
SYNTHETIC_PATH_PREFIX = "/__synthetic__/termux-native-desktop/selected-provider/"
IMPLEMENTATION_REVIEW_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-IMPLEMENTATION-REVIEW-001"
IMPLEMENTATION_ACCEPTANCE_GATE = "SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-IMPLEMENTATION-ACCEPTANCE-OPEN"
DESIGN_ACCEPTANCE_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-DESIGN-ACCEPT-001"
CONTRACT_ACCEPTANCE_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-ACCEPT-001"
ADAPTER_IMPLEMENTATION_ACCEPTANCE_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-IMPLEMENTATION-ACCEPT-001"
SUCCESS_DECISION = "QUALIFIED_SYNTHETIC_READ_ONLY_LOCAL_SUPPLY_MAP_EVIDENCE_TRANSACTION_IMPLEMENTATION_CANDIDATE"
FAILURE_DECISION = "REJECTED_SYNTHETIC_EVIDENCE_TRANSACTION_CASE_ZERO_PROVIDER_READS_WRITES_LIVE_AUTHORITY"

REVIEW_REL = Path("experiments/glibc/selected-obsidian-provider-authority/review")
DESIGN_ACCEPTANCE_NAME = "selected-provider-local-supply-map-evidence-transaction-design-boundary-acceptance.tsv"
INPUT_NAME = "selected-provider-local-supply-map-evidence-transaction-input-contract.tsv"
STATE_NAME = "selected-provider-local-supply-map-evidence-transaction-state-machine.tsv"
OPERATION_NAME = "selected-provider-local-supply-map-evidence-transaction-operation-contract.tsv"
FAILURE_NAME = "selected-provider-local-supply-map-evidence-transaction-failure-contract.tsv"
RECEIPT_NAME = "selected-provider-local-supply-map-evidence-transaction-receipt-contract.json"
DESIGN_METADATA_NAME = "selected-provider-local-supply-map-evidence-transaction-design-metadata.tsv"
CONTRACT_NAME = "selected-provider-local-supply-map-contract.tsv"
VALIDATION_NAME = "selected-provider-local-supply-map-validation-contract.tsv"
CONTRACT_ACCEPTANCE_NAME = "selected-provider-local-supply-map-contract-boundary-acceptance.tsv"
FIXTURE_NAME = "selected-provider-local-supply-map-evidence-transaction-implementation-synthetic-fixture.json"

SOURCE_DIGESTS = {'selected-provider-local-supply-map-evidence-transaction-design-boundary-acceptance.tsv': '1f60ec5983807d3f0f7527b11db953bf446eed39e1e526df21ad2f6a2812f8dd', 'selected-provider-local-supply-map-evidence-transaction-input-contract.tsv': 'fbb7b3e45ad45a7bffdf8fe8b6f483233c2fe048d809f2685796ba9e60a15089', 'selected-provider-local-supply-map-evidence-transaction-state-machine.tsv': '0d6005e4b188d98f1e44b4159db0db9f75314a047de7a2b95a0e680a19ed0f40', 'selected-provider-local-supply-map-evidence-transaction-operation-contract.tsv': '4269a87f864c22ce4bc920d4ac892483211245c64cf20e50b537e2c39e32b664', 'selected-provider-local-supply-map-evidence-transaction-failure-contract.tsv': 'eb49b325251af50524e17ae5136661418c922cb2107c94d83b9c3a1f736b7adb', 'selected-provider-local-supply-map-evidence-transaction-receipt-contract.json': '1fb99dbbc3581af9b77a52d34e2c6d25a51b245952491d4cf034b67e5ffd7dcd', 'selected-provider-local-supply-map-evidence-transaction-design-metadata.tsv': 'f461ea9622f02348323996a2042756d2f0252de35e997914503546526dcd1116', 'selected-provider-local-supply-map-contract.tsv': '2223af964e74cc8bb221d13e559e49aaf03abe364985346cb1d8e43973c6640e', 'selected-provider-local-supply-map-validation-contract.tsv': '0df8d9c7ddc28098ee220ee634a139b04aaa3d241bd36b2a4eb57ef8fbc41198', 'selected-provider-local-supply-map-contract-boundary-acceptance.tsv': '5401f46120d147394932d0004a2a37c761fc6471acaeabd730b90f1e5d859cd1'}
EXPECTED_COUNTS = {"inputs": 12, "states": 16, "operations": 32, "failures": 18, "validation_rules": 24, "coordinate_rows": 41, "coordinate_row_fields": 10}

FAILURE_CODES = {
    "LSME-FAIL-001": "LSME_EXECUTION_AUTHORIZATION_MISSING",
    "LSME-FAIL-002": "LSME_REPOSITORY_BASELINE_MISMATCH",
    "LSME-FAIL-003": "LSME_CONTRACT_ACCEPTANCE_MISMATCH",
    "LSME-FAIL-004": "LSME_COORDINATE_RECEIPT_INVALID",
    "LSME-FAIL-005": "LSME_PATH_DISCOVERY_ATTEMPT",
    "LSME-FAIL-006": "LSME_PATH_NOT_CANONICAL",
    "LSME-FAIL-007": "LSME_OPEN_NOFOLLOW_FAILED",
    "LSME-FAIL-008": "LSME_OWNER_MISMATCH",
    "LSME-FAIL-009": "LSME_FILE_CHANGED_DURING_READ",
    "LSME-FAIL-010": "LSME_MEMBER_SHA_MISMATCH",
    "LSME-FAIL-011": "LSME_ELF_IDENTITY_MISMATCH",
    "LSME-FAIL-012": "LSME_SUPPLY_IDENTITY_MISMATCH",
    "LSME-FAIL-013": "LSME_ATOMIC_FAMILY_INCOMPLETE",
    "LSME-FAIL-014": "LSME_RECEIPT_REJECTED",
    "LSME-FAIL-015": "LSME_RECEIPT_SERIALIZATION_FAILED",
    "LSME-FAIL-016": "LSME_RECEIPT_OVERFLOW",
    "LSME-FAIL-017": "LSME_PROTECTED_STATE_CHANGED",
    "LSME-FAIL-018": "LSME_ARCHIVE_OR_UPLOAD_FAILED",
}

FAILURE_CASES = (
    {"failure_id": "LSME-FAIL-001", "case": "authorization-missing", "stop_operation": "LSME-OP-002"},
    {"failure_id": "LSME-FAIL-002", "case": "baseline-mismatch", "stop_operation": "LSME-OP-003"},
    {"failure_id": "LSME-FAIL-003", "case": "contract-mismatch", "stop_operation": "LSME-OP-005"},
    {"failure_id": "LSME-FAIL-004", "case": "coordinate-invalid", "stop_operation": "LSME-OP-006"},
    {"failure_id": "LSME-FAIL-005", "case": "discovery-attempt", "stop_operation": "LSME-OP-008"},
    {"failure_id": "LSME-FAIL-006", "case": "path-noncanonical", "stop_operation": "LSME-OP-012"},
    {"failure_id": "LSME-FAIL-007", "case": "open-type-invalid", "stop_operation": "LSME-OP-014"},
    {"failure_id": "LSME-FAIL-008", "case": "owner-mode-invalid", "stop_operation": "LSME-OP-016"},
    {"failure_id": "LSME-FAIL-009", "case": "stability-invalid", "stop_operation": "LSME-OP-018"},
    {"failure_id": "LSME-FAIL-010", "case": "size-digest-invalid", "stop_operation": "LSME-OP-021"},
    {"failure_id": "LSME-FAIL-011", "case": "elf-soname-invalid", "stop_operation": "LSME-OP-023"},
    {"failure_id": "LSME-FAIL-012", "case": "supply-identity-invalid", "stop_operation": "LSME-OP-025"},
    {"failure_id": "LSME-FAIL-013", "case": "atomic-family-incomplete", "stop_operation": "LSME-OP-027"},
    {"failure_id": "LSME-FAIL-014", "case": "whole-map-incomplete", "stop_operation": "LSME-OP-028"},
    {"failure_id": "LSME-FAIL-015", "case": "serialization-invalid", "stop_operation": "LSME-OP-029"},
    {"failure_id": "LSME-FAIL-016", "case": "receipt-overflow", "stop_operation": "LSME-OP-030"},
    {"failure_id": "LSME-FAIL-017", "case": "protected-state-changed", "stop_operation": "LSME-OP-031"},
    {"failure_id": "LSME-FAIL-018", "case": "result-delivery-failure", "stop_operation": "LSME-OP-032"},
)

OPERATION_HANDLERS = {
    "PACKAGE": "_verify_repository_design_context",
    "AUTH": "_verify_inactive_synthetic_authorization",
    "BASE": "_verify_synthetic_baseline",
    "REMOTE": "_verify_synthetic_baseline",
    "CONTRACT": "_verify_repository_design_context",
    "COORD": "_validate_synthetic_coordinate_receipt",
    "COUNT": "_validate_synthetic_coordinate_receipt",
    "NOSEARCH": "_assert_no_discovery",
    "TOOLS": "_verify_modeled_capabilities",
    "PROTECT_PRE": "_verify_protected_state_model",
    "ROW_ORDER": "_validate_synthetic_coordinate_receipt",
    "PATH_CANON": "_validate_synthetic_coordinate_receipt",
    "COMPONENT_LSTAT": "_model_provider_read_step_without_execution",
    "OPEN_NOFOLLOW": "_model_provider_read_step_without_execution",
    "REGULAR": "_model_provider_read_step_without_execution",
    "OWNER": "_model_provider_read_step_without_execution",
    "MODE": "_model_provider_read_step_without_execution",
    "PRE_ID": "_model_provider_read_step_without_execution",
    "HASH": "_model_provider_read_step_without_execution",
    "POST_ID": "_model_provider_read_step_without_execution",
    "SIZE": "_model_provider_read_step_without_execution",
    "DIGEST": "_model_provider_read_step_without_execution",
    "ELF": "_model_provider_read_step_without_execution",
    "SONAME": "_model_provider_read_step_without_execution",
    "SUPPLY_ID": "_validate_synthetic_coordinate_receipt",
    "ROW_FINAL": "_build_synthetic_row_receipts",
    "ATOMIC": "_verify_atomic_family_model",
    "WHOLE_MAP": "_verify_whole_map_model",
    "SERIALIZE": "canonical_json_bytes",
    "CAP": "_verify_receipt_cap_model",
    "PROTECT_POST": "_verify_protected_state_model",
    "ARCHIVE_UPLOAD": "_assert_synthetic_delivery_only",
}

_FORBIDDEN_PATH_TOKENS = ("*", "?", "[", "]", "{", "}", "$", "`", "~", "\\", "$(", "${")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")

@dataclass(frozen=True)
class CandidateError(Exception):
    failure_id: str
    code: str
    message: str
    operation: str

    def __str__(self) -> str:
        return f"{self.failure_id}:{self.code}:{self.operation}:{self.message}"


def _fail(failure_id: str, message: str, operation: str) -> None:
    raise CandidateError(failure_id, FAILURE_CODES[failure_id], message, operation)


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
    except (TypeError, ValueError) as exc:
        _fail("LSME-FAIL-015", f"canonical serialization failed: {exc}", "LSME-OP-029")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _verify_source_digests(repo: Path) -> None:
    for name, digest in SOURCE_DIGESTS.items():
        if sha256_file(repo / REVIEW_REL / name) != digest:
            _fail("LSME-FAIL-003", f"source digest mismatch: {name}", "LSME-OP-005")


def _source_rows(repo: Path) -> dict[str, list[dict[str, str]]]:
    return {
        "inputs": _read_tsv(repo / REVIEW_REL / INPUT_NAME),
        "states": _read_tsv(repo / REVIEW_REL / STATE_NAME),
        "operations": _read_tsv(repo / REVIEW_REL / OPERATION_NAME),
        "failures": _read_tsv(repo / REVIEW_REL / FAILURE_NAME),
        "contract": _read_tsv(repo / REVIEW_REL / CONTRACT_NAME),
        "validations": _read_tsv(repo / REVIEW_REL / VALIDATION_NAME),
    }


def _synthetic_path(row: Mapping[str, str]) -> str:
    return SYNTHETIC_PATH_PREFIX + f"{int(row['sequence']):02d}/" + row["member_basename"]


def build_synthetic_fixture(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    _verify_source_digests(repo)
    rows = _source_rows(repo)
    if {k: len(rows[k]) for k in ("inputs", "states", "operations", "failures")} != {
        "inputs": 12, "states": 16, "operations": 32, "failures": 18
    }:
        _fail("LSME-FAIL-003", "design cardinality mismatch", "LSME-OP-005")
    if len(rows["contract"]) != 41 or len(rows["validations"]) != 24:
        _fail("LSME-FAIL-003", "inherited contract cardinality mismatch", "LSME-OP-005")
    coordinates = []
    for row in rows["contract"]:
        coordinates.append({
            "contract_row_id": row["contract_row_id"],
            "sequence": int(row["sequence"]),
            "absolute_canonical_path": _synthetic_path(row),
            "coordinate_origin": "SYNTHETIC_REPOSITORY_FIXTURE_ORIGIN",
            "expected_member_sha256": row["expected_member_sha256"],
            "expected_member_size_bytes": int(row["expected_member_size_bytes"]),
            "expected_soname": row["expected_soname"],
            "expected_result_index_identity": row["expected_result_index_identity"],
            "expected_container_locator": row["expected_container_locator"],
            "expected_member_locator": row["expected_member_locator"],
        })
    fixture = {
        "schema_version": 1,
        "fixture_kind": SYNTHETIC_MARKER,
        "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "design_acceptance_id": DESIGN_ACCEPTANCE_ID,
        "contract_acceptance_id": CONTRACT_ACCEPTANCE_ID,
        "adapter_implementation_acceptance_id": ADAPTER_IMPLEMENTATION_ACCEPTANCE_ID,
        "execution_mode": "SYNTHETIC_TEXT_MODEL_ONLY_NO_PROVIDER_OPEN_OR_READ",
        "execution_authorization": {
            "state": "SYNTHETIC_INACTIVE_NOT_ISSUED_NOT_LIVE",
            "authorization_kind": "READ_ONLY_LOCAL_SUPPLY_EVIDENCE_TRANSACTION_ONLY",
            "valid": True,
            "live": False,
            "provider_read_authorized": False,
        },
        "repository_baseline": {"head": "1" * 40, "tree": "2" * 40, "remote_head": "1" * 40},
        "executor": {"uid": 1000, "identity": "SYNTHETIC_EXECUTOR_ONLY_NOT_DEVICE_UID"},
        "toolchain_capabilities": {
            "nofollow_open_modeled": True,
            "sha256_stream_modeled": True,
            "elf64_aarch64_parser_modeled": True,
            "capabilities_executed": False,
        },
        "coordinate_receipt": {
            "receipt_kind": "SYNTHETIC_EXPLICIT_COORDINATE_TEXT_ONLY",
            "coordinate_count": 41,
            "row_field_count": 10,
            "discovery_used": False,
            "environment_inference_used": False,
            "basename_fallback_used": False,
            "rows": coordinates,
        },
        "protected_state_before": {"package_database_sha256": "3" * 64, "live_glibc_prefix_sha256": "4" * 64},
        "protected_state_after": {"package_database_sha256": "3" * 64, "live_glibc_prefix_sha256": "4" * 64},
        "evidence_output_root": "/__synthetic__/termux-native-desktop/evidence-output/transaction-001",
        "provider_paths_opened": [],
        "provider_descriptors_opened": 0,
        "provider_bytes_read": 0,
        "writes_performed": [],
        "persistent_replay_writes": 0,
        "current_authorized_coordinate_count": 0,
        "current_provider_read_count": 0,
        "current_write_count": 0,
        "current_live_authority_count": 0,
        "local_supply_map_produced": False,
    }
    return fixture


def build_negative_cases() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "case_count": len(FAILURE_CASES),
        "cases": [
            {
                **case,
                "failure_code": FAILURE_CODES[case["failure_id"]],
                "expected_provider_read_count": 0,
                "expected_write_count": 0,
                "expected_live_authority_count": 0,
            }
            for case in FAILURE_CASES
        ],
    }


def build_coverage_rows(repo: Path) -> list[dict[str, str]]:
    rows = _source_rows(repo.resolve())
    result: list[dict[str, str]] = []
    for kind, source_rows, id_field, symbol_field in (
        ("INPUT", rows["inputs"], "input_id", "input_class"),
        ("STATE", rows["states"], "state_id", "state_name"),
        ("OPERATION", rows["operations"], "step_id", "phase"),
        ("FAILURE", rows["failures"], "failure_id", "failure_class"),
    ):
        for row in source_rows:
            symbol = row[symbol_field]
            if kind == "OPERATION":
                symbol = OPERATION_HANDLERS.get(symbol, "_reject_unmapped_operation")
            elif kind == "INPUT":
                symbol = "validate_input_" + symbol.lower()
            elif kind == "STATE":
                symbol = "state_" + symbol.lower()
            else:
                symbol = "reject_" + symbol.lower()
            result.append({
                "coverage_kind": kind,
                "source_id": row[id_field],
                "sequence": row["sequence"],
                "implementation_symbol": symbol,
                "enforcement_layer": "SYNTHETIC_TEXT_MODEL_ONLY",
                "synthetic_case": "success" if kind != "FAILURE" else next(x["case"] for x in FAILURE_CASES if x["failure_id"] == row[id_field]),
                "current_state": "MAPPED_SYNTHETIC_NOT_EXECUTED",
                "authority_effect": "ZERO_PROVIDER_READS_ZERO_WRITES_ZERO_LIVE_AUTHORITY",
            })
    return result


def _verify_repository_design_context(repo: Path, fixture: Mapping[str, Any]) -> None:
    _verify_source_digests(repo)
    if fixture.get("design_acceptance_id") != DESIGN_ACCEPTANCE_ID or fixture.get("contract_acceptance_id") != CONTRACT_ACCEPTANCE_ID:
        _fail("LSME-FAIL-003", "accepted design or contract id mismatch", "LSME-OP-005")


def _verify_inactive_synthetic_authorization(fixture: Mapping[str, Any]) -> None:
    auth = fixture.get("execution_authorization", {})
    if auth.get("valid") is not True or auth.get("live") is not False or auth.get("provider_read_authorized") is not False:
        _fail("LSME-FAIL-001", "synthetic inactive authorization invalid", "LSME-OP-002")


def _verify_synthetic_baseline(fixture: Mapping[str, Any]) -> None:
    baseline = fixture.get("repository_baseline", {})
    if not all(_GIT_SHA_RE.fullmatch(str(baseline.get(k, ""))) for k in ("head", "tree", "remote_head")):
        _fail("LSME-FAIL-002", "synthetic baseline malformed", "LSME-OP-003")
    if baseline["head"] != baseline["remote_head"]:
        _fail("LSME-FAIL-002", "synthetic local/remote baseline mismatch", "LSME-OP-004")


def _validate_synthetic_coordinate_receipt(repo: Path, fixture: Mapping[str, Any]) -> list[dict[str, Any]]:
    receipt = fixture.get("coordinate_receipt", {})
    coordinates = receipt.get("rows", [])
    contract = _source_rows(repo)["contract"]
    if receipt.get("coordinate_count") != 41 or receipt.get("row_field_count") != 10 or len(coordinates) != 41:
        _fail("LSME-FAIL-004", "synthetic coordinate cardinality mismatch", "LSME-OP-006")
    if receipt.get("discovery_used") is not False or receipt.get("environment_inference_used") is not False or receipt.get("basename_fallback_used") is not False:
        _fail("LSME-FAIL-005", "discovery or inference marker set", "LSME-OP-008")
    if [row.get("contract_row_id") for row in coordinates] != [row["contract_row_id"] for row in contract]:
        _fail("LSME-FAIL-004", "coordinate row set/order mismatch", "LSME-OP-007")
    if len({row["absolute_canonical_path"] for row in coordinates}) != 41:
        _fail("LSME-FAIL-004", "coordinate paths not unique", "LSME-OP-007")
    for c, expected in zip(coordinates, contract):
        path = c.get("absolute_canonical_path", "")
        if any(token in path for token in _FORBIDDEN_PATH_TOKENS) or not path.startswith(SYNTHETIC_PATH_PREFIX):
            _fail("LSME-FAIL-006", "coordinate is not exact synthetic canonical path", "LSME-OP-012")
        pure = PurePosixPath(path)
        if not pure.is_absolute() or posixpath.normpath(path) != path or ".." in pure.parts or "." in pure.parts:
            _fail("LSME-FAIL-006", "coordinate path normalization failed", "LSME-OP-012")
        if c.get("coordinate_origin") != "SYNTHETIC_REPOSITORY_FIXTURE_ORIGIN":
            _fail("LSME-FAIL-004", "coordinate origin is not direct synthetic source", "LSME-OP-006")
        expected_pairs = {
            "expected_member_sha256": expected["expected_member_sha256"],
            "expected_member_size_bytes": int(expected["expected_member_size_bytes"]),
            "expected_soname": expected["expected_soname"],
            "expected_result_index_identity": expected["expected_result_index_identity"],
            "expected_container_locator": expected["expected_container_locator"],
            "expected_member_locator": expected["expected_member_locator"],
        }
        for key, value in expected_pairs.items():
            if c.get(key) != value:
                _fail("LSME-FAIL-012", f"coordinate supply identity mismatch: {key}", "LSME-OP-025")
        if len(c) != 10:
            _fail("LSME-FAIL-004", "coordinate row field count mismatch", "LSME-OP-006")
    return coordinates


def _assert_no_discovery(fixture: Mapping[str, Any]) -> None:
    receipt = fixture["coordinate_receipt"]
    if any(receipt[k] is not False for k in ("discovery_used", "environment_inference_used", "basename_fallback_used")):
        _fail("LSME-FAIL-005", "discovery marker set", "LSME-OP-008")


def _verify_modeled_capabilities(fixture: Mapping[str, Any]) -> None:
    caps = fixture.get("toolchain_capabilities", {})
    if not all(caps.get(k) is True for k in ("nofollow_open_modeled", "sha256_stream_modeled", "elf64_aarch64_parser_modeled")) or caps.get("capabilities_executed") is not False:
        _fail("LSME-FAIL-007", "synthetic capability model invalid", "LSME-OP-009")


def _verify_protected_state_model(fixture: Mapping[str, Any]) -> None:
    before = fixture.get("protected_state_before")
    after = fixture.get("protected_state_after")
    if before != after:
        _fail("LSME-FAIL-017", "protected state synthetic snapshots differ", "LSME-OP-031")


def _model_provider_read_step_without_execution(fixture: Mapping[str, Any]) -> None:
    if fixture.get("provider_paths_opened") != [] or fixture.get("provider_descriptors_opened") != 0 or fixture.get("provider_bytes_read") != 0:
        _fail("LSME-FAIL-007", "provider read surface widened", "LSME-OP-014")


def _build_synthetic_row_receipts(repo: Path, fixture: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = _validate_synthetic_coordinate_receipt(repo, fixture)
    return [
        {
            "contract_row_id": row["contract_row_id"],
            "sequence": row["sequence"],
            "synthetic_path": row["absolute_canonical_path"],
            "validation_state": "MODELED_PASS_NOT_EXECUTED",
            "provider_open_performed": False,
            "provider_read_performed": False,
        }
        for row in rows
    ]


def _verify_atomic_family_model(row_receipts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(row_receipts) != 41:
        _fail("LSME-FAIL-013", "synthetic atomic-family input incomplete", "LSME-OP-027")
    families = [
        {"family": "AT_SPI2_CORE", "state": "MODELED_COMPLETE_NOT_EXECUTED"},
        {"family": "GTK3_CORE", "state": "MODELED_COMPLETE_NOT_EXECUTED"},
        {"family": "CAIRO_CORE", "state": "MODELED_COMPLETE_NOT_EXECUTED"},
        {"family": "GENERAL_PROVIDER_SET", "state": "MODELED_COMPLETE_NOT_EXECUTED"},
    ]
    return families


def _verify_whole_map_model(row_receipts: list[dict[str, Any]]) -> None:
    if len(row_receipts) != 41 or any(row.get("validation_state") != "MODELED_PASS_NOT_EXECUTED" for row in row_receipts):
        _fail("LSME-FAIL-014", "synthetic whole-map model incomplete", "LSME-OP-028")


def _verify_receipt_cap_model(receipt_bytes: bytes) -> None:
    if len(receipt_bytes) > 1048576:
        _fail("LSME-FAIL-016", "synthetic receipt exceeds reservation", "LSME-OP-030")


def _assert_synthetic_delivery_only(fixture: Mapping[str, Any]) -> None:
    if not str(fixture.get("evidence_output_root", "")).startswith("/__synthetic__/"):
        _fail("LSME-FAIL-018", "synthetic output root widened", "LSME-OP-032")
    if fixture.get("writes_performed") != []:
        _fail("LSME-FAIL-018", "write surface widened", "LSME-OP-032")


def _failure_for_case(case: str) -> dict[str, str] | None:
    return next((row for row in FAILURE_CASES if row["case"] == case), None)


def _state_trace(rows: list[dict[str, str]], failed: bool) -> list[str]:
    names = [row["state_name"] for row in rows]
    if failed:
        return ["INIT", "REJECTED", "FINALIZED"]
    return [name for name in names if name != "REJECTED"]


def _base_result(case: str, pass_value: bool) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "case": case,
        "pass": pass_value,
        "execution_mode": "SYNTHETIC_TEXT_MODEL_ONLY_NO_PROVIDER_OPEN_OR_READ",
        "authority_state": "SYNTHETIC_ONLY_NOT_AUTHORITY",
        "provider_paths_opened": [],
        "provider_descriptors_opened": 0,
        "provider_bytes_read": 0,
        "writes_performed": [],
        "persistent_replay_writes": 0,
        "current_authorized_coordinate_count": 0,
        "current_provider_read_count": 0,
        "current_write_count": 0,
        "current_live_authority_count": 0,
        "local_supply_map_produced": False,
    }


def execute_synthetic_case(repo: Path, fixture: Mapping[str, Any], case: str) -> dict[str, Any]:
    repo = repo.resolve()
    data = copy.deepcopy(dict(fixture))
    if data.get("fixture_kind") != SYNTHETIC_MARKER:
        result = _base_result(case, False)
        result.update({"decision": FAILURE_DECISION, "failure_id": "LSME-FAIL-003", "failure_code": FAILURE_CODES["LSME-FAIL-003"], "failure_operation": "LSME-OP-001", "message": "fixture marker invalid", "operation_trace": [], "state_trace": ["INIT", "REJECTED", "FINALIZED"]})
        return result
    failure_case = _failure_for_case(case)
    if case != "success" and failure_case is None:
        raise ValueError(f"unknown synthetic case: {case}")
    rows = _source_rows(repo)
    operations = rows["operations"]
    trace: list[dict[str, Any]] = []
    row_receipts: list[dict[str, Any]] = []
    atomic_results: list[dict[str, Any]] = []
    receipt_bytes = b""
    try:
        for operation in operations:
            op_id = operation["step_id"]
            trace.append({"step_id": op_id, "phase": operation["phase"], "mode": "SYNTHETIC_MODELED_NOT_EXECUTED"})
            if failure_case and op_id == failure_case["stop_operation"]:
                _fail(failure_case["failure_id"], f"synthetic failure case: {case}", op_id)
            phase = operation["phase"]
            if phase in ("PACKAGE", "CONTRACT"):
                _verify_repository_design_context(repo, data)
            elif phase == "AUTH":
                _verify_inactive_synthetic_authorization(data)
            elif phase in ("BASE", "REMOTE"):
                _verify_synthetic_baseline(data)
            elif phase in ("COORD", "COUNT", "ROW_ORDER", "PATH_CANON", "SUPPLY_ID"):
                _validate_synthetic_coordinate_receipt(repo, data)
            elif phase == "NOSEARCH":
                _assert_no_discovery(data)
            elif phase == "TOOLS":
                _verify_modeled_capabilities(data)
            elif phase in ("PROTECT_PRE", "PROTECT_POST"):
                _verify_protected_state_model(data)
            elif phase in ("COMPONENT_LSTAT", "OPEN_NOFOLLOW", "REGULAR", "OWNER", "MODE", "PRE_ID", "HASH", "POST_ID", "SIZE", "DIGEST", "ELF", "SONAME"):
                _model_provider_read_step_without_execution(data)
            elif phase == "ROW_FINAL":
                row_receipts = _build_synthetic_row_receipts(repo, data)
            elif phase == "ATOMIC":
                atomic_results = _verify_atomic_family_model(row_receipts)
            elif phase == "WHOLE_MAP":
                _verify_whole_map_model(row_receipts)
            elif phase == "SERIALIZE":
                receipt_bytes = canonical_json_bytes({"rows": row_receipts, "atomic_family_results": atomic_results, "decision": SUCCESS_DECISION})
            elif phase == "CAP":
                _verify_receipt_cap_model(receipt_bytes)
            elif phase == "ARCHIVE_UPLOAD":
                _assert_synthetic_delivery_only(data)
        result = _base_result(case, True)
        result.update({
            "decision": SUCCESS_DECISION,
            "acceptance_gate": IMPLEMENTATION_ACCEPTANCE_GATE,
            "coverage_count": 78,
            "input_count": 12,
            "state_count": 16,
            "operation_count": 32,
            "failure_count": 18,
            "inherited_validation_rule_count": 24,
            "synthetic_coordinate_row_count": 41,
            "synthetic_coordinate_row_field_count": 10,
            "operation_trace": trace,
            "state_trace": _state_trace(rows["states"], False),
            "synthetic_row_receipts": row_receipts,
            "atomic_family_results": atomic_results,
            "receipt_bytes": len(receipt_bytes),
            "receipt_sha256": sha256_bytes(receipt_bytes),
            "evidence_transaction_executed": False,
            "provider_read_steps_modeled": True,
        })
        return result
    except CandidateError as exc:
        result = _base_result(case, False)
        result.update({
            "decision": FAILURE_DECISION,
            "failure_id": exc.failure_id,
            "failure_code": exc.code,
            "failure_operation": exc.operation,
            "message": exc.message,
            "operation_trace": trace,
            "state_trace": _state_trace(rows["states"], True),
            "evidence_transaction_executed": False,
        })
        return result


def _exact_fixture_path(repo: Path) -> Path:
    return (repo / REVIEW_REL / FIXTURE_NAME).resolve()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--case", default="success")
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    fixture_path = args.fixture.resolve()
    if fixture_path != _exact_fixture_path(repo):
        parser.error("fixture must be the exact repository-owned synthetic evidence-transaction implementation fixture")
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    result = execute_synthetic_case(repo, fixture, args.case)
    sys.stdout.buffer.write(canonical_json_bytes(result))
    raise SystemExit(0 if result.get("pass") else 2)


if __name__ == "__main__":
    main()
