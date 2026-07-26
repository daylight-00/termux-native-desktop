#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib
from pathlib import Path

BIND_FIELDS=['binding_row_id','composition_row_id','provider_review_id','artifact_package','artifact_version','member_basename','member_sha256','soname','authority_source','supply_artifact_kind','supply_artifact_sha256','archive_member_path','retained_result_sha256','acquisition_verification_state','binding_state','blocker_ids','authority_effect','prohibited_inference']
INT_FIELDS=['prerequisite_id','category','review_state','evidence','remaining_gap','closure_action','authority_effect','prohibited_inference']
META_FIELDS=['key','value']
EXCLUDE={'selected-provider-composition-members.tsv','selected-target-manifest-object-bindings.tsv','selected-target-manifest.tsv','selected-target-manifest-alias-bindings.tsv','selected-target-manifest-collisions.tsv','selected-target-manifest-metadata.tsv','selected-target-manifest-boundary-acceptance.tsv','selected-target-supply-byte-binding-review.tsv','selected-target-population-intervention-review.tsv','selected-target-population-intervention-supply-review-metadata.tsv'}

def read(p:Path):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p:Path,fields,rows):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def split(v):return [x for x in (v or '').split(';') if x]
def aligned(row, hash_value, sha_fields, path_fields):
 for sf in sha_fields:
  hashes=split(row.get(sf,''))
  if hash_value not in hashes:continue
  idx=hashes.index(hash_value)
  for pf in path_fields:
   paths=split(row.get(pf,''))
   if idx < len(paths):return paths[idx]
 return ''
def artifact_sha(row, member_hash):
 # Per-member artifact lists such as util-linux are aligned to exact member hashes.
 hashes=split(row.get('exact_member_sha256s','') or row.get('member_sha256s',''))
 artifacts=split(row.get('artifact_sha256s',''))
 if member_hash in hashes and len(artifacts)==len(hashes):return artifacts[hashes.index(member_hash)]
 for k in ('artifact_sha256','package_sha256'):
  if row.get(k):return row[k]
 if row.get('candidate_sha256')==member_hash:return member_hash
 return ''
def member_path(row, member_hash):
 p=aligned(row,member_hash,('exact_member_sha256s','member_sha256s'),('exact_member_paths','member_paths'))
 if p:return p
 if row.get('exact_member_sha256')==member_hash:return row.get('exact_member_path','')
 if row.get('member_sha256')==member_hash:return row.get('member_path','')
 if row.get('candidate_sha256')==member_hash:return row.get('candidate_member','')
 return ''
