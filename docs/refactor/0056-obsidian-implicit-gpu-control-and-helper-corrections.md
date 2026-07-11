# 0056 — Obsidian Implicit GPU Control and Helper Corrections

## Status

The same-feature-mode Obsidian implicit-discovery GPU control passed its workload gates, but the first post-processing pass exposed three helper defects that required correction before final policy A/B interpretation.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/obsidian-implicit-gpu-20260711-105419
```

Launch inputs:

```text
CONTROL_GL_GPU=1
VULKAN_POLICY_MODE=implicit-discovery
LIBGL_ALWAYS_SOFTWARE unset
SURVIVAL_SECONDS=100
```

## Workload result

Observed:

```text
topology gate: PASS
startup stabilization elapsed: 3 seconds
survival gate: PASS
survival elapsed: 101 seconds
maps capture: PASS
identity enrichment: PASS
coverage: 169/169
semantic classification: PASS with one review object before memfd correction
```

Final process set:

```text
main      1
zygote    2
gpu       1
utility   1
renderer  1
```

Therefore the real Electron GPU-feature workload remains structurally alive under implicit discovery for the captured control.

## Initial semantic result

Before runtime-anonymous-memory correction, the semantic counts included:

```text
OTHER_RUNTIME_DATA_REVIEW                      1
PROVIDER_GRAPHICS_VULKAN_SOFTWARE_LVP_ELF     1
PROVIDER_GRAPHICS_VULKAN_VIRTUAL_GFXSTREAM_ELF 1
```

and did not include:

```text
DEVICE_NODE_GPU
PROVIDER_GRAPHICS_VULKAN_DRIVER_ELF
```

This establishes a strong policy difference from the explicit-Freedreno GPU control:

```text
explicit GPU control:
    provider-store Freedreno present
    KGSL present

implicit GPU control:
    Freedreno class absent
    KGSL class absent
    LVP present
    Gfxstream present
```

The actual selected implicit rendering provider is not yet claimed from maps alone.

## Explicit GPU process ownership result

The explicit GPU control process report established that the live `gpu` process directly maps:

```text
AppDir libEGL.so
AppDir libGLESv2.so
AppDir libvulkan.so.1
provider-store libvulkan_freedreno.so
rootfs libVkLayer_MESA_device_select.so
rootfs libgbm.so.1.0.0
/dev/kgsl-3d0
```

Other process classes map rootfs GBM but not the explicit hardware provider tail.

Therefore the scoped explicit control now supports the stronger bounded statement:

```text
Obsidian gpu process
    -> AppDir ANGLE/Vulkan-facing libraries
    -> provider-store Freedreno
    -> KGSL device node
```

for captured mappings.

This remains mapping evidence, not command-submission proof.

## Helper defect 1 — graphics reporter coverage gap

The original:

```text
report-graphics-process-mappings.sh
```

tracked:

```text
Freedreno
Mesa device-select layer
GBM
AppDir Vulkan/EGL/GLES
KGSL
```

but did not track:

```text
libvulkan_lvp.so
libvulkan_gfxstream.so
libvk_swiftshader.so
```

As a result, the first implicit GPU report omitted the alternate Vulkan provider objects even though semantic classification had already identified LVP and Gfxstream.

The reporter now includes all three alternate provider patterns.

## Helper defect 2 — non-portable multiline AWK condition

The first execution of:

```text
compare-obsidian-policy-controls.sh
```

failed with:

```text
awk: cmd. line:3:         NR > 1 && (
awk: cmd. line:3:                    ^ unexpected newline or end of string
```

The failure came from a multiline parenthesized AWK boolean expression that was not portable to the device awk implementation.

The comparison helper now uses the same shell-defined single expression model already proven by the portable graphics reporter:

```text
is_graphics_path_awk='...'
```

and injects it into a one-line AWK condition.

The corrected helper also tracks:

```text
Freedreno
LVP
Gfxstream
SwiftShader
Mesa device-select layer
GBM
AppDir Vulkan/EGL/GLES
KGSL
```

## Helper defect 3 — Obsidian memfd review false positive

The one semantic review object in the implicit GPU control is consistent with the already observed:

```text
/memfd:allocation
```

runtime anonymous mapping class.

The GLX enrichment path had already learned this narrow pattern, but the Obsidian enrichment/classifier pair had not.

The Obsidian pipeline now recognizes only the evidence-backed pattern:

```text
/memfd:allocation*
```

as:

```text
package=RUNTIME_MEMORY
version=NOT_APPLICABLE
state=RUNTIME_ANONYMOUS_MAPPING
semantic_class=RUNTIME_ANON_MEMORY
```

The classifier does not generalize all `/memfd:*` mappings into the same class.

## Current interpretation boundary

The current evidence proves:

```text
GL_GPU=1 + explicit-freedreno
    -> workload PASS
    -> gpu process present
    -> gpu process maps Freedreno and KGSL

GL_GPU=1 + implicit-discovery
    -> workload PASS
    -> gpu process present
    -> Freedreno/KGSL semantic classes absent
    -> LVP and Gfxstream objects present
```

The current evidence does not yet prove:

```text
whether LVP or Gfxstream is the selected Electron rendering provider
whether both alternate ICDs are mapped by the gpu process
whether the implicit gpu process uses software rendering successfully
whether rendering output correctness is equivalent
```

The corrected process report and exact policy comparison must run before stronger provider-selection claims.

## Required re-processing order

No new capture is required.

For the existing implicit evidence root:

```text
identity re-enrichment
semantic reclassification
expanded graphics process report
same-feature-mode exact policy comparison
```

The explicit evidence root only needs the expanded graphics process report rerun.

No promoted launcher or global environment policy should change before those corrected outputs are interpreted.
