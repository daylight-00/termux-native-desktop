#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib
from pathlib import Path

INDEX_FIELDS=['binding_row_id','provider_review_id','artifact_package','member_basename','member_sha256','prior_coordinate_state','closure_kind','replacement_result_remote','replacement_drive_file_id','replacement_result_sha256','replacement_result_index_sha256','artifact_evidence_path','member_evidence_path','status_surface_boundary','coordinate_state','index_state','remaining_blocker_ids','authority_effect','prohibited_inference']
SIZE_FIELDS=['composition_row_id','provider_review_id','artifact_package','member_basename','member_sha256','member_size','size_state','size_source_kind','size_source_ref','size_source_member_path','resource_budget_state','authority_effect']
META_FIELDS=['key','value']
V101_REMOTE='gdrive:ChatGPT-Agent-Exchange/termux-native-desktop/user-results/termux-native-desktop-gtk3-v101-elf-validation-pipefail-boundary-20260725T172756Z-results.tar.zst'
V101_FILE_ID='1ST696OLuGiBt_lLvJbXOt6EIT0X17Fy9'
V101_SHA='ba0fa0e31cfea2a31f8065ecaccf998a49901c12aa5f62af978728ddd8f10b3a'
V101_INDEX_SHA='9b360f096afd8c464400a211feedc9ab20146b504415658c7a44c04cf6f026a0'
FREETYPE_REMOTE='gdrive:ChatGPT-Agent-Exchange/termux-native-desktop/termux-native-desktop-freetype-bounded-provider-authority-20260717T114408Z/termux-native-desktop-freetype-bounded-provider-authority-20260717T114408Z-results.tar.zst'
FREETYPE_FILE_ID='1t8tH6GqfGFe2kOVE5_nwLiUhoUp5E1iy'
FREETYPE_SHA='1d144d407e856a122135ab5ecbc8caebf8196037087fb15821c591a69a850073'
FREETYPE_RECEIPT_SHA='eed95221332a7dd309788b72e651ccb7c40ca91ffe6f7f3ea231433804b787f7'
FREETYPE_TRANSITIVE={'FREETYPE-TRANSITIVE-BROTLI-COMMON-001','FREETYPE-TRANSITIVE-BROTLI-DEC-001','FREETYPE-TRANSITIVE-LIBBZ2-001','FREETYPE-TRANSITIVE-ZLIB-001'}
PACKAGE_PATHS={'libcairo.so.2.11802.2': 'candidate/private-gtk-dependency-packages/libcairo-glibc_1.18.2_aarch64.deb', 'libcairo-gobject.so.2.11802.2': 'candidate/private-gtk-dependency-packages/libcairo-glibc_1.18.2_aarch64.deb', 'libfontconfig.so.1.14.0': 'candidate/private-gtk-dependency-packages/fontconfig-glibc_2.15.0-1_aarch64.deb', 'libfreetype.so.6.20.2': 'candidate/private-gtk-dependency-packages/freetype-glibc_2.13.3_aarch64.deb', 'libfribidi.so.0.4.0': 'candidate/private-pango-dependency-packages/fribidi-glibc_1.0.16_aarch64.deb', 'libglib-2.0.so.0.8200.2': 'candidate/private-dependency-packages/glib-glibc_2.82.2-2_aarch64.deb', 'libgobject-2.0.so.0.8200.2': 'candidate/private-dependency-packages/glib-glibc_2.82.2-2_aarch64.deb', 'libgmodule-2.0.so.0.8200.2': 'candidate/private-dependency-packages/glib-glibc_2.82.2-2_aarch64.deb', 'libgio-2.0.so.0.8200.2': 'candidate/private-dependency-packages/glib-glibc_2.82.2-2_aarch64.deb', 'libpng16.so.16.47.0': 'candidate/private-dependency-packages/libpng-glibc_1.6.47_aarch64.deb', 'libmount.so.1.1.0': 'candidate/private-dependency-packages/libmount-glibc_2.40.2-1_aarch64.deb', 'libgraphite2.so.3.2.1': 'candidate/private-pango-dependency-packages/libgraphite-glibc_1.3.14_aarch64.deb', 'libgdk-3.so.0.2417.32': 'candidate/gtk3-glibc_3.24.49_aarch64.deb', 'libgtk-3.so.0.2417.32': 'candidate/gtk3-glibc_3.24.49_aarch64.deb', 'libharfbuzz.so.0.61010.0': 'candidate/private-pango-dependency-packages/harfbuzz-glibc_10.1.0_aarch64.deb', 'libcloudproviders.so.0.3.6': 'candidate/private-gtk-active-dependency-packages/libcloudproviders-glibc_0.3.6_aarch64.deb', 'libdatrie.so.1.4.0': 'candidate/private-pango-dependency-packages/libdatrie-glibc_0.2.13_aarch64.deb', 'libepoxy.so.0.0.0': 'candidate/private-epoxy-dependency-packages/libepoxy-glibc_1.5.10_aarch64.deb', 'libiconv.so.2.7.0': 'candidate/private-pango-dependency-packages/libiconv-glibc_1.18_aarch64.deb', 'libthai.so.0.3.1': 'candidate/private-pango-dependency-packages/libthai-glibc_0.1.29_aarch64.deb', 'libXcursor.so.1.0.2': 'candidate/private-gtk-active-dependency-packages/libxcursor-glibc_1.2.3_aarch64.deb', 'libxkbcommon.so.0.8.0': 'candidate/private-xkbcommon-dependency-packages/libxkbcommon-glibc_1.8.0_aarch64.deb', 'libpango-1.0.so.0.5400.0': 'candidate/private-pango-dependency-packages/pango-glibc_1.54.0_aarch64.deb', 'libpangoft2-1.0.so.0.5400.0': 'candidate/private-pango-dependency-packages/pango-glibc_1.54.0_aarch64.deb', 'libpangocairo-1.0.so.0.5400.0': 'candidate/private-pango-dependency-packages/pango-glibc_1.54.0_aarch64.deb', 'libXfixes.so.3.1.0': 'candidate/private-gtk-active-dependency-packages/libxfixes-glibc_6.0.1_aarch64.deb', 'libXcomposite.so.1.0.0': 'candidate/private-gtk-active-dependency-packages/libxcomposite-glibc_0.4.6_aarch64.deb', 'libXi.so.6.1.0': 'candidate/private-gtk-active-dependency-packages/libxi-glibc_1.8.2_aarch64.deb', 'libXinerama.so.1.0.0': 'candidate/private-gtk-active-dependency-packages/libxinerama-glibc_1.1.5_aarch64.deb'}

