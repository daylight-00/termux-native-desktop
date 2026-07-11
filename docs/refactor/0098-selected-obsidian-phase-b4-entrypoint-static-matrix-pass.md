# 0098 — Selected Obsidian Phase B4 Entrypoint-Static Matrix Pass

## Status

Phase B4 passed.

```text
analysis.status:
    PASS

next state:
    READY_FOR_STATIC_CAPABILITY_OWNERSHIP_DECISION

runtime launch:
    NO

promoted runtime mutation:
    NO
```

The result closes the read-only direct-root closure and overlap analysis for the Obsidian entrypoint-static provider set.

It does not authorize candidate materialization by itself.

## Authoritative receipt

Archive:

```text
selected-obsidian-phase-b4-entrypoint-static-capability-matrix-20260711-211933.tgz
```

Archive SHA-256:

```text
3829cf756dc2a6526ca59073d245a1696b60fcaada0116ad386b9c941911258a
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    3fbe8ce5026b02f6de1e4e9e55c16dbf41beb5aa
```

Consumed corrected Phase B3 root:

```text
$PREFIX/tmp/selected-obsidian-closure/
    selected-obsidian-phase-b3-capability-grouping-corrected-20260711-204914
```

Captured Phase B3 head:

```text
2fe66ebca11104fa946848ede18df1ef57ad2d58
```

## Archive integrity

The archive contained 26 members under one relative Termux path.

It contained no:

```text
absolute path
parent traversal
symlink
hardlink
device node
special member
```

All seven required Phase B3 inputs were embedded and marked `PASS`.

The Phase B4 archive is self-contained for reproducing its own matrix analysis.

## Primary result

```text
entrypoint direct providers:
    34

external direct roots:
    28

app-local direct roots:
    1

world direct roots:
    5

prefix direct roots:
    6

rootfs direct roots:
    21

graphics GBM direct roots:
    1

shared external support objects:
    51

direct-root overlap pairs:
    111

external package dependency edges:
    144
```

Every structural count was independently re-evaluated from the embedded partition and resolved-edge files and matched the receipt.

## External static union

The union of all 28 external direct-root closures contains:

```text
external static objects:
    87

PROVIDER_PREFIX_ELF:
    32

PROVIDER_ROOTFS_ELF:
    54

PROVIDER_GRAPHICS_GBM_ELF:
    1
```

These 87 objects are the external portion of the 95-object entrypoint-static closure after removing:

```text
APP_LOCAL_ELF:
    2

WORLD_SUBSTRATE_ELF:
    6
```

This confirms again that world substrate and app-local payload remain outside provider materialization.

## Dominant GTK closure

The `libgtk-3.so.0` direct root has:

```text
external closure objects:
    60

full closure objects:
    63

external packages:
    51
```

Eighteen of the other 27 external direct roots are complete subsets of the GTK external closure.

Those contained roots include:

```text
libexpat.so.1
libX11.so.6
libxcb.so.1
libXext.so.6
libXrandr.so.2
libatk-bridge-2.0.so.0
libatk-1.0.so.0
libatspi.so.0
libcairo.so.2
libdbus-1.so.3
libgio-2.0.so.0
libglib-2.0.so.0
libgobject-2.0.so.0
libpango-1.0.so.0
libXcomposite.so.1
libXdamage.so.1
libXfixes.so.3
libxkbcommon.so.0
```

This does not make the GTK package the semantic owner of every dependency. It proves that a separate copied tree for each of these direct roots would duplicate one already-overlapping GUI closure.

## Residual direct-root directions

The external direct roots not fully contained in the GTK closure are:

```text
libgbm.so.1
libgcc_s.so.1
libasound.so.2
libcups.so.2
libnspr4.so
libnss3.so
libnssutil3.so
libsmime3.so
libudev.so.1
```

Their relation to the GTK external closure is:

```text
libgbm.so.1
    external closure: 3
    shared with GTK:   1
    residual:          2

libgcc_s.so.1
    external closure: 1
    residual:          1

libasound.so.2
    external closure: 1
    residual:          1

libcups.so.2
    external closure: 21
    shared with GTK:    5
    residual:           16

libnspr4.so
    external closure: 1
    residual:          1

libnss3.so
    external closure: 5
    residual:          5

libnssutil3.so
    external closure: 4
    residual:          4

libsmime3.so
    external closure: 6
    residual:          6

libudev.so.1
    external closure: 2
    shared with GTK:   1
    residual:          1
```

## Root-package concentration

Largest direct-root package unions:

```text
libgtk-3-0t64:arm64
    direct roots: 1
    union external objects: 60
    union external packages: 51

libatk-bridge2.0-0t64:arm64
    23 objects / 20 packages

libpango-1.0-0:arm64
    22 objects / 18 packages

libatspi2.0-0t64:arm64
    21 objects / 18 packages

libcups2t64:arm64
    21 objects / 18 packages

libcairo2:arm64
    18 objects / 15 packages

libglib2.0-0t64:arm64
    3 direct roots
    11 union objects / 8 packages

libnss3:arm64
    3 direct roots
    6 union objects / 2 packages
```

