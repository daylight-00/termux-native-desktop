#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json
from pathlib import Path

BASE=Path('experiments/glibc/selected-obsidian-provider-authority')
REVIEW=BASE/'review'
DESIGN_ID='SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-DESIGN-REVIEW-001'
ACCEPTANCE_GATE='SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-DESIGN-ACCEPTANCE-OPEN'
NEXT_ACTION='review-and-accept-read-only-selected-provider-local-supply-map-evidence-transaction-design-boundary'
SOURCE={
 'acceptance':REVIEW/'selected-provider-local-supply-map-contract-boundary-acceptance.tsv',
 'contract':REVIEW/'selected-provider-local-supply-map-contract.tsv',
 'validation':REVIEW/'selected-provider-local-supply-map-validation-contract.tsv',
 'receipt_schema':REVIEW/'selected-provider-local-supply-map-receipt-schema.json',
}
OUT={
 'inputs':REVIEW/'selected-provider-local-supply-map-evidence-transaction-input-contract.tsv',
 'states':REVIEW/'selected-provider-local-supply-map-evidence-transaction-state-machine.tsv',
 'operations':REVIEW/'selected-provider-local-supply-map-evidence-transaction-operation-contract.tsv',
 'failures':REVIEW/'selected-provider-local-supply-map-evidence-transaction-failure-contract.tsv',
 'receipt':REVIEW/'selected-provider-local-supply-map-evidence-transaction-receipt-contract.json',
 'metadata':REVIEW/'selected-provider-local-supply-map-evidence-transaction-design-metadata.tsv',
}

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def read_tsv(p:Path):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
def write_tsv(p:Path,fields,rows):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def r(**k):return k

