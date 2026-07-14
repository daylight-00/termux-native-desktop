#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BASE="$ROOT/experiments/glibc/selected-obsidian-provider-authority"
ISSUANCE="$BASE/evidence-supply/requests/SUP-02/custodian-export/custodian-export-request-issuance.tsv"
CONTRACTS="$BASE/evidence-supply/requests/SUP-02/custodian-export/custodian-export-record-contract-issuance.tsv"
RULES="$BASE/review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-acquisition-receipt-review-rules.tsv"
REVIEWER="$BASE/recipe/review-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-acquisition-receipt.py"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
make_fixture(){
 local out=$1
 rm -rf "$out"; mkdir -p "$out/candidate-response-root"
 python3 - "$ISSUANCE" "$out" <<'PY'
import csv,pathlib,sys
issuance=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2])
with issuance.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
claim='CANDIDATE_CUSTODIAN_EXPORT_RESPONSE_REVIEW_REQUIRED_NO_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT'
fields=['request_id','root_review_id','recipe_root','recipe_tree','issued_request_locator','response_drop_locator','response_state','verified_record_count','build_run_id','custodian_identity','immutable_locator_or_signed_envelope','candidate_response_path','build_attestation_state','claim_boundary','next_action']
with (out/'request-response-acquisition-status.tsv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader()
 for r in rows:w.writerow({'request_id':r['request_id'],'root_review_id':r['root_review_id'],'recipe_root':r['recipe_root'],'recipe_tree':r['recipe_tree'],'issued_request_locator':r['issued_request_locator'],'response_drop_locator':r['response_drop_locator'],'response_state':'NO_RESPONSE_DROP_PRESENT','verified_record_count':'0','build_run_id':'-','custodian_identity':'-','immutable_locator_or_signed_envelope':'-','candidate_response_path':'-','build_attestation_state':'OPEN_NO_ACCEPTANCE','claim_boundary':claim,'next_action':'AWAIT_EXACT_CUSTODIAN_EXPORT_RESPONSE'})
inv=['response_record_id','request_id','requirement_id','record_name','record_format','source_relative_path','candidate_relative_path','sha256','size_bytes','format_validation','build_run_id','custodian_identity','immutable_locator_or_signed_envelope','acceptance_state','claim_boundary']
with (out/'response-record-inventory.tsv').open('w',encoding='utf-8',newline='') as f: csv.writer(f,delimiter='\t',lineterminator='\n').writerow(inv)
summary=[('source_head','636aad838111d37be0ab8bd8364aa5795b32256d'),('source_tree','3a20228415cb835267e34ea0c10be6297d00cdaf'),('request_issuance_sha256','64a0932ede3920b868bd922726db1336884be1f1b53e24dda7ef216fa6dced71'),('record_contract_issuance_sha256','5e18dee415443a0e5e39040d0147844eeeb6aa3b71a96107c9d51a31056af628'),('response_input_root_state','ABSENT'),('issued_requests','28'),('issued_record_contracts','84'),('complete_candidate_responses_acquired','0'),('requests_without_response','28'),('verified_response_records','0'),('verified_response_bytes','0'),('requests_acknowledged','0'),('responses_accepted','0'),('build_attestations_accepted','0'),('final_provider_decisions_accepted','0'),('target_rows_populated','0'),('claim_boundary',claim),('next_state','REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSE_ACQUISITION_RECEIPT')]
with (out/'summary.tsv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['field','value']);w.writerows(summary)
(out/'analysis.status').write_text('PASS\n');(out/'claim-boundary.txt').write_text(claim+'\n');(out/'next-state.txt').write_text('REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSE_ACQUISITION_RECEIPT\n')
PY
}
run_review(){
 local fixture=$1 out=$2
 rm -rf "$out"
 PYTHONDONTWRITEBYTECODE=1 python3 "$REVIEWER" --request-issuance "$ISSUANCE" --record-contract-issuance "$CONTRACTS" --receipt-dir "$fixture" --rules "$RULES" --out "$out"
}
make_fixture "$TMP/fixture"
run_review "$TMP/fixture" "$TMP/review"
for n in generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-acquisition-receipt-review.tsv generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-root-custodian-export-response-acquisition-receipt-review.tsv generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-acquisition-receipt-review-metadata.tsv; do cmp "$TMP/review/$n" "$BASE/review/$n"; done
[[ $(cat "$TMP/review/analysis.status") == PASS ]]
[[ $(cat "$TMP/review/next-state.txt") == FULFILL_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSES ]]
tamper(){
 local name=$1 code=$2
 cp -a "$TMP/fixture" "$TMP/$name"
 python3 - "$TMP/$name" <<PY
$code
PY
 if run_review "$TMP/$name" "$TMP/out-$name" >/dev/null 2>&1; then echo "$name unexpectedly accepted" >&2; exit 1; fi
}
tamper false_response 'import csv,pathlib,sys
p=pathlib.Path(sys.argv[1])/"request-response-acquisition-status.tsv"
with p.open(encoding="utf-8",newline="") as f:r=list(csv.DictReader(f,delimiter="\t")); fields=list(r[0])
r[0]["response_state"]="COMPLETE_CANDIDATE_RESPONSE_ACQUIRED_REVIEW_REQUIRED";r[0]["verified_record_count"]="3"
with p.open("w",encoding="utf-8",newline="") as f:w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(r)'
tamper invented_inventory 'import csv,pathlib,sys
p=pathlib.Path(sys.argv[1])/"response-record-inventory.tsv"
with p.open(encoding="utf-8",newline="") as f: fields=next(csv.reader(f,delimiter="\t"))
with p.open("a",encoding="utf-8",newline="") as f: csv.writer(f,delimiter="\t",lineterminator="\n").writerow(["x"]*len(fields))'
tamper acknowledgement_promotion 'import csv,pathlib,sys
p=pathlib.Path(sys.argv[1])/"summary.tsv"
with p.open(encoding="utf-8",newline="") as f:r=list(csv.DictReader(f,delimiter="\t")); fields=list(r[0])
for x in r:
 if x["field"]=="requests_acknowledged":x["value"]="1"
with p.open("w",encoding="utf-8",newline="") as f:w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(r)'
mkdir "$TMP/fixture/candidate-response-root/invented"
if run_review "$TMP/fixture" "$TMP/out-candidate" >/dev/null 2>&1; then echo candidate_root_drift unexpectedly accepted >&2; exit 1; fi
printf '%s\n' GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSE_ACQUISITION_RECEIPT_REVIEW_SMOKE_PASS
