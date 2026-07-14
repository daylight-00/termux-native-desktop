#!/usr/bin/env python3
"""Review a bounded generic build-attestation/adaptation gap-closure receipt.

This reviewer validates the exact 0151 production receipt against the canonical
0150 closure set.  It can confirm that candidate evidence was absent, that six
local foundations remain bounded review inputs, and that ten direct gaps remain
explicit.  It never accepts closure evidence, build attestations, adaptation
semantics, filename-drift policy, object correction, provider authority, or
target population.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
from collections import Counter
from pathlib import Path
from typing import Iterable, NoReturn

EXPECTED_BRANCH = "docs/post-graphics-architecture-audit"
EXPECTED_SOURCE_HEAD = "ac0ed827321bc3e42c8c81b533ad024cd7b1ed69"
EXPECTED_SOURCE_TREE = "b86d78c327f6fad99578f29120e8c08156b0a359"
EXPECTED_LANES = 6
EXPECTED_REQUIREMENTS = 16
EXPECTED_ROOTS = 28
EXPECTED_OBJECTS = 37
EXPECTED_CANDIDATE_FILES = 0
EXPECTED_CANDIDATE_REQUIREMENTS = 0
EXPECTED_LOCAL_FOUNDATIONS = 6
EXPECTED_EXPLICIT_GAPS = 10
COLLECTOR_NEXT_STATE = "REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_RECEIPT"
NEXT_STATE = "DEFINE_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUISITION_SET"
AUTHORITY_STATE = "OPEN_NO_ACCEPTANCE"
TARGET_STATE = "UNPOPULATED"
FINAL_PROVIDER_STATE = "UNRESOLVED"
LOCAL_REQUIREMENTS = {"BA-003", "AD-001", "AD-002", "AD-004", "AD-006", "CF-002"}
DIRECT_GAPS = {
    "BA-001", "BA-002", "BA-004", "BA-005", "AD-003", "AD-005",
    "CF-001", "CF-003", "CF-004", "OJ-001",
}
EXPECTED_INPUT_HASHES = {
    "closure_lanes": "b6683d11ce96795cb4fa0da177adfe0cd7eb39206aead1ec55df3cf7b4800cc1",
    "closure_requirements": "fb99ed7fe42e789c5d5256363a7155814954867bfc86de4184b58b76c592ecbf",
    "root_closure_set": "315004ccbea3f7ae737a7d9ccc8e49510e416d305fe2670ea75c0f4cbdbd8580",
    "object_closure_set": "c7d004ad131244b1b9d29cd64b42f2b57f0af8f8219f2e8191fcf76471305bf3",
    "source_requirement_review": "338a99173cba976da922c1d6ce1bcf6015523ad6d82f35b5fa70ef0b4391a064",
    "source_root_review": "d72f7b4dfc38565f643ae6342d6f293ff42df36c4e8b7766355959aac3806ed6",
    "source_object_review": "c82cb3bf8257fb1cf1ac32898305f7b124303e4604e3dfee2ef024caed0105e6",
}
LOCAL_REVIEW_STATE = "LOCAL_FOUNDATION_RECONFIRMED_REVIEW_INPUT_CLOSURE_OPEN"
GAP_REVIEW_STATE = "NO_CANDIDATE_EVIDENCE_GAP_CONFIRMED_OPEN"
LANE_REVIEW_STATE = "NO_CANDIDATE_EVIDENCE_GAPS_PRESERVED_REVIEWED"
WORK_UNIT_REVIEW_STATE = "BOUNDED_GAP_CLOSURE_INPUTS_REVIEWED_INCOMPLETE"


def fail(message: str) -> NoReturn:
    raise SystemExit(f"generic gap-closure receipt review: FAIL: {message}")


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.is_file() or path.is_symlink():
        fail(f"missing regular input: {path}")
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if not reader.fieldnames:
            fail(f"missing TSV header: {path}")
        return [{key: value or "" for key, value in row.items()} for row in reader]


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
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
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def valid_sha256(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{64}", value))


def valid_oid(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{40}", value))


def read_key_values(path: Path) -> dict[str, str]:
    if not path.is_file() or path.is_symlink():
        fail(f"missing regular key/value input: {path}")
    result: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw:
            continue
        if "=" not in raw:
            fail(f"invalid key/value line in {path}: {raw}")
        key, value = raw.split("=", 1)
        if not key or key in result:
            fail(f"duplicate/empty key in {path}: {key!r}")
        result[key] = value
    return result


def require_fields(rows: list[dict[str, str]], fields: set[str], label: str, *, allow_empty: bool = False) -> None:
    if not rows:
        if allow_empty:
            return
        fail(f"empty {label}")
    missing = fields - set(rows[0])
    if missing:
        fail(f"{label} schema missing fields: {sorted(missing)}")


def unique_index(rows: list[dict[str, str]], key: str, label: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row.get(key, "")
        if not value or value in result:
            fail(f"duplicate/empty {key} in {label}: {value!r}")
        result[value] = row
    return result


def split_set(value: str) -> set[str]:
    return {item for item in value.split(";") if item and item != "NONE"}


def as_int(value: str, label: str) -> int:
    try:
        return int(value)
    except ValueError:
        fail(f"invalid integer for {label}: {value!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lanes", required=True, type=Path)
    parser.add_argument("--requirements", required=True, type=Path)
    parser.add_argument("--root-set", required=True, type=Path)
    parser.add_argument("--object-set", required=True, type=Path)
    parser.add_argument("--rules", required=True, type=Path)
    parser.add_argument("--input-verification", required=True, type=Path)
    parser.add_argument("--evidence-inventory", required=True, type=Path)
    parser.add_argument("--requirement-status", required=True, type=Path)
    parser.add_argument("--lane-status", required=True, type=Path)
    parser.add_argument("--root-observations", required=True, type=Path)
    parser.add_argument("--object-observations", required=True, type=Path)
    parser.add_argument("--unavailable-gaps", required=True, type=Path)
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--analysis-status", required=True, type=Path)
    parser.add_argument("--claim-boundary", required=True, type=Path)
    parser.add_argument("--collector-next-state", required=True, type=Path)
    parser.add_argument("--collector-input", required=True, type=Path)
    parser.add_argument("--transaction-status", required=True, type=Path)
    parser.add_argument("--final-git-state", required=True, type=Path)
    parser.add_argument("--remote-state", required=True, type=Path)
    parser.add_argument("--source-receipt-archive", required=True)
    parser.add_argument("--source-receipt-sha256", required=True)
    parser.add_argument("--expected-branch", default=EXPECTED_BRANCH)
    parser.add_argument("--expected-source-head", default=EXPECTED_SOURCE_HEAD)
    parser.add_argument("--expected-source-tree", default=EXPECTED_SOURCE_TREE)
    parser.add_argument("--expected-lanes", type=int, default=EXPECTED_LANES)
    parser.add_argument("--expected-requirements", type=int, default=EXPECTED_REQUIREMENTS)
    parser.add_argument("--expected-roots", type=int, default=EXPECTED_ROOTS)
    parser.add_argument("--expected-objects", type=int, default=EXPECTED_OBJECTS)
    parser.add_argument("--expected-candidate-files", type=int, default=EXPECTED_CANDIDATE_FILES)
    parser.add_argument("--expected-candidate-requirements", type=int, default=EXPECTED_CANDIDATE_REQUIREMENTS)
    parser.add_argument("--expected-local-foundations", type=int, default=EXPECTED_LOCAL_FOUNDATIONS)
    parser.add_argument("--expected-explicit-gaps", type=int, default=EXPECTED_EXPLICIT_GAPS)
    parser.add_argument("--next-state", default=NEXT_STATE)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    if args.out.exists() or args.out.is_symlink():
        fail(f"refusing existing output: {args.out}")
    if not valid_sha256(args.source_receipt_sha256):
        fail("invalid source receipt SHA-256")
    if not valid_oid(args.expected_source_head) or not valid_oid(args.expected_source_tree):
        fail("invalid expected Git identity")

    transaction = read_key_values(args.transaction_status)
    expected_transaction = {
        "TRANSACTION": "PASS",
        "VALIDATION": "PASS",
        "GAP_CLOSURE_COLLECTOR": "PASS_BOUNDED",
        "PUSH_AFTER_APPLY": "1",
    }
    if transaction != expected_transaction:
        fail(f"transaction status mismatch: {transaction}")

    final_git = read_key_values(args.final_git_state)
    if final_git != {
        "branch": args.expected_branch,
        "head": args.expected_source_head,
        "tree": args.expected_source_tree,
    }:
        fail(f"final Git state mismatch: {final_git}")

    remote = read_key_values(args.remote_state)
    if remote.get("push_after_apply") != "1" or remote.get("remote_head_after") != args.expected_source_head:
        fail(f"remote state mismatch: {remote}")

    collector_input = read_key_values(args.collector_input)
    if collector_input.get("state") != "ABSENT_NO_CANDIDATE_EVIDENCE":
        fail(f"unexpected collector evidence-root state: {collector_input}")
    if not collector_input.get("evidence_root"):
        fail("collector input missing evidence_root")

    if args.analysis_status.read_text(encoding="utf-8").strip() != "PASS":
        fail("collector analysis status is not PASS")
    if args.collector_next_state.read_text(encoding="utf-8").strip() != COLLECTOR_NEXT_STATE:
        fail("collector next-state mismatch")
    claim = args.claim_boundary.read_text(encoding="utf-8").strip()
    for token in (
        "review input only",
        "No build attestation",
        "provider authority",
        "target population",
    ):
        if token not in claim:
            fail(f"claim boundary missing token: {token}")

    lanes = read_tsv(args.lanes)
    requirements = read_tsv(args.requirements)
    roots = read_tsv(args.root_set)
    objects = read_tsv(args.object_set)
    rules = read_tsv(args.rules)
    input_verification = read_tsv(args.input_verification)
    evidence_inventory = read_tsv(args.evidence_inventory)
    requirement_status = read_tsv(args.requirement_status)
    lane_status = read_tsv(args.lane_status)
    root_observations = read_tsv(args.root_observations)
    object_observations = read_tsv(args.object_observations)
    unavailable_gaps = read_tsv(args.unavailable_gaps)
    summary_rows = read_tsv(args.summary)

    if len(lanes) != args.expected_lanes:
        fail(f"lane denominator drift: {len(lanes)}")
    if len(requirements) != args.expected_requirements:
        fail(f"requirement denominator drift: {len(requirements)}")
    if len(roots) != args.expected_roots:
        fail(f"root denominator drift: {len(roots)}")
    if len(objects) != args.expected_objects:
        fail(f"object denominator drift: {len(objects)}")
    if len(lane_status) != args.expected_lanes:
        fail(f"receipt lane denominator drift: {len(lane_status)}")
    if len(requirement_status) != args.expected_requirements:
        fail(f"receipt requirement denominator drift: {len(requirement_status)}")
    if len(root_observations) != args.expected_roots:
        fail(f"receipt root denominator drift: {len(root_observations)}")
    if len(object_observations) != args.expected_objects:
        fail(f"receipt object denominator drift: {len(object_observations)}")
    if len(evidence_inventory) != args.expected_candidate_files:
        fail(f"candidate evidence denominator drift: {len(evidence_inventory)}")
    if len(unavailable_gaps) != args.expected_explicit_gaps:
        fail(f"explicit gap denominator drift: {len(unavailable_gaps)}")

    require_fields(lanes, {"lane_id", "priority", "lane_class", "requirement_ids", "completion_gate", "stop_condition"}, "lanes")
    require_fields(requirements, {"requirement_id", "lane_id", "dimension", "scope", "closure_class", "remaining_gap_class", "completion_criteria", "rejection_criteria", "authority_state"}, "requirements")
    require_fields(rules, {"requirement_id", "expected_collection_state", "expected_candidate_count", "review_disposition", "receipt_review_state", "authority_state", "next_action"}, "rules")
    require_fields(input_verification, {"input_name", "path", "sha256", "state"}, "input verification")
    require_fields(requirement_status, {"requirement_id", "lane_id", "dimension", "scope", "closure_class", "local_foundation_state", "candidate_evidence_ids", "candidate_evidence_count", "collection_state", "completion_criteria", "rejection_criteria", "closure_state", "authority_state"}, "requirement status")
    require_fields(lane_status, {"lane_id", "priority", "lane_class", "requirement_ids", "candidate_evidence_count", "unavailable_requirement_ids", "local_foundation_only_requirement_ids", "collection_state", "completion_gate", "stop_condition", "closure_state", "authority_state"}, "lane status")
    require_fields(root_observations, {"root_review_id", "recipe_root", "recipe_tree", "closure_lane_ids", "requirement_ids", "candidate_evidence_ids", "candidate_evidence_count", "unavailable_requirement_ids", "collection_state", "authority_state"}, "root observations")
    require_fields(object_observations, {"object_review_id", "evidence_row_id", "identity_label", "artifact_id", "artifact_sha256", "recipe_root", "object_class", "closure_lane_ids", "requirement_ids", "candidate_evidence_ids", "candidate_evidence_count", "unavailable_requirement_ids", "collection_state", "final_provider_state", "authority_state", "target_population_state"}, "object observations")
    require_fields(unavailable_gaps, {"requirement_id", "lane_id", "remaining_gap_class", "required_evidence_mode", "completion_criteria", "gap_state", "authority_state"}, "unavailable gaps")
    require_fields(summary_rows, {"field", "value"}, "summary")

    lane_by_id = unique_index(lanes, "lane_id", "lanes")
    req_by_id = unique_index(requirements, "requirement_id", "requirements")
    rule_by_id = unique_index(rules, "requirement_id", "rules")
    status_by_id = unique_index(requirement_status, "requirement_id", "requirement status")
    lane_status_by_id = unique_index(lane_status, "lane_id", "lane status")
    root_set_by_id = unique_index(roots, "root_review_id", "root set")
    root_obs_by_id = unique_index(root_observations, "root_review_id", "root observations")
    object_set_by_id = unique_index(objects, "object_review_id", "object set")
    object_obs_by_id = unique_index(object_observations, "object_review_id", "object observations")
    gap_by_id = unique_index(unavailable_gaps, "requirement_id", "unavailable gaps")

    if set(req_by_id) != LOCAL_REQUIREMENTS | DIRECT_GAPS:
        fail("canonical requirement identity drift")
    if set(rule_by_id) != set(req_by_id) or set(status_by_id) != set(req_by_id):
        fail("rule/status requirement identity drift")
    if set(lane_status_by_id) != set(lane_by_id):
        fail("lane receipt identity drift")
    if set(root_obs_by_id) != set(root_set_by_id):
        fail("root receipt identity drift")
    if set(object_obs_by_id) != set(object_set_by_id):
        fail("object receipt identity drift")
    if set(gap_by_id) != DIRECT_GAPS:
        fail("explicit gap identity drift")

    summary = {row["field"]: row["value"] for row in summary_rows}
    expected_summary = {
        "closure_lanes": args.expected_lanes,
        "requirements": args.expected_requirements,
        "root_work_units": args.expected_roots,
        "object_work_units": args.expected_objects,
        "candidate_evidence_files": args.expected_candidate_files,
        "candidate_requirements": args.expected_candidate_requirements,
        "local_foundation_only_requirements": args.expected_local_foundations,
        "explicit_unavailable_gap_requirements": args.expected_explicit_gaps,
        "artifact_build_attestations_accepted": 0,
        "termux_android_adaptations_accepted": 0,
        "concrete_filename_drifts_accepted": 0,
        "final_provider_decisions_accepted": 0,
        "target_rows_populated": 0,
    }
    for key, expected in expected_summary.items():
        if key not in summary or as_int(summary[key], f"summary {key}") != expected:
            fail(f"summary mismatch for {key}: {summary.get(key)!r} != {expected}")
    if summary.get("next_state") != COLLECTOR_NEXT_STATE:
        fail("summary next-state mismatch")

    verification_by_name = unique_index(input_verification, "input_name", "input verification")
    required_inputs = {
        "closure_lanes", "closure_requirements", "root_closure_set", "object_closure_set",
        "source_requirement_review", "source_root_review", "source_object_review", "candidate_evidence_root",
    }
    if set(verification_by_name) != required_inputs:
        fail("input verification identity drift")
    for name, row in verification_by_name.items():
        if name == "candidate_evidence_root":
            if row["state"] != "ABSENT_NO_CANDIDATE_EVIDENCE" or row["sha256"] != "-":
                fail("candidate evidence root receipt mismatch")
        else:
            if row["state"] != "CANONICAL_REGULAR_FILE_VERIFIED" or row["sha256"] != EXPECTED_INPUT_HASHES[name]:
                fail(f"canonical input verification mismatch: {name}")

    requirement_review_rows: list[dict[str, object]] = []
    for req_id in sorted(req_by_id):
        req = req_by_id[req_id]
        status = status_by_id[req_id]
        rule = rule_by_id[req_id]
        is_local = req_id in LOCAL_REQUIREMENTS
        expected_collection = (
            "LOCAL_FOUNDATION_RECONFIRMED_CLOSURE_EVIDENCE_OPEN"
            if is_local else "EVIDENCE_UNAVAILABLE_EXPLICIT_GAP"
        )
        expected_review = LOCAL_REVIEW_STATE if is_local else GAP_REVIEW_STATE
        expected_disposition = "LOCAL_FOUNDATION_ONLY" if is_local else "EXPLICIT_GAP_NO_CANDIDATE"
        if req["authority_state"] != AUTHORITY_STATE:
            fail(f"canonical requirement authority promotion: {req_id}")
        if status["lane_id"] != req["lane_id"] or status["dimension"] != req["dimension"] or status["scope"] != req["scope"] or status["closure_class"] != req["closure_class"]:
            fail(f"requirement identity field drift: {req_id}")
        if status["completion_criteria"] != req["completion_criteria"] or status["rejection_criteria"] != req["rejection_criteria"]:
            fail(f"requirement criteria drift: {req_id}")
        if status["candidate_evidence_count"] != "0" or status["candidate_evidence_ids"] != "NONE":
            fail(f"unexpected candidate evidence: {req_id}")
        if status["collection_state"] != expected_collection:
            fail(f"collection state mismatch: {req_id}")
        if status["authority_state"] != AUTHORITY_STATE or status["closure_state"] != "OPEN_REVIEW_REQUIRED_NO_ACCEPTANCE":
            fail(f"requirement closure/authority promotion: {req_id}")
        expected_local_state = "PRESENT_BOUNDED_REVIEW_INPUT" if is_local else "NONE"
        if status["local_foundation_state"] != expected_local_state:
            fail(f"local foundation state mismatch: {req_id}")
        if rule != {
            "requirement_id": req_id,
            "expected_collection_state": expected_collection,
            "expected_candidate_count": "0",
            "review_disposition": expected_disposition,
            "receipt_review_state": expected_review,
            "authority_state": AUTHORITY_STATE,
            "next_action": "ACQUIRE_OR_AUTHOR_BOUNDED_EVIDENCE_THEN_RERUN_COLLECTOR",
        }:
            fail(f"review rule mismatch: {req_id}")
        if is_local:
            if req_id in gap_by_id:
                fail(f"local foundation incorrectly emitted as unavailable gap: {req_id}")
        else:
            gap = gap_by_id[req_id]
            if gap["lane_id"] != req["lane_id"] or gap["remaining_gap_class"] != req["remaining_gap_class"] or gap["completion_criteria"] != req["completion_criteria"]:
                fail(f"gap identity mismatch: {req_id}")
            if gap["gap_state"] != "EVIDENCE_UNAVAILABLE_EXPLICIT_GAP" or gap["authority_state"] != AUTHORITY_STATE:
                fail(f"gap state/authority mismatch: {req_id}")
        requirement_review_rows.append({
            "requirement_id": req_id,
            "lane_id": req["lane_id"],
            "dimension": req["dimension"],
            "scope": req["scope"],
            "closure_class": req["closure_class"],
            "candidate_evidence_count": "0",
            "collector_state": status["collection_state"],
            "review_disposition": expected_disposition,
            "receipt_review_state": expected_review,
            "remaining_gap_class": req["remaining_gap_class"],
            "completion_criteria": req["completion_criteria"],
            "closure_state": "OPEN_EVIDENCE_REQUIRED",
            "authority_state": AUTHORITY_STATE,
            "next_action": "ACQUIRE_OR_AUTHOR_BOUNDED_EVIDENCE_THEN_RERUN_COLLECTOR",
        })

    lane_review_rows: list[dict[str, object]] = []
    for lane_id in sorted(lane_by_id):
        lane = lane_by_id[lane_id]
        observed = lane_status_by_id[lane_id]
        req_ids = split_set(lane["requirement_ids"])
        expected_unavailable = sorted(req_ids & DIRECT_GAPS)
        expected_local = sorted(req_ids & LOCAL_REQUIREMENTS)
        if observed["priority"] != lane["priority"] or observed["lane_class"] != lane["lane_class"]:
            fail(f"lane identity drift: {lane_id}")
        if split_set(observed["requirement_ids"]) != req_ids:
            fail(f"lane requirement set drift: {lane_id}")
        if observed["candidate_evidence_count"] != "0":
            fail(f"unexpected lane candidate evidence: {lane_id}")
        if split_set(observed["unavailable_requirement_ids"]) != set(expected_unavailable):
            fail(f"lane unavailable set drift: {lane_id}")
        if split_set(observed["local_foundation_only_requirement_ids"]) != set(expected_local):
            fail(f"lane local-foundation set drift: {lane_id}")
        if observed["collection_state"] != "NO_NEW_CANDIDATE_EVIDENCE_EXPLICIT_GAPS_PRESERVED":
            fail(f"lane collection state drift: {lane_id}")
        if observed["completion_gate"] != lane["completion_gate"] or observed["stop_condition"] != lane["stop_condition"]:
            fail(f"lane criteria drift: {lane_id}")
        if observed["closure_state"] != "OPEN_REVIEW_REQUIRED_NO_ACCEPTANCE" or observed["authority_state"] != AUTHORITY_STATE:
            fail(f"lane closure/authority promotion: {lane_id}")
        lane_review_rows.append({
            "lane_id": lane_id,
            "priority": lane["priority"],
            "lane_class": lane["lane_class"],
            "requirement_ids": ";".join(sorted(req_ids)),
            "candidate_evidence_count": "0",
            "explicit_gap_requirement_ids": ";".join(expected_unavailable) or "NONE",
            "local_foundation_only_requirement_ids": ";".join(expected_local) or "NONE",
            "receipt_review_state": LANE_REVIEW_STATE,
            "completion_gate": lane["completion_gate"],
            "stop_condition": lane["stop_condition"],
            "closure_state": "OPEN_EVIDENCE_REQUIRED",
            "authority_state": AUTHORITY_STATE,
        })

    root_review_rows: list[dict[str, object]] = []
    for root_id in sorted(root_set_by_id):
        canonical = root_set_by_id[root_id]
        observed = root_obs_by_id[root_id]
        for field in ("recipe_root", "recipe_tree", "closure_lane_ids"):
            if observed[field] != canonical[field]:
                fail(f"root field drift {field}: {root_id}")
        expected_requirements = split_set(canonical["root_requirement_set"]) | split_set(canonical["dependent_object_requirement_set"])
        if split_set(observed["requirement_ids"]) != expected_requirements:
            fail(f"root requirement set drift: {root_id}")
        expected_unavailable = expected_requirements & DIRECT_GAPS
        if split_set(observed["unavailable_requirement_ids"]) != expected_unavailable:
            fail(f"root unavailable set drift: {root_id}")
        if observed["candidate_evidence_count"] != "0" or observed["candidate_evidence_ids"] != "NONE":
            fail(f"unexpected root candidate evidence: {root_id}")
        if observed["collection_state"] != "BOUNDED_CANDIDATE_INVENTORY_COMPLETE_REVIEW_REQUIRED" or observed["authority_state"] != AUTHORITY_STATE:
            fail(f"root state/authority drift: {root_id}")
        root_review_rows.append({
            "root_review_id": root_id,
            "recipe_root": canonical["recipe_root"],
            "recipe_tree": canonical["recipe_tree"],
            "closure_lane_ids": canonical["closure_lane_ids"],
            "requirement_ids": ";".join(sorted(expected_requirements)),
            "candidate_evidence_count": "0",
            "explicit_gap_requirement_ids": ";".join(sorted(expected_unavailable)) or "NONE",
            "local_foundation_requirement_ids": ";".join(sorted(expected_requirements & LOCAL_REQUIREMENTS)) or "NONE",
            "receipt_review_state": WORK_UNIT_REVIEW_STATE,
            "closure_state": "OPEN_EVIDENCE_REQUIRED",
            "authority_state": AUTHORITY_STATE,
        })

    object_review_rows: list[dict[str, object]] = []
    for object_id in sorted(object_set_by_id):
        canonical = object_set_by_id[object_id]
        observed = object_obs_by_id[object_id]
        for field in ("evidence_row_id", "identity_label", "artifact_id", "artifact_sha256", "recipe_root", "object_class", "closure_lane_ids"):
            if observed[field] != canonical[field]:
                fail(f"object field drift {field}: {object_id}")
        expected_requirements = split_set(canonical["root_requirement_set"]) | split_set(canonical["object_requirement_set"])
        if split_set(observed["requirement_ids"]) != expected_requirements:
            fail(f"object requirement set drift: {object_id}")
        expected_unavailable = expected_requirements & DIRECT_GAPS
        if split_set(observed["unavailable_requirement_ids"]) != expected_unavailable:
            fail(f"object unavailable set drift: {object_id}")
        if observed["candidate_evidence_count"] != "0" or observed["candidate_evidence_ids"] != "NONE":
            fail(f"unexpected object candidate evidence: {object_id}")
        if observed["collection_state"] != "BOUNDED_CANDIDATE_INVENTORY_COMPLETE_REVIEW_REQUIRED":
            fail(f"object collection state drift: {object_id}")
        if observed["final_provider_state"] != FINAL_PROVIDER_STATE or observed["authority_state"] != AUTHORITY_STATE or observed["target_population_state"] != TARGET_STATE:
            fail(f"object authority/target promotion: {object_id}")
        object_review_rows.append({
            "object_review_id": object_id,
            "evidence_row_id": canonical["evidence_row_id"],
            "identity_label": canonical["identity_label"],
            "artifact_id": canonical["artifact_id"],
            "artifact_sha256": canonical["artifact_sha256"],
            "recipe_root": canonical["recipe_root"],
            "object_class": canonical["object_class"],
            "closure_lane_ids": canonical["closure_lane_ids"],
            "requirement_ids": ";".join(sorted(expected_requirements)),
            "candidate_evidence_count": "0",
            "explicit_gap_requirement_ids": ";".join(sorted(expected_unavailable)) or "NONE",
            "local_foundation_requirement_ids": ";".join(sorted(expected_requirements & LOCAL_REQUIREMENTS)) or "NONE",
            "receipt_review_state": WORK_UNIT_REVIEW_STATE,
            "final_provider_state": FINAL_PROVIDER_STATE,
            "closure_state": "OPEN_EVIDENCE_REQUIRED",
            "authority_state": AUTHORITY_STATE,
            "target_population_state": TARGET_STATE,
        })

    args.out.mkdir(parents=True)
    requirement_out = args.out / "generic-build-attestation-adaptation-gap-closure-receipt-review.tsv"
    lane_out = args.out / "generic-build-attestation-adaptation-gap-closure-lane-receipt-review.tsv"
    root_out = args.out / "generic-build-attestation-adaptation-root-gap-closure-receipt-review.tsv"
    object_out = args.out / "generic-build-attestation-adaptation-object-gap-closure-receipt-review.tsv"
    metadata_out = args.out / "generic-build-attestation-adaptation-gap-closure-receipt-review-metadata.tsv"

    write_tsv(requirement_out, [
        "requirement_id", "lane_id", "dimension", "scope", "closure_class",
        "candidate_evidence_count", "collector_state", "review_disposition",
        "receipt_review_state", "remaining_gap_class", "completion_criteria",
        "closure_state", "authority_state", "next_action",
    ], requirement_review_rows)
    write_tsv(lane_out, [
        "lane_id", "priority", "lane_class", "requirement_ids", "candidate_evidence_count",
        "explicit_gap_requirement_ids", "local_foundation_only_requirement_ids",
        "receipt_review_state", "completion_gate", "stop_condition", "closure_state", "authority_state",
    ], lane_review_rows)
    write_tsv(root_out, [
        "root_review_id", "recipe_root", "recipe_tree", "closure_lane_ids", "requirement_ids",
        "candidate_evidence_count", "explicit_gap_requirement_ids", "local_foundation_requirement_ids",
        "receipt_review_state", "closure_state", "authority_state",
    ], root_review_rows)
    write_tsv(object_out, [
        "object_review_id", "evidence_row_id", "identity_label", "artifact_id", "artifact_sha256",
        "recipe_root", "object_class", "closure_lane_ids", "requirement_ids", "candidate_evidence_count",
        "explicit_gap_requirement_ids", "local_foundation_requirement_ids", "receipt_review_state",
        "final_provider_state", "closure_state", "authority_state", "target_population_state",
    ], object_review_rows)

    disposition_counts = Counter(row["review_disposition"] for row in requirement_review_rows)
    metadata_rows = [
        ("source_receipt_archive", args.source_receipt_archive),
        ("source_receipt_sha256", args.source_receipt_sha256),
        ("source_branch", args.expected_branch),
        ("source_head", args.expected_source_head),
        ("source_tree", args.expected_source_tree),
        ("closure_lanes", args.expected_lanes),
        ("requirements", args.expected_requirements),
        ("root_work_units", args.expected_roots),
        ("object_work_units", args.expected_objects),
        ("candidate_evidence_files", args.expected_candidate_files),
        ("candidate_requirements", args.expected_candidate_requirements),
        ("local_foundation_only_requirements", disposition_counts["LOCAL_FOUNDATION_ONLY"]),
        ("explicit_gap_no_candidate_requirements", disposition_counts["EXPLICIT_GAP_NO_CANDIDATE"]),
        ("artifact_build_attestations_accepted", 0),
        ("termux_android_adaptations_accepted", 0),
        ("concrete_filename_drifts_accepted", 0),
        ("object_corrections_accepted", 0),
        ("final_provider_decisions_accepted", 0),
        ("target_rows_populated", 0),
        ("rules_sha256", sha256(args.rules)),
        ("requirement_review_sha256", sha256(requirement_out)),
        ("lane_review_sha256", sha256(lane_out)),
        ("root_review_sha256", sha256(root_out)),
        ("object_review_sha256", sha256(object_out)),
        ("next_state", args.next_state),
    ]
    write_tsv(metadata_out, ["field", "value"], ({"field": key, "value": value} for key, value in metadata_rows))
    (args.out / "analysis.status").write_text("PASS\n", encoding="utf-8")
    (args.out / "claim-boundary.txt").write_text(
        "The production receipt contains no candidate evidence. Six local foundations remain bounded review inputs and ten direct gaps remain open. No closure evidence, build attestation, adaptation, filename drift, object correction, provider authority, or target population is accepted.\n",
        encoding="utf-8",
    )
    (args.out / "next-state.txt").write_text(f"{args.next_state}\n", encoding="utf-8")
    print("generic build attestation/adaptation gap-closure receipt review: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
