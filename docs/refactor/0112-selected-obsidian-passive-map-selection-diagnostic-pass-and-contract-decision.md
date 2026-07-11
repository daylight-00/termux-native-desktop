# 0112 — Selected Obsidian Passive Map-Selection Diagnostic Pass and Contract Decision

## Status

The read-only passive map-selection diagnostic passed.

```text
analysis.status:
    PASS

next-state:
    READY_FOR_CPU_MAP_CONTRACT_REDESIGN

runtime launch:
    NO

generation mutation:
    NO

promoted runtime mutation:
    NO
```

The diagnostic closes the cause of the passive B10 mapped-identity failure. It also supports a minimum-manipulation CPU map-contract decision.

## Authoritative receipt

Archive:

```text
selected-obsidian-passive-map-selection-diagnostic-20260712-022611.tgz
```

Archive SHA-256:

```text
78c6cf04963ce02f25924b900d9122bc22abcb22d2c38e0b7ca4b583d68d8bbb
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    7147e42bd204b85080e645498637ca2e8415d852
```

Archive structure:

```text
members:
    12

regular files:
    11

directories:
    1

absolute paths:
    0

parent traversal:
    0

symlink/hardlink/device/special members:
    0
```

## Input and identity gates

```text
required inputs:
    20

input PASS:
    20

selected content objects rehashed:
    96 / 96 MATCH

mapped source substitutes rehashed:
    2 / 2 MATCH

CPU-map exception identities:
    2 captured
```

The selected content store and immutable generation remain byte-correct.

## Passive runtime facts retained

```text
topology:
    PASS

100-second survival:
    PASS

maps capture:
    PASS

main:
    1

renderer:
    1

zygote:
    3

GPU process:
    0

unique mapped regular objects:
    143
```

## Selected map state

```text
selected objects total:
    96

mapped selected objects:
    93

mapped source substitutes:
    2

not mapped:
    1
```

By content kind:

```text
COPIED_ELF:
    89 selected objects mapped
    2 source substitutes mapped

COPIED_FONT:
    3 selected objects mapped
    1 not demanded

GENERATED_GSETTINGS:
    1 selected object mapped
```

## Source substitutions

The two selected ELF objects not mapped from the content store were:

```text
libXdmcp.so.6.0.0
    SHA-256 0245743bb594ee1ac2c1325873d70407c790f890477d8a0fe8323bda8803f705

libXau.so.6.0.0
    SHA-256 1a8bc733979360f2e3327d805efe64f9306247bacb90cac9efdc0cf1e033bb89
```

The mapped paths were:

```text
$PREFIX/glibc/lib/libXdmcp.so.6.0.0
$PREFIX/glibc/lib/libXau.so.6.0.0
```

Both mapped world-source files matched the selected object SHA-256 exactly.

Therefore this is an ownership/path-selection mismatch, not a byte-identity or ABI mismatch.

## Absolute RPATH proof

Four selected copied consumers retain:

```text
DT_RPATH=$PREFIX/glibc/lib
DT_RUNPATH absent
```

Consumers:

```text
libXrandr.so.2.2.0
libXrender.so.1.3.0
libxcb-render.so.0.0.0
libxcb-shm.so.0.0.0
```

All four selected copies were themselves mapped from the content store.

Retained direct edges from the RPATH consumers to the substituted providers:

```text
libXrandr -> libXau
libXrandr -> libXdmcp
libxcb-render -> libXau
libxcb-render -> libXdmcp
libxcb-shm -> libXau
libxcb-shm -> libXdmcp
```

```text
edge count:
    6
```

This closes the leading explanation for the substitutions: selected consumers use their inherited absolute RPATH for these nested dependencies.

## Demand-loaded font

The only content object neither selected nor source-mapped was:

```text
DejaVuSansMono-Bold.ttf
```

The object remains present and hash-correct. The passive initial window did not demand it.

The invariant is corrected:

```text
selected data presence and hash:
    REQUIRED

selected data mapping in every scenario:
    NOT REQUIRED

if selected data is mapped:
    it must resolve to the selected object identity
```

## CPU map exceptions

Exactly two semantic exceptions were observed:

```text
EXCLUDED_SEMANTIC_MAPPING
    $PREFIX/glibc/lib/libX11-xcb.so.1.0.0

UNMODELLED_APP_LOCAL
    $HOME/gl/apps/obsidian/libvk_swiftshader.so
```

Identity result:

```text
libX11-xcb:
    retained semantic hash MATCH

libvk_swiftshader:
    unmodelled live identity captured
```

The passive CPU process contract remained:

