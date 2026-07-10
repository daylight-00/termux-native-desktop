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

The operational handoff that initiated the semantic review is:

```text
0016-next-session-handoff.md
```

The first post-handoff Stage 2–4 records are:

```text
0017-gl-umbrella-semantic-inventory.md
0018-real-device-glibc-substrate-authority.md
0019-selected-closure-pilot-decision-criteria.md
0020-glibc-242-243-binary-abi-regression.md
```

Full top-down rationale is on `main`:

```text
docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
docs/system-foundation/12-document-consistency-audit-and-execution-order.md
```

Use this precedence where migration tactics conflict:

```text
system-foundation/11 and /12
    -> architecture rationale, consistency, execution order

refactor/0015
    -> branch implementation direction

refactor/0016
    -> handoff into semantic review

refactor/0017-0020
    -> current branch evidence/design records produced under that direction

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

### Semantic review and current evidence

- `0017-gl-umbrella-semantic-inventory.md` — Stage 2 inventory of current `gl` files, environment variables, helpers, actual consumers, minimum scopes, candidate owners, and migration conditions.
- `0018-real-device-glibc-substrate-authority.md` — Stage 3 evidence that the current device substrate is dpkg-owned and APT-supplied, with version availability, transaction history, control-state semantics, rollback limits, and the next non-mutating recovery experiment.
- `0019-selected-closure-pilot-decision-criteria.md` — Stage 4 target choice and acceptance criteria for a bounded D-Bus provider-chain pilot, including world protection, locality, provenance, byte materialization, candidate-selection proof, and decision outcomes.
- `0020-glibc-242-243-binary-abi-regression.md` — exact non-installing A/B evidence that the repository `glibc=2.42` artifact exports `__vsyslog_chk@@GLIBC_2.17` while the active 2.43 libc does not, plus the bounded recovery decision gate.

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

## Current incident state

The current device remains:

```text
BLOCKED_SUBSTRATE
```

because the active glibc 2.43 substrate does not export `__vsyslog_chk@GLIBC_2.17`, while the active Debian-derived `libdbus-1.so.3` requires it.

The current device substrate authority is now established:

```text
dpkg database ownership
    +
Termux APT repository supply
    +
explicit apt/full-upgrade update path
```

Pacman is absent on the device and is not part of the current substrate authority path.

The exact non-installing binary A/B comparison is now complete:

```text
glibc 2.42 artifact:
    __vsyslog_chk@@GLIBC_2.17 PRESENT

glibc 2.43 active libc:
    __vsyslog_chk@@GLIBC_2.17 ABSENT
```

The immediate recovery step is APT transaction simulation for `glibc=2.42`, followed by review of dependency and removal effects before any active mutation.

## Current implementation stop line

Until incident recovery is complete and semantic/pilot evidence justifies physical changes, do not implement:

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
selected-closure pilot work after substrate recovery
```

## Environment limitation

The execution container cannot resolve `github.com`, so a normal network `git clone` is not possible inside this runtime. Repository reads and writes are performed through the authenticated GitHub connector. Local working mirrors under `/mnt/data/` store design documents, generated migration material, candidate files, and validation records used to construct connector-backed Git commits.
