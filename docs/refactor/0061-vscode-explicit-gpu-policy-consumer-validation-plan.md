# 0061 — VS Code Explicit GPU Policy Consumer Validation Plan

## Status

The Obsidian same-feature-mode provider-policy A/B and implicit loader-selection question are closed strongly enough for the current architecture stage.

The next consumer gate is VS Code.

Do not start with a simultaneous explicit-versus-implicit A/B.

First close the explicit-freedreno GPU-path control with:

```text
topology
survival
process-class graphics mappings
Vulkan loader selected-provider identity
```

Only after the explicit control is closed should the same feature mode be tested under implicit discovery.

## Why VS Code is a separate consumer gate

The current evidence already proves consumer-specific behavior:

```text
standalone Zink
    implicit/default -> FAIL

Obsidian Electron
    implicit/default -> LVP/llvmpipe selected -> PASS
```

VS Code must therefore be tested as its own consumer rather than inheriting the Obsidian result by analogy.

## Existing experiment adapter

The existing experiment adapter:

```text
experiments/glibc/vulkan-policy-composition/recipe/launch-vscode-with-policy.sh
```

already separates:

```text
GL_GPU
    application feature/argv mode

VULKAN_POLICY_MODE
    provider discovery/selection policy
```

For `GL_GPU=1` it adds:

```text
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
--disable-gpu-sandbox
--ignore-gpu-blocklist
--disable-gpu-vsync
```

The adapter applies experiment-local Vulkan policy after sourcing the current shared glibc environment.

Promoted launchers remain unchanged.

## Capture harness reuse

The proven Electron capture harness now accepts:

```text
APP_ENTRYPOINT
CONTROL_NAME
```

while preserving the historical Obsidian defaults.

VS Code uses:

```text
APP=$HOME/gl/apps/vscode
APP_ENTRYPOINT=$APP/bin/code
CONTROL_NAME="VS Code"
```

The following capture semantics remain unchanged:

```text
PPID-descendant process-tree discovery
main/zygote/renderer topology gate
wall-clock survival gate
final process map capture
unique object set generation
process-class observation counts
```

## First control

Inputs:

```text
CONTROL_GL_GPU=1
VULKAN_POLICY_MODE=explicit-freedreno
LIBGL_ALWAYS_SOFTWARE unset
VK_LOADER_DEBUG=all
```

Recommended bounded survival:

```text
60 seconds
```

This is long enough for stable Electron process topology and loader diagnostics without repeating the already completed 100-second Obsidian survival gate.

## Explicit control success criteria

### Workload gate

```text
topology PASS
main survives 60-second gate
no FATAL diagnostic
final process maps captured
```

### Graphics process relation gate

Expected hardware-tail evidence:

```text
gpu process maps provider-store libvulkan_freedreno.so
gpu process maps /dev/kgsl-3d0
```

Application-local and infrastructure mappings should be recorded rather than assumed identical to Obsidian.

### Loader selection gate

Strong success requires a loader-selected physical-device/provider identity compatible with the explicit hardware policy, for example:

```text
Turnip / Adreno physical-device identity
selected driver path resolving to provider-store Freedreno
```

Do not infer hardware selection solely from:

```text
VK_DRIVER_FILES present
Freedreno object mapped
KGSL mapped
```

The loader-selected provider identity is a separate evidence level.

## Evidence outputs

Required first-pass outputs:

```text
capture-control output
processes.tsv
mapped-objects.tsv
graphics-process-mappings.tsv
graphics-class-object-relations.tsv
loader selected-driver lines
physical-device identities
removed-driver set
selected-driver path resolution
```

Identity enrichment and semantic decomposition are not required before the graphics selection gate is interpreted.

If the mapped graph differs materially from the Obsidian composition, enrich and classify the VS Code object set before proceeding.

## Claim boundary

The VS Code explicit control can establish:

```text
application topology and bounded survival
process-class graphics mappings
loader-selected Vulkan provider identity
loader-visible physical-device identity
```

It does not establish:

```text
frame-level correctness equivalence
performance characteristics
pixel-output equivalence
all Chromium subsystem backend choices
```

Those stronger claims are unnecessary for the current policy-composition architecture question.

## Validation order

```text
1. VS Code explicit-freedreno GPU capture
2. explicit graphics process-class mapping report
3. explicit loader selection summary
4. interpret provider identity and path provenance
5. only if explicit control passes, run VS Code implicit-discovery GPU control
6. compare selected provider identity and process relations
7. compare Zink / Obsidian / VS Code consumer requirements
8. define minimum graphics composition contract
```

No promoted launcher or shared `gl/env` migration should occur before this consumer comparison is complete.
