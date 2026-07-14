#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
base="$repo_root/experiments/glibc/selected-obsidian-provider-authority"
review="$base/review"
definer="$base/recipe/define-generic-build-attestation-and-adaptation-gap-evidence-acquisition-set.py"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

run_definer() {
    local out=$1
    local req_review=${2:-$review/generic-build-attestation-adaptation-gap-closure-receipt-review.tsv}
    local root_review=${3:-$review/generic-build-attestation-adaptation-root-gap-closure-receipt-review.tsv}
    local object_review=${4:-$review/generic-build-attestation-adaptation-object-gap-closure-receipt-review.tsv}
    local source_meta=${5:-$review/generic-build-attestation-adaptation-gap-closure-receipt-review-metadata.tsv}
    rm -rf "$out"
    PYTHONDONTWRITEBYTECODE=1 python3 "$definer" \
      --lanes "$review/generic-build-attestation-adaptation-gap-closure-lanes.tsv" \
      --requirements "$review/generic-build-attestation-adaptation-gap-closure-requirements.tsv" \
      --requirement-review "$req_review" \
      --lane-review "$review/generic-build-attestation-adaptation-gap-closure-lane-receipt-review.tsv" \
      --root-review "$root_review" \
      --object-review "$object_review" \
      --source-metadata "$source_meta" \
      --out "$out"
}

run_definer "$tmp/pass" >/dev/null
for file in \
  generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv \
  generic-build-attestation-adaptation-gap-evidence-acquisition-lanes.tsv \
  generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv \
  generic-build-attestation-adaptation-root-gap-evidence-acquisition-set.tsv \
  generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv \
  generic-build-attestation-adaptation-gap-evidence-acquisition-set-metadata.tsv; do
    cmp "$tmp/pass/$file" "$review/$file"
done
grep -qx PASS "$tmp/pass/analysis.status"
grep -qx CANDIDATE_EVIDENCE_REVIEW_REQUIRED_NO_AUTHORITY_EFFECT "$tmp/pass/claim-boundary.txt"
grep -qx IMPLEMENT_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUIRER "$tmp/pass/next-state.txt"

python3 - "$review/generic-build-attestation-adaptation-gap-closure-receipt-review.tsv" "$tmp/bad-requirement.tsv" <<'PY'
import csv,sys
src,dst=sys.argv[1:]
with open(src,newline='') as f: rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0])
rows[0]['candidate_evidence_count']='1'
with open(dst,'w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if run_definer "$tmp/bad1" "$tmp/bad-requirement.tsv" >/dev/null 2>&1; then
    echo 'candidate count drift unexpectedly passed' >&2; exit 1
fi

python3 - "$review/generic-build-attestation-adaptation-root-gap-closure-receipt-review.tsv" "$tmp/bad-root.tsv" <<'PY'
import csv,sys
src,dst=sys.argv[1:]
with open(src,newline='') as f: rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0])
rows[0]['authority_state']='ACCEPTED'
with open(dst,'w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if run_definer "$tmp/bad2" "$review/generic-build-attestation-adaptation-gap-closure-receipt-review.tsv" "$tmp/bad-root.tsv" >/dev/null 2>&1; then
    echo 'root authority promotion unexpectedly passed' >&2; exit 1
fi

python3 - "$review/generic-build-attestation-adaptation-object-gap-closure-receipt-review.tsv" "$tmp/bad-object.tsv" <<'PY'
import csv,sys
src,dst=sys.argv[1:]
with open(src,newline='') as f: rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0])
rows[0]['target_population_state']='POPULATED'
with open(dst,'w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if run_definer "$tmp/bad3" "$review/generic-build-attestation-adaptation-gap-closure-receipt-review.tsv" "$review/generic-build-attestation-adaptation-root-gap-closure-receipt-review.tsv" "$tmp/bad-object.tsv" >/dev/null 2>&1; then
    echo 'object target promotion unexpectedly passed' >&2; exit 1
fi

python3 - "$review/generic-build-attestation-adaptation-gap-closure-receipt-review-metadata.tsv" "$tmp/bad-meta.tsv" <<'PY'
import csv,sys
src,dst=sys.argv[1:]
with open(src,newline='') as f: rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0])
for row in rows:
 if row['field']=='next_state': row['value']='WRONG_STATE'
with open(dst,'w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if run_definer "$tmp/bad4" "$review/generic-build-attestation-adaptation-gap-closure-receipt-review.tsv" "$review/generic-build-attestation-adaptation-root-gap-closure-receipt-review.tsv" "$review/generic-build-attestation-adaptation-object-gap-closure-receipt-review.tsv" "$tmp/bad-meta.tsv" >/dev/null 2>&1; then
    echo 'source next-state drift unexpectedly passed' >&2; exit 1
fi

python3 - "$review/generic-build-attestation-adaptation-gap-evidence-acquisition-set-metadata.tsv" <<'PY'
import csv,sys
with open(sys.argv[1],newline='') as f: m={r['field']:r['value'] for r in csv.DictReader(f,delimiter='\t')}
expected={
 'closure_lane_rows':'6','requirement_rows':'16','direct_gap_requirement_rows':'10',
 'local_foundation_completion_rows':'6','source_contract_rows':'10',
 'root_acquisition_rows':'28','object_acquisition_rows':'37',
 'root_requirement_edges':'303','object_requirement_edges':'414',
 'candidate_evidence_files_acquired':'0','artifact_build_attestations_accepted':'0',
 'termux_android_adaptations_accepted':'0','concrete_filename_drifts_accepted':'0',
 'object_corrections_accepted':'0','final_provider_decisions_accepted':'0',
 'target_rows_populated':'0',
 'next_state':'IMPLEMENT_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUIRER',
}
for k,v in expected.items(): assert m.get(k)==v,(k,m.get(k),v)
PY

echo GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUISITION_SET_SMOKE_PASS
