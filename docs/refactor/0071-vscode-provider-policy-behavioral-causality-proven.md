# 0071 — VS Code Provider-Policy Behavioral Causality Proven

## Status

The same-consumer same-feature-mode VS Code A/B now demonstrates that changing only the application-main Vulkan provider-policy input changes the downstream GPU-process provider composition.

The compared controls keep:

```text
same VS Code payload
same Electron/Chromium build
same GL_GPU=1 application feature mode
same ANGLE/Vulkan flags
same main-process adoption contract
same capture harness
same topology contract
same 60-second survival contract
LIBGL_ALWAYS_SOFTWARE unset
```

The changed policy dimension is:

```text
explicit intent:
    VK_DRIVER_FILES=<Freedreno ICD>
    VK_ICD_FILENAMES=<Freedreno ICD>

implicit discovery:
    VK_DRIVER_FILES unset
    VK_ICD_FILENAMES unset
```

Observed GPU-process composition:

```text
explicit intent:
    app-local libEGL.so
    app-local libGLESv2.so
    app-local libvulkan.so.1
    provider-store libvulkan_freedreno.so
    rootfs libVkLayer_MESA_device_select.so
    rootfs libgbm.so.1.0.0
    /dev/kgsl-3d0

implicit discovery:
    app-local libEGL.so
    app-local libGLESv2.so
    app-local libvulkan.so.1
    rootfs libVkLayer_MESA_device_select.so
    rootfs libgbm.so.1.0.0
    rootfs libvulkan_gfxstream.so
    rootfs libvulkan_lvp.so
```

The implicit control does not map:

```text
libvulkan_freedreno.so
/dev/kgsl-3d0
```

This closes the behavioral causal gate:

```text
application-main provider-policy input
    -> changes downstream GPU provider/device composition
```

even though ordinary Chromium child processes reconstruct or drastically reduce their visible environment and do not expose the original `VK_*` variables.

## Evidence roots

Explicit control:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-explicit-adopted-20260711-134601
```

Implicit control:

```text
$VS_IMPLICIT_OUT
```

The exact implicit evidence-root pathname was not included in the pasted report excerpt. It is retained in the device shell variable and will be captured by the comparison receipt described below.

## Implicit launch identity

The implicit control launch stderr records:

```text
experiment Vulkan policy: implicit-discovery
GL_GPU=1
VK_DRIVER_FILES=<unset>
```

The VS Code application feature flags remain:

```text
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
--disable-gpu-vsync
```

The main process was selected by the established exact executable contract:

```text
main process selection:
    descendant argv0=$HOME/gl/apps/vscode/code
```

Observed main selection:

```text
pid: 11794
ppid at selection: 1
selection mode: descendant-argv0
```

The reparented PPID is consistent with the previously proven VS Code CLI/main handoff and does not invalidate the causal ownership proof.

## Explicit GPU relation

The explicit-intent control previously established:

```text
gpu -> $HOME/gl/apps/vscode/libEGL.so
gpu -> $HOME/gl/apps/vscode/libGLESv2.so
gpu -> $HOME/gl/apps/vscode/libvulkan.so.1
gpu -> $HOME/gl/opt/mesa-glibc-26.1.4-full/lib/libvulkan_freedreno.so
gpu -> rootfs libVkLayer_MESA_device_select.so
gpu -> rootfs libgbm.so.1.0.0
gpu -> /dev/kgsl-3d0
```

The hardware provider and device-node relation was therefore:

```text
gpu -> Freedreno -> KGSL
```

## Implicit GPU relation

The implicit-discovery control observed:

```text
gpu -> $HOME/gl/apps/vscode/libEGL.so
gpu -> $HOME/gl/apps/vscode/libGLESv2.so
gpu -> $HOME/gl/apps/vscode/libvulkan.so.1
gpu -> rootfs libVkLayer_MESA_device_select.so
gpu -> rootfs libgbm.so.1.0.0
gpu -> rootfs libvulkan_gfxstream.so
gpu -> rootfs libvulkan_lvp.so
```

Not observed in the implicit GPU relation:

```text
provider-store libvulkan_freedreno.so
/dev/kgsl-3d0
```

Therefore implicit discovery does not preserve the explicit hardware-provider/device composition in this captured VS Code runtime state.

## Shared front half and policy-dependent tail

The A/B supports the same architecture shape previously seen in the Obsidian consumer:

```text
stable consumer-local graphics front half
    + application-main provider-policy input
    -> policy-dependent downstream provider tail
