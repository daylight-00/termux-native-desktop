# Selected D-Bus Provider Closure Pilot

## Status

Active architecture-discrimination experiment.

Current stage:

```text
control capture: PASS
initial static traversal harness bug: fixed
complete static traversal: PASS
control/static libcap selection mismatch: found
ownership-aware static rerun: pending
candidate materialization: blocked until static/runtime sets agree
```

## Provenance

First-hand experiment design and device evidence derived from:

```text
docs/refactor/0019-selected-closure-pilot-decision-criteria.md
docs/refactor/0026-dbus-pilot-control-static-selection-mismatch.md
```

## Question

Can the broad Debian-rootfs library farm be replaced, for one bounded workload class, by a smaller selected provider closure that has:

```text
explicit identity
concrete provider bytes
package provenance
world-owned exclusion
candidate-specific validation
provable actual selection
```

without changing the active broad farm used as control/reference?

## Baseline

```text
active substrate:
    APT/dpkg-owned glibc 2.42 recovery substrate

active provider control:
    broad farm under $HOME/gl/lib

root provider under study:
    libdbus-1.so.3
```

## Minimal probe

The probe calls only:

```text
dbus_get_version()
```

and remains alive briefly so `/proc/<pid>/maps` can be captured.

Observed result:

```text
libdbus runtime version: 1.16.2
control capture: PASS
```

## Control runtime evidence

Relevant actual mapped objects:

```text
WORLD / substrate paths:
    $PREFIX/glibc/lib/ld-linux-aarch64.so.1
    $PREFIX/glibc/lib/libc.so.6
    $PREFIX/glibc/lib/libm.so.6

ROOTFS provider paths:
    libdbus-1.so.3.38.3
    libsystemd.so.0.40.0
    libcap.so.2.75
```

This is a strong boundedness signal, but candidate work remains blocked until static classification matches actual control selection.

## Static traversal finding

The completed static graph showed:

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

The first classifier incorrectly selected prefix `libcap.so.2.69` as `WORLD_PREFIX`, while runtime maps proved that farm-first control selected Debian rootfs `libcap.so.2.75`.

The rule:

```text
exists under $PREFIX/glibc/lib
    => WORLD
```

is therefore rejected.

## Current classification model

The discovery harness now models:

```text
1. actual farm-first control search order
2. explicit protected package ownership
3. prefix providers separately from world substrate
```

Classes:

```text
WORLD_SUBSTRATE
PROVIDER_ROOTFS
PROVIDER_PREFIX
REJECTED_SHADOWS_WORLD
REJECTED_NON_ROOTFS_CONTROL
UNRESOLVED
```

Default protected package set for the pilot:

```text
glibc
```

This keeps the first world contract narrow and evidence-based.

## Evidence contract

### `graph.tsv`

```text
consumer
needed
classification
selected_path
selection_reason
```

### `providers.tsv`

Rootfs providers:

```text
path
package
version
sha256
build_id
```

### `prefix-providers.tsv`

Non-protected prefix providers:

```text
path
package
version
sha256
build_id
```

### `world-prefix.tsv`

Protected substrate objects only:

```text
path
package
version
sha256
build_id
```

The historical filename is retained for continuity, but its semantics are now explicitly protected ownership rather than all prefix objects.

## Decision boundary

Do not yet implement:

```text
provider store
candidate activation
universal resolver
global gl sync
farm replacement
```

Next gate:

```text
ownership-aware static provider set
    ==
actual runtime mapped provider set
```

Only then proceed to concrete provider-byte materialization and candidate-specific loader validation.
