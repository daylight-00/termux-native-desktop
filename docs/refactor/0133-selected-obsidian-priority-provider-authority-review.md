# 0133 — Selected Obsidian Priority Provider-Authority Review

## Status

```text
corrected N3 normalized classification:
    PASS / ACCEPTED

source-recipe evidence:
    PASS / ACCEPTED

exact binary-artifact comparison:
    PASS / ACCEPTED

priority package review:
    28 / 28 DISPOSITIONED

selected/reference object review:
    59 / 59 DISPOSITIONED

base-profile object authorities:
    29

conditional-profile object authorities:
    30

semantic provider-authority review:
    PARTIAL PASS

successor manifest/materialization/current activation:
    BLOCKED
```

## Inputs

This review combines the three accepted N3 receipts:

```text
normalized classification archive:
    selected-obsidian-provider-authority-n3-normalized-classification-results-20260712-165805.tgz
SHA-256:
    4dd86c4af956b447ed1829d6b5d604f43d10a17e5b3dcb3ddff3e9b48c377a9c

source-recipe archive:
    selected-obsidian-provider-authority-n3-source-recipe-evidence-results-20260712-185001.tgz
SHA-256:
    c8160016267f3ff83b348146240f74f808ffbc93374a6f75988231ef22408cdb

binary-artifact archive:
    selected-obsidian-provider-authority-n3-binary-artifact-comparison-results-20260712-194542.tgz
SHA-256:
    da16d49acf54cbc8b6824e3974f08fea9ad0d6daf91687f4666d6c48d0b7567f
```

The review does not add package installation, runtime launch, generation materialization, or current activation evidence.

## Review outputs

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    package-authority-t0.tsv
    package-authority-t1.tsv
    selected-object-authority-base.tsv
    selected-object-authority-conditional.tsv
    unresolved-authority-ledger.tsv
```

The two package ledgers record package-level source/supply authority and explicitly reject package-wide runtime inference where the artifact contains unrelated tools, plugins, headers, documentation, or unselected libraries.

The base and conditional object ledgers record all 59 priority selected/reference objects and separate base-profile authority from conditional feature-profile authority.

## Central decision: package authority is not runtime scope

The exact `.deb` receipts establish reproducible supply identity. They do not justify copying or retaining every member of each package in the minimum runtime.

Examples:

```text
libdrm-glibc:
    selected ELF:                 1 (libdrm.so.2)
    unselected backend libraries: 8
    unselected diagnostic tools:  19

krb5-glibc:
    selected libraries:           4
    unselected plugin/libraries:  11
    unselected executables:       24

e2fsprogs-glibc:
    selected library:             1 (libcom_err.so.2)
    additional libraries/helpers: 4
    executables:                  17

libxcb-glibc:
    selected libraries:           8
    additional extension libs:    17
```

Therefore the accepted model is:

```text
source recipe authority
    + exact artifact authority
    + member-level object authority
    + profile inclusion decision
```

not:

```text
installed package == minimum runtime authority
```

## World substrate

### `glibc 2.42`

Decision:

```text
semantic authority:
    WORLD_CORE_SUBSTRATE

authority state:
    ACCEPTED_WORLD_AUTHORITY

source authority:
    Termux/Android-adapted glibc recipe

supply authority:
    exact indexed artifact
    59e47a50b77ba9c0c1cc7cd0dafbb1558528cb544a740858faad0263e8b9b27f
