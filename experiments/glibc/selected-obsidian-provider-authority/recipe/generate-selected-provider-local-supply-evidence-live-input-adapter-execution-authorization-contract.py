#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

BASE = Path("experiments/glibc/selected-obsidian-provider-authority")
REVIEW = BASE / "review"

REVIEW_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-CONTRACT-REVIEW-001"
ACCEPTANCE_GATE = "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-CONTRACT-ACCEPTANCE-OPEN"
CANDIDATE_STATE = "QUALIFIED_NON_EXECUTING_LIVE_INPUT_ADAPTER_EXECUTION_AUTHORIZATION_CONTRACT_CANDIDATE"

IMPLEMENTATION_ACCEPTANCE_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-IMPLEMENTATION-ACCEPT-001"
IMPLEMENTATION_REVIEW_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-IMPLEMENTATION-REVIEW-001"
IMPLEMENTATION_SHA256 = "039593be6144845b8be817bc45144be58c0f9a03bc60278a73748213d269df61"
CONTRACT_ACCEPTANCE_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-COORDINATE-CONTRACT-ACCEPT-001"
LOCAL_MAP_CONTRACT_ACCEPTANCE_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-ACCEPT-001"
EVIDENCE_DESIGN_ACCEPTANCE_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-DESIGN-ACCEPT-001"
ISSUANCE_DESIGN_ACCEPTANCE_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-DESIGN-ACCEPT-001"

SOURCE_DIGESTS = {
    "selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-boundary-acceptance.tsv": "5b3628f2612e0e3ee51001cb80b3c43a76262fd182b500e31b32abb6f7b8bb69",
    "selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-boundary-acceptance.tsv": "bf8d2377effb02db5e89c1b388b92f1ab5c9a908df51dc310d0d7eafba270d05",
    "selected-provider-local-supply-evidence-authorization-coordinate-contract-boundary-acceptance.tsv": "460a0e5133600a58467b5e736005700d835499476b4e19de147bd08d0507df8c",
    "selected-provider-local-supply-map-contract-boundary-acceptance.tsv": "5401f46120d147394932d0004a2a37c761fc6471acaeabd730b90f1e5d859cd1",
    "selected-provider-local-supply-map-evidence-transaction-design-boundary-acceptance.tsv": "1f60ec5983807d3f0f7527b11db953bf446eed39e1e526df21ad2f6a2812f8dd",
}

ADAPTER_NAME = "selected-provider-local-supply-evidence-live-input-adapter-contract.json"
EXECUTION_NAME = "selected-provider-local-supply-evidence-execution-authorization-schema.json"
VALIDATION_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-validation-contract.tsv"
STATE_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-state-machine.tsv"
OPERATION_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-operation-contract.tsv"
FAILURE_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-failure-contract.tsv"
RECEIPT_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-receipt-contract.json"
METADATA_NAME = "selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-metadata.tsv"

PROHIBITED = (
    "CONTRACT_REVIEW_DOES_NOT_SUPPLY_OR_ACCEPT_LIVE_INPUTS_ISSUE_OR_ACTIVATE_TOKENS_"
    "PRODUCE_COORDINATES_INVOKE_THE_SYNTHETIC_IMPLEMENTATION_WITH_LIVE_INPUT_REWRITE_LIVE_PATHS_"
    "SEARCH_OPEN_OR_READ_PROVIDER_BYTES_EXECUTE_EVIDENCE_COLLECTION_CREATE_RUNTIME_STATE_"
    "POPULATE_MATERIALIZE_PUBLISH_DEPLOY_OR_ACTIVATE"
)
AUTHORITY_EFFECT = "FUTURE_INTERFACE_RULE_ONLY_ZERO_CURRENT_LIVE_INPUTS_PROVIDER_READS_WRITES_OR_AUTHORITY"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(path: Path, values: dict[str, Any]) -> None:
    write_tsv(path, ["key", "value"], [{"key": key, "value": str(value)} for key, value in values.items()])


