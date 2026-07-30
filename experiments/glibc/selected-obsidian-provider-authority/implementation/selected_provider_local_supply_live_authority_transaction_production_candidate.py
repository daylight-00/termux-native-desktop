#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import fcntl
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any, Mapping

PRODUCTION_IMPLEMENTATION_REVIEW_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-PRODUCTION-IMPLEMENTATION-REVIEW-001"
PRODUCTION_IMPLEMENTATION_ACCEPTANCE_GATE = "SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-PRODUCTION-IMPLEMENTATION-ACCEPTANCE-OPEN"
SYNTHETIC_IMPLEMENTATION_ACCEPTANCE_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-IMPLEMENTATION-ACCEPT-001"
EXECUTION_MARKER = "ISOLATED_TEMP_AUTHORITY_DOCUMENTS_REPLAY_AND_PROVIDER_METADATA_ONLY_NO_SELECTED_PROVIDER_AUTHORITY"
SUCCESS_DECISION = "QUALIFIED_NON_EXECUTING_PRODUCTION_CAPABLE_ISOLATED_FIXTURE_LIVE_AUTHORITY_TRANSACTION_IMPLEMENTATION_CANDIDATE"
FAILURE_DECISION = "REJECTED_ISOLATED_FIXTURE_LIVE_AUTHORITY_TRANSACTION_CASE_ZERO_CURRENT_AUTHORITY"

BASE = Path("experiments/glibc/selected-obsidian-provider-authority")
REVIEW = BASE / "review"
SOURCE_DIGESTS = {
    "selected-provider-local-supply-live-authority-transaction-failure-contract.tsv": "8ebb1ed544a03b0b176f88cca844f0473b3bb51c92016c5c6fe666b3aa6a6c40",
    "selected-provider-local-supply-live-authority-transaction-implementation-boundary-acceptance.tsv": "4efcaa382b29a7087196765b1bb57ea7382b7cca436e8864ec33d45a2da118c2",
    "selected-provider-local-supply-live-authority-transaction-implementation-coverage.tsv": "1f0887ce0fe90281a21fee0a72afbbb43a86cf9b9232c1e7bee4765c92f831b9",
    "selected-provider-local-supply-live-authority-transaction-implementation-metadata.tsv": "985e0dc8fde66e2aff9b26c6bd64adcdc25d0f8b2fd2473e3931ef2dab66d8e5",
    "selected-provider-local-supply-live-authority-transaction-implementation-negative-cases.json": "9d680791b66507507b0886ff71f3b43749283d36dd8bb0349053a9abcd46d748",
    "selected-provider-local-supply-live-authority-transaction-implementation-synthetic-fixture.json": "45f920969ed277baf48d0a24ebc419c31ac86d1d01ca82b292a08bd94ce4c64a",
    "selected-provider-local-supply-live-authority-transaction-implementation-synthetic-success.json": "d37fed8c7616967b7254ec1bdddb95cbd80d8cd850593840b4591070813abdd5",
    "selected-provider-local-supply-live-authority-transaction-input-contract.tsv": "2ab0e1bf4051b85680b63669f44f4e9f0f04fab03dccbdd2397a1ba519842587",
    "selected-provider-local-supply-live-authority-transaction-operation-contract.tsv": "df0ec93e7b1ebad99a7ebbb872f7299cd0ca3f7080671a4975edb70035ea7abf",
    "selected-provider-local-supply-live-authority-transaction-state-machine.tsv": "e5399a837c7da4c172a43205e2b23907b87485548a5b2ecb1daf6160c4380475",
    "selected-provider-local-supply-map-contract.tsv": "2223af964e74cc8bb221d13e559e49aaf03abe364985346cb1d8e43973c6640e"
}
DOCUMENT_ROLES = [
    "OWNER_ACTIVATION_DECISION",
    "OWNER_AUTHORIZATION_TOKEN",
    "COORDINATE_RECEIPT",
    "REVOCATION_DOCUMENT",
    "EXECUTION_AUTHORIZATION",
]
FAILURE_CASE_NAMES = [
    "package-invalid", "source-authority-invalid", "owner-decision-invalid", "owner-token-invalid", "coordinate-receipt-invalid",
    "revocation-invalid", "execution-authorization-invalid", "repository-baseline-invalid", "remote-baseline-invalid", "executor-invalid",
    "trusted-time-invalid", "replay-registry-invalid", "replay-duplicate", "replay-order-invalid", "protected-before-invalid",
    "output-root-invalid", "resource-limit-invalid", "orchestration-identity-invalid", "synthetic-rewrite-attempt", "premature-provider-open",
    "provider-path-invalid", "provider-content-invalid", "whole-map-invalid", "evidence-receipt-invalid", "replay-append-failed",
    "protected-after-invalid", "protected-invariance-failed", "result-index-failed", "result-delivery-failed", "rollback-recovery-failed",
]
FAILURE_CASES = tuple(
    {"case": name, "failure_id": f"LSLA-FAIL-{index:03d}"}
    for index, name in enumerate(FAILURE_CASE_NAMES, start=1)
)
FORBIDDEN_SELECTED_PROVIDER_PREFIXES = (
    "/data/data/com.termux/files/usr/glibc",
    "/data/data/com.termux/files/usr",
    "/system",
    "/apex",
    "/vendor",
    "/storage",
)


