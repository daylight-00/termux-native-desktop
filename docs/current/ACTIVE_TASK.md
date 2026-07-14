# Active task: synchronize current documentation authority

> Task ID: `current-authority-synchronization`
>
> Expected state on completion: `documentation-control-plane` remains active, but all default current-facing documents agree with the accepted repository, deployment, local-layout, and research boundary.

## Objective

Repair the existing current-facing documentation so a new agent following `START_HERE.md` cannot be redirected into deleted branches, completed activation work, retired local ownership, or the former narrative-handoff lifecycle.

## Why now

The repository already has accepted structural changes that several prominent documents do not reflect:

```text
single canonical main
immutable repository releases
explicit deployment activation
retired ~/gl/.git authority
XDG-state Mesa workspace and provider store
provider-authority workstream paused for assurance-depth policy
```

Until these are synchronized, the new initialization control plane can route correctly but deeper current documents can still contradict it.

## Current accepted decisions

- New web-chat sessions start from a user-provided full Git bundle.
- The cloned repository initializes itself through `START_HERE.md`.
- Narrative handoff documents are not current authority.
- Canonical current state belongs under `docs/current/`.
- Historical records remain available but are excluded from default onboarding.
- GitHub connector use is limited to lightweight remote inspection.
- User Termux local Git and `gh` remain authoritative for remote mutation.
- Docker is unavailable and outside the project workflow.

## In scope

- Update root and documentation indexes to route through the new control plane.
- Synchronize `README.md`, `STATUS.md`, `docs/architecture.md`, `docs/glibc-layer.md`, and `modules/gl/README.md` with immutable deployment and the XDG-state local layout.
- Correct `docs/refactor/README.md` branch and current-chain metadata.
- Remove `docs/handoff/CURRENT.md` from current authority and classify dated handoffs as historical transition evidence.
- Recast the old session lifecycle and close documents as historical process material or replace them with bundle-native start guidance.
- Update the timeline through repository consolidation and local-layout migration.
- Mark Decision 0002 as superseded or narrowed by the later provider-authority model.
- Repair current internal links that still target removed pre-refactor paths.

## Out of scope

- Moving or renaming all numbered refactor records.
- Rewriting all experiment reports.
- Resuming provider evidence acquisition or SUP-02 response production.
- Performing device runtime, graphics, or application tests.
- Large constitutional consolidation beyond corrections needed to resolve current authority.
- Designing the final assurance-depth policy; this task may prepare its explicit decision surface only.

## Required reading

Read these documents as current authority or direct repair targets:

- `docs/current/BRIEF.md`
- `docs/current/STATE.yaml`
- `docs/PROJECT_PRINCIPLES.md`
- `docs/decisions/0004-single-main-and-immutable-release-deployment.md`
- `packages/mesa-glibc/README.md`
- `README.md`
- `STATUS.md`
- `docs/README.md`
- `docs/architecture.md`
- `docs/glibc-layer.md`
- `modules/gl/README.md`
- `docs/refactor/README.md`
- `docs/session-operations/README.md`
- `docs/handoff/CURRENT.md`

Do not read numbered refactor records or full experiment reports by default. Open a specific record only when one of the repair targets makes a claim whose current replacement cannot be established from the documents above and Git history.

## Known facts

- The accepted repository branch is `main`.
- Immutable release deployment is implemented and active.
- The local-layout migration completed successfully.
- The canonical active Mesa provider is represented through the XDG-state provider store.
- The old current handoff records a deleted branch and an obsolete boundary.
- There is no blocking result archive awaiting review.

## Pending external inputs

None. See [`PENDING_ARTIFACTS.yaml`](PENDING_ARTIFACTS.yaml).

## Next valid action

Produce one bounded documentation synchronization candidate and a repository test that rejects the known stale current-authority patterns.

## Stop conditions

Stop before implementation if:

- the checked-out bundle does not contain the accepted local-layout migration;
- `main` is not the candidate's sole intended long-lived base;
- a proposed correction would reinterpret provider evidence rather than only synchronize accepted state;
- a historical record would need destructive rewriting instead of indexing or status classification.

## Completion criteria

- Default onboarding contains no deleted branch or narrative-handoff dependency.
- Current-facing deployment and local-layout descriptions agree.
- The current provider-authority boundary and prohibited claims agree.
- Historical handoffs and numbered records remain discoverable but are not default authority.
- Repository tests reject reintroduction of the known stale patterns.
- `docs/current/` advances to the next explicit task without relying on chat memory.
