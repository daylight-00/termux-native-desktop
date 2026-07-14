#!/usr/bin/env python3
"""Review the bounded 0154 gap-evidence acquisition receipt without accepting evidence."""
from __future__ import annotations
import argparse, csv, hashlib, re
from pathlib import Path
from typing import Iterable, NoReturn

EXPECTED_BRANCH='docs/post-graphics-architecture-audit'
EXPECTED_HEAD='54afd42dcce27be00d70550facb5e0ceb391ce38'
EXPECTED_TREE='8c34d8987c98923a3b623a4d1be5304fe20b4964'
EXPECTED_COUNTS={'source_contract_rows':10,'lane_rows':6,'requirement_rows':16,'root_acquisition_rows':28,'object_acquisition_rows':37,'input_manifest_rows':0,'candidate_evidence_files_acquired':0,'candidate_requirements':0,'local_foundation_only_requirements':6,'direct_gap_unavailable_requirements':10,'root_units_with_candidates':0,'object_units_with_candidates':0,'artifact_build_attestations_accepted':0,'termux_android_adaptations_accepted':0,'concrete_filename_drifts_accepted':0,'object_corrections_accepted':0,'final_provider_decisions_accepted':0,'target_rows_populated':0}
CLAIM='CANDIDATE_EVIDENCE_REVIEW_REQUIRED_NO_AUTHORITY_EFFECT'
ACQUIRER_NEXT='REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUISITION_RECEIPT'
NEXT='DEFINE_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_REQUEST_SET'
AUTH='OPEN_NO_ACCEPTANCE'; TARGET='UNPOPULATED'; PROVIDER='UNRESOLVED'
LOCAL={'BA-003','AD-001','AD-002','AD-004','AD-006','CF-002'}
DIRECT={'BA-001','BA-002','BA-004','BA-005','AD-003','AD-005','CF-001','CF-003','CF-004','OJ-001'}
REQ_LOCAL_REVIEW='LOCAL_FOUNDATION_NO_NEW_ACQUISITION_REVIEWED_OPEN'
REQ_GAP_REVIEW='ACQUISITION_INPUT_UNAVAILABLE_GAP_REVIEWED_OPEN'
LANE_REVIEW='NO_ACQUISITION_INPUTS_PRESERVED_REVIEWED'
UNIT_REVIEW='BOUNDED_ACQUISITION_INPUTS_REVIEWED_INCOMPLETE'

def fail(msg:str)->NoReturn: raise SystemExit(f'generic gap-evidence acquisition receipt review: FAIL: {msg}')
def read_tsv(path:Path)->tuple[list[str],list[dict[str,str]]]:
    if not path.is_file() or path.is_symlink(): fail(f'missing regular input: {path}')
    with path.open(encoding='utf-8',newline='') as f:
        r=csv.DictReader(f,delimiter='\t'); fields=r.fieldnames or []
        if not fields: fail(f'missing TSV header: {path}')
        return fields,[{k:(v or '') for k,v in row.items()} for row in r]
def write_tsv(path:Path,fields:list[str],rows:Iterable[dict[str,object]])->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n',extrasaction='ignore'); w.writeheader()
        for row in rows: w.writerow({k:row.get(k,'') for k in fields})
def kv(path:Path)->dict[str,str]:
    if not path.is_file() or path.is_symlink(): fail(f'missing regular key/value input: {path}')
    out={}
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line: continue
        if '=' not in line: fail(f'invalid key/value line: {line}')
        k,v=line.split('=',1)
        if not k or k in out: fail(f'duplicate/empty key: {k!r}')
        out[k]=v
    return out
