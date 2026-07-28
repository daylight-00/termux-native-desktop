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


Current target-population status: `INTERVENTION_RETAINED`; 14 of 41 concrete objects have qualified retained-result binding inputs, 27 require exact result coordinates, and no materializer, population, deployment or activation authority exists.


## Local-supply evidence authorization and coordinate contract

The current candidate defines an 18-claim immutable owner-authorization token schema and a canonical complete 41-row coordinate-receipt schema with 30 fail-closed validation rules. It contains zero live tokens, paths or provider reads and grants no evidence-execution or runtime authority.


## Local-supply evidence authorization and coordinate contract acceptance

The exact 18-claim owner-authorization token schema, canonical 41-row/10-field coordinate-receipt schema and 30 validation rules are accepted as a non-mutating interface. No token or coordinate has been issued, no provider byte has been read and evidence execution remains unauthorized.


## Non-executing local-supply evidence authorization issuance and coordinate production design

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-DESIGN-REVIEW-001` qualifies a 14/18/36/20 design candidate with zero live authority. Separate design acceptance, owner issuance, coordinate production, provider reads, evidence execution and runtime effects remain blocked.


## Bounded non-executing selected-provider local-supply evidence authorization issuance and coordinate-receipt production transaction design acceptance

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-DESIGN-ACCEPT-001` accepts the exact v120 six-artifact 14-input/18-state/36-operation/20-failure design boundary. Historical candidate evidence remains frozen. Issuance, coordinate production, discovery, provider reads, evidence execution, local-map production and all runtime effects remain unauthorized.

bounded non-executing selected-provider local-supply evidence authorization issuance and coordinate-receipt production transaction design accepted

## Non-executing local-supply evidence issuance and coordinate-production implementation candidate

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-IMPLEMENTATION-REVIEW-001` qualifies a synthetic-only implementation candidate with 88 exact design-coverage rows, one deterministic success fixture and twenty fail-closed cases. It opens no provider path, reads no provider byte, performs no write and creates no live authority. Implementation acceptance and every live issuance or execution gate remain separate and blocked.

## Bounded non-executing synthetic local-supply evidence implementation acceptance

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-AUTHORIZATION-ISSUANCE-COORDINATE-PRODUCTION-IMPLEMENTATION-ACCEPT-001` accepts the exact v122 six-artifact synthetic-only implementation boundary: 88 coverage rows, one deterministic success fixture, twenty fail-closed cases, 41 synthetic coordinate rows, zero provider reads, zero writes and zero live authority. Live inputs, issuance, coordinate production, evidence execution and all runtime effects remain unauthorized.

bounded non-executing synthetic selected-provider local-supply evidence implementation accepted

## Non-executing live-input adapter and execution-authorization contract candidate

`SELECTED-PROVIDER-LOCAL-SUPPLY-EVIDENCE-LIVE-INPUT-ADAPTER-EXECUTION-AUTHORIZATION-CONTRACT-REVIEW-001` qualifies an exact eight-artifact contract candidate with ten explicit input channels, a twenty-field inactive adapter envelope, a 27-claim execution authorization, 37 validation rules, 18 states, 32 operations and 20 failure contracts. It preserves zero live inputs, provider reads, writes and live authority.

The accepted synthetic implementation remains immutable as a semantic and regression oracle, not a live executor. Live-to-synthetic path rewriting and live invocation of the synthetic CLI are forbidden; a future live adapter/executor requires separate implementation review and acceptance.
