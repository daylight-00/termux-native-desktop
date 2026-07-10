# Repository Refactor Work Log

This directory is the low-level source of truth for the repository refactor from the legacy `setup/` layout to explicit ownership, validated migration, and the current semantic hard-refactor direction.

## Working rule

Every structural change must be recorded here before or at the same time as the repository change. Session context is not authoritative.

## Current direction and precedence

The ownership migration in `0001` through `0011` remains accepted.

The ABI incident analysis in `0012` and `0013` remains evidence.

`0014` contains valuable transactional principles, but its concrete implementation sequence is partially superseded by:

```text
0015-architecture-reassessment-and-hard-refactor-direction.md
```

The operational entrypoint for the next session is:

```text
0016-next-session-handoff.md
```

Full top-down rationale is on `main`:

```text
docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
```

Use this precedence where migration tactics conflict:

```text
system-foundation/11
    -> architecture rationale

refactor/0015
    -> branch implementation direction

refactor/0016
    -> next-session operational entrypoint

refactor/0014
    -> retained transaction/validation insights,
       not the current next implementation sequence
```

## Documents

### Baseline and ownership migration

- `0001-current-state-inventory.md` — observed repository and live-system state before migration.
- `0002-ownership-map.md` — old path, new owner, new path, live target, and migration method.
- `0003-migration-plan.md` — ordered repository and live migration procedure.
- `0004-shell-uv-base-adoption.md` — exact legacy identities, new shell/uv-base ownership, hash-guarded adoption, and non-actions.
- `0005-device-preflight-test-failures.md` — first real-device preflight test failures and test-isolation corrections.
- `0006-second-device-preflight-findings.md` — second device preflight observations and corrections.
- `0007-third-device-preflight-deploy-return-status.md` — deploy return-status fault and repair.
- `0008-pre-apply-gate-passed.md` — repository/device pre-apply validation gate result.
- `0009-phase-a-user-env-adoption-passed.md` — live shell and uv-base adoption result.
- `0010-phase-b-runtime-deploy-plan.md` — scoped runtime-facing topology migration plan.
- `0011-phase-b-runtime-deploy-passed.md` — real-device ownership/deployment migration result.

### ABI incident and lifecycle reasoning

- `0012-post-refactor-vscode-libdbus-abi-regression.md` — workload failure capture and hypothesis separation.
- `0013-vscode-libdbus-root-cause-confirmed.md` — independent core/provider ABI root-cause confirmation and regression gates.
- `0014-robust-gl-update-and-farm-lifecycle.md` — candidate/validation/promotion principles and an earlier concrete lifecycle proposal; partially superseded for implementation order.

### Current architecture direction

- `0015-architecture-reassessment-and-hard-refactor-direction.md` — branch-specific semantic hard-refactor decision, `gl` umbrella critique, farm status, substrate authority, and stop line.
- `0016-next-session-handoff.md` — mandatory reading order, allowed/blocked work, incident context, and expected next-session outputs.

### Supporting records

- `MIGRATION_JOURNAL.md` — chronological execution log with commands, commit IDs, validation, incidents, recovery, and deviations.
- `repo-path-map.tsv` — machine-readable path mapping for moved tracked files.

## Refactor branch

```text
refactor/module-package-layout
```

Base commit:

```text
3cf41d6fc47050b06e18e956a23cefe25e4fb82a
```

The system-foundation documentation was added separately on `main` after this branch diverged. The histories must be reconciled deliberately; do not assume branch-local absence means architectural irrelevance.

## Current implementation stop line

Until semantic inventory and substrate-authority evidence are complete, do not implement:

```text
gl-sync
gl-status
gl-run auto-sync
pacman hooks as lifecycle authority
single global compatibility fingerprint
generational broad-farm activation
new global gl environment policy
```

Allowed work includes:

```text
read-only inspection
identity capture
incident recovery
regression gates
semantic inventory
contract design
small discriminating experiments
```

## Environment limitation

The execution container cannot resolve `github.com`, so a normal network `git clone` is not possible inside this runtime. Repository reads and writes are performed through the authenticated GitHub connector. Local working mirrors under `/mnt/data/` store design documents, generated migration material, candidate files, and validation records used to construct connector-backed Git commits.
