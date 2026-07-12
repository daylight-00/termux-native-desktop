# Selected Obsidian Provider Fragments and Locked Members

## Status

```text
priority provider evidence:
    PASS / BOUNDED 59-OBJECT SUBSET

exact artifact/member supply locks:
    PASS

package-wide runtime rejection:
    PASS

provider semantic authority:
    PARTIAL / CORRECTION REQUIRED

provider fragment draft:
    PASS / NON-MATERIALIZING

global authority coverage:
    OPEN

target-layout schema:
    ALLOWED TO DESIGN

target-layout population and materialization:
    BLOCKED
```

These files lock exact supply members and describe provider-fragment pressure. They are not complete runtime profiles, an installation plan, a successor generation, or activation authorization.

Current audit authority:

```text
docs/refactor/0135-selected-obsidian-provider-profile-lock-draft-architecture-audit.md
```

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

Structured audit findings:

```text
../review/post-0134-architecture-audit-findings.tsv
```

## Cardinality

```text
unique reviewed objects:
    59

provider-fragment content memberships:
    63

artifact alias rows:
    93

locked member rows:
    156

profile/package artifact edges:
    35

provider fragments:
    6
```

The 59-object denominator is the bounded priority subset, not the complete selected/reference/application-domain authority set.

Shared objects such as `libcap.so.2`, `libffi.so.8`, and `libz.so.1` can have multiple fragment memberships while retaining one canonical content and supply authority identity.

## Provider fragments

The existing identifiers are retained for continuity, but they are provider fragments rather than deployable profiles.

```text
world-substrate-selected
    reviewed glibc world-core objects plus glibc-coupled locale data

base-obsidian-x11-provider
    reviewed non-world members with passive/base X11 pressure

graphics-freedreno-provider
    reviewed conditional Freedreno provider members

gtk-font-device-compat-provider
    reviewed conditional compatibility members; not a final GTK/font/device provider

printing-provider
    reviewed conditional printing dependency members; not a complete printing provider

optional-termux-exec-provider
    exact optional interposer member; not inherited by default
```

`parent_profiles` expresses logical pressure only. It does not establish installation inheritance, complete dependencies, target layout, activation scope, or rollback scope.

## Member-lock semantics

### `CONTENT`

A `CONTENT` row proves one exact regular-file member in an accepted exact `.deb` artifact.

It locks:

```text
package and version;
artifact SHA-256;
artifact member path;
artifact member mode and size;
member content SHA-256;
selected evidence identity;
current semantic/provider decision state;
source-recipe evidence state;
update domain.
```

It does not define:

```text
future target path;
target mode or ownership;
final semantic source choice;
runtime necessity outside the named fragment;
materialization authorization.
```

### `ALIAS`

An `ALIAS` row records an exact package-provided symlink member and literal target.

It is artifact supply evidence, not automatic runtime inclusion.

Current alias rows include both SONAME aliases and unversioned names such as:

```text
libX11.so
libexpat.so
libstdc++.so
libdrm.so
```

Before target population every alias must be classified as:

```text
SONAME_RUNTIME_ALIAS
PROVEN_DLOPEN_RUNTIME_ALIAS
LOADER_OR_ENTRYPOINT_ALIAS
LINKER_DEVELOPMENT_ALIAS
PACKAGE_INTERNAL_RELATIVE_ALIAS
UNRESOLVED_ALIAS
```

Only runtime-authorized aliases may enter a runtime target. Until classification, use the term `artifact alias rows`, not `required aliases`.

## Path and mode boundary

```text
artifact_member_path:
    immutable supply identity inside the exact .deb archive

installed_source_path:
    historical evidence path used for live equivalence

artifact member mode:
    exact supply metadata

future target path/mode/owner:
    unresolved and independently owned
```

Neither installed paths nor artifact modes become target policy by copying them into a manifest.

A target-layout schema must define:

```text
target_domain;
target_relative_path;
target_node_type;
target_mode_policy;
target_owner_policy;
target_mutability;
target_alias_class;
target_collision_policy.
```

