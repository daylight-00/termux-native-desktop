# 2. Principles and Invariants

> **Lifecycle:** historical system-foundation provenance. Current constitutional authority is [`../constitution/`](../constitution/README.md); current architecture is [`../architecture/`](../architecture/README.md). Interpret this document in its recorded context; any later status, precedence, or execution-order wording below is historical to that context.

This document proposes a project constitution: rules that should remain stable even while implementations change.

A useful distinction:

```text
principle
    -> preferred direction and reasoning style

invariant
    -> condition that a valid architecture/runtime must preserve

implementation decision
    -> current mechanism satisfying a contract
```

For example:

```text
Invariant:
A process must stay in one coherent ABI world.

Current implementation decision:
glibc applications source ~/gl/env and use controlled glibc loader policy.
```

The implementation can change; the invariant should not change casually.

## 2.1 Principle: native host authority

**The Android/Termux bionic host is authoritative. Foreign userspaces are application domains, not host replacements.**

Consequences:

- host shell and session remain bionic-native;
- foreign loader variables are not exported globally;
- Android integration is reached through explicit bridges;
- foreign application requirements do not silently redefine the entire host environment.

## 2.2 Invariant: process ABI purity

**Every process must remain inside one coherent userspace ABI world.**

Allowed:

```text
bionic process -> bionic libraries

glibc process -> coherent glibc runtime and compatible libraries
```

Forbidden by default:

```text
one process
├── bionic libc/runtime object graph
└── glibc libc/runtime object graph
```

This invariant is stronger than “do not set `LD_LIBRARY_PATH`.” The environment-variable rule is only one implementation mechanism.

Validation implication:

```text
inspect actual /proc/<pid>/maps
classify mapped ELF objects by world
fail promotion on cross-world contamination
```

## 2.3 Invariant: explicit cross-world bridges

**Cross-world cooperation must occur through explicit, inspectable boundaries.**

Preferred bridge types:

```text
Unix/TCP socket protocols
pipes
byte streams
file descriptors with documented ownership
filesystem artifacts
X11 protocol
network protocols
host integration shims
```

High-risk implicit boundaries:

```text
foreign libc objects
allocator-owned pointers
FILE *
pthread objects
C++ STL objects
exceptions across incompatible runtimes
```

A bridge contract must document:

```text
producer
consumer
transport
address discovery
lifecycle
security assumptions
failure behavior
```

## 2.4 Principle: supply is not runtime

**The source of an artifact does not define the final runtime architecture.**

Examples:

```text
.deb
    -> upstream payload/source of metadata
    -> not necessarily final Debian runtime

AppImage
    -> extractable application input
    -> not necessarily AppImage execution mechanism

Debian rootfs
    -> package oracle/warehouse/passive data source
    -> not normal application execution path
```

This principle allows heterogeneous acquisition while preserving one runtime model.

## 2.5 Invariant: deterministic provider selection

**A required capability must resolve to an intended provider, not whichever compatible-looking artifact is discovered accidentally.**

Examples:

```text
Vulkan ICD -> explicit glibc or bionic provider
X11 client stack -> correct ABI/world-specific implementation
libc family -> designated coherent core
app-local libraries -> preserved where upstream requires them
```

Validation should inspect actual mapped providers, not only configuration files.

## 2.6 Principle: smallest valid policy scope

**Policy should be applied at the narrowest scope that correctly owns it.**

Examples:

```text
world-wide:
XDG runtime base, fundamental loader policy

capability-wide:
Vulkan provider selection, font provider

application-family:
Electron sandbox policy

application-specific:
VS Code GPU-vsync workaround
```

A shared environment file that accumulates all four categories becomes difficult to reason about.

## 2.7 Invariant: no untracked global foreign-runtime mutation

**Foreign application support must not depend on hidden shell-session mutation.**

The runtime should be reproducible from explicit launch composition.

Avoid architecture that requires the user to remember:

```sh
export SOMETHING=...
export LD_LIBRARY_PATH=...
unset SOMETHING_ELSE
```

