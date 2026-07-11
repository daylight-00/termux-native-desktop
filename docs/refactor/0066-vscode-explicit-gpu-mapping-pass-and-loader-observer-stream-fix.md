# 0066 — VS Code Explicit GPU Mapping Pass and Loader Observer Stream Fix

## Status

The repaired VS Code explicit-Freedreno control now has direct process-class mapping evidence for the explicit hardware provider tail.

Observed:

```text
gpu process
    -> app-local libEGL.so
    -> app-local libGLESv2.so
    -> app-local libvulkan.so.1
    -> provider-store libvulkan_freedreno.so
    -> rootfs VkLayer_MESA_device_select
    -> rootfs libgbm
    -> /dev/kgsl-3d0
```

Therefore the graphics process-relation half of the `0061` explicit-control gate passes.

The loader-selected provider half remains open because the first loader-debug summarization read only `launch.stderr` and produced zero loader signals. The capture harness stores `launch.stdout` and `launch.stderr` separately, so the observer has been corrected to inspect both streams before any workload rerun is considered.

## Evidence root

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-explicit-adopted-20260711-134601
```

This is the same evidence root recorded in `0065`.

No workload rerun is required for the next step.

## Graphics process mapping result

The reporter:

```text
experiments/glibc/selected-obsidian-closure/recipe/report-graphics-process-mappings.sh
```

passed against the existing evidence root.

The unique GPU-process relations are:

```text
gpu -> $HOME/gl/apps/vscode/libEGL.so
gpu -> $HOME/gl/apps/vscode/libGLESv2.so
gpu -> $HOME/gl/apps/vscode/libvulkan.so.1
gpu -> $HOME/gl/opt/mesa-glibc-26.1.4-full/lib/libvulkan_freedreno.so
gpu -> rootfs libVkLayer_MESA_device_select.so
gpu -> rootfs libgbm.so.1.0.0
gpu -> /dev/kgsl-3d0
```

Other final process classes map rootfs GBM, but the captured explicit hardware driver and KGSL device-node relations are owned by the `gpu` process in this final map set.

## Gate interpretation

The `0061` plan separated:

```text
1. graphics process relation
2. loader selected-provider identity
```

The first level is now closed for this control:

```text
GPU process maps provider-store Freedreno:
    PASS

GPU process maps KGSL device node:
    PASS
```

This is stronger than the earlier object-set-only statement because process-class ownership is now explicit.

It still does not prove the second level by itself:

```text
Freedreno object mapped
    + KGSL mapped
    != by itself
loader-selected provider identity
```

The project continues to keep those evidence levels separate.

## First loader-summary result

The original loader summary reported:

```text
loader_version_lines          0
icd_manifest_lines            0
physical_device_sort_lines    0
driver_removal_lines          0
selected_driver_lines         0
llvmpipe_lines                0
turnip_lines                  0
gfxstream_lines               0
lvp_lines                     0
```

All selected-driver, physical-device, removed-driver, and path-resolution outputs were empty.

Correct interpretation:

```text
loader-selection evidence from the inspected stream:
    NOT OBSERVED
```

not:

```text
Vulkan loader did not run
```

and not:

```text
Freedreno was not selected
```

The process maps independently prove Vulkan-facing application libraries, the Freedreno driver object, and KGSL device participation in the GPU process.

## Observer defect

The existing summarizer read only:

```text
$CONTROL_OUT/launch.stderr
```

while the capture harness records separately:

```text
$CONTROL_OUT/launch.stdout
$CONTROL_OUT/launch.stderr
```

The next smallest action is therefore to inspect both existing streams before designing any new runtime instrumentation.

The summarizer has been updated in commit:

```text
b57fc79e4c4b3b904da397c99de8228cb3e669a3
```

New behavior:

```text
read launch.stdout when present
read launch.stderr when present
combine both only for filtered loader analysis
record per-stream bytes and signal counts
preserve existing selected-driver and physical-device outputs
```

New provenance output:

```text
loader-selection-debug/input-streams.tsv
```

This allows a later result to distinguish:

```text
loader signals in stdout
loader signals in stderr
signals absent from both captured streams
```

## Why no workload rerun yet

The raw control already passed:

```text
causal main adoption
required topology
60-second survival
final process maps
GPU-process Freedreno relation
GPU-process KGSL relation
```

Only downstream interpretation failed to observe loader signals.

The project evidence rule therefore applies:

```text
reuse valid raw evidence
    -> repair downstream observer
    -> rerun summarization only
```

Do not repeat the 60-second GUI workload unless both stored output streams prove insufficient.

## Immediate next step

After fast-forwarding the branch, rerun only:

```text
CONTROL_OUT=$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-explicit-adopted-20260711-134601 \
  bash experiments/glibc/vulkan-policy-composition/recipe/summarize-obsidian-loader-debug.sh
```

Then inspect:

```text
loader-selection-debug/input-streams.tsv
loader-selection-debug/loader-debug-counts.tsv
loader-selection-debug/selected-driver-lines.txt
loader-selection-debug/physical-device-identities.txt
loader-selection-debug/removed-drivers.txt
loader-selection-debug/selected-driver-path-resolution.tsv
loader-selection-debug/driver-instance-warnings.txt
```

## Decision branches after corrected summarization

### Branch A — loader signals exist in stored stdout

```text
parse selected provider identity
resolve selected driver path provenance
close or refine the explicit loader-selection gate
```

### Branch B — loader signals exist in stored stderr under an unhandled format

```text
repair parser pattern only
reuse the same raw evidence again
```

### Branch C — both streams contain zero loader signals

```text
record observer-channel absence
inspect the mapped app-local Vulkan loader identity and debug capability
then design one bounded consumer-specific selection probe
```

Do not jump directly to invasive tracing or promoted runtime changes.

## Revised explicit-control state

```text
process handoff:
    CLOSED

causal main adoption:
    CLOSED

repaired control workload gate:
    PASS

graphics process relation:
    PASS

GPU -> provider-store Freedreno:
    PASS

GPU -> KGSL:
    PASS

loader selected-provider identity:
    OPEN / OBSERVER CORRECTION IN PROGRESS

implicit-discovery VS Code control:
    BLOCKED UNTIL EXPLICIT CONTROL INTERPRETATION CLOSES
```

## Claim boundary

This result establishes:

```text
VS Code GPU process ownership of the captured explicit hardware provider/device relation
```

It does not yet establish:

```text
loader-selected physical-device identity
loader-selected driver path identity
rendering submission
pixel correctness
performance
```

No promoted launcher, shared `gl/env`, or graphics provider policy is changed by this result or observer fix.
