# Selected Obsidian Provider-Authority Census

## Status

```text
N0_REPOSITORY_ONBOARDING_PASS
N1_CENSUS_SCHEMA_AND_EVIDENCE_PLAN_PASS
N2_READ_ONLY_PROVIDER_EVIDENCE_PASS
N3_CORRECTED_NORMALIZED_CLASSIFICATION_PASS
N3_SOURCE_RECIPE_EVIDENCE_PASS
N3_BINARY_ARTIFACT_COMPARISON_PASS
PRIORITY_PROVIDER_EVIDENCE_PASS
EXACT_MEMBER_SUPPLY_LOCK_PASS
PACKAGE_WIDE_RUNTIME_REJECTION_PASS
PROVIDER_SEMANTIC_AUTHORITY_PARTIAL
PROVIDER_FRAGMENT_DRAFT_PASS
POST_0134_ARCHITECTURE_AUDIT_INTERVENTION
GLOBAL_AUTHORITY_COVERAGE_OPEN
TARGET_LAYOUT_SCHEMA_ALLOWED
TARGET_LAYOUT_POPULATION_BLOCKED
SUCCESSOR_MATERIALIZATION_BLOCKED
CURRENT_ACTIVATION_BLOCKED
```

This workstream implements the provider-authority intervention required by `0116`.

Current audit authority:

```text
docs/refactor/0135-selected-obsidian-provider-profile-lock-draft-architecture-audit.md
```

## Accepted evidence transactions

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

The exact binary receipt established:

```text
priority package artifacts:
    28

artifact data members compared:
    6,887

artifact ELF objects inventoried:
    462

live member mismatches:
    0
```

This is exact supply evidence, not package-wide runtime or final source authority.

## Priority review and lock draft

```text
priority package dispositions:
    28 / 28

bounded priority selected/reference object dispositions:
    59 / 59

base-labeled reviewed objects:
    29

conditional reviewed objects:
    30

unique reviewed object identities:
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

Accepted without qualification:

```text
exact artifact and member identities;
package-wide runtime rejection;
glibc-runner research-only exclusion;
termux-exec optional status;
non-materialization boundaries;
installed path versus target path separation.
```

Qualified by the `0135` audit:

```text
59/59 is the bounded priority subset, not global completion;
exact Termux supply is not automatically final generic-provider authority;
platform integration class requires explicit adaptation evidence;
93 aliases are artifact alias rows, not automatically runtime-required;
provider profiles are non-deployable fragments;
artifact member modes are not target modes;
96 first-generation contents are not application-local identities.
```

## Current files

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

profiles/
    README.md
    provider-profile-definitions.tsv
    provider-profile-artifact-locks.tsv
    member-locks/*.tsv

work/                       # ignored by Git
    source/
    artifacts/
    receipts/unpacked/
    tmp/
```

## Claim boundaries

```text
path identity != content identity
package ownership != semantic authority
recipe candidate != exact artifact build attestation
exact artifact identity != final source choice
artifact alias identity != runtime alias requirement
artifact mode != target mode
provider fragment membership != deployable profile inclusion
installed source path != future target authority
working runtime != final provider composition
```

## Global coverage correction

The bounded priority review does not yet account for the complete application domain.

The next coverage ledger must reconcile at least:

```text
161 semantic objects;
113 ELF objects;
96 first-generation content identities;
91 first-generation selected ELF identities;
11 app-local reference identities;
18 protected-world reference identities;
17 non-ELF data identities;
application payload and launcher supply identity;
non-priority generic and data capabilities.
```

Every identity must map to an accepted authority row, an explicit exclusion, or one unresolved authority issue.

## Required authority-state split

Future normalized rows must separate:

```text
semantic_role_state;
termux_android_adaptation_state;
candidate_source_comparison_state;
exact_supply_artifact_state;
artifact_to_recipe_binding_state;
profile_necessity_state;
provisional_final_provider_state.
```

Do not compress these into one accepted authority state.

## Provider-fragment normalization

Current fragment identifiers remain historical keys:

```text
world-substrate-selected
base-obsidian-x11-provider
graphics-freedreno-provider
gtk-font-device-compat-provider
printing-provider
optional-termux-exec-provider
```

They are not materializer inputs.

The next normalized model requires:

```text
supply-artifact-registry.tsv
provider-object-registry.tsv
provider-fragment-memberships.tsv
runtime-alias-authority.tsv
authority-coverage-ledger.tsv
target-layout-schema.tsv
target-layout-invariants.md
```

Shared object and artifact identities must be canonical and referenced by many fragment memberships rather than duplicated in extraction semantics.

## Alias correction

Current member locks record exact package symlinks, including unversioned names.

Before target inclusion classify every alias:

```text
SONAME_RUNTIME_ALIAS
PROVEN_DLOPEN_RUNTIME_ALIAS
LOADER_OR_ENTRYPOINT_ALIAS
LINKER_DEVELOPMENT_ALIAS
PACKAGE_INTERNAL_RELATIVE_ALIAS
UNRESOLVED_ALIAS
```

Only runtime-authorized aliases enter runtime composition.

## Platform versus generic correction

A Termux-built artifact is an accepted supply candidate when locked. It is not automatically a platform-integration semantic provider.

Required adaptation evidence includes one or more of:

```text
Termux/Android patch or auxiliary source;
path, IPC, identity, security or device adaptation;
consumer behavior that distinguishes the adapted object;
explicit evidence that no adaptation exists and the role is generic.
```

X11/XCB and `libcap.so.2` rows without direct adaptation evidence remain provisional at the semantic-class layer while retaining exact supply locks.

## Application identity correction

Use:

```text
96 FIRST_GENERATION_CONTENT_IDENTITIES
11 APPLICATION_LOCAL_REFERENCE_IDENTITIES
APPLICATION_PAYLOAD_IDENTITY
APPLICATION_LAUNCHER_SUPPLY_IDENTITY
APPLICATION_DOMAIN_SUPPLEMENT_IDENTITIES
```

Do not call the 96 generation contents application-local.

## Open authority groups

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

Required repository-side order:

```text
P0 correct terminology and global denominator;
P1 split supply/adaptation/semantic/necessity/final states;
P2 classify aliases and target-independent modes;
P3 create canonical artifact/object registries and fragment edges;
P4 map every unreviewed capability to an authority issue;
P5 resolve base XCB narrative ambiguity;
P6 define target-layout schema and invariants only;
P7 close world, application, generic and data authority gaps;
P8 populate target paths only after ownership is accepted;
P9 perform intervention-lift audit before a materializer.
```

A new device transaction is not required for the immediate normalization work.

## Storage boundary

```text
work/ and Termux-private paths:
    source repositories, raw artifacts, caches, unpacked receipts and temporary state

$HOME/Downloads:
    final handoff archives and explicitly requested exports only
```

## Stop line

Do not:

```text
treat the 59-object review as global completion;
consume current provider fragments as extraction manifests;
copy all artifact aliases into a target;
copy package modes into target policy;
treat Termux package origin as automatic platform authority;
call the 96 first-generation contents application-local;
populate target paths before authority ownership closes;
install/remove/update packages or run maintainer scripts;
extract/copy profile members into a target;
materialize a successor;
create or change current;
change promoted launchers;
mutate loader state or patch RPATH;
promote conditional fragments by availability;
reopen closed graphics gates.
```