The 111 overlap pairs and 51 shared external objects show that package-root closures are heavily overlapping.

Therefore package boundaries are provenance inputs, not one-to-one physical deployment boundaries.

## Static capability ownership decision

The evidence now supports a two-level model.

### Semantic capability manifests

The selected application domain should describe typed capability roots such as:

```text
app.obsidian.local
world.glibc
runtime.compiler-support
electron.gui.gtk3
electron.printing.cups
electron.audio.alsa
electron.device.udev
electron.security.nss
electron.graphics.gbm-base
provider.locale.glibc
provider.fonts
provider.schemas.gsettings
```

The names are semantic directions, not final repository paths.

### One deduplicated application-domain generation

Because the static closures overlap heavily, the physical candidate must not create one copied `lib/` tree per direct root.

The target materialization direction is:

```text
one receipt-owned application-domain generation
    -> one deduplicated selected external ELF object set
    -> typed manifest membership for each semantic capability
    -> app-local payload left in the AppDir
    -> world substrate referenced but not copied
    -> graphics feature roots composed separately
    -> data capabilities stored separately from ELF
```

This is also the correct object model for later atomic activation:

```text
generation preparation
    -> validate manifests and object identities
    -> atomically switch one application-domain activation pointer
```

Atomic activation implementation remains deferred until the data decision and candidate manifest are complete.

## Minimum provider-neutral CPU candidate direction

The minimum CPU candidate should include:

```text
87 selected external entrypoint-static ELF objects
required NSS/security dynamic roots and support from Phase B3
```

It should exclude:

```text
APP_LOCAL ELF copies
WORLD_SUBSTRATE copies
Turnip Vulkan driver root
Mesa Vulkan device-selection layer root
other GPU-feature-only dynamic support
```

`libgbm.so.1` remains in the static set because the Obsidian entrypoint directly requires it even when application GPU feature mode is disabled.

This distinguishes:

```text
static graphics ABI support required to load the executable
    from
selected GPU provider/feature capability
```

## Capability-specific interpretation

### `electron.gui.gtk3`

The GTK root dominates the GUI/toolkit closure and contains the static X11, GLib/GIO, ATK/AT-SPI, Cairo/Pango, D-Bus, and xkbcommon directions observed in the entrypoint graph.

These remain separately typed in provenance/manifests even when physically deduplicated.

### `electron.printing.cups`

CUPS has 16 external objects outside the GTK closure and therefore remains a distinct static capability direction.

### `electron.security.nss`

The four static direct roots plus Phase B3 dynamic NSS modules and SQLite support form one required security capability direction.

### `electron.audio.alsa`

ALSA is a distinct one-root static capability direction.

### `electron.device.udev`

udev is a distinct device-observation capability with one residual object beyond shared support.

### `electron.graphics.gbm-base`

GBM static support is required by the executable and remains separate from GPU-provider selection.

### `runtime.compiler-support`

`libgcc_s.so.1` is prefix-managed reusable runtime support, not application-owned payload.

## Data remains blocking

Static ELF ownership is now sufficiently decomposed to design a candidate manifest.

Candidate materialization remains blocked on explicit ownership and provenance for:

```text
12 glibc locale objects
4 font objects
1 generated gschemas.compiled aggregate
```

The next step is a read-only data-capability provenance audit, especially for the schema source set and package ownership.

## Claim boundary

Phase B4 proves:

```text
all external entrypoint direct-root closures are explicit;
root containment and overlap are reproducible;
87 external static objects form the deduplicated static union;
GTK is the dominant closure root;
CUPS, NSS/NSPR, ALSA, udev, GBM, and compiler support remain residual directions;
package boundaries are too overlapping to be independent copied deployment trees;
static capability ownership can move to typed manifests over one deduplicated generation.
```

Phase B4 does not prove:

```text
selected bytes have been materialized;
loader search paths select a candidate generation;
data capability ownership or schema reproducibility;
dynamic dlopen search paths;
candidate workload equivalence;
final atomic activation implementation.
```

## Direction decision

```text
Phase B4:
    CLOSED / PASS

static provider model:
    TYPED MANIFESTS OVER ONE DEDUPLICATED APPLICATION-DOMAIN GENERATION

candidate ELF manifest design:
    READY

candidate materialization:
    BLOCKED ON DATA CAPABILITY PROVENANCE

next action:
    DATA CAPABILITY IDENTITY / PACKAGE / SCHEMA-SOURCE AUDIT
```

## Stop line

Do not:

```text
make one copied provider tree per direct root;
make one untyped 87-object blob without capability manifests;
copy app-local or world substrate objects into the candidate;
include Vulkan provider dynamic roots in the minimum CPU candidate;
drop static GBM merely because CPU mode disables GPU features;
materialize the candidate before data capability ownership is closed;
implement atomic activation before the generation manifest is complete.
```