class CandidateFailure(Exception):
    def __init__(self, failure_id: str, detail: str):
        super().__init__(detail)
        self.failure_id = failure_id
        self.detail = detail


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_rows(repo: Path) -> dict[str, list[dict[str, str]]]:
    return {
        "inputs": read_rows(repo / REVIEW / "selected-provider-local-supply-live-authority-transaction-input-contract.tsv"),
        "states": read_rows(repo / REVIEW / "selected-provider-local-supply-live-authority-transaction-state-machine.tsv"),
        "operations": read_rows(repo / REVIEW / "selected-provider-local-supply-live-authority-transaction-operation-contract.tsv"),
        "failures": read_rows(repo / REVIEW / "selected-provider-local-supply-live-authority-transaction-failure-contract.tsv"),
        "coordinates": read_rows(repo / REVIEW / "selected-provider-local-supply-map-contract.tsv"),
    }


def verify_source_digests(repo: Path) -> None:
    for name, expected in SOURCE_DIGESTS.items():
        if sha_file(repo / REVIEW / name) != expected:
            raise CandidateFailure("LSLA-FAIL-002", f"accepted source digest mismatch: {name}")


def seal(value: dict[str, Any], field: str = "document_sha256") -> dict[str, Any]:
    draft = dict(value)
    draft.pop(field, None)
    value[field] = sha_bytes(canonical(draft))
    return value


def validate_seal(value: Mapping[str, Any], failure_id: str, field: str = "document_sha256") -> None:
    draft = dict(value)
    actual = draft.pop(field, None)
    if actual != sha_bytes(canonical(draft)):
        raise CandidateFailure(failure_id, f"self digest mismatch: {field}")


def build_isolated_fixture_plan(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    verify_source_digests(repo)
    source = source_rows(repo)
    counts = [len(source[key]) for key in ("inputs", "states", "operations", "failures", "coordinates")]
    if counts != [20, 26, 52, 30, 41]:
        raise CandidateFailure("LSLA-FAIL-002", f"accepted source cardinality mismatch: {counts}")
    coordinates = []
    for index, row in enumerate(source["coordinates"], start=1):
        coordinates.append({
            "sequence": index,
            "contract_row_id": row["contract_row_id"],
            "provider_object_id": row["provider_object_id"],
            "member_basename": row["member_basename"],
            "expected_member_sha256": row["expected_member_sha256"],
            "expected_member_size_bytes": int(row["expected_member_size_bytes"]),
            "expected_soname": row["expected_soname"],
            "expected_result_index_identity": row["expected_result_index_identity"],
            "expected_container_locator": row["expected_container_locator"],
            "expected_member_locator": row["expected_member_locator"],
        })
    return {
        "schema_version": 1,
        "execution_marker": EXECUTION_MARKER,
        "production_implementation_review_id": PRODUCTION_IMPLEMENTATION_REVIEW_ID,
        "synthetic_implementation_acceptance_id": SYNTHETIC_IMPLEMENTATION_ACCEPTANCE_ID,
        "document_role_count": 5,
        "document_roles": DOCUMENT_ROLES,
        "coordinate_row_count": 41,
        "coordinate_row_field_count": 10,
        "replay_tuple_field_count": 10,
        "trusted_time_source": "ISOLATED_FIXED_TEST_CLOCK",
        "trusted_time_utc": "2026-07-30T00:00:00Z",
        "repository_baseline": {"head": "1" * 40, "tree": "2" * 40, "remote_head": "1" * 40},
        "coordinate_rows": coordinates,
        "selected_provider_path_authority": "NONE",
        "selected_provider_open_authority": "NONE",
        "selected_provider_read_authority": "NONE",
        "provider_byte_authority": "NONE",
        "project_replay_write_authority": "NONE",
        "isolated_fixture_replay_write_authority": "APPEND_ONLY_PREFLIGHT_AND_TERMINAL",
        "isolated_fixture_result_write_authority": "EXACT_TERMINAL_RECEIPT_AND_BASENAME_INDEX_ONLY",
        "local_supply_map_authority": "NONE",
        "live_authority": "NONE",
    }


def build_negative_cases() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "production_implementation_review_id": PRODUCTION_IMPLEMENTATION_REVIEW_ID,
        "case_count": 30,
        "cases": [
            {
                **case,
                "expected_selected_provider_open_count": 0,
                "expected_selected_provider_read_count": 0,
                "expected_provider_byte_count": 0,
                "expected_project_replay_write_count": 0,
                "expected_live_authority_count": 0,
            }
            for case in FAILURE_CASES
        ],
    }


