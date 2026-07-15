# Project constitution: identity and boundary

> **Status:** canonical constitutional authority
>
> This document is the single current source for the project's purpose, system boundary, quality goals, and non-goals. Earlier context and system-foundation documents are retained as design provenance, not competing current authority.

## Purpose

`termux-native-desktop` asks a practical systems-engineering question:

> How far can a stock, non-root Android phone be turned into a credible research and development workstation while preserving native host performance, explicit compatibility boundaries, and reversible system changes?

The immediate workload includes coding, remote development, complex project navigation, scientific visualization, data inspection, cluster work, diff review, and technical writing. A terminal-only environment is useful but insufficient; the target is a practical workstation that can use an external display, keyboard, and mouse through the phone's normal Android environment.

## Abstract identity

The project is a **heterogeneous userspace composition system for a non-root Android workstation**.

```text
Android / Termux native host authority
    + coherent bionic and glibc execution worlds
    + explicit cross-world bridges
    + ABI-appropriate capability providers
    + application runtime domains
    + evidence-gated promotion and activation
```

It is not a hidden container distribution. It does not replace Android or Termux with Debian. It composes conventional Linux application capabilities beside the native host while keeping each process inside a coherent ABI world.

## Authoritative host

The authoritative machine remains:

```text
stock Android kernel and security model
Termux bionic userspace
Termux:X11 and the Android display/device boundary
user-owned non-root storage and process authority
```

Android device interfaces, package behavior, GPU paths, deployment, and remote Git mutation are established only in the user's Termux environment. Sandboxes and reference root filesystems can prepare or explain work but cannot establish device facts.

## Execution worlds

One kernel does not imply one userspace.

```text
world.bionic
    native Termux processes and Android-compatible providers

world.glibc
    conventional Linux/glibc application processes and coherent glibc providers
```

The worlds may share services through explicit bridges such as X11 or URL opening. They must not silently share low-level runtime libraries, loader policy, or provider state across ABI boundaries.

## Capability and application model

The architecture is described through semantic objects rather than one umbrella directory or package manager:

```text
World
Application Domain
Capability
Provider
Bridge
Artifact Source / Supply Adapter
Validation Gate
```

Applications consume capabilities through selected providers. Artifact origin is an input to review, not automatic runtime ownership. Current concrete composition is documented under [`../architecture/`](../architecture/README.md).

## PRoot and distribution root filesystems

PRoot is excluded from the normal promoted application runtime. It remains useful for bounded roles:

```text
package and dependency oracle
supply or extraction source
reference/control environment
debugging and comparison
```

A distribution rootfs may supply evidence or artifacts without becoming the workstation's authoritative runtime.

## Project outputs

The project produces more than launchable applications. Its durable outputs are:

```text
an inspectable system model
project-owned source and integration contracts
reproducible candidate and deployment transactions
validated runtime/provider compositions
claim-scoped evidence and receipts
negative results that constrain future architecture
```

The repository is therefore both a live system source tree and a structured research record. Current interpretation is separated from historical provenance rather than rewriting history to resemble the latest design.

## Quality goals

The project optimizes for:

- **native performance:** avoid avoidable emulation and runtime indirection;
- **coherence:** preserve one valid ABI/runtime world per process;
- **explicitness:** make provider, bridge, adaptation, and policy selection inspectable;
- **reproducibility:** bind accepted transitions to exact Git and result coordinates;
- **inspectability:** prefer understandable mechanisms over opaque setup systems;
- **reversibility:** separate candidate preparation, promotion, activation, and rollback;
- **practicality:** spend assurance effort in proportion to changed semantics and consequence;
- **learning value:** preserve evidence that explains both successes and failures.

## Non-goals

The project is not:

- a general Android Linux distribution;
- a promise of universal Linux binary compatibility;
- a conventional container or virtual-machine desktop;
- a mandate to force every application through one graphics path;
- a package manager or general installer framework;
- a reason to treat every experiment, workaround, directory, or helper as permanent architecture;
- a requirement to reproduce an authoritative supplier's entire build chain when the project consumes an unchanged reference artifact and makes a narrower integration claim.

## Repository boundary

`termux-native-desktop` owns the end-to-end workstation system: native session, glibc worlds, capability providers, application integration, deployment, validation, and collaboration workflow.

`cpython-android-cli` remains a companion project. This repository may consume its released runtime contract without absorbing its independent experiment history.

## Related constitutional authority

- [`PRINCIPLES.md`](PRINCIPLES.md) — engineering invariants, evidence, promotion, and assurance.
- [`../../AGENTS.md`](../../AGENTS.md) — agent/user authority and execution contract.
- [`../decisions/README.md`](../decisions/README.md) — durable decision lifecycle.
- [`../architecture/README.md`](../architecture/README.md) — current system realization and component contracts.