```

For VS Code the stable front half is:

```text
app-local libEGL.so
app-local libGLESv2.so
vendor payload-local libvulkan.so.1
```

The explicit provider tail is:

```text
provider-store Freedreno
KGSL
```

The implicit discovery tail is:

```text
rootfs Gfxstream
rootfs Lavapipe
no mapped KGSL relation
```

This result strengthens the architectural conclusion that provider selection is not an unconditional world-baseline property.

It is a consumer composition input whose downstream effect must be validated against the real workload and child-process model.

## Causal interpretation

The cross-process environment probe established:

```text
explicit VK_* reaches Electron main
ordinary Chromium child processes do not expose those variables
```

The current A/B adds:

```text
changing the Electron-main provider-policy input
changes the GPU-process provider/device map
```

Therefore direct child environment inheritance is not required as the architecture's proof contract.

The valid behavioral contract is:

```text
controlled application-main policy input
    + same consumer feature mode
    -> reproducibly different downstream provider composition
```

The internal Chromium/ANGLE transfer mechanism remains unspecified.

The architecture does not need to force `VK_*` variables into ordinary child environments merely to make the causal effect visible.

## What this proves

This result proves for the captured VS Code consumer and runtime state:

```text
1. explicit and implicit modes are behaviorally distinct;

2. explicit intent yields a GPU-process Freedreno/KGSL composition;

3. implicit discovery yields a GPU-process Gfxstream/LVP composition;

4. the difference is downstream of one controlled provider-policy input;

5. the explicit provider policy is not redundant for preserving the hardware-provider composition;

6. application-main policy scope is behaviorally meaningful despite child environment reconstruction.
```

## What this does not prove

The map relation does not by itself prove:

```text
which implicit provider created the selected Vulkan physical device;
whether LVP or Gfxstream was the final selected provider;
whether every mapped driver completed instance/device creation;
rendering submission identity;
pixel correctness;
performance;
```

Both:

```text
libvulkan_lvp.so
libvulkan_gfxstream.so
```

are mapped by the implicit GPU process.

Do not choose one as the selected provider solely from map presence.

## Workload gate note

The final graphics relation files are produced from `mapped-objects.tsv` after the capture harness has passed topology and survival gates and performed final map capture.

A machine-readable comparison receipt has nevertheless been added to verify both control status files and relation deltas directly from the two evidence roots.

Added:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    compare-vscode-vulkan-policy-controls.sh
```

Commit:

```text
ec05180aeefccd8e46170b9eac34bb83430c6a08
```

The receipt requires both controls to have:

```text
topology.status=PASS
survival.status=PASS
maps-capture.status=PASS
```

and validates:

```text
explicit GPU Freedreno present
explicit GPU KGSL present
explicit GPU LVP absent
explicit GPU Gfxstream absent

implicit GPU LVP present
implicit GPU Gfxstream present
implicit GPU Freedreno absent
implicit GPU KGSL absent

bidirectional relation delta present
```

## Immediate next step

Run the comparison receipt against the existing evidence roots without repeating either GUI workload.

The receipt will record:

```text
exact explicit evidence root
exact implicit evidence root
control status matrix
common graphics relations
explicit-only graphics relations
implicit-only graphics relations
comparison gate states
```

After the receipt passes, the next unresolved gate is narrower:

```text
which implicit provider is actually selected by the VS Code/ANGLE Vulkan path?
```

That selected-provider question requires a consumer-level observer other than parent stdout/stderr because the Electron main and ordinary child stdio descriptors are `/dev/null` in the captured launch topology.

## Current gate state

```text
VS Code explicit-intent workload:
    PASS

VS Code implicit-discovery workload:
    FINAL MAP EVIDENCE PRESENT

application feature-mode equality:
    PASS

policy input difference:
    PASS

explicit GPU -> Freedreno:
    PASS

explicit GPU -> KGSL:
    PASS

implicit GPU -> Gfxstream:
    PASS

implicit GPU -> LVP:
    PASS

implicit GPU -> Freedreno:
    ABSENT

implicit GPU -> KGSL:
    ABSENT

application-main policy behavioral causality:
    PROVEN

implicit selected-provider identity:
    OPEN

promoted migration transaction:
    STILL BLOCKED
```

## Stop line

Do not yet:

```text
claim LVP is selected solely because it is mapped;
claim Gfxstream is selected solely because it is mapped;
change promoted VS Code launcher;
change shared gl/env;
force provider policy into ordinary Chromium child environments;
replace the vendor-local Vulkan loader;
remove explicit provider composition from VS Code;
```

First produce the machine-readable A/B receipt, then select the smallest consumer-level actual-selection observer.
