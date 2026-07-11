# 0090 — Current Obsidian CPU Policy and Survival PASS

## Status

The promoted Obsidian CPU policy validator passed on the authoritative Termux/Android device.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    current-obsidian-cpu-policy-20260711-181554
```

Captured repository state:

```text
branch:
    refactor/module-package-layout

head:
    5ab13fd6c2af5843abf7bbff3a8a26f46a8e84b5
```

Receipt:

```text
gate_failures=0
validation.status=PASS
```

All 21 gates passed.

Together with the canonical GPU receipt in `0089`, this closes both promoted Obsidian application-feature branches.

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

The validation exercised the promoted package-owned GUI launcher rather than a report-local or experiment-only wrapper.

## Isolated application authority

The validator aligned Obsidian's application-level configuration ownership with the actual Chromium user-data directory:

```text
XDG_CONFIG_HOME=
    $OUT/config

actual Obsidian user data=
    $OUT/config/obsidian
```

Observed summary:

```text
config_home=
    $PREFIX/tmp/tnd-vulkan-policy-composition/
        current-obsidian-cpu-policy-20260711-181554/config

user_data_dir=
    $PREFIX/tmp/tnd-vulkan-policy-composition/
        current-obsidian-cpu-policy-20260711-181554/config/obsidian
```

Passed:

```text
main_xdg_config_home_exact
all_observable_xdg_config_home_exact
main_uses_isolated_user_data
renderer_uses_isolated_user_data
normal_user_data_path_absent
```

No captured process command line used:

```text
$HOME/.config/obsidian
```

The result therefore does not depend on the user's normal Obsidian configuration, locks, vault state, or plugins.

## Deliberate hostile-policy input

The validator injected:

```text
VK_DRIVER_FILES=/bionic/freedreno.json
VK_ICD_FILENAMES=/bionic/freedreno.json
MESA_LOADER_DRIVER_OVERRIDE=llvmpipe
GALLIUM_DRIVER=llvmpipe
```

and selected:

```text
GL_GPU=0
```

The purpose was to prove that the public package launcher removes inherited bionic provider and bridge/device policy before applying the CPU branch.

## Direct observable environment evidence

Meaningful environments were captured for:

```text
main:
    75 entries

zygote:
    76 entries

utility:
    78 entries

renderer:
    78 entries
```

Every selected observable process environment contained only:

```text
GL_GPU=0
XDG_CONFIG_HOME=<receipt-local config root>
```

No selected observable process environment contained:

```text
VK_DRIVER_FILES
VK_ICD_FILENAMES
MESA_LOADER_DRIVER_OVERRIDE
GALLIUM_DRIVER
LIBGL_ALWAYS_SOFTWARE
LD_LIBRARY_PATH
non-empty LD_PRELOAD
/bionic/ provider path
```

Passed:

```text
main_gl_gpu_zero
main_xdg_config_home_exact
all_observable_gl_gpu_values_zero
all_observable_xdg_config_home_exact
observable_explicit_vulkan_policy_absent
observable_graphics_and_library_overrides_absent
observable_ld_preload_nonempty_absent
observable_injected_bionic_paths_absent
```

This directly proves that the CPU branch retained the sanitized, provider-neutral glibc baseline despite hostile inherited inputs.

## Main argv contract

Observed main command line:

```text
env LD_PRELOAD=
$HOME/gl/apps/obsidian/obsidian
    --disable-dev-shm-usage
    --ozone-platform=x11
    --disable-gpu
    --user-data-dir <receipt-local>/config/obsidian
