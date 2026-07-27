# Active task: review and accept the non-mutating local-supply evidence authorization and coordinate-receipt contract boundary

> Task ID: `review-and-accept-non-mutating-selected-provider-local-supply-evidence-authorization-and-coordinate-receipt-contract-boundary`
>
> Expected state on completion: the exact owner-authorization token schema, canonical 41-row coordinate-receipt schema, 30 validation rules and metadata are accepted as a bounded non-mutating interface. No token, coordinate, provider read or execution authority is created.

## Objective

Review the exact candidate produced by `SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-COORDINATE-CONTRACT-REVIEW-001` and decide whether its owner approval, time/replay/revocation, repository/remote/executor binding, complete coordinate-set and canonical digest rules may become accepted project authority.

## Why now

The accepted read-only evidence-transaction design requires two future external inputs before execution can ever be considered. The candidate now defines an 18-claim immutable owner token, a canonical 41×10 coordinate receipt and 30 fail-closed validation rules while preserving zero live tokens and zero coordinates.

## In scope

- freeze the exact four candidate artifacts by SHA-256;
- confirm the 18 required owner-authorization claims;
- confirm the exact accepted contract/design, repository, remote, executor, expiry, revocation and receipt-digest bindings;
- confirm the exact 41-row/10-field coordinate-receipt contract;
- confirm all 30 validation rules and whole-receipt rejection on any missing, duplicate, unknown or inferred coordinate;
- confirm zero current tokens, receipts, coordinates, paths and provider reads;
- record a separate acceptance decision and next evidence-authorization issuance design gate.

## Out of scope

Issuing a live owner token, supplying a coordinate receipt, searching local storage, opening or reading provider files, downloading or extracting results/packages, implementing or running the evidence collector, producing or accepting a local map, creating runtime roots, population, materialization, publication, deployment or activation.

## Required reading

- `docs/evidence/selected-provider-local-supply-evidence-authorization-coordinate-receipt-contract-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-owner-authorization-token-schema.json`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-coordinate-receipt-schema.json`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-coordinate-validation-contract.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-coordinate-contract-metadata.tsv`

## Pending external inputs

None for contract acceptance. A live owner decision, immutable token and complete local coordinate receipt require later separately reviewed transactions.

## Stop conditions

Stop if acceptance issues a token, populates a coordinate or path, grants discovery or provider-read authority, permits partial or inferred coordinates, weakens baseline/digest/revocation binding, authorizes execution or changes runtime state.

## Completion criteria

A separate acceptance record freezes the exact four candidate artifacts and preserves zero live authority. Token issuance, coordinate receipt production, evidence execution and all runtime effects remain blocked.

## Next valid action

Review and accept the contract boundary only. Do not issue, search, acquire, open, read, extract, localize, populate or execute.

Do not acquire or populate provider bytes.
