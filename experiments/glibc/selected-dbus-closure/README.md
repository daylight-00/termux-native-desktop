# Selected D-Bus Provider Closure Pilot

## Status

Active architecture-discrimination experiment.

Current stage:

```text
control capture: PASS
static traversal harness bug: fixed
control/static libcap mismatch: found and modeled
ownership-aware static discovery: PASS
static selected provider set == runtime mapped provider set: PASS
candidate byte materialization and isolated validation: ready to run
```

## Question

Can the broad Debian-rootfs library farm be replaced, for one bounded workload class, by a smaller selected provider closure with explicit identity, concrete bytes, provenance, world-owned exclusion, and provable actual selection?

## Current evidence

### Runtime control provider set

```text
libdbus-1.so.3.38.3
libsystemd.so.0.40.0
libcap.so.2.75
```

### Ownership-aware static provider set

```text
libdbus-1.so.3.38.3
libsystemd.so.0.40.0
libcap.so.2.75
```

Therefore, for the bounded `dbus_get_version()` probe:

```text
STATIC_SELECTED_PROVIDER_SET
    ==
RUNTIME_MAPPED_PROVIDER_SET
```

### Protected substrate set

Objects selected from package owner `glibc`:

```text
ld-linux-aarch64.so.1
libc.so.6
libm.so.6
```

The prefix `libcap.so.2.69` is owned by `libcap-glibc`, not `glibc`, and is not classified as protected world substrate merely because it lives under `$PREFIX/glibc/lib`.

## Current graph

```text
probe
    -> libdbus                  candidate provider root
        -> libsystemd           selected provider
            -> libcap           selected provider
            -> libm             protected world substrate
            -> libc             protected world substrate
            -> loader           protected world substrate
        -> libc                 protected world substrate
        -> loader               protected world substrate

libcap
    -> libc                     protected world substrate
    -> loader                   protected world substrate
```

## Candidate stage

### Materialization

`materialize-candidate.sh`:

```text
reads successful static evidence
verifies source SHA-256 and Build ID before copy
copies concrete provider bytes into candidate/lib
creates only candidate-internal SONAME links
records source and candidate identity in receipt.tsv
snapshots graph and world-substrate evidence
computes a candidate ID
```

The candidate does not symlink back into the mutable Debian rootfs.

### Validation

`validate-candidate.sh` runs the same minimal probe with:

```text
candidate/lib:$PREFIX/glibc/lib
```

and proves:

```text
all receipt providers were actually mapped from candidate bytes
mapped candidate set equals receipt provider set
candidate hashes and Build IDs still match the receipt
no $HOME/gl/lib provider object was mapped
no Debian rootfs provider object was mapped
mapped prefix objects stay inside the protected world whitelist
```

## Procedure

Given the successful ownership-aware static evidence directory:

```bash
STATIC_OUT=/path/to/selected-dbus-static-ownership-...
CANDIDATE=/path/to/candidate

STATIC_OUT="$STATIC_OUT" \
CANDIDATE="$CANDIDATE" \
bash recipe/materialize-candidate.sh

CANDIDATE="$CANDIDATE" \
bash recipe/validate-candidate.sh
```

## Decision boundary

A candidate validation PASS proves only the bounded pilot claim.

It does not yet justify:

```text
global provider store
activation pointer
gl-sync
one global fingerprint
broad-farm replacement
application-wide migration
```

After a PASS, the next task is to interpret what semantic owner this closure belongs to and whether the same mechanism survives a second, more discriminating workload/application-family pilot.
