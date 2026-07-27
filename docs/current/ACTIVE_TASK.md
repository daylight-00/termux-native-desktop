# Active task: design and review a non-executing local-supply evidence authorization issuance and coordinate-receipt production transaction

> Task ID: `design-and-review-non-executing-selected-provider-local-supply-evidence-authorization-issuance-and-coordinate-receipt-production-transaction`
>
> Expected state on completion: a non-executing transaction design defines how a future explicit owner decision may issue one immutable read-only authorization token and how a complete explicit 41-row coordinate receipt may be produced, validated, revoked and archived. No token, coordinate, provider read or execution occurs during design.

## Objective

Translate the accepted 18-claim authorization and 41-row coordinate-receipt contract into an auditable future issuance/production transaction design. The design must define external inputs, owner decision verification, canonical serialization, replay/revocation state, explicit coordinate ingestion, whole-receipt validation, failure receipts and protected-state invariance.

## Why now

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-COORDINATE-CONTRACT-ACCEPT-001` accepts the exact non-mutating interface while preserving zero live tokens, zero coordinate rows and zero provider reads. Before issuance or coordinate production can be considered, its transaction boundary must be designed separately.

## In scope

- define exact owner-decision and coordinate-input interfaces;
- define token issuance, expiry, replay and revocation ordering;
- define explicit 41-row coordinate ingestion with no discovery or inference;
- define canonical token/receipt serialization and digest binding;
- define bounded transaction-scoped output and failure receipts;
- define repository, remote, package-database and live-prefix invariance checks;
- prove that design approval grants no issuance, read or execution authority.

## Out of scope

Issuing a live token, supplying or discovering coordinates, opening or reading provider files, downloading or extracting results/packages, implementing or running the evidence collector, producing or accepting a live local map, creating runtime roots, population, materialization, publication, deployment or activation.

## Required reading

- `docs/evidence/selected-provider-local-supply-evidence-authorization-coordinate-contract-boundary-acceptance.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-coordinate-contract-boundary-acceptance.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-owner-authorization-token-schema.json`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-coordinate-receipt-schema.json`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-coordinate-validation-contract.tsv`

## Pending external inputs

None for design. A live owner decision and explicit complete coordinate set require later separate authorization.

## Stop conditions

Stop if design issues a token, populates a coordinate, reads provider bytes, permits discovery or inference, weakens baseline/digest/revocation binding, authorizes evidence execution or changes runtime state.

## Completion criteria

A separate machine-readable and narrative transaction design covers issuance, coordinate production, ordering, revocation, failures and invariance. Live authority and all runtime effects remain absent and unauthorized.

## Next valid action

Design and review only. Do not issue, search, acquire, open, read, extract, localize, populate or execute.

Do not acquire or populate provider bytes.