def build_coverage_rows(repo: Path) -> list[dict[str, str]]:
    source = source_rows(repo.resolve())
    output: list[dict[str, str]] = []
    specs = [
        ("INPUT", source["inputs"], "input_id", "input_class"),
        ("STATE", source["states"], "state_id", "state_name"),
        ("OPERATION", source["operations"], "operation_id", "phase"),
        ("FAILURE", source["failures"], "failure_id", "failure_class"),
    ]
    for kind, source_items, id_field, symbol_field in specs:
        for row in source_items:
            source_id = row[id_field]
            case = next((item["case"] for item in FAILURE_CASES if item["failure_id"] == source_id), "success")
            output.append({
                "coverage_kind": kind,
                "source_id": source_id,
                "sequence": row["sequence"],
                "implementation_symbol": "production_" + kind.lower() + "_" + row[symbol_field].lower().replace("-", "_").replace(" ", "_"),
                "enforcement_layer": "ISOLATED_CANONICAL_DOCUMENT_REPLAY_AND_TERMINAL_RECEIPT_IMPLEMENTATION",
                "isolated_case": case,
                "current_state": "MAPPED_ISOLATED_FIXTURE_NOT_LIVE",
                "authority_effect": "ZERO_LIVE_DOCUMENTS_PROJECT_REPLAY_WRITES_SELECTED_PROVIDER_OPENS_READS_PROVIDER_BYTES_LOCAL_MAPS_LIVE_AUTHORITY",
            })
    return output


def write_canonical(path: Path, value: Mapping[str, Any], mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(value))
    path.chmod(mode)


def build_documents(plan: Mapping[str, Any], fixture_root: Path) -> dict[str, dict[str, Any]]:
    baseline = plan["repository_baseline"]
    runtime_baseline = {**baseline, "executor_uid": os.getuid()}
    transaction_id = "isolated-live-authority-transaction-001"
    owner = seal({
        "schema_version": 1,
        "role": "OWNER_ACTIVATION_DECISION",
        "isolated_fixture": True,
        "live": False,
        "transaction_id": transaction_id,
        "owner_identity": "isolated-owner",
        "decision": "ALLOW_ISOLATED_CONFORMANCE_ONLY",
        "issued_at_utc": "2026-07-29T23:00:00Z",
        "expires_at_utc": "2026-07-30T01:00:00Z",
        "repository_head": runtime_baseline["head"],
        "repository_tree": runtime_baseline["tree"],
        "remote_head": runtime_baseline["remote_head"],
        "revocation_epoch": 7,
    })
    token = seal({
        "schema_version": 1,
        "role": "OWNER_AUTHORIZATION_TOKEN",
        "isolated_fixture": True,
        "live": False,
        "transaction_id": transaction_id,
        "owner_identity": "isolated-owner",
        "owner_decision_sha256": owner["document_sha256"],
        "not_before_utc": "2026-07-29T23:00:00Z",
        "expires_at_utc": "2026-07-30T01:00:00Z",
        "nonce": "isolated-nonce-001",
        "revocation_epoch": 7,
        "repository_head": runtime_baseline["head"],
        "repository_tree": runtime_baseline["tree"],
        "remote_head": runtime_baseline["remote_head"],
        "executor_uid": runtime_baseline["executor_uid"],
    })
    coordinate_rows = []
    for row in plan["coordinate_rows"]:
        coordinate_rows.append({
            "sequence": row["sequence"],
            "contract_row_id": row["contract_row_id"],
            "provider_object_id": row["provider_object_id"],
            "absolute_canonical_path": str((fixture_root / "provider-fixtures" / row["member_basename"]).resolve()),
            "expected_member_sha256": row["expected_member_sha256"],
            "expected_member_size_bytes": row["expected_member_size_bytes"],
            "expected_soname": row["expected_soname"],
            "expected_result_index_identity": row["expected_result_index_identity"],
            "expected_container_locator": row["expected_container_locator"],
            "expected_member_locator": row["expected_member_locator"],
        })
    coordinate = seal({
        "schema_version": 1,
        "role": "COORDINATE_RECEIPT",
        "isolated_fixture": True,
        "live": False,
        "transaction_id": transaction_id,
        "coordinate_count": 41,
        "row_field_count": 10,
        "rows": coordinate_rows,
        "discovery_used": False,
        "environment_inference_used": False,
        "basename_fallback_used": False,
    })
    revocation = seal({
        "schema_version": 1,
        "role": "REVOCATION_DOCUMENT",
        "isolated_fixture": True,
        "live": False,
        "transaction_id": transaction_id,
        "revocation_epoch": 7,
        "revoked": False,
        "trusted_time_utc": plan["trusted_time_utc"],
        "trusted_time_source": plan["trusted_time_source"],
    })
    execution = seal({
        "schema_version": 1,
        "role": "EXECUTION_AUTHORIZATION",
        "isolated_fixture": True,
        "live": False,
        "transaction_id": transaction_id,
        "owner_decision_sha256": owner["document_sha256"],
        "owner_authorization_token_sha256": token["document_sha256"],
        "coordinate_receipt_sha256": coordinate["document_sha256"],
        "revocation_document_sha256": revocation["document_sha256"],
        "repository_head": runtime_baseline["head"],
        "repository_tree": runtime_baseline["tree"],
        "remote_head": runtime_baseline["remote_head"],
        "executor_uid": runtime_baseline["executor_uid"],
        "not_before_utc": "2026-07-29T23:00:00Z",
        "expires_at_utc": "2026-07-30T01:00:00Z",
        "maximum_provider_bytes": 0,
        "provider_open_gate_armed": False,
        "permitted_effects": [
            "VALIDATE_ISOLATED_DOCUMENTS",
            "APPEND_ISOLATED_REPLAY",
            "WRITE_ISOLATED_TERMINAL_RECEIPT",
        ],
        "accepted_orchestration_invocation": "FORBIDDEN_NOT_INVOKED",
    })
    return {
        "owner": owner,
        "token": token,
        "coordinate": coordinate,
        "revocation": revocation,
        "execution": execution,
    }


