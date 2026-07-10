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

refactor/0017-0050
    -> current branch evidence/design records produced under that direction

refactor/0014
    -> retained transaction/validation insights,
       not the current next implementation sequence
```

## Document index

### Baseline and ownership migration

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

These records preserve the initial inventory, ownership map, migration procedure, shell/uv-base adoption, real-device preflight corrections, and the completed Phase A/B ownership migration.

### ABI incident and lifecycle reasoning

```text
0012-post-refactor-vscode-libdbus-abi-regression.md
0013-vscode-libdbus-root-cause-confirmed.md
0014-robust-gl-update-and-farm-lifecycle.md
```

`0012` and `0013` preserve the ABI incident evidence and root cause. `0014` retains candidate/validation/promotion and transactional principles but is not the current implementation order.

### Current architecture direction

```text
0015-architecture-reassessment-and-hard-refactor-direction.md
0016-next-session-handoff.md
```

These define the branch-local semantic hard-refactor direction, stop line, and the handoff into evidence-driven semantic review.

### Semantic review, substrate, and selected closure

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
```

These records establish:

```text
semantic decomposition of the old gl umbrella
real APT/dpkg substrate authority
binary glibc 2.42 -> 2.43 ABI regression evidence
package-managed recovery and corrected gates
VS Code CLI/GUI recovery closure
canonical checkout relocation
ownership-aware D-Bus closure selection
materialized selected-provider candidate validation
```

### Obsidian application-domain composition pilot

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

The Obsidian records establish:

```text
real multiprocess topology and survival gates
wall-clock-bounded capture semantics
161-path baseline semantic decomposition with zero review objects
process-class-specific graphics mappings
baseline explicit Freedreno/KGSL participation
strict policy-isolation topology/survival pass
strict alternate provider set:
    SwiftShader root 1
    Lavapipe root + strict-only closure 9
    Gfxstream root 1
zero unresolved or ambiguous mapped-universe SONAME edges
```

### Vulkan policy ownership and scoped composition

```text
0042-vulkan-policy-producer-consumer-inventory.md
0043-scoped-vulkan-policy-composition-experiment.md
0044-self-contained-glx-consumer-probe.md
0045-explicit-freedreno-zink-consumer-validation-passed.md
0046-zink-turnip-mixed-provider-version-signal.md
0047-explicit-zink-turnip-physical-provider-graph.md
0048-zink-frontend-and-cross-version-graphics-composition-confirmed.md
0049-implicit-discovery-zink-consumer-failure.md
0050-implicit-loader-discovery-and-zink-cpu-device-gate.md
```

The current Vulkan composition records establish:

```text
producer/consumer inventory:
    bionic session producer
    glibc shared producer
    gl-run consumer
    VS Code launcher consumer
    Obsidian launcher consumer

policy dimensions:
    provider discovery/selection policy
    application feature/argv mode
    consumer device-class intent

explicit-Freedreno GLX/Zink control:
    PASS
    Zink -> Turnip Adreno 730
    GLX/OpenGL 4.6 context

captured explicit physical graph:
    rootfs GLVND/GLX 1.7.0
    rootfs Mesa GLX vendor 25.0.7-2
    rootfs Gallium/Zink frontend 25.0.7-2
    rootfs Mesa device-selection layer 25.0.7-2
    prefix Vulkan loader 1.3.301 and support libraries
    provider-store Turnip/Freedreno 26.1.4 lineage
    KGSL device interface

implicit-discovery Zink control:
    manifest discovery PASS
    eight rootfs ICD manifests discovered
    Mesa device-select layer inserted
    sole surviving pdev: llvmpipe CPU
    rootfs Freedreno path: zero physical devices
    Zink default CPU-device acceptance: FAIL
    GLX/OpenGL path: FAIL before renderer identity
```

`0050` refines the failure model: implicit discovery did provide a Vulkan CPU physical device, but the tested Zink path did not accept CPU selection without explicit software intent. The next discriminating control changes only `LIBGL_ALWAYS_SOFTWARE=1` while keeping `VULKAN_POLICY_MODE=implicit-discovery`.

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

## Current selected-closure and composition state

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

The proven D-Bus selected provider set is:

```text
libdbus
libsystemd
libcap
```

This validates a materialized selected-provider closure as a real object class, but does not prove a world-global shared-provider boundary.

The active architecture-discrimination work is:

```text
selected Obsidian AppDir composition pilot
    +
scoped Vulkan policy composition experiment
```

For Obsidian, the 161-path baseline and 169-path strict policy-isolation control are semantically classified with zero review objects. The strict-only 11-path set is fully attributed to SwiftShader, Lavapipe, and Gfxstream roots inside the captured mapped universe.

For scoped Vulkan composition, explicit-Freedreno Zink/Turnip validation passed and the successful mixed physical graph is enriched with package/version identity. The implicit control failed, but loader diagnostics now show the exact reason chain:

```text
rootfs manifest discovery
    PASS
        ↓
multiple ICD loading/enumeration attempts
        ↓
sole surviving pdev
    llvmpipe CPU
        ↓
software device-class intent absent
        ↓
Zink rejects CPU pdev in default path
        ↓
GLX screen and FBConfig path fail
```

The active next gate is the one-variable control:

```text
VULKAN_POLICY_MODE=implicit-discovery
LIBGL_ALWAYS_SOFTWARE=1
```

with the same GLX probe and maps capture. If it passes, the resulting software graph will be enriched and compared with the explicit hardware graph before Electron consumer validation.

Candidate materialization remains blocked pending these graphics composition gates plus locality-shadowing and non-graphics static/runtime closure analysis.

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
