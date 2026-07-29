#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json
from pathlib import Path

BASE=Path('experiments/glibc/selected-obsidian-provider-authority')
REVIEW=BASE/'review'
DESIGN_ID='SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-DESIGN-REVIEW-001'
DECISION='QUALIFIED_NON_EXECUTING_SELECTED_PROVIDER_LOCAL_SUPPLY_LIVE_AUTHORITY_TRANSACTION_DESIGN_CANDIDATE'
ACCEPTANCE_GATE='SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-DESIGN-ACCEPTANCE-OPEN'
NEXT_ACTION='review-and-accept-non-executing-selected-provider-local-supply-live-authority-transaction-design-boundary'
SOURCE={
 'issuance':REVIEW/'selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-implementation-boundary-acceptance.tsv',
 'adapter':REVIEW/'selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-boundary-acceptance.tsv',
 'evidence_design':REVIEW/'selected-provider-local-supply-map-evidence-transaction-design-boundary-acceptance.tsv',
 'orchestration':REVIEW/'selected-provider-local-supply-live-evidence-orchestration-production-implementation-boundary-acceptance.tsv',
}
OUT={
 'inputs':REVIEW/'selected-provider-local-supply-live-authority-transaction-input-contract.tsv',
 'states':REVIEW/'selected-provider-local-supply-live-authority-transaction-state-machine.tsv',
 'operations':REVIEW/'selected-provider-local-supply-live-authority-transaction-operation-contract.tsv',
 'failures':REVIEW/'selected-provider-local-supply-live-authority-transaction-failure-contract.tsv',
 'receipt':REVIEW/'selected-provider-local-supply-live-authority-transaction-receipt-contract.json',
 'metadata':REVIEW/'selected-provider-local-supply-live-authority-transaction-design-metadata.tsv',
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
 rows={k:read_tsv(v) for k,v in p.items()}
 expected={
  'issuance':'ACCEPTED_BOUNDED_NON_EXECUTING_SYNTHETIC_IMPLEMENTATION_AUTHORITY',
  'adapter':'ACCEPTED_BOUNDED_NON_EXECUTING_SYNTHETIC_LIVE_INPUT_ADAPTER_EXECUTION_AUTHORIZATION_IMPLEMENTATION_AUTHORITY',
  'evidence_design':'ACCEPTED_BOUNDED_NON_EXECUTING_READ_ONLY_SELECTED_PROVIDER_LOCAL_SUPPLY_MAP_EVIDENCE_TRANSACTION_DESIGN',
  'orchestration':'ACCEPTED_BOUNDED_NON_EXECUTING_PRODUCTION_CAPABLE_ISOLATED_FIXTURE_LIVE_EVIDENCE_ORCHESTRATION_IMPLEMENTATION_AUTHORITY',
 }
 for k in p:
  if len(rows[k])!=1 or rows[k][0].get('decision')!=expected[k]:raise SystemExit(f'{k} accepted authority missing')
 joined='\n'.join('\t'.join(x.values()) for x in [rows[k][0] for k in p])
 forbidden=['\t1\t1\t','AUTHORIZED_SELECTED_PROVIDER','LIVE_AUTHORITY_GRANTED']
 if any(x in joined for x in forbidden):raise SystemExit('source acceptance unexpectedly grants current live authority')
 return p,rows

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',default='.');ap.add_argument('--output-root',default='.');a=ap.parse_args()
 repo=Path(a.repo_root).resolve();outroot=Path(a.output_root).resolve();p,src=validate(repo)
 none='DESIGN_ONLY_NOT_RUN'
 gate='SEPARATE_FUTURE_OWNER_ACTIVATION_AND_EXPLICIT_EXECUTION_AUTHORIZATION_REQUIRED'
 prohibited='DESIGN_DOES_NOT_CREATE_ACCEPT_OR_CONSUME_LIVE_AUTHORITY_DOCUMENTS_PERSIST_REPLAY_STATE_OPEN_OR_READ_SELECTED_PROVIDER_PATHS_EXECUTE_EVIDENCE_PRODUCE_A_LOCAL_SUPPLY_MAP_CREATE_A_GENERATION_ROOT_POPULATE_MATERIALIZE_PUBLISH_DEPLOY_OR_ACTIVATE'
 input_fields=['input_id','sequence','input_class','future_source','identity_and_provenance_rule','transport_rule','consumption_rule','failure_code','current_state','authority_gate','authority_effect','prohibited_inference']
 specs=[
 ('SOURCE_ISSUANCE_ACCEPTANCE',str(SOURCE['issuance']),'exact repository digest and accepted decision','repository tracked immutable input','design-time repository text only','LSLA_SOURCE_ISSUANCE_MISMATCH'),
 ('SOURCE_ADAPTER_ACCEPTANCE',str(SOURCE['adapter']),'exact repository digest and accepted decision','repository tracked immutable input','design-time repository text only','LSLA_SOURCE_ADAPTER_MISMATCH'),
 ('SOURCE_EVIDENCE_DESIGN_ACCEPTANCE',str(SOURCE['evidence_design']),'exact repository digest and accepted decision','repository tracked immutable input','design-time repository text only','LSLA_SOURCE_EVIDENCE_DESIGN_MISMATCH'),
 ('SOURCE_ORCHESTRATION_ACCEPTANCE',str(SOURCE['orchestration']),'exact repository digest and accepted decision','repository tracked immutable input','design-time repository text only','LSLA_SOURCE_ORCHESTRATION_MISMATCH'),
 ('OWNER_ACTIVATION_DECISION','future immutable owner activation decision','decision id scope exact source digests repository baseline executor and validity interval','explicit file argument only','read only after separate owner-activation ceremony','LSLA_OWNER_DECISION_MISSING_OR_INVALID'),
 ('OWNER_AUTHORIZATION_TOKEN','future canonical owner authorization token','exact token digest claims issuer decision id transaction id and coordinate receipt binding','explicit file argument only','read only after owner decision verification','LSLA_OWNER_TOKEN_MISSING_OR_INVALID'),
 ('COORDINATE_RECEIPT','future canonical 41-row coordinate receipt','exact digest 41 unique rows 10 fields and token binding','explicit file argument only; no discovery','paths remain opaque until every authority gate passes','LSLA_COORDINATE_RECEIPT_MISSING_OR_INVALID'),
 ('REVOCATION_DOCUMENT','future canonical revocation status document','exact decision/token/transaction binding and monotonic sequence','explicit file argument only','must prove not revoked before any provider open','LSLA_REVOCATION_STATUS_INVALID'),
 ('EXECUTION_AUTHORIZATION','future canonical execution authorization','exact 27 claims repository/remote/executor/time/replay/resource/output/orchestration bindings','explicit file argument only','must verify before provider-open gate can be armed','LSLA_EXECUTION_AUTHORIZATION_INVALID'),
 ('TRANSACTION_PACKAGE','future immutable transaction package and manifest','package digest manifest digest and transaction id exact','explicit local package path','package files only; no provider inputs','LSLA_TRANSACTION_PACKAGE_INVALID'),
 ('REPOSITORY_BASELINE','future local repository HEAD and tree','must equal owner/token/execution-authorization bindings','git metadata inspection only','repository metadata only','LSLA_REPOSITORY_BASELINE_MISMATCH'),
 ('REMOTE_BASELINE','future origin/main HEAD','must equal execution-authorization remote binding','git ls-remote read only','remote metadata only','LSLA_REMOTE_BASELINE_MISMATCH'),
 ('EXECUTOR_IDENTITY','future uid gid process identity and application id','must equal owner and execution-authorization bindings','kernel process metadata','identity comparison only','LSLA_EXECUTOR_IDENTITY_MISMATCH'),
 ('TRUSTED_TIME','future trusted time evidence','must satisfy not-before expiry skew and monotonicity contracts','explicit trusted-time provider record','time comparison only','LSLA_TRUSTED_TIME_INVALID'),
 ('REPLAY_REGISTRY','future append-only replay registry','exact registry identity schema generation and integrity root','explicit bounded registry path','read preflight; one append only after success','LSLA_REPLAY_REGISTRY_INVALID'),
 ('PROTECTED_STATE_BOUNDARY','Termux package databases and live glibc prefix','deterministic before/after equality','bounded snapshot implementation','metadata snapshot only; no candidate discovery','LSLA_PROTECTED_STATE_CHANGED'),
 ('ORCHESTRATION_ENTRYPOINT','accepted production orchestration implementation','exact accepted source digest and callable contract','repository tracked executable','invocation only after provider-open gate is armed','LSLA_ORCHESTRATION_ENTRYPOINT_MISMATCH'),
 ('RESOURCE_LIMITS','future open/read/byte/time/receipt limits','exact execution-authorization claims and repository policy','explicit claims and repository constants','limit comparison only','LSLA_RESOURCE_LIMIT_INVALID'),
 ('EVIDENCE_OUTPUT_ROOT','future transaction-scoped work/result roots','canonical owner transaction id path outside provider/live/generation roots','explicit bounded output path','writes limited to transaction evidence','LSLA_OUTPUT_ROOT_INVALID'),
 ('OPERATOR_INVOCATION','future explicit noninteractive invocation envelope','exact ordered arguments no environment authority no prompts','argv only','cannot supply implicit paths or authority','LSLA_OPERATOR_INVOCATION_INVALID'),
 ]
 inputs=[]
 for i,(cls,source,ident,transport,consume,fail) in enumerate(specs,1):
  inputs.append(r(input_id=f'LSLA-IN-{i:03d}',sequence=str(i),input_class=cls,future_source=source,identity_and_provenance_rule=ident,transport_rule=transport,consumption_rule=consume,failure_code=fail,current_state=none,authority_gate=gate,authority_effect='FUTURE_TRANSACTION_CONTRACT_ONLY_NO_CURRENT_AUTHORITY',prohibited_inference=prohibited))

 state_fields=['state_id','sequence','state_name','entry_requirement','permitted_effect','success_transition','failure_transition','resume_rule','current_state','authority_gate','prohibited_inference']
 state_specs=[
 ('INIT','exact package and no live inputs consumed','validate transaction package metadata only'),
 ('PACKAGE_VERIFIED','package manifest and transaction id exact','freeze immutable package identity'),
 ('SOURCE_AUTHORITIES_VERIFIED','four accepted source authorities exact','freeze inherited authority digests'),
 ('OWNER_DECISION_VERIFIED','owner activation decision exact and in scope','record decision digest in memory'),
 ('OWNER_TOKEN_VERIFIED','owner token canonical and decision-bound','record token digest in memory'),
 ('COORDINATE_RECEIPT_VERIFIED','41-row receipt canonical token-bound','record receipt digest; keep paths unopened'),
 ('REVOCATION_VERIFIED','revocation document current and not revoked','record revocation sequence'),
 ('EXECUTION_AUTHORIZATION_VERIFIED','27 claims exact and all prior documents bound','record authorization digest in memory'),
 ('REPOSITORY_BASELINE_VERIFIED','HEAD/tree equal all bindings','freeze local baseline'),
 ('REMOTE_BASELINE_VERIFIED','origin/main equals bound HEAD','freeze remote baseline'),
 ('EXECUTOR_VERIFIED','uid/gid/application identity equal bindings','freeze executor identity'),
 ('TRUSTED_TIME_VERIFIED','validity window and skew pass','freeze trusted timestamp evidence'),
 ('REPLAY_REGISTRY_VERIFIED','registry identity and integrity root exact','open read-only replay interface'),
 ('REPLAY_PRECHECKED','transaction tuple absent and monotonic','reserve in-memory replay tuple only'),
 ('PROTECTED_BEFORE_CAPTURED','package DB and live prefix snapshot complete','store transaction-scoped snapshot'),
 ('OUTPUT_ROOT_VERIFIED','output root canonical bounded and empty','allow transaction evidence writes only'),
 ('RESOURCE_LIMITS_VERIFIED','all limits positive bounded and consistent','freeze resource budget'),
 ('ORCHESTRATION_VERIFIED','accepted orchestration digest and entrypoint exact','freeze callable identity'),
 ('PROVIDER_OPEN_GATE_ARMED','all authority replay and invariance preconditions pass','permit future orchestration call only'),
 ('ORCHESTRATION_RUNNING','provider-open gate armed and callable invoked','future selected-provider reads only within bound rows'),
 ('EVIDENCE_RECEIPT_VERIFIED','orchestration returns canonical complete receipt','hold qualified map candidate in memory'),
 ('REPLAY_TUPLE_APPENDED','success tuple appended atomically once','persist append-only replay record'),
 ('PROTECTED_AFTER_CAPTURED','post snapshot complete','store transaction-scoped post snapshot'),
 ('INVARIANCE_VERIFIED','protected snapshots equal','seal protected-state evidence'),
 ('RESULT_INDEXED','success or failure receipt indexed','seal deterministic result index'),
 ('FINALIZED','archive delivered or canonical failure finalized','close descriptors and emit terminal receipt'),
 ]
 states=[]
 for i,(name,entry,effect) in enumerate(state_specs,1):
  success=f'LSLA-ST-{i+1:03d}' if i<len(state_specs) else 'TERMINAL_SUCCESS'
  states.append(r(state_id=f'LSLA-ST-{i:03d}',sequence=str(i),state_name=name,entry_requirement=entry,permitted_effect=effect,success_transition=success,failure_transition='TERMINAL_FAIL_CLOSED',resume_rule='resume only from exact indexed checkpoint before provider-open gate; after gate restart requires new authorization and replay precheck',current_state=none,authority_gate=gate,prohibited_inference=prohibited))

 operation_fields=['operation_id','sequence','phase','operation','precondition','future_effect','provider_open_allowed','persistent_write_allowed','failure_code','current_state','authority_gate','prohibited_inference']
 op_names=[
 ('PACKAGE','verify package manifest'),('PACKAGE','freeze package digest'),('SOURCES','verify issuance acceptance'),('SOURCES','verify adapter acceptance'),('SOURCES','verify evidence design acceptance'),('SOURCES','verify orchestration acceptance'),('OWNER','parse owner decision'),('OWNER','verify owner decision scope'),('TOKEN','parse owner token'),('TOKEN','verify owner token claims'),('COORDINATES','parse coordinate receipt'),('COORDINATES','verify 41-row canonical receipt'),('REVOCATION','parse revocation document'),('REVOCATION','verify non-revoked sequence'),('EXECUTION_AUTH','parse execution authorization'),('EXECUTION_AUTH','verify 27 claims and cross-document bindings'),('BASELINE','read local HEAD/tree'),('BASELINE','compare local bindings'),('REMOTE','read origin/main'),('REMOTE','compare remote binding'),('EXECUTOR','read uid/gid/application identity'),('EXECUTOR','compare executor binding'),('TIME','read trusted-time evidence'),('TIME','verify not-before expiry and skew'),('REPLAY','open registry read-only'),('REPLAY','verify registry integrity root'),('REPLAY','check tuple absence'),('REPLAY','reserve in-memory tuple'),('PROTECTED','capture protected-before'),('OUTPUT','validate transaction output root'),('OUTPUT','initialize bounded evidence files'),('LIMITS','verify open/read/byte/time limits'),('LIMITS','verify receipt and archive limits'),('ORCHESTRATION','verify accepted implementation digest'),('ORCHESTRATION','verify independent production entrypoint'),('GATE','re-evaluate all authority predicates'),('GATE','arm first selected-provider open gate'),('EXECUTE','invoke accepted orchestration'),('EXECUTE','enforce ordered 41-row processing'),('EXECUTE','collect canonical evidence receipt'),('EVIDENCE','verify whole-map completeness'),('EVIDENCE','verify result schema and limits'),('REPLAY_COMMIT','append canonical replay tuple'),('REPLAY_COMMIT','fsync registry and parent'),('PROTECTED','capture protected-after'),('PROTECTED','compare protected-state invariance'),('RESULT','write terminal receipt'),('RESULT','write result index'),('RESULT','archive indexed evidence'),('RESULT','verify result archive'),('RESULT','upload result archive'),('FINALIZE','close descriptors and finalize status'),
 ]
 operations=[]
 gate_index=38
 for i,(phase,name) in enumerate(op_names,1):
  open_allowed='YES_BOUND_TO_ACCEPTED_ORCHESTRATION_ONLY' if i>=gate_index and i<=40 else 'NO'
  persistent='YES_SINGLE_APPEND_ONLY_REPLAY_TUPLE' if i in (43,44) else 'NO'
  operations.append(r(operation_id=f'LSLA-OP-{i:03d}',sequence=str(i),phase=phase,operation=name,precondition='all prior ordered operations succeeded',future_effect='future transaction effect only; current design performs nothing',provider_open_allowed=open_allowed,persistent_write_allowed=persistent,failure_code=f'LSLA-FAIL-{min(30,(i+1)//2):03d}',current_state=none,authority_gate=gate,prohibited_inference=prohibited))

 failure_fields=['failure_id','sequence','failure_class','trigger','fail_closed_effect','provider_effect','replay_effect','cleanup_boundary','receipt_rule','current_state','authority_gate','prohibited_inference']
 failures=[
 ('PACKAGE','package manifest digest transaction id or self-test mismatch'),('SOURCE_AUTHORITY','accepted source artifact or decision mismatch'),('OWNER_DECISION','owner decision missing malformed expired or wrong scope'),('OWNER_TOKEN','token missing malformed signature/issuer/decision binding mismatch'),('COORDINATE_RECEIPT','receipt digest row count field count uniqueness or token binding mismatch'),('REVOCATION','revoked stale regressed or mismatched revocation document'),('EXECUTION_AUTHORIZATION','authorization missing malformed expired or cross-binding mismatch'),('REPOSITORY_BASELINE','local HEAD/tree mismatch'),('REMOTE_BASELINE','remote HEAD unavailable or mismatch'),('EXECUTOR','uid gid application identity mismatch'),('TRUSTED_TIME','not-before expiry skew rollback or provider failure'),('REPLAY_REGISTRY','registry path schema ownership mode or integrity-root mismatch'),('REPLAY_DUPLICATE','transaction tuple already present'),('REPLAY_ORDER','sequence rollback or monotonicity violation'),('PROTECTED_BEFORE','protected pre-snapshot unavailable'),('OUTPUT_ROOT','output root escapes transaction boundary or overlaps forbidden roots'),('RESOURCE_LIMIT','open read byte time receipt or archive budget invalid'),('ORCHESTRATION_IDENTITY','accepted orchestration source or entrypoint mismatch'),('SYNTHETIC_REWRITE','accepted synthetic CLI import invocation or live-to-synthetic rewrite attempted'),('PREMATURE_PROVIDER_OPEN','provider open attempted before gate armed'),('PROVIDER_PATH','coordinate path noncanonical symlink unsafe owner/mode or outside authorization'),('PROVIDER_CONTENT','stable identity size digest ELF machine type or SONAME mismatch'),('WHOLE_MAP','fewer than 41 rows or atomic family incomplete'),('EVIDENCE_RECEIPT','receipt schema serialization digest or limit mismatch'),('REPLAY_APPEND','append fsync parent-fsync or post-append verification failed'),('PROTECTED_AFTER','protected post-snapshot unavailable'),('PROTECTED_INVARIANCE','package database or live prefix changed'),('RESULT_INDEX','terminal receipt or index generation failed'),('RESULT_DELIVERY','archive verification or upload failed'),('ROLLBACK_RECOVERY','cleanup would cross bounded evidence roots or terminal state ambiguous'),
 ]
 failure_rows=[]
 for i,(cls,trig) in enumerate(failures,1):
  failure_rows.append(r(failure_id=f'LSLA-FAIL-{i:03d}',sequence=str(i),failure_class=cls,trigger=trig,fail_closed_effect='reject transaction; do not produce or accept a local-supply map; emit canonical failure receipt when possible',provider_effect='close exact opened descriptors only; never mutate provider paths',replay_effect='no append unless orchestration receipt is verified; failed append leaves transaction failed and non-resumable without new authorization',cleanup_boundary='exact transaction evidence temporaries only; never delete registry provider live prefix generation root or unknown paths',receipt_rule='indexed failure receipt plus protected-state evidence when possible',current_state=none,authority_gate=gate,prohibited_inference=prohibited))

 receipt={
  'schema_version':1,'design_id':DESIGN_ID,'decision':DECISION,'acceptance_gate':ACCEPTANCE_GATE,
  'future_live_document_roles':['owner_activation_decision','owner_authorization_token','coordinate_receipt','revocation_document','execution_authorization'],
  'future_replay_tuple_fields':['transaction_id','owner_decision_sha256','owner_token_sha256','coordinate_receipt_sha256','revocation_sha256','execution_authorization_sha256','repository_head','repository_tree','executor_uid','trusted_time_utc'],
  'future_success_receipt_required_fields':['schema_version','transaction_id','decision_id','authorization_id','repository_head','repository_tree','remote_head','executor_uid','trusted_time_utc','coordinate_receipt_sha256','orchestration_implementation_sha256','local_supply_map_candidate_sha256','row_count','provider_open_count','provider_read_count','provider_byte_count','replay_tuple_sha256','protected_before_sha256','protected_after_sha256','protected_invariant','result_index_sha256','result_archive_sha256','status'],
  'future_failure_receipt_required_fields':['schema_version','transaction_id','failure_id','failure_detail','last_completed_state','provider_open_count','provider_read_count','replay_append_count','protected_before_sha256','protected_after_sha256','result_index_sha256','status'],
  'current_live_documents':[],'current_replay_tuples':[],'current_selected_provider_paths':[],'current_local_supply_map':None,
  'current_counts':{'live_documents':0,'execution_authorizations':0,'replay_writes':0,'selected_provider_opens':0,'selected_provider_reads':0,'provider_bytes':0,'local_supply_maps':0,'live_authority':0},
  'authority_effect':'DESIGN_ONLY_ZERO_CURRENT_LIVE_AUTHORITY','prohibited_inference':prohibited,
 }

 metadata_fields=['design_id','decision','acceptance_gate','source_issuance_acceptance_sha256','source_adapter_acceptance_sha256','source_evidence_design_acceptance_sha256','source_orchestration_acceptance_sha256','input_count','state_count','operation_count','failure_count','inherited_issuance_coverage','inherited_adapter_coverage','inherited_evidence_coverage','inherited_orchestration_coverage','inherited_total_coverage','future_live_document_role_count','future_replay_tuple_field_count','current_live_document_count','current_execution_authorization_count','current_replay_write_count','current_selected_provider_open_count','current_selected_provider_read_count','current_provider_byte_count','current_local_supply_map_count','current_live_authority_count','current_state','authority_gate','next_action','authority_effect','prohibited_inference']
 metadata=[r(design_id=DESIGN_ID,decision=DECISION,acceptance_gate=ACCEPTANCE_GATE,source_issuance_acceptance_sha256=sha(p['issuance']),source_adapter_acceptance_sha256=sha(p['adapter']),source_evidence_design_acceptance_sha256=sha(p['evidence_design']),source_orchestration_acceptance_sha256=sha(p['orchestration']),input_count='20',state_count='26',operation_count='52',failure_count='30',inherited_issuance_coverage='88',inherited_adapter_coverage='164',inherited_evidence_coverage='78',inherited_orchestration_coverage='118',inherited_total_coverage='448',future_live_document_role_count='5',future_replay_tuple_field_count='10',current_live_document_count='0',current_execution_authorization_count='0',current_replay_write_count='0',current_selected_provider_open_count='0',current_selected_provider_read_count='0',current_provider_byte_count='0',current_local_supply_map_count='0',current_live_authority_count='0',current_state=none,authority_gate=gate,next_action=NEXT_ACTION,authority_effect='EXACT_20_INPUT_26_STATE_52_OPERATION_30_FAILURE_NON_EXECUTING_LIVE_AUTHORITY_TRANSACTION_DESIGN_CANDIDATE_448_INHERITED_COVERAGE_ZERO_CURRENT_LIVE_DOCUMENTS_REPLAY_WRITES_SELECTED_PROVIDER_OPENS_READS_PROVIDER_BYTES_LOCAL_MAPS_OR_LIVE_AUTHORITY',prohibited_inference=prohibited)]

 for key,fields,rows in [('inputs',input_fields,inputs),('states',state_fields,states),('operations',operation_fields,operations),('failures',failure_fields,failure_rows),('metadata',metadata_fields,metadata)]:write_tsv(outroot/OUT[key],fields,rows)
 q=outroot/OUT['receipt'];q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
 print('live-authority transaction design: generated 20 inputs, 26 states, 52 operations, 30 failures, zero current live authority')
if __name__=='__main__':main()
