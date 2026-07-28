# Selected-provider local-supply evidence live-input adapter and execution-authorization contract review

## Decision

```text
review_id=SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-CONTRACT-REVIEW-001
decision=QUALIFIED_NON_EXECUTING_LIVE_INPUT_ADAPTER_EXECUTION_AUTHORIZATION_CONTRACT_CANDIDATE
acceptance_gate=SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-CONTRACT-ACCEPTANCE-OPEN
```

The accepted synthetic-only issuance/coordinate implementation now has a deterministic interface boundary for future explicit live inputs and a separate read-only evidence-execution authorization. This is a contract candidate only. It supplies no live document, issues no authorization, opens no provider path and creates no runtime state.

## Architecture review finding

The accepted implementation is deliberately hard-bound to `SYNTHETIC_REPOSITORY_FIXTURE_ONLY`, the synthetic path namespace and synthetic coordinate origins. A separate adapter cannot safely present real coordinates to those exact bytes by rewriting live paths into the synthetic namespace: that would sever the evidence binding between the coordinate receipt and the provider bytes.

Therefore the contract fixes the accepted implementation's role as:

```text
IMMUTABLE_SEMANTIC_AND_REGRESSION_ORACLE_ONLY_NOT_LIVE_EXECUTOR
```

The exact implementation digest remains `039593be6144845b8be817bc45144be58c0f9a03bc60278a73748213d269df61`. Live-to-synthetic path/origin rewriting and live invocation of the synthetic CLI are forbidden. Any future live adapter or evidence executor requires a separate implementation review and acceptance; it may preserve the accepted cardinalities and validation semantics but may not silently widen the accepted synthetic implementation.

## Frozen candidate artifacts

| Artifact | SHA-256 |
|---|---|
| `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-contract.json` | `2e80bcb77b97b5ecc52304a9ef3693b123cb13dc74a7bc9c94dc1be557e82213` |
| `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-execution-authorization-schema.json` | `91cd60dbc10fd0d0d1e644011b1d5f4f06e903744e81982dc088264836757a20` |
| `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-validation-contract.tsv` | `408c213c941f8670129bf2e07da02ea06886895ee5c39e748d748b54e0993503` |
| `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-state-machine.tsv` | `6dcbc03906f755e836c7dd83f679b0202c6b219afcfa0afe5f254da88ed64d7b` |
| `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-operation-contract.tsv` | `912786adf77ef9beeaec22f3208b742a79ae3edcb33730e1267148be86266a66` |
| `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-failure-contract.tsv` | `a031e35872a8d2e0ad71e888a0040574bf6560b7b256ac5d7680cfb36c013e76` |
| `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-receipt-contract.json` | `0acb6152d3afa1397841c453d8b2cc6a72f3cbbd05bead51ee02596aafadf55b` |
| `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-metadata.tsv` | `ea0cfbed6e0d14a694cd1e0000acbbeecee156dd5e1923d551151c834506aa2e` |

## Contract cardinality

```text
explicit input channels:                    10
adapter envelope required fields:           20
execution-authorization required claims:    27
validation rules:                           37
state-machine states:                       18
ordered operations:                         32
failure contracts:                          20
required coordinate rows / row fields:   41 / 10
maximum provider bytes:             29,047,112
maximum result receipt bytes:        1,048,576
```

The ten future adapter inputs are exact owner-decision, owner-token, coordinate-receipt and revocation documents plus explicit repository HEAD, tree, remote HEAD, executor UID, clock snapshot and transaction output root. Every document is supplied by exact path argument; scalar values are supplied directly. Search, glob, basename fallback, environment inference, archive lookup and package-manager discovery are forbidden.

## Inactive adapter boundary

A future adapter may validate text and canonical document bytes and produce one digest-bound inactive envelope. Before a separate execution authorization:

```text
provider path opens: 0
provider byte reads: 0
runtime writes:      0
live authority:      0
```

The envelope binds owner decision, token, exact canonical 41-row coordinate receipt, revocation snapshot, repository HEAD/tree, remote HEAD, executor UID, coordinate-row digest manifest, replay tuple and transaction output root. The envelope is not an activated token, execution authorization, accepted local-supply map or runtime object.

## Execution-authorization boundary

The future execution authorization contains 27 exact claims and is valid for no more than 3600 seconds. It binds the adapter envelope, owner token, coordinate receipt, accepted implementation and evidence-design authorities, repository baseline, executor, revocation epoch, exact 41-path count, the 29,047,112-byte provider budget and transaction output root.

The only permitted future effects are:

```text
open the exact 41 explicit paths with no-follow semantics
read/hash/fstat and validate exact ELF SONAME identities
write transaction-scoped evidence logs, receipts, index and archive only
delegate only to a separately accepted read-only evidence implementation
```

The first provider open is forbidden until every contract rule passes and the exact execution replay tuple is atomically consumed. Package databases and the live glibc prefix must remain identical before and after; the authority registry may change only by the one expected consumed tuple.

## Current authority state

```text
live inputs:                   0
adapter envelopes:             0
execution authorizations:      0
provider reads:                0
writes:                        0
live authority:                0
local-supply map:              NOT_PRODUCED_NOT_AUTHORIZED
target population:             NOT_AUTHORIZED_UNPOPULATED_SCHEMA_ONLY
materialization/publication:   NOT_AUTHORIZED / NOT_AUTHORIZED
deployment/activation:         NOT_AUTHORIZED / NOT_AUTHORIZED
```

## Scope correction and next gate

This review closes a conceptual ambiguity but does not bypass implementation work. The accepted synthetic implementation remains unchanged and historical. A future live-capable adapter/executor must be separately generated, reviewed and accepted against this contract; the contract itself must first receive a separate Class D acceptance decision.

## Next action

`review-and-accept-non-executing-selected-provider-local-supply-evidence-live-input-adapter-and-execution-authorization-contract-candidate-boundary`

Acceptance may freeze the exact eight-artifact contract candidate only. It may not supply a live owner decision or coordinate receipt, issue or activate execution authorization, open a provider path, run evidence collection, produce a local-supply map or create runtime state.
