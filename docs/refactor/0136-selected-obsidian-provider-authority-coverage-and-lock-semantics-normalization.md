# 0136 — Selected Obsidian Provider-Authority Coverage and Lock-Semantics Normalization

## Status

```text
post-0134 audit corrections:
    ADOPTED

global identity denominator normalization:
    PASS

priority exact supply locks:
    PRESERVED

canonical artifact/object/fragment registries:
    PASS

artifact alias classification:
    PASS

target-layout schema and invariants:
    PASS / SCHEMA ONLY

final semantic provider authority:
    OPEN

target row population:
    BLOCKED

extraction/materializer design:
    BLOCKED
```

## Purpose

`0135` established that the exact `.deb` and member locks were strong bounded supply evidence but were not deployable provider profiles. This transaction implements the allowed normalization steps P0-P6 without populating any future target path.

It preserves all accepted artifact/member hashes while separating:

```text
supply artifact identity;
canonical provider-object identity;
provider-fragment pressure;
semantic role;
Termux/Android adaptation evidence;
candidate-source comparison;
artifact-to-recipe binding;
profile necessity;
provisional final-provider state;
runtime alias authority;
future target policy.
```

No package, runtime, device, generation, launcher, loader, or activation transaction was performed.

## Outputs

```text
review/
    authority-coverage-ledger.tsv
    authority-coverage-ledger/*.tsv
    non-priority-generic-authority-ledger.tsv
    non-priority-generic-authority-ledger/*.tsv
    normalization-codebook.tsv
    unresolved-authority-ledger.tsv

profiles/
    supply-repository-metadata-registry.tsv
    supply-artifact-registry.tsv
    provider-object-registry.tsv
    provider-object-registry/*.tsv
    provider-fragment-registry.tsv
    provider-fragment-memberships.tsv
    runtime-alias-authority.tsv
    runtime-alias-authority/*.tsv
    target-layout-schema.tsv
    target-layout-invariants.md
```

Large canonical registries use a root index plus content-hash-locked partitions. The authoritative set is the union of the indexed partitions; the root index records partition path, row count, SHA-256, and identity column. Remote Git blob identities were independently compared with the locally generated blobs before acceptance.

The pre-normalization `profiles/member-locks/*.tsv` files remain historical bounded supply ledgers. They are not materializer inputs.

## Global coverage denominator

The normalized coverage ledger preserves the actual identity sets instead of treating the bounded 59-object review as global completion.

```text
semantic-object denominator rows:
    161

ELF semantic objects:
    113

first-generation content identities:
    96

first-generation selected ELF:
    91

first-generation fonts:
    4

first-generation generated schema aggregate:
    1

application-local reference identities:
    11

protected-world references:
    18
```

The coverage ledger also records three application identity requirements that are not rows in the 161 semantic-object denominator:

```text
APPLICATION_PAYLOAD_IDENTITY
APPLICATION_LAUNCHER_SUPPLY_IDENTITY
APPLICATION_DOMAIN_SUPPLEMENT_IDENTITIES
```

Each denominator row resolves to a bounded authority record, explicit exclusion/reference class, data/world/application class, mutable/cache exclusion, or one or more living authority issues. This is complete coverage accounting, not authority closure.

## Corrected identity terminology

```text
FIRST_GENERATION_CONTENT_IDENTITIES:
    96 = 91 selected external ELF + 4 fonts + 1 generated schema aggregate

APPLICATION_LOCAL_REFERENCE_IDENTITIES:
    11 retained AppDir/$ORIGIN reference identities

APPLICATION_PAYLOAD_IDENTITY:
    upstream Obsidian/Electron payload identity; open

APPLICATION_LAUNCHER_SUPPLY_IDENTITY:
    entrypoint/launcher source and update identity; open

APPLICATION_DOMAIN_SUPPLEMENT_IDENTITIES:
    bounded application-family supplements; open
```

The 96 first-generation contents are not application-local payload.

## Canonical supply registry

```text
exact priority supply artifacts:
    28
```

Each artifact records exact repository filename, size, SHA-256, captured Packages/InRelease identity, acquisition/retention/future-availability state, installed-member equivalence, recipe candidates, artifact-to-recipe binding, and source-archive binding.

All exact artifact/member recognition claims remain accepted. Clean acquisition remains open because repository signature-key policy, immutable retention/snapshot policy, future availability, source-archive binding, and build attestation are incomplete.

## Canonical provider-object registry

```text
priority denominator objects:
    59

optional non-denominator objects:
    1 (libtermux-exec.so)

canonical provider-object rows:
    60
```

Every object has independent states for:

```text
semantic_role_state
termux_android_adaptation_state
candidate_source_comparison_state
exact_supply_artifact_state
artifact_to_recipe_binding_state
profile_necessity_state
provisional_final_provider_state
```

Exact supply remains accepted while generic/final provider choice is conservative.

### X11/XCB adaptation correction

```text
libxcb selected objects:
    adaptation proven by the Termux X11 socket-prefix patch
    final platform provider still provisional pending candidate comparison

libxshmfence selected object:
    adaptation proven by the Termux shared-memory directory policy
    final provider still provisional

libX11, libXau, libXdmcp, libXext, libXrandr, libXrender:
    generic builds supplied from the Termux repository
    no selected-object-specific adaptation recorded
    platform-versus-generic role provisional
```

A Termux-built artifact is not automatic platform semantic authority.

