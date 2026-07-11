# 0099 — Selected Obsidian Phase B5 Data-Provenance Review

## Status

Phase B5 completed successfully.

```text
analysis.status:
    PASS

next state:
    REVIEW_DATA_PROVENANCE_GAPS

failure-stage.txt:
    absent

runtime launch:
    NO

promoted runtime mutation:
    NO
```

This is a valid completed audit with one remaining provenance gap. It is not a script failure.

## Authoritative receipt

Archive:

```text
selected-obsidian-phase-b5-data-capability-provenance-20260711-214050.tgz
```

Archive SHA-256:

```text
bea406cd8bc69a7b12e418668f16cca46ee1777430bca43f24414be68980da9f
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    4e2fc5352d384c50bbf8370fa24fb7a377e8bab0
```

The archive contained 18 members under one relative Termux path and no absolute path, parent traversal, symlink, hardlink, device, or other special member.

## Primary result

```text
data objects:
    17

locale objects:
    12

font objects:
    4

schema aggregate objects:
    1

identity mismatches:
    0

missing paths:
    0

rootfs-owned font objects:
    4 / 4

rootfs unowned non-aggregate objects:
    0

schema source files:
    36

schema unowned source files:
    0

schema compiler instances present:
    0
```

All 17 current bytes matched their retained captured SHA-256 values.

## Independent verification

The embedded B2 input and Phase B5 object table were compared row-for-row.

Verified:

```text
17 input rows
17 verification rows
17 identity MATCH rows
0 metadata mismatch rows
```

Ownership-state distribution:

```text
font package ownership MATCH:
    4

prefix-managed non-rootfs locale:
    12

generated/unowned schema aggregate:
    1
```

## Locale ownership decision

All 12 locale objects are under:

```text
$PREFIX/glibc/lib/locale/en_US.utf8
```

They are version-coupled to the protected glibc 2.42 substrate and are not rootfs package files.

Accepted direction:

```text
owner:
    WORLD_LOCALE_GLIBC

candidate behavior:
    reference prefix-managed locale data

candidate materialization:
    do not copy locale bytes into the application-domain generation
```

A future glibc substrate replacement must revalidate locale compatibility as part of the world lifecycle.

## Font ownership decision

All four retained font files matched both byte identity and rootfs package ownership:

```text
fonts-noto-cjk
    NotoSansCJK-Regular.ttc

fonts-dejavu-extra
    DejaVuMathTeXGyre.ttf

fonts-dejavu-mono
    DejaVuSansMono.ttf
    DejaVuSansMono-Bold.ttf
```

Accepted direction:

```text
owner:
    SELECTED_FONT_DATA

candidate behavior:
    materialize the exact selected files with package/version/hash provenance

rootfs runtime authority:
    not required
```

This is selected passive data, not an ELF provider closure and not a request to install a broad desktop font set.

## GSettings source ownership

The retained aggregate is:

```text
/usr/share/glib-2.0/schemas/gschemas.compiled
```

It matched retained SHA-256 but remains a generated file with no direct dpkg file owner.

The audit found 36 source files:

```text
XML:
    35

override:
    1
```

All source files are package-owned:

```text
gsettings-desktop-schemas:
    32

libgtk-3-common:
    4

unowned source files:
    0
```

Therefore schema source ownership is closed.

Accepted semantic direction:

```text
owner:
    SELECTED_GSETTINGS_SCHEMA_DATA

source manifest:
    package/version/path/SHA-256 selected input set

aggregate:
    generated candidate artifact, not an opaque rootfs-owned byte
```

## Remaining blocker

The retained rootfs does not contain:

```text
/usr/bin/glib-compile-schemas
```

Receipt:

```text
compiler_present:
    NO

compiler_sha256:
    MISSING

dpkg_file_owners:
    UNOWNED
```

This means the aggregate cannot yet be claimed reproducible from the 36 owned sources using a captured compiler lineage.

The missing compiler does not invalidate the existing aggregate byte identity or source ownership. It blocks only the stronger reproducibility/materialization claim.

## Data ownership state

```text
locale ownership:
    CLOSED

font ownership:
    CLOSED

schema source ownership:
    CLOSED

schema aggregate compiler lineage:
    OPEN

candidate data manifest:
    ALMOST READY

candidate materialization:
    STILL BLOCKED
```

## Next action

Run a read-only schema compiler discovery and reproduction stage.

It must:

```text
verify all 36 source hashes again;
discover explicit glib-compile-schemas candidates;
record candidate path, byte identity, package provenance, and version output;
compile only in receipt-local temporary directories;
compare generated gschemas.compiled SHA-256 with the retained aggregate;
retain stdout/stderr/return code for every attempted candidate;
perform no rootfs installation and no promoted runtime mutation.
```

A byte-identical result closes schema aggregate provenance for that source/compiler identity.

A successful compile with a different hash is useful evidence but does not authorize replacing the retained aggregate without explaining version/ordering/format differences.

No compiler candidate means the next step is a separately documented compiler-oracle acquisition, not an unscoped package installation.

## Claim boundary

Phase B5 proves:

```text
all retained data bytes are identity-stable;
all four fonts have exact package ownership;
all 36 GSettings inputs are package-owned;
locale, font, and schema source ownership can be decided;
the remaining gap is compiler lineage/reproduction only.
```

Phase B5 does not prove:

```text
that any available compiler reproduces the aggregate;
that compiler versions are interchangeable;
that rootfs runtime data paths may remain candidate authority;
that candidate data has been materialized;
that Obsidian selects the future data generation.
```

## Stop line

Do not:

```text
rerun Phase B1-B5 without a source trigger;
install libglib2.0-bin into the rootfs merely to make the check pass;
copy the opaque rootfs gschemas.compiled without a source/compiler manifest;
copy glibc locale data into the application generation;
expand the selected font set by package or directory inertia;
materialize the CPU candidate before schema compiler reproduction is resolved.
```
