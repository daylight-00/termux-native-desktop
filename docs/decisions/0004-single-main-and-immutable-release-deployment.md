# Decision 0004: one canonical `main` and immutable repository releases

## Status

Accepted for the repository-consolidation transaction.

## Context

The project accumulated three lines after the original common base:

- `main` carried the top-down knowledge and system-foundation documents;
- `refactor/module-package-layout` carried the ownership refactor and validated runtime work;
- `docs/post-graphics-architecture-audit` continued the refactor line and became the actual integration line despite its documentation-oriented name.

The live Termux deployment also linked public runtime leaves directly into the repository checkout. Therefore a checkout, merge or `git pull` could change live behavior before a complete deployment transaction existed.

## Decision

### Repository branch policy

`main` is the only long-lived integration branch.

Temporary branches remain allowed when they provide a bounded isolation benefit, but they must have:

- one explicit purpose;
- one expected merge target (`main`);
- no unique constitutional document left behind after closure;
- deletion after their tip is verified as an ancestor of `main`.

Milestones and immutable historical boundaries use annotated tags or recorded commit/tree identities, not permanent topic branches.

The system-foundation history and the active refactor/provider-authority history are combined by a two-parent merge. Overlapping top-level status and guide files keep their newer active-line content; `docs/knowledge/` and `docs/system-foundation/` are added intact so the canonical checkout is self-contained.

### Deployment authority

The repository checkout is an authoring source, not the live runtime release.

`tools/deploy` now materializes an immutable release under:

```text
${XDG_STATE_HOME:-$HOME/.local/state}/termux-native-desktop/deployment/releases/<tree>-<profile>/
```

Public managed leaves point through one stable `current` symlink. A future repository change does not affect the live environment until a complete release is materialized and the `current` pointer is switched.

The deployment retains a `previous` pointer and supports pointer rollback.

### Profiles

```text
workstation
    shell/session integration
    glibc runtime adapters and policy leaves
    public application launchers

full
    workstation
    + uv-base configuration
    + glibc target toolchain wrappers
    + Mesa maintenance compatibility leaves
```

This is a physical deployment split, not a claim that all current files have reached final semantic ownership.

### Non-goals of this transaction

This transaction does not automatically delete or reinterpret:

- external application payloads under `$HOME/gl/apps/`;
- selected provider generations under `$HOME/gl/selected/`;
- installed providers and historical Mesa builds under `$HOME/gl/opt/`;
- build worktrees and caches under `$HOME/gl/build/`;
- the historical `$HOME/gl/.git` repository;
- user data and application profiles.

Those objects require separate ownership/evidence decisions. The deployment transaction removes checkout-as-live-authority without guessing about unrelated data.

## Consequences

- `git pull` no longer constitutes runtime activation after migration.
- `main` contains both constitutional design and implementation/evidence history.
- branch deletion can be mechanical after ancestry verification.
- deployment can be checked with `tools/deploy --status` and reverted with `tools/deploy --rollback`.
- the next semantic refactor may operate from one canonical history without preserving obsolete branch identities.
