# GdkPixbuf core provider acquisition result review

## Decision

```text
acquisition result:              REVIEWED_PARTIAL
exact candidate identities:      5 / 6
GdkPixbuf package or recipe:      NOT FOUND
GLib recipe:                     exact Class B reference-adapted root
libpng recipe:                   exact packaging-adapted root
provider authority accepted:     0
composition effect:              none
target manifest allowed:         NO
next action:                     produce GdkPixbuf 2.42.12 scratch candidate
```

The read-only acquisition result archive has SHA-256
`e96fb0e2d8fa1c16a228e41d60801abac0b8a43584a86b7e63f8adddfc4f5692`.
It binds exact `glib-glibc 2.82.2-2` and `libpng-glibc 1.6.47`
artifacts, exact pinned recipe trees and five exact AArch64 members. It does
not accept provider authority.

Canonical machine-readable review:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
  gdkpixbuf-core-provider-acquisition-result-review.tsv
  gdkpixbuf-core-provider-acquisition-result-review-metadata.tsv
```

## Exact candidates acquired

The GLib artifact is pinned by SHA-256
`d91fe1202c51f7e59b120d3b475e24cdc2ac2cc28f2804e9bcf4919b775978e6`
and supplies:

```text
libglib-2.0.so.0.8200.2
libgobject-2.0.so.0.8200.2
libgmodule-2.0.so.0.8200.2
libgio-2.0.so.0.8200.2
```

All four are ELF64 AArch64 shared objects, have the expected SONAME, have no
RPATH or RUNPATH, and have one exact SONAME alias in the artifact.

The libpng artifact is pinned by SHA-256
`b2835404d3b0f54b75eb464a58ad5eb46f2d64d4fe1167a7984031f0e990b33f`
and supplies exact member `libpng16.so.16.47.0` with SHA-256
`00c9fd06c139699552c086b60d116a01d067ceddddb29c56600bf9fd3bae746f`,
SONAME `libpng16.so.16`, no RPATH or RUNPATH, and both development and SONAME
aliases.

The selected Debian concrete suffixes `0.8400.4` and `16.48.0` remain drift
references. Provider identity is bound by SONAME and the exact accepted member,
not by copying Debian oracle bytes or inventing successor filenames.

## Recipe boundary

`gpkg/glib` is not a no-token recipe. Its exact tree
`de335e6ba82f295978c17dcf3666a38bfd51538f` contains thirteen files,
including GLib/GIO platform patches, Meson changes, package hooks and explicit
configuration. The four-member family therefore remains a Class B
reference-adapted candidate until functional consumer binding is complete.

`gpkg/libpng` exact tree `c28b21ff2f072e880bce82fe81e4022b88945c22`
contains one `build.sh`. Its library build follows the pinned upstream source,
but the recipe adds post-install utility builds. The library member is reviewed
separately from those utilities and remains a bounded Class B packaging
integration candidate.

## Missing GdkPixbuf coordinate

No GdkPixbuf package candidate appeared in any parsed Termux package index, and
no GdkPixbuf recipe was present in pinned source repository commit
`fd2ae25e04f3ea26d6c7b4678020814889331d86`. The Debian
`libgdk_pixbuf-2.0.so.0.4200.12` object remains functional oracle evidence and
is explicitly excluded from target provider authority.

The next bounded step is a project-produced Class C candidate from official
GdkPixbuf 2.42.12 source. Upstream versioning produces exact member
`libgdk_pixbuf-2.0.so.0.4200.12`. PNG and JPEG are built in, tests,
introspection, documentation and GIO sniffing are disabled, and the object is
linked only against the exact acquired GLib/libpng candidates and the already
accepted project `libjpeg.so.62` object.

The host Python build tool is repository-owned at
`packages/gdkpixbuf-glibc/build-env/{pyproject.toml,uv.lock}`. Meson is locked
as a platform-independent Python wheel and synchronized into a disposable
scratch venv with the installed Android CPython runtime. Ninja remains a
native Termux host command; PyPI Ninja/CMake executables are not selected as
Bionic build-tool authority.

## Protected-state result

The acquisition reported `PROTECTED_STATE_RC=1`, but the only differing digest
was the repository path. Repository HEAD, tree and tracked status remained
unchanged; `$PREFIX/glibc` and `$HOME/gl` digests were identical before and
after.

The collector hashed size and nanosecond mtime for every path, including the
nested retained source repository's `.git` metadata. Read-only Git inspection
may refresh `.git/index` metadata and therefore changed the parent raw-tree
metadata digest without changing tracked project content. This is classified as
`FALSE_POSITIVE_NESTED_GIT_METADATA_MTIME`. Future collectors must use Git
HEAD/tree/status for repository protection and exclude `.git` metadata from
filesystem snapshots.

## Authority boundary

This review authorizes no installation, extraction into a live prefix, provider
store mutation, composition acceptance, target population or activation. The
five exact members are candidate inputs only. Provider authority requires the
sixth exact GdkPixbuf candidate plus loader-isolated JPEG and PNG file/memory
functional evidence with exact mapped-member proof.
