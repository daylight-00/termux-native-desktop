# GdkPixbuf 2.42.12 bounded provider-authority decision

## Status

```text
candidate identity:         accepted
JPEG file / memory:         PASS / PASS
PNG file / memory:          PASS / PASS
exact mapped objects:       9
bounded provider authority: ACCEPTED
composition effect:         one accepted member, composition still blocked
target / activation effect: NONE
```

This decision reviews result archive SHA-256 `1cebcf8784c6d2e8c8549eadd63007d9f99bb3e90e35ce0786a5d89f6cbecca0` under [ADR 0005](../decisions/0005-proportional-assurance-depth.md).

Canonical machine-readable decision:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    gdkpixbuf-2-42-12-provider-candidate-result-review.tsv
```

## Exact accepted object

```text
source:         official GdkPixbuf 2.42.12
source SHA-256: b9505b3445b9a7e48ced34760c3bcb73e966df3ac94c95a148cb669ab748e3c7
member:         libgdk_pixbuf-2.0.so.0.4200.12
member SHA-256: 0c1404c6854e7674428a5b653b240759dac0374631697fe61ae275898f6a809f
Build ID:       3e9a87bdfc7e017001e570535eb8c09a4e3a8806
DT_SONAME:      libgdk_pixbuf-2.0.so.0
machine:        AArch64
DT_RPATH:       absent
DT_RUNPATH:     absent
```

The build enabled only builtin PNG and JPEG loaders and disabled GIF, TIFF, other loaders, GIO sniffing, introspection, tests, installed tests, documentation and manual pages. One build-tree search-path dynamic tag was removed after linking; the accepted identity is the final post-normalization digest above, not the pre-normalization object.

## Functional and mapping result

The fixed 3x2 fixtures passed all four bounded cells:

```text
JPEG file API:   PASS, 3x2x3x8
JPEG memory API: PASS, 3x2x3x8
PNG file API:    PASS, 3x2x3x8
PNG memory API:  PASS, 3x2x3x8
```

`/proc/self/maps` bound the exact final GdkPixbuf candidate, the four exact acquired GLib-family members, exact libpng, the already accepted project `libjpeg.so.62`, and scratch util-linux `libmount`/`libblkid` diagnostic candidates. The repository, live glibc prefix, provider store and deployment state were unchanged.

## Provider decision

```text
decision:
    ACCEPTED_BOUNDED_PROVIDER

scope:
    exact libgdk_pixbuf-2.0.so.0.4200.12 object
    fixed JPEG and PNG file and memory decode APIs

remaining dependency-provider boundary:
    GLib / GObject / GModule / GIO provider authority open
    libpng provider authority open
    libmount and libblkid transitive provider authority open
```

This acceptance is valid because source identity, project-owned build and post-link transformation, exact final ELF identity, direct dependency selection, four functional cells and protected-state invariants agree. It accepts the GdkPixbuf object only. Successful use of candidate dependencies does not promote those dependencies.

## Conflict and exclusion result

```text
project-built final GdkPixbuf candidate selected
Debian GdkPixbuf oracle bytes excluded from target authority
no Termux GdkPixbuf package or recipe inferred
no unversioned development alias accepted
no RPATH or RUNPATH accepted
scratch libmount and libblkid remain diagnostic only
no target path, copy, population or selector mutation authorized
```

The result archive's `candidate-manifest.tsv` contains literal `\t` text rather than actual tab delimiters. Its facts are independently verified by ELF, hash, map and functional files, so this is non-blocking evidence-format debt. Future `.tsv` result members must contain real tab-separated fields and be parser-validated before archival.

## Composition effect

The selected-provider composition may add this one accepted member and remove the historical Debian GdkPixbuf identity from the open-gap set. This changes:

```text
accepted provider roots:       8 -> 9
accepted exact members:        10 -> 11
included selected GTK members: 9 -> 10
unresolved selected identities:27 -> 26
```

Composition remains `REVIEWED_BLOCKED_INCOMPLETE`. The next bounded tranche is the exact GLib-family, libpng and transitive libmount/libblkid provider boundary.

## Update and rollback boundary

Re-review is mandatory if source/version/digest, build environment, toolchain, Meson options, post-link normalization, final digest, Build ID, SONAME, `DT_NEEDED`, fixed decode matrix, mapped direct dependency identities or transitive dependency set changes.

Before materialization, rollback is revocation of this provider row. A future materializer must place the object only in a new immutable generation. Runtime rollback must reverse the selector to the prior generation and remove the object from the successor target without modifying an existing generation in place.

## Explicitly prohibited inference

This decision does not establish provider authority for GLib, libpng, libmount or libblkid; complete GdkPixbuf loader coverage; complete GTK/application composition; target membership or paths; materialization, deployment or activation readiness.
