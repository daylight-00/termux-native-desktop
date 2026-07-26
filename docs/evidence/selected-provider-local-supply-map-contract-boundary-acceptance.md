# Selected-provider local-supply-map contract boundary acceptance

## Decision

```text
acceptance id: SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-ACCEPT-001
decision: ACCEPTED_BOUNDED_NON_MUTATING_SELECTED_PROVIDER_LOCAL_SUPPLY_MAP_CONTRACT
candidate: SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-REVIEW-001
populated local paths: 0
local supply map produced: NO
execution authorized: NO
```

The exact v114 contract candidate is accepted as a bounded Class D non-mutating interface. Acceptance covers four digest-frozen candidate artifacts, 41 object-bound contract rows, 24 fail-closed validation rules and the canonical empty receipt schema. It does not discover, bind, open, read, download or extract any provider or result byte.

## Frozen candidate

```text
selected-provider-local-supply-map-contract.tsv
2223af964e74cc8bb221d13e559e49aaf03abe364985346cb1d8e43973c6640e
selected-provider-local-supply-map-validation-contract.tsv
0df8d9c7ddc28098ee220ee634a139b04aaa3d241bd36b2a4eb57ef8fbc41198
selected-provider-local-supply-map-receipt-schema.json
8f7c8d26f7e646e431e6be53526b55ccc3f5c65584b4c2306e9d19544a9396fa
selected-provider-local-supply-map-contract-metadata.tsv
751510776aa6c7db15f3d968c7e910b7886d1a560c36e4b241cb5976041a7acd
```

Historical candidate metadata remains `QUALIFIED_NON_MUTATING_LOCAL_SUPPLY_MAP_CONTRACT_CANDIDATE` with its candidate-time gate open. This acceptance is recorded separately and does not rewrite candidate evidence.

## Accepted structural boundary

```text
contract rows: 41
validation rules: 24
populated local paths: 0
result-index rows: 23
append-only receipt rows: 4
existing-authority sentinel rows: 14
receipt schema: SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-RECEIPT-SCHEMA-001
```

The accepted interface requires exact immutable result/index/container/member identity; absolute canonical paths from a separately authorized localization receipt; no-follow regular-file opening; owner, mode and stable-inode checks; exact size and SHA-256; ELF64 little-endian AArch64 `ET_DYN`; exact SONAME; complete atomic families; and whole-map rejection on any failed row.

## Authority boundary

Acceptance grants no path-discovery authority, byte-read authority, local-map production, execution authorization, generation-root creation, target population, materialization, publication, deployment or activation. A later read-only evidence transaction must itself be designed and reviewed before any local path may be inspected.

## Update and rollback

Any contract row, validation rule, receipt schema, result/index/container/member identity, path rule, content/ELF/SONAME rule, failure semantics or authority change requires a new Class D contract review. Before localization this acceptance may be revoked directly. Revocation never authorizes reading or modifying provider, object-store or generation bytes.

## Next action

```text
design-and-review-read-only-selected-provider-local-supply-map-evidence-transaction
```

The next transaction may design exact input coordinates, bounded read operations, receipts and stop conditions only. It may not search, download, extract, populate or execute.
