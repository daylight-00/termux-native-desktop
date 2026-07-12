# Selected Obsidian Provider Profiles and Locked Members

## Status

```text
priority provider-authority review:
    PARTIAL PASS

reviewed selected/reference objects:
    59 / 59

profile content memberships:
    63

required alias rows:
    93

locked member rows:
    156

profile/package artifact locks:
    35

materialization authorized:
    NO
```

These files convert the accepted object-scoped authority decisions into profile-shaped, exact artifact-member locks. They are not a complete runtime manifest, installation plan, successor generation, or activation authorization.

## Files

```text
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

## Profile definitions

```text
world-substrate-selected
    selected glibc world objects and locale data only

base-obsidian-x11-provider
    reviewed non-world providers required by the base Obsidian X11 graph

graphics-freedreno-provider
    incremental conditional provider objects for the accepted Freedreno path

gtk-font-device-compat-provider
    conditional GTK/font/device/Wayland compatibility objects

printing-provider
    conditional printing dependency objects

optional-termux-exec-provider
    optional Termux exec interposer object
```

Parent profiles express logical composition pressure. They do not authorize copying, merging, installation, activation, or mutation.

## Cardinality

```text
profile                              content  aliases  artifact locks
world-substrate-selected                  18        3               1
base-obsidian-x11-provider                11       20               9
graphics-freedreno-provider               11       22               7
gtk-font-device-compat-provider           12       25               9
printing-provider                         11       22               8
optional-termux-exec-provider              1        0               1

unique reviewed objects                   59
profile content memberships               63
alias memberships                         93
total member-lock rows                   156
```

The content-membership total exceeds 59 because shared objects such as `libcap.so.2`, `libffi.so.8`, and `libz.so.1` belong to more than one conditional capability profile.

## Member-lock semantics

### `CONTENT`

A `CONTENT` row locks one exact regular-file member from an accepted indexed `.deb` artifact.

Required identity:

```text
package + version
artifact SHA-256
artifact member path
member mode and size
member content SHA-256
selected evidence row
semantic/provider authority state
source recipe state
update domain
```

### `ALIAS`

An `ALIAS` row records a package-provided symlink that resolves to a reviewed content member.

Aliases are not inferred from SONAME alone. They are copied from the exact accepted artifact inventory and retain their literal link target.

## Path boundary

```text
artifact_member_path:
    authoritative path inside the exact .deb data archive

installed_source_path:
    historical live evidence path used to establish byte equivalence

future target path:
    not yet defined
```

`installed_source_path` must never become successor target authority by path copying. A future extraction/target contract must map accepted artifact members into explicitly owned world/provider/application domains.

## Artifact locks

`provider-profile-artifact-locks.tsv` records the exact indexed artifact required to supply each profile's members.

An artifact lock means:

```text
this exact package artifact can supply accepted members
```

It does not mean:

```text
the entire package is runtime content
the package may be installed
maintainer scripts may run
all data members may be copied
the artifact owns the target layout
```

## Profile status

All profile rows use:

```text
materialization_state:
    DRAFT_LOCK_ONLY_BLOCKED
```

All profile definitions use:

```text
materialization_authorized:
    NO
```

The draft can be reviewed, hashed, diffed, and used to design a future transaction. It cannot be consumed by a materializer yet.

## Known incompleteness

### World

`world-substrate-selected` is a selected-object lock, not the complete glibc world reconstruction contract. It does not yet close:

```text
required NSS/gconv/runtime-internal modules
C.UTF-8 versus en_US.UTF-8 policy
ld.so.conf and ld.so.cache lifecycle ownership
clean world installation/update/rollback
2.42 -> 2.43 revalidation
```

### Base Obsidian X11

`base-obsidian-x11-provider` does not yet include:

```text
96 application-local generation identities
application payload and launcher identity
fonts
pixbuf modules and cache
icons and MIME data
D-Bus and other declared external capabilities
final graphics overlay choice
```

### Conditional profiles

GTK/font/device, printing, Wayland, and optional exec remain policy choices. Their exact members are locked so the choices can be made without reverting to package-wide inference.

## Blocking authority issues

```text
AUTH-001 world reconstruction/update/rollback
AUTH-002 termux-exec minimum-profile necessity
AUTH-003 GTK/font/device/Wayland provider composition
AUTH-004 printing capability/provider requirement
AUTH-005 graphics provider/update contract
AUTH-006 libwayland source-tree binding
AUTH-007 extraction and target-layout contract
AUTH-008 fonts, pixbuf/icons/MIME and loader-state authority
```

See:

```text
../review/unresolved-authority-ledger.tsv
```

## Next valid work

```text
CLOSE_BASE_PROVIDER_PROFILE_GAPS_AND_DEFINE_EXTRACTION_TARGET_CONTRACT
```

The next work is repository-side design and analysis. It must define target ownership independently from installed absolute paths and close the missing world, application-local, data-capability, and conditional-profile decisions before any materialization transaction is authored.
