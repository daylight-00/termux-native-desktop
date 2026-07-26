#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib
from pathlib import Path
FIELDS=['acceptance_id','decision','candidate_review_id','composition_acceptance_id','source_manifest_sha256','source_object_bindings_sha256','source_alias_bindings_sha256','source_collisions_sha256','source_metadata_sha256','accepted_target_row_count','accepted_regular_row_count','accepted_alias_row_count','accepted_unique_path_count','accepted_collision_count','accepted_unresolved_alias_count','accepted_target_domain','accepted_relative_root','candidate_issue_closed','accepted_authority_state','population_state','remaining_gate_ids','supply_byte_binding_state','intervention_lift_state','materializer_design_state','target_population_state','materialization_state','deployment_state','activation_state','update_boundary','rollback_boundary','next_action','authority_effect','prohibited_inference']
EXPECTED={
'selected-target-manifest.tsv':'1ec7f427599437bc0fc22df6ff171294a490296ef900f490b8c36f86c00ee63b',
'selected-target-manifest-object-bindings.tsv':'719484decceadd38d0c0a76c336d838f98f672eb6e27e26ad96143e54767ce60',
'selected-target-manifest-alias-bindings.tsv':'39bbac0376e31b0b792fc6c3af044e620472128337b2d06683e6d57846a2383b',
'selected-target-manifest-collisions.tsv':'5bb3a842bc757e66a903db8ab7e95599a4a77bc7c2266cfb8bee4f86f5c8cad8',
'selected-target-manifest-metadata.tsv':'1cfb289a7355945160184ba0a527f3c2d13682e9fc2157b21ce507baf2e79a09',
}
def rows(p):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path('.'));ap.add_argument('--output-root',type=Path,default=Path('.'));a=ap.parse_args()
 review=a.repo_root.resolve()/'experiments/glibc/selected-obsidian-provider-authority/review'
 for n,d in EXPECTED.items():
  if sha(review/n)!=d:raise SystemExit(f'frozen candidate digest mismatch: {n}')
 manifest=rows(review/'selected-target-manifest.tsv');objects=rows(review/'selected-target-manifest-object-bindings.tsv');aliases=rows(review/'selected-target-manifest-alias-bindings.tsv');collisions=rows(review/'selected-target-manifest-collisions.tsv')
 meta={r['key']:r['value'] for r in rows(review/'selected-target-manifest-metadata.tsv')}
 if len(manifest)!=82 or len(objects)!=41 or len(aliases)!=41 or collisions:raise SystemExit('candidate cardinality mismatch')
 if len({r['target_relative_path'] for r in manifest})!=82:raise SystemExit('target path collision')
 if any(r['population_state']!='UNPOPULATED_SCHEMA_ONLY' or r['authority_acceptance_state']!='PROVISIONAL_BLOCKED' or r['authority_issue_ids']!='TARGET-MANIFEST-ACCEPTANCE-OPEN' for r in manifest):raise SystemExit('candidate authority boundary drift')
 if meta.get('decision')!='QUALIFIED_NON_MUTATING_SELECTED_TARGET_MANIFEST':raise SystemExit('candidate decision drift')
 row={
 'acceptance_id':'SELECTED-TARGET-MANIFEST-ACCEPT-001','decision':'ACCEPTED_BOUNDED_NON_MUTATING_SELECTED_TARGET_MANIFEST','candidate_review_id':'SELECTED-TARGET-MANIFEST-REVIEW-001','composition_acceptance_id':'SELECTED-COMPOSITION-ACCEPT-001',
 'source_manifest_sha256':EXPECTED['selected-target-manifest.tsv'],'source_object_bindings_sha256':EXPECTED['selected-target-manifest-object-bindings.tsv'],'source_alias_bindings_sha256':EXPECTED['selected-target-manifest-alias-bindings.tsv'],'source_collisions_sha256':EXPECTED['selected-target-manifest-collisions.tsv'],'source_metadata_sha256':EXPECTED['selected-target-manifest-metadata.tsv'],
 'accepted_target_row_count':'82','accepted_regular_row_count':'41','accepted_alias_row_count':'41','accepted_unique_path_count':'82','accepted_collision_count':'0','accepted_unresolved_alias_count':'0','accepted_target_domain':'SHARED_PROVIDER','accepted_relative_root':'lib',
 'candidate_issue_closed':'TARGET-MANIFEST-ACCEPTANCE-OPEN','accepted_authority_state':'ACCEPTED_BOUNDED_TARGET_POLICY','population_state':'UNPOPULATED_SCHEMA_ONLY','remaining_gate_ids':'TARGET-POPULATION-INTERVENTION-LIFT-OPEN;SUPPLY-BYTE-BINDING-OPEN',
 'supply_byte_binding_state':'NOT_REVIEWED_NOT_AUTHORIZED','intervention_lift_state':'NOT_REVIEWED_NOT_LIFTED','materializer_design_state':'NOT_AUTHORIZED','target_population_state':'NOT_AUTHORIZED','materialization_state':'NOT_AUTHORIZED','deployment_state':'NOT_AUTHORIZED','activation_state':'NOT_AUTHORIZED',
 'update_boundary':'ANY_TARGET_PATH_NODE_POLICY_ALIAS_OBJECT_BINDING_DIGEST_ATOMIC_FAMILY_COMPOSITION_OR_CAPABILITY_CHANGE_REQUIRES_NEW_CLASS_D_TARGET_POLICY_REVIEW',
 'rollback_boundary':'BEFORE_POPULATION_REVOKE_ACCEPTANCE_DIRECTLY;AFTER_FUTURE_POPULATION_SELECT_PRIOR_IMMUTABLE_WHOLE_GENERATION_ONLY',
 'next_action':'review-target-population-intervention-lift-and-supply-byte-binding-boundary',
 'authority_effect':'EXACT_82_ROW_TARGET_POLICY_ACCEPTED_NO_SUPPLY_BINDING_COPY_INSTALL_POPULATION_MATERIALIZATION_DEPLOYMENT_OR_ACTIVATION',
 'prohibited_inference':'TARGET_POLICY_ACCEPTANCE_DOES_NOT_BIND_RETAINED_BYTES_CREATE_PATHS_OR_SYMLINKS_AUTHORIZE_MATERIALIZER_IMPLEMENTATION_POPULATION_DEPLOYMENT_LOADER_SELECTION_OR_ACTIVATION'}
 out=a.output_root/'experiments/glibc/selected-obsidian-provider-authority/review/selected-target-manifest-boundary-acceptance.tsv';out.parent.mkdir(parents=True,exist_ok=True)
 with out.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=FIELDS,delimiter='\t',lineterminator='\n');w.writeheader();w.writerow(row)
if __name__=='__main__':main()
