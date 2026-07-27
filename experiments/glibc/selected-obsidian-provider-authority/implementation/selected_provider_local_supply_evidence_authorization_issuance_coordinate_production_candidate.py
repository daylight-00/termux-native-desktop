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
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable, Mapping, MutableMapping, Sequence

SYNTHETIC_MARKER = "SYNTHETIC_REPOSITORY_FIXTURE_ONLY"
SYNTHETIC_PATH_PREFIX = "/__synthetic__/termux-native-desktop/selected-provider/"
IMPLEMENTATION_REVIEW_ID = (
    "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-"
    "COORDINATE-PRODUCTION-IMPLEMENTATION-REVIEW-001"
)
IMPLEMENTATION_ACCEPTANCE_GATE = (
    "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-"
    "COORDINATE-PRODUCTION-IMPLEMENTATION-ACCEPTANCE-OPEN"
)
DESIGN_ACCEPTANCE_ID = (
    "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-"
    "COORDINATE-PRODUCTION-DESIGN-ACCEPT-001"
)
CONTRACT_ACCEPTANCE_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-ACCEPT-001"
EVIDENCE_DESIGN_ACCEPTANCE_ID = (
    "SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-DESIGN-ACCEPT-001"
)
AUTHORIZATION_KIND = "READ_ONLY_LOCAL_SUPPLY_EVIDENCE_TRANSACTION_ONLY"
PERMITTED_EFFECT = "READ_ONLY_PROVIDER_VALIDATION_AND_TRANSACTION_SCOPED_EVIDENCE_OUTPUTS_ONLY"
INACTIVE_STATE = (
    "SYNTHETIC_INACTIVE_CANDIDATE_ONLY_NOT_AUTHORITY_"
    "SEPARATE_OWNER_ACTIVATION_AND_EVIDENCE_EXECUTION_AUTHORIZATION_REQUIRED"
)
SUCCESS_DECISION = (
    "QUALIFIED_SYNTHETIC_INACTIVE_OWNER_AUTHORIZATION_TOKEN_AND_"
    "COORDINATE_RECEIPT_IMPLEMENTATION_CANDIDATE"
)
FAILURE_DECISION = "REJECTED_SYNTHETIC_IMPLEMENTATION_CASE_ZERO_LIVE_AUTHORITY"

REVIEW_REL = Path("experiments/glibc/selected-obsidian-provider-authority/review")
IMPLEMENTATION_REL = Path("experiments/glibc/selected-obsidian-provider-authority/implementation")
TOKEN_SCHEMA_NAME = "selected-provider-local-supply-evidence-owner-authorization-token-schema.json"
COORDINATE_SCHEMA_NAME = "selected-provider-local-supply-evidence-coordinate-receipt-schema.json"
VALIDATION_NAME = "selected-provider-local-supply-evidence-authorization-coordinate-validation-contract.tsv"
CONTRACT_NAME = "selected-provider-local-supply-map-contract.tsv"
DESIGN_ACCEPTANCE_NAME = (
    "selected-provider-local-supply-evidence-authorization-issuance-"
    "coordinate-production-design-boundary-acceptance.tsv"
)
INPUT_NAME = (
    "selected-provider-local-supply-evidence-authorization-issuance-"
    "coordinate-production-input-contract.tsv"
)
STATE_NAME = (
    "selected-provider-local-supply-evidence-authorization-issuance-"
    "coordinate-production-state-machine.tsv"
)
OPERATION_NAME = (
    "selected-provider-local-supply-evidence-authorization-issuance-"
    "coordinate-production-operation-contract.tsv"
)
FAILURE_NAME = (
    "selected-provider-local-supply-evidence-authorization-issuance-"
    "coordinate-production-failure-contract.tsv"
)

SOURCE_DIGESTS = {
    DESIGN_ACCEPTANCE_NAME: "bf8d2377effb02db5e89c1b388b92f1ab5c9a908df51dc310d0d7eafba270d05",
    TOKEN_SCHEMA_NAME: "27d11e8bb8de3238b49aef77757f0328a2269a156f55fdcbdddcf4dcb4fd411b",
    COORDINATE_SCHEMA_NAME: "b94c25994ecc26e402607b9e61c0cee796c74b15435bc168a18821def9096f83",
    VALIDATION_NAME: "64a6c168e30c7a559387c27d6baa7d3bd49953d7ea304d1bd98e4043cbb57f56",
    CONTRACT_NAME: "2223af964e74cc8bb221d13e559e49aaf03abe364985346cb1d8e43973c6640e",
}

EXPECTED_COUNTS = {
    "inputs": 14,
    "states": 18,
    "operations": 36,
    "failures": 20,
    "authorization_claims": 18,
    "coordinate_rows": 41,
    "coordinate_row_fields": 10,
    "validation_rules": 30,
}

