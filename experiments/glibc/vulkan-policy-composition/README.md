# Vulkan Policy Composition Experiment

## Status

Active architecture-discrimination experiment.

The policy environment identity gate has passed for both experiment modes:

```text
explicit-freedreno
    VK_DRIVER_FILES=<glibc Freedreno ICD>
    VK_ICD_FILENAMES=<glibc Freedreno ICD>

implicit-discovery
    VK_DRIVER_FILES unset
    VK_ICD_FILENAMES unset
```

The first `glxinfo` attempt did not execute because `glxinfo` was not installed or available on `PATH`. A self-contained GLX renderer probe was then added and used successfully.

Current validation state:

```text
policy identity gate: PASS
self-contained GLX probe build: PASS
explicit-freedreno Zink/OpenGL probe: PASS
explicit-freedreno maps capture: PASS
explicit-freedreno map provenance enrichment: PASS
implicit-discovery Zink/OpenGL probe: NOT YET RUN
Obsidian adapter validation: NOT YET RUN
VS Code adapter validation: NOT YET RUN
```

## Question

Can Vulkan provider-selection policy be moved from unconditional shared glibc environment state into narrow launch composition without changing the promoted launchers yet?

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

## Current policy problem

The shared glibc environment currently combines two separate responsibilities:

```text
shield glibc applications from inherited bionic ICD policy

and

select the glibc Freedreno provider globally
```

Real consumers are:

```text
gl-run
VS Code launcher
Obsidian launcher
```

The bionic desktop session has its own separate provider policy and is not the target of this experiment.

## Experiment modes

This experiment intentionally implements only two modes.

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
allow loader discovery behavior
```

This mode is **not** called `no-vulkan` because direct evidence shows that removing the explicit override can map alternate Vulkan providers.

## Separation of controls

The experiment keeps these dimensions separate:

```text
GL_GPU
    application argv / feature-mode choice

VULKAN_POLICY_MODE
    provider-selection policy choice
```

The promoted launchers currently couple GPU feature flags to the presence of `VK_DRIVER_FILES`. Experimental adapters do not use that coupling.

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
    explicit vs implicit renderer and physical graph comparison

recipe/launch-vscode-with-policy.sh
    VS Code adapter

recipe/launch-obsidian-with-policy.sh
    Obsidian adapter
```

## Self-contained GLX probe

The probe exists because the validation host does not currently have `glxinfo` available.

It intentionally avoids a new diagnostic-package dependency.

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

Runtime behavior:

```text
open X display
query GLX version
choose pbuffer-capable RGBA FBConfig
create direct GLX context
create 1x1 GLX pbuffer
make context current
print:
    GLX_VERSION
    GL_VENDOR
    GL_RENDERER
    GL_VERSION
```

Observed explicit-Freedreno result:

```text
VULKAN_POLICY_MODE=explicit-freedreno
VK_DRIVER_FILES=$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json

GLX_VERSION=1.4
GL_VENDOR=Mesa
GL_RENDERER=zink Vulkan 1.4(Turnip Adreno (TM) 730 (MESA_TURNIP))
GL_VERSION=4.6 (Compatibility Profile) Mesa 25.0.7-2
```

Observed physical provider graph:

```text
rootfs libGL/libGLX/libGLdispatch 1.7.0
    -> rootfs libGLX_mesa 25.0.7-2
    -> rootfs mesa-libgallium 25.0.7-2
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
prefix Vulkan loader/support plane
    +
provider-store Turnip driver
    +
KGSL device interface
    ->
working GLX context and Zink/Turnip renderer identity
```

This is the first cross-consumer proof that the explicit provider-selection contract can be applied at launch scope while preserving the core behavior currently consumed by `gl-run`.

The exact captured graph is a tested cross-version composition. It does not imply arbitrary compatibility among Mesa release lineages.

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

The only goal is to validate that explicit provider policy can be composed at launch scope.

## Validation order

```text
1. environment identity check — PASS
2. build self-contained GLX renderer probe — PASS
3. Zink/OpenGL explicit-freedreno probe validation — PASS
4. explicit maps capture and provenance enrichment — PASS
5. compare implicit-discovery renderer and physical graph — NEXT
6. Obsidian explicit-freedreno control
7. Obsidian implicit-discovery control comparison
8. VS Code explicit-freedreno GPU validation
9. VS Code CPU/implicit policy behavior check
```

Promoted launchers and `gl/env` remain unchanged during this experiment.