def adapter_contract() -> dict[str, Any]:
    input_channels = [
        {"input_id": "LIA-IN-001", "name": "owner_decision_document", "delivery": "EXACT_PATH_ARGUMENT_NO_SEARCH", "read_scope": "INPUT_DOCUMENT_BYTES_ONLY"},
        {"input_id": "LIA-IN-002", "name": "owner_authorization_token_document", "delivery": "EXACT_PATH_ARGUMENT_NO_SEARCH", "read_scope": "INPUT_DOCUMENT_BYTES_ONLY"},
        {"input_id": "LIA-IN-003", "name": "canonical_41_row_coordinate_receipt_document", "delivery": "EXACT_PATH_ARGUMENT_NO_SEARCH", "read_scope": "INPUT_DOCUMENT_BYTES_ONLY"},
        {"input_id": "LIA-IN-004", "name": "revocation_and_replay_snapshot", "delivery": "EXACT_PATH_ARGUMENT_NO_SEARCH", "read_scope": "AUTHORITY_METADATA_ONLY"},
        {"input_id": "LIA-IN-005", "name": "repository_head", "delivery": "EXPLICIT_VALUE_ARGUMENT", "read_scope": "NONE"},
        {"input_id": "LIA-IN-006", "name": "repository_tree", "delivery": "EXPLICIT_VALUE_ARGUMENT", "read_scope": "NONE"},
        {"input_id": "LIA-IN-007", "name": "remote_head", "delivery": "EXPLICIT_VALUE_ARGUMENT", "read_scope": "NONE"},
        {"input_id": "LIA-IN-008", "name": "executor_uid", "delivery": "EXPLICIT_NUMERIC_ARGUMENT", "read_scope": "NONE"},
        {"input_id": "LIA-IN-009", "name": "current_time_utc", "delivery": "EXPLICIT_CLOCK_SNAPSHOT", "read_scope": "CLOCK_ONLY"},
        {"input_id": "LIA-IN-010", "name": "transaction_output_root", "delivery": "EXPLICIT_ABSOLUTE_PATH_ARGUMENT", "read_scope": "NONE"},
    ]
    envelope_fields = [
        "schema_version",
        "adapter_contract_review_id",
        "adapter_envelope_id",
        "transaction_id",
        "created_at_utc",
        "owner_decision_sha256",
        "owner_authorization_token_sha256",
        "coordinate_receipt_sha256",
        "revocation_snapshot_sha256",
        "repository_head",
        "repository_tree",
        "remote_head",
        "executor_uid",
        "revocation_epoch",
        "coordinate_row_count",
        "coordinate_row_digest_manifest_sha256",
        "replay_tuple_sha256",
        "transaction_output_root",
        "adapter_state",
        "envelope_sha256",
    ]
    return {
        "schema_version": 1,
        "review_id": REVIEW_ID,
        "acceptance_gate": ACCEPTANCE_GATE,
        "candidate_state": CANDIDATE_STATE,
        "current_live_input_count": 0,
        "current_adapter_envelope_count": 0,
        "current_execution_authorization_count": 0,
        "current_provider_read_count": 0,
        "current_write_count": 0,
        "current_live_authority_count": 0,
        "accepted_synthetic_implementation": {
            "implementation_acceptance_id": IMPLEMENTATION_ACCEPTANCE_ID,
            "implementation_review_id": IMPLEMENTATION_REVIEW_ID,
            "implementation_sha256": IMPLEMENTATION_SHA256,
            "role": "IMMUTABLE_SEMANTIC_AND_REGRESSION_ORACLE_ONLY",
            "live_input_invocation_authority": "NONE",
            "live_path_rewrite_to_synthetic_namespace": "FORBIDDEN",
            "mutation": "FORBIDDEN_NEW_CLASS_D_IMPLEMENTATION_REVIEW_REQUIRED",
        },
        "future_explicit_input_channel_count": len(input_channels),
        "future_explicit_input_channels": input_channels,
        "future_required_envelope_field_count": len(envelope_fields),
        "future_required_envelope_fields": envelope_fields,
        "future_adapter_state": "INACTIVE_DIGEST_BOUND_ENVELOPE_ONLY",
        "future_adapter_implementation_authority": "NONE_SEPARATE_IMPLEMENTATION_REVIEW_AND_ACCEPTANCE_REQUIRED",
        "coordinate_binding": {
            "required_row_count": 41,
            "required_row_field_count": 10,
            "required_unique_contract_row_count": 41,
            "rule": "EXACT_ACCEPTED_OBJECT_DIGEST_SIZE_SONAME_PATH_TEXT_AND_ROW_ID_BINDING",
            "provider_path_open": "FORBIDDEN_DURING_ADAPTER_VALIDATION",
            "discovery": "FORBIDDEN_NO_GLOB_SEARCH_ENVIRONMENT_INFERENCE_BASENAME_FALLBACK_OR_ARCHIVE_LOOKUP",
        },
        "digest_rules": {
            "input_documents": "SHA256_OF_EXACT_INPUT_BYTES",
            "envelope": "SHA256_OF_CANONICAL_DOCUMENT_WITH_ENVELOPE_SHA256_OMITTED",
            "cross_binding": "OWNER_TOKEN_COORDINATE_REVOCATION_BASELINE_EXECUTOR_TRANSACTION_AND_OUTPUT_ROOT_ALL_BOUND",
        },
        "staging_rule": "LOGICAL_INACTIVE_ENVELOPE_ONLY_NO_CURRENT_STAGING_AND_NO_PROVIDER_BYTES",
        "serialization": "canonical compact UTF-8 JSON sort_keys separators comma-colon newline terminated",
        "prohibited_inference": PROHIBITED,
    }