FAILURE_CODES = {
    "LSAEP-FAIL-001": "LSAEP_PACKAGE_INVALID",
    "LSAEP-FAIL-002": "LSAEP_SOURCE_CONTRACT_MISMATCH",
    "LSAEP-FAIL-003": "LSAEP_OWNER_DECISION_MISSING",
    "LSAEP-FAIL-004": "LSAEP_REPOSITORY_BASELINE_MISMATCH",
    "LSAEP-FAIL-005": "LSAEP_EXECUTOR_IDENTITY_MISMATCH",
    "LSAEP-FAIL-006": "LSAEP_TIME_WINDOW_INVALID",
    "LSAEP-FAIL-007": "LSAEP_REVOCATION_OR_REPLAY_INVALID",
    "LSAEP-FAIL-008": "LSAEP_REVOCATION_OR_REPLAY_INVALID",
    "LSAEP-FAIL-009": "LSAEP_COORDINATE_SOURCE_INVALID",
    "LSAEP-FAIL-010": "LSAEP_COORDINATE_SOURCE_INVALID",
    "LSAEP-FAIL-011": "LSAEP_COORDINATE_SOURCE_INVALID",
    "LSAEP-FAIL-012": "LSAEP_COORDINATE_SOURCE_INVALID",
    "LSAEP-FAIL-013": "LSAEP_COORDINATE_SOURCE_INVALID",
    "LSAEP-FAIL-014": "LSAEP_COORDINATE_SOURCE_INVALID",
    "LSAEP-FAIL-015": "LSAEP_SERIALIZER_UNAVAILABLE",
    "LSAEP-FAIL-016": "LSAEP_COORDINATE_SOURCE_INVALID",
    "LSAEP-FAIL-017": "LSAEP_OWNER_DECISION_MISSING",
    "LSAEP-FAIL-018": "LSAEP_OUTPUT_ROOT_INVALID",
    "LSAEP-FAIL-019": "LSAEP_PROTECTED_STATE_CHANGED",
    "LSAEP-FAIL-020": "LSAEP_RESULT_DELIVERY_FAILED",
}

FAILURE_CASES = (
    {"failure_id": "LSAEP-FAIL-001", "case": "package-invalid", "stop_operation": "LSAEP-OP-001"},
    {"failure_id": "LSAEP-FAIL-002", "case": "source-contract-mismatch", "stop_operation": "LSAEP-OP-002"},
    {"failure_id": "LSAEP-FAIL-003", "case": "owner-effect-invalid", "stop_operation": "LSAEP-OP-005"},
    {"failure_id": "LSAEP-FAIL-004", "case": "baseline-mismatch", "stop_operation": "LSAEP-OP-006"},
    {"failure_id": "LSAEP-FAIL-005", "case": "executor-mismatch", "stop_operation": "LSAEP-OP-008"},
    {"failure_id": "LSAEP-FAIL-006", "case": "time-window-invalid", "stop_operation": "LSAEP-OP-009"},
    {"failure_id": "LSAEP-FAIL-007", "case": "revocation-mismatch", "stop_operation": "LSAEP-OP-010"},
    {"failure_id": "LSAEP-FAIL-008", "case": "replay-detected", "stop_operation": "LSAEP-OP-011"},
    {"failure_id": "LSAEP-FAIL-009", "case": "coordinate-count-invalid", "stop_operation": "LSAEP-OP-013"},
    {"failure_id": "LSAEP-FAIL-010", "case": "coordinate-set-invalid", "stop_operation": "LSAEP-OP-014"},
    {"failure_id": "LSAEP-FAIL-011", "case": "object-binding-invalid", "stop_operation": "LSAEP-OP-016"},
    {"failure_id": "LSAEP-FAIL-012", "case": "path-syntax-invalid", "stop_operation": "LSAEP-OP-018"},
    {"failure_id": "LSAEP-FAIL-013", "case": "path-uniqueness-invalid", "stop_operation": "LSAEP-OP-019"},
    {"failure_id": "LSAEP-FAIL-014", "case": "coordinate-authority-invalid", "stop_operation": "LSAEP-OP-020"},
    {"failure_id": "LSAEP-FAIL-015", "case": "serialization-failure", "stop_operation": "LSAEP-OP-023"},
    {"failure_id": "LSAEP-FAIL-016", "case": "digest-mismatch", "stop_operation": "LSAEP-OP-021"},
    {"failure_id": "LSAEP-FAIL-017", "case": "cross-binding-mismatch", "stop_operation": "LSAEP-OP-029"},
    {"failure_id": "LSAEP-FAIL-018", "case": "output-scope-invalid", "stop_operation": "LSAEP-OP-031"},
    {"failure_id": "LSAEP-FAIL-019", "case": "protected-state-changed", "stop_operation": "LSAEP-OP-034"},
    {"failure_id": "LSAEP-FAIL-020", "case": "result-delivery-failure", "stop_operation": "LSAEP-OP-035"},
)

OPERATION_HANDLERS = {
    "PACKAGE": "_verify_package_context",
    "SOURCE": "_verify_source_contracts",
    "OWNER_INPUT": "_verify_owner_decision",
    "OWNER_ID": "_verify_owner_decision",
    "OWNER_EFFECT": "_verify_owner_decision",
    "BASELINE_LOCAL": "_verify_baselines",
    "BASELINE_REMOTE": "_verify_baselines",
    "EXECUTOR": "_verify_executor",
    "TIME": "_verify_time_window",
    "REVOCATION": "_verify_revocation_and_replay",
    "REPLAY": "_verify_revocation_and_replay",
    "COORD_INPUT": "_validate_coordinate_rows",
    "COORD_COUNT": "_validate_coordinate_rows",
    "COORD_SET": "_validate_coordinate_rows",
    "COORD_SEQUENCE": "_validate_coordinate_rows",
    "OBJECT_BIND": "_validate_coordinate_rows",
    "PATH_ABSOLUTE": "_validate_coordinate_rows",
    "PATH_COMPONENTS": "_validate_coordinate_rows",
    "PATH_UNIQUE": "_validate_coordinate_rows",
    "COORD_AUTH": "_validate_coordinate_rows",
    "ROW_DIGEST": "_validate_coordinate_rows",
    "COORD_ENVELOPE": "_build_coordinate_receipt",
    "COORD_SERIALIZE": "canonical_json_bytes",
    "COORD_DIGEST": "sha256_bytes",
    "TOKEN_CLAIMS": "_build_token_candidate",
    "TOKEN_BIND": "_build_token_candidate",
    "TOKEN_SERIALIZE": "canonical_json_bytes",
    "TOKEN_DIGEST": "sha256_bytes",
    "CROSS_BIND": "_verify_cross_bindings",
    "PROTECT_PRE": "_verify_protected_state",
    "STAGE": "_build_success_report",
    "NO_ACTIVATION": "_assert_zero_live_authority",
    "PROTECT_POST": "_verify_protected_state",
    "INVARIANCE": "_verify_protected_state",
    "RESULT": "_build_success_report",
    "ARCHIVE_UPLOAD": "_assert_synthetic_delivery_only",
}

