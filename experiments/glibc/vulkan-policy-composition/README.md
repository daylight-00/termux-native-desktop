# Vulkan Policy Composition Experiment

## Status

Active architecture-discrimination experiment.

Current validation state:

```text
policy identity gate: PASS
self-contained GLX probe build: PASS
explicit-freedreno Zink/OpenGL probe: PASS
explicit-freedreno maps capture: PASS
explicit-freedreno provenance enrichment: PASS
implicit-discovery/default-intent Zink probe: FAIL before renderer gate
implicit loader discovery diagnostics: PASS
implicit-discovery/software-intent Zink probe: PASS
software graph maps capture: PASS
software graph provenance enrichment: PASS
hardware-vs-software graph comparison: PASS
runtime anonymous memfd classification correction: COMMITTED, DEVICE RE-RUN PENDING
Obsidian adapter validation: NEXT
VS Code adapter validation: NOT YET RUN
```

## Primary question

Can Vulkan provider-selection policy move from unconditional shared glibc environment state into narrow launch composition without changing promoted launchers yet?

The completed Zink controls also answer a second question:

```text
provider discovery/selection policy
    and
consumer device-class intent
```

must be independent composition inputs.

## Evidence basis

The Obsidian selected-closure pilot previously established:

```text
baseline:
    explicit Freedreno override
    Freedreno mapped
    KGSL mapped

strict policy-isolation:
    explicit VK_* overrides removed
    SwiftShader mapped
    Lavapipe root + strict-only closure mapped
    Gfxstream mapped
    Freedreno absent
    KGSL absent
```

The Zink/GLX controls now refine the graphics decision chain:

```text
provider discovery
    !=
provider mapping
    !=
physical-device enumeration
    !=
consumer device-class acceptance
    !=
selected renderer identity
    !=
usable rendering path
```

## Independent control dimensions

The experiment keeps these dimensions separate:

```text
GL_GPU
    application feature / argv mode

VULKAN_POLICY_MODE
    provider discovery/selection policy

LIBGL_ALWAYS_SOFTWARE
    explicit software CPU device-class intent for the tested Zink path
```

These are not interchangeable.

In particular:

```text
implicit discovery
    !=
software rendering intent
```

and:

```text
GPU feature mode
    !=
Vulkan provider policy
```

## Policy modes

The experiment policy helper intentionally implements only two provider-policy modes.

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

Software CPU intent is supplied independently with:

```text
LIBGL_ALWAYS_SOFTWARE=1
```

No promoted `explicit-lavapipe` mode has been added.

## Self-contained GLX probe

The experiment owns a small GLX renderer probe because `glxinfo` was unavailable on the device.

Build contract:

```text
compiler:
    $HOME/gl/toolchain/glibc-gcc

link-time NEEDED:
    libc.so.6
    ld-linux-aarch64.so.1

runtime dlopen:
    libX11.so.6
    libGL.so.1
```

Runtime sequence:

```text
open X display
query GLX version
choose pbuffer-capable RGBA FBConfig
create GLX context
create 1x1 pbuffer
make context current
print renderer identity
hold process for bounded map capture
```

## Completed three-state matrix

### 1. Explicit hardware provider + default device intent

Observed:

```text
VULKAN_POLICY_MODE=explicit-freedreno

GLX_VERSION=1.4
GL_VENDOR=Mesa
GL_RENDERER=zink Vulkan 1.4(Turnip Adreno (TM) 730 (MESA_TURNIP))
GL_VERSION=4.6 (Compatibility Profile) Mesa 25.0.7-2
```

Result:

```text
PASS
```

### 2. Implicit discovery + default device intent

Observed:

```text
VULKAN_POLICY_MODE=implicit-discovery
LIBGL_ALWAYS_SOFTWARE unset

ZINK: failed to choose pdev
GLX screen creation failed
Zink driver load failed
renderer identity not reached
```

Loader diagnostics showed:

```text
manifest discovery: PASS
Mesa device-select layer insertion: PASS
physical-device enumeration: PASS
sole surviving pdev: llvmpipe CPU
Zink default CPU-device acceptance: FAIL
```

Result:

```text
FAIL before renderer identity
```

### 3. Implicit discovery + explicit software device intent

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/implicit-software-maps-20260711-025042
```

Observed:

```text
VULKAN_POLICY_MODE=implicit-discovery
LIBGL_ALWAYS_SOFTWARE=1

GLX_VERSION=1.4
GL_VENDOR=Mesa
GL_RENDERER=zink Vulkan 1.4(llvmpipe (LLVM 19.1.7, 128 bits) (MESA_LLVMPIPE))
GL_VERSION=4.6 (Compatibility Profile) Mesa 25.0.7-2
```

Result:

```text
PASS
```

## Causal conclusion

The completed matrix is:

```text
explicit-freedreno + default intent
    -> Turnip Adreno 730
    -> KGSL
    -> PASS

implicit-discovery + default intent
    -> llvmpipe CPU discovered
    -> CPU pdev rejected by Zink default path
    -> FAIL

implicit-discovery + software intent
    -> llvmpipe CPU selected
    -> Zink/GLX/OpenGL 4.6
    -> PASS
