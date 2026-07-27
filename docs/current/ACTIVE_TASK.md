# Active task: generate and review non-mutating local-supply evidence authorization and coordinate-receipt contracts

> Task ID: `generate-and-review-non-mutating-selected-provider-local-supply-evidence-authorization-and-coordinate-receipt-contract`
>
> Expected state on completion: deterministic non-mutating schemas define an owner authorization token and canonical 41-row coordinate receipt while all live coordinate values remain absent and provider reads remain unauthorized.

## Objective

Translate the accepted read-only evidence-transaction design into exact token and coordinate-receipt interface contracts. The contracts must bind owner approval, repository and remote baselines, executor identity, expiry, the accepted design and contract digests, and a complete 41-row coordinate set without supplying any actual local path.

## Why now

`SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-DESIGN-ACCEPT-001` accepts the exact 12-input/16-state/32-operation/18-failure design while preserving zero coordinates and zero reads. Before evidence execution can be considered, its two external authority inputs require separate deterministic schemas and fail-closed validation rules.

## In scope

- define an immutable owner-authorization token schema;
- define a canonical 41-row coordinate-receipt schema;
- bind both schemas to the accepted contract and evidence-design digests;
- require exact repository HEAD/tree and remote HEAD coordinates;
- require executor UID, transaction ID, issue/expiry times and receipt SHA-256;
- require 41 unique contract row IDs and zero missing/duplicate coordinates;
- define no-search, no-glob, no-environment-inference and no-basename-fallback rules;
- preserve zero current coordinate values and zero provider reads;
- define update, revocation and replay boundaries.

## Out of scope

Supplying a live token or coordinate receipt, searching local storage, opening or reading provider files, downloading or extracting results/packages, implementing or running the evidence collector, producing or accepting a local map, creating runtime roots, population, materialization, publication, deployment or activation.

## Required reading

- `docs/evidence/selected-provider-local-supply-map-evidence-transaction-design-boundary-acceptance.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-design-boundary-acceptance.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-input-contract.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-contract.tsv`

## Pending external inputs

None for contract generation. Live owner approval and local coordinates require a later separately authorized transaction.

## Stop conditions

Stop if a contract contains a live local path, grants discovery or provider-read authority, permits incomplete or inferred coordinates, weakens baseline/digest binding, authorizes execution or changes runtime state.

## Completion criteria

Machine-readable token and coordinate-receipt candidate schemas are deterministic, digest-bound, complete for 41 future rows and contain zero live coordinates. Evidence execution and all runtime effects remain blocked.

## Next valid action

Generate and review schemas only. Do not search, acquire, open, read, extract, localize, populate or execute.

Do not acquire or populate provider bytes.
