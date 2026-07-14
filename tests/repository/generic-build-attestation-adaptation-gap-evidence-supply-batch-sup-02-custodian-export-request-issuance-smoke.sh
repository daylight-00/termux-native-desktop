#!/usr/bin/env bash
set -euo pipefail
repo=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
base="$repo/experiments/glibc/selected-obsidian-provider-authority"
recipe="$base/recipe/issue-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-request-set.py"
review="$base/review"
tracked="$base/evidence-supply/requests/SUP-02/custodian-export"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

PYTHONDONTWRITEBYTECODE=1 python3 "$recipe" \
  --request-set "$review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-requests.tsv" \
  --record-contracts "$review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-record-contracts.tsv" \
  --request-set-metadata "$review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-request-set-metadata.tsv" \
  --source-head a12c6f3a96f74b27d633fc3956b20d450d2245ed \
  --source-tree b4255820347b03b179db9f65f6759bfce96939f4 \
  --out "$tmp/replay"

for name in \
  custodian-export-request-issuance.tsv \
  custodian-export-record-contract-issuance.tsv \
  custodian-export-request-issuance-metadata.tsv \
  analysis.status claim-boundary.txt next-state.txt; do
  cmp "$tracked/$name" "$tmp/replay/$name"
done

python3 - "$tracked" <<'PY'
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path
root = Path(sys.argv[1])

def rows(name):
    with (root / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))

requests = rows("custodian-export-request-issuance.tsv")
contracts = rows("custodian-export-record-contract-issuance.tsv")
metadata = {r["field"]: r["value"] for r in rows("custodian-export-request-issuance-metadata.tsv")}
assert len(requests) == 28
assert len(contracts) == 84
assert len({r["request_id"] for r in requests}) == 28
assert len({r["issuance_id"] for r in requests}) == 28
assert all(r["request_state"] == "REQUEST_ISSUED_REPOSITORY_PUBLICATION" for r in requests)
assert all(r["acknowledgement_state"] == "NOT_ACKNOWLEDGED" for r in requests)
assert all(r["responses_received"] == "0" for r in requests)
assert all(r["build_attestations_accepted"] == "0" for r in requests)
assert all(r["publication_model"] == "REMOTE_BRANCH_PUBLICATION_IS_REQUEST_ISSUANCE_NOT_CUSTODIAN_ACKNOWLEDGEMENT" for r in requests)
assert all(r["record_state"] == "ISSUED_REQUIRED_NOT_SUPPLIED" for r in contracts)
assert all(r["acceptance_state"] == "OPEN_NO_ACCEPTANCE" for r in contracts)
by_request = defaultdict(list)
for row in contracts:
    by_request[row["request_id"]].append(row)
assert set(by_request) == {r["request_id"] for r in requests}
for request_id, values in by_request.items():
    assert len(values) == 3
    assert {(r["requirement_id"], r["record_name"]) for r in values} == {
        ("BA-001", "build-invocation-record.json"),
        ("BA-002", "build-environment-record.json"),
        ("BA-003", "build-output-manifest.tsv"),
    }
assert Counter(r["requirement_id"] for r in contracts) == Counter({"BA-001": 28, "BA-002": 28, "BA-003": 28})
assert metadata["requests_issued"] == "28"
assert metadata["requests_acknowledged"] == "0"
assert metadata["responses_received"] == "0"
assert metadata["build_attestations_accepted"] == "0"
assert metadata["final_provider_decisions_accepted"] == "0"
assert metadata["target_rows_populated"] == "0"
assert metadata["next_state"] == "IMPLEMENT_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSE_ACQUIRER"
PY

# Negative: an already-issued source request set must fail closed.
cp "$review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-requests.tsv" "$tmp/requests.tsv"
python3 - "$tmp/requests.tsv" <<'PY'
from pathlib import Path
p = Path(__import__('sys').argv[1])
s = p.read_text(encoding='utf-8')
s = s.replace('REQUEST_DEFINED_NOT_ISSUED', 'REQUEST_ISSUED_REPOSITORY_PUBLICATION', 1)
p.write_text(s, encoding='utf-8')
PY
if PYTHONDONTWRITEBYTECODE=1 python3 "$recipe" \
  --request-set "$tmp/requests.tsv" \
  --record-contracts "$review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-record-contracts.tsv" \
  --request-set-metadata "$review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-request-set-metadata.tsv" \
  --source-head a12c6f3a96f74b27d633fc3956b20d450d2245ed \
  --source-tree b4255820347b03b179db9f65f6759bfce96939f4 \
  --out "$tmp/bad-state" >/dev/null 2>&1; then
  echo "already-issued request drift was accepted" >&2
  exit 1
fi

# Negative: a missing record contract must fail closed.
head -n -1 "$review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-record-contracts.tsv" > "$tmp/contracts.tsv"
if PYTHONDONTWRITEBYTECODE=1 python3 "$recipe" \
  --request-set "$review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-requests.tsv" \
  --record-contracts "$tmp/contracts.tsv" \
  --request-set-metadata "$review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-request-set-metadata.tsv" \
  --source-head a12c6f3a96f74b27d633fc3956b20d450d2245ed \
  --source-tree b4255820347b03b179db9f65f6759bfce96939f4 \
  --out "$tmp/bad-contract" >/dev/null 2>&1; then
  echo "missing record contract was accepted" >&2
  exit 1
fi

printf 'SUP-02 custodian-export request issuance smoke: PASS\n'
