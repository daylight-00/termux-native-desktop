# 0087 — Current VS Code CPU Policy PASS

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

All 18 CPU policy gates passed.

Together with the canonical GPU receipt in `0086`, this closes both promoted VS Code application-feature branches.

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

The validation exercised the package-owned promoted public entry point rather than an experiment-only adapter.

## Isolated application state

The validator used dedicated paths under the evidence root:

```text
user-data/
extensions/
```

It also passed:

```text
--disable-extensions
--new-window
```

The real user profile and extension state were not required for the result.

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

The purpose was to prove that the public launcher removes inherited bionic provider and bridge/device policy before applying the CPU branch.

## Observable environment receipt

Meaningful non-empty environment views were captured for:

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

Every selected observable process value was:

```text
GL_GPU=0
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
/bionic/ path
```

Passed gates:

```text
all_observable_gl_gpu_values_zero
main_gl_gpu_zero_observed
observable_explicit_vulkan_policy_absent
observable_graphics_and_library_overrides_absent
observable_ld_preload_nonempty_absent
observable_injected_bionic_paths_absent
```

This directly proves the package CPU branch retained the sanitized, provider-neutral glibc baseline despite hostile inherited inputs.

## Main argv contract

Observed Electron main command line included the exact token:

```text
--disable-gpu
```

It did not include the GPU-branch policy flags:

```text
--use-angle=vulkan
--use-gl=angle
--enable-features=Vulkan
--disable-gpu-vsync
--ignore-gpu-blocklist
--disable-gpu-sandbox
```

Passed:

```text
main_has_exact_disable_gpu
main_has_no_gpu_enable_flags
```

The exact-token check distinguishes `--disable-gpu` from unrelated longer options.

## Process topology and survival

Observed process classes included:

```text
main
zygote
renderer
gpu
utility
crashpad
```

Summary:

```text
main_seen=1
zygote_seen=1
renderer_seen=1
gpu_seen_observational=1
captured_processes=12
```

The main process remained part of the isolated probe at the end of the 20-second observation interval.

Passed:

```text
main_observed
zygote_observed
renderer_observed
main_survived_observation
no_fatal_diagnostic
```

This proves bounded GUI-process viability rather than only argument construction.

## Why a GPU helper process is not a failure

Chromium created a process with:

```text
--type=gpu-process
```

while the application main process was launched with:

```text
--disable-gpu
```

The helper command line itself showed:

```text
--use-gl=disabled
```

The renderer showed:

```text
--disable-gpu-compositing
```

Therefore process-name presence alone is not equivalent to hardware GPU enablement.

The architecture gate correctly evaluates:

```text
package feature policy
main argv
observable provider/bridge environment
effective child argv
bounded application survival
```

It does not encode the false invariant that CPU mode must contain no Chromium process named `gpu-process`.

## Child environment observability boundary

Observed:

```text
zygote_max_observable_environment_entries=0
renderer_max_observable_environment_entries=1
child_environment_value_claim=
    NOT_MADE_WHEN_PROC_ENVIRON_EMPTY
```

Passed:

```text
zygote_process_observed
zygote_environment_read_attempt
renderer_process_observed
renderer_environment_read_attempt
```

Exact child environment values are not claimed when `/proc/<pid>/environ` is empty or effectively empty.

This follows the observability model established by the corrected GPU validator.

## Non-fatal diagnostic

Launch stderr contained only:

```text
grep: /proc/version: Permission denied
```

No fatal Chromium diagnostic and no unusable-GPU-process signature was present.

## Proven promoted CPU composition

The receipt establishes:

```text
hostile bionic Vulkan and llvmpipe policy
    -> live gl/env sanitation
    -> package-owned GL_GPU=0 branch
    -> no explicit Vulkan provider
    -> no Zink/Gallium override
    -> exact --disable-gpu
    -> no GPU-enablement flags
    -> child GPU helper uses --use-gl=disabled
    -> renderer uses --disable-gpu-compositing
    -> viable main/zygote/renderer topology
    -> main survives 20-second observation
```

## VS Code promotion closure

The current promoted VS Code package now has complementary receipts:

```text
GPU branch:
    exact managed glibc Freedreno pair
    no observable Zink/Gallium leak
    ANGLE Vulkan argv
    CDP primary Turnip / Adreno 730
    managed provider + KGSL correlation

CPU branch:
    no explicit Vulkan provider
    no observable Zink/Gallium leak
    exact --disable-gpu
    no GPU-enablement flags
    bounded GUI-process survival
```

Therefore the VS Code portion of the scoped graphics-policy promotion transaction is closed.

## Claim boundary

This receipt proves:

```text
public launcher identity
hostile-policy sanitation in observable environments
CPU application-mode selection
exact main argv
absence of GPU-enablement argv
process topology
20-second main-process survival
absence of fatal startup diagnostics
```

It does not prove:

```text
that Chromium creates no GPU helper process
all rendering is performed by one named child process
long-duration stability
application-level feature correctness beyond startup
performance characteristics
```

## Next gate — promoted Obsidian

The remaining application workload is the package-owned Obsidian GUI launcher:

```text
$HOME/gl/bin/obsidian-app
```

Historical experiment evidence established:

```text
CPU/X11 GUI launch
WebGL2
ANGLE
Vulkan
Turnip
Adreno 730
Obsidian CLI connection
```

The promoted validation must now prove the current package launcher under the corrected shared baseline.

Required order:

```text
1. Obsidian GPU environment/argv and selected-device identity
2. Obsidian CPU environment/argv and bounded survival
```

Do not rely only on the historical onboarding report, because it predates the promoted scoped provider profile and the full four-variable graphics-policy sanitation contract.

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
rerun VS Code GPU or CPU without a runtime-source change
classify the CPU-mode Chromium GPU helper as hardware acceleration
reuse the real Obsidian user-data directory for promoted probes
run Obsidian GPU and CPU probes concurrently
mark the whole scoped transaction complete before both Obsidian branches pass
```

Inspect and reuse the existing Electron/CDP evidence machinery before adding Obsidian validators.
