#!/usr/bin/env python3
"""Review the exact production SUP-02 custodian-export response acquisition receipt."""
from __future__ import annotations
import argparse, csv, hashlib, re
from pathlib import Path
from typing import Iterable, NoReturn
EXPECTED_HEAD="d4d7eb4f452b392b9605fa9863a4ba731869d222"
EXPECTED_TREE="8432d4a731a2dc20047982b7a71b74e5a885ba0a"
EXPECTED_ARCHIVE_SHA="24ba9cb735e9dff3c48b8805210a955bc6c46440eb925301cb1899796da13849"
EXPECTED_ISSUANCE_SHA="64a0932ede3920b868bd922726db1336884be1f1b53e24dda7ef216fa6dced71"
EXPECTED_CONTRACT_SHA="5e18dee415443a0e5e39040d0147844eeeb6aa3b71a96107c9d51a31056af628"
SOURCE_CLAIM="CANDIDATE_CUSTODIAN_EXPORT_RESPONSE_REVIEW_REQUIRED_NO_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT"
REVIEW_CLAIM="CUSTODIAN_EXPORT_RESPONSE_ACQUISITION_RECEIPT_REVIEW_ACCEPTS_NO_RESPONSE_ONLY_NO_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT"
SOURCE_NEXT="REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSE_ACQUISITION_RECEIPT"
NEXT="FULFILL_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSES"
STATUS_FIELDS=["request_id","root_review_id","recipe_root","recipe_tree","issued_request_locator","response_drop_locator","response_state","verified_record_count","build_run_id","custodian_identity","immutable_locator_or_signed_envelope","candidate_response_path","build_attestation_state","claim_boundary","next_action"]
INVENTORY_FIELDS=["response_record_id","request_id","requirement_id","record_name","record_format","source_relative_path","candidate_relative_path","sha256","size_bytes","format_validation","build_run_id","custodian_identity","immutable_locator_or_signed_envelope","acceptance_state","claim_boundary"]
def fail(m:str)->NoReturn: raise SystemExit(f"SUP-02 response acquisition receipt review: FAIL: {m}")
def require(v:bool,m:str)->None:
    if not v: fail(m)
