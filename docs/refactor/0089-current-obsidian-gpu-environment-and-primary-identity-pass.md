# 0089 — Current Obsidian GPU Environment and Primary Identity PASS

## Status

The corrected promoted Obsidian GPU validator passed on the authoritative Termux/Android device.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    corrected-obsidian-gpu-environment-identity-20260711-180746
```

Captured repository state:

```text
branch:
    refactor/module-package-layout

head:
    3384bf136f3f35f7ab1d86b2005c2e7559d7e298
```

Receipt:

```text
gate_failures=0
validation.status=PASS
```

All 48 gates passed.

This is the canonical current-source promoted Obsidian GPU receipt. It supersedes the incomplete first attempt documented in `0088`.

## Public launcher authority

Observed launcher:

```text
$HOME/gl/bin/obsidian-app
```

Exact target:

```text
$HOME/projects/termux-native-desktop/
    packages/obsidian/launcher/obsidian-app
```

The validation therefore exercised the promoted package-owned GUI launcher rather than a report-local or experiment-only launch wrapper.

## Two independently isolated application trees

The corrected validator aligned Obsidian's application-level configuration authority with the Chromium user-data path.

Environment phase:

```text
XDG_CONFIG_HOME=
    $OUT/environment/config

actual user data=
    $OUT/environment/config/obsidian
```

CDP phase:

```text
XDG_CONFIG_HOME=
    $OUT/probe/config

actual user data=
    $OUT/probe/config/obsidian
```

Passed:

```text
main_xdg_config_home_exact
all_observable_xdg_config_home_exact
main_uses_isolated_user_data
renderer_uses_isolated_user_data
normal_user_data_path_absent
cdp_config_home
cdp_user_data_dir
```

No captured process command line used:

```text
$HOME/.config/obsidian
```

The environment and CDP phases used separate receipt-local roots and were not combined with the incomplete first attempt.

## Hostile inherited-policy input

The environment phase deliberately injected:

```text
VK_DRIVER_FILES=/bionic/freedreno.json
VK_ICD_FILENAMES=/bionic/freedreno.json
MESA_LOADER_DRIVER_OVERRIDE=llvmpipe
GALLIUM_DRIVER=llvmpipe
```

The purpose was to prove that the live glibc baseline and package launcher reject incompatible bionic provider and bridge/device policy before composing the Obsidian GPU branch.

## Direct environment evidence

The corrected run captured meaningful environments for all relevant process classes:

```text
main:
    77 entries

zygote:
    78 entries

gpu:
    80 entries

renderer:
    80 entries
```

Each observable main, zygote, GPU, utility, and renderer process contained:

```text
GL_GPU=1
XDG_CONFIG_HOME=$OUT/environment/config
VK_DRIVER_FILES=<exact managed glibc Freedreno ICD>
VK_ICD_FILENAMES=<same exact managed glibc Freedreno ICD>
```

Passed:

```text
main_gl_gpu_one
main_xdg_config_home_exact
main_vk_driver_files_exact
main_vk_icd_filenames_exact
all_observable_gl_gpu_values_one
all_observable_xdg_config_home_exact
all_observable_vk_driver_files_exact
all_observable_vk_icd_filenames_exact
```

Unlike the VS Code child environment observations, the Obsidian child environment views remained fully populated in this receipt. The validator still retains the general observability boundary and does not assume future child views must remain populated.

## Observable sanitation

Passed:

```text
observable_mesa_loader_override_absent
observable_gallium_driver_absent
observable_libgl_always_software_absent
observable_ld_library_path_absent
observable_ld_preload_nonempty_absent
observable_injected_bionic_paths_absent
```

Therefore the observable application tree contained:

```text
no inherited MESA_LOADER_DRIVER_OVERRIDE
no inherited GALLIUM_DRIVER
no LIBGL_ALWAYS_SOFTWARE
no LD_LIBRARY_PATH
no non-empty LD_PRELOAD
no /bionic/ provider path
```

The exact managed glibc ICD pair replaced the hostile bionic pair, while the hostile llvmpipe bridge/device policy was removed rather than inherited.

## Main GPU argv

Observed main command line:

```text
$HOME/gl/apps/obsidian/obsidian
    --disable-dev-shm-usage
    --ozone-platform=x11
    --disable-gpu-sandbox
    --ignore-gpu-blocklist
    --enable-features=Vulkan
    --use-gl=angle
    --use-angle=vulkan
    --disable-gpu-vsync
    --user-data-dir <receipt-local>/environment/config/obsidian
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

The GPU process independently showed:

```text
--use-angle=vulkan
--use-gl=angle
--enable-features=...Vulkan
--user-data-dir=<same receipt-local Obsidian directory>
```

The renderer used the same receipt-local user-data directory and retained Vulkan in its feature set.

## Process topology and bounded survival

Observed:

```text
main=1
zygote=1
renderer=1
gpu=1
```

Passed:

