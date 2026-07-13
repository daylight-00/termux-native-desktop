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

world/locale/loader lifecycle boundary:
    PASS / CLEAN RECONSTRUCTION OPEN

application identity/launcher boundary:
    PASS / EXACT PAYLOAD AND SUPPLEMENT MEMBERSHIP OPEN

non-priority generic source-class boundary:
    PASS / EXACT OBJECT/SOURCE BINDING OPEN

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
docs/refactor/0137-selected-obsidian-world-internals-locale-and-loader-lifecycle-boundary.md
docs/refactor/0138-selected-obsidian-application-payload-launcher-and-supplement-authority-boundary.md
docs/refactor/0139-selected-obsidian-non-priority-generic-source-authority-boundary.md
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

## World, locale and loader lifecycle boundary

`../review/world-lifecycle-authority-boundary.tsv` defines the accepted non-materializing boundary:

```text
exact glibc artifact supply:
    current world reconstruction input, not a package-wide runtime manifest

world internals:
    NSS/gconv/runtime modules are demand-gated; no named module occurs in the 161-row selected/reference denominator

locale:
    twelve glibc-coupled members remain referenced world data, not application payload

ld.so.conf:
    composition-derived policy input; current live hash is evidence only

ld.so.cache:
    derived mutable state; never copied as authority
```

The boundary defines future update/rollback gates without authorizing loader mutation, composition, target population or clean reconstruction.

## Application payload, launcher and supplement boundary

`../review/application-authority-boundary.tsv` defines seven non-materializing application contracts:

```text
historical Obsidian 1.12.7 arm64 AppImage behavior:
    bounded runtime evidence; exact upstream artifact identity remains open

application-local identities:
    eleven accepted AppDir/$ORIGIN reference roles; not the payload aggregate

GUI and CLI launchers:
    exact current repository source blobs and SHA-256 accepted

public launcher publication:
    current checkout symlink implementation accepted; not target-layout policy

application supplements:
    identity class accepted; no member accepted merely from historical selection or fallback classification

application release transition:
    payload, launcher and supplement domains remain separate but require one compatible composition/rollback tuple
```

The boundary does not authorize payload acquisition, extraction, RPATH adaptation, supplement inclusion, target population or activation.

## Non-priority generic source-class boundary

`../review/generic-source-authority-boundary.tsv` records one global rule and six capability rows for the 61 non-priority generic identities.

```text
60 Debian-rootfs oracle identities:
    exact historical comparison anchors only

1 local graphics-experiment identity:
    bounded feature evidence only

shared generic provider:
    default review direction, not final authority

Termux/upstream/project/native-adapter source classes:
    admissible only with exact artifact/source/adaptation evidence

protected world, application-local or application supplement:
    no inheritance; explicit object-specific exception required
```

No non-priority row has exact clean-supply, final-provider, composition or target-population authority.

The 34-artifact/44-edge comparison set and its bounded member-inventory collector are now repository-defined. The collector may verify and inspect exact package archive streams, but its observations do not populate provider objects, fragments, composition or target layout.

## Global incompleteness

Provider fragments do not close:

```text
complete clean-world reconstruction, acquisition/retention and exact internals if named demand appears;
exact Obsidian/Electron upstream payload artifact identity and retained extraction/adaptation receipt;
named application supplement membership and source authority;
future launcher publication and atomic update/rollback;
exact object/source bindings for D-Bus, GLib/GIO, GTK, Pango/ATK and other generic providers;
exact NSS/security, audio and device candidates;
fonts, pixbuf modules/cache, icons and MIME data;
final graphics, GTK/Wayland, printing and optional-exec composition;
clean artifact acquisition and retention.
```

See the living issue ledger `../review/unresolved-authority-ledger.tsv` (`AUTH-001` through `AUTH-010`).

## Next valid state

```text
CLOSE_GLOBAL_WORLD_APPLICATION_GENERIC_AND_DATA_AUTHORITY_GAPS
```

Active repository task:

```text
RUN_BOUNDED_GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE_COLLECTOR
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
