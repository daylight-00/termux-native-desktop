#!/usr/bin/env bash
set -euo pipefail
repo=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
base="$repo/experiments/glibc/selected-obsidian-provider-authority"
review="$base/review"
recipe="$base/recipe/define-generic-build-attestation-and-adaptation-gap-evidence-supply-request-set.py"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
export PYTHONDONTWRITEBYTECODE=1

run_definer() {
    local out=$1
    local requirements=${2:-$review/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv}
    local objects=${3:-$review/generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv}
    local receipt=${4:-$review/generic-build-attestation-adaptation-gap-evidence-acquisition-receipt-review.tsv}
    python3 "$recipe" \
        --source-contracts "$review/generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv" \
        --lanes "$review/generic-build-attestation-adaptation-gap-evidence-acquisition-lanes.tsv" \
        --requirements "$requirements" \
        --root-set "$review/generic-build-attestation-adaptation-root-gap-evidence-acquisition-set.tsv" \
        --object-set "$objects" \
        --receipt-review "$receipt" \
        --receipt-metadata "$review/generic-build-attestation-adaptation-gap-evidence-acquisition-receipt-review-metadata.tsv" \
        --out "$out"
}

run_definer "$tmp/out"
for name in \
    generic-build-attestation-adaptation-gap-evidence-supply-batches.tsv \
    generic-build-attestation-adaptation-gap-evidence-supply-requests.tsv \
    generic-build-attestation-adaptation-root-gap-evidence-supply-request-set.tsv \
    generic-build-attestation-adaptation-object-gap-evidence-supply-request-set.tsv \
    generic-build-attestation-adaptation-gap-evidence-supply-request-set-metadata.tsv
do
    cmp "$tmp/out/$name" "$review/$name"
done

python3 - "$review" <<'PY'
import csv, pathlib, sys
review=pathlib.Path(sys.argv[1])
def rows(name):
    with (review/name).open(newline='') as f:
        return list(csv.DictReader(f,delimiter='\t'))
requests=rows('generic-build-attestation-adaptation-gap-evidence-supply-requests.tsv')
batches=rows('generic-build-attestation-adaptation-gap-evidence-supply-batches.tsv')
roots=rows('generic-build-attestation-adaptation-root-gap-evidence-supply-request-set.tsv')
objects=rows('generic-build-attestation-adaptation-object-gap-evidence-supply-request-set.tsv')
meta={r['field']:r['value'] for r in rows('generic-build-attestation-adaptation-gap-evidence-supply-request-set-metadata.tsv')}
assert len(batches)==6
assert len(requests)==16 and len({r['requirement_id'] for r in requests})==16
assert len(roots)==28 and len(objects)==37
by_req={r['requirement_id']:r for r in requests}
assert by_req['OJ-001']['batch_id']=='SUP-01'
assert by_req['OJ-001']['next_action']=='PREPARE_SUP_01_AUTHORITATIVE_CORRECTION_RESPONSE'
assert by_req['OJ-001']['root_unit_count']=='1' and by_req['OJ-001']['object_unit_count']=='1'
for req in ('CF-002','CF-003','CF-004'):
    assert by_req[req]['dependency_component_kind']=='CYCLIC_ITERATIVE'
    assert by_req[req]['dependency_component_members']=='CF-002;CF-003;CF-004'
assert len({by_req[r]['dependency_component_id'] for r in ('CF-002','CF-003','CF-004')})==1
assert all(r['request_state']=='REQUEST_DEFINED_NOT_ISSUED' and r['responses_received']=='0' for r in requests)
assert all(r['authority_state']=='OPEN_NO_ACCEPTANCE' for r in requests+roots+objects)
assert all(r['final_provider_state']=='UNRESOLVED' and r['target_population_state']=='UNPOPULATED' for r in objects)
assert 'libjpeg.so.8' not in '\n'.join('\t'.join(r.values()) for r in requests+batches)
expected={
 'source_contract_rows':'10','closure_lane_rows':'6','requirement_request_rows':'16','supply_batch_rows':'6',
 'dependency_component_rows':'14','cyclic_dependency_component_rows':'1','cyclic_dependency_requirement_rows':'3',
 'root_supply_request_rows':'28','object_supply_request_rows':'37','root_request_edges':'303','object_request_edges':'414',
 'agent_reference_request_rows':'1','producer_custodian_request_rows':'3','independent_witness_request_rows':'1',
 'agent_semantic_request_rows':'5','device_capture_request_rows':'1','agent_consumer_review_request_rows':'1',
 'agent_policy_request_rows':'4','requests_issued':'0','responses_received':'0','candidate_evidence_files_acquired':'0',
 'artifact_build_attestations_accepted':'0','termux_android_adaptations_accepted':'0',
 'concrete_filename_drifts_accepted':'0','object_corrections_accepted':'0','final_provider_decisions_accepted':'0',
 'target_rows_populated':'0','first_batch_id':'SUP-01',
 'claim_boundary':'SUPPLY_REQUEST_ONLY_NO_EVIDENCE_OR_AUTHORITY_EFFECT',
 'next_state':'FULFILL_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_01',
}
for key,value in expected.items():
    assert meta.get(key)==value,(key,meta.get(key),value)
PY

python3 - "$review/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv" "$tmp/bad-requirements.tsv" <<'PY'
import csv,sys
src,dst=sys.argv[1:]
with open(src,newline='') as f: rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0])
for row in rows:
    if row['requirement_id']=='CF-003': row['dependency_requirement_ids']='CF-001'
with open(dst,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if run_definer "$tmp/bad-cycle" "$tmp/bad-requirements.tsv" >/dev/null 2>&1; then
    echo 'dependency drift unexpectedly passed' >&2; exit 1
fi

python3 - "$review/generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv" "$tmp/bad-objects.tsv" <<'PY'
import csv,sys
src,dst=sys.argv[1:]
with open(src,newline='') as f: rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0])
rows[0]['authority_state']='ACCEPTED'
with open(dst,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if run_definer "$tmp/bad-object" "$review/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv" "$tmp/bad-objects.tsv" >/dev/null 2>&1; then
    echo 'object authority promotion unexpectedly passed' >&2; exit 1
fi

python3 - "$review/generic-build-attestation-adaptation-gap-evidence-acquisition-receipt-review.tsv" "$tmp/bad-receipt.tsv" <<'PY'
import csv,sys
src,dst=sys.argv[1:]
with open(src,newline='') as f: rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0])
rows[0]['candidate_input_count']='1'
with open(dst,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if run_definer "$tmp/bad-receipt" "$review/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv" "$review/generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv" "$tmp/bad-receipt.tsv" >/dev/null 2>&1; then
    echo 'candidate invention unexpectedly passed' >&2; exit 1
fi

if run_definer "$tmp/out" >/dev/null 2>&1; then
    echo 'existing output unexpectedly accepted' >&2; exit 1
fi

python3 -m py_compile "$recipe"
echo GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_REQUEST_SET_SMOKE_PASS
