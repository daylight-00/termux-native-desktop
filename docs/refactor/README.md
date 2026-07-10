# Repository Refactor Work Log

This directory is the low-level source of truth for the repository refactor from the legacy `setup/` layout to explicit ownership, validated migration, and the current semantic hard-refactor direction.

## Working rule

Every structural change must be recorded here before or at the same time as the repository change. Session context is not authoritative.

## Current checkout root

Canonical live-device checkout:

```text
$HOME/projects/termux-native-desktop
```

Legacy checkout root:

```text
$HOME/termux-native-desktop
```

The legacy root is only a migration source identity and must not remain as a compatibility symlink after relocation.

## Current direction and precedence

The ownership migration in `0001` through `0011` remains accepted.

The ABI incident analysis in `0012` and `0013` remains evidence.

`0014` retains useful transaction, validation, candidate, and rollback principles, but its concrete implementation sequence is partially superseded.

Branch-local architecture direction:

```text
0015-architecture-reassessment-and-hard-refactor-direction.md
0016-next-session-handoff.md
```

Full top-down rationale on `main`:

```text
docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
docs/system-foundation/12-document-consistency-audit-and-execution-order.md
```

Precedence:

```text
system-foundation/11 and /12
    -> architecture rationale, consistency, execution order

refactor/0015
    -> branch implementation direction

refactor/0016
    -> handoff into semantic review

refactor/0017-0052
    -> current branch evidence/design records under that direction

refactor/0014
    -> retained transaction/validation insights,
       not the current implementation order
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

These records preserve the initial inventory, ownership map, migration procedure, shell/uv-base adoption, preflight corrections, and completed Phase A/B ownership migration.

### ABI incident and lifecycle reasoning

```text
0012-post-refactor-vscode-libdbus-abi-regression.md
0013-vscode-libdbus-root-cause-confirmed.md
0014-robust-gl-update-and-farm-lifecycle.md
```

`0012` and `0013` preserve the ABI incident and confirmed root cause. `0014` is retained for lifecycle principles only where it does not conflict with the later architecture direction.

### Current architecture direction

```text
0015-architecture-reassessment-and-hard-refactor-direction.md
0016-next-session-handoff.md
```

These define the semantic hard-refactor direction, stop line, and evidence-driven handoff.

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

These establish:

```text
semantic decomposition of the old gl umbrella
real APT/dpkg substrate authority
glibc 2.42 -> 2.43 binary ABI regression evidence
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
0051-implicit-software-intent-zink-llvmpipe-validation-passed.md
0052-glx-map-runtime-anonymous-memory-classification.md
```

The Vulkan records now establish a completed bounded Zink/GLX three-state matrix.

#### Explicit hardware provider + default device intent

```text
provider policy:
    explicit-freedreno

renderer:
    Zink -> Turnip Adreno 730

physical tail:
    provider-store libvulkan_freedreno.so
    -> /dev/kgsl-3d0

result:
    PASS
```

#### Implicit discovery + default device intent

```text
manifest discovery:
    PASS

device-select layer:
    inserted

sole surviving pdev:
    llvmpipe CPU

Zink default CPU-device acceptance:
    FAIL

renderer identity:
    NOT REACHED
```

#### Implicit discovery + explicit software device intent

```text
provider policy:
    implicit-discovery

device-class intent:
    LIBGL_ALWAYS_SOFTWARE=1

renderer:
    zink Vulkan 1.4(llvmpipe ... MESA_LLVMPIPE)

GLX/OpenGL:
    PASS
```

The completed causal matrix is:

```text
explicit-freedreno + default intent
    -> Turnip/KGSL
    -> PASS

implicit-discovery + default intent
    -> llvmpipe discovered
    -> CPU pdev rejected
    -> FAIL

implicit-discovery + software intent
    -> llvmpipe selected
    -> Zink/GLX/OpenGL 4.6
    -> PASS
```

Therefore:

```text
provider discovery/selection policy
    and
consumer device-class intent
```

are independent composition dimensions for the tested Zink/GLX consumer.

The successful hardware graph is:

```text
rootfs GLVND / libGL / libGLX 1.7.0
    -> rootfs Mesa GLX vendor 25.0.7-2
    -> rootfs Gallium/Zink frontend 25.0.7-2
    -> rootfs Mesa device-selection layer 25.0.7-2
    -> prefix Vulkan loader 1.3.301 and support plane
    -> provider-store Turnip/Freedreno 26.1.4 lineage
    -> KGSL device interface
```

The successful software graph shares the application-facing front half and changes the provider tail:

```text
rootfs GLVND / Mesa GLX / Gallium Zink
    -> prefix Vulkan loader/support
    -> rootfs Lavapipe
    -> llvmpipe CPU renderer
```

The software capture also maps `libvulkan_gfxstream.so`, but previous loader diagnostics show it as discovery/loading participation without a surviving physical device. Therefore:

```text
mapped ICD object
    !=
selected rendering provider
```

The explicit-vs-software comparison reported:

```text
explicit-only:
    mesa_shader_cache/index
    provider-store libvulkan_freedreno.so
    /dev/kgsl-3d0

software-control-only:
    rootfs libvulkan_gfxstream.so
    rootfs libvulkan_lvp.so
    /memfd:allocation
```

`0052` corrects enrichment classification for the narrow observed `/memfd:allocation*` pattern so it is represented as runtime anonymous memory rather than unresolved package provenance.

### Supporting records

- `MIGRATION_JOURNAL.md` — chronological commands, commit IDs, validations, incidents, recovery, and deviations.
- `repo-path-map.tsv` — machine-readable path mapping for moved tracked files.

## Refactor branch

```text
refactor/module-package-layout
```

Base commit:

```text
3cf41d6fc47050b06e18e956a23cefe25e4fb82a
```

The system-foundation documentation was added separately on `main` after this branch diverged. Branch-local absence does not make foundation direction irrelevant; histories must be reconciled deliberately.

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

The hold is temporary containment only. The long-term latest-first direction remains a corrected current/newer substrate validated by the same gates.

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

Proven D-Bus selected provider set:

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

For scoped Vulkan composition, the bounded Zink hardware/default, implicit/default, and implicit/software controls are complete. Hardware and software renderer graphs have been captured, enriched, and compared. The remaining immediate evidence correction is device-side re-enrichment of the software evidence root using the committed runtime-anonymous memfd classification.

After that, the next gate is real Electron consumer adapter validation:

```text
1. Obsidian explicit-freedreno adapter control
2. Obsidian implicit-discovery adapter comparison
3. VS Code explicit-freedreno GPU adapter validation
4. VS Code CPU/software-intent behavior check
5. compare consumer-specific policy requirements
6. define minimum graphics composition contract from evidence
```

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
