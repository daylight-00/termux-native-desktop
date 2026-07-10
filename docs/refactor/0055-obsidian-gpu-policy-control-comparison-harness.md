# 0055 — Obsidian GPU Policy-Control Comparison Harness

## Status

A dedicated comparison helper has been added for the Obsidian GPU-path provider-policy A/B:

```text
experiments/glibc/vulkan-policy-composition/recipe/compare-obsidian-policy-controls.sh
```

## Inputs

The helper accepts:

```text
EXPLICIT_OUT
    Obsidian GL_GPU=1 + explicit-freedreno evidence root

IMPLICIT_OUT
    Obsidian GL_GPU=1 + implicit-discovery evidence root
```

Both evidence roots must already contain:

```text
processes.tsv
mapped-objects.tsv
semantic-objects.tsv
```

## Outputs

The helper writes a comparison directory under the implicit evidence root by default and preserves:

```text
explicit-process-class-counts.tsv
implicit-process-class-counts.tsv

explicit-semantic-class-path.tsv
implicit-semantic-class-path.tsv
explicit-only-semantic-class-path.tsv
implicit-only-semantic-class-path.tsv

explicit-graphics-relations.tsv
implicit-graphics-relations.tsv
explicit-only-graphics-relations.tsv
implicit-only-graphics-relations.tsv
```

## Comparison principle

The helper compares controls with the same application feature mode:

```text
CONTROL_GL_GPU=1
```

and differs only in provider policy:

```text
explicit-freedreno
```

versus:

```text
implicit-discovery
```

This avoids treating the older CPU-control object counts as direct provider-policy deltas.

## Graphics relation scope

The comparison tracks process-class relations for the observed graphics objects:

```text
libvulkan_freedreno.so
libvulkan_lvp.so
libvulkan_gfxstream.so
libVkLayer_MESA_device_select.so
libgbm.so*
libvulkan.so.1
libEGL.so
libGLESv2.so
/dev/kgsl-3d0
```

The purpose is to distinguish:

```text
mapped object set
    from
process-class ownership relation
```

and:

```text
mapped ICD object
    from
selected rendering provider
```

## Claim boundary

The helper reports exact set differences and process-class relations. It does not infer:

```text
actual command submission
frame production
rendering correctness
provider preference order
```

Those require consumer-specific evidence beyond process maps.

## Execution order

After the implicit GPU-path capture completes:

```text
capture
    -> identity enrichment
    -> semantic classification
    -> graphics process mapping report
    -> exact policy-control comparison
```

No promoted launcher or global environment policy should change before this A/B is interpreted.