def validate(repo:Path):
 p={k:repo/v for k,v in SOURCE.items()}
 a=read_tsv(p['acceptance']);c=read_tsv(p['contract']);v=read_tsv(p['validation']);s=json.loads(p['receipt_schema'].read_text())
 if len(a)!=1 or a[0]['decision']!='ACCEPTED_BOUNDED_NON_MUTATING_SELECTED_PROVIDER_LOCAL_SUPPLY_MAP_CONTRACT':raise SystemExit('accepted contract boundary missing')
 if len(c)!=41 or len(v)!=24:raise SystemExit('contract cardinality mismatch')
 if any(x['local_regular_file_path'] or x['local_path_binding_state']!='UNBOUND_CONTRACT_ONLY' for x in c):raise SystemExit('source contract unexpectedly populated')
 if s.get('current_populated_row_count')!=0 or s.get('current_rows')!=[]:raise SystemExit('source receipt schema unexpectedly populated')
 if a[0]['source_contract_sha256']!=sha(p['contract']) or a[0]['source_validation_contract_sha256']!=sha(p['validation']) or a[0]['source_receipt_schema_sha256']!=sha(p['receipt_schema']):raise SystemExit('acceptance digest drift')
 return p,c,v,s

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',default='.');ap.add_argument('--output-root',default='.');args=ap.parse_args()
 repo=Path(args.repo_root).resolve();outroot=Path(args.output_root).resolve();p,c,v,s=validate(repo)
 auth='SEPARATE_FUTURE_READ_ONLY_EVIDENCE_EXECUTION_AUTHORIZATION_REQUIRED'
 none='DESIGN_ONLY_NOT_RUN'
 prohibited='DESIGN_DOES_NOT_AUTHORIZE_PATH_DISCOVERY_PROVIDER_OR_RESULT_DOWNLOAD_ARCHIVE_OR_PACKAGE_EXTRACTION_BYTE_READ_LOCAL_MAP_ACCEPTANCE_EXECUTION_ROOT_CREATION_POPULATION_MATERIALIZATION_PUBLICATION_DEPLOYMENT_OR_ACTIVATION'
 input_fields=['input_id','sequence','input_class','required_source','identity_rule','transport_or_binding_rule','path_or_read_rule','failure_code','current_state','authority_gate','authority_effect','prohibited_inference']
 input_rows=[
 r(input_id='LSME-IN-001',sequence='1',input_class='CONTRACT_ACCEPTANCE',required_source=str(SOURCE['acceptance']),identity_rule='exact accepted decision and source digests',transport_or_binding_rule='repository tracked immutable input',path_or_read_rule='read repository text only',failure_code='LSME_CONTRACT_ACCEPTANCE_MISMATCH',current_state=none,authority_gate=auth,authority_effect='FUTURE_INPUT_CONTRACT_ONLY',prohibited_inference=prohibited),
 r(input_id='LSME-IN-002',sequence='2',input_class='CONTRACT_ROWS',required_source=str(SOURCE['contract']),identity_rule='exact 41 rows and accepted SHA-256',transport_or_binding_rule='repository tracked immutable input',path_or_read_rule='no local path values may be populated in design',failure_code='LSME_CONTRACT_ROWS_MISMATCH',current_state=none,authority_gate=auth,authority_effect='FUTURE_INPUT_CONTRACT_ONLY',prohibited_inference=prohibited),
 r(input_id='LSME-IN-003',sequence='3',input_class='VALIDATION_RULES',required_source=str(SOURCE['validation']),identity_rule='exact 24 ordered rules and accepted SHA-256',transport_or_binding_rule='repository tracked immutable input',path_or_read_rule='rules consumed without provider reads during design',failure_code='LSME_VALIDATION_RULES_MISMATCH',current_state=none,authority_gate=auth,authority_effect='FUTURE_INPUT_CONTRACT_ONLY',prohibited_inference=prohibited),
 r(input_id='LSME-IN-004',sequence='4',input_class='RECEIPT_SCHEMA',required_source=str(SOURCE['receipt_schema']),identity_rule='exact canonical empty schema and accepted SHA-256',transport_or_binding_rule='repository tracked immutable input',path_or_read_rule='schema only; no live receipt rows',failure_code='LSME_RECEIPT_SCHEMA_MISMATCH',current_state=none,authority_gate=auth,authority_effect='FUTURE_INPUT_CONTRACT_ONLY',prohibited_inference=prohibited),
 r(input_id='LSME-IN-005',sequence='5',input_class='EXECUTION_AUTHORIZATION_TOKEN',required_source='future owner-approved immutable token',identity_rule='transaction id contract acceptance id repository HEAD/tree expiry uid and coordinate-receipt SHA-256 exact',transport_or_binding_rule='explicit file argument only; no environment inference',path_or_read_rule='token itself may be read only after separate authorization',failure_code='LSME_EXECUTION_AUTHORIZATION_MISSING',current_state='NOT_PROVIDED_NOT_AUTHORIZED',authority_gate=auth,authority_effect='NO_CURRENT_EXECUTION_AUTHORITY',prohibited_inference=prohibited),
 r(input_id='LSME-IN-006',sequence='6',input_class='LOCAL_COORDINATE_RECEIPT',required_source='future owner-approved canonical 41-row coordinate receipt',identity_rule='41 unique contract row ids and exact receipt SHA-256 bound by token',transport_or_binding_rule='explicit file argument only; no search glob or basename matching',path_or_read_rule='absolute paths supplied only by approved receipt',failure_code='LSME_COORDINATE_RECEIPT_INVALID',current_state='NOT_PROVIDED_ZERO_PATHS',authority_gate=auth,authority_effect='NO_CURRENT_PATH_AUTHORITY',prohibited_inference=prohibited),
 r(input_id='LSME-IN-007',sequence='7',input_class='REPOSITORY_BASELINE',required_source='future exact main HEAD and tree',identity_rule='must equal token-bound repository HEAD/tree',transport_or_binding_rule='local Git read-only inspection',path_or_read_rule='repository metadata only',failure_code='LSME_REPOSITORY_BASELINE_MISMATCH',current_state=none,authority_gate=auth,authority_effect='FUTURE_PREFLIGHT_ONLY',prohibited_inference=prohibited),
 r(input_id='LSME-IN-008',sequence='8',input_class='REMOTE_BASELINE',required_source='future origin/main',identity_rule='must equal token-bound repository HEAD',transport_or_binding_rule='git ls-remote read only',path_or_read_rule='remote metadata only',failure_code='LSME_REMOTE_BASELINE_MISMATCH',current_state=none,authority_gate=auth,authority_effect='FUTURE_PREFLIGHT_ONLY',prohibited_inference=prohibited),
 r(input_id='LSME-IN-009',sequence='9',input_class='PROTECTED_STATE_SNAPSHOT',required_source='Termux package databases and live glibc prefix',identity_rule='before/after deterministic snapshot equality',transport_or_binding_rule='bounded metadata snapshot',path_or_read_rule='no provider candidate path discovery',failure_code='LSME_PROTECTED_STATE_CHANGED',current_state=none,authority_gate=auth,authority_effect='FUTURE_INVARIANCE_CHECK_ONLY',prohibited_inference=prohibited),
 r(input_id='LSME-IN-010',sequence='10',input_class='EXECUTOR_IDENTITY',required_source='future process uid and gid',identity_rule='must equal token and localization receipt ownership authority',transport_or_binding_rule='kernel process metadata',path_or_read_rule='used for owner checks only',failure_code='LSME_EXECUTOR_IDENTITY_MISMATCH',current_state=none,authority_gate=auth,authority_effect='FUTURE_PREFLIGHT_ONLY',prohibited_inference=prohibited),
 r(input_id='LSME-IN-011',sequence='11',input_class='TOOLCHAIN_CAPABILITIES',required_source='future python sha256 ELF parser and nofollow open support',identity_rule='capability versions recorded in receipt',transport_or_binding_rule='explicit preflight commands only',path_or_read_rule='no provider reads until all capability gates pass',failure_code='LSME_TOOLCHAIN_UNAVAILABLE',current_state=none,authority_gate=auth,authority_effect='FUTURE_PREFLIGHT_ONLY',prohibited_inference=prohibited),
 r(input_id='LSME-IN-012',sequence='12',input_class='EVIDENCE_OUTPUT_ROOT',required_source='future transaction-scoped hw-t work/result roots',identity_rule='exact transaction id scoped and outside generation/live prefixes',transport_or_binding_rule='explicit bounded output coordinate',path_or_read_rule='writes limited to logs receipts result index and result archive',failure_code='LSME_OUTPUT_ROOT_INVALID',current_state='NOT_CREATED_DESIGN_ONLY',authority_gate=auth,authority_effect='FUTURE_EVIDENCE_OUTPUT_ONLY_NO_RUNTIME_AUTHORITY',prohibited_inference=prohibited),
 ]
 state_fields=['state_id','sequence','state_name','entry_requirement','permitted_effect','success_transition','failure_transition','resume_rule','current_state','authority_gate','prohibited_inference']
 names=[
 ('INIT','package and exact design artifacts verified','no provider or path read','AUTHORIZATION_VERIFIED'),
 ('AUTHORIZATION_VERIFIED','separate token exact and unexpired','metadata reads only','BASELINE_VERIFIED'),
 ('BASELINE_VERIFIED','repository and remote exact','contract reads only','CONTRACT_VERIFIED'),
 ('CONTRACT_VERIFIED','accepted digests and 41/24 counts exact','coordinate receipt parse only','COORDINATES_VERIFIED'),
 ('COORDINATES_VERIFIED','41 explicit rows no search inference','protected snapshot only','PROTECTED_BEFORE'),
 ('PROTECTED_BEFORE','protected metadata snapshot complete','authorized row reads may begin','ROW_VALIDATION'),
 ('ROW_VALIDATION','all 41 rows processed in contract order','bounded nofollow reads and row receipts','ATOMIC_FAMILY_VERIFIED'),
 ('ATOMIC_FAMILY_VERIFIED','four atomic families complete','canonical receipt serialization','RECEIPT_SERIALIZED'),
 ('RECEIPT_SERIALIZED','candidate receipt canonical and <=1MiB','protected after snapshot','PROTECTED_AFTER'),
 ('PROTECTED_AFTER','after snapshot complete','invariance comparison','INVARIANCE_VERIFIED'),
 ('INVARIANCE_VERIFIED','protected state identical','result indexing/archive only','RESULT_ARCHIVED'),
 ('RESULT_ARCHIVED','result index and archive complete','result upload only','RESULT_UPLOADED'),
 ('RESULT_UPLOADED','remote result coordinate verified','candidate finalization only','QUALIFIED_CANDIDATE'),
 ('QUALIFIED_CANDIDATE','all gates pass','emit non-accepted evidence candidate','FINALIZED'),
 ('REJECTED','any gate failed','failure receipt and bounded logs only','FINALIZED'),
 ('FINALIZED','status and result archive finalized','none','FINALIZED'),
 ]
 state_rows=[]
 for i,(n,entry,effect,succ) in enumerate(names,1):
  state_rows.append(r(state_id=f'LSME-ST-{i:03d}',sequence=str(i),state_name=n,entry_requirement=entry,permitted_effect=effect,success_transition=succ,failure_transition='REJECTED' if n not in ('REJECTED','FINALIZED') else 'FINALIZED',resume_rule='resume only from exact transaction id and digest-bound state receipt; otherwise restart before provider reads',current_state=none,authority_gate=auth,prohibited_inference=prohibited))
 op_fields=['step_id','sequence','phase','operation','input_refs','permitted_read_scope','permitted_write_scope','required_evidence','success_transition','failure_code','current_state','authority_gate','prohibited_inference']
 ops=[
 ('PACKAGE','verify package manifest and self-test','LSME-IN-001..012','package files only','none','package self-test'),
 ('AUTH','verify separate owner authorization token','LSME-IN-005','token only','logs only','token digest and fields'),
 ('BASE','verify repository HEAD/tree','LSME-IN-007','git metadata','logs only','exact HEAD/tree'),
 ('REMOTE','verify origin/main','LSME-IN-008','remote ref metadata','logs only','exact remote HEAD'),
 ('CONTRACT','verify accepted contract and artifact digests','LSME-IN-001..004','repository files','logs only','accepted digests'),
 ('COORD','parse coordinate receipt','LSME-IN-006','coordinate receipt only','logs only','receipt digest'),
 ('COUNT','require 41 unique ordered row ids','LSME-IN-002,006','coordinate receipt only','logs only','41-row bijection'),
 ('NOSEARCH','reject glob search environment inference and basename fallback','LSME-IN-006','none','logs only','no-discovery attestation'),
 ('TOOLS','verify nofollow hash and ELF parser capabilities','LSME-IN-011','tool metadata','logs only','tool versions'),
 ('PROTECT_PRE','snapshot protected state before provider reads','LSME-IN-009','protected metadata','snapshot/log only','before snapshot'),
 ('ROW_ORDER','iterate rows in contract sequence','LSME-IN-002,006','coordinate receipt metadata','row temp receipts only','sequence lock'),
 ('PATH_CANON','validate supplied absolute canonical path','LSME-VAL-009','one supplied path metadata','row temp receipt','canonical path'),
 ('COMPONENT_LSTAT','lstat every path component and reject symlink','LSME-VAL-010','one supplied path components','row temp receipt','component identities'),
 ('OPEN_NOFOLLOW','open final path O_RDONLY O_CLOEXEC O_NOFOLLOW','LSME-VAL-010','one final supplied file','row temp receipt','file descriptor'),
 ('REGULAR','compare lstat/fstat regular-file identity','LSME-VAL-011','opened file metadata','row temp receipt','mode identities'),
 ('OWNER','verify transaction uid ownership','LSME-VAL-012','opened file metadata','row temp receipt','uid'),
 ('MODE','reject group/other writable','LSME-VAL-013','opened file metadata','row temp receipt','mode'),
 ('PRE_ID','record dev inode size mtime ctime before stream','LSME-VAL-014','opened file metadata','row temp receipt','pre identity'),
 ('HASH','stream exact file descriptor through SHA-256','LSME-VAL-016','one authorized file descriptor','row temp receipt','digest and bytes read'),
 ('POST_ID','re-fstat and require stable identity','LSME-VAL-014','opened file metadata','row temp receipt','post identity'),
 ('SIZE','require exact member size','LSME-VAL-015','row metadata','row temp receipt','exact size'),
 ('DIGEST','require exact member SHA-256','LSME-VAL-016','row metadata','row temp receipt','exact digest'),
 ('ELF','parse ELF64 little-endian AArch64 ET_DYN','LSME-VAL-017','same opened file bytes','row temp receipt','ELF identity'),
 ('SONAME','require exact DT_SONAME','LSME-VAL-018','same opened file bytes','row temp receipt','SONAME'),
 ('SUPPLY_ID','verify result/index/container/member identities','LSME-VAL-019..022','contract and coordinate metadata','row temp receipt','supply identities'),
 ('ROW_FINAL','seal canonical row receipt','LSME-VAL-001..022','validated row metadata','row temp receipt','row validation state'),
 ('ATOMIC','require four complete atomic families','LSME-VAL-023','41 row receipts','candidate receipt temp','family results'),
 ('WHOLE_MAP','reject whole map on any failed or missing row','LSME-VAL-024','41 row receipts','candidate/failure receipt temp','whole-map decision'),
 ('SERIALIZE','serialize canonical compact UTF-8 JSON receipt','LSME-IN-004','validated metadata only','result receipt only','receipt SHA-256'),
 ('CAP','abort if receipt exceeds 1MiB reservation','LSME-IN-004','receipt bytes','result failure receipt only','receipt byte count'),
 ('PROTECT_POST','snapshot and compare protected state','LSME-IN-009','protected metadata','snapshot/log only','invariance receipt'),
 ('ARCHIVE_UPLOAD','index archive upload and finalize status','LSME-IN-012','transaction result files','result index/archive only','remote result coordinate'),
 ]
 op_rows=[]
 fail_codes=['LSME_PACKAGE_INVALID','LSME_EXECUTION_AUTHORIZATION_MISSING','LSME_REPOSITORY_BASELINE_MISMATCH','LSME_REMOTE_BASELINE_MISMATCH','LSME_CONTRACT_ACCEPTANCE_MISMATCH','LSME_COORDINATE_RECEIPT_INVALID','LSME_ROW_COUNT_MISMATCH','LSME_PATH_DISCOVERY_ATTEMPT','LSME_TOOLCHAIN_UNAVAILABLE','LSME_PROTECTED_STATE_CHANGED','LSME_ROW_ORDER_MISMATCH','LSME_PATH_NOT_CANONICAL','LSME_SYMLINK_REJECTED','LSME_OPEN_NOFOLLOW_FAILED','LSME_NOT_REGULAR_FILE','LSME_OWNER_MISMATCH','LSME_MODE_WRITABLE','LSME_FILE_CHANGED_DURING_READ','LSME_MEMBER_SHA_MISMATCH','LSME_FILE_CHANGED_DURING_READ','LSME_SIZE_MISMATCH','LSME_MEMBER_SHA_MISMATCH','LSME_ELF_IDENTITY_MISMATCH','LSME_SONAME_MISMATCH','LSME_SUPPLY_IDENTITY_MISMATCH','LSME_ROW_REJECTED','LSME_ATOMIC_FAMILY_INCOMPLETE','LSME_RECEIPT_REJECTED','LSME_RECEIPT_SERIALIZATION_FAILED','LSME_RECEIPT_OVERFLOW','LSME_PROTECTED_STATE_CHANGED','LSME_ARCHIVE_OR_UPLOAD_FAILED']
 for i,(x,fc) in enumerate(zip(ops,fail_codes),1):
  phase,operation,refs,read,write,evidence=x
  op_rows.append(r(step_id=f'LSME-OP-{i:03d}',sequence=str(i),phase=phase,operation=operation,input_refs=refs,permitted_read_scope=read,permitted_write_scope=write,required_evidence=evidence,success_transition=f'LSME-OP-{i+1:03d}' if i<len(ops) else 'QUALIFIED_CANDIDATE',failure_code=fc,current_state=none,authority_gate=auth,prohibited_inference=prohibited))
 failure_fields=['failure_id','sequence','failure_class','trigger','required_action','accepted_map_effect','cleanup_scope','result_requirement','current_state','authority_gate','prohibited_inference']
 failure_defs=[
 ('AUTHORIZATION','missing expired or mismatched token'),('BASELINE','repository or remote mismatch'),('CONTRACT','accepted artifact digest or count mismatch'),('COORDINATES','coordinate receipt invalid incomplete duplicate or inferred'),('DISCOVERY','search glob environment or basename fallback attempted'),('PATH','noncanonical path or symlink component'),('OPEN_TYPE','nofollow open failure or non-regular file'),('OWNER_MODE','owner or writable mode mismatch'),('STABILITY','device inode size timestamp changed'),('SIZE_DIGEST','exact size or SHA mismatch'),('ELF_SONAME','ELF identity or SONAME mismatch'),('SUPPLY_IDENTITY','result index container or member locator mismatch'),('ATOMIC_FAMILY','atomic family incomplete'),('WHOLE_MAP','any row failed or fewer than 41 passed'),('RECEIPT','canonical serialization or schema mismatch'),('RECEIPT_OVERFLOW','receipt greater than 1MiB'),('PROTECTED_STATE','package database or live prefix changed'),('RESULT_DELIVERY','result index archive or upload failed'),
 ]
 failure_rows=[]
 for i,(cl,trig) in enumerate(failure_defs,1):
  failure_rows.append(r(failure_id=f'LSME-FAIL-{i:03d}',sequence=str(i),failure_class=cl,trigger=trig,required_action='reject whole map; close provider descriptors; emit canonical failure receipt; do not emit accepted map',accepted_map_effect='NO_ACCEPTED_LOCAL_SUPPLY_MAP',cleanup_scope='exact transaction temporary receipt/log files only; never delete provider paths unknown paths generation roots or other transaction state',result_requirement='indexed failure result archive and protected-state evidence when possible',current_state=none,authority_gate=auth,prohibited_inference=prohibited))
 receipt={
  'schema_version':1,'design_review_id':DESIGN_ID,'current_state':'DESIGN_ONLY_NOT_RUN','current_authorized_coordinate_count':0,'current_provider_read_count':0,'current_receipt_rows':[],
  'future_success_receipt':{'decision':'QUALIFIED_READ_ONLY_LOCAL_SUPPLY_MAP_EVIDENCE_CANDIDATE','required_row_count':41,'validation_rule_count':24,'atomic_family_count':4,'required_fields':['transaction_id','authorization_token_sha256','contract_acceptance_id','repository_head','repository_tree','remote_head','coordinate_receipt_sha256','executor_uid','rows','atomic_family_results','protected_state_invariance','receipt_sha256'],'acceptance_state':'CANDIDATE_ONLY_SEPARATE_ACCEPTANCE_REQUIRED'},
  'future_failure_receipt':{'decision':'REJECTED_READ_ONLY_LOCAL_SUPPLY_MAP_EVIDENCE','accepted_row_count':0,'required_fields':['transaction_id','first_failure','failure_codes','failed_contract_row_ids','protected_state_invariance','receipt_sha256']},
  'serialization':'canonical compact UTF-8 JSON sort_keys separators comma-colon newline terminated','maximum_receipt_bytes':1048576,'overflow_action':'ABORT_BEFORE_CANDIDATE_QUALIFICATION','provider_mutation_authority':'NONE','runtime_mutation_authority':'NONE','execution_authority':'NONE_SEPARATE_FUTURE_DECISION_REQUIRED','prohibited_inference':prohibited
 }
 out={k:outroot/v for k,v in OUT.items()};write_tsv(out['inputs'],input_fields,input_rows);write_tsv(out['states'],state_fields,state_rows);write_tsv(out['operations'],op_fields,op_rows);write_tsv(out['failures'],failure_fields,failure_rows);out['receipt'].parent.mkdir(parents=True,exist_ok=True);out['receipt'].write_text(json.dumps(receipt,sort_keys=True,separators=(',',':'))+'\n')
 meta=[
 ('schema_version','1'),('design_review_id',DESIGN_ID),('candidate_state','QUALIFIED_NON_EXECUTING_READ_ONLY_LOCAL_SUPPLY_MAP_EVIDENCE_TRANSACTION_DESIGN_CANDIDATE'),('acceptance_gate',ACCEPTANCE_GATE),('source_contract_acceptance_id','SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-ACCEPT-001'),('source_contract_acceptance_sha256',sha(p['acceptance'])),('source_contract_sha256',sha(p['contract'])),('source_validation_contract_sha256',sha(p['validation'])),('source_receipt_schema_sha256',sha(p['receipt_schema'])),('input_contract_count',str(len(input_rows))),('state_count',str(len(state_rows))),('operation_count',str(len(op_rows))),('failure_contract_count',str(len(failure_rows))),('inherited_validation_rule_count',str(len(v))),('expected_future_receipt_row_count',str(len(c))),('current_authorized_coordinate_count','0'),('current_provider_read_count','0'),('current_populated_local_path_count','0'),('success_receipt_state','CANDIDATE_ONLY_SEPARATE_ACCEPTANCE_REQUIRED'),('local_path_discovery_authorized','NO'),('provider_byte_read_authorized','NO'),('evidence_transaction_execution_authorized','NO'),('local_supply_map_produced','NO'),('materializer_execution_authorized','NO'),('generation_root_creation_authorized','NO'),('target_population_authorized','NO'),('materialization_authorized','NO'),('publication_authorized','NO'),('deployment_authorized','NO'),('activation_authorized','NO'),('input_contract_sha256',sha(out['inputs'])),('state_machine_sha256',sha(out['states'])),('operation_contract_sha256',sha(out['operations'])),('failure_contract_sha256',sha(out['failures'])),('receipt_contract_sha256',sha(out['receipt'])),('next_action',NEXT_ACTION),('authority_effect','QUALIFIED_NON_EXECUTING_READ_ONLY_EVIDENCE_TRANSACTION_DESIGN_CANDIDATE_ONLY'),('prohibited_inference',prohibited)
 ]
 write_tsv(out['metadata'],['key','value'],[{'key':k,'value':val} for k,val in meta])
if __name__=='__main__':main()
