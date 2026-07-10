# 0038 — Obsidian CPU Control Vulkan Policy Leak Hypothesis

## Status

The Obsidian CPU-mode control used:

```text
GL_GPU=0
```

and the promoted launcher selected:

```text
--disable-gpu
```

However the captured runtime maps still showed:

```text
AppDir libEGL.so
AppDir libGLESv2.so
AppDir libvulkan.so.1
Mesa libvulkan_freedreno.so
Mesa device-select layer
GBM
/dev/kgsl-3d0
```

The process-class mapping concentrated the full Vulkan/driver/device chain in one zygote-class PID while GBM appeared across main, renderer, utility, and zygote classes.

## Environment path inspection

The promoted Obsidian launcher first executes:

```bash
source "$HOME/gl/env"
```

and only later chooses CPU or GPU Chromium flags from `GL_GPU`.

The shared `gl/env` unconditionally performs Vulkan provider selection when the Freedreno ICD JSON is readable:

```text
VK_ICD_FILENAMES=<freedreno ICD JSON>
VK_DRIVER_FILES=<freedreno ICD JSON>
```

Therefore:

```text
GL_GPU=0
    changes Chromium argv

but does not remove
    Vulkan provider-selection environment
```

The original CPU control is therefore not a strict graphics-policy-free control.

## Hypothesis

The remaining Vulkan provider-selection variables may cause Electron/Chromium or one of its runtime components to probe or initialize the Vulkan stack even while the application is launched with `--disable-gpu`.

This hypothesis is supported by environment and map correlation, but is not yet proven causally.

The experiment must compare:

```text
A. current CPU control
    --disable-gpu
    VK_DRIVER_FILES set
    VK_ICD_FILENAMES set

B. strict CPU control
    --disable-gpu
    VK_DRIVER_FILES unset
    VK_ICD_FILENAMES unset
```

with all other launcher composition held equal as closely as practical.

## Experiment-local launcher

The experiment now includes:

```text
recipe/launch-strict-cpu.sh
```

It reproduces the promoted Obsidian launcher composition required for the CPU path, then removes only:

```text
VK_DRIVER_FILES
VK_ICD_FILENAMES
```

before launching Obsidian with the same CPU-mode Chromium flags.

This experiment-local launcher does not modify the promoted launcher and does not yet change `gl/env`.

## Acceptance question

Compare the strict CPU control against the existing control for:

```text
process topology
survival
visible GUI behavior
AppDir locality
rootfs provider set
graphics process mappings
KGSL device mapping
Freedreno driver mapping
Mesa device-select layer mapping
GBM mapping
```

Possible outcomes:

```text
1. Vulkan/driver/device chain disappears
    -> strong evidence that global Vulkan env policy contaminated CPU control

2. chain remains unchanged
    -> Vulkan env variables are not sufficient to explain the mapping

3. workload fails or topology changes materially
    -> global graphics policy is coupled to current app startup behavior
```

## Architecture consequence

The semantic inventory already assigned Vulkan environment variables to:

```text
provider.graphics.vulkan.glibc
```

rather than global world policy.

This experiment tests that ownership conclusion with a real application-domain workload.

Do not yet:

```text
remove Vulkan variables from gl/env globally
change the promoted Obsidian launcher
change graphics provider activation policy
```

until the strict CPU A/B result is captured.
