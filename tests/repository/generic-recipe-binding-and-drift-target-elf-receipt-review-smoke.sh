#!/usr/bin/env bash
set -euo pipefail

REPO=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BASE="$REPO/experiments/glibc/selected-obsidian-provider-authority"
REVIEWER="$BASE/recipe/review-generic-recipe-binding-and-drift-target-elf.py"
RULES="$BASE/review/generic-recipe-binding-and-drift-target-receipt-review-rules.tsv"
REVIEW="$BASE/review/generic-recipe-binding-and-drift-target-receipt-review.tsv"
META="$BASE/review/generic-recipe-binding-and-drift-target-receipt-metadata.tsv"
ARTIFACTS="$BASE/review/generic-artifact-member-comparison-artifacts.tsv"

fail() {
    printf 'generic recipe binding and drift target ELF receipt review smoke: FAIL: %s\n' "$*" >&2
    exit 1
}

for path in "$REVIEWER" "$RULES" "$REVIEW" "$META" "$ARTIFACTS"; do
    [ -f "$path" ] || fail "missing review input: $path"
done
[ -x "$REVIEWER" ] || fail "reviewer is not executable"
python3 - "$REVIEWER" <<'PY'
from pathlib import Path
import sys
path=Path(sys.argv[1])
compile(path.read_text(encoding='utf-8'), str(path), 'exec')
PY

python3 - "$RULES" "$REVIEW" "$META" <<'PY'
import csv
import hashlib
import sys
from collections import Counter
from pathlib import Path

rules_path, review_path, meta_path = map(Path, sys.argv[1:])

def read(path):
    with path.open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

rules=read(rules_path)
review=read(review_path)
meta={row['field']:row['value'] for row in read(meta_path)}
assert len(rules)==37
assert len(review)==37
assert len({row['evidence_row_id'] for row in rules})==37
assert {row['evidence_row_id'] for row in review}=={row['evidence_row_id'] for row in rules}
assert all(row['receipt_review_policy']=='LINEAGE_ADAPTATION_AND_OBJECT_EVIDENCE_ONLY_NOT_AUTHORITY' for row in rules)
assert all(row['authority_state']=='CANDIDATE_ONLY' for row in rules)
assert Counter(row['object_member_review_state'] for row in review)==Counter({
    'EXACT_MEMBER_EXPECTED_SONAME_CANDIDATE_CONFIRMED':21,
    'DRIFT_TARGET_ELF_EXPECTED_SONAME_CANDIDATE_CONFIRMED':15,
    'EXPECTED_SONAME_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED':1,
})
assert Counter(row['adaptation_semantic_review_state'] for row in review)==Counter({
    'MATERIAL_RECIPE_DELTA_EVIDENCE_SEMANTIC_REVIEW_REQUIRED':20,
    'CONFIGURATION_OR_PACKAGING_DELTA_EVIDENCE_SEMANTIC_REVIEW_REQUIRED':8,
    'NO_EXPLICIT_DELTA_TOKEN_OBSERVED_SEMANTIC_REVIEW_OPEN':9,
})
assert all(row['recipe_lineage_review_state']=='PINNED_RECIPE_LINEAGE_CANDIDATE_CONFIRMED' for row in review)
assert all(row['artifact_build_attestation_review_state']=='OPEN_NO_INDEPENDENT_BUILD_PROVENANCE_OR_BYTE_REPRODUCTION' for row in review)
assert all(row['final_provider_state']=='UNRESOLVED' for row in review)
assert all(row['target_population_state']=='BLOCKED' for row in review)
assert meta['review_rules_sha256']==digest(rules_path)
assert meta['review_receipt_sha256']==digest(review_path)
assert meta['source_receipt_sha256']=='a415601cb3cfd6d3d85a69c589f38f9d2ba4151483b887c0e611d40a17beccd0'
assert meta['review_identity_rows']=='37'
assert meta['verified_cached_artifacts']=='34'
assert meta['artifact_build_attestations_accepted']=='0'
assert meta['termux_android_adaptations_accepted']=='0'
assert meta['concrete_filename_drifts_accepted']=='0'
assert meta['final_provider_decisions_accepted']=='0'
assert meta['target_rows_populated']=='0'
assert meta['next_state']=='DEFINE_BOUNDED_GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_REVIEW_SET'
by_label={row['identity_label']:row for row in review}
assert by_label['libsqlite3.so.0.8.6']['object_member_review_state']=='DRIFT_TARGET_ELF_EXPECTED_SONAME_CANDIDATE_CONFIRMED'
assert by_label['libsqlite3.so.0.8.6']['drift_target_observed_soname']=='libsqlite3.so.0'
assert by_label['libjpeg.so.62.3.0']['provider_review_eligibility_state']=='OBJECT_MEMBER_REQUIREMENT_UNSATISFIED'
assert by_label['libjpeg.so.62.3.0']['concrete_filename_policy_state']=='BLOCKED_EXPECTED_ALIAS_ABSENT'
PY

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
python3 - "$TMP" <<'PY'
import csv
import hashlib
import sys
from pathlib import Path

