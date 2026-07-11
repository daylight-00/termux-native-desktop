# Vulkan Policy Composition Experiment

## Status

Active architecture-discrimination experiment.

Current validation state:

```text
policy identity gate: PASS
self-contained GLX probe build: PASS
explicit-freedreno Zink/OpenGL probe: PASS
explicit-freedreno maps capture/enrichment: PASS
implicit-discovery/default-intent Zink probe: FAIL before renderer gate
implicit loader discovery diagnostics: PASS
implicit-discovery/software-intent Zink probe: PASS
software graph maps capture/enrichment: PASS
hardware-vs-software graph comparison: PASS
runtime anonymous memfd classification: PASS ON DEVICE
Obsidian explicit-freedreno GPU adapter: PASS
Obsidian explicit GPU process-class graphics relations: PASS
Obsidian implicit-discovery GPU adapter: PASS
Obsidian implicit GPU process-class graphics relations: PASS
Obsidian same-feature-mode policy comparison: PASS
Mesa shader_cache_db classification fix: COMMITTED, DEVICE RECLASSIFICATION NEXT
implicit Electron selected renderer identity: UNRESOLVED
VS Code adapter validation: NEXT
```

Promoted launchers and `gl/env` remain unchanged.

## Primary architecture question

Can Vulkan provider policy move from unconditional shared glibc environment state into narrow launch composition while preserving real consumers?

The experiment has established that graphics composition has at least these independent dimensions:

```text
application feature mode
provider discovery/selection policy
device-class intent
consumer-specific suitability
actual selected-provider evidence
```

These dimensions must not be collapsed into one boolean such as:

```text
GPU=0/1
```

or inferred only from whether:

```text
VK_DRIVER_FILES
```

is present.

## Evidence basis before this experiment

The earlier Obsidian CPU-path controls established:

```text
baseline explicit policy:
    Freedreno mapped
    KGSL mapped

strict policy-isolation control:
    explicit VK_* overrides removed
    topology/survival preserved
    SwiftShader mapped
    Lavapipe root + dependency closure mapped
    Gfxstream mapped
    Freedreno absent
    KGSL absent
```

The strict-only 11-path set was fully attributed inside the captured mapped universe:

```text
SwiftShader root                              1
Lavapipe root + strict-only dependency set   9
Gfxstream root                               1
unattributed                                 0
unresolved SONAME edge                       0
ambiguous mapped-universe SONAME edge        0
```

This established:

```text
explicit hardware provider selection
    !=
implicit/default discovery
```

but did not yet separate provider policy from consumer device-class intent.

## Independent control dimensions

The experiment keeps these inputs separate.

### Application feature mode

```text
GL_GPU
```

Meaning:

```text
application argv / feature-mode intent
```

### Provider policy

```text
VULKAN_POLICY_MODE
```

Current experiment modes:

```text
explicit-freedreno
implicit-discovery
```

### Software CPU device-class intent

For the bounded Zink consumer:

```text
LIBGL_ALWAYS_SOFTWARE=1
```

This is independent from implicit discovery.

## Policy modes

### explicit-freedreno

```text
VK_DRIVER_FILES=<glibc Freedreno ICD>
VK_ICD_FILENAMES=<same ICD>
```

Intent:

```text
explicit hardware provider selection
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

This is not named `no-vulkan` because alternate Vulkan providers can still be discovered and mapped.

No promoted explicit-Lavapipe mode has been added.

# Part I — Self-contained Zink/GLX consumer

## Probe rationale

`glxinfo` was unavailable on the device.

The experiment therefore owns a small GLX renderer probe instead of installing a diagnostic package.

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

## Zink three-state matrix

### A. Explicit hardware provider + default device intent

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

### B. Implicit discovery + default device intent

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

### C. Implicit discovery + explicit software device intent

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

## Zink causal conclusion

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
    !=
device-class intent
```

for the bounded Zink/GLX consumer.

## Explicit hardware graph

Enriched maps establish the tested physical graph:

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

Its selected provider tail is proven by renderer identity as:

```text
rootfs libvulkan_lvp.so
    -> llvmpipe CPU renderer
```

The captured software set also maps:

```text
libvulkan_gfxstream.so
```

but loader diagnostics showed Gfxstream discovery/loading participation followed by removal for exposing no surviving physical device.

Therefore:

```text
mapped ICD object
    !=
selected renderer provider
```

## Hardware-versus-software graph delta

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

The narrow observed:

```text
/memfd:allocation*
```

pattern is classified as:

```text
path_class=RUNTIME_ANON_MEMORY
package=RUNTIME_MEMORY
version=NOT_APPLICABLE
state=RUNTIME_ANONYMOUS_MAPPING
```

Device re-enrichment passed.

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

# Part II — Real Obsidian Electron GPU-path controls

