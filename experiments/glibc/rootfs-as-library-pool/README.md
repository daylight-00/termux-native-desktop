# Rootfs as a passive library pool

**Status:** historical experiment passed; broad-farm production interpretation superseded  
**Date:** 2026-07-04  
**Provenance:** first-hand summary

## Question

Can a PRoot-distribution Debian rootfs serve as a passive library warehouse for natively executed glibc binaries—providing Debian's broad library catalog without making PRoot the runtime?

## Baseline

- Termux glibc-repo provided a working Android-adapted glibc core but a limited package catalog.
- Debian provided the required desktop/application packages and metadata.
- PRoot-mediated normal workstation execution had already been rejected.

## Historical hypothesis

If the project needs library files and package metadata rather than the PRoot execution environment, a Debian rootfs can be demoted to a passive source.

A filtered symlink farm could expose broad shared-library coverage while excluding libc-family and other incompatible core objects.

## Historical procedure

1. Build `~/gl/lib` as symlinks into broad rootfs library directories.
2. Exclude libc-family/core runtime objects with a denylist.
3. Register the Termux glibc core first and the farm second.
4. Couple farm regeneration with loader-cache refresh and contamination checks.

## Evidence

- VS Code's large shared-library graph resolved through the core + farm model.
- Deliberate/accidental libc linker-script contamination produced the characteristic `invalid ELF header` failure, confirming that world protection was load-bearing.
- Application RPATH alone did not resolve every transitive dependency; loader-cache registration mattered in the historical composition.

## Historical result

The experiment proved:

```text
PRoot process execution is not required
for a native glibc application to consume Debian-derived artifacts.
```

It also established a productive research topology:

```text
Termux glibc core
    -> filtered Debian-rootfs farm
    -> app-local libraries preserved where required
```

## Current interpretation

The experiment did **not** prove that:

```text
one long-lived mutable Debian rootfs is the clean-system baseline;
the broad farm is the final production provider model;
all installed Debian dependencies should be promoted;
passive rootfs paths should remain runtime authority;
one accumulated rootfs should serve every oracle and supply question.
```

Later system-foundation and selected-closure work reclassify the objects.

```text
PRoot / Debian rootfs
    -> Build and Supply Plane
    -> oracle seed/scenarios
    -> package/dependency metadata
    -> artifact and behavioral controls

broad farm
    -> compatibility/research pool

selected materialized provider closure
    -> production/promotion target
```

The accepted architectural lesson is:

```text
package/supply authority
    can be separated from
runtime execution authority
```

The next lesson is stronger:

```text
oracle scenario state
    must also be separated from
promoted runtime and permanent supply authority
```

## PRoot baseline clarification

Use separate terms:

```text
oracle seed
oracle scenario
supply transaction
behavioral control
promoted runtime composition
```

For example, installing VS Code in a Debian rootfs can be a valid `oracle.vscode-control` scenario. Installing fonts can be a valid font-control experiment.

Neither installed state becomes the final workstation baseline merely because it produced useful evidence.

The target PRoot model is disposable/reconstructible scenario state, not one permanent Debian subsystem.

## Current decision

Retain this experiment as evidence that the rootfs can be demoted from process runtime to passive supply input.

Do not treat its historical farm implementation as final architecture.

Current direction:

```text
oracle/supply scenario
    -> locked artifacts and receipts
    -> selected materialization
    -> validation
    -> promotion outside PRoot
```

See:

```text
main:docs/system-foundation/01-essence.md
main:docs/system-foundation/03-system-model-v2.md
main:docs/system-foundation/05-ideal-target-architecture.md
main:docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
docs/refactor/0115-proot-oracle-supply-and-baseline-model.md
```
