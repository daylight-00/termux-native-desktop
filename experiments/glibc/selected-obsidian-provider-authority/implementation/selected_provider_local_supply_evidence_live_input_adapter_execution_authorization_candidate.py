#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import posixpath
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

SYNTHETIC_MARKER = "SYNTHETIC_REPOSITORY_FIXTURE_ONLY"
SYNTHETIC_PATH_PREFIX = "/__synthetic__/termux-native-desktop/selected-provider/"
SYNTHETIC_INPUT_PREFIX = "/__synthetic__/termux-native-desktop/repository-inputs/"
IMPLEMENTATION_REVIEW_ID = (
    "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-"
    "EXECUTION-AUTHORIZATION-IMPLEMENTATION-REVIEW-001"
)
IMPLEMENTATION_ACCEPTANCE_GATE = (
    "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-"
    "EXECUTION-AUTHORIZATION-IMPLEMENTATION-ACCEPTANCE-OPEN"
)
CONTRACT_REVIEW_ID = (
    "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-"
    "EXECUTION-AUTHORIZATION-CONTRACT-REVIEW-001"
)
CONTRACT_ACCEPTANCE_ID = (
    "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-"
    "EXECUTION-AUTHORIZATION-CONTRACT-ACCEPT-001"
)
SOURCE_IMPLEMENTATION_ACCEPTANCE_ID = (
    "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-"
    "COORDINATE-PRODUCTION-IMPLEMENTATION-ACCEPT-001"
)
LOCAL_SUPPLY_MAP_CONTRACT_ACCEPTANCE_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-ACCEPT-001"
EVIDENCE_DESIGN_ACCEPTANCE_ID = (
    "SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-DESIGN-ACCEPT-001"
)
AUTHORIZATION_KIND = "READ_ONLY_LOCAL_SUPPLY_EVIDENCE_EXECUTION_ONLY"
OWNER_AUTHORIZATION_KIND = "READ_ONLY_LOCAL_SUPPLY_EVIDENCE_TRANSACTION_ONLY"
OWNER_PERMITTED_EFFECT = "READ_ONLY_PROVIDER_VALIDATION_AND_TRANSACTION_SCOPED_EVIDENCE_OUTPUTS_ONLY"
ADAPTER_STATE = "INACTIVE_SEPARATE_EXECUTION_AUTHORIZATION_REQUIRED"
SUCCESS_DECISION = "QUALIFIED_NON_EXECUTING_SYNTHETIC_LIVE_INPUT_ADAPTER_EXECUTION_AUTHORIZATION_IMPLEMENTATION_CANDIDATE"
FAILURE_DECISION = "REJECTED_SYNTHETIC_LIVE_INPUT_ADAPTER_EXECUTION_AUTHORIZATION_CASE_ZERO_LIVE_AUTHORITY"

BASE_REL = Path("experiments/glibc/selected-obsidian-provider-authority")
REVIEW_REL = BASE_REL / "review"
IMPLEMENTATION_REL = BASE_REL / "implementation"
FIXTURE_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-synthetic-fixture.json"

ADAPTER_NAME = "selected-provider-local-supply-evidence-live-input-adapter-contract.json"
EXEC_AUTH_NAME = "selected-provider-local-supply-evidence-execution-authorization-schema.json"
VALIDATION_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-validation-contract.tsv"
STATE_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-state-machine.tsv"
OPERATION_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-operation-contract.tsv"
FAILURE_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-failure-contract.tsv"
RECEIPT_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-receipt-contract.json"
CONTRACT_METADATA_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-metadata.tsv"
CONTRACT_ACCEPTANCE_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-boundary-acceptance.tsv"
TOKEN_SCHEMA_NAME = "selected-provider-local-supply-evidence-owner-authorization-token-schema.json"
COORDINATE_SCHEMA_NAME = "selected-provider-local-supply-evidence-coordinate-receipt-schema.json"
LOCAL_SUPPLY_CONTRACT_NAME = "selected-provider-local-supply-map-contract.tsv"
SOURCE_IMPLEMENTATION_NAME = "selected_provider_local_supply_evidence_authorization_issuance_coordinate_production_candidate.py"

REVIEW_DIGESTS = {
    ADAPTER_NAME: "2e80bcb77b97b5ecc52304a9ef3693b123cb13dc74a7bc9c94dc1be557e82213",
    EXEC_AUTH_NAME: "91cd60dbc10fd0d0d1e644011b1d5f4f06e903744e81982dc088264836757a20",
    VALIDATION_NAME: "408c213c941f8670129bf2e07da02ea06886895ee5c39e748d748b54e0993503",
    STATE_NAME: "6dcbc03906f755e836c7dd83f679b0202c6b219afcfa0afe5f254da88ed64d7b",
    OPERATION_NAME: "912786adf77ef9beeaec22f3208b742a79ae3edcb33730e1267148be86266a66",
    FAILURE_NAME: "a031e35872a8d2e0ad71e888a0040574bf6560b7b256ac5d7680cfb36c013e76",
    RECEIPT_NAME: "0acb6152d3afa1397841c453d8b2cc6a72f3cbbd05bead51ee02596aafadf55b",
    CONTRACT_METADATA_NAME: "ea0cfbed6e0d14a694cd1e0000acbbeecee156dd5e1923d551151c834506aa2e",
    CONTRACT_ACCEPTANCE_NAME: "2b5646bc1987b7ec01fac5c0a44cf5247b2e0850463db21956cbcac3b0547dac",
    TOKEN_SCHEMA_NAME: "27d11e8bb8de3238b49aef77757f0328a2269a156f55fdcbdddcf4dcb4fd411b",
    COORDINATE_SCHEMA_NAME: "b94c25994ecc26e402607b9e61c0cee796c74b15435bc168a18821def9096f83",
    LOCAL_SUPPLY_CONTRACT_NAME: "2223af964e74cc8bb221d13e559e49aaf03abe364985346cb1d8e43973c6640e",
}
SOURCE_IMPLEMENTATION_SHA256 = "039593be6144845b8be817bc45144be58c0f9a03bc60278a73748213d269df61"

EXPECTED_COUNTS = {
    "inputs": 10,
    "envelope_fields": 20,
    "authorization_claims": 27,
    "validations": 37,
    "states": 18,
    "operations": 32,
    "failures": 20,
    "coordinate_rows": 41,
    "coordinate_row_fields": 10,
    "coverage": 164,
}

FAILURE_CODES = {
    "LSLIAE-FAIL-001": "LSLIAE_SOURCE_MISMATCH",
    "LSLIAE-FAIL-002": "LSLIAE_SYNTHETIC_ORACLE_BOUNDARY",
    "LSLIAE-FAIL-003": "LSLIAE_INPUT_NOT_EXPLICIT",
    "LSLIAE-FAIL-004": "LSLIAE_ADAPTER_SCHEMA_MISMATCH",
    "LSLIAE-FAIL-005": "LSLIAE_OWNER_DIGEST_MISMATCH",
    "LSLIAE-FAIL-006": "LSLIAE_OWNER_TOKEN_BINDING",
    "LSLIAE-FAIL-007": "LSLIAE_TOKEN_COORDINATE_BINDING",
    "LSLIAE-FAIL-008": "LSLIAE_HEAD_MISMATCH",
    "LSLIAE-FAIL-009": "LSLIAE_EXECUTOR_MISMATCH",
    "LSLIAE-FAIL-010": "LSLIAE_TIME_INVALID",
    "LSLIAE-FAIL-011": "LSLIAE_REVOKED",
    "LSLIAE-FAIL-012": "LSLIAE_REPLAY",
    "LSLIAE-FAIL-013": "LSLIAE_ROW_COUNT",
    "LSLIAE-FAIL-014": "LSLIAE_OBJECT_BINDING",
    "LSLIAE-FAIL-015": "LSLIAE_PATH_INVALID",
    "LSLIAE-FAIL-016": "LSLIAE_SYNTHETIC_REWRITE",
    "LSLIAE-FAIL-017": "LSLIAE_EXEC_AUTH_SCHEMA",
    "LSLIAE-FAIL-018": "LSLIAE_RESOURCE_BUDGET",
    "LSLIAE-FAIL-019": "LSLIAE_PROTECTED_STATE",
    "LSLIAE-FAIL-020": "LSLIAE_RESULT_DELIVERY",
}