root=Path(sys.argv[1])

def write(name, fields, rows):
    with (root/name).open('w', newline='', encoding='utf-8') as stream:
        writer=csv.DictWriter(stream, fieldnames=fields, delimiter='\t', lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)

def manifest(rows):
    payload=''.join(f"{row['path']}\t{row['blob_oid']}\t{row['size']}\t{row['content_sha256']}\n" for row in sorted(rows,key=lambda r:r['path']))
    return hashlib.sha256(payload.encode()).hexdigest()

head='1'*40; tree='2'*40
recipe_a=[
 {'recipe_root':'gpkg/foo','path':'gpkg/foo/build.sh','mode':'100644','blob_oid':'3'*40,'size':'10','content_sha256':'a'*64},
]
recipe_b=[
 {'recipe_root':'gpkg/bar','path':'gpkg/bar/build.sh','mode':'100644','blob_oid':'4'*40,'size':'20','content_sha256':'b'*64},
 {'recipe_root':'gpkg/bar','path':'gpkg/bar/fix.patch','mode':'100644','blob_oid':'5'*40,'size':'30','content_sha256':'c'*64},
]
inventory=recipe_a+recipe_b
write('inventory.tsv', list(inventory[0]), inventory)

rule_fields=['evidence_row_id','capability_partition','identity_label','expected_artifact_id','expected_artifact_package','expected_artifact_version','expected_artifact_sha256','expected_soname_alias','expected_member_receipt_review_state','expected_alias_member_path','expected_alias_target_member_path','expected_recipe_root','expected_recipe_tree','expected_recipe_resolved_full_version','expected_recipe_source_url_raw','expected_recipe_source_sha256','expected_recipe_file_manifest_sha256','expected_drift_target_input_state','receipt_review_policy','authority_state']
common={'capability_partition':'test','receipt_review_policy':'LINEAGE_ADAPTATION_AND_OBJECT_EVIDENCE_ONLY_NOT_AUTHORITY','authority_state':'CANDIDATE_ONLY'}
rules=[
 common|{'evidence_row_id':'selected:exact','identity_label':'libfoo.so.1.0.0','expected_artifact_id':'artifact:foo','expected_artifact_package':'foo','expected_artifact_version':'1.0','expected_artifact_sha256':'d'*64,'expected_soname_alias':'libfoo.so.1','expected_member_receipt_review_state':'EXACT_CONCRETE_MEMBER_AND_EXPECTED_SONAME_OBSERVED','expected_alias_member_path':'-','expected_alias_target_member_path':'-','expected_recipe_root':'gpkg/foo','expected_recipe_tree':'6'*40,'expected_recipe_resolved_full_version':'1.0','expected_recipe_source_url_raw':'https://example.invalid/foo.tar.xz','expected_recipe_source_sha256':'e'*64,'expected_recipe_file_manifest_sha256':manifest(recipe_a),'expected_drift_target_input_state':'NOT_REQUIRED_EXACT_MEMBER_ALREADY_OBSERVED'},
 common|{'evidence_row_id':'selected:drift','identity_label':'libbar.so.2.9.0','expected_artifact_id':'artifact:bar','expected_artifact_package':'bar','expected_artifact_version':'2.0','expected_artifact_sha256':'f'*64,'expected_soname_alias':'libbar.so.2','expected_member_receipt_review_state':'EXPECTED_SONAME_ALIAS_SYMLINK_PRESENT_CONCRETE_FILENAME_DRIFT','expected_alias_member_path':'usr/lib/libbar.so.2','expected_alias_target_member_path':'usr/lib/libbar.so.2.8.0','expected_recipe_root':'gpkg/bar','expected_recipe_tree':'7'*40,'expected_recipe_resolved_full_version':'2.0','expected_recipe_source_url_raw':'https://example.invalid/bar.tar.xz','expected_recipe_source_sha256':'0'*64,'expected_recipe_file_manifest_sha256':manifest(recipe_b),'expected_drift_target_input_state':'PENDING_READ_ONLY_TARGET_ELF_INSPECTION'},
 common|{'evidence_row_id':'selected:absent','identity_label':'libjpeg.so.62.3.0','expected_artifact_id':'artifact:bar','expected_artifact_package':'bar','expected_artifact_version':'2.0','expected_artifact_sha256':'f'*64,'expected_soname_alias':'libjpeg.so.62','expected_member_receipt_review_state':'EXPECTED_SONAME_ALIAS_NOT_OBSERVED_DIFFERENT_FAMILY_MEMBERS_PRESENT','expected_alias_member_path':'-','expected_alias_target_member_path':'-','expected_recipe_root':'gpkg/bar','expected_recipe_tree':'7'*40,'expected_recipe_resolved_full_version':'2.0','expected_recipe_source_url_raw':'https://example.invalid/bar.tar.xz','expected_recipe_source_sha256':'0'*64,'expected_recipe_file_manifest_sha256':manifest(recipe_b),'expected_drift_target_input_state':'NOT_APPLICABLE_EXPECTED_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED'},
]
write('rules.tsv', rule_fields, rules)

