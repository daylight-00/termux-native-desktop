# `libjpeg.so.62` loader-isolated bounded provider-authority decision

## Status

```text
requirement:                    OJ-001
candidate identity:             accepted
loader-isolated matrix cells:   6
matrix passes:                  6
matrix failures:                0
bounded provider authority:     ACCEPTED
composition effect:             NONE
target population effect:       NONE
activation effect:              NONE
```

This decision accepts one exact project-produced `libjpeg.so.62` provider for one bounded consumer capability. It is governed by [ADR 0005](../decisions/0005-proportional-assurance-depth.md).

Canonical machine-readable decision:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    libjpeg-so-62-loader-isolated-provider-authority.tsv
```

## Exact provider

```text
source:         libjpeg-turbo 3.1.0
source SHA-256:
                9564c72b1dfd1d6fe6274c5f95a8d989b59854575d4bbee44ade7bc17aa9bc93
build mode:     v6b compatibility; shared only; no RPATH/RUNPATH
member:         libjpeg.so.62.4.0
member SHA-256:
                a537840ef9da6135cb3284bc3b3e0d1fb4f624180a416c2a3964b94714eb7fe5
DT_SONAME:      libjpeg.so.62
symbol versions:
                LIBJPEG_6.2
                LIBJPEGTURBO_6.2
```

The first object with a colon-only build-tree `DT_RUNPATH` remains rejected. This decision applies only to the corrected runpath-free object above.

## Bounded consumer

```text
consumer:       libgdk_pixbuf-2.0.so.0.4200.12
consumer SHA-256:
                16d15168c69d4ad61862462da9fe811b5be3bef898b940a4023e15b039f5b43c
binding:        DT_NEEDED=libjpeg.so.62
undefined JPEG symbols: 22
missing candidate symbols: 0
```

The accepted capability is limited to the selected GdkPixbuf 2.42.12 file and memory JPEG decode paths. The consumer is named to bound the provider capability; this decision does not accept a complete GTK or image-codec composition.

## Loader-isolated functional result

Result archive:

```text
SHA-256:
4e546ac1ef2a92f3301dd51ca2328d6901a05e309da78b6d08b26211d9b621e3
```

The corrected matrix directly invoked the Termux-glibc loader and used an ELF-only scratch runtime shim. It did not start the Bionic `glibc-exec` shell under a foreign library path.

```text
direct candidate djpeg: PASS
direct Debian oracle djpeg: PASS
direct output SHA-256, both providers:
    8cef10ed9b5f2e4ffde1fdedc4b722d4738d86ac5d204554328c30ef34ecbdc6

GdkPixbuf candidate, file API:   PASS, stage 09:complete
GdkPixbuf candidate, memory API: PASS, stage 09:complete
GdkPixbuf oracle, file API:      PASS, stage 09:complete
GdkPixbuf oracle, memory API:    PASS, stage 09:complete
```

`dladdr` and `/proc/self/maps` evidence showed the exact scratch candidate in both candidate GdkPixbuf cells and the exact Debian oracle in both oracle cells. The exact GdkPixbuf consumer member was mapped in all four consumer cells. Protected live state was unchanged.

## Necessity and consumer binding

The selected GdkPixbuf object requires the stable SONAME `libjpeg.so.62` and exposes 22 unresolved JPEG symbols that the candidate supplies. The repository `libjpeg.so.8` family is an incompatible ABI family and cannot satisfy that lookup identity.

Independent evidence now agrees across:

1. exact v6b source and build coordinates;
2. exact candidate member, digest, SONAME, dynamic tags and symbol versions;
3. exact consumer digest and `DT_NEEDED` contract;
4. complete static symbol coverage;
5. direct candidate/oracle decode equivalence on the fixed fixture;
6. successful file and memory GdkPixbuf decode with exact mapped-provider proof;
7. unchanged protected state.

This closes the proportional assurance gap for the bounded GdkPixbuf JPEG capability.

## Conflict and exclusion result

```text
project v6b candidate selected for accepted scope
Termux libjpeg.so.8 family excluded
libjpeg.so.8 -> libjpeg.so.62 alias prohibited
Debian libjpeg.so.62.3.0 retained as oracle only
candidate contains no DT_RPATH or DT_RUNPATH
one exact candidate identity accepted for the bounded scope
unversioned development aliases excluded
installation and target paths not decided
```

The Debian oracle demonstrates comparison behavior but its bytes have no target authority. The project-produced candidate is the accepted provider identity.

## Decision

```text
decision:
    ACCEPTED_BOUNDED_PROVIDER

scope:
    exact libjpeg.so.62.4.0 object
    observed SONAME libjpeg.so.62
    selected GdkPixbuf 2.42.12 JPEG file and memory decoding

remaining provider gap:
    NONE_FOR_BOUNDED_GDKPIXBUF_JPEG_PROVIDER_AUTHORITY
```

This is provider authority only. It does not define a complete provider composition, target membership, target path, materialization plan or selected-generation activation.

## Update and rollback boundary

Re-review is mandatory if any of these changes:

```text
source version or source SHA-256
v6b/shared/RPATH build options or toolchain boundary
candidate member SHA-256, SONAME or symbol versions
GdkPixbuf consumer member SHA-256 or DT_NEEDED set
consumer unresolved JPEG symbol set
runtime loader or ELF-only core-shim construction
fixed fixture or file/memory API result
direct candidate/oracle output digest
candidate conflict set
```

Before materialization, rollback is revocation of this provider row. A future materializer must place this object only in a new immutable generation. Runtime rollback must reverse the selector to the prior immutable generation and remove this project v6b member from the successor target without rewriting an existing generation in place.

## Explicitly prohibited inference

This decision does not establish:

```text
libjpeg.so.8 compatibility or aliasability
Debian oracle bytes as target authority
all JPEG consumers or all image codecs
complete GdkPixbuf, GTK or application composition
target membership or target paths
materialization, deployment or activation readiness
```
