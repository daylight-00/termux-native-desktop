# 0057 — Obsidian Same-Feature-Mode Vulkan Policy Substitution Result

## Status

The corrected same-feature-mode Obsidian GPU-path policy A/B completed successfully.

Controls:

```text
explicit control:
    CONTROL_GL_GPU=1
    VULKAN_POLICY_MODE=explicit-freedreno
    LIBGL_ALWAYS_SOFTWARE unset

implicit control:
    CONTROL_GL_GPU=1
    VULKAN_POLICY_MODE=implicit-discovery
    LIBGL_ALWAYS_SOFTWARE unset
```

Evidence roots:

```text
explicit:
    $PREFIX/tmp/tnd-vulkan-policy-composition/obsidian-explicit-gpu-20260711-080703

implicit:
    $PREFIX/tmp/tnd-vulkan-policy-composition/obsidian-implicit-gpu-20260711-105419
```

Both controls passed topology and 100-second survival gates.

## Process topology equivalence

Both final process sets contain:

```text
main      1
zygote    2
gpu       1
utility   1
renderer  1
```

Therefore the provider-policy substitution did not alter the observed final Electron process-class topology for these controls.

This is important because policy deltas can be interpreted without conflating them with CPU-mode versus GPU-mode topology changes.

## Shared graphics process relations

In both controls, the `gpu` process maps:

```text
AppDir libEGL.so
AppDir libGLESv2.so
AppDir libvulkan.so.1
rootfs libVkLayer_MESA_device_select.so
rootfs libgbm.so.1.0.0
```

Across both controls, the non-GPU process classes:

```text
main
renderer
utility
zygote
```

map rootfs GBM.

Therefore the stable front half of the captured Electron graphics composition is:

```text
Electron gpu process
    -> AppDir EGL/GLES/Vulkan-facing libraries
    -> Mesa device-selection layer
    -> GBM infrastructure
```

while the Vulkan provider/device tail changes with provider policy.

## Explicit-only graphics relations

The exact explicit-only process-class relations are:

```text
gpu
    -> provider-store libvulkan_freedreno.so
    -> /dev/kgsl-3d0
```

The explicit GPU process therefore directly maps both the provider-store Freedreno driver and KGSL device node.

This supports the bounded mapping graph:

```text
Obsidian gpu process
    -> AppDir ANGLE/Vulkan-facing stack
    -> provider-store Freedreno/Turnip driver
    -> KGSL device node
```

This remains mapping evidence rather than rendering-command submission proof.

## Implicit-only graphics relations

The exact implicit-only process-class relations are:

```text
gpu
    -> rootfs libvulkan_lvp.so
    -> rootfs libvulkan_gfxstream.so
```

The implicit GPU process therefore directly maps both alternate Vulkan ICD objects while preserving the same process topology and surviving the workload gate.

However:

```text
mapped LVP
    and
mapped Gfxstream
```

must not be collapsed into:

```text
selected renderer identity
```

without stronger selection evidence.

The prior standalone loader diagnostics already showed that a mapped/discovered ICD can fail to provide a surviving physical device. Therefore the current Electron result proves mapped alternate provider participation, not which alternate ICD ultimately rendered frames.

## Semantic path substitution

The first exact semantic delta output reported the following policy-significant explicit-only objects:

```text
DEVICE_NODE_GPU
    /dev/kgsl-3d0

PROVIDER_GRAPHICS_VULKAN_DRIVER_ELF
    provider-store libvulkan_freedreno.so
```

The implicit-only provider graph includes:

```text
PROVIDER_GRAPHICS_VULKAN_SOFTWARE_LVP_ELF
    rootfs libvulkan_lvp.so

PROVIDER_GRAPHICS_VULKAN_VIRTUAL_GFXSTREAM_ELF
    rootfs libvulkan_gfxstream.so
```

and the LVP dependency-side additions:

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

This reproduces the previously observed LVP closure shape inside a same-feature-mode real Electron GPU-path comparison.

## Volatile-data delta separation

The exact semantic diff also contains non-policy-stable data differences:

```text
explicit-only:
    $HOME/.cache/mesa_shader_cache/index

implicit-only:
    $HOME/.cache/mesa_shader_cache_db/index
    DejaVuSansMono-Bold.ttf
```

These objects must not be interpreted as direct provider-policy consequences merely because they are exact path-set differences.

The font-data difference can reflect lazy mapping/capture timing.

The Mesa cache path difference represents runtime cache state and should remain visible in the full exact diff but be excluded from the policy-relevant semantic delta view.

The classifier previously treated:

```text
$HOME/.cache/mesa_shader_cache_db/index
```

as:

```text
OTHER_RUNTIME_DATA_REVIEW
```

because it recognized only:

```text
$HOME/.cache/mesa_shader_cache/
```

The classifier now recognizes both Mesa shader cache layouts as:

```text
RUNTIME_CACHE_MESA
```

## Comparison helper refinement

The policy comparison helper now preserves two views.

### Full exact semantic delta

Purpose:

```text
preserve every exact class/path difference
```

This includes:

```text
runtime cache differences
font/data timing differences
provider objects
provider dependency-side objects
```

### Policy-relevant semantic delta

Purpose:

```text
focus architecture interpretation on:
    device nodes
    app-local graphics providers
    graphics provider classes
    prefix ELF provider differences
    rootfs ELF provider differences
```

The helper now writes:

```text
explicit-policy-semantic-class-path.tsv
implicit-policy-semantic-class-path.tsv
explicit-only-policy-semantic-class-path.tsv
implicit-only-policy-semantic-class-path.tsv
```

This avoids hiding raw evidence while preventing cache/font noise from dominating policy interpretation.

## Architecture conclusion

For the tested Obsidian Electron GPU path:

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

Therefore the evidence supports a real launch-composition substitution boundary:

```text
stable Electron/AppDir graphics front half
    +
policy-selected provider tail
```

The provider tail is not a single immutable global Mesa object.

## Cross-consumer consequence

The standalone Zink/GLX consumer and Obsidian Electron consumer do not have identical policy outcomes.

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
    -> gpu process survives
    -> alternate ICDs mapped in gpu process
    -> topology preserved
    -> 100-second survival PASS
```

Therefore graphics provider policy must remain consumer-aware.

A valid policy for one consumer cannot be generalized to every glibc graphics consumer merely from shared use of Vulkan-related libraries.

## What remains unresolved

The current evidence does not establish:

```text
which implicit ICD is the selected renderer in Electron
whether LVP or Gfxstream submits rendering work
whether rendered output correctness is equivalent across policies
whether Electron internally falls back among multiple graphics backends
whether the implicit provider tail should be represented as one closure or multiple discovery candidates
```

These require consumer-specific selection evidence beyond map presence.

## Next gate

Before modifying promoted launchers or global environment policy:

```text
1. reclassify the implicit control with the Mesa shader_cache_db fix
2. rerun the refined policy comparison helper
3. inspect the clean policy-relevant semantic delta
4. design a bounded Electron actual-selection probe if feasible
5. proceed to VS Code consumer validation only after preserving these claim boundaries
```

No candidate materialization or global provider-policy migration should be inferred directly from this A/B.
