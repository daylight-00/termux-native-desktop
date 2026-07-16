# Bounded libXcursor provider authority for GTK 3.24.49 X11 cursors

## Decision

```text
root:               gpkg/libxcursor
decision:           ACCEPTED_BOUNDED_PROVIDER
accepted member:    libXcursor.so.1.0.2
accepted SONAME:    libXcursor.so.1
accepted capability: GTK 3.24.49 X11 cursor theme, image and surface handling
composition:        not accepted
target population:  not accepted
activation:         not accepted
```

The exact Termux glibc `libXcursor.so.1.0.2` member is accepted only for the selected GTK 3.24.49 X11 cursor path. This is a Class B reference-adapted provider decision under [ADR 0005](../decisions/0005-proportional-assurance-depth.md).

Canonical machine-readable record:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    libxcursor-bounded-provider-authority.tsv
```

## Exact provider identity

```text
root review:       generic-root-review:54ab99c9280e70c43600
recipe tree:       bb2495e04b246f60203d48720225ef13fa8a25bf
build script blob: a0ee9a7131a9ce3a3f8fbce0b1f5f2db88c21c29
patch blob:        379e15f8152af7a9665b113bc470042f73c3a8a8
package:           libxcursor-glibc 1.2.3
artifact SHA-256:  7901dd136016df9d694e38bb17923812f539241475e7ac97935c8dcdfcceb902
member:            data/data/com.termux/files/usr/glibc/lib/libXcursor.so.1.0.2
member SHA-256:    86e70b94186edb4c16cf00f2bcea4a03ea09bb486ee6a079dd11d3ef6fffe722
SONAME:            libXcursor.so.1
```

The exact regular ELF member and expected SONAME are observed. No concrete-filename drift exists.

## Class B adaptation boundary

The pinned recipe contains only `build.sh` and `src-library.c.patch`. The patch changes the built-in cursor search locations:

```text
/usr/X11R6/lib/X11/icons -> $TERMUX_PREFIX/X11R6/lib/X11/icons
/usr/share/icons         -> $TERMUX_PREFIX/share/icons
/usr/share/pixmaps       -> $TERMUX_PREFIX/share/pixmaps
```

It does not change the ELF ABI, SONAME, exported Xcursor call surface, cursor image format or X11 protocol behavior. The accepted project-owned change is therefore the Termux-prefix search-path relocation only.

This does not claim byte reproduction or producing-build equivalence. The exact artifact and member digests remain the supply boundary.

## GTK consumer binding

GTK 3.24.49 provides direct static binding evidence:

- `gdk/x11/meson.build` links the X11 backend with `xcursor_dep`.
- `gdk/x11/gdkcursor-x11.c` includes `<X11/Xcursor/Xcursor.h>` when `HAVE_XCURSOR` is defined.
- The implementation calls Xcursor APIs for theme lookup, default size, named and shaped cursor image loading, cursor replacement, theme updates and custom cursor creation.
- The selected GTK closure contains the exact required `libXcursor.so.1` identity.

The accepted `libXfixes.so.3` provider participates in cursor-theme replacement, and the accepted base `libXrender.so.1` provider satisfies the package dependency boundary. No new authority is granted to other dependencies.

This is sufficient to establish necessity and consumer binding without a device probe. A runtime probe would repeat already-resolved static binding rather than close an ambiguity.

## Conflict and exclusion result

```text
one exact dynamic Termux glibc candidate
static-only sibling package excluded
Debian-rootfs bytes remain oracle evidence only
no concrete-filename or SONAME drift
no accepted member or alias collision
cursor theme data and package-wide surfaces excluded
```

A future composition may propose the SONAME alias `libXcursor.so.1 -> libXcursor.so.1.0.2`, but this decision does not create the alias or authorize a target path.

## Update and rollback boundary

Re-review is mandatory if any of the following changes:

```text
artifact version or SHA-256
member SHA-256 or ELF SONAME
recipe tree, build-script blob or patch blob
Termux prefix or cursor search-path policy
GTK tag, X11 cursor source or dependency set
candidate multiplicity or collision set
```

Before materialization, rollback is revocation of this provider row. Any future materialization must occur in a new immutable generation; runtime rollback is selector reversal to the prior immutable generation preserving its previous X11 cursor provider set.

## Explicitly prohibited inference

This decision does not establish:

```text
complete X11 or GTK composition
cursor theme data authority
provider target paths or filesystem population
package-wide libXcursor development surfaces
materialization or deployment readiness
selected-generation activation readiness
producing-build equivalence
```

The selected composition remains blocked. The next smallest reviewed-root, single-member tranche is `gpkg/libthai`.
