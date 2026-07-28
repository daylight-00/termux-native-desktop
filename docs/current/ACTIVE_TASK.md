# Active task: generate and review the non-executing read-only local-supply evidence transaction implementation candidate

> Task ID: `generate-and-review-non-executing-selected-provider-local-supply-map-evidence-transaction-implementation-candidate`
>
> Expected state on completion: a deterministic repository-owned synthetic implementation candidate covers the already accepted 12-input, 16-state, 32-operation and 18-failure read-only evidence-transaction design while live coordinates, provider opens, provider reads, receipt production and runtime effects remain unauthorized.

## Objective

Implement the exact accepted local-supply-map evidence transaction design as a non-executing synthetic candidate, preserving explicit-coordinate-only input, bounded read semantics and fail-closed behavior without opening any provider path.

## Why now

The live-input adapter and execution-authorization implementation is now accepted as an immutable synthetic-only boundary. Evidence delegation intentionally remains unexecuted and requires a separate implementation review and acceptance before any live provider read can be considered.

## In scope

- map the accepted 12 inputs, 16 states, 32 operations and 18 failures to implementation coverage;
- create deterministic repository-owned success and fail-closed fixtures;
- validate explicit synthetic coordinates as text only;
- model bounded provider-read sequencing without opening files;
- prove zero provider reads, writes and live authority;
- add a separate implementation candidate review and acceptance gate.

## Out of scope

Live owner decisions, tokens, coordinate receipts, revocation snapshots or execution authorization; path discovery; opening or reading provider files; producing a live local-supply map; replay persistence; generation-root creation; population, materialization, publication, deployment or activation.

## Required reading

- `docs/evidence/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-boundary-acceptance.md`
- `docs/evidence/selected-provider-local-supply-map-evidence-transaction-design-boundary-acceptance.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-design-metadata.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-operation-contract.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-failure-contract.tsv`

## Pending external inputs

None. Live coordinate and authorization documents belong to a later execution transaction and must not be supplied during synthetic implementation review.

## Stop conditions

Stop if the implementation accepts arbitrary paths, searches storage, opens a provider file, reads provider bytes, persists replay state, writes runtime state, weakens any accepted cardinality or creates live authority.

## Completion criteria

A reproducible synthetic-only implementation candidate covers the exact accepted evidence-transaction design and passes deterministic positive and fail-closed tests with zero provider reads, writes and live authority.

## Next valid action

Generate and review the synthetic-only evidence-transaction implementation candidate only.

Do not supply, discover, open, read, localize, populate or execute against live provider inputs.

Do not acquire or populate provider bytes.