binding_fields=['evidence_row_id','capability_partition','identity_label','member_receipt_review_state','artifact_id','artifact_package','artifact_version','artifact_sha256','recipe_root','recipe_tree','recipe_resolved_full_version','recipe_source_url_raw','recipe_source_sha256','recipe_file_manifest_sha256','adaptation_evidence_tokens','recipe_lineage_candidate_state','artifact_to_recipe_binding_state','termux_android_adaptation_state','drift_target_elf_review_state','final_provider_state','target_population_state']
def binding(rule,tokens,drift_state):
 return {'evidence_row_id':rule['evidence_row_id'],'capability_partition':'test','identity_label':rule['identity_label'],'member_receipt_review_state':rule['expected_member_receipt_review_state'],'artifact_id':rule['expected_artifact_id'],'artifact_package':rule['expected_artifact_package'],'artifact_version':rule['expected_artifact_version'],'artifact_sha256':rule['expected_artifact_sha256'],'recipe_root':rule['expected_recipe_root'],'recipe_tree':rule['expected_recipe_tree'],'recipe_resolved_full_version':rule['expected_recipe_resolved_full_version'],'recipe_source_url_raw':rule['expected_recipe_source_url_raw'],'recipe_source_sha256':rule['expected_recipe_source_sha256'],'recipe_file_manifest_sha256':rule['expected_recipe_file_manifest_sha256'],'adaptation_evidence_tokens':tokens,'recipe_lineage_candidate_state':'PINNED_RECIPE_FAMILY_VERSION_ALIGNED_CANDIDATE','artifact_to_recipe_binding_state':'OPEN_NO_BUILD_ATTESTATION','termux_android_adaptation_state':'PINNED_RECIPE_ADAPTATION_EVIDENCE_INVENTORIED_REVIEW_OPEN','drift_target_elf_review_state':drift_state,'final_provider_state':'UNRESOLVED','target_population_state':'BLOCKED'}
