#!/usr/bin/env python3
"""Collect bounded candidate evidence for the generic gap-closure set.

The collector inventories only explicitly supplied evidence files and canonical
local-foundation review inputs.  It never interprets a candidate as accepted
build provenance, adaptation necessity, filename policy, provider authority,
or target population.
"""
from __future__ import annotations

import csv
import hashlib
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, NoReturn

PROJECT_REPO = Path(os.environ["PROJECT_REPO"]).resolve()
OUT = Path(os.environ["OUT"]).resolve()
BASE = PROJECT_REPO / "experiments/glibc/selected-obsidian-provider-authority"
REVIEW = BASE / "review"
LANES = Path(os.environ.get("GENERIC_GAP_LANES", REVIEW / "generic-build-attestation-adaptation-gap-closure-lanes.tsv")).resolve()
REQUIREMENTS = Path(os.environ.get("GENERIC_GAP_REQUIREMENTS", REVIEW / "generic-build-attestation-adaptation-gap-closure-requirements.tsv")).resolve()
ROOT_SET = Path(os.environ.get("GENERIC_GAP_ROOT_SET", REVIEW / "generic-build-attestation-adaptation-root-gap-closure-set.tsv")).resolve()
OBJECT_SET = Path(os.environ.get("GENERIC_GAP_OBJECT_SET", REVIEW / "generic-build-attestation-adaptation-object-gap-closure-set.tsv")).resolve()
SOURCE_REQUIREMENT_REVIEW = Path(os.environ.get("GENERIC_GAP_SOURCE_REQUIREMENT_REVIEW", REVIEW / "generic-build-attestation-adaptation-evidence-receipt-review.tsv")).resolve()
SOURCE_ROOT_REVIEW = Path(os.environ.get("GENERIC_GAP_SOURCE_ROOT_REVIEW", REVIEW / "generic-build-attestation-adaptation-root-evidence-receipt-review.tsv")).resolve()
SOURCE_OBJECT_REVIEW = Path(os.environ.get("GENERIC_GAP_SOURCE_OBJECT_REVIEW", REVIEW / "generic-build-attestation-adaptation-object-evidence-receipt-review.tsv")).resolve()
EVIDENCE_ROOT = Path(os.environ.get("GENERIC_GAP_EVIDENCE_ROOT", str(Path.home() / ".cache/hw-t-evidence/termux-native-desktop/generic-build-attestation-adaptation-gap-closure"))).resolve()
EXPECTED_LANES = int(os.environ.get("GENERIC_GAP_EXPECTED_LANES", "6"))
EXPECTED_REQUIREMENTS = int(os.environ.get("GENERIC_GAP_EXPECTED_REQUIREMENTS", "16"))
EXPECTED_ROOTS = int(os.environ.get("GENERIC_GAP_EXPECTED_ROOTS", "28"))
EXPECTED_OBJECTS = int(os.environ.get("GENERIC_GAP_EXPECTED_OBJECTS", "37"))
NEXT_STATE = "REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_RECEIPT"
MANIFEST_NAME = "evidence-manifest.tsv"
CLAIM_BOUNDARY = "CANDIDATE_EVIDENCE_REVIEW_REQUIRED_NO_AUTHORITY_EFFECT"
LOCAL_FOUNDATION_REQUIREMENTS = {"BA-003", "AD-001", "AD-002", "AD-004", "AD-006", "CF-002"}

