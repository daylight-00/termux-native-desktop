# 0050 — Implicit Loader Discovery and Zink CPU-Device Gate

## Status

The loader-side diagnostic capture for the failed implicit-discovery Zink/GLX path completed.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/implicit-loader-debug-20260711-022432
```

Observed workload exit status:

```text
6
```

The failure is no longer attributable to absent manifest discovery.

## Discovery result

With:

```text
VULKAN_POLICY_MODE=implicit-discovery
VK_DRIVER_FILES unset
VK_ICD_FILENAMES unset
VK_LOADER_DEBUG=error,warn,info,driver
MESA_LOADER_DRIVER_OVERRIDE=zink
```

the Vulkan loader searched the expected XDG/system data roots and discovered rootfs ICD manifests for:

```text
freedreno
gfxstream
lvp
nouveau
panfrost
radeon
virtio
broadcom
```

It also discovered the Mesa device-selection implicit layer:

```text
VkLayer_MESA_device_select.json
```

and inserted:

```text
VK_LAYER_MESA_device_select
```

## Driver/device result

The loader diagnostics show one surviving physical device:

```text
llvmpipe (LLVM 19.1.7, 128 bits)
```

The device-selection layer reported the same single device in original and sorted order.

The loader removed the following drivers because they exposed no physical devices in this environment:

```text
libvulkan_broadcom.so
libvulkan_virtio.so
libvulkan_radeon.so
libvulkan_panfrost.so
libvulkan_nouveau.so
libvulkan_gfxstream.so
libvulkan_freedreno.so
```

The diagnostics also recorded that `libvulkan_gfxstream.so` returned an error from `vkEnumerateInstanceVersion` and was treated as a Vulkan 1.0 ICD before later being removed for exposing no physical devices.

## Crucial supply-root distinction

The implicit loader discovered the rootfs manifest:

```text
$ROOTFS/usr/share/vulkan/icd.d/freedreno_icd.json
```

and searched for:

```text
libvulkan_freedreno.so
```

but that discovered rootfs driver path exposed no physical devices and was removed.

This is materially different from the explicit-Freedreno passing control, which selected:

```text
$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json
```

and mapped:

```text
$HOME/gl/opt/mesa-glibc-26.1.4-full/lib/libvulkan_freedreno.so
/dev/kgsl-3d0
```

with renderer identity:

```text
zink Vulkan 1.4(Turnip Adreno (TM) 730 (MESA_TURNIP))
```

Therefore:

```text
same semantic driver family name
    !=
same runtime capability
```

when physical supply root, provider build, and platform adaptation differ.

## Zink failure point

The loader did successfully enumerate one Vulkan physical device:

```text
llvmpipe
```

but Zink then emitted:

```text
ZINK: failed to choose pdev
```

The relevant Zink selection logic distinguishes normal device selection from an explicitly requested CPU/software path.

The source logic uses:

```text
LIBGL_ALWAYS_SOFTWARE
```

as a CPU-device selection signal. In the normal path, if the resulting Vulkan physical device is of CPU type and software rendering was not explicitly requested, Zink clears the selected physical device and fails selection.

The same source also treats the older:

```text
ZINK_USE_LAVAPIPE
```

as obsolete and directs users toward:

```text
LIBGL_ALWAYS_SOFTWARE
```

for the software path.

This explains the observed sequence:

```text
implicit loader discovery
    -> LVP exposes llvmpipe CPU pdev
    -> no software-rendering intent supplied
    -> Zink rejects CPU pdev in normal selection path
    -> failed to choose pdev
    -> GLX screen creation fails
```

## Refined A/B interpretation

The current Zink/GLX policy matrix is:

```text
explicit-freedreno
    provider selection: explicit hardware
    selected pdev: Turnip Adreno 730
    GLX/OpenGL result: PASS

implicit-discovery
    provider selection: default discovery
    surviving pdev: llvmpipe CPU
    software intent: absent
    Zink pdev selection: FAIL
    GLX/OpenGL result: FAIL
```

This is more precise than the previous provisional statement:

```text
implicit discovery did not provide a usable pdev
```

The loader did provide a Vulkan CPU pdev. The Zink consumer did not accept it because the software-rendering intent was not explicitly requested.

## Architecture consequence

Provider policy and consumer mode must remain separate dimensions.

The evidence now demonstrates at least:

```text
provider discovery policy
    explicit hardware
    implicit/default discovery

consumer device-class intent
    hardware/default
    explicit software CPU
```

These must not be collapsed into one boolean such as:

```text
GPU on/off
```

or inferred only from the existence of `VK_DRIVER_FILES`.

The tested Zink consumer requires both:

```text
which provider set is discoverable
```

and:

```text
whether CPU/software device selection is permitted
```

to be explicit parts of composition semantics.

## Next discriminating experiment

Do not add a promoted `software` mode yet.

Use the existing experiment primitives and change only one additional variable:

```text
VULKAN_POLICY_MODE=implicit-discovery
LIBGL_ALWAYS_SOFTWARE=1
```

with the same GLX probe and maps capture.

This tests:

```text
does the already-discovered llvmpipe pdev become a valid Zink consumer path
when software CPU intent is explicit?
```

Expected discriminating outcomes:

```text
PASS with Zink over llvmpipe
    -> confirms separate software-intent gate

FAIL before/after pdev selection
    -> identifies an additional capability or presentation constraint
```

If the software path passes, a later experiment may compare:

```text
implicit discovery + software intent
```

against a future deliberately scoped:

```text
explicit Lavapipe provider selection + software intent
```

before any final software-provider contract is designed.

## Stop line

Do not yet:

```text
add explicit-lavapipe to promoted policy
change gl/env
change gl-run
change Electron launchers
infer that all implicit discovery is broken
infer that llvmpipe is unsuitable for Zink
```

The next step is the one-variable software-intent control.
