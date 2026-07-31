#!/usr/bin/env python3
from pathlib import Path
import argparse

REL=Path("experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-production-owner-decision-boundary-acceptance.tsv")
DATA='acceptance_id\tdecision\towner_statement_sha256\towner_statement_received_at\towner_statement_timezone\tbound_repository_head\tbound_repository_tree\tbound_remote_head\taccepted_provider_member_count\taccepted_provider_byte_count\taccepted_transaction_count\tconsumed_transaction_count\tremaining_transaction_count\tlocal_supply_map_count\tselected_provider_live_mutation_authorized\tproject_replay_mutation_authorized\ttarget_population_authorized\tmaterialization_authorized\tpublication_authorized\tdeployment_authorized\tactivation_authorized\tlive_authority_count\tnext_action\nSELECTED-PROVIDER-LOCAL-SUPPLY-MAP-PRODUCTION-OWNER-DECISION-ACCEPT-001\tACCEPTED_EXPLICIT_ONE_EXACT_COORDINATE_BINDING_MAP_GENERATION_SEALING_REVIEW_TRANSACTION_ONLY\t0a68ff343e98680b6409f603dc67d6b578e859fb0013abb7e2f4bc580c2d68f0\t2026-08-01T03:12:00+09:00\tAsia/Seoul\t017527d92cac73d95b771c9fbd4dcf48ad681a9c\teb5531119eb5b00a1b455ca51be20d30803274c4\t017527d92cac73d95b771c9fbd4dcf48ad681a9c\t41\t29047112\t1\t0\t1\t0\tfalse\tfalse\tfalse\tfalse\tfalse\tfalse\tfalse\t0\texecute-one-owner-authorized-selected-provider-local-supply-map-production-transaction\n'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo-root', type=Path, required=True)
    ap.add_argument('--output-root', type=Path, required=True)
    ns=ap.parse_args()
    out=ns.output_root/REL
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(DATA, encoding='utf-8')
if __name__=='__main__': main()