def execution_schema() -> dict[str, Any]:
    required_claims = [
        "schema_version",
        "execution_authorization_id",
        "authorization_kind",
        "owner_identity",
        "owner_decision_id",
        "issued_at_utc",
        "not_before_utc",
        "expires_at_utc",
        "nonce",
        "revocation_epoch",
        "transaction_id",
        "adapter_contract_acceptance_id",
        "adapter_envelope_sha256",
        "implementation_acceptance_id",
        "local_supply_map_contract_acceptance_id",
        "evidence_design_acceptance_id",
        "repository_head",
        "repository_tree",
        "remote_head",
        "executor_uid",
        "owner_authorization_token_sha256",
        "coordinate_receipt_sha256",
        "exact_provider_path_count",
        "maximum_provider_bytes",
        "transaction_output_root",
        "permitted_effects",
        "authorization_sha256",
    ]
    permitted_effects = [
        "OPEN_EXACT_41_EXPLICIT_PROVIDER_PATHS_NOFOLLOW",
        "READ_HASH_FSTAT_AND_ELF_SONAME_VALIDATE_EXACT_PROVIDER_BYTES",
        "WRITE_TRANSACTION_SCOPED_EVIDENCE_LOGS_RECEIPTS_INDEX_AND_ARCHIVE_ONLY",
        "DELEGATE_TO_SEPARATELY_ACCEPTED_READ_ONLY_LOCAL_SUPPLY_EVIDENCE_IMPLEMENTATION_ONLY",
    ]
    prohibited_effects = [
        "PATH_DISCOVERY_OR_INFERENCE",
        "NETWORK_OR_PACKAGE_MANAGER_ACCESS",
        "ARCHIVE_OR_PACKAGE_EXTRACTION",
        "PROVIDER_FILE_MUTATION",
        "PACKAGE_DATABASE_MUTATION",
        "LIVE_GLIBC_PREFIX_MUTATION",
        "LOCAL_SUPPLY_MAP_ACCEPTANCE",
        "GENERATION_ROOT_OR_OBJECT_STORE_CREATION",
        "TARGET_POPULATION",
        "MATERIALIZATION",
        "PUBLICATION",
        "DEPLOYMENT",
        "ACTIVATION",
    ]
    return {
        "schema_version": 1,
        "review_id": REVIEW_ID,
        "acceptance_gate": ACCEPTANCE_GATE,
        "candidate_state": "SCHEMA_QUALIFIED_NOT_ISSUED_NOT_ACTIVE",
        "current_authorization": None,
        "current_authorization_count": 0,
        "current_consumed_replay_tuple_count": 0,
        "current_provider_read_count": 0,
        "current_write_count": 0,
        "current_live_authority_count": 0,
        "required_authorization_kind": "READ_ONLY_LOCAL_SUPPLY_EVIDENCE_EXECUTION_ONLY",
        "required_claim_count": len(required_claims),
        "required_claims": required_claims,
        "maximum_validity_seconds": 3600,
        "clock_skew_tolerance_seconds": 0,
        "required_exact_provider_path_count": 41,
        "maximum_provider_bytes": 29047112,
        "maximum_result_receipt_bytes": 1048576,
        "required_permitted_effects": permitted_effects,
        "prohibited_effects": prohibited_effects,
        "binding_rules": {
            "adapter_contract_acceptance_id": "FUTURE_EXACT_ACCEPTANCE_ID",
            "adapter_envelope": "EXACT_CANONICAL_SHA256",
            "implementation_acceptance_id": IMPLEMENTATION_ACCEPTANCE_ID,
            "local_supply_map_contract_acceptance_id": LOCAL_MAP_CONTRACT_ACCEPTANCE_ID,
            "evidence_design_acceptance_id": EVIDENCE_DESIGN_ACCEPTANCE_ID,
            "owner_authorization_token": "EXACT_CANONICAL_SHA256",
            "coordinate_receipt": "EXACT_CANONICAL_SHA256",
            "repository_identity": "EXACT_HEAD_AND_TREE",
            "remote_identity": "EXACT_HEAD_EQUALS_LOCAL_HEAD",
            "executor_identity": "EXACT_NUMERIC_UID",
            "revocation": "REVOCATION_EPOCH_MUST_EQUAL_CURRENT_OWNER_AUTHORITY_EPOCH",
            "replay": "AUTHORIZATION_ID_NONCE_TRANSACTION_ID_ADAPTER_ENVELOPE_AND_COORDINATE_RECEIPT_TUPLE_UNIQUE",
            "first_provider_open": "ONLY_AFTER_ALL_VALIDATIONS_AND_ATOMIC_REPLAY_TUPLE_CONSUMPTION",
        },
        "protected_state_rule": "PACKAGE_DATABASES_AND_LIVE_GLIBC_PREFIX_IDENTICAL_BEFORE_AND_AFTER;AUTHORITY_REGISTRY_CHANGE_LIMITED_TO_ONE_EXPECTED_CONSUMED_TUPLE",
        "authorization_digest_rule": "SHA256_OF_CANONICAL_DOCUMENT_WITH_AUTHORIZATION_SHA256_OMITTED",
        "serialization": "canonical compact UTF-8 JSON sort_keys separators comma-colon newline terminated",
        "prohibited_inference": PROHIBITED,
    }


