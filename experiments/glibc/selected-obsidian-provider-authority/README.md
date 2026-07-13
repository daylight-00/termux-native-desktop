# Selected Obsidian Provider-Authority Census

## Status

```text
N0_REPOSITORY_ONBOARDING_PASS
N1_CENSUS_SCHEMA_AND_EVIDENCE_PLAN_PASS
N2_READ_ONLY_PROVIDER_EVIDENCE_PASS
N3_CORRECTED_NORMALIZED_CLASSIFICATION_PASS
N3_SOURCE_RECIPE_EVIDENCE_PASS
N3_BINARY_ARTIFACT_COMPARISON_PASS
PRIORITY_PROVIDER_EVIDENCE_PASS_BOUNDED
EXACT_ARTIFACT_MEMBER_SUPPLY_STRONG_PASS
PACKAGE_WIDE_RUNTIME_REJECTION_PASS
POST_0134_ARCHITECTURE_AUDIT_ADOPTED
PROVIDER_AUTHORITY_COVERAGE_NORMALIZATION_PASS
LOCK_SEMANTICS_NORMALIZATION_PASS
TARGET_LAYOUT_SCHEMA_ONLY_PASS
WORLD_LOCALE_LOADER_LIFECYCLE_BOUNDARY_PASS
APPLICATION_PAYLOAD_LAUNCHER_SUPPLEMENT_BOUNDARY_PASS_BOUNDED
NON_PRIORITY_GENERIC_SOURCE_CLASS_BOUNDARY_PASS_BOUNDED
GENERIC_EXACT_CANDIDATE_COLLECTOR_READY
GENERIC_EXACT_CANDIDATE_RECEIPT_REVIEW_PASS_BOUNDED
GENERIC_ARTIFACT_MEMBER_COMPARISON_SET_DEFINED_BOUNDED
GENERIC_ARTIFACT_MEMBER_INVENTORY_COLLECTOR_READY
SEMANTIC_FINAL_PROVIDER_AUTHORITY_OPEN
APPLICATION_RUNTIME_COMPOSITION_NOT_REACHED
TARGET_LAYOUT_POPULATION_BLOCKED
EXTRACTION_MATERIALIZER_BLOCKED
SUCCESSOR_MATERIALIZATION_BLOCKED
CURRENT_ACTIVATION_BLOCKED
```

This workstream implements the provider-authority intervention controlled by `docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md`.

Current correction and normalization authority:

```text
docs/refactor/0135-selected-obsidian-provider-profile-lock-draft-architecture-audit.md
docs/refactor/0136-selected-obsidian-provider-authority-coverage-and-lock-semantics-normalization.md
docs/refactor/0137-selected-obsidian-world-internals-locale-and-loader-lifecycle-boundary.md
docs/refactor/0138-selected-obsidian-application-payload-launcher-and-supplement-authority-boundary.md
docs/refactor/0139-selected-obsidian-non-priority-generic-source-authority-boundary.md
docs/refactor/0140-selected-obsidian-non-priority-generic-exact-candidate-evidence-collector.md
docs/refactor/0141-selected-obsidian-non-priority-generic-exact-candidate-receipt-review.md
docs/refactor/0142-selected-obsidian-non-priority-generic-artifact-member-comparison-set.md
docs/refactor/0143-selected-obsidian-non-priority-generic-artifact-member-inventory-collector.md
```


Generic exact-candidate receipt review:

```text
receipt archive SHA-256:
    361d2105c57c6ce3f446de16aedd966a55593fbba4e77d8a40e92b857ca02ea7

review identities:
    61

direct apt + pinned-recipe family candidates:
    37

indirect token-only rows:
    13

no retained candidate rows:
    11

authority decisions accepted:
    0
```

Family-name matches rank later artifact/member comparison candidates only. They do not establish object membership, adaptation, necessity, final provider authority or target population.

Named artifact/member comparison set:

```text
direct identities:
    37

exact artifacts in download/member-inventory scope:
    34

named identity-to-artifact edges:
    44

compressed byte ceiling:
    51,771,348

explicit static/development exclusions:
    15

network download or extraction performed:
    NO

authority decisions accepted:
    0
```

The set is an execution contract for later bounded inspection, not artifact/member authority.

Bounded artifact member-inventory collector:

```text
exact artifacts permitted:
    34

named edges inspected:
    44

private exact-artifact cache:
    experiments/glibc/selected-obsidian-provider-authority/work/artifacts/generic-artifact-member-inventory

inspection mode:
    dpkg-deb control/data tar streams; no package installation or filesystem payload materialization

exact basename and ELF SONAME observation:
    IMPLEMENTED / CANDIDATE EVIDENCE ONLY

authority decisions accepted:
    0

target rows populated:
    0
```

The collector verifies exact size, SHA-256, Package, Version and Architecture, rejects unapproved hosts or redirects, preserves dpkg/apt/repository state and emits a reviewable receipt.

## Preserved evidence

