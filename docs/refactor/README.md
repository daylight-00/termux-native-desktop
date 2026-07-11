# Repository Refactor Work Log

This directory is the transaction-level source of truth for the migration from the legacy `setup/` layout toward explicit ownership, semantic composition, immutable selected providers, controlled activation, and clean-state reconstruction.

## Working rule

Every structural or architectural change is recorded here before or with the repository change.

```text
session narrative
    != authority

repository evidence + current canonical index
    = authority
```

Historical records remain intact when later evidence supersedes their interpretation or implementation.

## Current checkout root

```text
$HOME/projects/termux-native-desktop
```

The historical `$HOME/termux-native-desktop` path is evidence only and must not return as a compatibility identity.

## Current authority and precedence

Top-down foundation on `main`:

```text
docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
docs/system-foundation/12-document-consistency-audit-and-execution-order.md
```

Current branch-local authority:

```text
0113-clean-state-minimum-condition-and-supply-authority-audit.md
    -> clean-state definition, minimum sufficient conditions, supply authority,
       font/rootfs cleanup order, identity separation, and next-phase gates

0112-selected-obsidian-passive-map-selection-diagnostic-pass-and-contract-decision.md
    -> passive runtime/map facts, no-patch decision, corrected map classes,
       and provisional successor-generation baseline

0110-selected-obsidian-pixbuf-inventory-pass-and-interaction-boundary-correction.md
    -> passive versus interactive claim split and GTK capability inventory

0106-selected-obsidian-phase-b9-generation-materialization-pass.md
    -> first immutable selected CPU generation and publication receipt

0092-post-graphics-closure-architecture-midpoint-audit.md
0093-post-audit-direction-validator-lifecycle-and-selected-closure-reentry.md
    -> top-down direction, validator lifecycle, and parent-pilot continuation

0091-scoped-graphics-policy-promotion-closure.md
    -> closed graphics-policy transaction

0015-0019
    -> semantic hard-refactor, substrate authority, and selected-closure criteria
```

Precedence:

```text
system-foundation/11 and /12
    -> project essence and invariant authority

0113
    -> current clean-state and supply-layer pressure

0112 / 0110 / 0106
    -> current selected-Obsidian evidence and accepted bounded decisions

0092 / 0093
    -> post-graphics architecture direction

0091
    -> closed graphics contract

0015-0019
    -> semantic foundations

other numbered records
    -> chronological evidence and transaction history

0014
    -> retained candidate/validation/rollback principles only;
       concrete broad-farm/pacman/gl-run lifecycle sequence is superseded
```

## Current state

```text
ownership migration:
    DEPLOYED

scoped graphics-policy promotion:
    CLOSED

selected D-Bus provider pilot:
    PASS

selected Obsidian parent pilot:
    ACTIVE / INCOMPLETE

selected Obsidian phases B1-B8:
    CLOSED

first immutable selected CPU generation:
    PUBLISHED / UNACTIVATED

passive explicit-generation startup/topology/100-second survival/maps:
    PASS

passive map-selection diagnosis:
    PASS

CPU map contract:
    DECIDED, with Xau/Xdmcp semantic class name still provisional

interactive vault-open GTK capability:
    OPEN

clean-state supply authority:
    OPEN / IMMEDIATE AUDIT GATE

rootfs font/package cleanup:
    BLOCKED until supply inventory and locked inputs exist

atomic current activation:
    NOT STARTED

glibc corrected/newer substrate lifecycle:
    OPEN

PyMOL runtime implementation:
    DEFERRED
```

## Document index

### 0001–0011 — source ownership migration

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

### 0012–0014 — ABI incident and superseded lifecycle proposal

```text
0012-post-refactor-vscode-libdbus-abi-regression.md
0013-vscode-libdbus-root-cause-confirmed.md
0014-robust-gl-update-and-farm-lifecycle.md
```

The incident proves substrate/provider incompatibility is independent of application and farm regeneration.

### 0015–0019 — semantic architecture reassessment

```text
0015-architecture-reassessment-and-hard-refactor-direction.md
0016-next-session-handoff.md
0017-gl-umbrella-semantic-inventory.md
0018-real-device-glibc-substrate-authority.md
0019-selected-closure-pilot-decision-criteria.md
```

### 0020–0025 — glibc recovery and checkout relocation

```text
0020-glibc-242-243-binary-abi-regression.md
0021-glibc-242-downgrade-simulation-passed.md
0022-glibc-242-recovery-and-core-gate-false-negative.md
0023-cli-level-abi-incident-recovery-closed.md
0024-vscode-gui-recovery-validation-passed.md
0025-repository-checkout-relocation-to-projects.md
```

### 0026–0028 — selected D-Bus provider candidate

```text
0026-dbus-pilot-control-static-selection-mismatch.md
0027-dbus-static-runtime-closure-agreement.md
0028-selected-dbus-candidate-validation-passed.md
```

This proves materialized selected provider bytes, provenance, candidate-specific selection, protected-world separation, and zero broad-farm leakage for a bounded probe.

### 0029–0041 — Obsidian control and semantic decomposition

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

### 0042–0060 — graphics policy discrimination

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

### 0061–0075 — VS Code causality and selected-device proof

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

### 0076–0091 — scoped graphics promotion and closure

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

