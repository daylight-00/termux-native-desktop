# 0065 — VS Code Explicit Freedreno Repaired Control Workload Gates Passed

## Status

The repaired VS Code explicit-Freedreno control has now passed the workload-side gates that were previously blocked by the process-root ownership defect.

The control established:

```text
causal main-process adoption: PASS
topology gate: PASS
60-second survival gate: PASS
final process map capture: PASS
control capture: PASS
```

The graphics-provider interpretation gate is still open.

This result closes the question of whether the `0064` causal main-process adoption repair is sufficient for the real VS Code control workflow. It does not yet close selected Vulkan provider identity.

## Repository and branch context

```text
repository:
    daylight-00/termux-native-desktop

branch:
    refactor/module-package-layout

canonical device checkout:
    $HOME/projects/termux-native-desktop
```

The device fast-forwarded from:

```text
580b397
```

to:

```text
3b9f3fc
```

before running the repaired control.

## Evidence root

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-explicit-adopted-20260711-134601
```

## Control inputs

The run used the repaired causal adoption contract:

```text
APP=$HOME/gl/apps/vscode
APP_ENTRYPOINT=$APP/bin/code
CONTROL_NAME="VS Code"
MAIN_PROCESS_EXECUTABLE=$APP/code
CONTROL_GL_GPU=1
VULKAN_POLICY_MODE=explicit-freedreno
LIBGL_ALWAYS_SOFTWARE unset
VK_LOADER_DEBUG=all
STARTUP_TIMEOUT_SECONDS=30
POLL_SLEEP_SECONDS=0.1
SURVIVAL_SECONDS=60
PROGRESS_INTERVAL_SECONDS=10
```

The experiment launcher was:

```text
experiments/glibc/vulkan-policy-composition/recipe/launch-vscode-with-policy.sh
```

The shared capture harness was:

```text
experiments/glibc/selected-obsidian-closure/recipe/capture-control.sh
```

No promoted VS Code launcher, shared `gl/env`, or provider policy was changed for this control.

## Main-process adoption result

The harness reported:

```text
launch pid:
    22279

adopted main pid:
    22503

adopted argv0:
    $HOME/gl/apps/vscode/code

recorded PPID at adoption log time:
    1
```

This is compatible with the process-handoff behavior proven in `0064`:

```text
launch wrapper
    -> Electron/Node CLI
    -> Electron application main
    -> main reparents to PID 1 and survives
```

The important validation result is not the numeric PPID value at one later observation point. It is that the repaired harness successfully selected the exact main-process executable under the bounded causal adoption contract and then used the adopted PID for the remaining topology, survival, and map-capture workflow.

## Topology gate

The topology gate passed:

```text
topology gate: PASS
required classes: main renderer zygote
main pid: 22503
elapsed seconds: 6
```

The final captured process set was:

```text
22503   main
22518   zygote
22519   zygote
22774   gpu
22787   utility
22891   renderer
23122   utility
23123   utility
23282   utility
24493   helper
26523   renderer
```

Final class cardinalities therefore include:

```text
main        1
zygote      2
gpu         1
utility     4
helper      1
renderer    2
```

The required early topology contract:

```text
main + renderer + zygote
```

is satisfied.

## Survival gate

The bounded 60-second survival gate passed:

```text
survival gate: PASS
elapsed seconds: 62
```

Progress output showed continued observation through the bounded interval:

```text
15s elapsed, 45s remaining
30s elapsed, 30s remaining
43s elapsed, 17s remaining
53s elapsed, 7s remaining
```

This closes the `0064` open question of whether the adopted VS Code application main remains viable under the repaired shared control harness for the bounded control interval.

## Captured object-set summary

The control capture reported these unique mapped-path class counts:

```text
APP_LOCAL        15
OTHER_ABSOLUTE   29
PREFIX_GLIBC     50
ROOTFS_PROVIDER  59
```

These are capture observations only.

They do not by themselves identify:

```text
selected Vulkan provider
selected physical device
hardware versus software rendering identity
semantic provider ownership boundary
```

The project evidence discipline remains:

```text
object mapped
    !=
provider selected
```

and:

```text
GL_GPU=1
    !=
hardware acceleration identity
```

## Process observation counts

The capture reported:

```text
gpu       13
helper    10
launcher   1
main      13
renderer  14
utility   49
zygote    26
```

These counts show repeated bounded observation of the adopted topology. They are not performance metrics and should not be interpreted as process lifetime ratios.

## Revised gate state

```text
wrapper semantics:
    CLOSED

launch-root lifetime:
    CLOSED

CLI-to-application-main handoff:
    CLOSED

causal main adoption requirement:
    PROVEN

repaired shared-harness main adoption:
    VALIDATED BY REAL CONTROL

VS Code explicit control topology:
    PASS

VS Code explicit control 60-second survival:
    PASS

final map capture:
    PASS

GPU-process graphics mapping relation:
    CAPTURED BUT NOT YET INTERPRETED

loader-selected Vulkan provider:
    NOT YET INTERPRETED

loader-visible physical-device identity:
    NOT YET INTERPRETED
```

## What this result proves

The current evidence establishes:

```text
1. the `0064` causal main-process adoption repair works in the real VS Code control workflow;
2. the repaired harness can establish the required VS Code Electron topology;
3. the adopted main survives the bounded 60-second interval;
4. the final process set and process maps are captured successfully;
5. the earlier header-only final topology was a harness ownership false negative, not evidence that VS Code failed to create or sustain its Electron application topology.
```

## What this result does not prove

This result does not yet establish:

```text
provider-store Freedreno mapped by the GPU process
/dev/kgsl-3d0 mapped by the GPU process
Turnip / Adreno selected by the Vulkan loader
selected driver path provenance
rendering command submission
pixel correctness
performance characteristics
frame-level equivalence with another policy
```

Those questions belong to the graphics process-relation and loader-selection analysis of this same raw evidence root.

## Immediate next analysis

Reuse the existing evidence root.

Do not rerun the 60-second workload for downstream reporting.

First derive the graphics process relations:

```text
CONTROL_OUT=$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-explicit-adopted-20260711-134601 \
  bash experiments/glibc/selected-obsidian-closure/recipe/report-graphics-process-mappings.sh
```

Then summarize loader selection from the already captured `launch.stderr`:

```text
CONTROL_OUT=$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-explicit-adopted-20260711-134601 \
  bash experiments/glibc/vulkan-policy-composition/recipe/summarize-obsidian-loader-debug.sh
```

The helper name retains its historical Obsidian origin, but its current implementation consumes a generic `CONTROL_OUT/launch.stderr` path and can summarize this VS Code control without changing promoted runtime policy.

## Success criteria for the remaining explicit-control gate

The current validation plan requires two independent evidence levels.

### Graphics process relation

Expected explicit hardware-tail relation:

```text
gpu process
    -> provider-store libvulkan_freedreno.so
    -> /dev/kgsl-3d0
```

### Loader selected-provider identity

Strong closure requires loader-level evidence compatible with:

```text
selected physical device:
    Turnip / Adreno

selected driver path:
    resolves to the explicit Freedreno provider-store object
```

Do not infer the second level from the first.

## Decision

The repaired VS Code explicit-Freedreno control has passed its workload-side gates.

Proceed by reusing the existing raw evidence for:

```text
graphics process-class mapping report
    -> loader selection summary
    -> provider identity and path provenance interpretation
```

Only after the explicit provider-selection gate is closed should the project run the VS Code implicit-discovery control.

No promoted launcher, shared `gl/env`, or graphics provider policy should change before the consumer comparison is complete.
