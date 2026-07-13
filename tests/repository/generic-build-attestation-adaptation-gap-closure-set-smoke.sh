#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
repo=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
review="$repo/experiments/glibc/selected-obsidian-provider-authority/review"
definer="$repo/experiments/glibc/selected-obsidian-provider-authority/recipe/define-generic-build-attestation-and-adaptation-gap-closure-set.py"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

run_definer() {
    local out=$1 req_review=${2:-$review/generic-build-attestation-adaptation-evidence-receipt-review.tsv} root_review=${3:-$review/generic-build-attestation-adaptation-root-evidence-receipt-review.tsv} object_review=${4:-$review/generic-build-attestation-adaptation-object-evidence-receipt-review.tsv}
    python3 "$definer" \
      --requirements "$review/generic-build-attestation-adaptation-review-requirements.tsv" \
      --root-review-set "$review/generic-build-attestation-adaptation-root-review-set.tsv" \
      --object-review-set "$review/generic-build-attestation-adaptation-object-review-set.tsv" \
      --requirement-receipt-review "$req_review" \
      --root-receipt-review "$root_review" \
      --object-receipt-review "$object_review" \
      --source-metadata "$review/generic-build-attestation-adaptation-evidence-receipt-metadata.tsv" \
      --out "$out"
}

run_definer "$tmp/out" >/dev/null
for name in \
 generic-build-attestation-adaptation-gap-closure-lanes.tsv \
 generic-build-attestation-adaptation-gap-closure-requirements.tsv \
 generic-build-attestation-adaptation-root-gap-closure-set.tsv \
 generic-build-attestation-adaptation-object-gap-closure-set.tsv \
 generic-build-attestation-adaptation-gap-closure-set-metadata.tsv; do
    cmp "$tmp/out/$name" "$review/$name"
done

python3 - "$review/generic-build-attestation-adaptation-evidence-receipt-review.tsv" "$tmp/bad-requirement.tsv" <<'PY'
import csv,sys
src,dst=sys.argv[1:]
with open(src,newline='') as f: rows=list(csv.DictReader(f,delimiter='\t')); fields=rows[0].keys()
rows[0]['authority_state']='ACCEPTED'
with open(dst,'w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if run_definer "$tmp/bad1" "$tmp/bad-requirement.tsv" >/dev/null 2>&1; then echo 'authority promotion negative test unexpectedly passed' >&2; exit 1; fi

python3 - "$review/generic-build-attestation-adaptation-root-evidence-receipt-review.tsv" "$tmp/bad-root.tsv" <<'PY'
import csv,sys
src,dst=sys.argv[1:]
with open(src,newline='') as f: rows=list(csv.DictReader(f,delimiter='\t')); fields=rows[0].keys()
rows[0]['recipe_tree']='0'*40
with open(dst,'w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if run_definer "$tmp/bad2" "$review/generic-build-attestation-adaptation-evidence-receipt-review.tsv" "$tmp/bad-root.tsv" >/dev/null 2>&1; then echo 'root drift negative test unexpectedly passed' >&2; exit 1; fi

python3 - "$review/generic-build-attestation-adaptation-object-evidence-receipt-review.tsv" "$tmp/bad-object.tsv" <<'PY'
import csv,sys
src,dst=sys.argv[1:]
with open(src,newline='') as f: rows=list(csv.DictReader(f,delimiter='\t')); fields=rows[0].keys()
rows[0]['target_population_state']='POPULATED'
with open(dst,'w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if run_definer "$tmp/bad3" "$review/generic-build-attestation-adaptation-evidence-receipt-review.tsv" "$review/generic-build-attestation-adaptation-root-evidence-receipt-review.tsv" "$tmp/bad-object.tsv" >/dev/null 2>&1; then echo 'target population negative test unexpectedly passed' >&2; exit 1; fi

python3 - "$review/generic-build-attestation-adaptation-gap-closure-set-metadata.tsv" <<'PY'
import csv,sys
with open(sys.argv[1],newline='') as f: m={r['field']:r['value'] for r in csv.DictReader(f,delimiter='\t')}
expected={'closure_lane_rows':'6','requirement_rows':'16','direct_gap_requirement_rows':'10','local_foundation_completion_rows':'6','root_work_units':'28','object_work_units':'37','exact_object_work_units':'21','drift_object_work_units':'15','blocked_object_work_units':'1','artifact_build_attestations_accepted':'0','termux_android_adaptations_accepted':'0','concrete_filename_drifts_accepted':'0','final_provider_decisions_accepted':'0','target_rows_populated':'0','next_state':'IMPLEMENT_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_COLLECTOR'}
for k,v in expected.items():
 assert m.get(k)==v,(k,m.get(k),v)
PY

echo GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_CLOSURE_SET_SMOKE_PASS
