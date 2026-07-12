# 0123 — Selected Obsidian Provider-Authority Corrected N3 Receipt PASS and Source-Comparison Entry

## Status

```text
N3 normalization transaction:
    PASS

first 1,560-row decision surface:
    SUPERSEDED / RETAINED AS AUDIT EVIDENCE

corrected 1,551-row decision surface:
    PASS / ACCEPTED

source recipe and artifact comparison:
    READY

provider-authority intervention:
    ACTIVE

successor manifest/materialization/current activation:
    BLOCKED
```

This record accepts the corrected normalized decision surface. It does not accept any final provider authority.

## Authority

Read under:

```text
docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md
docs/refactor/0117-provider-authority-intervention-adoption-and-execution-order.md
docs/refactor/0118-selected-obsidian-provider-authority-census-schema-and-evidence-plan.md
docs/refactor/0119-selected-obsidian-provider-authority-n2-read-only-evidence-collector.md
docs/refactor/0120-selected-obsidian-provider-authority-n2-device-receipt-review.md
docs/refactor/0121-selected-obsidian-provider-authority-n3-normalization-implementation.md
docs/refactor/0122-selected-obsidian-provider-authority-n3-receipt-review-and-normalization-correction.md
```

The accepted sequence is now:

```text
N2 exhaustive raw evidence
    -> corrected N3 normalized decision surface
    -> source recipe / patch / artifact comparison
    -> provisional provider authority refinement
```

## Reviewed corrected receipt

```text
archive:
    selected-obsidian-provider-authority-n3-normalized-classification-results-20260712-165805.tgz

independent SHA-256:
    4dd86c4af956b447ed1829d6b5d604f43d10a17e5b3dcb3ddff3e9b48c377a9c

captured branch:
    docs/post-graphics-architecture-audit

captured HEAD:
    2d76d5b5253d10c415191b43f1427b64978695fb

archive members:
    24

archive safety:
    PASS
```

Archive review found zero absolute paths, parent traversal members, symlinks, or special archive members.

## Input identity reconstruction

```text
embedded N2/current-schema inputs:
    13

input status failures:
    0

embedded SHA-256 mismatches:
    0
```

The corrected output therefore derives from the accepted N2 evidence and the corrected capability registry without silent input substitution.

## Normalized census identity

```text
raw N2 census rows:
    26,419

raw prefix surface rows:
    27,279

corrected normalized census rows:
    1,551

unique normalized row IDs:
    1,551

duplicate normalized row IDs:
    0

blank required census fields:
    0

accepted final authority decisions:
    0
```

Decision-state accounting:

```text
PROVISIONAL:
    1,032

OPEN:
    507

BLOCKED:
    12
```

These states are pressure and investigation status only. `PROVISIONAL` is not final authority.

## Decision-unit accounting

```text
capability rows:
    26

selected/reference rows:
    161

pixbuf/icon/MIME supplemental rows:
    20

additional prefix ELF rows:
    911

package aggregate rows:
    86

unowned loader-state rows:
    2

non-ELF package-surface aggregate rows:
    345
```

The normalized row-type totals are:

```text
ELF_OBJECT:
    1,031

PACKAGE_SURFACE:
    432

DATA_OBJECT:
    29

CAPABILITY:
    26

MUTABLE_STATE:
    19

CACHE_CLASS:
    6

APP_LOCAL_OBJECT:
    5

GENERATED_DATA:
    2

DEVICE_RELATION:
    1
```

## Raw-prefix coverage proof

The raw prefix contained:

```text
directories:
    1,007

non-directory paths:
    26,272
```

The corrected decision surface accounts for every non-directory path exactly through:

```text
non-ELF aggregate path membership:
    25,300

individual object rows whose path exists in the prefix inventory:
    972

total:
    26,272
```

The 972 individual rows comprise:

```text
ELF paths:
    958

selected/reference non-ELF paths:
    12

unowned loader-state paths:
    2
```

The 1,007 directory rows remain structural raw evidence and are not independent authority decisions.

## Corrected symlink semantics

The raw prefix contains 8,168 symlinks.

Corrected path-aware grouping retains:

```text
actual library/loader-style SYMLINK_ALIAS paths:
    328

symlinks classified by path responsibility instead:
    7,840
```

All 8,168 symlinks remain represented in aggregate accounting. Documentation, shared data, headers, build metadata, configuration, locale data, tools, and start files no longer inherit runtime-provider pressure merely from symlink file type.

Corrected non-ELF path accounting:

```text
DOCUMENTATION:
    13,350

SHARED_DATA:
    6,365

HEADER:
    3,428

OTHER_NON_ELF:
    1,069

SYMLINK_ALIAS:
    328

SCRIPT_OR_LANGUAGE_MODULE:
    200

BUILD_METADATA:
    191

LOCALE_DATA:
    166

EXECUTABLE_TOOL:
    120

STATIC_OR_STARTFILE:
    43

CONFIGURATION:
    40

total:
    25,300
```

## Platform-pressure correction proof

### X11/XCB

The corrected selected/reference rows contain 16 X11/XCB package objects:

```text
active selected objects:
    9
    semantic pressure: PLATFORM_INTEGRATION_PROVIDER
    decision state: PROVISIONAL

closed graphics-feature objects:
    7
    semantic pressure: GENERIC_SHARED_CAPABILITY_PROVIDER
    decision state: BLOCKED
```

