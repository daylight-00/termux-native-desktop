# Active task: generate and review a non-mutating selected-provider local-supply-map contract

> Task ID: `generate-and-review-non-mutating-selected-provider-local-supply-map-contract`
>
> Expected state on completion: a separate 41-row contract defines how future local regular-file evidence must bind each accepted object plan row to an exact immutable result, index, container/member locator, member digest and size. No provider byte is acquired, read, extracted or localized.

## Objective

Translate the accepted non-executing materializer design into an auditable local-supply-map schema and validation contract. The map contract must remain non-mutating and cannot itself constitute a populated local map or execution authorization.

## Why now

`SELECTED-PROVIDER-MATERIALIZER-DESIGN-ACCEPT-001` accepts the exact 41-object, 20-state, 24-operation, 20-preflight, 18-verification and 11-recovery design boundary. The next unresolved interface is the future 41-row local read-only supply map required before any execution authorization can be reviewed.

## In scope

- define one local-supply contract row for each of the 41 accepted object-plan rows;
- bind expected result outer digest, result-index identity, container class, exact artifact/member locator, member digest, size and SONAME;
- define no-follow regular-file and ownership/mode checks for a future local path;
- define completeness, duplicate, collision, immutable-input and failure semantics;
- define a canonical map receipt schema and review-only acceptance gate;
- preserve separate execution authorization and all runtime mutation blockers.

## Out of scope

Searching local storage for provider bytes; downloading or reading retained results; extracting members; creating local supply paths; creating the generation root, objects, generations, receipts, locks, hardlinks, symlinks or selectors; implementing or running the materializer; target population, publication, deployment or activation.

## Required reading

- `docs/evidence/selected-target-materializer-runtime-preflight-design-boundary-acceptance.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-materializer-runtime-preflight-design-boundary-acceptance.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-materializer-object-plan.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-indexed-replacement-review.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-materializer-input-contract.tsv`

## Pending external inputs

None for contract generation. Producing an actual local map requires a later separately authorized, read-only localization/evidence transaction.

## Stop conditions

Stop if the contract reads or searches local provider bytes, authorizes download or extraction, invents a local path, permits symlink-following, weakens exact digest/index/member checks, creates execution authorization or changes runtime state.

## Completion criteria

A deterministic machine-readable and narrative 41-row local-supply-map contract is generated and reviewed. It records zero populated local paths and keeps execution authorization, byte acquisition, root creation, population, materialization, publication, deployment and activation blocked.

## Next valid action

Generate and review the contract only. Do not search for, acquire, read, extract or localize provider bytes.

Do not acquire or populate provider bytes.
