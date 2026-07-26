# Active task: review and accept the read-only materializer/runtime-preflight design boundary

> Task ID: `review-and-accept-read-only-selected-provider-materializer-runtime-preflight-design-boundary`
>
> Expected state on completion: the exact non-executing design candidate is separately accepted or rejected as a bounded design authority record. Acceptance must preserve `execution_authorized=NO` and may not localize supply bytes, create the generation root or populate any target.

## Objective

Review the exact `SELECTED-PROVIDER-MATERIALIZER-DESIGN-REVIEW-001` candidate, its source locks, 41-row object plan, state machine, operation ordering, runtime preflight, verification, publication, rollback and recovery contracts. Decide only whether the design boundary is internally complete and authority-safe.

## Why now

The v112 candidate translates the accepted 82-row target policy, complete supply/index evidence, 41 exact member sizes, 59,142,800-byte runtime budget and seven generation contracts into a deterministic non-executing design. A separate acceptance record is required before any implementation or execution review.

## In scope

- verify all nine generated candidate artifacts and their digests;
- verify 41 exact regular-object and alias plans;
- verify the future execution-authorization gate precedes every mutating state;
- verify hardlink-only object reuse and no copy fallback;
- verify regular-before-alias and atomic-family barriers;
- verify the 20 runtime-preflight and 18 verification checks;
- verify receipt overflow, generation publication, selector ordering, rollback, resume and orphan handling;
- accept or reject the design without broadening runtime authority.

## Out of scope

Localizing, downloading, reading or extracting provider bytes; creating the generation base, object store, staging tree, generation, receipt, lock, hardlink or symlink; implementing or running a materializer; publishing selectors; target population; deployment; activation.

## Required reading

- `docs/evidence/selected-target-materializer-runtime-preflight-design-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-materializer-design-metadata.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-materializer-runtime-preflight-design.json`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-materializer-object-plan.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-materializer-state-machine.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-runtime-preflight-contract.tsv`

## Pending external inputs

None for design acceptance. A future execution review will require a separate 41-row local supply-localization contract and explicit execution authorization.

## Stop conditions

Stop if acceptance would authorize execution, byte acquisition, local supply reads, root creation, object or generation writes, copy fallback, partial atomic-family handling, selector publication, population, deployment or activation.

## Completion criteria

A separate acceptance record binds the exact candidate digests and either accepts or rejects the design. Even accepted design authority remains non-executing; all filesystem and byte effects stay blocked.

## Next valid action

Review and accept or reject the exact design boundary only. Do not implement, localize, acquire, extract, create, link, populate, publish, deploy or activate.

Do not acquire or populate provider bytes.
