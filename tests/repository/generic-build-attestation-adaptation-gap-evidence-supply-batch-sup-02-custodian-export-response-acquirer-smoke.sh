#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BASE="$ROOT/experiments/glibc/selected-obsidian-provider-authority"
ISSUANCE="$BASE/evidence-supply/requests/SUP-02/custodian-export"
ACQUIRER="$BASE/recipe/acquire-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-responses.py"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

run_acquirer() {
    local input=$1
    local out=$2
    rm -rf "$out"
    PYTHONDONTWRITEBYTECODE=1 python3 "$ACQUIRER" \
      --request-issuance "$ISSUANCE/custodian-export-request-issuance.tsv" \
      --record-contract-issuance "$ISSUANCE/custodian-export-record-contract-issuance.tsv" \
      --input-root "$input" \
      --source-head 636aad838111d37be0ab8bd8364aa5795b32256d \
      --source-tree 3a20228415cb835267e34ea0c10be6297d00cdaf \
      --out "$out"
}

run_acquirer "$TMP/absent" "$TMP/out-empty"
python3 - "$TMP/out-empty" <<'PY'
import csv,pathlib,sys
out=pathlib.Path(sys.argv[1])
def read(name):
    with (out/name).open(encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f,delimiter='\t'))
summary={r['field']:r['value'] for r in read('summary.tsv')}
assert (out/'analysis.status').read_text()=='PASS\n'
assert summary['response_input_root_state']=='ABSENT'
assert summary['issued_requests']=='28'
assert summary['issued_record_contracts']=='84'
assert summary['complete_candidate_responses_acquired']=='0'
assert summary['requests_without_response']=='28'
assert summary['verified_response_records']=='0'
assert summary['build_attestations_accepted']=='0'
assert len(read('request-response-acquisition-status.tsv'))==28
assert read('response-record-inventory.tsv')==[]
assert list((out/'candidate-response-root').iterdir())==[]
assert (out/'next-state.txt').read_text().strip()=='REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSE_ACQUISITION_RECEIPT'
PY

INPUT="$TMP/input"
mkdir -p "$INPUT"
python3 - "$ISSUANCE" "$INPUT" <<'PY'
import csv,hashlib,json,pathlib,sys
issuance=pathlib.Path(sys.argv[1]); input_root=pathlib.Path(sys.argv[2])
def read(name):
    with (issuance/name).open(encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f,delimiter='\t'))
request=read('custodian-export-request-issuance.tsv')[0]
request_id=request['request_id']; response=input_root/request_id; response.mkdir()
build_run='build-run-fixture-0001'; custodian='fixture-custodian'; locator='signed-envelope:fixture:0001'
invocation={
 'schema_version':'1','request_id':request_id,'root_review_id':request['root_review_id'],'recipe_root':request['recipe_root'],'recipe_tree':request['recipe_tree'],
 'build_run_id':build_run,'build_started_at_utc':'2026-07-14T00:00:00Z','build_finished_at_utc':'2026-07-14T00:01:00Z','working_directory':'/build/work',
 'invocation_argv':['bash','build-package.sh'],'input_source_digests':{'source.tar.zst':'1'*64},'build_script_digest':'2'*64,
 'custodian_identity':custodian,'immutable_locator_or_signed_envelope':locator}
environment={
 'schema_version':'1','request_id':request_id,'root_review_id':request['root_review_id'],'recipe_tree':request['recipe_tree'],'build_run_id':build_run,
 'host_os':'linux','host_kernel':'fixture-kernel','host_arch':'aarch64','toolchain_components':['clang','ld.lld'],'toolchain_digests':{'clang':'3'*64},
 'dependency_lock_or_snapshot':'snapshot:fixture','container_or_vm_image_digest':'4'*64,'relevant_environment':{'SOURCE_DATE_EPOCH':'1'},'source_date_epoch':'1',
 'custodian_identity':custodian,'immutable_locator_or_signed_envelope':locator}
(response/'build-invocation-record.json').write_text(json.dumps(invocation,sort_keys=True)+'\n')
(response/'build-environment-record.json').write_text(json.dumps(environment,sort_keys=True)+'\n')
fields=['request_id','root_review_id','recipe_root','recipe_tree','build_run_id','package_name','package_version','package_revision','artifact_path','artifact_sha256','member_path','member_sha256','member_elf_soname','custodian_identity','immutable_locator_or_signed_envelope']
with (response/'build-output-manifest.tsv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerow({
      'request_id':request_id,'root_review_id':request['root_review_id'],'recipe_root':request['recipe_root'],'recipe_tree':request['recipe_tree'],'build_run_id':build_run,
      'package_name':'fixture-package','package_version':'1.0','package_revision':'1','artifact_path':'packages/fixture.pkg.tar.zst','artifact_sha256':'5'*64,
      'member_path':'usr/lib/libfixture.so.1','member_sha256':'6'*64,'member_elf_soname':'libfixture.so.1','custodian_identity':custodian,'immutable_locator_or_signed_envelope':locator})
