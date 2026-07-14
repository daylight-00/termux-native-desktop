# termux-native-desktop

An active systems-engineering project for turning a single non-root Android phone into a practical research and development workstation.

> **Goal:** run a high-performance native Termux desktop environment without a PRoot-mediated normal application runtime, while retaining access to mainstream glibc applications and real Adreno GPU acceleration.

This repository is both the working laboratory and the curated technical record. It is not an installer framework, package manager, or black-box setup script.

## Project question

Can a stock, non-root Android phone provide a desktop environment suitable for real technical work—coding, remote development, project navigation, scientific visualization, data inspection, Git review, and manuscript writing—without accepting a containerized runtime as the normal execution path?

## Current architecture direction

The project is best understood as a heterogeneous userspace composition system.

```text
Android/Termux native host
    +
coherent glibc application world
    +
explicit bridges
    +
capability providers
    +
application domains
    +
evidence-driven promotion
```

Current operational realization:

```text
native desktop/session
        |
        +-- bionic applications and services
        +-- native uv-base environment
        +-- Termux:X11 display bridge
        |
        +-- glibc application processes
        |      +-- package-manager-owned glibc substrate
        |      +-- current prefix/rootfs/farm providers
        |      +-- application-local payloads
        |      +-- VS Code / Obsidian / Conda
        |
        +-- graphics providers
               +-- bionic Mesa/Turnip
               +-- glibc Mesa/Turnip
               +-- ANGLE Vulkan and Zink consumers
```

PRoot remains useful as a dependency solver, artifact/library/data warehouse, behavioral oracle, and debugging control. It is excluded from normal application process execution.

Current paths such as `modules/gl`, `~/gl/env`, `gl-run`, and the broad farm are not automatically final architecture. The project preserves validated semantics and evidence rather than object identity by inertia.

## Current milestone

```text
scoped graphics-policy promotion:
    CLOSED

selected D-Bus provider pilot:
    PASS

selected Obsidian application-domain closure:
    ACTIVE / INCOMPLETE

atomic activation:
    OPEN

glibc corrected/newer substrate lifecycle:
    OPEN

PyMOL runtime pilot:
    DEFERRED pending reusable-object decisions
```

Current post-closure audit:

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
```

Current provider-authority gap-evidence acquirer:

```text
docs/refactor/0154-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-acquirer.md
```

## Repository checkout

Canonical live-device checkout:

```text
$HOME/projects/termux-native-desktop
```

Repository tools must derive source root from their own location rather than treating the checkout pathname as architectural identity.

## Repository map

- `modules/` — current project-authored physical integrations and overlays; not necessarily one-to-one with final semantic objects.
- `packages/` — lifecycle definitions and launch integration for external payloads.
- `experiments/` — architecture discrimination, evidence, provenance, and historical diagnostics.
- `tests/` — cross-cutting repository and integration validation.
- `tools/` — repository/deployment operator workflows.
- `docs/` — context, architecture, operational guides, refactor records, audits, timeline, and durable decisions.
- `STATUS.md` — current conclusions, architecture authority, stop lines, and next focus.

The intended information flow is:

```text
question
  -> experiment
  -> evidence
  -> interpretation correction
  -> working conclusion
  -> semantic contract / decision
  -> active gate
  -> promoted implementation
  -> trigger-based revalidation
```

Not every experiment helper becomes a permanent active test.

## Documentation guide

- [`docs/PROJECT_CONTEXT.md`](docs/PROJECT_CONTEXT.md) — motivation and scope.
- [`docs/architecture.md`](docs/architecture.md) — current operational realization and target semantic model.
- [`docs/glibc-layer.md`](docs/glibc-layer.md) — current compatibility baseline, application-domain target, and lifecycle boundaries.
- [`docs/gpu.md`](docs/gpu.md) — current graphics composition and evidence contract.
- [`docs/desktop-session.md`](docs/desktop-session.md) — Termux:X11/XFCE two-world session contract.
- [`docs/refactor/README.md`](docs/refactor/README.md) — chronological refactor/evidence index and precedence.
- [`docs/refactor/0091-scoped-graphics-policy-promotion-closure.md`](docs/refactor/0091-scoped-graphics-policy-promotion-closure.md) — closed graphics transaction.
- [`docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md`](docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md) — current top-down audit, missing work, and revised priority.
- [`experiments/README.md`](experiments/README.md) — experiment status and provenance contract.

Top-down foundation documents live on `main` under `docs/system-foundation/`; branch-local absence does not make them irrelevant.

## Immediate architecture order

```text
1. synchronize documentation and gate lifecycle;
2. resume or terminate selected Obsidian closure;
3. decide semantic world/provider/bridge/family/application ownership;
4. define atomic activation before another multi-file migration;
5. move high-risk over-scoped policies with evidence;
6. define glibc substrate upgrade/recovery lifecycle;
7. use PyMOL as proof of the resulting architecture.
```

Do not begin PyMOL by copying an Electron launcher, expanding `gl/env`, or blindly broadening the farm.

## Companion project

[`cpython-android-cli`](https://github.com/daylight-00/cpython-android-cli) is maintained separately. It was motivated by this workstation, but its research question—adapting the official Android CPython runtime for normal Termux CLI use with uv integration—is independently coherent.

## Status

This is an active experiment and architecture-refactoring project, not a finished distribution. Failed and superseded paths remain when they define useful boundaries. See [`STATUS.md`](STATUS.md).
