# Current project brief

> Semantic state version: `2026-07-15.04`
>
> This is the compact current-state entry point. Exact commit and tree coordinates come from the checked-out full Git bundle, not from self-referential repository text.

## Purpose and constitutional boundary

`termux-native-desktop` is a systems-engineering project for turning a stock, non-root Android phone into a practical native Termux research and development workstation.

```text
Android / Termux native host authority
    + coherent bionic and glibc execution worlds
    + explicit bridges and capability providers
    + application runtime domains
    + evidence-gated promotion and activation
```

PRoot and Debian may serve as oracle, supply, reference, or debugging control. They are excluded from the normal promoted application runtime.

Current constitutional authority is deliberately compact:

```text
docs/constitution/PROJECT.md
    identity, boundary, quality goals and non-goals

docs/constitution/PRINCIPLES.md
    engineering, evidence, promotion and assurance invariants

AGENTS.md
    agent/user authority, context, transport and execution discipline
```

Former project-context/principles and system-foundation documents are preserved as design provenance.

## Current structural state

- `main` is the only intended long-lived integration branch.
- The user Termux checkout is authoritative for remote Git mutation and device execution.
- A checkout is authoring state, not live runtime authority.
- Repository deployment uses immutable releases with explicit `current` activation and retained rollback state.
- The historical `$HOME/gl/.git` authority is retired and preserved in safety artifacts.
- Mesa mutable work and provider candidates are canonical under XDG state.
- Legacy `$HOME/gl/build` and `$HOME/gl/opt` are compatibility coordinates only.
- Application bodies, selected generations, provider contents, and user data remain outside repository ownership.

## Current provider boundary

The provider-authority workstream remains paused at the 0165 SUP-02 boundary:

```text
SUP-02 producer implemented
28 issued requests still without canonical responses
no build-attestation/adaptation closure accepted
no provider/composition/target-layout completion accepted
no selected-generation activation accepted
```

[`../decisions/0005-proportional-assurance-depth.md`](../decisions/0005-proportional-assurance-depth.md) is now accepted policy.

Assurance is selected before evidence collection from:

```text
exact claim
    + implementation class
    + project-owned changed boundary
    + risk modifiers
```

The previous blanket demand for producing-build custodian exports across all 28 roots is no longer the default. Existing provider claims must be reclassified before further evidence requests. This policy change does not itself accept a provider or target.

## Documentation and web-session state

- New web-chat sessions receive a user-created full Git bundle and start at `START_HERE.md`.
- `docs/current/` owns current semantic state, the active task, and pending external artifacts.
- [`../DOCUMENTATION_MODEL.md`](../DOCUMENTATION_MODEL.md) defines authority and lifecycle by question.
- [`../catalog.tsv`](../catalog.tsv) is the machine-readable document catalog.
- Default onboarding is exactly four files and loads no history.
- Narrative handoffs, numbered refactor records, experiment reports, and system-foundation documents are not default onboarding authority.
- GitHub connector use is limited to lightweight remote inspection; it is not clone/commit/push transport.
- Google Drive is the normal exchange path for bundles, patches, runners, results, logs, and safety artifacts.

## Current project phase

The active task is `operations-consolidation-and-historical-surface-cleanup`.

It will:

```text
consolidate durable collaboration and tool rules under docs/operations
remove remaining overlap with legacy session-operations documents
preserve reusable failure lessons
keep normal accepted sessions handoff-free
make optional incomplete-work checkpoints explicit and bounded
```

The provider-authority workstream stays paused during this task.

## Current non-goals

Do not currently:

- resume or fulfill SUP-02 requests;
- infer provider acceptance from ADR 0005;
- populate a provider target layout;
- activate the selected Obsidian generation;
- redesign the runtime around Docker or a PRoot application baseline;
- reconstruct the repository through raw GitHub connector reads;
- read or move the full historical corpus by default.

## Start and navigation

- Active task: [`ACTIVE_TASK.md`](ACTIVE_TASK.md)
- Machine state: [`STATE.yaml`](STATE.yaml)
- Pending external inputs: [`PENDING_ARTIFACTS.yaml`](PENDING_ARTIFACTS.yaml)
- Documentation model: [`../DOCUMENTATION_MODEL.md`](../DOCUMENTATION_MODEL.md)
- Documentation router: [`../INDEX.md`](../INDEX.md)
- Constitution: [`../constitution/README.md`](../constitution/README.md)
- Agent contract: [`../../AGENTS.md`](../../AGENTS.md)
