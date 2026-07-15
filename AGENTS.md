# Project agent contract

This is the canonical platform-neutral contract for agents working on `termux-native-desktop`. Platform-specific transport and tool constraints are documented under `docs/operations/platforms/`.

## Project identity

The project investigates whether a stock, non-root Android phone can provide a practical native Termux research and development workstation while retaining controlled access to mainstream glibc applications and real Adreno GPU acceleration.

The system is a heterogeneous userspace composition, not a hidden container distribution and not a general installer framework.

```text
Android / Termux native host authority
    + explicit glibc application worlds
    + explicit bridges
    + capability providers
    + application domains
    + evidence-driven promotion
```

PRoot or Debian may be used as an oracle, dependency solver, supply source, artifact warehouse, or debugging control. They are not the normal application runtime baseline.

## Stable engineering principles

- Preserve the native Android/Termux host authority.
- Keep ABI and provider boundaries explicit.
- Prefer the simplest reference path that satisfies the actual requirement.
- Require additional evidence in proportion to the deviation and risk, not by habit.
- Separate observation, candidate identity, provider authority, composition, population, activation, and acceptance.
- Preserve exact Git and result coordinates for accepted transitions.
- Treat a repository checkout as authoring state, not live runtime activation.
- Keep generated providers, workspaces, application payloads, selected generations, and user data outside Git unless their semantic contract explicitly says otherwise.
- Do not claim device behavior that was not verified on the user's Android environment.

## Current authority order

For normal onboarding and active work, read in this order:

```text
START_HERE.md
AGENTS.md
docs/current/BRIEF.md
docs/current/ACTIVE_TASK.md
ACTIVE_TASK required-reading list
applicable platform profile
```

Use `docs/INDEX.md` to locate deeper material. [`docs/DOCUMENTATION_MODEL.md`](docs/DOCUMENTATION_MODEL.md) defines authority by question, lifecycle states, conflict handling, and the machine-readable catalog.

Current semantic state is owned by `docs/current/`. Durable architecture and decisions support that state. Experiment reports and numbered refactor records preserve evidence and history; they are not default onboarding material. A proposed decision has no authority effect until explicitly accepted.

A dated handoff is never current authority. Historical handoffs may be consulted only when a task requires reconstruction of a specific transition.

## Context discipline

- Do not read the whole repository before starting a bounded task.
- Do not load `docs/refactor/`, dated handoffs, or large experiment reports by default.
- Read historical evidence only when a current document cites a specific unresolved claim or the active task explicitly requests historical reconstruction.
- Do not read session-close instructions during normal onboarding or active research.
- Keep default onboarding within the cataloged four-file budget; active-task required reading may contain at most eight documents.
- A platform profile is loaded when platform-specific transport, exchange, or execution becomes relevant, not merely because the platform exists.
- When a current document conflicts with an older document, record the conflict and follow the explicit current authority until it is repaired.
- Reusable lessons belong in durable operations or architecture documents, not only in chat narrative.

## User and agent roles

The agent performs the complex, context-heavy work:

```text
inspect repository and evidence
author and test changes in the sandbox
construct patches, bundles, scripts, and one-command runners
simulate non-device portions
package immutable .tar.zst exchanges
review returned result archives
update canonical documentation with accepted transitions
```

The user normally performs only work that must occur in the authoritative Android/Termux environment:

```text
create and attach a full Git bundle for a new web-chat session
run one bounded command or wrapper
perform authoritative local Git / gh mutation and push
provide device-only evidence and final status
make project-priority and policy decisions
```

Do not shift patch editing, command assembly, log analysis, or Git repair to the user when the agent can do it safely.

## Git and repository transport

The user's Termux checkout is the authoritative environment for remote Git mutation.

For a new web-chat session, the normal repository input is a user-created full Git bundle. Clone the bundle locally and work with ordinary Git objects. Do not reconstruct the repository by repeatedly fetching raw files through the GitHub connector.

The GitHub connector is limited to lightweight remote inspection such as repository metadata, commit confirmation, branch comparison, issues, pull requests, and small targeted file reads. It is not the normal clone, authoring, commit, or push transport.

Local sandbox commits and candidate bundles are preparation artifacts. A change becomes accepted only after the guarded Termux transaction applies, tests, pushes, verifies, and returns evidence.

## File exchange

Google Drive is the normal bidirectional exchange channel for:

```text
agent-to-user runner packages
user-to-agent result archives
patches and Git bundles
safety bundles
logs and bounded evidence
```

Use one related `.tar.zst` per exchange. Prefer a full Git bundle only when repository history or topology must cross the environment boundary; use patches for ordinary bounded changes.

## Execution environment restrictions

- Do not use or propose Docker for this project.
- The sandbox cannot establish Android runtime, GPU, package-manager, or live deployment facts.
- The user Termux environment is authoritative for Android execution, deployment, `git`, `gh`, and `rclone` actions.
- Synthetic tests must be identified as synthetic.
- A prepared package is not an executed change.
- A received result is not an accepted result until its integrity and semantic meaning are reviewed.
- An unexecuted stage should be represented explicitly, normally with status `125` in transaction summaries.

## Change discipline

Before authoring:

1. verify the exact repository baseline;
2. identify the active task and its stop conditions;
3. inspect only required authority and evidence;
4. state material assumptions.

Before publishing a candidate:

1. run repository checks and bounded regression tests;
2. use a real timeout and closed stdin for shell tests;
3. verify exact changed paths and `git diff --check`;
4. preserve unrelated user state;
5. create a self-contained runner and result archive path;
6. keep remote push guarded by an exact expected baseline.

After a successful transition, update canonical current state during the same repository transition. Do not defer current-state maintenance to a future narrative handoff.

## Working boundaries

The current active task defines the permitted workstream. Do not silently expand a review into acquisition, installation, runtime mutation, provider promotion, target population, or unrelated refactoring.

When blocked by missing device evidence, produce the smallest bounded device action needed. When blocked by a project decision, stop and present the decision rather than choosing an architecture by inertia.
