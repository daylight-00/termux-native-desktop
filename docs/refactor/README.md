# Repository Refactor Work Log

This directory is the transaction-level source of truth for the repository refactor from the legacy `setup/` layout to explicit ownership, semantic decomposition, selected-provider experiments, and validated runtime promotion.

## Working rule

Every structural or architectural change must be recorded here before or at the same time as the repository change.

```text
session context
    != authority

repository evidence and current index
    = authority
```

Historical records are preserved even when their implementation direction is later superseded.

## Current checkout root

Canonical live-device checkout:

```text
$HOME/projects/termux-native-desktop
```

The legacy root:

```text
$HOME/termux-native-desktop
```

is only a historical migration identity and must not be reintroduced as a compatibility symlink.

## Current direction and precedence

The ownership migration in `0001` through `0011` remains accepted.

The ABI incident analysis in `0012` and `0013` remains evidence.

`0014` retains useful candidate, validation, receipt, promotion, and rollback reasoning, but its concrete pacman-hook/broad-farm/gl-run lifecycle sequence is superseded.

Top-down authority on `main`:

```text
docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
docs/system-foundation/12-document-consistency-audit-and-execution-order.md
```

Branch-local architecture direction:

```text
0015-architecture-reassessment-and-hard-refactor-direction.md
0016-next-session-handoff.md
0017-gl-umbrella-semantic-inventory.md
0018-real-device-glibc-substrate-authority.md
0019-selected-closure-pilot-decision-criteria.md
0092-post-graphics-closure-architecture-midpoint-audit.md
```

Current precedence:

```text
system-foundation/11 and /12
    -> project essence, invariants, object model, execution-order authority

refactor/0092
    -> post-graphics-closure architecture audit and next-phase pressure

refactor/0091
    -> closed graphics-policy transaction and evidence-backed contract

refactor/0015-0019
    -> branch semantic direction, substrate authority, and pilot criteria

other numbered records
    -> evidence and transaction history in chronological order

refactor/0014
    -> retained transaction insights only
```

## Current state

```text
ownership migration:
    accepted and deployed

glibc 2.42/2.43 ABI incident:
    recovered for tested workload
    2.42 hold remains temporary containment

bounded D-Bus selected-provider pilot:
    PASS

selected Obsidian application-domain closure pilot:
    ACTIVE / INCOMPLETE
    control and semantic/graphics decomposition advanced
    candidate materialization and locality-preserving equivalence not closed

scoped graphics-policy promotion:
    CLOSED

atomic activation:
    OPEN

remaining gl semantic ownership split:
    OPEN

corrected/newer glibc substrate lifecycle:
    OPEN

PyMOL implementation:
    DEFERRED pending reusable-object decisions
```

## Document index

### 0001–0011 — baseline and ownership migration

```text
0001-current-state-inventory.md
0002-ownership-map.md
0003-migration-plan.md
0004-shell-uv-base-adoption.md
0005-device-preflight-test-failures.md
0006-second-device-preflight-findings.md
0007-third-device-preflight-deploy-return-status.md
0008-pre-apply-gate-passed.md
0009-phase-a-user-env-adoption-passed.md
0010-phase-b-runtime-deploy-plan.md
0011-phase-b-runtime-deploy-passed.md
```

These establish the move from the legacy `setup/` tree into explicit module, package, experiment, and tool ownership.

### 0012–0014 — ABI incident and first lifecycle proposal

```text
0012-post-refactor-vscode-libdbus-abi-regression.md
0013-vscode-libdbus-root-cause-confirmed.md
0014-robust-gl-update-and-farm-lifecycle.md
```

The incident proves substrate/provider incompatibility can exist independently of application code and farm generation.

### 0015–0019 — architecture reassessment and semantic direction

```text
0015-architecture-reassessment-and-hard-refactor-direction.md
0016-next-session-handoff.md
0017-gl-umbrella-semantic-inventory.md
0018-real-device-glibc-substrate-authority.md
0019-selected-closure-pilot-decision-criteria.md
```

These reject accidental preservation of `modules/gl`, `gl-run`, the broad farm, or one package-manager integration as architecture.

### 0020–0025 — substrate recovery and repository relocation

