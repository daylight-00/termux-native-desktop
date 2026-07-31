#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv
from pathlib import Path

BASE = Path("experiments/glibc/selected-obsidian-provider-authority")
NAME = "selected-provider-local-supply-live-authority-transaction-production-exact-input-set-correction-bootstrap-boundary-acceptance.tsv"
ROW = {
"acceptance_id":"SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-PRODUCTION-EXACT-INPUT-SET-CORRECTION-BOOTSTRAP-ACCEPT-001",
"decision":"ACCEPTED_EXACT_NON_EXECUTING_PRODUCTION_BOOTSTRAP_COLLECTION_BOUNDARY_ZERO_LIVE_AUTHORITY",
"candidate_review_id":"SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-PRODUCTION-EXACT-INPUT-SET-CORRECTION-BOOTSTRAP-REVIEW-001",
"candidate_issue_closed":"SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-PRODUCTION-EXACT-INPUT-SET-CORRECTION-BOOTSTRAP-ACCEPTANCE-OPEN",
"source_review_sha256":"77d8f5cc50e3bfa69d42182822b9dc51765927cf22085ce9030124357f1e5eb9",
"source_metadata_sha256":"9c5ca8e728bea6b5a936282691a7a0291d99b5175386f8841a4304ad44532223",
"source_provider_members_sha256":"dc446494dfe9dd55e73749f82b0df0db0ba00b11e732e85d92d608977b8c06e4",
"source_source_archives_sha256":"024f9d35c0da1a95fbde2398d75f81fff930213ad2f19d74dde35f2dafb70763",
"source_review_document_sha256":"d19f7de400043ddf5dd65e331b6ad33347091c9cb5c5f63c6bc1d85937182bdc",
"v151_result_archive_sha256":"55807be078f3861de6d7f596cb3dcfeefabd8acd122de77e9cae8ba32e65b77d",
"v151_result_archive_size_bytes":"133157","v151_result_drive_file_id":"1YVYOLqptqpkCFP5u5JM8Uhm7wasDbdqF","v151_transaction_id":"LSLA-PROD-COLLECT-20260731T162143Z",
"v153_promotion_result_archive_sha256":"db2fa441de06edde9dc44ef9e3661dc67db0f14cca90ad50afe8f180e5db1109",
"v153_promotion_result_archive_size_bytes":"9097","v153_promotion_result_drive_file_id":"1jH4kyNCA-OwqMLGDQ1NeslRIGZPRFr65",
"promotion_commit":"2ac9b6870c1ad9bd7e06c68ec40d8a13863f8d32","promotion_tree":"0e565e244f7f52728cb9805a8bfe70eb8a10703a","promotion_remote_head":"2ac9b6870c1ad9bd7e06c68ec40d8a13863f8d32",
"owner_approval_statement_sha256":"45637e4377068f284b5fa7b7a1e8908fb2cf5c6ab73c24cb0f56e77817e1a3e2",
"accepted_transaction_count":"1","consumed_transaction_count":"1","remaining_transaction_count":"0","accepted_source_archive_count":"9","accepted_byte_carrier_count":"33","accepted_provider_member_count":"41","accepted_provider_byte_count":"29047112","accepted_isolated_provider_open_count":"41","accepted_isolated_provider_read_count":"41","accepted_replay_registry_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","accepted_replay_registry_size_bytes":"0","accepted_selected_provider_live_open_count":"0","accepted_selected_provider_live_read_count":"0","accepted_project_replay_read_count":"0","accepted_project_replay_write_count":"0","accepted_local_supply_map_count":"0","accepted_target_population_write_count":"0","accepted_live_authority_count":"0",
"trusted_time_contract_state":"ACCEPTED_EXTERNAL_CANONICAL_TRUSTED_TIME_EVIDENCE_NOT_HARDCODED","replay_baseline_contract_state":"ACCEPTED_EXACT_EMPTY_BASELINE_IDENTITY_VERIFIED_UNCHANGED","output_root_contract_state":"ACCEPTED_ISOLATED_OUTPUT_ROOT_REQUIRED_EMPTY_BEFORE_COLLECTION","byte_carrier_model_state":"ACCEPTED_AUTHORITY_PROVENANCE_DISTINCT_FROM_EXACT_BYTE_CARRIER","owner_transaction_state":"ONE_ACCEPTED_ONE_CONSUMED_ZERO_REMAINING_NO_REPLAY","execution_authorization_state":"COLLECTION_ONLY_EXPIRED_WITH_CONSUMED_TRANSACTION","provider_open_gate_state":"CLOSED_NOT_AUTHORIZED","local_supply_map_state":"NOT_PRODUCED_NOT_AUTHORIZED","target_population_state":"NOT_AUTHORIZED_UNPOPULATED","materialization_state":"NOT_AUTHORIZED","publication_state":"NOT_AUTHORIZED","deployment_state":"NOT_AUTHORIZED","activation_state":"NOT_AUTHORIZED",
"update_boundary":"ANY_RESULT_ARCHIVE_PROMOTION_COMMIT_SOURCE_LINEAGE_CARRIER_MEMBER_DIGEST_ORDER_ACCOUNTING_TRUSTED_TIME_REPLAY_OUTPUT_ROOT_OR_AUTHORITY_CHANGE_REQUIRES_NEW_PRODUCTION_BOOTSTRAP_BOUNDARY_REVIEW",
"rollback_boundary":"REMOVE_ACCEPTANCE_RECORD_AND_RESTORE_EXACT_PRODUCTION_BOOTSTRAP_COLLECTION_PROMOTION_ACCEPTANCE_OPEN_WITH_OWNER_ACCOUNTING_ONE_ONE_ZERO_AND_ZERO_LIVE_AUTHORITY",
"next_action":"await-explicit-owner-decision-for-selected-provider-local-supply-map-production-transaction",
"authority_effect":"EXACT_V151_PRODUCTION_BOOTSTRAP_COLLECTION_ACCEPTED_9_SOURCES_33_CARRIERS_41_MEMBERS_29047112_BYTES_41_ISOLATED_OPENS_READS_OWNER_ONE_ONE_ZERO_EMPTY_REPLAY_ZERO_LIVE_AUTHORITY",
"prohibited_inference":"ACCEPTANCE_DOES_NOT_RECREATE_OR_AUTHORIZE_AN_OWNER_TRANSACTION_REOPEN_COLLECTION_AUTHORIZATION_OPEN_OR_READ_LIVE_SELECTED_PROVIDER_PATHS_READ_OR_WRITE_PROJECT_REPLAY_PRODUCE_A_LOCAL_SUPPLY_MAP_POPULATE_MATERIALIZE_PUBLISH_DEPLOY_ACTIVATE_OR_EXECUTE_LIVE_AUTHORITY",
}

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--repo-root",type=Path,required=True); ap.add_argument("--output-root",type=Path,required=True); a=ap.parse_args()
    out=a.output_root/BASE/"review"/NAME; out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",newline="",encoding="utf-8") as h:
        w=csv.DictWriter(h,fieldnames=list(ROW),delimiter="\t",lineterminator="\n"); w.writeheader(); w.writerow(ROW)
    return 0
if __name__ == "__main__": raise SystemExit(main())
