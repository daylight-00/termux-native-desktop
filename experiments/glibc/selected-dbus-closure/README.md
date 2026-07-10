# Selected D-Bus Provider Closure Pilot

## Status

Active architecture-discrimination experiment.

Current stage:

```text
control capture: PASS
first static discovery run: INCOMPLETE due harness early-exit bug
corrected static discovery rerun: pending after checkout relocation
```

## Dates

Started after the glibc/libdbus ABI incident was recovered and VS Code passed real GUI workload validation.

## Provenance

First-hand experiment design and first-hand device evidence derived from:

```text
docs/refactor/0019-selected-closure-pilot-decision-criteria.md
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

Control state:

```text
active substrate:
    APT/dpkg-owned glibc 2.42 recovery substrate

active provider mechanism:
    broad farm under $HOME/gl/lib

root provider under study:
    libdbus-1.so.3

known control behavior:
    active libdbus relocation PASS
    VS Code CLI PASS
    VS Code GUI workload PASS
```

## Pilot scope

The pilot begins with two deliberately small phases.

### Phase A — control capture

Capture:

```text
selected root provider identity
transitive control resolution
loader trace
/proc/<pid>/maps
probe output and status
```

### Phase B — control-guided static closure discovery

Starting from `libdbus-1.so.3`:

```text
read DT_NEEDED
classify an edge as WORLD_PREFIX when satisfied by $PREFIX/glibc/lib
otherwise resolve through the active broad-farm control
require the broad-farm target to resolve into the Debian rootfs
record package owner/version, SHA-256, and Build ID
recurse over rootfs provider objects
```

This is intentionally **not** a universal resolver. It is a bounded discovery harness that converts current control behavior into explicit evidence before candidate materialization is attempted.

## Minimal probe

The pilot probe calls only:

```text
dbus_get_version()
```

and then remains alive for a bounded interval so `/proc/<pid>/maps` can be captured.

This avoids requiring a running D-Bus daemon while still executing code from the selected `libdbus` provider and its transitive runtime closure.

## First control result

Probe identity:

```text
ELF:
    AArch64 PIE
    interpreter $PREFIX/glibc/lib/ld-linux-aarch64.so.1

Build ID:
    0a310fa7489d5754b03ab936da9462869bb05198

SHA-256:
    d55c783cd68c97b9d5976935cfcb26538cbded69dc119179a2050b318809a9a4
```

Probe dynamic requirements:

```text
libdbus-1.so.3
libc.so.6
ld-linux-aarch64.so.1
```

Runtime result:

```text
libdbus runtime version: 1.16.2
control capture: PASS
```

Actual mapped objects relevant to the pilot were:

```text
WORLD / substrate:
    $PREFIX/glibc/lib/ld-linux-aarch64.so.1
    $PREFIX/glibc/lib/libc.so.6
    $PREFIX/glibc/lib/libm.so.6

ROOTFS providers:
    libdbus-1.so.3.38.3
    libsystemd.so.0.40.0
    libcap.so.2.75
```

This first runtime result is already a useful boundedness signal: the direct probe mapped three rootfs provider objects and three substrate objects in the observed relevant set.

It is not yet the final selected closure because static graph traversal must be completed and static/runtime differences must be reconciled.

## First static discovery run

The first static run produced only a partial graph:

```text
libdbus-1.so.3.38.3
    -> libsystemd.so.0   PROVIDER_ROOTFS
    -> libc.so.6         WORLD_PREFIX
```

and recorded provider identities for:

```text
libdbus-1-3:arm64  1.16.2-2
libsystemd0:arm64  257.13-1~deb13u1
```

The run did not print its terminal PASS/FAIL summary and `world-prefix.tsv` contained only its header.

This was not interpreted as a real static/runtime closure mismatch. Inspection of the harness showed another `pipefail` plus early-exit consumer pattern in Build-ID extraction:

```text
readelf -n object
    |
awk '... { print; exit }'
```

For sufficiently long producer output, the consumer exits after the Build ID and the producer may receive SIGPIPE. Under `set -o pipefail`, the helper can fail while recording the first world-prefix object, terminating traversal early.

The helper was corrected to consume the complete `readelf` stream before printing the captured Build ID.

Therefore:

```text
first control capture:
    valid evidence

first static closure result:
    partial evidence only
    not an architectural conclusion

next static run:
    required with corrected harness
```

## Current hypothesis

The selected provider closure will be substantially smaller and more explainable than the broad farm.

The current observed runtime shape is:

```text
probe
    -> libdbus-1.so.3             PROVIDER_ROOTFS
        -> libsystemd.so.0        PROVIDER_ROOTFS
            -> libcap.so.2        PROVIDER_ROOTFS or transitive provider edge
        -> substrate objects      WORLD
```

The exact static edge structure must come from the corrected rerun rather than from this expectation.

## Procedure

```text
1. build the minimal probe
2. capture broad-farm control behavior
3. discover the bounded static provider closure
4. compare static graph with actual mapped objects
5. inspect graph.tsv and providers.tsv
6. only then design candidate byte materialization
```

Commands:

```bash
bash experiments/glibc/selected-dbus-closure/recipe/build-probe.sh

bash experiments/glibc/selected-dbus-closure/recipe/capture-control.sh

bash experiments/glibc/selected-dbus-closure/recipe/discover-static-closure.sh
```

Each script writes evidence under a caller-selected or timestamped directory beneath `$PREFIX/tmp`.

## Evidence contract

### `graph.tsv`

Columns:

```text
consumer
needed
classification
selected_path
selection_reason
```

### `providers.tsv`

Columns:

```text
path
package
version
sha256
build_id
```

### control capture

Expected artifacts include:

```text
probe.stdout
loader-debug.log
maps.txt
control-ldd.txt
root-provider-identity.txt
substrate-identity.txt
```

## Decision boundary after this stage

Do not yet implement:

```text
provider store
candidate activation
universal resolver
global gl sync
farm replacement
```

First inspect whether the discovered provider set is actually bounded and semantically coherent.

If it is bounded, the next experiment stage will materialize concrete provider bytes into an isolated candidate directory and run the same probe under an explicit candidate-only loader path while proving actual mapped identities.

If it expands toward a broad rootfs pool, the experiment must record that result rather than force the selected-closure model.
