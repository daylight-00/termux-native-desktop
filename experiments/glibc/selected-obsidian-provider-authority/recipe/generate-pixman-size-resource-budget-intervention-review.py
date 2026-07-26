#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,math
from pathlib import Path

PIXMAN_RESULT_REMOTE='gdrive:ChatGPT-Agent-Exchange/termux-native-desktop/user-results/termux-native-desktop-cairo-pixman-prerequisite-evidence-v2-20260718T033508Z-results.tar.zst'
PIXMAN_FILE_ID='1-slSGw5H4_Qn-lL9z8aBeqOBlybW7vBB'
PIXMAN_RESULT_SHA='3df4f72452b6fb36525ea651f58a0d9d0e551d6ab1f0076653588e767fb1ad9a'
PIXMAN_MEMBER='libpixman-1.so.0.46.4'
PIXMAN_MEMBER_SHA='cab54c7f8e4c3a5c1980aa7564b9321114418f2d3c6fa37a3c0723f9f22e1eb2'
PIXMAN_MEMBER_SIZE=460920
PIXMAN_ARCHIVE_MEMBER='./evidence/pixman/libpixman-1.so.0.46.4'
PIXMAN_SHA_EVIDENCE='./evidence/pixman/sha256.txt'
RECEIPT_FLOOR=1048576

EVIDENCE_FIELDS=['review_id','provider_review_id','result_remote','drive_file_id','result_sha256','archive_member_path','member_basename','member_sha256','member_size','size_source','verification_state','authority_effect','prohibited_inference']
GATE_FIELDS=['prerequisite_id','category','evidence_state','review_result','evidence_reference','remaining_runtime_preflight','authority_effect','prohibited_inference']

