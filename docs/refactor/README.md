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

refactor/0017-0057
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

### ABI incident and lifecycle reasoning

```text
0012-post-refactor-vscode-libdbus-abi-regression.md
0013-vscode-libdbus-root-cause-confirmed.md
0014-robust-gl-update-and-farm-lifecycle.md
```

### Current architecture direction

```text
0015-architecture-reassessment-and-hard-refactor-direction.md
0016-next-session-handoff.md
```

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

The CPU-path Obsidian records establish:

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
0053-obsidian-capture-feature-mode-parameterization.md
0054-obsidian-explicit-freedreno-gpu-adapter-validation-passed.md
0055-obsidian-gpu-policy-control-comparison-harness.md
0056-obsidian-implicit-gpu-control-and-helper-corrections.md
0057-obsidian-same-feature-mode-vulkan-policy-substitution-result.md
```

## Zink/GLX consumer result

The bounded Zink three-state matrix is complete.

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
    !=
consumer device-class intent
```

for the tested Zink consumer.

The explicit hardware graph is:

```text
rootfs GLVND / libGL / libGLX 1.7.0
    -> rootfs Mesa GLX vendor 25.0.7-2
    -> rootfs Gallium/Zink frontend 25.0.7-2
    -> rootfs Mesa device-selection layer 25.0.7-2
    -> prefix Vulkan loader 1.3.301 and support plane
    -> provider-store Turnip/Freedreno 26.1.4 lineage
    -> KGSL device interface
```

The passing software graph shares the application-facing front half and changes the selected provider tail:

```text
rootfs GLVND / Mesa GLX / Gallium Zink
    -> prefix Vulkan loader/support
    -> rootfs Lavapipe
    -> llvmpipe CPU renderer
```

The software capture also maps Gfxstream, but loader diagnostics show discovery/loading participation without a surviving physical device.

Therefore:

```text
mapped ICD object
    !=
selected rendering provider
```

## Obsidian real Electron same-feature-mode policy A/B

Both GPU-path controls keep:

```text
CONTROL_GL_GPU=1
LIBGL_ALWAYS_SOFTWARE unset
same experiment launcher adapter
same capture harness
same 100-second survival budget
```

and change only:

```text
VULKAN_POLICY_MODE=explicit-freedreno
```

versus:

```text
VULKAN_POLICY_MODE=implicit-discovery
```

### Process topology

Both controls end with:

```text
main      1
zygote    2
gpu       1
utility   1
renderer  1
```

Both pass topology and survival gates.

Therefore the policy substitution preserves the captured final process-class topology for these controls.

### Shared captured graphics front half

Both controls share these `gpu` process relations:

```text
gpu -> AppDir libEGL.so
gpu -> AppDir libGLESv2.so
gpu -> AppDir libvulkan.so.1
gpu -> rootfs libVkLayer_MESA_device_select.so
gpu -> rootfs libgbm.so.1.0.0
```

The non-GPU process classes map rootfs GBM in both controls.

This supports a stable captured front half:

```text
Electron gpu process
    -> AppDir EGL/GLES/Vulkan-facing stack
    -> Mesa device-selection layer
    -> GBM infrastructure
```

### Explicit-only graphics tail

```text
gpu -> provider-store libvulkan_freedreno.so
gpu -> /dev/kgsl-3d0
```

### Implicit-only graphics tail

```text
gpu -> rootfs libvulkan_lvp.so
gpu -> rootfs libvulkan_gfxstream.so
```

The implicit control preserves topology and survival without the captured Freedreno/KGSL relation.

This proves alternate ICD mapping participation in the real Electron GPU process.

It does not prove which implicit ICD is the selected renderer.

### Semantic substitution

Policy-significant explicit-only objects:

```text
DEVICE_NODE_GPU
    /dev/kgsl-3d0

PROVIDER_GRAPHICS_VULKAN_DRIVER_ELF
    provider-store libvulkan_freedreno.so
```

Implicit-only graphics roots:

