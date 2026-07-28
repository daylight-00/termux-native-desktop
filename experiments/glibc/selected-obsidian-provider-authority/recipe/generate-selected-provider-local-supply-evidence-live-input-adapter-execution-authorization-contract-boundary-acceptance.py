#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib
from pathlib import Path
BASE=Path('experiments/glibc/selected-obsidian-provider-authority');REVIEW=BASE/'review'
META=REVIEW/'selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-metadata.tsv'
OUT=REVIEW/'selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-boundary-acceptance.tsv'
def rows(p:Path):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,required=True);ap.add_argument('--output-root',type=Path,required=True);a=ap.parse_args()
 root=a.repo_root.resolve();outroot=a.output_root.resolve();meta={r['key']:r['value'] for r in rows(root/META)}
 row={
 'acceptance_id':'SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-CONTRACT-ACCEPT-001',
 'decision':'ACCEPTED_BOUNDED_NON_EXECUTING_LIVE_INPUT_ADAPTER_EXECUTION_AUTHORIZATION_CONTRACT_AUTHORITY',
 'candidate_review_id':meta['contract_review_id'],
 'source_adapter_contract_sha256':meta['adapter_contract_sha256'],
 'source_execution_authorization_schema_sha256':meta['execution_authorization_schema_sha256'],
 'source_validation_contract_sha256':meta['validation_contract_sha256'],
 'source_state_machine_sha256':meta['state_machine_sha256'],
 'source_operation_contract_sha256':meta['operation_contract_sha256'],
 'source_failure_contract_sha256':meta['failure_contract_sha256'],
 'source_receipt_contract_sha256':meta['receipt_contract_sha256'],
 'source_metadata_sha256':sha(root/META),
 'source_synthetic_implementation_sha256':meta['source_implementation_sha256'],
 'accepted_explicit_input_channel_count':meta['explicit_input_channel_count'],
 'accepted_adapter_envelope_required_field_count':meta['adapter_envelope_required_field_count'],
 'accepted_execution_authorization_required_claim_count':meta['execution_authorization_required_claim_count'],
 'accepted_validation_rule_count':meta['validation_rule_count'],
 'accepted_state_count':meta['state_count'],
 'accepted_operation_count':meta['operation_count'],
 'accepted_failure_count':meta['failure_count'],
 'accepted_coordinate_required_row_count':meta['coordinate_required_row_count'],
 'accepted_coordinate_required_row_field_count':meta['coordinate_required_row_field_count'],
 'accepted_maximum_provider_bytes':meta['maximum_provider_bytes'],
 'accepted_maximum_result_receipt_bytes':meta['maximum_result_receipt_bytes'],
 'accepted_current_live_input_count':'0','accepted_current_adapter_envelope_count':'0','accepted_current_execution_authorization_count':'0','accepted_current_provider_read_count':'0','accepted_current_write_count':'0','accepted_current_live_authority_count':'0',
 'candidate_issue_closed':meta['acceptance_gate'],
 'accepted_authority_state':'ACCEPTED_BOUNDED_NON_EXECUTING_LIVE_INPUT_ADAPTER_EXECUTION_AUTHORIZATION_CONTRACT_AUTHORITY',
 'synthetic_implementation_role':'IMMUTABLE_SEMANTIC_AND_REGRESSION_ORACLE_ONLY_NOT_LIVE_EXECUTOR',
 'live_to_synthetic_path_rewrite_state':'FORBIDDEN',
 'future_live_adapter_implementation_state':'NOT_AUTHORIZED_SEPARATE_IMPLEMENTATION_REVIEW_AND_ACCEPTANCE_REQUIRED',
 'owner_authorization_issuance_state':'NOT_AUTHORIZED',
 'coordinate_receipt_production_state':'NOT_AUTHORIZED',
 'local_path_discovery_state':'NOT_AUTHORIZED',
 'execution_authorization_issuance_state':'NOT_AUTHORIZED',
 'provider_byte_read_state':'NOT_AUTHORIZED',
 'evidence_transaction_execution_state':'NOT_AUTHORIZED',
 'local_supply_map_state':'NOT_PRODUCED_NOT_AUTHORIZED',
 'byte_acquisition_state':'NOT_AUTHORIZED',
 'generation_root_state':'NOT_CREATED_NOT_AUTHORIZED',
 'target_population_state':'NOT_AUTHORIZED_UNPOPULATED_SCHEMA_ONLY',
 'materialization_state':'NOT_AUTHORIZED','publication_state':'NOT_AUTHORIZED','deployment_state':'NOT_AUTHORIZED','activation_state':'NOT_AUTHORIZED',
 'update_boundary':'ANY_ACCEPTED_SCHEMA_FIELD_INPUT_BINDING_VALIDATION_STATE_OPERATION_FAILURE_RECEIPT_RESOURCE_REPLAY_REVOCATION_SYNTHETIC_OR_AUTHORITY_CHANGE_REQUIRES_NEW_CLASS_D_CONTRACT_REVIEW',
 'rollback_boundary':'BEFORE_ANY_FUTURE_IMPLEMENTATION_REMOVE_CONTRACT_ACCEPTANCE_ONLY_NO_LIVE_INPUT_PROVIDER_READ_WRITE_OR_RUNTIME_STATE_EXISTS',
 'next_action':'generate-and-review-non-executing-selected-provider-local-supply-evidence-live-input-adapter-and-execution-authorization-implementation-candidate',
 'authority_effect':'EXACT_EIGHT_ARTIFACT_NON_EXECUTING_CONTRACT_ACCEPTED_ZERO_LIVE_INPUTS_ZERO_PROVIDER_READS_ZERO_WRITES_ZERO_LIVE_AUTHORITY',
 'prohibited_inference':'CONTRACT_ACCEPTANCE_DOES_NOT_IMPLEMENT_OR_RUN_A_LIVE_ADAPTER_SUPPLY_OR_ACCEPT_LIVE_INPUTS_ISSUE_OR_ACTIVATE_AUTHORIZATION_REWRITE_LIVE_PATHS_INVOKE_SYNTHETIC_CLI_WITH_LIVE_INPUT_SEARCH_OPEN_OR_READ_PROVIDER_BYTES_EXECUTE_EVIDENCE_COLLECTION_CREATE_RUNTIME_STATE_POPULATE_MATERIALIZE_PUBLISH_DEPLOY_OR_ACTIVATE',
 }
 dest=outroot/OUT;dest.parent.mkdir(parents=True,exist_ok=True)
 with dest.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(row),delimiter='\t',lineterminator='\n');w.writeheader();w.writerow(row)
if __name__=='__main__':main()
