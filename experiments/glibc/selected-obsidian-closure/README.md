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
CLEAN_STATE_SUPPLY_INVENTORY_NEXT
INTERACTIVE_VAULT_OPEN_CAPABILITY_OPEN
CONTROLLED_PIXBUF_DIAGNOSTIC_AFTER_SUPPLY_INVENTORY
```

The current immutable generation remains published but unactivated.

Canonical clean-state audit:

```text
docs/refactor/0113-clean-state-minimum-condition-and-supply-authority-audit.md
```

## Parent question

Can a real Electron AppDir consume selected external provider/data capabilities while preserving:

```text
valid AppDir/$ORIGIN locality
protected world references
selected immutable provider bytes
application-owned state
passive and interactive workload behavior
clean-state reproducibility
```

The last condition is now explicit. Runtime independence from the rootfs is insufficient when generation construction still depends on undeclared installed rootfs source paths.

## Accepted cumulative results

### Semantic and supply-input analysis

```text
semantic objects:
    161

ELF objects:
    113

entrypoint static closure:
    95

all-app-local static closure:
    98

mapped-only dynamic/discovery objects:
    15

non-ELF data objects:
    17

APP_LOCAL/external lookup collisions:
    0

unresolved/ambiguous captured DT_NEEDED edges:
    0 / 0
```

### Selected CPU manifest and generation

```text
selected ELF:
    91 in the first generation

selected fonts:
    4

generated GSettings aggregate:
    1

content objects:
    96

aliases:
    175

materialized bytes:
    70,897,301

structural validation:
    1851 / 1851 PASS

current:
    ABSENT
```

The generation is immutable evidence. It is not the final clean-state generation.

### Passive explicit-generation runtime

```text
startup/topology:
    PASS

100-second survival:
    PASS

maps capture:
    PASS

main / renderer / zygote / GPU:
    1 / 1 / 3 / 0

broad-farm mappings:
    0

rootfs-provider mappings:
    0

current mappings:
    0
```

## Map-contract decision

### Xau/Xdmcp

Observed world paths:

```text
$PREFIX/glibc/lib/libXau.so.6.0.0
$PREFIX/glibc/lib/libXdmcp.so.6.0.0
```

They are byte-identical to the duplicate selected objects and selected through exact retained absolute RPATH edges.

Accepted operational decision:

```text
RPATH patch:
    NO

existing generation mutation:
    NO

next-generation duplicate materialization:
    REMOVE

world reference:
    REQUIRED BY EXACT HASH/EDGE CONTRACT
```

Semantic owner name remains provisional. The successor manifest should prefer:

```text
PROTECTED_WORLD_X11_SUPPORT
```

or another world-prefix-provider name rather than inferring glibc substrate ownership from physical location.

### Demand-loaded selected data

`DejaVuSansMono-Bold.ttf` remained present and hash-correct but was not mapped by the passive initial window.

```text
selected data presence/hash:
    REQUIRED

mapping in every scenario:
    NOT REQUIRED

if mapped:
    selected identity required
```

### CPU graphics-adjacent mappings

```text
libX11-xcb.so.1.0.0
    required protected world CPU/X11 support

app-local libvk_swiftshader.so
    allowed auxiliary mapping
    not GPU-enable evidence
```

The CPU process contract remained exact `--disable-gpu`, renderer `--disable-gpu-compositing`, and zero GPU process.

## Provisional successor baseline

Before resolving the open GTK capability:

```text
first-generation content:
    96

remove duplicate Xau/Xdmcp selected objects:
    -2

provisional baseline:
    94

selected ELF:
    89

selected fonts:
    4

selected schema:
    1
```

This baseline must not be materialized yet.

The four-font set is an observed, provenance-backed provider set. It is not yet proven as the minimum clean-state contract for Latin UI, monospace/code, bold, Korean/CJK, math, and fallback requirements.

## Clean-state supply gap

The first generation runs without broad-farm/rootfs mappings, but its source preflight and materializer depend on the currently installed source tree.

```text
selected rootfs ELF paths
selected rootfs font paths
rootfs schema source paths
native schema compiler path
```

are rehashed as live absolute source paths.

Therefore:

```text
existing generation after source deletion:
    remains byte-complete

