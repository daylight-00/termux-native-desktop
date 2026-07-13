#!/usr/bin/env bash
set -euo pipefail

REPO=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BOUNDARY="$REPO/experiments/glibc/selected-obsidian-provider-authority/review/generic-source-authority-boundary.tsv"
INDEX="$REPO/experiments/glibc/selected-obsidian-provider-authority/review/non-priority-generic-authority-ledger.tsv"
PART_ROOT="$REPO/experiments/glibc/selected-obsidian-provider-authority/review"
ISSUES="$REPO/experiments/glibc/selected-obsidian-provider-authority/review/unresolved-authority-ledger.tsv"

fail() {
  printf 'generic source authority boundary smoke: FAIL: %s\n' "$*" >&2
  exit 1
}

[ -f "$BOUNDARY" ] || fail "missing generic source authority boundary"
[ -f "$INDEX" ] || fail "missing non-priority generic index"
[ "$(awk 'END {print NR-1}' "$BOUNDARY")" -eq 7 ] || fail "expected 7 GENSRC contract rows"

expected_ids=$'GENSRC-001\nGENSRC-002\nGENSRC-003\nGENSRC-004\nGENSRC-005\nGENSRC-006\nGENSRC-007'
actual_ids=$(awk -F '\t' 'NR > 1 {print $1}' "$BOUNDARY")
[ "$actual_ids" = "$expected_ids" ] || fail "unexpected GENSRC contract IDs"

awk -F '\t' 'NR > 1 && $12 != "NOT_REACHED" {exit 1}' "$BOUNDARY" || fail "composition reached unexpectedly"
awk -F '\t' 'NR > 1 && $13 != "BLOCKED" {exit 1}' "$BOUNDARY" || fail "target population is not blocked"
awk -F '\t' 'NR > 1 && $9 ~ /ACCEPTED_FINAL/ {exit 1}' "$BOUNDARY" || fail "final provider accepted unexpectedly"
[ "$(awk -F '\t' 'NR > 2 {sum += $4} END {print sum+0}' "$BOUNDARY")" -eq 61 ] || fail "capability row count does not sum to 61"
[ "$(awk -F '\t' '$1 == "GENSRC-001" {print $4}' "$BOUNDARY")" -eq 61 ] || fail "global denominator is not 61"

python3 - "$INDEX" "$PART_ROOT" "$BOUNDARY" <<'PY'
import csv
import hashlib
import pathlib
import sys

index = pathlib.Path(sys.argv[1])
root = pathlib.Path(sys.argv[2])
boundary = pathlib.Path(sys.argv[3])

expected_counts = {
    "audio": 1,
    "graphics": 3,
    "gtk-gui": 36,
    "other": 1,
    "printing": 10,
    "security": 10,
}

with index.open(newline="") as stream:
    index_rows = list(csv.DictReader(stream, delimiter="\t"))
if len(index_rows) != 6:
    raise SystemExit("expected six indexed generic partitions")

origin_counts = {}
partition_counts = {}
all_ids = set()
for row in index_rows:
    partition_id = row["partition_id"]
    path = root / row["partition_path"]
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != row["sha256"]:
        raise SystemExit(f"partition SHA drift: {partition_id}")
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(rows) != int(row["row_count"]):
        raise SystemExit(f"partition row-count drift: {partition_id}")
    if len(rows) != expected_counts[partition_id]:
        raise SystemExit(f"unexpected canonical count: {partition_id}")
    partition_counts[partition_id] = len(rows)
    for item in rows:
        evidence_id = item["evidence_row_id"]
        if evidence_id in all_ids:
            raise SystemExit(f"duplicate evidence identity: {evidence_id}")
        all_ids.add(evidence_id)
        origin = item["observed_supply_origin"]
        origin_counts[origin] = origin_counts.get(origin, 0) + 1
        if item["exact_supply_artifact_state"] != "NOT_LOCKED_PRIORITY":
            raise SystemExit(f"non-priority exact supply promoted: {evidence_id}")
        if item["provisional_final_provider_state"] != "UNRESOLVED":
            raise SystemExit(f"non-priority final provider promoted: {evidence_id}")
        if item["target_population_state"] != "BLOCKED":
            raise SystemExit(f"target population changed: {evidence_id}")

if len(all_ids) != 61:
    raise SystemExit("generic denominator is not 61")
if origin_counts != {
    "DEBIAN_ROOTFS_ORACLE_BYTES": 60,
    "LOCAL_GRAPHICS_EXPERIMENT_BYTES": 1,
}:
    raise SystemExit(f"unexpected origin counts: {origin_counts}")

with boundary.open(newline="") as stream:
    boundary_rows = {row["contract_id"]: row for row in csv.DictReader(stream, delimiter="\t")}
expected_boundary_counts = {
    "GENSRC-002": partition_counts["security"],
    "GENSRC-003": partition_counts["gtk-gui"],
    "GENSRC-004": partition_counts["audio"],
    "GENSRC-005": partition_counts["other"],
    "GENSRC-006": partition_counts["printing"],
    "GENSRC-007": partition_counts["graphics"],
}
for contract_id, count in expected_boundary_counts.items():
    if int(boundary_rows[contract_id]["identity_count"]) != count:
        raise SystemExit(f"boundary/partition count mismatch: {contract_id}")
PY

awk -F '\t' '$1 == "AUTH-009" && $4 == "OPEN_OBJECT_SOURCE_BINDING" {found=1} END {exit !found}' "$ISSUES" || fail "AUTH-009 is not OPEN_OBJECT_SOURCE_BINDING"
[ "$(awk 'END {print NR-1}' "$REPO/experiments/glibc/selected-obsidian-provider-authority/profiles/target-layout-schema.tsv")" -eq 20 ] || fail "target schema field count changed"
grep -q '^NON_PRIORITY_GENERIC_SOURCE_CLASS_BOUNDARY_PASS_BOUNDED$' "$REPO/STATUS.md" || fail "generic source boundary state missing"
grep -q '^APPLICATION_RUNTIME_COMPOSITION_NOT_REACHED$' "$REPO/STATUS.md" || fail "composition stop state missing"

printf 'generic source authority boundary smoke: PASS\n'
