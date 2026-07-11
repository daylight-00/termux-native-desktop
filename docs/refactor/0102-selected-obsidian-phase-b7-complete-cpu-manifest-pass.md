# 0102 — Selected Obsidian Phase B7 Complete CPU Manifest Pass

## Status

Phase B7 passed.

```text
analysis.status:
    PASS

next state:
    READY_FOR_CANDIDATE_MATERIALIZATION_DESIGN

runtime launch:
    NO

promoted runtime mutation:
    NO
```

The result closes semantic accounting for the retained selected-Obsidian control set before any candidate bytes are materialized.

## Authoritative receipt

Archive:

```text
selected-obsidian-phase-b7-complete-cpu-candidate-manifest-20260711-225234.tgz
```

Archive SHA-256:

```text
6afcbf799f1c73bbc1a058176f30eada84502d29e5507c9ed6b1c7bdb9d495b8
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    ef8eaaaf7af467a7732bb7a00383585cb43d654d
```

The archive contained 41 safe members under one relative Termux path.

```text
regular files:
    39

directories:
    2

absolute paths:
    0

parent traversal:
    0

symlinks/hardlinks/devices/special members:
    0
```

All 19 required receipt inputs were embedded and marked `PASS`.

## Primary result

```text
semantic objects:
    161

semantic disposition coverage:
    161

ELF objects:
    113

external static ELF materialize:
    87

required NSS dynamic ELF materialize:
    4

total ELF materialize:
    91

graphics feature dynamic ELF excluded:
    11

app-local ELF reference:
    5

world ELF reference:
    6

app-local data reference:
    6

world locale reference:
    12

selected fonts materialize:
    4

GSettings aggregate generate:
    1

schema source files:
    37

mutable state objects:
    19

fontconfig cache objects:
    4

Mesa cache objects:
    1

GPU device objects:
    1

selected ELF lookup collisions:
    0

unclassified objects:
    0
```

Every summary value matched independent reconstruction from the embedded B1, corrected B3, B4, B5, and corrected B6 evidence.

## Semantic coverage

`semantic-object-disposition.tsv` contains exactly one row for each of the 161 retained semantic paths.

Verified:

```text
unique disposition paths:
    161

unique B1 semantic paths:
    161

path-set equality:
    YES

semantic class/path class/package/version/SHA-256 equality:
    YES
```

Primary action counts:

```text
MATERIALIZE_SELECTED_STATIC_ELF          87
MATERIALIZE_REQUIRED_DYNAMIC_ELF          4
EXCLUDE_CPU_BASE_GRAPHICS_FEATURE        11
REFERENCE_APP_LOCAL                      11
REFERENCE_WORLD_SUBSTRATE                 6
REFERENCE_WORLD_LOCALE                   12
MATERIALIZE_SELECTED_FONT                 4
GENERATE_GSETTINGS_SCHEMA                 1
ISOLATED_MUTABLE_STATE                   19
REGENERATE_RUNTIME_CACHE                  5
REFERENCE_OPTIONAL_GPU_DEVICE             1
```

The non-ELF disposition total is 48, and `113 + 48 = 161`.

## ELF accounting

The 113 retained ELF objects partition exactly into:

```text
selected external static:
    87

required NSS/security dynamic:
    4

excluded Vulkan feature dynamic:
    11

app-local reference:
    5

world substrate reference:
    6
```

```text
87 + 4 + 11 + 5 + 6 = 113
```

The three derived external sets are disjoint:

```text
static ∩ NSS dynamic:
    empty

static ∩ graphics dynamic:
    empty

NSS dynamic ∩ graphics dynamic:
    empty
```

## Required dynamic CPU objects

The four materialized mapped-only NSS/security objects are:

```text
libfreeblpriv3.so
libnssckbi.so
libsoftokn3.so
libsqlite3.so.0.8.6
```

They are distinct from NSS/NSPR objects already present in the static set.

## Excluded graphics feature objects

The eleven dynamic objects excluded from the minimum CPU base are:

```text
libvulkan_freedreno.so
libVkLayer_MESA_device_select.so
libX11-xcb.so.1.0.0
libstdc++.so.6.0.34
libxcb-dri3.so.0.1.0
libxcb-present.so.0.0.0
libxcb-randr.so.0.1.0
libxcb-sync.so.1.0.0
libxcb-xfixes.so.0.0.0
libxshmfence.so.1.0.0
libzstd.so.1.5.7
```

These remain available only through the separately accepted graphics feature/provider composition.

Static `libgbm.so.1` remains in the selected static set because it is an entrypoint load requirement, not a selected Vulkan provider root.

## Candidate ELF manifest