MANIFEST_FIELDS = [
    "evidence_id", "requirement_id", "lane_id", "scope_kind", "scope_id",
    "evidence_class", "source_kind", "source_locator", "relative_path",
    "sha256", "size_bytes", "claim_boundary",
]
ALLOWED_SOURCE_KINDS = {
    "AUTHORITATIVE_REFERENCE", "IMMUTABLE_BUILD_RECORD", "SIGNED_PROVENANCE",
    "INDEPENDENT_REPRODUCTION", "OUTPUT_MANIFEST", "PINNED_UPSTREAM_BASELINE",
    "SEMANTIC_REVIEW", "CONSUMER_REFERENCE", "LOADER_POLICY",
    "CONTINUITY_POLICY",
}
REQUIREMENT_SOURCE_KINDS = {
    "BA-001": {"IMMUTABLE_BUILD_RECORD", "SIGNED_PROVENANCE"},
    "BA-002": {"IMMUTABLE_BUILD_RECORD", "SIGNED_PROVENANCE"},
    "BA-003": {"OUTPUT_MANIFEST", "IMMUTABLE_BUILD_RECORD", "SIGNED_PROVENANCE"},
    "BA-004": {"INDEPENDENT_REPRODUCTION", "SIGNED_PROVENANCE"},
    "BA-005": {"CONTINUITY_POLICY"},
    "AD-001": {"PINNED_UPSTREAM_BASELINE", "SEMANTIC_REVIEW"},
    "AD-002": {"PINNED_UPSTREAM_BASELINE", "SEMANTIC_REVIEW"},
    "AD-003": {"SEMANTIC_REVIEW"},
    "AD-004": {"SEMANTIC_REVIEW"},
    "AD-005": {"CONTINUITY_POLICY"},
    "AD-006": {"PINNED_UPSTREAM_BASELINE", "SEMANTIC_REVIEW"},
    "CF-001": {"CONSUMER_REFERENCE", "LOADER_POLICY"},
    "CF-002": {"CONSUMER_REFERENCE", "LOADER_POLICY", "CONTINUITY_POLICY"},
    "CF-003": {"CONTINUITY_POLICY"},
    "CF-004": {"CONTINUITY_POLICY"},
    "OJ-001": {"AUTHORITATIVE_REFERENCE"},
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"generic gap-closure collector: FAIL: {message}")


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.is_file() or path.is_symlink():
        fail(f"missing regular input: {path}")
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if not reader.fieldnames:
            fail(f"missing header: {path}")
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


def safe_relative_path(value: str) -> Path:
    candidate = Path(value)
    if not value or candidate.is_absolute() or ".." in candidate.parts or value.startswith("/"):
        fail(f"unsafe evidence relative_path: {value!r}")
    return candidate


def validate_inputs(lanes: list[dict[str, str]], requirements: list[dict[str, str]], roots: list[dict[str, str]], objects: list[dict[str, str]]) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    if len(lanes) != EXPECTED_LANES:
        fail(f"lane denominator drift: {len(lanes)} != {EXPECTED_LANES}")
    if len(requirements) != EXPECTED_REQUIREMENTS:
        fail(f"requirement denominator drift: {len(requirements)} != {EXPECTED_REQUIREMENTS}")
    if len(roots) != EXPECTED_ROOTS:
        fail(f"root denominator drift: {len(roots)} != {EXPECTED_ROOTS}")
    if len(objects) != EXPECTED_OBJECTS:
        fail(f"object denominator drift: {len(objects)} != {EXPECTED_OBJECTS}")

    lane_by_id: dict[str, dict[str, str]] = {}
    for row in lanes:
        lane_id = row["lane_id"]
        if lane_id in lane_by_id:
            fail(f"duplicate lane_id: {lane_id}")
        lane_by_id[lane_id] = row
    req_by_id: dict[str, dict[str, str]] = {}
    for row in requirements:
        req_id = row["requirement_id"]
        if req_id in req_by_id:
            fail(f"duplicate requirement_id: {req_id}")
        if row["lane_id"] not in lane_by_id:
            fail(f"unknown lane for {req_id}: {row['lane_id']}")
        if row["authority_state"] != "OPEN_NO_ACCEPTANCE":
            fail(f"authority promotion in requirement set: {req_id}")
        req_by_id[req_id] = row
    if set(req_by_id) != set(REQUIREMENT_SOURCE_KINDS):
        fail("requirement identity drift")
    for row in roots:
        if row["authority_state"] != "OPEN_NO_ACCEPTANCE":
            fail(f"root authority promotion: {row['root_review_id']}")
        unknown = split_set(row["closure_lane_ids"]) - set(lane_by_id)
        if unknown:
            fail(f"unknown root lanes: {row['root_review_id']} {sorted(unknown)}")
    for row in objects:
        if row["authority_state"] != "OPEN_NO_ACCEPTANCE" or row["target_population_state"] != "UNPOPULATED":
            fail(f"object authority/target promotion: {row['object_review_id']}")
        unknown = split_set(row["closure_lane_ids"]) - set(lane_by_id)
        if unknown:
            fail(f"unknown object lanes: {row['object_review_id']} {sorted(unknown)}")
    return lane_by_id, req_by_id


