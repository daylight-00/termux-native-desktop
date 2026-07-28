# Active task: review and accept the non-executing synthetic local-supply-map evidence transaction implementation candidate

> Task ID: `review-and-accept-non-executing-selected-provider-local-supply-map-evidence-transaction-implementation-candidate-boundary`
>
> Expected state on completion: the exact six-artifact 78-row synthetic-only implementation boundary is accepted while provider opens, provider reads, live receipt production and runtime effects remain unauthorized.

## Objective

Review and accept the exact repository-owned implementation candidate for the already accepted 12-input, 16-state, 32-operation and 18-failure read-only evidence transaction design.

## Why now

The implementation candidate deterministically covers all 78 accepted design elements, one success fixture and eighteen fail-closed cases. All provider-read operations are modeled only; no provider path has been opened and no provider byte has been read.

## In scope

- verify and freeze the exact six candidate artifacts and their SHA-256 digests;
- re-run the 78-row coverage audit and all nineteen synthetic cases;
- confirm the 41-row/10-field synthetic coordinate model and 24 inherited validation rules;
- preserve zero provider opens, reads, writes, replay persistence and live authority;
- close only the implementation acceptance gate.

## Out of scope

Live authorization, coordinate production, local path discovery, provider open/read, live local-supply-map receipt production, replay persistence, generation-root creation, target population, materialization, publication, deployment or activation.

## Required reading

- `docs/evidence/selected-provider-local-supply-map-evidence-transaction-implementation-review.md`
- `docs/evidence/selected-provider-local-supply-map-evidence-transaction-design-boundary-acceptance.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-implementation-metadata.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-implementation-coverage.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-implementation-negative-cases.json`

## Pending external inputs

None. Live coordinates and authorization documents must not be supplied during synthetic implementation acceptance.

## Stop conditions

Stop if any accepted artifact digest changes, any coverage row is missing, the implementation accepts a live path, opens a provider file, reads provider bytes, writes replay/runtime state or widens authority.

## Completion criteria

The exact six-artifact implementation boundary is accepted with 78 coverage rows, one success, eighteen fail-closed cases and zero provider opens, reads, writes and live authority.

## Next valid action

Review and accept the exact synthetic-only implementation candidate boundary only.

Do not acquire, open, read or populate provider bytes.

Do not supply, discover, open, read, localize, populate or execute against live provider inputs.

Do not acquire or populate provider bytes.
