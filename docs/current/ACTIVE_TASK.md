# Active task: review and accept the read-only selected-provider local-supply-map evidence transaction design boundary

> Task ID: `review-and-accept-read-only-selected-provider-local-supply-map-evidence-transaction-design-boundary`
>
> Expected state on completion: the exact non-executing transaction design is accepted as bounded project authority while actual authorization tokens, coordinate receipts, provider reads, local-map production and runtime mutation remain absent and unauthorized.

## Objective

Review `SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-DESIGN-REVIEW-001` and decide whether its exact input, state, operation, failure and receipt contracts may become accepted non-executing design authority.

## Why now

The accepted 41-row/24-rule local-supply-map contract now has a deterministic design candidate covering 12 input contracts, 16 states, 32 ordered operations and 18 transaction failure classes. Acceptance must remain distinct from future evidence execution.

## In scope

- freeze the exact six design artifacts by SHA-256;
- confirm the 12/16/32/18 structure and inherited 41/24 contract boundary;
- confirm zero authorized coordinates and zero current provider reads;
- confirm authorization, baseline and contract gates precede any future provider read;
- confirm no-search, no-glob, no-environment-inference and no-basename-fallback rules;
- confirm bounded evidence-output writes and protected-state invariance;
- confirm successful output remains a candidate requiring separate acceptance;
- record a separate Class D design acceptance decision.

## Out of scope

Providing an execution token or coordinate receipt, searching local storage, opening or reading provider files, downloading or extracting results/packages, implementing or running the collector, producing or accepting a live local map, creating the generation root, target population, materialization, publication, deployment or activation.

## Required reading

- `docs/evidence/selected-provider-local-supply-map-evidence-transaction-design-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-input-contract.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-state-machine.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-operation-contract.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-failure-contract.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-receipt-contract.json`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-design-metadata.tsv`

## Pending external inputs

None for design acceptance. Actual evidence execution requires a later explicit owner authorization token and canonical coordinate receipt.

## Stop conditions

Stop if acceptance supplies a path, authorizes a provider read, permits discovery or inference, changes the contract counts, accepts runtime writes, produces a local map, authorizes execution or mutates protected state.

## Completion criteria

A separate acceptance record freezes the exact candidate artifacts and preserves zero coordinates, zero reads and zero runtime effects. Future evidence execution and map acceptance remain separate blocked gates.

## Next valid action

Review and accept the design boundary only. Do not search, acquire, open, read, extract, localize, populate or execute.

Do not acquire or populate provider bytes.
