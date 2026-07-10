# 0036 — Obsidian Graphics Provider and Device-Node Boundary

## Status

The first successful semantic classifier run reduced the Obsidian control review set to exactly two objects:

```text
OTHER_ABSOLUTE_ELF_REVIEW
    $HOME/gl/opt/mesa-glibc-26.1.4-full/lib/libvulkan_freedreno.so

MISSING_AT_ENRICHMENT
    /dev/kgsl-3d0
```

Both are now understood as classifier-model defects rather than unresolved provider objects.

## Review object 1 — Mesa Vulkan driver

The object:

```text
$HOME/gl/opt/mesa-glibc-26.1.4-full/lib/libvulkan_freedreno.so
```

is a concrete ELF object with:

```text
SHA-256:
    bc88f566f986486464d92f3b160c1b4028f94509661c8c874a7671631dff0eec

Build ID:
    29bb37b585a0905a979afad60ff9e4022c89c66b
```

It was previously classified as `OTHER_ABSOLUTE_ELF_REVIEW` only because the first classifier recognized AppDir, prefix, rootfs, cache, and mutable-state domains but did not recognize the existing Mesa provider store.

The semantic class is now:

```text
PROVIDER_GRAPHICS_VULKAN_ELF
```

This does not by itself prove which Vulkan physical device or adapter was selected, but it does prove that a concrete graphics-provider ELF object was mapped by the captured workload.

## Review object 2 — KGSL device node

The path:

```text
/dev/kgsl-3d0
```

was captured in the process maps but the first enrichment pass used:

```text
-f path
```

as its definition of a present identity-bearing object.

Because `/dev/kgsl-3d0` is a device node rather than a regular file, the tool incorrectly emitted:

```text
state = MISSING_AT_ENRICHMENT
```

The enrichment model now distinguishes:

```text
PRESENT regular file
DEVICE_NODE
PRESENT_NONREGULAR
MISSING_AT_ENRICHMENT
```

For device nodes it records:

```text
state = DEVICE_NODE
sha256 = NOT_APPLICABLE
build_id = NOT_APPLICABLE
```

The semantic class for this observed device path is:

```text
DEVICE_NODE_GPU
```

## Updated semantic decomposition

After rerunning enrichment and classification, the expected complete decomposition is:

```text
APP_LOCAL_DATA                 6
APP_LOCAL_ELF                  5
APP_MUTABLE_STATE             19
DEVICE_NODE_GPU                1
PROVIDER_FONT_DATA             4
PROVIDER_GRAPHICS_VULKAN_ELF   1
PROVIDER_LOCALE_DATA          12
PROVIDER_PREFIX_ELF           41
PROVIDER_ROOTFS_ELF           60
PROVIDER_SCHEMA_DATA           1
RUNTIME_CACHE_FONTCONFIG       4
RUNTIME_CACHE_MESA             1
WORLD_SUBSTRATE_ELF            6
```

Total:

```text
161 objects
```

Expected semantic review count:

```text
0
```

## Important graphics interpretation

The control launcher used:

```text
GL_GPU=0
```

and the promoted launcher translated that into a CPU-mode Chromium/Electron launch configuration including `--disable-gpu`.

However the captured runtime object set still contains graphics-related objects across multiple domains, including:

```text
APP_LOCAL:
    libvulkan.so.1
    libEGL.so
    libGLESv2.so

Mesa provider store:
    libvulkan_freedreno.so

rootfs:
    libVkLayer_MESA_device_select.so
    libgbm.so.1

kernel/device interface:
    /dev/kgsl-3d0
```

Therefore:

```text
CPU-mode launch flag
    !=
proof of graphics-provider non-participation
```

At the same time, mapped graphics objects and a device node do not alone prove:

```text
which process class mapped each graphics object
which ICD JSON was opened
which physical Vulkan device was selected
whether rendering work was actually submitted
whether a graphics path was used only for initialization/probing
```

Those are separate evidence claims.

## Next graphics evidence question

Before using this Obsidian control as evidence that the closure experiment is graphics-independent, inspect process-class-specific mappings for:

```text
libvulkan_freedreno.so
libVkLayer_MESA_device_select.so
libgbm.so.1
libvulkan.so.1
libEGL.so
libGLESv2.so
/dev/kgsl-3d0
```

The result should identify whether these objects belong to:

```text
main
renderer
utility
zygote
```

or multiple process classes.

## Architecture consequence

The Obsidian application domain now visibly composes another semantic capability:

```text
provider.graphics.vulkan.glibc
```

alongside:

```text
app-local payload
world substrate
locale provider
prefix ELF providers
rootfs ELF providers
font data
schema data
mutable state
runtime caches
device interface
```

This further supports capability-oriented composition and argues against treating all mapped paths as one monolithic application closure.

Candidate materialization remains blocked until:

```text
1. semantic review count reaches zero
2. graphics object process ownership is inspected
3. APP_LOCAL/external SONAME collision audit is completed
4. rootfs ELF static closure is compared against runtime selection
```
