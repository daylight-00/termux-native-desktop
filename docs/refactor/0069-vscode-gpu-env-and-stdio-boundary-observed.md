# 0069 — VS Code GPU Environment and stdio Boundary Observed

## Status

The bounded VS Code GPU observer-contract probe passed and produced two direct observations about the real Electron GPU subprocess:

```text
selected Vulkan-related environment keys:
    none observed

fd 0:
    /dev/null

fd 1:
    /dev/null

fd 2:
    /dev/null
```

The GPU process was directly identified as:

```text
$HOME/gl/apps/vscode/code --type=gpu-process ... --use-angle=vulkan ... --use-gl=angle ...
```

This result explains why `VK_LOADER_DEBUG` output was absent from the parent capture streams, but it also opens a more important policy-causality question.

The current evidence does not yet establish that the launch-scoped:

```text
VK_DRIVER_FILES
VK_ICD_FILENAMES
VK_LOADER_DEBUG
TND_EXPERIMENT_VULKAN_POLICY
```

were present in the GPU subprocess initial environment.

Therefore the project must not claim yet that:

```text
explicit-freedreno launch environment
    causally selected
GPU-process Freedreno
```

merely from the combination of launcher intent plus GPU-process mappings.

The correct current state is:

```text
explicit policy intent at launch:
    ESTABLISHED

GPU process maps Freedreno:
    PASS

GPU process maps KGSL:
    PASS

GPU subprocess selected environment keys:
    NONE OBSERVED

GPU subprocess stdio:
    /dev/null for fd 0/1/2

causal effect of scoped env policy on GPU provider selection:
    OPEN
```

## Evidence root

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-gpu-observer-contract-20260711-143625
```

## Probe result

The probe reported:

```text
VS Code GPU observer contract probe: PASS
```

GPU process:

```text
pid:
    30020

ppid at capture:
    29921

argv facts:
    --type=gpu-process
    --use-angle=vulkan
    --use-gl=angle
    --enable-features=...,Vulkan
    --disable-gpu-vsync
```

The argv evidence confirms the intended Electron/Chromium graphics feature mode.

It does not identify the provider-selection mechanism by itself.

## GPU environment observation

The selected-key report contained only its header:

```text
key    value
```

No values were observed for:

```text
VK_LOADER_DEBUG
VK_DRIVER_FILES
VK_ICD_FILENAMES
TND_EXPERIMENT_VULKAN_POLICY
LD_LIBRARY_PATH
LD_PRELOAD
LIBGL_ALWAYS_SOFTWARE
MESA_LOADER_DRIVER_OVERRIDE
```

The first GPU-only observer probe treated a readable `/proc/<pid>/environ` with zero selected matches as a successful capture without separately recording total environment-entry count or read state.

That is useful but not yet sufficient to establish the exact environment boundary with maximum confidence.

The observer has therefore been hardened to record:

```text
READ_OK / READ_FAILED
full environment entry count
selected-key count
```

and to avoid noisy `/proc/<pid>/cmdline` races during cleanup.

Hardening commit:

```text
fa605ff113dc6b942fc37fcd95bf50057f9f9860
```

## GPU stdio observation

The GPU process file descriptors were:

```text
fd 0 -> /dev/null
fd 1 -> /dev/null
fd 2 -> /dev/null
```

This directly explains why the parent launch capture files:

```text
launch.stdout
launch.stderr
```

cannot be assumed to contain child-local Vulkan loader diagnostics.

Observed parent capture state:

```text
launch.stdout:
    0 bytes

launch.stderr:
    launcher policy echo
    Electron/Chromium option warnings
    no selected-driver loader diagnostics
```

The earlier absence of loader diagnostics is therefore no longer mysterious at the stdio level.

## Architecture consequence

The scoped Vulkan policy experiment originally asks whether provider-selection responsibility can move from unconditional shared `gl/env` policy to the smallest valid launch-composition scope.

For VS Code, the current evidence now separates three facts:

```text
1. launch adapter composes explicit-freedreno environment intent;

