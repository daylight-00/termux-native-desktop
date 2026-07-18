# Active task: acquire exact GTK 3 core-pair provider evidence

> Task ID: `acquire-gtk3-core-provider-evidence`
>
> Expected state on completion: exact Termux glibc candidate evidence is retained for the selected GDK/GTK 3 core pair, or one precise package/recipe blocker is recorded. No installation, target population, deployment, or activation occurs.

## Objective

Inspect the approved Termux glibc package index and pinned glibc recipe repository for the provider family that can produce the exact selected GTK 3.24.49 GDK and GTK SONAMEs.

## Why now

The AT-SPI2 accessibility tranche stopped without authority because the approved index has no `at-spi2-core-glibc` package and the pinned recipe source has no AT-SPI2/ATK root; only ordinary Termux/bionic packages were observed. The next two selected gaps share one GTK 3.24.49 Debian lineage and should be investigated atomically before the independent libSELinux platform tranche.

## Known selected coordinates

```text
selected:3b13f088b32606984a58  libgdk-3.so.0.2417.32  lookup libgdk-3.so.0
selected:7bf9d7a4d1980f5e0a95  libgtk-3.so.0.2417.32  lookup libgtk-3.so.0
reference package:                libgtk-3-0t64:arm64
reference lineage:                3.24.49-3
pinned glibc recipe root:         not yet identified
current root mapping:             NONE_REVIEWED_ROOT
```

## In scope

- read-only inspection of approved glibc package metadata;
- exact package names, versions, filenames, sizes and SHA-256 values;
- exact GDK/GTK member digests, ELF identities, SONAMEs and alias chains;
- pinned recipe root or roots, complete recipe tree, dependencies and adaptation semantics;
- direct pair binding and closure against already accepted providers;
- optional backend and accessibility dependencies, conflicts, exclusions, update and rollback boundaries.

## Out of scope

Package-manager mutation, installation, target generation, materialization, deployment, activation, complete GTK functional validation, accessibility service activation, broad backend authority, or acceptance of a bionic package as a glibc provider.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/at-spi2-core-provider-evidence-blocker.md`
- `docs/evidence/cairo-bounded-provider-authority.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-gaps.tsv`

## Pending external inputs

None before approved-index and pinned-repository inspection. Use one read-only Termux acquisition probe only when exact package bytes cannot be retained in the sandbox evidence path.

## Stop conditions

Stop without authority if no exact glibc candidate exists, the two identities do not form a coherent bounded provider pair, SONAME or alias continuity fails, recipe provenance is missing, runtime closure contains unresolved mandatory providers, optional backend or accessibility behavior is ambiguous, or a member/alias collision exists.

## Next valid action

Inspect the approved Termux glibc index for GTK 3 package names and locate the exact producing root in pinned `termux-pacman/glibc-packages` before acquiring any archive.

## Completion criteria

- Exact package/member/SONAME/alias/recipe/dependency/pair-binding coordinates are retained for both members, or one precise blocker is recorded.
- Optional backend, accessibility, adaptation, conflict, exclusion, update and rollback boundaries are explicit.
- No target, materialization, deployment or activation occurs.