def validation_rows() -> list[dict[str, str]]:
    specs = [
        ("SOURCE", "accepted source artifacts", "all source ids and SHA-256 values exact", "LSLIAE_SOURCE_MISMATCH"),
        ("ADAPTER_SCHEMA", "adapter contract", "schema version review id and acceptance gate exact", "LSLIAE_ADAPTER_SCHEMA_MISMATCH"),
        ("SYNTHETIC_ORACLE", "accepted synthetic implementation", "exact implementation digest and oracle-only role; no live invocation", "LSLIAE_SYNTHETIC_ORACLE_BOUNDARY"),
        ("EXPLICIT_INPUT", "input delivery", "only ten exact value or path arguments; no search discovery inference or fallback", "LSLIAE_INPUT_NOT_EXPLICIT"),
        ("OWNER_DIGEST", "owner decision", "canonical owner decision digest exact", "LSLIAE_OWNER_DIGEST_MISMATCH"),
        ("TOKEN_DIGEST", "owner authorization token", "canonical token digest exact", "LSLIAE_TOKEN_DIGEST_MISMATCH"),
        ("COORDINATE_DIGEST", "coordinate receipt", "canonical coordinate receipt digest exact", "LSLIAE_COORDINATE_DIGEST_MISMATCH"),
        ("REVOCATION_DIGEST", "revocation snapshot", "immutable snapshot digest exact", "LSLIAE_REVOCATION_SNAPSHOT_MISMATCH"),
        ("OWNER_TOKEN_BINDING", "owner decision and token", "owner identity decision id transaction baseline executor and effect exact", "LSLIAE_OWNER_TOKEN_BINDING"),
        ("TOKEN_COORDINATE_BINDING", "token and coordinate receipt", "token coordinate_receipt_sha256 equals exact canonical receipt digest", "LSLIAE_TOKEN_COORDINATE_BINDING"),
        ("BASELINE_HEAD", "repository HEAD", "exact forty lowercase hex and all documents agree", "LSLIAE_HEAD_MISMATCH"),
        ("BASELINE_TREE", "repository tree", "exact forty lowercase hex and all documents agree", "LSLIAE_TREE_MISMATCH"),
        ("REMOTE_HEAD", "remote HEAD", "exactly equals repository HEAD and all bound documents", "LSLIAE_REMOTE_MISMATCH"),
        ("EXECUTOR", "executor uid", "exact nonnegative numeric uid and all documents agree", "LSLIAE_EXECUTOR_MISMATCH"),
        ("TIME", "time windows", "UTC ordered active and validity within contract maximum", "LSLIAE_TIME_INVALID"),
        ("REVOCATION", "revocation epoch", "token envelope and execution authorization equal current epoch", "LSLIAE_REVOKED"),
        ("REPLAY", "replay tuple", "token and execution replay tuples absent from consumed registry", "LSLIAE_REPLAY"),
        ("ROW_COUNT", "coordinate rows", "exactly forty-one rows", "LSLIAE_ROW_COUNT"),
        ("ROW_FIELD_COUNT", "coordinate row fields", "each row has exact ten required fields", "LSLIAE_ROW_FIELD_COUNT"),
        ("ROW_IDENTITY", "contract row ids", "exact accepted set LSM-CONTRACT-001 through 041 once each", "LSLIAE_ROW_IDENTITY"),
        ("OBJECT_UNIQUENESS", "provider object ids", "exactly forty-one unique provider object ids", "LSLIAE_OBJECT_DUPLICATE"),
        ("PATH_CANONICAL", "absolute provider paths", "absolute canonical UTF-8 no dotdot no empty component", "LSLIAE_PATH_INVALID"),
        ("PATH_EXPRESSION", "provider paths", "no glob variable tilde command substitution or search expression", "LSLIAE_PATH_EXPRESSION"),
        ("PATH_DIGEST", "path text digest", "SHA-256 equals exact UTF-8 path text", "LSLIAE_PATH_DIGEST"),
        ("OBJECT_BINDING", "selected object identity", "row digest size SONAME sequence and object id match accepted contract", "LSLIAE_OBJECT_BINDING"),
        ("NO_SYNTHETIC_REWRITE", "live coordinate presentation", "never rewrite a live path or origin into synthetic namespace or invoke synthetic CLI", "LSLIAE_SYNTHETIC_REWRITE"),
        ("ENVELOPE_FIELDS", "adapter envelope", "exact twenty required fields and no unbound extension fields", "LSLIAE_ENVELOPE_FIELDS"),
        ("ENVELOPE_DIGEST", "adapter envelope", "canonical digest with envelope_sha256 omitted exact", "LSLIAE_ENVELOPE_DIGEST"),
        ("INACTIVE_STAGE", "adapter result", "state is inactive digest-bound envelope and provider reads remain zero", "LSLIAE_STAGE_ACTIVE"),
        ("EXEC_AUTH_SCHEMA", "execution authorization", "exact twenty-seven claims authorization kind and canonical digest", "LSLIAE_EXEC_AUTH_SCHEMA"),
        ("EXEC_AUTH_BINDING", "execution authorization bindings", "envelope token coordinate contracts baseline executor transaction and owner exact", "LSLIAE_EXEC_AUTH_BINDING"),
        ("EXEC_AUTH_EFFECT", "permitted effects", "exact four-item allowlist and all prohibited effects absent", "LSLIAE_EXEC_AUTH_EFFECT"),
        ("RESOURCE_BUDGET", "execution resource limits", "forty-one paths no more than 29047112 provider bytes and 1MiB receipt", "LSLIAE_RESOURCE_BUDGET"),
        ("OUTPUT_SCOPE", "transaction output root", "exact transaction-scoped absolute root outside provider generation package database and live glibc roots", "LSLIAE_OUTPUT_SCOPE"),
        ("FIRST_OPEN_GATE", "first provider open", "all validation passes and replay tuple atomically consumed before open", "LSLIAE_FIRST_OPEN_GATE"),
        ("PROTECTED_STATE", "protected state", "package databases and live glibc prefix identical; registry delta exactly one consumed tuple", "LSLIAE_PROTECTED_STATE"),
        ("ZERO_CURRENT", "candidate current state", "zero live inputs envelopes execution authorizations provider reads writes and live authority", "LSLIAE_CURRENT_LIVE_STATE"),
    ]
    rows: list[dict[str, str]] = []
    for i, (category, subject, rule, failure) in enumerate(specs, 1):
        rows.append({
            "validation_id": f"LSLIAE-VAL-{i:03d}",
            "sequence": str(i),
            "category": category,
            "subject": subject,
            "required_rule": rule,
            "failure_code": failure,
            "current_state": "CONTRACT_DEFINED_NOT_RUN",
            "authority_effect": AUTHORITY_EFFECT,
            "prohibited_inference": PROHIBITED,
        })
    return rows


