#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping

REVIEW_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-EXACT-INPUT-SET-COLLECTION-REVIEW-001"
ACCEPTANCE_GATE = "SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-EXACT-INPUT-SET-COLLECTION-ACCEPTANCE-OPEN"
OWNER_ACCEPTANCE_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-OWNER-ACTIVATION-ACCEPT-001"
SUCCESS_DECISION = "QUALIFIED_NON_EXECUTING_EXACT_INPUT_SET_COLLECTION_SEALING_CANDIDATE"
FAILURE_DECISION = "REJECTED_EXACT_INPUT_SET_COLLECTION_CASE_ZERO_CURRENT_AUTHORITY"
EXECUTION_MODE = "ISOLATED_FIXTURE_DOCUMENT_SEALING_PROVIDER_AND_REPLAY_LSTAT_ONLY_NO_LIVE_EXECUTION"

BASE = Path("experiments/glibc/selected-obsidian-provider-authority")
REVIEW = BASE / "review"
SOURCE_DIGESTS = {
    "selected-provider-local-supply-live-authority-transaction-owner-activation-decision-boundary-acceptance.tsv": "5cdd364870d3a4fcf7ed7b67a5acd97fa2ea14c96e7ef3e03f7499074c196fa9",
    "selected-provider-local-supply-live-authority-transaction-input-contract.tsv": "2ab0e1bf4051b85680b63669f44f4e9f0f04fab03dccbdd2397a1ba519842587",
    "selected-provider-local-supply-map-contract.tsv": "2223af964e74cc8bb221d13e559e49aaf03abe364985346cb1d8e43973c6640e",
    "selected-provider-local-supply-live-authority-transaction-production-implementation-boundary-acceptance.tsv": "9b3b8b312668dd231a1c133048673d76076e676f5a4c183a75843a8320429c99",
}
DOCUMENT_ROLES = (
    "OWNER_ACTIVATION_DECISION",
    "OWNER_AUTHORIZATION_TOKEN",
    "COORDINATE_RECEIPT",
    "REVOCATION_DOCUMENT",
    "EXECUTION_AUTHORIZATION",
)
FAILURE_NAMES = (
    "source-authority-invalid",
    "owner-activation-acceptance-invalid",
    "manifest-invalid",
    "implicit-path-or-inference",
    "owner-decision-invalid",
    "owner-token-invalid",
    "coordinate-receipt-invalid",
    "revocation-invalid",
    "execution-authorization-invalid",
    "repository-baseline-invalid",
    "remote-baseline-invalid",
    "executor-identity-invalid",
    "trusted-time-invalid",
    "replay-registry-metadata-invalid",
    "provider-coordinate-metadata-invalid",
    "output-root-invalid",
    "transaction-count-invalid",
    "provider-open-requested",
    "project-replay-open-or-write-requested",
    "live-execution-requested",
)
FAILURES = tuple(
    {"case": name, "failure_id": f"LSLA-COLLECT-FAIL-{index:03d}"}
    for index, name in enumerate(FAILURE_NAMES, start=1)
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


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_source_digests(repo: Path) -> None:
    for name, expected in SOURCE_DIGESTS.items():
        path = repo / REVIEW / name
        if not path.is_file() or sha_file(path) != expected:
            raise CandidateFailure("LSLA-COLLECT-FAIL-001", f"accepted source digest mismatch: {name}")
    acceptance = read_tsv(repo / REVIEW / "selected-provider-local-supply-live-authority-transaction-owner-activation-decision-boundary-acceptance.tsv")
    if len(acceptance) != 1:
        raise CandidateFailure("LSLA-COLLECT-FAIL-002", "owner activation acceptance cardinality")
    row = acceptance[0]
    expected = {
        "decision": "ACCEPTED_EXPLICIT_OWNER_ACTIVATION_DECISION_FOR_ONE_NON_EXECUTING_EXACT_INPUT_SET_COLLECTION_SEALING_AND_REVIEW_TRANSACTION_ONLY",
        "accepted_transaction_count": "1",
        "accepted_transaction_consumed_count": "0",
        "accepted_transaction_remaining_count": "1",
        "selected_provider_open_authorized": "NO",
        "selected_provider_read_authorized": "NO",
        "execution_authorized": "NO",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise CandidateFailure("LSLA-COLLECT-FAIL-002", f"owner activation acceptance mismatch: {key}")


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
    inputs = read_tsv(repo / REVIEW / "selected-provider-local-supply-live-authority-transaction-input-contract.tsv")
    coordinates = read_tsv(repo / REVIEW / "selected-provider-local-supply-map-contract.tsv")
    if len(inputs) != 20 or len(coordinates) != 41:
        raise CandidateFailure("LSLA-COLLECT-FAIL-001", "accepted source cardinality mismatch")
    coordinate_plan = [
        {
            "sequence": index,
            "contract_row_id": row["contract_row_id"],
            "provider_object_id": row["provider_object_id"],
            "member_basename": row["member_basename"],
        }
        for index, row in enumerate(coordinates, start=1)
    ]
    return {
        "schema_version": 1,
        "review_id": REVIEW_ID,
        "owner_acceptance_id": OWNER_ACCEPTANCE_ID,
        "execution_mode": EXECUTION_MODE,
        "input_contract_count": 20,
        "document_roles": list(DOCUMENT_ROLES),
        "document_role_count": 5,
        "coordinate_rows": coordinate_plan,
        "coordinate_row_count": 41,
        "coordinate_metadata_field_count": 10,
        "accepted_transaction_count": 1,
        "consumed_transaction_count": 0,
        "remaining_transaction_count": 1,
        "provider_content_open_authority": "NONE",
        "provider_content_read_authority": "NONE",
        "provider_byte_authority": "NONE",
        "project_replay_open_authority": "NONE",
        "project_replay_read_authority": "NONE",
        "project_replay_write_authority": "NONE",
        "live_execution_authority": "NONE",
        "isolated_output_authority": "EXACT_ENVELOPE_AND_BASENAME_RELATIVE_SHA256_ONLY",
    }


def build_negative_cases() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "review_id": REVIEW_ID,
        "case_count": 20,
        "cases": [
            {
                **item,
                "expected_selected_provider_open_count": 0,
                "expected_selected_provider_read_count": 0,
                "expected_provider_byte_count": 0,
                "expected_project_replay_open_count": 0,
                "expected_project_replay_read_count": 0,
                "expected_project_replay_write_count": 0,
                "expected_live_authority_count": 0,
            }
            for item in FAILURES
        ],
    }


def build_coverage_rows(repo: Path) -> list[dict[str, str]]:
    verify_source_digests(repo.resolve())
    inputs = read_tsv(repo.resolve() / REVIEW / "selected-provider-local-supply-live-authority-transaction-input-contract.tsv")
    if len(inputs) != 20:
        raise CandidateFailure("LSLA-COLLECT-FAIL-001", "input contract cardinality mismatch")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(inputs, start=1):
        rows.append({
            "coverage_kind": "INPUT",
            "source_id": row["input_id"],
            "sequence": str(index),
            "input_class": row["input_class"],
            "collection_action": collection_action(row["input_class"]),
            "isolated_case": "success",
            "current_state": "ISOLATED_FIXTURE_ONLY_NOT_LIVE_INPUT",
            "authority_effect": "ZERO_SELECTED_PROVIDER_OPENS_READS_PROVIDER_BYTES_PROJECT_REPLAY_OPENS_READS_WRITES_LIVE_AUTHORITY",
        })
    return rows


def collection_action(input_class: str) -> str:
    actions = {
        "SOURCE_ISSUANCE_ACCEPTANCE": "VERIFY_REPOSITORY_DIGEST_ONLY",
        "SOURCE_ADAPTER_ACCEPTANCE": "VERIFY_REPOSITORY_DIGEST_ONLY",
        "SOURCE_EVIDENCE_DESIGN_ACCEPTANCE": "VERIFY_REPOSITORY_DIGEST_ONLY",
        "SOURCE_ORCHESTRATION_ACCEPTANCE": "VERIFY_REPOSITORY_DIGEST_ONLY",
        "OWNER_ACTIVATION_DECISION": "CANONICAL_READ_AND_DIGEST_SEAL_ISOLATED_FIXTURE_ONLY",
        "OWNER_AUTHORIZATION_TOKEN": "CANONICAL_READ_AND_DIGEST_SEAL_ISOLATED_FIXTURE_ONLY",
        "COORDINATE_RECEIPT": "CANONICAL_READ_AND_DIGEST_SEAL_ISOLATED_FIXTURE_ONLY",
        "REVOCATION_DOCUMENT": "CANONICAL_READ_AND_DIGEST_SEAL_ISOLATED_FIXTURE_ONLY",
        "EXECUTION_AUTHORIZATION": "CANONICAL_READ_AND_DIGEST_SEAL_ISOLATED_FIXTURE_ONLY",
        "TRANSACTION_PACKAGE": "VERIFY_EXPLICIT_MANIFEST_ONLY",
        "REPOSITORY_BASELINE": "CAPTURE_GIT_HEAD_AND_TREE",
        "REMOTE_BASELINE": "CAPTURE_EXPLICIT_ORIGIN_MAIN_HEAD",
        "EXECUTOR_IDENTITY": "CAPTURE_UID_GID_ONLY",
        "TRUSTED_TIME": "SEAL_DOCUMENT_FIELD_ONLY_NO_CLOCK_AUTHORITY",
        "REPLAY_REGISTRY": "LSTAT_METADATA_ONLY_NO_OPEN_READ_WRITE",
        "PROTECTED_STATE_BOUNDARY": "RECORD_CALLER_SUPPLIED_SNAPSHOT_DIGESTS_ONLY",
        "ORCHESTRATION_ENTRYPOINT": "VERIFY_REPOSITORY_DIGEST_ONLY_NOT_INVOKED",
        "RESOURCE_LIMITS": "SEAL_DOCUMENT_CLAIMS_ONLY",
        "EVIDENCE_OUTPUT_ROOT": "WRITE_EXACT_ISOLATED_ENVELOPE_AND_SIDECAR_ONLY",
        "OPERATOR_INVOCATION": "VERIFY_EXPLICIT_ORDERED_ARGUMENTS_ONLY",
    }
    return actions.get(input_class, "REJECT_UNMAPPED_INPUT_CLASS")


def write_canonical(path: Path, value: Mapping[str, Any], mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(value))
    os.chmod(path, mode)


def _git(args: list[str], cwd: Path, env: Mapping[str, str] | None = None) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, env=dict(env) if env else None, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.strip()


def materialize_isolated_fixture(plan: Mapping[str, Any], fixture_root: Path, case: str, repo: Path) -> dict[str, Any]:
    root = fixture_root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    documents_root = root / "documents"
    provider_root = root / "provider-metadata-objects"
    output_root = root / "sealed-output"
    replay_path = root / "project-replay-registry.metadata-only"
    repository_root = root / "repository"
    remote_root = root / "origin.git"
    documents_root.mkdir(); provider_root.mkdir(); output_root.mkdir()
    replay_path.write_bytes(b"")
    os.chmod(replay_path, 0o600)

    env = os.environ.copy()
    env.update({
        "GIT_AUTHOR_NAME": "HW-T isolated collector",
        "GIT_AUTHOR_EMAIL": "isolated@example.invalid",
        "GIT_COMMITTER_NAME": "HW-T isolated collector",
        "GIT_COMMITTER_EMAIL": "isolated@example.invalid",
        "GIT_AUTHOR_DATE": "2026-07-30T00:00:00+00:00",
        "GIT_COMMITTER_DATE": "2026-07-30T00:00:00+00:00",
    })
    repository_root.mkdir()
    _git(["init", "-q"], repository_root, env)
    _git(["config", "user.name", env["GIT_AUTHOR_NAME"]], repository_root, env)
    _git(["config", "user.email", env["GIT_AUTHOR_EMAIL"]], repository_root, env)
    (repository_root / "baseline.txt").write_text("isolated exact-input-set baseline\n", encoding="utf-8")
    _git(["add", "baseline.txt"], repository_root, env)
    _git(["commit", "-q", "-m", "isolated baseline"], repository_root, env)
    subprocess.run(["git", "init", "--bare", "-q", str(remote_root)], check=True, env=env)
    _git(["remote", "add", "origin", str(remote_root)], repository_root, env)
    _git(["push", "-q", "origin", "HEAD:main"], repository_root, env)
    head = _git(["rev-parse", "HEAD"], repository_root, env)
    tree = _git(["rev-parse", "HEAD^{tree}"], repository_root, env)

    transaction_id = "lsla-exact-input-set-isolated-001"
    activation = seal({
        "schema_version": 1,
        "role": "OWNER_ACTIVATION_DECISION",
        "transaction_id": transaction_id,
        "owner_acceptance_id": OWNER_ACCEPTANCE_ID,
        "scope": "ONE_NON_EXECUTING_EXACT_INPUT_SET_COLLECTION_SEALING_AND_REVIEW_TRANSACTION_ONLY",
    })
    token = seal({
        "schema_version": 1,
        "role": "OWNER_AUTHORIZATION_TOKEN",
        "transaction_id": transaction_id,
        "activation_sha256": activation["document_sha256"],
        "authorization_scope": "COLLECTION_SEALING_REVIEW_ONLY_NO_PROVIDER_OPEN_READ_OR_EXECUTION",
    })
    coordinate_rows: list[dict[str, Any]] = []
    for item in plan["coordinate_rows"]:
        path = provider_root / f"{int(item['sequence']):02d}-{item['member_basename']}"
        path.write_bytes(b"isolated provider metadata placeholder; content must not be opened\n")
        os.chmod(path, 0o600)
        coordinate_rows.append({
            "sequence": item["sequence"],
            "contract_row_id": item["contract_row_id"],
            "provider_object_id": item["provider_object_id"],
            "absolute_canonical_path": str(path.resolve()),
        })
    coordinate = seal({
        "schema_version": 1,
        "role": "COORDINATE_RECEIPT",
        "transaction_id": transaction_id,
        "owner_token_sha256": token["document_sha256"],
        "coordinate_count": 41,
        "rows": coordinate_rows,
    })
    revocation = seal({
        "schema_version": 1,
        "role": "REVOCATION_DOCUMENT",
        "transaction_id": transaction_id,
        "owner_token_sha256": token["document_sha256"],
        "revoked": False,
        "sequence": 1,
    })
    execution = seal({
        "schema_version": 1,
        "role": "EXECUTION_AUTHORIZATION",
        "transaction_id": transaction_id,
        "owner_token_sha256": token["document_sha256"],
        "coordinate_receipt_sha256": coordinate["document_sha256"],
        "revocation_sha256": revocation["document_sha256"],
        "repository_head": head,
        "repository_tree": tree,
        "remote_head": head,
        "trusted_time_utc": "2026-07-30T00:00:00Z",
        "provider_open_authorized": False,
        "provider_read_authorized": False,
        "live_execution_authorized": False,
        "maximum_provider_bytes": 0,
    })
    docs = {
        "activation": activation,
        "token": token,
        "coordinate": coordinate,
        "revocation": revocation,
        "execution": execution,
    }
    paths: dict[str, str] = {}
    for name, value in docs.items():
        path = documents_root / f"{name}.json"
        write_canonical(path, value)
        paths[name] = str(path.resolve())

    manifest: dict[str, Any] = {
        "schema_version": 1,
        "case": case,
        "fixture_root": str(root),
        "transaction_id": transaction_id,
        "document_paths": paths,
        "repository_path": str(repository_root.resolve()),
        "remote_ref": "refs/heads/main",
        "replay_registry_path": str(replay_path.resolve()),
        "output_root": str(output_root.resolve()),
        "expected_repository_head": head,
        "expected_repository_tree": tree,
        "expected_remote_head": head,
        "expected_executor_uid": os.getuid(),
        "expected_executor_gid": os.getgid(),
        "protected_state_before": {"package_database_sha256": "3" * 64, "live_glibc_prefix_sha256": "4" * 64},
        "operator_invocation_mode": "EXPLICIT_ORDERED_ARGUMENTS_ONLY",
        "accepted_transaction_count": 1,
        "consumed_transaction_count": 0,
        "remaining_transaction_count": 1,
        "infer_paths": False,
        "provider_open_requested": False,
        "provider_read_requested": False,
        "project_replay_open_requested": False,
        "project_replay_write_requested": False,
        "live_execution_requested": False,
    }
    apply_fault(manifest, docs, documents_root, case)
    return manifest


def apply_fault(manifest: dict[str, Any], docs: dict[str, dict[str, Any]], documents_root: Path, case: str) -> None:
    mapping = {item["case"]: item["failure_id"] for item in FAILURES}
    if case == "success":
        return
    manifest["expected_failure_id"] = mapping[case]
    if case == "source-authority-invalid": manifest["source_authority_valid"] = False
    elif case == "owner-activation-acceptance-invalid": manifest["owner_acceptance_valid"] = False
    elif case == "manifest-invalid": manifest["schema_version"] = 2
    elif case == "implicit-path-or-inference": manifest["infer_paths"] = True
    elif case == "owner-decision-invalid": _mutate_doc(documents_root / "activation.json", "scope", "LIVE_EXECUTION")
    elif case == "owner-token-invalid": _mutate_doc(documents_root / "token.json", "activation_sha256", "0" * 64)
    elif case == "coordinate-receipt-invalid": _mutate_doc(documents_root / "coordinate.json", "coordinate_count", 40)
    elif case == "revocation-invalid": _mutate_doc(documents_root / "revocation.json", "revoked", True)
    elif case == "execution-authorization-invalid": _mutate_doc(documents_root / "execution.json", "provider_open_authorized", True)
    elif case == "repository-baseline-invalid": manifest["expected_repository_head"] = "0" * 40
    elif case == "remote-baseline-invalid": manifest["expected_remote_head"] = "0" * 40
    elif case == "executor-identity-invalid": manifest["expected_executor_uid"] = os.getuid() + 1
    elif case == "trusted-time-invalid": _mutate_doc(documents_root / "execution.json", "trusted_time_utc", "invalid")
    elif case == "replay-registry-metadata-invalid": Path(manifest["replay_registry_path"]).unlink()
    elif case == "provider-coordinate-metadata-invalid": Path(docs["coordinate"]["rows"][0]["absolute_canonical_path"]).unlink()
    elif case == "output-root-invalid": manifest["output_root"] = str(Path(manifest["fixture_root"]).parent / "escape")
    elif case == "transaction-count-invalid": manifest["consumed_transaction_count"] = 1; manifest["remaining_transaction_count"] = 0
    elif case == "provider-open-requested": manifest["provider_open_requested"] = True
    elif case == "project-replay-open-or-write-requested": manifest["project_replay_open_requested"] = True
    elif case == "live-execution-requested": manifest["live_execution_requested"] = True


def _mutate_doc(path: Path, key: str, value: Any) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    data[key] = value
    data.pop("document_sha256", None)
    seal(data)
    write_canonical(path, data)


def ensure_under(path: Path, root: Path, failure_id: str) -> Path:
    absolute = path.resolve(strict=False)
    if absolute == root or root not in absolute.parents:
        raise CandidateFailure(failure_id, f"path outside isolated root: {path}")
    return absolute


def read_canonical(path: Path, root: Path, failure_id: str) -> tuple[dict[str, Any], os.stat_result]:
    absolute = ensure_under(path, root, failure_id)
    before = os.lstat(absolute)
    if not stat.S_ISREG(before.st_mode) or before.st_uid != os.getuid() or stat.S_IMODE(before.st_mode) & 0o077:
        raise CandidateFailure(failure_id, f"unsafe document metadata: {absolute}")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(absolute, flags)
    try:
        opened = os.fstat(fd)
        if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            raise CandidateFailure(failure_id, "document identity changed before read")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 65536)
            if not chunk: break
            chunks.append(chunk)
        after = os.fstat(fd)
    finally:
        os.close(fd)
    if (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns) != (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns):
        raise CandidateFailure(failure_id, "document changed during read")
    data = b"".join(chunks)
    try:
        value = json.loads(data)
    except Exception as exc:
        raise CandidateFailure(failure_id, "document JSON invalid") from exc
    if data != canonical(value):
        raise CandidateFailure(failure_id, "document not canonical JSON")
    validate_seal(value, failure_id)
    return value, before