def read(p):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,fields,rows):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def next_pow2(n):return 1 if n<=1 else 1 << (n-1).bit_length()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[4]);ap.add_argument('--output-root',type=Path);a=ap.parse_args()
 root=a.repo_root.resolve();out=(a.output_root or root).resolve();review=root/'experiments/glibc/selected-obsidian-provider-authority/review'
 sizes=read(review/'selected-target-member-size-census.tsv');bindings=read(review/'selected-target-manifest-object-bindings.tsv');aliases=read(review/'selected-target-manifest-alias-bindings.tsv');manifest=read(review/'selected-target-manifest.tsv');contracts=read(review/'selected-target-generation-root-contract-review.tsv')
 if len(sizes)!=41 or len(bindings)!=41 or len(aliases)!=41 or len(manifest)!=82 or len(contracts)!=7:raise SystemExit('unexpected canonical row count')
 pix=[r for r in sizes if r['provider_review_id']=='PIXMAN-CAIRO-PREQ-PROV-001']
 if len(pix)!=1 or pix[0]['member_basename']!=PIXMAN_MEMBER or pix[0]['member_sha256']!=PIXMAN_MEMBER_SHA or pix[0]['size_state']!='OPEN':raise SystemExit('historical Pixman blocker drift')
 exact_sum=sum(int(r['member_size']) for r in sizes if r['size_state']=='EXACT')
 if exact_sum!=28586192:raise SystemExit(f'historical size sum drift {exact_sum}')
 total=exact_sum+PIXMAN_MEMBER_SIZE
 bind_by={r['member_basename']:r for r in bindings}
 regular_by={r['target_relative_path'].split('/')[-1]:r for r in manifest if r['target_node_type']=='REGULAR'}
 if set(bind_by)!=set(regular_by):raise SystemExit('binding/target mismatch')
 object_receipts=[]
 for r in sorted(sizes,key=lambda x:x['member_basename']):
  size=PIXMAN_MEMBER_SIZE if r['member_basename']==PIXMAN_MEMBER else int(r['member_size'])
  b=bind_by[r['member_basename']];m=regular_by[r['member_basename']]
  object_receipts.append({'provider_object_id':b['provider_object_id'],'composition_row_id':r['composition_row_id'],'provider_review_id':r['provider_review_id'],'member_basename':r['member_basename'],'expected_sha256':r['member_sha256'],'expected_size_bytes':size,'expected_soname':b['soname'],'target_relative_path':m['target_relative_path'],'verification_fields':{'actual_sha256':'0'*64,'actual_size_bytes':size,'elf_class':'ELF64','elf_machine':'AArch64','elf_type':'DYN','actual_soname':b['soname'],'needed':[],'rpath':None,'runpath':None,'loader_resolutions':[],'verification_state':'PENDING_RUNTIME_MATERIALIZATION'}})
 alias_receipts=[]
 for r in sorted(aliases,key=lambda x:x['alias_relative_path']):
  alias_receipts.append({'alias_target_record_id':r['alias_target_record_id'],'alias_relative_path':r['alias_relative_path'],'concrete_target_record_id':r['concrete_target_record_id'],'concrete_relative_path':r['concrete_relative_path'],'alias_class':r['alias_class'],'verification_state':'PENDING_RUNTIME_MATERIALIZATION'})
 prototype={'schema_version':1,'receipt_schema_id':'SELECTED-TARGET-GENERATION-RECEIPT-001','composition_acceptance_id':'SELECTED-COMPOSITION-ACCEPT-001','target_manifest_acceptance_id':'SELECTED-TARGET-MANIFEST-ACCEPT-001','generation_contract_review_id':'RETAINED-SUPPLY-COORDINATE-GENERATION-CONTRACT-001','object_count':41,'alias_count':41,'collision_count':0,'objects':object_receipts,'aliases':alias_receipts,'publication_fields':{'generation_id':'sha256:'+'0'*64,'transaction_id':'0'*32,'staging_device_id':0,'generation_device_id':0,'selector_parent_device_id':0,'tree_fsync_complete':False,'parent_fsync_complete':False,'publication_rename_complete':False,'selector_rename_complete':False,'result_index_sha256':'0'*64},'authority_boundary':'PROTOTYPE_ONLY_NO_RECEIPT_GENERATION_ROOT_CREATION_COPY_POPULATION_PUBLICATION_OR_ACTIVATION'}
 proto_bytes=(json.dumps(prototype,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode()
 reservation=max(RECEIPT_FLOOR,next_pow2(len(proto_bytes)))
 if len(proto_bytes)>reservation:raise SystemExit('prototype exceeds reservation')
 final_budget=max(16*1024*1024,2*total+reservation)
 evidence=[{'review_id':'PIXMAN-SIZE-RESOURCE-INTERVENTION-001','provider_review_id':'PIXMAN-CAIRO-PREQ-PROV-001','result_remote':PIXMAN_RESULT_REMOTE,'drive_file_id':PIXMAN_FILE_ID,'result_sha256':PIXMAN_RESULT_SHA,'archive_member_path':PIXMAN_ARCHIVE_MEMBER,'member_basename':PIXMAN_MEMBER,'member_sha256':PIXMAN_MEMBER_SHA,'member_size':str(PIXMAN_MEMBER_SIZE),'size_source':f'TAR_REGULAR_MEMBER_METADATA_AND_{PIXMAN_SHA_EVIDENCE}','verification_state':'EXACT_RESULT_OUTER_SHA_MEMBER_PATH_SIZE_AND_MEMBER_SHA_TEXT_EVIDENCE_QUALIFIED','authority_effect':'READ_ONLY_SIZE_AND_RESOURCE_BUDGET_EVIDENCE_ONLY_NO_PROVIDER_ACQUISITION_EXTRACTION_TARGET_WRITE_OR_POPULATION','prohibited_inference':'HISTORICAL_RESULT_EVIDENCE_DOES_NOT_AUTHORIZE_REUSING_OR_EXTRACTING_EMBEDDED_PROVIDER_BYTES'}]
 gates=[
 ('INTLIFT-001','TARGET_POLICY','SATISFIED','SATISFIED_FOR_READ_ONLY_MATERIALIZER_DESIGN_REVIEW','selected-target-manifest-boundary-acceptance.tsv','REVERIFY_82_ROWS_AND_ZERO_COLLISIONS'),
 ('INTLIFT-002','ALIAS_RESOLUTION','SATISFIED','SATISFIED_FOR_READ_ONLY_MATERIALIZER_DESIGN_REVIEW','selected-target-manifest-alias-bindings.tsv','REVERIFY_41_RELATIVE_ALIAS_TARGETS'),
 ('INTLIFT-003','ATOMIC_FAMILIES','SATISFIED','SATISFIED_FOR_READ_ONLY_MATERIALIZER_DESIGN_REVIEW','selected-provider-composition-members.tsv','REVERIFY_ATSPI2_CAIRO_PANGO_GDK_GTK_FAMILY_COMPLETENESS'),
 ('INTLIFT-004','SUPPLY_BINDINGS_AND_SIZES','SATISFIED','SATISFIED_FOR_READ_ONLY_MATERIALIZER_DESIGN_REVIEW','selected-target-indexed-replacement-review.tsv;selected-target-member-size-census.tsv;selected-target-pixman-size-evidence.tsv','REVERIFY_41_COORDINATE_INDEX_SHA_SIZE_BINDINGS_BEFORE_ANY_BYTE_READ'),
 ('INTLIFT-005','GENERATION_ROOT_CONTRACT','SATISFIED_CONTRACT_ONLY','SATISFIED_FOR_READ_ONLY_MATERIALIZER_DESIGN_REVIEW','GEN-001;GEN-002','RUNTIME_VERIFY_ABSOLUTE_NON_SYMLINK_OWNER_MODE_AND_SAME_DEVICE_NO_ROOT_CREATION_NOW'),
 ('INTLIFT-006','ATOMIC_PUBLICATION_CONTRACT','SATISFIED_CONTRACT_ONLY','SATISFIED_FOR_READ_ONLY_MATERIALIZER_DESIGN_REVIEW','GEN-003','RUNTIME_VERIFY_FSYNCS_AND_RENAMES_NO_PUBLICATION_NOW'),
 ('INTLIFT-007','RESOURCE_BUDGET','SATISFIED_POLICY_RESERVATION','SATISFIED_FOR_READ_ONLY_MATERIALIZER_DESIGN_REVIEW','selected-target-resource-budget-metadata.tsv','RUNTIME_VERIFY_STATVFS_FREE_BYTES_AT_LEAST_FINAL_BUDGET'),
 ('INTLIFT-008','VERIFICATION_RECEIPT','SATISFIED_SCHEMA_AND_CAP','SATISFIED_FOR_READ_ONLY_MATERIALIZER_DESIGN_REVIEW','selected-target-verification-receipt-prototype.json;GEN-005','ABORT_BEFORE_PUBLICATION_IF_CANONICAL_RECEIPT_EXCEEDS_RESERVATION'),
 ('INTLIFT-009','ROLLBACK_SELECTOR','SATISFIED_CONTRACT_ONLY','SATISFIED_FOR_READ_ONLY_MATERIALIZER_DESIGN_REVIEW','GEN-006','RUNTIME_VERIFY_COMPLETE_PRIOR_GENERATION_NO_SELECTOR_CHANGE_NOW'),
 ('INTLIFT-010','FAILURE_CLEANUP_OBSERVABILITY','SATISFIED_CONTRACT_ONLY','SATISFIED_FOR_READ_ONLY_MATERIALIZER_DESIGN_REVIEW','GEN-007','RUNTIME_VERIFY_TRANSACTION_SCOPING_AND_FAILURE_RECEIPT_NO_CLEANUP_NOW')]
 grows=[]
 for i,c,e,r,ref,pre in gates:grows.append({'prerequisite_id':i,'category':c,'evidence_state':e,'review_result':r,'evidence_reference':ref,'remaining_runtime_preflight':pre,'authority_effect':'CONDITIONALLY_LIFTS_INTERVENTION_FOR_READ_ONLY_MATERIALIZER_DESIGN_REVIEW_ONLY','prohibited_inference':'DOES_NOT_AUTHORIZE_BYTE_ACQUISITION_EXTRACTION_ROOT_CREATION_TARGET_WRITE_POPULATION_MATERIALIZATION_PUBLICATION_DEPLOYMENT_OR_ACTIVATION'})
 meta=[
 {'key':'schema_version','value':'1'},{'key':'review_id','value':'PIXMAN-SIZE-RESOURCE-INTERVENTION-001'},{'key':'decision','value':'INTERVENTION_CONDITIONALLY_LIFTED_FOR_READ_ONLY_MATERIALIZER_DESIGN_REVIEW_ONLY'},
 {'key':'pixman_result_sha256','value':PIXMAN_RESULT_SHA},{'key':'pixman_member_sha256','value':PIXMAN_MEMBER_SHA},{'key':'pixman_member_size_bytes','value':str(PIXMAN_MEMBER_SIZE)},
 {'key':'exact_member_size_count','value':'41'},{'key':'open_member_size_count','value':'0'},{'key':'exact_member_bytes','value':str(total)},
 {'key':'receipt_prototype_sha256','value':hashlib.sha256(proto_bytes).hexdigest()},{'key':'receipt_prototype_bytes','value':str(len(proto_bytes))},{'key':'receipt_reservation_rule','value':'MAX_1048576_NEXT_POWER_OF_TWO_CANONICAL_PROTOTYPE_BYTES'},{'key':'receipt_overhead_budget_bytes','value':str(reservation)},{'key':'receipt_headroom_bytes','value':str(reservation-len(proto_bytes))},{'key':'receipt_overflow_policy','value':'ABORT_BEFORE_GENERATION_PUBLICATION'},
 {'key':'member_100_percent_margin_bytes','value':str(2*total)},{'key':'minimum_floor_bytes','value':str(16*1024*1024)},{'key':'final_resource_preflight_bytes','value':str(final_budget)},
 {'key':'prerequisite_count','value':'10'},{'key':'design_review_satisfied_count','value':'10'},{'key':'intervention_state','value':'CONDITIONALLY_LIFTED_FOR_READ_ONLY_MATERIALIZER_DESIGN_REVIEW_ONLY'},
 {'key':'materializer_design_authorized','value':'YES_READ_ONLY_DESIGN_REVIEW_ONLY'},{'key':'target_population_authorized','value':'NO'},{'key':'byte_acquisition_authorized','value':'NO'},{'key':'generation_root_creation_authorized','value':'NO'},{'key':'materialization_authorized','value':'NO'},{'key':'publication_authorized','value':'NO'},{'key':'deployment_authorized','value':'NO'},{'key':'activation_authorized','value':'NO'},
 {'key':'next_action','value':'design-read-only-selected-provider-materializer-and-runtime-preflight-contract'},{'key':'authority_effect','value':'READ_ONLY_MATERIALIZER_DESIGN_REVIEW_GATE_OPEN_ONLY_NO_RUNTIME_OR_FILESYSTEM_AUTHORITY'}]
 base=out/'experiments/glibc/selected-obsidian-provider-authority/review'
 write(base/'selected-target-pixman-size-evidence.tsv',EVIDENCE_FIELDS,evidence)
 (base/'selected-target-verification-receipt-prototype.json').write_bytes(proto_bytes)
 write(base/'selected-target-population-intervention-lift-review.tsv',GATE_FIELDS,grows)
 write(base/'selected-target-resource-budget-metadata.tsv',['key','value'],meta)
if __name__=='__main__':main()
