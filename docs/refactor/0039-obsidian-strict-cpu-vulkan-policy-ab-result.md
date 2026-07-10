# 0039 — Obsidian Strict CPU Vulkan Policy A/B Result

## Status

The strict CPU A/B experiment completed successfully.

Baseline control:

```text
GL_GPU=0
--disable-gpu
VK_DRIVER_FILES set by gl/env
VK_ICD_FILENAMES set by gl/env
```

Strict CPU control:

```text
same application payload
same shared gl/env composition
same CPU-mode Chromium flags
VK_DRIVER_FILES unset after sourcing gl/env
VK_ICD_FILENAMES unset after sourcing gl/env
```

The strict control passed:

```text
topology gate: PASS
required classes: main renderer zygote
startup stabilization: 3 seconds
survival gate: PASS
survival duration: 60 seconds
final process classes:
    main
    zygote x3
    utility
    renderer
```

The strict control evidence root is:

```text
$PREFIX/tmp/selected-obsidian-strict-cpu-20260710-235208
```

## Graphics relation A/B

### Baseline

The baseline graphics relation contained:

```text
main:
    libgbm.so

renderer:
    libgbm.so

utility:
    libgbm.so

zygote:
    AppDir libEGL.so
    AppDir libGLESv2.so
    AppDir libvulkan.so.1
    Mesa libvulkan_freedreno.so
    rootfs libVkLayer_MESA_device_select.so
    rootfs libgbm.so
    /dev/kgsl-3d0
```

### Strict CPU

The strict CPU relation contained:

```text
main:
    libgbm.so

renderer:
    libgbm.so

utility:
    libgbm.so

zygote:
    AppDir libEGL.so
    AppDir libGLESv2.so
    AppDir libvulkan.so.1
    rootfs libVkLayer_MESA_device_select.so
    rootfs libgbm.so
```

### Exact graphics delta

The strict CPU control removed exactly these two observed graphics relations:

```text
libvulkan_freedreno.so
/dev/kgsl-3d0
```

The following remained:

```text
AppDir libEGL.so
AppDir libGLESv2.so
AppDir libvulkan.so.1
Mesa device-select layer
GBM across main/renderer/utility/zygote classes
```

## Causal interpretation

The A/B changed only the Vulkan provider-selection environment after shared environment composition and before launch.

The strict control retained the same process topology and survived the bounded observation interval while:

```text
Freedreno driver mapping disappeared
KGSL device-node mapping disappeared
```

Therefore the evidence supports the following causal conclusion for this workload and captured environment:

```text
global Vulkan provider-selection policy
    was sufficient to cause or enable
concrete Freedreno driver loading
    and
KGSL device participation
inside the nominal CPU-mode control
```

This is stronger than the earlier correlation-only hypothesis.

The evidence does not prove that the two environment variables are the only possible mechanism by which a graphics provider could be selected. It proves that removing them in this bounded A/B removed the captured driver/device relation while preserving workload topology and survival.

## What remained graphics-related

Strict CPU still mapped:

```text
AppDir Vulkan/EGL/GLES libraries
Mesa device-selection layer
GBM
```

Therefore these objects are not explained solely by the explicit Freedreno ICD-selection environment.

Possible causes include:

```text
application-local loader linkage
Chromium/Electron graphics initialization
implicit Vulkan layer discovery
GBM probing or infrastructure use
```

No stronger claim is made without separate evidence.

## Whole runtime-set difference

The baseline and strict runs were not identical at the whole mapped-object-set level.

Path-class totals:

```text
baseline:
    APP_LOCAL        11
    OTHER_ABSOLUTE   26
    PREFIX_GLIBC     59
    ROOTFS_PROVIDER  65
    total           161

strict:
    APP_LOCAL        12
    OTHER_ABSOLUTE   23
    PREFIX_GLIBC     60
    ROOTFS_PROVIDER  74
    total           169
```

Refined semantic-count differences included:

```text
strict:
    +1 APP_LOCAL_ELF
    -1 DEVICE_NODE_GPU
    -1 Vulkan driver
    +1 PROVIDER_PREFIX_ELF
    +9 generic PROVIDER_ROOTFS_ELF
    -1 RUNTIME_CACHE_MESA
```

These broader differences must not be attributed to Vulkan environment removal without exact path-set analysis.

The experiment now includes:

```text
compare-control-semantic-sets.sh
```

which reports:

```text
baseline-only paths
strict-only paths
class/path set deltas
common-path semantic-class changes
per-class delta summary
```

## Architecture decision

The A/B result invalidates Vulkan provider-selection variables as unconditional shared world environment policy.

The target ownership is:

```text
provider.graphics.vulkan.glibc
```

not:

```text
world.glibc baseline environment
```

The policy direction is therefore:

```text
gl/env
    must not remain the final owner of unconditional VK_DRIVER_FILES / VK_ICD_FILENAMES selection

graphics-enabled launch composition
    should opt into provider.graphics.vulkan.glibc policy

CPU/non-graphics application composition
    should not inherit Vulkan provider selection by default
```

This is an architecture decision, not yet a global implementation patch.

Before editing the promoted shared environment, inventory and migrate every real consumer that currently relies on the global variables.

## Next order

```text
1. exact baseline/strict semantic path-set comparison
2. identify whether strict-only objects are deterministic capability additions or run variance
3. inventory current VK_* consumers on the refactor branch
4. define narrow graphics-provider composition contract
5. audit APP_LOCAL versus external SONAME collisions
6. compare rootfs ELF static closure against runtime-selected ELF set
7. only then design Obsidian candidate composition
```

Candidate materialization remains blocked.
