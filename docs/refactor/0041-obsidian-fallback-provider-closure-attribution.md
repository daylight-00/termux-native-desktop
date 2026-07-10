# 0041 — Obsidian Fallback Provider Closure Attribution

## Status

The bounded static DT_NEEDED attribution over the strict CPU control evidence completed successfully.

Strict evidence root:

```text
$PREFIX/tmp/selected-obsidian-strict-cpu-20260710-235208
```

Fallback analysis output:

```text
fallback-provider-closures/
```

Result:

```text
unresolved edges: 0
ambiguous mapped SONAME edges: 0
```

## Strict-only attribution result

The exact strict-only set contained 11 paths.

All 11 are attributable to one of the three alternate Vulkan provider roots in the strict mapped ELF universe.

### SwiftShader root

```text
libvk_swiftshader.so
```

Strict-only attribution:

```text
swiftshader = 1
lvp         = 0
gfxstream   = 0
```

No additional strict-only path is needed to explain its mapped-universe DT_NEEDED reachability. This does not mean the object has no dependencies; dependencies already common to baseline and strict are outside the strict-only delta.

### Lavapipe root and strict-only closure

Root:

```text
libvulkan_lvp.so
```

Strict-only paths reachable from the LVP root:

```text
libvulkan_lvp.so
libLLVM.so.19.1
libz3.so.4
libxml2.so.2.9.14
libedit.so.2.0.75
libtinfo.so.6.5
libbsd.so.0.12.2
libmd.so.0.1.0
liblzma.so.5.6.4
```

Count:

```text
9
```

This resolves the previously provisional dependency-candidate cluster.

Within the captured strict mapped universe, the LVP DT_NEEDED graph accounts for:

```text
rootfs provider objects:
    libvulkan_lvp
    libLLVM
    libz3
    libxml2
    libedit
    libtinfo
    libbsd
    libmd

prefix provider object:
    liblzma
```

The result demonstrates that a single semantic provider closure may cross current physical supply roots.

### Gfxstream root

```text
libvulkan_gfxstream.so
```

Strict-only attribution:

```text
swiftshader = 0
lvp         = 0
gfxstream   = 1
```

No additional strict-only path is attributed to the Gfxstream root. As with SwiftShader, this means its mapped-universe reachable dependencies were already common to baseline and strict or were otherwise outside the strict-only delta; it does not prove a dependency-free object.

## Exact delta accounting

Baseline-only paths:

```text
Mesa shader-cache index
Freedreno Vulkan driver
KGSL device node
```

Count:

```text
3
```

Strict-only paths:

```text
SwiftShader root       1
LVP root + closure     9
Gfxstream root         1
```

Count:

```text
11
```

Therefore:

```text
baseline total = 161
strict total   = 169

161 - 3 + 11 = 169
```

The whole mapped-path count delta is structurally explained by the captured set difference.

## Architecture interpretation

The strict control did not merely remove one provider.

The observed transition is:

```text
explicit Freedreno policy
    -> Freedreno driver
    -> KGSL device participation

explicit override removed
    -> alternate/default discovery
    -> AppDir SwiftShader root
    -> rootfs Lavapipe closure
    -> rootfs Gfxstream root
```

The 11-object strict-only set is therefore not consistent with random lazy-load noise as the primary explanation.

It is a coherent alternate-provider composition.

## Claim boundary

The analysis algorithm is intentionally bounded.

It proves:

```text
DT_NEEDED reachability
within the ELF objects actually mapped by the strict control
using unique SONAME matches in that mapped universe
```

It does not prove:

```text
complete filesystem closure
all dlopen/plugin edges
manifest-discovery causality for every provider root
that all three alternate provider roots executed rendering work
that mapped-universe closures are globally disjoint
```

The strict-only attribution has no overlap among its 11 delta paths, but common baseline/strict dependencies may be shared by multiple roots.

## Semantic consequence

The graphics capability model must distinguish at least:

```text
explicit hardware provider
    Freedreno

app-local software provider
    SwiftShader

software Vulkan provider
    Lavapipe

virtual/streamed provider
    Gfxstream

layer/infrastructure
    Mesa device-select layer
    GBM

kernel/device participation
    KGSL
```

These capabilities cross physical supply roots:

```text
AppDir
Mesa provider store
Termux glibc prefix
Debian rootfs
kernel device namespace
```

Therefore physical source location is not a sufficient semantic owner.

## Next gate

Before changing the promoted environment:

```text
1. inventory every real VK_* producer and consumer
2. separate bionic session policy from glibc provider policy
3. define a narrow explicit glibc Vulkan composition contract
4. preserve gl-run behavior without making gl-run a lifecycle authority
5. migrate GPU-enabled application launch composition deliberately
6. then audit APP_LOCAL/external SONAME collisions
```

Candidate materialization remains blocked until the provider-selection contract is explicit.