_FORBIDDEN_PATH_TOKENS = ("*", "?", "[", "]", "{", "}", "$", "`", "~", "\\", "$(", "${")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_ID_RE = re.compile(r"^[A-Z0-9][A-Z0-9._:-]{3,127}$")


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
        _fail("LSAEP-FAIL-015", f"canonical serialization failed: {exc}", "LSAEP-OP-023")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _parse_utc(value: str, *, failure_id: str = "LSAEP-FAIL-006", operation: str = "LSAEP-OP-009") -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        _fail(failure_id, f"invalid UTC value: {value!r}", operation)
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        _fail(failure_id, f"invalid UTC value: {exc}", operation)
    if parsed.tzinfo != timezone.utc:
        _fail(failure_id, "timestamp is not UTC", operation)
    return parsed


def load_contract_context(repo_root: Path) -> dict[str, Any]:
    review = repo_root.resolve() / REVIEW_REL
    for name, digest in SOURCE_DIGESTS.items():
        path = review / name
        if not path.is_file() or sha256_file(path) != digest:
            _fail("LSAEP-FAIL-002", f"source digest mismatch: {name}", "LSAEP-OP-002")
    design_acceptance = _read_tsv(review / DESIGN_ACCEPTANCE_NAME)
    if len(design_acceptance) != 1 or design_acceptance[0].get("acceptance_id") != DESIGN_ACCEPTANCE_ID:
        _fail("LSAEP-FAIL-002", "design acceptance identity mismatch", "LSAEP-OP-002")
    token_schema = json.loads((review / TOKEN_SCHEMA_NAME).read_text(encoding="utf-8"))
    coordinate_schema = json.loads((review / COORDINATE_SCHEMA_NAME).read_text(encoding="utf-8"))
    validation_rows = _read_tsv(review / VALIDATION_NAME)
    contract_rows = _read_tsv(review / CONTRACT_NAME)
    inputs = _read_tsv(review / INPUT_NAME)
    states = _read_tsv(review / STATE_NAME)
    operations = _read_tsv(review / OPERATION_NAME)
    failures = _read_tsv(review / FAILURE_NAME)
    counts = {
        "inputs": len(inputs),
        "states": len(states),
        "operations": len(operations),
        "failures": len(failures),
        "authorization_claims": len(token_schema.get("required_claims", [])),
        "coordinate_rows": len(contract_rows),
        "coordinate_row_fields": len(coordinate_schema.get("future_required_row_fields", [])),
        "validation_rules": len(validation_rows),
    }
    if counts != EXPECTED_COUNTS:
        _fail("LSAEP-FAIL-002", f"accepted cardinality mismatch: {counts}", "LSAEP-OP-002")
    return {
        "review": review,
        "design_acceptance": design_acceptance[0],
        "token_schema": token_schema,
        "coordinate_schema": coordinate_schema,
        "validation_rows": validation_rows,
        "contract_rows": contract_rows,
        "inputs": inputs,
        "states": states,
        "operations": operations,
        "failures": failures,
        "counts": counts,
    }