```

The recipe is not a generic upstream build. It carries Android-specific syscall handling, Android user/group identity integration, Android logging, System V shared-memory emulation, disabled or emulated kernel interfaces, and Termux prefix/loader policy.

Generic upstream glibc and Debian glibc remain references, not native Termux world authority.

Accepted world runtime pressure includes:

```text
ld-linux-aarch64.so.1
libc.so.6
libdl.so.2
libm.so.6
libpthread.so.0
libresolv.so.2
selected locale data
runtime-internal NSS/gconv/locale modules demanded by declared applications
```

Headers, static/start files, build metadata, and administration/diagnostic programs belong to build or maintenance profiles even when the current indivisible package installs them.

Open world contract:

```text
clean reconstruction
world update trigger
2.42 -> 2.43 validation
world rollback independent of generation rollback
```

No device update is authorized by this review.

## Platform integration

### X11/XCB providers

The following package sources and exact artifacts are accepted as object-scoped platform providers:

```text
libx11-glibc
libxau-glibc
libxcb-glibc
libxdmcp-glibc
libxext-glibc
libxrandr-glibc
libxrender-glibc
libxshmfence-glibc
```

Base X11 authority includes the selected SONAME objects required by Obsidian and the X11 dependency chain:

```text
libX11.so.6
libXau.so.6
libxcb.so.1
libXdmcp.so.6
libXext.so.6
libXrandr.so.2
libXrender.so.1
```

Graphics-provider conditional authority includes:

```text
libX11-xcb.so.1
libxcb-dri3.so.0
libxcb-present.so.0
libxcb-randr.so.0
libxcb-render.so.0
libxcb-shm.so.0
libxcb-sync.so.1
libxcb-xfixes.so.0
libxshmfence.so.1
```

The remaining XCB extension libraries and development surfaces are not admitted by package membership.

### `termux-exec-glibc`

Decision:

```text
semantic authority:
    PLATFORM_INTEGRATION_PROVIDER

authority state:
    ACCEPTED_OPTIONAL_PLATFORM_PROVIDER

minimum runtime inclusion:
    NOT ACCEPTED
```

The exact `libtermux-exec.so` artifact is a valid Termux-specific exec interposer. However, the accepted graph contains zero selected/reference paths and zero direct consumers from this package. The promoted explicit-loader path has not demonstrated a unique need for it.

It remains outside the minimum runtime until a named child-exec transition fails without it.

### `glibc-runner`

Decision:

```text
semantic authority:
    TOOLCHAIN_ONLY

authority state:
    ACCEPTED_RESEARCH_ONLY_REJECT_RUNTIME
```

The package is a convenience shell/launcher with dependencies on `patchelf`, binutils, and strace. It can rewrite interpreter and RPATH and has no selected/reference object.

This is incompatible with treating it as the promoted runtime launcher under the accepted no-RPATH-patch contract. It remains optional research/build/maintenance tooling only.

## Generic and mixed object providers

### Base object authority

The following exact objects have base-profile pressure independent of conditional printing or Wayland profiles:

```text
libgcc_s.so.1       from gcc-libs-glibc
libexpat.so.1       from libexpat-glibc
```

`libgcc_s.so.1` is consumed directly by Obsidian application-local objects. `libexpat.so.1` is consumed directly by Obsidian and by the graphics provider.

The packages remain mixed:

```text
gcc-libs-glibc:
    base:        libgcc_s.so.1
    graphics:    libstdc++.so.6
    GTK compat:  libatomic.so.1
    excluded:    sanitizer, Fortran, OpenMP and other unselected runtimes

libexpat-glibc:
    runtime:     libexpat.so.1
    excluded:    xmlwf and development surface