### 0092–0093 — post-closure audit and re-entry

```text
0092-post-graphics-closure-architecture-midpoint-audit.md
0093-post-audit-direction-validator-lifecycle-and-selected-closure-reentry.md
```

### 0094–0103 — selected-Obsidian semantic closure and generation design

```text
0094-selected-obsidian-phase-b1-retained-control-locality-pass.md
0095-selected-obsidian-phase-b2-static-runtime-closure-pass.md
0096-selected-obsidian-phase-b3-first-run-script-failure.md
0097-selected-obsidian-phase-b3-capability-grouping-pass.md
0098-selected-obsidian-phase-b4-entrypoint-static-matrix-pass.md
0099-selected-obsidian-phase-b5-data-provenance-review.md
0100-selected-obsidian-phase-b6-source-manifest-gap.md
0101-selected-obsidian-phase-b6-corrected-schema-reproduction-pass.md
0102-selected-obsidian-phase-b7-complete-cpu-manifest-pass.md
0103-selected-obsidian-phase-b8-generation-layout-preflight-pass.md
```

This chain establishes:

```text
app-local locality preservation
complete static/dynamic/data accounting
four provisional selected font identities
37-source reproducible GSettings aggregate
complete CPU semantic manifest
content-addressed immutable generation design
explicit validation-before-activation contract
```

### 0104–0106 — generation materialization failures and pass

```text
0104-selected-obsidian-phase-b9-first-run-hardlink-publication-failure.md
0105-selected-obsidian-phase-b9-generation-directory-publication-failure.md
0106-selected-obsidian-phase-b9-generation-materialization-pass.md
```

The final result is one published but unactivated immutable generation with 96 content identities and 175 aliases.

### 0107–0112 — explicit runtime validation and map-contract correction

```text
0107-selected-obsidian-phase-b10-first-run-launcher-environment-failure.md
0108-selected-obsidian-phase-b10-second-run-short-lived-main-diagnostic.md
0109-selected-obsidian-phase-b10-short-runtime-topology-pass-gtk-pixbuf-survival-failure.md
0110-selected-obsidian-pixbuf-inventory-pass-and-interaction-boundary-correction.md
0111-selected-obsidian-passive-b10-survival-pass-map-selection-failure.md
0112-selected-obsidian-passive-map-selection-diagnostic-pass-and-contract-decision.md
```

This chain establishes:

```text
exec-only candidate loader injection
short receipt-owned Chromium socket/runtime path
passive topology and 100-second survival
zero broad-farm/rootfs/current mappings
class-based map acceptance
Xau/Xdmcp exact RPATH-driven world substitution
interactive GTK pixbuf/icon/MIME gap
```

### 0113 — clean-state and supply-layer audit

```text
0113-clean-state-minimum-condition-and-supply-authority-audit.md
```

This audit adds the missing final-system criterion:

```text
minimum sufficient clean conditions
    >
minimum change to accumulated live state
```

It identifies:

```text
installed rootfs path dependence in materialization
unknown rootfs base/manual package delta
provisional rather than proven-minimum font set
conflated generation identity axes
generation-scoped rather than domain-wide rollback
Xau/Xdmcp ownership-name overclaim
coarse-versus-final pixbuf capability distinction
experiment-tool versus final-tool boundary
```

## Immediate execution order

```text
C0. read-only rootfs supply/package mutation inventory;
C1. controlled relocated-cache vault-open diagnostic, no installs;
C2. minimum pixbuf/icon/MIME and font capability derivation;
C3. lock supply artifacts and separate causal identities;
C4. build one unified immutable successor generation;
C5. passive + interactive + warehouse-independence acceptance;
C6. atomic activation and generation-scoped rollback;
C7. remove/recreate accidental rootfs delta and repeat acceptance;
C8. preserve bootstrap inputs for the later full Termux reset rehearsal.
```

## Current stop lines

Do not:

```text
rerun closed graphics gates without a trigger;
purge rootfs font packages before the supply/mutation inventory;
install another package to make the pixbuf path pass;
expand gl-run into lifecycle authority;
make the broad farm the production target;
mutate the existing immutable generation;
patch RPATH for Xau/Xdmcp;
call prefix selection proof of semantic substrate ownership;
copy all pixbuf/icon/MIME inventory paths wholesale;
retain or remove fonts solely from one observed map set;
activate current before clean supply and composition identities close;
use phase-specific counts or wrappers as final operational architecture;
reset Termux before all external inputs and clean bootstrap contracts are preserved;
implement garbage collection.
```

## Evidence handoff

Every evidence-producing stage uses a unique stage-specific output root and archive name.

```bash
tar czf ~/Downloads/$out.tgz $OUT
```

Generic archive names are rejected because they erase stage identity.

## Refactor lineage

```text
original refactor branch:
    refactor/module-package-layout

base:
    3cf41d6fc47050b06e18e956a23cefe25e4fb82a

post-graphics audit base:
    07b2f9a6f8f985fb3f152abd77c0ad3f04237cc9

selected-Obsidian state audited by 0113:
    6c00ac7f9ca46bc2159c51689904e154146f0d2a

clean-state audit branch:
    docs/clean-state-minimum-condition-audit
```

The foundation documents exist on `main`; branch-local absence never makes them irrelevant. Histories must be reconciled deliberately before final integration.