def sha256(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def read_tsv(p:Path, fields:list[str]|None=None)->list[dict[str,str]]:
    if not p.is_file() or p.is_symlink(): fail(f"missing regular input: {p}")
    with p.open(encoding='utf-8',newline='') as f:
        r=csv.DictReader(f,delimiter='\t'); actual=r.fieldnames or []
        if fields is not None and actual!=fields: fail(f"header drift: {p}")
        return [{k:(v or '') for k,v in row.items()} for row in r]
def write_tsv(p:Path, fields:list[str], rows:Iterable[dict[str,object]])->None:
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n',extrasaction='ignore'); w.writeheader()
        for row in rows:w.writerow({x:row.get(x,'') for x in fields})
def unique(rows:list[dict[str,str]], key:str)->dict[str,dict[str,str]]:
    out={}
    for row in rows:
        value=row.get(key,'')
        if not value or value in out: fail(f"duplicate or empty {key}: {value!r}")
        out[value]=row
    return out
def kv(rows:list[dict[str,str]])->dict[str,str]: return {r['field']:r['value'] for r in rows}
def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--request-issuance',required=True,type=Path); ap.add_argument('--record-contract-issuance',required=True,type=Path)
    ap.add_argument('--receipt-dir',required=True,type=Path); ap.add_argument('--rules',required=True,type=Path)
    ap.add_argument('--source-head',default=EXPECTED_HEAD); ap.add_argument('--source-tree',default=EXPECTED_TREE); ap.add_argument('--source-archive-sha256',default=EXPECTED_ARCHIVE_SHA)
    ap.add_argument('--out',required=True,type=Path); a=ap.parse_args()
    for label,value,expected,pattern in [('head',a.source_head,EXPECTED_HEAD,r'[0-9a-f]{40}'),('tree',a.source_tree,EXPECTED_TREE,r'[0-9a-f]{40}'),('archive',a.source_archive_sha256,EXPECTED_ARCHIVE_SHA,r'[0-9a-f]{64}')]:
        require(re.fullmatch(pattern,value) is not None,f"invalid source {label}"); require(value==expected,f"source {label} drift")
    require(not a.out.exists() and not a.out.is_symlink(),f"refusing existing output: {a.out}")
    rules=read_tsv(a.rules,["rule_id","dimension","scope","acceptance_rule","rejection_rule","authority_effect"])
    require(len(rules)==10 and [r['rule_id'] for r in rules]==[f'SUP02R-R{i:02d}' for i in range(1,11)],'review rule drift')
    issuance=read_tsv(a.request_issuance); contracts=read_tsv(a.record_contract_issuance)
    require(len(issuance)==28 and len(contracts)==84,'issuance denominator drift')
    require(sha256(a.request_issuance)==EXPECTED_ISSUANCE_SHA,'issuance digest drift'); require(sha256(a.record_contract_issuance)==EXPECTED_CONTRACT_SHA,'contract digest drift')
    issue_i=unique(issuance,'request_id')
    require(all(r['request_state']=='REQUEST_ISSUED_REPOSITORY_PUBLICATION' and r['acknowledgement_state']=='NOT_ACKNOWLEDGED' and r['responses_received']=='0' and r['build_attestations_accepted']=='0' for r in issuance),'issuance state drift')
    contract_keys={(r['request_id'],r['record_name']) for r in contracts}
    require(len(contract_keys)==84 and all(r['record_state']=='ISSUED_REQUIRED_NOT_SUPPLIED' and r['acceptance_state']=='OPEN_NO_ACCEPTANCE' for r in contracts),'record contract state drift')
    d=a.receipt_dir
    require(d.is_dir() and not d.is_symlink(),'unsafe receipt directory')
    require((d/'analysis.status').read_text()=='PASS\n','analysis status drift'); require((d/'claim-boundary.txt').read_text().strip()==SOURCE_CLAIM,'source claim drift'); require((d/'next-state.txt').read_text().strip()==SOURCE_NEXT,'source next-state drift')
    summary=kv(read_tsv(d/'summary.tsv',["field","value"]))
    expected={'source_head':'636aad838111d37be0ab8bd8364aa5795b32256d','source_tree':'3a20228415cb835267e34ea0c10be6297d00cdaf','request_issuance_sha256':EXPECTED_ISSUANCE_SHA,'record_contract_issuance_sha256':EXPECTED_CONTRACT_SHA,'response_input_root_state':'ABSENT','issued_requests':'28','issued_record_contracts':'84','complete_candidate_responses_acquired':'0','requests_without_response':'28','verified_response_records':'0','verified_response_bytes':'0','requests_acknowledged':'0','responses_accepted':'0','build_attestations_accepted':'0','final_provider_decisions_accepted':'0','target_rows_populated':'0','claim_boundary':SOURCE_CLAIM,'next_state':SOURCE_NEXT}
    require(summary==expected,'receipt summary drift')
    statuses=read_tsv(d/'request-response-acquisition-status.tsv',STATUS_FIELDS); require(len(statuses)==28,'status denominator drift')
    status_i=unique(statuses,'request_id'); require(set(status_i)==set(issue_i),'request identity set drift')
    root_review=[]
    for request_id,issued in issue_i.items():
        row=status_i[request_id]
        for f in ('root_review_id','recipe_root','recipe_tree','issued_request_locator','response_drop_locator'): require(row[f]==issued[f],f"request binding drift: {request_id} {f}")
        require(row['response_state']=='NO_RESPONSE_DROP_PRESENT' and row['verified_record_count']=='0','invented response state')
        require(row['build_run_id']=='-' and row['custodian_identity']=='-' and row['immutable_locator_or_signed_envelope']=='-' and row['candidate_response_path']=='-','invented response identity')
        require(row['build_attestation_state']=='OPEN_NO_ACCEPTANCE' and row['claim_boundary']==SOURCE_CLAIM and row['next_action']=='AWAIT_EXACT_CUSTODIAN_EXPORT_RESPONSE','response boundary drift')
        root_review.append({'request_id':request_id,'root_review_id':row['root_review_id'],'recipe_root':row['recipe_root'],'recipe_tree':row['recipe_tree'],'response_receipt_state':'CONFIRMED_NO_RESPONSE_DROP_PRESENT','acknowledgement_state':'NOT_ACKNOWLEDGED','ba_001_state':'OPEN_EXACT_RESPONSE_REQUIRED','ba_002_state':'OPEN_EXACT_RESPONSE_REQUIRED','ba_003_state':'OPEN_EXACT_RESPONSE_REQUIRED','build_attestation_state':'OPEN_NO_ACCEPTANCE','final_provider_state':'UNRESOLVED','target_population_state':'UNPOPULATED','next_action':'FULFILL_EXACT_CUSTODIAN_EXPORT_RESPONSE'})
    require(read_tsv(d/'response-record-inventory.tsv',INVENTORY_FIELDS)==[],'response record inventory must be header-only')
    candidate=d/'candidate-response-root'; require(candidate.is_dir() and not candidate.is_symlink() and not any(candidate.iterdir()),'candidate root must be empty')
    a.out.mkdir(parents=True)
    overall_path=a.out/'generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-acquisition-receipt-review.tsv'
    roots_path=a.out/'generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-root-custodian-export-response-acquisition-receipt-review.tsv'
    overall=[{'review_id':'sup-02-response-acquisition-receipt-review:production-20260714T051519Z','batch_id':'SUP-02','requirement_ids':'BA-001;BA-002;BA-003','issued_requests':28,'complete_candidate_responses':0,'requests_without_response':28,'verified_response_records':0,'receipt_decision':'PASS_BOUNDED_NO_CUSTODIAN_EXPORT_RESPONSES_ACQUIRED','requests_acknowledged':0,'responses_accepted':0,'build_attestations_accepted':0,'final_provider_decisions_accepted':0,'target_rows_populated':0,'claim_boundary':REVIEW_CLAIM,'next_action':'FULFILL_EXACT_SUP_02_CUSTODIAN_EXPORT_RESPONSES'}]
    write_tsv(overall_path,["review_id","batch_id","requirement_ids","issued_requests","complete_candidate_responses","requests_without_response","verified_response_records","receipt_decision","requests_acknowledged","responses_accepted","build_attestations_accepted","final_provider_decisions_accepted","target_rows_populated","claim_boundary","next_action"],overall)
    write_tsv(roots_path,["request_id","root_review_id","recipe_root","recipe_tree","response_receipt_state","acknowledgement_state","ba_001_state","ba_002_state","ba_003_state","build_attestation_state","final_provider_state","target_population_state","next_action"],root_review)
    metadata=[{'field':'source_head','value':a.source_head},{'field':'source_tree','value':a.source_tree},{'field':'source_archive_sha256','value':a.source_archive_sha256},{'field':'issued_requests_reviewed','value':28},{'field':'record_contracts_reviewed','value':84},{'field':'complete_candidate_responses','value':0},{'field':'requests_without_response','value':28},{'field':'verified_response_records','value':0},{'field':'requests_acknowledged','value':0},{'field':'responses_accepted','value':0},{'field':'build_attestations_accepted','value':0},{'field':'final_provider_decisions_accepted','value':0},{'field':'target_rows_populated','value':0},{'field':'rules_sha256','value':sha256(a.rules)},{'field':'source_status_sha256','value':sha256(d/'request-response-acquisition-status.tsv')},{'field':'source_inventory_sha256','value':sha256(d/'response-record-inventory.tsv')},{'field':'source_summary_sha256','value':sha256(d/'summary.tsv')},{'field':'receipt_review_sha256','value':sha256(overall_path)},{'field':'root_review_sha256','value':sha256(roots_path)},{'field':'next_state','value':NEXT}]
    write_tsv(a.out/'generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-acquisition-receipt-review-metadata.tsv',["field","value"],metadata)
    (a.out/'analysis.status').write_text('PASS\n'); (a.out/'claim-boundary.txt').write_text(REVIEW_CLAIM+'\n'); (a.out/'next-state.txt').write_text(NEXT+'\n')
    print('SUP02_CUSTODIAN_EXPORT_RESPONSE_ACQUISITION_RECEIPT_REVIEW=PASS requests=28 responses=0 accepted=0')
    return 0
if __name__=='__main__': raise SystemExit(main())
