# 0048 — Zink Frontend and Cross-Version Graphics Composition Confirmed

## Status

The explicit-Freedreno GLX probe map enrichment completed successfully.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/explicit-maps-20260711-012434
```

The enrichment attached:

```text
path class
package owner
package version
SHA-256
Build ID
SONAME
state
```

to every normalized mapped path.

## Renderer identity

The successful probe reported:

```text
GLX_VERSION=1.4
GL_VENDOR=Mesa
GL_RENDERER=zink Vulkan 1.4(Turnip Adreno (TM) 730 (MESA_TURNIP))
GL_VERSION=4.6 (Compatibility Profile) Mesa 25.0.7-2
```

## Zink/Gallium frontend provenance

The enriched maps contain:

```text
$ROOTFS/usr/lib/aarch64-linux-gnu/libgallium-25.0.7-2.so
```

Package provenance:

```text
mesa-libgallium:arm64
version 25.0.7-2
```

Build ID:

```text
8808ec9df277b745c9b2e2033a2799e1976911d9
```

SHA-256:

```text
333dfaa45db020be43045149404252cdbc99b7338cd14adffe464758f6d0ac20
```

The Mesa documentation defines Zink as a Gallium driver that emits Vulkan API calls.

Combined evidence:

```text
renderer identity reports Zink
rootfs mesa-libgallium 25.0.7 object is mapped
explicit Vulkan provider is Turnip/Freedreno from a separate Mesa provider store
```

Therefore the tested composition supports the following physical interpretation:

```text
rootfs Mesa 25.0.7 Gallium/Zink frontend
    -> prefix Vulkan loader/support plane
    -> Mesa provider-store Turnip/Freedreno driver
    -> KGSL device
```

The exact internal symbol-to-file layout of every Zink function is not required for this bounded provider-graph conclusion. The renderer identity and mapped Gallium provider object establish the application-facing Gallium/Zink side of the tested path.

## Rootfs GL/GLX plane provenance

Observed objects:

```text
libGL.so.1.7.0
    package libgl1:arm64
    version 1.7.0-1+b2

libGLX.so.0.0.0
    package libglx0:arm64
    version 1.7.0-1+b2

libGLdispatch.so.0.0.0
    package libglvnd0:arm64
    version 1.7.0-1+b2

libGLX_mesa.so.0.0.0
    package libglx-mesa0:arm64
    version 25.0.7-2
```

This separates the vendor-neutral GL/GLX dispatch layer from the Mesa GLX vendor implementation and Gallium/Zink frontend package lineage.

## Prefix Vulkan/support plane provenance

Observed objects include:

```text
libvulkan.so.1.3.301
    package vulkan-icd-loader-glibc
    version 1.3.301

libdrm.so.2.124.0
libdrm_amdgpu.so.1.124.0
    package libdrm-glibc
    version 2.4.124

libxcb-dri3.so.0.1.0
    package libxcb-glibc
    version 1.17.0-1
```

Mapped presence is not equivalent to selected hardware path.

In particular, the presence of `libdrm_amdgpu.so` is not evidence that an AMD device path was selected.

The selected hardware path is supported by the combined observation of:

```text
Zink renderer identity naming Turnip Adreno 730
mapped libvulkan_freedreno.so
mapped /dev/kgsl-3d0
```

## Mesa provider-store Vulkan driver

Observed object:

```text
$HOME/gl/opt/mesa-glibc-26.1.4-full/lib/libvulkan_freedreno.so
```

SHA-256:

```text
bc88f566f986486464d92f3b160c1b4028f94509661c8c874a7671631dff0eec
```

Build ID:

```text
29bb37b585a0905a979afad60ff9e4022c89c66b
```

SONAME:

```text
libvulkan_freedreno.so
```

This is physically separate from the rootfs Mesa 25.0.7 Gallium/Zink frontend lineage.

## Confirmed tested graph

```text
GL/GLX dispatch
    rootfs libglvnd/libGL/libGLX 1.7.0
        ↓
Mesa GLX vendor
    rootfs libglx-mesa 25.0.7-2
        ↓
Gallium/Zink frontend
    rootfs mesa-libgallium 25.0.7-2
        ↓
Vulkan loader and support
    Termux glibc-prefix packages
        ↓
Turnip/Freedreno Vulkan driver
    Mesa provider store 26.1.4 lineage
        ↓
KGSL device interface
```

This is a tested cross-version graphics composition.

The correct claim is:

```text
this exact captured combination works for the bounded GLX probe
```

not:

```text
arbitrary Mesa versions are mutually compatible
```

## Architecture consequence

The evidence strongly rejects a single coarse object such as:

```text
one Mesa provider owns the entire graphics stack
```

The runtime graph contains independently supplied layers:

```text
GLVND dispatch
Mesa GLX vendor
Gallium/Zink frontend
Vulkan loader/support
concrete Vulkan driver
kernel device interface
runtime caches
```

These layers have different package provenance, version lineages, and lifecycle authorities.

The target architecture should therefore preserve separate capability ownership at least conceptually:

```text
provider.graphics.opengl.glibc
provider.graphics.vulkan.glibc
bridge/device capability
runtime graphics cache
```

Physical packaging may later combine some components if evidence and lifecycle authority justify it, but semantic ownership must not be inferred solely from common upstream origin.

## Next gate

The explicit physical graph is now sufficiently characterized for A/B comparison.

Next:

```text
1. capture the same GLX probe under implicit-discovery
2. enrich the implicit maps with the same provenance script
3. compare:
    renderer identity
    mapped provider roots
    package/version graph
    device-node participation
    runtime cache participation
4. only then proceed to Electron adapters
```