def collect_manifest(req_by_id: dict[str, dict[str, str]], lane_by_id: dict[str, dict[str, str]], roots: list[dict[str, str]], objects: list[dict[str, str]]) -> tuple[str, list[dict[str, str]]]:
    if not EVIDENCE_ROOT.exists():
        return "ABSENT_NO_CANDIDATE_EVIDENCE", []
    if not EVIDENCE_ROOT.is_dir() or EVIDENCE_ROOT.is_symlink():
        fail(f"unsafe evidence root: {EVIDENCE_ROOT}")
    manifest = EVIDENCE_ROOT / MANIFEST_NAME
    if not manifest.is_file() or manifest.is_symlink():
        fail(f"evidence root exists without regular {MANIFEST_NAME}")
    rows = read_tsv(manifest)
    if rows and list(rows[0].keys()) != MANIFEST_FIELDS:
        fail("evidence manifest header drift")

    root_ids = {row["root_review_id"] for row in roots} | {row["recipe_root"] for row in roots}
    object_ids = {row["object_review_id"] for row in objects} | {row["evidence_row_id"] for row in objects}
    evidence_ids: set[str] = set()
    seen_paths: set[str] = set()
    collected: list[dict[str, str]] = []
    for row in rows:
        evidence_id = row["evidence_id"]
        req_id = row["requirement_id"]
        lane_id = row["lane_id"]
        if not evidence_id or evidence_id in evidence_ids:
            fail(f"duplicate/empty evidence_id: {evidence_id!r}")
        evidence_ids.add(evidence_id)
        if req_id not in req_by_id:
            fail(f"unknown evidence requirement: {req_id}")
        if lane_id != req_by_id[req_id]["lane_id"] or lane_id not in lane_by_id:
            fail(f"lane mismatch for evidence {evidence_id}")
        if row["source_kind"] not in ALLOWED_SOURCE_KINDS or row["source_kind"] not in REQUIREMENT_SOURCE_KINDS[req_id]:
            fail(f"source_kind not permitted for {req_id}: {row['source_kind']}")
        scope_kind = row["scope_kind"]
        scope_id = row["scope_id"]
        if scope_kind == "GLOBAL":
            if scope_id != "ALL":
                fail(f"GLOBAL evidence requires scope_id ALL: {evidence_id}")
        elif scope_kind == "ROOT":
            if scope_id not in root_ids:
                fail(f"unknown root scope_id for {evidence_id}: {scope_id}")
        elif scope_kind == "OBJECT":
            if scope_id not in object_ids:
                fail(f"unknown object scope_id for {evidence_id}: {scope_id}")
        else:
            fail(f"invalid scope_kind for {evidence_id}: {scope_kind}")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            fail(f"claim boundary violation: {evidence_id}")
        rel = safe_relative_path(row["relative_path"])
        if str(rel) in seen_paths:
            fail(f"duplicate evidence relative_path: {rel}")
        seen_paths.add(str(rel))
        path = EVIDENCE_ROOT / rel
        if not path.is_file() or path.is_symlink():
            fail(f"missing/unsafe evidence file: {rel}")
        observed_size = path.stat().st_size
        observed_sha = sha256(path)
        try:
            expected_size = int(row["size_bytes"])
        except ValueError:
            fail(f"invalid size_bytes for {evidence_id}")
        if observed_size != expected_size or observed_sha != row["sha256"]:
            fail(f"digest/size mismatch for {evidence_id}")
        collected.append({**row, "observed_sha256": observed_sha, "observed_size_bytes": str(observed_size), "inventory_state": "CANDIDATE_FILE_VERIFIED_REVIEW_REQUIRED"})
    return "PRESENT_MANIFEST_VERIFIED", collected


