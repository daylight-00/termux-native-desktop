# 0087 — Current VS Code CPU Policy and Survival PASS

## Status

The promoted VS Code CPU policy validator passed on the real Termux/Android device.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    current-vscode-cpu-policy-20260711-173034
```

Captured repository state:

```text
branch:
    refactor/module-package-layout

head:
    0c6a85235ee9b759addc9963a16060c806277fe3
```

Receipt:

```text
gate_failures=0
validation.status=PASS
```

All 18 CPU-policy gates passed.

This closes the promoted VS Code CPU branch. Together with the canonical GPU receipt in `0086`, both package-owned VS Code feature branches are now validated on the corrected graphics-policy baseline.

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

The validator used the actual promoted public launcher rather than an experiment-only adapter.

## Isolated application state

The run used receipt-local paths:

```text
user data:
    $OUT/user-data

extensions:
    $OUT/extensions
```

and passed:

```text
--disable-extensions
--new-window
```

The gate therefore did not depend on or mutate the normal VS Code user-data directory.

## Deliberate hostile-policy input

The validator injected:

```text
VK_DRIVER_FILES=/bionic/freedreno.json
VK_ICD_FILENAMES=/bionic/freedreno.json
MESA_LOADER_DRIVER_OVERRIDE=llvmpipe
GALLIUM_DRIVER=llvmpipe
```

It then launched the promoted package with:

```text
GL_GPU=0
```

The purpose was to prove that the CPU branch begins from the corrected glibc baseline and does not accidentally retain a bionic provider, a software Vulkan provider pin, or an inherited OpenGL/Gallium selection.

## Observable environment result

Meaningful non-empty environments were captured for:

```text
cli-wrapper:
    73 entries

node-cli:
    75 entries

main:
    78 entries

crashpad:
    80 entries
```

The selected environment receipt contained only:

```text
GL_GPU=0
```

for those observable launch-chain processes.

It did not contain:

```text
VK_DRIVER_FILES
VK_ICD_FILENAMES
MESA_LOADER_DRIVER_OVERRIDE
GALLIUM_DRIVER
LIBGL_ALWAYS_SOFTWARE
LD_LIBRARY_PATH
non-empty LD_PRELOAD
/bionic/ paths
```

Passed environment gates:

```text
all_observable_gl_gpu_values_zero
main_gl_gpu_zero_observed
observable_explicit_vulkan_policy_absent
observable_graphics_and_library_overrides_absent
observable_ld_preload_nonempty_absent
observable_injected_bionic_paths_absent
```

This directly proves that the hostile graphics-policy inputs did not survive into the meaningful observable CPU launch chain.

## Main argv contract

Observed Electron main command line:

```text
$HOME/gl/apps/vscode/code
    --disable-dev-shm-usage
    --ozone-platform=x11
    --disable-gpu
    --user-data-dir $OUT/user-data
    --extensions-dir $OUT/extensions
    --disable-extensions
    --new-window
```

Passed:

```text
main_has_exact_disable_gpu
main_has_no_gpu_enable_flags
```

The main process contained the exact token:

```text
--disable-gpu
```

and did not contain:

```text
--use-angle=vulkan
--use-gl=angle
--enable-features=Vulkan
--disable-gpu-vsync
--ignore-gpu-blocklist
--disable-gpu-sandbox
```

The exact-token test does not confuse a hypothetical `--disable-gpu-sandbox` with `--disable-gpu`.

## Process topology and survival

Observed:

```text
main_seen=1
zygote_seen=1
renderer_seen=1
gpu_seen_observational=1
captured_processes=12
```

Passed:

```text
main_observed
zygote_observed
renderer_observed
main_environment_readable
zygote_process_observed
zygote_environment_read_attempt
renderer_process_observed
renderer_environment_read_attempt
main_survived_observation
no_fatal_diagnostic
```

The main process survived the full bounded 20-second observation period. The final observation samples continued to show main, zygote, renderer, and the Chromium GPU helper.

Launch stderr contained only:

```text
grep: /proc/version: Permission denied
```

No fatal diagnostic or unusable-GPU-process signature was present.

## Why a GPU helper process is compatible with CPU mode

A Chromium GPU helper process was observed even though the main process used `--disable-gpu`.

Its command line contained:

```text
--type=gpu-process
--use-gl=disabled
```

It did not contain the promoted GPU-branch flags:

```text
--use-angle=vulkan
--use-gl=angle
--enable-features=Vulkan
--disable-gpu-vsync
--ignore-gpu-blocklist
```

The renderer command line contained:

```text
--disable-gpu-compositing
```

Therefore the helper's existence does not mean that the hardware GPU branch was active. Chromium may retain a process named `gpu-process` for internal software/disabled graphics services even under `--disable-gpu`.

The project contract is intentionally:

```text
CPU mode
    -> exact --disable-gpu on main
    -> no GPU-enablement argv on main
    -> no explicit Vulkan provider policy
    -> no Zink/Gallium override
    -> viable renderer topology
    -> bounded main-process survival
