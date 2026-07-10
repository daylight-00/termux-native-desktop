# Vulkan Policy Composition Experiment

## Status

Active architecture-discrimination experiment.

Current validation state:

```text
policy identity gate: PASS
self-contained GLX probe build: PASS
explicit-freedreno Zink/OpenGL probe: PASS
explicit-freedreno maps capture: PASS
explicit-freedreno map provenance enrichment: PASS
implicit-discovery Zink/OpenGL probe: FAIL before renderer gate
implicit loader discovery diagnostics: PASS
implicit-discovery + explicit software intent: NEXT
Obsidian adapter validation: NOT YET RUN
VS Code adapter validation: NOT YET RUN
```

The policy environment identity gate passed for both experiment modes:

```text
explicit-freedreno
    VK_DRIVER_FILES=<glibc Freedreno ICD>
    VK_ICD_FILENAMES=<glibc Freedreno ICD>

implicit-discovery
    VK_DRIVER_FILES unset
    VK_ICD_FILENAMES unset
```

The first `glxinfo` attempt did not execute because `glxinfo` was not installed or available on `PATH`. A self-contained GLX renderer probe was then added so the experiment owns its validation consumer and does not require a diagnostic-package installation.

## Question

Can Vulkan provider-selection policy be moved from unconditional shared glibc environment state into narrow launch composition without changing the promoted launchers yet?

The evidence now adds a second question:

```text
how should provider discovery policy
and consumer device-class intent
be represented independently?
```

## Evidence basis

The Obsidian selected-closure pilot demonstrated:

```text
baseline:
    explicit Freedreno override
    Freedreno driver mapped
    KGSL device mapped

strict policy-isolation run:
    explicit VK_* override removed
    SwiftShader mapped
    Lavapipe root + 8 strict-only dependencies mapped
    Gfxstream mapped
    Freedreno absent
    KGSL absent
```

All 11 strict-only paths were attributed to the three alternate provider roots with zero unresolved or ambiguous mapped-universe SONAME edges.

The GLX/Zink consumer adds the following distinction:

```text
provider discovery
    !=
provider mapping
    !=
physical-device enumeration
    !=
consumer device-class acceptance
    !=
usable rendering path
```

## Current policy problem

The shared glibc environment currently combines two responsibilities:

```text
shield glibc applications from inherited bionic ICD policy

and

select the glibc Freedreno provider globally
```

Real glibc consumers include:

```text
gl-run
VS Code launcher
Obsidian launcher
```

The bionic desktop session has its own separate provider policy and is not the target of this experiment.

## Experiment modes

The policy helper intentionally implements only two discovery modes.

### explicit-freedreno

```text
VK_DRIVER_FILES=<glibc Freedreno ICD>
VK_ICD_FILENAMES=<glibc Freedreno ICD>
```

Intent:

```text
explicit hardware-provider selection
```

### implicit-discovery

```text
VK_DRIVER_FILES unset
VK_ICD_FILENAMES unset
```

Intent:

```text
allow loader default discovery behavior
```

This mode is not called `no-vulkan` because direct evidence shows that removing explicit overrides can discover and map alternate Vulkan providers.

## Independent control dimensions

The experiment keeps at least these dimensions separate:

```text
GL_GPU
    application argv / feature-mode choice

VULKAN_POLICY_MODE
    provider discovery/selection policy

LIBGL_ALWAYS_SOFTWARE
    explicit software/CPU device-class intent for the tested Zink path
```

The promoted Electron launchers currently couple GPU feature flags to the presence of `VK_DRIVER_FILES`. The experimental adapters do not make provider-policy identity and application feature mode the same variable.

The loader diagnostics and Zink source behavior now show that software CPU intent is another independent dimension and must not be inferred merely from implicit discovery.

## Files

```text
recipe/policy-env.sh
    shared experiment-local policy function

recipe/run-zink-with-policy.sh
    gl-run-equivalent Zink/OpenGL adapter

recipe/glx-renderer-probe.c
    self-contained runtime GLX pbuffer probe

recipe/build-glx-renderer-probe.sh
    builds the probe through the existing glibc GCC wrapper

recipe/capture-glx-probe-maps.sh
    bounded process-map capture while the context is current

recipe/enrich-glx-probe-maps.sh
    package/version/identity/SONAME enrichment for mapped paths

recipe/compare-glx-provider-graphs.sh
    successful control graph comparison

recipe/capture-implicit-loader-debug.sh
    preserves loader discovery diagnostics for a failing implicit Zink path

recipe/launch-vscode-with-policy.sh
    VS Code adapter

recipe/launch-obsidian-with-policy.sh
    Obsidian adapter
```

## Self-contained GLX probe

Build contract:

```text
compiler:
    $HOME/gl/toolchain/glibc-gcc

link-time dependency:
    libc / loader only

runtime libraries:
    dlopen libX11.so.6
    dlopen libGL.so.1
```

Observed build result:

```text
GLX renderer probe build: PASS

interpreter:
    $PREFIX/glibc/lib/ld-linux-aarch64.so.1

NEEDED:
    libc.so.6
    ld-linux-aarch64.so.1
```

Runtime sequence:

```text
open X display
query GLX version
choose pbuffer-capable RGBA FBConfig
create GLX context
create 1x1 GLX pbuffer
make context current
print:
    GLX_VERSION
    GL_VENDOR
    GL_RENDERER
    GL_VERSION
```

