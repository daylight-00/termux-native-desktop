# Selected Obsidian Provider Authority, Fragments and Target Schema

## Status

```text
exact artifact/member supply:
    STRONG PASS

bounded priority object evidence:
    PASS / 59-OBJECT SUBSET

global coverage normalization:
    PASS / 161 SEMANTIC IDENTITIES ACCOUNTED

canonical object and fragment semantics:
    PASS

artifact alias classification:
    PASS

final semantic provider authority:
    OPEN

deployable runtime profile:
    NOT REACHED

target-layout schema:
    PASS / SCHEMA ONLY

target row population:
    BLOCKED

extraction/materializer:
    BLOCKED
```

Current authority:

```text
docs/refactor/0135-selected-obsidian-provider-profile-lock-draft-architecture-audit.md
docs/refactor/0136-selected-obsidian-provider-authority-coverage-and-lock-semantics-normalization.md
```

The historical member locks remain exact bounded supply evidence. They are not complete profiles, target manifests, extraction inputs, or materialization authorization.

## Normalized architecture

```text
SupplyArtifact
    exact artifact/index identity, acquisition, retention and source-binding state

ProviderObjectAuthority
    canonical content identity and separated authority states

ProviderFragmentMembership
    capability/composition-pressure edges

ApplicationRuntimeComposition
    not yet defined

TargetLayout
    schema and invariants only
```

No lower layer silently authorizes the next layer.

## Current files

```text
supply-repository-metadata-registry.tsv
supply-artifact-registry.tsv

provider-object-registry.tsv
provider-object-registry/
    world-and-data.tsv
    x11-and-platform.tsv
    generic-a-l.tsv
    generic-m-z.tsv

provider-fragment-registry.tsv
provider-fragment-memberships.tsv

runtime-alias-authority.tsv
runtime-alias-authority/
    soname-runtime.tsv
    linker-development.tsv
    loader-and-internal.tsv

target-layout-schema.tsv
target-layout-invariants.md

provider-profile-definitions.tsv          # historical pre-normalization grouping
provider-profile-artifact-locks.tsv       # historical bounded artifact edges
member-locks/*.tsv                        # historical exact supply lock rows
```

Large canonical registries use root indexes plus SHA-256-locked partitions. The authoritative registry is the union of its indexed partitions.

## Canonical counts

```text
exact priority artifacts:
    28

canonical provider objects:
    60
        59 priority denominator objects
        1 optional non-denominator termux-exec object

reviewed priority fragment memberships:
    63

optional non-denominator memberships:
    1

total fragment content edges:
    64

canonical artifact aliases:
    84

historical fragment alias edges:
    92

historical lock rows:
    156
```

The earlier `63 content + 93 required aliases` interpretation is withdrawn. Correct historical accounting is `64 content edges + 92 artifact alias edges = 156 rows`.

## Supply registry semantics

A supply artifact row records:

```text
repository metadata identity;
package/version/architecture;
repository filename;
artifact size and SHA-256;
exact index match;
acquisition and retention state;
future availability state;
installed member equivalence;
recipe candidate set;
artifact-to-recipe binding state;
source archive binding state.
```

Exact artifact recognition is accepted. Clean acquisition is not closed until repository trust/key/signature policy, immutable retention or snapshot policy, future availability, source archive identity, and build attestation are defined.

## Provider-object semantics

Every object has separate fields for:

```text
semantic_role_state
termux_android_adaptation_state
candidate_source_comparison_state
exact_supply_artifact_state
artifact_to_recipe_binding_state
profile_necessity_state
provisional_final_provider_state
```

`exact_supply_artifact_state=ACCEPTED` does not force `provisional_final_provider_state=ACCEPTED_FINAL`.

### Current adaptation evidence

```text
glibc world objects:
    explicit Termux/Android adaptation proven

libxcb selected objects:
    Termux X11 socket-prefix patch proven
    final platform source remains provisional

libxshmfence selected object:
    Termux shared-memory directory policy proven
    final provider remains provisional

libX11/libXau/libXdmcp/libXext/libXrandr/libXrender:
    generic Termux repository builds
    no object-specific adaptation recorded

libcap.so.2:
    platform-or-generic provisional
    exact supply accepted
    selected-object adaptation effect unresolved
```

