# 0060 — Obsidian Implicit Loader Selected LVP / llvmpipe

## Status

The bounded Obsidian implicit-discovery loader-debug experiment produced direct loader-level provider-selection evidence.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/obsidian-implicit-loader-debug-20260711-123513
```

Inputs:

```text
CONTROL_GL_GPU=1
VULKAN_POLICY_MODE=implicit-discovery
LIBGL_ALWAYS_SOFTWARE unset
VK_LOADER_DEBUG=all
SURVIVAL_SECONDS=30
```

Workload result:

```text
topology gate: PASS
startup elapsed: 5 seconds
survival gate: PASS
survival elapsed: 30 seconds
```

Final process topology:

```text
main      1
zygote    2
gpu       1
utility   1
renderer  1
```

## Loader result

The loader diagnostics repeatedly expose only this physical-device identity:

```text
llvmpipe (LLVM 19.1.7, 128 bits)
```

The log repeatedly states:

```text
Using "llvmpipe (LLVM 19.1.7, 128 bits)"
with driver:
$HOME/gl/lib/libvulkan_lvp.so
```

The loader also removes the discovered Gfxstream and Freedreno drivers because they expose no physical devices:

```text
libvulkan_gfxstream.so
    -> removed: no physical devices

libvulkan_freedreno.so
    -> removed: no physical devices
```

Other discovered non-viable ICDs are likewise removed:

```text
Broadcom
Virtio
Radeon
Panfrost
Nouveau
```

The Gfxstream ICD also reports:

```text
vkEnumerateInstanceVersion returned error
```

and is treated as a Vulkan 1.0 ICD before later removal for exposing no physical devices.

No Turnip/Adreno identity appears in the loader-debug capture.

## Selection conclusion

For this bounded Obsidian implicit-discovery control, the desktop Vulkan loader selected:

```text
provider family:
    Lavapipe

Vulkan ICD:
    libvulkan_lvp.so

physical device identity:
    llvmpipe (LLVM 19.1.7, 128 bits)
```

Therefore the earlier ambiguity:

```text
LVP mapped
Gfxstream mapped
selected provider unresolved
```

is now resolved at loader-selection level as:

```text
LVP / llvmpipe selected
Gfxstream discovery/loading participation observed
Gfxstream removed from viable driver set
```

## Process attribution boundary

The loader log is aggregated through the captured Electron process tree and does not carry PID tags on each Vulkan Loader line.

Therefore the strongest direct statement is:

```text
the captured Obsidian process tree selected LVP / llvmpipe
```

The earlier same-feature-mode process-map control showed:

```text
only the gpu process maps:
    libvulkan_lvp.so
    libvulkan_gfxstream.so
```

Combining the independent controls strongly supports the inference that the Electron GPU-process graphics path is the LVP/llvmpipe path under implicit discovery.

That inference is stronger than map presence alone but is still distinguished from a PID-tagged selection log.

## Loader-reported path versus mapped canonical path

The loader reports:

```text
$HOME/gl/lib/libvulkan_lvp.so
```

while process maps from the earlier implicit control show the canonical mapped object under the Debian rootfs path.

This is consistent with the current broad-farm implementation:

```text
~/gl/lib/<soname>
    -> symlink to rootfs shared object
```

The current `gl-farm` implementation creates `~/gl/lib` symlinks from Debian rootfs `.so*` objects and then refreshes the glibc loader cache.

Therefore the semantic interpretation is:

```text
loader resolution route:
    broad-farm alias path

physical supplied object:
    rootfs Mesa LVP provider

semantic provider identity:
    Lavapipe software Vulkan provider
```

This is another reason not to treat:

```text
physical lookup path
```

as equivalent to:

```text
semantic provider ownership boundary
```

The broad farm is observed here as a compatibility resolution surface, not as proof that all farm contents form one valid production provider object.

## Same-feature-mode policy result is now stronger

The completed Obsidian GPU-path A/B can now be written as:

```text
same application feature mode:
    GL_GPU=1

same captured process topology:
    main / zygote / gpu / utility / renderer

same workload result:
    topology PASS
    survival PASS
```

with provider tails:

```text
explicit-freedreno:
    provider-store Freedreno/Turnip
    -> KGSL
    -> hardware provider tail

implicit-discovery:
    rootfs Lavapipe
    -> llvmpipe CPU physical device
    -> software provider tail
```

## Architecture consequence: GL_GPU is not hardware identity

This experiment proves that:

```text
GL_GPU=1
```

means application GPU/Vulkan feature-mode argv intent, not:

```text
hardware acceleration selected
```

For the tested Obsidian consumer:

```text
GL_GPU=1 + explicit-freedreno
    -> hardware Turnip/KGSL path

GL_GPU=1 + implicit-discovery
    -> software LVP/llvmpipe path
```

Both controls preserve the observed Electron process topology and pass their bounded survival gates.

Therefore the architecture must keep separate:

```text
application feature mode
provider discovery policy
selected provider identity
device class
hardware/software acceleration property
```

No one boolean or global environment side effect can represent all five dimensions correctly.

## Cross-consumer result

The combined consumer matrix is now:

```text
standalone Zink:
    explicit-freedreno + default intent
        -> Turnip/KGSL
        -> PASS

    implicit-discovery + default intent
        -> llvmpipe discovered
        -> CPU pdev rejected by default Zink path
        -> FAIL

    implicit-discovery + explicit software intent
        -> LVP/llvmpipe
        -> PASS

Obsidian Electron:
    GL_GPU=1 + explicit-freedreno
        -> Freedreno/KGSL mapped by gpu process
        -> PASS

    GL_GPU=1 + implicit-discovery
        -> LVP/llvmpipe selected at loader level
        -> Gfxstream removed from viable device set
        -> PASS
```

Therefore consumer-specific suitability remains a first-class architecture concern.

## Claim boundary

The current evidence establishes:

```text
loader-selected Vulkan provider identity
loader-visible physical-device identity
non-viable ICD removal
application topology and survival
```

It does not establish:

```text
frame-level rendering correctness equivalence
GPU/CPU performance equivalence
command-submission trace
pixel-output equivalence
whether all Electron rendering subsystems use Vulkan identically
```

Those are unnecessary for the current provider-policy architecture discrimination.

## Decision

The Electron implicit selected-provider question is closed strongly enough for the current architecture stage.

Do not add a more invasive Electron tracing stack merely to re-prove the same provider identity.

Proceed to the next consumer-validation gate:

```text
VS Code explicit-freedreno GPU-path control
VS Code alternate policy behavior
consumer requirement comparison
```

The promoted launchers and shared `gl/env` remain unchanged until the consumer comparison is complete.
