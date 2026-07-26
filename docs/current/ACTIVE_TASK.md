# Active task: review and accept the non-mutating selected target manifest boundary

> Task ID: `review-and-accept-non-mutating-selected-target-manifest-boundary`
>
> Expected state on completion: accept the exact reviewed 82-row target policy and companion object/alias relations while preserving `UNPOPULATED_SCHEMA_ONLY` and prohibiting copy, installation, population, materialization, deployment and activation.

## Objective

Review the exact `SELECTED-TARGET-MANIFEST-REVIEW-001` output as a Class D target-policy decision. Acceptance may freeze proposed target paths, node types, owner/mode/mutability policy, SONAME alias relations, collision results, update/rollback domains and validation gates. It may not populate a target.

## Why now

The accepted 41-member current composition was translated into 41 concrete `SHARED_PROVIDER/lib/*` rows and 41 SONAME-alias rows. All 82 paths are unique, all aliases resolve to included concrete rows, all atomic families are complete, deferred `libtasn1.so.6.6.4` is absent, and the collision table is empty.

## In scope

- verify exact manifest, object-binding, alias-binding, collision and metadata digests;
- accept or reject the proposed target-policy boundary as one Class D decision;
- preserve all rows as `UNPOPULATED_SCHEMA_ONLY`;
- preserve `TARGET-MANIFEST-ACCEPTANCE-OPEN` until the acceptance record is committed;
- identify the separate intervention-lift and supply-byte-binding gate required before materializer design.

## Out of scope

Copying, extracting or installing bytes; creating directories or symlinks; binding retained archive bytes for population; changing package, loader or live-prefix state; generating caches or schemas; enabling modules or services; target population; immutable generation creation; selector publication; deployment; display execution; or activation.

## Required reading

- `docs/evidence/selected-obsidian-target-manifest-review.md`
- `docs/evidence/selected-obsidian-provider-composition-boundary-acceptance.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-manifest.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-manifest-alias-bindings.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/profiles/target-layout-schema.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/profiles/target-layout-invariants.md`
- `docs/decisions/0005-proportional-assurance-depth.md`

## Pending external inputs

None. The exact manifest candidate and review evidence are repository-local.

## Stop conditions

Stop if any digest drifts, any target path or alias collides, any alias target is absent, any atomic family is partial, deferred libtasn1 appears, any row is population-authorized, or acceptance would require supply-byte acquisition or filesystem mutation.

## Completion criteria

A separate acceptance record freezes the exact candidate digests and changes only target-policy authority. Population, materialization, deployment and activation remain blocked.

## Next valid action

Review and accept the exact non-mutating target manifest boundary only. Do not populate a target.