2. final GPU process maps provider-store Freedreno and KGSL;

3. the GPU subprocess itself does not expose those selected env keys in the first observer result and has stdio detached to /dev/null.
```

Facts 1 and 2 are not enough to infer the mechanism connecting them.

Possible mechanisms still include:

```text
A. policy exists in main and is removed before GPU exec;

B. policy exists through a zygote or broker stage and provider choice is passed by another mechanism;

C. GPU process performs provider discovery without the explicit env policy and happens to reach Freedreno;

D. the first environment observer under-reported due to read semantics or timing and needs cross-process verification.
```

No one mechanism is established yet.

## Claim correction

The previous working phrase:

```text
VS Code explicit-freedreno control
```

must currently be interpreted as:

```text
VS Code control launched under explicit-freedreno policy intent
```

not yet as:

```text
proved causal selection of Freedreno by the GPU subprocess through inherited VK_* variables
```

The workload and mapping results remain valid:

```text
topology PASS
60-second survival PASS
GPU -> vendor-local libvulkan.so.1
GPU -> provider-store libvulkan_freedreno.so
GPU -> /dev/kgsl-3d0
```

Only the causal policy mechanism remains open.

## Next bounded gate

The next experiment must locate the environment boundary across the real process classes.

Added:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    probe-vscode-policy-env-boundary.sh
```

Commit:

```text
08129dbb1e2ab9aeaee587e0dd0a6bbd289c2076
```

The probe records first successful observations for process classes including:

```text
launch-wrapper
node-cli
main
zygote
gpu
utility
renderer
crashpad
```

For each observed PID it records:

```text
pid / ppid / class / argv0 / cmdline
initial environment read state
full environment entry count
selected Vulkan-related keys
fd 0/1/2 targets
```

The required gate is:

```text
main environment READ_OK
zygote environment READ_OK
gpu environment READ_OK
```

This allows direct comparison of:

```text
main
    -> zygote
        -> gpu
```

without assuming where sanitation or reconstruction occurs.

## Expected decision branches

### Branch A — main has VK_*; zygote and GPU do not

Interpretation:

```text
policy environment is lost or deliberately sanitized before/at child process creation
```

Next question:

```text
how the GPU process nevertheless reaches Freedreno
```

Possible work:

```text
compare explicit and implicit controls only after proving the provider outcome differs,
or inspect a consumer-specific provider handoff mechanism.
```

### Branch B — main and zygote have VK_*; GPU does not

Interpretation:

```text
GPU-specific child boundary is the policy-loss point
```

Next work should stay narrowly focused on GPU child construction.

### Branch C — main, zygote, and GPU all have VK_*

Interpretation:

```text
first GPU-only environment observer was insufficient
```

Then the stdio `/dev/null` result still explains loader-log absence, while policy inheritance remains plausible.

### Branch D — main itself lacks VK_*

Interpretation:

```text
policy intent is lost before the actual Electron application main process
```

Then the launcher/CLI handoff boundary becomes the next target.

## Current gate state

```text
VS Code explicit-intent workload:
    PASS

GPU process -> vendor-local Vulkan loader:
    ESTABLISHED

GPU process -> Freedreno:
    PASS

GPU process -> KGSL:
    PASS

GPU fd 0/1/2:
    /dev/null

parent capture suitability for child loader logs:
    REJECTED

GPU selected Vulkan env keys:
    NONE OBSERVED IN FIRST PROBE

cross-process policy env boundary:
    NEXT GATE

causal scoped-policy effect:
    OPEN

VS Code implicit-discovery control:
    STILL BLOCKED
```

## Stop line

Do not yet:

```text
claim explicit VK_* inheritance into the GPU process
claim VK_LOADER_DEBUG failure
run implicit-discovery as a causal A/B before the explicit mechanism is understood
change promoted launcher
change shared gl/env
replace vendor-local libvulkan.so.1
force another Vulkan loader into VS Code
add invasive tracing
```

First locate the real environment boundary across main, zygote, and GPU process classes.
