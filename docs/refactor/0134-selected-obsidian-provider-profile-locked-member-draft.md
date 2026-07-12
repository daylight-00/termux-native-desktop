# 0134 — Selected Obsidian Provider Profile and Locked-Member Draft

## Status

```text
priority provider-authority review:
    PARTIAL PASS

profile definition draft:
    PASS

exact artifact-member assignment:
    PASS

materialization authorization:
    NO

successor generation/current activation:
    BLOCKED
```

## Purpose

`0133` rejected package-wide runtime authority and accepted object-scoped provider decisions for all 59 priority selected/reference objects. This step converts those decisions into profile-shaped exact artifact-member locks without copying, installing, extracting, launching, materializing, or activating anything.

The draft answers:

```text
which reviewed object belongs to which named profile;
which exact indexed artifact supplies it;
which exact data-archive member contains the content;
which package-provided aliases belong with that content;
which authority and update domain govern the object;
which remaining gates prevent materialization.
```

It does not answer the final target layout, complete world reconstruction, complete application composition, or activation contract.

## Outputs

```text
experiments/glibc/selected-obsidian-provider-authority/profiles/
    README.md
    provider-profile-definitions.tsv
    provider-profile-artifact-locks.tsv

    member-locks/
        world-substrate-selected.tsv
        base-obsidian-x11-provider.tsv
        graphics-freedreno-provider.tsv
        gtk-font-device-compat-provider.tsv
        printing-provider.tsv
        optional-termux-exec-provider.tsv
```

## Validation result

```text
reviewed selected/reference objects:
    59 unique

profile content memberships:
    63

required exact-artifact alias rows:
    93

locked rows:
    156

profile/package artifact locks:
    35

profiles:
    6

missing reviewed objects:
    0

artifact-member identity mismatches:
    0
```

Four additional content memberships arise because accepted shared objects belong to more than one conditional profile. The source selected-object identity remains unique.

## Profiles

### Selected world substrate

```text
profile:
    world-substrate-selected

content rows:
    18

alias rows:
    3

artifact locks:
    1
```

This locks the reviewed glibc loader/core libraries and selected locale members. It is not the full glibc world manifest.

### Base Obsidian X11 providers

```text
profile:
    base-obsidian-x11-provider

content rows:
    11

alias rows:
    20

artifact locks:
    9
```

This locks the reviewed non-world provider objects used by the base X11 Obsidian graph: X11/XCB core objects, `libgcc_s.so.1`, and `libexpat.so.1`.

It does not include the application-local generation, GTK data, fonts, pixbuf/icons/MIME, or an optional graphics overlay.

### Freedreno graphics overlay

```text
profile:
    graphics-freedreno-provider

content rows:
    11

alias rows:
    22

artifact locks:
    7
```

This is an incremental conditional provider overlay. It locks the reviewed X11/XCB graphics extension objects, `libstdc++.so.6`, `libdrm.so.2`, `libz.so.1`, and `libzstd.so.1`.

It excludes package-wide `libdrm` tools/backends and all unselected XCB extensions.

### GTK/font/device compatibility overlay

```text
profile:
    gtk-font-device-compat-provider

content rows:
    12

alias rows:
    25

artifact locks:
    9
```

This locks reviewed generic/device/Wayland objects but does not choose a final GTK, font, pixbuf, icon, MIME, or device provider.

Wayland objects remain conditional and are not part of the X11 base.

### Printing overlay

```text
profile:
    printing-provider

content rows:
    11

alias rows:
    22

artifact locks:
    8
```

This locks the reviewed printing dependency objects while printing capability and its actual service/provider remain unaccepted.

### Optional Termux exec integration

```text
profile:
    optional-termux-exec-provider

content rows:
    1

alias rows:
    0

artifact locks:
    1
```

`libtermux-exec.so` is locked as an optional platform object. The profile is not inherited by the default base runtime and remains blocked by the unique-necessity test in `AUTH-002`.

## Supply identity

Each content lock binds:

```text
package and installed version
exact repository artifact SHA-256
exact .deb data member path
member content SHA-256
member mode and size
selected evidence identity
semantic/provider authority state
source recipe state
update domain
```

Each alias lock binds the exact package-provided symlink member and literal link target.

This replaces future dependence on mutable installed source paths for the reviewed object set.

## Path and ownership boundary

The draft intentionally contains both:

```text
artifact_member_path
installed_source_path
```

Their meanings are different.

```text
artifact_member_path:
    immutable supply identity inside an accepted exact artifact

installed_source_path:
    evidence path that proved the artifact member equals the current installed bytes
```

Neither field defines the future target path.

A future extraction/target contract must explicitly choose whether an object belongs to:

```text
world substrate
external shared provider
application-local provider
application domain supplement
data capability
research/build/maintenance profile
```

The current absolute `$PREFIX/glibc` path cannot become target authority by copying it into a manifest.

## Materialization stop

Every member row states:

```text
materialization_state:
    DRAFT_LOCK_ONLY_BLOCKED
```

Every profile states:

```text
materialization_authorized:
    NO
```

No extraction command, staging tree, generation directory, current pointer, launcher mutation, or package operation is introduced.

## Remaining incompleteness

### World gap

The reviewed world selected set does not close:

```text
required NSS and gconv modules
runtime-internal glibc data
locale policy
ld.so.conf and ld.so.cache lifecycle
clean reconstruction, update, and rollback
2.42 -> 2.43 transition
```

### Application/base gap

The provider base does not close:

```text
96 application-local generation identities
application payload/launcher supply identity
D-Bus and other external capability ownership
fonts
pixbuf modules/cache
icons and MIME data
final graphics overlay inclusion
```

### Conditional-profile gap

The exact members are locked, but policy remains open for:

```text
GTK/font/device/Wayland composition
printing capability and provider
optional termux-exec integration
graphics provider/update contract
libwayland source-tree binding
```

## Accepted claims

This step establishes:

```text
all 59 reviewed selected/reference objects are assigned to explicit provider profiles;
every assignment resolves to an exact accepted artifact member;
required package-provided aliases are locked explicitly;
shared conditional objects may belong to multiple profiles without duplicating source authority;
package artifact identity is separated from member runtime authority;
installed absolute paths are evidence, not target authority.
```

It does not establish:

```text
a complete clean runtime;
a complete world installation;
a successor generation manifest;
a final target layout;
a package installation plan;
activation or rollback readiness.
```

## Next valid state

```text
CLOSE_BASE_PROVIDER_PROFILE_GAPS_AND_DEFINE_EXTRACTION_TARGET_CONTRACT
```

The next repository-side work must:

```text
define target-domain and target-path rules independent of installed paths;
close world runtime-internal and loader-state ownership;
incorporate application-local content/provenance/composition identity;
resolve fonts and pixbuf/icon/MIME authority;
make explicit inclusion decisions for graphics, GTK/Wayland, printing, and optional exec profiles;
define extraction verification without package installation or maintainer scripts.
```

Materialization remains blocked until those gaps are closed enough to produce a truthful composition contract.
