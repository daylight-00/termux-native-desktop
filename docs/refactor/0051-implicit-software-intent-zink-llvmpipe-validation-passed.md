# 0051 — Implicit Software-Intent Zink/Llvmpipe Validation Passed

## Status

The one-variable software-intent control passed.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/implicit-software-maps-20260711-025042
```

The control retained:

```text
VULKAN_POLICY_MODE=implicit-discovery
VK_DRIVER_FILES unset
VK_ICD_FILENAMES unset
```

and added only:

```text
LIBGL_ALWAYS_SOFTWARE=1
```

The same experiment-owned GLX probe reached renderer identity and the map capture, provenance enrichment, and explicit-vs-software graph comparison all passed.

## Renderer result

Observed software control renderer identity:

```text
GLX_VERSION=1.4
GL_VENDOR=Mesa
GL_RENDERER=zink Vulkan 1.4(llvmpipe (LLVM 19.1.7, 128 bits) (MESA_LLVMPIPE))
GL_VERSION=4.6 (Compatibility Profile) Mesa 25.0.7-2
```

Therefore the previously discovered CPU physical device becomes a valid Zink/GLX/OpenGL path when software CPU intent is explicit.

## Completed three-state matrix

The bounded Zink/GLX experiment now has three directly observed states.

### Explicit hardware provider, default device intent

```text
provider policy:
    explicit-freedreno

device-class intent:
    default

renderer:
    zink Vulkan 1.4(Turnip Adreno (TM) 730 (MESA_TURNIP))

result:
    PASS
```

### Implicit discovery, default device intent

```text
provider policy:
    implicit-discovery

device-class intent:
    default

loader result:
    llvmpipe CPU pdev enumerated

Zink result:
    CPU pdev rejected in default path

result:
    FAIL before renderer identity
```

### Implicit discovery, explicit software device intent

```text
provider policy:
    implicit-discovery

device-class intent:
    software CPU

selected renderer identity:
    Zink over MESA_LLVMPIPE

result:
    PASS
```

This closes the immediate causal question introduced by `0050`.

## Hardware graph versus software graph

The graph comparison completed successfully.

Explicit hardware renderer:

```text
zink Vulkan 1.4(Turnip Adreno (TM) 730 (MESA_TURNIP))
```

Software renderer:

```text
zink Vulkan 1.4(llvmpipe (LLVM 19.1.7, 128 bits) (MESA_LLVMPIPE))
```

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

## Selected provider versus mapped discovery attempt

The software map contains both:

```text
libvulkan_lvp.so
libvulkan_gfxstream.so
```

but these must not be assigned the same semantic role.

Actual selected rendering identity is established by:

```text
GL_RENDERER=... llvmpipe ... (MESA_LLVMPIPE)
```

and the corresponding mapped LVP driver:

```text
libvulkan_lvp.so
```

The previous loader diagnostics showed that Gfxstream was discovered and loaded far enough to participate in loader probing, but exposed no surviving physical device and was removed from physical-device consideration.

Therefore:

```text
mapped Vulkan ICD object
    !=
selected rendering provider
```

For this control:

```text
selected Vulkan software provider:
    Lavapipe / llvmpipe

additional mapped discovery-attempt ICD:
    Gfxstream
```

This distinction is required for future provenance and candidate-closure logic.

## Shared and differing graph layers

Both hardware and software controls share the application-facing graphics composition layers:

```text
rootfs GLVND dispatch
rootfs Mesa GLX vendor implementation
rootfs Gallium/Zink frontend
rootfs Mesa device-selection layer
prefix Vulkan loader/support plane
```

The provider/device tail differs.

Hardware tail:

```text
provider-store Turnip/Freedreno
    -> KGSL device interface
```

Software tail:

```text
rootfs Lavapipe
    -> llvmpipe CPU execution
```

The successful controls therefore support the conceptual graph:

```text
OpenGL/GLX consumer
    -> GLVND / Mesa GLX
    -> Gallium/Zink frontend
    -> Vulkan loader/support plane
    -> selected Vulkan provider tail
         hardware: Turnip/Freedreno -> KGSL
         software: Lavapipe -> llvmpipe CPU
```

## Package-provenance observations

The software graph contains:

```text
ROOTFS mesa-vulkan-drivers:arm64 25.0.7-2
    object count: 3
```

corresponding in the graphics-focused set to:

```text
libVkLayer_MESA_device_select.so
libvulkan_gfxstream.so
libvulkan_lvp.so
```

The hardware graph contains only one rootfs `mesa-vulkan-drivers` object in the captured set, the Mesa device-selection layer, while the selected concrete Vulkan driver comes from the separately managed Mesa provider store.

This reinforces that one package count or one upstream family name is insufficient to describe runtime role.

## Runtime anonymous object classification gap

The software control contains:

```text
/memfd:allocation
```

which the current enrichment script reports as:

```text
path_class=OTHER
package=UNKNOWN
version=UNKNOWN
```

This should not be interpreted as an unresolved provider dependency.

It is a non-filesystem runtime memory object captured from process maps. Its presence is evidence that the current path classifier needs a narrow runtime-anonymous-memory class.

Until classification is corrected, the safe interpretation is:

```text
/memfd:allocation
    runtime anonymous memory object
    not package-provenance evidence
    not candidate-provider closure evidence
```

The exact producer or use of that mapping is not established by the current evidence and must not be inferred from the name alone.

## Architecture conclusion

The experiment now directly proves that the following are independent composition dimensions:

```text
provider discovery/selection policy
    and
consumer device-class intent
```

The pass/fail matrix is:

```text
explicit hardware provider + default intent
    PASS -> Turnip/KGSL

implicit discovery + default intent
    FAIL -> CPU pdev discovered but rejected

implicit discovery + software intent
    PASS -> Lavapipe/llvmpipe
```

Therefore a final launch composition model must not encode graphics behavior as one boolean such as:

```text
GPU=0/1
```

or derive device-class intent from whether:

```text
VK_DRIVER_FILES
```

is set.

At minimum the contract requires separate inputs for:

```text
application feature intent
provider discovery/selection policy
device-class intent
consumer validation gate
actual selected-provider evidence
```

## What this does not prove

This result does not prove:

```text
implicit discovery is the final desired software policy
all discovered ICDs are valid candidate members
Gfxstream is selected for rendering
all Electron consumers should inherit LIBGL_ALWAYS_SOFTWARE
explicit Lavapipe selection is unnecessary
hardware/software provider policy should be globally shared
```

The result is bounded to the tested Zink/GLX consumer and captured runtime state.

## Next gate

The immediate Zink causal question is closed.

Before promoted policy changes or candidate materialization, proceed to real consumer adapter validation while preserving the now-proven independent dimensions.

Recommended order:

```text
1. classify runtime-anonymous memfd objects separately from provider files
2. Obsidian explicit-freedreno adapter control
3. Obsidian implicit-discovery adapter control comparison
4. VS Code explicit-freedreno GPU adapter validation
5. VS Code CPU/software-intent behavior check
6. compare consumer-specific policy requirements
7. only then define the minimum graphics composition contract
```

Do not add new global graphics policy or modify promoted launchers yet.
