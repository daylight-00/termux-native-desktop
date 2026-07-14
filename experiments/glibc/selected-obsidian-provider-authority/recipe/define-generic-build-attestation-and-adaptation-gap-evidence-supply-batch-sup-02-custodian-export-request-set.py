#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib
from pathlib import Path
from typing import Iterable, NoReturn

EXPECTED_ROOTS=28
CLAIM="CUSTODIAN_EXPORT_REQUEST_SET_ONLY_NO_REQUEST_ISSUANCE_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT"
NEXT="ISSUE_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_REQUEST_SET"
RECORDS=(
 ("build-invocation-record.json","BA-001","JSON_OBJECT","schema_version;request_id;root_review_id;recipe_root;recipe_tree;build_run_id;build_started_at_utc;build_finished_at_utc;working_directory;invocation_argv;input_source_digests;build_script_digest;custodian_identity;immutable_locator_or_signed_envelope"),
 ("build-environment-record.json","BA-002","JSON_OBJECT","schema_version;request_id;root_review_id;recipe_tree;build_run_id;host_os;host_kernel;host_arch;toolchain_components;toolchain_digests;dependency_lock_or_snapshot;container_or_vm_image_digest;relevant_environment;source_date_epoch;custodian_identity;immutable_locator_or_signed_envelope"),
 ("build-output-manifest.tsv","BA-003","TSV_WITH_ROWS","request_id;root_review_id;recipe_root;recipe_tree;build_run_id;package_name;package_version;package_revision;artifact_path;artifact_sha256;member_path;member_sha256;member_elf_soname;custodian_identity;immutable_locator_or_signed_envelope"),
)

def fail(msg:str)->NoReturn: raise SystemExit(f"sup-02 custodian request set: FAIL: {msg}")
def read_tsv(p:Path)->list[dict[str,str]]:
    if not p.is_file() or p.is_symlink(): fail(f"missing regular input: {p}")
    with p.open(encoding="utf-8",newline="") as f:
        r=csv.DictReader(f,delimiter="\t")
        if not r.fieldnames: fail(f"missing header: {p}")
        return [{k:(v or "") for k,v in row.items()} for row in r]
def write_tsv(p:Path, fields:list[str], rows:Iterable[dict[str,object]])->None:
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n",extrasaction="ignore"); w.writeheader()
        for row in rows: w.writerow({k:row.get(k,"") for k in fields})
def sha(p:Path)->str:
    h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def token(s:str)->str: return s.rsplit(":",1)[-1]

def main()->None:
    ap=argparse.ArgumentParser(); ap.add_argument("--root-review",type=Path,required=True); ap.add_argument("--source-head",required=True); ap.add_argument("--source-tree",required=True); ap.add_argument("--out",type=Path,required=True); a=ap.parse_args()
    roots=read_tsv(a.root_review)
    if len(roots)!=EXPECTED_ROOTS: fail(f"expected {EXPECTED_ROOTS} roots, got {len(roots)}")
    seen=set(); req=[]; contracts=[]
    for r in roots:
        rid=r.get("root_review_id",""); aid=r.get("acquisition_unit_id","")
        if not rid or rid in seen: fail("missing or duplicate root_review_id")
        seen.add(rid)
        if r.get("locator_receipt_state")!="CONFIRMED_NO_EXISTING_CUSTODIAN_EXPORT": fail(f"locator state drift: {rid}")
        if r.get("next_action")!="INCLUDE_IN_SUP_02_CUSTODIAN_EXPORT_REQUEST_SET": fail(f"next action drift: {rid}")
        request_id=f"SUP02-CER-{token(rid)}"
        response_dir=f"evidence-supply/responses/SUP-02/{request_id}/"
        req.append({
          "request_id":request_id,"batch_id":"SUP-02","acquisition_unit_id":aid,"root_review_id":rid,
          "recipe_root":r["recipe_root"],"recipe_tree":r["recipe_tree"],"requirement_ids":"BA-001;BA-002;BA-003",
          "supplier_role":"PRODUCING_BUILD_RECORD_CUSTODIAN","one_build_linkage":"SAME_BUILD_RUN_ID_RECIPE_TREE_AND_ARTIFACT_SET_ACROSS_ALL_THREE_RECORDS",
          "required_record_names":"build-invocation-record.json;build-environment-record.json;build-output-manifest.tsv",
          "custodian_binding":"NAMED_CUSTODIAN_IDENTITY_AND_IMMUTABLE_LOCATOR_OR_SIGNED_ENVELOPE_REQUIRED",
          "response_directory":response_dir,
          "completion_gate":"ALL_THREE_RECORDS_VALID_DIGEST_BOUND_AND_CROSS_LINKED_TO_ONE_PRODUCING_BUILD",
          "request_state":"REQUEST_DEFINED_NOT_ISSUED","responses_received":0,"build_attestations_accepted":0,
          "claim_boundary":CLAIM,"next_action":"ISSUE_EXACT_CUSTODIAN_EXPORT_REQUEST"})
        for name,reqid,fmt,fields in RECORDS:
            contracts.append({"request_id":request_id,"root_review_id":rid,"recipe_root":r["recipe_root"],"recipe_tree":r["recipe_tree"],
              "requirement_id":reqid,"record_name":name,"record_format":fmt,"mandatory_fields":fields,
              "cross_record_binding":"request_id;root_review_id;recipe_tree;build_run_id;custodian_identity;immutable_locator_or_signed_envelope",
              "record_state":"REQUIRED_NOT_SUPPLIED","acceptance_state":"OPEN_NO_ACCEPTANCE","claim_boundary":CLAIM})
    a.out.mkdir(parents=True,exist_ok=False)
    req_path=a.out/"generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-requests.tsv"
    con_path=a.out/"generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-record-contracts.tsv"
    write_tsv(req_path,["request_id","batch_id","acquisition_unit_id","root_review_id","recipe_root","recipe_tree","requirement_ids","supplier_role","one_build_linkage","required_record_names","custodian_binding","response_directory","completion_gate","request_state","responses_received","build_attestations_accepted","claim_boundary","next_action"],req)
    write_tsv(con_path,["request_id","root_review_id","recipe_root","recipe_tree","requirement_id","record_name","record_format","mandatory_fields","cross_record_binding","record_state","acceptance_state","claim_boundary"],contracts)
    meta=a.out/"generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-request-set-metadata.tsv"
    write_tsv(meta,["field","value"],[
      {"field":"source_head","value":a.source_head},{"field":"source_tree","value":a.source_tree},
      {"field":"root_requests","value":len(req)},{"field":"record_contracts","value":len(contracts)},
      {"field":"ba_001_record_contracts","value":EXPECTED_ROOTS},{"field":"ba_002_record_contracts","value":EXPECTED_ROOTS},{"field":"ba_003_record_contracts","value":EXPECTED_ROOTS},
      {"field":"requests_issued","value":0},{"field":"responses_received","value":0},{"field":"build_attestations_accepted","value":0},{"field":"final_provider_decisions_accepted","value":0},{"field":"target_rows_populated","value":0},
      {"field":"request_set_sha256","value":sha(req_path)},{"field":"record_contracts_sha256","value":sha(con_path)},
      {"field":"claim_boundary","value":CLAIM},{"field":"next_state","value":NEXT}])
    (a.out/"analysis.status").write_text("PASS\n",encoding="utf-8")
    (a.out/"claim-boundary.txt").write_text(CLAIM+"\n",encoding="utf-8")
    (a.out/"next-state.txt").write_text(NEXT+"\n",encoding="utf-8")
if __name__=="__main__": main()