def sha(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def idx(rows:list[dict[str,str]],key:str,label:str)->dict[str,dict[str,str]]:
    out={}
    for row in rows:
        v=row.get(key,'')
        if not v or v in out: fail(f'duplicate/empty {key} in {label}: {v!r}')
        out[v]=row
    return out
def sset(v:str)->set[str]: return {x for x in v.split(';') if x and x!='NONE'}
def intval(v:str,label:str)->int:
    try:return int(v)
    except ValueError: fail(f'invalid integer {label}: {v!r}')
def require_exact_keys(actual:dict[str,str],expected:dict[str,str],label:str)->None:
    if actual!=expected: fail(f'{label} mismatch: {actual}')

def main()->int:
    p=argparse.ArgumentParser()
    for name in ['source-contracts','lanes','requirements','root-set','object-set','input-verification','acquisition-inventory','requirement-status','lane-status','root-status','object-status','unavailable-inputs','evidence-manifest','summary','analysis-status','claim-boundary','acquirer-next-state','acquirer-input','transaction-status','final-git-state','remote-state','rules']:
        p.add_argument('--'+name,required=True,type=Path)
    p.add_argument('--source-receipt-archive',required=True); p.add_argument('--source-receipt-sha256',required=True)
    p.add_argument('--expected-branch',default=EXPECTED_BRANCH); p.add_argument('--expected-source-head',default=EXPECTED_HEAD); p.add_argument('--expected-source-tree',default=EXPECTED_TREE); p.add_argument('--next-state',default=NEXT); p.add_argument('--out',required=True,type=Path)
    a=p.parse_args()
    if a.out.exists() or a.out.is_symlink(): fail(f'refusing existing output: {a.out}')
    if not re.fullmatch(r'[0-9a-f]{64}',a.source_receipt_sha256): fail('invalid source receipt SHA')
    if not re.fullmatch(r'[0-9a-f]{40}',a.expected_source_head) or not re.fullmatch(r'[0-9a-f]{40}',a.expected_source_tree): fail('invalid expected Git identity')
    require_exact_keys(kv(a.transaction_status),{'TRANSACTION':'PASS','VALIDATION':'PASS','GAP_EVIDENCE_ACQUIRER':'PASS_BOUNDED','PUSH_AFTER_APPLY':'1'},'transaction status')
    require_exact_keys(kv(a.final_git_state),{'branch':a.expected_branch,'head':a.expected_source_head,'tree':a.expected_source_tree},'final Git state')
    rem=kv(a.remote_state)
    if rem.get('push_after_apply')!='1' or rem.get('remote_head_after')!=a.expected_source_head: fail(f'remote state mismatch: {rem}')
    acq_input=kv(a.acquirer_input)
    if acq_input.get('input_state')!='ABSENT_NO_ACQUISITION_INPUT' or acq_input.get('candidate_evidence_files')!='0' or not acq_input.get('input_root'): fail(f'acquirer input mismatch: {acq_input}')
    if a.analysis_status.read_text(encoding='utf-8')!='PASS\n': fail('analysis status mismatch')
    if a.claim_boundary.read_text(encoding='utf-8').strip()!=CLAIM: fail('claim boundary drift')
    if a.acquirer_next_state.read_text(encoding='utf-8').strip()!=ACQUIRER_NEXT: fail('acquirer next-state drift')

    _,contracts=read_tsv(a.source_contracts); _,lanes=read_tsv(a.lanes); _,reqs=read_tsv(a.requirements); _,roots=read_tsv(a.root_set); _,objs=read_tsv(a.object_set)
    if [len(contracts),len(lanes),len(reqs),len(roots),len(objs)]!=[10,6,16,28,37]: fail('canonical denominator drift')
    contract_i=idx(contracts,'source_kind','contracts'); lane_i=idx(lanes,'lane_id','lanes'); req_i=idx(reqs,'requirement_id','requirements'); root_i=idx(roots,'acquisition_unit_id','roots'); obj_i=idx(objs,'acquisition_unit_id','objects')
    if set(req_i)!=LOCAL|DIRECT: fail('requirement identity drift')
    for row in contracts:
        if row['claim_boundary']!=CLAIM or row['authority_state']!=AUTH: fail(f'contract claim/authority drift: {row["source_kind"]}')
    for row in reqs:
        if row['lane_id'] not in lane_i or row['claim_boundary']!=CLAIM or row['authority_state']!=AUTH or row['acquisition_state']!='ACQUISITION_WORK_UNIT_DEFINED_NOT_EXECUTED': fail(f'canonical requirement drift: {row["requirement_id"]}')
    for row in roots:
        if row['manifest_scope_kind']!='ROOT' or row['authority_state']!=AUTH: fail(f'canonical root drift: {row["acquisition_unit_id"]}')
    for row in objs:
        if row['manifest_scope_kind']!='OBJECT' or row['authority_state']!=AUTH or row['final_provider_state']!=PROVIDER or row['target_population_state']!=TARGET: fail(f'canonical object drift: {row["acquisition_unit_id"]}')

    _,verify=read_tsv(a.input_verification); verify_i=idx(verify,'input_name','input verification')
    canon={'source_contracts':a.source_contracts,'acquisition_lanes':a.lanes,'acquisition_requirements':a.requirements,'root_acquisition_set':a.root_set,'object_acquisition_set':a.object_set}
    for name,path in canon.items():
        row=verify_i.get(name)
        if not row or row['sha256']!=sha(path) or row['state']!='CANONICAL_REGULAR_FILE_VERIFIED': fail(f'canonical input verification drift: {name}')
    if verify_i.get('acquisition_input_root',{}).get('state')!='ABSENT_NO_ACQUISITION_INPUT': fail('input-root verification drift')

    _,summary_rows=read_tsv(a.summary); sm={r['field']:r['value'] for r in summary_rows}
    for k,v in EXPECTED_COUNTS.items():
        if intval(sm.get(k,''),k)!=v: fail(f'summary count drift: {k}')
    if sm.get('acquisition_input_root_state')!='ABSENT_NO_ACQUISITION_INPUT' or sm.get('next_state')!=ACQUIRER_NEXT: fail('summary state drift')
    if not re.fullmatch(r'[0-9a-f]{64}',sm.get('evidence_manifest_sha256','')) or sm['evidence_manifest_sha256']!=sha(a.evidence_manifest): fail('evidence manifest digest drift')

    ef,ev=read_tsv(a.evidence_manifest)
    expected_ef=['evidence_id','requirement_id','lane_id','scope_kind','scope_id','evidence_class','source_kind','source_locator','relative_path','sha256','size_bytes','claim_boundary']
    if ef!=expected_ef or ev: fail('expected header-only evidence manifest')
    _,inventory=read_tsv(a.acquisition_inventory)
    if inventory: fail('unexpected acquisition inventory rows')

    _,req_status=read_tsv(a.requirement_status); _,lane_status=read_tsv(a.lane_status); _,root_status=read_tsv(a.root_status); _,obj_status=read_tsv(a.object_status); _,unavail=read_tsv(a.unavailable_inputs)
    req_s=idx(req_status,'requirement_id','requirement status'); lane_s=idx(lane_status,'lane_id','lane status'); root_s=idx(root_status,'acquisition_unit_id','root status'); obj_s=idx(obj_status,'acquisition_unit_id','object status'); un_s=idx(unavail,'requirement_id','unavailable inputs')
    if set(req_s)!=set(req_i) or set(lane_s)!=set(lane_i) or set(root_s)!=set(root_i) or set(obj_s)!=set(obj_i) or set(un_s)!=set(req_i): fail('receipt identity denominator drift')

    req_out=[]
    for rid in sorted(req_i):
        c=req_i[rid]; r=req_s[rid]; u=un_s[rid]
        for f in ['lane_id','closure_class','acquisition_class','manifest_scope_kind']:
            if r[f]!=c[f]: fail(f'requirement field drift {rid}:{f}')
        if r['candidate_input_count']!='0' or r['evidence_ids']!='NONE' or r['claim_boundary']!=CLAIM or r['authority_state']!=AUTH or r['closure_state']!='OPEN_SEPARATE_REVIEW_REQUIRED': fail(f'requirement receipt promotion: {rid}')
        expected_state='LOCAL_FOUNDATION_ONLY_NO_NEW_ACQUISITION' if rid in LOCAL else 'ACQUISITION_INPUT_UNAVAILABLE_EXPLICIT_GAP'
        if r['acquisition_state']!=expected_state or u['unavailable_state']!=expected_state: fail(f'requirement unavailable state drift: {rid}')
        if u['lane_id']!=c['lane_id'] or u['closure_class']!=c['closure_class'] or u['manifest_scope_kind']!=c['manifest_scope_kind'] or u['claim_boundary']!=CLAIM: fail(f'unavailable row drift: {rid}')
        review=REQ_LOCAL_REVIEW if rid in LOCAL else REQ_GAP_REVIEW
        req_out.append({'requirement_id':rid,'lane_id':c['lane_id'],'dimension':c['dimension'],'scope':c['scope'],'closure_class':c['closure_class'],'acquisition_class':c['acquisition_class'],'manifest_scope_kind':c['manifest_scope_kind'],'candidate_input_count':'0','acquirer_state':r['acquisition_state'],'receipt_review_state':review,'remaining_gap_class':c['remaining_gap_class'],'deliverable_contract':c['deliverable_contract'],'completion_gate':c['completion_gate'],'closure_state':'OPEN_EVIDENCE_SUPPLY_REQUIRED','authority_state':AUTH,'next_action':'INCLUDE_IN_BOUNDED_EVIDENCE_SUPPLY_REQUEST_SET'})

    lane_out=[]
    for lid in sorted(lane_i):
        c=lane_i[lid]; r=lane_s[lid]
        if sset(r['requirement_ids'])!=sset(c['requirement_ids']) or r['candidate_input_count']!='0' or r['candidate_requirement_ids']!='NONE' or r['acquisition_state']!='NO_NEW_INPUTS_CLOSURE_REMAINS_OPEN' or r['claim_boundary']!=CLAIM or r['authority_state']!=AUTH: fail(f'lane receipt drift: {lid}')
        if r['completion_gate']!=c['completion_gate'] or r['stop_condition']!=c['stop_condition']: fail(f'lane criteria drift: {lid}')
        lane_out.append({'lane_id':lid,'priority':c['priority'],'lane_class':c['lane_class'],'requirement_ids':';'.join(sorted(sset(c['requirement_ids']))),'candidate_input_count':'0','unavailable_requirement_ids':r['unavailable_requirement_ids'],'local_foundation_only_requirement_ids':r['local_foundation_only_requirement_ids'],'receipt_review_state':LANE_REVIEW,'completion_gate':c['completion_gate'],'stop_condition':c['stop_condition'],'closure_state':'OPEN_EVIDENCE_SUPPLY_REQUIRED','authority_state':AUTH})

    root_out=[]
    for uid in sorted(root_i):
        c=root_i[uid]; r=root_s[uid]
        for f in ['root_review_id','recipe_root','recipe_tree','requirement_ids','completion_gate']:
            if r[f]!=c[f]: fail(f'root field drift {uid}:{f}')
        if r['candidate_input_count']!='0' or r['candidate_requirement_ids']!='NONE' or r['evidence_ids']!='NONE' or r['missing_requirement_ids']!=c['requirement_ids'] or r['acquisition_state']!='ROOT_NO_NEW_INPUTS_CLOSURE_OPEN' or r['claim_boundary']!=CLAIM or r['authority_state']!=AUTH: fail(f'root receipt drift: {uid}')
        root_out.append({'acquisition_unit_id':uid,'root_review_id':c['root_review_id'],'recipe_root':c['recipe_root'],'recipe_tree':c['recipe_tree'],'requirement_ids':c['requirement_ids'],'candidate_input_count':'0','missing_requirement_ids':c['requirement_ids'],'receipt_review_state':UNIT_REVIEW,'completion_gate':c['completion_gate'],'closure_state':'OPEN_EVIDENCE_SUPPLY_REQUIRED','authority_state':AUTH})

    obj_out=[]
    for uid in sorted(obj_i):
        c=obj_i[uid]; r=obj_s[uid]
        for f in ['object_review_id','evidence_row_id','identity_label','artifact_sha256','recipe_root','object_class','requirement_ids','completion_gate']:
            if r[f]!=c[f]: fail(f'object field drift {uid}:{f}')
        if r['candidate_input_count']!='0' or r['candidate_requirement_ids']!='NONE' or r['evidence_ids']!='NONE' or r['missing_requirement_ids']!=c['requirement_ids'] or r['acquisition_state']!='OBJECT_NO_NEW_INPUTS_CLOSURE_OPEN' or r['claim_boundary']!=CLAIM or r['authority_state']!=AUTH or r['final_provider_state']!=PROVIDER or r['target_population_state']!=TARGET: fail(f'object receipt drift: {uid}')
        obj_out.append({'acquisition_unit_id':uid,'object_review_id':c['object_review_id'],'evidence_row_id':c['evidence_row_id'],'identity_label':c['identity_label'],'artifact_id':c['artifact_id'],'artifact_sha256':c['artifact_sha256'],'recipe_root':c['recipe_root'],'object_class':c['object_class'],'requirement_ids':c['requirement_ids'],'candidate_input_count':'0','missing_requirement_ids':c['requirement_ids'],'receipt_review_state':UNIT_REVIEW,'completion_gate':c['completion_gate'],'final_provider_state':PROVIDER,'closure_state':'OPEN_EVIDENCE_SUPPLY_REQUIRED','authority_state':AUTH,'target_population_state':TARGET})

    a.out.mkdir(parents=True)
    reqp=a.out/'generic-build-attestation-adaptation-gap-evidence-acquisition-receipt-review.tsv'; lanep=a.out/'generic-build-attestation-adaptation-gap-evidence-acquisition-lane-receipt-review.tsv'; rootp=a.out/'generic-build-attestation-adaptation-root-gap-evidence-acquisition-receipt-review.tsv'; objp=a.out/'generic-build-attestation-adaptation-object-gap-evidence-acquisition-receipt-review.tsv'; metap=a.out/'generic-build-attestation-adaptation-gap-evidence-acquisition-receipt-review-metadata.tsv'
    write_tsv(reqp,['requirement_id','lane_id','dimension','scope','closure_class','acquisition_class','manifest_scope_kind','candidate_input_count','acquirer_state','receipt_review_state','remaining_gap_class','deliverable_contract','completion_gate','closure_state','authority_state','next_action'],req_out)
    write_tsv(lanep,['lane_id','priority','lane_class','requirement_ids','candidate_input_count','unavailable_requirement_ids','local_foundation_only_requirement_ids','receipt_review_state','completion_gate','stop_condition','closure_state','authority_state'],lane_out)
    write_tsv(rootp,['acquisition_unit_id','root_review_id','recipe_root','recipe_tree','requirement_ids','candidate_input_count','missing_requirement_ids','receipt_review_state','completion_gate','closure_state','authority_state'],root_out)
    write_tsv(objp,['acquisition_unit_id','object_review_id','evidence_row_id','identity_label','artifact_id','artifact_sha256','recipe_root','object_class','requirement_ids','candidate_input_count','missing_requirement_ids','receipt_review_state','completion_gate','final_provider_state','closure_state','authority_state','target_population_state'],obj_out)
    meta=[('source_receipt_archive',a.source_receipt_archive),('source_receipt_sha256',a.source_receipt_sha256),('source_branch',a.expected_branch),('source_head',a.expected_source_head),('source_tree',a.expected_source_tree),('source_contract_rows',10),('lane_rows',6),('requirement_rows',16),('root_acquisition_rows',28),('object_acquisition_rows',37),('candidate_evidence_files',0),('candidate_requirements',0),('local_foundation_only_requirements',6),('direct_gap_unavailable_requirements',10),('artifact_build_attestations_accepted',0),('termux_android_adaptations_accepted',0),('concrete_filename_drifts_accepted',0),('object_corrections_accepted',0),('final_provider_decisions_accepted',0),('target_rows_populated',0),('rules_sha256',sha(a.rules)),('requirement_review_sha256',sha(reqp)),('lane_review_sha256',sha(lanep)),('root_review_sha256',sha(rootp)),('object_review_sha256',sha(objp)),('next_state',a.next_state)]
    write_tsv(metap,['field','value'],({'field':k,'value':v} for k,v in meta))
    (a.out/'analysis.status').write_text('PASS\n',encoding='utf-8')
    (a.out/'claim-boundary.txt').write_text('The production acquirer received no staged acquisition input. Six local foundations remain incomplete and ten direct gaps remain unavailable. No evidence, build attestation, adaptation, filename drift, object correction, provider authority, or target population is accepted.\n',encoding='utf-8')
    (a.out/'next-state.txt').write_text(a.next_state+'\n',encoding='utf-8')
    print('generic build attestation/adaptation gap-evidence acquisition receipt review: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