## Explicit-Freedreno result

Observed:

```text
VULKAN_POLICY_MODE=explicit-freedreno
VK_DRIVER_FILES=$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json

GLX_VERSION=1.4
GL_VENDOR=Mesa
GL_RENDERER=zink Vulkan 1.4(Turnip Adreno (TM) 730 (MESA_TURNIP))
GL_VERSION=4.6 (Compatibility Profile) Mesa 25.0.7-2
```

Enriched process maps establish the tested physical graph:

```text
rootfs libGL/libGLX/libGLdispatch 1.7.0
    -> rootfs libGLX_mesa 25.0.7-2
    -> rootfs mesa-libgallium 25.0.7-2
    -> rootfs Mesa device-selection layer 25.0.7-2
    -> prefix Vulkan loader 1.3.301 and support libraries
    -> Mesa provider-store libvulkan_freedreno.so 26.1.4 lineage
    -> /dev/kgsl-3d0
```

Interpretation:

```text
scoped explicit Freedreno provider policy
    +
rootfs Gallium/Zink frontend
    +
rootfs Mesa device-selection layer
    +
prefix Vulkan loader/support plane
    +
provider-store Turnip driver
    +
KGSL device interface
    ->
working GLX context and Zink/Turnip renderer identity
```

This exact captured graph is a tested cross-version composition. It does not imply arbitrary compatibility among Mesa release lineages.

## Implicit-discovery result

Without explicit software intent, the same Zink/GLX consumer failed before renderer identity:

```text
VULKAN_POLICY_MODE=implicit-discovery
VK_DRIVER_FILES=<unset>

ZINK: failed to choose pdev
GLX screen creation failed
Zink driver load failed
GLX FBConfig gate failed
renderer identity not reached
```

Loader diagnostics show that this was not a manifest-discovery failure.

The loader discovered rootfs ICD manifests for:

```text
freedreno
gfxstream
lvp
nouveau
panfrost
radeon
virtio
broadcom
```

It also found and inserted:

```text
VK_LAYER_MESA_device_select
```

The one surviving physical device was:

```text
llvmpipe (LLVM 19.1.7, 128 bits)
```

Drivers removed for exposing no physical devices included:

```text
broadcom
virtio
radeon
panfrost
nouveau
gfxstream
freedreno
```

This means:

```text
implicit loader discovery: PASS
physical-device enumeration: PASS
surviving device: llvmpipe CPU
Zink default device-class acceptance: FAIL
GLX/OpenGL path: FAIL
```

## Zink CPU-device gate interpretation

The inspected Zink selection logic distinguishes normal selection from explicitly requested CPU/software selection.

The relevant behavior is:

```text
LIBGL_ALWAYS_SOFTWARE=1
    -> CPU device selection is requested

no software intent
    +
selected Vulkan device type == CPU
    -> selected pdev is rejected
```

The older `ZINK_USE_LAVAPIPE` path is treated as obsolete in the inspected source and points users toward `LIBGL_ALWAYS_SOFTWARE`.

This is consistent with the observed implicit sequence:

```text
rootfs LVP manifest discovered
    -> llvmpipe CPU pdev enumerated
    -> software intent absent
    -> Zink rejects CPU pdev
    -> failed to choose pdev
```

## Supply-root distinction

Implicit discovery also found the rootfs Freedreno manifest and searched for `libvulkan_freedreno.so`, but that path exposed no physical devices and was removed.

The passing explicit control instead selected the separately managed provider-store ICD and mapped:

```text
$HOME/gl/opt/mesa-glibc-26.1.4-full/lib/libvulkan_freedreno.so
/dev/kgsl-3d0
```

Therefore:

```text
same semantic driver-family name
    !=
same runtime capability
```

when supply root, provider build, and platform adaptation differ.

## Architecture interpretation

The current evidence requires at least:

```text
provider discovery policy
    explicit hardware provider
    implicit/default discovery

consumer device-class intent
    hardware/default
    explicit software CPU
```

These states must not be collapsed into:

```text
GPU on/off
```

or inferred solely from whether `VK_DRIVER_FILES` exists.

A consumer composition contract must express:

```text
consumer intent
    +
provider-selection/discovery policy
    +
device-class intent
    +
provider suitability validation
    +
actual-selection evidence
```

## Non-goals

Do not use this experiment to implement:

```text
provider updates
provider promotion
provider discovery database
gl-sync
gl-run lifecycle expansion
global environment migration
final directory layout
```

Do not yet add a promoted `explicit-lavapipe` or software-provider mode.

## Validation order

```text
1. environment identity check — PASS
2. build self-contained GLX renderer probe — PASS
3. Zink/OpenGL explicit-freedreno probe validation — PASS
4. explicit maps capture and provenance enrichment — PASS
5. implicit-discovery Zink/OpenGL probe — FAIL before renderer gate
6. implicit loader discovery diagnostics — PASS
7. implicit-discovery + LIBGL_ALWAYS_SOFTWARE=1 control — NEXT
8. if successful, capture/enrich/compare software graph
9. Obsidian explicit-freedreno control
10. Obsidian implicit-discovery control comparison
11. VS Code explicit-freedreno GPU validation
12. VS Code CPU/implicit policy behavior check
```

Promoted launchers and `gl/env` remain unchanged during this experiment.
