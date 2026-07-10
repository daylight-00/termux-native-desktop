# 0050 — Implicit Loader Discovery Diagnostics

## Status

Loader-side diagnostics were captured for the failing implicit-discovery Zink/GLX path.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/implicit-loader-debug-20260711-022432
```

Observed workload exit status:

```text
6
```

The loader diagnostics refine the previous failure boundary substantially.

## Policy state

The run used:

```text
VULKAN_POLICY_MODE=implicit-discovery
VK_DRIVER_FILES unset
VK_ICD_FILENAMES unset
MESA_LOADER_DRIVER_OVERRIDE=zink
VK_LOADER_DEBUG=error,warn,info,driver
```

The Vulkan loader reported version:

```text
1.3.301
```

## Discovery search paths

The loader searched driver manifests under:

```text
$HOME/.config/vulkan/icd.d
$PREFIX/glibc/etc/xdg/vulkan/icd.d
$PREFIX/glibc/etc/vulkan/icd.d
$HOME/.local/share/vulkan/icd.d
$ROOTFS/usr/share/vulkan/icd.d
$ROOTFS/usr/local/share/vulkan/icd.d
```

The effective discovered ICD manifests came from the Debian/rootfs Vulkan data path.

## Discovered ICD manifest set

The loader discovered:

```text
freedreno_icd.json
gfxstream_vk_icd.json
lvp_icd.json
nouveau_icd.json
panfrost_icd.json
radeon_icd.json
virtio_icd.json
broadcom_icd.json
```

It therefore reached default multi-driver discovery successfully.

This is not a manifest-discovery failure.

## Layer discovery

The loader discovered and inserted:

```text
VK_LAYER_MESA_device_select
    libVkLayer_MESA_device_select.so
```

from the rootfs implicit-layer data path.

The rootfs Mesa overlay explicit-layer manifest was also discovered as layer data, but the observed active inserted instance layer in this run was the Mesa device-select layer.

## Driver initialization observations

The loader reported a Gfxstream compatibility warning:

```text
libvulkan_gfxstream.so
vkEnumerateInstanceVersion returned error
ICD treated as Vulkan 1.0
```

This did not become the final consumer-visible physical device path.

## Physical-device enumeration result

The loader's sorted physical-device list contained only:

```text
llvmpipe (LLVM 19.1.7, 128 bits)
```

The loader then reported removal of these drivers because they exposed no physical devices in this environment:

```text
libvulkan_broadcom.so
libvulkan_virtio.so
libvulkan_radeon.so
libvulkan_panfrost.so
libvulkan_nouveau.so
libvulkan_gfxstream.so
libvulkan_freedreno.so
```

The LVP path was not removed by that no-physical-device filter, and the remaining visible device identity was llvmpipe.

## Refined failure boundary

The failure can now be classified as:

```text
default manifest discovery: PASS
manifest parsing: PASS
multi-driver loading path: reached
implicit Mesa device-select layer: inserted
physical-device enumeration: PASS
visible physical-device set: llvmpipe only
rootfs hardware-driver device exposure: none
Zink usable-pdev selection: FAIL
GLX screen formation: FAIL
renderer identity gate: NOT REACHED
```

The final stderr remained:

```text
MESA: error: ZINK: failed to choose pdev
glx: failed to create drisw screen
failed to load driver: zink
glXChooseFBConfig found no pbuffer-capable RGBA config
```

## Architecture interpretation

The implicit failure is not caused by the loader failing to find Vulkan manifests.

The loader successfully discovered a broad rootfs driver set and obtained one visible physical device from the resulting composition.

The stronger evidence chain is:

```text
implicit discovery
    -> broad rootfs ICD manifest set discovered
    -> most hardware/virtual drivers expose no physical devices here
    -> llvmpipe remains visible
    -> Zink does not select a usable pdev
    -> GLX screen path fails
```

This establishes a critical contract distinction:

```text
discovery success
    !=
physical-device exposure
    !=
consumer suitability
```

## Rootfs Freedreno interpretation

The rootfs `freedreno_icd.json` was discovered and the loader attempted to use:

```text
libvulkan_freedreno.so
```

but the loader later removed that driver because it exposed no physical device in the tested environment.

This sharply distinguishes it from the explicit provider-store Freedreno path:

```text
provider-store Freedreno 26.1.4 lineage
    -> Turnip Adreno 730
    -> KGSL
    -> Zink/GLX PASS

rootfs-discovered Freedreno 25.0.7 lineage
    -> no physical device exposed in implicit run
```

The current evidence does not yet identify the exact implementation-level reason for that difference.

Do not infer one solely from package version or physical location.

## LVP/llvmpipe interpretation boundary

The loader exposed:

```text
llvmpipe (LLVM 19.1.7, 128 bits)
```

but Zink still failed with:

```text
failed to choose pdev
```

The loader log alone does not prove why Zink rejected or failed to use that device.

Possible classes of explanation include:

```text
Zink device suitability requirements
software-device policy
feature/extension mismatch
interaction with the discovered driver/layer set
```

No one of these is accepted without a discriminating experiment.

## Next discriminating experiment

The smallest useful next experiment is driver isolation, not another broad discovery run.

Test the same GLX/Zink probe against:

```text
A. provider-store Freedreno
    known passing control

B. rootfs LVP only
    tests whether llvmpipe is usable by Zink when isolated

C. rootfs Freedreno only
    tests whether the rootfs Freedreno path exposes a physical device when isolated
```

The comparison should preserve:

```text
same probe binary
same X display
same Zink override
same glibc baseline environment
same loader debug categories
```

Only the explicit driver manifest should vary.

## Claim boundary

This diagnostic proves the loader's observed discovery and enumeration behavior for this one run.

It does not prove:

```text
why Zink rejected llvmpipe internally
that LVP cannot work when isolated
that rootfs Freedreno can never expose KGSL
that all Electron consumers require explicit Freedreno
```

Those remain separate tests.