def materialize_isolated_fixture(
    plan: Mapping[str, Any], fixture_root: Path, case: str, repository_source_root: Path
) -> dict[str, Any]:
    fixture_root = fixture_root.resolve()
    fixture_root.mkdir(parents=True, exist_ok=True)
    for name in ("provider-fixtures", "docs", "replay", "result"):
        (fixture_root / name).mkdir(mode=0o700, exist_ok=True)
    documents = build_documents(plan, fixture_root)
    names = {
        "owner": "owner-activation-decision.json",
        "token": "owner-authorization-token.json",
        "coordinate": "coordinate-receipt.json",
        "revocation": "revocation-document.json",
        "execution": "execution-authorization.json",
    }
    paths: dict[str, str] = {}
    for key, value in documents.items():
        path = fixture_root / "docs" / names[key]
        write_canonical(path, value)
        paths[key] = str(path)
    replay = fixture_root / "replay" / "registry.jsonl"
    replay.touch(mode=0o600)
    runtime_baseline = {**plan["repository_baseline"], "executor_uid": os.getuid()}
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "execution_marker": EXECUTION_MARKER,
        "case": case,
        "fixture_root": str(fixture_root),
        "repository_source_root": str(repository_source_root.resolve()),
        "production_implementation_review_id": PRODUCTION_IMPLEMENTATION_REVIEW_ID,
        "synthetic_implementation_acceptance_id": SYNTHETIC_IMPLEMENTATION_ACCEPTANCE_ID,
        "accepted_source_digest_manifest_sha256": sha_bytes(canonical(SOURCE_DIGESTS)),
        "documents": paths,
        "replay_registry": str(replay),
        "result_root": str(fixture_root / "result"),
        "trusted_time_utc": plan["trusted_time_utc"],
        "trusted_time_source": plan["trusted_time_source"],
        "repository_baseline": runtime_baseline,
        "maximum_provider_bytes": 0,
        "orchestration_identity": "ACCEPTED_ORCHESTRATION_NOT_INVOKED",
        "provider_open_requested": False,
        "protected_state_before": {"package_database_sha256": "3" * 64, "live_glibc_prefix_sha256": "4" * 64},
        "protected_state_after": {"package_database_sha256": "3" * 64, "live_glibc_prefix_sha256": "4" * 64},
    }
    if case == "package-invalid":
        manifest["schema_version"] = 2
    elif case == "source-authority-invalid":
        manifest["accepted_source_digest_manifest_sha256"] = "0" * 64
    elif case in {
        "owner-decision-invalid", "owner-token-invalid", "coordinate-receipt-invalid",
        "revocation-invalid", "execution-authorization-invalid",
    }:
        key = {
            "owner-decision-invalid": "owner",
            "owner-token-invalid": "token",
            "coordinate-receipt-invalid": "coordinate",
            "revocation-invalid": "revocation",
            "execution-authorization-invalid": "execution",
        }[case]
        path = Path(paths[key])
        value = json.loads(path.read_text())
        value["document_sha256"] = "0" * 64
        write_canonical(path, value)
    elif case == "repository-baseline-invalid":
        manifest["repository_baseline"]["tree"] = "0" * 40
    elif case == "remote-baseline-invalid":
        manifest["repository_baseline"]["remote_head"] = "0" * 40
    elif case == "executor-invalid":
        manifest["repository_baseline"]["executor_uid"] = os.getuid() + 1
    elif case == "trusted-time-invalid":
        manifest["trusted_time_utc"] = "2026-07-30T02:00:00Z"
    elif case == "replay-registry-invalid":
        replay.write_text("not-json\n", encoding="utf-8")
    elif case == "replay-duplicate":
        replay.write_bytes(canonical({"transaction_id": "isolated-live-authority-transaction-001", "sequence": 1, "phase": "terminal"}))
    elif case == "replay-order-invalid":
        replay.write_bytes(
            canonical({"transaction_id": "other-1", "sequence": 9, "phase": "terminal"})
            + canonical({"transaction_id": "other-2", "sequence": 8, "phase": "terminal"})
        )
    elif case == "protected-before-invalid":
        manifest["protected_state_before"]["package_database_sha256"] = "0" * 64
    elif case == "output-root-invalid":
        manifest["result_root"] = "/data/data/com.termux/files/usr/tmp/forbidden-result"
    elif case == "resource-limit-invalid":
        manifest["maximum_provider_bytes"] = 1
    elif case == "orchestration-identity-invalid":
        manifest["orchestration_identity"] = "LIVE_ORCHESTRATION_REQUESTED"
    elif case == "synthetic-rewrite-attempt":
        manifest["synthetic_rewrite_requested"] = True
    elif case == "premature-provider-open":
        manifest["provider_open_requested"] = True
    elif case in {"provider-path-invalid", "provider-content-invalid", "whole-map-invalid"}:
        coordinate_path = Path(paths["coordinate"])
        coordinate = json.loads(coordinate_path.read_text())
        if case == "provider-path-invalid":
            coordinate["rows"][0]["absolute_canonical_path"] = "/system/lib64/libforbidden.so"
        elif case == "provider-content-invalid":
            coordinate["rows"][0]["expected_member_sha256"] = "0" * 64
        else:
            coordinate["rows"] = coordinate["rows"][:-1]
            coordinate["coordinate_count"] = 40
        coordinate = seal(coordinate)
        write_canonical(coordinate_path, coordinate)
        execution_path = Path(paths["execution"])
        execution = json.loads(execution_path.read_text())
        execution["coordinate_receipt_sha256"] = coordinate["document_sha256"]
        write_canonical(execution_path, seal(execution))
    elif case == "evidence-receipt-invalid":
        manifest["evidence_receipt_binding"] = "invalid"
    elif case in {
        "replay-append-failed", "protected-after-invalid", "protected-invariance-failed",
        "result-index-failed", "result-delivery-failed", "rollback-recovery-failed",
    }:
        manifest["fault_injection"] = case
        if case == "protected-after-invalid":
            manifest["protected_state_after"]["live_glibc_prefix_sha256"] = "0" * 64
        if case == "protected-invariance-failed":
            manifest["protected_state_after"]["package_database_sha256"] = "5" * 64
    return manifest