## Provider fragments

```text
world-core-provider-fragment
    six reviewed world-core ELF objects

glibc-locale-data-fragment
    twelve glibc-coupled en_US locale members

base-obsidian-x11-provider-fragment
    eleven reviewed passive-base provider objects

graphics-freedreno-provider-fragment
    eleven conditional graphics pressure objects

gtk-font-device-compat-provider-fragment
    twelve conditional GTK/font/device/Wayland memberships

printing-provider-fragment
    eleven conditional printing memberships

optional-termux-exec-provider-fragment
    one optional non-denominator object
```

Fragments express bounded pressure only. They do not establish install inheritance, full dependency closure, final inclusion, target ownership, activation scope, or rollback scope.

World core and glibc locale data remain separate fragments even though both come from the same exact glibc artifact.

### XCB base resolution

`libxcb-render.so.0` and `libxcb-shm.so.0` remain in the base fragment because passive evidence records mapped/direct base consumers. Graphics is secondary pressure only and creates no duplicate graphics membership.

## Alias authority

```text
SONAME_RUNTIME_ALIAS:
    40

LINKER_DEVELOPMENT_ALIAS:
    41

LOADER_OR_ENTRYPOINT_ALIAS:
    2

PACKAGE_INTERNAL_RELATIVE_ALIAS:
    1
```

Interpretation:

```text
SONAME runtime candidate:
    eligible only if the final externalized object/composition needs lookup by that SONAME

linker/development alias:
    excluded from runtime target; research/build profile only

loader/entrypoint alias:
    world entrypoint policy remains open

package-internal relative alias:
    runtime necessity unresolved
```

No alias currently has target inclusion authorization.

## Historical member-lock boundary

A historical `CONTENT` row proves exact supply-member identity and live equivalence. A historical `ALIAS` row proves an exact package symlink and literal target.

Neither defines:

```text
future target path;
target mode or owner;
final provider source;
application composition;
runtime alias necessity;
materialization authorization.
```

```text
artifact_member_path:
    immutable supply identity

installed_source_path:
    historical evidence path

artifact mode/uid/gid:
    supply metadata

future target policy:
    independently governed and unpopulated
```

## Target-layout schema

The schema contains twenty required/conditional fields for:

```text
composition and authority references;
supply references;
target domain and relative path;
node, mode, owner and mutability policy;
alias and collision policy;
update and rollback domains;
validation gates;
authority issues and acceptance;
population state.
```

Current invariant:

```text
population_state:
    UNPOPULATED_SCHEMA_ONLY
```

No target rows, extraction paths, mode decisions, ownership decisions, collision resolutions, or materializer steps may be added in the current state.

## Global incompleteness

Provider fragments do not close:

```text
world NSS/gconv/runtime internals;
locale policy and loader-state lifecycle;
Obsidian/Electron payload identity;
launcher supply identity;
application supplement identities;
D-Bus, GLib/GIO, GTK, Pango/ATK and other generic providers;
NSS/security and audio providers;
fonts, pixbuf modules/cache, icons and MIME data;
final graphics, GTK/Wayland, printing and optional-exec composition;
clean artifact acquisition and retention.
```

See the living issue ledger `../review/unresolved-authority-ledger.tsv` (`AUTH-001` through `AUTH-010`).

## Next valid state

```text
CLOSE_GLOBAL_WORLD_APPLICATION_GENERIC_AND_DATA_AUTHORITY_GAPS
```

Only after authority closure may the repository define an `ApplicationRuntimeComposition`. Only after composition acceptance may target rows be populated. An intervention-lift audit is required before extraction or materializer implementation.

## Stop line

Do not:

```text
consume fragments or historical member locks as extraction manifests;
call any fragment a deployable runtime profile;
populate target paths, modes, owners or aliases;
copy linker/development aliases into runtime;
treat artifact metadata as target policy;
treat Termux supply as automatic final source authority;
duplicate shared objects or artifacts by fragment;
write extraction or materializer code;
materialize or activate a successor;
mutate packages, current, launcher, loader state or RPATH.
```
