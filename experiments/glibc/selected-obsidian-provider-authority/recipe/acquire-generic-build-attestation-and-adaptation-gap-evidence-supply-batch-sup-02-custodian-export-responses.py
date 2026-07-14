#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import stat
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, NoReturn

EXPECTED_REQUESTS = 28
EXPECTED_RECORD_CONTRACTS = 84
RECORDS_PER_RESPONSE = 3
MANIFEST_NAME = "custodian-export-response-manifest.tsv"
CLAIM_BOUNDARY = "CANDIDATE_CUSTODIAN_EXPORT_RESPONSE_REVIEW_REQUIRED_NO_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT"
NEXT_STATE = "REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSE_ACQUISITION_RECEIPT"
MAX_FILE_SIZE = 64 * 1024 * 1024
MAX_TOTAL_SIZE = 512 * 1024 * 1024
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_OID_RE = re.compile(r"^[0-9a-f]{40}$")
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
MANIFEST_FIELDS = [
    "response_record_id",
    "request_id",
    "root_review_id",
    "recipe_root",
    "recipe_tree",
    "record_name",
    "relative_path",
    "sha256",
    "size_bytes",
    "custodian_identity",
    "immutable_locator_or_signed_envelope",
    "claim_boundary",
]
REQUEST_STATUS_FIELDS = [
    "request_id",
    "root_review_id",
    "recipe_root",
    "recipe_tree",
    "issued_request_locator",
    "response_drop_locator",
    "response_state",
    "verified_record_count",
    "build_run_id",
    "custodian_identity",
    "immutable_locator_or_signed_envelope",
    "candidate_response_path",
    "build_attestation_state",
    "claim_boundary",
    "next_action",
]
RECORD_INVENTORY_FIELDS = [
    "response_record_id",
    "request_id",
    "requirement_id",
    "record_name",
    "record_format",
    "source_relative_path",
    "candidate_relative_path",
    "sha256",
    "size_bytes",
    "format_validation",
    "build_run_id",
    "custodian_identity",
    "immutable_locator_or_signed_envelope",
    "acceptance_state",
    "claim_boundary",
]


def fail(message: str) -> NoReturn:
    raise SystemExit(f"SUP-02 custodian-export response acquirer: FAIL: {message}")


def read_tsv(path: Path, expected_fields: list[str] | None = None) -> list[dict[str, str]]:
    if not path.is_file() or path.is_symlink():
        fail(f"missing regular TSV: {path}")
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if not reader.fieldnames:
            fail(f"missing TSV header: {path}")
        if expected_fields is not None and reader.fieldnames != expected_fields:
            fail(f"TSV header drift: {path}")
        return [{key: value or "" for key, value in row.items()} for row in reader]


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def nonempty(value: Any) -> bool:
    if value is None or value == "":
        return False
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def safe_relative_path(value: str) -> Path:
    candidate = Path(value)
    if not value or candidate.is_absolute() or ".." in candidate.parts:
        fail(f"unsafe relative path: {value!r}")
    if any(part in {"", "."} for part in candidate.parts):
        fail(f"non-canonical relative path: {value!r}")
    return candidate


def safe_text(value: Any, label: str, limit: int = 8192) -> str:
    if not isinstance(value, str) or not value or len(value) > limit or any(ord(ch) < 32 for ch in value):
        fail(f"invalid {label}")
    return value


def validate_sha(value: str, label: str) -> None:
    if not SHA256_RE.fullmatch(value):
        fail(f"invalid SHA-256 for {label}")


def validate_git_oid(value: str, label: str) -> None:
    if not GIT_OID_RE.fullmatch(value):
        fail(f"invalid Git object ID for {label}")