def state_rows() -> list[dict[str, str]]:
    specs = [
        ("CONTRACT_LOADED", "accepted source digests verified", "explicit input arguments only", "INPUTS_PRESENT"),
        ("INPUTS_PRESENT", "owner token coordinate revocation baseline executor time and output inputs present", "parse bounded documents only", "SOURCE_VALIDATED"),
        ("SOURCE_VALIDATED", "schemas ids counts and source digests exact", "cross-binding validation only", "OWNER_TOKEN_BOUND"),
        ("OWNER_TOKEN_BOUND", "owner decision and token exact", "coordinate digest validation only", "COORDINATE_BOUND"),
        ("COORDINATE_BOUND", "token binds exact canonical 41-row receipt", "baseline validation only", "BASELINE_VERIFIED"),
        ("BASELINE_VERIFIED", "HEAD tree and remote exact", "executor and time validation only", "EXECUTOR_TIME_VERIFIED"),
        ("EXECUTOR_TIME_VERIFIED", "uid and active time windows exact", "revocation and replay validation only", "REVOCATION_REPLAY_VERIFIED"),
        ("REVOCATION_REPLAY_VERIFIED", "current epoch and unused token tuple", "coordinate text validation only", "COORDINATES_VERIFIED"),
        ("COORDINATES_VERIFIED", "41 exact rows validated without opening paths", "canonical envelope serialization only", "ENVELOPE_SERIALIZED"),
        ("ENVELOPE_SERIALIZED", "twenty fields and digest exact", "inactive logical staging only", "ADAPTER_INACTIVE"),
        ("ADAPTER_INACTIVE", "digest-bound envelope exists as future candidate only", "execution authorization validation only", "EXECUTION_AUTHORIZATION_VERIFIED"),
        ("EXECUTION_AUTHORIZATION_VERIFIED", "27 claims bindings effects limits time epoch and replay exact", "atomic replay consumption only", "AUTHORIZATION_CONSUMED"),
        ("AUTHORIZATION_CONSUMED", "one exact execution tuple consumed", "protected pre-snapshot only", "PROTECTED_BEFORE"),
        ("PROTECTED_BEFORE", "package database and live glibc metadata snapshotted", "first provider-open gate may open", "EVIDENCE_DELEGATED"),
        ("EVIDENCE_DELEGATED", "separately accepted read-only evidence implementation completed", "protected post-snapshot only", "PROTECTED_AFTER"),
        ("PROTECTED_AFTER", "protected state and registry delta verified", "result binding and receipt only", "RESULT_BOUND"),
        ("RESULT_BOUND", "result binds execution authorization envelope and evidence receipt", "archive/index delivery only", "COMPLETE"),
        ("REJECTED", "any failure before or during future transaction", "close descriptors emit bounded failure receipt zero accepted map", "TERMINAL"),
    ]
    rows=[]
    for i, (name, entry, effect, success) in enumerate(specs, 1):
        rows.append({
            "state_id": f"LSLIAE-ST-{i:03d}",
            "sequence": str(i),
            "state_name": name,
            "entry_requirement": entry,
            "permitted_effect": effect,
            "success_transition": success,
            "failure_transition": "REJECTED" if name != "REJECTED" else "TERMINAL",
            "current_state": "CONTRACT_ONLY_NOT_RUN",
            "authority_gate": "SEPARATE_FUTURE_ADAPTER_IMPLEMENTATION_ACCEPTANCE_AND_EXPLICIT_EXECUTION_AUTHORIZATION_REQUIRED",
            "prohibited_inference": PROHIBITED,
        })
    return rows