```

### Graphics profile

The current Freedreno-facing object authority is accepted conditionally for:

```text
libstdc++.so.6       gcc-libs-glibc
libdrm.so.2          libdrm-glibc
libz.so.1            zlib-glibc
libzstd.so.1         zstd-glibc
selected X11/XCB graphics SONAMEs
```

The exact provider objects are accepted, but final profile inclusion remains tied to the selected graphics provider and its update contract.

`libdrm-glibc` backend libraries and tools are excluded unless a future provider demonstrates a direct need.

### GTK, font, device and Wayland compatibility

The following are accepted object providers only for a future declared GTK/font/device profile:

```text
libbrotlicommon.so.1
libbrotlidec.so.1
libblkid.so.1
libbz2.so.1.0
libatomic.so.1
libcap.so.2
libffi.so.8
libpcre2-8.so.0
```

Wayland objects are even narrower:

```text
libwayland-client.so.0
libwayland-cursor.so.0
libwayland-egl.so.1
```

They are not part of the X11-only minimum profile merely because a historical generic GTK provider loaded them.

`libwayland-server.so.0` and `wayland-scanner` are excluded from the current selected runtime scope.

### Printing profile

The following object closure is accepted only as a conditional printing capability:

```text
libcom_err.so.2
libgssapi_krb5.so.2
libk5crypto.so.3
libkrb5.so.3
libkrb5support.so.0
libgmp.so.10
libidn2.so.0
libunistring.so.5
plus already shared libffi/libz where required
```

Printing is not admitted into the base profile until its capability requirement and provider are explicitly accepted.

The whole `e2fsprogs-glibc` and `krb5-glibc` package surfaces are rejected as runtime authority.

## `libwayland-glibc` source lineage

Binary authority is accepted:

```text
artifact SHA-256:
    dedc307a6a818b028343e00eb8465a80e990f3d5ec93a37fc28f86f814673e49

live equivalence:
    PASS
```

Source-tree binding remains open:

```text
d0c7dcd812e720f00a781c0410af150fbfffdae0
    includes force-libm.patch
    2024-11-13

fb5924ca0b3f42a87d0d865e11a8aa9f6163e5a2
    omits force-libm.patch
    2025-03-10
```

The exact artifact timestamps strongly pressure the older tree, but no cryptographic publication/build record currently binds the artifact SHA to one tree. This does not block binary use under a locked artifact contract; it blocks claiming fully closed source lineage.

## Review cardinality

```text
priority package rows:
    28

selected/reference object rows:
    59

base-profile object rows:
    29

conditional-profile object rows:
    30

unresolved authority groups:
    8
```

Package dispositions:

```text
world authority:
    1

object-scoped platform providers:
    8

optional platform provider:
    1

research-only runtime rejection:
    1

object-scoped generic/mixed providers:
    16

binary authority accepted with source lineage open:
    1
```

## Remaining gates

Eight authority groups remain open:

```text
AUTH-001 world reconstruction/update/rollback
AUTH-002 termux-exec minimum-profile necessity
AUTH-003 GTK/font/device/Wayland provider composition
AUTH-004 printing capability and provider requirement
AUTH-005 graphics provider/update profile contract
AUTH-006 libwayland artifact-to-source-tree binding
AUTH-007 exact artifact member extraction/materialization contract
AUTH-008 fonts, pixbuf/icon/MIME and loader-state authority outside the 28 packages
```

These do not invalidate the accepted object authorities. They prevent a truthful unified successor manifest.

## Architecture decision

The provider-authority intervention has advanced from evidence collection to object-scoped decisions.

Accepted:

```text
Termux-adapted glibc is the native world authority.
Selected X11/XCB SONAMEs have object-scoped platform authority.
Exact selected generic-library objects have supply and semantic authority within named profiles.
glibc-runner is research-only and excluded from the promoted runtime.
termux-exec-glibc is optional platform integration, not proven minimum runtime.
Package-wide inclusion is rejected where only a subset is justified.
```

Not accepted:

```text
all 28 packages as one minimum runtime closure
all package members as generation content
historical GTK/printing/Wayland closure as base profile
successor materialization or activation
```

## Next valid state

```text
DEFINE_PROVIDER_PROFILES_AND_LOCKED_MEMBER_MANIFESTS
```

The next repository-side work is to convert accepted object authorities into explicit profile manifests:

```text
world substrate
base Obsidian X11 runtime
conditional Freedreno graphics
conditional GTK/font/device compatibility
conditional printing
research/build/maintenance
```

No device-side transaction is needed to draft those manifests. Materialization remains blocked until the open provider/profile gates are resolved.
