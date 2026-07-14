# 8. Implementation Roadmap

This roadmap translates the target architecture into incremental engineering work. It is deliberately ordered to minimize conflict with an active refactor and to avoid replacing working behavior before equivalent validation exists.

The phases are not dates. Advancement is gate-based.

## Phase 0 — Snapshot and protect current semantics

### Goal

Establish a regression baseline before structural change.

### Deliverables

```text
validation/baseline/
    session-native
    glibc-x11
    glibc-vulkan
    glibc-zink
    vscode-basic
    vscode-gpu
    obsidian-basic
    conda-numpy
```

Each baseline should capture:

```text
exact invocation
required preconditions
expected exit/result
key stdout/stderr evidence
provider identity
artifact/build identity
```

### Exit criterion

The current live system can be tested without relying on memory or manual interpretation alone.

## Phase 1 — Semantic inventory

### Goal

Make current implicit policy visible without changing it.

### Work items

Create an inventory of:

```text
setup/glibc/env variables
session exports/unsets
app launcher flags
toolchain wrapper assumptions
farm denylist and directory order
Mesa build and promotion assumptions
shim responsibilities
rootfs path dependencies
```

Suggested record fields:

```text
mechanism
semantic purpose
current file
actual consumers
scope
source evidence
future owner
migration status
```

### Exit criterion

Every current environment variable and major launcher flag has an identified semantic owner candidate.

## Phase 2 — Human-readable contracts

### Goal

Establish object-model usage before creating a machine-readable schema.

### Initial world contracts

```text
contracts/worlds/bionic.md
contracts/worlds/glibc.md
```

### Initial capability contracts

```text
contracts/capabilities/display-x11.md
contracts/capabilities/fonts-fontconfig.md
contracts/capabilities/tls-ca-trust.md
contracts/capabilities/graphics-vulkan-glibc.md
contracts/capabilities/graphics-opengl-glibc.md
contracts/capabilities/integration-url-open.md
```

### Initial application contracts

```text
contracts/apps/vscode.md
contracts/apps/obsidian.md
contracts/apps/conda-base.md
contracts/apps/pymol-pilot.md
```

The exact repository path can differ if the ongoing refactor establishes a better location. Preserve the conceptual separation.

### Exit criterion

VS Code and Obsidian can be explained completely through world + capability + app-specific contracts.

## Phase 3 — Core validators

### Goal

Convert architecture invariants into executable checks.

### Validator 1: world purity

Input:

```text
PID or launcher command
```

Output:

```text
mapped ELF list
classification by ABI world
forbidden mappings
result
```

### Validator 2: loader contract

Check:

```text
interpreter
RPATH/RUNPATH
NEEDED
symbol-version summary
broken symlinks
```

### Validator 3: X11 bridge

Check:

```text
expected DISPLAY
client connection
intended client library world
basic operation
```

### Validator 4: Vulkan provider

Check:

```text
ICD metadata path
driver object loaded
device identity
no cross-world ICD mapping
```

### Validator 5: Zink/OpenGL

Check:

```text
gl-run behavior
renderer string/evidence
OpenGL version evidence
underlying Vulkan provider identity
```

### Exit criterion

A refactor of environment files can be evaluated by repeatable before/after gates.

## Phase 4 — Scope decomposition behind compatibility facades

### Goal

Split responsibility without breaking existing public entrypoints.

Keep stable initially:

```text
~/gl/env
~/gl/bin/gl-run
~/.local/bin/code
startxfce-x11
```

Refactor internal ownership conceptually into:

```text
world base
bridge client policy
font/data provider
TLS provider
Vulkan provider
Electron family
app-specific VS Code
```

### Exit criterion

Current entrypoints pass all baseline gates while policy ownership is no longer monolithic internally.

## Phase 5 — Provider manifests and promotion

### Goal

Generalize the successful Mesa versioned-prefix pattern.

Provider manifest minimum:

```text
provider id
world
version/build id
source commit/artifact
build options
provided capabilities
required capabilities
materialization path
validation gates
current promotion state
```

### Candidates

Start with Mesa because lifecycle discipline already exists.

Then consider:

```text
font/data provider
selected shared-library closure provider
Python runtime provider for PyMOL
```

### Exit criterion

At least two provider categories use a common promotion/rollback model.

## Phase 6 — Passive data capability materialization

### Goal

Make rootfs runtime data dependencies explicit and optionally independent.

