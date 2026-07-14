# Current project brief

> Semantic state version: `2026-07-15.01`
>
> This document is the compact current-state entry point. Exact commit and tree coordinates come from the checked-out Git bundle, not from self-referential text in the repository.

## Purpose

`termux-native-desktop` is an active systems-engineering project for turning a stock, non-root Android phone into a practical native Termux research and development workstation. It keeps the Android/Termux host authoritative while composing explicit glibc application worlds, graphics providers, bridges, application domains, and promotion evidence.

PRoot and Debian remain useful as oracle, dependency solver, supply source, artifact warehouse, and debugging control. They are excluded from the normal application runtime baseline.

## Current structural state

- `main` is the only intended long-lived integration branch.
- The canonical checkout is `$HOME/projects/termux-native-desktop`.
- The checkout is authoring state, not live runtime authority.
- Repository deployment materializes immutable releases under XDG state and activates them through a stable `current` pointer with a retained `previous` pointer.
- The historical `$HOME/gl/.git` authority is retired and preserved in safety artifacts.
- Mutable Mesa source/build state lives under the XDG-state workspace.
- Versioned Mesa provider candidates and the active provider pointer live under the XDG-state provider store.
- Legacy `$HOME/gl/build` and `$HOME/gl/opt` coordinates are compatibility paths, not canonical ownership.
- VS Code and Obsidian payloads, selected generations, user data, and provider contents were preserved through the local-layout migration.

## Current research boundary

The provider-authority workstream is paused at a bounded boundary:

```text
SUP-02 producer implemented
all 28 issued requests outstanding
no canonical supplier response produced
no build-attestation/adaptation closure accepted
no provider or target-layout completion accepted
```

Before resuming that workstream, the project must decide how much assurance is appropriate for reference-supplied, adapted, independently reproduced, and novel providers. Evidence depth should be proportional to deviation and risk rather than expanding automatically.

## Current project phase

The active phase is construction of a repository-owned documentation and agent control plane suitable for recurring web-chat sessions.

Phase 1 establishes:

```text
bundle-native repository initialization
stable agent contract
compact current-state surface
active-task routing
web-chat platform constraints
machine-checkable control-plane consistency
```

The next active task is to synchronize all current-facing documentation with the already accepted branch, deployment, local-layout, and provider-authority state.

## Current non-goals

Do not currently:

- resume or fulfill SUP-02 requests;
- populate a target provider layout;
- activate the selected Obsidian generation;
- redesign the runtime around Docker or a PRoot application baseline;
- reconstruct the repository through raw GitHub connector reads;
- reorganize all historical records before the current authority surface is stable.

## Start and navigation

- Active task: [`ACTIVE_TASK.md`](ACTIVE_TASK.md)
- Machine state: [`STATE.yaml`](STATE.yaml)
- Pending external inputs: [`PENDING_ARTIFACTS.yaml`](PENDING_ARTIFACTS.yaml)
- Documentation router: [`../INDEX.md`](../INDEX.md)
- Project agent contract: [`../../AGENTS.md`](../../AGENTS.md)