```

Passed:

```text
main_has_exact_disable_gpu
main_has_no_gpu_enable_flags
```

The exact-token check confirms the presence of:

```text
--disable-gpu
```

and the absence of GPU-branch policy flags:

```text
--use-angle=vulkan
--use-gl=angle
--enable-features=Vulkan
--disable-gpu-vsync
--ignore-gpu-blocklist
--disable-gpu-sandbox
```

## Effective renderer mode

No process with:

```text
--type=gpu-process
```

was observed during the full 20-second run:

```text
gpu_seen_observational=0
gpu_max_observable_environment_entries=0
```

The renderer command line contained:

```text
--disable-gpu-compositing
```

and did not contain the Vulkan GPU branch feature flag.

This provides a stronger CPU-mode observation than the VS Code CPU receipt, where Chromium retained an internal GPU helper using `--use-gl=disabled`.

The architecture contract does not require GPU-helper absence in every Electron version, but this specific Obsidian receipt directly observed none.

## Process topology and bounded survival

Observed process classes:

```text
main
zygote
utility
renderer
```

Summary:

```text
main_seen=1
zygote_seen=1
renderer_seen=1
gpu_seen_observational=0
captured_processes=6
duration_seconds=20
```

Passed:

```text
main_observed
main_environment_read_attempt
zygote_observed
zygote_environment_read_attempt
renderer_observed
renderer_environment_read_attempt
main_survived_observation
no_fatal_diagnostic
```

The observation timeline showed the main, zygote, and renderer classes continuously present from startup through the end of the bounded interval.

This proves GUI-process viability rather than only argument construction.

## Fresh-profile startup behavior

Launch stdout contained:

```text
Ignored: ENOENT for receipt-local obsidian.json
Loaded main app package
Checking for update using Github
Success.
Latest version is 1.12.7
App is up to date.
```

The missing `obsidian.json` is expected for the newly created isolated profile and was explicitly treated as ignored by the application.

## Non-fatal platform diagnostics

Launch stderr contained:

```text
inotify max_user_watches read failure
dbus system socket unavailable
xdg-settings unavailable
```

The diagnostics did not terminate the application, prevent renderer creation, or break the 20-second survival gate.

They are not CPU policy failures.

## Proven promoted CPU composition

The receipt establishes:

```text
hostile bionic Vulkan and llvmpipe policy
    -> live gl/env sanitation
    -> package-owned GL_GPU=0 branch
    -> no explicit Vulkan provider
    -> no Zink/Gallium override
    -> receipt-local XDG config root
    -> receipt-local Obsidian user-data directory
    -> exact --disable-gpu
    -> no GPU-enablement flags
    -> no observed GPU process
    -> renderer --disable-gpu-compositing
    -> viable main/zygote/renderer topology
    -> main survives 20-second observation
```

## Obsidian promotion closure

The current promoted Obsidian package now has complementary receipts:

```text
GPU branch:
    exact managed glibc Freedreno pair
    no observable Zink/Gallium leak
    ANGLE Vulkan argv
    receipt-local application profile
    CDP primary Turnip / Adreno 730
    managed provider + KGSL correlation

CPU branch:
    no explicit Vulkan provider
    no observable Zink/Gallium leak
    exact --disable-gpu
    no GPU-enablement flags
    receipt-local application profile
    no observed GPU process
    renderer --disable-gpu-compositing
    bounded GUI-process survival
```

Therefore the Obsidian portion of the scoped graphics-policy promotion transaction is closed.

## Claim boundary

This receipt proves:

```text
public launcher identity
hostile-policy sanitation in observable environments
receipt-local application configuration and user-data ownership
CPU application-mode selection
exact main argv
absence of GPU-enablement argv
absence of an observed GPU process during this run
renderer CPU-compositing mode
process topology
20-second main-process survival
absence of fatal startup diagnostics
```

It does not prove:

```text
long-duration stability
normal-profile behavior with user vaults and plugins
application feature correctness beyond bounded startup
performance characteristics
that all Electron releases must omit a GPU helper in CPU mode
```

## Transaction consequence

This receipt removes the final workload-level blocker from the scoped graphics-policy promotion transaction.

All required workload gates now have canonical current-source receipts:

```text
gl-run renderer
VS Code GPU
VS Code CPU
Obsidian GPU
Obsidian CPU
```

The transaction may now be closed at the architecture/evidence level, while unrelated open work such as atomic activation, WebGPU, video decode, and PyMOL remains separate.

## Stop line

Do not:

```text
rerun Obsidian GPU or CPU without a relevant source change
use the normal Obsidian profile as validation evidence
reinterpret platform diagnostics as a graphics-policy failure
extend the CPU PASS to long-duration or normal-vault behavior
keep the scoped transaction marked pending after closure documentation is committed
```
