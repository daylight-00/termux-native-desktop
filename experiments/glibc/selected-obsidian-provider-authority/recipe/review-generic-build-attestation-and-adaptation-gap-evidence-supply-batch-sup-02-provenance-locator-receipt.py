#!/usr/bin/env python3
"""Review the exact production SUP-02 producing-build provenance locator receipt."""
from __future__ import annotations
import argparse, csv, hashlib, re
from pathlib import Path
from typing import Iterable, NoReturn

EXPECTED_HEAD = "8bcbf79d1e79b6fdcbe4c4440ccee144372853e7"
EXPECTED_TREE = "297775f099d7b8b21a3b2e356e8f999360acee2d"
EXPECTED_ARCHIVE_SHA = "91698e4737ab101e4798cfc555c31f0eaa9d885c07c606111a1227e61a1db6bc"
SOURCE_CLAIM = "PROVENANCE_LOCATOR_RECEIPT_ONLY_NO_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT"
REVIEW_CLAIM = "PROVENANCE_LOCATOR_RECEIPT_REVIEW_ACCEPTS_NO_EXPORT_FOUND_NO_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT"
SOURCE_NEXT = "REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_PROVENANCE_LOCATOR_RECEIPT"
NEXT = "DEFINE_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_REQUEST_SET"
ROOT_FIELDS = ["acquisition_unit_id","root_review_id","recipe_root","recipe_tree","build_invocation_records","build_environment_records","build_output_manifests","locator_state","ba_001_state","ba_002_state","ba_003_state","authority_state","claim_boundary"]
INVENTORY_FIELDS = ["root_review_id","acquisition_unit_id","recipe_root","record_kind","path","sha256","size_bytes","validation_state","claim_boundary"]
SURFACE_FIELDS = ["surface","state","item_count","sha256","evidentiary_effect"]
SUMMARY_FIELDS = ["field","value"]
EXPECTED_SURFACES = {
    "github_repository_metadata": ("CAPTURED", "1", "c2d00006e78b330f1cd94ad59ca94c0d6475d5ec4fc35d25bfa2bc66de008d8d", "LOCATOR_ONLY"),
    "github_actions_workflows": ("CAPTURED", "2", "0c0058ce3654d5140808e299078d1cf1e2dd3cda50fb5c375dfacb2c955fad73", "LOCATOR_ONLY_NOT_BUILD_PROVENANCE"),
    "github_releases": ("CAPTURED", "4", "0b62b3e3568c04722ce8b3ad9b84980da817b0803a932a01f2b3b525a6b157f4", "LOCATOR_ONLY_NOT_BUILD_PROVENANCE"),
}

def fail(message: str) -> NoReturn:
    raise SystemExit(f"SUP-02 provenance locator receipt review: FAIL: {message}")

def require(value: bool, message: str) -> None:
    if not value: fail(message)

def read_tsv(path: Path, fields: list[str] | None = None) -> tuple[list[str], list[dict[str,str]]]:
    if not path.is_file() or path.is_symlink(): fail(f"missing regular input: {path}")
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader=csv.DictReader(stream, delimiter="\t")
        actual=reader.fieldnames or []
        if not actual: fail(f"missing header: {path}")
        if fields is not None and actual != fields: fail(f"header drift: {path}")
        return actual, [{k:(v or "") for k,v in row.items()} for row in reader]

def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str,object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer=csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows: writer.writerow({field:row.get(field,"") for field in fields})

def sha256(path: Path) -> str:
    digest=hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""): digest.update(block)
    return digest.hexdigest()

def unique(rows: list[dict[str,str]], key: str, label: str) -> dict[str,dict[str,str]]:
    result={}
    for row in rows:
        value=row.get(key,"")
        if not value or value in result: fail(f"duplicate or empty {key} in {label}: {value!r}")
        result[value]=row
    return result

def split_set(value: str) -> set[str]:
    return {item for item in value.split(";") if item and item != "NONE"}