FAILURE_CASES = (
    {"failure_id": "LSLIAE-FAIL-001", "case": "package-invalid", "stop_operation": "LSLIAE-OP-001"},
    {"failure_id": "LSLIAE-FAIL-002", "case": "synthetic-boundary-invalid", "stop_operation": "LSLIAE-OP-002"},
    {"failure_id": "LSLIAE-FAIL-003", "case": "input-discovery-attempted", "stop_operation": "LSLIAE-OP-004"},
    {"failure_id": "LSLIAE-FAIL-004", "case": "input-document-missing", "stop_operation": "LSLIAE-OP-005"},
    {"failure_id": "LSLIAE-FAIL-005", "case": "owner-digest-mismatch", "stop_operation": "LSLIAE-OP-009"},
    {"failure_id": "LSLIAE-FAIL-006", "case": "owner-token-binding-mismatch", "stop_operation": "LSLIAE-OP-012"},
    {"failure_id": "LSLIAE-FAIL-007", "case": "token-coordinate-binding-mismatch", "stop_operation": "LSLIAE-OP-013"},
    {"failure_id": "LSLIAE-FAIL-008", "case": "baseline-mismatch", "stop_operation": "LSLIAE-OP-014"},
    {"failure_id": "LSLIAE-FAIL-009", "case": "executor-mismatch", "stop_operation": "LSLIAE-OP-014"},
    {"failure_id": "LSLIAE-FAIL-010", "case": "time-invalid", "stop_operation": "LSLIAE-OP-015"},
    {"failure_id": "LSLIAE-FAIL-011", "case": "revocation-mismatch", "stop_operation": "LSLIAE-OP-016"},
    {"failure_id": "LSLIAE-FAIL-012", "case": "replay-detected", "stop_operation": "LSLIAE-OP-016"},
    {"failure_id": "LSLIAE-FAIL-013", "case": "coordinate-cardinality-invalid", "stop_operation": "LSLIAE-OP-017"},
    {"failure_id": "LSLIAE-FAIL-014", "case": "coordinate-binding-invalid", "stop_operation": "LSLIAE-OP-018"},
    {"failure_id": "LSLIAE-FAIL-015", "case": "path-invalid", "stop_operation": "LSLIAE-OP-019"},
    {"failure_id": "LSLIAE-FAIL-016", "case": "synthetic-rewrite-detected", "stop_operation": "LSLIAE-OP-020"},
    {"failure_id": "LSLIAE-FAIL-017", "case": "execution-authorization-invalid", "stop_operation": "LSLIAE-OP-025"},
    {"failure_id": "LSLIAE-FAIL-018", "case": "resource-budget-invalid", "stop_operation": "LSLIAE-OP-026"},
    {"failure_id": "LSLIAE-FAIL-019", "case": "protected-state-changed", "stop_operation": "LSLIAE-OP-031"},
    {"failure_id": "LSLIAE-FAIL-020", "case": "result-delivery-failed", "stop_operation": "LSLIAE-OP-032"},
)

_FORBIDDEN_PATH_TOKENS = ("*", "?", "[", "]", "{", "}", "$", "`", "~", "\\", "$(", "${")
_GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_ID_RE = re.compile(r"^[A-Z0-9][A-Z0-9._:-]{3,159}$")


@dataclass(frozen=True)
class CandidateError(Exception):
    failure_id: str
    code: str
    message: str
    operation: str

    def __str__(self) -> str:
        return self.message


def _fail(failure_id: str, message: str, operation: str) -> None:
    raise CandidateError(failure_id, FAILURE_CODES[failure_id], message, operation)


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
    except (TypeError, ValueError) as exc:
        _fail("LSLIAE-FAIL-020", f"canonical serialization failed: {exc}", "LSLIAE-OP-032")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _parse_utc(value: Any, failure_id: str = "LSLIAE-FAIL-010", operation: str = "LSLIAE-OP-015") -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        _fail(failure_id, "UTC timestamp syntax invalid", operation)
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        _fail(failure_id, "UTC timestamp parse failed", operation)
    if parsed.tzinfo != timezone.utc:
        _fail(failure_id, "UTC timestamp offset invalid", operation)
    return parsed


def _canonical_digest_without(document: Mapping[str, Any], field: str) -> str:
    value = dict(document)
    value.pop(field, None)
    return sha256_bytes(canonical_json_bytes(value))


def _execution_replay_tuple(auth: Mapping[str, Any]) -> list[str]:
    return [
        str(auth["execution_authorization_id"]),
        str(auth["nonce"]),
        str(auth["transaction_id"]),
        str(auth["adapter_envelope_sha256"]),
        str(auth["coordinate_receipt_sha256"]),
    ]


def _owner_replay_tuple(token: Mapping[str, Any]) -> list[str]:
    return [
        str(token["authorization_token_id"]),
        str(token["nonce"]),
        str(token["transaction_id"]),
        str(token["coordinate_receipt_sha256"]),
    ]


def load_contract_context(repo_root: Path) -> dict[str, Any]:
    repo = repo_root.resolve()
    review = repo / REVIEW_REL
    for name, digest in REVIEW_DIGESTS.items():
        path = review / name
        if not path.is_file() or sha256_file(path) != digest:
            _fail("LSLIAE-FAIL-001", f"accepted source artifact mismatch: {name}", "LSLIAE-OP-001")
    source_implementation = repo / IMPLEMENTATION_REL / SOURCE_IMPLEMENTATION_NAME
    if not source_implementation.is_file() or sha256_file(source_implementation) != SOURCE_IMPLEMENTATION_SHA256:
        _fail("LSLIAE-FAIL-002", "accepted synthetic implementation digest mismatch", "LSLIAE-OP-002")

    adapter = json.loads((review / ADAPTER_NAME).read_text(encoding="utf-8"))
    execution_schema = json.loads((review / EXEC_AUTH_NAME).read_text(encoding="utf-8"))
    receipt_contract = json.loads((review / RECEIPT_NAME).read_text(encoding="utf-8"))
    token_schema = json.loads((review / TOKEN_SCHEMA_NAME).read_text(encoding="utf-8"))
    coordinate_schema = json.loads((review / COORDINATE_SCHEMA_NAME).read_text(encoding="utf-8"))
    validations = _read_tsv(review / VALIDATION_NAME)
    states = _read_tsv(review / STATE_NAME)
    operations = _read_tsv(review / OPERATION_NAME)
    failures = _read_tsv(review / FAILURE_NAME)
    contract_rows = _read_tsv(review / LOCAL_SUPPLY_CONTRACT_NAME)
    acceptance_rows = _read_tsv(review / CONTRACT_ACCEPTANCE_NAME)

    if len(acceptance_rows) != 1 or acceptance_rows[0].get("acceptance_id") != CONTRACT_ACCEPTANCE_ID:
        _fail("LSLIAE-FAIL-001", "contract acceptance identity mismatch", "LSLIAE-OP-001")
    if acceptance_rows[0].get("accepted_authority_state") != "ACCEPTED_BOUNDED_NON_EXECUTING_LIVE_INPUT_ADAPTER_EXECUTION_AUTHORIZATION_CONTRACT_AUTHORITY":
        _fail("LSLIAE-FAIL-001", "contract authority state mismatch", "LSLIAE-OP-001")
    if adapter.get("review_id") != CONTRACT_REVIEW_ID or adapter.get("accepted_synthetic_implementation", {}).get("role") != "IMMUTABLE_SEMANTIC_AND_REGRESSION_ORACLE_ONLY":
        _fail("LSLIAE-FAIL-002", "synthetic oracle role mismatch", "LSLIAE-OP-002")
    if adapter.get("accepted_synthetic_implementation", {}).get("live_input_invocation_authority") != "NONE":
        _fail("LSLIAE-FAIL-002", "synthetic oracle live invocation widened", "LSLIAE-OP-002")
    counts = {
        "inputs": len(adapter.get("future_explicit_input_channels", [])),
        "envelope_fields": len(adapter.get("future_required_envelope_fields", [])),
        "authorization_claims": len(execution_schema.get("required_claims", [])),
        "validations": len(validations),
        "states": len(states),
        "operations": len(operations),
        "failures": len(failures),
        "coordinate_rows": len(contract_rows),
        "coordinate_row_fields": len(coordinate_schema.get("future_required_row_fields", [])),
    }
    if any(counts[key] != EXPECTED_COUNTS[key] for key in counts):
        _fail("LSLIAE-FAIL-001", f"accepted contract cardinality mismatch: {counts}", "LSLIAE-OP-001")
    if execution_schema.get("required_exact_provider_path_count") != 41 or execution_schema.get("maximum_provider_bytes") != 29047112:
        _fail("LSLIAE-FAIL-001", "execution resource contract mismatch", "LSLIAE-OP-001")
    if execution_schema.get("maximum_result_receipt_bytes") != 1048576 or execution_schema.get("maximum_validity_seconds") != 3600:
        _fail("LSLIAE-FAIL-001", "execution receipt/time contract mismatch", "LSLIAE-OP-001")
    return {
        "adapter": adapter,
        "execution_schema": execution_schema,
        "receipt_contract": receipt_contract,
        "token_schema": token_schema,
        "coordinate_schema": coordinate_schema,
        "validations": validations,
        "states": states,
        "operations": operations,
        "failures": failures,
        "contract_rows": contract_rows,
    }


