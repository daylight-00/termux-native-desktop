# 0037 — Obsidian Graphics Process-Class Mapping

## Status

The Obsidian control evidence reached:

```text
identity enrichment coverage: 161/161
semantic classifier review count: 0
```

The complete semantic decomposition before graphics-capability refinement was:

```text
APP_LOCAL_DATA                  6
APP_LOCAL_ELF                   5
APP_MUTABLE_STATE              19
DEVICE_NODE_GPU                 1
PROVIDER_FONT_DATA              4
PROVIDER_GRAPHICS_VULKAN_ELF    1
PROVIDER_LOCALE_DATA           12
PROVIDER_PREFIX_ELF            41
PROVIDER_ROOTFS_ELF            60
PROVIDER_SCHEMA_DATA            1
RUNTIME_CACHE_FONTCONFIG        4
RUNTIME_CACHE_MESA              1
WORLD_SUBSTRATE_ELF             6
```

Total:

```text
161
```

Review count:

```text
0
```

## Ad-hoc AWK portability failure

A user-facing analysis command intended to deduplicate graphics class/object relations repeated the same portability mistake previously fixed in the classifier.

The failing form used:

```awk
NR > 1 &&
(
    condition_a ||
    condition_b
)
```

The device AWK rejected the newline before the opening grouped expression.

The user correctly rewrote the condition into a single portable expression and obtained the result.

This analysis step is now implemented as:

```text
report-graphics-process-mappings.sh
```

so the experiment no longer depends on repeatedly pasting complex multiline AWK predicates.

## Raw graphics mappings

Observed graphics-related mappings:

```text
main:
    rootfs libgbm.so.1.0.0

zygote:
    rootfs libgbm.so.1.0.0

zygote PID 27444:
    AppDir libEGL.so
    AppDir libGLESv2.so
    AppDir libvulkan.so.1
    Mesa store libvulkan_freedreno.so
    rootfs libVkLayer_MESA_device_select.so
    rootfs libgbm.so.1.0.0
    /dev/kgsl-3d0

utility:
    rootfs libgbm.so.1.0.0

renderer:
    rootfs libgbm.so.1.0.0
```

The unique process-class/object relation is:

```text
main
    libgbm.so.1.0.0

renderer
    libgbm.so.1.0.0

utility
    libgbm.so.1.0.0

zygote
    libEGL.so
    libGLESv2.so
    libvulkan.so.1
    libvulkan_freedreno.so
    libVkLayer_MESA_device_select.so
    libgbm.so.1.0.0
    /dev/kgsl-3d0
```

## Interpretation

The evidence proves a stronger statement than simple graphics-library presence:

```text
a zygote-class process address space contained:
    app-local Vulkan/EGL/GLES objects
    concrete Freedreno Vulkan driver
    Mesa device-selection layer
    GBM
    KGSL device mapping
```

At the same time:

```text
main
renderer
utility
other zygote-class processes
```

also mapped GBM or subsets of the graphics infrastructure.

This means the graphics runtime composition is process-class asymmetric.

## Claim boundary

The evidence proves:

```text
CPU-mode control does not exclude graphics-provider participation

concrete Freedreno Vulkan provider bytes were mapped

KGSL device-node mapping was present in the same zygote-class PID

GBM was mapped across main, renderer, utility, and zygote classes
```

The evidence does not yet prove:

```text
that PID 27444 submitted rendering work
that a particular physical Vulkan device was selected
that a specific ICD JSON path was opened
that the zygote-class process remained semantically a pure zygote after all runtime transitions
that GPU acceleration determined visible rendering output
```

Process labels in this experiment are derived from captured command-line `--type=` classification. Runtime address-space evidence and command-line class are both facts, but further inference about Chromium internal role transitions requires separate evidence.

## Taxonomy refinement

The first review-free classifier still grouped two graphics capability objects under generic rootfs ELF providers:

```text
libVkLayer_MESA_device_select.so
libgbm.so.1.0.0
```

The classifier is now refined to separate graphics semantic role from supply location:

```text
PROVIDER_GRAPHICS_VULKAN_DRIVER_ELF
    libvulkan_freedreno.so

PROVIDER_GRAPHICS_VULKAN_LAYER_ELF
    libVkLayer_MESA_device_select.so

PROVIDER_GRAPHICS_GBM_ELF
    libgbm.so.1.0.0

DEVICE_NODE_GPU
    /dev/kgsl-3d0
```

The resulting expected decomposition is:

```text
APP_LOCAL_DATA                         6
APP_LOCAL_ELF                          5
APP_MUTABLE_STATE                     19
DEVICE_NODE_GPU                        1
PROVIDER_FONT_DATA                      4
PROVIDER_GRAPHICS_GBM_ELF               1
PROVIDER_GRAPHICS_VULKAN_DRIVER_ELF     1
PROVIDER_GRAPHICS_VULKAN_LAYER_ELF      1
PROVIDER_LOCALE_DATA                   12
PROVIDER_PREFIX_ELF                    41
PROVIDER_ROOTFS_ELF                    58
PROVIDER_SCHEMA_DATA                    1
RUNTIME_CACHE_FONTCONFIG                4
RUNTIME_CACHE_MESA                      1
WORLD_SUBSTRATE_ELF                     6
```

Total remains:

```text
161
```

This refinement demonstrates an important rule:

```text
semantic capability boundary
    may cut across
physical supply roots
```

The Vulkan driver comes from the Mesa provider store, the Vulkan layer and GBM come from the Debian/rootfs supply path, app-local graphics libraries remain inside the AppDir locality domain, and the kernel interface is a device capability rather than a provider byte.

## Architecture consequence

The Obsidian runtime graphics composition is better represented as:

```text
app.obsidian locality
    libEGL.so
    libGLESv2.so
    libvulkan.so.1

provider.graphics.vulkan.glibc
    driver component
    layer component

provider.graphics.gbm.glibc
    GBM component

kernel/device interface
    /dev/kgsl-3d0
```

This is a semantic composition model, not yet a final physical packaging design.

## Next gate

Before candidate materialization:

```text
1. rerun refined classifier and verify total 161, review 0
2. preserve process-class graphics mapping report
3. inspect PID 27444 command line from processes.tsv
4. audit APP_LOCAL vs external SONAME collisions
5. derive rootfs ELF static closure and compare against runtime-selected ELF set
```
