# 0026 — D-Bus Pilot Control/Static Selection Mismatch

## Status

The corrected static traversal completed, but comparison with the previously captured runtime maps revealed a semantically important mismatch in `libcap` provider selection.

This is not treated as a candidate-materialization failure. It is a resolver-classification correction discovered before candidate bytes were built.

## Observed runtime selection

The broad-farm control probe actually mapped:

```text
$PREFIX/glibc/lib/ld-linux-aarch64.so.1
$PREFIX/glibc/lib/libc.so.6
$PREFIX/glibc/lib/libm.so.6
$ROOTFS/usr/lib/aarch64-linux-gnu/libcap.so.2.75
$ROOTFS/usr/lib/aarch64-linux-gnu/libdbus-1.so.3.38.3
$ROOTFS/usr/lib/aarch64-linux-gnu/libsystemd.so.0.40.0
```

Therefore the observed rootfs provider set was:

```text
libdbus-1.so.3.38.3
libsystemd.so.0.40.0
libcap.so.2.75
```

## First complete static-classifier result

The static graph correctly traversed:

```text
libdbus
    -> libsystemd
    -> libc
    -> loader

libsystemd
    -> libcap
    -> libm
    -> libc
    -> loader
```

However, it classified:

```text
libsystemd -> libcap.so.2
    selected: $PREFIX/glibc/lib/libcap.so.2.69
    class: WORLD_PREFIX
```

while runtime maps proved:

```text
selected: $ROOTFS/usr/lib/aarch64-linux-gnu/libcap.so.2.75
```

## Root cause in the pilot classifier

The first classifier used:

```text
if exact SONAME exists under $PREFIX/glibc/lib:
    classify WORLD_PREFIX
else:
    inspect broad-farm control target
```

This rule was wrong for two reasons.

### 1. Prefix location is not semantic world ownership

`$PREFIX/glibc/lib` contains more than the core `glibc` package substrate.

A file living in the prefix can be supplied by another package and act as a provider rather than a protected world object.

Therefore:

```text
path location
    !=
semantic ownership
```

### 2. The control runtime search order was farm-first

The control probe was launched with:

```text
$HOME/gl/lib:$PREFIX/glibc/lib
```

Therefore an available farm object can be selected before a same-SONAME prefix object.

The static classifier must model the actual control search order before comparing candidate behavior with the control.

## Architecture consequence

The previous provisional class:

```text
WORLD_PREFIX
```

is too broad and is removed as a semantic rule.

The pilot now distinguishes:

```text
WORLD_SUBSTRATE
    explicit protected package ownership

PROVIDER_ROOTFS
    farm-first control target resolving into Debian rootfs

PROVIDER_PREFIX
    non-protected prefix package/provider selected when no farm-first target exists
```

For the first iteration, the explicit protected package set defaults narrowly to:

```text
glibc
```

This is intentionally conservative. More packages must not be promoted into world substrate merely because they install under `$PREFIX/glibc`.

## Control contamination rule

If the farm-first control path contains a provider for a SONAME whose prefix candidate is owned by an explicitly protected world package, the pilot now records:

```text
REJECTED_SHADOWS_WORLD
```

and fails discovery.

This turns protected-world exclusion into an explicit contract rather than relying on path order or a broad prefix test.

## Current closure interpretation

The evidence now strongly suggests a bounded runtime provider set of three rootfs objects:

```text
libdbus
libsystemd
libcap
```

with core substrate objects supplied by the protected `glibc` package:

```text
loader
libc
libm
```

This remains a hypothesis until the ownership-aware static rerun matches the runtime maps.

## Next gate

Rerun only static discovery with the ownership-aware classifier.

Acceptance requires:

```text
static rootfs provider set == runtime rootfs provider set

expected current set:
    libdbus
    libsystemd
    libcap

protected world set:
    only objects whose exact active paths are owned by protected world packages
```

Only after static and runtime selection agree should the pilot proceed to concrete provider-byte materialization.
