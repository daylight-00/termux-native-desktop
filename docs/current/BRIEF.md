# Current project brief

> Semantic state version: `2026-07-15.06`
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

The provider-authority corpus is now classified under accepted ADR 0005.

```text
28 roots
37 reviewed objects
89 separated claims
36 Class A
49 Class B
 1 conditional Class C
 3 Class D
```

The 28 historical SUP-02 requests are classified as:

```text
still necessary now: 0
narrowed:            14
replaced:             7
unnecessary:          7
```

This classification does not accept provider authority. Exact artifact/member identity, adaptation semantics, provider selection, composition, target population, and activation remain separate states. The current review surface is [`../evidence/provider-claim-classification.md`](../evidence/provider-claim-classification.md).

## Documentation and web-session state

- New web-chat sessions receive a user-created full Git bundle and start at `START_HERE.md`.
- `docs/current/` owns current semantic state, the active task, and pending external artifacts.
- [`../DOCUMENTATION_MODEL.md`](../DOCUMENTATION_MODEL.md) defines authority and lifecycle by question.
- [`../catalog.tsv`](../catalog.tsv) is the machine-readable document catalog.
- Default onboarding is exactly four files and loads no history.
- Narrative handoffs, numbered refactor records, experiment reports, and system-foundation documents are not default onboarding authority.
- GitHub connector use is limited to lightweight remote inspection; it is not clone/commit/push transport.
- [`../operations/README.md`](../operations/README.md) is the single current surface for collaboration, bundle transport, execution transactions, result review, checkpoints, troubleshooting, and platform capabilities.
- The former `docs/session-operations/` surface and narrative handoffs are historical only.
- Google Drive is the normal exchange path for bundles, patches, runners, results, logs, and safety artifacts.

## Current project phase

The active task is `review-no-token-reference-consumed-roots`.

It reviews seven roots whose earlier collector found no explicit adaptation token:

```text
libepoxy
libtasn1
libxcomposite
libxfixes
libxi
libxinerama
pango
```

The exact pinned recipe and upstream baseline must confirm Class A or identify the exact Class B changed boundary. No external evidence request, provider promotion, target population, or activation is allowed in this phase.

## Current non-goals

Do not currently:

- issue or fulfill a SUP-02 request without a recorded Class C reclassification or escalation trigger;
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
