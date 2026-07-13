#!/usr/bin/env bash
set -euo pipefail

REPO=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BASE="$REPO/experiments/glibc/selected-obsidian-provider-authority"
GENERATOR="$BASE/recipe/define-generic-artifact-member-comparison-set.py"
REVIEW="$BASE/review/generic-exact-candidate-receipt-review.tsv"
ARTIFACTS="$BASE/review/generic-artifact-member-comparison-artifacts.tsv"
EDGES="$BASE/review/generic-artifact-member-comparison-edges.tsv"
EXCLUSIONS="$BASE/review/generic-artifact-member-comparison-exclusions.tsv"
META="$BASE/review/generic-artifact-member-comparison-metadata.tsv"
REPOSITORY="$BASE/profiles/supply-repository-metadata-registry.tsv"

fail() {
    printf 'generic artifact member comparison set smoke: FAIL: %s\n' "$*" >&2
    exit 1
}

for path in "$GENERATOR" "$REVIEW" "$ARTIFACTS" "$EDGES" "$EXCLUSIONS" "$META" "$REPOSITORY"; do
    [ -f "$path" ] || fail "missing canonical input/product: $path"
done
[ -x "$GENERATOR" ] || fail "generator is not executable"
python3 -m py_compile "$GENERATOR"

[ "$(awk 'END {print NR-1}' "$ARTIFACTS")" -eq 34 ] || fail "artifact denominator is not 34"
[ "$(awk 'END {print NR-1}' "$EDGES")" -eq 44 ] || fail "edge denominator is not 44"
[ "$(awk 'END {print NR-1}' "$EXCLUSIONS")" -eq 15 ] || fail "exclusion denominator is not 15"
[ "$(awk -F '\t' 'NR > 1 {sum += $7} END {print sum+0}' "$ARTIFACTS")" -eq 51771348 ] || fail "compressed byte total drift"
[ "$(awk -F '\t' 'NR > 1 && $10 == "STATIC_ONLY_PACKAGE_OUTSIDE_DYNAMIC_MEMBER_SEARCH" {n++} END {print n+0}' "$EXCLUSIONS")" -eq 14 ] || fail "static exclusion count drift"
[ "$(awk -F '\t' 'NR > 1 && $10 == "ARCH_ALL_DEVELOPMENT_PACKAGE_OUTSIDE_AARCH64_ELF_MEMBER_SEARCH" {n++} END {print n+0}' "$EXCLUSIONS")" -eq 1 ] || fail "development exclusion count drift"

awk -F '\t' 'NR > 1 && ($10 != "DYNAMIC_OR_SPLIT_RUNTIME_CANDIDATE" || $11 != "NAMED_DOWNLOAD_ONLY_MEMBER_INVENTORY_SCOPE" || $12 != "NOT_DOWNLOADED_CONTRACT_ONLY" || $13 != "OPEN" || $14 != "UNRESOLVED" || $15 != "BLOCKED") {exit 1}' "$ARTIFACTS" || fail "artifact claim boundary drift"
awk -F '\t' 'NR > 1 && ($10 != "NAMED_MEMBER_SEARCH_CANDIDATE_ONLY" || $11 != "OPEN" || $12 != "OPEN" || $13 != "OPEN" || $14 != "UNRESOLVED" || $15 != "BLOCKED") {exit 1}' "$EDGES" || fail "edge claim boundary drift"
awk -F '\t' 'NR > 1 && ($13 != "EXCLUDED_FROM_DOWNLOAD_SET_RETAINED_AS_NEGATIVE_PACKAGE_CLASS_EVIDENCE" || $14 != "OPEN_NO_DEB_DOWNLOAD_OR_EXTRACTION" || $15 != "UNRESOLVED" || $16 != "BLOCKED") {exit 1}' "$EXCLUSIONS" || fail "exclusion claim boundary drift"

[ "$(awk -F '\t' '$1 == "artifact_set_sha256" {print $2}' "$META")" = "$(sha256sum "$ARTIFACTS" | awk '{print $1}')" ] || fail "artifact hash drift"
[ "$(awk -F '\t' '$1 == "edge_set_sha256" {print $2}' "$META")" = "$(sha256sum "$EDGES" | awk '{print $1}')" ] || fail "edge hash drift"
[ "$(awk -F '\t' '$1 == "exclusion_set_sha256" {print $2}' "$META")" = "$(sha256sum "$EXCLUSIONS" | awk '{print $1}')" ] || fail "exclusion hash drift"
[ "$(awk -F '\t' '$1 == "authority_decisions_accepted" {print $2}' "$META")" = 0 ] || fail "metadata accepted authority"
[ "$(awk -F '\t' '$1 == "network_download_performed" {print $2}' "$META")" = NO ] || fail "metadata claims download"
[ "$(awk -F '\t' '$1 == "deb_extraction_performed" {print $2}' "$META")" = NO ] || fail "metadata claims extraction"
[ "$(awk -F '\t' '$1 == "target_rows_populated" {print $2}' "$META")" = 0 ] || fail "metadata populated targets"

python3 - "$REVIEW" "$ARTIFACTS" "$EDGES" "$EXCLUSIONS" <<'PY'
import csv
import sys
from collections import Counter

review_path, artifact_path, edge_path, exclusion_path = sys.argv[1:]

def read(path):
    with open(path, newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))

