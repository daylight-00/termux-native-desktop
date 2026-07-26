# Active task: design and review a read-only selected-provider local-supply-map evidence transaction

> Task ID: `design-and-review-read-only-selected-provider-local-supply-map-evidence-transaction`
>
> Expected state on completion: a non-executing transaction design defines exact authorized input coordinates, bounded no-follow local reads, 41-row receipt production, failure handling and protected-state checks. No path is searched or read during design.

## Objective

Translate the accepted 41-row local-supply-map contract into an auditable read-only evidence transaction design. The design must explain how a future explicitly authorized transaction receives exact path coordinates, validates all 24 rules and emits or rejects a canonical 41-row receipt without creating runtime state.

## Why now

`SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-ACCEPT-001` accepts the exact contract boundary while preserving zero populated paths. Before any evidence collection can be authorized, the read set, input authority, ordering, race resistance, result receipt, failure cleanup and protected-state invariance must be designed separately.

## In scope

- define exact input-coordinate and authorization-token interfaces;
- define no-search, no-glob and no-environment-inference rules;
- define component `lstat`, `O_NOFOLLOW`, regular-file, owner and mode checks;
- define stable identity, size, SHA-256, ELF and SONAME validation order;
- define 41-row completeness and four atomic-family barriers;
- define canonical receipt and failure receipt production;
- define repository, remote, package-database and live-prefix invariance checks;
- prove that design approval grants no local read or execution authority.

## Out of scope

Searching local storage, supplying actual local paths, opening or reading provider bytes, downloading retained results, extracting packages or archives, creating the generation root or object store, implementing or executing the evidence collector or materializer, producing a live accepted map, target population, publication, deployment or activation.

## Required reading

- `docs/evidence/selected-provider-local-supply-map-contract-boundary-acceptance.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-contract-boundary-acceptance.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-contract.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-validation-contract.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-receipt-schema.json`

## Pending external inputs

None for read-only design. Actual path coordinates and provider reads require a later separately approved transaction.

## Stop conditions

Stop if design performs discovery, binds a real path, opens a provider file, downloads or extracts evidence, weakens no-follow or exact identity rules, accepts partial rows, authorizes execution or changes runtime state.

## Completion criteria

A separate machine-readable and narrative transaction design covers inputs, ordering, validation, receipt, failures and invariance. Local-map production and all runtime effects remain unauthorized.

## Next valid action

Design and review only. Do not search, acquire, open, read, extract, localize, populate or execute.

Do not acquire or populate provider bytes.
