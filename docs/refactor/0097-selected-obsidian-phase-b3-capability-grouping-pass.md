# 0097 — Selected Obsidian Phase B3 Capability-Grouping Pass

## Status

The corrected Phase B3 receipt passed.

```text
analysis.status:
    PASS

next state:
    READY_FOR_CAPABILITY_OWNERSHIP_DECISION

failure-stage.txt:
    absent

runtime launch:
    NO

promoted runtime mutation:
    NO
```

The first failed Phase B3 run remains preserved separately in `0096`. This corrected receipt does not reuse or overwrite the failed evidence root.

## Authoritative receipt

Archive:

```text
selected-obsidian-phase-b3-capability-grouping-corrected-20260711-204914.tgz
```

Archive SHA-256:

```text
9700e71be0795a8a2634deb1c369d1aa0d5c0878cbd7b244091318702521ab7c
```

Contained evidence root:

```text
$PREFIX/tmp/selected-obsidian-closure/
    selected-obsidian-phase-b3-capability-grouping-corrected-20260711-204914
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    2fe66ebca11104fa946848ede18df1ef57ad2d58
```

Consumed Phase B2 root:

```text
$PREFIX/tmp/selected-obsidian-closure/
    selected-obsidian-phase-b2-static-runtime-closure-20260711-195310
```

Captured Phase B2 head:

```text
26546a015708765cd8a624a8bb4976a8db191d2a
```

## Archive integrity

The archive contained 27 members under one relative Termux path.

It contained no:

```text
absolute path
parent traversal
symlink
hardlink
device node
special member
```

All eight required Phase B2 inputs were embedded into the B3 output and marked `PASS`:

```text
analysis.status
summary.tsv
resolved-edges.tsv
candidate-elf-partition.tsv
mapped-only-dynamic.tsv
data-capabilities.tsv
input/elf-objects.tsv
input/process-semantic-usage.tsv
```

Unlike the Phase B2 archive packaging boundary, this B3 archive is self-contained for reproducing its own capability-grouping analysis.

## Primary result

```text
mapped-only objects:
    15

dynamic discovery roots:
    5

unclassified dynamic roots:
    0

shared mapped-only support objects:
    1

entrypoint direct providers:
    34

data capability objects:
    17
```

The output includes:

```text
dynamic-root-candidates.tsv
dynamic-root-closure.tsv
dynamic-root-members.tsv
shared-dynamic-support.tsv
suggested-dynamic-family-summary.tsv
entrypoint-direct-providers.tsv
partition-package-summary.tsv
data-capability-summary.tsv
claim-boundary.txt
summary.tsv
next-state.txt
analysis.status
```

## Independent verification

The embedded Phase B2 partition and resolved-edge files were independently re-evaluated.

Verified:

```text
mapped-only objects:
    15

roots with no incoming mapped-only edge:
    5

root identities:
    libvulkan_freedreno.so
    libVkLayer_MESA_device_select.so
    libfreeblpriv3.so
    libnssckbi.so
    libsoftokn3.so

root closure counts:
    libvulkan_freedreno.so             mapped-only 10 / full 21
    libVkLayer_MESA_device_select.so   mapped-only  2 / full 10
    libfreeblpriv3.so                  mapped-only  1 / full  3
    libnssckbi.so                      mapped-only  1 / full  6
    libsoftokn3.so                     mapped-only  2 / full  9

shared mapped-only member:
    libxcb-dri3.so.0.1.0

entrypoint direct providers:
    34

data capability objects:
    17
```

Every reported count matched the receipt.

## Dynamic family result

```text
GRAPHICS_VULKAN
    roots:
        2

    unique mapped-only members:
        11

NSS_SECURITY
    roots:
        3

    unique mapped-only members:
        4
```

No dynamic root remained in `REVIEW`.

These labels are evidence-guided capability directions, not final filesystem or activation objects.

## Graphics dynamic capability

Roots:

```text
libvulkan_freedreno.so
libVkLayer_MESA_device_select.so
```

### Turnip provider root

```text
root:
    libvulkan_freedreno.so

mapped-only closure:
    10

full closure:
    21

observed process class:
    zygote
```

Mapped-only support includes:

```text
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

The remaining full-closure members are already part of the entrypoint-static support set, including world substrate, X11/XCB support, DRM, Expat, and compression support.

### Mesa device-selection layer root

```text
root:
    libVkLayer_MESA_device_select.so

mapped-only closure:
    2

full closure:
    10

observed process class:
    zygote
```

Its only additional mapped-only support object is:

```text
libxcb-dri3.so.0
```

### Shared graphics support

The only mapped-only object shared by multiple dynamic roots is:

```text
libxcb-dri3.so.0.1.0
```

It is shared by the two graphics roots.

There is no mapped-only support object shared between graphics and NSS/security families.

## NSS/security dynamic capability

Roots:

```text
libfreeblpriv3.so
libnssckbi.so
libsoftokn3.so
```

All three roots:

```text
package:
    libnss3:arm64

version:
    2:3.110-1+deb13u2

observed process class:
    main
