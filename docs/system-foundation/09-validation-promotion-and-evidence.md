# 9. Validation, Promotion, Rollback, and Evidence

> **Lifecycle:** historical system-foundation provenance. Current constitutional authority is [`../constitution/`](../constitution/README.md); current architecture is [`../architecture/`](../architecture/README.md). Interpret this document in its recorded context; any later status, precedence, or execution-order wording below is historical to that context.

A system assembled from several ABI worlds, upstream artifacts, locally built providers, and runtime bridges needs stronger lifecycle discipline than “the command exited zero once.”

This document defines a validation and promotion model.

## 9.1 Claim-oriented validation

Every gate should support a specific claim.

Weak gate definition:

```text
run test.sh
```

Strong gate definition:

```text
claim:
The glibc Vulkan provider selects the intended Turnip ICD and enumerates the Adreno device without mapping bionic driver libraries.

procedure:
run controlled Vulkan probe under world.glibc policy

collect:
ICD path, driver mapping, device identity, exit status

pass:
expected provider/device identity and no forbidden mappings
```

## 9.2 Validation levels

### Static validation

No process execution required.

Examples:

```text
file type and architecture
ELF interpreter
NEEDED graph
RUNPATH/RPATH
symbol-version requirements
broken symlinks
manifest schema/provenance
```

### Startup validation

```text
process starts
loader completes
basic initialization reaches checkpoint
```

### Bridge validation

```text
X11 connection
URL intent handoff
proxy endpoint reachability
```

### Capability validation

```text
Vulkan device enumeration
OpenGL renderer path
font discovery/rendering
TLS trust verification
```

### Application workflow validation

```text
open project
edit/save file
run extension/native workload
load molecular structure
rotate/render scene
```

A higher level should not erase lower-level evidence. Keep results compositional.

## 9.3 Suggested gate namespace

```text
world/
    bionic-purity
    glibc-purity

loader/
    interpreter
    search-policy
    symbol-versions

bridge/
    x11
    url-open
    network

capability/
    fonts
    tls
    vulkan-bionic
    vulkan-glibc
    opengl-zink-glibc

app/
    vscode-basic
    vscode-gpu
    obsidian-basic
    conda-numpy
    pymol-import
    pymol-gui
    pymol-render
```

The physical path can differ. The taxonomy is useful.

## 9.4 Evidence bundle format

A gate run should create a directory such as:

```text
run-<timestamp-or-id>/
├── metadata.json or metadata.txt
├── command.txt
├── environment.diff
├── stdout.log
├── stderr.log
├── result.txt
├── artifacts/
│   ├── maps.txt
│   ├── needed.txt
│   ├── version-info.txt
│   └── renderer.txt
└── checksums.txt
```

Not every gate needs every file. The model ensures evidence is inspectable later.

## 9.5 Environment capture

Full environments can contain secrets. Evidence capture should therefore be selective.

Prefer:

```text
known runtime variables
world/provider selection variables
PATH fragments relevant to test
explicit unset/set differences
```

Avoid blindly publishing:

```text
tokens
credentials
private proxy secrets
unrelated personal variables
```

A sanitized environment diff is better than an uncontrolled `env` dump.

## 9.6 World-purity gate design

### Input

```text
launcher + test duration/action
```

### Procedure

```text
launch process
identify relevant PID tree
capture maps
classify ELF file origins and ABI worlds
check forbidden families
```

### Evidence

```text
PID tree
mapped object list
classification
violations
```

### Pass condition

No mapped low-level runtime object from a forbidden ABI world.

The classifier should be conservative. Unknown objects should be reported as unknown rather than guessed safe.

## 9.7 Provider identity gate

Configuration does not prove selection.

For Vulkan, evidence should distinguish:

```text
configured ICD metadata
actual driver object mapped
reported physical device/driver identity
```

For OpenGL/Zink:

```text
OpenGL renderer/version
Vulkan provider identity
actual mapped driver libraries
```

This prevents false confidence from environment variables alone.

## 9.8 Bridge gate

An X11 bridge gate should verify:

```text
server alive
expected DISPLAY contract
client can connect
client belongs to expected world
basic request succeeds
```

A URL bridge gate should verify:

```text
shim selected
host integration invoked
Android permission prerequisite documented
```

Each bridge has different evidence.

## 9.9 Application gate design

Application gates should be layered.

VS Code example:

```text
vscode-basic
    -> process tree stable
    -> window opens
    -> workspace opens

vscode-gpu
    -> GPU process stable
    -> expected renderer/provider evidence
    -> representative interaction

vscode-remote
    -> authentication path
    -> persistent transport path
    -> project workflow
```

Do not let success at one level imply success at all others.

## 9.10 Promotion states

A provider/application candidate can have explicit states:

```text
raw
staged
transformed
candidate
validated
promoted
deprecated
retired
```

State transitions should be evidence-backed.

Example:

```text
candidate Mesa prefix
    -> capability.vulkan gate PASS
    -> capability.opengl-zink gate PASS
    -> app regression gates PASS
    -> promoted symlink updated
```

## 9.11 Promotion record

Record:

```text
component/provider id
previous target
new target
source/build identity
validation run IDs
reason
project commit
rollback instruction
```

This turns a symlink update into an auditable system event.

## 9.12 Rollback

Rollback should be tested, not merely assumed.

For versioned providers:

```text
promote candidate B
    -> post-promotion failure
    -> point stable reference back to A
    -> rerun smoke gate
```

Keep at least the previous validated provider until the new version has survived an appropriate confidence period.

## 9.13 A/B experiment structure

A strong comparison holds most variables constant.

```text
A: provider version/config X
B: provider version/config Y
same app
same launcher contract except provider selection
same workload
same evidence collection
```

This is especially important for GPU investigations where version and build configuration can both change behavior.

## 9.14 Evidence strength vocabulary

Suggested terms:

### Observed

Directly seen in logs/output/trace.

### Correlated

Two conditions repeatedly vary together, but mechanism not proven.

### Validated workaround

A practical configuration reliably restores required behavior under defined scope.

### Mechanism supported

Trace/source/debug evidence directly supports causal explanation.

### Open hypothesis

Plausible explanation requiring further evidence.

This vocabulary helps prevent a successful workaround from becoming an overconfident mechanism claim.

## 9.15 Negative results

A failed experiment is valuable when it establishes a boundary.

Record:

```text
question
baseline
change
result
failure point
what the result rules out
what remains possible
```

Do not preserve every transient typo as architecture evidence. Preserve failures that meaningfully narrow the system model.

## 9.16 Validation before and after refactor

For each responsibility-moving refactor:

```text
run baseline gates on old implementation
    -> capture evidence
change structure without intended behavior change
run same gates
compare
```

If results differ, the change is behavioral even if shell code appears equivalent.

## 9.17 CI versus device validation

Not all gates can run in generic GitHub Actions.

Classify:

```text
host-independent static gates
    -> CI candidate

Termux filesystem/ELF gates
    -> device or Android runner

GPU/X11 interaction gates
    -> physical target device
```

A future automation system may combine CI static checks with device-side validation reports.

## 9.18 Minimum validation before PyMOL promotion

Suggested:

```text
world purity
Python runtime identity
native extension load closure
X11 bridge
font provider
OpenGL/Zink renderer
interactive molecule load/render smoke
representative scientific action
```

The pilot can discover additional requirements, but these establish a structured baseline.

## 9.19 Evidence is part of architecture

The project’s unusual value is not only that the runtime works. It records why a configuration exists and what evidence supports it.

Therefore the final architecture includes:

```text
runtime system
    +
knowledge/control system
```

A runtime change without evidence linkage is incomplete.
