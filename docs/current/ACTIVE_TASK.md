# Active task: generate and review a non-executing local-supply evidence authorization issuance and coordinate-receipt production transaction implementation candidate

> Task ID: `generate-and-review-non-executing-selected-provider-local-supply-evidence-authorization-issuance-and-coordinate-receipt-production-transaction-implementation-candidate`
>
> Expected state on completion: a deterministic non-executing implementation candidate enforces the accepted 14-input/18-state/36-operation/20-failure design and 18-claim/41-row/10-field/30-rule interface using synthetic fixtures only, while live token issuance, coordinate production, provider reads and evidence execution remain absent and unauthorized.

## Objective

Translate `SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-DESIGN-ACCEPT-001` into a reviewable implementation candidate. The candidate must parse and validate explicit owner-decision and coordinate inputs, enforce baselines, time, revocation, replay, canonicalization, inactive staging, failure receipts and protected-state checks without receiving live inputs or creating authority.

## Why now

The exact issuance/production transaction design is accepted, but no implementation exists. A separately reviewed non-executing implementation candidate is required before any owner decision, coordinate receipt or execution authorization can be considered.

## In scope

- implement deterministic parsers and validators for accepted schemas;
- implement the 14/18/36/20 state and operation boundary;
- implement canonical inactive candidate and failure-receipt serialization;
- implement revocation, expiry, anti-replay and digest cross-binding checks;
- use synthetic fixtures only;
- prove zero live token, coordinate, provider read and runtime effect;
- preserve repository, remote, package-database and live-prefix invariance.

## Out of scope

Supplying a real owner decision, issuing or activating a token, producing or accepting a live coordinate receipt, searching storage, opening or reading provider files, downloading or extracting evidence, running against live coordinates, producing a local map, creating runtime roots, population, materialization, publication, deployment or activation.

## Required reading

- `docs/evidence/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-boundary-acceptance.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-boundary-acceptance.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-operation-contract.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-failure-contract.tsv`

## Pending external inputs

None for implementation-candidate generation. Live owner decisions and local coordinates require later separate authorization.

## Stop conditions

Stop if implementation uses a live token or coordinate, searches or infers a path, opens provider bytes, activates authority, changes accepted cardinality, creates runtime state or weakens failure/invariance rules.

## Completion criteria

A deterministic implementation candidate and synthetic test suite reproduce the accepted design, emit no live authority and remain behind separate implementation acceptance and execution gates.

## Next valid action

Generate and review the implementation candidate only. Do not issue, activate, search, acquire, open, read, extract, localize, populate or execute against live inputs.

Do not acquire or populate provider bytes.
