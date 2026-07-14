#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BASE="$ROOT/experiments/glibc/selected-obsidian-provider-authority"
REVIEW="$BASE/review"
RESPONSE="$BASE/evidence-supply/responses/SUP-01/SRQ-OJ-001"
REVIEWER="$BASE/recipe/review-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-01-response.py"
RULES="$REVIEW/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-response-review-rules.tsv"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
run_review() {
  local response=$1 out=$2
  rm -rf "$out"
  PYTHONDONTWRITEBYTECODE=1 python3 "$REVIEWER" \
    --source-contracts "$REVIEW/generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv" \
    --requirements "$REVIEW/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv" \
    --object-set "$REVIEW/generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv" \
    --supply-batches "$REVIEW/generic-build-attestation-adaptation-gap-evidence-supply-batches.tsv" \
    --supply-requests "$REVIEW/generic-build-attestation-adaptation-gap-evidence-supply-requests.tsv" \
    --response-dir "$response" \
    --rules "$RULES" \
    --out "$out"
}
run_review "$RESPONSE" "$TMP/review"
python3 - "$TMP/review" <<'PY'
import csv,pathlib,sys
out=pathlib.Path(sys.argv[1])
def rows(name):
    with (out/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
assert (out/'analysis.status').read_text()=='PASS\n'
assert (out/'next-state.txt').read_text().strip()=='FULFILL_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02'
r=rows('generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-response-review.tsv')
assert len(r)==1
assert r[0]['accepted_required_identity']=='libjpeg.so.62'
assert r[0]['rejected_substitute_identity']=='libjpeg.so.8'
assert r[0]['requirement_closure_state']=='OJ_001_CLOSED_BY_REQUIRED_IDENTITY_CORRECTION'
assert r[0]['final_provider_state']=='UNRESOLVED'
assert r[0]['target_population_state']=='UNPOPULATED'
o=rows('generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-object-review.tsv')
assert len(o)==1
assert o[0]['matching_provider_candidate_state']=='ABSENT_SUPPLY_STILL_REQUIRED'
meta={x['field']:x['value'] for x in rows('generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-01-response-review-metadata.tsv')}
assert meta['object_requirement_corrections_accepted']=='1'
assert meta['remaining_open_requirements']=='15'
assert meta['matching_soname_62_provider_candidates_bound']=='0'
assert meta['final_provider_decisions_accepted']=='0'
assert meta['target_rows_populated']=='0'
assert meta['next_batch']=='SUP-02'
PY

tamper_case() {
  local name=$1 py=$2
  local dir="$TMP/$name"
  cp -a "$RESPONSE" "$dir"
  python3 - "$dir" <<PY
$py
PY
  if run_review "$dir" "$TMP/out-$name" >/dev/null 2>&1; then
    echo "$name unexpectedly accepted" >&2; exit 1
  fi
}

tamper_case required_identity 'import csv,pathlib,sys
p=pathlib.Path(sys.argv[1])/"acquisition-input/object-requirement-correction-review.tsv"
with p.open(encoding="utf-8",newline="") as f:r=list(csv.DictReader(f,delimiter="\t")); fields=list(r[0])
r[0]["required_identity"]="libjpeg.so.8"
with p.open("w",encoding="utf-8",newline="") as f:w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(r)'

tamper_case invented_provider 'import csv,pathlib,sys
p=pathlib.Path(sys.argv[1])/"acquisition-input/object-requirement-correction-review.tsv"
with p.open(encoding="utf-8",newline="") as f:r=list(csv.DictReader(f,delimiter="\t")); fields=list(r[0])
r[0]["candidate_observed_family"] += ";libjpeg.so.62"
r[0]["provider_candidate_state"]="MATCHING_PROVIDER_BOUND"
with p.open("w",encoding="utf-8",newline="") as f:w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(r)'

tamper_case authority_promotion 'import csv,pathlib,sys
p=pathlib.Path(sys.argv[1])/"acquisition-input/object-requirement-correction-review.tsv"
with p.open(encoding="utf-8",newline="") as f:r=list(csv.DictReader(f,delimiter="\t")); fields=list(r[0])
r[0]["authority_state"]="ACCEPTED"
with p.open("w",encoding="utf-8",newline="") as f:w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(r)'

tamper_case reference_loss 'import csv,pathlib,sys
p=pathlib.Path(sys.argv[1])/"acquisition-input/object-requirement-correction-review.tsv"
with p.open(encoding="utf-8",newline="") as f:r=list(csv.DictReader(f,delimiter="\t")); fields=list(r[0])
r[0]["reference_locator"]="debian:trixie:libjpeg62-turbo:arm64:1%3A2.1.5-4:files"
with p.open("w",encoding="utf-8",newline="") as f:w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(r)'

printf '%s\n' 'GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_01_RESPONSE_REVIEW_SMOKE_PASS'
