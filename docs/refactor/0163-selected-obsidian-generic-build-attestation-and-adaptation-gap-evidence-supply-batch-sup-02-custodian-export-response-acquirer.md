# 0163 — Selected Obsidian SUP-02 custodian-export response acquirer

## Status

```text
SUPPLY BATCH: SUP-02
REQUIREMENTS: BA-001, BA-002, BA-003
ISSUED ROOT REQUESTS: 28
ISSUED RECORD CONTRACTS: 84
RESPONSE ACQUIRER: IMPLEMENTED / BOUNDED / INPUT-ONLY
MALFORMED OR PARTIAL RESPONSE: REJECTED
CANDIDATE RESPONSE ACCEPTANCE: SEPARATE REVIEW REQUIRED
BUILD ATTESTATIONS ACCEPTED: 0
FINAL PROVIDER AUTHORITY: 0
TARGET POPULATION: 0
```

This transaction implements the strict response acquirer for the repository-published `SUP-02` custodian-export requests. It does not discover or synthesize build provenance. It consumes only explicitly staged response drops and converts structurally complete, digest-bound responses into candidate review input.

## Canonical implementation

```text
experiments/glibc/selected-obsidian-provider-authority/recipe/
    acquire-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-responses.py
    run-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-acquirer.sh

tests/repository/
    generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-acquirer-smoke.sh
```

Canonical issuance inputs:

```text
experiments/glibc/selected-obsidian-provider-authority/evidence-supply/requests/SUP-02/custodian-export/
    custodian-export-request-issuance.tsv
    custodian-export-record-contract-issuance.tsv
```

## Response input root

Default location:

```text
$HOME/.cache/hw-t-evidence/termux-native-desktop/
    sup-02-custodian-export-responses/
```

The input root may be absent. Absence is a successful bounded acquisition with 28 explicit `NO_RESPONSE_DROP_PRESENT` states.

A supplied response uses the exact request ID as its directory name:

```text
<request-id>/
    custodian-export-response-manifest.tsv
    build-invocation-record.json
    build-environment-record.json
    build-output-manifest.tsv
```

The response manifest has exactly three rows and the following fields:

```text
response_record_id
request_id
root_review_id
recipe_root
recipe_tree
record_name
relative_path
sha256
size_bytes
custodian_identity
immutable_locator_or_signed_envelope
claim_boundary
```

Every payload file must occur exactly once in the manifest. Unknown request directories, missing or extra files, symlinks, special files, path traversal, digest drift and size drift are rejected.

## One-build validation

The acquirer validates the mandatory-field contract published for each record. All three records must agree on:

```text
request_id
root_review_id
recipe_tree
build_run_id
custodian_identity
immutable_locator_or_signed_envelope
```

The invocation and output records must also bind the exact recipe root. The output manifest must contain at least one row, use the exact contract header, bind the request and recipe coordinates on every row, and carry syntactically valid artifact and member SHA-256 values.

A partial response directory is not recorded as a partial attestation. It is rejected fail-closed because the completion gate requires all three cross-linked records from one producing build.

## Candidate receipt

The acquirer emits:

```text
analysis.status
claim-boundary.txt
next-state.txt
summary.tsv
request-response-acquisition-status.tsv
response-record-inventory.tsv
candidate-response-root/
    <request-id>/
        custodian-export-response-manifest.tsv
        build-invocation-record.json
        build-environment-record.json
        build-output-manifest.tsv
```

Verified candidate files are copied read-only and rehashed after copying. The fixed claim boundary is:

```text
CANDIDATE_CUSTODIAN_EXPORT_RESPONSE_REVIEW_REQUIRED_NO_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT
```

A complete acquisition state means only that a candidate response is available for review. It does not acknowledge the request on behalf of the custodian, accept build attestation, select a provider, or populate a target row.

## Resource bounds

```text
maximum request responses: 28
records per response:       3
maximum single record:      64 MiB
maximum total records:     512 MiB
```

## Next state

```text
REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSE_ACQUISITION_RECEIPT
```
