#!/usr/bin/env bash
set -euo pipefail

REPO=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
REVIEWER="$REPO/experiments/glibc/selected-obsidian-provider-authority/recipe/review-generic-exact-candidate-evidence.py"
RULES="$REPO/experiments/glibc/selected-obsidian-provider-authority/review/generic-exact-candidate-review-rules.tsv"
REVIEW="$REPO/experiments/glibc/selected-obsidian-provider-authority/review/generic-exact-candidate-receipt-review.tsv"
META="$REPO/experiments/glibc/selected-obsidian-provider-authority/review/generic-exact-candidate-receipt-metadata.tsv"

fail() {
    printf 'generic exact candidate receipt review smoke: FAIL: %s\n' "$*" >&2
    exit 1
}

[ -x "$REVIEWER" ] || fail "missing executable reviewer"
[ -f "$RULES" ] || fail "missing review rules"
[ -f "$REVIEW" ] || fail "missing reviewed receipt"
[ -f "$META" ] || fail "missing receipt metadata"
[ "$(awk 'END {print NR-1}' "$RULES")" -eq 61 ] || fail "rule denominator is not 61"
[ "$(awk 'END {print NR-1}' "$REVIEW")" -eq 61 ] || fail "review denominator is not 61"
awk -F '\t' 'NR > 1 && ($5 != "FAMILY_NAME_MATCH_ONLY_NOT_AUTHORITY" || $6 != "CANDIDATE_ONLY") {exit 1}' "$RULES" || fail "rule authority boundary drift"
awk -F '\t' 'NR > 1 && ($10 != "OPEN_NO_DEB_EXTRACTION" || $11 != "UNRESOLVED" || $12 != "BLOCKED") {exit 1}' "$REVIEW" || fail "review promoted authority"
[ "$(awk -F '\t' 'NR > 1 && $9 == "DIRECT_APT_AND_RECIPE_FAMILY_CANDIDATE" {n++} END {print n+0}' "$REVIEW")" -eq 37 ] || fail "direct-family count drift"
[ "$(awk -F '\t' 'NR > 1 && $9 == "INDIRECT_TOKEN_ONLY" {n++} END {print n+0}' "$REVIEW")" -eq 13 ] || fail "indirect-only count drift"
[ "$(awk -F '\t' 'NR > 1 && $9 == "NO_RETAINED_CANDIDATE" {n++} END {print n+0}' "$REVIEW")" -eq 11 ] || fail "no-candidate count drift"
[ "$(awk -F '\t' '$1 == "receipt_review_sha256" {print $2}' "$META")" = "$(sha256sum "$REVIEW" | awk '{print $1}')" ] || fail "review hash drift"
[ "$(awk -F '\t' '$1 == "authority_decisions_accepted" {print $2}' "$META")" = 0 ] || fail "metadata accepted authority"
[ "$(awk -F '\t' '$1 == "deb_extraction_performed" {print $2}' "$META")" = NO ] || fail "metadata claims deb extraction"

python3 -m py_compile "$REVIEWER"
for forbidden in \
    '\["apt",[[:space:]]*"(update|install|download|remove|upgrade|full-upgrade)"' \
    '\["git",[[:space:]]*"(fetch|pull|clone)"' \
    '\["(curl|wget)"' \
    '\["dpkg-deb",[[:space:]]*"(-x|--extract)"'; do
    if grep -E "$forbidden" "$REVIEWER" >/dev/null; then
        fail "forbidden mutating/network command appears: $forbidden"
    fi