## Same-feature-mode control design

Both policy controls keep:

```text
CONTROL_GL_GPU=1
LIBGL_ALWAYS_SOFTWARE unset
same launcher adapter
same capture harness
same survival budget
```

and change only:

```text
VULKAN_POLICY_MODE=explicit-freedreno
```

versus:

```text
VULKAN_POLICY_MODE=implicit-discovery
```

This avoids mixing policy effects with CPU-mode versus GPU-mode differences.

## Explicit-Freedreno GPU control

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/obsidian-explicit-gpu-20260711-080703
```

Observed:

```text
topology gate: PASS
startup elapsed: 3 seconds
survival gate: PASS
survival elapsed: 100 seconds
identity enrichment: PASS
coverage: 160/160
semantic classification: PASS
semantic review objects: 0
```

Final process topology:

```text
main      1
zygote    2
gpu       1
utility   1
renderer  1
```

The `gpu` process directly maps:

```text
AppDir libEGL.so
AppDir libGLESv2.so
AppDir libvulkan.so.1
provider-store libvulkan_freedreno.so
rootfs libVkLayer_MESA_device_select.so
rootfs libgbm.so.1.0.0
/dev/kgsl-3d0
```

This supports the bounded mapping graph:

```text
Obsidian gpu process
    -> AppDir ANGLE/Vulkan-facing stack
    -> provider-store Freedreno/Turnip driver
    -> KGSL device node
```

This is mapping evidence, not rendering-command submission proof.

## Implicit-discovery GPU control

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/obsidian-implicit-gpu-20260711-105419
```

Observed:

```text
topology gate: PASS
startup elapsed: 3 seconds
survival gate: PASS
survival elapsed: 101 seconds
identity enrichment: PASS
coverage: 169/169
```

Final process topology:

```text
main      1
zygote    2
gpu       1
utility   1
renderer  1
```

The corrected graphics reporter shows the `gpu` process directly maps:

```text
AppDir libEGL.so
AppDir libGLESv2.so
AppDir libvulkan.so.1
rootfs libVkLayer_MESA_device_select.so
rootfs libgbm.so.1.0.0
rootfs libvulkan_lvp.so
rootfs libvulkan_gfxstream.so
```

The implicit control does not map the explicit control's:

```text
provider-store libvulkan_freedreno.so
/dev/kgsl-3d0
```

## Same-feature-mode process topology result

Both controls have exactly:

```text
gpu       1
main      1
renderer  1
utility   1
zygote    2
```

Therefore the provider-policy substitution preserved the observed final process-class topology.

## Shared graphics relations

Both controls share:

```text
gpu -> AppDir libEGL.so
gpu -> AppDir libGLESv2.so
gpu -> AppDir libvulkan.so.1
gpu -> rootfs libVkLayer_MESA_device_select.so
gpu -> rootfs libgbm.so.1.0.0

main     -> rootfs libgbm.so.1.0.0
renderer -> rootfs libgbm.so.1.0.0
utility  -> rootfs libgbm.so.1.0.0
zygote   -> rootfs libgbm.so.1.0.0
```

This supports a stable captured front half:

```text
Electron gpu process
    -> AppDir EGL/GLES/Vulkan-facing stack
    -> Mesa device-selection layer
    -> GBM infrastructure
```

## Explicit-only graphics relations

```text
gpu -> provider-store libvulkan_freedreno.so
gpu -> /dev/kgsl-3d0
```

## Implicit-only graphics relations

```text
gpu -> rootfs libvulkan_lvp.so
gpu -> rootfs libvulkan_gfxstream.so
```

This proves alternate ICD mapping participation in the real Electron GPU process.

It does not prove which implicit ICD is the selected renderer.

## Semantic provider substitution

Policy-significant explicit-only objects:

```text
DEVICE_NODE_GPU
    /dev/kgsl-3d0

PROVIDER_GRAPHICS_VULKAN_DRIVER_ELF
    provider-store libvulkan_freedreno.so
```

Implicit-only graphics roots:

```text
PROVIDER_GRAPHICS_VULKAN_SOFTWARE_LVP_ELF
    rootfs libvulkan_lvp.so

PROVIDER_GRAPHICS_VULKAN_VIRTUAL_GFXSTREAM_ELF
    rootfs libvulkan_gfxstream.so
```

The implicit side also adds the LVP dependency-side set:

```text
prefix:
    liblzma.so.5.6.4

rootfs:
    libLLVM.so.19.1
    libz3.so.4
    libxml2.so.2.9.14
    libedit.so.2.0.75
    libtinfo.so.6.5
    libbsd.so.0.12.2
    libmd.so.0.1.0
```

## Volatile-data separation

The raw exact semantic delta also includes:

