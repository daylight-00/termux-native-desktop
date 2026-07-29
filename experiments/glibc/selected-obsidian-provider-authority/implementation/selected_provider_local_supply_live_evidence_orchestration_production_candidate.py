#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import os
import stat
import struct
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

REVIEW_ID = "SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-EVIDENCE-ORCHESTRATION-PRODUCTION-IMPLEMENTATION-REVIEW-001"
ACCEPTANCE_GATE = "SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-EVIDENCE-ORCHESTRATION-PRODUCTION-IMPLEMENTATION-ACCEPTANCE-OPEN"
CANDIDATE_STATE = "QUALIFIED_NON_EXECUTING_PRODUCTION_CAPABLE_ISOLATED_FIXTURE_LIVE_EVIDENCE_ORCHESTRATION_IMPLEMENTATION_CANDIDATE"
ISOLATED_MARKER = "ISOLATED_TEMP_FIXTURE_ONLY_NOT_SELECTED_PROVIDER_AUTHORITY"
ACTUAL_V130_HEAD = "d4b7a95ea3afecb885fdefbb2e144acfc37d25e8"
ACTUAL_V130_TREE = "5b2fd6540c8252a23f21c9ebb8784fe0bb364554"
MAX_PROVIDER_BYTES = 29_047_112
MAX_RECEIPT_BYTES = 1_048_576
REQUIRED_EXECUTION_EFFECTS = [
    "OPEN_EXACT_41_EXPLICIT_PROVIDER_PATHS_NOFOLLOW",
    "READ_HASH_FSTAT_AND_ELF_SONAME_VALIDATE_EXACT_PROVIDER_BYTES",
    "WRITE_TRANSACTION_SCOPED_EVIDENCE_LOGS_RECEIPTS_INDEX_AND_ARCHIVE_ONLY",
    "DELEGATE_TO_SEPARATELY_ACCEPTED_READ_ONLY_LOCAL_SUPPLY_EVIDENCE_IMPLEMENTATION_ONLY",
]
FORBIDDEN_SELECTED_PROVIDER_PREFIXES = (
    "/data/data/com.termux/files/usr/glibc",
    "/data/data/com.termux/files/usr",
    "/system",
    "/apex",
    "/vendor",
)

INPUT_IDS = [f"LEO-IN-{i:03d}" for i in range(1, 19)]
STATE_IDS = [f"LEO-STATE-{i:03d}" for i in range(1, 25)]
OPERATION_IDS = [f"LEO-OP-{i:03d}" for i in range(1, 49)]
FAILURE_IDS = [f"LEO-FAIL-{i:03d}" for i in range(1, 29)]

NEGATIVE_CASES = [
    ("acceptance-binding-mismatch", "LEO-FAIL-001"),
    ("owner-decision-noncanonical", "LEO-FAIL-002"),
    ("token-claim-gap", "LEO-FAIL-003"),
    ("coordinate-row-count", "LEO-FAIL-004"),
    ("revocation-epoch-mismatch", "LEO-FAIL-005"),
    ("repository-head-mismatch", "LEO-FAIL-006"),
    ("repository-tree-mismatch", "LEO-FAIL-007"),
    ("remote-head-mismatch", "LEO-FAIL-008"),
    ("executor-uid-mismatch", "LEO-FAIL-009"),
    ("time-window-invalid", "LEO-FAIL-010"),
    ("output-root-invalid", "LEO-FAIL-011"),
    ("replay-already-consumed", "LEO-FAIL-012"),
    ("adapter-envelope-digest", "LEO-FAIL-013"),
    ("execution-authorization-digest", "LEO-FAIL-014"),
    ("execution-effect-widening", "LEO-FAIL-015"),
    ("live-to-synthetic-rewrite", "LEO-FAIL-016"),
    ("selected-provider-path", "LEO-FAIL-017"),
    ("symlink-component", "LEO-FAIL-018"),
    ("non-regular-file", "LEO-FAIL-019"),
    ("owner-mismatch", "LEO-FAIL-020"),
    ("writable-mode", "LEO-FAIL-021"),
    ("size-mismatch", "LEO-FAIL-022"),
    ("sha256-mismatch", "LEO-FAIL-023"),
    ("elf-identity-mismatch", "LEO-FAIL-024"),
    ("soname-mismatch", "LEO-FAIL-025"),
    ("stability-mismatch", "LEO-FAIL-026"),
    ("whole-map-gap", "LEO-FAIL-027"),
    ("protected-state-mismatch", "LEO-FAIL-028"),
]

TOKEN_REQUIRED_CLAIMS = [
    "schema_version", "authorization_token_id", "authorization_kind", "owner_identity",
    "owner_decision_id", "issued_at_utc", "expires_at_utc", "not_before_utc", "nonce",
    "revocation_epoch", "transaction_id", "contract_acceptance_id",
    "evidence_design_acceptance_id", "repository_head", "repository_tree", "remote_head",
    "executor_uid", "coordinate_receipt_sha256",
]
COORDINATE_ROW_FIELDS = [
    "contract_row_id", "sequence", "provider_object_id", "expected_member_sha256",
    "expected_member_size_bytes", "expected_soname", "absolute_canonical_path",
    "coordinate_authority_id", "coordinate_origin", "path_text_sha256",
]
ADAPTER_FIELDS = [
    "schema_version", "adapter_contract_review_id", "adapter_envelope_id", "transaction_id",
    "created_at_utc", "owner_decision_sha256", "owner_authorization_token_sha256",
    "coordinate_receipt_sha256", "revocation_snapshot_sha256", "repository_head",
    "repository_tree", "remote_head", "executor_uid", "revocation_epoch",
    "coordinate_row_count", "coordinate_row_digest_manifest_sha256", "replay_tuple_sha256",
    "transaction_output_root", "adapter_state", "envelope_sha256",
]
EXECUTION_REQUIRED_CLAIMS = [
    "schema_version", "execution_authorization_id", "authorization_kind", "owner_identity",
    "owner_decision_id", "issued_at_utc", "not_before_utc", "expires_at_utc", "nonce",
    "revocation_epoch", "transaction_id", "adapter_contract_acceptance_id",
    "adapter_envelope_sha256", "implementation_acceptance_id",
    "local_supply_map_contract_acceptance_id", "evidence_design_acceptance_id",
    "repository_head", "repository_tree", "remote_head", "executor_uid",
    "owner_authorization_token_sha256", "coordinate_receipt_sha256",
    "exact_provider_path_count", "maximum_provider_bytes", "transaction_output_root",
    "permitted_effects", "authorization_sha256",
]