def applies(row: dict[str, str], root: dict[str, str] | None = None, obj: dict[str, str] | None = None) -> bool:
    if row["scope_kind"] == "GLOBAL":
        return True
    if root is not None and row["scope_kind"] == "ROOT":
        return row["scope_id"] in {root["root_review_id"], root["recipe_root"]}
    if obj is not None and row["scope_kind"] == "OBJECT":
        return row["scope_id"] in {obj["object_review_id"], obj["evidence_row_id"]}
    return False


def main() -> None:
    if OUT.exists() or OUT.is_symlink():
        fail(f"refusing existing output: {OUT}")
    OUT.mkdir(parents=True)

    lanes = read_tsv(LANES)
    requirements = read_tsv(REQUIREMENTS)
    roots = read_tsv(ROOT_SET)
    objects = read_tsv(OBJECT_SET)
    source_req = read_tsv(SOURCE_REQUIREMENT_REVIEW)
    source_root = read_tsv(SOURCE_ROOT_REVIEW)
    source_obj = read_tsv(SOURCE_OBJECT_REVIEW)
    lane_by_id, req_by_id = validate_inputs(lanes, requirements, roots, objects)
    if len(source_req) != EXPECTED_REQUIREMENTS or len(source_root) != EXPECTED_ROOTS or len(source_obj) != EXPECTED_OBJECTS:
        fail("source receipt-review denominator drift")

    evidence_root_state, evidence_rows = collect_manifest(req_by_id, lane_by_id, roots, objects)
    evidence_by_req: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in evidence_rows:
        evidence_by_req[row["requirement_id"]].append(row)

    input_rows = []
    for name, path in [
        ("closure_lanes", LANES), ("closure_requirements", REQUIREMENTS),
        ("root_closure_set", ROOT_SET), ("object_closure_set", OBJECT_SET),
        ("source_requirement_review", SOURCE_REQUIREMENT_REVIEW),
        ("source_root_review", SOURCE_ROOT_REVIEW), ("source_object_review", SOURCE_OBJECT_REVIEW),
    ]:
        input_rows.append({"input_name": name, "path": str(path), "sha256": sha256(path), "state": "CANONICAL_REGULAR_FILE_VERIFIED"})
    input_rows.append({"input_name": "candidate_evidence_root", "path": str(EVIDENCE_ROOT), "sha256": sha256(EVIDENCE_ROOT / MANIFEST_NAME) if evidence_rows or (EVIDENCE_ROOT / MANIFEST_NAME).is_file() else "-", "state": evidence_root_state})
    write_tsv(OUT / "input-verification.tsv", ["input_name", "path", "sha256", "state"], input_rows)

    write_tsv(OUT / "evidence-file-inventory.tsv", MANIFEST_FIELDS + ["observed_sha256", "observed_size_bytes", "inventory_state"], evidence_rows)

    requirement_status = []
    unavailable = []
    for req_id in sorted(req_by_id):
        req = req_by_id[req_id]
        candidates = sorted(evidence_by_req.get(req_id, []), key=lambda row: row["evidence_id"])
        local = req_id in LOCAL_FOUNDATION_REQUIREMENTS
        if local and candidates:
            state = "LOCAL_FOUNDATION_AND_CANDIDATE_EVIDENCE_COLLECTED_REVIEW_REQUIRED"
        elif local:
            state = "LOCAL_FOUNDATION_RECONFIRMED_CLOSURE_EVIDENCE_OPEN"
        elif candidates:
            state = "CANDIDATE_EVIDENCE_COLLECTED_REVIEW_REQUIRED"
        else:
            state = "EVIDENCE_UNAVAILABLE_EXPLICIT_GAP"
        row = {
            "requirement_id": req_id,
            "lane_id": req["lane_id"],
            "dimension": req["dimension"],
            "scope": req["scope"],
            "closure_class": req["closure_class"],
            "local_foundation_state": "PRESENT_BOUNDED_REVIEW_INPUT" if local else "NONE",
            "candidate_evidence_ids": ";".join(item["evidence_id"] for item in candidates) or "NONE",
            "candidate_evidence_count": str(len(candidates)),
            "collection_state": state,
            "completion_criteria": req["completion_criteria"],
            "rejection_criteria": req["rejection_criteria"],
            "closure_state": "OPEN_REVIEW_REQUIRED_NO_ACCEPTANCE",
            "authority_state": "OPEN_NO_ACCEPTANCE",
        }
        requirement_status.append(row)
        if not candidates and not local:
            unavailable.append({
                "requirement_id": req_id,
                "lane_id": req["lane_id"],
                "remaining_gap_class": req["remaining_gap_class"],
                "required_evidence_mode": req["evidence_mode"],
                "completion_criteria": req["completion_criteria"],
                "gap_state": "EVIDENCE_UNAVAILABLE_EXPLICIT_GAP",
                "authority_state": "OPEN_NO_ACCEPTANCE",
            })
    write_tsv(OUT / "requirement-collection-status.tsv", [
        "requirement_id", "lane_id", "dimension", "scope", "closure_class",
        "local_foundation_state", "candidate_evidence_ids", "candidate_evidence_count",
        "collection_state", "completion_criteria", "rejection_criteria", "closure_state", "authority_state",
    ], requirement_status)
    write_tsv(OUT / "unavailable-evidence-gaps.tsv", [
        "requirement_id", "lane_id", "remaining_gap_class", "required_evidence_mode",
        "completion_criteria", "gap_state", "authority_state",
    ], unavailable)

    status_by_req = {row["requirement_id"]: row for row in requirement_status}
    lane_status = []
    for lane in lanes:
        req_ids = split_set(lane["requirement_ids"])
        candidate_count = sum(int(status_by_req[item]["candidate_evidence_count"]) for item in req_ids)
        unavailable_ids = sorted(item for item in req_ids if status_by_req[item]["collection_state"] == "EVIDENCE_UNAVAILABLE_EXPLICIT_GAP")
        local_only_ids = sorted(item for item in req_ids if status_by_req[item]["collection_state"] == "LOCAL_FOUNDATION_RECONFIRMED_CLOSURE_EVIDENCE_OPEN")
        lane_status.append({
            "lane_id": lane["lane_id"], "priority": lane["priority"], "lane_class": lane["lane_class"],
            "requirement_ids": ";".join(sorted(req_ids)), "candidate_evidence_count": str(candidate_count),
            "unavailable_requirement_ids": ";".join(unavailable_ids) or "NONE",
            "local_foundation_only_requirement_ids": ";".join(local_only_ids) or "NONE",
            "collection_state": "CANDIDATE_INPUTS_PRESENT_REVIEW_REQUIRED" if candidate_count else "NO_NEW_CANDIDATE_EVIDENCE_EXPLICIT_GAPS_PRESERVED",
            "completion_gate": lane["completion_gate"], "stop_condition": lane["stop_condition"],
            "closure_state": "OPEN_REVIEW_REQUIRED_NO_ACCEPTANCE", "authority_state": "OPEN_NO_ACCEPTANCE",
        })
    write_tsv(OUT / "lane-collection-status.tsv", [
        "lane_id", "priority", "lane_class", "requirement_ids", "candidate_evidence_count",
        "unavailable_requirement_ids", "local_foundation_only_requirement_ids", "collection_state",
        "completion_gate", "stop_condition", "closure_state", "authority_state",
    ], lane_status)

    root_obs = []
    for root in roots:
        req_ids = split_set(root["root_requirement_set"]) | split_set(root["dependent_object_requirement_set"])
        applicable = sorted({row["evidence_id"] for row in evidence_rows if applies(row, root=root) or row["scope_kind"] == "GLOBAL"})
        missing = sorted(item for item in req_ids if not evidence_by_req.get(item) and item not in LOCAL_FOUNDATION_REQUIREMENTS)
        root_obs.append({
            "root_review_id": root["root_review_id"], "recipe_root": root["recipe_root"], "recipe_tree": root["recipe_tree"],
            "closure_lane_ids": root["closure_lane_ids"], "requirement_ids": ";".join(sorted(req_ids)),
            "candidate_evidence_ids": ";".join(applicable) or "NONE", "candidate_evidence_count": str(len(applicable)),
            "unavailable_requirement_ids": ";".join(missing) or "NONE",
            "collection_state": "BOUNDED_CANDIDATE_INVENTORY_COMPLETE_REVIEW_REQUIRED",
            "authority_state": "OPEN_NO_ACCEPTANCE",
        })
    write_tsv(OUT / "root-gap-closure-observations.tsv", [
        "root_review_id", "recipe_root", "recipe_tree", "closure_lane_ids", "requirement_ids",
        "candidate_evidence_ids", "candidate_evidence_count", "unavailable_requirement_ids", "collection_state", "authority_state",
    ], root_obs)

    object_obs = []
    for obj in objects:
        req_ids = split_set(obj["root_requirement_set"]) | split_set(obj["object_requirement_set"])
        root = next((item for item in roots if item["recipe_root"] == obj["recipe_root"]), None)
        applicable = sorted({row["evidence_id"] for row in evidence_rows if applies(row, root=root) or applies(row, obj=obj) or row["scope_kind"] == "GLOBAL"})
        missing = sorted(item for item in req_ids if not evidence_by_req.get(item) and item not in LOCAL_FOUNDATION_REQUIREMENTS)
        object_obs.append({
            "object_review_id": obj["object_review_id"], "evidence_row_id": obj["evidence_row_id"],
            "identity_label": obj["identity_label"], "artifact_id": obj["artifact_id"], "artifact_sha256": obj["artifact_sha256"],
            "recipe_root": obj["recipe_root"], "object_class": obj["object_class"], "closure_lane_ids": obj["closure_lane_ids"],
            "requirement_ids": ";".join(sorted(req_ids)), "candidate_evidence_ids": ";".join(applicable) or "NONE",
            "candidate_evidence_count": str(len(applicable)), "unavailable_requirement_ids": ";".join(missing) or "NONE",
            "collection_state": "BOUNDED_CANDIDATE_INVENTORY_COMPLETE_REVIEW_REQUIRED",
            "final_provider_state": "UNRESOLVED", "authority_state": "OPEN_NO_ACCEPTANCE", "target_population_state": "UNPOPULATED",
        })
    write_tsv(OUT / "object-gap-closure-observations.tsv", [
        "object_review_id", "evidence_row_id", "identity_label", "artifact_id", "artifact_sha256", "recipe_root",
        "object_class", "closure_lane_ids", "requirement_ids", "candidate_evidence_ids", "candidate_evidence_count",
        "unavailable_requirement_ids", "collection_state", "final_provider_state", "authority_state", "target_population_state",
    ], object_obs)

    counts = Counter(row["collection_state"] for row in requirement_status)
    summary = [
        ("closure_lanes", len(lanes)), ("requirements", len(requirements)), ("root_work_units", len(roots)),
        ("object_work_units", len(objects)), ("candidate_evidence_files", len(evidence_rows)),
        ("candidate_requirements", sum(1 for row in requirement_status if int(row["candidate_evidence_count"]) > 0)),
        ("local_foundation_only_requirements", counts["LOCAL_FOUNDATION_RECONFIRMED_CLOSURE_EVIDENCE_OPEN"]),
        ("explicit_unavailable_gap_requirements", counts["EVIDENCE_UNAVAILABLE_EXPLICIT_GAP"]),
        ("artifact_build_attestations_accepted", 0), ("termux_android_adaptations_accepted", 0),
        ("concrete_filename_drifts_accepted", 0), ("final_provider_decisions_accepted", 0),
        ("target_rows_populated", 0), ("next_state", NEXT_STATE),
    ]
    write_tsv(OUT / "summary.tsv", ["field", "value"], ({"field": key, "value": value} for key, value in summary))
    (OUT / "analysis.status").write_text("PASS\n", encoding="utf-8")
    (OUT / "claim-boundary.txt").write_text(
        "Candidate evidence inventory is review input only. No build attestation, adaptation, filename drift, object correction, provider authority, or target population is accepted.\n",
        encoding="utf-8",
    )
    (OUT / "next-state.txt").write_text(f"{NEXT_STATE}\n", encoding="utf-8")
    print("generic build attestation and adaptation gap-closure collector: PASS")


if __name__ == "__main__":
    main()
