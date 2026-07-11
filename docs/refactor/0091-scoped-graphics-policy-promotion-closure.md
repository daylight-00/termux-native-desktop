# 0091 — Scoped Graphics-Policy Promotion Closure

## Decision

The scoped graphics-policy promotion transaction is closed.

The promoted source contract, live installation, actual renderer path, VS Code GPU/CPU branches, and Obsidian GPU/CPU branches all have authoritative Termux/Android receipts with zero gate failures.

Closure means the following source architecture is accepted as the current project contract:

```text
bionic desktop session
    owns bionic Vulkan provider and bionic Zink session policy

~/gl/env
    sanitizes inherited bionic Vulkan provider policy
    sanitizes inherited Mesa bridge/Gallium policy
    selects no glibc provider
    selects no glibc OpenGL bridge

~/gl/policy/vulkan/freedreno.sh
    selects the exact managed glibc Freedreno ICD pair
    remains source-only and consumer-scoped

gl-run
    owns explicit Freedreno provider selection
    owns MESA_LOADER_DRIVER_OVERRIDE=zink

VS Code / Obsidian GPU branches
    own GL_GPU=1
    own explicit Freedreno provider selection
    own ANGLE Vulkan feature argv
    do not own Zink/Gallium overrides

VS Code / Obsidian CPU branches
    own GL_GPU=0
    retain provider-neutral sanitized baseline
    pass exact --disable-gpu
```

This decision does not close unrelated work such as atomic activation, hardware video decode, native Dawn WebGPU, long-duration application stability, or PyMOL onboarding.

## Promoted runtime source boundary

The expanded pre-deploy and live-installation receipt was captured at:

```text
5ed76ec9c7409a141da02a28b5297b8b71965467
```

A repository comparison from that commit through the closure branch state shows changes only under:

```text
STATUS.md
docs/refactor/
experiments/glibc/vulkan-policy-composition/recipe/
```

No changes occurred under:

```text
modules/
packages/
tests/
tools/
```

Therefore all current workload receipts exercise the same promoted runtime-source transaction validated by the expanded source/live installation gates. Later commits strengthened experiment observability, corrected false-negative assumptions, and added documentation; they did not mutate the promoted runtime composition.

## Evidence matrix

### 1. Expanded pre-deploy source transaction

Canonical record:

```text
docs/refactor/
    0083-expanded-graphics-policy-predeploy-and-live-installation-pass.md
```

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    promoted-graphics-policy-predeploy-20260711-162231
```

Source commit:

```text
5ed76ec9c7409a141da02a28b5297b8b71965467
```

Result:

```text
20 gates PASS
gate_failures=0
```

It proved:

```text
shell syntax
repository graphics-policy scope regression
deploy smoke
deploy dry-run
baseline clears both Vulkan loader variables
baseline clears Mesa bridge/Gallium variables
baseline exports none of those variables
explicit Freedreno profile exports both Vulkan loader variables
gl-run sources the provider profile and owns Zink
VS Code and Obsidian GPU launchers source the provider profile
managed deployment plan contains all required leaves
```

### 2. Expanded live installation

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    live-graphics-policy-installation-20260711-162316
```

Result:

```text
17 gates PASS
gate_failures=0
```

It proved exact live symlink targets for:

```text
$HOME/gl/env
$HOME/gl/policy/vulkan/freedreno.sh
$HOME/gl/bin/gl-run
$HOME/.local/bin/code
$HOME/gl/bin/obsidian
$HOME/gl/bin/obsidian-app
```

It also directly proved:

```text
baseline VK_DRIVER_FILES absent
baseline VK_ICD_FILENAMES absent
baseline MESA_LOADER_DRIVER_OVERRIDE absent
baseline GALLIUM_DRIVER absent
explicit profile exact managed VK pair
explicit profile bridge-neutral
private profile implementation variable not exported
```

### 3. Current-head gl-run renderer

Canonical record:

```text
docs/refactor/
    0084-current-head-gl-run-regression-pass-and-strengthened-vscode-gpu-gate.md
```

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    current-gl-run-renderer-20260711-164455
```

Captured commit:

```text
147c7e2fc9b414a6be5561589293c01820d5f7f6
```

Hostile inherited input:

```text
MESA_LOADER_DRIVER_OVERRIDE=llvmpipe
GALLIUM_DRIVER=llvmpipe
```

Result:

```text
6 gates PASS
gate_failures=0
validation.status=PASS
```

Actual renderer:

```text
zink Vulkan 1.4(Turnip Adreno (TM) 730 (MESA_TURNIP))
OpenGL 4.6 Compatibility Profile Mesa 25.0.7-2
```

ABI evidence:

```text
interpreter=$PREFIX/glibc/lib/ld-linux-aarch64.so.1
direct NEEDED includes libc.so.6 and ld-linux-aarch64.so.1
```

This proves the consumer-owned OpenGL bridge composition:

```text
glibc GLX/OpenGL
    -> Zink
    -> managed Turnip
    -> Adreno 730 / KGSL
