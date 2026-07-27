#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json
from pathlib import Path

BASE=Path('experiments/glibc/selected-obsidian-provider-authority')
REVIEW=BASE/'review'
REVIEW_ID='SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-COORDINATE-CONTRACT-REVIEW-001'
ACCEPTANCE_GATE='SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-COORDINATE-CONTRACT-ACCEPTANCE-OPEN'
NEXT_ACTION='review-and-accept-non-mutating-selected-provider-local-supply-evidence-authorization-and-coordinate-receipt-contract-boundary'
SOURCE={
 'design_acceptance':REVIEW/'selected-provider-local-supply-map-evidence-transaction-design-boundary-acceptance.tsv',
 'contract_acceptance':REVIEW/'selected-provider-local-supply-map-contract-boundary-acceptance.tsv',
 'contract':REVIEW/'selected-provider-local-supply-map-contract.tsv',
 'validation':REVIEW/'selected-provider-local-supply-map-validation-contract.tsv',
}
OUT={
 'token':REVIEW/'selected-provider-local-supply-evidence-owner-authorization-token-schema.json',
 'coordinate':REVIEW/'selected-provider-local-supply-evidence-coordinate-receipt-schema.json',
 'validation':REVIEW/'selected-provider-local-supply-evidence-authorization-coordinate-validation-contract.tsv',
 'metadata':REVIEW/'selected-provider-local-supply-evidence-authorization-coordinate-contract-metadata.tsv',
}

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def read_tsv(p:Path):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
def write_tsv(p:Path,fields,rows):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def write_json(p:Path,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')

def validate(repo:Path):
 p={k:repo/v for k,v in SOURCE.items()}
 da=read_tsv(p['design_acceptance']);ca=read_tsv(p['contract_acceptance']);c=read_tsv(p['contract']);v=read_tsv(p['validation'])
 if len(da)!=1 or da[0]['decision']!='ACCEPTED_BOUNDED_NON_EXECUTING_READ_ONLY_SELECTED_PROVIDER_LOCAL_SUPPLY_MAP_EVIDENCE_TRANSACTION_DESIGN':raise SystemExit('evidence design acceptance missing')
 if len(ca)!=1 or ca[0]['decision']!='ACCEPTED_BOUNDED_NON_MUTATING_SELECTED_PROVIDER_LOCAL_SUPPLY_MAP_CONTRACT':raise SystemExit('local supply contract acceptance missing')
 if len(c)!=41 or len(v)!=24:raise SystemExit('41/24 source boundary mismatch')
 if any(x['local_regular_file_path'] or x['local_path_binding_state']!='UNBOUND_CONTRACT_ONLY' for x in c):raise SystemExit('source contract contains live path')
 return p,c,v,da[0],ca[0]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',default='.');ap.add_argument('--output-root',default='.');a=ap.parse_args()
 repo=Path(a.repo_root).resolve();outroot=Path(a.output_root).resolve();p,c,v,da,ca=validate(repo)
 out={k:outroot/x for k,x in OUT.items()}
 prohibited='SCHEMA_REVIEW_DOES_NOT_ISSUE_A_TOKEN_POPULATE_A_COORDINATE_AUTHORIZE_DISCOVERY_OR_READ_PROVIDER_BYTES_EXECUTE_EVIDENCE_COLLECTION_CREATE_RUNTIME_STATE_POPULATE_MATERIALIZE_PUBLISH_DEPLOY_OR_ACTIVATE'
 token_claims=[
  'schema_version','authorization_token_id','authorization_kind','owner_identity','owner_decision_id','issued_at_utc','expires_at_utc','not_before_utc','nonce','revocation_epoch','transaction_id','contract_acceptance_id','evidence_design_acceptance_id','repository_head','repository_tree','remote_head','executor_uid','coordinate_receipt_sha256'
 ]
 token={
  'schema_version':1,'review_id':REVIEW_ID,'candidate_state':'SCHEMA_QUALIFIED_NOT_ISSUED','acceptance_gate':ACCEPTANCE_GATE,
  'serialization':'canonical compact UTF-8 JSON sort_keys separators comma-colon newline terminated',
  'current_token':None,'current_token_count':0,'current_authorization_state':'NOT_ISSUED_NOT_AUTHORIZED',
  'required_claim_count':len(token_claims),'required_claims':token_claims,
  'required_authorization_kind':'READ_ONLY_LOCAL_SUPPLY_EVIDENCE_TRANSACTION_ONLY',
  'required_permitted_effect':'READ_ONLY_PROVIDER_VALIDATION_AND_TRANSACTION_SCOPED_EVIDENCE_OUTPUTS_ONLY',
  'maximum_validity_seconds':86400,'clock_skew_tolerance_seconds':0,
  'binding_rules':{
   'contract_acceptance_id':ca['acceptance_id'],'evidence_design_acceptance_id':da['acceptance_id'],
   'repository_identity':'EXACT_HEAD_AND_TREE','remote_identity':'EXACT_HEAD_EQUALS_LOCAL_HEAD',
   'executor_identity':'EXACT_NUMERIC_UID','coordinate_receipt':'EXACT_CANONICAL_SHA256',
   'replay':'TOKEN_ID_NONCE_TRANSACTION_ID_AND_RECEIPT_SHA_MUST_BE_UNIQUE','revocation':'REVOCATION_EPOCH_MUST_EQUAL_CURRENT_OWNER_AUTHORITY_EPOCH'
  },
  'prohibited_effects':['PATH_DISCOVERY','RESULT_OR_PACKAGE_ACQUISITION','ARCHIVE_OR_PACKAGE_EXTRACTION','PROVIDER_MUTATION','RUNTIME_MUTATION','LOCAL_MAP_ACCEPTANCE','MATERIALIZER_EXECUTION','GENERATION_ROOT_CREATION','TARGET_POPULATION','PUBLICATION','DEPLOYMENT','ACTIVATION'],
  'prohibited_inference':prohibited,
 }
 row_fields=['contract_row_id','sequence','provider_object_id','expected_member_sha256','expected_member_size_bytes','expected_soname','absolute_canonical_path','coordinate_authority_id','coordinate_origin','path_text_sha256']
 coord={
  'schema_version':1,'review_id':REVIEW_ID,'candidate_state':'SCHEMA_QUALIFIED_ZERO_LIVE_COORDINATES','acceptance_gate':ACCEPTANCE_GATE,
  'serialization':'canonical compact UTF-8 JSON sort_keys separators comma-colon newline terminated',
  'current_receipt':None,'current_receipt_count':0,'current_coordinate_row_count':0,'current_rows':[],
  'future_required_row_count':41,'future_required_unique_contract_row_count':41,'future_required_row_field_count':len(row_fields),'future_required_row_fields':row_fields,
  'future_required_envelope_fields':['schema_version','coordinate_receipt_id','contract_acceptance_id','evidence_design_acceptance_id','repository_head','repository_tree','remote_head','issuer_identity','issued_at_utc','rows','receipt_sha256'],
  'contract_row_ids':[x['contract_row_id'] for x in c],
  'row_rules':{
   'cardinality':'EXACTLY_41_ROWS','uniqueness':'CONTRACT_ROW_ID_PROVIDER_OBJECT_ID_AND_PATH_TEXT_SHA256_UNIQUE',
   'path':'ABSOLUTE_CANONICAL_UTF8_NO_DOTDOT_NO_GLOB_NO_VARIABLE_NO_SEARCH_EXPRESSION',
   'binding':'EACH_ROW_EXACTLY_MATCHES_ACCEPTED_CONTRACT_OBJECT_DIGEST_SIZE_AND_SONAME',
   'missing_or_duplicate':'REJECT_WHOLE_RECEIPT','inference':'NO_BASENAME_FALLBACK_NO_ENVIRONMENT_INFERENCE_NO_FILESYSTEM_DISCOVERY'
  },
  'receipt_digest_rule':'SHA256_OF_CANONICAL_DOCUMENT_WITH_RECEIPT_SHA256_FIELD_OMITTED',
  'prohibited_inference':prohibited,
 }
 vf=['validation_id','sequence','category','subject','required_rule','future_receipt_or_token_field','failure_code','candidate_state','authority_effect','prohibited_inference']
 specs=[
 ('AUTH_SCHEMA','authorization schema','schema version and review id exact','schema_version;review_id','LSAE_AUTH_SCHEMA_MISMATCH'),
 ('AUTH_CARDINALITY','authorization claims','exact 18 required claims','required_claims','LSAE_AUTH_CLAIM_COUNT_MISMATCH'),
 ('AUTH_KIND','authorization kind','exact read-only evidence authorization kind','authorization_kind','LSAE_AUTH_KIND_MISMATCH'),
 ('OWNER_IDENTITY','owner approval','owner identity and immutable owner decision id required','owner_identity;owner_decision_id','LSAE_OWNER_IDENTITY_MISSING'),
 ('TIME_WINDOW','authorization time','not-before issued and expiry times ordered and validity no more than 86400 seconds','not_before_utc;issued_at_utc;expires_at_utc','LSAE_AUTH_TIME_INVALID'),
 ('TOKEN_UNIQUENESS','anti replay','token id nonce transaction id and receipt digest unique','authorization_token_id;nonce;transaction_id','LSAE_TOKEN_REPLAY'),
 ('REVOCATION','revocation epoch','token epoch equals current owner authority epoch','revocation_epoch','LSAE_TOKEN_REVOKED'),
 ('CONTRACT_BINDING','contract acceptance','exact accepted contract id','contract_acceptance_id','LSAE_CONTRACT_BINDING_MISMATCH'),
 ('DESIGN_BINDING','design acceptance','exact accepted evidence design id','evidence_design_acceptance_id','LSAE_DESIGN_BINDING_MISMATCH'),
 ('REPOSITORY_HEAD','repository head','exact token-bound local repository head','repository_head','LSAE_REPOSITORY_HEAD_MISMATCH'),
 ('REPOSITORY_TREE','repository tree','exact token-bound local repository tree','repository_tree','LSAE_REPOSITORY_TREE_MISMATCH'),
 ('REMOTE_HEAD','remote head','origin main equals token and local head','remote_head','LSAE_REMOTE_HEAD_MISMATCH'),
 ('EXECUTOR_UID','executor uid','numeric process uid exactly equals token uid','executor_uid','LSAE_EXECUTOR_UID_MISMATCH'),
 ('RECEIPT_DIGEST_BINDING','coordinate receipt digest','token binds exact canonical coordinate receipt sha256','coordinate_receipt_sha256','LSAE_RECEIPT_DIGEST_MISMATCH'),
 ('PERMITTED_EFFECT','effect scope','only read-only provider validation and transaction-scoped evidence outputs','required_permitted_effect','LSAE_EFFECT_SCOPE_WIDENED'),
 ('PROHIBITED_EFFECTS','prohibited effects','all runtime and acquisition effects explicitly denied','prohibited_effects','LSAE_PROHIBITED_EFFECT_MISSING'),
 ('COORD_SCHEMA','coordinate schema','schema version and review id exact','schema_version;review_id','LSAE_COORD_SCHEMA_MISMATCH'),
 ('COORD_ENVELOPE','coordinate envelope','all 11 future envelope fields required','future_required_envelope_fields','LSAE_COORD_ENVELOPE_INCOMPLETE'),
 ('COORD_CARDINALITY','coordinate rows','exactly 41 rows','rows','LSAE_COORD_ROW_COUNT_MISMATCH'),
 ('COORD_ROW_FIELDS','coordinate row shape','exact 10 fields per row','rows','LSAE_COORD_ROW_SHAPE_MISMATCH'),
 ('CONTRACT_ROW_SET','contract row ids','exact accepted 41 contract row id set','contract_row_id','LSAE_CONTRACT_ROW_SET_MISMATCH'),
 ('OBJECT_BINDING','object identity','provider object digest size and soname match accepted contract','provider_object_id;expected_member_sha256;expected_member_size_bytes;expected_soname','LSAE_OBJECT_BINDING_MISMATCH'),
 ('PATH_ABSOLUTE','path absolute','path begins slash and is canonical UTF8','absolute_canonical_path','LSAE_PATH_NOT_ABSOLUTE'),
 ('PATH_NO_DOTDOT','path traversal','no dot or dotdot component','absolute_canonical_path','LSAE_PATH_TRAVERSAL'),
 ('PATH_NO_EXPANSION','path expression','no glob variable tilde command or search expression','absolute_canonical_path','LSAE_PATH_EXPRESSION'),
 ('PATH_UNIQUENESS','path uniqueness','path text digest and canonical path unique across rows','path_text_sha256;absolute_canonical_path','LSAE_PATH_DUPLICATE'),
 ('COORD_AUTHORITY','coordinate authority','each row names exact immutable coordinate authority id and origin','coordinate_authority_id;coordinate_origin','LSAE_COORD_AUTHORITY_MISSING'),
 ('NO_INFERENCE','no discovery','missing coordinates cause whole receipt rejection with no basename environment or filesystem inference','rows','LSAE_COORD_INFERENCE_ATTEMPT'),
 ('CANONICAL_DIGEST','receipt digest','receipt digest computed over canonical document with digest field omitted','receipt_sha256','LSAE_RECEIPT_CANONICAL_DIGEST_MISMATCH'),
 ('ZERO_CURRENT','candidate current state','candidate contains zero live token zero receipt and zero coordinate rows','current_token_count;current_receipt_count;current_coordinate_row_count','LSAE_CANDIDATE_LIVE_AUTHORITY_PRESENT'),
 ]
 rows=[]
 for i,(cat,sub,rule,field,code) in enumerate(specs,1):rows.append({'validation_id':f'LSAE-VAL-{i:03d}','sequence':str(i),'category':cat,'subject':sub,'required_rule':rule,'future_receipt_or_token_field':field,'failure_code':code,'candidate_state':'CONTRACT_DEFINED_NOT_RUN','authority_effect':'FUTURE_INPUT_VALIDATION_RULE_ONLY_NO_CURRENT_TOKEN_PATH_OR_READ_AUTHORITY','prohibited_inference':prohibited})
 write_json(out['token'],token);write_json(out['coordinate'],coord);write_tsv(out['validation'],vf,rows)
 meta=[
  ('schema_version','1'),('review_id',REVIEW_ID),('candidate_state','QUALIFIED_NON_MUTATING_AUTHORIZATION_AND_COORDINATE_RECEIPT_CONTRACT_CANDIDATE'),('acceptance_gate',ACCEPTANCE_GATE),
  ('source_design_acceptance_id',da['acceptance_id']),('source_design_acceptance_sha256',sha(p['design_acceptance'])),('source_contract_acceptance_id',ca['acceptance_id']),('source_contract_acceptance_sha256',sha(p['contract_acceptance'])),('source_contract_sha256',sha(p['contract'])),('source_validation_contract_sha256',sha(p['validation'])),
  ('authorization_required_claim_count',str(len(token_claims))),('coordinate_required_row_count','41'),('coordinate_required_row_field_count',str(len(row_fields))),('validation_rule_count',str(len(rows))),
  ('current_token_count','0'),('current_coordinate_receipt_count','0'),('current_coordinate_row_count','0'),('current_provider_read_count','0'),('current_populated_local_path_count','0'),
  ('owner_authorization_issued','NO'),('coordinate_receipt_issued','NO'),('local_path_discovery_authorized','NO'),('provider_byte_read_authorized','NO'),('evidence_transaction_execution_authorized','NO'),('local_supply_map_produced','NO'),('materializer_execution_authorized','NO'),('generation_root_creation_authorized','NO'),('target_population_authorized','NO'),('materialization_authorized','NO'),('publication_authorized','NO'),('deployment_authorized','NO'),('activation_authorized','NO'),
  ('owner_authorization_token_schema_sha256',sha(out['token'])),('coordinate_receipt_schema_sha256',sha(out['coordinate'])),('validation_contract_sha256',sha(out['validation'])),('next_action',NEXT_ACTION),('authority_effect','QUALIFIED_NON_MUTATING_INPUT_CONTRACT_CANDIDATE_ONLY'),('prohibited_inference',prohibited)
 ]
 write_tsv(out['metadata'],['key','value'],[{'key':k,'value':v} for k,v in meta])
if __name__=='__main__':main()