bindings=[binding(rules[0],'NONE_DECLARED','NOT_REQUIRED_EXACT_MEMBER_ALREADY_OBSERVED'),binding(rules[1],'CUSTOM_TERMUX_STEP;PATCH_FILE','DRIFT_TARGET_ELF_EXPECTED_SONAME_CONFIRMED'),binding(rules[2],'EXTRA_CONFIGURE_ARGS','NOT_APPLICABLE_EXPECTED_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED')]
write('binding.tsv', binding_fields, bindings)

drift_fields=['evidence_row_id','identity_label','artifact_id','artifact_package','expected_soname_alias','alias_member_path','target_member_path','target_member_size','target_member_mode_octal','target_member_sha256','elf_parse_state','elf_class','elf_data','elf_machine','observed_soname','drift_target_elf_review_state','object_member_evidence_state','artifact_to_recipe_binding_state','termux_android_adaptation_state','final_provider_state','target_population_state']
drift=[{'evidence_row_id':'selected:drift','identity_label':'libbar.so.2.9.0','artifact_id':'artifact:bar','artifact_package':'bar','expected_soname_alias':'libbar.so.2','alias_member_path':'usr/lib/libbar.so.2','target_member_path':'usr/lib/libbar.so.2.8.0','target_member_size':'100','target_member_mode_octal':'755','target_member_sha256':'1'*64,'elf_parse_state':'ELF_SONAME_PARSED','elf_class':'ELF64','elf_data':'LITTLE','elf_machine':'183','observed_soname':'libbar.so.2','drift_target_elf_review_state':'DRIFT_TARGET_ELF_EXPECTED_SONAME_CONFIRMED','object_member_evidence_state':'OBSERVED_CANDIDATE_NOT_AUTHORITY_ACCEPTED','artifact_to_recipe_binding_state':'OPEN_NO_BUILD_ATTESTATION','termux_android_adaptation_state':'OPEN_REVIEW_REQUIRED','final_provider_state':'UNRESOLVED','target_population_state':'BLOCKED'}]
write('drift.tsv', drift_fields, drift)

artifact_fields=['artifact_id','package','version','architecture','artifact_size','artifact_sha256']
artifacts=[{'artifact_id':'artifact:foo','package':'foo','version':'1.0','architecture':'aarch64','artifact_size':'10','artifact_sha256':'d'*64},{'artifact_id':'artifact:bar','package':'bar','version':'2.0','architecture':'aarch64','artifact_size':'20','artifact_sha256':'f'*64}]
write('artifacts.tsv', artifact_fields, artifacts)
verify_fields=['artifact_id','package','version','architecture','actual_size','actual_sha256','control_identity_state','package_operation_performed']
verified=[{'artifact_id':r['artifact_id'],'package':r['package'],'version':r['version'],'architecture':r['architecture'],'actual_size':r['artifact_size'],'actual_sha256':r['artifact_sha256'],'control_identity_state':'EXACT_PACKAGE_VERSION_ARCHITECTURE_MATCH','package_operation_performed':'NO'} for r in artifacts]
write('verify.tsv', verify_fields, verified)
write('source.tsv',['head','tree','origin','is_shallow','is_bare','worktree_state','fsck_state'],[{'head':head,'tree':tree,'origin':'https://example.invalid/source.git','is_shallow':'false','is_bare':'false','worktree_state':'CLEAN','fsck_state':'PASS'}])
summary={
 'source_repository_head':head,'source_repository_tree':tree,'review_identity_rows':'3','unique_recipe_roots':'2','selected_rule_artifacts':'2','verified_cached_artifacts':'2','recipe_family_version_aligned_rows':'3','drift_target_elf_rows':'1','drift_target_expected_soname_confirmed':'1','expected_alias_absent_correct_candidate_required':'1','artifact_to_recipe_bindings_accepted':'0','termux_android_adaptations_accepted':'0','final_provider_decisions_accepted':'0','target_rows_populated':'0','next_state':'REVIEW_BOUNDED_GENERIC_RECIPE_BINDING_AND_DRIFT_TARGET_ELF_RECEIPT'}