```text
PROVIDER_GRAPHICS_VULKAN_SOFTWARE_LVP_ELF
    rootfs libvulkan_lvp.so

PROVIDER_GRAPHICS_VULKAN_VIRTUAL_GFXSTREAM_ELF
    rootfs libvulkan_gfxstream.so
```

The implicit side also includes the LVP dependency-side additions:

```text
prefix:
    liblzma.so.5.6.4

rootfs:
    libLLVM.so.19.1
    libz3.so.4
    libxml2.so.2.9.14
    libedit.so.2.0.75
    libtinfo.so.6.5
    libbsd.so.0.12.2
    libmd.so.0.1.0
```

This reproduces the earlier LVP closure shape inside a same-feature-mode real Electron GPU-path comparison.

## Evidence hygiene corrections

### Runtime anonymous memory

The narrow observed:

```text
/memfd:allocation*
```

pattern is classified as:

```text
RUNTIME_ANON_MEMORY
RUNTIME_MEMORY
RUNTIME_ANONYMOUS_MAPPING
```

### Mesa shader cache database

The Obsidian classifier previously recognized only:

```text
$HOME/.cache/mesa_shader_cache/
```

and misclassified:

```text
$HOME/.cache/mesa_shader_cache_db/index
```

as review data.

The classifier now recognizes both cache layouts as:

```text
RUNTIME_CACHE_MESA
```

Device-side reclassification of the existing implicit evidence root is the immediate cleanup step.

### Full exact delta versus policy-relevant delta

The policy comparison helper preserves:

```text
full exact semantic delta
```

and separately emits:

```text
policy-relevant semantic delta
```

The filtered view includes:

```text
device nodes
app-local graphics providers
graphics provider classes
prefix ELF provider differences
rootfs ELF provider differences
```

while the full view retains cache/font/data timing differences.

This avoids deleting evidence while preventing volatile runtime data from dominating policy interpretation.

## Architecture conclusion

The current evidence supports:

```text
stable consumer-facing graphics front half
    +
consumer-specific provider-policy composition
    +
policy-dependent provider tail
```

The provider tail is not one immutable global Mesa object.

Cross-consumer behavior differs:

```text
standalone Zink:
    implicit/default -> FAIL

Obsidian Electron GPU path:
    implicit/default -> topology/survival PASS
    alternate ICDs mapped by gpu process
```

Therefore graphics provider policy must remain consumer-aware.

Do not generalize one consumer's valid policy to every glibc graphics consumer merely because they share Vulkan-related libraries.

## Current unresolved questions

The current evidence does not establish:

```text
which implicit ICD is the selected Electron renderer
whether LVP or Gfxstream submits rendering work
whether rendered output correctness is equivalent across policies
whether Electron internally falls back among multiple graphics backends
whether the implicit provider tail should be one closure or multiple discovery candidates
```

Map presence alone cannot answer these questions.

## Refactor branch

```text
refactor/module-package-layout
```

Base commit:

```text
3cf41d6fc47050b06e18e956a23cefe25e4fb82a
```

The system-foundation documentation was added separately on `main` after this branch diverged. Branch-local absence does not make foundation direction irrelevant; histories must be reconciled deliberately.

## Current device and ABI incident state

The tested VS Code workload recovered through CLI and real GUI validation.

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

The Obsidian same-feature-mode explicit-versus-implicit GPU policy A/B is now complete at topology, survival, semantic-set, and process-class mapping levels.

The immediate next evidence sequence is:

```text
1. reclassify implicit Obsidian evidence with shader_cache_db correction
2. rerun refined full/policy-relevant Obsidian comparison
3. decide whether a bounded Electron actual-selection probe is feasible
4. VS Code explicit-freedreno GPU adapter validation
5. VS Code CPU/software-intent behavior check
6. compare consumer-specific policy requirements
7. define minimum graphics composition contract from evidence
8. only then resume locality-shadowing and non-graphics static/runtime closure analysis
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