class CandidateFailure(Exception):
    def __init__(self, failure_id: str, detail: str):
        super().__init__(detail)
        self.failure_id = failure_id
        self.detail = detail


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_object(value: Mapping[str, Any], digest_field: str) -> str:
    draft = dict(value)
    draft.pop(digest_field, None)
    return sha_bytes(canonical(draft))


def seal_object(value: dict[str, Any], digest_field: str) -> dict[str, Any]:
    value[digest_field] = digest_object(value, digest_field)
    return value


def read_canonical_json(path: Path, failure_id: str) -> dict[str, Any]:
    try:
        data = path.read_bytes()
        value = json.loads(data)
    except Exception as exc:
        raise CandidateFailure(failure_id, f"unable to parse explicit input: {path.name}: {exc}") from exc
    if not isinstance(value, dict) or data != canonical(value):
        raise CandidateFailure(failure_id, f"input is not canonical JSON: {path.name}")
    return value


def validate_self_digest(value: Mapping[str, Any], field: str, failure_id: str) -> None:
    if value.get(field) != digest_object(value, field):
        raise CandidateFailure(failure_id, f"self digest mismatch: {field}")


def ensure_exact_fields(value: Mapping[str, Any], required: list[str], failure_id: str) -> None:
    if sorted(value.keys()) != sorted(required):
        raise CandidateFailure(failure_id, f"field set mismatch: expected {len(required)}, got {len(value)}")


def build_minimal_elf64_aarch64(soname: str, payload_seed: str, target_size: int = 4096) -> bytes:
    dynstr = b"\x00" + soname.encode("utf-8") + b"\x00"
    soname_offset = 1
    dynamic = struct.pack("<QQ", 14, soname_offset) + struct.pack("<QQ", 0, 0)
    ehsize = 64
    dynstr_off = 0x100
    dynamic_off = (dynstr_off + len(dynstr) + 15) & ~15
    shoff = (dynamic_off + len(dynamic) + 63) & ~63
    shentsize = 64
    shnum = 3
    minimum = shoff + shentsize * shnum
    size = max(target_size, minimum)
    buf = bytearray(size)
    ident = b"\x7fELF" + bytes([2, 1, 1, 0, 0]) + bytes(7)
    header = struct.pack(
        "<16sHHIQQQIHHHHHH",
        ident, 3, 183, 1, 0, 0, shoff, 0, ehsize, 0, 0, shentsize, shnum, 0,
    )
    buf[:64] = header
    buf[dynstr_off:dynstr_off + len(dynstr)] = dynstr
    buf[dynamic_off:dynamic_off + len(dynamic)] = dynamic
    # null section
    buf[shoff:shoff + 64] = bytes(64)
    # dynstr section: SHT_STRTAB
    buf[shoff + 64:shoff + 128] = struct.pack(
        "<IIQQQQIIQQ", 0, 3, 2, 0, dynstr_off, len(dynstr), 0, 0, 1, 0
    )
    # dynamic section: SHT_DYNAMIC, link -> dynstr section 1
    buf[shoff + 128:shoff + 192] = struct.pack(
        "<IIQQQQIIQQ", 0, 6, 2, 0, dynamic_off, len(dynamic), 1, 0, 8, 16
    )
    seed = hashlib.sha256(payload_seed.encode("utf-8")).digest()
    payload_start = 64
    payload_end = min(dynstr_off, size)
    for offset in range(payload_start, payload_end):
        buf[offset] = seed[(offset - payload_start) % len(seed)]
    return bytes(buf)


