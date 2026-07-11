# 0086 — Current VS Code GPU Environment and Primary Identity PASS

## Status

The corrected strengthened promoted VS Code GPU validator passed on the real Termux/Android device.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    current-vscode-gpu-observability-identity-20260711-171024
```

Captured repository state:

```text
branch:
    refactor/module-package-layout

head:
    bea4062df2e132639ea08c8bb94abc8235fb0a96
```

Receipt:

```text
gate_failures=0
validation.status=PASS
```

All 44 validator gates passed.

This is the canonical post-sanitation current-source VS Code GPU receipt.

The earlier failed strengthened receipt remains preserved as an observability-model false negative documented in `0085`.

## Public launch authority

Observed launcher:

```text
$HOME/.local/bin/code
```

Exact target:

```text
$HOME/projects/termux-native-desktop/
    packages/vscode/launcher/code
```

The receipt therefore validates the promoted package-owned public entry point.

## Deliberate hostile-policy input

The environment phase injected:

```text
VK_DRIVER_FILES=/bionic/freedreno.json
VK_ICD_FILENAMES=/bionic/freedreno.json
MESA_LOADER_DRIVER_OVERRIDE=llvmpipe
GALLIUM_DRIVER=llvmpipe
```

The purpose was not to create a realistic desired configuration. It was to prove that the live glibc boundary rejects incompatible session/provider and bridge/device policy before the package-owned GPU branch composes its own settings.

## Exact observable launch-chain environment

The validator directly observed meaningful non-empty `/proc/<pid>/environ` content for:

```text
launch-wrapper:
    83 entries

node-cli:
    85 entries

main:
    88 entries
```

Each of those three classes contained:

```text
GL_GPU=1
VK_DRIVER_FILES=
    $HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/
        freedreno_icd.aarch64.json
VK_ICD_FILENAMES=
    the same exact managed glibc ICD
```

All twelve exact-value gates passed:

```text
launch-wrapper_environment_readable
launch-wrapper_gl_gpu_one
launch-wrapper_vk_driver_files_exact
launch-wrapper_vk_icd_filenames_exact

node-cli_environment_readable
node-cli_gl_gpu_one
node-cli_vk_driver_files_exact
node-cli_vk_icd_filenames_exact

main_environment_readable
main_gl_gpu_one
main_vk_driver_files_exact
main_vk_icd_filenames_exact
```

This proves that the public launcher, vendor CLI chain, and Electron main process all received the intended application mode and exact managed Vulkan provider pair.

## Observable sanitation receipt

Passed:

```text
all_observable_gl_gpu_values_one
all_observable_vk_driver_files_exact
all_observable_vk_icd_filenames_exact
observable_mesa_loader_override_absent
observable_gallium_driver_absent
observable_libgl_always_software_absent
observable_ld_library_path_absent
observable_ld_preload_nonempty_absent
observable_injected_bionic_paths_absent
```

Therefore the meaningful observable process environments contained:

```text
exact glibc Freedreno Vulkan pair
no inherited bionic ICD path
no MESA_LOADER_DRIVER_OVERRIDE
no GALLIUM_DRIVER
no LIBGL_ALWAYS_SOFTWARE
no LD_LIBRARY_PATH
no non-empty LD_PRELOAD
```

The hostile bionic and llvmpipe inputs did not survive into the observable promoted launch chain.

## Main argv contract

Observed main command line:

```text
$HOME/gl/apps/vscode/code
    --disable-dev-shm-usage
    --ozone-platform=x11
    --disable-gpu-sandbox
    --ignore-gpu-blocklist
    --enable-features=Vulkan
    --use-gl=angle
    --use-angle=vulkan
    --disable-gpu-vsync
```

Passed:

```text
main_has_disable_gpu_sandbox
main_has_ignore_gpu_blocklist
main_has_enable_features_Vulkan
main_has_use_gl_angle
main_has_use_angle_vulkan
main_has_disable_gpu_vsync
main_exact_disable_gpu_absent
```

This proves that the actual package GPU branch, rather than the CPU fallback, reached the Electron main process.

## Child environment observability boundary

Observed:

```text
zygote_max_observable_environment_entries=0
gpu_max_observable_environment_entries=1
child_environment_value_claim=
    NOT_MADE_WHEN_PROC_ENVIRON_EMPTY
```

Passed child gates:

```text
zygote_process_observed
ygote_environment_read_attempt
gpu_process_observed
gpu_environment_read_attempt
```

The exact zygote/GPU environment values are deliberately not claimed because the captured `/proc/<pid>/environ` views were empty or effectively empty.

This does not weaken the effective GPU identity claim. That claim is established independently through CDP and mapped runtime paths.

## CDP primary selected device

Observed primary GPU device:

```text
primary=true
vendorString=Google Inc. (Qualcomm)
deviceString=
    ANGLE (Qualcomm,
        Vulkan 1.4.354
        (Turnip Adreno (TM) 730 (0x07030001)),
        turnip Mesa driver-538.1.4)