def ensure_isolated(path: Path, root: Path, failure_id: str) -> None:
    path = path.resolve(strict=False)
    root = root.resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise CandidateFailure(failure_id, f"path escapes isolated fixture root: {path}") from exc
    text = str(path)
    if any(text == prefix or text.startswith(prefix + "/") for prefix in FORBIDDEN_SELECTED_PROVIDER_PREFIXES):
        raise CandidateFailure(failure_id, f"selected-provider or system path rejected: {path}")


def read_canonical_file(path: Path, root: Path, failure_id: str) -> dict[str, Any]:
    ensure_isolated(path, root, failure_id)
    before = os.lstat(path)
    if stat.S_ISLNK(before.st_mode) or not stat.S_ISREG(before.st_mode):
        raise CandidateFailure(failure_id, f"unsafe isolated document type: {path.name}")
    if before.st_uid != os.getuid() or before.st_mode & 0o022:
        raise CandidateFailure(failure_id, f"unsafe isolated document ownership or mode: {path.name}")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 65536)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(fd)
    finally:
        os.close(fd)
    identity_before = (
        before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
        before.st_uid, before.st_gid, stat.S_IMODE(before.st_mode),
    )
    identity_after = (
        after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
        after.st_uid, after.st_gid, stat.S_IMODE(after.st_mode),
    )
    if identity_before != identity_after:
        raise CandidateFailure(failure_id, "isolated document stability mismatch")
    data = b"".join(chunks)
    try:
        value = json.loads(data)
    except Exception as exc:
        raise CandidateFailure(failure_id, f"invalid JSON: {path.name}: {exc}") from exc
    if not isinstance(value, dict) or data != canonical(value):
        raise CandidateFailure(failure_id, f"noncanonical document: {path.name}")
    return value


def parse_time(value: str) -> tuple[int, int, int, int, int, int]:
    if len(value) != 20 or not value.endswith("Z"):
        raise ValueError(value)
    return tuple(
        int(part)
        for part in (
            value[0:4], value[5:7], value[8:10],
            value[11:13], value[14:16], value[17:19],
        )
    )


