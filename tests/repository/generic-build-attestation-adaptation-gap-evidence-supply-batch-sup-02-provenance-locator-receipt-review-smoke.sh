#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BASE="$ROOT/experiments/glibc/selected-obsidian-provider-authority"
REVIEW="$BASE/review"
REVIEWER="$BASE/recipe/review-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-provenance-locator-receipt.py"
RULES="$REVIEW/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-provenance-locator-receipt-review-rules.tsv"
ROOTS="$REVIEW/generic-build-attestation-adaptation-root-gap-evidence-supply-request-set.tsv"
BATCHES="$REVIEW/generic-build-attestation-adaptation-gap-evidence-supply-batches.tsv"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
make_fixture() {
  local out=$1
  rm -rf "$out"; mkdir -p "$out"
  python3 - "$ROOTS" "$out" <<'PY'
import csv,pathlib,sys
roots_path=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2])
with roots_path.open(encoding='utf-8',newline='') as f: roots=list(csv.DictReader(f,delimiter='\t'))
def write(name,fields,rows):
    with (out/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
claim='PROVENANCE_LOCATOR_RECEIPT_ONLY_NO_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT'
write('sup-02-local-record-inventory.tsv',['root_review_id','acquisition_unit_id','recipe_root','record_kind','path','sha256','size_bytes','validation_state','claim_boundary'],[])
write('sup-02-root-provenance-locator.tsv',['acquisition_unit_id','root_review_id','recipe_root','recipe_tree','build_invocation_records','build_environment_records','build_output_manifests','locator_state','ba_001_state','ba_002_state','ba_003_state','authority_state','claim_boundary'],[
 {'acquisition_unit_id':r['acquisition_unit_id'],'root_review_id':r['root_review_id'],'recipe_root':r['recipe_root'],'recipe_tree':r['recipe_tree'],'build_invocation_records':'0','build_environment_records':'0','build_output_manifests':'0','locator_state':'NO_CUSTODIAN_EXPORT_FOUND','ba_001_state':'OPEN_NO_RECORD_LOCATED','ba_002_state':'OPEN_NO_RECORD_LOCATED','ba_003_state':'OPEN_NO_RECORD_LOCATED','authority_state':'OPEN_NO_ACCEPTANCE','claim_boundary':claim} for r in roots])
write('sup-02-custodian-surface.tsv',['surface','state','item_count','sha256','evidentiary_effect'],[
 {'surface':'github_repository_metadata','state':'CAPTURED','item_count':'1','sha256':'c2d00006e78b330f1cd94ad59ca94c0d6475d5ec4fc35d25bfa2bc66de008d8d','evidentiary_effect':'LOCATOR_ONLY'},
 {'surface':'github_actions_workflows','state':'CAPTURED','item_count':'2','sha256':'0c0058ce3654d5140808e299078d1cf1e2dd3cda50fb5c375dfacb2c955fad73','evidentiary_effect':'LOCATOR_ONLY_NOT_BUILD_PROVENANCE'},
 {'surface':'github_releases','state':'CAPTURED','item_count':'4','sha256':'0b62b3e3568c04722ce8b3ad9b84980da817b0803a932a01f2b3b525a6b157f4','evidentiary_effect':'LOCATOR_ONLY_NOT_BUILD_PROVENANCE'},])
write('summary.tsv',['field','value'],[
 {'field':'root_rows','value':'28'},{'field':'record_roots','value':'1'},{'field':'complete_custodian_exports','value':'0'},{'field':'partial_custodian_exports','value':'0'},{'field':'absent_custodian_exports','value':'28'},{'field':'record_files_located','value':'0'},{'field':'build_attestations_accepted','value':'0'},{'field':'final_provider_decisions_accepted','value':'0'},{'field':'target_rows_populated','value':'0'},{'field':'next_state','value':'REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_PROVENANCE_LOCATOR_RECEIPT'}])
(out/'analysis.status').write_text('PASS\n')
(out/'claim-boundary.txt').write_text(claim+'\n')
(out/'next-state.txt').write_text('REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_PROVENANCE_LOCATOR_RECEIPT\n')
PY
}
run_review() {
  local fixture=$1 out=$2
  rm -rf "$out"
  PYTHONDONTWRITEBYTECODE=1 python3 "$REVIEWER" \
    --root-request-set "$ROOTS" \
    --supply-batches "$BATCHES" \
    --locator-dir "$fixture" \
    --rules "$RULES" \
    --out "$out"
}
make_fixture "$TMP/fixture"
run_review "$TMP/fixture" "$TMP/review"
for name in \
  generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-provenance-locator-receipt-review.tsv \
  generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-root-provenance-locator-receipt-review.tsv \
  generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-surface-receipt-review.tsv \
  generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-provenance-locator-receipt-review-metadata.tsv; do
  cmp "$TMP/review/$name" "$REVIEW/$name"