before launching one application.

## 2.8 Principle: application domains consume capabilities

**Applications should declare what they need; providers should be selected separately.**

Example:

```text
PyMOL requires:
    x11
    fonts
    python-runtime
    opengl

Current provider mapping:
    x11 -> glibc Termux-aware X11 stack
    fonts -> selected font/fontconfig provider
    python-runtime -> chosen Conda/prefix runtime
    opengl -> Zink -> Vulkan -> Turnip
```

This allows provider upgrades without rewriting the application’s identity.

## 2.9 Invariant: warehouse is not promoted runtime closure

**A broad artifact pool may support research, but a promoted runtime contract must identify its actual intended dependency/provider set.**

The current broad farm can remain a compatibility/research pool during migration, but long-term production promotion should be manifest-driven.

## 2.10 Principle: preserve upstream locality when valid

**Do not destroy application-local runtime topology without evidence.**

Upstream applications may bundle libraries for specific reasons. Preserve `$ORIGIN`-based locality unless analysis proves replacement is safe and preferable.

This prevents the shared provider pool from becoming an uncontrolled override layer.

## 2.11 Invariant: evidence precedes promotion

**A runtime artifact or policy becomes promoted only after repeatable gates support the claim.**

A successful screenshot proves visible output, not necessarily:

```text
GPU acceleration path
specific driver provider
zero-copy presentation
absence of software fallback
```

Promotion criteria must match the claim.

## 2.12 Principle: mechanism before automation

**Do not generalize helpers until the manual contract is understood and stable.**

Preferred order:

```text
manual experiment
    -> record evidence
    -> isolate mechanism
    -> define contract
    -> create validator
    -> automate repeatable transformation
```

This is especially important for future `gl-adopt` or `gl-doctor` tooling.

## 2.13 Invariant: source, generated state, mutable state, and cache have owners

Every top-level runtime path should answer:

```text
Who creates it?
Who may modify it?
Is it version controlled?
Can it be regenerated?
Can it be deleted safely?
Is it part of rollback/promotion?
```

At minimum distinguish:

```text
source-of-truth configuration
materialized runtime output
mutable user/application state
build/cache state
evidence artifacts
```

## 2.14 Principle: reversible promotion

**Validated candidates should be promoted through cheap reversible indirection when practical.**

The versioned Mesa-prefix + stable symlink model is a strong pattern:

```text
candidate versioned prefix
    -> validate
    -> promote stable pointer
    -> rollback by repointing
```

Apply the same pattern to other replaceable providers when appropriate.

## 2.15 Invariant: claims have scopes

Every project conclusion should identify scope:

```text
hardware target
Android/kernel context
ABI world
provider version/configuration
feature path tested
validation method
```

Example:

```text
“Default WSI presentation worked in tested glibc stack”
```

must not silently become:

```text
“All presentation is proven zero-copy and universally correct.”
```

## 2.16 Principle: failures are architecture data

Negative experiments should be preserved when they define boundaries.

But failed paths should not remain active configuration merely because they are historically interesting.

Separation:

```text
experiments/
    -> preserve investigation history

contracts/current docs
    -> current interpretation

setup/runtime
    -> promoted active behavior only
```

## 2.17 Constitutional review checklist

Before merging a structural change, ask:

1. Does it preserve process ABI purity?
2. Does it introduce an implicit bridge?
3. Does it broaden policy scope unnecessarily?
4. Does it make provider resolution less deterministic?
5. Does it turn a warehouse into an undocumented runtime dependency?
6. Can the change be validated and rolled back?
7. Is provenance preserved?
8. Is the change an architectural contract or merely a current workaround?

## Project references

- [`../architecture.md`](../architecture.md)
- [`../glibc-layer.md`](../glibc-layer.md)
- [`../desktop-session.md`](../desktop-session.md)
- [`../gpu.md`](../gpu.md)
- [`../../STATUS.md`](../../STATUS.md)
