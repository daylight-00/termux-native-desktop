#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
COLLECTOR="$ROOT/experiments/glibc/selected-obsidian-provider-authority/recipe/collect-generic-build-attestation-and-adaptation-evidence.py"
REQUIREMENTS="$ROOT/experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-review-requirements.tsv"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
SRC="$TMP/source"
FIX="$TMP/fixture"
FOUNDATION="$TMP/foundation"
OUT="$TMP/out"
mkdir -p "$SRC/gpkg/foo" "$SRC/gpkg/bar" "$FIX" "$FOUNDATION"

cat > "$SRC/gpkg/foo/build.sh" <<'EOF'
TERMUX_PKG_VERSION=1.0
TERMUX_PKG_SRCURL=https://example.invalid/foo.tar.xz
TERMUX_PKG_SHA256=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
TERMUX_PKG_EXTRA_CONFIGURE_ARGS="--with-prefix=$TERMUX_PREFIX"
termux_step_post_make_install() { :; }
EOF
printf '%s\n' 'synthetic patch' > "$SRC/gpkg/foo/android.patch"
cat > "$SRC/gpkg/bar/build.sh" <<'EOF'
TERMUX_PKG_VERSION=2.0
TERMUX_PKG_SRCURL=https://example.invalid/bar.tar.xz
TERMUX_PKG_SHA256=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
EOF

git -C "$SRC" init -q
git -C "$SRC" config user.name test
git -C "$SRC" config user.email test@example.invalid
git -C "$SRC" add .
git -C "$SRC" commit -qm fixture

python3 - "$SRC" "$FIX" "$FOUNDATION" "$REQUIREMENTS" <<'PY'
import csv, hashlib, pathlib, subprocess, sys
src, fix, foundation, requirements = map(pathlib.Path, sys.argv[1:])

def git(*args, text=True):
    return subprocess.run(["git", *args], cwd=src, check=True, stdout=subprocess.PIPE, text=text).stdout