```text
main_observed
main_environment_read_attempt
zygote_observed
zygote_environment_read_attempt
renderer_observed
renderer_environment_read_attempt
gpu_observed
gpu_environment_read_attempt
main_survived_observation
no_fatal_gpu_diagnostic
```

The main, zygote, GPU, utility, and renderer processes remained observable through the 20-second environment phase.

Normal isolated-profile startup output included:

```text
missing initial obsidian.json ignored
main application package loaded
update check succeeded
latest version 1.12.7
application up to date
```

The missing initial `obsidian.json` is consistent with a fresh isolated profile and was explicitly logged as ignored by the application.

## Non-fatal platform diagnostics

Stderr contained:

```text
inotify max_user_watches read failure
dbus system socket unavailable
xdg-settings unavailable
```

These diagnostics did not terminate the application, prevent renderer/GPU creation, or prevent CDP identity collection.

They are not graphics-policy failures.

## CDP primary GPU identity

The fresh CDP phase successfully discovered its receipt-local `DevToolsActivePort` and executed `SystemInfo.getInfo`.

Primary device:

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

Passed:

```text
cdp_probe_status
identity_status
classification
selected_provider
selected_device_family
renderer_identity
```

This is selected primary-device evidence, not merely a library-mapping inference.

## Feature-mode identity

Observed:

```text
display_type=ANGLE_VULKAN
skia_backend=GaneshVulkan
hardware_supports_vulkan=true
vulkan_feature_status=enabled_on
```

Additional feature status included:

```text
gpu_compositing=enabled
opengl=enabled_on
rasterization=enabled
webgl=enabled
webgl2=enabled
webgpu=disabled_off
video_decode=disabled_software
video_encode=disabled_software
```

Passed:

```text
display_type
skia_backend
hardware_supports_vulkan
vulkan_feature_status
```

The receipt proves conventional Electron/Chromium ANGLE-Vulkan acceleration. It does not claim Dawn WebGPU or hardware video decode.

## Provider and device correlation

Mapped graphics paths included:

```text
$HOME/gl/apps/obsidian/libEGL.so
$HOME/gl/apps/obsidian/libGLESv2.so
$HOME/gl/apps/obsidian/libvulkan.so.1
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

The CDP primary Turnip/Adreno identity agrees with the managed Freedreno provider mapping and KGSL device-node mapping.

## Proven promoted composition

The corrected receipt establishes:

```text
hostile bionic Vulkan and llvmpipe policy
    -> live gl/env sanitation
    -> package-owned GL_GPU=1 branch
    -> exact managed glibc Freedreno ICD pair
    -> no observable Zink/Gallium override
    -> receipt-local XDG and Obsidian user-data authority
    -> ANGLE Vulkan main/GPU argv
    -> viable main/zygote/GPU/renderer topology
    -> fresh CDP primary Turnip/Freedreno identity
    -> Adreno 730
    -> managed libvulkan_freedreno.so mapping
    -> /dev/kgsl-3d0
```

This closes the promoted Obsidian GPU gate.

## Claim boundary

This receipt proves:

```text
public launcher identity
fresh receipt-local application profile isolation
exact observable provider environment
hostile policy sanitation
GPU application argv
process topology and bounded survival
CDP primary selected provider/device
ANGLE/Vulkan and Ganesh/Vulkan feature mode
managed provider and KGSL correlation
```

It does not prove:

```text
complete zero-copy presentation
all frames or all application views
long-duration stability
hardware video decoding
native Dawn WebGPU exposure
normal-profile behavior with user plugins and vaults
```

## Next gate — promoted Obsidian CPU

The final application-mode gate is the same package-owned launcher under:

```text
GL_GPU=0
```

A dedicated validator now exists:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    validate-promoted-obsidian-cpu-policy.sh
```

It uses:

```text
XDG_CONFIG_HOME=$OUT/config
USER_DATA_DIR=$OUT/config/obsidian
```

and deliberately injects the hostile bionic Vulkan pair plus llvmpipe Mesa/Gallium policy.

Required result:

```text
GL_GPU=0
no explicit Vulkan pair
no Zink/Gallium override
exact --disable-gpu
no GPU-enablement flags
receipt-local main and renderer user-data argv
no $HOME/.config/obsidian path
main/zygote/renderer topology
20-second main survival
no fatal startup diagnostic
```

The presence of an internal process named `gpu-process` remains observational and is not by itself a CPU-mode failure.

## Current gate state

```text
expanded pre-deploy:
    PASS

expanded live installation:
    PASS

current-head gl-run:
    PASS

current-head VS Code GPU:
    PASS

current-head VS Code CPU:
    PASS

current-head Obsidian GPU:
    PASS

promoted Obsidian CPU:
    NEXT

scoped graphics-policy promotion closure:
    BLOCKED ON OBSIDIAN CPU
```

## Stop line

Do not:

```text
rerun the Obsidian GPU gate without a source change
reuse the incomplete first Obsidian evidence root
use the normal Obsidian profile for the CPU gate
interpret WebGPU or video-decode status as part of the GPU PASS
mark the transaction closed before the CPU receipt passes
```