def operation_rows() -> list[dict[str, str]]:
    specs = [
        ("PREFLIGHT", "verify exact accepted source artifact digests", "accepted repository evidence", "none"),
        ("PREFLIGHT", "verify immutable synthetic implementation digest and oracle-only role", "implementation bytes", "none"),
        ("PREFLIGHT", "verify current candidate contains zero live inputs reads writes and authority", "contract artifacts", "none"),
        ("INPUT", "accept only ten explicit path or value arguments", "input documents and scalar values", "none"),
        ("INPUT", "read exact owner decision document bytes", "owner decision input only", "future transaction log only"),
        ("INPUT", "read exact owner authorization token document bytes", "token input only", "future transaction log only"),
        ("INPUT", "read exact coordinate receipt document bytes", "coordinate input only", "future transaction log only"),
        ("INPUT", "read exact revocation and replay snapshot bytes", "authority metadata only", "future transaction log only"),
        ("DIGEST", "canonicalize and verify owner decision digest", "input document bytes", "none"),
        ("DIGEST", "canonicalize and verify token digest", "input document bytes", "none"),
        ("DIGEST", "canonicalize and verify coordinate receipt digest", "input document bytes", "none"),
        ("BIND", "verify owner decision to token bindings", "normalized input values", "none"),
        ("BIND", "verify token to coordinate receipt digest binding", "normalized input values", "none"),
        ("BASELINE", "verify repository HEAD tree remote HEAD and executor uid", "explicit scalar values", "none"),
        ("TIME", "verify owner and token time windows", "explicit clock snapshot", "none"),
        ("AUTHORITY", "verify revocation epoch and token replay tuple unused", "authority metadata", "none"),
        ("COORDINATE", "verify exact 41-row and 10-field cardinality", "coordinate text only", "none"),
        ("COORDINATE", "verify row ids object ids digests sizes SONAMEs and sequences", "coordinate text and accepted contract", "none"),
        ("COORDINATE", "validate absolute canonical path text and path_text_sha256 without opening path", "coordinate text only", "none"),
        ("BOUNDARY", "reject live-to-synthetic path or origin rewriting and synthetic CLI invocation", "adapter behavior contract", "none"),
        ("ENVELOPE", "serialize exact twenty-field adapter envelope", "normalized validated values", "future transaction-scoped inactive envelope only"),
        ("ENVELOPE", "compute and verify canonical envelope digest", "adapter envelope bytes", "future transaction-scoped inactive envelope only"),
        ("STAGE", "mark envelope inactive and provider-read gate closed", "adapter envelope metadata", "future transaction-scoped receipt only"),
        ("EXEC_AUTH", "parse exact execution authorization document", "execution authorization bytes only", "future transaction log only"),
        ("EXEC_AUTH", "verify twenty-seven claims kind digest and all bindings", "authorization document and envelope", "none"),
        ("EXEC_AUTH", "verify exact effects resource limits and output root", "authorization document", "none"),
        ("EXEC_AUTH", "verify execution time revocation and unused replay tuple", "authorization and authority metadata", "none"),
        ("EXEC_AUTH", "atomically consume exact execution replay tuple before first provider open", "authority registry only", "one append-only consumed tuple"),
        ("PROTECT", "snapshot protected package database and live glibc metadata", "protected metadata only", "future transaction snapshot only"),
        ("DELEGATE", "delegate exact envelope to separately accepted read-only evidence implementation", "exact 41 authorized paths only after gate", "evidence outputs only"),
        ("PROTECT", "snapshot and compare protected state and exact registry delta", "protected metadata only", "future transaction snapshot only"),
        ("RESULT", "bind result or failure receipt to authorization envelope evidence and protected-state outcome", "transaction evidence only", "logs receipt index archive only"),
    ]
    rows=[]
    for i, (phase, operation, reads, writes) in enumerate(specs, 1):
        rows.append({
            "operation_id": f"LSLIAE-OP-{i:03d}",
            "sequence": str(i),
            "phase": phase,
            "operation": operation,
            "permitted_read_scope": reads,
            "permitted_write_scope": writes,
            "current_state": "CONTRACT_ONLY_NOT_RUN",
            "authority_gate": "SEPARATE_FUTURE_ADAPTER_IMPLEMENTATION_ACCEPTANCE_AND_EXPLICIT_EXECUTION_AUTHORIZATION_REQUIRED",
            "prohibited_inference": PROHIBITED,
        })
    return rows


