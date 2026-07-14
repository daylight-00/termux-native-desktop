#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BASE="$ROOT/experiments/glibc/selected-obsidian-provider-authority"
REVIEW="$BASE/review"
ACQUIRER="$BASE/recipe/acquire-generic-build-attestation-and-adaptation-gap-evidence.py"
COLLECTOR="$BASE/recipe/collect-generic-build-attestation-and-adaptation-gap-closure.py"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

run_acquirer() {
    local input=$1 out=$2
    rm -rf "$out"
    PYTHONDONTWRITEBYTECODE=1 python3 "$ACQUIRER" \
      --source-contracts "$REVIEW/generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv" \
      --lanes "$REVIEW/generic-build-attestation-adaptation-gap-evidence-acquisition-lanes.tsv" \
      --requirements "$REVIEW/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv" \
      --roots "$REVIEW/generic-build-attestation-adaptation-root-gap-evidence-acquisition-set.tsv" \
      --objects "$REVIEW/generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv" \
      --input-root "$input" \
      --out "$out"
}

run_acquirer "$TMP/absent-input" "$TMP/out-empty"
python3 - "$TMP/out-empty" <<'PY'
import csv,pathlib,sys
out=pathlib.Path(sys.argv[1])
def read(name):
 with (out/name).open(encoding='utf-8',newline='') as f: return list(csv.DictReader(f,delimiter='\t'))
summary={r['field']:r['value'] for r in read('summary.tsv')}
assert (out/'analysis.status').read_text()=='PASS\n'
assert summary['acquisition_input_root_state']=='ABSENT_NO_ACQUISITION_INPUT'
assert summary['candidate_evidence_files_acquired']=='0'
assert summary['candidate_requirements']=='0'
assert summary['local_foundation_only_requirements']=='6'
assert summary['direct_gap_unavailable_requirements']=='10'
assert summary['artifact_build_attestations_accepted']=='0'
assert summary['final_provider_decisions_accepted']=='0'
assert summary['target_rows_populated']=='0'
assert len(read('requirement-acquisition-status.tsv'))==16
assert len(read('lane-acquisition-status.tsv'))==6
assert len(read('root-acquisition-status.tsv'))==28
assert len(read('object-acquisition-status.tsv'))==37
assert len(read('unavailable-acquisition-inputs.tsv'))==16
with (out/'evidence-root/evidence-manifest.tsv').open(encoding='utf-8',newline='') as f:
 rows=list(csv.DictReader(f,delimiter='\t'))
assert rows==[]
assert (out/'next-state.txt').read_text().strip()=='REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUISITION_RECEIPT'
PY

INPUT="$TMP/input"
mkdir -p "$INPUT/files"
printf '%s\n' 'immutable producing-build candidate' > "$INPUT/files/build-record.txt"
printf '%s\n' 'authoritative object correction candidate' > "$INPUT/files/object-reference.txt"
printf '%s\n' 'bounded consumer reference candidate' > "$INPUT/files/consumer-reference.txt"
python3 - "$REVIEW" "$INPUT" <<'PY'
import csv,hashlib,pathlib,sys
review=pathlib.Path(sys.argv[1]); root=pathlib.Path(sys.argv[2])
def read(name):
 with (review/name).open(encoding='utf-8',newline='') as f: return list(csv.DictReader(f,delimiter='\t'))
contracts={r['source_kind']:r for r in read('generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv')}
reqs={r['requirement_id']:r for r in read('generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv')}
roots=read('generic-build-attestation-adaptation-root-gap-evidence-acquisition-set.tsv')
objects=read('generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv')
root_ba=next(r for r in roots if 'BA-001' in r['requirement_ids'].split(';') and 'IMMUTABLE_BUILD_RECORD' in r['source_kinds'].split(';'))
obj_oj=next(r for r in objects if 'OJ-001' in r['requirement_ids'].split(';') and 'AUTHORITATIVE_REFERENCE' in r['source_kinds'].split(';'))
obj_cf=next(r for r in objects if 'CF-001' in r['requirement_ids'].split(';') and 'CONSUMER_REFERENCE' in r['source_kinds'].split(';'))
fields=['input_id','acquisition_unit_id','requirement_id','lane_id','scope_kind','scope_id','source_kind','acquisition_mode','locator_class','source_locator','relative_path','sha256','size_bytes','evidence_class','claim_boundary']
items=[
 ('build-001',root_ba,'BA-001','IMMUTABLE_BUILD_RECORD','files/build-record.txt','DIGEST_BOUND_BUILD_INVOCATION'),
 ('object-001',obj_oj,'OJ-001','AUTHORITATIVE_REFERENCE','files/object-reference.txt','AUTHORITATIVE_OBJECT_REQUIREMENT_REFERENCE'),
 ('consumer-001',obj_cf,'CF-001','CONSUMER_REFERENCE','files/consumer-reference.txt','CONSUMER_BINDING_REFERENCE'),
]
rows=[]
for input_id,unit,req_id,source_kind,rel,eclass in items:
 p=root/rel; c=contracts[source_kind]; req=reqs[req_id]
 rows.append({
  'input_id':input_id,'acquisition_unit_id':unit['acquisition_unit_id'],'requirement_id':req_id,'lane_id':req['lane_id'],
  'scope_kind':unit['manifest_scope_kind'],'scope_id':unit['manifest_scope_id'],'source_kind':source_kind,
  'acquisition_mode':c['acquisition_mode'],'locator_class':c['required_locator_class'],
  'source_locator':f'fixture:{input_id}:immutable','relative_path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
  'size_bytes':str(p.stat().st_size),'evidence_class':eclass,
  'claim_boundary':'CANDIDATE_EVIDENCE_REVIEW_REQUIRED_NO_AUTHORITY_EFFECT'})