def kv(rows: list[dict[str,str]]) -> dict[str,str]:
    result={}
    for row in rows:
        key=row["field"]
        if not key or key in result: fail(f"duplicate or empty summary field: {key!r}")
        result[key]=row["value"]
    return result

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--root-request-set", required=True, type=Path)
    parser.add_argument("--supply-batches", required=True, type=Path)
    parser.add_argument("--locator-dir", required=True, type=Path)
    parser.add_argument("--rules", required=True, type=Path)
    parser.add_argument("--source-head", default=EXPECTED_HEAD)
    parser.add_argument("--source-tree", default=EXPECTED_TREE)
    parser.add_argument("--source-archive-sha256", default=EXPECTED_ARCHIVE_SHA)
    parser.add_argument("--out", required=True, type=Path)
    args=parser.parse_args()
    for label,value,expected in [("head",args.source_head,EXPECTED_HEAD),("tree",args.source_tree,EXPECTED_TREE),("archive",args.source_archive_sha256,EXPECTED_ARCHIVE_SHA)]:
        require(re.fullmatch(r"[0-9a-f]{64}" if label=="archive" else r"[0-9a-f]{40}", value) is not None, f"invalid source {label}")
        require(value==expected, f"source {label} drift")
    if args.out.exists() or args.out.is_symlink(): fail(f"refusing existing output: {args.out}")

    _, rules=read_tsv(args.rules, ["rule_id","dimension","scope","acceptance_rule","rejection_rule","authority_effect"])
    require(len(rules)==10 and [r["rule_id"] for r in rules]==[f"SUP02L-R{i:02d}" for i in range(1,11)], "review rule drift")
    _, root_requests=read_tsv(args.root_request_set)
    _, batches=read_tsv(args.supply_batches)
    require(len(root_requests)==28 and len(batches)==6, "canonical denominator drift")
    root_i=unique(root_requests,"acquisition_unit_id","root request set")
    batch_i=unique(batches,"batch_id","supply batches")
    batch=batch_i.get("SUP-02") or fail("missing SUP-02 batch")
    require(batch["requirement_ids"]=="BA-001;BA-002;BA-003", "SUP-02 requirement drift")
    require(batch["execution_contract"]=="EXPORT_DIGEST_BOUND_INVOCATION_ENVIRONMENT_AND_OUTPUT_MANIFEST_FROM_ONE_PRODUCING_BUILD", "SUP-02 execution contract drift")
    require(batch["stop_condition"]=="NO_REPOSITORY_COLOCATION_VERSION_ALIGNMENT_OR_RECEIPT_ONLY_OUTPUT_AS_PROVENANCE", "SUP-02 stop-condition drift")
    for row in root_requests:
        require("SUP-02" in split_set(row["batch_ids"]), f"SUP-02 missing from root: {row['root_review_id']}")
        require(row["manifest_scope_kind"]=="ROOT" and row["authority_state"]=="OPEN_NO_ACCEPTANCE", "canonical root scope/authority drift")
        require({"BA-001","BA-002","BA-003"} <= split_set(row["requirement_ids"]), f"SUP-02 requirements missing from root: {row['root_review_id']}")

    locator=args.locator_dir
    require(locator.is_dir() and not locator.is_symlink(), "unsafe locator directory")
    require((locator/"analysis.status").read_text(encoding="utf-8")=="PASS\n", "locator analysis status drift")
    require((locator/"claim-boundary.txt").read_text(encoding="utf-8").strip()==SOURCE_CLAIM, "locator claim-boundary drift")
    require((locator/"next-state.txt").read_text(encoding="utf-8").strip()==SOURCE_NEXT, "locator next-state drift")
    _, inventory=read_tsv(locator/"sup-02-local-record-inventory.tsv", INVENTORY_FIELDS)
    _, located=read_tsv(locator/"sup-02-root-provenance-locator.tsv", ROOT_FIELDS)
    _, surfaces=read_tsv(locator/"sup-02-custodian-surface.tsv", SURFACE_FIELDS)
    _, summary_rows=read_tsv(locator/"summary.tsv", SUMMARY_FIELDS)
    require(len(inventory)==0, "record inventory must be header-only")
    require(len(located)==28, "locator root denominator drift")
    located_i=unique(located,"acquisition_unit_id","locator roots")
    require(set(located_i)==set(root_i), "locator root identity set drift")
    root_review=[]
    for unit,canonical in root_i.items():
        row=located_i[unit]
        for field in ("root_review_id","recipe_root","recipe_tree"):
            require(row[field]==canonical[field], f"locator root binding drift: {unit} {field}")
        require([row["build_invocation_records"],row["build_environment_records"],row["build_output_manifests"]]==["0","0","0"], f"invented record count: {unit}")
        require(row["locator_state"]=="NO_CUSTODIAN_EXPORT_FOUND", f"locator state drift: {unit}")
        require(row["ba_001_state"]=="OPEN_NO_RECORD_LOCATED" and row["ba_002_state"]=="OPEN_NO_RECORD_LOCATED" and row["ba_003_state"]=="OPEN_NO_RECORD_LOCATED", f"BA state drift: {unit}")
        require(row["authority_state"]=="OPEN_NO_ACCEPTANCE" and row["claim_boundary"]==SOURCE_CLAIM, f"authority/claim drift: {unit}")
        root_review.append({
            "acquisition_unit_id":unit,"root_review_id":row["root_review_id"],"recipe_root":row["recipe_root"],"recipe_tree":row["recipe_tree"],
            "locator_receipt_state":"CONFIRMED_NO_EXISTING_CUSTODIAN_EXPORT","build_invocation_state":"OPEN_CUSTODIAN_EXPORT_REQUIRED",
            "build_environment_state":"OPEN_CUSTODIAN_EXPORT_REQUIRED","build_output_linkage_state":"OPEN_CUSTODIAN_EXPORT_REQUIRED",
            "receipt_review_decision":"ACCEPT_ABSENCE_AS_GAP_EVIDENCE_ONLY","build_attestation_state":"OPEN_NO_ACCEPTANCE",
            "final_provider_state":"UNRESOLVED","target_population_state":"UNPOPULATED","next_action":"INCLUDE_IN_SUP_02_CUSTODIAN_EXPORT_REQUEST_SET",
        })
    surface_i=unique(surfaces,"surface","custodian surfaces")
    require(set(surface_i)==set(EXPECTED_SURFACES), "custodian surface identity drift")
    surface_review=[]
    for name,(state,count,digest,effect) in EXPECTED_SURFACES.items():
        row=surface_i[name]
        require((row["state"],row["item_count"],row["sha256"],row["evidentiary_effect"])==(state,count,digest,effect), f"custodian surface drift: {name}")
        surface_review.append({"surface":name,"capture_state":state,"item_count":count,"sha256":digest,"receipt_review_state":"VERIFIED_LOCATOR_ONLY","build_provenance_effect":"NONE","rejection_boundary":"MUST_NOT_SATISFY_BA_001_BA_002_OR_BA_003"})
    summary=kv(summary_rows)
    expected_summary={"root_rows":"28","record_roots":"1","complete_custodian_exports":"0","partial_custodian_exports":"0","absent_custodian_exports":"28","record_files_located":"0","build_attestations_accepted":"0","final_provider_decisions_accepted":"0","target_rows_populated":"0","next_state":SOURCE_NEXT}
    require(summary==expected_summary, "locator summary drift")

    args.out.mkdir(parents=True)
    overall_fields=["review_id","batch_id","requirement_ids","root_rows","complete_custodian_exports","partial_custodian_exports","absent_custodian_exports","record_files_located","receipt_decision","ba_001_state","ba_002_state","ba_003_state","build_attestations_accepted","final_provider_decisions_accepted","target_rows_populated","claim_boundary","next_action"]
    overall=[{"review_id":"sup-02-provenance-locator-receipt-review:production-20260714T034350Z","batch_id":"SUP-02","requirement_ids":"BA-001;BA-002;BA-003","root_rows":28,"complete_custodian_exports":0,"partial_custodian_exports":0,"absent_custodian_exports":28,"record_files_located":0,"receipt_decision":"PASS_BOUNDED_NO_EXISTING_CUSTODIAN_EXPORT_FOUND","ba_001_state":"OPEN_CUSTODIAN_INVOCATION_EXPORT_REQUIRED","ba_002_state":"OPEN_CUSTODIAN_ENVIRONMENT_EXPORT_REQUIRED","ba_003_state":"OPEN_CUSTODIAN_OUTPUT_MANIFEST_REQUIRED","build_attestations_accepted":0,"final_provider_decisions_accepted":0,"target_rows_populated":0,"claim_boundary":REVIEW_CLAIM,"next_action":"DEFINE_EXACT_SUP_02_CUSTODIAN_EXPORT_REQUEST_SET"}]
    overall_path=args.out/"generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-provenance-locator-receipt-review.tsv"
    root_path=args.out/"generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-root-provenance-locator-receipt-review.tsv"
    surface_path=args.out/"generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-surface-receipt-review.tsv"
    write_tsv(overall_path,overall_fields,overall)
    write_tsv(root_path,["acquisition_unit_id","root_review_id","recipe_root","recipe_tree","locator_receipt_state","build_invocation_state","build_environment_state","build_output_linkage_state","receipt_review_decision","build_attestation_state","final_provider_state","target_population_state","next_action"],root_review)
    write_tsv(surface_path,["surface","capture_state","item_count","sha256","receipt_review_state","build_provenance_effect","rejection_boundary"],surface_review)
    metadata=[
        {"field":"source_head","value":args.source_head},{"field":"source_tree","value":args.source_tree},{"field":"source_archive_sha256","value":args.source_archive_sha256},
        {"field":"root_request_rows","value":28},{"field":"supply_batch_rows","value":6},{"field":"locator_root_rows_reviewed","value":28},
        {"field":"complete_custodian_exports","value":0},{"field":"partial_custodian_exports","value":0},{"field":"absent_custodian_exports","value":28},
        {"field":"record_files_reviewed","value":0},{"field":"github_locator_surfaces_reviewed","value":3},{"field":"build_attestations_accepted","value":0},
        {"field":"final_provider_decisions_accepted","value":0},{"field":"target_rows_populated","value":0},{"field":"rules_sha256","value":sha256(args.rules)},
        {"field":"source_inventory_sha256","value":sha256(locator/"sup-02-local-record-inventory.tsv")},{"field":"source_root_locator_sha256","value":sha256(locator/"sup-02-root-provenance-locator.tsv")},
        {"field":"source_custodian_surface_sha256","value":sha256(locator/"sup-02-custodian-surface.tsv")},{"field":"source_summary_sha256","value":sha256(locator/"summary.tsv")},
        {"field":"receipt_review_sha256","value":sha256(overall_path)},{"field":"root_review_sha256","value":sha256(root_path)},{"field":"surface_review_sha256","value":sha256(surface_path)},
        {"field":"next_state","value":NEXT},
    ]
    write_tsv(args.out/"generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-provenance-locator-receipt-review-metadata.tsv",["field","value"],metadata)
    (args.out/"analysis.status").write_text("PASS\n",encoding="utf-8")
    (args.out/"claim-boundary.txt").write_text(REVIEW_CLAIM+"\n",encoding="utf-8")
    (args.out/"next-state.txt").write_text(NEXT+"\n",encoding="utf-8")
    print("SUP02_PROVENANCE_LOCATOR_RECEIPT_REVIEW=PASS roots=28 complete=0 partial=0 absent=28 records=0 accepted=0")
    return 0

if __name__=="__main__": raise SystemExit(main())
