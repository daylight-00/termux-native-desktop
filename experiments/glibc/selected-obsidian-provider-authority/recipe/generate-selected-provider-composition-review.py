#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv
from pathlib import Path

R=Path('experiments/glibc/selected-obsidian-provider-authority/review')
MEM=R/'selected-provider-composition-members.tsv'
GAPS=R/'selected-provider-composition-gaps.tsv'
META=R/'selected-provider-composition-metadata.tsv'

MEM_FIELDS=['composition_row_id','provider_review_id','recipe_root','artifact_package','artifact_version','member_basename','member_sha256','soname','alias_basename','alias_target_basename','capability_scope','composition_inclusion','inclusion_reason','collision_state','update_boundary','rollback_boundary','authority_effect','prohibited_inference']
GAP_FIELDS=['composition_gap_id','selected_evidence_row_id','identity_label','lookup_name','soname','package_or_source','version','root_mapping','gap_class','priority_tranche','blocker_reason','minimum_next_action','authority_effect']

def read(p):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,fields,rows):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def bn(p):return p.rsplit('/',1)[-1]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path.cwd());ap.add_argument('--output-root',type=Path);a=ap.parse_args()
 repo=a.repo_root.resolve();out=(a.output_root.resolve() if a.output_root else repo)
 review=repo/R
 rows=[]
 # X.Org
 for x in read(review/'xorg-reference-consumed-provider-authority.tsv'):
  member=bn(x['exact_member_path']);soname=x['observed_soname']
  rows.append(dict(composition_row_id=f"COMP-{x['review_id']}",provider_review_id=x['review_id'],recipe_root=x['recipe_root'],artifact_package=x['artifact_package'],artifact_version=x['artifact_version'],member_basename=member,member_sha256=x['exact_member_sha256'],soname=soname,alias_basename=soname,alias_target_basename=member,capability_scope=x['capability_scope'],composition_inclusion='INCLUDED_SELECTED_GTK_SCOPE',inclusion_reason='EXACT_SELECTED_GTK_X11_PROVIDER_DECISION',collision_state='NO_ACCEPTED_MEMBER_OR_ALIAS_COLLISION',update_boundary=x['update_boundary'],rollback_boundary=x['rollback_boundary'],authority_effect='MEMBER_AND_SONAME_ALIAS_PROPOSED_ONLY_NO_TARGET_POPULATION',prohibited_inference=x['prohibited_inference']))
 # libtasn1 accepted but not selected in this GTK composition
 x=read(review/'libtasn1-reference-consumed-provider-authority.tsv')[0];member=bn(x['exact_member_path']);soname=x['observed_soname']
 rows.append(dict(composition_row_id='COMP-LIBTASN1-PROV-001',provider_review_id=x['review_id'],recipe_root=x['recipe_root'],artifact_package=x['artifact_package'],artifact_version=x['artifact_version'],member_basename=member,member_sha256=x['exact_member_sha256'],soname=soname,alias_basename=soname,alias_target_basename=member,capability_scope=x['capability_scope'],composition_inclusion='DEFERRED_PROFILE_REQUIREMENT_OPEN',inclusion_reason='BOUNDED_PROVIDER_ACCEPTED_BUT_GNUTLS_SECURITY_OR_PRINTING_PROFILE_NOT_SELECTED_FOR_CURRENT_GTK_SCOPE',collision_state='NO_ACCEPTED_MEMBER_OR_ALIAS_COLLISION',update_boundary=x['update_boundary'],rollback_boundary=x['rollback_boundary'],authority_effect='ACCEPTED_PROVIDER_RETAINED_OUTSIDE_CURRENT_COMPOSITION_NO_TARGET_POPULATION',prohibited_inference=x['prohibited_inference']))
 # libepoxy
 x=read(review/'libepoxy-reference-consumed-provider-authority.tsv')[0];member=bn(x['exact_member_path']);soname=x['observed_soname']
 rows.append(dict(composition_row_id='COMP-LIBEPOXY-PROV-001',provider_review_id=x['review_id'],recipe_root=x['recipe_root'],artifact_package=x['artifact_package'],artifact_version=x['artifact_version'],member_basename=member,member_sha256=x['exact_member_sha256'],soname=soname,alias_basename=soname,alias_target_basename=member,capability_scope=x['consumer_scope'],composition_inclusion='INCLUDED_SELECTED_GTK_SCOPE',inclusion_reason='EXACT_SELECTED_GTK_X11_GLX_DISPATCH_PROVIDER_DECISION',collision_state='NO_ACCEPTED_MEMBER_OR_ALIAS_COLLISION',update_boundary=x['update_boundary'],rollback_boundary=x['rollback_boundary'],authority_effect='MEMBER_AND_SONAME_ALIAS_PROPOSED_ONLY_NO_TARGET_POPULATION',prohibited_inference=x['prohibited_inference']))
 # Pango family
 x=read(review/'pango-reference-consumed-provider-authority.tsv')[0]
 paths=x['exact_member_paths'].split(';');shas=x['exact_member_sha256s'].split(';');sons=x['observed_sonames'].split(';');aliases=x['observed_alias_paths'].split(';');targets=x['observed_alias_targets'].split(';')
 for i,(p,s,so,al,tgt) in enumerate(zip(paths,shas,sons,aliases,targets),1):
  rows.append(dict(composition_row_id=f'COMP-PANGO-PROV-001-{i}',provider_review_id=x['review_id'],recipe_root=x['recipe_root'],artifact_package=x['artifact_package'],artifact_version=x['artifact_version'],member_basename=bn(p),member_sha256=s,soname=so,alias_basename=bn(al),alias_target_basename=bn(tgt),capability_scope=x['capability_scope'],composition_inclusion='INCLUDED_SELECTED_GTK_SCOPE',inclusion_reason='ATOMIC_THREE_MEMBER_PANGO_PROVIDER_FAMILY',collision_state='NO_ACCEPTED_MEMBER_OR_ALIAS_COLLISION',update_boundary=x['update_boundary'],rollback_boundary=x['rollback_boundary'],authority_effect='MEMBER_AND_SONAME_ALIAS_PROPOSED_ONLY_NO_TARGET_POPULATION',prohibited_inference=x['prohibited_inference']))
 # libjpeg
 x=read(review/'libjpeg-so-62-loader-isolated-provider-authority.tsv')[0];member=x['candidate_member'];soname=x['observed_soname']
 rows.append(dict(composition_row_id='COMP-LIBJPEG-PROV-001',provider_review_id=x['review_id'],recipe_root=x['recipe_root'],artifact_package='project-libjpeg-turbo-v6b',artifact_version='3.1.0',member_basename=member,member_sha256=x['candidate_sha256'],soname=soname,alias_basename=soname,alias_target_basename=member,capability_scope=x['capability_scope'],composition_inclusion='INCLUDED_SELECTED_GTK_SCOPE',inclusion_reason='EXACT_GDKPIXBUF_JPEG_FILE_AND_MEMORY_DECODE_PROVIDER_DECISION',collision_state='NO_ACCEPTED_MEMBER_OR_ALIAS_COLLISION_LIBJPEG_SO_8_FAMILY_EXCLUDED',update_boundary=x['update_boundary'],rollback_boundary=x['rollback_boundary'],authority_effect='MEMBER_AND_SONAME_ALIAS_PROPOSED_ONLY_NO_TARGET_POPULATION',prohibited_inference=x['prohibited_inference']))
 # project-built GdkPixbuf
 x=read(review/'gdkpixbuf-2-42-12-provider-candidate-result-review.tsv')[0];member=x['candidate_member'];soname=x['observed_soname']
 rows.append(dict(composition_row_id='COMP-GDKPIXBUF-PROV-001',provider_review_id=x['review_id'],recipe_root='project/upstream-gdk-pixbuf',artifact_package='project-gdk-pixbuf',artifact_version=x['source_version'],member_basename=member,member_sha256=x['candidate_sha256'],soname=soname,alias_basename=soname,alias_target_basename=member,capability_scope=x['capability_scope'],composition_inclusion='INCLUDED_SELECTED_GTK_SCOPE',inclusion_reason='EXACT_FIXED_JPEG_AND_PNG_FILE_AND_MEMORY_DECODE_PROVIDER_DECISION',collision_state='NO_ACCEPTED_MEMBER_OR_ALIAS_COLLISION_DEBIAN_ORACLE_EXCLUDED',update_boundary=x['update_boundary'],rollback_boundary=x['rollback_boundary'],authority_effect='MEMBER_AND_SONAME_ALIAS_PROPOSED_ONLY_NO_TARGET_POPULATION',prohibited_inference=x['prohibited_inference']))
 # exact GDK Pixbuf reference dependency providers: GLib four-member family and libpng
 for x in read(review/'gdkpixbuf-reference-dependency-provider-authority.tsv'):
  paths=x['exact_member_paths'].split(';');shas=x['exact_member_sha256s'].split(';');sons=x['observed_sonames'].split(';');aliases=x['observed_alias_paths'].split(';');targets=x['observed_alias_targets'].split(';')
  if not (len(paths)==len(shas)==len(sons)==len(aliases)==len(targets)):
   raise SystemExit(f"reference dependency member list length mismatch for {x['review_id']}")
  for i,(member_path,member_sha,soname,alias,target) in enumerate(zip(paths,shas,sons,aliases,targets),1):
   rows.append(dict(composition_row_id=f"COMP-{x['review_id']}-{i}",provider_review_id=x['review_id'],recipe_root=x['recipe_root'],artifact_package=x['artifact_package'],artifact_version=x['artifact_version'],member_basename=bn(member_path),member_sha256=member_sha,soname=soname,alias_basename=bn(alias),alias_target_basename=bn(target),capability_scope=x['capability_scope'],composition_inclusion='INCLUDED_SELECTED_GTK_SCOPE',inclusion_reason='EXACT_GDKPIXBUF_REFERENCE_DEPENDENCY_PROVIDER_DECISION',collision_state='NO_ACCEPTED_MEMBER_OR_ALIAS_COLLISION_ORACLE_CONCRETE_SUFFIX_EXCLUDED',update_boundary=x['update_boundary'],rollback_boundary=x['rollback_boundary'],authority_effect='MEMBER_AND_SONAME_ALIAS_PROPOSED_ONLY_NO_TARGET_POPULATION',prohibited_inference=x['prohibited_inference']))
 # exact GDK Pixbuf util-linux transitive provider pair
 x=read(review/'gdkpixbuf-exact-util-linux-provider-authority.tsv')[0]
 paths=x['exact_member_paths'].split(';');shas=x['exact_member_sha256s'].split(';');sons=x['observed_sonames'].split(';');aliases=x['observed_alias_paths'].split(';');targets=x['observed_alias_targets'].split(';');packages=x['artifact_packages'].split(';');versions=x['artifact_versions'].split(';')
 if not (len(paths)==len(shas)==len(sons)==len(aliases)==len(targets)==len(packages)==len(versions)==2):
  raise SystemExit('util-linux accepted member list length mismatch')
 for i,(member_path,member_sha,soname,alias,target,pkg,ver) in enumerate(zip(paths,shas,sons,aliases,targets,packages,versions),1):
  inclusion=('INCLUDED_SELECTED_GTK_SCOPE' if soname=='libmount.so.1' else 'INCLUDED_TRANSITIVE_GDKPIXBUF_SCOPE')
  reason=('EXACT_SELECTED_GTK_GIO_LIBMOUNT_PROVIDER_DECISION' if soname=='libmount.so.1' else 'EXACT_LIBMOUNT_TRANSITIVE_LIBBLKID_PROVIDER_DECISION')
  rows.append(dict(composition_row_id=f"COMP-{x['review_id']}-{i}",provider_review_id=x['review_id'],recipe_root=x['recipe_root'],artifact_package=pkg,artifact_version=ver,member_basename=bn(member_path),member_sha256=member_sha,soname=soname,alias_basename=bn(alias),alias_target_basename=bn(target),capability_scope=x['capability_scope'],composition_inclusion=inclusion,inclusion_reason=reason,collision_state='NO_ACCEPTED_MEMBER_OR_ALIAS_COLLISION_SCRATCH_PAIR_EXCLUDED',update_boundary=x['update_boundary'],rollback_boundary=x['rollback_boundary'],authority_effect='MEMBER_AND_SONAME_ALIAS_PROPOSED_ONLY_NO_TARGET_POPULATION',prohibited_inference=x['prohibited_inference']))
 # exact libXcursor selected GTK X11 cursor provider
 x=read(review/'libxcursor-bounded-provider-authority.tsv')[0];member=bn(x['exact_member_path']);soname=x['observed_soname']
 rows.append(dict(composition_row_id='COMP-LIBXCURSOR-PROV-001',provider_review_id=x['review_id'],recipe_root=x['recipe_root'],artifact_package=x['artifact_package'],artifact_version=x['artifact_version'],member_basename=member,member_sha256=x['exact_member_sha256'],soname=soname,alias_basename=soname,alias_target_basename=member,capability_scope=x['consumer_scope'],composition_inclusion='INCLUDED_SELECTED_GTK_SCOPE',inclusion_reason='EXACT_SELECTED_GTK_X11_CURSOR_PROVIDER_DECISION',collision_state='NO_ACCEPTED_MEMBER_OR_ALIAS_COLLISION_STATIC_SIBLING_AND_DEBIAN_ORACLE_EXCLUDED',update_boundary=x['update_boundary'],rollback_boundary=x['rollback_boundary'],authority_effect='MEMBER_AND_SONAME_ALIAS_PROPOSED_ONLY_NO_TARGET_POPULATION',prohibited_inference=x['prohibited_inference']))
 # exact libthai and libdatrie selected GTK Thai break providers
 for x in read(review/'libthai-libdatrie-bounded-provider-authority.tsv'):
  member=bn(x['exact_member_path']);soname=x['observed_soname']
  reason=('EXACT_SELECTED_PANGO_THAI_BREAK_PROVIDER_AND_DICTIONARY_CONTENT_DECISION' if soname=='libthai.so.0' else 'EXACT_SELECTED_LIBTHAI_TRANSITIVE_TRIE_PROVIDER_DECISION')
  rows.append(dict(composition_row_id=f"COMP-{x['review_id']}",provider_review_id=x['review_id'],recipe_root=x['recipe_root'],artifact_package=x['artifact_package'],artifact_version=x['artifact_version'],member_basename=member,member_sha256=x['exact_member_sha256'],soname=soname,alias_basename=soname,alias_target_basename=member,capability_scope=x['consumer_scope'],composition_inclusion='INCLUDED_SELECTED_GTK_SCOPE',inclusion_reason=reason,collision_state='NO_ACCEPTED_MEMBER_OR_ALIAS_COLLISION_SIGNED_EXACT_CANDIDATE_ONLY',update_boundary=x['update_boundary'],rollback_boundary=x['rollback_boundary'],authority_effect='MEMBER_AND_SONAME_ALIAS_PROPOSED_ONLY_NO_TARGET_POPULATION',prohibited_inference=x['prohibited_inference']))
 # exact libiconv transitive Thai break provider outside the 28-root inventory
 x=read(review/'libiconv-transitive-provider-authority.tsv')[0];member=bn(x['exact_member_path']);soname=x['observed_soname']
 rows.append(dict(composition_row_id='COMP-LIBICONV-TRANSITIVE-PROV-001',provider_review_id=x['review_id'],recipe_root=x['recipe_root'],artifact_package=x['artifact_package'],artifact_version=x['artifact_version'],member_basename=member,member_sha256=x['exact_member_sha256'],soname=soname,alias_basename=soname,alias_target_basename=member,capability_scope=x['consumer_scope'],composition_inclusion='INCLUDED_TRANSITIVE_PANGO_THAI_SCOPE',inclusion_reason='EXACT_LIBTHAI_LIBDATRIE_ICONV_TRANSITIVE_PROVIDER_DECISION',collision_state='NO_ACCEPTED_MEMBER_OR_ALIAS_COLLISION_LIBCHARSET_CLI_AND_HEADERS_EXCLUDED',update_boundary=x['update_boundary'],rollback_boundary=x['rollback_boundary'],authority_effect='MEMBER_AND_SONAME_ALIAS_PROPOSED_ONLY_NO_TARGET_POPULATION',prohibited_inference=x['prohibited_inference']))
 # exact libcloudproviders selected GTK PlacesSidebar provider
 x=read(review/'libcloudproviders-bounded-provider-authority.tsv')[0];member=bn(x['exact_member_path']);soname=x['observed_soname']
 rows.append(dict(composition_row_id='COMP-LIBCLOUDPROVIDERS-PROV-001',provider_review_id=x['review_id'],recipe_root=x['recipe_root'],artifact_package=x['artifact_package'],artifact_version=x['artifact_version'],member_basename=member,member_sha256=x['exact_member_sha256'],soname=soname,alias_basename=soname,alias_target_basename=member,capability_scope=x['consumer_scope'],composition_inclusion='INCLUDED_SELECTED_GTK_SCOPE',inclusion_reason='EXACT_SELECTED_GTK_PLACES_SIDEBAR_CLOUD_PROVIDER_LIBRARY_DECISION',collision_state='NO_ACCEPTED_MEMBER_OR_ALIAS_COLLISION_SERVICES_ACCOUNTS_AND_DEBIAN_ORACLE_EXCLUDED',update_boundary=x['update_boundary'],rollback_boundary=x['rollback_boundary'],authority_effect='MEMBER_AND_SONAME_ALIAS_PROPOSED_ONLY_NO_TARGET_POPULATION',prohibited_inference=x['prohibited_inference']))
 # exact FriBidi selected Pango core bidi provider
 x=read(review/'fribidi-bounded-provider-authority.tsv')[0];member=bn(x['exact_member_path']);soname=x['observed_soname']
 rows.append(dict(composition_row_id='COMP-FRIBIDI-PROV-001',provider_review_id=x['review_id'],recipe_root=x['recipe_root'],artifact_package=x['artifact_package'],artifact_version=x['artifact_version'],member_basename=member,member_sha256=x['exact_member_sha256'],soname=soname,alias_basename=soname,alias_target_basename=member,capability_scope=x['consumer_scope'],composition_inclusion='INCLUDED_SELECTED_GTK_SCOPE',inclusion_reason='EXACT_SELECTED_PANGO_CORE_UNICODE_BIDI_PROVIDER_DECISION',collision_state='NO_ACCEPTED_MEMBER_OR_ALIAS_COLLISION_CLI_DEV_AND_DEBIAN_ORACLE_EXCLUDED',update_boundary=x['update_boundary'],rollback_boundary=x['rollback_boundary'],authority_effect='MEMBER_AND_SONAME_ALIAS_PROPOSED_ONLY_NO_TARGET_POPULATION',prohibited_inference=x['prohibited_inference']))
 rows.sort(key=lambda r:r['composition_row_id'])
 if len(rows)!=24:raise SystemExit(f'expected 24 accepted member rows, got {len(rows)}')
 if len({r['soname'] for r in rows})!=24:raise SystemExit('accepted SONAME collision')
 if len({r['alias_basename'] for r in rows})!=24:raise SystemExit('accepted alias collision')

 accepted_eids={'selected:0802b57eadc2dd33925a','selected:1ae5e5d5ff7893c87e25','selected:beb2bb532f0a84c2835f','selected:d73a4eb5d9d5ee688632','selected:a7e42baafca8ed4717e3','selected:325be465ce7f532f8ff1','selected:83bc985c49ec2d778e60','selected:b869b82b3c70ee88cb30','selected:26a520f7c61bdc61e17c','selected:b577593923c28a50a012','selected:1997bce83f1eb5ffef9a','selected:6052b6396205eed6dbb6','selected:6e7f73b2a1ff4758f39a','selected:d8dfbc099c8bd2072e3f','selected:4a768de6fd1891617456','selected:ff6dae6f57afefe0d2b1','selected:e57423d1cb58b1b78ba4','selected:fec77ea4c45ec1a2990d','selected:5909031aa9e67d50214b','selected:b912b41387c558b52895','selected:5d210dfa49b6cf4c1077'}
 root_map={
  'libcairo-gobject.so.2.11804.4':'gpkg/libcairo','libcairo.so.2.11804.4':'gpkg/libcairo','libcloudproviders.so.0.3.6':'gpkg/libcloudproviders','libdatrie.so.1.4.0':'gpkg/libdatrie','libfontconfig.so.1.12.1':'gpkg/fontconfig','libfreetype.so.6.20.2':'gpkg/freetype','libfribidi.so.0.4.0':'gpkg/fribidi','libgio-2.0.so.0.8400.4':'gpkg/glib','libglib-2.0.so.0.8400.4':'gpkg/glib','libgmodule-2.0.so.0.8400.4':'gpkg/glib','libgobject-2.0.so.0.8400.4':'gpkg/glib','libharfbuzz.so.0.61020.0':'gpkg/harfbuzz','libmount.so.1.1.0':'gpkg/util-linux','libpng16.so.16.48.0':'gpkg/libpng','libthai.so.0.3.1':'gpkg/libthai','libXcursor.so.1.0.2':'gpkg/libxcursor','libxkbcommon.so.0.0.0':'gpkg/libxkbcommon'}
 core={'libfreetype.so.6.20.2'}
 gaps=[]
 ledger=read(review/'non-priority-generic-authority-ledger/gtk-gui.tsv')
 for n,r in enumerate([r for r in ledger if r['evidence_row_id'] not in accepted_eids],1):
  ident=r['identity_label'];mapped=root_map.get(ident,'NONE_REVIEWED_ROOT')
  gc='OPEN_REVIEWED_ROOT_PROVIDER_AUTHORITY' if mapped!='NONE_REVIEWED_ROOT' else 'NO_ACCEPTED_TERMUX_PROVIDER_CANDIDATE_OR_OUTSIDE_28_ROOTS'
  pri='FREETYPE_BOUNDED_PROVIDER_AUTHORITY' if ident in core else 'LATER_GTK_COMPOSITION_TRANCHE'
  action=('REVIEW_EXACT_FREETYPE_IDENTITY_CUSTOM_STEP_AND_CONFIGURE_SEMANTICS_PANGO_CONSUMER_BINDING_CONFLICT_UPDATE_AND_ROLLBACK' if pri.startswith('FREETYPE') else 'REVIEW_EXACT_PROVIDER_IDENTITY_ADAPTATION_CONSUMER_BINDING_CONFLICT_UPDATE_AND_ROLLBACK')
  gaps.append(dict(composition_gap_id=f'COMP-GAP-{n:03d}',selected_evidence_row_id=r['evidence_row_id'],identity_label=ident,lookup_name=r['lookup_name'],soname=r['soname'],package_or_source=r['package_or_source'],version=r['version'],root_mapping=mapped,gap_class=gc,priority_tranche=pri,blocker_reason='SELECTED_GTK_RUNTIME_IDENTITY_HAS_NO_ACCEPTED_PROVIDER_ROW_IN_CURRENT_COMPOSITION',minimum_next_action=action,authority_effect='BLOCKS_COMPOSITION_ACCEPTANCE_AND_TARGET_MANIFEST_GENERATION'))
 if len(gaps)!=15:raise SystemExit(f'expected 15 gaps, got {len(gaps)}')
 reviewed=sum(g['root_mapping']!='NONE_REVIEWED_ROOT' for g in gaps)
 outside=len(gaps)-reviewed
 metadata=[
 ('schema_version','1'),('decision_policy','ADR-0005'),('selected_gtk_identity_count','36'),('accepted_provider_root_count','18'),('accepted_member_count','24'),('included_member_count','23'),('deferred_member_count','1'),('unresolved_selected_identity_count','15'),('reviewed_root_gap_count',str(reviewed)),('outside_28_root_gap_count',str(outside)),('accepted_soname_collision_count','0'),('accepted_alias_collision_count','0'),('composition_decision','REVIEWED_BLOCKED_INCOMPLETE'),('target_manifest_allowed','NO'),('next_review_tranche','FREETYPE_BOUNDED_PROVIDER_AUTHORITY'),('authority_effect','NO_TARGET_POPULATION_MATERIALIZATION_OR_ACTIVATION')]
 write(out/MEM,MEM_FIELDS,rows);write(out/GAPS,GAP_FIELDS,gaps);write(out/META,['key','value'],[{'key':k,'value':v} for k,v in metadata])
if __name__=='__main__':main()
