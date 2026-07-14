#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BASE="$ROOT/experiments/glibc/selected-obsidian-provider-authority"
REVIEW="$BASE/review"
ACQUIRER="$BASE/recipe/acquire-generic-build-attestation-and-adaptation-gap-evidence.py"
REVIEWER="$BASE/recipe/review-generic-build-attestation-and-adaptation-gap-evidence-acquisition-receipt.py"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

run_acquirer() {
    local out=$1
    rm -rf "$out"
    PYTHONDONTWRITEBYTECODE=1 python3 "$ACQUIRER" \
      --source-contracts "$REVIEW/generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv" \
      --lanes "$REVIEW/generic-build-attestation-adaptation-gap-evidence-acquisition-lanes.tsv" \
      --requirements "$REVIEW/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv" \
      --roots "$REVIEW/generic-build-attestation-adaptation-root-gap-evidence-acquisition-set.tsv" \
      --objects "$REVIEW/generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv" \
      --input-root "$TMP/absent-input" \
      --out "$out"
}

write_receipt_metadata() {
    local dir=$1
    cat > "$dir/transaction-status.txt" <<'EOF'
TRANSACTION=PASS
VALIDATION=PASS
GAP_EVIDENCE_ACQUIRER=PASS_BOUNDED
PUSH_AFTER_APPLY=1
EOF
    cat > "$dir/final-git-state.txt" <<'EOF'
branch=docs/post-graphics-architecture-audit
head=54afd42dcce27be00d70550facb5e0ceb391ce38
tree=8c34d8987c98923a3b623a4d1be5304fe20b4964
EOF
    cat > "$dir/remote-state.txt" <<'EOF'
push_after_apply=1
remote_head_before=67049e95c18063b432b9d962cbaa9ccda89bb2c9
remote_head_after=54afd42dcce27be00d70550facb5e0ceb391ce38
EOF
    cat > "$dir/acquirer-input.txt" <<EOF
input_root=$TMP/absent-input
input_state=ABSENT_NO_ACQUISITION_INPUT
candidate_evidence_files=0
EOF
}

run_review() {
    local receipt=$1 out=$2
    local acq="$receipt/gap-evidence-acquisition"
    rm -rf "$out"
    PYTHONDONTWRITEBYTECODE=1 python3 "$REVIEWER" \
      --source-contracts "$REVIEW/generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv" \
      --lanes "$REVIEW/generic-build-attestation-adaptation-gap-evidence-acquisition-lanes.tsv" \
      --requirements "$REVIEW/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv" \
      --root-set "$REVIEW/generic-build-attestation-adaptation-root-gap-evidence-acquisition-set.tsv" \
      --object-set "$REVIEW/generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv" \
      --rules "$REVIEW/generic-build-attestation-adaptation-gap-evidence-acquisition-receipt-review-rules.tsv" \
      --input-verification "$acq/input-verification.tsv" \
      --acquisition-inventory "$acq/acquisition-file-inventory.tsv" \
      --requirement-status "$acq/requirement-acquisition-status.tsv" \
      --lane-status "$acq/lane-acquisition-status.tsv" \
      --root-status "$acq/root-acquisition-status.tsv" \
      --object-status "$acq/object-acquisition-status.tsv" \
      --unavailable-inputs "$acq/unavailable-acquisition-inputs.tsv" \
      --evidence-manifest "$acq/evidence-root/evidence-manifest.tsv" \
      --summary "$acq/summary.tsv" \
      --analysis-status "$acq/analysis.status" \
      --claim-boundary "$acq/claim-boundary.txt" \
      --acquirer-next-state "$acq/next-state.txt" \
      --acquirer-input "$receipt/acquirer-input.txt" \
      --transaction-status "$receipt/transaction-status.txt" \
      --final-git-state "$receipt/final-git-state.txt" \
      --remote-state "$receipt/remote-state.txt" \
      --source-receipt-archive fixture-gap-evidence-acquirer-result.tar.zst \
      --source-receipt-sha256 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef \
      --out "$out"
}

RECEIPT="$TMP/receipt"
mkdir -p "$RECEIPT"
run_acquirer "$RECEIPT/gap-evidence-acquisition"
write_receipt_metadata "$RECEIPT"
run_review "$RECEIPT" "$TMP/review"

python3 - "$TMP/review" <<'PY'
import csv,pathlib,sys
out=pathlib.Path(sys.argv[1])
def rows(name):
    with (out/name).open(encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f,delimiter='\t'))
assert (out/'analysis.status').read_text()=='PASS\n'
assert (out/'next-state.txt').read_text().strip()=='DEFINE_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_REQUEST_SET'
assert len(rows('generic-build-attestation-adaptation-gap-evidence-acquisition-receipt-review.tsv'))==16
assert len(rows('generic-build-attestation-adaptation-gap-evidence-acquisition-lane-receipt-review.tsv'))==6
assert len(rows('generic-build-attestation-adaptation-root-gap-evidence-acquisition-receipt-review.tsv'))==28
assert len(rows('generic-build-attestation-adaptation-object-gap-evidence-acquisition-receipt-review.tsv'))==37
meta={r['field']:r['value'] for r in rows('generic-build-attestation-adaptation-gap-evidence-acquisition-receipt-review-metadata.tsv')}
assert meta['candidate_evidence_files']=='0'
assert meta['local_foundation_only_requirements']=='6'
assert meta['direct_gap_unavailable_requirements']=='10'
assert meta['artifact_build_attestations_accepted']=='0'
assert meta['final_provider_decisions_accepted']=='0'
assert meta['target_rows_populated']=='0'
for row in rows('generic-build-attestation-adaptation-object-gap-evidence-acquisition-receipt-review.tsv'):
    assert row['final_provider_state']=='UNRESOLVED'
    assert row['authority_state']=='OPEN_NO_ACCEPTANCE'
    assert row['target_population_state']=='UNPOPULATED'
PY

cp -a "$RECEIPT" "$TMP/tampered-summary"
python3 - "$TMP/tampered-summary/gap-evidence-acquisition/summary.tsv" <<'PY'
import csv,pathlib,sys
p=pathlib.Path(sys.argv[1])
with p.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
for row in rows:
    if row['field']=='candidate_evidence_files_acquired': row['value']='1'
with p.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['field','value'],delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if run_review "$TMP/tampered-summary" "$TMP/review-bad-summary" >/dev/null 2>&1; then
    echo 'tampered candidate count unexpectedly accepted' >&2; exit 1
fi

cp -a "$RECEIPT" "$TMP/tampered-authority"
python3 - "$TMP/tampered-authority/gap-evidence-acquisition/object-acquisition-status.tsv" <<'PY'
import csv,pathlib,sys
p=pathlib.Path(sys.argv[1])
with p.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0])
rows[0]['authority_state']='ACCEPTED'
with p.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if run_review "$TMP/tampered-authority" "$TMP/review-bad-authority" >/dev/null 2>&1; then
    echo 'authority promotion unexpectedly accepted' >&2; exit 1
fi

cp -a "$RECEIPT" "$TMP/tampered-manifest"
printf '%s\n' 'fixture-row' >> "$TMP/tampered-manifest/gap-evidence-acquisition/evidence-root/evidence-manifest.tsv"
if run_review "$TMP/tampered-manifest" "$TMP/review-bad-manifest" >/dev/null 2>&1; then
    echo 'non-empty evidence manifest unexpectedly accepted' >&2; exit 1
fi

printf '%s\n' 'GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUISITION_RECEIPT_REVIEW_SMOKE_PASS'
