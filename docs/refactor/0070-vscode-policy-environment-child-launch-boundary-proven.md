# 0070 — VS Code Policy Environment Child-Launch Boundary Proven

## Status

The VS Code cross-process policy-environment boundary probe passed and located the policy environment discontinuity precisely enough for the current architecture question.

Observed process-class matrix:

```text
class            env entries    selected policy/debug keys
launch-wrapper   83             4
node-cli         85             4
main             88             4
crashpad         90             4
zygote            0             0
zygote            0             0
gpu               1             0
utility           1             0
renderer          1             0
```

The four selected keys present in launcher, node CLI, main, and crashpad were:

```text
TND_EXPERIMENT_VULKAN_POLICY=explicit-freedreno
VK_DRIVER_FILES=<Freedreno ICD JSON>
VK_ICD_FILENAMES=<Freedreno ICD JSON>
VK_LOADER_DEBUG=all
```

The ordinary Chromium child-process classes did not expose those keys.

This closes the broad boundary question:

```text
launch adapter
    -> node CLI
        -> Electron main
```

preserves the scoped policy environment, while:

```text
Electron main
    -> ordinary Chromium child-process launch paths
```

produce a drastically reduced process environment that does not contain the selected policy/debug variables.

## Evidence root

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-policy-env-boundary-20260711-144312
```

Probe status:

```text
PASS
```

## Process graph observed

The bounded probe directly observed:

```text
launch-wrapper  pid 5727
    -> node-cli pid 5740
        -> main pid 5899
            -> zygote pid 5926
            -> zygote pid 5927
            -> gpu pid 6134
            -> utility pid 6162

zygote pid 5927
    -> renderer pid 6306

crashpad pid 6055
    -> observed reparented to pid 1 by capture time
```

The GPU process was a direct child of the Electron main at the captured boundary:

```text
main 5899
    -> gpu 6134
```

The utility process was also a direct child of the main:

```text
main 5899
    -> utility 6162
```

The renderer was observed below a zygote:

```text
zygote 5927
    -> renderer 6306
```

This matters because the environment reduction is not explainable merely as one zygote-only inheritance event.

## Launcher to main policy preservation

The following classes retained the four selected keys:

```text
launch-wrapper
node-cli
main
```

The Electron main therefore directly proves that the policy variables survive the previously diagnosed VS Code CLI handoff:

```text
shell wrapper
    -> Electron/Node CLI
        -> Electron application main
```

The earlier concern:

```text
policy may disappear before the actual Electron main
```

is rejected for this control.

The exact main observation was:

```text
pid: 5899
class: main
environment state: READ_OK
environment entries: 88
selected keys: 4
```

with:

```text
TND_EXPERIMENT_VULKAN_POLICY=explicit-freedreno
VK_DRIVER_FILES=<provider-store Freedreno ICD JSON>
VK_ICD_FILENAMES=<provider-store Freedreno ICD JSON>
VK_LOADER_DEBUG=all
```

## Chromium ordinary child environment boundary

The two zygotes were read successfully and exposed zero environment entries:

```text
zygote 5926:
    READ_OK
    entry_count=0
    selected_key_count=0

zygote 5927:
    READ_OK
    entry_count=0
    selected_key_count=0
```

The GPU process was also read successfully:

```text
gpu 6134:
    READ_OK
    entry_count=1
    selected_key_count=0
```

The utility and renderer process observations were structurally similar:

```text
utility:
    READ_OK
    entry_count=1
    selected_key_count=0

renderer:
    READ_OK
    entry_count=1
    selected_key_count=0
```

Therefore the current evidence supports:

```text
ordinary Chromium child-process launch paths
    reconstruct or drastically reduce environment state
```

at least for the captured Electron build and this Android/Termux glibc execution context.

The evidence does not yet identify the internal implementation mechanism or the identity of the one retained entry in the one-entry child environments.

Those details are not required before the next architecture-discriminating A/B.

## Crashpad contrast

Crashpad retained the four selected keys:

```text
crashpad 6055:
    READ_OK
    entry_count=90
    selected_key_count=4
```

This is a useful control.

It rejects the overly broad interpretation:

```text
all processes after Electron main lose the policy environment
```

The stronger observed statement is:

```text
policy environment preservation differs by child-launch contract
```

with the captured contrast:

```text
crashpad launch path:
    policy keys preserved

ordinary Chromium zygote/gpu/utility/renderer paths:
    policy keys absent
```

Do not generalize this result beyond the captured process classes and build without additional evidence.

## stdio boundary

The process fd map also shows a sharp transition.

### Launcher and node CLI

```text
launch-wrapper:
    fd 0 -> /dev/null
    fd 1 -> launch.stdout
    fd 2 -> launch.stderr

node-cli:
    fd 0 -> /dev/null
    fd 1 -> launch.stdout
    fd 2 -> launch.stderr
```

### Electron main and ordinary children

```text
main:
    fd 0 -> /dev/null
    fd 1 -> /dev/null
    fd 2 -> /dev/null

