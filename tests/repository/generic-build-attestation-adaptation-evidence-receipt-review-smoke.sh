#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
REVIEWER="$ROOT/experiments/glibc/selected-obsidian-provider-authority/recipe/review-generic-build-attestation-and-adaptation-evidence.py"
REQUIREMENTS="$ROOT/experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-review-requirements.tsv"
RULES="$ROOT/experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-evidence-receipt-review-rules.tsv"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

fail() {
    printf 'generic build attestation/adaptation evidence receipt review smoke: FAIL: %s\n' "$*" >&2
    exit 1
}

python3 - "$TMP" "$REQUIREMENTS" "$RULES" <<'PY'
import csv
import sys
from pathlib import Path

out=Path(sys.argv[1]); req_path=Path(sys.argv[2]); rules_path=Path(sys.argv[3])
out.mkdir(parents=True,exist_ok=True)

def read(path):
    with path.open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f,delimiter='\t'))

def write(name, fields, rows):
    with (out/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n')
        w.writeheader(); w.writerows(rows)

reqs=read(req_path); rules=read(rules_path); rule={r['requirement_id']:r for r in rules}
status=[]; gaps=[]
for r in reqs:
    q=rule[r['requirement_id']]
    status.append({**r,
        'collection_state':q['expected_collection_state'],
        'evidence_references':q['expected_evidence_references'],
        'collection_note':'synthetic bounded evidence or explicit gap',
        'review_state':'EVIDENCE_COLLECTED_OR_GAP_RECORDED_REVIEW_REQUIRED',
        'authority_state':'OPEN_NO_ACCEPTANCE'})
    if q['review_disposition']=='GAP':
        gaps.append({'requirement_id':r['requirement_id'],'dimension':r['dimension'],'scope':r['scope'],
            'collection_state':q['expected_collection_state'],'gap':'synthetic explicit gap',
            'next_action':'PROVIDE_BOUNDED_EVIDENCE_FOR_SEPARATE_RECEIPT_REVIEW'})
write('requirement.tsv',list(status[0]),status)
write('gaps.tsv',['requirement_id','dimension','scope','collection_state','gap','next_action'],gaps)

root_fields=['root_review_id','review_tier','recipe_root','recipe_tree','recipe_resolved_full_version','artifact_ids','artifact_packages','artifact_count','identity_count','adaptation_evidence_tokens','build_attestation_requirement_set','adaptation_requirement_set','concrete_filename_requirement_set','object_correction_requirement_set','eligible_object_count','blocked_object_count','review_state','authority_state','next_action']
roots=[
 {'root_review_id':'root:one','review_tier':'T1_MATERIAL_DELTA_AND_DRIFT','recipe_root':'gpkg/one','recipe_tree':'1'*40,'recipe_resolved_full_version':'1.0','artifact_ids':'artifact:one','artifact_packages':'one','artifact_count':'1','identity_count':'2','adaptation_evidence_tokens':'PATCH_FILE','build_attestation_requirement_set':'BA-001;BA-002;BA-003;BA-004;BA-005','adaptation_requirement_set':'AD-001;AD-002;AD-003;AD-004;AD-005','concrete_filename_requirement_set':'CF-001;CF-002;CF-003;CF-004','object_correction_requirement_set':'NONE','eligible_object_count':'2','blocked_object_count':'0','review_state':'REQUIREMENTS_DEFINED_EVIDENCE_NOT_COLLECTED','authority_state':'OPEN_NO_ACCEPTANCE','next_action':'COLLECT_ROOT_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE'},
 {'root_review_id':'root:two','review_tier':'T0_OBJECT_REQUIREMENT_CORRECTION','recipe_root':'gpkg/two','recipe_tree':'2'*40,'recipe_resolved_full_version':'2.0','artifact_ids':'artifact:two','artifact_packages':'two','artifact_count':'1','identity_count':'1','adaptation_evidence_tokens':'EXTRA_CONFIGURE_ARGS','build_attestation_requirement_set':'BA-001;BA-002;BA-003;BA-004;BA-005','adaptation_requirement_set':'AD-001;AD-002;AD-003;AD-004','concrete_filename_requirement_set':'NONE','object_correction_requirement_set':'OJ-001','eligible_object_count':'0','blocked_object_count':'1','review_state':'REQUIREMENTS_DEFINED_EVIDENCE_NOT_COLLECTED','authority_state':'OPEN_NO_ACCEPTANCE','next_action':'CORRECT_OBJECT_REQUIREMENT'},
]
write('root-set.tsv',root_fields,roots)
root_obs=[]
for r,files,signals in [(roots[0],2,2),(roots[1],1,0)]:
    root_obs.append({'root_review_id':r['root_review_id'],'review_tier':r['review_tier'],'recipe_root':r['recipe_root'],'recipe_tree':r['recipe_tree'],'recipe_resolved_full_version':r['recipe_resolved_full_version'],'recipe_source_url_raw':'https://example.invalid/source.tar.xz','recipe_source_sha256':'a'*64,'recipe_file_count':str(files),'build_script_signal_count':str(signals),'artifact_count':r['artifact_count'],'identity_count':r['identity_count'],'adaptation_evidence_tokens':r['adaptation_evidence_tokens'],'build_provenance_collection_state':'EXTERNAL_DIGEST_BOUND_BUILD_RECORD_REQUIRED','recipe_inventory_collection_state':'COMPLETE_PINNED_RECIPE_FILE_INVENTORY_COLLECTED','upstream_semantic_comparison_state':'NOT_PERFORMED_REQUIRES_BOUNDED_SEMANTIC_REVIEW','adaptation_classification_state':'OPEN_NO_NECESSITY_CLASSIFICATION','update_rollback_state':'OPEN_NO_CONTINUITY_POLICY','authority_state':'OPEN_NO_ACCEPTANCE'})
write('root-observations.tsv',list(root_obs[0]),root_obs)

obj_fields=['object_review_id','evidence_row_id','review_tier','capability_partition','identity_label','artifact_id','artifact_package','artifact_version','artifact_sha256','recipe_root','recipe_tree','recipe_resolved_full_version','adaptation_evidence_tokens','object_member_review_state','build_attestation_requirement_set','adaptation_requirement_set','concrete_filename_requirement_set','object_correction_requirement_set','review_eligibility_state','authority_state','target_population_state','next_action']
objs=[
 {'object_review_id':'object:exact','evidence_row_id':'selected:exact','review_tier':'T2_MATERIAL_DELTA_EXACT','capability_partition':'test','identity_label':'libexact.so.1.0','artifact_id':'artifact:one','artifact_package':'one','artifact_version':'1.0','artifact_sha256':'b'*64,'recipe_root':'gpkg/one','recipe_tree':'1'*40,'recipe_resolved_full_version':'1.0','adaptation_evidence_tokens':'PATCH_FILE','object_member_review_state':'EXACT_MEMBER_EXPECTED_SONAME_CANDIDATE_CONFIRMED','build_attestation_requirement_set':'BA-001;BA-002;BA-003;BA-004;BA-005','adaptation_requirement_set':'AD-001;AD-002;AD-003;AD-004;AD-005','concrete_filename_requirement_set':'NONE','object_correction_requirement_set':'NONE','review_eligibility_state':'EVIDENCE_COLLECTION_ELIGIBLE_AUTHORITY_BLOCKED','authority_state':'OPEN_NO_ACCEPTANCE','target_population_state':'UNPOPULATED','next_action':'COLLECT_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE'},
 {'object_review_id':'object:drift','evidence_row_id':'selected:drift','review_tier':'T1_MATERIAL_DELTA_AND_DRIFT','capability_partition':'test','identity_label':'libdrift.so.2.9','artifact_id':'artifact:one','artifact_package':'one','artifact_version':'1.0','artifact_sha256':'b'*64,'recipe_root':'gpkg/one','recipe_tree':'1'*40,'recipe_resolved_full_version':'1.0','adaptation_evidence_tokens':'PATCH_FILE','object_member_review_state':'DRIFT_TARGET_ELF_EXPECTED_SONAME_CANDIDATE_CONFIRMED','build_attestation_requirement_set':'BA-001;BA-002;BA-003;BA-004;BA-005','adaptation_requirement_set':'AD-001;AD-002;AD-003;AD-004;AD-005','concrete_filename_requirement_set':'CF-001;CF-002;CF-003;CF-004','object_correction_requirement_set':'NONE','review_eligibility_state':'EVIDENCE_COLLECTION_ELIGIBLE_AUTHORITY_BLOCKED','authority_state':'OPEN_NO_ACCEPTANCE','target_population_state':'UNPOPULATED','next_action':'COLLECT_BUILD_ATTESTATION_ADAPTATION_AND_DRIFT_POLICY_EVIDENCE'},
 {'object_review_id':'object:blocked','evidence_row_id':'selected:blocked','review_tier':'T0_OBJECT_REQUIREMENT_CORRECTION','capability_partition':'test','identity_label':'libjpeg.so.62.3.0','artifact_id':'artifact:two','artifact_package':'two','artifact_version':'2.0','artifact_sha256':'c'*64,'recipe_root':'gpkg/two','recipe_tree':'2'*40,'recipe_resolved_full_version':'2.0','adaptation_evidence_tokens':'EXTRA_CONFIGURE_ARGS','object_member_review_state':'EXPECTED_SONAME_ALIAS_NOT_OBSERVED_DIFFERENT_FAMILY_MEMBERS_PRESENT','build_attestation_requirement_set':'BA-001;BA-002;BA-003;BA-004;BA-005','adaptation_requirement_set':'AD-001;AD-002;AD-003;AD-004','concrete_filename_requirement_set':'NONE','object_correction_requirement_set':'OJ-001','review_eligibility_state':'OBJECT_REQUIREMENT_CORRECTION_BLOCKED','authority_state':'OPEN_NO_ACCEPTANCE','target_population_state':'UNPOPULATED','next_action':'CORRECT_OBJECT_REQUIREMENT_OR_LOCATE_EXACT_CANDIDATE'},
]
write('object-set.tsv',obj_fields,objs)

files=[
 {'recipe_root':'gpkg/one','recipe_tree':'1'*40,'path':'gpkg/one/build.sh','mode':'100644','blob_oid':'3'*40,'size':'10','content_sha256':'d'*64,'file_class':'BUILD_SCRIPT','semantic_review_state':'NOT_PERFORMED_EVIDENCE_INVENTORY_ONLY'},
 {'recipe_root':'gpkg/one','recipe_tree':'1'*40,'path':'gpkg/one/fix.patch','mode':'100644','blob_oid':'4'*40,'size':'20','content_sha256':'e'*64,'file_class':'PATCH','semantic_review_state':'NOT_PERFORMED_EVIDENCE_INVENTORY_ONLY'},
 {'recipe_root':'gpkg/two','recipe_tree':'2'*40,'path':'gpkg/two/build.sh','mode':'100644','blob_oid':'5'*40,'size':'30','content_sha256':'f'*64,'file_class':'BUILD_SCRIPT','semantic_review_state':'NOT_PERFORMED_EVIDENCE_INVENTORY_ONLY'},
]
write('recipe-files.tsv',list(files[0]),files)
signals=[
 {'recipe_root':'gpkg/one','recipe_tree':'1'*40,'path':'gpkg/one/build.sh','line_number':'1','signal_classes':'PATCH_FILE','line_sha256':'1'*64,'line_text':'patch signal','semantic_classification_state':'UNCLASSIFIED_SYNTACTIC_SIGNAL_ONLY'},
 {'recipe_root':'gpkg/one','recipe_tree':'1'*40,'path':'gpkg/one/build.sh','line_number':'2','signal_classes':'EXTRA_CONFIGURE_ARGS','line_sha256':'2'*64,'line_text':'configure signal','semantic_classification_state':'UNCLASSIFIED_SYNTACTIC_SIGNAL_ONLY'},
]
write('signals.tsv',list(signals[0]),signals)

cross=[]
for obj,root in [(objs[0],roots[0]),(objs[1],roots[0]),(objs[2],roots[1])]:
    cross.append({'root_review_id':root['root_review_id'],'object_review_id':obj['object_review_id'],'evidence_row_id':obj['evidence_row_id'],'recipe_root':obj['recipe_root'],'identity_label':obj['identity_label'],'artifact_id':obj['artifact_id'],'adaptation_evidence_tokens':obj['adaptation_evidence_tokens'],'adaptation_requirement_set':obj['adaptation_requirement_set'],'object_impact_evidence_state':'ROOT_OBJECT_CROSSWALK_COLLECTED_SEMANTIC_IMPACT_REVIEW_OPEN','authority_state':'OPEN_NO_ACCEPTANCE'})
write('crosswalk.tsv',list(cross[0]),cross)
outputs=[
 {'object_review_id':'object:exact','evidence_row_id':'selected:exact','identity_label':'libexact.so.1.0','artifact_id':'artifact:one','artifact_package':'one','artifact_version':'1.0','artifact_sha256':'b'*64,'recipe_root':'gpkg/one','recipe_tree':'1'*40,'member_path':'usr/lib/libexact.so.1.0','member_sha256':'6'*64,'observed_soname':'libexact.so.1','alias_member_path':'-','alias_link_target':'-','output_binding_evidence_state':'EXACT_MEMBER_DIGEST_AND_SONAME_OBSERVED_NOT_BUILD_ATTESTED','producing_build_binding_state':'OPEN_NO_DIGEST_BOUND_BUILD_RECORD','authority_state':'OPEN_NO_ACCEPTANCE','target_population_state':'UNPOPULATED'},
 {'object_review_id':'object:drift','evidence_row_id':'selected:drift','identity_label':'libdrift.so.2.9','artifact_id':'artifact:one','artifact_package':'one','artifact_version':'1.0','artifact_sha256':'b'*64,'recipe_root':'gpkg/one','recipe_tree':'1'*40,'member_path':'usr/lib/libdrift.so.2.8','member_sha256':'7'*64,'observed_soname':'libdrift.so.2','alias_member_path':'usr/lib/libdrift.so.2','alias_link_target':'libdrift.so.2.8','output_binding_evidence_state':'ALIAS_TARGET_MEMBER_DIGEST_AND_SONAME_OBSERVED_NOT_BUILD_ATTESTED','producing_build_binding_state':'OPEN_NO_DIGEST_BOUND_BUILD_RECORD','authority_state':'OPEN_NO_ACCEPTANCE','target_population_state':'UNPOPULATED'},
 {'object_review_id':'object:blocked','evidence_row_id':'selected:blocked','identity_label':'libjpeg.so.62.3.0','artifact_id':'artifact:two','artifact_package':'two','artifact_version':'2.0','artifact_sha256':'c'*64,'recipe_root':'gpkg/two','recipe_tree':'2'*40,'member_path':'-','member_sha256':'-','observed_soname':'-','alias_member_path':'-','alias_link_target':'-','output_binding_evidence_state':'OBJECT_REQUIREMENT_UNSATISFIED_NO_OUTPUT_BINDING','producing_build_binding_state':'OPEN_NO_DIGEST_BOUND_BUILD_RECORD','authority_state':'OPEN_NO_ACCEPTANCE','target_population_state':'UNPOPULATED'},
]
write('outputs.tsv',list(outputs[0]),outputs)

verify=[
 {'input':'requirements','path':'requirements','sha256_or_state':'8'*64,'verification_state':'PASS'},
 {'input':'root_review_set','path':'root-set','sha256_or_state':'9'*64,'verification_state':'PASS'},
 {'input':'object_review_set','path':'object-set','sha256_or_state':'a'*64,'verification_state':'PASS'},
 {'input':'member_receipt_review','path':'member','sha256_or_state':'b'*64,'verification_state':'PASS'},
 {'input':'recipe_receipt_review','path':'recipe','sha256_or_state':'c'*64,'verification_state':'PASS'},
 {'input':'foundation_summary','path':'summary','sha256_or_state':'d'*64,'verification_state':'PASS'},
 {'input':'source_checkout','path':'source','sha256_or_state':'e'*64,'verification_state':'PINNED_CLEAN_IMMUTABLE_PASS'},
]
write('input-verification.tsv',list(verify[0]),verify)
summary={
 'requirements':'16','root_work_units':'2','object_work_units':'3','verified_foundation_artifacts':'2','recipe_files_collected':'3','build_script_signal_rows':'2','exact_output_rows':'1','drift_output_rows':'1','blocked_object_rows':'1','local_evidence_or_partial_evidence_requirement_rows':'6','external_semantic_policy_or_correction_gap_rows':'10','artifact_build_attestations_accepted':'0','termux_android_adaptations_accepted':'0','concrete_filename_drifts_accepted':'0','final_provider_decisions_accepted':'0','target_rows_populated':'0','package_operations_performed':'0','maintainer_scripts_executed':'0','filesystem_payload_extractions':'0','network_acquisitions':'0','source_manifest_before':'f'*64,'source_manifest_after':'f'*64,'next_state':'REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE_RECEIPT'}
write('summary.tsv',['field','value'],[{'field':k,'value':v} for k,v in summary.items()])
(out/'analysis.status').write_text('PASS\n')
(out/'claim-boundary.txt').write_text('Local observations are not build provenance or adaptation acceptance.\nNo build, package operation, maintainer script, payload extraction, network acquisition, provider promotion or target population is performed.\n')
(out/'collector-next-state.txt').write_text('REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE_RECEIPT\n')
(out/'transaction-status.txt').write_text('TRANSACTION=PASS\nVALIDATION=PASS\nEVIDENCE_COLLECTION=PASS\nPUSH_AFTER_APPLY=1\n')
(out/'final-git-state.txt').write_text('branch=test\nhead='+'1'*40+'\ntree='+'2'*40+'\n')
(out/'remote-state.txt').write_text('push_after_apply=1\nremote_head_before='+'0'*40+'\nremote_head_after='+'1'*40+'\n')
PY

run_review() {
    local out=$1
    shift
    python3 "$REVIEWER" \
        --requirements "$REQUIREMENTS" \
        --root-review-set "$TMP/root-set.tsv" \
        --object-review-set "$TMP/object-set.tsv" \
        --rules "$RULES" \
        --requirement-status "${REQUIREMENT_STATUS_INPUT:-$TMP/requirement.tsv}" \
        --root-observations "$TMP/root-observations.tsv" \
        --recipe-file-evidence "$TMP/recipe-files.tsv" \
        --build-script-signal-evidence "$TMP/signals.tsv" \
        --root-object-crosswalk "$TMP/crosswalk.tsv" \
        --artifact-member-output "${ARTIFACT_OUTPUT_INPUT:-$TMP/outputs.tsv}" \
        --external-gaps "${EXTERNAL_GAPS_INPUT:-$TMP/gaps.tsv}" \
        --input-verification "$TMP/input-verification.tsv" \
        --summary "$TMP/summary.tsv" \
        --analysis-status "$TMP/analysis.status" \
        --claim-boundary "$TMP/claim-boundary.txt" \
        --collector-next-state "$TMP/collector-next-state.txt" \
        --transaction-status "$TMP/transaction-status.txt" \
        --final-git-state "$TMP/final-git-state.txt" \
        --remote-state "$TMP/remote-state.txt" \
        --out "$out" \
        --source-receipt-archive synthetic.tar.zst \
        --source-receipt-sha256 "$(printf synthetic | sha256sum | awk '{print $1}')" \
        --expected-roots 2 \
        --expected-objects 3 \
        --expected-recipe-files 3 \
        --expected-signals 2 \
        --expected-exact-outputs 1 \
        --expected-drift-outputs 1 \
        --expected-blocked-outputs 1 \
        --expected-foundation-artifacts 2 \
        --expected-root-artifact-references 2 \
        --expected-branch test \
        --expected-source-head "$(printf '1%.0s' {1..40})" \
        --expected-source-tree "$(printf '2%.0s' {1..40})" \
        "$@"
}

run_review "$TMP/out" >/dev/null
python3 - "$TMP/out" <<'PY'
import csv,sys
from pathlib import Path
root=Path(sys.argv[1])
def rows(name):
    with (root/name).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
req={r['requirement_id']:r for r in rows('generic-build-attestation-adaptation-evidence-receipt-review.tsv')}
assert req['BA-003']['receipt_review_state']=='LOCAL_EVIDENCE_CONFIRMED_BOUNDED_REVIEW_INPUT'
assert req['BA-001']['receipt_review_state']=='EXTERNAL_SEMANTIC_POLICY_OR_CORRECTION_GAP_CONFIRMED'
obj={r['object_review_id']:r for r in rows('generic-build-attestation-adaptation-object-evidence-receipt-review.tsv')}
assert obj['object:exact']['output_evidence_review_state'].startswith('EXACT_MEMBER')
assert obj['object:drift']['consumer_binding_review_state']=='OPEN_CONSUMER_BINDING_EVIDENCE_REQUIRED'
assert obj['object:blocked']['object_requirement_review_state'].startswith('OPEN_CORRECT_REQUIREMENT')
PY

cp "$TMP/requirement.tsv" "$TMP/bad-requirement.tsv"
sed -i '0,/OPEN_NO_ACCEPTANCE/s//ACCEPTED/' "$TMP/bad-requirement.tsv"
if REQUIREMENT_STATUS_INPUT="$TMP/bad-requirement.tsv" run_review "$TMP/bad-out-authority" >/dev/null 2>&1; then
    fail "reviewer accepted authority promotion"
fi

head -n -1 "$TMP/gaps.tsv" > "$TMP/bad-gaps.tsv"
if EXTERNAL_GAPS_INPUT="$TMP/bad-gaps.tsv" run_review "$TMP/bad-out-gap" >/dev/null 2>&1; then
    fail "reviewer accepted missing explicit gap"
fi

cp "$TMP/outputs.tsv" "$TMP/bad-outputs.tsv"
sed -i '0,/EXACT_MEMBER_DIGEST_AND_SONAME_OBSERVED_NOT_BUILD_ATTESTED/s//ALIAS_TARGET_MEMBER_DIGEST_AND_SONAME_OBSERVED_NOT_BUILD_ATTESTED/' "$TMP/bad-outputs.tsv"
if ARTIFACT_OUTPUT_INPUT="$TMP/bad-outputs.tsv" run_review "$TMP/bad-out-output" >/dev/null 2>&1; then
    fail "reviewer accepted output class cardinality drift"
fi

printf 'generic build attestation/adaptation evidence receipt review smoke: PASS\n'