def verify_issuance(
    requests: list[dict[str, str]], contracts: list[dict[str, str]]
) -> tuple[dict[str, dict[str, str]], dict[tuple[str, str], dict[str, str]]]:
    if len(requests) != EXPECTED_REQUESTS:
        fail("request denominator drift")
    if len(contracts) != EXPECTED_RECORD_CONTRACTS:
        fail("record-contract denominator drift")
    request_by_id: dict[str, dict[str, str]] = {}
    for row in requests:
        request_id = row.get("request_id", "")
        if not SAFE_ID_RE.fullmatch(request_id) or request_id in request_by_id:
            fail(f"invalid or duplicate request ID: {request_id!r}")
        if row.get("batch_id") != "SUP-02":
            fail(f"batch drift: {request_id}")
        if row.get("requirement_ids") != "BA-001;BA-002;BA-003":
            fail(f"requirement-set drift: {request_id}")
        if row.get("request_state") != "REQUEST_ISSUED_REPOSITORY_PUBLICATION":
            fail(f"request not issued: {request_id}")
        if row.get("acknowledgement_state") != "NOT_ACKNOWLEDGED":
            fail(f"unexpected acknowledgement state: {request_id}")
        if row.get("responses_received") != "0" or row.get("build_attestations_accepted") != "0":
            fail(f"pre-existing response or attestation effect: {request_id}")
        if row.get("required_record_names") != "build-invocation-record.json;build-environment-record.json;build-output-manifest.tsv":
            fail(f"required record-name drift: {request_id}")
        if row.get("claim_boundary") != "CUSTODIAN_EXPORT_REQUEST_ISSUANCE_ONLY_NO_RESPONSE_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT":
            fail(f"issuance claim drift: {request_id}")
        validate_git_oid(row.get("recipe_tree", ""), f"recipe tree {request_id}")
        safe_text(row.get("root_review_id"), f"root review ID {request_id}")
        safe_text(row.get("recipe_root"), f"recipe root {request_id}")
        safe_text(row.get("response_drop_locator"), f"response drop locator {request_id}")
        request_by_id[request_id] = row

    contract_by_key: dict[tuple[str, str], dict[str, str]] = {}
    count_by_request: Counter[str] = Counter()
    req_counts: Counter[str] = Counter()
    for row in contracts:
        key = (row.get("request_id", ""), row.get("record_name", ""))
        if key in contract_by_key:
            fail(f"duplicate record contract: {key}")
        request = request_by_id.get(key[0])
        if request is None:
            fail(f"orphan record contract: {key}")
        if row.get("root_review_id") != request["root_review_id"] or row.get("recipe_root") != request["recipe_root"] or row.get("recipe_tree") != request["recipe_tree"]:
            fail(f"record contract request binding drift: {key}")
        if row.get("record_state") != "ISSUED_REQUIRED_NOT_SUPPLIED" or row.get("acceptance_state") != "OPEN_NO_ACCEPTANCE":
            fail(f"record contract state drift: {key}")
        if row.get("record_name") not in {"build-invocation-record.json", "build-environment-record.json", "build-output-manifest.tsv"}:
            fail(f"unknown record contract: {key}")
        expected_format = "TSV_WITH_ROWS" if row["record_name"].endswith(".tsv") else "JSON_OBJECT"
        if row.get("record_format") != expected_format:
            fail(f"record format drift: {key}")
        if not row.get("mandatory_fields") or not row.get("cross_record_binding"):
            fail(f"empty record contract fields: {key}")
        contract_by_key[key] = row
        count_by_request[key[0]] += 1
        req_counts[row.get("requirement_id", "")] += 1
    if any(count_by_request[request_id] != RECORDS_PER_RESPONSE for request_id in request_by_id):
        fail("per-request record-contract denominator drift")
    if req_counts != Counter({"BA-001": 28, "BA-002": 28, "BA-003": 28}):
        fail("requirement record-contract denominator drift")
    return request_by_id, contract_by_key


def inspect_response_root(input_root: Path, known_requests: set[str]) -> dict[str, Path]:
    if not input_root.exists():
        return {}
    if not input_root.is_dir() or input_root.is_symlink():
        fail(f"unsafe response input root: {input_root}")
    found: dict[str, Path] = {}
    for entry in sorted(input_root.iterdir(), key=lambda path: path.name):
        mode = entry.lstat().st_mode
        if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
            fail(f"unexpected non-directory response-root member: {entry.name}")
        if entry.name not in known_requests:
            fail(f"unknown request response directory: {entry.name}")
        found[entry.name] = entry
    return found


