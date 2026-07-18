# Active task: acquire exact AT-SPI2 core accessibility provider evidence

> Task ID: `acquire-at-spi2-core-provider-evidence`
>
> Expected state on completion: exact Termux glibc candidate evidence is retained for the selected ATK bridge, ATK core, and AT-SPI runtime identities, or one precise package/recipe blocker is recorded. No installation, target population, deployment, or activation occurs.

## Objective

Inspect the approved Termux glibc package index and pinned glibc recipe repository for the coupled accessibility provider family that can produce the selected ATK bridge, ATK core, and AT-SPI SONAMEs.

## Why now

The exact Graphite2 1.3.14 member and stable SONAME alias are accepted as the bounded prerequisite for the Graphite shaping path compiled into exact HarfBuzz 10.1.0. The next three selected gaps share the Debian 2.56.2 accessibility lineage and should be investigated as one coupled tranche before the GTK core pair.

## Known selected coordinates

```text
selected:bcc68afe696f548e1b77  libatk-bridge-2.0.so.0.0.0  lookup libatk-bridge-2.0.so.0
selected:292a5f56eeea3bd65c4b  libatk-1.0.so.0.25611.1       lookup libatk-1.0.so.0
selected:36e7af00d16415ae9efa  libatspi.so.0.0.1              lookup libatspi.so.0
reference lineage:             2.56.2
pinned glibc recipe root:      not yet identified
current root mapping:          NONE_REVIEWED_ROOT
```

## In scope

- read-only inspection of approved glibc package metadata;
- exact package names, versions, filenames, sizes and SHA-256 values;
- exact member digests, ELF identities, SONAMEs and alias chains;
- pinned recipe root or roots, complete recipe tree, dependencies and adaptation semantics;
- GTK 3.24.49 accessibility consumer binding and coupled-family boundary;
- conflict, exclusion, update and rollback boundaries.

## Out of scope

Package-manager mutation, installation, target generation, materialization, deployment, activation, broad accessibility service authority, D-Bus session activation, complete GTK composition, or acceptance of a bionic package as a glibc provider.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/graphite2-harfbuzz-prerequisite-provider-authority.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-gaps.tsv`

## Pending external inputs

None before approved-index and pinned-repository inspection. Use one read-only Termux acquisition probe only when exact package bytes cannot be retained in the sandbox evidence path.

## Stop conditions

Stop without authority if no exact glibc candidate exists, the three identities do not form a coherent bounded provider family, SONAME or alias continuity fails, recipe provenance is missing, runtime closure contains unresolved providers, GTK consumer binding is ambiguous, or a member/alias collision exists.

## Next valid action

Inspect the approved Termux glibc index for packages matching AT-SPI2/ATK/bridge terminology and locate their exact producing root or roots in the pinned `termux-pacman/glibc-packages` repository before acquiring any archive.

## Completion criteria

- Exact package/member/SONAME/alias/recipe/dependency/consumer coordinates are retained for all available coupled members, or one precise blocker is recorded.
- Service, D-Bus, adaptation, conflict, exclusion, update and rollback boundaries are explicit.
- No target, materialization, deployment, or activation occurs.
