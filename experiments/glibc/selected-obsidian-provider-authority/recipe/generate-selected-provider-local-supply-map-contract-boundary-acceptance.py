#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json
from pathlib import Path
FILES={
 'selected-provider-local-supply-map-contract.tsv':'2223af964e74cc8bb221d13e559e49aaf03abe364985346cb1d8e43973c6640e',
 'selected-provider-local-supply-map-validation-contract.tsv':'0df8d9c7ddc28098ee220ee634a139b04aaa3d241bd36b2a4eb57ef8fbc41198',
 'selected-provider-local-supply-map-receipt-schema.json':'8f7c8d26f7e646e431e6be53526b55ccc3f5c65584b4c2306e9d19544a9396fa',
 'selected-provider-local-supply-map-contract-metadata.tsv':'751510776aa6c7db15f3d968c7e910b7886d1a560c36e4b241cb5976041a7acd',
}
FIELDS=['acceptance_id','decision','candidate_review_id','source_contract_sha256','source_validation_contract_sha256','source_receipt_schema_sha256','source_metadata_sha256','accepted_contract_row_count','accepted_validation_rule_count','accepted_populated_local_path_count','accepted_result_index_sha256_row_count','accepted_append_only_index_receipt_row_count','accepted_existing_authority_digest_sentinel_row_count','accepted_receipt_schema_id','accepted_path_authority','accepted_byte_read_authority','candidate_issue_closed','accepted_authority_state','local_path_discovery_state','local_supply_map_state','execution_authorization_state','byte_acquisition_state','generation_root_state','target_population_state','materialization_state','publication_state','deployment_state','activation_state','update_boundary','rollback_boundary','next_action','authority_effect','prohibited_inference']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path('.'));ap.add_argument('--output-root',type=Path,default=Path('.'));a=ap.parse_args()
 r=a.repo_root.resolve()/'experiments/glibc/selected-obsidian-provider-authority/review'
 for name,digest in FILES.items():
  if sha(r/name)!=digest:raise SystemExit(f'frozen local supply contract candidate digest mismatch: {name}')
 contract=rows(r/'selected-provider-local-supply-map-contract.tsv');valid=rows(r/'selected-provider-local-supply-map-validation-contract.tsv');meta={x['key']:x['value'] for x in rows(r/'selected-provider-local-supply-map-contract-metadata.tsv')};schema=json.loads((r/'selected-provider-local-supply-map-receipt-schema.json').read_text())
 if len(contract)!=41 or len(valid)!=24:raise SystemExit('candidate cardinality mismatch')
 if any(x['local_regular_file_path'] or x['local_path_binding_state']!='UNBOUND_CONTRACT_ONLY' for x in contract):raise SystemExit('candidate local path population detected')
 split={k:sum(x['result_index_contract_kind']==k for x in contract) for k in ['RESULT_INDEX_SHA256','APPEND_ONLY_INDEX_RECEIPT_SHA256','EXISTING_AUTHORITY_DIGEST_SENTINEL']}
 if split!={'RESULT_INDEX_SHA256':23,'APPEND_ONLY_INDEX_RECEIPT_SHA256':4,'EXISTING_AUTHORITY_DIGEST_SENTINEL':14}:raise SystemExit('candidate index split mismatch')
 required={'contract_review_id':'SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-REVIEW-001','candidate_state':'QUALIFIED_NON_MUTATING_LOCAL_SUPPLY_MAP_CONTRACT_CANDIDATE','acceptance_gate':'SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-ACCEPTANCE-OPEN','contract_row_count':'41','validation_rule_count':'24','current_populated_local_path_count':'0','local_supply_map_state':'NOT_PRODUCED_NOT_AUTHORIZED','local_path_discovery_authorized':'NO','byte_read_authorized':'NO','execution_authorized':'NO','generation_root_creation_authorized':'NO','target_population_authorized':'NO','materialization_authorized':'NO','publication_authorized':'NO','deployment_authorized':'NO','activation_authorized':'NO'}
 for k,v in required.items():
  if meta.get(k)!=v:raise SystemExit(f'candidate metadata mismatch {k}: {meta.get(k)!r}')
 if schema.get('receipt_schema_id')!='SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-RECEIPT-SCHEMA-001' or schema.get('current_populated_row_count')!=0 or schema.get('current_rows')!=[]:raise SystemExit('receipt schema candidate drift')
 row={
  'acceptance_id':'SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-ACCEPT-001','decision':'ACCEPTED_BOUNDED_NON_MUTATING_SELECTED_PROVIDER_LOCAL_SUPPLY_MAP_CONTRACT','candidate_review_id':'SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-REVIEW-001',
  'source_contract_sha256':FILES['selected-provider-local-supply-map-contract.tsv'],'source_validation_contract_sha256':FILES['selected-provider-local-supply-map-validation-contract.tsv'],'source_receipt_schema_sha256':FILES['selected-provider-local-supply-map-receipt-schema.json'],'source_metadata_sha256':FILES['selected-provider-local-supply-map-contract-metadata.tsv'],
  'accepted_contract_row_count':'41','accepted_validation_rule_count':'24','accepted_populated_local_path_count':'0','accepted_result_index_sha256_row_count':'23','accepted_append_only_index_receipt_row_count':'4','accepted_existing_authority_digest_sentinel_row_count':'14','accepted_receipt_schema_id':'SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-RECEIPT-SCHEMA-001','accepted_path_authority':'NONE_CONTRACT_ONLY','accepted_byte_read_authority':'NONE_CONTRACT_ONLY',
  'candidate_issue_closed':'SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-ACCEPTANCE-OPEN','accepted_authority_state':'ACCEPTED_BOUNDED_NON_MUTATING_LOCAL_SUPPLY_MAP_CONTRACT_AUTHORITY','local_path_discovery_state':'NOT_AUTHORIZED_SEPARATE_READ_ONLY_EVIDENCE_TRANSACTION_REQUIRED','local_supply_map_state':'NOT_PRODUCED_NOT_AUTHORIZED','execution_authorization_state':'NOT_AUTHORIZED_SEPARATE_EXPLICIT_DECISION_REQUIRED','byte_acquisition_state':'NOT_AUTHORIZED','generation_root_state':'NOT_CREATED_NOT_AUTHORIZED','target_population_state':'NOT_AUTHORIZED_UNPOPULATED_SCHEMA_ONLY','materialization_state':'NOT_AUTHORIZED','publication_state':'NOT_AUTHORIZED','deployment_state':'NOT_AUTHORIZED','activation_state':'NOT_AUTHORIZED',
  'update_boundary':'ANY_CONTRACT_ROW_VALIDATION_RULE_RECEIPT_SCHEMA_RESULT_INDEX_CONTAINER_MEMBER_PATH_IDENTITY_CONTENT_ELF_SONAME_FAILURE_OR_AUTHORITY_CHANGE_REQUIRES_NEW_CLASS_D_CONTRACT_REVIEW','rollback_boundary':'BEFORE_LOCALIZATION_REVOKE_CONTRACT_ACCEPTANCE_DIRECTLY;AFTER_FUTURE_LOCAL_MAP_REVOKE_MAP_ACCEPTANCE_WITHOUT_READING_OR_MUTATING_PROVIDER_OR_GENERATION_BYTES','next_action':'design-and-review-read-only-selected-provider-local-supply-map-evidence-transaction','authority_effect':'EXACT_41_ROW_24_RULE_NON_MUTATING_LOCAL_SUPPLY_MAP_CONTRACT_ACCEPTED_NO_PATH_DISCOVERY_BYTE_READ_LOCAL_MAP_EXECUTION_ROOT_CREATION_POPULATION_MATERIALIZATION_PUBLICATION_DEPLOYMENT_OR_ACTIVATION','prohibited_inference':'CONTRACT_ACCEPTANCE_DOES_NOT_AUTHORIZE_PATH_SEARCH_RESULT_DOWNLOAD_ARCHIVE_OR_PACKAGE_EXTRACTION_PROVIDER_BYTE_READ_LOCAL_MAP_PRODUCTION_EXECUTION_OBJECT_OR_GENERATION_WRITE_POPULATION_PUBLICATION_DEPLOYMENT_OR_ACTIVATION'}
 out=a.output_root/'experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-contract-boundary-acceptance.tsv';out.parent.mkdir(parents=True,exist_ok=True)
 with out.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=FIELDS,delimiter='\t',lineterminator='\n');w.writeheader();w.writerow(row)
if __name__=='__main__':main()