def inspect_response_dir(response_dir: Path, manifest_paths: set[str]) -> None:
    actual_files: set[str] = set()
    for current, dirnames, filenames in os.walk(response_dir, topdown=True, followlinks=False):
        current_path = Path(current)
        for dirname in list(dirnames):
            path = current_path / dirname
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
                fail(f"unsafe response directory member: {path.relative_to(response_dir)}")
        for filename in filenames:
            path = current_path / filename
            rel = path.relative_to(response_dir).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
                fail(f"unsafe response file member: {rel}")
            if rel != MANIFEST_NAME:
                actual_files.add(rel)
    if actual_files != manifest_paths:
        missing = sorted(manifest_paths - actual_files)
        extra = sorted(actual_files - manifest_paths)
        fail(f"response manifest/file-set mismatch missing={missing} extra={extra}")


def validate_json_record(path: Path, contract: dict[str, str], request: dict[str, str]) -> tuple[dict[str, Any], str]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON record {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"JSON record is not an object: {path}")
    for field in contract["mandatory_fields"].split(";"):
        if field not in value or not nonempty(value[field]):
            fail(f"missing mandatory JSON field {field}: {path}")
    for field, expected in (
        ("request_id", request["request_id"]),
        ("root_review_id", request["root_review_id"]),
        ("recipe_tree", request["recipe_tree"]),
    ):
        if value.get(field) != expected:
            fail(f"JSON request binding mismatch {field}: {path}")
    if "recipe_root" in value and value["recipe_root"] != request["recipe_root"]:
        fail(f"JSON recipe-root mismatch: {path}")
    build_run_id = safe_text(value.get("build_run_id"), f"build_run_id in {path.name}")
    safe_text(value.get("custodian_identity"), f"custodian identity in {path.name}")
    safe_text(value.get("immutable_locator_or_signed_envelope"), f"immutable locator in {path.name}")
    if path.name == "build-invocation-record.json":
        argv = value.get("invocation_argv")
        if not isinstance(argv, list) or not argv or not all(isinstance(item, str) and item for item in argv):
            fail("invocation_argv must be a non-empty string list")
    if path.name == "build-environment-record.json":
        components = value.get("toolchain_components")
        digests = value.get("toolchain_digests")
        if not isinstance(components, (list, dict)) or not components:
            fail("toolchain_components must be non-empty")
        if not isinstance(digests, (list, dict)) or not digests:
            fail("toolchain_digests must be non-empty")
    return value, build_run_id


def validate_tsv_record(path: Path, contract: dict[str, str], request: dict[str, str]) -> tuple[list[dict[str, str]], str, str, str]:
    expected_fields = contract["mandatory_fields"].split(";")
    rows = read_tsv(path, expected_fields)
    if not rows:
        fail(f"output manifest has no rows: {path}")
    common_build_run = ""
    common_custodian = ""
    common_locator = ""
    for index, row in enumerate(rows, 1):
        for field in expected_fields:
            if not row[field]:
                fail(f"empty output-manifest field {field} row {index}")
        for field, expected in (
            ("request_id", request["request_id"]),
            ("root_review_id", request["root_review_id"]),
            ("recipe_root", request["recipe_root"]),
            ("recipe_tree", request["recipe_tree"]),
        ):
            if row[field] != expected:
                fail(f"output-manifest request binding mismatch {field} row {index}")
        validate_sha(row["artifact_sha256"], f"artifact row {index}")
        validate_sha(row["member_sha256"], f"member row {index}")
        safe_relative_path(row["artifact_path"])
        safe_relative_path(row["member_path"])
        for field in ("build_run_id", "custodian_identity", "immutable_locator_or_signed_envelope"):
            safe_text(row[field], f"{field} row {index}")
        if index == 1:
            common_build_run = row["build_run_id"]
            common_custodian = row["custodian_identity"]
            common_locator = row["immutable_locator_or_signed_envelope"]
        elif (row["build_run_id"], row["custodian_identity"], row["immutable_locator_or_signed_envelope"]) != (common_build_run, common_custodian, common_locator):
            fail("output-manifest cross-row producing-build binding drift")
    return rows, common_build_run, common_custodian, common_locator