def build_synthetic_fixture(repo_root: Path) -> dict[str, Any]:
    context = load_contract_context(repo_root)
    head = "1111111111111111111111111111111111111111"
    tree = "2222222222222222222222222222222222222222"
    issued = "2026-07-27T06:30:00Z"
    expires = "2026-07-27T07:30:00Z"
    transaction_id = "SYNTHETIC-TRANSACTION-IMPLEMENTATION-001"
    rows: list[dict[str, Any]] = []
    for source in sorted(context["contract_rows"], key=lambda row: int(row["sequence"])):
        sequence = int(source["sequence"])
        basename = source["member_basename"].replace("/", "_")
        path = f"{SYNTHETIC_PATH_PREFIX}{sequence:03d}/{basename}"
        rows.append(
            {
                "contract_row_id": source["contract_row_id"],
                "sequence": sequence,
                "provider_object_id": source["provider_object_id"],
                "expected_member_sha256": source["expected_member_sha256"],
                "expected_member_size_bytes": int(source["expected_member_size_bytes"]),
                "expected_soname": source["expected_soname"],
                "absolute_canonical_path": path,
                "coordinate_authority_id": "SYNTHETIC-COORDINATE-AUTHORITY-001",
                "coordinate_origin": SYNTHETIC_MARKER,
                "path_text_sha256": sha256_bytes(path.encode("utf-8")),
            }
        )
    return {
        "schema_version": 1,
        "fixture_kind": SYNTHETIC_MARKER,
        "fixture_id": "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-ISSUANCE-COORDINATE-SYNTHETIC-001",
        "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "package_valid": True,
        "source_contract_valid": True,
        "current_time_utc": "2026-07-27T06:45:00Z",
        "repository_head": head,
        "repository_tree": tree,
        "remote_head": head,
        "executor_uid": 4242,
        "owner_decision": {
            "schema_version": 1,
            "authorization_token_id": "SYNTHETIC-TOKEN-CANDIDATE-001",
            "authorization_kind": AUTHORIZATION_KIND,
            "owner_identity": "SYNTHETIC-OWNER-IDENTITY",
            "owner_decision_id": "SYNTHETIC-OWNER-DECISION-001",
            "issued_at_utc": issued,
            "expires_at_utc": expires,
            "not_before_utc": issued,
            "nonce": "SYNTHETIC-NONCE-001",
            "revocation_epoch": 7,
            "transaction_id": transaction_id,
            "contract_acceptance_id": CONTRACT_ACCEPTANCE_ID,
            "evidence_design_acceptance_id": EVIDENCE_DESIGN_ACCEPTANCE_ID,
            "repository_head": head,
            "repository_tree": tree,
            "remote_head": head,
            "executor_uid": 4242,
            "permitted_effect": PERMITTED_EFFECT,
            "prohibited_effects": [
                "PATH_DISCOVERY",
                "RESULT_OR_PACKAGE_ACQUISITION",
                "ARCHIVE_OR_PACKAGE_EXTRACTION",
                "PROVIDER_MUTATION",
                "RUNTIME_MUTATION",
                "LOCAL_MAP_ACCEPTANCE",
                "MATERIALIZER_EXECUTION",
                "GENERATION_ROOT_CREATION",
                "TARGET_POPULATION",
                "PUBLICATION",
                "DEPLOYMENT",
                "ACTIVATION",
            ],
        },
        "coordinate_source": {
            "schema_version": 1,
            "coordinate_receipt_id": "SYNTHETIC-COORDINATE-RECEIPT-CANDIDATE-001",
            "contract_acceptance_id": CONTRACT_ACCEPTANCE_ID,
            "evidence_design_acceptance_id": EVIDENCE_DESIGN_ACCEPTANCE_ID,
            "repository_head": head,
            "repository_tree": tree,
            "remote_head": head,
            "issuer_identity": "SYNTHETIC-COORDINATE-ISSUER",
            "issued_at_utc": issued,
            "rows": rows,
        },
        "revocation_registry": {
            "schema_version": 1,
            "current_revocation_epoch": 7,
            "consumed_tuples": [],
            "registry_state": "SYNTHETIC_IMMUTABLE_SNAPSHOT_ONLY",
        },
        "protected_before": {
            "repository_head": head,
            "repository_tree": tree,
            "remote_head": head,
            "package_db_sha256": "3" * 64,
            "live_glibc_tree_sha256": "4" * 64,
            "live_glibc_entry_count": 0,
            "registry_sha256": "5" * 64,
        },
        "protected_after": {
            "repository_head": head,
            "repository_tree": tree,
            "remote_head": head,
            "package_db_sha256": "3" * 64,
            "live_glibc_tree_sha256": "4" * 64,
            "live_glibc_entry_count": 0,
            "registry_sha256": "5" * 64,
        },
        "output_root": f"/__synthetic__/termux-native-desktop/evidence-output/{transaction_id}",
        "current_live_authority_count": 0,
        "current_provider_read_count": 0,
        "current_issued_token_count": 0,
        "current_coordinate_receipt_count": 0,
        "current_coordinate_row_count": 0,
    }


def build_negative_cases() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "fixture_kind": SYNTHETIC_MARKER,
        "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "case_count": len(FAILURE_CASES),
        "cases": [
            {
                **case,
                "failure_code": FAILURE_CODES[case["failure_id"]],
                "expected_live_authority_count": 0,
                "expected_provider_read_count": 0,
            }
            for case in FAILURE_CASES
        ],
    }


def _mutate_fixture(base: Mapping[str, Any], case_name: str) -> dict[str, Any]:
    fixture = copy.deepcopy(base)
    if case_name == "success":
        return fixture
    if case_name == "package-invalid":
        fixture["package_valid"] = False
    elif case_name == "source-contract-mismatch":
        fixture["source_contract_valid"] = False
    elif case_name == "owner-effect-invalid":
        fixture["owner_decision"]["permitted_effect"] = "RUNTIME_MUTATION"
    elif case_name == "baseline-mismatch":
        fixture["owner_decision"]["repository_tree"] = "9" * 40
    elif case_name == "executor-mismatch":
        fixture["executor_uid"] = 4243
    elif case_name == "time-window-invalid":
        fixture["owner_decision"]["expires_at_utc"] = "2026-07-29T06:30:01Z"
    elif case_name == "revocation-mismatch":
        fixture["revocation_registry"]["current_revocation_epoch"] = 8
    elif case_name == "replay-detected":
        owner = fixture["owner_decision"]
        fixture["revocation_registry"]["consumed_tuples"] = [
            [owner["authorization_token_id"], owner["nonce"], owner["transaction_id"]]
        ]
    elif case_name == "coordinate-count-invalid":
        fixture["coordinate_source"]["rows"].pop()
    elif case_name == "coordinate-set-invalid":
        fixture["coordinate_source"]["rows"][0]["contract_row_id"] = "LSM-CONTRACT-999"
    elif case_name == "object-binding-invalid":
        fixture["coordinate_source"]["rows"][0]["expected_member_sha256"] = "0" * 64
    elif case_name == "path-syntax-invalid":
        fixture["coordinate_source"]["rows"][0]["absolute_canonical_path"] = "/__synthetic__/../escape"
    elif case_name == "path-uniqueness-invalid":
        fixture["coordinate_source"]["rows"][1]["absolute_canonical_path"] = fixture["coordinate_source"]["rows"][0]["absolute_canonical_path"]
        fixture["coordinate_source"]["rows"][1]["path_text_sha256"] = fixture["coordinate_source"]["rows"][0]["path_text_sha256"]
    elif case_name == "coordinate-authority-invalid":
        fixture["coordinate_source"]["rows"][0]["coordinate_origin"] = "LIVE_FILESYSTEM"
    elif case_name == "serialization-failure":
        fixture["synthetic_fault"] = "SERIALIZATION"
    elif case_name == "digest-mismatch":
        fixture["coordinate_source"]["rows"][0]["path_text_sha256"] = "0" * 64
    elif case_name == "cross-binding-mismatch":
        fixture["coordinate_source"]["repository_head"] = "8" * 40
    elif case_name == "output-scope-invalid":
        fixture["output_root"] = "/data/data/com.termux/files/usr/glibc"
    elif case_name == "protected-state-changed":
        fixture["protected_after"]["package_db_sha256"] = "6" * 64
    elif case_name == "result-delivery-failure":
        fixture["synthetic_fault"] = "RESULT_DELIVERY"
    else:
        raise ValueError(f"unknown synthetic case: {case_name}")
    return fixture


