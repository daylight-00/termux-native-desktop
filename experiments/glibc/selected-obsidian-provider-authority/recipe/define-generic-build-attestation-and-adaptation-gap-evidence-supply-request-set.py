#!/usr/bin/env python3
"""Define bounded evidence-supply requests from the reviewed no-input receipt.

The output assigns every open requirement to exactly one bounded supply batch,
keeps exact ROOT/OBJECT acquisition units, detects dependency components, and
records transport and supplier boundaries. It issues no request, receives no
response, and accepts no evidence or authority.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter
from pathlib import Path
from typing import Iterable, NoReturn

EXPECTED = {
    "source_contracts": 10,
    "lanes": 6,
    "requirements": 16,
    "roots": 28,
    "objects": 37,
    "root_edges": 303,
    "object_edges": 414,
}
EXPECTED_HASHES = {
    "source_contracts": "97cf1d4c06f32119e14cb026532e8a107c52ba7238c09cceab894701fb967f04",
    "lanes": "bde6e8b421e4f5e669896acfc91bbe1246a6b3e0951ce842b4e1c4752e28c88b",
    "requirements": "900dc80c0785185b83b2fd4a1cc9428a08e8cc1afd459eb6412871a1aaf6e025",
    "roots": "ff6fb1dd71d7fdb1cc3566817face077d80ff96270a5f6c270da5402f4ec2e24",
    "objects": "c8ed9478efb239f352a77564aec42226a7ec616715bc090d607e3e74c68b098e",
    "receipt_review": "c4341c4947b180c1352528bbed7742edbe7f4b65eec8ead454edfb53c28fe628",
    "receipt_metadata": "f2c958a2d7e252832b485c9f9da33c4903a804db4017a399640f9c711aa0dee6",
}
NEXT_STATE = "FULFILL_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_01"
CLAIM_BOUNDARY = "SUPPLY_REQUEST_ONLY_NO_EVIDENCE_OR_AUTHORITY_EFFECT"
AUTHORITY_STATE = "OPEN_NO_ACCEPTANCE"
REQUEST_STATE = "REQUEST_DEFINED_NOT_ISSUED"
RESPONSE_MANIFEST_CONTRACT = (
    "input_id;acquisition_unit_id;requirement_id;lane_id;scope_kind;scope_id;"
    "source_kind;acquisition_mode;locator_class;source_locator;relative_path;"
    "sha256;size_bytes;evidence_class;claim_boundary"
)

BATCH_PLAN = [
    {
        "batch_id": "SUP-01",
        "sequence": "01",
        "batch_class": "AUTHORITATIVE_OBJECT_CORRECTION",
        "supplier_role": "AGENT_REFERENCE_RESEARCH_WITH_OPERATOR_DECISION",
        "transport_boundary": "CONNECTOR_RESEARCH_THEN_REPOSITORY_AUTHORED_RESPONSE",
        "requirement_ids": "OJ-001",
        "prerequisite_batch_ids": "NONE",
        "dependency_mode": "ACYCLIC_SINGLETON",
        "execution_contract": "FIND_IMMUTABLE_AUTHORITATIVE_REFERENCE_AND_RECORD_EXACT_LIBJPEG_REQUIRED_IDENTITY",
        "stop_condition": "NO_LIBJPEG_SO_8_SUBSTITUTION_AND_NO_ABI_FAMILY_INFERENCE",
    },
    {
        "batch_id": "SUP-02",
        "sequence": "02",
        "batch_class": "PRODUCING_BUILD_PROVENANCE_AND_OUTPUT_LINKAGE",
        "supplier_role": "PRODUCING_BUILD_RECORD_CUSTODIAN",
        "transport_boundary": "EXTERNAL_IMMUTABLE_OR_SIGNED_RECORD_EXPORT",
        "requirement_ids": "BA-001;BA-002;BA-003",
        "prerequisite_batch_ids": "NONE",
        "dependency_mode": "INTERNALLY_ORDERED_ACYCLIC",
        "execution_contract": "EXPORT_DIGEST_BOUND_INVOCATION_ENVIRONMENT_AND_OUTPUT_MANIFEST_FROM_ONE_PRODUCING_BUILD",
        "stop_condition": "NO_REPOSITORY_COLOCATION_VERSION_ALIGNMENT_OR_RECEIPT_ONLY_OUTPUT_AS_PROVENANCE",
    },
    {
        "batch_id": "SUP-03",
        "sequence": "03",
        "batch_class": "INDEPENDENT_BUILD_VERIFICATION",
        "supplier_role": "INDEPENDENT_LINUX_WORKSTATION_WITNESS_OR_SIGNED_PROVENANCE_CUSTODIAN",
        "transport_boundary": "INDEPENDENT_RECEIPT_OR_VERIFIABLE_SIGNED_ENVELOPE_EXPORT",
        "requirement_ids": "BA-004",
        "prerequisite_batch_ids": "SUP-02",
        "dependency_mode": "ACYCLIC_EXTERNAL_INDEPENDENCE",
        "execution_contract": "SUPPLY_INDEPENDENT_REPRODUCTION_OR_INDEPENDENTLY_VERIFIABLE_SIGNED_PROVENANCE",
        "stop_condition": "NO_SAME_HOST_SELF_REPLAY_AS_INDEPENDENT_VERIFICATION",
    },
    {
        "batch_id": "SUP-04",
        "sequence": "04",
        "batch_class": "REPOSITORY_SEMANTIC_BASELINE_AND_OBJECT_IMPACT_REVIEW",
        "supplier_role": "PROJECT_AGENT_WITH_PINNED_UPSTREAM_REFERENCE",
        "transport_boundary": "CONNECTOR_RESEARCH_AND_REPOSITORY_AUTHORED_RECORDS",
        "requirement_ids": "AD-001;AD-002;AD-003;AD-004;AD-006",
        "prerequisite_batch_ids": "NONE",
        "dependency_mode": "INTERNALLY_ORDERED_ACYCLIC",
        "execution_contract": "PIN_UPSTREAM_BASELINES_AND_AUTHOR_COMPLETE_DELTA_NECESSITY_AND_OBJECT_IMPACT_REVIEWS",
        "stop_condition": "NO_TOKEN_PRESENCE_TERMUX_ORIGIN_OR_UNPINNED_LATEST_AS_SEMANTIC_PROOF",
    },
    {
        "batch_id": "SUP-05",
        "sequence": "05",
        "batch_class": "DEVICE_CONSUMER_CAPTURE_AND_ALIAS_CONTINUITY_FIXED_POINT",
        "supplier_role": "DEVICE_CAPTURE_OPERATOR_AND_PROJECT_AGENT",
        "transport_boundary": "BOUNDED_DEVICE_CAPTURE_THEN_REPOSITORY_POLICY_REVIEW",
        "requirement_ids": "CF-001;CF-002;CF-003;CF-004",
        "prerequisite_batch_ids": "NONE",
        "dependency_mode": "CF_002_CF_003_CF_004_ITERATIVE_CYCLIC_COMPONENT",
        "execution_contract": "CAPTURE_CONSUMER_REFERENCES_DRAFT_SUCCESSOR_ROLLBACK_POLICIES_AND_ITERATE_ALIAS_REVIEW_TO_FIXED_POINT",
        "stop_condition": "NO_PROVIDER_SONAME_EQUALITY_OR_CURRENT_CONCRETE_FILENAME_AS_PERMANENT_CONSUMER_POLICY",
    },
    {
        "batch_id": "SUP-06",
        "sequence": "06",
        "batch_class": "BUILD_AND_ADAPTATION_CONTINUITY_POLICY",
        "supplier_role": "PROJECT_AGENT_POLICY_AUTHOR",
        "transport_boundary": "REPOSITORY_AUTHORED_POLICY_AFTER_PREREQUISITE_RESPONSES",
        "requirement_ids": "AD-005;BA-005",
        "prerequisite_batch_ids": "SUP-02;SUP-03;SUP-04",
        "dependency_mode": "ACYCLIC_CROSS_BATCH_FINALIZATION",
        "execution_contract": "AUTHOR_SUCCESSOR_AND_ROLLBACK_ATTESTATION_AND_ADAPTATION_REVALIDATION_GATES",
        "stop_condition": "NO_CURRENT_VERSION_ONLY_CONTINUITY_CLAIM",
    },
]

REQUEST_ROLE = {
    "OJ-001": ("SUP-01", "AGENT_REFERENCE_RESEARCH_WITH_OPERATOR_DECISION", "AUTHORITATIVE_REFERENCE_REQUIRED", "PREPARE_SUP_01_AUTHORITATIVE_CORRECTION_RESPONSE"),
    "BA-001": ("SUP-02", "PRODUCING_BUILD_RECORD_CUSTODIAN", "PRODUCER_OR_SIGNED_PROVENANCE", "REQUEST_IMMUTABLE_PRODUCER_EXPORT"),
    "BA-002": ("SUP-02", "PRODUCING_BUILD_RECORD_CUSTODIAN", "PRODUCER_OR_SIGNED_PROVENANCE", "REQUEST_IMMUTABLE_PRODUCER_EXPORT"),
    "BA-003": ("SUP-02", "PRODUCING_BUILD_RECORD_CUSTODIAN", "PRODUCER_OR_SIGNED_PROVENANCE", "REQUEST_IMMUTABLE_PRODUCER_EXPORT"),
    "BA-004": ("SUP-03", "INDEPENDENT_LINUX_WORKSTATION_WITNESS_OR_SIGNED_PROVENANCE_CUSTODIAN", "INDEPENDENT_FROM_PRODUCING_HOST", "REQUEST_INDEPENDENT_REPRODUCTION_OR_SIGNED_PROVENANCE"),
    "AD-001": ("SUP-04", "PROJECT_AGENT_REPOSITORY_SEMANTIC_REVIEW", "PROJECT_AUTHORED_WITH_PINNED_EXTERNAL_BASELINE", "PREPARE_REPOSITORY_SEMANTIC_RESPONSE"),
    "AD-002": ("SUP-04", "PROJECT_AGENT_REPOSITORY_SEMANTIC_REVIEW", "PROJECT_AUTHORED_WITH_PINNED_EXTERNAL_BASELINE", "PREPARE_REPOSITORY_SEMANTIC_RESPONSE"),
    "AD-003": ("SUP-04", "PROJECT_AGENT_REPOSITORY_SEMANTIC_REVIEW", "PROJECT_AUTHORED_WITH_PINNED_EXTERNAL_BASELINE", "PREPARE_REPOSITORY_SEMANTIC_RESPONSE"),
    "AD-004": ("SUP-04", "PROJECT_AGENT_REPOSITORY_SEMANTIC_REVIEW", "PROJECT_AUTHORED_WITH_PINNED_EXTERNAL_BASELINE", "PREPARE_REPOSITORY_SEMANTIC_RESPONSE"),
    "AD-006": ("SUP-04", "PROJECT_AGENT_REPOSITORY_SEMANTIC_REVIEW", "PROJECT_AUTHORED_WITH_PINNED_EXTERNAL_BASELINE", "PREPARE_REPOSITORY_SEMANTIC_RESPONSE"),
    "CF-001": ("SUP-05", "DEVICE_PASSIVE_CAPTURE_OPERATOR", "DEVICE_OBSERVATION", "RUN_BOUNDED_DEVICE_CONSUMER_CAPTURE"),
    "CF-002": ("SUP-05", "PROJECT_AGENT_CONSUMER_ALIAS_REVIEW", "PROJECT_AUTHORED_FROM_DEVICE_CAPTURE_AND_POLICY", "ITERATE_CF_ALIAS_COMPONENT_TO_FIXED_POINT"),
    "CF-003": ("SUP-05", "PROJECT_AGENT_POLICY_AUTHOR", "PROJECT_AUTHORED_POLICY", "ITERATE_CF_ALIAS_COMPONENT_TO_FIXED_POINT"),
    "CF-004": ("SUP-05", "PROJECT_AGENT_POLICY_AUTHOR", "PROJECT_AUTHORED_POLICY", "ITERATE_CF_ALIAS_COMPONENT_TO_FIXED_POINT"),
    "AD-005": ("SUP-06", "PROJECT_AGENT_POLICY_AUTHOR", "PROJECT_AUTHORED_POLICY_AFTER_SEMANTIC_REVIEW", "AUTHOR_POLICY_AFTER_PREREQUISITE_RESPONSES"),
    "BA-005": ("SUP-06", "PROJECT_AGENT_POLICY_AUTHOR", "PROJECT_AUTHORED_POLICY_AFTER_PROVENANCE", "AUTHOR_POLICY_AFTER_PREREQUISITE_RESPONSES"),
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"generic gap evidence supply request set: FAIL: {message}")


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
    result = sorted(set(values))
    return ";".join(result) if result else "NONE"


def unique(rows: list[dict[str, str]], key: str, label: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row.get(key, "")
        if not value or value in result:
            fail(f"duplicate/empty {key} in {label}: {value!r}")
        result[value] = row
    return result


def metadata(path: Path) -> dict[str, str]:
    rows = read_tsv(path)
    if not rows or set(rows[0]) != {"field", "value"}:
        fail("metadata schema drift")
    return {row["field"]: row["value"] for row in rows}


def tarjan_components(graph: dict[str, set[str]]) -> list[list[str]]:
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    low: dict[str, int] = {}
    result: list[list[str]] = []

    def visit(node: str) -> None:
        nonlocal index
        indices[node] = low[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for dep in sorted(graph[node]):
            if dep not in indices:
                visit(dep)
                low[node] = min(low[node], low[dep])
            elif dep in on_stack:
                low[node] = min(low[node], indices[dep])
        if low[node] == indices[node]:
            component: list[str] = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.append(member)
                if member == node:
                    break
            result.append(sorted(component))

    for node in sorted(graph):
        if node not in indices:
            visit(node)
    return sorted(result, key=lambda members: members[0])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-contracts", required=True, type=Path)
    parser.add_argument("--lanes", required=True, type=Path)
    parser.add_argument("--requirements", required=True, type=Path)
    parser.add_argument("--root-set", required=True, type=Path)
    parser.add_argument("--object-set", required=True, type=Path)
    parser.add_argument("--receipt-review", required=True, type=Path)
    parser.add_argument("--receipt-metadata", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    if args.out.exists() or args.out.is_symlink():
        fail(f"refusing existing output: {args.out}")
    inputs = {
        "source_contracts": args.source_contracts,
        "lanes": args.lanes,
        "requirements": args.requirements,
        "roots": args.root_set,
        "objects": args.object_set,
        "receipt_review": args.receipt_review,
        "receipt_metadata": args.receipt_metadata,
    }
    for name, path in inputs.items():
        observed = sha256(path)
        if observed != EXPECTED_HASHES[name]:
            fail(f"canonical input hash drift for {name}: {observed}")

    source_contracts = read_tsv(args.source_contracts)
    lanes = read_tsv(args.lanes)
    requirements = read_tsv(args.requirements)
    roots = read_tsv(args.root_set)
    objects = read_tsv(args.object_set)
    receipt = read_tsv(args.receipt_review)
    receipt_meta = metadata(args.receipt_metadata)

    if len(source_contracts) != EXPECTED["source_contracts"] or len(lanes) != EXPECTED["lanes"]:
        fail("source-contract/lane denominator drift")
    if len(requirements) != EXPECTED["requirements"] or len(receipt) != EXPECTED["requirements"]:
        fail("requirement denominator drift")
    if len(roots) != EXPECTED["roots"] or len(objects) != EXPECTED["objects"]:
        fail("acquisition-unit denominator drift")

    req_by_id = unique(requirements, "requirement_id", "requirements")
    receipt_by_id = unique(receipt, "requirement_id", "receipt review")
    unique(lanes, "lane_id", "lanes")
    unique(roots, "acquisition_unit_id", "root acquisition set")
    unique(objects, "acquisition_unit_id", "object acquisition set")

    if set(req_by_id) != set(REQUEST_ROLE) or set(receipt_by_id) != set(req_by_id):
        fail("request requirement identity drift")
    if receipt_meta.get("next_state") != "DEFINE_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_REQUEST_SET":
        fail("receipt metadata next-state drift")
    for key, expected in {
        "candidate_evidence_files": "0",
        "candidate_requirements": "0",
        "local_foundation_only_requirements": "6",
        "direct_gap_unavailable_requirements": "10",
        "artifact_build_attestations_accepted": "0",
        "termux_android_adaptations_accepted": "0",
        "concrete_filename_drifts_accepted": "0",
        "object_corrections_accepted": "0",
        "final_provider_decisions_accepted": "0",
        "target_rows_populated": "0",
    }.items():
        if receipt_meta.get(key) != expected:
            fail(f"receipt metadata mismatch for {key}")

    source_by_kind = unique(source_contracts, "source_kind", "source contracts")
    graph: dict[str, set[str]] = {}
    for req_id, row in req_by_id.items():
        if row["authority_state"] != AUTHORITY_STATE or row["acquisition_state"] != "ACQUISITION_WORK_UNIT_DEFINED_NOT_EXECUTED":
            fail(f"canonical requirement promoted: {req_id}")
        deps = split_set(row["dependency_requirement_ids"])
        if not deps <= set(req_by_id):
            fail(f"unknown dependency for {req_id}: {sorted(deps - set(req_by_id))}")
        graph[req_id] = deps
        reviewed = receipt_by_id[req_id]
        if reviewed["candidate_input_count"] != "0" or reviewed["next_action"] != "INCLUDE_IN_BOUNDED_EVIDENCE_SUPPLY_REQUEST_SET":
            fail(f"receipt request boundary drift: {req_id}")
        if reviewed["closure_state"] != "OPEN_EVIDENCE_SUPPLY_REQUIRED" or reviewed["authority_state"] != AUTHORITY_STATE:
            fail(f"receipt closure/authority promotion: {req_id}")
        if reviewed["deliverable_contract"] != row["deliverable_contract"]:
            fail(f"deliverable drift: {req_id}")
        source_kinds = {row["primary_source_kind"]} | split_set(row["alternate_source_kinds"])
        if not source_kinds <= set(source_by_kind):
            fail(f"unknown source kind for {req_id}")

    components = tarjan_components(graph)
    component_by_req: dict[str, tuple[str, list[str], str]] = {}
    for ordinal, members in enumerate(components, 1):
        component_id = f"DEP-{ordinal:02d}"
        cyclic = len(members) > 1 or any(member in graph[member] for member in members)
        kind = "CYCLIC_ITERATIVE" if cyclic else "ACYCLIC"
        for member in members:
            component_by_req[member] = (component_id, members, kind)
    cyclic_members = {req for req, (_, _, kind) in component_by_req.items() if kind == "CYCLIC_ITERATIVE"}
    if cyclic_members != {"CF-002", "CF-003", "CF-004"}:
        fail(f"unexpected dependency cycle: {sorted(cyclic_members)}")

    batch_by_id = unique(BATCH_PLAN, "batch_id", "batch plan")
    assigned: set[str] = set()
    batch_rows: list[dict[str, object]] = []
    for batch in BATCH_PLAN:
        req_ids = split_set(batch["requirement_ids"])
        if not req_ids or not req_ids <= set(req_by_id) or assigned & req_ids:
            fail(f"invalid batch requirement assignment: {batch['batch_id']}")
        assigned |= req_ids
        deliverables = join_set(req_by_id[req]["deliverable_contract"] for req in req_ids)
        source_kinds = join_set(
            kind
            for req in req_ids
            for kind in ({req_by_id[req]["primary_source_kind"]} | split_set(req_by_id[req]["alternate_source_kinds"]))
        )
        component_ids = join_set(component_by_req[req][0] for req in req_ids)
        batch_rows.append({
            **batch,
            "source_kinds": source_kinds,
            "dependency_component_ids": component_ids,
            "requested_deliverables": deliverables,
            "response_manifest_contract": RESPONSE_MANIFEST_CONTRACT,
            "request_directory": f"evidence-supply/requests/{batch['batch_id']}/",
            "response_directory": f"evidence-supply/responses/{batch['batch_id']}/",
            "request_state": REQUEST_STATE,
            "responses_received": "0",
            "claim_boundary": CLAIM_BOUNDARY,
            "authority_state": AUTHORITY_STATE,
        })
    if assigned != set(req_by_id):
        fail(f"unassigned requirements: {sorted(set(req_by_id) - assigned)}")

    root_counts = Counter()
    object_counts = Counter()
    root_edges = 0
    object_edges = 0
    for row in roots:
        req_ids = split_set(row["requirement_ids"])
        if not req_ids <= set(req_by_id):
            fail(f"unknown root requirement: {row['acquisition_unit_id']}")
        root_edges += len(req_ids)
        root_counts.update(req_ids)
        if row["authority_state"] != AUTHORITY_STATE or row["acquisition_state"] != "ACQUISITION_WORK_UNIT_DEFINED_NOT_EXECUTED":
            fail(f"root unit promoted: {row['acquisition_unit_id']}")
    for row in objects:
        req_ids = split_set(row["requirement_ids"])
        if not req_ids <= set(req_by_id):
            fail(f"unknown object requirement: {row['acquisition_unit_id']}")
        object_edges += len(req_ids)
        object_counts.update(req_ids)
        if row["authority_state"] != AUTHORITY_STATE or row["acquisition_state"] != "ACQUISITION_WORK_UNIT_DEFINED_NOT_EXECUTED":
            fail(f"object unit promoted: {row['acquisition_unit_id']}")
        if row["final_provider_state"] != "UNRESOLVED" or row["target_population_state"] != "UNPOPULATED":
            fail(f"object provider/target promotion: {row['acquisition_unit_id']}")
    if root_edges != EXPECTED["root_edges"] or object_edges != EXPECTED["object_edges"]:
        fail(f"request edge denominator drift: roots={root_edges} objects={object_edges}")

    request_rows: list[dict[str, object]] = []
    for req_id in sorted(req_by_id):
        row = req_by_id[req_id]
        batch_id, supplier_role, independence, next_action = REQUEST_ROLE[req_id]
        if req_id not in split_set(batch_by_id[batch_id]["requirement_ids"]):
            fail(f"request/batch mismatch: {req_id}")
        component_id, component_members, component_kind = component_by_req[req_id]
        source_kinds = {row["primary_source_kind"]} | split_set(row["alternate_source_kinds"])
        request_rows.append({
            "request_id": f"SRQ-{req_id}",
            "batch_id": batch_id,
            "requirement_id": req_id,
            "lane_id": row["lane_id"],
            "priority": row["acquisition_priority"],
            "dimension": row["dimension"],
            "scope_kind": row["manifest_scope_kind"],
            "supplier_role": supplier_role,
            "supplier_independence": independence,
            "acquisition_class": row["acquisition_class"],
            "acquisition_mode": row["acquisition_mode"],
            "primary_source_kind": row["primary_source_kind"],
            "alternate_source_kinds": row["alternate_source_kinds"],
            "source_kinds": join_set(source_kinds),
            "deliverable_contract": row["deliverable_contract"],
            "minimum_binding_fields": row["minimum_binding_fields"],
            "dependency_requirement_ids": row["dependency_requirement_ids"],
            "dependency_component_id": component_id,
            "dependency_component_members": join_set(component_members),
            "dependency_component_kind": component_kind,
            "root_unit_count": str(root_counts[req_id]),
            "object_unit_count": str(object_counts[req_id]),
            "request_package_relative_path": f"evidence-supply/requests/{batch_id}/SRQ-{req_id}.tsv",
            "response_package_relative_path": f"evidence-supply/responses/{batch_id}/SRQ-{req_id}/",
            "response_manifest_contract": RESPONSE_MANIFEST_CONTRACT,
            "completion_gate": row["completion_gate"],
            "review_after_supply": row["review_after_collection"],
            "claim_boundary": CLAIM_BOUNDARY,
            "request_state": REQUEST_STATE,
            "responses_received": "0",
            "authority_state": AUTHORITY_STATE,
            "next_action": next_action,
        })

    request_by_req = {row["requirement_id"]: row for row in request_rows}

    root_rows: list[dict[str, object]] = []
    for row in roots:
        req_ids = split_set(row["requirement_ids"])
        root_rows.append({
            "acquisition_unit_id": row["acquisition_unit_id"],
            "root_review_id": row["root_review_id"],
            "recipe_root": row["recipe_root"],
            "recipe_tree": row["recipe_tree"],
            "closure_lane_ids": row["closure_lane_ids"],
            "requirement_ids": join_set(req_ids),
            "request_ids": join_set(request_by_req[req]["request_id"] for req in req_ids),
            "batch_ids": join_set(request_by_req[req]["batch_id"] for req in req_ids),
            "supplier_roles": join_set(request_by_req[req]["supplier_role"] for req in req_ids),
            "dependency_component_ids": join_set(request_by_req[req]["dependency_component_id"] for req in req_ids),
            "direct_gap_requirement_ids": row["direct_gap_requirement_ids"],
            "local_foundation_requirement_ids": row["local_foundation_requirement_ids"],
            "manifest_scope_kind": row["manifest_scope_kind"],
            "manifest_scope_id": row["manifest_scope_id"],
            "response_directory": f"evidence-supply/responses/units/root/{row['acquisition_unit_id'].replace(':', '__')}/",
            "completion_gate": row["completion_gate"],
            "request_state": REQUEST_STATE,
            "responses_received": "0",
            "authority_state": AUTHORITY_STATE,
        })

    object_rows: list[dict[str, object]] = []
    for row in objects:
        req_ids = split_set(row["requirement_ids"])
        object_rows.append({
            "acquisition_unit_id": row["acquisition_unit_id"],
            "object_review_id": row["object_review_id"],
            "evidence_row_id": row["evidence_row_id"],
            "identity_label": row["identity_label"],
            "artifact_id": row["artifact_id"],
            "artifact_sha256": row["artifact_sha256"],
            "recipe_root": row["recipe_root"],
            "object_class": row["object_class"],
            "closure_lane_ids": row["closure_lane_ids"],
            "requirement_ids": join_set(req_ids),
            "request_ids": join_set(request_by_req[req]["request_id"] for req in req_ids),
            "batch_ids": join_set(request_by_req[req]["batch_id"] for req in req_ids),
            "supplier_roles": join_set(request_by_req[req]["supplier_role"] for req in req_ids),
            "dependency_component_ids": join_set(request_by_req[req]["dependency_component_id"] for req in req_ids),
            "direct_gap_requirement_ids": row["direct_gap_requirement_ids"],
            "local_foundation_requirement_ids": row["local_foundation_requirement_ids"],
            "manifest_scope_kind": row["manifest_scope_kind"],
            "manifest_scope_id": row["manifest_scope_id"],
            "response_directory": f"evidence-supply/responses/units/object/{row['acquisition_unit_id'].replace(':', '__')}/",
            "completion_gate": row["completion_gate"],
            "request_state": REQUEST_STATE,
            "responses_received": "0",
            "final_provider_state": "UNRESOLVED",
            "authority_state": AUTHORITY_STATE,
            "target_population_state": "UNPOPULATED",
        })

    args.out.mkdir(parents=True)
    paths = {
        "batches": args.out / "generic-build-attestation-adaptation-gap-evidence-supply-batches.tsv",
        "requests": args.out / "generic-build-attestation-adaptation-gap-evidence-supply-requests.tsv",
        "roots": args.out / "generic-build-attestation-adaptation-root-gap-evidence-supply-request-set.tsv",
        "objects": args.out / "generic-build-attestation-adaptation-object-gap-evidence-supply-request-set.tsv",
        "metadata": args.out / "generic-build-attestation-adaptation-gap-evidence-supply-request-set-metadata.tsv",
    }
    write_tsv(paths["batches"], [
        "batch_id", "sequence", "batch_class", "supplier_role", "transport_boundary", "requirement_ids",
        "source_kinds", "prerequisite_batch_ids", "dependency_component_ids", "dependency_mode",
        "execution_contract", "requested_deliverables", "response_manifest_contract", "request_directory",
        "response_directory", "stop_condition", "request_state", "responses_received", "claim_boundary", "authority_state",
    ], batch_rows)
    write_tsv(paths["requests"], [
        "request_id", "batch_id", "requirement_id", "lane_id", "priority", "dimension", "scope_kind",
        "supplier_role", "supplier_independence", "acquisition_class", "acquisition_mode", "primary_source_kind",
        "alternate_source_kinds", "source_kinds", "deliverable_contract", "minimum_binding_fields",
        "dependency_requirement_ids", "dependency_component_id", "dependency_component_members",
        "dependency_component_kind", "root_unit_count", "object_unit_count", "request_package_relative_path",
        "response_package_relative_path", "response_manifest_contract", "completion_gate", "review_after_supply",
        "claim_boundary", "request_state", "responses_received", "authority_state", "next_action",
    ], request_rows)
    write_tsv(paths["roots"], [
        "acquisition_unit_id", "root_review_id", "recipe_root", "recipe_tree", "closure_lane_ids", "requirement_ids",
        "request_ids", "batch_ids", "supplier_roles", "dependency_component_ids", "direct_gap_requirement_ids",
        "local_foundation_requirement_ids", "manifest_scope_kind", "manifest_scope_id", "response_directory",
        "completion_gate", "request_state", "responses_received", "authority_state",
    ], root_rows)
    write_tsv(paths["objects"], [
        "acquisition_unit_id", "object_review_id", "evidence_row_id", "identity_label", "artifact_id", "artifact_sha256",
        "recipe_root", "object_class", "closure_lane_ids", "requirement_ids", "request_ids", "batch_ids",
        "supplier_roles", "dependency_component_ids", "direct_gap_requirement_ids", "local_foundation_requirement_ids",
        "manifest_scope_kind", "manifest_scope_id", "response_directory", "completion_gate", "request_state",
        "responses_received", "final_provider_state", "authority_state", "target_population_state",
    ], object_rows)

    role_counts = Counter(row["supplier_role"] for row in request_rows)
    component_count = len({row["dependency_component_id"] for row in request_rows})
    cyclic_component_count = len({row["dependency_component_id"] for row in request_rows if row["dependency_component_kind"] == "CYCLIC_ITERATIVE"})
    meta_rows = [
        {"field": "source_contract_rows", "value": len(source_contracts)},
        {"field": "closure_lane_rows", "value": len(lanes)},
        {"field": "requirement_request_rows", "value": len(request_rows)},
        {"field": "supply_batch_rows", "value": len(batch_rows)},
        {"field": "dependency_component_rows", "value": component_count},
        {"field": "cyclic_dependency_component_rows", "value": cyclic_component_count},
        {"field": "cyclic_dependency_requirement_rows", "value": len(cyclic_members)},
        {"field": "root_supply_request_rows", "value": len(root_rows)},
        {"field": "object_supply_request_rows", "value": len(object_rows)},
        {"field": "root_request_edges", "value": root_edges},
        {"field": "object_request_edges", "value": object_edges},
        {"field": "agent_reference_request_rows", "value": role_counts["AGENT_REFERENCE_RESEARCH_WITH_OPERATOR_DECISION"]},
        {"field": "producer_custodian_request_rows", "value": role_counts["PRODUCING_BUILD_RECORD_CUSTODIAN"]},
        {"field": "independent_witness_request_rows", "value": role_counts["INDEPENDENT_LINUX_WORKSTATION_WITNESS_OR_SIGNED_PROVENANCE_CUSTODIAN"]},
        {"field": "agent_semantic_request_rows", "value": role_counts["PROJECT_AGENT_REPOSITORY_SEMANTIC_REVIEW"]},
        {"field": "device_capture_request_rows", "value": role_counts["DEVICE_PASSIVE_CAPTURE_OPERATOR"]},
        {"field": "agent_consumer_review_request_rows", "value": role_counts["PROJECT_AGENT_CONSUMER_ALIAS_REVIEW"]},
        {"field": "agent_policy_request_rows", "value": role_counts["PROJECT_AGENT_POLICY_AUTHOR"]},
        {"field": "requests_issued", "value": 0},
        {"field": "responses_received", "value": 0},
        {"field": "candidate_evidence_files_acquired", "value": 0},
        {"field": "artifact_build_attestations_accepted", "value": 0},
        {"field": "termux_android_adaptations_accepted", "value": 0},
        {"field": "concrete_filename_drifts_accepted", "value": 0},
        {"field": "object_corrections_accepted", "value": 0},
        {"field": "final_provider_decisions_accepted", "value": 0},
        {"field": "target_rows_populated", "value": 0},
        {"field": "source_contracts_sha256", "value": EXPECTED_HASHES["source_contracts"]},
        {"field": "acquisition_lanes_sha256", "value": EXPECTED_HASHES["lanes"]},
        {"field": "acquisition_requirements_sha256", "value": EXPECTED_HASHES["requirements"]},
        {"field": "root_acquisition_set_sha256", "value": EXPECTED_HASHES["roots"]},
        {"field": "object_acquisition_set_sha256", "value": EXPECTED_HASHES["objects"]},
        {"field": "acquisition_receipt_review_sha256", "value": EXPECTED_HASHES["receipt_review"]},
        {"field": "acquisition_receipt_metadata_sha256", "value": EXPECTED_HASHES["receipt_metadata"]},
        {"field": "supply_batches_sha256", "value": sha256(paths["batches"])},
        {"field": "supply_requests_sha256", "value": sha256(paths["requests"])},
        {"field": "root_supply_request_set_sha256", "value": sha256(paths["roots"])},
        {"field": "object_supply_request_set_sha256", "value": sha256(paths["objects"])},
        {"field": "first_batch_id", "value": "SUP-01"},
        {"field": "claim_boundary", "value": CLAIM_BOUNDARY},
        {"field": "next_state", "value": NEXT_STATE},
    ]
    write_tsv(paths["metadata"], ["field", "value"], meta_rows)


if __name__ == "__main__":
    main()