```text
0020-glibc-242-243-binary-abi-regression.md
0021-glibc-242-downgrade-simulation-passed.md
0022-glibc-242-recovery-and-core-gate-false-negative.md
0023-cli-level-abi-incident-recovery-closed.md
0024-vscode-gui-recovery-validation-passed.md
0025-repository-checkout-relocation-to-projects.md
```

These establish the real APT/dpkg substrate authority, glibc 2.42/2.43 binary regression, package-managed recovery, corrected gates, and canonical checkout path.

### 0026–0028 — first bounded selected-provider closure

```text
0026-dbus-pilot-control-static-selection-mismatch.md
0027-dbus-static-runtime-closure-agreement.md
0028-selected-dbus-candidate-validation-passed.md
```

The D-Bus pilot proves a selected materialized provider object with actual bytes, provenance, candidate-specific selection proof, protected substrate boundary, and no broad-farm/rootfs provider leakage.

It does not prove one world-global shared-provider boundary.

### 0029–0041 — Obsidian application-domain closure control and semantic decomposition

```text
0029-second-selected-closure-pilot-target.md
0030-obsidian-control-capture-first-timeout.md
0031-obsidian-cpu-topology-and-survival-gate.md
0032-obsidian-control-wall-clock-gate-timing.md
0033-obsidian-control-maps-captured-provenance-split.md
0034-obsidian-control-semantic-decomposition.md
0035-obsidian-semantic-classifier-awk-portability-fix.md
0036-obsidian-graphics-provider-and-device-node-boundary.md
0037-obsidian-graphics-process-class-mapping.md
0038-obsidian-cpu-control-vulkan-policy-leak-hypothesis.md
0039-obsidian-strict-cpu-vulkan-policy-ab-result.md
0040-obsidian-explicit-freedreno-vs-implicit-fallback-provider-set.md
0041-obsidian-fallback-provider-closure-attribution.md
```

This chain establishes a real multiprocess application-domain composition with:

```text
app-local ELF/data
world substrate
prefix providers
rootfs ELF providers
font/locale/schema data
mutable state/cache
graphics provider/device relations
```

The parent selected-closure pilot remains incomplete until locality-shadowing, non-graphics closure agreement, candidate materialization, actual candidate selection, and control/candidate equivalence are closed or intentionally terminated.

### 0042–0060 — graphics-policy architecture discrimination

```text
0042-vulkan-policy-producer-consumer-inventory.md
0043-scoped-vulkan-policy-composition-experiment.md
0044-self-contained-glx-consumer-probe.md
0045-explicit-freedreno-zink-consumer-validation-passed.md
0046-zink-turnip-mixed-provider-version-signal.md
0047-explicit-zink-turnip-physical-provider-graph.md
0048-zink-frontend-and-cross-version-graphics-composition-confirmed.md
0049-implicit-discovery-zink-consumer-failure.md
0050-implicit-loader-discovery-diagnostics.md
0050-implicit-loader-discovery-and-zink-cpu-device-gate.md
0051-implicit-software-intent-zink-llvmpipe-validation-passed.md
0052-glx-map-runtime-anonymous-memory-classification.md
0053-obsidian-capture-feature-mode-parameterization.md
0054-obsidian-explicit-freedreno-gpu-adapter-validation-passed.md
0055-obsidian-gpu-policy-control-comparison-harness.md
0056-obsidian-implicit-gpu-control-and-helper-corrections.md
0057-obsidian-same-feature-mode-vulkan-policy-substitution-result.md
0058-obsidian-policy-ab-evidence-hygiene-closed.md
0059-bounded-obsidian-implicit-loader-selection-debug-plan.md
0060-obsidian-implicit-loader-selected-lvp-llvmpipe.md
```

This chain separates:

```text
application feature mode
provider discovery/selection
device-class intent
consumer suitability
mapped provider participation
actual selected device/provider
```

It also establishes that graphics policy must remain consumer-aware.

### 0061–0075 — VS Code consumer causality and selected-device evidence