def _build_coordinate_rows(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for contract in sorted(context["contract_rows"], key=lambda row: int(row["sequence"])):
        path = f"{SYNTHETIC_PATH_PREFIX}{int(contract['sequence']):02d}-{contract['member_basename']}"
        rows.append(
            {
                "contract_row_id": contract["contract_row_id"],
                "sequence": int(contract["sequence"]),
                "provider_object_id": contract["provider_object_id"],
                "expected_member_sha256": contract["expected_member_sha256"],
                "expected_member_size_bytes": int(contract["expected_member_size_bytes"]),
                "expected_soname": contract["expected_soname"],
                "absolute_canonical_path": path,
                "coordinate_authority_id": "SYNTHETIC-COORDINATE-AUTHORITY-001",
                "coordinate_origin": "SYNTHETIC_REPOSITORY_FIXTURE_ORIGIN",
                "path_text_sha256": sha256_bytes(path.encode("utf-8")),
            }
        )
    return rows


def _refresh_auth_digest(auth: dict[str, Any]) -> None:
    auth["authorization_sha256"] = _canonical_digest_without(auth, "authorization_sha256")


def _refresh_envelope_chain(fixture: dict[str, Any]) -> None:
    envelope = fixture["adapter_envelope_document"]
    envelope["envelope_sha256"] = _canonical_digest_without(envelope, "envelope_sha256")
    auth = fixture["execution_authorization_document"]
    auth["adapter_envelope_sha256"] = envelope["envelope_sha256"]
    _refresh_auth_digest(auth)


def _refresh_token_chain(fixture: dict[str, Any]) -> None:
    token = fixture["input_documents"]["owner_authorization_token_document"]
    token_digest = sha256_bytes(canonical_json_bytes(token))
    fixture["input_byte_digests"]["owner_authorization_token_document"] = token_digest
    fixture["adapter_envelope_document"]["owner_authorization_token_sha256"] = token_digest
    fixture["execution_authorization_document"]["owner_authorization_token_sha256"] = token_digest
    _refresh_envelope_chain(fixture)


def _refresh_coordinate_chain(fixture: dict[str, Any], *, sync_token: bool = True) -> None:
    receipt = fixture["input_documents"]["canonical_41_row_coordinate_receipt_document"]
    receipt["receipt_sha256"] = _canonical_digest_without(receipt, "receipt_sha256")
    fixture["input_byte_digests"]["canonical_41_row_coordinate_receipt_document"] = sha256_bytes(canonical_json_bytes(receipt))
    token = fixture["input_documents"]["owner_authorization_token_document"]
    if sync_token:
        token["coordinate_receipt_sha256"] = receipt["receipt_sha256"]
    row_digests = [sha256_bytes(canonical_json_bytes(row)) for row in receipt["rows"]]
    envelope = fixture["adapter_envelope_document"]
    envelope["coordinate_receipt_sha256"] = receipt["receipt_sha256"]
    envelope["coordinate_row_count"] = len(receipt["rows"])
    envelope["coordinate_row_digest_manifest_sha256"] = sha256_bytes(canonical_json_bytes(row_digests))
    fixture["execution_authorization_document"]["coordinate_receipt_sha256"] = receipt["receipt_sha256"]
    _refresh_token_chain(fixture)


def _refresh_revocation_chain(fixture: dict[str, Any]) -> None:
    snapshot = fixture["input_documents"]["revocation_and_replay_snapshot"]
    snapshot_digest = sha256_bytes(canonical_json_bytes(snapshot))
    fixture["input_byte_digests"]["revocation_and_replay_snapshot"] = snapshot_digest
    envelope = fixture["adapter_envelope_document"]
    envelope["revocation_snapshot_sha256"] = snapshot_digest
    envelope["revocation_epoch"] = snapshot["current_revocation_epoch"]
    fixture["execution_authorization_document"]["revocation_epoch"] = snapshot["current_revocation_epoch"]
    _refresh_envelope_chain(fixture)


def build_synthetic_fixture(repo_root: Path) -> dict[str, Any]:
    context = load_contract_context(repo_root)
    head = "0123456789abcdef0123456789abcdef01234567"
    tree = "89abcdef0123456789abcdef0123456789abcdef"
    transaction_id = "SYNTHETIC-LSLIAE-TXN-001"
    executor_uid = 10555
    current_time = "2026-07-28T09:15:00Z"
    output_root = f"/__synthetic__/termux-native-desktop/evidence-output/{transaction_id}"

    owner_decision = {
        "schema_version": 1,
        "owner_identity": "SYNTHETIC-OWNER-001",
        "owner_decision_id": "SYNTHETIC-OWNER-DECISION-001",
        "authorization_kind": OWNER_AUTHORIZATION_KIND,
        "permitted_effect": OWNER_PERMITTED_EFFECT,
        "transaction_id": transaction_id,
        "repository_head": head,
        "repository_tree": tree,
        "remote_head": head,
        "executor_uid": executor_uid,
        "issued_at_utc": "2026-07-28T09:00:00Z",
        "not_before_utc": "2026-07-28T09:00:00Z",
        "expires_at_utc": "2026-07-28T10:00:00Z",
        "revocation_epoch": 7,
    }
    coordinate_receipt = {
        "schema_version": 1,
        "coordinate_receipt_id": "SYNTHETIC-COORDINATE-RECEIPT-001",
        "contract_acceptance_id": LOCAL_SUPPLY_MAP_CONTRACT_ACCEPTANCE_ID,
        "evidence_design_acceptance_id": EVIDENCE_DESIGN_ACCEPTANCE_ID,
        "repository_head": head,
        "repository_tree": tree,
        "remote_head": head,
        "issuer_identity": "SYNTHETIC-COORDINATE-ISSUER-001",
        "issued_at_utc": "2026-07-28T09:01:00Z",
        "rows": _build_coordinate_rows(context),
        "receipt_sha256": "",
    }
    coordinate_receipt["receipt_sha256"] = _canonical_digest_without(coordinate_receipt, "receipt_sha256")
    owner_token = {
        "schema_version": 1,
        "authorization_token_id": "SYNTHETIC-OWNER-TOKEN-001",
        "authorization_kind": OWNER_AUTHORIZATION_KIND,
        "owner_identity": owner_decision["owner_identity"],
        "owner_decision_id": owner_decision["owner_decision_id"],
        "issued_at_utc": "2026-07-28T09:02:00Z",
        "expires_at_utc": "2026-07-28T10:00:00Z",
        "not_before_utc": "2026-07-28T09:02:00Z",
        "nonce": "SYNTHETIC-OWNER-NONCE-001",
        "revocation_epoch": 7,
        "transaction_id": transaction_id,
        "contract_acceptance_id": LOCAL_SUPPLY_MAP_CONTRACT_ACCEPTANCE_ID,
        "evidence_design_acceptance_id": EVIDENCE_DESIGN_ACCEPTANCE_ID,
        "repository_head": head,
        "repository_tree": tree,
        "remote_head": head,
        "executor_uid": executor_uid,
        "coordinate_receipt_sha256": coordinate_receipt["receipt_sha256"],
    }
    revocation_snapshot = {
        "schema_version": 1,
        "snapshot_id": "SYNTHETIC-REVOCATION-SNAPSHOT-001",
        "captured_at_utc": current_time,
        "current_revocation_epoch": 7,
        "consumed_owner_token_replay_tuples": [],
        "consumed_execution_replay_tuples": [],
        "snapshot_state": "SYNTHETIC_IMMUTABLE_SNAPSHOT",
    }
    documents = {
        "owner_decision_document": owner_decision,
        "owner_authorization_token_document": owner_token,
        "canonical_41_row_coordinate_receipt_document": coordinate_receipt,
        "revocation_and_replay_snapshot": revocation_snapshot,
    }
    input_digests = {name: sha256_bytes(canonical_json_bytes(document)) for name, document in documents.items()}
    row_digests = [sha256_bytes(canonical_json_bytes(row)) for row in coordinate_receipt["rows"]]
    owner_replay_sha = sha256_bytes(canonical_json_bytes(_owner_replay_tuple(owner_token)))
    envelope = {
        "schema_version": 1,
        "adapter_contract_review_id": CONTRACT_REVIEW_ID,
        "adapter_envelope_id": "SYNTHETIC-ADAPTER-ENVELOPE-001",
        "transaction_id": transaction_id,
        "created_at_utc": current_time,
        "owner_decision_sha256": input_digests["owner_decision_document"],
        "owner_authorization_token_sha256": input_digests["owner_authorization_token_document"],
        "coordinate_receipt_sha256": coordinate_receipt["receipt_sha256"],
        "revocation_snapshot_sha256": input_digests["revocation_and_replay_snapshot"],
        "repository_head": head,
        "repository_tree": tree,
        "remote_head": head,
        "executor_uid": executor_uid,
        "revocation_epoch": 7,
        "coordinate_row_count": 41,
        "coordinate_row_digest_manifest_sha256": sha256_bytes(canonical_json_bytes(row_digests)),
        "replay_tuple_sha256": owner_replay_sha,
        "transaction_output_root": output_root,
        "adapter_state": ADAPTER_STATE,
        "envelope_sha256": "",
    }
    envelope["envelope_sha256"] = _canonical_digest_without(envelope, "envelope_sha256")
    execution_schema = context["execution_schema"]
    execution_auth = {
        "schema_version": 1,
        "execution_authorization_id": "SYNTHETIC-EXECUTION-AUTHORIZATION-001",
        "authorization_kind": AUTHORIZATION_KIND,
        "owner_identity": owner_decision["owner_identity"],
        "owner_decision_id": owner_decision["owner_decision_id"],
        "issued_at_utc": "2026-07-28T09:10:00Z",
        "not_before_utc": "2026-07-28T09:10:00Z",
        "expires_at_utc": "2026-07-28T09:40:00Z",
        "nonce": "SYNTHETIC-EXECUTION-NONCE-001",
        "revocation_epoch": 7,
        "transaction_id": transaction_id,
        "adapter_contract_acceptance_id": CONTRACT_ACCEPTANCE_ID,
        "adapter_envelope_sha256": envelope["envelope_sha256"],
        "implementation_acceptance_id": SOURCE_IMPLEMENTATION_ACCEPTANCE_ID,
        "local_supply_map_contract_acceptance_id": LOCAL_SUPPLY_MAP_CONTRACT_ACCEPTANCE_ID,
        "evidence_design_acceptance_id": EVIDENCE_DESIGN_ACCEPTANCE_ID,
        "repository_head": head,
        "repository_tree": tree,
        "remote_head": head,
        "executor_uid": executor_uid,
        "owner_authorization_token_sha256": input_digests["owner_authorization_token_document"],
        "coordinate_receipt_sha256": coordinate_receipt["receipt_sha256"],
        "exact_provider_path_count": 41,
        "maximum_provider_bytes": 29047112,
        "transaction_output_root": output_root,
        "permitted_effects": list(execution_schema["required_permitted_effects"]),
        "authorization_sha256": "",
    }
    _refresh_auth_digest(execution_auth)
    execution_tuple = _execution_replay_tuple(execution_auth)
    input_arguments: list[dict[str, Any]] = []
    values = {
        "owner_decision_document": f"{SYNTHETIC_INPUT_PREFIX}owner-decision.json",
        "owner_authorization_token_document": f"{SYNTHETIC_INPUT_PREFIX}owner-token.json",
        "canonical_41_row_coordinate_receipt_document": f"{SYNTHETIC_INPUT_PREFIX}coordinate-receipt.json",
        "revocation_and_replay_snapshot": f"{SYNTHETIC_INPUT_PREFIX}revocation-snapshot.json",
        "repository_head": head,
        "repository_tree": tree,
        "remote_head": head,
        "executor_uid": executor_uid,
        "current_time_utc": current_time,
        "transaction_output_root": output_root,
    }
    for channel in context["adapter"]["future_explicit_input_channels"]:
        input_arguments.append(
            {
                "input_id": channel["input_id"],
                "name": channel["name"],
                "delivery": channel["delivery"],
                "value": values[channel["name"]],
                "source_mode": "EXPLICIT_SYNTHETIC_LITERAL",
                "discovery_used": False,
            }
        )
    protected = {
        "package_database_sha256": "a" * 64,
        "live_glibc_prefix_metadata_sha256": "b" * 64,
    }
    fixture = {
        "schema_version": 1,
        "fixture_kind": SYNTHETIC_MARKER,
        "fixture_id": "SYNTHETIC-LSLIAE-IMPLEMENTATION-FIXTURE-001",
        "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "contract_acceptance_id": CONTRACT_ACCEPTANCE_ID,
        "source_contract_valid": True,
        "accepted_synthetic_implementation_sha256": SOURCE_IMPLEMENTATION_SHA256,
        "accepted_synthetic_implementation_role": "IMMUTABLE_SEMANTIC_AND_REGRESSION_ORACLE_ONLY_NOT_LIVE_EXECUTOR",
        "accepted_synthetic_cli_invoked": False,
        "live_to_synthetic_rewrite_detected": False,
        "explicit_input_arguments": input_arguments,
        "input_documents": documents,
        "input_byte_digests": input_digests,
        "adapter_envelope_document": envelope,
        "execution_authorization_document": execution_auth,
        "repository_head": head,
        "repository_tree": tree,
        "remote_head": head,
        "executor_uid": executor_uid,
        "current_time_utc": current_time,
        "transaction_output_root": output_root,
        "protected_before": protected,
        "protected_after": copy.deepcopy(protected),
        "authority_registry_before": {"consumed_execution_replay_tuples": []},
        "authority_registry_after": {"consumed_execution_replay_tuples": [execution_tuple]},
        "first_provider_open_attempted": False,
        "provider_paths_opened": [],
        "provider_bytes_read": 0,
        "writes_performed": [],
        "result_delivery_state": "SYNTHETIC_STDOUT_ONLY",
        "current_live_input_count": 0,
        "current_adapter_envelope_count": 0,
        "current_execution_authorization_count": 0,
        "current_provider_read_count": 0,
        "current_write_count": 0,
        "current_live_authority_count": 0,
    }
    return fixture


def build_negative_cases() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "fixture_kind": SYNTHETIC_MARKER,
        "case_count": len(FAILURE_CASES),
        "cases": [
            {
                **row,
                "failure_code": FAILURE_CODES[row["failure_id"]],
                "expected_provider_read_count": 0,
                "expected_write_count": 0,
                "expected_live_authority_count": 0,
            }
            for row in FAILURE_CASES
        ],
    }