```

### 4. Current VS Code GPU branch

Canonical records:

```text
docs/refactor/0085-vscode-child-proc-environ-observability-false-negative.md
docs/refactor/0086-current-vscode-gpu-environment-and-primary-identity-pass.md
```

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    current-vscode-gpu-observability-identity-20260711-171024
```

Captured commit:

```text
bea4062df2e132639ea08c8bb94abc8235fb0a96
```

Result:

```text
44 gates PASS
gate_failures=0
validation.status=PASS
```

It proved:

```text
public launcher identity
hostile bionic Vulkan and llvmpipe policy sanitation
observable GL_GPU=1
exact managed glibc VK pair
no observable Mesa/Gallium bridge leak
ANGLE Vulkan main argv
no exact --disable-gpu
CDP primary FREEDRENO_TURNIP
Adreno 730
ANGLE_VULKAN
GaneshVulkan
vulkan=enabled_on
managed libvulkan_freedreno.so mapping
/dev/kgsl-3d0 mapping
```

The receipt treats empty/near-empty child `/proc/<pid>/environ` as an observability boundary rather than a value mismatch.

### 5. Current VS Code CPU branch

Canonical record:

```text
docs/refactor/
    0087-current-vscode-cpu-policy-and-survival-pass.md
```

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    current-vscode-cpu-policy-20260711-173034
```

Captured commit:

```text
0c6a85235ee9b759addc9963a16060c806277fe3
```

Result:

```text
18 gates PASS
gate_failures=0
validation.status=PASS
```

It proved:

```text
hostile Vulkan/Zink/Gallium policy sanitation
observable GL_GPU=0
no explicit Vulkan provider
no graphics/library overrides
exact --disable-gpu
no GPU-enablement flags
isolated user-data and extensions paths
main/zygote/renderer topology
20-second main survival
```

The internal Chromium GPU helper used:

```text
--use-gl=disabled
```

and the renderer used:

```text
--disable-gpu-compositing
```

This established that CPU policy is an effective-mode contract, not a process-name absence contract.

### 6. Corrected current Obsidian GPU branch

Canonical records:

```text
docs/refactor/0088-obsidian-user-data-authority-and-cdp-path-false-negative.md
docs/refactor/0089-current-obsidian-gpu-environment-and-primary-identity-pass.md
```

Invalid first attempt:

```text
current-obsidian-gpu-environment-identity-20260711-174948
```

The first attempt is preserved as incomplete because Obsidian retained the normal `$HOME/.config/obsidian` authority and the CDP probe waited in the wrong directory.

Canonical corrected evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    corrected-obsidian-gpu-environment-identity-20260711-180746
```

Captured commit:

```text
3384bf136f3f35f7ab1d86b2005c2e7559d7e298
```

Result:

```text
48 gates PASS
gate_failures=0
validation.status=PASS
```

It proved:

```text
separate receipt-local environment and CDP XDG roots
actual <config>/obsidian user-data ownership
normal $HOME/.config/obsidian absent
hostile provider/bridge policy sanitation
full observable main/zygote/GPU/utility/renderer GL_GPU=1 chain
exact managed glibc VK pair throughout the observable tree
ANGLE Vulkan argv
20-second main survival
fresh CDP primary FREEDRENO_TURNIP
Adreno 730
ANGLE_VULKAN
GaneshVulkan
hardwareSupportsVulkan=true
vulkan=enabled_on
WebGL and WebGL2 enabled
managed provider and KGSL mapping
```

### 7. Current Obsidian CPU branch

Canonical record:

```text
docs/refactor/
    0090-current-obsidian-cpu-policy-and-survival-pass.md
```

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    current-obsidian-cpu-policy-20260711-181554
```

Captured commit:

```text
5ab13fd6c2af5843abf7bbff3a8a26f46a8e84b5
```

Result:

```text
21 gates PASS
gate_failures=0
validation.status=PASS
```

It proved:

```text
receipt-local XDG_CONFIG_HOME
actual receipt-local <config>/obsidian user data
normal profile path absent
hostile provider/bridge policy sanitation
full observable GL_GPU=0 chain
no explicit Vulkan provider
no Mesa/Gallium/library override
exact --disable-gpu
no GPU-enablement flags
no observed GPU process
renderer --disable-gpu-compositing
main/zygote/renderer topology
20-second main survival
```

## Final invariant set

The promoted architecture now has the following evidence-backed invariants.

### ABI boundary

```text
bionic process
    never receives glibc LD_LIBRARY_PATH or glibc provider libraries

