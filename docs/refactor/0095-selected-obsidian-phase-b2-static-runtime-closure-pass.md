# 0095 — Selected Obsidian Phase B2 Static/Runtime Closure Pass

## Status

Phase B2 passed.

```text
analysis.status:
    PASS

next state:
    READY_FOR_CAPABILITY_GROUPING_DECISION

runtime launch:
    NO

promoted runtime mutation:
    NO
```

The result partitions the retained control ELF set into entrypoint-static, auxiliary app-local, and mapped-only dynamic/discovery objects while keeping non-ELF data capabilities separate.

It does not authorize candidate materialization.

## Authoritative receipt

Archive:

```text
selected-obsidian-phase-b2-static-runtime-closure-20260711-195310.tgz
```

Archive SHA-256:

```text
70847e572fc338f20b3369e4b8af71aa0f3033b47857bd956e9b55289ca2e65a
```

Contained evidence root:

```text
$PREFIX/tmp/selected-obsidian-closure/
    selected-obsidian-phase-b2-static-runtime-closure-20260711-195310
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    26546a015708765cd8a624a8bb4976a8db191d2a
```

Consumed Phase B1 root:

```text
$PREFIX/tmp/selected-obsidian-closure/
    selected-obsidian-phase-b1-retained-control-locality-20260711-192919
```

Phase B1 captured head:

```text
0d1307fd94c8115b0d0ce3d76a3a3d48957530f9
```

The archive contained only regular files and directories under one relative Termux path. No absolute path, parent traversal, symlink, device, or other special archive member was present.

## Primary result

```text
ELF objects:
    113

resolved DT_NEEDED edges:
    531

entrypoint-static closure:
    95

all-app-local static closure:
    98

mapped-only dynamic/discovery objects:
    15

non-ELF data capability objects:
    17

unresolved DT_NEEDED edges:
    0

ambiguous DT_NEEDED edges:
    0

duplicate provider lookup names:
    0
```

All required Phase B1 inputs were present on the authoritative device and all analysis gates passed.

## Independent verification

The uploaded TSV files were independently re-evaluated.

Verified:

```text
113 unique ELF paths
113 unique provider lookup names
531 resolved edges exactly match the Phase B1 DT_NEEDED/name mapping
95 objects reachable from the Obsidian entrypoint
98 objects reachable from the union of all APP_LOCAL ELF roots
15 objects outside every APP_LOCAL static graph
113 partition rows with no partition mismatch
17 non-ELF data capability rows
```

The independent partition matched the receipt exactly.

## Partition composition

```text
ENTRYPOINT_STATIC_CLOSURE
    APP_LOCAL_ELF                         2
    WORLD_SUBSTRATE_ELF                   6
    PROVIDER_PREFIX_ELF                  32
    PROVIDER_ROOTFS_ELF                  54
    PROVIDER_GRAPHICS_GBM_ELF             1

AUX_APP_LOCAL_STATIC_CLOSURE
    APP_LOCAL_ELF                         3

MAPPED_ONLY_DYNAMIC_OR_DISCOVERY
    PROVIDER_GRAPHICS_VULKAN_DRIVER_ELF   1
    PROVIDER_GRAPHICS_VULKAN_LAYER_ELF    1
    PROVIDER_PREFIX_ELF                   9
    PROVIDER_ROOTFS_ELF                   4
```

The auxiliary app-local roots are:

```text
libEGL.so
libGLESv2.so
libvulkan.so.1
```

Their dependencies are already present in the entrypoint-static closure.

## Dynamic root refinement

The 15 mapped-only objects are not 15 independent discovery roots.

Considering only edges between mapped-only objects, there are five roots with no incoming mapped-only dependency edge:

```text
libvulkan_freedreno.so
libVkLayer_MESA_device_select.so
libfreeblpriv3.so
libnssckbi.so
libsoftokn3.so
```

The remaining ten objects are dependencies of these roots.

### Turnip driver root

`libvulkan_freedreno.so` reaches ten mapped-only members including itself:

```text
libvulkan_freedreno.so
libX11-xcb.so.1
libstdc++.so.6
libxcb-dri3.so.0
libxcb-present.so.0
libxcb-randr.so.0
libxcb-sync.so.1
libxcb-xfixes.so.0
libxshmfence.so.1
libzstd.so.1
```