def _mutate_fixture(base: Mapping[str, Any], case_name: str) -> dict[str, Any]:
    fixture = copy.deepcopy(base)
    if case_name == "success":
        return fixture
    if case_name == "package-invalid":
        fixture["fixture_kind"] = "LIVE_OR_EXTERNAL_INPUT"
    elif case_name == "synthetic-boundary-invalid":
        fixture["accepted_synthetic_cli_invoked"] = True
    elif case_name == "input-discovery-attempted":
        fixture["explicit_input_arguments"][0]["delivery"] = "SEARCH_BY_BASENAME"
        fixture["explicit_input_arguments"][0]["discovery_used"] = True
    elif case_name == "input-document-missing":
        del fixture["input_documents"]["owner_decision_document"]
    elif case_name == "owner-digest-mismatch":
        fixture["input_byte_digests"]["owner_decision_document"] = "0" * 64
    elif case_name == "owner-token-binding-mismatch":
        fixture["input_documents"]["owner_authorization_token_document"]["owner_identity"] = "SYNTHETIC-OTHER-OWNER-001"
        _refresh_token_chain(fixture)
    elif case_name == "token-coordinate-binding-mismatch":
        fixture["input_documents"]["owner_authorization_token_document"]["coordinate_receipt_sha256"] = "0" * 64
        _refresh_token_chain(fixture)
    elif case_name == "baseline-mismatch":
        fixture["repository_head"] = "f" * 40
    elif case_name == "executor-mismatch":
        fixture["executor_uid"] += 1
    elif case_name == "time-invalid":
        fixture["current_time_utc"] = "2026-07-28T11:00:00Z"
    elif case_name == "revocation-mismatch":
        fixture["input_documents"]["revocation_and_replay_snapshot"]["current_revocation_epoch"] = 8
        _refresh_revocation_chain(fixture)
    elif case_name == "replay-detected":
        token = fixture["input_documents"]["owner_authorization_token_document"]
        fixture["input_documents"]["revocation_and_replay_snapshot"]["consumed_owner_token_replay_tuples"].append(_owner_replay_tuple(token))
        _refresh_revocation_chain(fixture)
    elif case_name == "coordinate-cardinality-invalid":
        fixture["input_documents"]["canonical_41_row_coordinate_receipt_document"]["rows"].pop()
        _refresh_coordinate_chain(fixture)
    elif case_name == "coordinate-binding-invalid":
        fixture["input_documents"]["canonical_41_row_coordinate_receipt_document"]["rows"][0]["expected_soname"] = "libWrong.so.0"
        _refresh_coordinate_chain(fixture)
    elif case_name == "path-invalid":
        row = fixture["input_documents"]["canonical_41_row_coordinate_receipt_document"]["rows"][0]
        row["absolute_canonical_path"] = "relative/provider.so"
        row["path_text_sha256"] = sha256_bytes(row["absolute_canonical_path"].encode("utf-8"))
        _refresh_coordinate_chain(fixture)
    elif case_name == "synthetic-rewrite-detected":
        fixture["live_to_synthetic_rewrite_detected"] = True
    elif case_name == "execution-authorization-invalid":
        del fixture["execution_authorization_document"]["authorization_kind"]
        _refresh_auth_digest(fixture["execution_authorization_document"])
    elif case_name == "resource-budget-invalid":
        fixture["execution_authorization_document"]["maximum_provider_bytes"] = 29047113
        _refresh_auth_digest(fixture["execution_authorization_document"])
    elif case_name == "protected-state-changed":
        fixture["protected_after"]["package_database_sha256"] = "c" * 64
    elif case_name == "result-delivery-failed":
        fixture["result_delivery_state"] = "FAILED"
    else:
        raise ValueError(f"unknown synthetic case: {case_name}")
    return fixture


