# termux-native-desktop

An active systems-engineering project for turning a single non-root Android phone into a practical research and development workstation.

> **Goal:** run a high-performance native Termux desktop environment without a PRoot-mediated normal application runtime, while retaining access to mainstream glibc applications and real Adreno GPU acceleration.

This repository is both the working laboratory and the curated technical record. It is not an installer framework, package manager, or black-box setup script.


## Agent and session initialization

The repository is its own onboarding surface. Web-chat sessions receive a user-created full Git bundle, clone it in the sandbox, and begin at [`START_HERE.md`](START_HERE.md). Current semantic state and the active task live under [`docs/current/`](docs/current/); dated handoffs are historical transition evidence, not current authority.

The GitHub connector is limited to lightweight remote inspection. Authoritative remote Git mutation and Android/device execution remain in the user's Termux environment.

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
        |      +-- protected substrate, selected compatibility providers and rootfs-derived candidates
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

The repository and deployment control planes are consolidated:

```text
canonical integration branch: main
repository deployment: immutable release + current/previous pointers
legacy ~/gl Git authority: retired
Mesa mutable workspace: XDG state
Mesa provider candidates/current: XDG state
provider-authority workstream: paused at SUP-02 pending assurance-depth policy
documentation control plane: active
```

Use [`docs/current/BRIEF.md`](docs/current/BRIEF.md) for the compact current boundary and [`docs/current/ACTIVE_TASK.md`](docs/current/ACTIVE_TASK.md) for the next valid work.

## Repository checkout

Canonical live-device checkout:

```text
$HOME/projects/termux-native-desktop
```

Repository tools must derive source root from their own location rather than treating the checkout pathname as architectural identity.

The checkout is not the live release. `tools/deploy` materializes an immutable repository release under XDG state and points managed public leaves through one stable `current` pointer. Repository pulls and branch changes therefore remain authoring events until an explicit deployment activation.

## Branch policy

`main` is the only long-lived integration branch. Bounded topic branches may be used temporarily, but constitutional documents and accepted implementation must be merged into `main`, and merged branches are deleted after ancestry verification. Milestones use tags and recorded commit/tree identities rather than permanent branch proliferation.

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

- [`START_HERE.md`](START_HERE.md) — bundle-native agent/session initialization.
- [`AGENTS.md`](AGENTS.md) — durable project-agent contract.
- [`docs/DOCUMENTATION_MODEL.md`](docs/DOCUMENTATION_MODEL.md) — authority classes, lifecycle, conflict handling, and context budget.
- [`docs/INDEX.md`](docs/INDEX.md) — question-oriented router.
- [`docs/current/`](docs/current/) — current semantic state and active task.
- [`docs/constitution/`](docs/constitution/) — project purpose and invariants.
- [`docs/architecture/`](docs/architecture/) — current system and component contracts.
- [`docs/operations/`](docs/operations/) — collaboration, tool, and platform contracts.
- [`docs/decisions/`](docs/decisions/) — durable decision lifecycle.
- [`docs/evidence/`](docs/evidence/) — experiment and transaction evidence routing.
- [`docs/history/`](docs/history/) — chronology and old-state reconstruction.

Historical numbered records and dated handoffs remain available but are not default onboarding material.

## Immediate work order

The authoritative work order is maintained in [`docs/current/ACTIVE_TASK.md`](docs/current/ACTIVE_TASK.md). Historical numbered records remain evidence and are opened only when the active task names a specific need.

## Companion project

[`cpython-android-cli`](https://github.com/daylight-00/cpython-android-cli) is maintained separately. It was motivated by this workstation, but its research question—adapting the official Android CPython runtime for normal Termux CLI use with uv integration—is independently coherent.

## Status

This is an active experiment and architecture-refactoring project, not a finished distribution. Failed and superseded paths remain when they define useful boundaries. See [`STATUS.md`](STATUS.md).