This means the prefix X11/DRI/support tail is not an independent application closure. It is the support closure of the dynamically selected Turnip provider in this receipt.

### Vulkan layer root

`libVkLayer_MESA_device_select.so` reaches:

```text
libVkLayer_MESA_device_select.so
libxcb-dri3.so.0
```

`libxcb-dri3.so.0` is therefore shared by both graphics dynamic roots.

### NSS/security roots

```text
libfreeblpriv3.so
    -> no additional mapped-only dependency

libnssckbi.so
    -> no additional mapped-only dependency

libsoftokn3.so
    -> libsqlite3.so.0
```

These four mapped-only root/support objects form an NSS/security database direction, not part of the Vulkan capability.

## Process-class observation

```text
Turnip driver root:
    zygote

Mesa device-select layer root:
    zygote

Turnip support dependencies:
    mostly zygote

libX11-xcb.so.1:
    main, zygote

NSS/security roots and sqlite support:
    main
```

Process class supports capability attribution but does not by itself prove the exact `dlopen` caller or search path.

## Data capability partition

```text
locale data:
    12
    source: glibc 2.42 prefix

font data:
    4
    source: Debian rootfs packages

GSettings schema data:
    1
    source: rootfs generated aggregate
```

The data set remains outside ELF closure.

`gschemas.compiled` retains:

```text
package:
    UNOWNED

version:
    UNKNOWN
```

Its byte identity is stable, but selected-candidate reproducibility requires an explicit schema compilation/input provenance contract or an explicitly retained rootfs-backed data authority.

## Receipt packaging boundary

The B2 output directory verified the Phase B1 file:

```text
input/semantic-objects.tsv
```

but the B2 tgz did not embed a copy of that nested source file.

Therefore:

```text
B2 graph and partition result:
    VALID

B2 archive alone:
    not fully self-contained for re-deriving data-capabilities.tsv

B1 + B2 archive chain:
    sufficient for complete independent verification
```

The omission does not invalidate the current result because:

```text
the B1 archive is separately retained;
all B2 graph inputs used for ELF partition are embedded;
data-capabilities.tsv is embedded;
the data capability count and rows match the B1 semantic source;
independent recomputation matches every reported partition count.
```

Future B2 receipts should embed the nested semantic source or explicitly declare a two-receipt dependency instead of appearing self-contained.

No runtime rerun is justified for this packaging-only defect.

## Capability directions established

The current evidence supports these bounded directions:

```text
APP_LOCAL payload
WORLD_SUBSTRATE
entrypoint-static external GUI/runtime closure
graphics Vulkan dynamic roots and support closure
NSS/security dynamic roots and support closure
locale data capability
font data capability
GSettings schema capability
```

The large entrypoint-static external set remains heterogeneous and is not accepted as one permanent capability group merely because it is statically reachable.

## Claim boundary

Phase B2 proves:

```text
the captured DT_NEEDED graph is uniquely resolvable;
entrypoint and all-app-local static closures are reproducible;
mapped-only objects are explicit;
non-ELF data capabilities are separate;
five dynamic roots explain the mapped-only set;
capability grouping analysis can proceed without a workload launch.
```

Phase B2 does not prove:

```text
exact dlopen callers;
exact search-path selection for dynamic roots;
that all entrypoint-static providers belong to one reusable object;
that mapped-only roots are optional;
that rootfs-backed data is the final target;
candidate materialization, actual selection, or workload equivalence.
```

## Direction decision

```text
Phase B2:
    CLOSED / PASS

fresh workload capture:
    NOT REQUIRED

candidate materialization:
    STILL BLOCKED

next action:
    DYNAMIC ROOT + STATIC PACKAGE CAPABILITY GROUPING INPUT
```

The next read-only step should emit:

```text
dynamic discovery roots;
root-specific dependency closures;
shared support objects;
entrypoint direct providers;
partition/package summaries;
data capability summaries;
unclassified capability decisions.
```

## Stop line

Do not:

```text
copy all 113 ELF objects into one directory;
treat all 95 entrypoint-static objects as one semantic provider;
treat all 15 mapped-only objects as independent roots;
drop dynamic support dependencies;
merge NSS/security and graphics dynamic closures;
merge locale/font/schema data into ELF closure;
rerun Obsidian or graphics workloads for this read-only decision;
materialize candidate bytes before capability ownership is decided.
```