def _verify_package_and_boundary(fixture: Mapping[str, Any]) -> None:
    if fixture.get("fixture_kind") != SYNTHETIC_MARKER or fixture.get("implementation_review_id") != IMPLEMENTATION_REVIEW_ID:
        _fail("LSLIAE-FAIL-001", "fixture package identity invalid", "LSLIAE-OP-001")
    if fixture.get("source_contract_valid") is not True:
        _fail("LSLIAE-FAIL-001", "source contract marker invalid", "LSLIAE-OP-001")
    if fixture.get("accepted_synthetic_implementation_sha256") != SOURCE_IMPLEMENTATION_SHA256:
        _fail("LSLIAE-FAIL-002", "synthetic oracle digest marker invalid", "LSLIAE-OP-002")
    if fixture.get("accepted_synthetic_implementation_role") != "IMMUTABLE_SEMANTIC_AND_REGRESSION_ORACLE_ONLY_NOT_LIVE_EXECUTOR":
        _fail("LSLIAE-FAIL-002", "synthetic oracle role marker invalid", "LSLIAE-OP-002")
    if fixture.get("accepted_synthetic_cli_invoked") is not False:
        _fail("LSLIAE-FAIL-002", "accepted synthetic CLI invocation forbidden", "LSLIAE-OP-002")
    zero_keys = (
        "current_live_input_count",
        "current_adapter_envelope_count",
        "current_execution_authorization_count",
        "current_provider_read_count",
        "current_write_count",
        "current_live_authority_count",
    )
    if any(fixture.get(key) != 0 for key in zero_keys):
        _fail("LSLIAE-FAIL-002", "current live state is nonzero", "LSLIAE-OP-003")


def _verify_explicit_inputs(fixture: Mapping[str, Any], context: Mapping[str, Any]) -> None:
    supplied = fixture.get("explicit_input_arguments")
    expected = context["adapter"]["future_explicit_input_channels"]
    if not isinstance(supplied, list) or len(supplied) != EXPECTED_COUNTS["inputs"]:
        _fail("LSLIAE-FAIL-003", "explicit input cardinality invalid", "LSLIAE-OP-004")
    by_id = {row.get("input_id"): row for row in supplied if isinstance(row, dict)}
    if len(by_id) != EXPECTED_COUNTS["inputs"]:
        _fail("LSLIAE-FAIL-003", "explicit input ids duplicate or absent", "LSLIAE-OP-004")
    for channel in expected:
        row = by_id.get(channel["input_id"])
        if row is None or row.get("name") != channel["name"] or row.get("delivery") != channel["delivery"]:
            _fail("LSLIAE-FAIL-003", f"input channel mismatch: {channel['input_id']}", "LSLIAE-OP-004")
        if row.get("source_mode") != "EXPLICIT_SYNTHETIC_LITERAL" or row.get("discovery_used") is not False:
            _fail("LSLIAE-FAIL-003", "search or inference input mode forbidden", "LSLIAE-OP-004")
        value = row.get("value")
        if channel["delivery"].startswith("EXACT_PATH") and (not isinstance(value, str) or not value.startswith(SYNTHETIC_INPUT_PREFIX)):
            _fail("LSLIAE-FAIL-003", "synthetic document path argument invalid", "LSLIAE-OP-004")