## Supply authority boundary

`provider-profile-artifact-locks.tsv` proves that one exact artifact can supply accepted members.

It does not prove:

```text
the entire package is runtime content;
the package may be installed;
maintainer scripts may run;
the artifact is the final source for every generic capability;
the artifact is cryptographically bound to one source recipe tree;
the artifact owns target layout.
```

Future clean reconstruction also needs an acquisition/retention and trust contract for the exact artifact.

## Required normalized registries

The next repository-side normalization should create:

```text
supply-artifact-registry.tsv
    one row per exact artifact identity

provider-object-registry.tsv
    one row per canonical content/provider object identity

provider-fragment-memberships.tsv
    many-to-many object-to-fragment pressure edges

runtime-alias-authority.tsv
    alias class and runtime evidence

authority-coverage-ledger.tsv
    complete denominator and issue mapping

target-layout-schema.tsv
    schema/invariants only; no populated target rows yet
```

Do not extract the current per-fragment rows directly.

## Known incompleteness

### Global coverage

The current locks cover 59 priority selected/reference objects only. They do not complete the authority matrix for:

```text
all 96 first-generation content identities;
11 app-local reference identities;
application payload and launcher supply identity;
D-Bus and other non-priority generic providers;
font, pixbuf, icon and MIME data;
complete world internals and loader state.
```

The 96 first-generation content identities are not application-local identities.

### World

`world-substrate-selected` is not a full world reconstruction contract. It omits or leaves open:

```text
required NSS/gconv/runtime-internal modules;
C.UTF-8 versus en_US.UTF-8 policy;
ld.so.conf and ld.so.cache ownership;
clean world installation/update/rollback;
2.42 -> 2.43 revalidation.
```

World-core ELF and glibc-coupled locale data share an artifact but remain separate semantic/target domains.

### Platform versus generic classification

Exact Termux artifact supply is accepted for reviewed objects. Final `PLATFORM_INTEGRATION_PROVIDER` classification requires explicit adaptation or host-integration evidence.

X11/XCB and `libcap.so.2` classifications remain subject to the `0135` audit corrections where such evidence is not yet recorded.

### Application and capabilities

Still open:

```text
application payload/$ORIGIN composition;
D-Bus, GTK/GLib/GIO/Pango/ATK and other generic provider authority;
fonts and fontconfig/cache authority;
pixbuf modules/cache and icon/MIME authority;
final graphics overlay choice;
GTK/Wayland, printing and optional exec policy.
```

## Blocking authority issues

```text
AUTH-001 world reconstruction/update/rollback
AUTH-002 termux-exec minimum-profile necessity
AUTH-003 GTK/font/device/Wayland provider composition
AUTH-004 printing capability/provider requirement
AUTH-005 graphics provider/update contract
AUTH-006 libwayland source-tree binding
AUTH-007 supply split, alias and target-layout schema
AUTH-008 non-priority data and loader-state authority
AUTH-009 non-priority generic capability authority
```

## Revised next valid state

```text
NORMALIZE_PROVIDER_AUTHORITY_COVERAGE_AND_LOCK_SEMANTICS
```

Order:

```text
1. correct global coverage and terminology;
2. split supply, adaptation, semantic authority, necessity and final-source states;
3. classify aliases;
4. deduplicate canonical artifact/object registries;
5. resolve base-fragment narrative ambiguity;
6. define target-layout schema/invariants only;
7. close world, application, generic and data authority;
8. populate target rows only after ownership decisions;
9. perform intervention-lift audit before a materializer.
```

## Stop line

Do not:

```text
consume these fragments as extraction manifests;
treat 59/59 as complete global authority coverage;
call artifact aliases runtime-required without classification;
preserve package modes as target modes automatically;
treat Termux package origin as automatic platform semantic authority;
call the 96 first-generation contents application-local;
duplicate shared objects or artifacts per fragment;
populate target paths before authority ownership closes;
install packages or run maintainer scripts;
materialize a successor;
create or change current;
mutate loader state or patch RPATH;
reopen closed graphics gates.
```
