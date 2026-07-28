# Selected-provider local-supply evidence live-input adapter and execution-authorization implementation boundary acceptance

## Decision

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-IMPLEMENTATION-ACCEPT-001` accepts the exact v127 corrected and recovered candidate boundary:

```text
ACCEPTED_BOUNDED_NON_EXECUTING_SYNTHETIC_LIVE_INPUT_ADAPTER_EXECUTION_AUTHORIZATION_IMPLEMENTATION_AUTHORITY
```

This is bounded implementation authority for the exact repository-owned synthetic fixture only. It is not authority to supply live documents, issue execution authorization, persist replay state, open provider paths, read provider bytes or execute evidence collection.

## Frozen candidate evidence

The acceptance freezes these exact SHA-256 values:

- implementation source: `2a2d50f8cd93acd6dc4bb06e6c9380c1539b7bdb879c4ed05fbb0c57fbc1d309`;
- synthetic fixture: `3620d96d70f7b7794e77353465aee5c8545ead955268729510154aefe52fbc11`;
- negative cases: `cc8644526a810cd5a8beb1fca9f6713e95ae06bc44ef3e44742b818c34aa1db3`;
- 164-row coverage ledger: `3c4277e9a036023b409a156a2712edfe086599fa7cbb9e77bfa4171649235908`;
- synthetic success result: `0ac8eed9e3c6315dcabdab47ebff7e0c0f2fd52b4ac4fbcfca9edf50f1872af5`;
- candidate metadata: `371f4a26e50b47f94c45b217c07e5c61fa4b5e00cff5360a4f2822373ea522a6`.

Historical candidate artifacts remain unchanged and continue to state `QUALIFIED_NON_EXECUTING_SYNTHETIC_LIVE_INPUT_ADAPTER_EXECUTION_AUTHORIZATION_IMPLEMENTATION_CANDIDATE`.

## Accepted implementation boundary

```text
explicit input coverage:              10
adapter-envelope field coverage:      20
execution-authorization claims:       27
validation coverage:                  37
state coverage:                       18
operation coverage:                   32
failure coverage:                     20
total coverage rows:                 164
synthetic success cases:               1
fail-closed cases:                    20
synthetic coordinate rows/fields:  41 / 10
provider reads:                        0
writes:                                0
live authority:                        0
```

The implementation accepts only its exact repository-owned fixture, treats synthetic coordinate paths as text, does not invoke the previously accepted synthetic issuance implementation, does not rewrite live paths, does not persist replay state and does not delegate to an evidence executor.

## Current authority state

```text
live inputs: 0
adapter envelopes: 0
execution authorizations: 0
provider reads: 0
writes: 0
live authority: 0
```

## Authority exclusions

This acceptance does not authorize live owner decisions, tokens, coordinate receipts or revocation snapshots; arbitrary input paths; live-to-synthetic rewriting; replay persistence; local path discovery; provider opening or byte reads; evidence-transaction execution; local-supply-map production; generation-root creation; target population, materialization, publication, deployment or activation.

## Next action

`generate-and-review-non-executing-selected-provider-local-supply-map-evidence-transaction-implementation-candidate`

The next step may implement the already accepted 12-input/16-state/32-operation/18-failure read-only evidence-transaction design using repository-owned synthetic fixtures only. It may not accept live coordinates, open provider files, read provider bytes or create runtime authority.
