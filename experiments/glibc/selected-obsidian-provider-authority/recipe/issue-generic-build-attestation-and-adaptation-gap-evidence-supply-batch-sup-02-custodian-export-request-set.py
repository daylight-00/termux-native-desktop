#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, NoReturn

EXPECTED_ROOTS = 28
EXPECTED_CONTRACTS = 84
CLAIM = "CUSTODIAN_EXPORT_REQUEST_ISSUANCE_ONLY_NO_RESPONSE_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT"
NEXT = "IMPLEMENT_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSE_ACQUIRER"
PUBLICATION_MODEL = "REMOTE_BRANCH_PUBLICATION_IS_REQUEST_ISSUANCE_NOT_CUSTODIAN_ACKNOWLEDGEMENT"
REQUEST_OUTPUT = "custodian-export-request-issuance.tsv"
CONTRACT_OUTPUT = "custodian-export-record-contract-issuance.tsv"
METADATA_OUTPUT = "custodian-export-request-issuance-metadata.tsv"


def fail(message: str) -> NoReturn:
    raise SystemExit(f"sup-02 custodian request issuance: FAIL: {message}")


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file() or path.is_symlink():
        fail(f"missing regular input: {path}")
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if not reader.fieldnames:
            fail(f"missing header: {path}")
        return list(reader.fieldnames), [
            {key: (value or "") for key, value in row.items()} for row in reader
        ]


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def metadata_map(rows: list[dict[str, str]]) -> dict[str, str]:
    result: dict[str, str] = {}
    for row in rows:
        field = row.get("field", "")
        if not field or field in result:
            fail("missing or duplicate metadata field")
        result[field] = row.get("value", "")
    return result