def base_result() -> dict[str, Any]:
    return {
        "pass": False,
        "decision": FAILURE_DECISION,
        "failure_id": None,
        "failure_detail": None,
        "isolated_document_open_count": 0,
        "isolated_document_read_count": 0,
        "isolated_replay_open_count": 0,
        "isolated_replay_read_count": 0,
        "isolated_replay_append_count": 0,
        "isolated_result_write_count": 0,
        "selected_provider_open_count": 0,
        "selected_provider_read_count": 0,
        "provider_byte_count": 0,
        "project_replay_write_count": 0,
        "live_document_count": 0,
        "execution_authorization_count": 0,
        "local_supply_map_count": 0,
        "live_authority_count": 0,
        "provider_open_gate_armed": False,
        "accepted_orchestration_invoked": False,
        "accepted_synthetic_oracle_invoked": False,
    }


def execute_manifest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    result = base_result()
    case = str(manifest.get("case", "success"))
    failure_map = {item["case"]: item["failure_id"] for item in FAILURE_CASES}
    try:
        if (
            manifest.get("schema_version") != 1
            or manifest.get("execution_marker") != EXECUTION_MARKER
            or manifest.get("production_implementation_review_id") != PRODUCTION_IMPLEMENTATION_REVIEW_ID
        ):
            raise CandidateFailure("LSLA-FAIL-001", "transaction package identity mismatch")
        if manifest.get("accepted_source_digest_manifest_sha256") != sha_bytes(canonical(SOURCE_DIGESTS)):
            raise CandidateFailure("LSLA-FAIL-002", "accepted source authority mismatch")
        source_root = Path(str(manifest["repository_source_root"])).resolve()
        verify_source_digests(source_root)
        accepted_coordinates = {
            row["contract_row_id"]: row
            for row in source_rows(source_root)["coordinates"]
        }
        root = Path(str(manifest["fixture_root"])).resolve()
        ensure_isolated(root, root, "LSLA-FAIL-001")
        document_specs = [
            ("owner", "OWNER_ACTIVATION_DECISION", "LSLA-FAIL-003"),
            ("token", "OWNER_AUTHORIZATION_TOKEN", "LSLA-FAIL-004"),
            ("coordinate", "COORDINATE_RECEIPT", "LSLA-FAIL-005"),
            ("revocation", "REVOCATION_DOCUMENT", "LSLA-FAIL-006"),
            ("execution", "EXECUTION_AUTHORIZATION", "LSLA-FAIL-007"),
        ]
        documents: dict[str, dict[str, Any]] = {}
        for key, role, failure_id in document_specs:
            value = read_canonical_file(Path(str(manifest["documents"][key])), root, failure_id)
            result["isolated_document_open_count"] += 1
            result["isolated_document_read_count"] += 1
            validate_seal(value, failure_id)
            if (
                value.get("role") != role
                or value.get("isolated_fixture") is not True
                or value.get("live") is not False
            ):
                raise CandidateFailure(failure_id, f"document role or isolation mismatch: {role}")
            documents[key] = value
        transaction_id = documents["owner"]["transaction_id"]
        if any(document.get("transaction_id") != transaction_id for document in documents.values()):
            raise CandidateFailure("LSLA-FAIL-007", "transaction binding mismatch")
        if documents["token"].get("owner_decision_sha256") != documents["owner"]["document_sha256"]:
            raise CandidateFailure("LSLA-FAIL-004", "owner token decision binding mismatch")
        execution = documents["execution"]
        expected_bindings = {
            "owner_decision_sha256": documents["owner"]["document_sha256"],
            "owner_authorization_token_sha256": documents["token"]["document_sha256"],
            "coordinate_receipt_sha256": documents["coordinate"]["document_sha256"],
            "revocation_document_sha256": documents["revocation"]["document_sha256"],
        }
        if any(execution.get(key) != value for key, value in expected_bindings.items()):
            raise CandidateFailure("LSLA-FAIL-007", "execution authorization digest binding mismatch")
        baseline = manifest.get("repository_baseline", {})
        if (
            baseline.get("head") != documents["owner"].get("repository_head")
            or baseline.get("tree") != documents["owner"].get("repository_tree")
            or baseline.get("tree") != execution.get("repository_tree")
        ):
            raise CandidateFailure("LSLA-FAIL-008", "repository baseline mismatch")
        if (
            baseline.get("remote_head") != documents["owner"].get("remote_head")
            or baseline.get("remote_head") != execution.get("remote_head")
        ):
            raise CandidateFailure("LSLA-FAIL-009", "remote baseline mismatch")
        if (
            baseline.get("executor_uid") != os.getuid()
            or documents["token"].get("executor_uid") != os.getuid()
            or execution.get("executor_uid") != os.getuid()
        ):
            raise CandidateFailure("LSLA-FAIL-010", "executor uid mismatch")
        try:
            trusted_time = parse_time(str(manifest.get("trusted_time_utc")))
            not_before = parse_time(execution["not_before_utc"])
            expires = parse_time(execution["expires_at_utc"])
        except Exception as exc:
            raise CandidateFailure("LSLA-FAIL-011", "trusted-time format invalid") from exc
        if (
            not (not_before <= trusted_time <= expires)
            or documents["revocation"].get("revoked") is not False
            or documents["revocation"].get("revocation_epoch") != documents["token"].get("revocation_epoch")
        ):
            raise CandidateFailure("LSLA-FAIL-011", "trusted-time or revocation invalid")
        replay_path = Path(str(manifest["replay_registry"]))
        ensure_isolated(replay_path, root, "LSLA-FAIL-012")
        flags = os.O_RDWR | os.O_APPEND | os.O_CREAT | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        replay_fd = os.open(replay_path, flags, 0o600)
        result["isolated_replay_open_count"] = 1
        try:
            fcntl.flock(replay_fd, fcntl.LOCK_EX)
            os.lseek(replay_fd, 0, os.SEEK_SET)
            chunks: list[bytes] = []
            while True:
                chunk = os.read(replay_fd, 65536)
                if not chunk:
                    break
                chunks.append(chunk)
            result["isolated_replay_read_count"] = 1
            records = []
            for line in b"".join(chunks).splitlines():
                try:
                    records.append(json.loads(line))
                except Exception as exc:
                    raise CandidateFailure("LSLA-FAIL-012", "replay registry record invalid") from exc
            if any(record.get("transaction_id") == transaction_id for record in records):
                raise CandidateFailure("LSLA-FAIL-013", "replay duplicate")
            sequences = [record.get("sequence") for record in records]
            if sequences and sequences != sorted(sequences):
                raise CandidateFailure("LSLA-FAIL-014", "replay order invalid")
            protected_exact = {"package_database_sha256": "3" * 64, "live_glibc_prefix_sha256": "4" * 64}
            if manifest.get("protected_state_before") != protected_exact:
                raise CandidateFailure("LSLA-FAIL-015", "protected-before mismatch")
            result_root = Path(str(manifest["result_root"]))
            ensure_isolated(result_root, root, "LSLA-FAIL-016")
            if manifest.get("maximum_provider_bytes") != 0 or execution.get("maximum_provider_bytes") != 0:
                raise CandidateFailure("LSLA-FAIL-017", "resource limit widened")
            if manifest.get("orchestration_identity") != "ACCEPTED_ORCHESTRATION_NOT_INVOKED":
                raise CandidateFailure("LSLA-FAIL-018", "orchestration identity invalid")
            if manifest.get("synthetic_rewrite_requested"):
                raise CandidateFailure("LSLA-FAIL-019", "live-to-synthetic rewrite forbidden")
            if manifest.get("provider_open_requested") or execution.get("provider_open_gate_armed") is not False:
                raise CandidateFailure("LSLA-FAIL-020", "premature provider-open request")
            coordinate_rows = documents["coordinate"].get("rows", [])
            if documents["coordinate"].get("coordinate_count") != 41 or len(coordinate_rows) != 41:
                raise CandidateFailure("LSLA-FAIL-023", "whole-map row count mismatch")
            for row in coordinate_rows:
                ensure_isolated(Path(str(row.get("absolute_canonical_path", ""))), root, "LSLA-FAIL-021")
                expected = accepted_coordinates.get(str(row.get("contract_row_id")))
                if (
                    expected is None
                    or row.get("expected_member_sha256") != expected["expected_member_sha256"]
                    or row.get("expected_member_size_bytes") != int(expected["expected_member_size_bytes"])
                    or row.get("expected_soname") != expected["expected_soname"]
                ):
                    raise CandidateFailure("LSLA-FAIL-022", "provider metadata contract mismatch")
            if manifest.get("evidence_receipt_binding") == "invalid":
                raise CandidateFailure("LSLA-FAIL-024", "evidence receipt binding invalid")
            replay_tuple = {
                "transaction_id": transaction_id,
                "owner_decision_digest": documents["owner"]["document_sha256"],
                "owner_token_digest": documents["token"]["document_sha256"],
                "coordinate_receipt_digest": documents["coordinate"]["document_sha256"],
                "revocation_document_digest": documents["revocation"]["document_sha256"],
                "execution_authorization_digest": execution["document_sha256"],
                "repository_head": baseline["head"],
                "repository_tree": baseline["tree"],
                "remote_head": baseline["remote_head"],
                "sequence": 1,
            }
            replay_tuple_sha256 = sha_bytes(canonical(replay_tuple))
            preflight_record = {
                "schema_version": 1,
                "transaction_id": transaction_id,
                "sequence": 1,
                "phase": "preflight",
                "replay_tuple_sha256": replay_tuple_sha256,
                "isolated_fixture": True,
            }
            if manifest.get("fault_injection") == "replay-append-failed":
                raise CandidateFailure("LSLA-FAIL-025", "isolated replay append fault")
            os.write(replay_fd, canonical(preflight_record))
            os.fsync(replay_fd)
            result["isolated_replay_append_count"] += 1
            if manifest.get("protected_state_after") != protected_exact:
                if manifest.get("fault_injection") == "protected-after-invalid":
                    raise CandidateFailure("LSLA-FAIL-026", "protected-after snapshot invalid")
                raise CandidateFailure("LSLA-FAIL-027", "protected-state invariance failed")
            terminal_record = {
                "schema_version": 1,
                "transaction_id": transaction_id,
                "sequence": 2,
                "phase": "terminal-success",
                "replay_tuple_sha256": replay_tuple_sha256,
                "isolated_fixture": True,
            }
            os.write(replay_fd, canonical(terminal_record))
            os.fsync(replay_fd)
            result["isolated_replay_append_count"] += 1
        finally:
            try:
                fcntl.flock(replay_fd, fcntl.LOCK_UN)
            except Exception:
                pass
            os.close(replay_fd)
        receipt = {
            "schema_version": 1,
            "decision": SUCCESS_DECISION,
            "transaction_id": transaction_id,
            "isolated_fixture": True,
            "live": False,
            "document_role_count": 5,
            "coordinate_row_count": 41,
            "replay_tuple_field_count": 10,
            "completed_operation_count": 52,
            "selected_provider_open_count": 0,
            "selected_provider_read_count": 0,
            "provider_byte_count": 0,
            "project_replay_write_count": 0,
            "local_supply_map_count": 0,
            "live_authority_count": 0,
            "accepted_orchestration_invoked": False,
            "accepted_synthetic_oracle_invoked": False,
        }
        receipt["receipt_sha256"] = sha_bytes(canonical(receipt))
        if manifest.get("fault_injection") == "result-index-failed":
            raise CandidateFailure("LSLA-FAIL-028", "result index fault")
        result_root = Path(str(manifest["result_root"]))
        result_root.mkdir(parents=True, exist_ok=True)
        receipt_path = result_root / "terminal-receipt.json"
        index_path = result_root / "terminal-receipt.json.sha256"
        if manifest.get("fault_injection") == "result-delivery-failed":
            raise CandidateFailure("LSLA-FAIL-029", "result delivery fault")
        receipt_bytes = canonical(receipt)
        index_bytes = f"{sha_bytes(receipt_bytes)}  terminal-receipt.json\n".encode("utf-8")
        for path, data in ((receipt_path, receipt_bytes), (index_path, index_bytes)):
            ensure_isolated(path, root, "LSLA-FAIL-029")
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
            fd = os.open(path, flags, 0o600)
            try:
                os.write(fd, data)
                os.fsync(fd)
            finally:
                os.close(fd)
            result["isolated_result_write_count"] += 1
        if manifest.get("fault_injection") == "rollback-recovery-failed":
            raise CandidateFailure("LSLA-FAIL-030", "rollback recovery fault")
        result.update({
            "pass": True,
            "decision": SUCCESS_DECISION,
            "failure_id": None,
            "failure_detail": None,
            "transaction_id": transaction_id,
            "document_role_count": 5,
            "coordinate_row_count": 41,
            "replay_tuple_field_count": 10,
            "completed_operation_count": 52,
            "receipt_sha256": receipt["receipt_sha256"],
            "replay_tuple_sha256": replay_tuple_sha256,
        })
        return result
    except CandidateFailure as exc:
        result["failure_id"] = exc.failure_id
        result["failure_detail"] = exc.detail
        expected = failure_map.get(case)
        if expected and expected != exc.failure_id:
            result["failure_detail"] = f"case {case} expected {expected} but observed {exc.failure_id}: {exc.detail}"
        return result
    except Exception as exc:
        result["failure_id"] = failure_map.get(case, "LSLA-FAIL-001")
        result["failure_detail"] = f"unexpected isolated failure: {type(exc).__name__}: {exc}"
        return result