review = read(review_path)
artifacts = read(artifact_path)
edges = read(edge_path)
exclusions = read(exclusion_path)
direct = {r["evidence_row_id"] for r in review if r["review_state"] == "DIRECT_APT_AND_RECIPE_FAMILY_CANDIDATE"}
indirect_or_absent = {r["evidence_row_id"] for r in review if r["review_state"] != "DIRECT_APT_AND_RECIPE_FAMILY_CANDIDATE"}
edge_ids = {r["evidence_row_id"] for r in edges}
assert len(direct) == 37
assert edge_ids == direct
assert not edge_ids.intersection(indirect_or_absent)
assert len({r["artifact_id"] for r in artifacts}) == 34
assert len({r["artifact_id"] for r in exclusions}) == 15
assert not {r["artifact_id"] for r in artifacts}.intersection({r["artifact_id"] for r in exclusions})
cardinality = Counter(Counter(r["evidence_row_id"] for r in edges).values())
assert cardinality == Counter({1: 31, 2: 5, 3: 1})
assert all(r["package"].endswith("-glibc-static") or (r["package"] == "mesa-dev-glibc" and r["architecture"] == "all") for r in exclusions)
PY

for forbidden in \
    'subprocess' \
    'urllib' \
    'requests' \
    'curl' \
    'wget' \
    'apt[[:space:]]+(update|install|download)' \
    'dpkg-deb' \
    'tarfile'; do
    if grep -E "$forbidden" "$GENERATOR" >/dev/null; then
        fail "forbidden network/extraction implementation appears: $forbidden"
    fi
done

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/evidence"
python3 - "$REVIEW" "$ARTIFACTS" "$EDGES" "$EXCLUSIONS" "$TMP/evidence/apt-candidate-records.tsv" <<'PY'
import csv
import sys
from pathlib import Path

review_path, artifacts_path, edges_path, exclusions_path, out_path = sys.argv[1:]

def read(path):
    with open(path, newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))

review = {r["evidence_row_id"]: r for r in read(review_path)}
artifacts = {r["artifact_id"]: r for r in read(artifacts_path)}
edges = read(edges_path)
exclusions = read(exclusions_path)
fields = [
    "evidence_row_id", "capability_partition", "lookup_name", "candidate_package",
    "candidate_version", "architecture", "match_tokens", "index_file", "index_sha256",
    "repository_filename", "artifact_size", "artifact_sha256", "source_field",
    "candidate_state", "object_member_binding_state", "authority_state",
]
rows = []
for edge in edges:
    artifact = artifacts[edge["artifact_id"]]
    source = review[edge["evidence_row_id"]]
    rows.append({
        "evidence_row_id": edge["evidence_row_id"],
        "capability_partition": edge["capability_partition"],
        "lookup_name": edge["identity_label"],
        "candidate_package": artifact["package"],
        "candidate_version": artifact["version"],
        "architecture": artifact["architecture"],
        "match_tokens": source["direct_family_roots"],
        "index_file": "synthetic-locked-index",
        "index_sha256": artifact["packages_index_sha256"],
        "repository_filename": artifact["repository_filename"],
        "artifact_size": artifact["artifact_size"],
        "artifact_sha256": artifact["artifact_sha256"],
        "source_field": "-",
        "candidate_state": "EXACT_INDEX_ARTIFACT_IDENTITY_CANDIDATE",
        "object_member_binding_state": "OPEN_NO_DEB_EXTRACTION",
        "authority_state": "CANDIDATE_ONLY",
    })
for exclusion in exclusions:
    for evidence_row_id in exclusion["affected_evidence_row_ids"].split(";"):
        source = review[evidence_row_id]
        rows.append({
            "evidence_row_id": evidence_row_id,
            "capability_partition": source["capability_partition"],
            "lookup_name": source["identity_label"],
            "candidate_package": exclusion["package"],
            "candidate_version": exclusion["version"],
            "architecture": exclusion["architecture"],
            "match_tokens": source["direct_family_roots"],
            "index_file": "synthetic-locked-index",
            "index_sha256": exclusion["packages_index_sha256"],
            "repository_filename": exclusion["repository_filename"],
            "artifact_size": exclusion["artifact_size"],
            "artifact_sha256": exclusion["artifact_sha256"],
            "source_field": "-",
            "candidate_state": "EXACT_INDEX_ARTIFACT_IDENTITY_CANDIDATE",
            "object_member_binding_state": "OPEN_NO_DEB_EXTRACTION",
            "authority_state": "CANDIDATE_ONLY",
        })
with Path(out_path).open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
PY

python3 "$GENERATOR" \
    --evidence-dir "$TMP/evidence" \
    --review "$REVIEW" \
    --repository-metadata "$REPOSITORY" \
    --out "$TMP/out"
cmp "$ARTIFACTS" "$TMP/out/generic-artifact-member-comparison-artifacts.tsv" || fail "artifact regeneration drift"
cmp "$EDGES" "$TMP/out/generic-artifact-member-comparison-edges.tsv" || fail "edge regeneration drift"
cmp "$EXCLUSIONS" "$TMP/out/generic-artifact-member-comparison-exclusions.tsv" || fail "exclusion regeneration drift"
[ "$(cat "$TMP/out/definition.status")" = PASS ] || fail "regenerated definition did not pass"

printf 'generic artifact member comparison set smoke: PASS\n'