def base_result() -> dict[str, Any]:
    return {
        "pass": False,
        "decision": FAILURE_DECISION,
        "failure_id": None,
        "failure_detail": None,
        "input_contract_count": 20,
        "document_role_count": 5,
        "coordinate_row_count": 41,
        "coordinate_metadata_field_count": 10,
        "isolated_document_open_count": 0,
        "isolated_document_read_count": 0,
        "isolated_provider_lstat_count": 0,
        "isolated_replay_lstat_count": 0,
        "isolated_repository_metadata_capture_count": 0,
        "isolated_remote_metadata_capture_count": 0,
        "isolated_executor_identity_capture_count": 0,
        "isolated_envelope_write_count": 0,
        "selected_provider_open_count": 0,
        "selected_provider_read_count": 0,
        "provider_byte_count": 0,
        "project_replay_open_count": 0,
        "project_replay_read_count": 0,
        "project_replay_write_count": 0,
        "live_document_count": 0,
        "execution_authorization_count": 0,
        "local_supply_map_count": 0,
        "live_authority_count": 0,
        "provider_open_gate_armed": False,
        "accepted_transaction_count": 1,
        "consumed_transaction_count": 0,
        "remaining_transaction_count": 1,
    }


def execute_manifest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    result = base_result()
    expected_failure = manifest.get("expected_failure_id")
    try:
        if manifest.get("source_authority_valid", True) is not True:
            raise CandidateFailure("LSLA-COLLECT-FAIL-001", "source authority invalid")
        if manifest.get("owner_acceptance_valid", True) is not True:
            raise CandidateFailure("LSLA-COLLECT-FAIL-002", "owner activation acceptance invalid")
        if manifest.get("schema_version") != 1 or manifest.get("case") not in {"success", *FAILURE_NAMES}:
            raise CandidateFailure("LSLA-COLLECT-FAIL-003", "manifest invalid")
        root = Path(str(manifest.get("fixture_root", ""))).resolve()
        if not root.is_dir() or manifest.get("infer_paths") or manifest.get("operator_invocation_mode") != "EXPLICIT_ORDERED_ARGUMENTS_ONLY":
            raise CandidateFailure("LSLA-COLLECT-FAIL-004", "implicit path or inference forbidden")
        docs: dict[str, dict[str, Any]] = {}
        failure_ids = {
            "activation": "LSLA-COLLECT-FAIL-005", "token": "LSLA-COLLECT-FAIL-006",
            "coordinate": "LSLA-COLLECT-FAIL-007", "revocation": "LSLA-COLLECT-FAIL-008",
            "execution": "LSLA-COLLECT-FAIL-009",
        }
        for name in ("activation", "token", "coordinate", "revocation", "execution"):
            value, _ = read_canonical(Path(str(manifest["document_paths"][name])), root, failure_ids[name])
            docs[name] = value
            result["isolated_document_open_count"] += 1
            result["isolated_document_read_count"] += 1
        transaction_id = str(manifest["transaction_id"])
        if docs["activation"].get("scope") != "ONE_NON_EXECUTING_EXACT_INPUT_SET_COLLECTION_SEALING_AND_REVIEW_TRANSACTION_ONLY" or docs["activation"].get("transaction_id") != transaction_id:
            raise CandidateFailure("LSLA-COLLECT-FAIL-005", "owner decision scope or transaction mismatch")
        if docs["token"].get("activation_sha256") != docs["activation"].get("document_sha256") or docs["token"].get("transaction_id") != transaction_id:
            raise CandidateFailure("LSLA-COLLECT-FAIL-006", "owner token binding mismatch")
        rows = docs["coordinate"].get("rows")
        if docs["coordinate"].get("coordinate_count") != 41 or not isinstance(rows, list) or len(rows) != 41 or docs["coordinate"].get("owner_token_sha256") != docs["token"].get("document_sha256"):
            raise CandidateFailure("LSLA-COLLECT-FAIL-007", "coordinate receipt invalid")
        if docs["revocation"].get("revoked") is not False or docs["revocation"].get("owner_token_sha256") != docs["token"].get("document_sha256"):
            raise CandidateFailure("LSLA-COLLECT-FAIL-008", "revocation document invalid")
        execution = docs["execution"]
        if (
            execution.get("owner_token_sha256") != docs["token"].get("document_sha256")
            or execution.get("coordinate_receipt_sha256") != docs["coordinate"].get("document_sha256")
            or execution.get("revocation_sha256") != docs["revocation"].get("document_sha256")
            or execution.get("provider_open_authorized") is not False
            or execution.get("provider_read_authorized") is not False
            or execution.get("live_execution_authorized") is not False
            or execution.get("maximum_provider_bytes") != 0
        ):
            raise CandidateFailure("LSLA-COLLECT-FAIL-009", "execution authorization invalid for collection-only scope")
        repository = ensure_under(Path(str(manifest["repository_path"])), root, "LSLA-COLLECT-FAIL-010")
        head = _git(["rev-parse", "HEAD"], repository)
        tree = _git(["rev-parse", "HEAD^{tree}"], repository)
        result["isolated_repository_metadata_capture_count"] = 2
        if head != manifest.get("expected_repository_head") or tree != manifest.get("expected_repository_tree") or execution.get("repository_head") != head or execution.get("repository_tree") != tree:
            raise CandidateFailure("LSLA-COLLECT-FAIL-010", "repository baseline mismatch")
        remote_output = _git(["ls-remote", "origin", str(manifest["remote_ref"])], repository)
        remote_head = remote_output.split()[0] if remote_output else ""
        result["isolated_remote_metadata_capture_count"] = 1
        if remote_head != manifest.get("expected_remote_head") or execution.get("remote_head") != remote_head:
            raise CandidateFailure("LSLA-COLLECT-FAIL-011", "remote baseline mismatch")
        if os.getuid() != manifest.get("expected_executor_uid") or os.getgid() != manifest.get("expected_executor_gid"):
            raise CandidateFailure("LSLA-COLLECT-FAIL-012", "executor identity mismatch")
        result["isolated_executor_identity_capture_count"] = 1
        if execution.get("trusted_time_utc") != "2026-07-30T00:00:00Z":
            raise CandidateFailure("LSLA-COLLECT-FAIL-013", "trusted time evidence invalid")
        replay_path = ensure_under(Path(str(manifest["replay_registry_path"])), root, "LSLA-COLLECT-FAIL-014")
        replay_stat = os.lstat(replay_path)
        if not stat.S_ISREG(replay_stat.st_mode) or stat.S_IMODE(replay_stat.st_mode) & 0o077:
            raise CandidateFailure("LSLA-COLLECT-FAIL-014", "replay registry metadata invalid")
        result["isolated_replay_lstat_count"] = 1
        provider_metadata: list[dict[str, Any]] = []
        seen_paths: set[str] = set()
        for row in rows:
            path = ensure_under(Path(str(row.get("absolute_canonical_path", ""))), root, "LSLA-COLLECT-FAIL-015")
            if str(path) in seen_paths:
                raise CandidateFailure("LSLA-COLLECT-FAIL-015", "duplicate provider path")
            seen_paths.add(str(path))
            st = os.lstat(path)
            if not stat.S_ISREG(st.st_mode) or stat.S_IMODE(st.st_mode) & 0o077:
                raise CandidateFailure("LSLA-COLLECT-FAIL-015", "provider coordinate metadata invalid")
            provider_metadata.append({
                "sequence": row["sequence"],
                "contract_row_id": row["contract_row_id"],
                "absolute_canonical_path": str(path),
                "st_dev": st.st_dev,
                "st_ino": st.st_ino,
                "st_mode": stat.S_IMODE(st.st_mode),
                "st_uid": st.st_uid,
                "st_gid": st.st_gid,
                "st_size": st.st_size,
                "st_mtime_ns": st.st_mtime_ns,
            })
            result["isolated_provider_lstat_count"] += 1
        output_root = ensure_under(Path(str(manifest["output_root"])), root, "LSLA-COLLECT-FAIL-016")
        if not output_root.is_dir():
            raise CandidateFailure("LSLA-COLLECT-FAIL-016", "output root invalid")
        counts = (manifest.get("accepted_transaction_count"), manifest.get("consumed_transaction_count"), manifest.get("remaining_transaction_count"))
        if counts != (1, 0, 1):
            raise CandidateFailure("LSLA-COLLECT-FAIL-017", "owner transaction accounting invalid")
        if manifest.get("provider_open_requested") or manifest.get("provider_read_requested"):
            raise CandidateFailure("LSLA-COLLECT-FAIL-018", "provider open/read request forbidden")
        if manifest.get("project_replay_open_requested") or manifest.get("project_replay_write_requested"):
            raise CandidateFailure("LSLA-COLLECT-FAIL-019", "project replay open/write request forbidden")
        if manifest.get("live_execution_requested"):
            raise CandidateFailure("LSLA-COLLECT-FAIL-020", "live execution request forbidden")
        envelope = {
            "schema_version": 1,
            "decision": SUCCESS_DECISION,
            "review_id": REVIEW_ID,
            "transaction_id": transaction_id,
            "owner_acceptance_id": OWNER_ACCEPTANCE_ID,
            "document_digests": {role: docs[name]["document_sha256"] for role, name in zip(DOCUMENT_ROLES, ("activation", "token", "coordinate", "revocation", "execution"))},
            "repository_baseline": {"head": head, "tree": tree, "remote_head": remote_head},
            "executor_identity": {"uid": os.getuid(), "gid": os.getgid()},
            "trusted_time_utc": execution["trusted_time_utc"],
            "protected_state_before": manifest["protected_state_before"],
            "replay_registry_metadata": {
                "absolute_canonical_path": str(replay_path), "st_dev": replay_stat.st_dev, "st_ino": replay_stat.st_ino,
                "st_mode": stat.S_IMODE(replay_stat.st_mode), "st_uid": replay_stat.st_uid, "st_gid": replay_stat.st_gid,
                "st_size": replay_stat.st_size, "st_mtime_ns": replay_stat.st_mtime_ns,
            },
            "provider_coordinate_metadata": provider_metadata,
            "authority_counts": {
                "selected_provider_opens": 0, "selected_provider_reads": 0, "provider_bytes": 0,
                "project_replay_opens": 0, "project_replay_reads": 0, "project_replay_writes": 0,
                "live_documents": 0, "execution_authorizations": 0, "local_supply_maps": 0, "live_authority": 0,
            },
            "owner_activation_transaction_accounting": {"accepted": 1, "consumed": 0, "remaining": 1},
            "candidate_only": True,
            "live_input_set_accepted": False,
        }
        envelope_bytes = canonical(envelope)
        envelope_path = output_root / "exact-input-set-collection-envelope.json"
        sidecar_path = output_root / "exact-input-set-collection-envelope.json.sha256"
        for path, data in (
            (envelope_path, envelope_bytes),
            (sidecar_path, f"{sha_bytes(envelope_bytes)}  exact-input-set-collection-envelope.json\n".encode("utf-8")),
        ):
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
            fd = os.open(path, flags, 0o600)
            try:
                os.write(fd, data); os.fsync(fd)
            finally:
                os.close(fd)
            result["isolated_envelope_write_count"] += 1
        result.update({
            "pass": True,
            "decision": SUCCESS_DECISION,
            "failure_id": None,
            "failure_detail": None,
            "transaction_id": transaction_id,
            "sealed_envelope_member_count": 2,
            "sealed_document_digest_count": 5,
            "provider_coordinate_metadata_count": 41,
        })
        return result
    except CandidateFailure as exc:
        result["failure_id"] = exc.failure_id
        result["failure_detail"] = exc.detail
        if expected_failure and expected_failure != exc.failure_id:
            result["failure_detail"] = f"expected {expected_failure} but observed {exc.failure_id}: {exc.detail}"
        return result
    except Exception as exc:
        result["failure_id"] = str(expected_failure or "LSLA-COLLECT-FAIL-003")
        result["failure_detail"] = f"unexpected isolated failure: {type(exc).__name__}: {exc}"
        return result


def normalize_result(result: Mapping[str, Any]) -> dict[str, Any]:
    keys = (
        "pass", "decision", "failure_id", "failure_detail", "transaction_id",
        "input_contract_count", "document_role_count", "coordinate_row_count", "coordinate_metadata_field_count",
        "sealed_envelope_member_count", "sealed_document_digest_count", "provider_coordinate_metadata_count",
        "isolated_document_open_count", "isolated_document_read_count", "isolated_provider_lstat_count",
        "isolated_replay_lstat_count", "isolated_repository_metadata_capture_count", "isolated_remote_metadata_capture_count",
        "isolated_executor_identity_capture_count", "isolated_envelope_write_count",
        "selected_provider_open_count", "selected_provider_read_count", "provider_byte_count",
        "project_replay_open_count", "project_replay_read_count", "project_replay_write_count",
        "live_document_count", "execution_authorization_count", "local_supply_map_count", "live_authority_count",
        "provider_open_gate_armed", "accepted_transaction_count", "consumed_transaction_count", "remaining_transaction_count",
    )
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
    if args.output: args.output.write_bytes(output)
    else: sys.stdout.buffer.write(output)
    raise SystemExit(0 if result.get("pass") else 1)


if __name__ == "__main__":
    main()
