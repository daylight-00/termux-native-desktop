# 0058 — Obsidian GPU Policy A/B Evidence Hygiene Closed

## Status

The existing Obsidian implicit-discovery GPU evidence root was reclassified with the Mesa shader-cache database correction, and the refined same-feature-mode comparison was rerun successfully.

Evidence roots:

```text
explicit:
    $PREFIX/tmp/tnd-vulkan-policy-composition/obsidian-explicit-gpu-20260711-080703

implicit:
    $PREFIX/tmp/tnd-vulkan-policy-composition/obsidian-implicit-gpu-20260711-105419
```

No new workload capture was required.

## Reclassification result

The implicit control now reports:

```text
semantic classification: PASS
review objects: 0
```

Relevant counts:

```text
PROVIDER_GRAPHICS_GBM_ELF                         1
PROVIDER_GRAPHICS_VULKAN_LAYER_ELF                1
PROVIDER_GRAPHICS_VULKAN_SOFTWARE_LVP_ELF         1
PROVIDER_GRAPHICS_VULKAN_VIRTUAL_GFXSTREAM_ELF    1
RUNTIME_CACHE_MESA                                1
```

The previous:

```text
OTHER_RUNTIME_DATA_REVIEW    1
```

row is gone.

The observed path:

```text
$HOME/.cache/mesa_shader_cache_db/index
```

is now classified as:

```text
RUNTIME_CACHE_MESA
```

## Refined comparison result

The same-feature-mode comparison completed with:

```text
Obsidian policy control comparison: PASS
```

Both controls retain identical final process-class counts:

```text
gpu         1
main        1
renderer    1
utility     1
zygote      2
```

## Full exact semantic delta

The explicit-only exact semantic set contains:

```text
DEVICE_NODE_GPU
    /dev/kgsl-3d0

PROVIDER_GRAPHICS_VULKAN_DRIVER_ELF
    provider-store libvulkan_freedreno.so

RUNTIME_CACHE_MESA
    $HOME/.cache/mesa_shader_cache/index
```

The implicit-only exact semantic set contains:

```text
PROVIDER_GRAPHICS_VULKAN_SOFTWARE_LVP_ELF
    rootfs libvulkan_lvp.so

PROVIDER_GRAPHICS_VULKAN_VIRTUAL_GFXSTREAM_ELF
    rootfs libvulkan_gfxstream.so

PROVIDER_PREFIX_ELF
    prefix liblzma.so.5.6.4

PROVIDER_ROOTFS_ELF
    rootfs libLLVM.so.19.1
    rootfs libbsd.so.0.12.2
    rootfs libedit.so.2.0.75
    rootfs libmd.so.0.1.0
    rootfs libtinfo.so.6.5
    rootfs libxml2.so.2.9.14
    rootfs libz3.so.4

PROVIDER_FONT_DATA
    DejaVuSansMono-Bold.ttf

RUNTIME_CACHE_MESA
    $HOME/.cache/mesa_shader_cache_db/index
```

The font and cache-path differences remain preserved as exact evidence but are not treated as provider-policy causes merely because they differ.

## Policy-relevant semantic delta

The refined helper emits a separate policy-relevant view.

### Explicit-only

```text
DEVICE_NODE_GPU
    /dev/kgsl-3d0

PROVIDER_GRAPHICS_VULKAN_DRIVER_ELF
    provider-store libvulkan_freedreno.so
```

### Implicit-only

```text
PROVIDER_GRAPHICS_VULKAN_SOFTWARE_LVP_ELF
    rootfs libvulkan_lvp.so

PROVIDER_GRAPHICS_VULKAN_VIRTUAL_GFXSTREAM_ELF
    rootfs libvulkan_gfxstream.so

PROVIDER_PREFIX_ELF
    prefix liblzma.so.5.6.4

PROVIDER_ROOTFS_ELF
    rootfs libLLVM.so.19.1
    rootfs libbsd.so.0.12.2
    rootfs libedit.so.2.0.75
    rootfs libmd.so.0.1.0
    rootfs libtinfo.so.6.5
    rootfs libxml2.so.2.9.14
    rootfs libz3.so.4
```

This cleanly separates the provider/device substitution from volatile cache and lazy font-data differences.

## Process-class graphics delta

The process-class relation comparison remains:

```text
explicit-only:
    gpu -> provider-store libvulkan_freedreno.so
    gpu -> /dev/kgsl-3d0

implicit-only:
    gpu -> rootfs libvulkan_lvp.so
    gpu -> rootfs libvulkan_gfxstream.so
```

The common captured front half remains:

```text
gpu -> AppDir libEGL.so
gpu -> AppDir libGLESv2.so
gpu -> AppDir libvulkan.so.1
gpu -> rootfs libVkLayer_MESA_device_select.so
gpu -> rootfs libgbm.so.1.0.0
```

Other process classes continue to map rootfs GBM in both controls.

## Architecture conclusion

The same-feature-mode Obsidian A/B is now closed at:

```text
topology
survival
identity coverage
semantic classification
exact semantic path delta
policy-relevant semantic delta
process-class graphics relations
```

The evidence supports:

```text
stable captured Electron/AppDir graphics front half
    +
policy-dependent Vulkan provider tail
```

with:

```text
explicit-freedreno:
    gpu -> Freedreno -> KGSL

implicit-discovery:
    gpu -> LVP mapped
    gpu -> Gfxstream mapped
    selected renderer unresolved
```

## Remaining claim boundary

The A/B does not establish:

```text
selected implicit Electron renderer identity
whether LVP or Gfxstream submits rendering work
whether both ICD mappings are only discovery participation
whether rendered output correctness is equivalent
```

The next experiment should first test whether the existing Electron/AppDir Vulkan loader emits enough selection evidence under loader debug logging before introducing stronger tracing machinery.