def _assert_synthetic_fixture(fixture: Mapping[str, Any]) -> None:
    if fixture.get("fixture_kind") != SYNTHETIC_MARKER:
        _fail("LSAEP-FAIL-003", "non-synthetic fixture rejected", "LSAEP-OP-003")
    if fixture.get("implementation_review_id") != IMPLEMENTATION_REVIEW_ID:
        _fail("LSAEP-FAIL-002", "implementation review id mismatch", "LSAEP-OP-002")
    for key in (
        "current_live_authority_count",
        "current_provider_read_count",
        "current_issued_token_count",
        "current_coordinate_receipt_count",
        "current_coordinate_row_count",
    ):
        if fixture.get(key) != 0:
            _fail("LSAEP-FAIL-001", f"nonzero current authority marker: {key}", "LSAEP-OP-001")


def _verify_package_context(fixture: Mapping[str, Any]) -> None:
    if fixture.get("package_valid") is not True:
        _fail("LSAEP-FAIL-001", "synthetic package context invalid", "LSAEP-OP-001")


def _verify_source_contracts(fixture: Mapping[str, Any]) -> None:
    if fixture.get("source_contract_valid") is not True:
        _fail("LSAEP-FAIL-002", "synthetic source contract mismatch", "LSAEP-OP-002")


def _verify_owner_decision(fixture: Mapping[str, Any], context: Mapping[str, Any]) -> dict[str, Any]:
    owner = fixture.get("owner_decision")
    if not isinstance(owner, dict):
        _fail("LSAEP-FAIL-003", "owner decision missing", "LSAEP-OP-003")
    required = [claim for claim in context["token_schema"]["required_claims"] if claim != "coordinate_receipt_sha256"]
    missing = [claim for claim in required if claim not in owner]
    if missing:
        _fail("LSAEP-FAIL-003", f"owner decision missing claims: {missing}", "LSAEP-OP-003")
    if owner.get("authorization_kind") != AUTHORIZATION_KIND:
        _fail("LSAEP-FAIL-003", "authorization kind mismatch", "LSAEP-OP-005")
    if owner.get("permitted_effect") != PERMITTED_EFFECT:
        _fail("LSAEP-FAIL-003", "permitted effect mismatch", "LSAEP-OP-005")
    prohibited = set(context["token_schema"]["prohibited_effects"])
    if set(owner.get("prohibited_effects", [])) != prohibited:
        _fail("LSAEP-FAIL-003", "prohibited effect set mismatch", "LSAEP-OP-005")
    for key in ("owner_identity", "owner_decision_id", "authorization_token_id", "nonce", "transaction_id"):
        value = owner.get(key)
        if not isinstance(value, str) or not _ID_RE.fullmatch(value):
            _fail("LSAEP-FAIL-003", f"invalid owner field: {key}", "LSAEP-OP-004")
    return owner


def _verify_baselines(fixture: Mapping[str, Any], owner: Mapping[str, Any]) -> None:
    for key in ("repository_head", "repository_tree", "remote_head"):
        value = fixture.get(key)
        if not isinstance(value, str) or not _GIT_SHA_RE.fullmatch(value):
            _fail("LSAEP-FAIL-004", f"invalid baseline syntax: {key}", "LSAEP-OP-006")
        if owner.get(key) != value:
            _fail("LSAEP-FAIL-004", f"owner baseline mismatch: {key}", "LSAEP-OP-006")
    if fixture["remote_head"] != fixture["repository_head"]:
        _fail("LSAEP-FAIL-004", "remote head differs from local head", "LSAEP-OP-007")


def _verify_executor(fixture: Mapping[str, Any], owner: Mapping[str, Any]) -> None:
    uid = fixture.get("executor_uid")
    if not isinstance(uid, int) or uid < 0 or owner.get("executor_uid") != uid:
        _fail("LSAEP-FAIL-005", "executor uid mismatch", "LSAEP-OP-008")


def _verify_time_window(fixture: Mapping[str, Any], owner: Mapping[str, Any]) -> None:
    issued = _parse_utc(owner["issued_at_utc"])
    not_before = _parse_utc(owner["not_before_utc"])
    expires = _parse_utc(owner["expires_at_utc"])
    current = _parse_utc(fixture["current_time_utc"])
    if not (not_before <= issued <= current <= expires):
        _fail("LSAEP-FAIL-006", "time ordering invalid", "LSAEP-OP-009")
    if (expires - issued).total_seconds() > 86400:
        _fail("LSAEP-FAIL-006", "validity exceeds 86400 seconds", "LSAEP-OP-009")


