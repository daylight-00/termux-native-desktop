# Selected Obsidian AppDir Closure Pilot

## Status

```text
PHASE_B1_B8_CLOSED
PHASE_B9_PASS
PASSIVE_B10_STARTUP_PASS
PASSIVE_B10_100_SECOND_SURVIVAL_PASS
PASSIVE_B10_MAPS_CAPTURE_PASS
PASSIVE_MAP_SELECTION_DIAGNOSTIC_PASS
CPU_MAP_CONTRACT_DECIDED
INTERACTIVE_VAULT_OPEN_CAPABILITY_OPEN
CONTROLLED_PIXBUF_DIAGNOSTIC_NEXT
```

The current immutable generation remains published but unactivated.

## Passive map-selection diagnostic

Authoritative receipt:

```text
selected-obsidian-passive-map-selection-diagnostic-20260712-022611
```

```text
archive SHA-256:
    78c6cf04963ce02f25924b900d9122bc22abcb22d2c38e0b7ca4b583d68d8bbb

captured head:
    7147e42bd204b85080e645498637ca2e8415d852

analysis.status:
    PASS

next-state:
    READY_FOR_CPU_MAP_CONTRACT_REDESIGN
```

Input and identity result:

```text
required inputs:
    20 / 20 PASS

selected content objects:
    96 / 96 hash MATCH

mapped source substitutes:
    2 / 2 hash MATCH
```

Passive runtime facts retained:

```text
topology:
    PASS

100-second survival:
    PASS

maps capture:
    PASS

main / renderer / zygote / GPU:
    1 / 1 / 3 / 0

unique mapped regular objects:
    143
```

## Selected map states

```text
MAPPED_SELECTED_OBJECT:
    93

MAPPED_SOURCE_SUBSTITUTE:
    2

NOT_MAPPED:
    1
```

By content kind:

```text
selected ELF:
    89 selected-object mappings
    2 exact source substitutes

selected fonts:
    3 mapped
    1 not demanded

selected schema:
    1 mapped
```

## Xau/Xdmcp decision

Substituted paths:

```text
$PREFIX/glibc/lib/libXau.so.6.0.0
$PREFIX/glibc/lib/libXdmcp.so.6.0.0
```

Both mapped sources are byte-identical to their selected content objects.

Four selected consumers retain:

```text
DT_RPATH=$PREFIX/glibc/lib
```

```text
libXrandr.so.2.2.0
libXrender.so.1.3.0
libxcb-render.so.0.0.0
libxcb-shm.so.0.0.0
```

Six retained direct edges connect the RPATH consumers to Xau/Xdmcp.

Decision:

```text
Xau/Xdmcp next-generation ownership:
    PROTECTED_WORLD_SUBSTRATE

RPATH patch:
    NO

existing generation mutation:
    NO

next-generation duplicate materialization:
    REMOVE
```

The decision follows minimum manipulation: actual loader selection and bytes are already correct; forcing a different path would require transformed ELF identities and a larger validation surface.

## Data map rule

`DejaVuSansMono-Bold.ttf` was present and hash-correct but not used by the passive initial window.

Correct rule:

```text
selected data presence/hash:
    REQUIRED

selected data mapping in every scenario:
    OPTIONAL / DEMAND-LOADED

if mapped:
    selected identity required
```

## CPU graphics map correction

Observed exceptions:

```text
$PREFIX/glibc/lib/libX11-xcb.so.1.0.0
    new class: PROTECTED_WORLD_CPU_X11_BRIDGE

$HOME/gl/apps/obsidian/libvk_swiftshader.so
    new class: APP_LOCAL_CPU_AUXILIARY_ALLOWED
```

Exact CPU process policy still passed:

```text
main --disable-gpu:
    exact

renderer --disable-gpu-compositing:
    present

GPU process:
    0
```

A graphics-related mapping is not equivalent to active GPU execution.

Clean negative boundaries:

```text
broad farm:
    0

rootfs provider:
    0

current:
    0
```

## Corrected map classes

```text
REQUIRED_SELECTED_ELF
REQUIRED_PROTECTED_WORLD
REQUIRED_APP_LOCAL
ALLOWED_APP_LOCAL_AUXILIARY
DEMAND_LOADED_SELECTED_DATA
RECEIPT_MUTABLE_STATE
FORBIDDEN_PROVIDER_MAPPING
```

The universal exact-125-mapped-object rule is retired.

## Next-generation baseline

Before adding the unresolved interactive GTK capability:

```text
old selected content:
    96

remove Xau/Xdmcp duplicates:
    2

corrected baseline:
    94

selected ELF:
    89

selected fonts:
    4

selected schema:
    1
```

Do not materialize this baseline yet. It must be combined with the minimum pixbuf/icon/MIME delta in one new-generation preflight.

## Open interactive capability

The prior vault-open interaction failed in GTK icon/pixbuf handling.

Read-only inventory found:

```text
rootfs loaders.cache:
    1

loader modules:
    12

icon-theme indexes:
    2

MIME database files:
    5

paths absent from B9 semantic manifest:
    20
```

The rootfs cache contains unusable native `/usr/...` references and cannot be selected unchanged.

## Next action

```text
CONTROLLED PIXBUF VAULT-OPEN DIAGNOSTIC
```

The diagnostic must:

```text
use the same explicit immutable generation;
use short receipt-owned runtime paths;
create a receipt-local relocated loader cache;
point only the diagnostic Obsidian exec at that cache;
allow exact rootfs loader-module paths as diagnostic-only;
instruct the operator to click Open vault once after topology stabilizes;
record whether the file chooser appears and whether the process survives;
record all rootfs module mappings and hashes;
leave current absent;
perform no generation mutation.
```

If the relocated cache alone does not fix the interaction, icon-theme data must be added as a separate discriminator rather than bundled wholesale.

## Stop line

Do not:

```text
patch RPATH;
mutate the existing generation;
materialize Xau/Xdmcp in the next generation;
require all selected data to map;
use the rootfs loaders.cache unchanged;
copy all icon/MIME data wholesale;
create current;
create a new generation before the interactive capability closes;
claim practical usability from passive PASS alone.
```