driverVendor=Mesa
```

Classification:

```text
classification=FREEDRENO_TURNIP
selected_provider=FREEDRENO_TURNIP
selected_device_family=Adreno
correlation_state=PASS
```

This is primary selected-device evidence, not only a mapped-library inference.

## Feature-mode identity

Observed:

```text
display_type=ANGLE_VULKAN
skia_backend=GaneshVulkan
hardware_supports_vulkan=true
vulkan_feature_status=enabled_on
```

Passed:

```text
display_type
skia_backend
vulkan_feature_status
renderer_identity
```

The package GPU branch retained the intended ANGLE/Vulkan and Ganesh/Vulkan feature composition.

## Runtime correlation

Observed mapped paths included:

```text
$HOME/gl/apps/vscode/libEGL.so
$HOME/gl/apps/vscode/libGLESv2.so
$HOME/gl/apps/vscode/libvulkan.so.1
$HOME/gl/opt/mesa-glibc-26.1.4-full/lib/
    libvulkan_freedreno.so
rootfs libVkLayer_MESA_device_select.so
rootfs libgbm.so.1.0.0
/dev/kgsl-3d0
```

Passed:

```text
provider_path_relation=PRESENT
device_node_relation=PRESENT
```

The CDP-selected Turnip/Adreno primary identity agrees with the managed provider mapping and KGSL device-node mapping.

## Two-launch evidence separation

The validator used two independent VS Code launches.

```text
phase 1:
    hostile-policy injection
    observable environment
    process topology
    main argv
    cleanup

phase 2:
    fresh launch
    CDP primary identity
    provider/device correlation
```

The second phase began only after the first process tree had been cleaned up.

This prevents environment/argv evidence and CDP evidence from accidentally describing overlapping application trees.

## Non-fatal diagnostics

Launch stderr contained:

```text
grep: /proc/version: Permission denied
VS Code CLI warnings that Chromium flags are not known VS Code options
```

The warnings explicitly state that the options were still passed to Electron/Chromium. The observed main argv and CDP result confirm that they took effect.

They are not gate failures.

## Proven promoted composition

The current post-correction evidence establishes:

```text
bionic/session hostile provider and bridge policy
    -> live gl/env sanitation
    -> package-owned GL_GPU=1 branch
    -> exact managed glibc Freedreno ICD pair
    -> no observable Zink/Gallium override
    -> ANGLE Vulkan argv
    -> Turnip/Freedreno primary selected provider
    -> Adreno 730
    -> managed provider mapping
    -> /dev/kgsl-3d0
```

This closes the current-source promoted VS Code GPU environment and selected-device gate.

## Claim boundary

This receipt proves:

```text
public launcher identity
exact observable launch-chain environment
hostile policy sanitation in observable environments
main GPU argv
zygote and GPU process existence
ANGLE/Vulkan feature mode
CDP primary selected provider/device
managed provider and KGSL correlation
```

It does not prove:

```text
exact child environment values when /proc/environ is empty
complete zero-copy presentation
all rendered frames
hardware video decode
native Dawn WebGPU adapter exposure
long-duration stability
```

## Strengthened CPU gate

Before running the promoted CPU gate, its validator was reviewed against the same lessons.

Updated:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    validate-promoted-vscode-cpu-policy.sh
```

Commit:

```text
69d49c49ff599bc4cbe4d0d94946ae37138a59f9
```

The CPU validator now deliberately injects:

```text
VK_DRIVER_FILES=/bionic/freedreno.json
VK_ICD_FILENAMES=/bionic/freedreno.json
MESA_LOADER_DRIVER_OVERRIDE=llvmpipe
GALLIUM_DRIVER=llvmpipe
```

It launches the promoted public launcher with:

```text
GL_GPU=0
isolated user-data directory
isolated extensions directory
--disable-extensions
--new-window
```

Required CPU environment result:

```text
main GL_GPU=0 directly observed
all observable GL_GPU values are 0
VK_DRIVER_FILES absent
VK_ICD_FILENAMES absent
MESA_LOADER_DRIVER_OVERRIDE absent
GALLIUM_DRIVER absent
LIBGL_ALWAYS_SOFTWARE absent
LD_LIBRARY_PATH absent
LD_PRELOAD absent or empty
/bionic/ paths absent
```

Required CPU argv result:

```text
exact --disable-gpu present
all GPU-enablement flags absent
```

Required topology/survival result:

```text
main observed
zygote observed
renderer observed
main survives the bounded observation
no fatal diagnostic
```

Zygote and renderer exact environment values are not required when their `/proc/environ` content is empty. Their process existence and environment read attempt are recorded instead.

The presence or absence of a Chromium GPU helper process remains observational and is not itself a CPU pass/fail condition.

## Current gate state

```text
expanded pre-deploy:
    PASS

expanded live installation:
    PASS

current-head gl-run renderer:
    PASS

current-head VS Code GPU environment/identity:
    PASS

promoted VS Code CPU policy:
    NEXT

promoted Obsidian GPU/CPU:
    BLOCKED ON VS CODE CPU RESULT

scoped graphics-policy promotion closure:
    PENDING
```

## Stop line

Do not:

```text
rerun the GPU gate without a new source change
interpret child empty /proc/environ as a policy value
run CPU and Obsidian probes concurrently
use the real user-data directory for the CPU gate
require absence of a Chromium GPU helper process in CPU mode
mark VS Code fully closed before the CPU gate
```

Sync the CPU-validator-only commit, run its targeted syntax check, and execute the promoted CPU policy gate with a fresh evidence root.