def _verify_revocation_and_replay(fixture: Mapping[str, Any], owner: Mapping[str, Any]) -> None:
    registry = fixture.get("revocation_registry")
    if not isinstance(registry, dict):
        _fail("LSAEP-FAIL-007", "revocation registry missing", "LSAEP-OP-010")
    if owner.get("revocation_epoch") != registry.get("current_revocation_epoch"):
        _fail("LSAEP-FAIL-007", "revocation epoch mismatch", "LSAEP-OP-010")
    tuple3 = [owner["authorization_token_id"], owner["nonce"], owner["transaction_id"]]
    if tuple3 in registry.get("consumed_tuples", []):
        _fail("LSAEP-FAIL-008", "anti-replay tuple consumed", "LSAEP-OP-011")


def _validate_path(path: str) -> None:
    if not isinstance(path, str) or not path.startswith(SYNTHETIC_PATH_PREFIX):
        _fail("LSAEP-FAIL-012", "path outside synthetic prefix", "LSAEP-OP-017")
    if not path.startswith("/") or posixpath.normpath(path) != path:
        _fail("LSAEP-FAIL-012", "path is not absolute canonical", "LSAEP-OP-017")
    pure = PurePosixPath(path)
    if any(part in (".", "..") for part in pure.parts):
        _fail("LSAEP-FAIL-012", "dot path component", "LSAEP-OP-018")
    if any(token in path for token in _FORBIDDEN_PATH_TOKENS):
        _fail("LSAEP-FAIL-012", "path expression syntax forbidden", "LSAEP-OP-018")


def _validate_coordinate_rows(fixture: Mapping[str, Any], context: Mapping[str, Any]) -> list[dict[str, Any]]:
    source = fixture.get("coordinate_source")
    if not isinstance(source, dict) or not isinstance(source.get("rows"), list):
        _fail("LSAEP-FAIL-009", "coordinate source missing", "LSAEP-OP-012")
    rows = copy.deepcopy(source["rows"])
    if len(rows) != EXPECTED_COUNTS["coordinate_rows"]:
        _fail("LSAEP-FAIL-009", "coordinate count is not 41", "LSAEP-OP-013")
    contracts = {row["contract_row_id"]: row for row in context["contract_rows"]}
    ids = [row.get("contract_row_id") for row in rows]
    if len(set(ids)) != len(ids) or set(ids) != set(contracts):
        _fail("LSAEP-FAIL-010", "coordinate row-id set mismatch", "LSAEP-OP-014")
    rows.sort(key=lambda row: int(contracts[row["contract_row_id"]]["sequence"]))
    seen_paths: set[str] = set()
    seen_path_digests: set[str] = set()
    required_fields = set(context["coordinate_schema"]["future_required_row_fields"])
    for row in rows:
        if set(row) != required_fields:
            _fail("LSAEP-FAIL-010", "coordinate row field set mismatch", "LSAEP-OP-014")
        contract = contracts[row["contract_row_id"]]
        exact = {
            "sequence": int(contract["sequence"]),
            "provider_object_id": contract["provider_object_id"],
            "expected_member_sha256": contract["expected_member_sha256"],
            "expected_member_size_bytes": int(contract["expected_member_size_bytes"]),
            "expected_soname": contract["expected_soname"],
        }
        for key, value in exact.items():
            if row.get(key) != value:
                _fail("LSAEP-FAIL-011", f"object binding mismatch: {row['contract_row_id']}:{key}", "LSAEP-OP-016")
        path = row.get("absolute_canonical_path")
        _validate_path(path)
        digest = row.get("path_text_sha256")
        if digest != sha256_bytes(path.encode("utf-8")):
            _fail("LSAEP-FAIL-016", "path-text digest mismatch", "LSAEP-OP-021")
        if path in seen_paths or digest in seen_path_digests:
            _fail("LSAEP-FAIL-013", "duplicate path or path digest", "LSAEP-OP-019")
        seen_paths.add(path)
        seen_path_digests.add(digest)
        if row.get("coordinate_authority_id") != "SYNTHETIC-COORDINATE-AUTHORITY-001" or row.get("coordinate_origin") != SYNTHETIC_MARKER:
            _fail("LSAEP-FAIL-014", "coordinate authority/origin mismatch", "LSAEP-OP-020")
    return rows


def _build_coordinate_receipt(fixture: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]) -> tuple[dict[str, Any], str]:
    source = fixture["coordinate_source"]
    envelope = {
        "schema_version": 1,
        "coordinate_receipt_id": source["coordinate_receipt_id"],
        "contract_acceptance_id": source["contract_acceptance_id"],
        "evidence_design_acceptance_id": source["evidence_design_acceptance_id"],
        "repository_head": source["repository_head"],
        "repository_tree": source["repository_tree"],
        "remote_head": source["remote_head"],
        "issuer_identity": source["issuer_identity"],
        "issued_at_utc": source["issued_at_utc"],
        "rows": list(rows),
    }
    digest = sha256_bytes(canonical_json_bytes(envelope))
    receipt = {**envelope, "receipt_sha256": digest}
    return receipt, digest


