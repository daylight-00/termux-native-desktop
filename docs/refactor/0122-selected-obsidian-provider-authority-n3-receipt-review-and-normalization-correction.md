# 0122 — Selected Obsidian Provider-Authority N3 Receipt Review and Normalization Correction

## Status

```text
N3 device normalization transaction:
    PASS

first normalized decision surface:
    REVIEWED / CORRECTION REQUIRED

corrected normalizer:
    READY_FOR_DEVICE EXECUTION

provider-source comparison:
    BLOCKED UNTIL CORRECTED RECEIPT

provider-authority intervention:
    ACTIVE

successor manifest/materialization/current activation:
    BLOCKED
```

The first N3 execution was operationally successful and read-only. Its output is retained as audit evidence, but it is not accepted as the decision surface because normalization pressure contained three classification defects.

## Reviewed receipt

```text
archive:
    selected-obsidian-provider-authority-n3-normalized-classification-results-20260712-163413.tgz

independent SHA-256:
    483e5a5a48fed1f2e6e4698d3ac99d023dd0a1c9c087278be6f837b36b4b9fed

captured branch:
    docs/post-graphics-architecture-audit

captured HEAD:
    46e6094e969d55fbd68d9bf2c8a0ca8906f49585

archive members:
    24

archive safety:
    PASS
```

Independent reconstruction confirmed:

```text
embedded N2/current-schema inputs:
    13 / 13 SHA-256 MATCH

raw N2 census rows:
    26,419

raw prefix paths:
    27,279

first normalized rows:
    1,560

duplicate row IDs:
    0

blank required fields:
    0

accepted final authority decisions:
    0

package/runtime/generation/current operations:
    NONE
```

The transaction therefore remains valid evidence of the executed code and inputs.

## Defect 1 — symlink path semantics were discarded

The first normalizer returned `SYMLINK_ALIAS` before evaluating path meaning.

Result:

```text
all symlink paths classified as SYMLINK_ALIAS:
    8,168

actual library/loader-style alias paths after path-aware classification:
    328
```

The other 7,840 symlinks belong to path classes such as:

```text
DOCUMENTATION
SHARED_DATA
HEADER
BUILD_METADATA
EXECUTABLE_TOOL
CONFIGURATION
LOCALE_DATA
STATIC_OR_STARTFILE
```

A documentation or data symlink must not inherit runtime provider pressure merely because its package also owns runtime libraries.

Correction:

```text
classify semantic path first;
use SYMLINK_ALIAS only for otherwise-unclassified symlinks.
```

## Defect 2 — selected X11/XCB objects lost platform pressure

The selected/reference rows retained only historical workload-capability membership. Current package pressure correctly identified the Termux X11/XCB packages, but selected paths were excluded from the additional prefix-ELF pass.

Therefore 16 selected/excluded X11/XCB objects were absent from `platform.x11-xcb.termux` membership.

Correction:

```text
augment selected rows with package-derived provider-capability pressure;
preserve historical GTK/graphics memberships as overlapping groups.
```

Expected corrected behavior:

```text
active selected X11/XCB objects:
    9
    PLATFORM_INTEGRATION_PROVIDER provisional pressure

closed graphics-feature X11/XCB objects:
    7
    retain GENERIC_SHARED_CAPABILITY_PROVIDER / BLOCKED
    also retain platform.x11-xcb.termux overlapping membership
```

No closed graphics gate is reopened.

## Defect 3 — consumer capability was confused with provider authority

`libcap.so.2.69` participated in the udev consumer closure, so its historical capability membership included `platform.device-udev.termux`.

That does not make libcap itself an Android/Termux integration provider.

Correction:

```text
libcap:
    GENERIC_SHARED_CAPABILITY_PROVIDER pressure

libudev:
    PLATFORM_INTEGRATION_PROVIDER pressure
```

Historical consumer memberships remain visible.

## Termux world-entry correction

The package:

```text
termux-exec-glibc
```

was assigned to `platform.device-udev.termux`. Its responsibility is instead world-entry/glibc adaptation.

Correction:

```text
termux-exec-glibc
    -> platform.glibc-adaptation.termux
```

Documentation owned by that package remains documentation/tooling surface, not runtime integration surface.

## Corrected development fixture

The corrected normalizer passed against the accepted N2 receipt fixture.

```text
analysis.status:
    PASS

normalized rows:
    1,551

capability rows:
    26

selected/reference rows:
    161

supplemental rows:
    20

additional prefix ELF rows:
    911

package aggregate rows:
    86

unowned loader-state rows:
    2

non-ELF aggregates:
    345

duplicate normalized row IDs:
    0

authority decisions accepted:
    0
```

Corrected non-ELF path accounting:

```text
DOCUMENTATION:
    13,350 paths

SHARED_DATA:
    6,365 paths

HEADER:
    3,428 paths

OTHER_NON_ELF:
    1,069 paths

SYMLINK_ALIAS:
    328 paths

remaining classes:
    760 paths

total:
    25,300 paths
```

The total is unchanged; only the normalized grouping is corrected.

## Added validation gates

The corrected normalizer fails if:

```text
selected X11/XCB rows lose platform capability pressure;
active selected X11/XCB rows are not platform-integration pressure;
termux-exec package/ELF rows are not glibc-adaptation pressure;
normalized row IDs collide;
required census fields are blank.
```

## Direction decision

```text
first N3 receipt:
    TRANSACTION PASS
    DECISION SURFACE SUPERSEDED

corrected N3 implementation:
    READY_FOR_DEVICE EXECUTION

next accepted state requires:
    corrected device receipt PASS
```

After corrected receipt review, the valid next analytical work is source recipe, patch, and artifact comparison.

## Stop line

Do not:

```text
use the first 1,560-row output for provider-source decisions;
treat documentation/data symlinks as runtime aliases;
treat consumer membership as provider authority;
treat selected X11/XCB objects as generic-only without platform pressure;
run package operations;
mutate the generation or current;
reopen graphics work;
start successor composition.
```