def accepted(row):
 text=';'.join(str(row.get(k,'')) for k in ('decision','candidate_decision','final_provider_state','authority_review_state'))
 return 'ACCEPTED' in text or 'QUALIFIED' in text

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path('.'));ap.add_argument('--output-root',type=Path,default=Path('.'));a=ap.parse_args()
 root=a.repo_root.resolve();out=a.output_root.resolve();review=root/'experiments/glibc/selected-obsidian-provider-authority/review'
 comp=[r for r in read(review/'selected-provider-composition-members.tsv') if r['composition_inclusion'].startswith('INCLUDED_')]
 if len(comp)!=41:raise SystemExit(f'expected 41 included members, got {len(comp)}')
 authority=[]
 for p in sorted(review.glob('*.tsv')):
  if p.name in EXCLUDE:continue
  try:
   for row in read(p):authority.append((p,row))
  except Exception:pass
 bindings=[]
 for c in comp:
  rid=c['provider_review_id'];mh=c['member_sha256'];candidates=[]
  for p,row in authority:
   if row.get('review_id')!=rid and row.get('provider_review_id')!=rid:continue
   if mh not in ';'.join(str(v or '') for v in row.values()):continue
   path=member_path(row,mh);asha=artifact_sha(row,mh);rsha=row.get('result_archive_sha256','')
   score=(1 if accepted(row) else 0,1 if rsha else 0,1 if asha else 0,1 if path else 0,1 if 'provider-authority' in p.name else 0)
   candidates.append((score,p,row,asha,path,rsha))
  if not candidates:raise SystemExit(f'no authority source for {rid} {c["member_basename"]}')
  score,p,row,asha,path,rsha=max(candidates,key=lambda x:x[0])
  if not asha or not path:raise SystemExit(f'incomplete artifact/member identity for {rid} {c["member_basename"]}: {p.name}')
  qualified=bool(rsha)
  kind='RESULT_ARCHIVE_DIRECT_MEMBER' if row.get('candidate_sha256')==mh else 'PACKAGE_ARCHIVE_MEMBER'
  bindings.append({
   'binding_row_id':'SUPPLY-BIND-'+hashlib.sha256((rid+'\0'+mh).encode()).hexdigest()[:16],
   'composition_row_id':c['composition_row_id'],'provider_review_id':rid,'artifact_package':c['artifact_package'],'artifact_version':c['artifact_version'],'member_basename':c['member_basename'],'member_sha256':mh,'soname':c['soname'],'authority_source':str(p.relative_to(root)),
   'supply_artifact_kind':kind,'supply_artifact_sha256':asha,'archive_member_path':path,'retained_result_sha256':rsha or '-',
   'acquisition_verification_state':'DIGEST_BOUND_RETAINED_RESULT_REVIEW_INPUT' if qualified else 'OPEN_RETAINED_RESULT_COORDINATE_REQUIRED',
   'binding_state':'QUALIFIED_READ_ONLY_BINDING_INPUT' if qualified else 'BLOCKED_RESULT_COORDINATE_MISSING',
   'blocker_ids':'-' if qualified else 'SUPPLY-BYTE-BINDING-OPEN;RETAINED-RESULT-COORDINATE-OPEN',
   'authority_effect':'READ_ONLY_BINDING_INPUT_ONLY_NO_EXTRACTION_COPY_OR_POPULATION' if qualified else 'NO_SUPPLY_BINDING_AUTHORITY_EFFECT',
   'prohibited_inference':'RESULT_OR_ARTIFACT_IDENTITY_DOES_NOT_AUTHORIZE_DOWNLOAD_EXTRACTION_COPY_INSTALL_POPULATION_MATERIALIZATION_DEPLOYMENT_OR_ACTIVATION'
  })
 q=sum(r['binding_state'].startswith('QUALIFIED_') for r in bindings);blocked=len(bindings)-q
 if (q,blocked)!=(14,27):raise SystemExit(f'expected 14 qualified / 27 blocked, got {q}/{blocked}')
 intervention=[
  ('INT-001','TARGET_POLICY','SATISFIED','SELECTED-TARGET-MANIFEST-ACCEPT-001;82_UNIQUE_ROWS;ZERO_COLLISIONS','-','RETAIN_ACCEPTED_POLICY','NO_NEW_AUTHORITY','TARGET_POLICY_ACCEPTANCE_IS_NOT_POPULATION'),
  ('INT-002','ALIAS_RESOLUTION','SATISFIED','41_OF_41_SONAME_ALIASES_RESOLVE_TO_ACCEPTED_CONCRETE_ROWS','-','RETAIN_ALIAS_RELATIONS','NO_NEW_AUTHORITY','ALIAS_RESOLUTION_IS_NOT_SYMLINK_CREATION'),
  ('INT-003','ATOMIC_FAMILIES','SATISFIED','AT_SPI2_CAIRO_PANGO_AND_GDK_GTK_FAMILIES_COMPLETE','-','PRESERVE_WHOLE_FAMILY_UPDATE_AND_ROLLBACK','NO_NEW_AUTHORITY','ATOMICITY_REVIEW_IS_NOT_MATERIALIZATION'),
  ('INT-004','SUPPLY_BINDINGS','BLOCKED','14_QUALIFIED_READ_ONLY_BINDING_INPUTS;27_RESULT_COORDINATE_GAPS','27_EXACT_RETAINED_RESULT_COORDINATES_AND_ACQUISITION_CONTRACTS_MISSING','CLOSE_RETAINED_RESULT_COORDINATES_WITHOUT_ACQUIRING_BYTES','INTERVENTION_RETAINED','ARTIFACT_AND_MEMBER_DIGESTS_ALONE_DO_NOT_AUTHORIZE_POPULATION'),
  ('INT-005','GENERATION_ROOT','OPEN','NO_ACCEPTED_ABSOLUTE_IMMUTABLE_GENERATION_ROOT','GENERATION_ROOT_AND_OWNER_BOUNDARY_MISSING','DEFINE_NON_LIVE_GENERATION_ROOT_AND_PROTECTED_PATH_EXCLUSIONS','INTERVENTION_RETAINED','TARGET_RELATIVE_PATHS_DO_NOT_SELECT_A_FILESYSTEM_ROOT'),
  ('INT-006','ATOMIC_PUBLICATION','OPEN','NO_SAME_FILESYSTEM_STAGING_OR_ATOMIC_RENAME_PROOF','STAGING_PUBLICATION_AND_INTERRUPTION_BOUNDARY_MISSING','REVIEW_SAME_FILESYSTEM_STAGING_AND_WHOLE_GENERATION_PUBLICATION','INTERVENTION_RETAINED','IMMUTABLE_ROWS_DO_NOT_PROVE_ATOMIC_PUBLICATION'),
  ('INT-007','SPACE_AND_OWNERSHIP','OPEN','NO_TOTAL_BYTE_BUDGET_FREE_SPACE_MARGIN_OR_MODE_OWNER_FEASIBILITY_RECORD','RESOURCE_AND_PERMISSION_PREFLIGHT_MISSING','REVIEW_BYTE_BUDGET_FREE_SPACE_OWNER_AND_MODE_PREFLIGHT','INTERVENTION_RETAINED','TERMUX_WRITABILITY_MUST_NOT_BE_ASSUMED'),
  ('INT-008','VERIFICATION_RECEIPT','OPEN','NO_PRE_PUBLICATION_WHOLE_GENERATION_DIGEST_ALIAS_ELF_AND_LOADER_RECEIPT_CONTRACT','MATERIALIZATION_RECEIPT_SCHEMA_MISSING','DEFINE_READ_ONLY_POST_STAGE_VERIFICATION_AND_RECEIPT_CONTRACT','INTERVENTION_RETAINED','SUCCESSFUL_COPY_COUNT_IS_NOT_VERIFICATION'),
  ('INT-009','ROLLBACK_SELECTOR','OPEN','NO_ACCEPTED_SELECTOR_PUBLICATION_OR_PRIOR_GENERATION_ROLLBACK_PROTOCOL','SELECTOR_AND_ROLLBACK_PROTOCOL_MISSING','REVIEW_ATOMIC_SELECTOR_PUBLICATION_AND_WHOLE_GENERATION_ROLLBACK','INTERVENTION_RETAINED','ROLLBACK_MUST_NOT_DELETE_OR_REWRITE_LIVE_FILES_IN_PLACE'),
  ('INT-010','FAILURE_CLEANUP_OBSERVABILITY','OPEN','NO_CRASH_RESUME_OR_ORPHAN_STAGING_OBSERVABILITY_CONTRACT','INTERRUPTION_CLEANUP_AND_OBSERVABILITY_MISSING','DEFINE_IDEMPOTENT_FAILURE_RECEIPTS_AND_ORPHAN_STAGING_POLICY','INTERVENTION_RETAINED','FAILURE_CLEANUP_MUST_NOT_TOUCH_PACKAGE_DB_OR_LIVE_GLIBC_PREFIX'),
 ]
 int_rows=[dict(zip(INT_FIELDS,x)) for x in intervention]
 meta=[
  {'key':'schema_version','value':'1'},{'key':'review_id','value':'TARGET-POPULATION-INTERVENTION-SUPPLY-REVIEW-001'},{'key':'decision','value':'INTERVENTION_RETAINED'},{'key':'concrete_object_count','value':'41'},{'key':'qualified_read_only_binding_count','value':str(q)},{'key':'blocked_result_coordinate_count','value':str(blocked)},{'key':'intervention_prerequisite_count','value':str(len(int_rows))},{'key':'satisfied_prerequisite_count','value':str(sum(r['review_state']=='SATISFIED' for r in int_rows))},{'key':'blocked_or_open_prerequisite_count','value':str(sum(r['review_state']!='SATISFIED' for r in int_rows))},{'key':'population_authorized','value':'NO'},{'key':'materializer_design_authorized','value':'NO'},{'key':'byte_acquisition_authorized','value':'NO'},{'key':'next_action','value':'close-retained-supply-result-coordinate-and-generation-root-prerequisite-gaps'},{'key':'authority_effect','value':'READ_ONLY_CENSUS_COMPLETED_INTERVENTION_RETAINED_NO_SUPPLY_ACQUISITION_EXTRACTION_COPY_POPULATION_MATERIALIZATION_DEPLOYMENT_OR_ACTIVATION'}]
 base=out/'experiments/glibc/selected-obsidian-provider-authority/review'
 write(base/'selected-target-supply-byte-binding-review.tsv',BIND_FIELDS,bindings)
 write(base/'selected-target-population-intervention-review.tsv',INT_FIELDS,int_rows)
 write(base/'selected-target-population-intervention-supply-review-metadata.tsv',META_FIELDS,meta)
if __name__=='__main__':main()
