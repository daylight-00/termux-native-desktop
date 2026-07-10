# 0029 — Second Selected-Closure Pilot Target: Obsidian AppDir CPU Path

## Status

The first bounded selected-provider pilot passed.

The next discriminating target is selected as:

```text
Obsidian extracted AppDir
CPU-path GUI startup
```

This target is chosen to test the major Stage 4 property not exercised by the minimal D-Bus probe:

```text
preservation of valid application-local $ORIGIN locality
```

while also testing a real application-domain composition across app-local, protected substrate, prefix-provider, and selected rootfs-provider boundaries.

## Why not generalize the D-Bus candidate immediately

The first pilot proves that a real selected-provider closure object class exists.

It does not prove that the three-object D-Bus closure is:

```text
a global world extension
an Electron-family closure
a universal glibc shared-provider set
```

Therefore the project must not promote the first candidate into a global provider by naming convention alone.

The next experiment should try to break the model at a stronger boundary.

## Why Obsidian is the best next discriminator

The existing Obsidian AppImage experiment established a mixed runtime composition:

```text
application-local Electron libraries
    from $ORIGIN / AppDir

Android-sensitive X11/xcb providers
    from $PREFIX/glibc/lib

GTK, NSS, GIO, font, and desktop providers
    from the broad farm control
```

The main executable originally had:

```text
RPATH: $ORIGIN
```

and the onboarding experiment explicitly preserved `$ORIGIN` when adding project search paths.

This makes Obsidian materially different from the synthetic D-Bus probe.

It can test whether selected closure resolution:

```text
preserves valid app-local libraries
protects world/substrate objects
classifies prefix providers semantically
materializes only external selected providers
handles a real GUI workload
```

without collapsing everything into one flat shared provider directory.

## Why CPU path first

The first Obsidian closure pilot should use the already validated CPU-mode application path.

Reason:

```text
application/runtime closure question
    should be separated from
Vulkan/ANGLE/Turnip provider-selection question
```

The existing project evidence already showed that CPU-mode Obsidian opens successfully with:

```text
--disable-dev-shm-usage
--ozone-platform=x11
--disable-gpu
```

Graphics-provider actual selection is independently evidenced elsewhere and should not contaminate this closure experiment.

## Required control capture

The control run should preserve the existing application payload and broad farm unchanged.

Capture:

```text
main process and descendant process set
/proc/<pid>/maps for all stable Obsidian-owned processes
LD_DEBUG or equivalent loader-selection evidence where practical
ELF identity for app-local objects actually mapped
prefix object identity and package ownership
rootfs/farm provider identity and package provenance
startup output
visible-window success
```

The process graph matters because Electron is multiprocess.

A single main-process map is not sufficient to characterize renderer/GPU/utility closures.

For the CPU-path first experiment, the primary required process classes are:

```text
main
renderer
utility
```

A GPU process may still exist in limited form depending on Electron behavior, but graphics-provider interpretation is out of scope for this closure claim.

## Classification model

For every mapped/required object:

```text
APP_LOCAL
    valid application payload locality selected before external providers

WORLD_SUBSTRATE
    explicitly protected substrate package ownership

PROVIDER_PREFIX
    non-protected provider package under the glibc prefix

PROVIDER_ROOTFS
    broad-farm control target resolving into Debian rootfs

UNRESOLVED_OR_DYNAMIC
    runtime-only or unresolved edge requiring explicit analysis
```

The model must not use physical prefix location as semantic ownership.

## Locality invariant

Candidate composition must preserve:

```text
valid APP_LOCAL selection
    before external selected provider closure
```

for objects that the application payload intentionally provides.

The experiment must detect and reject a candidate/provider object that shadows an app-local object unless the application contract explicitly requires replacement and validates it.

## Candidate flow

The target experiment sequence is:

```text
control launch
    -> process graph capture
    -> actual maps aggregation
    -> static ELF closure analysis
    -> APP_LOCAL / WORLD / PREFIX / ROOTFS classification
    -> runtime enrichment
    -> selected external provider bytes materialization
    -> provenance receipt
    -> candidate-specific CPU launch
    -> actual process maps proof
    -> control/candidate workload equivalence
```

## Workload equivalence gate

Minimum candidate success requires:

```text
Obsidian visible window opens
main/renderer/utility process set survives startup interval
application-local mapped set is preserved for validated local providers
external selected provider maps come from candidate bytes
protected substrate maps come only from allowed substrate objects
no broad-farm/rootfs provider leakage occurs
no unresolved relocation error occurs
```

The first candidate run does not need GPU acceleration enabled.

## Relationship to semantic ownership

The first D-Bus pilot validates the existence of:

```text
selected materialized shared-provider closure
```

as an object class.

The Obsidian pilot asks whether a real application domain can consume such a closure while preserving its own local runtime locality.

Only after that evidence should the project decide whether the physical object is best serialized as:

```text
provider.shared-libs.glibc
```

or split into narrower provider capability groups and application-domain bindings.

## Stop line

Do not yet:

```text
replace the broad farm
change the promoted Obsidian launcher
rewrite Obsidian payload RPATH globally
introduce a global provider store framework
add one universal resolver
make selected D-Bus closure world-global
```

The next work is a control capture and classification experiment, not production migration.
