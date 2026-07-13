#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
COLLECTOR="$ROOT/experiments/glibc/selected-obsidian-provider-authority/recipe/collect-generic-build-attestation-and-adaptation-gap-closure.py"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

OUT_EMPTY="$TMP/out-empty"
PROJECT_REPO="$ROOT" \
OUT="$OUT_EMPTY" \
GENERIC_GAP_EVIDENCE_ROOT="$TMP/absent-evidence-root" \
PYTHONDONTWRITEBYTECODE=1 \
python3 "$COLLECTOR"

python3 - "$OUT_EMPTY" <<'PY'
import csv, pathlib, sys
out=pathlib.Path(sys.argv[1])
def read(name):
    with (out/name).open(encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f,delimiter='\t'))
def meta(): return {r['field']:r['value'] for r in read('summary.tsv')}
assert (out/'analysis.status').read_text()=='PASS\n'
req={r['requirement_id']:r for r in read('requirement-collection-status.tsv')}
assert len(req)==16
assert req['BA-003']['collection_state']=='LOCAL_FOUNDATION_RECONFIRMED_CLOSURE_EVIDENCE_OPEN'
assert req['AD-001']['collection_state']=='LOCAL_FOUNDATION_RECONFIRMED_CLOSURE_EVIDENCE_OPEN'
assert req['CF-002']['collection_state']=='LOCAL_FOUNDATION_RECONFIRMED_CLOSURE_EVIDENCE_OPEN'
assert req['BA-001']['collection_state']=='EVIDENCE_UNAVAILABLE_EXPLICIT_GAP'
assert req['CF-001']['collection_state']=='EVIDENCE_UNAVAILABLE_EXPLICIT_GAP'
assert req['OJ-001']['collection_state']=='EVIDENCE_UNAVAILABLE_EXPLICIT_GAP'
assert len(read('lane-collection-status.tsv'))==6
assert len(read('root-gap-closure-observations.tsv'))==28
assert len(read('object-gap-closure-observations.tsv'))==37
m=meta()
assert m['candidate_evidence_files']=='0'
assert m['local_foundation_only_requirements']=='6'
assert m['explicit_unavailable_gap_requirements']=='10'
assert m['artifact_build_attestations_accepted']=='0'
assert m['final_provider_decisions_accepted']=='0'
assert m['target_rows_populated']=='0'
assert m['next_state']=='REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_RECEIPT'
PY

EVIDENCE="$TMP/evidence"
mkdir -p "$EVIDENCE/files"
printf '%s\n' 'digest-bound build invocation candidate' > "$EVIDENCE/files/build-record.txt"
printf '%s\n' 'bounded consumer reference candidate' > "$EVIDENCE/files/consumer-reference.txt"
printf '%s\n' 'authoritative workload reference candidate' > "$EVIDENCE/files/object-reference.txt"
python3 - "$EVIDENCE" <<'PY'
import csv, hashlib, pathlib, sys
root=pathlib.Path(sys.argv[1])
fields=['evidence_id','requirement_id','lane_id','scope_kind','scope_id','evidence_class','source_kind','source_locator','relative_path','sha256','size_bytes','claim_boundary']
items=[
 ('evidence:build','BA-001','GC-02','GLOBAL','ALL','DIGEST_BOUND_BUILD_INVOCATION','IMMUTABLE_BUILD_RECORD','fixture:build','files/build-record.txt'),
 ('evidence:consumer','CF-001','GC-05','GLOBAL','ALL','CONSUMER_BINDING_REFERENCE','CONSUMER_REFERENCE','fixture:consumer','files/consumer-reference.txt'),
 ('evidence:object','OJ-001','GC-01','GLOBAL','ALL','AUTHORITATIVE_OBJECT_REQUIREMENT_REFERENCE','AUTHORITATIVE_REFERENCE','fixture:object','files/object-reference.txt'),
]
rows=[]
for evidence_id,req,lane,scope_kind,scope_id,eclass,source_kind,locator,rel in items:
 p=root/rel
 rows.append(dict(evidence_id=evidence_id,requirement_id=req,lane_id=lane,scope_kind=scope_kind,scope_id=scope_id,evidence_class=eclass,source_kind=source_kind,source_locator=locator,relative_path=rel,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size_bytes=str(p.stat().st_size),claim_boundary='CANDIDATE_EVIDENCE_REVIEW_REQUIRED_NO_AUTHORITY_EFFECT'))
with (root/'evidence-manifest.tsv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY

OUT_PRESENT="$TMP/out-present"
PROJECT_REPO="$ROOT" \
OUT="$OUT_PRESENT" \
GENERIC_GAP_EVIDENCE_ROOT="$EVIDENCE" \
PYTHONDONTWRITEBYTECODE=1 \
python3 "$COLLECTOR"
python3 - "$OUT_PRESENT" <<'PY'
import csv, pathlib, sys
out=pathlib.Path(sys.argv[1])
def read(name):
    with (out/name).open(encoding='utf-8',newline='') as f: return list(csv.DictReader(f,delimiter='\t'))
req={r['requirement_id']:r for r in read('requirement-collection-status.tsv')}
assert req['BA-001']['collection_state']=='CANDIDATE_EVIDENCE_COLLECTED_REVIEW_REQUIRED'
assert req['CF-001']['collection_state']=='CANDIDATE_EVIDENCE_COLLECTED_REVIEW_REQUIRED'
assert req['OJ-001']['collection_state']=='CANDIDATE_EVIDENCE_COLLECTED_REVIEW_REQUIRED'
assert req['BA-003']['authority_state']=='OPEN_NO_ACCEPTANCE'
assert len(read('evidence-file-inventory.tsv'))==3
summary={r['field']:r['value'] for r in read('summary.tsv')}
assert summary['candidate_evidence_files']=='3'
assert summary['candidate_requirements']=='3'
assert summary['artifact_build_attestations_accepted']=='0'
assert summary['termux_android_adaptations_accepted']=='0'
assert summary['concrete_filename_drifts_accepted']=='0'
assert summary['final_provider_decisions_accepted']=='0'
PY

cp -a "$EVIDENCE" "$TMP/tampered"
printf '%s\n' 'tamper' >> "$TMP/tampered/files/build-record.txt"
if PROJECT_REPO="$ROOT" OUT="$TMP/out-tampered" GENERIC_GAP_EVIDENCE_ROOT="$TMP/tampered" PYTHONDONTWRITEBYTECODE=1 python3 "$COLLECTOR" >/dev/null 2>&1; then
    printf '%s\n' 'tampered evidence unexpectedly accepted' >&2
    exit 1
fi

cp -a "$EVIDENCE" "$TMP/unsafe"
python3 - "$TMP/unsafe/evidence-manifest.tsv" <<'PY'
import csv, pathlib, sys
p=pathlib.Path(sys.argv[1])
with p.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0])
rows[0]['relative_path']='../escape'
with p.open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if PROJECT_REPO="$ROOT" OUT="$TMP/out-unsafe" GENERIC_GAP_EVIDENCE_ROOT="$TMP/unsafe" PYTHONDONTWRITEBYTECODE=1 python3 "$COLLECTOR" >/dev/null 2>&1; then
    printf '%s\n' 'unsafe evidence path unexpectedly accepted' >&2
    exit 1
fi

printf '%s\n' 'GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_COLLECTOR_SMOKE_PASS'
