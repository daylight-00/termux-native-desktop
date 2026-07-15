
# Current project brief

> Semantic state version: `2026-07-15.03`
>
> This document is the compact current-state entry point. Exact commit and tree coordinates come from the checked-out Git bundle, not from self-referential text in the repository.

## Purpose

`termux-native-desktop` is an active systems-engineering project for turning a stock, non-root Android phone into a practical native Termux research and development workstation. It keeps the Android/Termux host authoritative while composing explicit glibc application worlds, graphics providers, bridges, application domains, and promotion evidence.

PRoot and Debian remain useful as oracle, dependency solver, supply source, artifact warehouse, and debugging control. They are excluded from the normal application runtime baseline.

## Current structural state

- `main` is the only intended long-lived integration branch.
- The canonical checkout is `$HOME/projects/termux-native-desktop`.
- The checkout is authoring state, not live runtime authority.
- Repository deployment materializes immutable releases under XDG state and activates them through stable `current` and retained `previous` pointers.
- The historical `$HOME/gl/.git` authority is retired and preserved in safety artifacts.
- Mutable Mesa source/build state and versioned providers are separated under XDG state.
- Legacy `$HOME/gl/build` and `$HOME/gl/opt` coordinates are compatibility paths, not canonical ownership.
- VS Code and Obsidian application bodies, selected generations, user data, and provider contents remain outside repository ownership.

## Current research boundary

The provider-authority workstream remains paused:

```text
SUP-02 producer implemented
all 28 issued requests outstanding
no canonical supplier response produced
no build-attestation/adaptation closure accepted
no provider/composition/target-layout completion accepted
```

The project must decide how much assurance is appropriate for reference-consumed, reference-adapted, independently reproduced, and novel paths before additional evidence production resumes.

[`../decisions/0005-proportional-assurance-depth.md`](../decisions/0005-proportional-assurance-depth.md) is a proposed policy only. It has no provider, target-population, or activation effect.

## Documentation authority state

The repository now has a canonical logical documentation model:

```text
current
constitution
architecture
operations
decisions
evidence
history
knowledge
```

- [`../DOCUMENTATION_MODEL.md`](../DOCUMENTATION_MODEL.md) defines authority, lifecycle, conflict handling, and context budgets.
- [`../catalog.tsv`](../catalog.tsv) is the machine-readable catalog of canonical routers and key authority documents.
- Canonical routers exist for constitution, architecture, operations, evidence, and history.
- The large historical corpus has not been physically moved; its current classification is inherited from its directory indexes.
- Narrative handoffs remain historical only.

Default onboarding remains bounded to four files and loads no history.

## Current project phase

The next bounded task is to consolidate the overlapping constitutional surface and decide the proposed assurance-depth policy.

It will:

```text
review ADR 0005 without silently accepting it
consolidate project context, principles, and foundation precedence
separate durable constitution from historical design assessment
prepare any physical moves with automated link migration
keep the provider-authority workstream paused until the policy decision
```

## Current non-goals

Do not currently:

- resume or fulfill additional SUP-02 requests;
- populate a target provider layout;
- activate the selected Obsidian generation;
- redesign the runtime around Docker or a PRoot application baseline;
- reconstruct the repository through raw GitHub connector reads;
- move or rewrite the entire historical corpus;
- treat proposed ADR 0005 as accepted.

## Start and navigation

- Active task: [`ACTIVE_TASK.md`](ACTIVE_TASK.md)
- Machine state: [`STATE.yaml`](STATE.yaml)
- Pending external inputs: [`PENDING_ARTIFACTS.yaml`](PENDING_ARTIFACTS.yaml)
- Documentation authority model: [`../DOCUMENTATION_MODEL.md`](../DOCUMENTATION_MODEL.md)
- Documentation router: [`../INDEX.md`](../INDEX.md)
- Project agent contract: [`../../AGENTS.md`](../../AGENTS.md)
