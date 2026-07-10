# Repository Refactor Work Log

This directory is the low-level source of truth for the repository refactor from the legacy `setup/` layout to explicit ownership, validated migration, and the current semantic hard-refactor direction.

## Working rule

Every structural change must be recorded here before or at the same time as the repository change. Session context is not authoritative.

## Current checkout root

The canonical live-device checkout is:

```text
$HOME/projects/termux-native-desktop
```

The legacy checkout root:

```text
$HOME/termux-native-desktop
```

is retained only as a migration source identity. It must not remain as a compatibility symlink after relocation.

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

The post-handoff evidence and decision records are:

```text
0017-gl-umbrella-semantic-inventory.md
0018-real-device-glibc-substrate-authority.md
0019-selected-closure-pilot-decision-criteria.md
0020-glibc-242-243-binary-abi-regression.md
0021-glibc-242-downgrade-simulation-passed.md
0022-glibc-242-recovery-and-core-gate-false-negative.md
0023-cli-level-abi-incident-recovery-closed.md
0024-vscode-gui-recovery-validation-passed.md
0025-repository-checkout-relocation-to-projects.md
0026-dbus-pilot-control-static-selection-mismatch.md
0027-dbus-static-runtime-closure-agreement.md
0028-selected-dbus-candidate-validation-passed.md
0029-second-selected-closure-pilot-target.md
0030-obsidian-control-capture-first-timeout.md
0031-obsidian-cpu-topology-and-survival-gate.md
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

refactor/0017-0031
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
- `0018-real-device-glibc-substrate-authority.md` — Stage 3 evidence that the current device substrate is dpkg-owned and APT-supplied, with rollback and update-path facts.
- `0019-selected-closure-pilot-decision-criteria.md` — Stage 4 criteria for a bounded selected-provider pilot.
- `0020-glibc-242-243-binary-abi-regression.md` — exact binary A/B evidence for the missing fortified syslog export.
- `0021-glibc-242-downgrade-simulation-passed.md` — bounded one-package APT downgrade simulation result.
- `0022-glibc-242-recovery-and-core-gate-false-negative.md` — package-managed recovery evidence and test-harness corrections.
- `0023-cli-level-abi-incident-recovery-closed.md` — strict core/provider/VS Code CLI recovery gate closure.
- `0024-vscode-gui-recovery-validation-passed.md` — real GUI workload recovery validation.
- `0025-repository-checkout-relocation-to-projects.md` — canonical checkout move and relocation-safe relinking contract.
- `0026-dbus-pilot-control-static-selection-mismatch.md` — path-based world inference rejected after libcap control/static mismatch.
- `0027-dbus-static-runtime-closure-agreement.md` — ownership-aware static selection matches runtime provider maps.
- `0028-selected-dbus-candidate-validation-passed.md` — concrete three-object provider bytes, receipt/map equality, actual candidate selection, and zero broad-farm/rootfs leakage.
- `0029-second-selected-closure-pilot-target.md` — Obsidian AppDir CPU path selected to test `$ORIGIN` locality and real application-domain composition.
- `0030-obsidian-control-capture-first-timeout.md` — first Obsidian control-capture timeout, harness observability defect, and topology-preserving correction.
- `0031-obsidian-cpu-topology-and-survival-gate.md` — actual CPU-path topology evidence, utility-class requirement correction, descendant-tree discovery, and separate workload survival gate.

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

The system-foundation documentation was added separately on `main` after this branch diverged. The histories must be reconciled deliberately; branch-local absence does not make foundation direction irrelevant.

## Current device and incident state

The tested VS Code workload has recovered through CLI and real GUI validation.

```text
SUBSTRATE_RECOVERED
PROVIDER_RELOCATION_VALID
VS_CODE_GPU_CLI_VALID
VS_CODE_CPU_CLI_VALID
VS_CODE_GUI_WORKLOAD_VALID
ABI_INCIDENT_RECOVERY_COMPLETE_FOR_TESTED_VSCODE_WORKLOAD
```

Containment:

```text
glibc 2.42 installed
exact 2.42 recovery artifact preserved
glibc temporarily held from upgrading to known-broken 2.43
```

The hold is temporary incident containment only. The long-term latest-first direction remains a corrected current/newer substrate validated by the same gates.

## Current selected-closure state

The bounded D-Bus selected-provider pilot is passed for the captured probe.

```text
static/runtime provider-set agreement: PASS
candidate byte materialization: PASS
provenance receipt: PASS
candidate actual-selection proof: PASS
candidate receipt/map equality: PASS
broad-farm provider leakage: ZERO
rootfs provider leakage: ZERO
protected substrate boundary: PASS
```

The proven selected provider set is:

```text
libdbus
libsystemd
libcap
```

This validates a materialized selected-provider closure as a real object class, but does not prove a world-global shared-provider boundary.

The active next experiment is:

```text
selected Obsidian AppDir CPU-path closure pilot
```

Observed CPU topology currently supports `main + renderer + zygote`, with `utility` absent across the captured startup samples. A later `GPU process isn't usable. Goodbye.` fatal requires an explicit survival gate. The current harness follows launch descendants by PPID tree and separates topology from survival before map classification. Candidate materialization for Obsidian remains blocked.

## Current implementation stop line

Do not implement by inertia:

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
graphics-provider actual-selection evidence
read-only inspection
identity capture
regression gates
semantic inventory
contract design
small discriminating experiments
bounded selected-closure pilots
minimum lifecycle work only after the owning semantic object is proven
```

## Environment limitation

The execution container cannot resolve `github.com`, so normal network cloning is not available inside this runtime. Repository reads and writes are performed through the authenticated GitHub connector. Local mirrors under `/mnt/data/` hold design material and generated evidence used to construct connector-backed commits.
