#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BASE="$ROOT/experiments/glibc/selected-obsidian-provider-authority"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
records="$TMP/records"; mkdir -p "$records"
first=$(awk -F'\t' 'NR==2{print $2}' "$BASE/review/generic-build-attestation-adaptation-root-gap-evidence-supply-request-set.tsv")
mkdir -p "$records/$first"
printf '{"build_run_id":"fixture","invocation":["fixture"]}\n' > "$records/$first/build-invocation-record.json"
printf '{"build_run_id":"fixture","toolchain":{}}\n' > "$records/$first/build-environment-record.json"
printf 'root_review_id\tbuild_run_id\tartifact_sha256\tmember_path\tmember_sha256\n%s\tfixture\t%s\tfile\t%s\n' "$first" "$(printf a%.0s {1..64})" "$(printf b%.0s {1..64})" > "$records/$first/build-output-manifest.tsv"
printf '{"full_name":"termux-pacman/glibc-packages"}\n' > "$TMP/repo.json"
printf '{"workflows":[{"id":1}]}\n' > "$TMP/workflows.json"
printf '[]\n' > "$TMP/releases.json"
python3 "$BASE/recipe/probe-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02.py" \
 --root-request-set "$BASE/review/generic-build-attestation-adaptation-root-gap-evidence-supply-request-set.tsv" \
 --record-root "$records" --github-repository-metadata "$TMP/repo.json" --github-workflows "$TMP/workflows.json" --github-releases "$TMP/releases.json" --out "$TMP/out" >/dev/null
[[ $(awk -F'\t' '$1=="complete_custodian_exports"{print $2}' "$TMP/out/summary.tsv") == 1 ]]
[[ $(awk -F'\t' '$1=="record_files_located"{print $2}' "$TMP/out/summary.tsv") == 3 ]]
[[ $(cat "$TMP/out/analysis.status") == PASS ]]
# unsafe symlink must fail
rm -rf "$TMP/out"; rm "$records/$first/build-environment-record.json"; ln -s /etc/passwd "$records/$first/build-environment-record.json"
if python3 "$BASE/recipe/probe-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02.py" --root-request-set "$BASE/review/generic-build-attestation-adaptation-root-gap-evidence-supply-request-set.tsv" --record-root "$records" --out "$TMP/out" >/dev/null 2>&1; then exit 1; fi
printf 'generic SUP-02 provenance locator smoke: PASS\n'
