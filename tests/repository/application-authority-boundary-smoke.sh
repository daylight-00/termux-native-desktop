#!/usr/bin/env bash
set -euo pipefail

REPO=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BOUNDARY="$REPO/experiments/glibc/selected-obsidian-provider-authority/review/application-authority-boundary.tsv"
LOCAL_LEDGER="$REPO/experiments/glibc/selected-obsidian-provider-authority/review/authority-coverage-ledger/application-local.tsv"
REQUIREMENTS="$REPO/experiments/glibc/selected-obsidian-provider-authority/review/authority-coverage-ledger/set-and-application-requirements.tsv"
ISSUES="$REPO/experiments/glibc/selected-obsidian-provider-authority/review/unresolved-authority-ledger.tsv"

fail() {
  printf 'application authority boundary smoke: FAIL: %s\n' "$*" >&2
  exit 1
}

[ -f "$BOUNDARY" ] || fail "missing application authority boundary"
[ "$(awk 'END {print NR-1}' "$BOUNDARY")" -eq 7 ] || fail "expected 7 APP contract rows"

expected_ids=$'APP-001\nAPP-002\nAPP-003\nAPP-004\nAPP-005\nAPP-006\nAPP-007'
actual_ids=$(awk -F '\t' 'NR > 1 {print $1}' "$BOUNDARY")
[ "$actual_ids" = "$expected_ids" ] || fail "unexpected APP contract IDs"

awk -F '\t' 'NR > 1 && $12 != "BLOCKED" {exit 1}' "$BOUNDARY" || fail "target population is not blocked"
[ "$(awk 'END {print NR-1}' "$LOCAL_LEDGER")" -eq 11 ] || fail "expected 11 application-local reference rows"
[ "$(awk -F '\t' 'NR > 1 && $1 ~ /^APP_REQUIREMENT:/ {count++} END {print count+0}' "$REQUIREMENTS")" -eq 3 ] || fail "expected 3 additional application identity requirements"
awk -F '\t' '$1 == "AUTH-010" && $4 == "OPEN_CONTRACT" {found=1} END {exit !found}' "$ISSUES" || fail "AUTH-010 is not OPEN_CONTRACT"

declare -A expected_sha=(
  [packages/obsidian/launcher/obsidian]=f9787804d6e17e1e53f7096890d352c05247cd902e73312797d27967516bc751
  [packages/obsidian/launcher/obsidian-app]=010de5793e9e28c77277f0801e10ae0841e60d7ff432770644e03b54f0a66aad
  [tools/deploy]=bfe4eb01b36f476673088603c936dfb71cb6796984695e60f1d72240ec3208dd
)

declare -A expected_blob=(
  [packages/obsidian/launcher/obsidian]=42f1c164f77804822f6773c34b232cc205c59fb3
  [packages/obsidian/launcher/obsidian-app]=b3f131392f0aeed9ba9d45b9d13ec7531fe477c7
  [tools/deploy]=44fceda2fae67b5931da299523c798127844a7b4
)

for rel in "${!expected_sha[@]}"; do
  actual_sha=$(sha256sum "$REPO/$rel" | awk '{print $1}')
  [ "$actual_sha" = "${expected_sha[$rel]}" ] || fail "SHA-256 drift: $rel"

  actual_blob=$(git -C "$REPO" hash-object "$rel")
  [ "$actual_blob" = "${expected_blob[$rel]}" ] || fail "Git blob drift: $rel"

  mode=$(git -C "$REPO" ls-files -s -- "$rel" | awk '{print $1}')
  [ "$mode" = "100755" ] || fail "mode drift: $rel"
done

[ "$(awk 'END {print NR-1}' "$REPO/experiments/glibc/selected-obsidian-provider-authority/profiles/target-layout-schema.tsv")" -eq 20 ] || fail "target schema field count changed"
grep -q '^APPLICATION_RUNTIME_COMPOSITION_NOT_REACHED$' "$REPO/STATUS.md" || fail "composition stop state missing"

printf 'application authority boundary smoke: PASS\n'
