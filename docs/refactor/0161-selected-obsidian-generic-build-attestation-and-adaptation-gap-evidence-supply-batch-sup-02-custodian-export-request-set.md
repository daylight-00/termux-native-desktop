# 0161 — Selected Obsidian SUP-02 custodian-export request set

## Status

```text
SUPPLY BATCH: SUP-02
REQUIREMENTS: BA-001, BA-002, BA-003
ROOT REQUESTS: 28
RECORD CONTRACTS: 84
REQUESTS ISSUED: 0
RESPONSES RECEIVED: 0
BUILD ATTESTATIONS ACCEPTED: 0
FINAL PROVIDER AUTHORITY: 0
TARGET POPULATION: 0
```

The production locator found no existing explicit custodian export. This transaction converts that bounded absence into one exact request per pinned root. It does not issue the requests and does not infer provenance.

Each root request requires three records from the same producing build:

```text
build-invocation-record.json  -> BA-001
build-environment-record.json -> BA-002
build-output-manifest.tsv     -> BA-003
```

All three records must bind the same request ID, root review ID, recipe tree, build-run ID, custodian identity, and immutable locator or signed envelope. The output manifest must bind package artifacts and members by SHA-256 and retain ELF SONAME where applicable.

## Completion boundary

A response is complete only when all three records are structurally valid, digest-bound, and cross-linked to one producing build. Repository proximity, workflow definitions, release metadata, package presence, and artifact digests without a build-run identity remain insufficient.

## Canonical outputs

```text
review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-requests.tsv
review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-record-contracts.tsv
review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-request-set-metadata.tsv
```

## Stop line

No request is issued, no response is received, no build attestation is accepted, and no provider or target population effect is permitted.

## Next state

```text
ISSUE_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_REQUEST_SET
```