def write(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

def sha(b): return hashlib.sha256(b).hexdigest()
head=git("rev-parse","HEAD").strip(); tree=git("rev-parse","HEAD^{tree}").strip()
root_trees={r:git("rev-parse",f"HEAD:{r}").strip() for r in ["gpkg/foo","gpkg/bar"]}
recipe_files=[]
for root in root_trees:
    for raw in git("ls-tree","-r","-l","HEAD","--",root).splitlines():
        meta,path=raw.split("\t",1); mode,kind,oid,size=meta.split(None,3)
        payload=git("show",f"HEAD:{path}",text=False)
        recipe_files.append({"recipe_root":root,"path":path,"mode":mode,"blob_oid":oid,"size":len(payload),"content_sha256":sha(payload)})
write(foundation/"source-repository-state.tsv", ["path","head","tree","origin","is_shallow","is_bare","worktree_state","fsck_state"], [{"path":str(src),"head":head,"tree":tree,"origin":"fixture","is_shallow":"false","is_bare":"false","worktree_state":"CLEAN","fsck_state":"PASS"}])
write(foundation/"recipe-file-inventory.tsv", ["recipe_root","path","mode","blob_oid","size","content_sha256"], recipe_files)
write(foundation/"artifact-verification.tsv", ["artifact_id","package","version","architecture","local_path","actual_size","actual_sha256","control_identity_state","package_operation_performed"], [
 {"artifact_id":"artifact:a","package":"foo","version":"1.0","architecture":"aarch64","local_path":"/fixture/a.deb","actual_size":"10","actual_sha256":"a"*64,"control_identity_state":"EXACT_PACKAGE_VERSION_ARCHITECTURE_MATCH","package_operation_performed":"NO"},
 {"artifact_id":"artifact:b","package":"bar","version":"2.0","architecture":"aarch64","local_path":"/fixture/b.deb","actual_size":"20","actual_sha256":"b"*64,"control_identity_state":"EXACT_PACKAGE_VERSION_ARCHITECTURE_MATCH","package_operation_performed":"NO"},
])
write(foundation/"drift-target-elf-review.tsv", ["evidence_row_id","identity_label","artifact_id","artifact_package","expected_soname_alias","alias_member_path","target_member_path","target_member_size","target_member_mode_octal","target_member_sha256","elf_parse_state","elf_class","elf_data","elf_machine","observed_soname","drift_target_elf_review_state","object_member_evidence_state","artifact_to_recipe_binding_state","termux_android_adaptation_state","final_provider_state","target_population_state"], [
 {"evidence_row_id":"ev2","identity_label":"libfoo.so.1.2.3","artifact_id":"artifact:a","artifact_package":"foo","expected_soname_alias":"libfoo.so.1","alias_member_path":"lib/libfoo.so.1","target_member_path":"lib/libfoo.so.1.2.0","target_member_size":"100","target_member_mode_octal":"755","target_member_sha256":"2"*64,"elf_parse_state":"ELF_SONAME_PARSED","elf_class":"ELF64","elf_data":"LITTLE","elf_machine":"183","observed_soname":"libfoo.so.1","drift_target_elf_review_state":"DRIFT_TARGET_ELF_EXPECTED_SONAME_CONFIRMED","object_member_evidence_state":"CANDIDATE","artifact_to_recipe_binding_state":"OPEN","termux_android_adaptation_state":"OPEN","final_provider_state":"UNRESOLVED","target_population_state":"BLOCKED"}
])
obj_fields=["object_review_id","evidence_row_id","review_tier","capability_partition","identity_label","artifact_id","artifact_package","artifact_version","artifact_sha256","recipe_root","recipe_tree","recipe_resolved_full_version","adaptation_evidence_tokens","object_member_review_state","build_attestation_requirement_set","adaptation_requirement_set","concrete_filename_requirement_set","object_correction_requirement_set","review_eligibility_state","authority_state","target_population_state","next_action"]
objects=[
 {"object_review_id":"obj1","evidence_row_id":"ev1","review_tier":"T2_MATERIAL_DELTA_EXACT","capability_partition":"test","identity_label":"libfoo.so.1.2.0","artifact_id":"artifact:a","artifact_package":"foo","artifact_version":"1.0","artifact_sha256":"a"*64,"recipe_root":"gpkg/foo","recipe_tree":root_trees["gpkg/foo"],"recipe_resolved_full_version":"1.0","adaptation_evidence_tokens":"PATCH_FILE;TERMUX_PREFIX_REFERENCE","object_member_review_state":"EXACT_MEMBER_EXPECTED_SONAME_CANDIDATE_CONFIRMED","build_attestation_requirement_set":"BA-001;BA-002;BA-003;BA-004;BA-005","adaptation_requirement_set":"AD-001;AD-002;AD-003;AD-004;AD-005","concrete_filename_requirement_set":"NONE","object_correction_requirement_set":"NONE","review_eligibility_state":"EVIDENCE_COLLECTION_ELIGIBLE_AUTHORITY_BLOCKED","authority_state":"OPEN_NO_ACCEPTANCE","target_population_state":"UNPOPULATED","next_action":"COLLECT"},
 {"object_review_id":"obj2","evidence_row_id":"ev2","review_tier":"T1_MATERIAL_DELTA_AND_DRIFT","capability_partition":"test","identity_label":"libfoo.so.1.2.3","artifact_id":"artifact:a","artifact_package":"foo","artifact_version":"1.0","artifact_sha256":"a"*64,"recipe_root":"gpkg/foo","recipe_tree":root_trees["gpkg/foo"],"recipe_resolved_full_version":"1.0","adaptation_evidence_tokens":"PATCH_FILE;TERMUX_PREFIX_REFERENCE","object_member_review_state":"DRIFT_TARGET_ELF_EXPECTED_SONAME_CANDIDATE_CONFIRMED","build_attestation_requirement_set":"BA-001;BA-002;BA-003;BA-004;BA-005","adaptation_requirement_set":"AD-001;AD-002;AD-003;AD-004;AD-005","concrete_filename_requirement_set":"CF-001;CF-002;CF-003;CF-004","object_correction_requirement_set":"NONE","review_eligibility_state":"EVIDENCE_COLLECTION_ELIGIBLE_AUTHORITY_BLOCKED","authority_state":"OPEN_NO_ACCEPTANCE","target_population_state":"UNPOPULATED","next_action":"COLLECT"},
 {"object_review_id":"obj3","evidence_row_id":"ev3","review_tier":"T0_OBJECT_REQUIREMENT_CORRECTION","capability_partition":"test","identity_label":"libjpeg.so.62.3.0","artifact_id":"artifact:b","artifact_package":"bar","artifact_version":"2.0","artifact_sha256":"b"*64,"recipe_root":"gpkg/bar","recipe_tree":root_trees["gpkg/bar"],"recipe_resolved_full_version":"2.0","adaptation_evidence_tokens":"NONE_DECLARED","object_member_review_state":"EXPECTED_SONAME_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED","build_attestation_requirement_set":"BA-001;BA-002;BA-003;BA-004;BA-005","adaptation_requirement_set":"AD-002;AD-003;AD-004;AD-006","concrete_filename_requirement_set":"NONE","object_correction_requirement_set":"OJ-001","review_eligibility_state":"BLOCKED_OBJECT_REQUIREMENT_UNSATISFIED","authority_state":"OPEN_NO_ACCEPTANCE","target_population_state":"UNPOPULATED","next_action":"CORRECT"},
]
write(fix/"objects.tsv", obj_fields, objects)
root_fields=["root_review_id","review_tier","recipe_root","recipe_tree","recipe_resolved_full_version","artifact_ids","artifact_packages","artifact_count","identity_count","adaptation_evidence_tokens","build_attestation_requirement_set","adaptation_requirement_set","concrete_filename_requirement_set","object_correction_requirement_set","eligible_object_count","blocked_object_count","review_state","authority_state","next_action"]
write(fix/"roots.tsv", root_fields, [
 {"root_review_id":"root1","review_tier":"T1_MATERIAL_DELTA_AND_DRIFT","recipe_root":"gpkg/foo","recipe_tree":root_trees["gpkg/foo"],"recipe_resolved_full_version":"1.0","artifact_ids":"artifact:a","artifact_packages":"foo","artifact_count":"1","identity_count":"2","adaptation_evidence_tokens":"PATCH_FILE;TERMUX_PREFIX_REFERENCE","build_attestation_requirement_set":"BA-001;BA-002;BA-003;BA-004;BA-005","adaptation_requirement_set":"AD-001;AD-002;AD-003;AD-004;AD-005","concrete_filename_requirement_set":"CF-001;CF-002;CF-003;CF-004","object_correction_requirement_set":"NONE","eligible_object_count":"2","blocked_object_count":"0","review_state":"REQUIREMENTS_DEFINED_EVIDENCE_NOT_COLLECTED","authority_state":"OPEN_NO_ACCEPTANCE","next_action":"COLLECT"},
 {"root_review_id":"root2","review_tier":"T0_OBJECT_REQUIREMENT_CORRECTION","recipe_root":"gpkg/bar","recipe_tree":root_trees["gpkg/bar"],"recipe_resolved_full_version":"2.0","artifact_ids":"artifact:b","artifact_packages":"bar","artifact_count":"1","identity_count":"1","adaptation_evidence_tokens":"NONE_DECLARED","build_attestation_requirement_set":"BA-001;BA-002;BA-003;BA-004;BA-005","adaptation_requirement_set":"AD-002;AD-003;AD-004;AD-006","concrete_filename_requirement_set":"NONE","object_correction_requirement_set":"OJ-001","eligible_object_count":"0","blocked_object_count":"1","review_state":"REQUIREMENTS_DEFINED_EVIDENCE_NOT_COLLECTED","authority_state":"OPEN_NO_ACCEPTANCE","next_action":"CORRECT"},
])
member_fields=["evidence_row_id","capability_partition","identity_label","expected_soname_alias","candidate_artifact_ids","candidate_packages","exact_artifact_id","exact_member_path","exact_member_sha256","exact_observed_elf_soname","alias_artifact_id","alias_member_path","alias_link_target","alias_target_member_path","family_observed_basenames","review_state","object_member_evidence_state","artifact_to_recipe_binding_state","termux_android_adaptation_state","final_provider_state","target_population_state"]
write(fix/"member.tsv", member_fields, [
 {"evidence_row_id":"ev1","identity_label":"libfoo.so.1.2.0","exact_member_path":"lib/libfoo.so.1.2.0","exact_member_sha256":"1"*64,"exact_observed_elf_soname":"libfoo.so.1","review_state":"EXACT_CONCRETE_MEMBER_AND_EXPECTED_SONAME_OBSERVED"},
 {"evidence_row_id":"ev2","identity_label":"libfoo.so.1.2.3","alias_member_path":"lib/libfoo.so.1","alias_link_target":"libfoo.so.1.2.0","alias_target_member_path":"lib/libfoo.so.1.2.0","review_state":"EXPECTED_SONAME_ALIAS_SYMLINK_PRESENT_CONCRETE_FILENAME_DRIFT"},
 {"evidence_row_id":"ev3","identity_label":"libjpeg.so.62.3.0","review_state":"EXPECTED_SONAME_ALIAS_NOT_OBSERVED_DIFFERENT_FAMILY_MEMBERS_PRESENT"},
])
recipe_fields=["evidence_row_id","capability_partition","identity_label","artifact_id","artifact_package","artifact_version","artifact_sha256","recipe_root","recipe_tree","recipe_resolved_full_version","recipe_source_url_raw","recipe_source_sha256","recipe_file_manifest_sha256","adaptation_evidence_tokens","recipe_lineage_review_state","artifact_build_attestation_review_state","adaptation_semantic_review_state","member_receipt_review_state","object_member_review_state","drift_target_member_path","drift_target_member_sha256","drift_target_observed_soname","concrete_filename_policy_state","provider_review_eligibility_state","final_provider_state","target_population_state","next_action"]
recipe_rows=[]
for o in objects:
 recipe_rows.append({"evidence_row_id":o["evidence_row_id"],"identity_label":o["identity_label"],"artifact_id":o["artifact_id"],"artifact_package":o["artifact_package"],"artifact_version":o["artifact_version"],"artifact_sha256":o["artifact_sha256"],"recipe_root":o["recipe_root"],"recipe_tree":o["recipe_tree"],"recipe_resolved_full_version":o["recipe_resolved_full_version"],"recipe_source_url_raw":"https://example.invalid/source.tar.xz","recipe_source_sha256":"c"*64,"recipe_file_manifest_sha256":"d"*64,"adaptation_evidence_tokens":o["adaptation_evidence_tokens"],"object_member_review_state":o["object_member_review_state"]})
write(fix/"recipe.tsv", recipe_fields, recipe_rows)
binding_fields=["evidence_row_id","capability_partition","identity_label","member_receipt_review_state","artifact_id","artifact_package","artifact_version","artifact_sha256","recipe_root","recipe_tree","recipe_resolved_full_version","recipe_source_url_raw","recipe_source_sha256","recipe_file_manifest_sha256","adaptation_evidence_tokens","recipe_lineage_candidate_state","artifact_to_recipe_binding_state","termux_android_adaptation_state","drift_target_elf_review_state","final_provider_state","target_population_state"]
write(foundation/"recipe-binding-review.tsv", binding_fields, [{**r,"recipe_lineage_candidate_state":"PINNED","artifact_to_recipe_binding_state":"OPEN","termux_android_adaptation_state":"OPEN","final_provider_state":"UNRESOLVED","target_population_state":"BLOCKED"} for r in recipe_rows])
write(foundation/"summary.tsv", ["field","value"], [
 {"field":"artifact_to_recipe_bindings_accepted","value":"0"},
 {"field":"termux_android_adaptations_accepted","value":"0"},
 {"field":"final_provider_decisions_accepted","value":"0"},
 {"field":"target_rows_populated","value":"0"},
])
PY

before=$(git -C "$SRC" status --porcelain --untracked-files=all)
PROJECT_REPO="$ROOT" \
OUT="$OUT" \
GENERIC_EVIDENCE_REQUIREMENTS="$REQUIREMENTS" \
GENERIC_EVIDENCE_ROOT_SET="$FIX/roots.tsv" \
GENERIC_EVIDENCE_OBJECT_SET="$FIX/objects.tsv" \
GENERIC_MEMBER_RECEIPT_REVIEW="$FIX/member.tsv" \
GENERIC_RECIPE_RECEIPT_REVIEW="$FIX/recipe.tsv" \
GENERIC_EVIDENCE_FOUNDATION_OUT="$FOUNDATION" \
GENERIC_SOURCE_REPO="$SRC" \
GENERIC_EVIDENCE_EXPECTED_ROOTS=2 \
GENERIC_EVIDENCE_EXPECTED_OBJECTS=3 \
GENERIC_EVIDENCE_EXPECTED_EXACT=1 \
GENERIC_EVIDENCE_EXPECTED_DRIFT=1 \
GENERIC_EVIDENCE_EXPECTED_BLOCKED=1 \
PYTHONDONTWRITEBYTECODE=1 \
python3 "$COLLECTOR"
after=$(git -C "$SRC" status --porcelain --untracked-files=all)
[ "$before" = "$after" ]

python3 - "$OUT" <<'PY'
import csv, pathlib, sys
out=pathlib.Path(sys.argv[1])
def read(name):
 with (out/name).open(encoding="utf-8",newline="") as f: return list(csv.DictReader(f,delimiter="\t"))
def meta(): return {r["field"]:r["value"] for r in read("summary.tsv")}
assert (out/"analysis.status").read_text()=="PASS\n"
req=read("requirement-evidence-status.tsv")
assert len(req)==16
states={r["requirement_id"]:r["collection_state"] for r in req}
assert states["BA-001"]=="EXTERNAL_BUILD_PROVENANCE_REQUIRED"
assert states["BA-003"]=="LOCAL_OUTPUT_BINDING_EVIDENCE_COLLECTED_BUILD_LINK_OPEN"
assert states["AD-001"]=="LOCAL_COMPLETE_RECIPE_FILE_AND_SIGNAL_INVENTORY_COLLECTED_REVIEW_REQUIRED"
assert states["CF-002"]=="LOCAL_EXACT_ALIAS_TARGET_EVIDENCE_COLLECTED_REVIEW_REQUIRED"
assert states["OJ-001"]=="OBJECT_REQUIREMENT_CORRECTION_REQUIRED"
assert len(read("root-evidence-observations.tsv"))==2
assert len(read("artifact-member-output-evidence.tsv"))==3
assert len(read("root-object-impact-crosswalk.tsv"))==3
m=meta()
assert m["requirements"]=="16"
assert m["root_work_units"]=="2"
assert m["object_work_units"]=="3"
assert m["exact_output_rows"]=="1"
assert m["drift_output_rows"]=="1"
assert m["blocked_object_rows"]=="1"
assert m["artifact_build_attestations_accepted"]=="0"
assert m["target_rows_populated"]=="0"
assert m["next_state"]=="REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE_RECEIPT"
PY

printf '%s\n' 'generic build attestation and adaptation evidence collector smoke: PASS'
