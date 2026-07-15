# Project agent contract

This is the canonical platform-neutral contract for agents working on `termux-native-desktop`. Platform-specific transport and tool constraints are documented under `docs/operations/platforms/`.

## Constitutional routing

Do not reconstruct project philosophy from historical records.

- [`docs/constitution/PROJECT.md`](docs/constitution/PROJECT.md) owns project identity, boundary, quality goals, and non-goals.
- [`docs/constitution/PRINCIPLES.md`](docs/constitution/PRINCIPLES.md) owns stable engineering, evidence, promotion, and assurance principles.
- This file owns agent/user authority, context discipline, transport, and change execution.

The compact onboarding brief may summarize those documents but does not replace them.

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
Durable collaboration and execution mechanics are routed by [`docs/operations/README.md`](docs/operations/README.md).

Current semantic state is owned by `docs/current/`. Architecture and accepted decisions support that state. Experiment reports, foundation records, numbered refactor records, and dated handoffs preserve evidence or design provenance; they are not default onboarding authority. A proposed decision has no authority effect until explicitly accepted.

## Context discipline

- Do not read the whole repository before starting a bounded task.
- Do not load `docs/refactor/`, dated handoffs, the system-foundation corpus, or large experiment reports by default.
- Read historical evidence only when a current document cites a specific unresolved claim or the active task explicitly requests reconstruction.
- Do not read session-close instructions during normal onboarding or active research.
- Keep default onboarding within the cataloged four-file budget; active-task required reading may contain at most eight documents.
- Load a platform profile only when platform-specific transport, exchange, or execution becomes relevant.
- When current authority conflicts with an older document, follow current authority and record the conflict for repair.
- Reusable lessons belong in durable operations, constitution, decisions, or architecture documents, not only in chat narrative.

## User and agent roles

The agent performs the complex, context-heavy work:

```text
inspect repository and bounded evidence
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

For a new web-chat session, the normal repository input is a user-created full Git bundle. Clone it locally and work with ordinary Git objects. Do not reconstruct the repository through repeated raw-file GitHub connector reads.

The GitHub connector is limited to lightweight remote inspection such as metadata, commit confirmation, branch comparison, issues, pull requests, and small targeted file reads. It is not the normal clone, authoring, commit, or push transport.

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

Use one related `.tar.zst` per exchange. Prefer a full Git bundle when repository history or topology must cross the environment boundary; use patches or candidate bundles for ordinary bounded changes.

## Execution environment restrictions

- Do not use or propose Docker for this project.
- The sandbox cannot establish Android runtime, GPU, package-manager, or live deployment facts.
- The user Termux environment is authoritative for Android execution, deployment, `git`, `gh`, and `rclone` actions.
- Synthetic tests must be identified as synthetic.
- A prepared package is not an executed change.
- A received result is not accepted until its integrity and semantic meaning are reviewed.
- An unexecuted stage should be represented explicitly, normally with status `125`.

## Platform-failure stop-loss

A web-chat limitation is an execution boundary, not an invitation to accumulate retries.

```text
one bounded representative probe
    -> classify the unavailable capability
    -> stop repeating the same failing path
    -> switch to the documented fallback authority
    -> record a reusable new limitation in the platform registry
```

When exact external bytes are required but sandbox DNS or outbound access fails, do not keep trying mirrors, proxy tricks, alternate package managers, or repeated clone/download commands. Prepare one self-contained user-Termux acquisition or analyzer wrapper with exact URLs, expected digests, bounded analysis, and one result `.tar.zst`. The user performs the authoritative network/device action; the agent reviews the returned bytes or compact evidence.

The current web-chat limitation registry and fallback matrix are owned by [`docs/operations/platforms/chatgpt-web.md`](docs/operations/platforms/chatgpt-web.md) and [`docs/operations/platforms/chatgpt-web-limitations.tsv`](docs/operations/platforms/chatgpt-web-limitations.tsv).

## Change discipline

Before authoring:

1. verify the exact repository baseline;
2. identify the active task and stop conditions;
3. inspect only required authority and evidence;
4. state material assumptions.

Before publishing a candidate:

1. run repository checks and bounded regression tests;
2. use a real timeout and closed stdin for shell tests;
3. verify changed paths and `git diff --check`;
4. preserve unrelated user state;
5. create a self-contained runner and result archive path;
6. guard remote push with the exact expected baseline.

After a successful transition, update canonical current state during the same repository transition. Do not defer current-state maintenance to a narrative handoff.

## Working boundaries

The active task defines the permitted workstream. Do not silently expand a review into acquisition, installation, runtime mutation, provider promotion, target population, or unrelated refactoring.

When blocked by missing device evidence, produce the smallest bounded device action. When blocked by a project decision, stop and present the decision rather than choosing an architecture by inertia.