def read(p):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,fields,rows):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[4]);ap.add_argument('--output-root',type=Path);a=ap.parse_args()
 root=a.repo_root.resolve();out=(a.output_root or root).resolve();rv=root/'experiments/glibc/selected-obsidian-provider-authority/review';pf=root/'experiments/glibc/selected-obsidian-provider-authority/profiles'
 prior=read(rv/'selected-target-retained-result-coordinate-review.tsv');supply={r['binding_row_id']:r for r in read(rv/'selected-target-supply-byte-binding-review.tsv')};sizes=read(pf/'selected-target-member-size-evidence.tsv');size_by={r['provider_review_id']+'|'+r['member_basename']:r for r in sizes}
 if len(prior)!=41 or len(sizes)!=41:raise SystemExit('expected 41 rows')
 freetype_index=pf/'freetype-legacy-result-file-index.tsv'
 if hashlib.sha256(freetype_index.read_bytes()).hexdigest()!=FREETYPE_RECEIPT_SHA:raise SystemExit('freetype append-only receipt drift')
 irows=[]
 for r in prior:
  key=r['provider_review_id']+'|'+r['member_basename'];sr=size_by[key];old=supply[r['binding_row_id']]
  if old['binding_state']=='QUALIFIED_READ_ONLY_BINDING_INPUT':
   kind='EXISTING_DIGEST_BOUND_UNCHANGED';remote='sha256:'+old['retained_result_sha256'];fid='-';rsha=old['retained_result_sha256'];isha='EXISTING_AUTHORITY_DIGEST';artifact='EXISTING_AUTHORITY_RECORD';member=old['archive_member_path'];status='EXISTING_AUTHORITY_STATUS_RETAINED';coord='CLOSED';idx='CLOSED_EXISTING_DIGEST_BOUND'
  elif r['provider_review_id'] in FREETYPE_TRANSITIVE:
   kind='APPEND_ONLY_LEGACY_INDEX_UPGRADE';remote=FREETYPE_REMOTE;fid=FREETYPE_FILE_ID;rsha=FREETYPE_SHA;isha=FREETYPE_RECEIPT_SHA;artifact='profiles/freetype-legacy-result-file-index.tsv';member=sr['size_source_member_path'];status='LEGACY_TRANSACTION_RC_0_EXTERNAL_APPEND_ONLY_INDEX_RECEIPT';coord='CLOSED';idx='CLOSED_APPEND_ONLY_RECEIPT'
  else:
   kind='V101_INDEXED_REPLACEMENT';remote=V101_REMOTE;fid=V101_FILE_ID;rsha=V101_SHA;isha=V101_INDEX_SHA;artifact=PACKAGE_PATHS[r['member_basename']];member=sr['size_source_member_path'];status='CORE_TRANSACTION_RC_0_SUCCESS_ACTION_FAILURE_NONE_OUTER_TRANSACTION_RC_1_STATUS_SURFACE_DEFECT_RECORDED';coord='CLOSED';idx='CLOSED_INDEXED_REPLACEMENT'
  irows.append({'binding_row_id':r['binding_row_id'],'provider_review_id':r['provider_review_id'],'artifact_package':r['artifact_package'],'member_basename':r['member_basename'],'member_sha256':r['member_sha256'],'prior_coordinate_state':r['coordinate_review_state'],'closure_kind':kind,'replacement_result_remote':remote,'replacement_drive_file_id':fid,'replacement_result_sha256':rsha,'replacement_result_index_sha256':isha,'artifact_evidence_path':artifact,'member_evidence_path':member,'status_surface_boundary':status,'coordinate_state':coord,'index_state':idx,'remaining_blocker_ids':'-' if sr['size_state']=='EXACT' else 'EXACT-MEMBER-SIZE-OPEN;RESOURCE-BUDGET-OPEN;INTERVENTION-LIFT-OPEN','authority_effect':'READ_ONLY_INDEXED_SUPPLY_EVIDENCE_ONLY_NO_ACQUISITION_EXTRACTION_COPY_POPULATION_OR_MATERIALIZATION','prohibited_inference':'INDEX_OR_COORDINATE_CLOSURE_DOES_NOT_AUTHORIZE_PROVIDER_BYTE_DOWNLOAD_EXTRACTION_INSTALL_TARGET_WRITE_POPULATION_DEPLOYMENT_OR_ACTIVATION'})
 exact=[r for r in sizes if r['size_state']=='EXACT'];openrows=[r for r in sizes if r['size_state']!='EXACT'];known=sum(int(r['member_size']) for r in exact)
 if len(exact)!=40 or len(openrows)!=1 or openrows[0]['provider_review_id']!='PIXMAN-CAIRO-PREQ-PROV-001' or known!=28586192:raise SystemExit((len(exact),openrows,known))
 srows=[]
 for r in sizes:
  x=dict(r);x['resource_budget_state']='COUNTED_EXACT' if r['size_state']=='EXACT' else 'BLOCKED_EXACT_SIZE_REQUIRED';x['authority_effect']='READ_ONLY_SIZE_EVIDENCE_ONLY_NO_BYTE_ACQUISITION_OR_TARGET_WRITE';srows.append(x)
 meta=[
 {'key':'schema_version','value':'1'},{'key':'review_id','value':'INDEXED-REPLACEMENT-MEMBER-SIZE-REVIEW-001'},{'key':'decision','value':'INTERVENTION_RETAINED_ALL_COORDINATE_AND_INDEX_GAPS_CLOSED_ONE_MEMBER_SIZE_OPEN'},
 {'key':'concrete_object_count','value':'41'},{'key':'existing_digest_bound_count','value':'14'},{'key':'v101_indexed_replacement_count','value':'23'},{'key':'append_only_legacy_index_upgrade_count','value':'4'},{'key':'remaining_coordinate_gap_count','value':'0'},{'key':'remaining_result_index_gap_count','value':'0'},
 {'key':'exact_member_size_count','value':'40'},{'key':'open_member_size_count','value':'1'},{'key':'open_member_size_provider','value':'PIXMAN-CAIRO-PREQ-PROV-001'},{'key':'known_exact_member_bytes','value':'28586192'},{'key':'known_100_percent_margin_lower_bound_bytes','value':'57172384'},{'key':'receipt_overhead_state','value':'NOT_YET_CENSUSED'},{'key':'final_resource_budget_state','value':'BLOCKED_ONE_MEMBER_SIZE_AND_RECEIPT_OVERHEAD_OPEN'},
 {'key':'intervention_state','value':'RETAINED'},{'key':'population_authorized','value':'NO'},{'key':'materializer_design_authorized','value':'NO'},{'key':'byte_acquisition_authorized','value':'NO'},{'key':'generation_root_creation_authorized','value':'NO'},
 {'key':'next_action','value':'close-exact-pixman-member-size-and-review-population-intervention-lift-gate'},{'key':'authority_effect','value':'READ_ONLY_INDEX_AND_SIZE_REVIEW_ONLY_NO_ACQUISITION_EXTRACTION_COPY_POPULATION_MATERIALIZATION_DEPLOYMENT_OR_ACTIVATION'}]
 dest=out/'experiments/glibc/selected-obsidian-provider-authority/review';write(dest/'selected-target-indexed-replacement-review.tsv',INDEX_FIELDS,irows);write(dest/'selected-target-member-size-census.tsv',SIZE_FIELDS,srows);write(dest/'selected-target-index-size-review-metadata.tsv',META_FIELDS,meta);shutil_src=freetype_index;target=dest/'freetype-legacy-result-index-upgrade.tsv';target.write_bytes(shutil_src.read_bytes())
if __name__=='__main__':main()