def _load_documents(fixture: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    documents = fixture.get("input_documents")
    names = (
        "owner_decision_document",
        "owner_authorization_token_document",
        "canonical_41_row_coordinate_receipt_document",
        "revocation_and_replay_snapshot",
    )
    if not isinstance(documents, dict) or any(not isinstance(documents.get(name), dict) for name in names):
        _fail("LSLIAE-FAIL-004", "required synthetic input document missing or malformed", "LSLIAE-OP-005")
    return tuple(documents[name] for name in names)  # type: ignore[return-value]


def _verify_input_digests(fixture: Mapping[str, Any], documents: Sequence[Mapping[str, Any]]) -> None:
    names = (
        "owner_decision_document",
        "owner_authorization_token_document",
        "canonical_41_row_coordinate_receipt_document",
        "revocation_and_replay_snapshot",
    )
    digests = fixture.get("input_byte_digests")
    if not isinstance(digests, dict):
        _fail("LSLIAE-FAIL-005", "input digest manifest missing", "LSLIAE-OP-009")
    for index, (name, document) in enumerate(zip(names, documents), start=9):
        actual = sha256_bytes(canonical_json_bytes(document))
        if digests.get(name) != actual:
            _fail("LSLIAE-FAIL-005", f"input digest mismatch: {name}", f"LSLIAE-OP-{index:03d}")
    receipt = documents[2]
    if receipt.get("receipt_sha256") != _canonical_digest_without(receipt, "receipt_sha256"):
        _fail("LSLIAE-FAIL-005", "coordinate receipt canonical digest mismatch", "LSLIAE-OP-011")


def _verify_owner_token_binding(owner: Mapping[str, Any], token: Mapping[str, Any], context: Mapping[str, Any]) -> None:
    if set(token) != set(context["token_schema"]["required_claims"]):
        _fail("LSLIAE-FAIL-006", "owner token claim set mismatch", "LSLIAE-OP-012")
    if owner.get("authorization_kind") != OWNER_AUTHORIZATION_KIND or owner.get("permitted_effect") != OWNER_PERMITTED_EFFECT:
        _fail("LSLIAE-FAIL-006", "owner decision effect mismatch", "LSLIAE-OP-012")
    for key in ("owner_identity", "owner_decision_id", "transaction_id", "repository_head", "repository_tree", "remote_head", "executor_uid", "revocation_epoch"):
        if token.get(key) != owner.get(key):
            _fail("LSLIAE-FAIL-006", f"owner-token binding mismatch: {key}", "LSLIAE-OP-012")
    if token.get("authorization_kind") != OWNER_AUTHORIZATION_KIND:
        _fail("LSLIAE-FAIL-006", "owner token kind mismatch", "LSLIAE-OP-012")
    for key in ("owner_identity", "owner_decision_id", "authorization_token_id", "nonce", "transaction_id"):
        if not isinstance(token.get(key), str) or not _ID_RE.fullmatch(str(token[key])):
            _fail("LSLIAE-FAIL-006", f"owner token id syntax invalid: {key}", "LSLIAE-OP-012")


def _verify_token_coordinate_binding(token: Mapping[str, Any], receipt: Mapping[str, Any]) -> None:
    if token.get("coordinate_receipt_sha256") != receipt.get("receipt_sha256"):
        _fail("LSLIAE-FAIL-007", "token-coordinate digest binding mismatch", "LSLIAE-OP-013")


def _verify_baseline_executor_time(fixture: Mapping[str, Any], owner: Mapping[str, Any], token: Mapping[str, Any], receipt: Mapping[str, Any]) -> None:
    for key in ("repository_head", "repository_tree", "remote_head"):
        value = fixture.get(key)
        if not isinstance(value, str) or not _GIT_SHA_RE.fullmatch(value):
            _fail("LSLIAE-FAIL-008", f"baseline syntax invalid: {key}", "LSLIAE-OP-014")
        if owner.get(key) != value or token.get(key) != value or receipt.get(key) != value:
            _fail("LSLIAE-FAIL-008", f"baseline binding mismatch: {key}", "LSLIAE-OP-014")
    if fixture.get("remote_head") != fixture.get("repository_head"):
        _fail("LSLIAE-FAIL-008", "remote head differs from repository head", "LSLIAE-OP-014")
    uid = fixture.get("executor_uid")
    if not isinstance(uid, int) or uid < 0 or owner.get("executor_uid") != uid or token.get("executor_uid") != uid:
        _fail("LSLIAE-FAIL-009", "executor uid mismatch", "LSLIAE-OP-014")
    current = _parse_utc(fixture.get("current_time_utc"))
    for document in (owner, token):
        issued = _parse_utc(document.get("issued_at_utc"))
        not_before = _parse_utc(document.get("not_before_utc"))
        expires = _parse_utc(document.get("expires_at_utc"))
        if not (not_before <= issued <= current <= expires):
            _fail("LSLIAE-FAIL-010", "owner or token time window inactive", "LSLIAE-OP-015")


def _verify_revocation_replay(token: Mapping[str, Any], snapshot: Mapping[str, Any]) -> None:
    if token.get("revocation_epoch") != snapshot.get("current_revocation_epoch"):
        _fail("LSLIAE-FAIL-011", "owner token revocation epoch mismatch", "LSLIAE-OP-016")
    consumed = snapshot.get("consumed_owner_token_replay_tuples")
    if not isinstance(consumed, list) or _owner_replay_tuple(token) in consumed:
        _fail("LSLIAE-FAIL-012", "owner token replay tuple already consumed", "LSLIAE-OP-016")


def _validate_path(path: Any) -> None:
    if not isinstance(path, str) or not path.startswith(SYNTHETIC_PATH_PREFIX):
        _fail("LSLIAE-FAIL-015", "path outside direct synthetic fixture prefix", "LSLIAE-OP-019")
    if not path.startswith("/") or posixpath.normpath(path) != path:
        _fail("LSLIAE-FAIL-015", "path is not absolute canonical text", "LSLIAE-OP-019")
    if any(part in (".", "..") for part in PurePosixPath(path).parts) or any(token in path for token in _FORBIDDEN_PATH_TOKENS):
        _fail("LSLIAE-FAIL-015", "path expression syntax forbidden", "LSLIAE-OP-019")


def _verify_coordinates(receipt: Mapping[str, Any], context: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = receipt.get("rows")
    if not isinstance(rows, list) or len(rows) != EXPECTED_COUNTS["coordinate_rows"]:
        _fail("LSLIAE-FAIL-013", "coordinate receipt row count is not 41", "LSLIAE-OP-017")
    required_fields = set(context["coordinate_schema"]["future_required_row_fields"])
    contracts = {row["contract_row_id"]: row for row in context["contract_rows"]}
    ids = [row.get("contract_row_id") for row in rows if isinstance(row, dict)]
    if len(ids) != 41 or len(set(ids)) != 41 or set(ids) != set(contracts):
        _fail("LSLIAE-FAIL-014", "coordinate row identity set mismatch", "LSLIAE-OP-018")
    seen_objects: set[str] = set()
    seen_paths: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != required_fields:
            _fail("LSLIAE-FAIL-013", "coordinate row field count mismatch", "LSLIAE-OP-017")
        contract = contracts[row["contract_row_id"]]
        exact = {
            "sequence": int(contract["sequence"]),
            "provider_object_id": contract["provider_object_id"],
            "expected_member_sha256": contract["expected_member_sha256"],
            "expected_member_size_bytes": int(contract["expected_member_size_bytes"]),
            "expected_soname": contract["expected_soname"],
        }
        if any(row.get(key) != value for key, value in exact.items()):
            _fail("LSLIAE-FAIL-014", f"coordinate object binding mismatch: {row['contract_row_id']}", "LSLIAE-OP-018")
        if row["provider_object_id"] in seen_objects:
            _fail("LSLIAE-FAIL-014", "provider object duplicated", "LSLIAE-OP-018")
        seen_objects.add(row["provider_object_id"])
        _validate_path(row.get("absolute_canonical_path"))
        path = row["absolute_canonical_path"]
        if row.get("path_text_sha256") != sha256_bytes(path.encode("utf-8")) or path in seen_paths:
            _fail("LSLIAE-FAIL-015", "path digest mismatch or duplicate", "LSLIAE-OP-019")
        seen_paths.add(path)
        if row.get("coordinate_origin") != "SYNTHETIC_REPOSITORY_FIXTURE_ORIGIN" or row.get("coordinate_authority_id") != "SYNTHETIC-COORDINATE-AUTHORITY-001":
            _fail("LSLIAE-FAIL-016", "coordinate origin is not direct synthetic fixture origin", "LSLIAE-OP-020")
    return sorted(rows, key=lambda row: int(row["sequence"]))


def _verify_no_rewrite_or_synthetic_invocation(fixture: Mapping[str, Any]) -> None:
    if fixture.get("live_to_synthetic_rewrite_detected") is not False or fixture.get("accepted_synthetic_cli_invoked") is not False:
        _fail("LSLIAE-FAIL-016", "live-to-synthetic rewriting or synthetic CLI invocation detected", "LSLIAE-OP-020")


def _verify_envelope(fixture: Mapping[str, Any], context: Mapping[str, Any], owner: Mapping[str, Any], token: Mapping[str, Any], receipt: Mapping[str, Any], snapshot: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    envelope = fixture.get("adapter_envelope_document")
    if not isinstance(envelope, dict) or set(envelope) != set(context["adapter"]["future_required_envelope_fields"]):
        _fail("LSLIAE-FAIL-004", "adapter envelope field set mismatch", "LSLIAE-OP-021")
    input_digests = fixture["input_byte_digests"]
    row_digests = [sha256_bytes(canonical_json_bytes(row)) for row in rows]
    expected = {
        "schema_version": 1,
        "adapter_contract_review_id": CONTRACT_REVIEW_ID,
        "transaction_id": owner["transaction_id"],
        "owner_decision_sha256": input_digests["owner_decision_document"],
        "owner_authorization_token_sha256": input_digests["owner_authorization_token_document"],
        "coordinate_receipt_sha256": receipt["receipt_sha256"],
        "revocation_snapshot_sha256": input_digests["revocation_and_replay_snapshot"],
        "repository_head": fixture["repository_head"],
        "repository_tree": fixture["repository_tree"],
        "remote_head": fixture["remote_head"],
        "executor_uid": fixture["executor_uid"],
        "revocation_epoch": snapshot["current_revocation_epoch"],
        "coordinate_row_count": 41,
        "coordinate_row_digest_manifest_sha256": sha256_bytes(canonical_json_bytes(row_digests)),
        "replay_tuple_sha256": sha256_bytes(canonical_json_bytes(_owner_replay_tuple(token))),
        "transaction_output_root": fixture["transaction_output_root"],
        "adapter_state": ADAPTER_STATE,
    }
    if any(envelope.get(key) != value for key, value in expected.items()):
        _fail("LSLIAE-FAIL-004", "adapter envelope binding mismatch", "LSLIAE-OP-021")
    if envelope.get("envelope_sha256") != _canonical_digest_without(envelope, "envelope_sha256"):
        _fail("LSLIAE-FAIL-005", "adapter envelope digest mismatch", "LSLIAE-OP-022")
    if envelope.get("adapter_state") != ADAPTER_STATE or fixture.get("first_provider_open_attempted") is not False:
        _fail("LSLIAE-FAIL-018", "adapter stage is active or provider gate opened", "LSLIAE-OP-023")
    return envelope


def _verify_execution_authorization(fixture: Mapping[str, Any], context: Mapping[str, Any], owner: Mapping[str, Any], token: Mapping[str, Any], receipt: Mapping[str, Any], snapshot: Mapping[str, Any], envelope: Mapping[str, Any]) -> dict[str, Any]:
    auth = fixture.get("execution_authorization_document")
    schema = context["execution_schema"]
    if not isinstance(auth, dict) or set(auth) != set(schema["required_claims"]):
        _fail("LSLIAE-FAIL-017", "execution authorization claim set mismatch", "LSLIAE-OP-024")
    if auth.get("authorization_sha256") != _canonical_digest_without(auth, "authorization_sha256"):
        _fail("LSLIAE-FAIL-017", "execution authorization digest mismatch", "LSLIAE-OP-025")
    expected = {
        "schema_version": 1,
        "authorization_kind": AUTHORIZATION_KIND,
        "owner_identity": owner["owner_identity"],
        "owner_decision_id": owner["owner_decision_id"],
        "revocation_epoch": snapshot["current_revocation_epoch"],
        "transaction_id": owner["transaction_id"],
        "adapter_contract_acceptance_id": CONTRACT_ACCEPTANCE_ID,
        "adapter_envelope_sha256": envelope["envelope_sha256"],
        "implementation_acceptance_id": SOURCE_IMPLEMENTATION_ACCEPTANCE_ID,
        "local_supply_map_contract_acceptance_id": LOCAL_SUPPLY_MAP_CONTRACT_ACCEPTANCE_ID,
        "evidence_design_acceptance_id": EVIDENCE_DESIGN_ACCEPTANCE_ID,
        "repository_head": fixture["repository_head"],
        "repository_tree": fixture["repository_tree"],
        "remote_head": fixture["remote_head"],
        "executor_uid": fixture["executor_uid"],
        "owner_authorization_token_sha256": fixture["input_byte_digests"]["owner_authorization_token_document"],
        "coordinate_receipt_sha256": receipt["receipt_sha256"],
    }
    if any(auth.get(key) != value for key, value in expected.items()):
        _fail("LSLIAE-FAIL-017", "execution authorization binding mismatch", "LSLIAE-OP-025")
    if set(auth.get("permitted_effects", [])) != set(schema["required_permitted_effects"]):
        _fail("LSLIAE-FAIL-018", "execution effect allowlist mismatch", "LSLIAE-OP-026")
    if auth.get("maximum_provider_bytes") != schema["maximum_provider_bytes"] or auth.get("exact_provider_path_count") != 41:
        _fail("LSLIAE-FAIL-018", "execution resource budget mismatch", "LSLIAE-OP-026")
    output = auth.get("transaction_output_root")
    if output != fixture.get("transaction_output_root") or not isinstance(output, str) or not output.startswith("/__synthetic__/termux-native-desktop/evidence-output/"):
        _fail("LSLIAE-FAIL-018", "transaction output scope mismatch", "LSLIAE-OP-026")
    issued = _parse_utc(auth.get("issued_at_utc"), "LSLIAE-FAIL-017", "LSLIAE-OP-027")
    not_before = _parse_utc(auth.get("not_before_utc"), "LSLIAE-FAIL-017", "LSLIAE-OP-027")
    expires = _parse_utc(auth.get("expires_at_utc"), "LSLIAE-FAIL-017", "LSLIAE-OP-027")
    current = _parse_utc(fixture.get("current_time_utc"), "LSLIAE-FAIL-017", "LSLIAE-OP-027")
    if not (not_before <= issued <= current <= expires) or (expires - issued).total_seconds() > 3600:
        _fail("LSLIAE-FAIL-017", "execution authorization time window invalid", "LSLIAE-OP-027")
    consumed = snapshot.get("consumed_execution_replay_tuples")
    replay_tuple = _execution_replay_tuple(auth)
    if not isinstance(consumed, list) or replay_tuple in consumed:
        _fail("LSLIAE-FAIL-012", "execution replay tuple already consumed", "LSLIAE-OP-027")
    before = fixture.get("authority_registry_before")
    after = fixture.get("authority_registry_after")
    if before != {"consumed_execution_replay_tuples": []} or after != {"consumed_execution_replay_tuples": [replay_tuple]}:
        _fail("LSLIAE-FAIL-017", "synthetic replay consumption delta invalid", "LSLIAE-OP-028")
    return auth


def _verify_protected_and_delegate(fixture: Mapping[str, Any]) -> dict[str, Any]:
    before = fixture.get("protected_before")
    after = fixture.get("protected_after")
    if not isinstance(before, dict) or before != after:
        _fail("LSLIAE-FAIL-019", "protected package database or glibc state changed", "LSLIAE-OP-031")
    if fixture.get("first_provider_open_attempted") is not False:
        _fail("LSLIAE-FAIL-018", "first provider open gate widened", "LSLIAE-OP-030")
    if fixture.get("provider_paths_opened") != [] or fixture.get("provider_bytes_read") != 0 or fixture.get("writes_performed") != []:
        _fail("LSLIAE-FAIL-019", "synthetic delegate performed provider read or write", "LSLIAE-OP-030")
    return {
        "delegation_state": "NOT_EXECUTED_SEPARATE_READ_ONLY_EVIDENCE_IMPLEMENTATION_ACCEPTANCE_REQUIRED",
        "provider_paths_opened": [],
        "provider_bytes_read": 0,
        "writes_performed": [],
    }


def _operation_trace(context: Mapping[str, Any], stop_operation: str | None = None) -> list[str]:
    trace: list[str] = []
    for row in sorted(context["operations"], key=lambda item: int(item["sequence"])):
        trace.append(row["operation_id"])
        if row["operation_id"] == stop_operation:
            break
    return trace


def _state_trace(context: Mapping[str, Any], rejected: bool = False) -> list[str]:
    states = [row["state_id"] for row in sorted(context["states"], key=lambda item: int(item["sequence"]))]
    return [states[-1]] if rejected else states[:-1]


def _build_success_report(fixture: Mapping[str, Any], context: Mapping[str, Any], envelope: Mapping[str, Any], auth: Mapping[str, Any], delegate: Mapping[str, Any]) -> dict[str, Any]:
    report = {
        "schema_version": 1,
        "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "implementation_acceptance_gate": IMPLEMENTATION_ACCEPTANCE_GATE,
        "fixture_kind": SYNTHETIC_MARKER,
        "fixture_id": fixture["fixture_id"],
        "decision": SUCCESS_DECISION,
        "pass": True,
        "contract_acceptance_id": CONTRACT_ACCEPTANCE_ID,
        "coverage_count": EXPECTED_COUNTS["coverage"],
        "explicit_input_count": EXPECTED_COUNTS["inputs"],
        "adapter_envelope_field_count": EXPECTED_COUNTS["envelope_fields"],
        "execution_authorization_claim_count": EXPECTED_COUNTS["authorization_claims"],
        "validation_rule_count": EXPECTED_COUNTS["validations"],
        "state_count": EXPECTED_COUNTS["states"],
        "operation_count": EXPECTED_COUNTS["operations"],
        "failure_contract_count": EXPECTED_COUNTS["failures"],
        "coordinate_row_count": EXPECTED_COUNTS["coordinate_rows"],
        "coordinate_row_field_count": EXPECTED_COUNTS["coordinate_row_fields"],
        "adapter_envelope_sha256": envelope["envelope_sha256"],
        "execution_authorization_sha256": auth["authorization_sha256"],
        "operation_trace": _operation_trace(context),
        "state_trace": _state_trace(context),
        "synthetic_replay_tuple_consumption_validated": True,
        "synthetic_replay_registry_write_performed": False,
        "accepted_synthetic_cli_invoked": False,
        "live_to_synthetic_rewrite_performed": False,
        "delegate": dict(delegate),
        "current_live_input_count": 0,
        "current_adapter_envelope_count": 0,
        "current_execution_authorization_count": 0,
        "current_provider_read_count": 0,
        "current_write_count": 0,
        "current_live_authority_count": 0,
        "provider_paths_opened": [],
        "provider_bytes_read": 0,
        "writes_performed": [],
    }
    return {**report, "report_sha256": sha256_bytes(canonical_json_bytes(report))}


def _build_failure_report(fixture: Mapping[str, Any], context: Mapping[str, Any], error: CandidateError) -> dict[str, Any]:
    report = {
        "schema_version": 1,
        "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "implementation_acceptance_gate": IMPLEMENTATION_ACCEPTANCE_GATE,
        "fixture_kind": fixture.get("fixture_kind", "UNKNOWN"),
        "fixture_id": fixture.get("fixture_id", "UNKNOWN"),
        "decision": FAILURE_DECISION,
        "pass": False,
        "failure_id": error.failure_id,
        "failure_code": error.code,
        "first_failure": error.message,
        "operation_trace": _operation_trace(context, error.operation),
        "state_trace": _state_trace(context, rejected=True),
        "current_live_input_count": 0,
        "current_adapter_envelope_count": 0,
        "current_execution_authorization_count": 0,
        "current_provider_read_count": 0,
        "current_write_count": 0,
        "current_live_authority_count": 0,
        "provider_paths_opened": [],
        "provider_bytes_read": 0,
        "writes_performed": [],
    }
    return {**report, "report_sha256": sha256_bytes(canonical_json_bytes(report))}


def execute_synthetic_case(repo_root: Path, fixture: Mapping[str, Any], case_name: str = "success") -> dict[str, Any]:
    context = load_contract_context(repo_root)
    case_fixture = _mutate_fixture(fixture, case_name)
    try:
        _verify_package_and_boundary(case_fixture)
        _verify_explicit_inputs(case_fixture, context)
        owner, token, receipt, snapshot = _load_documents(case_fixture)
        _verify_input_digests(case_fixture, (owner, token, receipt, snapshot))
        _verify_owner_token_binding(owner, token, context)
        _verify_token_coordinate_binding(token, receipt)
        _verify_baseline_executor_time(case_fixture, owner, token, receipt)
        _verify_revocation_replay(token, snapshot)
        rows = _verify_coordinates(receipt, context)
        _verify_no_rewrite_or_synthetic_invocation(case_fixture)
        envelope = _verify_envelope(case_fixture, context, owner, token, receipt, snapshot, rows)
        auth = _verify_execution_authorization(case_fixture, context, owner, token, receipt, snapshot, envelope)
        delegate = _verify_protected_and_delegate(case_fixture)
        if case_fixture.get("result_delivery_state") != "SYNTHETIC_STDOUT_ONLY":
            _fail("LSLIAE-FAIL-020", "synthetic result delivery failed", "LSLIAE-OP-032")
        return _build_success_report(case_fixture, context, envelope, auth, delegate)
    except CandidateError as error:
        return _build_failure_report(case_fixture, context, error)


def build_coverage_rows(repo_root: Path) -> list[dict[str, str]]:
    context = load_contract_context(repo_root)
    rows: list[dict[str, str]] = []

    def add(kind: str, source_id: str, sequence: Any, symbol: str, synthetic_case: str) -> None:
        rows.append(
            {
                "coverage_kind": kind,
                "source_id": source_id,
                "sequence": str(sequence),
                "implementation_symbol": symbol,
                "enforcement_layer": "IMPLEMENTATION_CANDIDATE_SYNTHETIC_ONLY",
                "synthetic_case": synthetic_case,
                "current_state": "MAPPED_SYNTHETIC_NOT_LIVE",
                "authority_effect": "ZERO_LIVE_INPUTS_ZERO_PROVIDER_READS_ZERO_WRITES_ZERO_LIVE_AUTHORITY",
            }
        )

    for channel in context["adapter"]["future_explicit_input_channels"]:
        add("INPUT", channel["input_id"], int(channel["input_id"].rsplit("-", 1)[1]), "_verify_explicit_inputs", "success")
    for index, field in enumerate(context["adapter"]["future_required_envelope_fields"], start=1):
        add("ENVELOPE_FIELD", f"LIA-ENV-{index:03d}:{field}", index, "_verify_envelope", "success")
    for index, claim in enumerate(context["execution_schema"]["required_claims"], start=1):
        add("AUTHORIZATION_CLAIM", f"LIA-AUTH-{index:03d}:{claim}", index, "_verify_execution_authorization", "success")
    for row in context["validations"]:
        add("VALIDATION", row["validation_id"], row["sequence"], "execute_synthetic_case", "success")
    for row in context["states"]:
        add("STATE", row["state_id"], row["sequence"], "_state_trace", "all-negative-cases" if row["state_name"] == "REJECTED" else "success")
    for row in context["operations"]:
        add("OPERATION", row["operation_id"], row["sequence"], "_operation_trace", "success")
    failure_cases = {row["failure_id"]: row["case"] for row in FAILURE_CASES}
    for row in context["failures"]:
        add("FAILURE", row["failure_id"], row["sequence"], "_build_failure_report", failure_cases[row["failure_id"]])
    if len(rows) != EXPECTED_COUNTS["coverage"]:
        raise RuntimeError(f"coverage cardinality mismatch: {len(rows)}")
    return rows


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Repository-owned synthetic-only live-input adapter/execution-authorization implementation candidate")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--case", default="success")
    args = parser.parse_args(argv)
    expected_fixture = (args.repo_root.resolve() / REVIEW_REL / FIXTURE_NAME).resolve()
    if args.fixture.resolve() != expected_fixture:
        parser.error("fixture must be the exact repository-owned synthetic implementation fixture")
    known_cases = {"success", *(row["case"] for row in FAILURE_CASES)}
    if args.case not in known_cases:
        parser.error("unknown synthetic case")
    fixture = json.loads(expected_fixture.read_text(encoding="utf-8"))
    report = execute_synthetic_case(args.repo_root, fixture, args.case)
    print(canonical_json_bytes(report).decode("utf-8"), end="")
    return 0 if report["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