done
python3 - "$TMP/review" <<'PY'
import csv,pathlib,sys
out=pathlib.Path(sys.argv[1])
def rows(name):
    with (out/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
assert (out/'analysis.status').read_text()=='PASS\n'
assert (out/'next-state.txt').read_text().strip()=='DEFINE_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_REQUEST_SET'
overall=rows('generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-provenance-locator-receipt-review.tsv')
assert len(overall)==1 and overall[0]['absent_custodian_exports']=='28' and overall[0]['record_files_located']=='0'
roots=rows('generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-root-provenance-locator-receipt-review.tsv')
assert len(roots)==28 and {r['locator_receipt_state'] for r in roots}=={'CONFIRMED_NO_EXISTING_CUSTODIAN_EXPORT'}
assert {r['build_attestation_state'] for r in roots}=={'OPEN_NO_ACCEPTANCE'}
surfaces=rows('generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-surface-receipt-review.tsv')
assert len(surfaces)==3 and {r['build_provenance_effect'] for r in surfaces}=={'NONE'}
meta={r['field']:r['value'] for r in rows('generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-provenance-locator-receipt-review-metadata.tsv')}
assert meta['complete_custodian_exports']=='0' and meta['absent_custodian_exports']=='28'
assert meta['build_attestations_accepted']=='0' and meta['target_rows_populated']=='0'
PY

tamper_case() {
  local name=$1 code=$2
  local fixture="$TMP/$name"
  cp -a "$TMP/fixture" "$fixture"
  python3 - "$fixture" <<PY
$code
PY
  if run_review "$fixture" "$TMP/out-$name" >/dev/null 2>&1; then
    echo "$name unexpectedly accepted" >&2; exit 1
  fi
}
tamper_case false_complete 'import csv,pathlib,sys
p=pathlib.Path(sys.argv[1])/"sup-02-root-provenance-locator.tsv"
with p.open(encoding="utf-8",newline="") as f:r=list(csv.DictReader(f,delimiter="\t")); fields=list(r[0])
r[0]["build_invocation_records"]="1"; r[0]["locator_state"]="COMPLETE_CUSTODIAN_EXPORT_FOUND"
with p.open("w",encoding="utf-8",newline="") as f:w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(r)'
tamper_case invented_record 'import csv,pathlib,sys
p=pathlib.Path(sys.argv[1])/"sup-02-local-record-inventory.tsv"
with p.open(encoding="utf-8",newline="") as f:fields=next(csv.reader(f,delimiter="\t"))
with p.open("a",encoding="utf-8",newline="") as f:csv.writer(f,delimiter="\t",lineterminator="\n").writerow(["x"]*len(fields))'
tamper_case metadata_promotion 'import csv,pathlib,sys
p=pathlib.Path(sys.argv[1])/"sup-02-custodian-surface.tsv"
with p.open(encoding="utf-8",newline="") as f:r=list(csv.DictReader(f,delimiter="\t")); fields=list(r[0])
r[1]["evidentiary_effect"]="BUILD_PROVENANCE_ACCEPTED"
with p.open("w",encoding="utf-8",newline="") as f:w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(r)'
if PYTHONDONTWRITEBYTECODE=1 python3 "$REVIEWER" --root-request-set "$ROOTS" --supply-batches "$BATCHES" --locator-dir "$TMP/fixture" --rules "$RULES" --source-archive-sha256 "$(printf 0%.0s {1..64})" --out "$TMP/out-source-drift" >/dev/null 2>&1; then
  echo 'source identity drift unexpectedly accepted' >&2; exit 1
fi
printf '%s\n' 'GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_PROVENANCE_LOCATOR_RECEIPT_REVIEW_SMOKE_PASS'