```

Therefore:

```text
provider policy
    and
device-class intent
```

are proven independent for the bounded Zink/GLX consumer.

## Explicit hardware graph

Enriched maps establish the tested explicit physical composition:

```text
rootfs GLVND / libGL / libGLX 1.7.0
    -> rootfs Mesa GLX vendor 25.0.7-2
    -> rootfs Gallium/Zink frontend 25.0.7-2
    -> rootfs Mesa device-selection layer 25.0.7-2
    -> prefix Vulkan loader 1.3.301 and support plane
    -> provider-store Turnip/Freedreno 26.1.4 lineage
    -> /dev/kgsl-3d0
```

Renderer identity:

```text
MESA_TURNIP
Turnip Adreno 730
```

This exact cross-version graph is tested. Arbitrary Mesa cross-version compatibility is not claimed.

## Software graph

The passing software control shares the application-facing front half:

```text
rootfs GLVND
rootfs Mesa GLX vendor
rootfs Gallium/Zink frontend
rootfs Mesa device-selection layer
prefix Vulkan loader/support plane
```

Its provider tail is:

```text
rootfs libvulkan_lvp.so
    -> llvmpipe CPU renderer
```

Renderer identity:

```text
MESA_LLVMPIPE
llvmpipe (LLVM 19.1.7, 128 bits)
```

The captured software set also maps:

```text
libvulkan_gfxstream.so
```

but this must not be called the selected rendering provider. Previous loader diagnostics showed Gfxstream discovery/loading participation followed by removal for exposing no surviving physical device.

Therefore:

```text
mapped ICD object
    !=
selected renderer provider
```

## Hardware-vs-software graph comparison

Explicit-only paths:

```text
$HOME/.cache/mesa_shader_cache/index
$HOME/gl/opt/mesa-glibc-26.1.4-full/lib/libvulkan_freedreno.so
/dev/kgsl-3d0
```

Software-control-only paths:

```text
$ROOTFS/usr/lib/aarch64-linux-gnu/libvulkan_gfxstream.so
$ROOTFS/usr/lib/aarch64-linux-gnu/libvulkan_lvp.so
/memfd:allocation
```

The `/memfd:allocation` entry is a runtime anonymous mapping, not package-provenance evidence. The enrichment classifier has been corrected for the narrow observed `/memfd:allocation*` pattern and requires device-side re-enrichment to regenerate the evidence summary.

## Supply-root distinction

Implicit discovery found the rootfs Freedreno manifest and searched for rootfs `libvulkan_freedreno.so`, but that path exposed no physical devices and was removed.

The passing hardware control used the separately managed provider-store ICD/driver and reached Turnip/KGSL.

Therefore:

```text
same upstream driver-family name
    !=
same runtime capability
```

when supply root, build lineage, and platform adaptation differ.

## Architecture interpretation

A graphics launch composition contract must express at least:

```text
application feature intent
provider discovery/selection policy
device-class intent
consumer validation gate
actual selected-provider evidence
```

A single boolean such as:

```text
GPU=0/1
```

is not sufficient.

Presence or absence of:

```text
VK_DRIVER_FILES
```

must not be used as a proxy for software-device intent.

## Files

```text
recipe/policy-env.sh
    experiment-local provider-policy helper

recipe/run-zink-with-policy.sh
    GLX/Zink consumer adapter

recipe/glx-renderer-probe.c
    self-contained GLX renderer probe

recipe/build-glx-renderer-probe.sh
    glibc probe build

recipe/capture-glx-probe-maps.sh
    bounded process-map capture

recipe/enrich-glx-probe-maps.sh
    path/package/version/hash/Build-ID/SONAME enrichment
    includes narrow runtime-anonymous allocation classification

recipe/compare-glx-provider-graphs.sh
    A/B graph comparison

recipe/capture-implicit-loader-debug.sh
    loader discovery diagnostics

recipe/launch-vscode-with-policy.sh
    VS Code experiment adapter

recipe/launch-obsidian-with-policy.sh
    Obsidian experiment adapter
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

Do not yet:

```text
add global software-rendering policy
add promoted explicit-lavapipe mode
change gl/env
change gl-run
change promoted Electron launchers
```

## Validation order

Completed:

```text
1. environment identity check — PASS
2. self-contained GLX probe build — PASS
3. explicit-freedreno Zink validation — PASS
4. explicit maps capture/enrichment — PASS
5. implicit/default-intent Zink control — FAIL, discriminating result
6. implicit loader diagnostics — PASS
7. implicit/software-intent Zink control — PASS
8. software maps capture/enrichment — PASS
9. hardware-vs-software graph comparison — PASS
```

Next:

```text
10. re-run software enrichment with runtime-anonymous memfd classification
11. Obsidian explicit-freedreno adapter control
12. Obsidian implicit-discovery adapter control comparison
13. VS Code explicit-freedreno GPU validation
14. VS Code CPU/software-intent behavior check
15. compare consumer-specific policy requirements
16. define minimum graphics composition contract only from proven consumer evidence
```

Promoted launchers and `gl/env` remain unchanged during this experiment.