def request_anchor(request_id: str) -> str:
    return f"{REQUEST_OUTPUT}#request_id={request_id}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-set", required=True, type=Path)
    parser.add_argument("--record-contracts", required=True, type=Path)
    parser.add_argument("--request-set-metadata", required=True, type=Path)
    parser.add_argument("--source-head", required=True)
    parser.add_argument("--source-tree", required=True)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    request_fields, requests = read_tsv(args.request_set)
    contract_fields, contracts = read_tsv(args.record_contracts)
    _, metadata_rows = read_tsv(args.request_set_metadata)
    metadata = metadata_map(metadata_rows)

    if len(requests) != EXPECTED_ROOTS:
        fail(f"expected {EXPECTED_ROOTS} requests, got {len(requests)}")
    if len(contracts) != EXPECTED_CONTRACTS:
        fail(f"expected {EXPECTED_CONTRACTS} contracts, got {len(contracts)}")
    if metadata.get("root_requests") != str(EXPECTED_ROOTS):
        fail("request metadata root count drift")
    if metadata.get("record_contracts") != str(EXPECTED_CONTRACTS):
        fail("request metadata contract count drift")
    if metadata.get("requests_issued") != "0":
        fail("request set was already issued")
    if metadata.get("responses_received") != "0":
        fail("request set already records responses")
    if metadata.get("build_attestations_accepted") != "0":
        fail("request set already records build-attestation acceptance")
    if metadata.get("request_set_sha256") != sha256(args.request_set):
        fail("request-set digest mismatch")
    if metadata.get("record_contracts_sha256") != sha256(args.record_contracts):
        fail("record-contract digest mismatch")

    request_ids: set[str] = set()
    issued_rows: list[dict[str, object]] = []
    request_by_id: dict[str, dict[str, str]] = {}
    response_paths: set[str] = set()

    for row in requests:
        request_id = row.get("request_id", "")
        if not request_id or request_id in request_ids:
            fail("missing or duplicate request_id")
        request_ids.add(request_id)
        request_by_id[request_id] = row
        if row.get("batch_id") != "SUP-02":
            fail(f"batch drift: {request_id}")
        if row.get("supplier_role") != "PRODUCING_BUILD_RECORD_CUSTODIAN":
            fail(f"supplier role drift: {request_id}")
        if row.get("request_state") != "REQUEST_DEFINED_NOT_ISSUED":
            fail(f"request state drift: {request_id}")
        if row.get("responses_received") != "0" or row.get("build_attestations_accepted") != "0":
            fail(f"pre-issuance acceptance drift: {request_id}")
        if row.get("required_record_names") != (
            "build-invocation-record.json;build-environment-record.json;build-output-manifest.tsv"
        ):
            fail(f"required record drift: {request_id}")
        response_directory = row.get("response_directory", "")
        if not response_directory or response_directory in response_paths:
            fail(f"missing or duplicate response directory: {request_id}")
        response_paths.add(response_directory)
        issuance_id = f"SUP02-ISSUE-{request_id.removeprefix('SUP02-CER-')}"
        issued_rows.append(
            {
                "issuance_id": issuance_id,
                "request_id": request_id,
                "batch_id": row["batch_id"],
                "acquisition_unit_id": row["acquisition_unit_id"],
                "root_review_id": row["root_review_id"],
                "recipe_root": row["recipe_root"],
                "recipe_tree": row["recipe_tree"],
                "requirement_ids": row["requirement_ids"],
                "supplier_role": row["supplier_role"],
                "publication_model": PUBLICATION_MODEL,
                "transport_class": "REPOSITORY_PUBLISHED_IMMUTABLE_REQUEST_PACKET",
                "issued_request_locator": request_anchor(request_id),
                "response_drop_locator": response_directory,
                "required_record_names": row["required_record_names"],
                "one_build_linkage": row["one_build_linkage"],
                "custodian_binding": row["custodian_binding"],
                "completion_gate": row["completion_gate"],
                "request_state": "REQUEST_ISSUED_REPOSITORY_PUBLICATION",
                "acknowledgement_state": "NOT_ACKNOWLEDGED",
                "responses_received": 0,
                "build_attestations_accepted": 0,
                "claim_boundary": CLAIM,
                "next_action": "AWAIT_OR_IMPORT_EXACT_CUSTODIAN_EXPORT_RESPONSE",
            }
        )

    contracts_by_request: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in contracts:
        request_id = row.get("request_id", "")
        if request_id not in request_by_id:
            fail(f"orphan record contract: {request_id}")
        contracts_by_request[request_id].append(row)

    issued_contracts: list[dict[str, object]] = []
    requirement_counts: Counter[str] = Counter()
    for request_id in sorted(request_ids):
        rows = contracts_by_request[request_id]
        if len(rows) != 3:
            fail(f"request must have exactly three contracts: {request_id}")
        expected = {
            ("BA-001", "build-invocation-record.json", "JSON_OBJECT"),
            ("BA-002", "build-environment-record.json", "JSON_OBJECT"),
            ("BA-003", "build-output-manifest.tsv", "TSV_WITH_ROWS"),
        }
        actual = {
            (row.get("requirement_id", ""), row.get("record_name", ""), row.get("record_format", ""))
            for row in rows
        }
        if actual != expected:
            fail(f"record contract set drift: {request_id}")
        parent = request_by_id[request_id]
        issuance_id = f"SUP02-ISSUE-{request_id.removeprefix('SUP02-CER-')}"
        for row in sorted(rows, key=lambda item: item["requirement_id"]):
            for field in ("root_review_id", "recipe_root", "recipe_tree"):
                if row.get(field) != parent.get(field):
                    fail(f"request/contract {field} drift: {request_id}")
            if row.get("record_state") != "REQUIRED_NOT_SUPPLIED":
                fail(f"record state drift: {request_id}/{row.get('requirement_id')}")
            if row.get("acceptance_state") != "OPEN_NO_ACCEPTANCE":
                fail(f"record acceptance drift: {request_id}/{row.get('requirement_id')}")
            requirement_counts[row["requirement_id"]] += 1
            issued_contracts.append(
                {
                    "issuance_id": issuance_id,
                    "request_id": request_id,
                    "root_review_id": row["root_review_id"],
                    "recipe_root": row["recipe_root"],
                    "recipe_tree": row["recipe_tree"],
                    "requirement_id": row["requirement_id"],
                    "record_name": row["record_name"],
                    "record_format": row["record_format"],
                    "mandatory_fields": row["mandatory_fields"],
                    "cross_record_binding": row["cross_record_binding"],
                    "issued_request_locator": request_anchor(request_id),
                    "response_drop_locator": parent["response_directory"],
                    "record_state": "ISSUED_REQUIRED_NOT_SUPPLIED",
                    "acceptance_state": "OPEN_NO_ACCEPTANCE",
                    "claim_boundary": CLAIM,
                }
            )

    if requirement_counts != Counter({"BA-001": EXPECTED_ROOTS, "BA-002": EXPECTED_ROOTS, "BA-003": EXPECTED_ROOTS}):
        fail("requirement contract counts drift")

    if args.out.exists():
        fail(f"output already exists: {args.out}")
    args.out.mkdir(parents=True)

    issued_request_path = args.out / REQUEST_OUTPUT
    issued_contract_path = args.out / CONTRACT_OUTPUT
    write_tsv(
        issued_request_path,
        [
            "issuance_id", "request_id", "batch_id", "acquisition_unit_id", "root_review_id",
            "recipe_root", "recipe_tree", "requirement_ids", "supplier_role", "publication_model",
            "transport_class", "issued_request_locator", "response_drop_locator", "required_record_names",
            "one_build_linkage", "custodian_binding", "completion_gate", "request_state",
            "acknowledgement_state", "responses_received", "build_attestations_accepted",
            "claim_boundary", "next_action",
        ],
        issued_rows,
    )
    write_tsv(
        issued_contract_path,
        [
            "issuance_id", "request_id", "root_review_id", "recipe_root", "recipe_tree",
            "requirement_id", "record_name", "record_format", "mandatory_fields",
            "cross_record_binding", "issued_request_locator", "response_drop_locator",
            "record_state", "acceptance_state", "claim_boundary",
        ],
        issued_contracts,
    )
    metadata_path = args.out / METADATA_OUTPUT
    write_tsv(
        metadata_path,
        ["field", "value"],
        [
            {"field": "source_head", "value": args.source_head},
            {"field": "source_tree", "value": args.source_tree},
            {"field": "defined_request_set_sha256", "value": sha256(args.request_set)},
            {"field": "defined_record_contracts_sha256", "value": sha256(args.record_contracts)},
            {"field": "request_issuance_rows", "value": len(issued_rows)},
            {"field": "record_contract_issuance_rows", "value": len(issued_contracts)},
            {"field": "ba_001_issued_contracts", "value": requirement_counts["BA-001"]},
            {"field": "ba_002_issued_contracts", "value": requirement_counts["BA-002"]},
            {"field": "ba_003_issued_contracts", "value": requirement_counts["BA-003"]},
            {"field": "requests_issued", "value": len(issued_rows)},
            {"field": "requests_acknowledged", "value": 0},
            {"field": "responses_received", "value": 0},
            {"field": "build_attestations_accepted", "value": 0},
            {"field": "final_provider_decisions_accepted", "value": 0},
            {"field": "target_rows_populated", "value": 0},
            {"field": "publication_model", "value": PUBLICATION_MODEL},
            {"field": "request_issuance_sha256", "value": sha256(issued_request_path)},
            {"field": "record_contract_issuance_sha256", "value": sha256(issued_contract_path)},
            {"field": "claim_boundary", "value": CLAIM},
            {"field": "next_state", "value": NEXT},
        ],
    )
    (args.out / "analysis.status").write_text("PASS\n", encoding="utf-8")
    (args.out / "claim-boundary.txt").write_text(CLAIM + "\n", encoding="utf-8")
    (args.out / "next-state.txt").write_text(NEXT + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
