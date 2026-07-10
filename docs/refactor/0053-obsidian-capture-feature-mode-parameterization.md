# 0053 — Obsidian Capture Feature-Mode Parameterization

## Status

The Obsidian capture harness previously hardcoded:

```text
GL_GPU=0
```

when invoking its launcher.

That was correct for the original CPU control, but it prevented reuse of the same topology/survival/maps harness for the scoped Vulkan policy composition experiment.

## Problem

The next Electron consumer experiment needs to vary at least:

```text
provider policy:
    explicit-freedreno
    implicit-discovery

application feature mode:
    GL_GPU=1 for GPU-path validation
```

The old capture harness forced:

```text
GL_GPU=0
```

regardless of the launcher selected through `LAUNCHER=`.

Therefore pointing `LAUNCHER` at:

```text
experiments/glibc/vulkan-policy-composition/recipe/launch-obsidian-with-policy.sh
```

would not have created a real GPU-feature-mode control.

## Correction

The capture harness now accepts:

```text
CONTROL_GL_GPU
```

with default:

```text
0
```

so all existing CPU-control behavior remains unchanged.

Accepted values:

```text
0
1
```

The launch boundary is now:

```text
GL_GPU="$CONTROL_GL_GPU" "$LAUNCHER"
```

and the evidence directory records:

```text
mode: GL_GPU=<0|1>
```

## Why this is not a promoted policy change

The change is limited to:

```text
experiments/glibc/selected-obsidian-closure/recipe/capture-control.sh
```

It does not change:

```text
gl/env
gl-run
promoted Obsidian launcher
promoted VS Code launcher
session policy
provider promotion
```

It only exposes an already meaningful experimental dimension to the capture harness.

## Next use

For the scoped Obsidian GPU-path policy controls, set:

```text
LAUNCHER=$REPO/experiments/glibc/vulkan-policy-composition/recipe/launch-obsidian-with-policy.sh
CONTROL_GL_GPU=1
```

and vary only:

```text
VULKAN_POLICY_MODE=explicit-freedreno
```

versus:

```text
VULKAN_POLICY_MODE=implicit-discovery
```

The topology, survival, and maps gates remain the same.

## Evidence principle

This parameterization preserves the architecture rule:

```text
application feature mode
    !=
provider discovery/selection policy
```

The harness must be able to vary those inputs independently before the project can infer a final composition contract.
