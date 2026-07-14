#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
base="$repo_root/experiments/glibc/selected-obsidian-provider-authority"
review="$base/review"
collector="$base/recipe/collect-generic-build-attestation-and-adaptation-gap-closure.py"
reviewer="$base/recipe/review-generic-build-attestation-and-adaptation-gap-closure-receipt.py"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
collection="$tmp/collection"
missing_evidence="$tmp/missing-evidence"

PROJECT_REPO="$repo_root" \
OUT="$collection" \
GENERIC_GAP_EVIDENCE_ROOT="$missing_evidence" \
PYTHONDONTWRITEBYTECODE=1 \
python3 "$collector" >/dev/null

cat > "$tmp/transaction-status.txt" <<'EOF'
TRANSACTION=PASS
VALIDATION=PASS
GAP_CLOSURE_COLLECTOR=PASS_BOUNDED
PUSH_AFTER_APPLY=1
EOF
cat > "$tmp/final-git-state.txt" <<'EOF'
branch=docs/post-graphics-architecture-audit
head=ac0ed827321bc3e42c8c81b533ad024cd7b1ed69
tree=b86d78c327f6fad99578f29120e8c08156b0a359
EOF
cat > "$tmp/remote-state.txt" <<'EOF'
push_after_apply=1
remote_head_before=afeb058fa062e728994bbd4b075c52279c245195
remote_head_after=ac0ed827321bc3e42c8c81b533ad024cd7b1ed69
EOF
cat > "$tmp/collector-input.txt" <<EOF
evidence_root=$missing_evidence
state=ABSENT_NO_CANDIDATE_EVIDENCE
EOF

run_review() {
    local out=$1
    local input_verification=${INPUT_VERIFICATION_INPUT:-$collection/input-verification.tsv}
    local requirement_status=${REQUIREMENT_STATUS_INPUT:-$collection/requirement-collection-status.tsv}
    local object_observations=${OBJECT_OBSERVATIONS_INPUT:-$collection/object-gap-closure-observations.tsv}
    local final_git_state=${FINAL_GIT_STATE_INPUT:-$tmp/final-git-state.txt}
    rm -rf "$out"
    PYTHONDONTWRITEBYTECODE=1 python3 "$reviewer" \
      --lanes "$review/generic-build-attestation-adaptation-gap-closure-lanes.tsv" \
      --requirements "$review/generic-build-attestation-adaptation-gap-closure-requirements.tsv" \
      --root-set "$review/generic-build-attestation-adaptation-root-gap-closure-set.tsv" \
      --object-set "$review/generic-build-attestation-adaptation-object-gap-closure-set.tsv" \
      --rules "$review/generic-build-attestation-adaptation-gap-closure-receipt-review-rules.tsv" \
      --input-verification "$input_verification" \
      --evidence-inventory "$collection/evidence-file-inventory.tsv" \
      --requirement-status "$requirement_status" \
      --lane-status "$collection/lane-collection-status.tsv" \
      --root-observations "$collection/root-gap-closure-observations.tsv" \
      --object-observations "$object_observations" \
      --unavailable-gaps "$collection/unavailable-evidence-gaps.tsv" \
      --summary "$collection/summary.tsv" \
      --analysis-status "$collection/analysis.status" \
      --claim-boundary "$collection/claim-boundary.txt" \
      --collector-next-state "$collection/next-state.txt" \
      --collector-input "$tmp/collector-input.txt" \
      --transaction-status "$tmp/transaction-status.txt" \
      --final-git-state "$final_git_state" \
      --remote-state "$tmp/remote-state.txt" \
      --source-receipt-archive termux-native-desktop-gap-closure-collector-result-20260713T234326Z.tar.zst \
      --source-receipt-sha256 35560345126fcc7a50b61beece5a04d44f85af4ad12a610bfba1df670c37196d \
      --out "$out"
}

run_review "$tmp/review-pass" >/dev/null
for file in \
  generic-build-attestation-adaptation-gap-closure-receipt-review.tsv \
  generic-build-attestation-adaptation-gap-closure-lane-receipt-review.tsv \
  generic-build-attestation-adaptation-root-gap-closure-receipt-review.tsv \
  generic-build-attestation-adaptation-object-gap-closure-receipt-review.tsv \
  generic-build-attestation-adaptation-gap-closure-receipt-review-metadata.tsv; do
    cmp "$tmp/review-pass/$file" "$review/$file"
done

grep -qx 'PASS' "$tmp/review-pass/analysis.status"
grep -qx 'DEFINE_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUISITION_SET' "$tmp/review-pass/next-state.txt"

cp "$collection/requirement-collection-status.tsv" "$tmp/bad-requirement.tsv"
python3 - "$tmp/bad-requirement.tsv" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text()
s=s.replace('BA-001\tGC-02\tBUILD_ATTESTATION\tROOT\tDIRECT_GAP\tNONE\tNONE\t0\tEVIDENCE_UNAVAILABLE_EXPLICIT_GAP',
            'BA-001\tGC-02\tBUILD_ATTESTATION\tROOT\tDIRECT_GAP\tNONE\tEV-FAKE\t1\tCANDIDATE_EVIDENCE_COLLECTED_REVIEW_REQUIRED', 1)
p.write_text(s)
PY
if REQUIREMENT_STATUS_INPUT="$tmp/bad-requirement.tsv" run_review "$tmp/review-bad-requirement" >/dev/null 2>&1; then
    echo 'candidate evidence drift was not rejected' >&2
    exit 1
fi

cp "$collection/object-gap-closure-observations.tsv" "$tmp/bad-object.tsv"
python3 - "$tmp/bad-object.tsv" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text().replace('\tUNRESOLVED\tOPEN_NO_ACCEPTANCE\tUNPOPULATED\n',
                         '\tACCEPTED\tACCEPTED\tPOPULATED\n', 1)
p.write_text(s)
PY
if OBJECT_OBSERVATIONS_INPUT="$tmp/bad-object.tsv" run_review "$tmp/review-bad-object" >/dev/null 2>&1; then
    echo 'authority promotion was not rejected' >&2
    exit 1
fi

cp "$collection/input-verification.tsv" "$tmp/bad-input-verification.tsv"
python3 - "$tmp/bad-input-verification.tsv" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text().replace('b6683d11ce96795cb4fa0da177adfe0cd7eb39206aead1ec55df3cf7b4800cc1', '0'*64, 1)
p.write_text(s)
PY
if INPUT_VERIFICATION_INPUT="$tmp/bad-input-verification.tsv" run_review "$tmp/review-bad-input" >/dev/null 2>&1; then
    echo 'canonical input hash drift was not rejected' >&2
    exit 1
fi

cp "$tmp/final-git-state.txt" "$tmp/bad-final-git-state.txt"
sed -i 's/ac0ed827321bc3e42c8c81b533ad024cd7b1ed69/0000000000000000000000000000000000000000/' "$tmp/bad-final-git-state.txt"
if FINAL_GIT_STATE_INPUT="$tmp/bad-final-git-state.txt" run_review "$tmp/review-bad-git" >/dev/null 2>&1; then
    echo 'source Git identity drift was not rejected' >&2
    exit 1
fi

echo 'generic build attestation/adaptation gap-closure receipt review smoke: PASS'
