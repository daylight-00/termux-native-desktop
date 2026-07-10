# 0040 — Obsidian Explicit Freedreno vs Implicit Fallback Provider Set

## Status

The exact semantic path-set comparison between the original nominal CPU control and the strict CPU control completed successfully.

Baseline evidence:

```text
$PREFIX/tmp/selected-obsidian-control-survival-20260710-220652
```

Strict evidence:

```text
$PREFIX/tmp/selected-obsidian-strict-cpu-20260710-235208
```

The strict control differed from baseline only by unsetting:

```text
VK_DRIVER_FILES
VK_ICD_FILENAMES
```

after sourcing the shared environment and before application launch.

## Exact baseline-only set

```text
$HOME/.cache/mesa_shader_cache/index
$HOME/gl/opt/mesa-glibc-26.1.4-full/lib/libvulkan_freedreno.so
/dev/kgsl-3d0
```

Semantic interpretation:

```text
RUNTIME_CACHE_MESA
PROVIDER_GRAPHICS_VULKAN_DRIVER_ELF
DEVICE_NODE_GPU
```

## Exact strict-only set

```text
$HOME/gl/apps/obsidian/libvk_swiftshader.so
$PREFIX/glibc/lib/liblzma.so.5.6.4
$ROOTFS/usr/lib/aarch64-linux-gnu/libLLVM.so.19.1
$ROOTFS/usr/lib/aarch64-linux-gnu/libbsd.so.0.12.2
$ROOTFS/usr/lib/aarch64-linux-gnu/libedit.so.2.0.75
$ROOTFS/usr/lib/aarch64-linux-gnu/libmd.so.0.1.0
$ROOTFS/usr/lib/aarch64-linux-gnu/libtinfo.so.6.5
$ROOTFS/usr/lib/aarch64-linux-gnu/libvulkan_gfxstream.so
$ROOTFS/usr/lib/aarch64-linux-gnu/libvulkan_lvp.so
$ROOTFS/usr/lib/aarch64-linux-gnu/libxml2.so.2.9.14
$ROOTFS/usr/lib/aarch64-linux-gnu/libz3.so.4
```

The strict-only set is not random cache noise. It contains three directly identifiable Vulkan-provider implementations or components:

```text
AppDir libvk_swiftshader.so
rootfs libvulkan_lvp.so
rootfs libvulkan_gfxstream.so
```

The remaining strict-only libraries form a coherent dependency-candidate cluster that appeared together with the alternate Vulkan provider set:

```text
libLLVM
libz3
libxml2
libedit
libtinfo
libbsd
libmd
liblzma
```

Current evidence does not yet prove every dependency edge. Those libraries remain under their existing generic provider classes until static DT_NEEDED closure analysis confirms the graph.

## Loader-model interpretation

The Vulkan loader contract distinguishes:

```text
explicit override discovery
    VK_DRIVER_FILES
    VK_ICD_FILENAMES

from

default driver discovery
    manifest search paths
    discovered available drivers
```

Therefore removing the explicit Freedreno override does not mean:

```text
no Vulkan driver
```

It means the loader may return to normal discovery of available drivers.

The observed A/B is consistent with:

```text
baseline:
    explicit Freedreno override
    -> Freedreno provider mapped
    -> KGSL device mapped

strict:
    explicit override removed
    -> alternate/default discovery path
    -> SwiftShader mapped
    -> Lavapipe mapped
    -> Gfxstream mapped
    -> Freedreno absent
    -> KGSL absent
```

This is the current best interpretation of the captured evidence.

## Corrected meaning of “strict CPU”

The experiment-local strict launcher was useful as a policy-isolation A/B, but its name must not be interpreted as proof of a graphics-free runtime.

The correct statement is:

```text
strict CPU argv:
    --disable-gpu

explicit Freedreno selection:
    removed

Vulkan provider discovery:
    still possible

observed result:
    alternate Vulkan providers mapped
```

Therefore:

```text
--disable-gpu
    !=
no graphics infrastructure

unset explicit Vulkan driver override
    !=
no Vulkan provider discovery
```

## Architecture conclusion

The A/B strengthens the case that graphics provider policy must be explicit and scoped.

The problem with the current global environment is not only that it enables graphics in a CPU-mode workload.

The deeper issue is:

```text
provider-selection policy is hidden in shared process environment
```

and therefore the workload cannot express clearly whether it intends:

```text
explicit hardware provider
explicit software provider
implicit discovery
no Vulkan provider participation
```

The target composition model should expose those choices deliberately.

Conceptually:

```text
provider.graphics.vulkan.glibc
    explicit hardware provider policy
    explicit software provider policy
    validation contract
    actual-selection evidence

application domain
    requests one graphics composition policy
    or requests none
```

Do not replace the current global variables with another unconditional fallback policy.

## Taxonomy refinement

The semantic classifier now recognizes:

```text
APP_LOCAL_GRAPHICS_VULKAN_SWIFTSHADER_ELF
PROVIDER_GRAPHICS_VULKAN_SOFTWARE_LVP_ELF
PROVIDER_GRAPHICS_VULKAN_VIRTUAL_GFXSTREAM_ELF
```

in addition to:

```text
PROVIDER_GRAPHICS_VULKAN_DRIVER_ELF
PROVIDER_GRAPHICS_VULKAN_LAYER_ELF
PROVIDER_GRAPHICS_GBM_ELF
DEVICE_NODE_GPU
```

This separates provider semantics from physical supply root while preserving app-local locality for the bundled SwiftShader object.

## Next gate

Before changing promoted `gl/env`:

```text
1. rerun the refined classifier on baseline and strict evidence
2. inspect static DT_NEEDED closure for libvulkan_lvp.so and libvulkan_gfxstream.so
3. determine which strict-only dependency-candidate libraries belong to which provider graph
4. inventory all current VK_* consumers
5. define narrow explicit graphics-provider composition contracts
6. audit APP_LOCAL versus external SONAME collisions
7. compare the non-graphics rootfs ELF static closure against runtime-selected sets
```

Candidate materialization remains blocked.
