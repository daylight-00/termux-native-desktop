# 3. System Model v2: Six Architectural Planes

> **Lifecycle:** historical system-foundation provenance. Current constitutional authority is [`../constitution/`](../constitution/README.md); current architecture is [`../architecture/`](../architecture/README.md). Interpret this document in its recorded context; any later status, precedence, or execution-order wording below is historical to that context.

The existing project history is naturally organized into workstreams: desktop/session, glibc applications, and GPU. Those workstreams remain useful as historical and operational categories. For long-term architecture, however, they mix different kinds of concern.

For example:

```text
session
    -> lifecycle and host execution concern

glibc world
    -> ABI/runtime-domain concern

GPU
    -> capability-provider concern
```

A target architecture should separate these dimensions.

This document proposes six planes.

## 3.1 Overview

```text
┌─────────────────────────────────────────────────────────┐
│ 6. Knowledge and Control Plane                          │
│ experiments, evidence, contracts, validation, promotion │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 5. Build and Supply Plane                               │
│ upstream artifacts, Debian oracle, source builds        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 4. Application Runtime Domains                         │
│ VS Code, Obsidian, Conda/PyMOL, future workloads        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 3. Capability Provider Plane                           │
│ X11, Vulkan, OpenGL/Zink, fonts, locale, TLS, bridges   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 2. Bridge Plane                                         │
│ X11 protocol, sockets, pipes, URL intents, filesystem   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 1. Native Host Plane                                    │
│ Android kernel, Termux bionic, session, host tools       │
└─────────────────────────────────────────────────────────┘
```

The planes are conceptual responsibilities. They do not require one directory per plane or one process per plane.

## 3.2 Plane 1: Native Host Plane

### Responsibility

Provide the authoritative machine and workstation substrate.

Includes:

```text
Android kernel and hardware
Termux application sandbox/private filesystem
bionic-native shell and host tools
Termux:X11 integration
XFCE/current desktop session
native Chromium/Code OSS and other native apps
native build orchestration tools
```

### Contract

The host plane exposes:

```text
process execution
filesystem and storage
networking
X11 display endpoint
Android integration mechanisms
GPU device interfaces through kernel
native toolchain/orchestration
```

### Boundary

Foreign runtime policy must not silently mutate host-wide loader/provider behavior.

Example invariant:

```text
No global glibc LD_LIBRARY_PATH in the bionic shell/session.
```

## 3.3 Plane 2: Bridge Plane

### Responsibility

Connect otherwise separate runtime domains through explicit interfaces.

Examples:

```text
X11 protocol over local Unix socket
TCP/Unix sockets
pipes
filesystem artifacts
network protocols
URL-opening shim to Android integration
optional file-descriptor passing protocols
```

### Contract shape

Each bridge should define:

```text
name
producer/initiator
consumer/server
transport
address discovery
security/permission assumptions
lifecycle owner
health check
failure semantics
```

Example: X11 bridge

```text
name: x11-display
client worlds: bionic, glibc
server owner: native host session
transport: local X11 Unix socket
address: DISPLAY=:1 plus Termux-aware client behavior
health check: X client connects and performs known operation
```

## 3.4 Plane 3: Capability Provider Plane

### Responsibility

Provide named workstation capabilities independently of applications.

Possible capability taxonomy:

```text
display.x11
graphics.vulkan
graphics.opengl
fonts.fontconfig
locale.posix
tls.ca-trust
integration.url-open
network.proxy
python.runtime
```

A provider is one implementation of a capability for a particular world/context.

Examples:

```text
graphics.vulkan/glibc
    -> glibc Mesa Turnip ICD

graphics.opengl/glibc
    -> Zink + Vulkan provider

display.x11/glibc
    -> Termux-aware glibc X11/xcb client libraries

tls.ca-trust/glibc
    -> Termux CA bundle exposed through explicit policy
```

### Why this plane matters

Without capability modeling, application launchers accumulate provider-selection logic and every app becomes a snowflake.

With capability modeling:

```text
Application requires graphics.opengl
    -> provider mapping can evolve independently
```

## 3.5 Plane 4: Application Runtime Domains

### Responsibility

Materialize coherent per-application execution contracts.

Examples:

```text
VS Code domain
Obsidian domain
Conda base domain
PyMOL domain
```

A domain definition includes:

```text
identity and version
ABI world
entry point
source provenance
app-local libraries/resources
required capabilities
application-family policy
app-specific policy
mutable state locations
validation gates
```

