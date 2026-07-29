# Selected-provider local-supply live-authority transaction implementation review

## Decision

`QUALIFIED_NON_EXECUTING_SYNTHETIC_LIVE_AUTHORITY_TRANSACTION_IMPLEMENTATION_CANDIDATE`

Review ID: `SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-IMPLEMENTATION-REVIEW-001`

Acceptance gate: `SELECTED-PROVIDER-LOCAL-SUPPLY-LIVE-AUTHORITY-TRANSACTION-IMPLEMENTATION-ACCEPTANCE-OPEN`

## Accepted design basis

The implementation candidate consumes only the repository-owned accepted design and its immutable source contracts. It does not consume owner activation, a live owner token, a live coordinate receipt, revocation evidence, trusted-time evidence, an execution authorization, a replay registry, selected-provider paths or provider bytes.

## Exact implementation artifacts

1. `implementation/selected_provider_local_supply_live_authority_transaction_candidate.py`
2. `review/selected-provider-local-supply-live-authority-transaction-implementation-synthetic-fixture.json`
3. `review/selected-provider-local-supply-live-authority-transaction-implementation-negative-cases.json`
4. `review/selected-provider-local-supply-live-authority-transaction-implementation-coverage.tsv`
5. `review/selected-provider-local-supply-live-authority-transaction-implementation-synthetic-success.json`
6. `review/selected-provider-local-supply-live-authority-transaction-implementation-metadata.tsv`

## Coverage

| Surface | Count |
|---|---:|
| accepted inputs | 20 |
| accepted states | 26 |
| accepted operations | 52 |
| accepted failures | 30 |
| exact direct coverage | 128 |
| inherited semantic coverage | 448 |

Every row is mapped as `MAPPED_SYNTHETIC_NOT_EXECUTED`. The candidate models five synthetic non-live document roles, forty-one synthetic coordinate rows and a ten-field replay tuple preview.

## Synthetic review cases

- success cases: 1
- fail-closed cases: 30
- synthetic document roles: 5
- synthetic coordinate rows: 41
- replay tuple fields: 10

The success case produces deterministic state and operation traces. Each negative case returns the exact accepted failure identity while all current authority counters remain zero.

## Current effects

| Effect | Count/state |
|---|---:|
| live documents accepted or consumed | 0 |
| execution authorizations | 0 |
| replay writes | 0 |
| selected-provider opens | 0 |
| selected-provider reads | 0 |
| provider bytes | 0 |
| local-supply maps | 0 |
| live authority | 0 |

The provider-open gate is never armed. The accepted orchestration implementation and previous synthetic implementations are not imported or invoked. No persistent filesystem or replay mutation occurs.

## Boundary

This review qualifies a separately acceptable implementation candidate only. It does not accept the candidate, authorize execution, create live authority documents, write replay state, open or read selected-provider paths, produce a local map, create a generation root, populate, materialize, publish, deploy or activate.

## Next action

`review-and-accept-non-executing-selected-provider-local-supply-live-authority-transaction-implementation-candidate-boundary`