write('summary.tsv',['field','value'],[{'field':k,'value':v} for k,v in summary.items()])
PY

run_review() {
    local out=$1
    local binding=$2
    local drift=$3
    shift 3
    python3 "$REVIEWER" \
        --rules "$TMP/rules.tsv" \
        --binding-receipt "$binding" \
        --drift-receipt "$drift" \
        --artifact-verification "$TMP/verify.tsv" \
        --artifact-registry "$TMP/artifacts.tsv" \
        --recipe-inventory "$TMP/inventory.tsv" \
        --source-state "$TMP/source.tsv" \
        --summary "$TMP/summary.tsv" \
        --out "$out" \
        --source-receipt-archive synthetic.tar.zst \
        --source-receipt-sha256 "$(printf s | sha256sum | awk '{print $1}')" \
        --expected-identities 3 \
        --expected-drift-rows 1 \
        --expected-artifacts 2 \
        --expected-selected-artifacts 2 \
        --expected-recipe-roots 2 \
        --expected-recipe-files 3 \
        --expected-source-head "$(printf '1%.0s' {1..40})" \
        --expected-source-tree "$(printf '2%.0s' {1..40})" \
        --expected-source-origin https://example.invalid/source.git \
        "$@"
}

run_review "$TMP/out" "$TMP/binding.tsv" "$TMP/drift.tsv" >/dev/null
python3 - "$TMP/out/generic-recipe-binding-and-drift-target-receipt-review.tsv" <<'PY'
import csv,sys
from pathlib import Path
with Path(sys.argv[1]).open(newline='',encoding='utf-8') as stream:
    rows={row['evidence_row_id']:row for row in csv.DictReader(stream,delimiter='\t')}
assert rows['selected:exact']['adaptation_semantic_review_state']=='NO_EXPLICIT_DELTA_TOKEN_OBSERVED_SEMANTIC_REVIEW_OPEN'
assert rows['selected:drift']['adaptation_semantic_review_state']=='MATERIAL_RECIPE_DELTA_EVIDENCE_SEMANTIC_REVIEW_REQUIRED'
assert rows['selected:drift']['object_member_review_state']=='DRIFT_TARGET_ELF_EXPECTED_SONAME_CANDIDATE_CONFIRMED'
assert rows['selected:absent']['adaptation_semantic_review_state']=='CONFIGURATION_OR_PACKAGING_DELTA_EVIDENCE_SEMANTIC_REVIEW_REQUIRED'
assert rows['selected:absent']['provider_review_eligibility_state']=='OBJECT_MEMBER_REQUIREMENT_UNSATISFIED'
PY

cp "$TMP/drift.tsv" "$TMP/bad-drift.tsv"
sed -i 's/libbar\.so\.2\tDRIFT_TARGET/libbar.so.9\tDRIFT_TARGET/' "$TMP/bad-drift.tsv"
if run_review "$TMP/bad-drift-out" "$TMP/binding.tsv" "$TMP/bad-drift.tsv" >/dev/null 2>&1; then
    fail "reviewer accepted drift-target SONAME mismatch"
fi

cp "$TMP/binding.tsv" "$TMP/bad-binding.tsv"
sed -i '0,/OPEN_NO_BUILD_ATTESTATION/s//ACCEPTED/' "$TMP/bad-binding.tsv"
if run_review "$TMP/bad-binding-out" "$TMP/bad-binding.tsv" "$TMP/drift.tsv" >/dev/null 2>&1; then
    fail "reviewer accepted promoted artifact-to-recipe binding"
fi

printf 'generic recipe binding and drift target ELF receipt review smoke: PASS\n'
