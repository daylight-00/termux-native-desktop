# Active task: acquire exact libSELinux provider evidence

> Task ID: `acquire-libselinux-provider-evidence`
>
> Expected state on completion: exact Termux glibc candidate evidence is retained for selected `libselinux.so.1`, or one precise package/recipe blocker is recorded. No installation, target population, deployment, policy loading, labeling, or activation occurs.

## Objective

Inspect the approved Termux glibc package index and pinned glibc recipe repository for the provider family that can produce the exact selected `libselinux.so.1` runtime identity.

## Why now

The GTK 3 core-pair tranche stopped without authority because the approved index has no GTK 3 glibc package under the bounded candidate-name set and the pinned recipe source has no GTK 3 producing root; only the ordinary Termux/X11 bionic `gtk3` package was observed. `libselinux.so.1` is the last independent non-blocker selected identity before composition can only wait on explicitly recorded missing-provider families.

## Known selected coordinates

```text
selected:7e82ba054b7d9f26f80e  libselinux.so.1  lookup libselinux.so.1
reference package:                libselinux1:arm64
reference lineage:                3.8.1-1
pinned glibc recipe root:         not yet identified
current root mapping:             NONE_REVIEWED_ROOT
```

## In scope

- read-only inspection of approved glibc package metadata;
- exact package name, version, filename, size and SHA-256;
- exact member digest, ELF identity, SONAME and alias chain;
- pinned recipe root or precise absence, complete recipe tree, dependencies and adaptation semantics;
- direct selected-consumer binding and closure against already accepted providers;
- Android/Termux SELinux API behavior, policy-store, labeling, process-context, filesystem-context and service boundaries;
- conflict, exclusion, update and rollback boundaries.

## Out of scope

Package-manager mutation, installation, policy compilation or loading, context relabeling, `setenforce`, Android platform-policy mutation, target generation, materialization, deployment, activation, package-wide authority, or acceptance of a bionic package as a glibc provider.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/gtk3-core-provider-evidence-blocker.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-gaps.tsv`

## Pending external inputs

None before approved-index and pinned-repository inspection. Use one read-only Termux acquisition probe only when exact package bytes cannot be retained in the sandbox evidence path.

## Stop conditions

Stop without authority if no exact glibc candidate exists, SONAME or alias continuity fails, recipe provenance is missing, mandatory runtime closure is unresolved, Android/Termux SELinux semantics are ambiguous for the selected consumer scope, policy or labeling mutation would be required to validate the provider, or a member/alias collision exists.

## Next valid action

Inspect the approved Termux glibc index for libSELinux package names and locate the exact producing root in pinned `termux-pacman/glibc-packages` before acquiring any archive.

## Completion criteria

- Exact package/member/SONAME/alias/recipe/dependency/consumer coordinates are retained, or one precise blocker is recorded.
- Platform-policy, labeling, process-context, filesystem-context, service, adaptation, conflict, exclusion, update and rollback boundaries are explicit.
- No target, materialization, deployment, policy mutation, or activation occurs.