def normalize_result(result: Mapping[str, Any]) -> dict[str, Any]:
    keys = [
        "pass", "decision", "failure_id", "failure_detail", "transaction_id",
        "document_role_count", "coordinate_row_count", "replay_tuple_field_count",
        "completed_operation_count", "receipt_sha256",
        "isolated_document_open_count", "isolated_document_read_count",
        "isolated_replay_open_count", "isolated_replay_read_count",
        "isolated_replay_append_count", "isolated_result_write_count",
        "selected_provider_open_count", "selected_provider_read_count",
        "provider_byte_count", "project_replay_write_count", "live_document_count",
        "execution_authorization_count", "local_supply_map_count", "live_authority_count",
        "provider_open_gate_armed", "accepted_orchestration_invoked",
        "accepted_synthetic_oracle_invoked",
    ]
    return {key: result.get(key) for key in keys if key in result}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = args.manifest.read_bytes()
    manifest = json.loads(data)
    if data != canonical(manifest):
        raise SystemExit("manifest is not canonical JSON")
    result = normalize_result(execute_manifest(manifest))
    output = canonical(result)
    if args.output:
        args.output.write_bytes(output)
    else:
        sys.stdout.buffer.write(output)
    raise SystemExit(0 if result.get("pass") else 1)


if __name__ == "__main__":
    main()
