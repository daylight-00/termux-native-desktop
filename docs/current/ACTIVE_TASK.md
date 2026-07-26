# Active task: design a read-only selected-provider materializer and runtime preflight contract

> Task ID: `design-read-only-selected-provider-materializer-and-runtime-preflight-contract`
>
> Expected state on completion: a non-executing design specifies exact input bindings, content-addressed object handling, staging order, verification, receipt generation, publication preflight, rollback and failure cleanup. No provider byte is acquired and no filesystem root or target node is created.

## Objective

Translate the accepted 82-row target policy, complete 41-member size census, 59,142,800-byte resource budget and seven generation contracts into an auditable materializer/preflight design without implementing or running it.

## Why now

The exact Pixman member size is 460,920 bytes, all 41 member sizes are exact, and the deterministic receipt reservation closes the final resource-budget blocker. The intervention is conditionally lifted only for read-only design review.

## In scope

- define immutable input and result interfaces;
- define content-addressed object-store and staging algorithms;
- define regular-file and relative SONAME-alias ordering;
- define hash, ELF, SONAME, dependency, collision and loader verification ordering;
- define receipt serialization and 1 MiB overflow abort behavior;
- define statvfs, owner, mode, same-device and symlink preflight;
- define publication, selector rollback, idempotent resume and orphan reporting;
- prove that every mutating operation remains behind a separate future authorization gate.

## Out of scope

Downloading or extracting provider bytes, creating the generation root, directories, files or symlinks, package installation, running a materializer, generating a live receipt, publishing selectors, target population, deployment or activation.

## Required reading

- `docs/evidence/selected-target-pixman-size-resource-budget-intervention-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-resource-budget-metadata.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-population-intervention-lift-review.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-generation-root-contract-review.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-manifest-boundary-acceptance.tsv`

## Pending external inputs

None for read-only design. Any operation requiring provider or filesystem bytes remains a separate blocked authority decision.

## Stop conditions

Stop if the design begins acquiring bytes, creating paths, relaxing exact digest checks, allowing partial atomic families, publishing selectors, or treating design approval as population authority.

## Completion criteria

A separate machine-readable and narrative design covers inputs, ordering, preflight, verification, receipt, publication, rollback and cleanup; negative tests reject mutation and authority widening. Population remains unauthorized.

## Next valid action

Design and review only. Do not acquire, extract, create, copy, install, populate, publish, deploy or activate.

Do not acquire or populate provider bytes.