### `libcap.so.2` correction

```text
semantic role:
    PLATFORM_OR_GENERIC

Termux/Android adaptation:
    UNRESOLVED_SELECTED_OBJECT_EFFECT

exact artifact/member supply:
    ACCEPTED

necessity:
    CONDITIONAL

final provider:
    PROVISIONAL
```

## Provider fragments

Seven canonical fragments replace deployable-profile language:

```text
world-core-provider-fragment
glibc-locale-data-fragment
base-obsidian-x11-provider-fragment
graphics-freedreno-provider-fragment
gtk-font-device-compat-provider-fragment
printing-provider-fragment
optional-termux-exec-provider-fragment
```

World core and glibc-coupled locale data use one supply artifact but remain separate semantic and lifecycle fragments.

Correct cardinality:

```text
reviewed priority objects:
    59

reviewed priority fragment memberships:
    63

optional non-denominator memberships:
    1

total content edges:
    64
```

Fragment edges are capability/composition pressure, not target inclusion or installation inheritance.

## XCB base boundary resolution

`libxcb-render.so.0` and `libxcb-shm.so.0` remain in the base X11 fragment because accepted passive evidence records mapped/direct base consumers.

```text
libxcb-render.so.0:
    direct consumers 1
    mapped selected object

libxcb-shm.so.0:
    direct consumers 2
    mapped selected object
```

Graphics is retained as secondary narrative pressure only; no duplicate graphics-fragment membership is created.

## Alias authority

Legacy locks contain 92 fragment alias edges. Canonical deduplication produces:

```text
canonical artifact alias rows:
    84

SONAME_RUNTIME_ALIAS:
    40

LINKER_DEVELOPMENT_ALIAS:
    41

LOADER_OR_ENTRYPOINT_ALIAS:
    2

PACKAGE_INTERNAL_RELATIVE_ALIAS:
    1
```

The prior statement `93 required aliases` is withdrawn. Exact legacy accounting is:

```text
64 content edges + 92 alias edges = 156 lock rows
```

No alias is automatically accepted into a target. Linker/development aliases are excluded from runtime composition; runtime-capable aliases still require final object authority and an accepted application composition.

## Non-priority generic authority

```text
non-priority selected/reference provider identities:
    61
```

These cover D-Bus, GLib/GIO, GTK, Pango/ATK, fontconfig/freetype/harfbuzz, NSS/security, audio, printing, graphics, device integration, and other providers outside the 28-package transaction.

Every identity is mapped to `AUTH-009` or a more specific graphics/printing issue. Debian rootfs, local experiment, and other observed bytes remain oracle evidence only; none is accepted as final provider authority.

## Target-layout schema

The schema defines twenty fields covering composition/authority references, supply references, target domain/path/node policy, mode/owner/mutability policy, alias and collision policy, update/rollback domains, validation gates, authority issues, and population state.

The only permitted state is:

```text
population_state:
    UNPOPULATED_SCHEMA_ONLY
```

No target row is populated. Artifact path/mode/uid/gid and historical installed path remain evidence only.

## Living authority issues

```text
AUTH-001 world reconstruction and lifecycle
AUTH-002 optional Termux exec necessity
AUTH-003 GTK/GLib/font/device/Wayland provider composition
AUTH-004 printing capability/provider
AUTH-005 graphics/X11/XCB provider composition
AUTH-006 libwayland artifact-to-recipe binding
AUTH-007 supply/alias/target contract population
AUTH-008 data capabilities and loader state
AUTH-009 non-priority generic capabilities
AUTH-010 application payload/launcher/supplement authority
```

No issue is closed merely by normalization.

## Accepted claims

```text
all 161 semantic identities are coverage-accounted;
the 96 first-generation identities are correctly named and split;
the 28 priority artifacts are canonical supply records;
the 59 bounded reviewed objects plus optional exec are canonical object records;
reviewed fragment membership is separated from object authority;
world core and locale data are separate fragments;
X11/XCB and libcap semantic finality is conservatively represented;
artifact aliases are classified and deduplicated;
non-priority provider identities are connected to authority issues;
target-layout schema/invariants exist without target population.
```

## Claims not accepted

```text
global semantic provider-authority closure;
complete application runtime composition;
final generic provider selection;
clean artifact reacquisition;
complete world reconstruction;
font/pixbuf/icon/MIME authority;
final conditional-fragment inclusion;
populated target layout;
extraction/materializer readiness;
successor materialization or activation.
```

## Next valid state

```text
CLOSE_GLOBAL_WORLD_APPLICATION_GENERIC_AND_DATA_AUTHORITY_GAPS
```

The next work remains repository-side authority analysis. It must close or explicitly exclude world internals, application payload/launcher/supplements, non-priority generic providers, fonts, pixbuf/icons/MIME, loader state, and conditional capability choices before any `ApplicationRuntimeComposition` or target-layout row is populated.

## Stop line

Do not:

```text
consume provider fragments as deployable profiles;
use historical member-lock files as extraction input;
populate target paths, target modes or ownership;
copy linker/development aliases into a runtime target;
treat artifact path/mode/uid/gid as target policy;
treat exact Termux supply as final generic provider authority;
duplicate shared objects or artifacts by fragment;
install or mutate packages;
write an extraction/materializer script;
materialize a successor;
create or change current;
modify the promoted launcher or loader state;
patch RPATH;
run a device workload.
```