def acquire_response(
    response_dir: Path,
    request: dict[str, str],
    contract_by_key: dict[tuple[str, str], dict[str, str]],
    candidate_root: Path,
) -> tuple[dict[str, str], list[dict[str, str]], int]:
    manifest = response_dir / MANIFEST_NAME
    rows = read_tsv(manifest, MANIFEST_FIELDS)
    if len(rows) != RECORDS_PER_RESPONSE:
        fail(f"response manifest must contain exactly three rows: {request['request_id']}")
    row_by_name: dict[str, dict[str, str]] = {}
    manifest_paths: set[str] = set()
    seen_record_ids: set[str] = set()
    total_size = 0
    for row in rows:
        record_id = row["response_record_id"]
        if not SAFE_ID_RE.fullmatch(record_id) or record_id in seen_record_ids:
            fail(f"invalid or duplicate response_record_id: {record_id!r}")
        seen_record_ids.add(record_id)
        if row["request_id"] != request["request_id"] or row["root_review_id"] != request["root_review_id"] or row["recipe_root"] != request["recipe_root"] or row["recipe_tree"] != request["recipe_tree"]:
            fail(f"response manifest request binding drift: {record_id}")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            fail(f"response claim-boundary drift: {record_id}")
        record_name = row["record_name"]
        if record_name in row_by_name or (request["request_id"], record_name) not in contract_by_key:
            fail(f"duplicate or unknown response record: {record_name}")
        rel = safe_relative_path(row["relative_path"])
        if rel.as_posix() != record_name:
            fail(f"response record path must equal canonical record name: {record_name}")
        if rel.as_posix() in manifest_paths:
            fail(f"duplicate response relative path: {rel}")
        manifest_paths.add(rel.as_posix())
        validate_sha(row["sha256"], record_id)
        try:
            size = int(row["size_bytes"])
        except ValueError:
            fail(f"invalid size: {record_id}")
        if size <= 0 or size > MAX_FILE_SIZE:
            fail(f"response file size outside bound: {record_id}")
        total_size += size
        if total_size > MAX_TOTAL_SIZE:
            fail("response byte total outside bound")
        safe_text(row["custodian_identity"], f"manifest custodian {record_id}")
        safe_text(row["immutable_locator_or_signed_envelope"], f"manifest locator {record_id}")
        row_by_name[record_name] = row
    expected_names = {name for req_id, name in contract_by_key if req_id == request["request_id"]}
    if set(row_by_name) != expected_names:
        fail(f"response record-name set mismatch: {request['request_id']}")
    inspect_response_dir(response_dir, manifest_paths)

    record_inventory: list[dict[str, str]] = []
    common: tuple[str, str, str] | None = None
    candidate_dir = candidate_root / request["request_id"]
    candidate_dir.mkdir(parents=True, exist_ok=False)
    for record_name in sorted(row_by_name):
        row = row_by_name[record_name]
        source = response_dir / row["relative_path"]
        if not source.is_file() or source.is_symlink():
            fail(f"missing regular response record: {source}")
        if source.stat().st_size != int(row["size_bytes"]) or sha256(source) != row["sha256"]:
            fail(f"response record digest or size mismatch: {source}")
        contract = contract_by_key[(request["request_id"], record_name)]
        if contract["record_format"] == "JSON_OBJECT":
            value, build_run_id = validate_json_record(source, contract, request)
            custodian = safe_text(value["custodian_identity"], f"record custodian {record_name}")
            locator = safe_text(value["immutable_locator_or_signed_envelope"], f"record locator {record_name}")
            validation = "VALID_JSON_OBJECT_CONTRACT_BOUND"
        else:
            _rows, build_run_id, custodian, locator = validate_tsv_record(source, contract, request)
            validation = "VALID_TSV_WITH_ROWS_CONTRACT_BOUND"
        if row["custodian_identity"] != custodian or row["immutable_locator_or_signed_envelope"] != locator:
            fail(f"manifest-to-record custodian or locator mismatch: {record_name}")
        binding = (build_run_id, custodian, locator)
        if common is None:
            common = binding
        elif binding != common:
            fail(f"cross-record producing-build binding drift: {request['request_id']}")
        destination = candidate_dir / record_name
        shutil.copyfile(source, destination)
        if destination.stat().st_size != source.stat().st_size or sha256(destination) != row["sha256"]:
            fail(f"post-copy verification failed: {record_name}")
        destination.chmod(0o444)
        record_inventory.append({
            "response_record_id": row["response_record_id"],
            "request_id": request["request_id"],
            "requirement_id": contract["requirement_id"],
            "record_name": record_name,
            "record_format": contract["record_format"],
            "source_relative_path": f"{request['request_id']}/{row['relative_path']}",
            "candidate_relative_path": f"candidate-response-root/{request['request_id']}/{record_name}",
            "sha256": row["sha256"],
            "size_bytes": row["size_bytes"],
            "format_validation": validation,
            "build_run_id": build_run_id,
            "custodian_identity": custodian,
            "immutable_locator_or_signed_envelope": locator,
            "acceptance_state": "CANDIDATE_RESPONSE_ACQUIRED_REVIEW_REQUIRED_NO_ACCEPTANCE",
            "claim_boundary": CLAIM_BOUNDARY,
        })
    assert common is not None
    copied_manifest = candidate_dir / MANIFEST_NAME
    shutil.copyfile(manifest, copied_manifest)
    if sha256(copied_manifest) != sha256(manifest):
        fail("post-copy response manifest verification failed")
    copied_manifest.chmod(0o444)
    request_status = {
        "request_id": request["request_id"],
        "root_review_id": request["root_review_id"],
        "recipe_root": request["recipe_root"],
        "recipe_tree": request["recipe_tree"],
        "issued_request_locator": request["issued_request_locator"],
        "response_drop_locator": request["response_drop_locator"],
        "response_state": "COMPLETE_CANDIDATE_RESPONSE_ACQUIRED_REVIEW_REQUIRED",
        "verified_record_count": "3",
        "build_run_id": common[0],
        "custodian_identity": common[1],
        "immutable_locator_or_signed_envelope": common[2],
        "candidate_response_path": f"candidate-response-root/{request['request_id']}/",
        "build_attestation_state": "OPEN_NO_ACCEPTANCE",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": "REVIEW_EXACT_CANDIDATE_CUSTODIAN_EXPORT_RESPONSE",
    }
    return request_status, record_inventory, total_size


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-issuance", required=True, type=Path)
    parser.add_argument("--record-contract-issuance", required=True, type=Path)
    parser.add_argument("--input-root", required=True, type=Path)
    parser.add_argument("--source-head", required=True)
    parser.add_argument("--source-tree", required=True)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    validate_git_oid(args.source_head, "source HEAD")
    validate_git_oid(args.source_tree, "source tree")
    if args.out.exists() or args.out.is_symlink():
        fail(f"refusing existing output: {args.out}")

    requests = read_tsv(args.request_issuance)
    contracts = read_tsv(args.record_contract_issuance)
    request_by_id, contract_by_key = verify_issuance(requests, contracts)
    response_dirs = inspect_response_root(args.input_root, set(request_by_id))

    args.out.mkdir(parents=True)
    candidate_root = args.out / "candidate-response-root"
    candidate_root.mkdir()
    request_status_rows: list[dict[str, str]] = []
    record_inventory_rows: list[dict[str, str]] = []
    total_bytes = 0
    for request_id in sorted(request_by_id):
        request = request_by_id[request_id]
        response_dir = response_dirs.get(request_id)
        if response_dir is None:
            request_status_rows.append({
                "request_id": request_id,
                "root_review_id": request["root_review_id"],
                "recipe_root": request["recipe_root"],
                "recipe_tree": request["recipe_tree"],
                "issued_request_locator": request["issued_request_locator"],
                "response_drop_locator": request["response_drop_locator"],
                "response_state": "NO_RESPONSE_DROP_PRESENT",
                "verified_record_count": "0",
                "build_run_id": "-",
                "custodian_identity": "-",
                "immutable_locator_or_signed_envelope": "-",
                "candidate_response_path": "-",
                "build_attestation_state": "OPEN_NO_ACCEPTANCE",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_action": "AWAIT_EXACT_CUSTODIAN_EXPORT_RESPONSE",
            })
            continue
        status, inventory, acquired_bytes = acquire_response(response_dir, request, contract_by_key, candidate_root)
        request_status_rows.append(status)
        record_inventory_rows.extend(inventory)
        total_bytes += acquired_bytes
        if total_bytes > MAX_TOTAL_SIZE:
            fail("acquired response byte total outside bound")

    complete = sum(row["response_state"] == "COMPLETE_CANDIDATE_RESPONSE_ACQUIRED_REVIEW_REQUIRED" for row in request_status_rows)
    absent = EXPECTED_REQUESTS - complete
    write_tsv(args.out / "request-response-acquisition-status.tsv", REQUEST_STATUS_FIELDS, request_status_rows)
    write_tsv(args.out / "response-record-inventory.tsv", RECORD_INVENTORY_FIELDS, record_inventory_rows)
    write_tsv(args.out / "summary.tsv", ["field", "value"], [
        {"field": "source_head", "value": args.source_head},
        {"field": "source_tree", "value": args.source_tree},
        {"field": "request_issuance_sha256", "value": sha256(args.request_issuance)},
        {"field": "record_contract_issuance_sha256", "value": sha256(args.record_contract_issuance)},
        {"field": "response_input_root_state", "value": "PRESENT" if args.input_root.exists() else "ABSENT"},
        {"field": "issued_requests", "value": str(EXPECTED_REQUESTS)},
        {"field": "issued_record_contracts", "value": str(EXPECTED_RECORD_CONTRACTS)},
        {"field": "complete_candidate_responses_acquired", "value": str(complete)},
        {"field": "requests_without_response", "value": str(absent)},
        {"field": "verified_response_records", "value": str(len(record_inventory_rows))},
        {"field": "verified_response_bytes", "value": str(total_bytes)},
        {"field": "requests_acknowledged", "value": "0"},
        {"field": "responses_accepted", "value": "0"},
        {"field": "build_attestations_accepted", "value": "0"},
        {"field": "final_provider_decisions_accepted", "value": "0"},
        {"field": "target_rows_populated", "value": "0"},
        {"field": "claim_boundary", "value": CLAIM_BOUNDARY},
        {"field": "next_state", "value": NEXT_STATE},
    ])
    (args.out / "analysis.status").write_text("PASS\n", encoding="utf-8")
    (args.out / "claim-boundary.txt").write_text(CLAIM_BOUNDARY + "\n", encoding="utf-8")
    (args.out / "next-state.txt").write_text(NEXT_STATE + "\n", encoding="utf-8")
    print("SUP_02_CUSTODIAN_EXPORT_RESPONSE_ACQUIRER=PASS_BOUNDED")
    print(f"COMPLETE_CANDIDATE_RESPONSES_ACQUIRED={complete}")
    print(f"REQUESTS_WITHOUT_RESPONSE={absent}")
    print(f"VERIFIED_RESPONSE_RECORDS={len(record_inventory_rows)}")
    print("BUILD_ATTESTATIONS_ACCEPTED=0")


if __name__ == "__main__":
    main()