All 16 preserve overlapping `platform.x11-xcb.termux` capability pressure. The seven blocked rows do not reopen graphics work.

### libcap versus udev

The corrected surface retains historical udev consumer membership where observed, while the concrete libcap provider pressure is generic shared capability rather than automatic platform integration.

### termux-exec

The corrected surface records:

```text
libtermux-exec.so:
    platform.glibc-adaptation.termux
    PLATFORM_INTEGRATION_PROVIDER

termux-exec-glibc package aggregate:
    platform.glibc-adaptation.termux
    PLATFORM_INTEGRATION_PROVIDER

termux-exec documentation aggregate:
    build.glibc-target
    TOOLCHAIN_ONLY
```

This separates world-entry adaptation from documentation/tooling surface.

## Semantic pressure distribution

```text
UNRESOLVED:
    487

GENERIC_SHARED_CAPABILITY_PROVIDER:
    346

TOOLCHAIN_ONLY:
    317

WORLD_CORE_SUBSTRATE:
    274

PLATFORM_INTEGRATION_PROVIDER:
    53

DATA_CAPABILITY_PROVIDER:
    34

MUTABLE_OR_CACHE:
    26

APPLICATION_LOCAL:
    12

APPLICATION_DOMAIN_SUPPLEMENT:
    1

ORACLE_ONLY:
    1
```

These counts are a prioritization map, not an approved runtime composition.

## Source-comparison priority

The N3 package pressure identifies 26 installed packages with selected/reference paths or retained direct-consumer edges in the accepted Obsidian graph.

Source comparison begins with:

```text
T0 world and platform boundary:
    glibc
    termux-exec-glibc
    libx11-glibc
    libxau-glibc
    libxcb-glibc
    libxdmcp-glibc
    libxext-glibc
    libxrandr-glibc
    libxrender-glibc
    libxshmfence-glibc

T1 selected generic/runtime support:
    brotli-glibc
    e2fsprogs-glibc
    gcc-libs-glibc
    krb5-glibc
    libblkid-glibc
    libbz2-glibc
    libcap-glibc
    libdrm-glibc
    libexpat-glibc
    libffi-glibc
    libgmp-glibc
    libidn2-glibc
    libunistring-glibc
    libwayland-glibc
    pcre2-glibc
    zlib-glibc
    zstd-glibc
```

The other installed packages remain package-context evidence. They are neither approved runtime members nor removal candidates.

## External source repository boundary

The installed package family is supplied by the public source repository:

```text
https://github.com/termux-pacman/glibc-packages.git
```

The repository describes its gpkg binary repository as:

```text
https://service.termux-pacman.dev/gpkg/$arch
```

GitHub connector access is sufficient for bounded file inspection but is inefficient for package-history and recipe-tree correlation. The next evidence stage may therefore consume a user-created local clone as an external immutable input.

The clone must be treated as source evidence, not as project runtime state.

## Next evidence contract

The next collector must record, without installing or upgrading packages:

```text
corrected N3 receipt identity;
local glibc-packages clone remote, HEAD, refs, and clean state;
installed apt/dpkg package identities;
configured package repository sources;
locally available apt Release/Packages metadata;
exact repository filename, size, and SHA-256 where indexed;
recipe directory and matching historical recipe commit;
recipe build.sh and subpackage identities;
source URL and declared source SHA-256;
patch and auxiliary-file inventory;
current-recipe versus installed-version relationship;
unresolved exact binary artifact acquisition needs.
```

Package acquisition, if later required, must be a separate bounded download transaction into an isolated evidence root. It must not invoke installation or package maintainer scripts.

## Claim boundary

The corrected N3 receipt proves:

```text
the accepted N2 evidence was normalized without identity loss;
the corrected decision surface has complete required fields and unique identities;
all raw prefix non-directory paths remain represented;
symlink path semantics are corrected;
selected X11/XCB platform pressure is preserved;
consumer capability is separated from concrete provider authority pressure;
termux-exec is separated as glibc/world-entry adaptation;
no final provider decision was accepted;
no package, runtime, generation, or current operation was performed.
```

It does not prove:

```text
that current termux-pacman recipes match the installed binary artifacts;
which historical recipe commit built each installed package;
which patches are semantically required by Android/Termux;
that an installed package belongs in the minimum runtime profile;
that Debian or upstream generic artifacts are interchangeable;
locked source or binary supply identities;
update compatibility;
successor composition or activation.
```

## Direction decision

```text
corrected N3 decision surface:
    ACCEPTED

next state:
    READY_FOR_N3_SOURCE_RECIPE_AND_ARTIFACT_COMPARISON

provider-authority intervention:
    ACTIVE

successor work:
    BLOCKED
```

## Stop line

Do not:

```text
use the superseded 1,560-row surface for decisions;
treat PROVISIONAL as final authority;
classify package presence as runtime necessity;
assume current source-repository HEAD built the installed package;
assume recipe package boundaries equal semantic authority boundaries;
run apt/dpkg install, upgrade, remove, or maintainer scripts;
mutate ld.so.conf, ld.so.cache, the immutable generation, or current;
materialize a successor;
reopen closed graphics work.
```