successor materialization after source deletion:
    can fail before exact package artifacts or retained source objects exist

fresh Termux reconstruction from repository alone:
    not yet proven
```

The Debian rootfs is currently an evidence/supply oracle, not a declared clean-state package specification.

## Immediate next stage — clean-state rootfs supply inventory

Before a package purge or the controlled pixbuf launch, capture read-only:

```text
full dpkg package/version/status state
apt manual and automatic marks
apt and dpkg histories
relevant package policies/origins
installed reverse dependencies
font/config/cache filesystem inventory
selected font/schema/pixbuf source ownership and identities
```

This stage performs no install, removal, generation mutation, or application launch.

It must answer:

```text
which packages were added beyond the intended minimal baseline;
which font packages were deliberate/manual versus dependencies;
which exact artifacts must be retained for clean reconstruction;
which current runtime paths still depend on the expanded rootfs.
```

## Open interactive capability

The vault-open path currently fails in GTK icon/pixbuf handling.

Inventory found:

```text
one generated rootfs loaders.cache
12 loader modules
2 icon-theme indexes
5 MIME database files
20 paths absent from the first-generation manifest
```

The rootfs cache contains invalid native `/usr/...` references and cannot be used unchanged.

After the supply inventory, the next runtime discriminator may:

```text
use the same explicit immutable generation;
use short receipt-owned runtime paths;
generate one receipt-local relocated pixbuf loader cache;
reference exact existing rootfs modules as diagnostic-only inputs;
perform one declared Open-vault interaction;
record the file chooser result, survival, file opens/maps, and hashes;
leave current absent;
perform no package install or generation mutation.
```

A pass with all twelve modules proves only that the coarse loader capability helps. It does not authorize all modules, icon files, or MIME files in the final generation.

## Minimum-capability derivation after diagnosis

The successor design must determine:

```text
which pixbuf modules were actually used;
whether a relocated generated cache is required;
whether embedded PNG support is independent;
which icon-theme data is required;
which MIME database products are required;
which generated data can be reproduced from locked sources/tools;
the minimum required font coverage and exact files.
```

## Identity correction before activation

The current generation digest mixes:

```text
content identities
absolute source paths
package provenance
repository head
compiler path
absolute generation base
```

while not completely identifying:

```text
application payload
protected world objects
launcher/policy
validation scenarios
```

Before activation, split:

```text
content generation identity
supply/provenance identity
runtime composition identity
installation/activation identity
validation-policy identity
```

Do not rename or rewrite the existing B9 generation. Apply the correction to the unified successor.

## Font-package cleanup boundary

Do not remove the rootfs font packages yet.

Reasons:

```text
package/manual history is not captured;
exact package artifacts are not retained as locked supply objects;
the successor materializer still depends on live source paths;
the current promoted compatibility runtime may still use rootfs font/data policy;
the pixbuf/source diagnostic remains open.
```

Preferred cleanup sequence:

```text
supply inventory
    -> retain exact artifacts/source objects
    -> controlled pixbuf diagnosis
    -> minimum font/GTK capability
    -> unified successor generation
    -> passive + interactive + warehouse-independence acceptance
    -> clean reconstruction proof
    -> purge or recreate rootfs
    -> repeat acceptance
```

## Stop line

Do not:

```text
purge rootfs font packages before supply inventory;
install packages for the pixbuf test;
patch RPATH;
mutate or delete the existing generation;
materialize Xau/Xdmcp again;
call Xau/Xdmcp substrate solely because prefix paths were selected;
require every selected data object to map;
copy all pixbuf/icon/MIME inventory paths;
retain or remove fonts solely from one map observation;
use the rootfs loaders.cache unchanged;
add broad-farm/rootfs paths to an acceptance run;
create current;
create the successor generation before the interactive and supply deltas close;
claim clean reproducibility from the current installed rootfs;
carry phase-specific experiment wrappers into final deployed tooling;
reset Termux before locked inputs and bootstrap contracts are preserved.
```