```text
exact --disable-gpu
renderer --disable-gpu-compositing
GPU process count 0
```

Therefore a graphics-related object mapping is not equivalent to an active GPU process or enabled GPU rendering path.

## Clean negative boundaries

```text
broad-farm mappings:
    0

rootfs-provider mappings:
    0

current-path mappings:
    0
```

## CPU map-contract decision

### `libXau` and `libXdmcp`

Decision:

```text
next-generation ownership:
    PROTECTED_WORLD_SUBSTRATE

selected materialization:
    REMOVE IN THE NEXT GENERATION

existing immutable generation:
    DO NOT MUTATE

RPATH transformation:
    DO NOT APPLY
```

Rationale:

```text
the loader demonstrably selects the protected world paths;
the selected and world bytes are identical;
forcing path-local selection requires ELF transformation;
transformation would create new content identities and a larger validation surface;
world reference is already an accepted architecture class;
minimum manipulation favors explicit reclassification over RPATH patching.
```

This decision does not endorse arbitrary world leakage. It recognizes only the two exact hash-matched providers reached through the six retained RPATH edges.

### `libX11-xcb`

Decision:

```text
old class:
    EXCLUDE_CPU_BASE_GRAPHICS_FEATURE

new class:
    PROTECTED_WORLD_CPU_X11_BRIDGE
```

It is part of the passive CPU/X11 runtime substrate, even though it is graphics-adjacent.

### `libvk_swiftshader`

Decision:

```text
ownership:
    APP_LOCAL

CPU map policy:
    ALLOWED AUXILIARY MAPPING

GPU process implication:
    NONE
```

It must enter the semantic manifest with an exact hash, but it should not be copied into the selected generation.

### Selected data

Decision:

```text
presence/hash:
    REQUIRED

mapping:
    SCENARIO-DEPENDENT

passive acceptance:
    validate mapped selected data identities, not universal data-map completeness
```

## Corrected passive map classes

```text
REQUIRED_SELECTED_ELF
    selected ELF that must map from content-store identities

REQUIRED_PROTECTED_WORLD
    protected world substrate, including exact RPATH-bound providers and CPU X11 bridge

REQUIRED_APP_LOCAL
    retained AppDir identities

ALLOWED_APP_LOCAL_AUXILIARY
    app-local auxiliary objects such as SwiftShader under CPU process policy

DEMAND_LOADED_SELECTED_DATA
    generation-owned data whose presence/hash is invariant but mapping is scenario-dependent

RECEIPT_MUTABLE_STATE
    receipt-owned runtime files

FORBIDDEN_PROVIDER_MAPPING
    rootfs, broad farm, current, and remaining excluded providers
```

The old exact `125 mapped identities` rule is retired. Acceptance becomes class/set based rather than one universal object count.

## Next generation effect

Before adding the still-open GTK pixbuf/icon/MIME capability, the corrected baseline would remove two duplicate selected ELF identities:

```text
old selected content objects:
    96

remove world-reclassified ELF:
    2

corrected baseline selected content objects:
    94

corrected baseline selected ELF:
    89

selected fonts:
    4

selected generated schema:
    1
```

A new generation must not be created yet. The interactive vault-open capability still needs its minimum data/plugin set identified, and both deltas should enter one unified generation preflight.

## Direction decision

```text
map-selection diagnostic:
    CLOSED / PASS

RPATH cause:
    CLOSED

Xau/Xdmcp ownership:
    PROTECTED WORLD

RPATH patching:
    REJECTED

all-data-must-map invariant:
    REJECTED

CPU graphics-map classification:
    CORRECTED IN DESIGN

existing generation mutation:
    FORBIDDEN

next action:
    CONTROLLED PIXBUF VAULT-OPEN DIAGNOSTIC
```

## Claim boundary

This receipt and decision prove:

```text
the passive runtime is viable for 100 seconds;
the two source substitutions are byte-identical and explained by exact RPATH edges;
the missing font is demand-unmapped rather than absent;
libX11-xcb and app-local SwiftShader require explicit CPU map classes;
no broad-farm, rootfs, or current leakage occurred.
```

They do not prove:

```text
the vault-open path is fixed;
the minimum pixbuf/icon/MIME capability;
a corrected new generation;
interactive usability;
activation or rollback readiness.
```

## Stop line

Do not:

```text
patch RPATH in the current generation;
mutate or delete the current immutable generation;
materialize Xau/Xdmcp again in the next generation;
require every selected data object to map;
forbid SwiftShader solely because its name is graphics-related;
activate current;
create a new generation before the interactive capability delta is closed.
```