Categories:

```text
fontconfig config
font files
locale data
XDG shared data/schemas actually used
```

Method:

```text
trace reads under controlled workloads
map files to source packages
materialize selected closure
validate behavior
compare with rootfs-backed provider
```

Do not copy all `/usr/share` by default.

### Exit criterion

At least fonts and locale have explicit provider contracts, whether the provider remains rootfs-backed or becomes project-materialized.

## Phase 7 — Resolved shared-library closure pilot

### Goal

Build an alternative to broad farm usage without removing the farm.

Pipeline:

```text
app/provider manifest
    -> static ELF closure
    -> allow/deny/core rules
    -> selected materialization
    -> provenance manifest
    -> runtime trace enrichment
    -> validation
```

Start with a bounded target.

Possible pilot criteria:

```text
few plugins
small process graph
clear feature test
stable upstream artifact
```

### Exit criterion

One real workload passes the same gates with a resolved closure and the result is reproducible from manifest/provenance data.

## Phase 8 — Application onboarding pilot: PyMOL

### Goal

Use PyMOL to test the new architecture, not to create another special case.

Before installation, define:

```text
selected world
Python runtime provider strategy
OpenGL capability provider
X11 bridge
font provider
native extension ABI expectations
source/licensing boundary
validation levels
```

Suggested validation levels:

```text
L0 package/runtime materialization
L1 Python import
L2 CLI/basic molecular load
L3 GUI startup
L4 OpenGL context and renderer validation
L5 interactive rendering workflow
L6 representative scientific workload
```

### Exit criterion

PyMOL onboarding reuses existing contracts and adds only genuinely new capabilities/providers.

## Phase 9 — Machine-readable manifests

### Goal

Encode patterns proven by multiple applications/providers.

Do this only after the Markdown contracts reveal stable fields.

Candidate serialization:

```text
TOML
YAML
JSON
```

Selection criteria:

```text
shell/tooling ergonomics
schema validation
human editability
comment support
minimal dependency burden
```

### Exit criterion

At least two applications and two providers can be represented without escape-hatch fields that simply embed arbitrary shell.

## Phase 10 — `gl-doctor`

### Goal

Diagnose contract violations before users manually interpret scattered failures.

Potential checks:

```text
world core present
loader config coherent
farm/resolved closure state
provider symlinks valid
ICD target exists
X11 bridge reachable
font provider healthy
CA provider readable
app manifest consistency
actual mapping contamination
```

Output should distinguish:

```text
ERROR: contract violated
WARNING: unvalidated configuration
INFO: optional capability unavailable
```

### Exit criterion

Common known failure signatures are detected with actionable, layer-specific reports.

## Phase 11 — `gl-adopt`

### Goal

Automate application onboarding only after the transformation contract is stable.

Potential pipeline:

```text
input adapter
    -> verify
    -> stage
    -> classify ELF
    -> interpreter transformation
    -> RUNPATH preservation/normalization
    -> shared dependency resolution
    -> app manifest generation
    -> static validation
    -> candidate materialization
```

App-specific exceptions should be declarative policy whenever possible, not hidden case statements.

### Exit criterion

A new compatible application can be onboarded with less manual state while producing better provenance than current ad hoc methods.

## Phase 12 — Release/distribution strategy

Only after stable local materialization, decide whether end-user distribution should use:

```text
versioned tar.zst bundles
installer + manifests
repository packages
hybrid shared runtime + app payloads
user-supplied proprietary payload adapters
```

The runtime architecture should determine packaging, not the reverse.

## Parallel work safety

During an active refactor elsewhere:

### Low-conflict tasks

```text
contract documentation
semantic inventory
read-only validators
baseline capture
manifest prototypes
```

### Coordinate before doing

```text
mass path moves
live symlink changes
renaming setup roots
changing deploy ownership
replacing launchers
farm semantics changes
```

## Milestone summary

```text
M0: behavior baseline captured
M1: current policy inventory complete
M2: world/capability/app contracts written
M3: core validators executable
M4: env responsibilities decomposed behind stable entrypoints
M5: provider promotion model generalized
M6: passive data providers explicit
M7: resolved closure pilot works
M8: PyMOL onboarded through contracts
M9: stable manifest schema
M10: doctor/adopter automation
```

## Principle of completion

A phase is complete when its contract and validation exist, not merely when a new directory or script has been created.