```

It is not:

```text
CPU mode
    -> no process named gpu-process may ever exist
```

Encoding the latter would create a false architecture dependency on Chromium's internal process topology.

## Child environment observability boundary

Observed:

```text
zygote_max_observable_environment_entries=0
renderer_max_observable_environment_entries=1
child_environment_value_claim=
    NOT_MADE_WHEN_PROC_ENVIRON_EMPTY
```

The validator records child process existence and successful `/proc/<pid>/environ` read attempts, but does not claim exact child values when the returned content is empty or effectively empty.

This is the same corrected observability model used by the canonical VS Code GPU gate.

## Proven promoted CPU composition

The receipt establishes:

```text
hostile bionic Vulkan and llvmpipe policy
    -> live gl/env sanitation
    -> package-owned GL_GPU=0 branch
    -> exact --disable-gpu main argv
    -> no observable explicit Vulkan provider
    -> no observable Zink/Gallium override
    -> Chromium software/disabled graphics topology
    -> renderer process created
    -> main process survives 20 seconds
```

## VS Code package closure

Current-source VS Code evidence now includes:

```text
GPU branch:
    exact managed glibc Freedreno pair
    no observable Zink/Gallium leak
    ANGLE Vulkan argv
    CDP primary Turnip/Adreno 730
    managed provider mapping
    /dev/kgsl-3d0 mapping
    PASS

CPU branch:
    no explicit Vulkan provider
    no observable Zink/Gallium leak
    exact --disable-gpu
    no GPU-enablement argv
    viable renderer topology
    bounded survival
    PASS
```

The scoped graphics-policy transaction can now advance from VS Code to the promoted Obsidian GUI branches.

## Claim boundary

This CPU receipt proves:

```text
public launcher identity
observable CPU environment composition
hostile graphics-policy sanitation
exact main CPU argv
main/zygote/renderer topology
bounded startup survival
absence of fatal startup diagnostics
```

It does not prove:

```text
long-duration application stability
performance characteristics
all rendered frames
exact child environment values when /proc/environ is empty
absence of all Chromium GPU helper processes
```

## Next gate — promoted Obsidian GPU

The historical Obsidian AppImage onboarding experiment already established a working WebGL2 path:

```text
Obsidian
    -> WebGL2
    -> ANGLE
    -> Vulkan
    -> Turnip
    -> Adreno 730
```

The remaining promotion question is whether the current public launcher:

```text
$HOME/gl/bin/obsidian-app
```

preserves the corrected baseline, explicit provider profile, GPU argv, selected primary device, and runtime provider/device correlation.

The Obsidian gate must use isolated application state, hostile-policy injection, and the same child-environment observability boundary as the VS Code gates.

## Current gate state

```text
expanded pre-deploy:
    PASS

expanded live installation:
    PASS

current-head gl-run renderer:
    PASS

current-head VS Code GPU:
    PASS

current-head VS Code CPU:
    PASS

promoted Obsidian GPU:
    NEXT

promoted Obsidian CPU:
    AFTER GPU

scoped graphics-policy promotion closure:
    PENDING
```

## Stop line

Do not:

```text
rerun VS Code gates without a source change
interpret a Chromium GPU helper name as hardware acceleration
reuse the normal Obsidian user-data directory for the next gate
run Obsidian GPU and CPU probes concurrently
mark the whole scoped transaction complete before both Obsidian branches pass
```

Inspect and promote bounded Obsidian GPU/CPU validators next.