def _build_token_candidate(owner: Mapping[str, Any], coordinate_digest: str, context: Mapping[str, Any]) -> tuple[dict[str, Any], str]:
    token = {claim: owner[claim] for claim in context["token_schema"]["required_claims"] if claim != "coordinate_receipt_sha256"}
    token["coordinate_receipt_sha256"] = coordinate_digest
    if set(token) != set(context["token_schema"]["required_claims"]):
        _fail("LSAEP-FAIL-003", "token claim set mismatch", "LSAEP-OP-025")
    digest = sha256_bytes(canonical_json_bytes(token))
    return token, digest


def _verify_cross_bindings(fixture: Mapping[str, Any], owner: Mapping[str, Any], receipt: Mapping[str, Any], token: Mapping[str, Any]) -> None:
    keys = ("contract_acceptance_id", "evidence_design_acceptance_id", "repository_head", "repository_tree", "remote_head")
    for key in keys:
        if owner.get(key) != receipt.get(key) or token.get(key) != owner.get(key):
            _fail("LSAEP-FAIL-017", f"cross-binding mismatch: {key}", "LSAEP-OP-029")
    if token.get("executor_uid") != fixture.get("executor_uid") or token.get("transaction_id") != owner.get("transaction_id"):
        _fail("LSAEP-FAIL-017", "uid or transaction cross-binding mismatch", "LSAEP-OP-029")


def _verify_protected_state(fixture: Mapping[str, Any]) -> None:
    before = fixture.get("protected_before")
    after = fixture.get("protected_after")
    if not isinstance(before, dict) or before != after:
        _fail("LSAEP-FAIL-019", "protected-state invariance failed", "LSAEP-OP-034")


def _verify_output_scope(fixture: Mapping[str, Any], owner: Mapping[str, Any]) -> None:
    output = fixture.get("output_root")
    expected_prefix = f"/__synthetic__/termux-native-desktop/evidence-output/{owner['transaction_id']}"
    if output != expected_prefix:
        _fail("LSAEP-FAIL-018", "output root outside synthetic transaction scope", "LSAEP-OP-031")


def _assert_zero_live_authority(fixture: Mapping[str, Any]) -> None:
    keys = (
        "current_live_authority_count",
        "current_provider_read_count",
        "current_issued_token_count",
        "current_coordinate_receipt_count",
        "current_coordinate_row_count",
    )
    if any(fixture.get(key) != 0 for key in keys):
        _fail("LSAEP-FAIL-018", "live authority marker changed", "LSAEP-OP-032")


def _operation_trace(context: Mapping[str, Any], stop_operation: str | None = None) -> list[str]:
    result: list[str] = []
    for row in sorted(context["operations"], key=lambda item: int(item["sequence"])):
        result.append(row["step_id"])
        if row["step_id"] == stop_operation:
            break
    return result


def _state_trace(context: Mapping[str, Any], *, rejected: bool = False) -> list[str]:
    ordered = [row["state_id"] for row in sorted(context["states"], key=lambda item: int(item["sequence"]))]
    return [ordered[-1]] if rejected else ordered[:-1]


def _build_success_report(
    fixture: Mapping[str, Any],
    context: Mapping[str, Any],
    token: Mapping[str, Any],
    token_digest: str,
    receipt: Mapping[str, Any],
    coordinate_digest: str,
) -> dict[str, Any]:
    report_without_digest = {
        "schema_version": 1,
        "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "implementation_acceptance_gate": IMPLEMENTATION_ACCEPTANCE_GATE,
        "fixture_kind": SYNTHETIC_MARKER,
        "fixture_id": fixture["fixture_id"],
        "decision": SUCCESS_DECISION,
        "candidate_scope": "SYNTHETIC_ONLY_NOT_AUTHORITY",
        "inactive_state": INACTIVE_STATE,
        "pass": True,
        "accepted_design_acceptance_id": DESIGN_ACCEPTANCE_ID,
        "input_contract_count": EXPECTED_COUNTS["inputs"],
        "state_count": EXPECTED_COUNTS["states"],
        "operation_count": EXPECTED_COUNTS["operations"],
        "failure_contract_count": EXPECTED_COUNTS["failures"],
        "authorization_claim_count": len(token),
        "coordinate_row_count": len(receipt["rows"]),
        "coordinate_row_field_count": EXPECTED_COUNTS["coordinate_row_fields"],
        "validation_rule_count": EXPECTED_COUNTS["validation_rules"],
        "token_candidate_sha256": token_digest,
        "coordinate_receipt_candidate_sha256": coordinate_digest,
        "operation_trace": _operation_trace(context),
        "state_trace": _state_trace(context),
        "current_issued_token_count": 0,
        "current_coordinate_receipt_count": 0,
        "current_coordinate_row_count": 0,
        "current_provider_read_count": 0,
        "current_live_authority_count": 0,
        "owner_authorization_issuance_state": "NOT_AUTHORIZED",
        "coordinate_receipt_production_state": "NOT_AUTHORIZED",
        "evidence_transaction_execution_state": "NOT_AUTHORIZED",
        "runtime_mutation_state": "NOT_AUTHORIZED",
        "provider_paths_opened": [],
        "writes_performed": [],
    }
    return {**report_without_digest, "report_sha256": sha256_bytes(canonical_json_bytes(report_without_digest))}