done

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
EVIDENCE="$TMP/evidence"
OUT="$TMP/out"
mkdir -p "$EVIDENCE"
cat > "$EVIDENCE/apt-candidate-records.tsv" <<'EOF'
evidence_row_id	capability_partition	lookup_name	candidate_package	candidate_version	architecture	match_tokens	index_file	index_sha256	repository_filename	artifact_size	artifact_sha256	source_field	candidate_state	object_member_binding_state	authority_state
EOF
cat > "$EVIDENCE/recipe-candidate-records.tsv" <<'EOF'
evidence_row_id	capability_partition	lookup_name	candidate_package	recipe_root	recipe_tree	candidate_version	candidate_revision	match_tokens	source_url	source_sha256	depends	build_depends	candidate_state	artifact_build_binding_state	authority_state
EOF
FIRST_ID=$(awk -F '\t' 'NR == 2 {print $1}' "$RULES")
FIRST_PART=$(awk -F '\t' 'NR == 2 {print $2}' "$RULES")
FIRST_LABEL=$(awk -F '\t' 'NR == 2 {print $3}' "$RULES")
FIRST_ROOT=$(awk -F '\t' 'NR == 2 {split($4,a,";"); print a[1]}' "$RULES")
SECOND_ID=$(awk -F '\t' 'NR == 3 {print $1}' "$RULES")
SECOND_PART=$(awk -F '\t' 'NR == 3 {print $2}' "$RULES")
SECOND_LABEL=$(awk -F '\t' 'NR == 3 {print $3}' "$RULES")
printf '%s\t%s\t%s\t%s-glibc\t1\taarch64\t%s\tindex\tsha\tpool/x.deb\t1\tsha\t-\tCANDIDATE\tOPEN\tCANDIDATE_ONLY\n' \
    "$FIRST_ID" "$FIRST_PART" "$FIRST_LABEL" "$FIRST_ROOT" "$FIRST_ROOT" >> "$EVIDENCE/apt-candidate-records.tsv"
printf '%s\t%s\t%s\t%s\tgpkg/%s\ttree\t1\t0\t%s\turl\tsha\t-\t-\tCANDIDATE\tOPEN\tCANDIDATE_ONLY\n' \
    "$FIRST_ID" "$FIRST_PART" "$FIRST_LABEL" "$FIRST_ROOT" "$FIRST_ROOT" "$FIRST_ROOT" >> "$EVIDENCE/recipe-candidate-records.tsv"
printf '%s\t%s\t%s\tunrelated-glibc\t1\taarch64\tbroad\tindex\tsha\tpool/y.deb\t1\tsha\t-\tCANDIDATE\tOPEN\tCANDIDATE_ONLY\n' \
    "$SECOND_ID" "$SECOND_PART" "$SECOND_LABEL" >> "$EVIDENCE/apt-candidate-records.tsv"

python3 "$REVIEWER" --evidence-dir "$EVIDENCE" --rules "$RULES" --out "$OUT" >/dev/null
[ "$(cat "$OUT/review.status")" = PASS ] || fail "synthetic review did not pass"
[ "$(awk -F '\t' 'NR > 1 && $9 == "DIRECT_APT_AND_RECIPE_FAMILY_CANDIDATE" {n++} END {print n+0}' "$OUT/generic-exact-candidate-receipt-review.tsv")" -eq 1 ] || fail "synthetic direct family classification failed"
[ "$(awk -F '\t' 'NR > 1 && $9 == "INDIRECT_TOKEN_ONLY" {n++} END {print n+0}' "$OUT/generic-exact-candidate-receipt-review.tsv")" -eq 1 ] || fail "synthetic indirect classification failed"
[ "$(awk -F '\t' 'NR > 1 && $9 == "NO_RETAINED_CANDIDATE" {n++} END {print n+0}' "$OUT/generic-exact-candidate-receipt-review.tsv")" -eq 59 ] || fail "synthetic no-candidate classification failed"
[ "$(awk -F '\t' '$1 == "authority_decisions_accepted" {print $2}' "$OUT/review-summary.tsv")" = 0 ] || fail "reviewer accepted authority"
[ "$(awk -F '\t' '$1 == "deb_extraction_performed" {print $2}' "$OUT/review-summary.tsv")" = NO ] || fail "reviewer claims deb extraction"

printf 'generic exact candidate receipt review smoke: PASS\n'
