# 0047 — Explicit Zink/Turnip Physical Provider Graph

## Status

The explicit-Freedreno GLX renderer probe was rerun with a bounded hold and `/proc/<pid>/maps` capture.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/explicit-maps-20260711-012434
```

The probe again reported:

```text
GLX_VERSION=1.4
GL_VENDOR=Mesa
GL_RENDERER=zink Vulkan 1.4(Turnip Adreno (TM) 730 (MESA_TURNIP))
GL_VERSION=4.6 (Compatibility Profile) Mesa 25.0.7-2
```

Policy identity:

```text
VULKAN_POLICY_MODE=explicit-freedreno
VK_DRIVER_FILES=$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json
```

## Captured graphics-related physical paths

### Mesa provider store

```text
$HOME/gl/opt/mesa-glibc-26.1.4-full/lib/libvulkan_freedreno.so
```

Role:

```text
explicit Turnip/Freedreno Vulkan driver provider
```

### Termux glibc prefix

```text
$PREFIX/glibc/lib/libvulkan.so.1.3.301
$PREFIX/glibc/lib/libdrm.so.2.124.0
$PREFIX/glibc/lib/libdrm_amdgpu.so.1.124.0
$PREFIX/glibc/lib/libxcb-dri3.so.0.1.0
```

Observed role family:

```text
Vulkan loader
DRM support
XCB DRI3 support
```

The exact semantic owner of each prefix object remains package/provenance driven; physical prefix location alone is not world ownership.

### Debian/rootfs GL and GLX plane

```text
$ROOTFS/usr/lib/aarch64-linux-gnu/libGL.so.1.7.0
$ROOTFS/usr/lib/aarch64-linux-gnu/libGLX.so.0.0.0
$ROOTFS/usr/lib/aarch64-linux-gnu/libGLX_mesa.so.0.0.0
$ROOTFS/usr/lib/aarch64-linux-gnu/libGLdispatch.so.0.0.0
```

This is concrete evidence that the successful OpenGL/GLX consumer path uses the rootfs-supplied GL/GLX dispatch/vendor plane while the explicitly selected Vulkan driver comes from the separate Mesa provider store.

### Device interface

```text
/dev/kgsl-3d0
```

The explicit policy path therefore reaches the KGSL device interface.

### Runtime caches

```text
$HOME/.cache/mesa_shader_cache/index
$HOME/.cache/mesa_shader_cache_db/index
```

These remain mutable runtime state, not provider bytes.

## Physical composition result

The successful tested composition is:

```text
GLX/OpenGL dispatch and Mesa GLX vendor plane
    Debian/rootfs
        ↓
OpenGL renderer
    Zink
        ↓
Vulkan loader/support plane
    Termux glibc prefix
        ↓
Turnip/Freedreno Vulkan driver
    Mesa provider store 26.1.4 lineage
        ↓
KGSL device interface
```

This is a real cross-supply-root composition, not a theoretical target diagram.

## GLVND interpretation

The rootfs mapping contains the expected GLVND/GLX dispatch pieces:

```text
libGL
libGLX
libGLdispatch
```

and the Mesa GLX vendor library:

```text
libGLX_mesa
```

This is consistent with a vendor-neutral GL dispatch layer plus a Mesa GLX vendor implementation.

The maps establish the physical objects. The architecture conclusion is that the successful application-facing GLX/OpenGL plane is distinct from the explicitly selected Vulkan driver provider plane.

## Zink frontend path remains partially unresolved

The renderer string proves a working Zink path, but the first graphics-path filter did not expose a file named:

```text
zink_dri.so
```

The next evidence must inspect the complete mapped path set, including generic Mesa/Gallium objects such as:

```text
libgallium*
```

and enrich every mapped path with:

```text
path class
package owner
package version
SHA-256
Build ID
SONAME
```

The experiment now includes:

```text
recipe/enrich-glx-probe-maps.sh
```

for that purpose.

## Architecture consequence

The current evidence strongly supports separate semantic capabilities:

```text
provider.graphics.opengl.glibc
    application-facing GL/GLX/Zink plane

provider.graphics.vulkan.glibc
    Vulkan loader policy and concrete driver selection

kernel/device interface
    KGSL
```

These capabilities currently compose across:

```text
Debian/rootfs supply
Termux glibc-prefix packages
Mesa provider store
kernel device namespace
```

Therefore the final architecture must not assume:

```text
one Mesa version
one physical directory
one supply root
one provider package
```

for the entire graphics stack.

At the same time, this one successful composition does not prove arbitrary cross-version compatibility. It proves only the exact captured graph.

## Next gate

```text
1. enrich the captured explicit probe maps
2. identify the actual Mesa/Gallium/Zink frontend object path and package version
3. record package provenance for GLVND, Mesa GLX vendor, Vulkan loader, DRM, and XCB DRI3 objects
4. then capture the same probe under implicit-discovery
5. compare renderer identity and physical provider graph
```

Electron consumer validation remains after the GLX consumer A/B is fully characterized.