```text
0061-vscode-explicit-gpu-policy-consumer-validation-plan.md
0062-next-session-handoff-vscode-control-and-collaboration-workflow.md
0063-vscode-cli-wrapper-process-handoff-diagnosis.md
0064-vscode-process-handoff-proven-and-causal-main-adoption.md
0065-vscode-explicit-freedreno-repaired-control-workload-gates-passed.md
0066-vscode-explicit-gpu-mapping-pass-and-loader-observer-stream-fix.md
0067-vscode-explicit-loader-log-absence-and-app-local-loader-identity-probe.md
0068-vscode-vendor-loader-identity-and-gpu-observer-contract-gate.md
0069-vscode-gpu-env-and-stdio-boundary-observed.md
0070-vscode-policy-environment-child-launch-boundary-proven.md
0071-vscode-provider-policy-behavioral-causality-proven.md
0072-vscode-policy-comparison-receipt-pass-and-cdp-gpu-identity-plan.md
0073-vscode-implicit-primary-gpu-lvp-selected.md
0074-vscode-explicit-turnip-and-implicit-llvmpipe-primary-device-ab.md
0075-vscode-primary-device-receipt-pass-and-policy-ownership-audit.md
```

This chain proves the difference between policy propagation, mapped providers, and primary selected GPU identity for a real Electron consumer.

### 0076–0091 — scoped policy promotion and closure

```text
0076-scoped-vulkan-policy-promotion-candidate.md
0077-predeploy-pass-and-symlink-activation-gap.md
0078-live-installation-pass-and-promoted-workload-gates.md
0079-promoted-gl-run-validator-prerequisite-and-parser-false-negatives.md
0080-promoted-gl-run-zink-turnip-renderer-pass.md
0081-promoted-vscode-turnip-primary-identity-pass-and-cpu-policy-gate.md
0082-bionic-zink-policy-leak-and-glibc-boundary-correction.md
0083-expanded-graphics-policy-predeploy-and-live-installation-pass.md
0084-current-head-gl-run-regression-pass-and-strengthened-vscode-gpu-gate.md
0085-vscode-child-proc-environ-observability-false-negative.md
0086-current-vscode-gpu-environment-and-primary-identity-pass.md
0087-current-vscode-cpu-policy-and-survival-pass.md
0088-obsidian-user-data-authority-and-cdp-path-false-negative.md
0089-current-obsidian-gpu-environment-and-primary-identity-pass.md
0090-current-obsidian-cpu-policy-and-survival-pass.md
0091-scoped-graphics-policy-promotion-closure.md
```

The transaction is closed.

Accepted semantic contract:

```text
world-boundary graphics sanitation
consumer-scoped provider selection
consumer-owned bridge selection
application-owned GPU/CPU feature mode
isolated application-state authority
selected-device correlation
claim-triggered revalidation
```

Current paths and command names are implementations, not permanent invariants.

### 0092 — post-closure architecture audit

```text
0092-post-graphics-closure-architecture-midpoint-audit.md
```

This audit identifies the next top-down pressure:

```text
resume or terminate the parent Obsidian selected-closure pilot
separate semantic invariants from current adapters
complete gl umbrella ownership split
define atomic activation before another multi-file migration
scope Electron/security and other global policies
establish glibc upgrade/recovery lifecycle
synchronize canonical documentation
use PyMOL only after reusable objects are decided
```

## Current stop lines

Do not:

```text
rerun closed graphics gates without a documented trigger;
expand gl-run into lifecycle authority;
make the broad farm the production target by inertia;
add package-manager hooks before substrate lifecycle ownership is settled;
add more global policy to gl/env because it is convenient;
start PyMOL by copying Electron launcher patterns;
skip the unfinished Obsidian selected-closure question;
apply another multi-file runtime migration before activation semantics are defined;
keep every experiment helper as a permanent active gate.
```

## Current next-phase order

```text
1. synchronize documentation/control-plane state;
2. classify semantic invariants versus current adapters;
3. classify active contract gates versus historical diagnostics;
4. resume or explicitly terminate selected-obsidian-closure;
5. decide semantic provider/bridge/family/application ownership;
6. define minimum atomic activation boundary;
7. apply bounded ownership moves, beginning with high-risk global policies;
8. define corrected/newer glibc substrate acceptance and rollback;
9. use PyMOL as a proof of the resulting architecture.
```

## Refactor lineage

Original refactor branch:

```text
refactor/module-package-layout
```

Base commit:

```text
3cf41d6fc47050b06e18e956a23cefe25e4fb82a
```

Audited post-graphics-closure commit:

```text
07b2f9a6f8f985fb3f152abd77c0ad3f04237cc9
```

The system-foundation documentation was added on `main` after the refactor branch diverged. Branch-local absence never makes foundation direction irrelevant; histories must be reconciled deliberately before final integration.