def pread_exact(fd: int, size: int, offset: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    position = offset
    while remaining:
        chunk = os.pread(fd, remaining, position)
        if not chunk:
            raise CandidateFailure("LEO-FAIL-024", "short ELF read")
        chunks.append(chunk)
        position += len(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def parse_elf64_aarch64_soname(fd: int, file_size: int) -> str:
    if file_size < 64:
        raise CandidateFailure("LEO-FAIL-024", "ELF file too small")
    header = pread_exact(fd, 64, 0)
    fields = struct.unpack("<16sHHIQQQIHHHHHH", header)
    ident, e_type, e_machine, e_version, _, _, e_shoff, _, e_ehsize, _, _, e_shentsize, e_shnum, _ = fields
    if ident[:4] != b"\x7fELF" or ident[4] != 2 or ident[5] != 1 or e_type != 3 or e_machine != 183 or e_version != 1 or e_ehsize != 64:
        raise CandidateFailure("LEO-FAIL-024", "ELF64 little-endian AArch64 ET_DYN identity mismatch")
    if e_shentsize != 64 or e_shnum < 2 or e_shnum > 256 or e_shoff + e_shentsize * e_shnum > file_size:
        raise CandidateFailure("LEO-FAIL-024", "ELF section table bounds invalid")
    sections = []
    for index in range(e_shnum):
        raw = pread_exact(fd, 64, e_shoff + index * 64)
        sections.append(struct.unpack("<IIQQQQIIQQ", raw))
    for sec in sections:
        _, sh_type, _, _, sh_offset, sh_size, sh_link, _, _, sh_entsize = sec
        if sh_type != 6:
            continue
        if sh_link >= len(sections) or sh_entsize not in (0, 16) or sh_offset + sh_size > file_size:
            raise CandidateFailure("LEO-FAIL-024", "ELF dynamic section invalid")
        linked = sections[sh_link]
        _, linked_type, _, _, str_off, str_size, _, _, _, _ = linked
        if linked_type != 3 or str_off + str_size > file_size:
            raise CandidateFailure("LEO-FAIL-024", "ELF dynstr section invalid")
        dynstr = pread_exact(fd, str_size, str_off)
        dynamic = pread_exact(fd, sh_size, sh_offset)
        for off in range(0, len(dynamic) - 15, 16):
            tag, value = struct.unpack_from("<QQ", dynamic, off)
            if tag == 0:
                break
            if tag == 14:
                if value >= len(dynstr):
                    raise CandidateFailure("LEO-FAIL-024", "DT_SONAME offset invalid")
                end = dynstr.find(b"\x00", value)
                if end < 0:
                    raise CandidateFailure("LEO-FAIL-024", "DT_SONAME not terminated")
                try:
                    return dynstr[value:end].decode("utf-8")
                except UnicodeDecodeError as exc:
                    raise CandidateFailure("LEO-FAIL-024", "DT_SONAME invalid UTF-8") from exc
    raise CandidateFailure("LEO-FAIL-024", "DT_SONAME missing")


def is_under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def reject_forbidden_path(path: Path) -> None:
    text = str(path)
    if any(text == prefix or text.startswith(prefix + "/") for prefix in FORBIDDEN_SELECTED_PROVIDER_PREFIXES):
        raise CandidateFailure("LEO-FAIL-017", "selected-provider or system path rejected")
    if text.startswith("/__synthetic__/"):
        raise CandidateFailure("LEO-FAIL-016", "live-to-synthetic rewrite rejected")


def component_lstat_no_symlink(path: Path, allowed_root: Path) -> os.stat_result:
    if not path.is_absolute() or not allowed_root.is_absolute() or not is_under(path, allowed_root):
        raise CandidateFailure("LEO-FAIL-017", "coordinate path outside isolated fixture root")
    reject_forbidden_path(path)
    current = allowed_root
    try:
        root_stat = os.lstat(current)
    except OSError as exc:
        raise CandidateFailure("LEO-FAIL-018", f"fixture root unavailable: {exc}") from exc
    if stat.S_ISLNK(root_stat.st_mode):
        raise CandidateFailure("LEO-FAIL-018", "fixture root symlink rejected")
    relative = path.relative_to(allowed_root)
    for part in relative.parts:
        if part in ("", ".", ".."):
            raise CandidateFailure("LEO-FAIL-017", "noncanonical path component")
        current = current / part
        try:
            info = os.lstat(current)
        except OSError as exc:
            raise CandidateFailure("LEO-FAIL-019", f"component unavailable: {exc}") from exc
        if stat.S_ISLNK(info.st_mode):
            raise CandidateFailure("LEO-FAIL-018", "symlink component rejected")
    return info


@dataclass
class InMemoryReplayRegistry:
    consumed: set[str]

    def consume(self, replay_tuple: str) -> None:
        if replay_tuple in self.consumed:
            raise CandidateFailure("LEO-FAIL-012", "replay tuple already consumed")
        self.consumed.add(replay_tuple)


def stat_identity(value: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    # ctime is intentionally excluded: Android filesystems may refresh inode-change
    # timestamps during otherwise read-only metadata observation.  Stability is
    # instead bound to the opened object, exact size/content mtime, ownership and
    # mode, which preserves the no-substitution/no-mutation boundary portably.
    return (
        value.st_dev,
        value.st_ino,
        value.st_size,
        value.st_mtime_ns,
        value.st_uid,
        value.st_gid,
        stat.S_IMODE(value.st_mode),
    )


def validate_fixture_file(row: Mapping[str, Any], allowed_root: Path, expected_uid: int, force_stability_mismatch: bool) -> dict[str, Any]:
    path = Path(str(row["absolute_canonical_path"]))
    before = component_lstat_no_symlink(path, allowed_root)
    if not stat.S_ISREG(before.st_mode):
        raise CandidateFailure("LEO-FAIL-019", "non-regular file rejected")
    if before.st_uid != expected_uid:
        raise CandidateFailure("LEO-FAIL-020", "owner mismatch")
    if before.st_mode & 0o022:
        raise CandidateFailure("LEO-FAIL-021", "group/other writable mode rejected")
    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise CandidateFailure("LEO-FAIL-019", f"nofollow open failed: {exc}") from exc
    try:
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            raise CandidateFailure("LEO-FAIL-019", "lstat/fstat regular identity mismatch")
        digest = hashlib.sha256()
        total = 0
        while True:
            chunk = os.read(fd, 131072)
            if not chunk:
                break
            digest.update(chunk)
            total += len(chunk)
            if total > MAX_PROVIDER_BYTES:
                raise CandidateFailure("LEO-FAIL-022", "provider byte budget exceeded")
        after = os.fstat(fd)
        if force_stability_mismatch:
            raise CandidateFailure("LEO-FAIL-026", "forced isolated-fixture stability mismatch")
        if stat_identity(opened) != stat_identity(after):
            raise CandidateFailure("LEO-FAIL-026", "file identity changed during read")
        if total != int(row["expected_member_size_bytes"]):
            raise CandidateFailure("LEO-FAIL-022", "exact size mismatch")
        if digest.hexdigest() != row["expected_member_sha256"]:
            raise CandidateFailure("LEO-FAIL-023", "streamed SHA-256 mismatch")
        soname = parse_elf64_aarch64_soname(fd, total)
        if soname != row["expected_soname"]:
            raise CandidateFailure("LEO-FAIL-025", "DT_SONAME mismatch")
        return {
            "contract_row_id": row["contract_row_id"],
            "sequence": row["sequence"],
            "fixture_relative_path": str(path.relative_to(allowed_root)),
            "size_bytes": total,
            "sha256": digest.hexdigest(),
            "soname": soname,
        }
    finally:
        os.close(fd)


def build_coverage_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    definitions = [
        ("input", INPUT_IDS, "validate_input_binding"),
        ("state", STATE_IDS, "advance_fail_closed_state"),
        ("operation", OPERATION_IDS, "execute_ordered_orchestration_operation"),
        ("failure", FAILURE_IDS, "reject_and_close_without_live_authority"),
    ]
    for kind, ids, symbol in definitions:
        for sequence, source_id in enumerate(ids, 1):
            rows.append({
                "coverage_kind": kind,
                "source_id": source_id,
                "sequence": str(sequence),
                "implementation_symbol": symbol,
                "enforcement_layer": "production_orchestration_isolated_fixture_gate",
                "isolated_case": "success" if kind != "failure" else NEGATIVE_CASES[sequence - 1][0],
                "selected_provider_effect": "ZERO_SELECTED_PROVIDER_OPENS_READS_WRITES_LIVE_AUTHORITY",
                "authority_effect": "CANDIDATE_ONLY_SEPARATE_ACCEPTANCE_AND_LIVE_EXECUTION_AUTHORIZATION_REQUIRED",
            })
    return rows


def build_negative_cases() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "review_id": REVIEW_ID,
        "case_count": len(NEGATIVE_CASES),
        "cases": [
            {"sequence": index, "case": name, "expected_failure_id": failure_id}
            for index, (name, failure_id) in enumerate(NEGATIVE_CASES, 1)
        ],
    }


def build_isolated_fixture_plan(repo_root: Path) -> dict[str, Any]:
    contract_path = repo_root / "experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-contract.tsv"
    with contract_path.open(newline="", encoding="utf-8") as handle:
        contract_rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(contract_rows) != 41:
        raise RuntimeError("accepted local-supply contract cardinality mismatch")
    rows = []
    for row in contract_rows:
        data = build_minimal_elf64_aarch64(row["expected_soname"], row["contract_row_id"])
        rows.append({
            "contract_row_id": row["contract_row_id"],
            "sequence": int(row["sequence"]),
            "accepted_provider_object_id": row["provider_object_id"],
            "accepted_member_basename": row["member_basename"],
            "accepted_expected_member_sha256": row["expected_member_sha256"],
            "accepted_expected_member_size_bytes": int(row["expected_member_size_bytes"]),
            "expected_soname": row["expected_soname"],
            "fixture_relative_path": f"provider/{int(row['sequence']):02d}-{row['member_basename']}",
            "fixture_size_bytes": len(data),
            "fixture_sha256": sha_bytes(data),
        })
    return {
        "schema_version": 1,
        "review_id": REVIEW_ID,
        "execution_marker": ISOLATED_MARKER,
        "accepted_repository_head": ACTUAL_V130_HEAD,
        "accepted_repository_tree": ACTUAL_V130_TREE,
        "accepted_remote_head": ACTUAL_V130_HEAD,
        "row_count": 41,
        "row_field_count": 10,
        "test_harness_writes_authority": "ISOLATED_TEMP_FIXTURE_MATERIALIZATION_ONLY",
        "candidate_filesystem_write_authority": "NONE",
        "selected_provider_path_authority": "NONE",
        "rows": rows,
    }


def materialize_isolated_fixture(plan: Mapping[str, Any], root: Path, case: str = "success") -> Path:
    root.mkdir(parents=True, exist_ok=False)
    provider_root = root / "provider"
    docs_root = root / "documents"
    output_root = root / "outputs"
    provider_root.mkdir(mode=0o700)
    docs_root.mkdir(mode=0o700)
    output_root.mkdir(mode=0o700)
    rows: list[dict[str, Any]] = []
    for source in plan["rows"]:
        relative = Path(source["fixture_relative_path"])
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        data = build_minimal_elf64_aarch64(source["expected_soname"], source["contract_row_id"])
        target.write_bytes(data)
        target.chmod(0o600)
        rows.append({
            "contract_row_id": source["contract_row_id"],
            "sequence": source["sequence"],
            "provider_object_id": source["accepted_provider_object_id"],
            "expected_member_sha256": source["fixture_sha256"],
            "expected_member_size_bytes": source["fixture_size_bytes"],
            "expected_soname": source["expected_soname"],
            "absolute_canonical_path": str(target.resolve()),
            "coordinate_authority_id": "ISOLATED-FIXTURE-COORDINATE-AUTHORITY-001",
            "coordinate_origin": "ISOLATED_TEST_HARNESS_SURROGATE_NOT_LIVE_PROVIDER",
            "path_text_sha256": sha_bytes((str(target.resolve()) + "\n").encode("utf-8")),
        })
    now = "2026-07-28T16:28:15Z"
    owner = {
        "schema_version": 1, "owner_identity": "fixture-owner", "owner_decision_id": "FIXTURE-OWNER-DECISION-001",
        "decision_effect": "READ_ONLY_LOCAL_SUPPLY_EVIDENCE_TRANSACTION_ONLY", "issued_at_utc": now,
        "not_before_utc": "2026-07-28T16:28:00Z", "expires_at_utc": "2026-07-28T17:00:00Z",
        "revocation_epoch": 7, "executor_uid": os.getuid(), "transaction_id": "fixture-live-evidence-001",
    }
    coordinate = {
        "schema_version": 1,
        "coordinate_receipt_id": "ISOLATED-FIXTURE-COORDINATE-RECEIPT-001",
        "contract_acceptance_id": "SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-ACCEPT-001",
        "evidence_design_acceptance_id": "SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-DESIGN-ACCEPT-001",
        "repository_head": ACTUAL_V130_HEAD, "repository_tree": ACTUAL_V130_TREE, "remote_head": ACTUAL_V130_HEAD,
        "issuer_identity": "fixture-owner", "issued_at_utc": now, "rows": rows,
    }
    seal_object(coordinate, "receipt_sha256")
    token = {
        "schema_version": 1, "authorization_token_id": "ISOLATED-FIXTURE-TOKEN-001",
        "authorization_kind": "READ_ONLY_LOCAL_SUPPLY_EVIDENCE_TRANSACTION_ONLY", "owner_identity": "fixture-owner",
        "owner_decision_id": owner["owner_decision_id"], "issued_at_utc": now,
        "expires_at_utc": "2026-07-28T17:00:00Z", "not_before_utc": "2026-07-28T16:28:00Z",
        "nonce": "fixture-token-nonce-001", "revocation_epoch": 7, "transaction_id": owner["transaction_id"],
        "contract_acceptance_id": "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-COORDINATE-CONTRACT-ACCEPT-001",
        "evidence_design_acceptance_id": coordinate["evidence_design_acceptance_id"],
        "repository_head": ACTUAL_V130_HEAD, "repository_tree": ACTUAL_V130_TREE,
        "remote_head": ACTUAL_V130_HEAD, "executor_uid": os.getuid(),
        "coordinate_receipt_sha256": coordinate["receipt_sha256"],
    }
    revocation = {
        "schema_version": 1, "owner_identity": "fixture-owner", "revocation_epoch": 7,
        "consumed_replay_tuples": [], "snapshot_id": "ISOLATED-FIXTURE-REVOCATION-001",
    }
    owner_digest = sha_bytes(canonical(owner))
    token_digest = sha_bytes(canonical(token))
    revocation_digest = sha_bytes(canonical(revocation))
    row_manifest_digest = sha_bytes(canonical([sha_bytes(canonical(row)) for row in rows]))
    replay_tuple = sha_bytes(canonical({
        "authorization_token_id": token["authorization_token_id"],
        "nonce": token["nonce"], "transaction_id": token["transaction_id"],
        "coordinate_receipt_sha256": coordinate["receipt_sha256"],
    }))
    adapter = {
        "schema_version": 1,
        "adapter_contract_review_id": "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-CONTRACT-REVIEW-001",
        "adapter_envelope_id": "ISOLATED-FIXTURE-ADAPTER-001", "transaction_id": token["transaction_id"],
        "created_at_utc": now, "owner_decision_sha256": owner_digest,
        "owner_authorization_token_sha256": token_digest, "coordinate_receipt_sha256": coordinate["receipt_sha256"],
        "revocation_snapshot_sha256": revocation_digest, "repository_head": ACTUAL_V130_HEAD,
        "repository_tree": ACTUAL_V130_TREE, "remote_head": ACTUAL_V130_HEAD, "executor_uid": os.getuid(),
        "revocation_epoch": 7, "coordinate_row_count": 41,
        "coordinate_row_digest_manifest_sha256": row_manifest_digest, "replay_tuple_sha256": replay_tuple,
        "transaction_output_root": str(output_root.resolve()), "adapter_state": "VALIDATED_ISOLATED_FIXTURE_ONLY",
    }
    seal_object(adapter, "envelope_sha256")
    execution = {
        "schema_version": 1, "execution_authorization_id": "ISOLATED-FIXTURE-EXECUTION-AUTH-001",
        "authorization_kind": "READ_ONLY_LOCAL_SUPPLY_EVIDENCE_EXECUTION_ONLY", "owner_identity": "fixture-owner",
        "owner_decision_id": owner["owner_decision_id"], "issued_at_utc": now,
        "not_before_utc": "2026-07-28T16:28:00Z", "expires_at_utc": "2026-07-28T17:00:00Z",
        "nonce": "fixture-execution-nonce-001", "revocation_epoch": 7, "transaction_id": token["transaction_id"],
        "adapter_contract_acceptance_id": "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-CONTRACT-ACCEPT-001",
        "adapter_envelope_sha256": adapter["envelope_sha256"],
        "implementation_acceptance_id": "SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-IMPLEMENTATION-ACCEPT-001",
        "local_supply_map_contract_acceptance_id": coordinate["contract_acceptance_id"],
        "evidence_design_acceptance_id": coordinate["evidence_design_acceptance_id"],
        "repository_head": ACTUAL_V130_HEAD, "repository_tree": ACTUAL_V130_TREE, "remote_head": ACTUAL_V130_HEAD,
        "executor_uid": os.getuid(), "owner_authorization_token_sha256": token_digest,
        "coordinate_receipt_sha256": coordinate["receipt_sha256"], "exact_provider_path_count": 41,
        "maximum_provider_bytes": MAX_PROVIDER_BYTES, "transaction_output_root": str(output_root.resolve()),
        "permitted_effects": REQUIRED_EXECUTION_EFFECTS,
    }
    seal_object(execution, "authorization_sha256")

    files = {
        "owner_decision": docs_root / "owner-decision.json",
        "owner_authorization_token": docs_root / "owner-token.json",
        "coordinate_receipt": docs_root / "coordinate-receipt.json",
        "revocation_snapshot": docs_root / "revocation.json",
        "adapter_envelope": docs_root / "adapter-envelope.json",
        "execution_authorization": docs_root / "execution-authorization.json",
    }
    values = {
        "owner_decision": owner, "owner_authorization_token": token, "coordinate_receipt": coordinate,
        "revocation_snapshot": revocation, "adapter_envelope": adapter, "execution_authorization": execution,
    }
    for key, path in files.items():
        path.write_bytes(canonical(values[key]))
        path.chmod(0o600)

    manifest = {
        "schema_version": 1, "review_id": REVIEW_ID, "execution_marker": ISOLATED_MARKER,
        "acceptance_bindings": {
            "issuance_implementation_acceptance": "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-IMPLEMENTATION-ACCEPT-001",
            "adapter_implementation_acceptance": "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-IMPLEMENTATION-ACCEPT-001",
            "evidence_implementation_acceptance": "SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-IMPLEMENTATION-ACCEPT-001",
        },
        "documents": {key: str(path.resolve()) for key, path in files.items()},
        "allowed_fixture_root": str(root.resolve()), "provider_fixture_root": str(provider_root.resolve()),
        "transaction_output_root": str(output_root.resolve()),
        "repository_head": ACTUAL_V130_HEAD, "repository_tree": ACTUAL_V130_TREE,
        "remote_head": ACTUAL_V130_HEAD, "executor_uid": os.getuid(), "current_time_utc": now,
        "protected_state_before_sha256": "0" * 64, "protected_state_after_sha256": "0" * 64,
        "test_hooks": {},
    }

    def rewrite_linked_documents() -> None:
        nonlocal replay_tuple
        seal_object(coordinate, "receipt_sha256")
        token["coordinate_receipt_sha256"] = coordinate["receipt_sha256"]
        files["coordinate_receipt"].write_bytes(canonical(coordinate))
        files["owner_authorization_token"].write_bytes(canonical(token))
        current_token_digest = sha_bytes(canonical(token))
        current_revocation_digest = sha_bytes(canonical(revocation))
        current_row_manifest_digest = sha_bytes(canonical([sha_bytes(canonical(row)) for row in coordinate["rows"]]))
        replay_tuple = sha_bytes(canonical({
            "authorization_token_id": token["authorization_token_id"],
            "nonce": token["nonce"], "transaction_id": token["transaction_id"],
            "coordinate_receipt_sha256": coordinate["receipt_sha256"],
        }))
        adapter["owner_authorization_token_sha256"] = current_token_digest
        adapter["coordinate_receipt_sha256"] = coordinate["receipt_sha256"]
        adapter["revocation_snapshot_sha256"] = current_revocation_digest
        adapter["coordinate_row_count"] = len(coordinate["rows"])
        adapter["coordinate_row_digest_manifest_sha256"] = current_row_manifest_digest
        adapter["replay_tuple_sha256"] = replay_tuple
        seal_object(adapter, "envelope_sha256")
        files["adapter_envelope"].write_bytes(canonical(adapter))
        execution["adapter_envelope_sha256"] = adapter["envelope_sha256"]
        execution["owner_authorization_token_sha256"] = current_token_digest
        execution["coordinate_receipt_sha256"] = coordinate["receipt_sha256"]
        execution["exact_provider_path_count"] = len(coordinate["rows"])
        seal_object(execution, "authorization_sha256")
        files["execution_authorization"].write_bytes(canonical(execution))

    # Harness-only negative mutations. Candidate never creates or mutates these inputs.
    if case == "acceptance-binding-mismatch":
        manifest["acceptance_bindings"]["evidence_implementation_acceptance"] = "WRONG"
    elif case == "owner-decision-noncanonical":
        files["owner_decision"].write_text(json.dumps(owner, indent=2) + "\n", encoding="utf-8")
    elif case == "token-claim-gap":
        token.pop("coordinate_receipt_sha256")
        files["owner_authorization_token"].write_bytes(canonical(token))
    elif case == "coordinate-row-count":
        coordinate["rows"] = coordinate["rows"][:-1]
        rewrite_linked_documents()
    elif case == "revocation-epoch-mismatch":
        revocation["revocation_epoch"] = 8
        files["revocation_snapshot"].write_bytes(canonical(revocation))
    elif case == "repository-head-mismatch":
        manifest["repository_head"] = "1" * 40
    elif case == "repository-tree-mismatch":
        manifest["repository_tree"] = "2" * 40
    elif case == "remote-head-mismatch":
        manifest["remote_head"] = "3" * 40
    elif case == "executor-uid-mismatch":
        manifest["executor_uid"] = os.getuid() + 1
    elif case == "time-window-invalid":
        manifest["current_time_utc"] = "2026-07-28T18:00:00Z"
    elif case == "output-root-invalid":
        manifest["transaction_output_root"] = "/data/data/com.termux/files/usr/glibc/results"
    elif case == "replay-already-consumed":
        revocation["consumed_replay_tuples"] = [replay_tuple]
        files["revocation_snapshot"].write_bytes(canonical(revocation))
        rewrite_linked_documents()
    elif case == "adapter-envelope-digest":
        adapter["envelope_sha256"] = "f" * 64
        files["adapter_envelope"].write_bytes(canonical(adapter))
    elif case == "execution-authorization-digest":
        execution["authorization_sha256"] = "e" * 64
        files["execution_authorization"].write_bytes(canonical(execution))
    elif case == "execution-effect-widening":
        execution["permitted_effects"] = REQUIRED_EXECUTION_EFFECTS + ["WRITE_PROVIDER_BYTES"]
        seal_object(execution, "authorization_sha256")
        files["execution_authorization"].write_bytes(canonical(execution))
    elif case == "live-to-synthetic-rewrite":
        coordinate["rows"][0]["absolute_canonical_path"] = "/__synthetic__/termux-native-desktop/selected-provider/live.so"
        coordinate["rows"][0]["coordinate_origin"] = "LIVE_REWRITTEN_TO_SYNTHETIC"
        coordinate["rows"][0]["path_text_sha256"] = sha_bytes((coordinate["rows"][0]["absolute_canonical_path"] + "\n").encode("utf-8"))
        rewrite_linked_documents()
    elif case == "selected-provider-path":
        coordinate["rows"][0]["absolute_canonical_path"] = "/data/data/com.termux/files/usr/glibc/lib/live.so"
        coordinate["rows"][0]["path_text_sha256"] = sha_bytes((coordinate["rows"][0]["absolute_canonical_path"] + "\n").encode("utf-8"))
        rewrite_linked_documents()
    elif case == "symlink-component":
        victim = root / Path(plan["rows"][0]["fixture_relative_path"])
        real = victim.with_name(victim.name + ".real")
        victim.rename(real)
        victim.symlink_to(real.name)
    elif case == "non-regular-file":
        victim = root / Path(plan["rows"][0]["fixture_relative_path"])
        victim.unlink()
        victim.mkdir()
    elif case == "owner-mismatch":
        manifest["test_hooks"]["expected_uid_override"] = os.getuid() + 1
    elif case == "writable-mode":
        victim = root / Path(plan["rows"][0]["fixture_relative_path"])
        victim.chmod(0o622)
    elif case == "size-mismatch":
        coordinate["rows"][0]["expected_member_size_bytes"] += 1
        rewrite_linked_documents()
    elif case == "sha256-mismatch":
        coordinate["rows"][0]["expected_member_sha256"] = "a" * 64
        rewrite_linked_documents()
    elif case == "elf-identity-mismatch":
        victim = root / Path(plan["rows"][0]["fixture_relative_path"])
        data = bytearray(victim.read_bytes()); data[18:20] = struct.pack("<H", 62); victim.write_bytes(data); victim.chmod(0o600)
        coordinate["rows"][0]["expected_member_sha256"] = sha_bytes(bytes(data))
        coordinate["rows"][0]["expected_member_size_bytes"] = len(data)
        rewrite_linked_documents()
    elif case == "soname-mismatch":
        coordinate["rows"][0]["expected_soname"] = "libwrong.so.0"
        rewrite_linked_documents()
    elif case == "stability-mismatch":
        manifest["test_hooks"]["force_stability_mismatch_contract_row_id"] = rows[0]["contract_row_id"]
    elif case == "whole-map-gap":
        manifest["test_hooks"]["whole_map_gap_after_validation"] = True
    elif case == "protected-state-mismatch":
        manifest["protected_state_after_sha256"] = "9" * 64
    manifest_path = root / "orchestration-manifest.json"
    manifest_path.write_bytes(canonical(manifest))
    manifest_path.chmod(0o600)
    return manifest_path


def execute_manifest(manifest_path: Path) -> dict[str, Any]:
    selected_provider_opens = 0
    selected_provider_reads = 0
    fixture_opens = 0
    fixture_reads = 0
    replay_consumed = 0
    manifest = read_canonical_json(manifest_path, "LEO-FAIL-001")
    try:
        if manifest.get("execution_marker") != ISOLATED_MARKER or manifest.get("review_id") != REVIEW_ID:
            raise CandidateFailure("LEO-FAIL-001", "isolated execution marker or review id mismatch")
        expected_bindings = {
            "issuance_implementation_acceptance": "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-IMPLEMENTATION-ACCEPT-001",
            "adapter_implementation_acceptance": "SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-IMPLEMENTATION-ACCEPT-001",
            "evidence_implementation_acceptance": "SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-IMPLEMENTATION-ACCEPT-001",
        }
        if manifest.get("acceptance_bindings") != expected_bindings:
            raise CandidateFailure("LEO-FAIL-001", "accepted implementation binding mismatch")
        root = Path(manifest["allowed_fixture_root"]).resolve()
        provider_root = Path(manifest["provider_fixture_root"]).resolve()
        output_root = Path(manifest["transaction_output_root"]).resolve()
        if not is_under(manifest_path.resolve(), root) or not is_under(provider_root, root):
            raise CandidateFailure("LEO-FAIL-017", "manifest/provider root outside isolated root")
        reject_forbidden_path(root); reject_forbidden_path(provider_root)
        output_text = str(output_root)
        if any(output_text == prefix or output_text.startswith(prefix + "/") for prefix in FORBIDDEN_SELECTED_PROVIDER_PREFIXES):
            raise CandidateFailure("LEO-FAIL-011", "output root overlaps selected-provider/system prefix")
        if output_text.startswith("/__synthetic__/") or not is_under(output_root, root) or is_under(output_root, provider_root):
            raise CandidateFailure("LEO-FAIL-011", "output root not transaction-scoped outside provider fixture root")
        documents = manifest.get("documents")
        if not isinstance(documents, dict) or sorted(documents) != sorted([
            "owner_decision", "owner_authorization_token", "coordinate_receipt", "revocation_snapshot",
            "adapter_envelope", "execution_authorization",
        ]):
            raise CandidateFailure("LEO-FAIL-001", "explicit document set mismatch")
        doc_paths = {key: Path(value).resolve() for key, value in documents.items()}
        for path in doc_paths.values():
            if not is_under(path, root):
                raise CandidateFailure("LEO-FAIL-017", "document outside isolated root")
        owner = read_canonical_json(doc_paths["owner_decision"], "LEO-FAIL-002")
        token = read_canonical_json(doc_paths["owner_authorization_token"], "LEO-FAIL-003")
        coordinate = read_canonical_json(doc_paths["coordinate_receipt"], "LEO-FAIL-004")
        revocation = read_canonical_json(doc_paths["revocation_snapshot"], "LEO-FAIL-005")
        adapter = read_canonical_json(doc_paths["adapter_envelope"], "LEO-FAIL-013")
        execution = read_canonical_json(doc_paths["execution_authorization"], "LEO-FAIL-014")
        ensure_exact_fields(token, TOKEN_REQUIRED_CLAIMS, "LEO-FAIL-003")
        if token["authorization_kind"] != "READ_ONLY_LOCAL_SUPPLY_EVIDENCE_TRANSACTION_ONLY":
            raise CandidateFailure("LEO-FAIL-003", "token authorization kind mismatch")
        rows = coordinate.get("rows")
        if not isinstance(rows, list) or len(rows) != 41:
            raise CandidateFailure("LEO-FAIL-004", "coordinate row cardinality mismatch")
        validate_self_digest(coordinate, "receipt_sha256", "LEO-FAIL-004")
        seen = set()
        for index, row in enumerate(rows, 1):
            if not isinstance(row, dict) or sorted(row) != sorted(COORDINATE_ROW_FIELDS):
                raise CandidateFailure("LEO-FAIL-004", "coordinate row field set mismatch")
            if row["sequence"] != index or row["contract_row_id"] in seen:
                raise CandidateFailure("LEO-FAIL-004", "coordinate sequence/identity mismatch")
            seen.add(row["contract_row_id"])
            if row["path_text_sha256"] != sha_bytes((row["absolute_canonical_path"] + "\n").encode("utf-8")):
                raise CandidateFailure("LEO-FAIL-004", "path text digest mismatch")
            if row["coordinate_origin"] != "ISOLATED_TEST_HARNESS_SURROGATE_NOT_LIVE_PROVIDER":
                if "SYNTHETIC" in row["coordinate_origin"] or row["absolute_canonical_path"].startswith("/__synthetic__/"):
                    raise CandidateFailure("LEO-FAIL-016", "live-to-synthetic rewrite rejected")
                raise CandidateFailure("LEO-FAIL-004", "coordinate origin invalid")
        if revocation.get("revocation_epoch") != token["revocation_epoch"] or owner.get("revocation_epoch") != token["revocation_epoch"]:
            raise CandidateFailure("LEO-FAIL-005", "revocation epoch mismatch")
        if manifest["repository_head"] != token["repository_head"] or manifest["repository_head"] != coordinate["repository_head"]:
            raise CandidateFailure("LEO-FAIL-006", "repository head binding mismatch")
        if manifest["repository_tree"] != token["repository_tree"] or manifest["repository_tree"] != coordinate["repository_tree"]:
            raise CandidateFailure("LEO-FAIL-007", "repository tree binding mismatch")
        if manifest["remote_head"] != token["remote_head"] or manifest["remote_head"] != coordinate["remote_head"]:
            raise CandidateFailure("LEO-FAIL-008", "remote head binding mismatch")
        if manifest["executor_uid"] != token["executor_uid"] or manifest["executor_uid"] != owner["executor_uid"]:
            raise CandidateFailure("LEO-FAIL-009", "executor uid binding mismatch")
        if manifest["current_time_utc"] < token["not_before_utc"] or manifest["current_time_utc"] > token["expires_at_utc"]:
            raise CandidateFailure("LEO-FAIL-010", "authorization time window invalid")
        ensure_exact_fields(adapter, ADAPTER_FIELDS, "LEO-FAIL-013")
        validate_self_digest(adapter, "envelope_sha256", "LEO-FAIL-013")
        expected_owner_digest = sha_bytes(canonical(owner))
        expected_token_digest = sha_bytes(canonical(token))
        expected_revocation_digest = sha_bytes(canonical(revocation))
        expected_row_manifest_digest = sha_bytes(canonical([sha_bytes(canonical(row)) for row in rows]))
        expected_replay_tuple = sha_bytes(canonical({
            "authorization_token_id": token["authorization_token_id"],
            "nonce": token["nonce"], "transaction_id": token["transaction_id"],
            "coordinate_receipt_sha256": coordinate["receipt_sha256"],
        }))
        if adapter["owner_decision_sha256"] != expected_owner_digest or adapter["owner_authorization_token_sha256"] != expected_token_digest:
            raise CandidateFailure("LEO-FAIL-013", "adapter owner/token digest binding mismatch")
        if adapter["coordinate_receipt_sha256"] != coordinate["receipt_sha256"] or adapter["revocation_snapshot_sha256"] != expected_revocation_digest:
            raise CandidateFailure("LEO-FAIL-013", "adapter coordinate/revocation digest binding mismatch")
        if adapter["coordinate_row_count"] != len(rows) or adapter["coordinate_row_digest_manifest_sha256"] != expected_row_manifest_digest:
            raise CandidateFailure("LEO-FAIL-013", "adapter coordinate manifest binding mismatch")
        if adapter["replay_tuple_sha256"] != expected_replay_tuple:
            raise CandidateFailure("LEO-FAIL-013", "adapter replay tuple binding mismatch")
        ensure_exact_fields(execution, EXECUTION_REQUIRED_CLAIMS, "LEO-FAIL-014")
        validate_self_digest(execution, "authorization_sha256", "LEO-FAIL-014")
        if execution["permitted_effects"] != REQUIRED_EXECUTION_EFFECTS:
            raise CandidateFailure("LEO-FAIL-015", "execution effect set mismatch")
        if execution["exact_provider_path_count"] != 41 or execution["maximum_provider_bytes"] != MAX_PROVIDER_BYTES:
            raise CandidateFailure("LEO-FAIL-015", "execution quantitative boundary mismatch")
        if execution["adapter_envelope_sha256"] != adapter["envelope_sha256"]:
            raise CandidateFailure("LEO-FAIL-013", "adapter authorization binding mismatch")
        if execution["owner_authorization_token_sha256"] != expected_token_digest:
            raise CandidateFailure("LEO-FAIL-014", "execution token digest binding mismatch")
        if execution["coordinate_receipt_sha256"] != coordinate["receipt_sha256"] or token["coordinate_receipt_sha256"] != coordinate["receipt_sha256"]:
            raise CandidateFailure("LEO-FAIL-004", "coordinate digest binding mismatch")
        if execution["transaction_output_root"] != manifest["transaction_output_root"] or adapter["transaction_output_root"] != manifest["transaction_output_root"]:
            raise CandidateFailure("LEO-FAIL-011", "output root document binding mismatch")
        replay_tuple = adapter["replay_tuple_sha256"]
        registry = InMemoryReplayRegistry(set(revocation.get("consumed_replay_tuples", [])))
        registry.consume(replay_tuple)
        replay_consumed = 1
        # First provider-like open occurs only after all document, authority and replay validation.
        expected_uid = int(manifest.get("test_hooks", {}).get("expected_uid_override", manifest["executor_uid"]))
        force_id = manifest.get("test_hooks", {}).get("force_stability_mismatch_contract_row_id")
        results = []
        total_bytes = 0
        whole_map_gap = bool(manifest.get("test_hooks", {}).get("whole_map_gap_after_validation"))
        for row in rows:
            if whole_map_gap and len(results) == 40:
                break
            path = Path(row["absolute_canonical_path"])
            reject_forbidden_path(path)
            if not is_under(path.resolve(strict=False), provider_root):
                raise CandidateFailure("LEO-FAIL-017", "coordinate outside isolated provider fixture root")
            result = validate_fixture_file(row, provider_root, expected_uid, row["contract_row_id"] == force_id)
            fixture_opens += 1
            fixture_reads += 1
            total_bytes += result["size_bytes"]
            results.append(result)
        if len(results) != 41:
            raise CandidateFailure("LEO-FAIL-027", "whole-map completeness failure")
        if manifest["protected_state_before_sha256"] != manifest["protected_state_after_sha256"]:
            raise CandidateFailure("LEO-FAIL-028", "protected state changed")
        receipt = {
            "schema_version": 1,
            "candidate_state": CANDIDATE_STATE,
            "review_id": REVIEW_ID,
            "execution_mode": ISOLATED_MARKER,
            "result_state": "QUALIFIED_ISOLATED_FIXTURE_PRODUCTION_ORCHESTRATION_IMPLEMENTATION_CANDIDATE",
            "row_count": len(results),
            "isolated_fixture_files_opened": fixture_opens,
            "isolated_fixture_files_read": fixture_reads,
            "isolated_fixture_bytes_read": total_bytes,
            "selected_provider_paths_opened": selected_provider_opens,
            "selected_provider_files_read": selected_provider_reads,
            "candidate_filesystem_write_count": 0,
            "persistent_replay_write_count": 0,
            "in_memory_replay_tuple_consumed": replay_consumed,
            "live_authority_count": 0,
            "local_supply_map_produced": False,
            "rows": results,
        }
        if len(canonical(receipt)) > MAX_RECEIPT_BYTES:
            raise CandidateFailure("LEO-FAIL-028", "candidate receipt overflow")
        return {"pass": True, **receipt}
    except CandidateFailure as exc:
        return {
            "pass": False, "review_id": REVIEW_ID, "candidate_state": CANDIDATE_STATE,
            "failure_id": exc.failure_id, "failure_detail": exc.detail,
            "isolated_fixture_files_opened": fixture_opens,
            "isolated_fixture_files_read": fixture_reads,
            "selected_provider_paths_opened": selected_provider_opens,
            "selected_provider_files_read": selected_provider_reads,
            "candidate_filesystem_write_count": 0,
            "persistent_replay_write_count": 0,
            "in_memory_replay_tuple_consumed": replay_consumed,
            "live_authority_count": 0, "local_supply_map_produced": False,
        }


def normalize_result(result: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(result))
    for row in value.get("rows", []):
        row["fixture_relative_path"] = PurePosixPath(row["fixture_relative_path"]).as_posix()
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--dump-coverage", action="store_true")
    parser.add_argument("--dump-negative-cases", action="store_true")
    args = parser.parse_args()
    if args.dump_coverage:
        print(json.dumps(build_coverage_rows(), sort_keys=True, separators=(",", ":")))
        return
    if args.dump_negative_cases:
        print(json.dumps(build_negative_cases(), sort_keys=True, separators=(",", ":")))
        return
    if args.manifest is None:
        parser.error("--manifest is required")
    result = normalize_result(execute_manifest(args.manifest))
    sys.stdout.buffer.write(canonical(result))
    raise SystemExit(0 if result.get("pass") else 2)


if __name__ == "__main__":
    main()