`candidate-elf-manifest.tsv` contains:

```text
rows:
    91

unique source paths:
    91

STATIC rows:
    87

DYNAMIC_NSS rows:
    4
```

Every row matches the B1 SHA-256 and B3 lookup-name/SONAME metadata for the same source path.

```text
selected lookup-name collisions:
    0
```

The materialized ELF set spans 71 package provenance labels. Package boundaries remain provenance metadata rather than copied physical-tree boundaries.

## Data manifest

`candidate-data-manifest.tsv` contains exactly the 17 B5 retained external data objects.

```text
REFERENCE_WORLD_LOCALE:
    12

MATERIALIZE_SELECTED_FONT:
    4

GENERATE_GSETTINGS_SCHEMA:
    1
```

Every path and captured hash matches the B5 identity-verification receipt.

## GSettings build contract

```text
source files:
    37

compiler:
    $PREFIX/bin/glib-compile-schemas

compiler package/version:
    glib 2.88.2

compiler SHA-256:
    5f8cfe28f5eed9e5b9400260ec0127cae5c3f881437915df3fcdca33cbe5d165

accepted modes:
    default,strict

byte-identical attempts:
    2

expected aggregate SHA-256:
    457f7461585b4caf6e11de65f707077bcb2208f9916c0c588080262f43ecb938
```

The emitted schema-source manifest exactly matches the corrected Phase B6 source manifest.

## Capability membership

The manifest contains 268 evidence-root membership rows over 102 external ELF objects.

Typed capability directions are:

```text
electron.gui.gtk3
electron.printing.cups
electron.security.nss
electron.graphics.gbm-base
electron.device.udev
electron.audio.alsa
runtime.compiler-support
graphics.vulkan.feature
```

Typed capability membership may overlap while each semantic object retains exactly one primary lifecycle disposition.

Six external static objects have membership in more than one semantic capability. This is expected and is the reason the physical generation must remain deduplicated.

## Materialized content boundary

Before schema generation, the selected copied-byte inputs are:

```text
ELF source objects:
    91

font source objects:
    4

copied source objects total:
    95
```

All 95 source hashes are unique in this receipt.

After generation of the schema aggregate, the immutable generation will contain 96 content identities unless later design deliberately shares an existing identical content-addressed object.

## Lifecycle boundary

### Immutable generation content

```text
91 selected ELF objects
4 selected font files
1 generated GSettings aggregate
typed manifests
provenance/build receipts
```

### Referenced but not copied

```text
AppDir ELF/data
protected world glibc ELF
protected world locale data
optional GPU device node
```

### Excluded/recreated

```text
11 Vulkan feature dynamic objects from CPU base
19 mutable application-state paths
4 fontconfig cache paths
1 Mesa cache path
```

## Architecture consequence

Semantic ownership and complete candidate inputs are now explicit.

The next step must define physical materialization and activation without changing the promoted runtime.

Required design topics:

```text
content-addressed object identity;
generation-local ELF alias namespace;
font and schema target paths;
source-byte preflight;
generation identifier derivation;
staging and final generation directories;
validation before activation;
atomic current-pointer replacement;
rollback pointer semantics;
launcher selection boundary;
garbage-collection safety.
```

## Claim boundary

Phase B7 proves:

```text
all 161 retained semantic objects have one primary lifecycle disposition;
all 113 ELF objects are completely and disjointly accounted;
the selected ELF set has 91 objects and no lookup-name collision;
the external data set has complete ownership/build contracts;
typed capability membership can be represented over one deduplicated physical set;
materialization design may proceed without a workload launch.
```

Phase B7 does not prove:

```text
source bytes still match at the instant of future materialization;
a physical object-store or alias layout is safe;
all source basename/SONAME/lookup aliases are collision-free as one filesystem namespace;
a generation has been staged;
loader selection or application behavior;
atomic activation or rollback.
```

## Direction decision

```text
Phase B7:
    CLOSED / PASS

semantic ownership:
    CLOSED FOR MATERIALIZATION DESIGN

complete CPU candidate manifest:
    CLOSED

candidate bytes:
    NOT MATERIALIZED

next action:
    READ-ONLY MATERIALIZATION / ALIAS / ATOMIC-ACTIVATION DESIGN PREFLIGHT
```

## Stop line

Do not:

```text
rerun Phase B1-B7 without a source trigger;
copy selected bytes directly into a live farm;
activate a partial multi-file candidate;
use source basenames or SONAME aliases without collision analysis;
replace the promoted launcher before explicit-generation validation;
copy app-local/world objects into the generation;
include the excluded Vulkan feature set in the minimum CPU base;
implement garbage collection before generation references and rollback are defined.
```
