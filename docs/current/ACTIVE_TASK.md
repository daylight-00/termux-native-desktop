# Active task: acquire exact Graphite2 provider evidence

> Task ID: `acquire-graphite2-provider-evidence`
>
> Expected state on completion: an exact Termux glibc candidate for selected `libgraphite2.so.3` is acquired and retained with package, member, SONAME, alias, recipe, dependency, and Pango/HarfBuzz consumer coordinates, or the identity remains open with one precise repository/candidate blocker. No installation, target population, deployment, or activation occurs.

## Objective

Close the next independent selected GTK composition gap by acquiring and reviewing exact Graphite2 provider evidence without installation.

## Why now

The libXdamage tranche reached its stop condition: the approved glibc package index has no `libxdamage-glibc` package and the pinned glibc recipe repository has no libXdamage root. That identity remains open with a precise blocker. Graphite2 is independent, has one selected SONAME, and has a pinned glibc recipe root.

## Known coordinates

```text
selected identity:      libgraphite2.so.3.2.1
selected row:           selected:5de74dd687fd1dd5ee3a
selected SHA-256:       e429689818c47c7eb3033cf7410a1d8dfb49891dc6ffe9c8a54a28d5bf15b208
required lookup/SONAME: libgraphite2.so.3
reference package:      libgraphite2-3:arm64 1.3.14-2+b1
recipe root:            gpkg/libgraphite
recipe commit:          9bdd20c1d36524a0ab016d9b71c748b0cbb20a34
recipe file/blob:       gpkg/libgraphite/build.sh @ 1fd081fa93558fd044a053afb26a170a2cef6a09
recipe version:         1.3.14
candidate state:        PINNED_RECIPE_ROOT_BINARY_NOT_YET_ACQUIRED
current root mapping:   NONE_REVIEWED_ROOT
```

## In scope

- approved glibc repository package metadata and exact archive acquisition without installation;
- exact member digest, ELF identity, SONAME and alias chain;
- pinned `gpkg/libgraphite` recipe semantics, including skipped install RPATH, disabled compare renderer, and direct VM mode;
- runtime dependency closure;
- selected Pango/HarfBuzz Graphite shaping consumer binding;
- conflict, exclusion, update and rollback boundaries.

## Out of scope

Installation, package-manager mutation, target generation, materialization, deployment, activation, HarfBuzz provider widening, broad text-stack authority, and complete GTK composition.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/libxdamage-provider-evidence-blocker.md`
- `docs/evidence/harfbuzz-bounded-provider-authority.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-exact-candidate-receipt-review.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/non-priority-generic-authority-ledger/gtk-gui.tsv`

## Pending external inputs

None before approved-index inspection. Request one read-only Termux acquisition probe only if exact package bytes cannot be retained in the sandbox evidence path.

## Stop conditions

Stop without authority if no exact glibc candidate can be acquired, the SONAME or alias does not match, recipe semantics cannot be bounded, runtime closure contains an unresolved provider, consumer binding is ambiguous, or a member/alias collision exists.

## Next valid action

Inspect the approved Termux glibc package index for the package produced by `gpkg/libgraphite`, then acquire and extract the exact archive without installation if available.

## Completion criteria

- Exact package, member, SHA-256, SONAME, alias, recipe, dependency, and consumer coordinates are retained, or one precise blocker is recorded.
- Adaptation, conflict, exclusion, update, and rollback boundaries are explicit.
- No target, materialization, deployment, or activation occurs.
