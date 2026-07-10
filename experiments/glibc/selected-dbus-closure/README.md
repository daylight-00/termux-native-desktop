# Selected D-Bus Provider Closure Pilot

## Status

Active architecture-discrimination experiment.

## Dates

Started after the glibc/libdbus ABI incident was recovered and VS Code passed real GUI workload validation.

## Provenance

First-hand experiment design derived from:

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

## Current hypothesis

The selected provider closure will be substantially smaller and more explainable than the broad farm.

The expected first-order shape is:

```text
probe
    -> libdbus-1.so.3             PROVIDER_ROOTFS
        -> libsystemd.so.0        PROVIDER_ROOTFS
        -> low-level dependencies classified per observed path

world-owned / prefix-owned objects
    remain outside candidate materialization
```

The actual closure must be derived from evidence, not from this expectation.

## Procedure

```text
1. build the minimal probe
2. capture broad-farm control behavior
3. discover the bounded static provider closure
4. inspect graph.tsv and providers.tsv
5. only then design candidate byte materialization
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
probe.stderr
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
