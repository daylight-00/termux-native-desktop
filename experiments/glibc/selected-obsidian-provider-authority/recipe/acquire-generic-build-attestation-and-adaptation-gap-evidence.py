#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import shutil
import stat
from collections import defaultdict
from pathlib import Path
from typing import Iterable, NoReturn

EXPECTED_SOURCE_CONTRACTS = 10
EXPECTED_LANES = 6
EXPECTED_REQUIREMENTS = 16
EXPECTED_ROOTS = 28
EXPECTED_OBJECTS = 37
EXPECTED_DIRECT_GAPS = 10
EXPECTED_LOCAL_FOUNDATIONS = 6
CLAIM_BOUNDARY = "CANDIDATE_EVIDENCE_REVIEW_REQUIRED_NO_AUTHORITY_EFFECT"
AUTHORITY_STATE = "OPEN_NO_ACCEPTANCE"
TARGET_STATE = "UNPOPULATED"
FINAL_PROVIDER_STATE = "UNRESOLVED"
INPUT_MANIFEST_NAME = "acquisition-input-manifest.tsv"
INPUT_FIELDS = [
    "input_id",
    "acquisition_unit_id",
    "requirement_id",
    "lane_id",
    "scope_kind",
    "scope_id",
    "source_kind",
    "acquisition_mode",
    "locator_class",
    "source_locator",
    "relative_path",
    "sha256",
    "size_bytes",
    "evidence_class",
    "claim_boundary",
]
EVIDENCE_FIELDS = [
    "evidence_id",
    "requirement_id",
    "lane_id",
    "scope_kind",
    "scope_id",
    "evidence_class",
    "source_kind",
    "source_locator",
    "relative_path",
    "sha256",
    "size_bytes",
    "claim_boundary",
]
MAX_INPUT_FILES = 256
MAX_FILE_SIZE = 64 * 1024 * 1024
MAX_TOTAL_SIZE = 512 * 1024 * 1024
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
SAFE_CLASS = re.compile(r"^[A-Z0-9][A-Z0-9_:-]{1,127}$")


def fail(message: str) -> NoReturn:
    raise SystemExit(f"generic gap evidence acquirer: FAIL: {message}")


def read_tsv(path: Path, expected_fields: list[str] | None = None) -> list[dict[str, str]]:
    if not path.is_file() or path.is_symlink():
        fail(f"missing regular input: {path}")
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if not reader.fieldnames:
            fail(f"missing header: {path}")
        if expected_fields is not None and reader.fieldnames != expected_fields:
            fail(f"header drift: {path}")
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


def split_set(value: str) -> set[str]:
    return {item for item in value.split(";") if item and item != "NONE"}


def join_set(values: Iterable[str]) -> str:
    result = sorted({value for value in values if value})
    return ";".join(result) if result else "NONE"