```

Root-specific closure:

```text
libfreeblpriv3.so
    mapped-only: 1
    full:        3

libnssckbi.so
    mapped-only: 1
    full:        6

libsoftokn3.so
    mapped-only: 2
    full:        9
    dynamic support:
        libsqlite3.so.0
```

Static NSS support already in the entrypoint closure includes:

```text
libnss3.so
libnssutil3.so
libsmime3.so
libnspr4.so
libplc4.so
libplds4.so
```

Therefore the evidence supports one reusable NSS/security capability direction composed from:

```text
libnss3 package members
libnspr4 package members
libsqlite3 support for softokn
world substrate provided separately
```

This is a semantic grouping decision input. Exact materialization format remains open.

## Entrypoint direct-provider boundary

The Obsidian entrypoint has 34 direct provider names:

```text
APP_LOCAL_ELF:
    1

WORLD_SUBSTRATE_ELF:
    5

PROVIDER_PREFIX_ELF:
    6

PROVIDER_ROOTFS_ELF:
    21

PROVIDER_GRAPHICS_GBM_ELF:
    1
```

Direct app-local provider:

```text
libffmpeg.so
```

Direct world providers:

```text
ld-linux-aarch64.so.1
libc.so.6
libdl.so.2
libm.so.6
libpthread.so.0
```

Direct prefix providers:

```text
libgcc_s.so.1
libexpat.so.1
libX11.so.6
libxcb.so.1
libXext.so.6
libXrandr.so.2
```

Direct rootfs/provider roots include GTK, GLib/GIO, ATK/AT-SPI, Cairo/Pango, D-Bus, NSS/NSPR, ALSA, CUPS, udev, X11 extensions, xkbcommon, and GBM.

This set is heterogeneous and must not be converted into one permanent `electron-runtime` directory merely because the entrypoint directly needs it.

## Data capability result

```text
PROVIDER_LOCALE_DATA
    package: glibc
    version: 2.42
    objects: 12

PROVIDER_FONT_DATA
    fonts-dejavu-extra  2.37-8             1
    fonts-dejavu-mono   2.37-8             2
    fonts-noto-cjk      1:20240730+repack1-1 1

PROVIDER_SCHEMA_DATA
    package: UNOWNED
    version: UNKNOWN
    objects: 1
```

The schema aggregate remains the strongest unresolved data-provenance item.

## Ownership decisions now supported

### 1. Graphics is a separate feature capability

The two `GRAPHICS_VULKAN` roots and their support closure belong to the separately closed graphics provider/feature composition.

They are not part of the minimum provider-neutral Obsidian CPU candidate.

```text
base CPU candidate:
    exclude GRAPHICS_VULKAN dynamic roots

GPU candidate/feature extension:
    compose the accepted graphics provider policy separately
```

The retained old control mapping does not override the current accepted CPU policy receipt.

### 2. NSS/security is a required application capability

The three NSS roots were observed in the main process and are distinct from the graphics family.

The first CPU selected candidate must preserve an explicit NSS/security capability containing:

```text
NSS direct/static members
NSPR support
freebl / built-in trust / softokn dynamic modules
SQLite support required by softokn
```

### 3. World substrate remains separate

The glibc loader/libc family is support shared by all root closures and must not be copied into application-provider materialization.

### 4. Data remains separate from ELF

Locale, font, and schema data are independent capability decisions and must not be flattened into an ELF closure.

### 5. Static GUI/runtime grouping remains open

The 95-object entrypoint-static closure and 28 external direct provider roots remain too heterogeneous for one final semantic owner.

The next analysis must decompose direct-root closure overlap and package families before candidate materialization.

## Claim boundary

Phase B3 proves:

```text
the 15 mapped-only objects reduce to five dynamic roots;
root-specific dependency closures are reproducible;
graphics and NSS/security dynamic families are disjoint;
one mapped-only support object is shared by the graphics roots;
the entrypoint direct-provider set is explicit;
package/data distributions are explicit;
capability ownership decisions may proceed without a workload launch.
```

Phase B3 does not prove:

```text
exact dlopen callers or search paths;
that suggested families are final activation units;
that all static GTK/X11/GLib support is one reusable provider;
selected candidate materialization;
candidate-specific actual selection;
control/candidate equivalence.
```

## Direction decision

```text
Phase B3:
    CLOSED / PASS

first failed B3 archive:
    INVALID / PRESERVED

graphics dynamic ownership:
    SEPARATE FEATURE CAPABILITY

NSS/security dynamic ownership:
    REQUIRED APPLICATION CAPABILITY DIRECTION

candidate materialization:
    STILL BLOCKED

next action:
    ENTRYPOINT-STATIC DIRECT-ROOT CLOSURE / OVERLAP MATRIX
```

## Stop line

Do not:

```text
rerun Phase B1, B2, or B3 without a source trigger;
include graphics dynamic roots in the minimum CPU candidate;
drop NSS dynamic roots or sqlite support;
copy world substrate into provider materialization;
treat all 34 direct providers as one capability;
treat all 95 static objects as one provider;
merge data capabilities into ELF closure;
materialize candidate bytes before static provider ownership is decomposed.
```