with (root/'acquisition-input-manifest.tsv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY

run_acquirer "$INPUT" "$TMP/out-present"
python3 - "$TMP/out-present" <<'PY'
import csv,pathlib,sys
out=pathlib.Path(sys.argv[1])
def read(name):
 with (out/name).open(encoding='utf-8',newline='') as f: return list(csv.DictReader(f,delimiter='\t'))
summary={r['field']:r['value'] for r in read('summary.tsv')}
assert summary['acquisition_input_root_state']=='PRESENT_MANIFEST_VERIFIED'
assert summary['candidate_evidence_files_acquired']=='3'
assert summary['candidate_requirements']=='3'
assert len(read('acquisition-file-inventory.tsv'))==3
assert len(read('evidence-root/evidence-manifest.tsv'))==3
req={r['requirement_id']:r for r in read('requirement-acquisition-status.tsv')}
assert req['BA-001']['acquisition_state']=='CANDIDATE_EVIDENCE_ACQUIRED_REVIEW_REQUIRED'
assert req['OJ-001']['acquisition_state']=='CANDIDATE_EVIDENCE_ACQUIRED_REVIEW_REQUIRED'
assert req['CF-001']['acquisition_state']=='CANDIDATE_EVIDENCE_ACQUIRED_REVIEW_REQUIRED'
assert req['BA-003']['authority_state']=='OPEN_NO_ACCEPTANCE'
for row in read('object-acquisition-status.tsv'):
 assert row['final_provider_state']=='UNRESOLVED'
 assert row['authority_state']=='OPEN_NO_ACCEPTANCE'
 assert row['target_population_state']=='UNPOPULATED'
PY

PROJECT_REPO="$ROOT" OUT="$TMP/collector-out" GENERIC_GAP_EVIDENCE_ROOT="$TMP/out-present/evidence-root" PYTHONDONTWRITEBYTECODE=1 python3 "$COLLECTOR"
python3 - "$TMP/collector-out" <<'PY'
import csv,pathlib,sys
out=pathlib.Path(sys.argv[1])
def read(name):
 with (out/name).open(encoding='utf-8',newline='') as f: return list(csv.DictReader(f,delimiter='\t'))
summary={r['field']:r['value'] for r in read('summary.tsv')}
assert summary['candidate_evidence_files']=='3'
assert summary['candidate_requirements']=='3'
assert summary['final_provider_decisions_accepted']=='0'
PY

cp -a "$INPUT" "$TMP/tampered"
printf '%s\n' tamper >> "$TMP/tampered/files/build-record.txt"
if run_acquirer "$TMP/tampered" "$TMP/out-tampered" >/dev/null 2>&1; then
    echo 'tampered acquisition input unexpectedly accepted' >&2; exit 1
fi

cp -a "$INPUT" "$TMP/extra"
printf '%s\n' unmanifested > "$TMP/extra/files/extra.txt"
if run_acquirer "$TMP/extra" "$TMP/out-extra" >/dev/null 2>&1; then
    echo 'unmanifested acquisition input unexpectedly accepted' >&2; exit 1
fi

cp -a "$INPUT" "$TMP/bad-mode"
python3 - "$TMP/bad-mode/acquisition-input-manifest.tsv" <<'PY'
import csv,pathlib,sys
p=pathlib.Path(sys.argv[1])
with p.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0])
rows[0]['acquisition_mode']='UNBOUNDED_NETWORK_DISCOVERY'
with p.open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if run_acquirer "$TMP/bad-mode" "$TMP/out-bad-mode" >/dev/null 2>&1; then
    echo 'invalid acquisition mode unexpectedly accepted' >&2; exit 1
fi

printf '%s\n' 'GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUIRER_SMOKE_PASS'