def unique(rows: list[dict[str, str]], key: str, label: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row.get(key, "")
        if not value or value in result:
            fail(f"{label} duplicate or empty {key}: {value!r}")
        result[value] = row
    return result


def safe_relative_path(value: str) -> Path:
    candidate = Path(value)
    if not value or candidate.is_absolute() or ".." in candidate.parts or value.startswith("/"):
        fail(f"unsafe relative path: {value!r}")
    if any(part in {"", "."} for part in candidate.parts):
        fail(f"non-canonical relative path: {value!r}")
    return candidate


def ensure_plain_text(value: str, label: str, max_len: int = 4096) -> None:
    if not value or len(value) > max_len or any(ord(ch) < 32 for ch in value):
        fail(f"invalid {label}")


def allowed_source_kinds(requirement: dict[str, str]) -> set[str]:
    return {requirement["primary_source_kind"]} | split_set(requirement["alternate_source_kinds"])


def verify_canonical_inputs(
    contracts: list[dict[str, str]],
    lanes: list[dict[str, str]],
    requirements: list[dict[str, str]],
    roots: list[dict[str, str]],
    objects: list[dict[str, str]],
) -> tuple[
    dict[str, dict[str, str]],
    dict[str, dict[str, str]],
    dict[str, dict[str, str]],
    dict[str, dict[str, str]],
    dict[str, dict[str, str]],
]:
    if len(contracts) != EXPECTED_SOURCE_CONTRACTS:
        fail("source contract denominator drift")
    if len(lanes) != EXPECTED_LANES:
        fail("lane denominator drift")
    if len(requirements) != EXPECTED_REQUIREMENTS:
        fail("requirement denominator drift")
    if len(roots) != EXPECTED_ROOTS:
        fail("root denominator drift")
    if len(objects) != EXPECTED_OBJECTS:
        fail("object denominator drift")

    contract_by_kind = unique(contracts, "source_kind", "source contracts")
    lane_by_id = unique(lanes, "lane_id", "lanes")
    req_by_id = unique(requirements, "requirement_id", "requirements")
    root_by_unit = unique(roots, "acquisition_unit_id", "root acquisitions")
    object_by_unit = unique(objects, "acquisition_unit_id", "object acquisitions")

    direct = 0
    local = 0
    for contract in contracts:
        if contract["authority_state"] != AUTHORITY_STATE or contract["claim_boundary"] != CLAIM_BOUNDARY:
            fail(f"source contract authority/claim drift: {contract['source_kind']}")
        if not split_set(contract["allowed_requirements"]) <= set(req_by_id):
            fail(f"source contract requirement drift: {contract['source_kind']}")
        if not split_set(contract["allowed_scope_kinds"]) <= {"ROOT", "OBJECT"}:
            fail(f"source contract scope drift: {contract['source_kind']}")

    for req_id, req in req_by_id.items():
        if req["lane_id"] not in lane_by_id:
            fail(f"unknown lane for requirement: {req_id}")
        if req["authority_state"] != AUTHORITY_STATE or req["claim_boundary"] != CLAIM_BOUNDARY:
            fail(f"requirement authority/claim drift: {req_id}")
        if req["acquisition_state"] != "ACQUISITION_WORK_UNIT_DEFINED_NOT_EXECUTED":
            fail(f"requirement acquisition state drift: {req_id}")
        if req["manifest_scope_kind"] not in {"ROOT", "OBJECT"}:
            fail(f"requirement scope drift: {req_id}")
        if req["closure_class"] == "DIRECT_GAP":
            direct += 1
        elif req["closure_class"] == "LOCAL_FOUNDATION_COMPLETION":
            local += 1
        else:
            fail(f"requirement closure class drift: {req_id}")
        for source_kind in allowed_source_kinds(req):
            contract = contract_by_kind.get(source_kind)
            if not contract or req_id not in split_set(contract["allowed_requirements"]):
                fail(f"requirement/source contract mismatch: {req_id} {source_kind}")
            if req["manifest_scope_kind"] not in split_set(contract["allowed_scope_kinds"]):
                fail(f"requirement/source scope mismatch: {req_id} {source_kind}")
    if direct != EXPECTED_DIRECT_GAPS or local != EXPECTED_LOCAL_FOUNDATIONS:
        fail("closure class denominator drift")

    for row in roots:
        if row["manifest_scope_kind"] != "ROOT" or row["authority_state"] != AUTHORITY_STATE:
            fail(f"root scope/authority drift: {row['acquisition_unit_id']}")
        if row["acquisition_state"] != "ACQUISITION_WORK_UNIT_DEFINED_NOT_EXECUTED":
            fail(f"root acquisition state drift: {row['acquisition_unit_id']}")
        if not split_set(row["requirement_ids"]) <= set(req_by_id):
            fail(f"root requirement drift: {row['acquisition_unit_id']}")
    for row in objects:
        if row["manifest_scope_kind"] != "OBJECT" or row["authority_state"] != AUTHORITY_STATE:
            fail(f"object scope/authority drift: {row['acquisition_unit_id']}")
        if row["final_provider_state"] != FINAL_PROVIDER_STATE or row["target_population_state"] != TARGET_STATE:
            fail(f"object provider/target drift: {row['acquisition_unit_id']}")
        if row["acquisition_state"] != "ACQUISITION_WORK_UNIT_DEFINED_NOT_EXECUTED":
            fail(f"object acquisition state drift: {row['acquisition_unit_id']}")
        if not split_set(row["requirement_ids"]) <= set(req_by_id):
            fail(f"object requirement drift: {row['acquisition_unit_id']}")
    return contract_by_kind, lane_by_id, req_by_id, root_by_unit, object_by_unit


def inspect_input_tree(input_root: Path, manifest_paths: set[str]) -> None:
    actual_files: set[str] = set()
    for current, dirnames, filenames in os.walk(input_root, topdown=True, followlinks=False):
        current_path = Path(current)
        for dirname in list(dirnames):
            path = current_path / dirname
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
                fail(f"unsafe input directory member: {path.relative_to(input_root)}")
        for filename in filenames:
            path = current_path / filename
            rel = path.relative_to(input_root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
                fail(f"unsafe input file member: {rel}")
            if rel != INPUT_MANIFEST_NAME:
                actual_files.add(rel)
    if actual_files != manifest_paths:
        missing = sorted(manifest_paths - actual_files)
        extra = sorted(actual_files - manifest_paths)
        fail(f"manifest/file-set mismatch missing={missing[:3]} extra={extra[:3]}")


def collect_inputs(
    input_root: Path,
    contract_by_kind: dict[str, dict[str, str]],
    req_by_id: dict[str, dict[str, str]],
    root_by_unit: dict[str, dict[str, str]],
    object_by_unit: dict[str, dict[str, str]],
) -> tuple[str, list[dict[str, str]]]:
    if not input_root.exists():
        return "ABSENT_NO_ACQUISITION_INPUT", []
    if not input_root.is_dir() or input_root.is_symlink():
        fail(f"unsafe acquisition input root: {input_root}")
    manifest = input_root / INPUT_MANIFEST_NAME
    rows = read_tsv(manifest, INPUT_FIELDS)
    if len(rows) > MAX_INPUT_FILES:
        fail(f"too many acquisition input rows: {len(rows)}")

    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    total_size = 0
    verified: list[dict[str, str]] = []
    for row in rows:
        input_id = row["input_id"]
        if not SAFE_ID.fullmatch(input_id) or input_id in seen_ids:
            fail(f"invalid or duplicate input_id: {input_id!r}")
        seen_ids.add(input_id)
        if not SAFE_CLASS.fullmatch(row["evidence_class"]):
            fail(f"invalid evidence_class: {input_id}")
        req_id = row["requirement_id"]
        req = req_by_id.get(req_id)
        if not req:
            fail(f"unknown requirement: {input_id} {req_id}")
        if row["lane_id"] != req["lane_id"]:
            fail(f"lane mismatch: {input_id}")
        source_kind = row["source_kind"]
        if source_kind not in allowed_source_kinds(req):
            fail(f"source kind not permitted: {input_id} {source_kind}")
        contract = contract_by_kind[source_kind]
        if req_id not in split_set(contract["allowed_requirements"]):
            fail(f"source contract requirement mismatch: {input_id}")
        if row["scope_kind"] != req["manifest_scope_kind"] or row["scope_kind"] not in split_set(contract["allowed_scope_kinds"]):
            fail(f"scope kind mismatch: {input_id}")
        if row["acquisition_mode"] != contract["acquisition_mode"]:
            fail(f"acquisition mode mismatch: {input_id}")
        if row["locator_class"] != contract["required_locator_class"]:
            fail(f"locator class mismatch: {input_id}")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            fail(f"claim boundary drift: {input_id}")
        ensure_plain_text(row["source_locator"], f"source_locator for {input_id}")

        unit_id = row["acquisition_unit_id"]
        if row["scope_kind"] == "ROOT":
            unit = root_by_unit.get(unit_id)
            if not unit:
                fail(f"unknown root acquisition unit: {input_id}")
            valid_scope_ids = {unit["manifest_scope_id"], unit["root_review_id"], unit["recipe_root"]}
        else:
            unit = object_by_unit.get(unit_id)
            if not unit:
                fail(f"unknown object acquisition unit: {input_id}")
            valid_scope_ids = {unit["manifest_scope_id"], unit["object_review_id"], unit["evidence_row_id"]}
        if req_id not in split_set(unit["requirement_ids"]):
            fail(f"requirement not assigned to acquisition unit: {input_id}")
        if source_kind not in split_set(unit["source_kinds"]):
            fail(f"source kind not assigned to acquisition unit: {input_id}")
        if row["scope_id"] not in valid_scope_ids:
            fail(f"scope id mismatch: {input_id}")

        rel = safe_relative_path(row["relative_path"])
        rel_text = rel.as_posix()
        if rel_text == INPUT_MANIFEST_NAME or rel_text in seen_paths:
            fail(f"duplicate/reserved input path: {input_id}")
        seen_paths.add(rel_text)
        path = input_root / rel
        if not path.is_file() or path.is_symlink():
            fail(f"missing/unsafe acquisition input file: {input_id}")
        observed_size = path.stat().st_size
        if observed_size > MAX_FILE_SIZE:
            fail(f"input file exceeds size bound: {input_id}")
        total_size += observed_size
        if total_size > MAX_TOTAL_SIZE:
            fail("acquisition input total size exceeds bound")
        try:
            expected_size = int(row["size_bytes"])
        except ValueError:
            fail(f"invalid size_bytes: {input_id}")
        observed_sha = sha256(path)
        if expected_size != observed_size or row["sha256"] != observed_sha:
            fail(f"digest/size mismatch: {input_id}")
        verified.append({
            **row,
            "observed_sha256": observed_sha,
            "observed_size_bytes": str(observed_size),
            "input_state": "ACQUISITION_INPUT_VERIFIED_CANDIDATE_ONLY",
            "absolute_path": str(path),
        })
    inspect_input_tree(input_root, seen_paths)
    return "PRESENT_MANIFEST_VERIFIED", verified


def output_relative_path(row: dict[str, str]) -> str:
    suffix = "".join(Path(row["relative_path"]).suffixes)[-32:]
    suffix = re.sub(r"[^A-Za-z0-9._-]", "_", suffix)
    id_hash = hashlib.sha256(row["input_id"].encode("utf-8")).hexdigest()[:16]
    return f"files/{id_hash}-{row['observed_sha256'][:16]}{suffix}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-contracts", required=True, type=Path)
    parser.add_argument("--lanes", required=True, type=Path)
    parser.add_argument("--requirements", required=True, type=Path)
    parser.add_argument("--roots", required=True, type=Path)
    parser.add_argument("--objects", required=True, type=Path)
    parser.add_argument("--input-root", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    if args.out.exists() or args.out.is_symlink():
        fail(f"refusing existing output: {args.out}")
    args.out.mkdir(parents=True)
    evidence_root = args.out / "evidence-root"
    evidence_root.mkdir()

    contracts = read_tsv(args.source_contracts)
    lanes = read_tsv(args.lanes)
    requirements = read_tsv(args.requirements)
    roots = read_tsv(args.roots)
    objects = read_tsv(args.objects)
    contract_by_kind, lane_by_id, req_by_id, root_by_unit, object_by_unit = verify_canonical_inputs(
        contracts, lanes, requirements, roots, objects
    )

    input_root_state, inputs = collect_inputs(
        args.input_root, contract_by_kind, req_by_id, root_by_unit, object_by_unit
    )

    input_rows: list[dict[str, object]] = []
    for name, path in [
        ("source_contracts", args.source_contracts),
        ("acquisition_lanes", args.lanes),
        ("acquisition_requirements", args.requirements),
        ("root_acquisition_set", args.roots),
        ("object_acquisition_set", args.objects),
    ]:
        input_rows.append({"input_name": name, "path": str(path), "sha256": sha256(path), "state": "CANONICAL_REGULAR_FILE_VERIFIED"})
    manifest_path = args.input_root / INPUT_MANIFEST_NAME
    input_rows.append({
        "input_name": "acquisition_input_root",
        "path": str(args.input_root),
        "sha256": sha256(manifest_path) if manifest_path.is_file() and not manifest_path.is_symlink() else "-",
        "state": input_root_state,
    })
    write_tsv(args.out / "input-verification.tsv", ["input_name", "path", "sha256", "state"], input_rows)

    evidence_rows: list[dict[str, str]] = []
    inventory_rows: list[dict[str, str]] = []
    for row in sorted(inputs, key=lambda item: item["input_id"]):
        out_rel = output_relative_path(row)
        destination = evidence_root / out_rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(row["absolute_path"], destination)
        os.chmod(destination, 0o444)
        copied_sha = sha256(destination)
        copied_size = destination.stat().st_size
        if copied_sha != row["observed_sha256"] or str(copied_size) != row["observed_size_bytes"]:
            fail(f"post-copy integrity mismatch: {row['input_id']}")
        evidence_id = f"gap-acquired:{row['input_id']}"
        evidence_rows.append({
            "evidence_id": evidence_id,
            "requirement_id": row["requirement_id"],
            "lane_id": row["lane_id"],
            "scope_kind": row["scope_kind"],
            "scope_id": row["scope_id"],
            "evidence_class": row["evidence_class"],
            "source_kind": row["source_kind"],
            "source_locator": row["source_locator"],
            "relative_path": out_rel,
            "sha256": copied_sha,
            "size_bytes": str(copied_size),
            "claim_boundary": CLAIM_BOUNDARY,
        })
        inventory_rows.append({
            "input_id": row["input_id"],
            "evidence_id": evidence_id,
            "acquisition_unit_id": row["acquisition_unit_id"],
            "requirement_id": row["requirement_id"],
            "lane_id": row["lane_id"],
            "scope_kind": row["scope_kind"],
            "scope_id": row["scope_id"],
            "source_kind": row["source_kind"],
            "acquisition_mode": row["acquisition_mode"],
            "locator_class": row["locator_class"],
            "source_locator": row["source_locator"],
            "input_relative_path": row["relative_path"],
            "evidence_relative_path": out_rel,
            "sha256": copied_sha,
            "size_bytes": str(copied_size),
            "acquisition_state": "CANDIDATE_EVIDENCE_ACQUIRED_REVIEW_REQUIRED",
            "claim_boundary": CLAIM_BOUNDARY,
            "authority_state": AUTHORITY_STATE,
        })
    write_tsv(evidence_root / "evidence-manifest.tsv", EVIDENCE_FIELDS, evidence_rows)
    write_tsv(
        args.out / "acquisition-file-inventory.tsv",
        [
            "input_id", "evidence_id", "acquisition_unit_id", "requirement_id", "lane_id",
            "scope_kind", "scope_id", "source_kind", "acquisition_mode", "locator_class",
            "source_locator", "input_relative_path", "evidence_relative_path", "sha256", "size_bytes",
            "acquisition_state", "claim_boundary", "authority_state",
        ],
        inventory_rows,
    )

    evidence_by_req: dict[str, list[dict[str, str]]] = defaultdict(list)
    evidence_by_unit: dict[str, list[dict[str, str]]] = defaultdict(list)
    for input_row, evidence_row in zip(sorted(inputs, key=lambda item: item["input_id"]), evidence_rows):
        evidence_by_req[evidence_row["requirement_id"]].append(evidence_row)
        evidence_by_unit[input_row["acquisition_unit_id"]].append(evidence_row)

    requirement_rows: list[dict[str, object]] = []
    unavailable_rows: list[dict[str, object]] = []
    candidate_requirements = 0
    local_only = 0
    direct_unavailable = 0
    for req_id in sorted(req_by_id):
        req = req_by_id[req_id]
        evidence = evidence_by_req[req_id]
        if evidence:
            candidate_requirements += 1
            if req["closure_class"] == "LOCAL_FOUNDATION_COMPLETION":
                state = "LOCAL_FOUNDATION_AND_CANDIDATE_EVIDENCE_ACQUIRED_REVIEW_REQUIRED"
            else:
                state = "CANDIDATE_EVIDENCE_ACQUIRED_REVIEW_REQUIRED"
        elif req["closure_class"] == "LOCAL_FOUNDATION_COMPLETION":
            local_only += 1
            state = "LOCAL_FOUNDATION_ONLY_NO_NEW_ACQUISITION"
        else:
            direct_unavailable += 1
            state = "ACQUISITION_INPUT_UNAVAILABLE_EXPLICIT_GAP"
        requirement_rows.append({
            "requirement_id": req_id,
            "lane_id": req["lane_id"],
            "closure_class": req["closure_class"],
            "acquisition_class": req["acquisition_class"],
            "manifest_scope_kind": req["manifest_scope_kind"],
            "allowed_source_kinds": join_set(allowed_source_kinds(req)),
            "candidate_input_count": str(len(evidence)),
            "evidence_ids": join_set(item["evidence_id"] for item in evidence),
            "acquisition_state": state,
            "completion_gate": req["completion_gate"],
            "review_after_collection": req["review_after_collection"],
            "claim_boundary": CLAIM_BOUNDARY,
            "closure_state": "OPEN_SEPARATE_REVIEW_REQUIRED",
            "authority_state": AUTHORITY_STATE,
        })
        if not evidence:
            unavailable_rows.append({
                "requirement_id": req_id,
                "lane_id": req["lane_id"],
                "closure_class": req["closure_class"],
                "expected_source_kinds": join_set(allowed_source_kinds(req)),
                "manifest_scope_kind": req["manifest_scope_kind"],
                "deliverable_contract": req["deliverable_contract"],
                "unavailable_state": state,
                "claim_boundary": CLAIM_BOUNDARY,
            })
    write_tsv(
        args.out / "requirement-acquisition-status.tsv",
        [
            "requirement_id", "lane_id", "closure_class", "acquisition_class", "manifest_scope_kind",
            "allowed_source_kinds", "candidate_input_count", "evidence_ids", "acquisition_state",
            "completion_gate", "review_after_collection", "claim_boundary", "closure_state", "authority_state",
        ],
        requirement_rows,
    )
    write_tsv(
        args.out / "unavailable-acquisition-inputs.tsv",
        [
            "requirement_id", "lane_id", "closure_class", "expected_source_kinds", "manifest_scope_kind",
            "deliverable_contract", "unavailable_state", "claim_boundary",
        ],
        unavailable_rows,
    )

    req_status = {row["requirement_id"]: row for row in requirement_rows}
    lane_rows: list[dict[str, object]] = []
    for lane_id in sorted(lane_by_id):
        lane = lane_by_id[lane_id]
        req_ids = split_set(lane["requirement_ids"])
        candidate_ids = {req for req in req_ids if int(str(req_status[req]["candidate_input_count"])) > 0}
        unavailable = {req for req in req_ids if req_status[req]["acquisition_state"] == "ACQUISITION_INPUT_UNAVAILABLE_EXPLICIT_GAP"}
        foundation_only = {req for req in req_ids if req_status[req]["acquisition_state"] == "LOCAL_FOUNDATION_ONLY_NO_NEW_ACQUISITION"}
        lane_rows.append({
            "lane_id": lane_id,
            "requirement_ids": join_set(req_ids),
            "candidate_input_count": str(sum(int(str(req_status[req]["candidate_input_count"])) for req in req_ids)),
            "candidate_requirement_ids": join_set(candidate_ids),
            "unavailable_requirement_ids": join_set(unavailable),
            "local_foundation_only_requirement_ids": join_set(foundation_only),
            "acquisition_state": "CANDIDATE_INPUTS_ACQUIRED_SEPARATE_REVIEW_REQUIRED" if candidate_ids else "NO_NEW_INPUTS_CLOSURE_REMAINS_OPEN",
            "completion_gate": lane["completion_gate"],
            "stop_condition": lane["stop_condition"],
            "claim_boundary": CLAIM_BOUNDARY,
            "authority_state": AUTHORITY_STATE,
        })
    write_tsv(
        args.out / "lane-acquisition-status.tsv",
        [
            "lane_id", "requirement_ids", "candidate_input_count", "candidate_requirement_ids",
            "unavailable_requirement_ids", "local_foundation_only_requirement_ids", "acquisition_state",
            "completion_gate", "stop_condition", "claim_boundary", "authority_state",
        ],
        lane_rows,
    )

    root_status_rows: list[dict[str, object]] = []
    root_units_with_candidates = 0
    for unit_id in sorted(root_by_unit):
        unit = root_by_unit[unit_id]
        evidence = evidence_by_unit[unit_id]
        if evidence:
            root_units_with_candidates += 1
        req_ids = split_set(unit["requirement_ids"])
        candidate_req_ids = {row["requirement_id"] for row in evidence}
        root_status_rows.append({
            "acquisition_unit_id": unit_id,
            "root_review_id": unit["root_review_id"],
            "recipe_root": unit["recipe_root"],
            "recipe_tree": unit["recipe_tree"],
            "requirement_ids": join_set(req_ids),
            "candidate_input_count": str(len(evidence)),
            "candidate_requirement_ids": join_set(candidate_req_ids),
            "evidence_ids": join_set(row["evidence_id"] for row in evidence),
            "missing_requirement_ids": join_set(req_ids - candidate_req_ids),
            "acquisition_state": "ROOT_CANDIDATE_INPUTS_ACQUIRED_REVIEW_REQUIRED" if evidence else "ROOT_NO_NEW_INPUTS_CLOSURE_OPEN",
            "completion_gate": unit["completion_gate"],
            "claim_boundary": CLAIM_BOUNDARY,
            "authority_state": AUTHORITY_STATE,
        })
    write_tsv(
        args.out / "root-acquisition-status.tsv",
        [
            "acquisition_unit_id", "root_review_id", "recipe_root", "recipe_tree", "requirement_ids",
            "candidate_input_count", "candidate_requirement_ids", "evidence_ids", "missing_requirement_ids",
            "acquisition_state", "completion_gate", "claim_boundary", "authority_state",
        ],
        root_status_rows,
    )

    object_status_rows: list[dict[str, object]] = []
    object_units_with_candidates = 0
    for unit_id in sorted(object_by_unit):
        unit = object_by_unit[unit_id]
        evidence = evidence_by_unit[unit_id]
        if evidence:
            object_units_with_candidates += 1
        req_ids = split_set(unit["requirement_ids"])
        candidate_req_ids = {row["requirement_id"] for row in evidence}
        object_status_rows.append({
            "acquisition_unit_id": unit_id,
            "object_review_id": unit["object_review_id"],
            "evidence_row_id": unit["evidence_row_id"],
            "identity_label": unit["identity_label"],
            "artifact_sha256": unit["artifact_sha256"],
            "recipe_root": unit["recipe_root"],
            "object_class": unit["object_class"],
            "requirement_ids": join_set(req_ids),
            "candidate_input_count": str(len(evidence)),
            "candidate_requirement_ids": join_set(candidate_req_ids),
            "evidence_ids": join_set(row["evidence_id"] for row in evidence),
            "missing_requirement_ids": join_set(req_ids - candidate_req_ids),
            "acquisition_state": "OBJECT_CANDIDATE_INPUTS_ACQUIRED_REVIEW_REQUIRED" if evidence else "OBJECT_NO_NEW_INPUTS_CLOSURE_OPEN",
            "completion_gate": unit["completion_gate"],
            "claim_boundary": CLAIM_BOUNDARY,
            "final_provider_state": FINAL_PROVIDER_STATE,
            "authority_state": AUTHORITY_STATE,
            "target_population_state": TARGET_STATE,
        })
    write_tsv(
        args.out / "object-acquisition-status.tsv",
        [
            "acquisition_unit_id", "object_review_id", "evidence_row_id", "identity_label", "artifact_sha256",
            "recipe_root", "object_class", "requirement_ids", "candidate_input_count", "candidate_requirement_ids",
            "evidence_ids", "missing_requirement_ids", "acquisition_state", "completion_gate", "claim_boundary",
            "final_provider_state", "authority_state", "target_population_state",
        ],
        object_status_rows,
    )

    summary_rows = [
        {"field": "source_contract_rows", "value": str(len(contracts))},
        {"field": "lane_rows", "value": str(len(lanes))},
        {"field": "requirement_rows", "value": str(len(requirements))},
        {"field": "root_acquisition_rows", "value": str(len(roots))},
        {"field": "object_acquisition_rows", "value": str(len(objects))},
        {"field": "acquisition_input_root_state", "value": input_root_state},
        {"field": "input_manifest_rows", "value": str(len(inputs))},
        {"field": "candidate_evidence_files_acquired", "value": str(len(evidence_rows))},
        {"field": "candidate_requirements", "value": str(candidate_requirements)},
        {"field": "local_foundation_only_requirements", "value": str(local_only)},
        {"field": "direct_gap_unavailable_requirements", "value": str(direct_unavailable)},
        {"field": "root_units_with_candidates", "value": str(root_units_with_candidates)},
        {"field": "object_units_with_candidates", "value": str(object_units_with_candidates)},
        {"field": "evidence_manifest_sha256", "value": sha256(evidence_root / "evidence-manifest.tsv")},
        {"field": "artifact_build_attestations_accepted", "value": "0"},
        {"field": "termux_android_adaptations_accepted", "value": "0"},
        {"field": "concrete_filename_drifts_accepted", "value": "0"},
        {"field": "object_corrections_accepted", "value": "0"},
        {"field": "final_provider_decisions_accepted", "value": "0"},
        {"field": "target_rows_populated", "value": "0"},
        {"field": "next_state", "value": "REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUISITION_RECEIPT"},
    ]
    write_tsv(args.out / "summary.tsv", ["field", "value"], summary_rows)
    (args.out / "analysis.status").write_text("PASS\n", encoding="utf-8")
    (args.out / "claim-boundary.txt").write_text(CLAIM_BOUNDARY + "\n", encoding="utf-8")
    (args.out / "next-state.txt").write_text(
        "REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUISITION_RECEIPT\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
