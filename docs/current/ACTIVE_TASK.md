# Active task: prepare the atomic AT-SPI2/ATK 2.56.2 glibc candidate family

> Task ID: `prepare-at-spi2-core-2-56-2-atomic-glibc-candidate`
>
> Expected state on completion: one exact Class B production recipe candidate and one isolated Class C candidate archive set coherently provide `libatk-bridge-2.0.so.0.0.0`, `libatk-1.0.so.0.25611.1` and `libatspi.so.0.0.1`, or the lane stops with a precise source, recipe, dependency, atomicity or service-lifecycle blocker. No provider authority, publication, installation, target population, D-Bus activation, accessibility enablement, deployment or selected-generation activation occurs.

## Objective

Prepare the second authorized missing-provider production lane as one atomic AT-SPI2/ATK family. Establish exact source lineage, production recipe semantics, package/file surfaces, three ELF identities, dependency closure, GTK accessibility binding and disabled-by-default service boundaries without splitting the family.

## Why now

Exact project-produced `libXdamage.so.1.1.0` now has bounded provider authority for the selected GTK 3.24.49 GDK X11 damage-extension capability. The accepted production order authorizes AT-SPI2/ATK candidate preparation next and requires it before GTK 3 core candidate preparation.

## Authoritative selected identities

```text
source family:       at-spi2-core 2.56.2
selected members:    libatk-bridge-2.0.so.0.0.0
                     libatk-1.0.so.0.25611.1
                     libatspi.so.0.0.1
required SONAMEs:    libatk-bridge-2.0.so.0
                     libatk-1.0.so.0
                     libatspi.so.0
atomicity:           one source and coordinated package/archive family
```

## In scope

- acquire and pin the exact upstream 2.56.2 source tag/commit and archive SHA-256;
- derive a production Termux glibc recipe candidate without private evidence-harness logic;
- classify every Android/Termux adaptation and package split;
- build only in an isolated workspace with no package-database or live-prefix mutation;
- retain complete package manifests, all three exact members and aliases;
- verify direct `DT_NEEDED` closure and controlled loading without cross-world escapes;
- inventory D-Bus service, helper, schema, registry and accessibility-related files;
- keep all services and accessibility behavior disabled and unactivated;
- define coordinated update, removal and rollback boundaries.

## Out of scope

Provider authority, accepting only one or two members, approved-supplier publication, package installation, D-Bus bus ownership, registry-daemon acceptance, accessibility enablement, schema installation, target layout, materialization, deployment or activation.

## Required reading

- `docs/evidence/libxdamage-bounded-provider-authority.md`
- `docs/evidence/at-spi2-core-provider-evidence-blocker.md`
- `docs/evidence/missing-glibc-provider-production-boundary.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `docs/decisions/0005-proportional-assurance-depth.md`

## Pending external inputs

None. Source and recipe acquisition must use the established bounded Termux/network and bundle workflow when execution begins.

## Completion criteria

One machine-readable and narrative candidate review records exact source, recipe, producing environment, archive set, all three members and aliases, dependency closure, GTK binding, complete service/helper inventory, protected-state invariance, collision/exclusion state and coordinated update/rollback. Production recipe and private isolation harness must be separated before qualification succeeds.

## Stop conditions

Stop if exact 2.56.2 source lineage cannot be pinned, one coherent source cannot produce all three selected identities, package splitting changes their coordinated lifecycle, a required dependency lacks accepted authority or an explicitly bounded candidate lane, service activation is required merely to validate the libraries, controlled loading escapes into bionic/live state, or protected state changes.

## Next valid action

Design and execute a bounded read-only/source-acquisition and recipe-shape probe. Do not install the ordinary Termux/bionic packages, copy installed bytes, start accessibility services or widen into GTK 3 core.