def failure_rows() -> list[dict[str, str]]:
    specs = [
        ("PACKAGE", "contract package or accepted source digest invalid"),
        ("SYNTHETIC_BOUNDARY", "accepted synthetic implementation mutated invoked with live input or treated as live executor"),
        ("INPUT_DISCOVERY", "input obtained by search glob environment inference fallback or unlisted channel"),
        ("INPUT_DOCUMENT", "owner token coordinate or revocation document missing malformed or noncanonical"),
        ("DIGEST", "any input or envelope digest mismatch"),
        ("OWNER_TOKEN_BINDING", "owner decision and token identifiers effects transaction baseline or executor differ"),
        ("TOKEN_COORDINATE_BINDING", "token coordinate_receipt_sha256 differs from canonical receipt"),
        ("BASELINE", "repository HEAD tree or remote HEAD stale or mismatched"),
        ("EXECUTOR", "executor uid absent invalid or mismatched"),
        ("TIME", "not-before issuance expiry ordering or validity invalid"),
        ("REVOCATION", "revocation epoch stale future or revoked"),
        ("REPLAY", "token or execution replay tuple previously consumed"),
        ("COORDINATE_CARDINALITY", "coordinate receipt not exactly 41 rows with 10 fields"),
        ("COORDINATE_BINDING", "row id object digest size SONAME sequence authority or origin mismatch"),
        ("PATH", "path not absolute canonical literal or path text digest mismatch"),
        ("SYNTHETIC_REWRITE", "live path or origin rewritten into synthetic namespace"),
        ("EXECUTION_AUTHORIZATION", "execution authorization absent malformed unbound expired revoked replayed or wrong kind"),
        ("EFFECT_RESOURCE_OUTPUT", "effect allowlist resource cap or transaction output scope invalid"),
        ("PROTECTED_STATE", "package database live glibc prefix or registry delta violates contract"),
        ("RESULT_DELIVERY", "canonical result failure receipt index archive or upload failed"),
    ]
    rows=[]
    for i, (klass, trigger) in enumerate(specs, 1):
        rows.append({
            "failure_id": f"LSLIAE-FAIL-{i:03d}",
            "sequence": str(i),
            "failure_class": klass,
            "trigger": trigger,
            "required_action": "reject whole adapter/execution transaction; before first open keep provider reads zero; after open close descriptors; emit bounded failure receipt; produce no accepted local map",
            "live_authority_effect": "ZERO_NEW_LIVE_AUTHORITY_AND_NO_RUNTIME_AUTHORITY",
            "cleanup_scope": "exact transaction-scoped draft envelope logs receipts index and archive only; never delete or mutate provider files package databases live glibc prefix generation roots or other authority state",
            "result_requirement": "canonical failure receipt with first failure codes read count write scope replay state and protected-state outcome when possible",
            "current_state": "CONTRACT_ONLY_NOT_RUN",
            "authority_gate": "SEPARATE_FUTURE_ADAPTER_IMPLEMENTATION_ACCEPTANCE_AND_EXPLICIT_EXECUTION_AUTHORIZATION_REQUIRED",
            "prohibited_inference": PROHIBITED,
        })
    return rows