```text
N2 read-only evidence:
    e1eec5b68286cd6f888241afb50d9eabe00a8765269ecf20eb57bc0d7fe270d0

corrected N3 normalization:
    4dd86c4af956b447ed1829d6b5d604f43d10a17e5b3dcb3ddff3e9b48c377a9c

source-recipe evidence:
    c8160016267f3ff83b348146240f74f808ffbc93374a6f75988231ef22408cdb

exact binary-artifact comparison:
    da16d49acf54cbc8b6824e3974f08fea9ad0d6daf91687f4666d6c48d0b7567f
```

Exact binary result:

```text
priority package artifacts:
    28

artifact data members compared:
    6,887

artifact ELF members:
    462

member mismatches:
    0
```

This proves exact bounded supply recognition and installed equivalence. It does not prove final semantic provider authority or future clean acquisition.

## Global coverage normalization

```text
semantic-object denominator:
    161

ELF semantic objects:
    113

FIRST_GENERATION_CONTENT_IDENTITIES:
    96 = 91 external selected ELF + 4 fonts + 1 generated schema aggregate

APPLICATION_LOCAL_REFERENCE_IDENTITIES:
    11

protected-world references:
    18

bounded priority reviewed objects:
    59

non-priority generic provider identities:
    61
```

The 59 priority objects are a subset of the 161-row denominator. The 96 first-generation contents are not the application-local payload.

Additional application identity classes are now bounded separately:

```text
APPLICATION_PAYLOAD_IDENTITY
    historical version/architecture/format bounded; exact source identity open

APPLICATION_LAUNCHER_SUPPLY_IDENTITY
    exact current repository GUI/CLI source accepted; future publication/update lifecycle open

APPLICATION_DOMAIN_SUPPLEMENT_IDENTITIES
    identity class accepted; named membership open
```

## Canonical normalized layers

```text
SupplyArtifact
    exact repository metadata, artifact identity, retention and binding state

ProviderObjectAuthority
    canonical content identity with separated semantic/adaptation/source/supply/necessity/final states

ProviderFragmentMembership
    capability and composition-pressure edges only

ApplicationRuntimeComposition
    not yet reached

TargetLayout
    schema and invariants only; no populated rows
```

### Supply registry

```text
repository metadata records:
    1

exact priority artifacts:
    28
```

Clean acquisition remains open because signature-key policy, immutable retention/snapshot, future availability, source archive binding, and build attestation are not complete.

### Provider-object registry

```text
priority denominator objects:
    59

optional non-denominator objects:
    1 (libtermux-exec.so)

canonical object rows:
    60
```

Each object has independent fields for:

```text
semantic_role_state
termux_android_adaptation_state
candidate_source_comparison_state
exact_supply_artifact_state
artifact_to_recipe_binding_state
profile_necessity_state
provisional_final_provider_state
```

Exact supply is retained while final generic/platform source choice is conservative.

### Adaptation correction

```text
glibc:
    explicit Termux/Android adaptation proven for the reviewed world set

libxcb:
    Termux X11 socket-prefix patch proven
    final platform source still provisional

libxshmfence:
    Termux shared-memory directory policy proven
    final provider still provisional

libX11/libXau/libXdmcp/libXext/libXrandr/libXrender:
    generic Termux repository builds
    object-specific platform adaptation not recorded

libcap.so.2:
    PLATFORM_OR_GENERIC provisional
    selected-object adaptation effect unresolved
```

## Provider fragments

Normalized fragments:

```text
world-core-provider-fragment
glibc-locale-data-fragment
base-obsidian-x11-provider-fragment
graphics-freedreno-provider-fragment
gtk-font-device-compat-provider-fragment
printing-provider-fragment
optional-termux-exec-provider-fragment
```

Cardinality:

```text
reviewed priority fragment memberships:
    63

optional non-denominator memberships:
    1

total content edges:
    64
```

These are pressure edges, not deployable profiles, installation inheritance, complete dependency closures, or extraction instructions.

`libxcb-render.so.0` and `libxcb-shm.so.0` remain in the base fragment because passive evidence records mapped/direct base consumers. They are not duplicated in the graphics fragment.

## Alias authority

```text
canonical artifact aliases:
    84

SONAME runtime candidates:
    40

linker/development aliases:
    41

loader/entrypoint aliases:
    2

package-internal unresolved aliases:
    1

historical fragment alias edges:
    92
```

The historical lock files therefore contain:

```text
64 content edges + 92 alias edges = 156 rows
```

“93 required aliases” is withdrawn. No alias is automatically included in a runtime target. Linker/development aliases are excluded from runtime composition unless a separate research/build profile is declared.

## Files