```text
explicit-only:
    $HOME/.cache/mesa_shader_cache/index

implicit-only:
    $HOME/.cache/mesa_shader_cache_db/index
    DejaVuSansMono-Bold.ttf
```

These remain visible in the full exact diff but must not be treated as direct provider-policy consequences merely because they differ.

The font difference can reflect lazy mapping/capture timing.

The Mesa cache database path was initially classified as:

```text
OTHER_RUNTIME_DATA_REVIEW
```

because the classifier knew only:

```text
$HOME/.cache/mesa_shader_cache/
```

The classifier now also recognizes:

```text
$HOME/.cache/mesa_shader_cache_db/
```

as:

```text
RUNTIME_CACHE_MESA
```

Device-side semantic reclassification is required to regenerate the implicit evidence set with this correction.

## Comparison helper views

`compare-obsidian-policy-controls.sh` preserves two semantic views.

### Full exact semantic delta

Preserves every exact class/path difference, including:

```text
runtime cache differences
font/data timing differences
provider objects
provider dependency-side objects
```

### Policy-relevant semantic delta

Focuses on:

```text
device nodes
app-local graphics providers
graphics provider classes
prefix ELF provider differences
rootfs ELF provider differences
```

Outputs:

```text
explicit-policy-semantic-class-path.tsv
implicit-policy-semantic-class-path.tsv
explicit-only-policy-semantic-class-path.tsv
implicit-only-policy-semantic-class-path.tsv
```

The raw full diff is retained; the filtered view is an interpretation aid, not evidence deletion.

## Obsidian policy conclusion

For the tested real Electron GPU path:

```text
application feature mode:
    unchanged

process topology:
    unchanged

workload survival:
    PASS in both controls

provider policy:
    changed
```

and the captured provider tail changes as:

```text
explicit-freedreno
    -> gpu maps provider-store Freedreno
    -> gpu maps KGSL

implicit-discovery
    -> gpu maps LVP
    -> gpu maps Gfxstream
    -> no captured Freedreno/KGSL relation
```

This supports a real launch-composition substitution boundary:

```text
stable Electron/AppDir graphics front half
    +
policy-dependent provider tail
```

The provider tail is not one immutable global Mesa object.

## Cross-consumer consequence

Standalone Zink and Obsidian Electron do not have identical policy outcomes.

Standalone Zink:

```text
implicit discovery + default device intent
    -> CPU pdev discovered
    -> Zink rejects default CPU path
    -> FAIL
```

Obsidian Electron:

```text
GL_GPU=1 + implicit discovery
    -> gpu process present
    -> alternate ICDs mapped by gpu process
    -> topology preserved
    -> survival PASS
```

Therefore graphics policy must remain consumer-aware.

A policy valid for one consumer cannot be generalized to all glibc graphics consumers merely because they share Vulkan-related libraries.

## Unresolved Electron selection question

The current Electron evidence does not establish:

```text
which implicit ICD is the selected renderer
whether LVP or Gfxstream submits rendering work
whether rendered output correctness is equivalent across policies
whether Electron internally falls back among multiple graphics backends
whether the implicit provider tail should be modeled as one closure or multiple discovery candidates
```

Map presence alone cannot answer these questions.

# Files

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
    bounded GLX process-map capture

recipe/enrich-glx-probe-maps.sh
    path/package/version/hash/Build-ID/SONAME enrichment
    runtime-anonymous allocation classification

recipe/compare-glx-provider-graphs.sh
    GLX hardware/software graph comparison

recipe/capture-implicit-loader-debug.sh
    loader discovery diagnostics

recipe/launch-vscode-with-policy.sh
    VS Code experiment adapter

recipe/launch-obsidian-with-policy.sh
    Obsidian experiment adapter

recipe/compare-obsidian-policy-controls.sh
    same-feature-mode Obsidian policy comparison
    full exact and policy-relevant semantic views
```

# Non-goals

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

# Validation order

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
10. software memfd classification device re-enrichment — PASS
11. Obsidian explicit-freedreno GPU adapter control — PASS
12. explicit Obsidian GPU process-class graphics report — PASS
13. Obsidian implicit-discovery GPU adapter control — PASS
14. implicit identity enrichment and semantic classification — PASS, cache-db reclass pending
15. implicit Obsidian GPU process-class graphics report — PASS
16. same-feature-mode Obsidian policy comparison — PASS
```

Next:

```text
17. reclassify implicit Obsidian evidence with shader_cache_db correction
18. rerun refined full/policy-relevant Obsidian comparison
19. decide whether a bounded Electron actual-selection probe is feasible
20. VS Code explicit-freedreno GPU validation
21. VS Code CPU/software-intent behavior check
22. compare consumer-specific policy requirements
23. define minimum graphics composition contract only from proven consumer evidence
```
