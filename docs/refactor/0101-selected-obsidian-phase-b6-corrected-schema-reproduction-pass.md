# 0101 — Selected Obsidian Corrected Phase B6 Schema-Reproduction Pass

## Status

The corrected Phase B6 receipt passed and closes the remaining GSettings source/compiler provenance gap.

```text
analysis.status:
    PASS

next state:
    READY_FOR_COMPLETE_DATA_MANIFEST

runtime launch:
    NO

promoted runtime mutation:
    NO
```

## Authoritative receipt

Archive:

```text
selected-obsidian-phase-b6-gsettings-schema-reproduction-corrected-20260711-222459.tgz
```

Archive SHA-256:

```text
4b86b884f31a87c38636b7c96b4a45de7588b89fd9b5073d02a8db4c52edf699
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    b772acb5f6895622e73eda1a6133094885304627
```

The archive contained 127 safe members under one relative Termux path.

It contained no:

```text
absolute path
parent traversal
symlink
hardlink
device node
special member
```

## Corrected source closure

```text
Phase B5 source files:
    36

corrected source files:
    37

sources added:
    1

Phase B5 sources missing from current schema directory:
    0
```

The only added source is:

```text
org.gnome.desktop.enums.xml
```

Path:

```text
/usr/share/glib-2.0/schemas/org.gnome.desktop.enums.xml
```

Package owner:

```text
gsettings-desktop-schemas
```

SHA-256:

```text
d38d656ef78f69f47f19cb19ea9b9d463d56b3660e1f25d499f66f7e3b6a508d
```

Corrected source distribution:

```text
XML:
    36

override:
    1

gsettings-desktop-schemas:
    33

libgtk-3-common:
    4
```

Every source copied into both compile attempts matched the corrected manifest SHA-256.

```text
source verification:
    37 / 37 MATCH

duplicate basenames:
    0

unowned corrected sources:
    0
```

Independent XML inspection found:

```text
defined enum/flags identifiers:
    41

referenced enum/flags identifiers:
    40

referenced but undefined identifiers:
    0
```

## Compiler identity

```text
path:
    $PREFIX/bin/glib-compile-schemas

realpath:
    $PREFIX/bin/glib-compile-schemas

package:
    glib

version:
    2.88.2

SHA-256:
    5f8cfe28f5eed9e5b9400260ec0127cae5c3f881437915df3fcdca33cbe5d165
```

No rootfs compiler or package installation was used.

## Reproduction result

Retained aggregate SHA-256:

```text
457f7461585b4caf6e11de65f707077bcb2208f9916c0c588080262f43ecb938
```

### Default mode

```text
return code:
    0

stdout:
    empty

stderr:
    empty

generated size:
    42597 bytes

generated SHA-256:
    457f7461585b4caf6e11de65f707077bcb2208f9916c0c588080262f43ecb938

byte-identical:
    YES
```

### Strict mode

```text
return code:
    0

stdout:
    empty

stderr:
    empty

generated size:
    42597 bytes

generated SHA-256:
    457f7461585b4caf6e11de65f707077bcb2208f9916c0c588080262f43ecb938

byte-identical:
    YES
```

The two generated aggregates are also byte-identical to each other.

## Data ownership closure

```text
locale ownership:
    CLOSED
    WORLD_LOCALE_GLIBC
    reference protected glibc prefix data

font ownership:
    CLOSED
    SELECTED_FONT_DATA
    materialize four exact package-owned files

schema source ownership:
    CLOSED
    37 exact package-owned inputs

schema compiler lineage:
    CLOSED
    native Termux glib 2.88.2 compiler identity

schema aggregate reproducibility:
    CLOSED
    clean default and strict byte-identical reproduction
```

The retained `gschemas.compiled` may now be represented as a generated selected-data artifact with:

```text
37-source manifest
compiler path/package/version/SHA-256
compile mode contract
expected aggregate SHA-256
```

It no longer needs opaque rootfs aggregate authority.

## Candidate consequence

The last data-provenance blocker before complete manifest synthesis is removed.

```text
static ELF ownership model:
    CLOSED FOR MANIFEST SYNTHESIS

dynamic CPU capability ownership:
    CLOSED FOR MANIFEST SYNTHESIS

data ownership/provenance:
    CLOSED FOR MANIFEST SYNTHESIS

candidate bytes:
    NOT MATERIALIZED

next action:
    SYNTHESIZE COMPLETE SELECTED CPU CANDIDATE MANIFEST
```

The complete semantic disposition should account for all retained classes:

```text
application-local ELF/data:
    reference AppDir

world glibc ELF/locale:
    reference protected world

external static ELF:
    materialize one deduplicated selected set

NSS/security dynamic ELF:
    materialize required CPU dynamic set

Vulkan provider/layer dynamic ELF:
    exclude from minimum CPU base

selected fonts:
    materialize exact files

GSettings aggregate:
    generate from the 37-source/compiler manifest

mutable state and runtime caches:
    exclude from immutable generation and recreate under runtime ownership

GPU device node:
    reference only for optional GPU feature composition
```

## Claim boundary

Corrected Phase B6 proves:

```text
the complete retained schema source set contains 37 files;
the previously omitted enum-definition input is explicit and package-owned;
all source identities are stable;
the native compiler identity is explicit;
default and strict compilation are clean;
both modes reproduce the retained aggregate byte-for-byte;
schema aggregate provenance is reproducible without rootfs package installation.
```

It does not prove:

```text
a selected candidate generation has been materialized;
loader paths select that generation;
Obsidian consumes a generated candidate schema directory;
atomic activation or rollback;
workload equivalence.
```

## Stop line

Do not:

```text
rerun Phase B1-B6 without a source trigger;
copy rootfs gschemas.compiled as an opaque unmanaged input;
materialize before the complete semantic manifest is emitted and checked;
copy app-local or world objects into the application generation;
include Vulkan provider roots in the minimum CPU base;
implement activation before the generation manifest is complete.
```
