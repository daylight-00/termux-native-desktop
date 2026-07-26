# Active task: generate and review a non-mutating selected target manifest

> Task ID: `generate-and-review-non-mutating-selected-target-manifest`
>
> Expected state on completion: produce and review a deterministic dry-run target manifest for the accepted bounded composition without copying, installing, populating, deploying, or activating anything.

## Objective

Translate the accepted Class D composition boundary into proposed target rows under the existing target-layout schema. This task is evidence generation and review only; it does not accept target population.

## Why now

`SELECTED-COMPOSITION-ACCEPT-001` accepted the exact zero-gap composition boundary: 42 reviewed provider decision rows, 41 included current-scope members, one profile-deferred libtasn1 member, and zero SONAME or alias collisions. Target paths and materialization order have not been decided.

## In scope

- derive proposed target rows only from the 41 included composition members;
- preserve exact concrete-member and SONAME-alias identities;
- keep `libtasn1.so.6.6.4` excluded from the current target manifest;
- validate target-layout schema, path uniqueness, alias targets, atomic-family grouping, and collision absence;
- record a deterministic non-mutating manifest and review decision;
- identify the exact next gate for target-population acceptance.

## Out of scope

Copying or extracting provider bytes into a target, installing packages, creating live symlinks, changing loader paths, generating caches or schemas, enabling modules or services, adding data, including deferred libtasn1, deployment, display execution, or activation.

## Required reading

- `docs/evidence/selected-obsidian-provider-composition-boundary-acceptance.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/profiles/target-layout-schema.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/profiles/target-layout-invariants.md`
- `docs/decisions/0005-proportional-assurance-depth.md`

## Pending external inputs

None. The accepted composition tables and target-layout schema are sufficient for a non-mutating manifest review.

## Stop conditions

Stop if any included member lacks a unique target path, any alias collides, an atomic family cannot be represented without partial membership, or the manifest requires package-wide, deferred, service, module, schema, data, or activation authority. Such a finding requires a separate composition-repair transaction.

## Completion criteria

A deterministic dry-run manifest is generated and reviewed with zero target-path or alias collisions, exact 41-member inclusion, exact libtasn1 exclusion, and no filesystem mutation. Target population must remain unaccepted for a separate transaction.

## Next valid action

Generate and review the non-mutating manifest only. Do not populate a target.
