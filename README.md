# termux-native-desktop

An active systems-engineering project for turning a single non-root Android phone into a practical research and development workstation.

> **Goal:** run a high-performance native Termux desktop environment without a PRoot-mediated normal application runtime, while retaining access to mainstream glibc applications and real Adreno GPU acceleration.

This repository is both the working laboratory and the curated technical record. It is not an installer framework, package manager, or black-box setup script.

## Project question

Can a stock, non-root Android phone provide a desktop environment suitable for real technical work—coding, remote development, project navigation, scientific visualization, data inspection, Git review, and manuscript writing—without accepting a containerized runtime as the normal execution path?

The project was discovered through three practical workstreams:

```text
native desktop/session
        |
        +-- bionic-native applications and services
        |
        +-- glibc application layer
        |      +-- Termux glibc core
        |      +-- Debian rootfs research/library/data inputs
        |      +-- application-local libraries
        |
        +-- GPU acceleration
               +-- bionic Mesa/Turnip
               +-- glibc Mesa/Turnip
               +-- ANGLE Vulkan and Zink consumers
```

The current target architecture describes the deeper model as a heterogeneous userspace composition system: coherent worlds, explicit bridges, capability providers, application runtime domains, supply adapters, and validation gates.

PRoot remains useful as a dependency solver, artifact/library warehouse, behavioral oracle, and debugging control environment. It is intentionally excluded from the normal application execution path. Selected passive reads from the Debian rootfs still exist and are modeled separately from PRoot process execution.

## Active architecture and refactor note

The repository is currently crossing from bottom-up discovery into top-down semantic refactoring.

```text
main
    -> system knowledge, project foundation, target architecture,
       reassessment, consistency audit

refactor/module-package-layout
    -> validated ownership migration, live deployment records,
       ABI incident evidence, branch-specific hard-refactor handoff
```

The ownership refactor is retained, but current objects such as `modules/gl`, `~/gl/env`, `gl-run`, and the broad farm are not automatically treated as final architecture merely because they work or already exist.

For current architectural direction, read:

- [`docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md`](docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md) — why the direction changed and what is decided.
- [`docs/system-foundation/12-document-consistency-audit-and-execution-order.md`](docs/system-foundation/12-document-consistency-audit-and-execution-order.md) — how all foundation documents fit together, what remains open, and the current execution order.

The refactor branch carries its operational handoff in `docs/refactor/0016-next-session-handoff.md`.

## Repository map

The default branch still reflects the pre-merge physical layout in parts of the tree. Treat this map as current branch topology, not a declaration of final ownership architecture.

- `docs/` — project context, current operational guides, foundational knowledge, target-system design, reassessment, consistency audit, timeline, and durable decisions.
- `experiments/` — the living workbench. Each experiment keeps a concise canonical `README.md`; session-derived full reports live beside it as `report.md`; raw captures go in `evidence/` when useful.
- `setup/` — current default-branch promoted runtime configuration and launch artifacts; the refactor branch migrates ownership toward `modules/`, `packages/`, and `tools/`.
- `scripts/` — current default-branch repository/deployment helpers; the refactor branch introduces explicit `tools/` ownership.
- `STATUS.md` — current conclusions, architecture authority, implementation stop line, unresolved questions, and immediate execution order.

The intended information flow is:

```text
question
  -> experiment
  -> evidence
  -> working conclusion (STATUS.md)
  -> durable decision / invariant update
  -> contract
  -> validation gate
  -> implementation candidate
  -> validation evidence
  -> promotion
```

## Documentation guide

- [`docs/PROJECT_CONTEXT.md`](docs/PROJECT_CONTEXT.md) — motivation and scope.
- [`docs/architecture.md`](docs/architecture.md) — current integrated system model for its recorded branch/runtime context.
- [`docs/glibc-layer.md`](docs/glibc-layer.md) — current glibc layer bootstrap, boundaries, onboarding, traps, and maintenance model.
- [`docs/gpu.md`](docs/gpu.md) — Turnip/Zink build and runtime contract plus diagnostic history.
- [`docs/desktop-session.md`](docs/desktop-session.md) — Termux:X11/XFCE two-world session contract.
- [`docs/knowledge/README.md`](docs/knowledge/README.md) — progressive systems knowledge layer developed from the project investigation.
- [`docs/system-foundation/README.md`](docs/system-foundation/README.md) — project essence, invariants, system/object model, target architecture, reassessment, consistency audit, and execution order.
- [`experiments/README.md`](experiments/README.md) — experiment index and provenance contract.

## Companion project

[`cpython-android-cli`](https://github.com/daylight-00/cpython-android-cli) is maintained separately. It was motivated by this workstation, but its research question—adapting the official Android CPython runtime for normal Termux CLI use with uv integration—is independently coherent.

## Status

This is an active experiment and architecture-refactoring project, not a finished distribution. Working paths are kept alongside failed and abandoned investigations when those failures define useful boundaries. Preserve evidence and validated semantics; implementation objects and command names remain replaceable. See [`STATUS.md`](STATUS.md).