manifest_fields=['response_record_id','request_id','root_review_id','recipe_root','recipe_tree','record_name','relative_path','sha256','size_bytes','custodian_identity','immutable_locator_or_signed_envelope','claim_boundary']
rows=[]
for i,name in enumerate(['build-invocation-record.json','build-environment-record.json','build-output-manifest.tsv'],1):
    p=response/name
    rows.append({'response_record_id':f'{request_id}:record:{i}','request_id':request_id,'root_review_id':request['root_review_id'],'recipe_root':request['recipe_root'],'recipe_tree':request['recipe_tree'],
      'record_name':name,'relative_path':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size_bytes':str(p.stat().st_size),'custodian_identity':custodian,
      'immutable_locator_or_signed_envelope':locator,'claim_boundary':'CANDIDATE_CUSTODIAN_EXPORT_RESPONSE_REVIEW_REQUIRED_NO_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT'})
with (response/'custodian-export-response-manifest.tsv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=manifest_fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
(input_root/'fixture-request-id.txt').write_text(request_id+'\n')
PY
REQ=$(cat "$INPUT/fixture-request-id.txt")
rm "$INPUT/fixture-request-id.txt"
run_acquirer "$INPUT" "$TMP/out-present"
python3 - "$TMP/out-present" "$REQ" <<'PY'
import csv,pathlib,sys
out=pathlib.Path(sys.argv[1]); request_id=sys.argv[2]
def read(name):
    with (out/name).open(encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f,delimiter='\t'))
summary={r['field']:r['value'] for r in read('summary.tsv')}
assert summary['response_input_root_state']=='PRESENT'
assert summary['complete_candidate_responses_acquired']=='1'
assert summary['requests_without_response']=='27'
assert summary['verified_response_records']=='3'
assert summary['build_attestations_accepted']=='0'
status={r['request_id']:r for r in read('request-response-acquisition-status.tsv')}
assert status[request_id]['response_state']=='COMPLETE_CANDIDATE_RESPONSE_ACQUIRED_REVIEW_REQUIRED'
assert status[request_id]['verified_record_count']=='3'
assert len(read('response-record-inventory.tsv'))==3
candidate=out/'candidate-response-root'/request_id
assert (candidate/'build-invocation-record.json').is_file()
assert (candidate/'build-environment-record.json').is_file()
assert (candidate/'build-output-manifest.tsv').is_file()
assert (candidate/'custodian-export-response-manifest.tsv').is_file()
PY

cp -a "$INPUT" "$TMP/tampered"
printf '\n' >> "$TMP/tampered/$REQ/build-invocation-record.json"
if run_acquirer "$TMP/tampered" "$TMP/out-tampered" >/dev/null 2>&1; then
    echo 'digest-tampered response unexpectedly accepted' >&2; exit 1
fi

cp -a "$INPUT" "$TMP/build-run-drift"
python3 - "$TMP/build-run-drift/$REQ/build-environment-record.json" "$TMP/build-run-drift/$REQ/custodian-export-response-manifest.tsv" <<'PY'
import csv,hashlib,json,pathlib,sys
p=pathlib.Path(sys.argv[1]); manifest=pathlib.Path(sys.argv[2])
obj=json.loads(p.read_text()); obj['build_run_id']='different-build-run'; p.write_text(json.dumps(obj,sort_keys=True)+'\n')
with manifest.open(encoding='utf-8',newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0])
for row in rows:
    if row['record_name']==p.name:
        row['sha256']=hashlib.sha256(p.read_bytes()).hexdigest(); row['size_bytes']=str(p.stat().st_size)
with manifest.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if run_acquirer "$TMP/build-run-drift" "$TMP/out-build-run-drift" >/dev/null 2>&1; then
    echo 'cross-record build-run drift unexpectedly accepted' >&2; exit 1
fi

cp -a "$INPUT" "$TMP/incomplete"
rm "$TMP/incomplete/$REQ/build-output-manifest.tsv"
if run_acquirer "$TMP/incomplete" "$TMP/out-incomplete" >/dev/null 2>&1; then
    echo 'incomplete response unexpectedly accepted' >&2; exit 1
fi

cp -a "$INPUT" "$TMP/extra"
printf 'extra\n' > "$TMP/extra/$REQ/extra.txt"
if run_acquirer "$TMP/extra" "$TMP/out-extra" >/dev/null 2>&1; then
    echo 'unmanifested response file unexpectedly accepted' >&2; exit 1
fi

mkdir -p "$TMP/unknown/UNKNOWN-REQUEST"
if run_acquirer "$TMP/unknown" "$TMP/out-unknown" >/dev/null 2>&1; then
    echo 'unknown request directory unexpectedly accepted' >&2; exit 1
fi

printf '%s\n' 'SUP_02_CUSTODIAN_EXPORT_RESPONSE_ACQUIRER_SMOKE_PASS'