def receipt_contract() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "review_id": REVIEW_ID,
        "acceptance_gate": ACCEPTANCE_GATE,
        "candidate_state": CANDIDATE_STATE,
        "current_live_inputs": [],
        "current_adapter_envelopes": [],
        "current_execution_authorizations": [],
        "current_provider_read_count": 0,
        "current_write_count": 0,
        "current_live_authority_count": 0,
        "future_adapter_success_receipt": {
            "decision": "QUALIFIED_INACTIVE_LIVE_INPUT_ADAPTER_ENVELOPE_CANDIDATE",
            "required_fields": [
                "transaction_id", "owner_decision_sha256", "owner_authorization_token_sha256",
                "coordinate_receipt_sha256", "adapter_envelope_sha256", "repository_head",
                "repository_tree", "remote_head", "executor_uid", "revocation_epoch",
                "coordinate_row_count", "provider_read_count", "write_scope",
                "synthetic_oracle_boundary", "receipt_sha256",
            ],
            "required_coordinate_row_count": 41,
            "provider_read_count": 0,
            "state": "INACTIVE_SEPARATE_EXECUTION_AUTHORIZATION_REQUIRED",
        },
        "future_execution_authorization_receipt": {
            "decision": "QUALIFIED_INACTIVE_READ_ONLY_EVIDENCE_EXECUTION_AUTHORIZATION_CANDIDATE",
            "required_fields": [
                "transaction_id", "execution_authorization_sha256", "adapter_envelope_sha256",
                "owner_authorization_token_sha256", "coordinate_receipt_sha256", "repository_head",
                "repository_tree", "remote_head", "executor_uid", "revocation_epoch",
                "exact_provider_path_count", "maximum_provider_bytes", "transaction_output_root",
                "receipt_sha256",
            ],
            "activation_state": "NOT_ACTIVE_UNTIL_EXACT_FUTURE_OWNER_ISSUANCE_AND_ATOMIC_REPLAY_CONSUMPTION",
        },
        "future_failure_receipt": {
            "decision": "REJECTED_LIVE_INPUT_ADAPTER_OR_EXECUTION_AUTHORIZATION",
            "required_fields": [
                "transaction_id_if_available", "first_failure", "failure_codes",
                "provider_read_count", "writes_performed", "replay_state",
                "protected_state_outcome", "receipt_sha256",
            ],
        },
        "maximum_receipt_bytes": 1048576,
        "overflow_action": "ABORT_WITH_ZERO_NEW_LIVE_AUTHORITY_AND_NO_ACCEPTED_LOCAL_MAP",
        "synthetic_implementation_role": "IMMUTABLE_SEMANTIC_AND_REGRESSION_ORACLE_ONLY_NOT_LIVE_EXECUTOR",
        "serialization": "canonical compact UTF-8 JSON sort_keys separators comma-colon newline terminated",
        "prohibited_inference": PROHIBITED,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output-root", type=Path, default=Path("."))
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    output = args.output_root.resolve()
    source_review = repo / REVIEW
    for name, digest in SOURCE_DIGESTS.items():
        path = source_review / name
        if not path.is_file() or sha(path) != digest:
            raise SystemExit(f"source digest mismatch: {name}")
    implementation = repo / BASE / "implementation/selected_provider_local_supply_evidence_authorization_issuance_coordinate_production_candidate.py"
    if sha(implementation) != IMPLEMENTATION_SHA256:
        raise SystemExit("accepted synthetic implementation digest mismatch")

    out = output / REVIEW
    out.mkdir(parents=True, exist_ok=True)
    artifacts = {
        ADAPTER_NAME: canonical_json(adapter_contract()),
        EXECUTION_NAME: canonical_json(execution_schema()),
        RECEIPT_NAME: canonical_json(receipt_contract()),
    }
    for name, data in artifacts.items():
        (out / name).write_bytes(data)

    validations = validation_rows()
    states = state_rows()
    operations = operation_rows()
    failures = failure_rows()
    write_tsv(out / VALIDATION_NAME,
              ["validation_id", "sequence", "category", "subject", "required_rule", "failure_code", "current_state", "authority_effect", "prohibited_inference"], validations)
    write_tsv(out / STATE_NAME,
              ["state_id", "sequence", "state_name", "entry_requirement", "permitted_effect", "success_transition", "failure_transition", "current_state", "authority_gate", "prohibited_inference"], states)
    write_tsv(out / OPERATION_NAME,
              ["operation_id", "sequence", "phase", "operation", "permitted_read_scope", "permitted_write_scope", "current_state", "authority_gate", "prohibited_inference"], operations)
    write_tsv(out / FAILURE_NAME,
              ["failure_id", "sequence", "failure_class", "trigger", "required_action", "live_authority_effect", "cleanup_scope", "result_requirement", "current_state", "authority_gate", "prohibited_inference"], failures)

    metadata = {
        "schema_version": 1,
        "contract_review_id": REVIEW_ID,
        "candidate_state": CANDIDATE_STATE,
        "acceptance_gate": ACCEPTANCE_GATE,
        "source_implementation_acceptance_id": IMPLEMENTATION_ACCEPTANCE_ID,
        "source_implementation_review_id": IMPLEMENTATION_REVIEW_ID,
        "source_implementation_sha256": IMPLEMENTATION_SHA256,
        "source_authorization_coordinate_contract_acceptance_id": CONTRACT_ACCEPTANCE_ID,
        "source_issuance_design_acceptance_id": ISSUANCE_DESIGN_ACCEPTANCE_ID,
        "source_local_supply_map_contract_acceptance_id": LOCAL_MAP_CONTRACT_ACCEPTANCE_ID,
        "source_evidence_design_acceptance_id": EVIDENCE_DESIGN_ACCEPTANCE_ID,
        "adapter_contract_sha256": sha(out / ADAPTER_NAME),
        "execution_authorization_schema_sha256": sha(out / EXECUTION_NAME),
        "validation_contract_sha256": sha(out / VALIDATION_NAME),
        "state_machine_sha256": sha(out / STATE_NAME),
        "operation_contract_sha256": sha(out / OPERATION_NAME),
        "failure_contract_sha256": sha(out / FAILURE_NAME),
        "receipt_contract_sha256": sha(out / RECEIPT_NAME),
        "explicit_input_channel_count": 10,
        "adapter_envelope_required_field_count": 20,
        "execution_authorization_required_claim_count": 27,
        "validation_rule_count": len(validations),
        "state_count": len(states),
        "operation_count": len(operations),
        "failure_count": len(failures),
        "coordinate_required_row_count": 41,
        "coordinate_required_row_field_count": 10,
        "maximum_provider_bytes": 29047112,
        "maximum_result_receipt_bytes": 1048576,
        "current_live_input_count": 0,
        "current_adapter_envelope_count": 0,
        "current_execution_authorization_count": 0,
        "current_provider_read_count": 0,
        "current_write_count": 0,
        "current_live_authority_count": 0,
        "synthetic_implementation_role": "IMMUTABLE_SEMANTIC_AND_REGRESSION_ORACLE_ONLY_NOT_LIVE_EXECUTOR",
        "live_to_synthetic_path_rewrite": "FORBIDDEN",
        "future_adapter_implementation_authorized": "NO",
        "execution_authorization_issuance_authorized": "NO",
        "provider_byte_read_authorized": "NO",
        "evidence_transaction_execution_authorized": "NO",
        "local_supply_map_produced": "NO",
        "generation_root_creation_authorized": "NO",
        "target_population_authorized": "NO",
        "materialization_authorized": "NO",
        "publication_authorized": "NO",
        "deployment_authorized": "NO",
        "activation_authorized": "NO",
        "update_boundary": "ANY_SCHEMA_FIELD_INPUT_CHANNEL_BINDING_VALIDATION_STATE_OPERATION_FAILURE_RECEIPT_RESOURCE_REPLAY_REVOCATION_SYNTHETIC_BOUNDARY_OR_AUTHORITY_CHANGE_REQUIRES_NEW_CLASS_D_CONTRACT_REVIEW",
        "rollback_boundary": "REMOVE_UNACCEPTED_CONTRACT_CANDIDATE_ONLY_NO_LIVE_INPUT_PROVIDER_READ_WRITE_OR_RUNTIME_STATE_EXISTS",
        "next_action": "review-and-accept-non-executing-selected-provider-local-supply-evidence-live-input-adapter-and-execution-authorization-contract-candidate-boundary",
        "authority_effect": "CONTRACT_CANDIDATE_ONLY_ZERO_LIVE_INPUTS_ZERO_PROVIDER_READS_ZERO_WRITES_ZERO_LIVE_AUTHORITY",
        "prohibited_inference": PROHIBITED,
    }
    write_metadata(out / METADATA_NAME, metadata)


if __name__ == "__main__":
    main()