```text
schema/
    census-columns.tsv
    capability-groups.tsv

review/
    package-authority-t0.tsv
    package-authority-t1.tsv
    selected-object-authority-base.tsv
    selected-object-authority-conditional.tsv
    unresolved-authority-ledger.tsv
    post-0134-architecture-audit-findings.tsv
    normalization-codebook.tsv
    world-lifecycle-authority-boundary.tsv
    application-authority-boundary.tsv
    generic-source-authority-boundary.tsv
    generic-exact-candidate-search-tokens.tsv

    authority-coverage-ledger.tsv
    authority-coverage-ledger/*.tsv

    non-priority-generic-authority-ledger.tsv
    non-priority-generic-authority-ledger/*.tsv

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

    provider-profile-definitions.tsv          # historical pre-normalization fragment draft
    provider-profile-artifact-locks.tsv       # historical bounded artifact edges
    member-locks/*.tsv                        # historical bounded supply locks

work/                                        # ignored by Git
    source/
    artifacts/
    receipts/unpacked/
    tmp/
```

Large canonical registries use a root index plus SHA-256-locked partitions. The authoritative set is the union of indexed partitions.

## Non-priority generic source-class boundary

`review/generic-source-authority-boundary.tsv` defines seven non-materializing contracts:

```text
global denominator:
    61 identities in six capability groups

observed byte origins:
    60 Debian-rootfs oracle identities
    1 local graphics-experiment identity

accepted boundary:
    observed origins are reference evidence only
    shared generic ownership is the default review direction
    protected-world, application-local and application-supplement ownership require explicit exceptions

open:
    exact Termux/upstream/project/native-adapter candidates
    object-to-artifact/source binding
    adaptation, necessity, final provider and update/rollback authority
```

This boundary does not accept clean supply, final provider authority, composition or target population.

## Generic exact-candidate collector

`review/generic-exact-candidate-search-tokens.tsv` preserves one candidate-search row for each of the 61 generic identities. `recipe/run-generic-exact-candidate-evidence.sh` reads only retained apt indexes/cache and the pinned clean source checkout.

```text
accepted by implementation:
    search contract and read-only collector mechanics

not accepted:
    search match as package ownership
    object membership inside a candidate artifact
    artifact-to-build attestation
    adaptation, necessity or final provider
    target population
```

The collector performs no network, package, extraction, build, runtime, generation or current operation.

## Generic artifact member-inventory collector

`recipe/run-generic-artifact-member-inventory.sh` and `recipe/collect-generic-artifact-member-inventory.py` implement the bounded 0142 execution contract.

```text
allowed persistent writes:
    exact verified .deb cache under experiment work
    evidence receipt under work or handoff directory

allowed package inspection:
    control identity query
    control/data tar stream metadata inventory
    bounded in-memory ELF SONAME observation for named members

forbidden:
    apt/pkg/dpkg installation transaction
    maintainer-script execution
    filesystem payload extraction/materialization
    runtime composition or target population
```

All member observations remain candidate evidence pending receipt review.

## Target-layout boundary

The target schema defines twenty fields for authority/composition references, supply references, target domain/path/node policy, mode/owner/mutability, alias/collision policy, update/rollback, validation, authority issues, and population state.

Current permitted state:

```text
population_state:
    UNPOPULATED_SCHEMA_ONLY
```

No target path, mode, owner, alias, collision result, extraction command, staging tree, or generation is defined.

```text
artifact member path/mode:
    supply recognition metadata

installed source path:
    historical evidence

future target path/mode/owner:
    independently governed and currently unpopulated
```

## Open authority issues

```text
AUTH-001 world clean reconstruction, acquisition, named internals and successor validation
AUTH-002 optional Termux exec necessity
AUTH-003 GTK/GLib/font/device/Wayland composition
AUTH-004 printing capability/provider
AUTH-005 graphics/X11/XCB provider composition
AUTH-006 libwayland artifact-to-recipe binding
AUTH-007 supply/alias/target population contract
AUTH-008 remaining data capabilities; locale/loader lifecycle bounded
AUTH-009 non-priority generic capabilities; source classes, retained candidate quality and named comparison set bounded, object/member and final bindings open
AUTH-010 exact payload supply, named supplement membership and release execution; launcher source boundary bounded
```

## Claim discipline

```text
bounded 59-object review != global 161-row authority closure
96 first-generation contents != application-local payload
package ownership != semantic authority
Termux supply origin != automatic platform authority
exact artifact identity != final generic source choice
recipe candidate != build attestation
artifact alias != runtime alias requirement
artifact mode/path != target policy
fragment membership != runtime composition
schema definition != target population
working runtime != final provider composition
```

## Next valid state

```text
CLOSE_GLOBAL_WORLD_APPLICATION_GENERIC_AND_DATA_AUTHORITY_GAPS
```

Active repository task:

```text
RUN_BOUNDED_GENERIC_ARTIFACT_MEMBER_INVENTORY_COLLECTOR
```

The bounded collector is implemented. The next work is to collect one exact device receipt and review member observations without accepting provider authority or target population.

## Stop line

Do not:

```text
consume historical member locks or fragments as extraction manifests;
populate target rows;
write an extraction/materializer script;
treat exact Termux supply as final generic/platform authority;
copy linker/development aliases into a runtime target;
copy artifact paths/modes/ownership into target policy;
install, remove, upgrade or downgrade packages;
run maintainer scripts;
materialize a successor;
create or modify current;
change the promoted launcher or loader state;
patch RPATH;
reopen closed graphics gates.
```