A runtime domain is not necessarily fully self-contained. It may consume shared providers, but those dependencies are explicit.

## 3.6 Plane 5: Build and Supply Plane

### Responsibility

Acquire and produce candidate artifacts without defining runtime authority.

Inputs:

```text
upstream tarballs
.deb packages
AppImages
Conda packages
wheels
source repositories
Termux packages
```

Tools/environments:

```text
Debian PRoot oracle/warehouse
Termux host build tools
project glibc toolchain wrappers
Meson/Ninja/CMake
package metadata tools
```

Outputs:

```text
verified raw artifact
staged extraction
locally built provider candidate
dependency/provenance data
```

The plane ends before promotion to live runtime.

## 3.7 Plane 6: Knowledge and Control Plane

### Responsibility

Convert uncertain experiments into durable, validated system state.

Includes:

```text
questions and hypotheses
experiments
raw evidence
canonical experiment summaries
working conclusions
architecture decisions
contracts
validators
promotion records
rollback records
```

This plane is what prevents a research-heavy project from becoming an untraceable collection of hacks.

## 3.8 Control flow versus data flow

The planes interact in two different directions.

### Artifact/data flow

```text
Supply
    -> candidate artifact
    -> runtime materialization
    -> application domain
    -> capability/bridge use
    -> host kernel/hardware
```

### Knowledge/control flow

```text
observation
    -> experiment evidence
    -> conclusion
    -> contract change
    -> validator
    -> promotion policy
```

Confusing these flows creates structural debt. For example, copying a library directly from the warehouse into a live runtime bypasses the control flow that should explain and validate the decision.

## 3.9 Runtime execution example: VS Code

```text
Application Runtime Domain
    VS Code
        |
        +-- requires display.x11
        +-- requires graphics.angle-vulkan
        +-- requires fonts.fontconfig
        +-- requires tls.ca-trust
        +-- requires integration.url-open
        |
        v
Capability Providers
    X11 client provider
    glibc Vulkan/Turnip provider
    font provider
    CA provider
    URL shim
        |
        v
Bridges
    X11 Unix socket
    network sockets
    Android intent bridge
        |
        v
Native Host
    Termux:X11 / Android / kernel / Adreno
```

Supply history is separate:

```text
upstream VS Code tarball
    -> verify/extract
    -> inspect/transform
    -> materialize runtime domain
```

## 3.10 Future PyMOL example

A PyMOL domain might require:

```text
python.runtime
display.x11
graphics.opengl
fonts.fontconfig
tls.ca-trust (if network features need it)
```

Provider choices could be:

```text
python.runtime
    -> Conda prefix or project-built Python strategy

graphics.opengl
    -> Zink -> Vulkan -> Turnip
```

The application contract remains stable even if the Python provider implementation changes later.

## 3.11 Why PRoot belongs to supply plane

The project uses PRoot for:

```text
apt/dpkg solving
known-good Debian behavior
library/package discovery
control comparisons
```

The normal application process should not depend on PRoot execution mediation.

A separate open question is whether passive runtime reads from the rootfs remain an accepted provider mechanism or are eventually materialized into project-owned runtime data closures.

## 3.12 Why GPU belongs to capability plane

GPU acceleration is not one universal runtime world.

Different consumers use different paths:

```text
bionic Chromium
    -> ANGLE Vulkan -> bionic Turnip

glibc VS Code
    -> ANGLE Vulkan -> glibc Turnip

glibc OpenGL app
    -> Zink -> Vulkan -> glibc Turnip
```

The common concept is capability provision with ABI-appropriate implementations.

## 3.13 Why this model scales better

Adding a new application becomes:

```text
1. classify world;
2. declare capabilities;
3. select existing providers where valid;
4. add only genuinely new bridges/providers;
5. validate application-specific behavior.
```

Instead of:

```text
copy previous launcher
add missing env vars
copy more libraries
patch until window opens
```

The second approach is faster for one experiment but scales poorly.

## 3.14 Directory structure does not need to mirror planes exactly

Avoid premature directory-driven architecture.

The model should first produce stable ownership rules. A later repository structure may use directories such as:

```text
contracts/
providers/
apps/
validation/
```

or may keep existing `setup/` and `scripts/` while adding manifests.

The test is not aesthetic symmetry. The test is whether each artifact has one clear responsibility and ownership path.

## Project references

- [`../architecture.md`](../architecture.md)
- [`../desktop-session.md`](../desktop-session.md)
- [`../glibc-layer.md`](../glibc-layer.md)
- [`../gpu.md`](../gpu.md)
