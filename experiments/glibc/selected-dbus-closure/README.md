# Selected D-Bus Provider Closure Pilot

## Status

Passed for the bounded `dbus_get_version()` probe.

```text
control capture: PASS
static traversal harness bug: fixed
control/static libcap mismatch: found and corrected
ownership-aware static discovery: PASS
static selected provider set == runtime mapped provider set: PASS
candidate byte materialization: PASS
candidate actual-selection proof: PASS
broad-farm/rootfs provider leakage: ZERO
protected world boundary: PASS
```

## Proven claim

For the bounded probe under the captured glibc 2.42 substrate:

```text
selected provider candidate:
    libdbus-1.so.3.38.3
    libsystemd.so.0.40.0
    libcap.so.2.75

protected substrate:
    ld-linux-aarch64.so.1
    libc.so.6
    libm.so.6
```

is sufficient to execute `dbus_get_version()` successfully without mapping provider objects from the broad farm or Debian rootfs.

## Candidate identity

First successful candidate ID:

```text
198a0ea278f09518a6b0ead7a228bb198a837e4096343228cfb32b1115286e6b
```

Validation evidence:

```text
$PREFIX/tmp/selected-dbus-candidate-validation-20260710-202400
```

## Strong validation result

The validator proved:

```text
candidate providers mapped from candidate bytes only
candidate receipt provider set == actual mapped candidate set
candidate file SHA-256 and Build IDs matched the receipt
protected prefix objects remained inside the world whitelist
no $HOME/gl/lib provider object was mapped
no Debian rootfs provider object was mapped
```

## Important correction discovered by the pilot

The first static classifier incorrectly assumed:

```text
exists under $PREFIX/glibc/lib
    => WORLD
```

Runtime maps disproved that rule for `libcap`:

```text
prefix candidate:
    libcap.so.2.69
    owner: libcap-glibc

actual broad-farm control selection:
    rootfs libcap.so.2.75
    owner: libcap2:arm64
```

The corrected model uses explicit protected package ownership plus observed control search order.

## Architecture interpretation

The pilot validates a real object class:

```text
materialized selected provider closure
```

with:

```text
bounded bytes
provenance receipt
candidate identity
actual-selection proof
protected-world exclusion
runtime independence from warehouse paths
```

It does not yet prove a global shared-provider boundary.

The next discriminating pilot should test real application-locality preservation and application-domain composition rather than repeating another synthetic low-level probe.

Current next target:

```text
Obsidian AppDir CPU-path selected-closure pilot
```

See:

```text
docs/refactor/0029-second-selected-closure-pilot-target.md
```

## Historical evidence policy

The broad farm remains unchanged as a control/reference mechanism.

Historical failed and partial runs remain evidence:

```text
first static run:
    incomplete due pipefail/SIGPIPE helper bug

first complete static run:
    exposed libcap control/static selection mismatch

ownership-aware rerun:
    static/runtime provider-set agreement

candidate run:
    isolated selected-provider success
```

The pilot is not rewritten to make the final successful model appear inevitable.
