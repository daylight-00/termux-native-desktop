# Four X.Org reference-consumed provider-authority decisions

## Status

```text
reviewed roots:                4
accepted bounded providers:    4
rejected providers:            0
open explicit gaps:            0
composition effect:            NONE
target population effect:      NONE
activation effect:             NONE
```

This record decides provider authority for four exact Class A X.Org recipe roots under [ADR 0005](../decisions/0005-proportional-assurance-depth.md):

```text
gpkg/libxfixes
gpkg/libxcomposite
gpkg/libxi
gpkg/libxinerama
```

The canonical machine-readable result is:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    xorg-reference-consumed-provider-authority.tsv
```

Each decision is limited to one exact Termux glibc package artifact, one exact regular ELF member, its observed `DT_SONAME`, and the selected GTK 3.24.49 X11 capability that consumes it.

## Evidence boundary

The review combines five bounded evidence classes:

1. Phase B4 selected-entrypoint static closure evidence showing the four lookup names inside the selected GTK/X11 closure; `libXcomposite.so.1` and `libXfixes.so.3` were direct roots of the dominant GTK closure.
2. Exact Termux glibc repository artifact identity, package version and SHA-256.
3. Exact regular member path, member SHA-256 and matching ELF `DT_SONAME`.
4. Completed Class A recipe semantic review showing no package-specific patch, hook, build option or output transformation.
5. The pinned GTK 3.24.49 upstream build definition:
   - `meson.build` declares the X11 dependencies and feature probes;
   - `gdk/x11/meson.build` links the X11 backend against Xi, XFixes, XComposite and Xinerama when the corresponding feature is present.

This is sufficient for bounded provider selection. It is not a producing-build equivalence claim and does not require SUP-02.

## Decisions

### `gpkg/libxfixes`

```text
artifact:  libxfixes-glibc 6.0.1
member:    libXfixes.so.3.1.0
SONAME:    libXfixes.so.3
decision:  ACCEPTED_BOUNDED_PROVIDER
```

Necessity is established by the selected GTK direct-root closure, GTK X11 feature binding, and the XComposite/XI dependency chain. The static package is excluded and no second dynamic Termux candidate exists in the bounded comparison set.

### `gpkg/libxcomposite`

```text
artifact:  libxcomposite-glibc 0.4.6
member:    libXcomposite.so.1.0.0
SONAME:    libXcomposite.so.1
decision:  ACCEPTED_BOUNDED_PROVIDER
```

The object is a selected GTK direct root and the GTK X11 backend links the detected XComposite feature into GDK. The exact Termux member has no concrete-filename or SONAME drift.

### `gpkg/libxi`

```text
artifact:  libxi-glibc 1.8.2
member:    libXi.so.6.1.0
SONAME:    libXi.so.6
decision:  ACCEPTED_BOUNDED_PROVIDER
```

GTK 3.24.49 requires the `xi` dependency for the X11 backend and compiles the XI2 device and gesture implementation into GDK. The selected closure contains the exact required SONAME.

### `gpkg/libxinerama`

```text
artifact:  libxinerama-glibc 1.1.5
member:    libXinerama.so.1.0.0
SONAME:    libXinerama.so.1
decision:  ACCEPTED_BOUNDED_PROVIDER
```

Xinerama is not claimed as universally mandatory. GTK enables it conditionally when found. The selected GTK closure contains the exact SONAME, which proves the selected build bound this feature. Authority is therefore limited to preserving that existing selected GTK/X11 behavior.

## Conflict and exclusion result

For every row:

```text
one exact dynamic Termux glibc candidate
static-only sibling package excluded
debian-rootfs bytes remain oracle/reference evidence only
no concrete-filename drift
observed SONAME equals required lookup name
```

The Debian oracle members are not selected as the target provider because the project is constructing a coherent Termux glibc provider generation rather than preserving the first-generation Debian-rootfs supply mechanism.

## Update and rollback boundary

Re-review is mandatory if any of the following changes:

```text
artifact version or SHA-256
member SHA-256 or ELF SONAME
pinned recipe tree
GTK X11 feature set or consumer binding
candidate multiplicity or conflict set
```

This decision performs no runtime mutation. A future materializer must place accepted providers only in a new immutable generation. Runtime rollback remains a selector reversal to the previous immutable generation; before materialization, rollback is simply revocation of the provider row.

## Explicitly prohibited inference

These four decisions do not establish:

```text
complete provider authority
complete application runtime composition
target membership or target paths
alias or collision policy
materialization readiness
selected-generation activation readiness
```

The remaining no-token provider roots and all explicit-delta roots remain separate decisions.
