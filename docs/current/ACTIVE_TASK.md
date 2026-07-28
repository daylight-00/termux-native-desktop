# Active task: review and accept the non-executing live-input adapter and execution-authorization implementation candidate

> Task ID: `review-and-accept-non-executing-selected-provider-local-supply-evidence-live-input-adapter-and-execution-authorization-implementation-candidate-boundary`
>
> Expected state on completion: the exact six-artifact repository-owned synthetic implementation is accepted as bounded non-executing implementation authority while live inputs, authorization issuance, replay persistence, provider reads, evidence execution and runtime effects remain unauthorized.

## Objective

Review the exact implementation candidate qualified by `SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-IMPLEMENTATION-REVIEW-001` and, if unchanged, freeze its source, fixture, negative cases, 164-row coverage ledger, synthetic success result and metadata as a separate acceptance boundary.

## Why now

The accepted contract is implemented with exact coverage for ten input channels, twenty adapter-envelope fields, 27 execution-authorization claims, 37 validations, 18 states, 32 operations and 20 failures. The candidate has one deterministic success case and twenty fail-closed cases, with zero provider reads, zero writes and zero live authority.

## In scope

- regenerate and byte-compare the six candidate artifacts;
- verify all frozen SHA-256 values and exact cardinalities;
- run the positive and twenty negative synthetic cases;
- prove the CLI accepts only the exact repository-owned fixture;
- prove the accepted synthetic implementation remains an immutable oracle and is not invoked;
- prove live-to-synthetic rewriting, replay persistence, provider opening, provider reads and writes remain absent;
- record append-only implementation acceptance and advance the next task.

## Out of scope

Supplying live owner decisions, tokens, coordinates, revocation snapshots or execution authorization; accepting arbitrary input paths; searching storage; opening or reading provider files; persisting a replay tuple; delegating to a live evidence executor; producing a local-supply map; generation-root creation; population, materialization, publication, deployment or activation.

## Required reading

- `docs/evidence/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-review.md`
- `docs/evidence/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-contract-boundary-acceptance.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-metadata.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-coverage.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-negative-cases.json`

## Pending external inputs

None. Live documents and authorization belong to later separate transactions and must not be supplied during implementation acceptance.

## Stop conditions

Stop if regeneration differs, any artifact digest or cardinality differs, a negative case does not fail closed, the CLI accepts a non-exact fixture, the implementation imports discovery/network/process surfaces, any provider path is opened, any provider byte is read, any replay tuple is persisted, the accepted synthetic implementation is invoked, or current live authority becomes nonzero.

## Completion criteria

The exact six-artifact candidate is accepted without changing its bytes and with all live-input, provider-read, replay-persistence, evidence-execution and runtime gates still closed.

## Next valid action

Review and accept the exact non-executing implementation candidate boundary only.

Do not supply, discover, open, read, localize, populate or execute against live provider inputs.

Do not acquire or populate provider bytes.