def _build_failure_report(fixture: Mapping[str, Any], context: Mapping[str, Any], error: CandidateError) -> dict[str, Any]:
    report_without_digest = {
        "schema_version": 1,
        "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "implementation_acceptance_gate": IMPLEMENTATION_ACCEPTANCE_GATE,
        "fixture_kind": fixture.get("fixture_kind", "UNKNOWN"),
        "fixture_id": fixture.get("fixture_id", "UNKNOWN"),
        "decision": FAILURE_DECISION,
        "candidate_scope": "SYNTHETIC_ONLY_NOT_AUTHORITY",
        "pass": False,
        "failure_id": error.failure_id,
        "failure_code": error.code,
        "first_failure": str(error),
        "operation_trace": _operation_trace(context, error.operation),
        "state_trace": _state_trace(context, rejected=True),
        "current_issued_token_count": 0,
        "current_coordinate_receipt_count": 0,
        "current_coordinate_row_count": 0,
        "current_provider_read_count": 0,
        "current_live_authority_count": 0,
        "provider_paths_opened": [],
        "writes_performed": [],
    }
    return {**report_without_digest, "report_sha256": sha256_bytes(canonical_json_bytes(report_without_digest))}


def execute_synthetic_case(repo_root: Path, fixture: Mapping[str, Any], case_name: str = "success") -> dict[str, Any]:
    context = load_contract_context(repo_root)
    case_fixture = _mutate_fixture(fixture, case_name)
    try:
        _assert_synthetic_fixture(case_fixture)
        _verify_package_context(case_fixture)
        _verify_source_contracts(case_fixture)
        owner = _verify_owner_decision(case_fixture, context)
        _verify_baselines(case_fixture, owner)
        _verify_executor(case_fixture, owner)
        _verify_time_window(case_fixture, owner)
        _verify_revocation_and_replay(case_fixture, owner)
        rows = _validate_coordinate_rows(case_fixture, context)
        if case_fixture.get("synthetic_fault") == "SERIALIZATION":
            canonical_json_bytes({"not_serializable": {1, 2, 3}})
        receipt, coordinate_digest = _build_coordinate_receipt(case_fixture, rows)
        token, token_digest = _build_token_candidate(owner, coordinate_digest, context)
        _verify_cross_bindings(case_fixture, owner, receipt, token)
        _verify_output_scope(case_fixture, owner)
        _verify_protected_state(case_fixture)
        _assert_zero_live_authority(case_fixture)
        if case_fixture.get("synthetic_fault") == "RESULT_DELIVERY":
            _fail("LSAEP-FAIL-020", "synthetic result delivery fault", "LSAEP-OP-035")
        return _build_success_report(case_fixture, context, token, token_digest, receipt, coordinate_digest)
    except CandidateError as error:
        return _build_failure_report(case_fixture, context, error)


def build_coverage_rows(repo_root: Path) -> list[dict[str, str]]:
    context = load_contract_context(repo_root)
    rows: list[dict[str, str]] = []
    for row in context["inputs"]:
        rows.append(
            {
                "coverage_kind": "INPUT",
                "source_id": row["input_id"],
                "sequence": row["sequence"],
                "implementation_symbol": "load_contract_context" if int(row["sequence"]) <= 4 else "execute_synthetic_case",
                "enforcement_layer": "IMPLEMENTATION_CANDIDATE_SYNTHETIC_ONLY",
                "synthetic_case": "success",
                "current_state": "MAPPED_NOT_LIVE",
                "authority_effect": "ZERO_LIVE_AUTHORITY",
            }
        )
    for row in context["states"]:
        rows.append(
            {
                "coverage_kind": "STATE",
                "source_id": row["state_id"],
                "sequence": row["sequence"],
                "implementation_symbol": "_state_trace",
                "enforcement_layer": "IMPLEMENTATION_CANDIDATE_SYNTHETIC_ONLY",
                "synthetic_case": "success" if row["state_name"] != "REJECTED" else "all-negative-cases",
                "current_state": "MAPPED_NOT_LIVE",
                "authority_effect": "ZERO_LIVE_AUTHORITY",
            }
        )
    for row in context["operations"]:
        rows.append(
            {
                "coverage_kind": "OPERATION",
                "source_id": row["step_id"],
                "sequence": row["sequence"],
                "implementation_symbol": OPERATION_HANDLERS[row["phase"]],
                "enforcement_layer": "IMPLEMENTATION_CANDIDATE_SYNTHETIC_ONLY",
                "synthetic_case": "success",
                "current_state": "MAPPED_NOT_LIVE",
                "authority_effect": "ZERO_LIVE_AUTHORITY",
            }
        )
    failure_case_by_id = {row["failure_id"]: row["case"] for row in FAILURE_CASES}
    for row in context["failures"]:
        rows.append(
            {
                "coverage_kind": "FAILURE",
                "source_id": row["failure_id"],
                "sequence": row["sequence"],
                "implementation_symbol": "_build_failure_report",
                "enforcement_layer": "IMPLEMENTATION_CANDIDATE_SYNTHETIC_ONLY",
                "synthetic_case": failure_case_by_id[row["failure_id"]],
                "current_state": "MAPPED_NOT_LIVE",
                "authority_effect": "ZERO_LIVE_AUTHORITY",
            }
        )
    return rows


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Synthetic-only non-executing implementation candidate")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--case", default="success")
    args = parser.parse_args(argv)
    fixture_path = args.fixture.resolve()
    allowed_parent = (args.repo_root.resolve() / REVIEW_REL).resolve()
    try:
        fixture_path.relative_to(allowed_parent)
    except ValueError:
        parser.error("fixture must be repository-owned review evidence")
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    known_cases = {"success", *(row["case"] for row in FAILURE_CASES)}
    if args.case not in known_cases:
        parser.error("unknown synthetic case")
    report = execute_synthetic_case(args.repo_root, fixture, args.case)
    print(canonical_json_bytes(report).decode("utf-8"), end="")
    return 0 if report["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
