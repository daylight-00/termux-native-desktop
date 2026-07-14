# 1. The Essence of the Project

## 1.1 Start from the need, but do not confuse the need with the architecture

The project began from a practical need: a phone had to become a credible workstation for coding, remote development, scientific visualization, data inspection, Git review, and writing.

The first visible desires were concrete:

```text
run a desktop
run VS Code
use GPU acceleration
run PyMOL
avoid PRoot sluggishness
```

Those are valid product-level goals, but they are not the deepest system definition.

A project defined as “make VS Code run” tends to accumulate app-specific workarounds. A project defined as “make Debian run” tends to reproduce a distribution runtime even when that is not the desired execution model. A project defined as “build Mesa” tends to optimize a provider rather than the workstation system.

The architecture must describe what remains true when VS Code, Mesa version, desktop environment, or package source changes.

## 1.2 Proposed abstract identity

The project is:

> **A heterogeneous userspace composition system for a non-root Android workstation.**

Expanded:

> Keep the Android/Termux host native; construct coherent foreign userspace application domains beside it; connect domains through explicit kernel or protocol boundaries rather than accidental library mixing; expose display, GPU, networking, fonts, TLS, and other workstation capabilities through intentional providers; and preserve an evidence chain from experiment to promoted runtime contract.

This definition explains the project more accurately than any individual implementation technique.

## 1.3 What the project composes

The system composes four kinds of thing:

### Execution worlds

```text
bionic-native world
glibc foreign-application world
```

### Capability providers

```text
X11 display
Vulkan/Turnip
OpenGL through Zink
ANGLE Vulkan
fonts/fontconfig
locale data
TLS trust
URL/Android integration
network/proxy transport
```

### Application runtime domains

```text
VS Code
Obsidian
Conda environments
future PyMOL
future desktop/scientific workloads
```

### Knowledge and lifecycle mechanisms

```text
experiments
evidence
decisions
contracts
validation gates
promotion/rollback
```

The project is successful when these are composed coherently, not merely when many files are present.

## 1.4 The authoritative host

The native Android/Termux world is the host authority.

```text
Android kernel and security model
    -> Termux app sandbox/private storage
    -> bionic-native tools and session
    -> Termux:X11 bridge to Android display surface
```

Foreign runtimes are guests beside the host, not replacements for it.

This leads to a fundamental asymmetry:

```text
host policy may expose bridges and capabilities to guest domains
foreign runtime policy must not globally contaminate the host
```

For example, global glibc library search paths must not leak into bionic processes.

## 1.5 One kernel does not mean one userspace

The shared kernel provides:

```text
processes and threads
virtual memory
filesystem interfaces
networking
sockets and IPC primitives
device interfaces
scheduler
security enforcement
```

But userspace runtime contracts remain distinct.

```text
bionic process
    -> Android linker + bionic runtime + bionic libraries

glibc process
    -> glibc loader + coherent glibc runtime + glibc libraries
```

The architecture should exploit the shared kernel for explicit bridges while preserving userspace coherence.

## 1.6 The project is not a conventional Linux distribution port

The goal is not:

```text
turn Termux into Debian
```

or:

```text
boot a second Linux kernel
```

or:

```text
make PRoot the normal desktop runtime
```

Instead:

```text
native host remains authoritative
    +
foreign application domains are materialized only where useful
    +
services/capabilities cross via explicit contracts
```

This avoids paying for a full distribution runtime as the default path when only selected foreign applications require it.

## 1.7 The project is not primarily a package manager

Package-management capability may become useful later, but the present system question is different.

A package manager answers:

```text
Which package versions should be installed?
Which files does each package own?
How are upgrades/removals transacted?
```

The project must first answer:

```text
Which runtime worlds exist?
Which providers are coherent in each world?
How are applications admitted?
Which bridges cross boundaries?
How are capabilities validated?
```

Automating the wrong runtime model would only make architectural mistakes repeat faster.

## 1.8 The project is not an installer framework yet

The repository currently serves as both research workbench and live-system source of truth. Its priority is understanding and reproducibility.

A generalized installer should come after stable contracts exist.

Sequence:

```text
discover behavior
    -> identify invariant
    -> define contract
    -> validate repeatedly
    -> automate
```

not:

```text
one successful command sequence
    -> immediately generalize installer
```

## 1.9 PRoot’s essential role

PRoot is not rejected absolutely. Its role is demoted and made explicit.

Useful roles:

```text
package dependency solver
artifact warehouse
behavioral oracle
control environment
reproduction aid
```

Rejected role:

```text
normal application execution path
```

A further distinction must remain explicit: a process can run outside PRoot while still reading passive files located inside a Debian rootfs. “No PRoot runtime” must specify whether it means no PRoot execution mediation, no rootfs process semantics, or complete filesystem decoupling.

## 1.10 Main quality attributes

The architecture optimizes for:

### Performance

Avoid unnecessary mediation in the normal workstation path.

### Coherence

Each process maps a compatible runtime universe.

### Explicitness

Provider selection and bridge boundaries are intentional.

### Reproducibility

Transformations and runtime materialization can be reconstructed from known inputs.

### Inspectability

A developer can determine why a file/provider/flag exists.

### Rollback

Experimental provider versions and promoted versions can coexist and switch cheaply.

### Evidence quality

Claims are no stronger than observations and instrumentation justify.

## 1.11 Non-goals

The architecture should explicitly reject several goals unless the project later changes scope.

### Not a general Android Linux distribution

It need not reproduce every Debian service or filesystem assumption.

### Not universal binary compatibility

The project supports selected coherent runtime contracts, not arbitrary Linux binaries by magic.

### Not a promise to eliminate every external artifact source

Using Debian, Conda, upstream tarballs, or local source builds is acceptable if the supply/runtime boundary is explicit.

### Not a reason to force all apps through one graphics path

OpenGL/Zink, Vulkan-native, and ANGLE Vulkan consumers can legitimately use different capability compositions.

### Not a claim that every workaround is architectural truth

`--disable-gpu-vsync` and a particular Mesa KMD build option are implementation decisions with evidence scopes, not eternal project principles.

## 1.12 The fundamental output of the project

The project’s durable output is not merely a collection of working binaries.

It is a body of:

```text
runtime-domain definitions
capability provider contracts
bridge contracts
application admission contracts
validation gates
provenance records
operational artifacts
```

A working application is evidence that a composition is viable. The reusable product is the composition knowledge and its reproducible implementation.

## 1.13 The top-down derivation

From the essence, the rest follows:

```text
Mission
    -> build a practical native-first Android workstation

Constraint
    -> non-root Android and Termux host remain authoritative

Problem
    -> desired applications span incompatible userspace assumptions

Architectural response
    -> compose multiple coherent runtime domains

Safety rule
    -> explicit bridges, no accidental cross-ABI loading

Scalability response
    -> capabilities/providers and per-application contracts

Operational response
    -> validation gates, promotion, rollback, provenance
```

The following documents make each of these statements concrete.

## Project references

- [`../PROJECT_CONTEXT.md`](../PROJECT_CONTEXT.md)
- [`../architecture.md`](../architecture.md)
- [`../glibc-layer.md`](../glibc-layer.md)
- [`../../STATUS.md`](../../STATUS.md)