zygote:
    fd 0/1/2 -> /dev/null

gpu:
    fd 0/1/2 -> /dev/null

utility:
    fd 0/1/2 -> /dev/null

renderer:
    fd 0/1/2 -> /dev/null
```

Therefore the parent `launch.stdout` and `launch.stderr` files are valid observers for the wrapper and Node CLI stages but are not valid observers for the Electron main or its ordinary child processes in this launch topology.

This explains the absence of GPU-process Vulkan loader debug output from those parent capture files.

## Revised policy-causality interpretation

Current proven facts:

```text
1. explicit-freedreno policy environment reaches Electron main;

2. ordinary Chromium child processes do not expose those VK_* policy keys;

3. the GPU process maps the vendor-local Vulkan loader;

4. the GPU process maps provider-store libvulkan_freedreno.so;

5. the GPU process maps /dev/kgsl-3d0;

6. topology and 60-second survival pass.
```

The missing causal edge is:

```text
how does changing provider policy at Electron-main scope affect
GPU-process provider composition when the child process environment
itself no longer exposes the VK_* variables?
```

Possible mechanisms include:

```text
policy consumed before child launch and effect transmitted by another mechanism;
provider choice performed in a process or component with policy access;
child launch receives provider-relevant state outside the inspected environment keys;
provider composition remains the same because implicit discovery also reaches Freedreno.
```

The current evidence does not choose among these mechanisms.

## Architecture consequence

The scope question is now more subtle than:

```text
put VK_DRIVER_FILES in the application launcher
```

For this VS Code/Electron consumer, the architecture must distinguish:

```text
application-main policy scope
```

from:

```text
GPU-child environment scope
```

because they are observably not the same environment domain.

This does not make launch-scoped composition invalid.

It means that the correct validation contract must be behavioral:

```text
change one application-main provider-policy input
    -> observe whether GPU provider composition changes
```

rather than assuming successful inheritance of environment variables into every child process.

## Next architecture-discriminating experiment

The next highest-information experiment is the same-consumer same-feature-mode A/B that was previously blocked.

The explicit side is already captured:

```text
GL_GPU=1
VULKAN_POLICY_MODE=explicit-freedreno
LIBGL_ALWAYS_SOFTWARE unset

result:
    topology PASS
    survival PASS
    GPU -> provider-store Freedreno
    GPU -> KGSL
```

Now run the same VS Code GPU-feature control with only provider policy changed:

```text
GL_GPU=1
VULKAN_POLICY_MODE=implicit-discovery
LIBGL_ALWAYS_SOFTWARE unset
```

Keep:

```text
same application payload
same launcher adapter
same capture harness
same main-process adoption contract
same ANGLE/Vulkan feature flags
same 60-second survival gate
```

Then compare:

```text
topology
survival
GPU graphics process relations
mapped ICD/provider objects
KGSL presence
alternate software/discovery providers
```

This experiment does not by itself replace selected-provider proof with map presence.

Its purpose is narrower:

```text
does the application-main provider-policy input causally change
GPU-process provider composition for this consumer?
```

Possible outcomes:

### Outcome A — implicit changes GPU provider composition

```text
explicit intent:
    GPU -> Freedreno + KGSL

implicit discovery:
    GPU -> different provider set and/or no KGSL
```

Then the scoped application-main policy input has a demonstrated causal effect on downstream GPU composition even though the child environment is reconstructed.

The remaining selected-provider identity question can then be addressed within each observed composition.

### Outcome B — implicit preserves the same Freedreno/KGSL composition

Then the current explicit environment policy may be redundant for this VS Code consumer under the present runtime discovery state.

Do not assume global redundancy; this would be a consumer- and runtime-state-specific result.

### Outcome C — implicit workload fails before stable topology/survival

Then explicit application-main policy remains behaviorally required for this consumer under the tested runtime state, even if the exact child handoff mechanism is not yet identified.

## Current gate state

```text
VS Code explicit-intent workload:
    PASS

policy reaches node CLI:
    PASS

policy reaches Electron main:
    PASS

ordinary child VK_* inheritance:
    NOT OBSERVED

ordinary child environment reconstruction/reduction boundary:
    PROVEN FOR CAPTURED CLASSES

crashpad policy preservation contrast:
    OBSERVED

GPU -> vendor-local Vulkan loader:
    ESTABLISHED

GPU -> Freedreno:
    PASS

GPU -> KGSL:
    PASS

application-main policy causal effect on GPU composition:
    NEXT A/B GATE

VS Code implicit-discovery control:
    NOW UNBLOCKED AS THE NEXT DISCRIMINATING EXPERIMENT
```

## Stop line

Do not yet:

```text
change promoted launcher
change shared gl/env
force VK_* into Chromium child environments
replace the vendor-local Vulkan loader
add invasive tracing
claim selected-provider identity solely from map presence
```

First run the same-consumer implicit-discovery control and compare downstream GPU composition.