glibc process
    starts from ~/gl/env
    does not inherit bionic Vulkan provider policy
    does not inherit bionic Mesa bridge/Gallium policy
```

### Baseline sanitation

```text
~/gl/env clears:
    VK_ICD_FILENAMES
    VK_DRIVER_FILES
    MESA_LOADER_DRIVER_OVERRIDE
    GALLIUM_DRIVER
```

The baseline exports none of them and does not choose a graphics provider or bridge.

### Provider ownership

```text
explicit glibc Freedreno provider:
    ~/gl/policy/vulkan/freedreno.sh

provider profile exports together:
    VK_DRIVER_FILES
    VK_ICD_FILENAMES
```

Provider selection is consumer-scoped and never a glibc-world global default.

### Bridge ownership

```text
gl-run:
    owns MESA_LOADER_DRIVER_OVERRIDE=zink

VS Code / Obsidian:
    never add Zink or GALLIUM_DRIVER
```

### Application feature-mode ownership

```text
GL_GPU=1:
    explicit managed Freedreno profile
    ANGLE Vulkan feature argv
    no exact --disable-gpu

GL_GPU=0:
    no explicit provider
    no bridge/Gallium override
    exact --disable-gpu
    no GPU-enablement argv
```

### Selected-device evidence

For GPU branches, a provider mapping alone is insufficient. Canonical acceptance requires:

```text
CDP primary identity
    + feature-mode identity
    + managed provider mapping
    + KGSL device-node mapping
```

Both VS Code and Obsidian satisfy this requirement with:

```text
FREEDRENO_TURNIP
Adreno 730
ANGLE_VULKAN
GaneshVulkan
managed libvulkan_freedreno.so
/dev/kgsl-3d0
```

### Application-state isolation

```text
VS Code validation:
    isolated user-data/extensions paths

Obsidian validation:
    receipt-local XDG_CONFIG_HOME
    actual receipt-local <config>/obsidian directory
```

Normal user state is not part of promotion evidence.

## Revalidation triggers

The closed transaction does not require periodic blind reruns.

Rerun the relevant gate only when its claim surface changes.

### Rerun expanded pre-deploy and live installation when

```text
modules/gl/overlay/home/gl/env changes
freedreno.sh changes
gl-run changes
public application launcher path/target changes
tools/deploy ownership or managed target set changes
```

### Rerun gl-run renderer when

```text
gl-run changes
Freedreno provider profile changes
Mesa glibc prefix or stable symlink changes
glibc core changes
X11/GLX dependency stack changes
```

### Rerun an application GPU gate when

```text
its package launcher changes
Electron/Chromium application version changes
provider profile changes
Mesa/Vulkan loader/provider changes
CDP classifier or correlation logic changes materially
```

### Rerun an application CPU gate when

```text
its package launcher changes
Electron/Chromium application version changes
baseline sanitation changes
user-data authority changes
CPU argv policy changes
```

Experiment-only documentation or unrelated validator additions do not require rerunning previously closed workload gates unless they invalidate the prior evidence interpretation.

## Known non-blocking boundaries

The following remain open but are not part of this transaction:

```text
atomic activation for multi-file live migrations
permanent glibc upgrade lifecycle beyond the current 2.42 hold
hardware video decode
native Dawn WebGPU
complete end-to-end zero-copy presentation
normal-profile and plugin/vault long-duration application behavior
PyMOL end-to-end scientific workload
other inherited Mesa/session variables such as vblank_mode
exact Mesa kgsl-only present-SIGBUS mechanism
```

## Operational consequence

No deployment or desktop restart is required merely to record this closure.

The live promoted runtime leaves were already validated and the closure-period changes after the original source receipt were confined to experiment and documentation ownership.

The next project focus should move away from repeated graphics-policy promotion reruns and toward the remaining repository/module ownership refactor, atomic activation design, and the next scientific workload.

## Final state

```text
expanded pre-deploy:
    PASS

expanded live installation:
    PASS

current gl-run renderer:
    PASS

current VS Code GPU:
    PASS

current VS Code CPU:
    PASS

current Obsidian GPU:
    PASS

current Obsidian CPU:
    PASS

scoped graphics-policy promotion transaction:
    CLOSED
```

## Stop line

Do not:

```text
rerun closed gates without a relevant source/runtime trigger
reopen the transaction for unrelated WebGPU/video/PyMOL work
promote the incomplete first Obsidian attempt
claim zero-copy, video decode, WebGPU, or long-duration stability
replace consumer-scoped policy with a glibc-world global graphics default
remove the bionic/glibc ABI boundary
```
