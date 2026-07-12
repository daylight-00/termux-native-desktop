# 0135 — Selected Obsidian Provider-Profile Lock Draft Architecture Audit

## Status

This record audits the repository state at:

```text
branch:
    docs/post-graphics-architecture-audit

HEAD reviewed:
    9bc7e9ffb92cf5d7b1095508e8a21438026656cd
```

Audit verdict:

```text
priority evidence and package/object disposition:
    PASS WITH BOUNDED SCOPE

exact .deb and member identity locks:
    STRONG PASS AS NON-MATERIALIZING SUPPLY DRAFT

package-wide runtime rejection:
    PASS

semantic provider-authority completeness:
    PARTIAL PASS / REQUIRED CORRECTIONS

deployable profile or target-layout readiness:
    FAIL / NOT REACHED

successor materialization and current activation:
    BLOCKED

immediate device intervention:
    NOT REQUIRED
```

The work is directionally correct and contains no unsafe runtime mutation. The next state must be narrowed before target paths or extraction manifests are populated.

## Inputs reviewed

```text
docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md
docs/refactor/0117-provider-authority-intervention-adoption-and-execution-order.md
docs/refactor/0133-selected-obsidian-priority-provider-authority-review.md
docs/refactor/0134-selected-obsidian-provider-profile-locked-member-draft.md
STATUS.md
experiments/glibc/selected-obsidian-provider-authority/README.md
experiments/glibc/selected-obsidian-provider-authority/review/*.tsv
experiments/glibc/selected-obsidian-provider-authority/profiles/*.tsv
experiments/glibc/selected-obsidian-provider-authority/profiles/member-locks/*.tsv
```

The claimed branch tip is exact. The eighteen commits since `3722d5e9e138b517b1daec30bee3d4d1270d80f6` modify only the documented review/profile surface and status files. No package, runtime, launcher, generation, or activation transaction is introduced.

## What is accepted without qualification

### 1. Exact bounded evidence

The following evidence remains accepted:

```text
28 priority package identities dispositioned;
59 bounded priority selected/reference objects dispositioned;
28 exact indexed .deb artifacts acquired and verified;
6,887 data members compared with zero live-member mismatches;
462 artifact ELF objects inventoried;
59 reviewed object contents matched exact artifact members;
93 package-provided symlink members recorded;
35 profile/package artifact edges recorded;
all materialization flags remain NO / DRAFT_LOCK_ONLY_BLOCKED.
```

### 2. Package authority is not runtime scope

The package/member distinction is correct and load-bearing.

Examples such as `libdrm-glibc`, `krb5-glibc`, `e2fsprogs-glibc`, and `libxcb-glibc` correctly reject package-wide promotion when only selected SONAME members have workload evidence.

The accepted supply model remains:

```text
recipe/source evidence
    + exact artifact identity
    + exact member identity
    + explicit semantic/profile decision
```

not:

```text
installed package
    = minimum runtime authority
```

### 3. Non-materialization boundary

The current drafts correctly avoid:

```text
package installation/removal/update;
maintainer-script execution;
target extraction;
staging tree creation;
generation materialization;
current creation or mutation;
promoted launcher change;
loader-state mutation;
RPATH patching;
runtime launch.
```

No immediate stop or rollback is required.

### 4. Strong accepted decisions

The following decisions survive this audit:

```text
Termux/Android-adapted glibc 2.42 is the accepted current native world candidate and exact binary authority for the reviewed world set;
glibc-runner remains research/build/maintenance tooling and is excluded from promoted runtime;
termux-exec-glibc remains optional and outside the minimum runtime until a named exec transition proves necessity;
package-wide inclusion is rejected;
conditional graphics, GTK/device/Wayland, printing, and optional-exec fragments do not enter base by availability;
installed absolute paths are evidence and not future target authority;
existing selected generation remains immutable and unactivated.
```

The world reconstruction/update/rollback contract remains open, so accepted current glibc authority is not equivalent to a completed clean-world installation contract.

## Required correction 1 — bounded denominator versus global coverage

The statement:

```text
selected/reference objects:
    59 / 59 dispositioned
```

is true only for the bounded priority subset.

It must not be read as completion of the `0116` requirement over the complete selected/reference application domain.

The repository already preserves larger denominators:

```text
semantic objects:
    161

ELF objects:
    113

first generation content identities:
    96

first generation selected ELF:
    91

app-local reference identities:
    11

protected-world references:
    18

non-ELF data objects:
    17
```

The next audit layer needs one coverage ledger that accounts for every relevant identity under one of:

```text
reviewed authority row;
application-local authority row;
world reconstruction row;
data-capability authority row;
conditional capability row;
mutable/cache row;
explicitly excluded row;
unresolved evidence row.
```

Until that denominator closes, the current profiles are priority provider fragments, not a complete base composition.

## Required correction 2 — application identity terminology

Current living documents state that the base profile omits:

```text
96 application-local generation identities
```

This is architecturally incorrect.

The ninety-six first-generation content identities are selected external ELF/data generation content:

```text
91 selected ELF;
4 selected fonts;
1 generated schema aggregate.
```

They are not the application-local AppDir payload.

The application-local boundary is separate:

```text
11 retained app-local reference identities;
upstream Obsidian/Electron payload identity;
application entrypoint and launcher supply identity;
valid $ORIGIN topology;
app-local auxiliary identities such as SwiftShader;
mutable user/application state.
```

Use these terms going forward:

```text
FIRST_GENERATION_CONTENT_IDENTITIES
APPLICATION_LOCAL_REFERENCE_IDENTITIES
APPLICATION_PAYLOAD_IDENTITY
APPLICATION_DOMAIN_SUPPLEMENT_IDENTITIES
```

This correction is required before any target-domain schema is populated.

## Required correction 3 — supply authority versus final provider authority

The exact Termux `.deb` member locks prove:

```text
one exact artifact can supply the accepted byte;
the installed file matched that artifact member;
the package recipe history contains bounded source candidates.
```

They do not, by themselves, prove:

```text
the Termux artifact is the final source for every generic capability;
the semantic role is platform integration rather than generic capability;
a Debian/upstream/app-local/project candidate is inferior;
the exact artifact is cryptographically bound to one recipe tree;
the artifact remains reconstructibly obtainable in the future.
```

The ledgers currently compress several claims into `ACCEPTED_OBJECT_SCOPED_AUTHORITY`.

The normalized authority model must split at least:

```text
semantic_role_state;
termux_android_adaptation_state;
candidate_source_comparison_state;
exact_supply_artifact_state;
artifact_to_recipe_binding_state;
profile_necessity_state;
provisional_final_provider_state.
```

The existing member locks remain valid. The semantic finality of generic and nominal platform providers must be downgraded where candidate comparison or adaptation evidence is incomplete.

## Required correction 4 — X11/XCB adaptation evidence

`0116` authorizes platform classification for Termux-aware or Android/path-sensitive providers. It does not classify every object built by a Termux glibc repository as platform integration.

The current review assigns all selected X11/XCB SONAME objects to:

```text
PLATFORM_INTEGRATION_PROVIDER
```

The source-recipe receipt explicitly preserved adaptation inputs for `libxcb`, but the current authority rows do not record an object/package-specific adaptation proof for every X11 package.

A Termux prefix, Termux recipe, or Termux-built artifact can be the selected supply source while the semantic role remains a generic X11 capability.

Required field:

```text
adaptation_evidence_state:
    PROVEN_TERMUX_ANDROID_ADAPTATION
    GENERIC_BUILD_IN_TERMUX_SUPPLY
    MIXED_OR_UNRESOLVED
```

Required evidence examples:

```text
patch or auxiliary source path;
Termux/Android-specific compile option;
path/IPC/credential/device behavior;
consumer test that distinguishes the adapted object;
absence of meaningful adaptation and generic ABI equivalence.
```

Until populated, preserve exact member locks but treat platform-versus-generic classification as provisional for objects without direct adaptation evidence.

## Required correction 5 — `libcap.so.2` classification

The current ledger classifies `libcap.so.2` as:

```text
PLATFORM_INTEGRATION_PROVIDER
```

The fact that Linux capabilities interact with Android security does not by itself prove that the selected library implements a Termux integration responsibility.

The current review record does not name a concrete Termux patch or distinguishing behavior for `libcap.so.2`.

Correct interim state:

```text
semantic authority:
    PLATFORM_OR_GENERIC_PROVISIONAL

exact artifact/member supply:
    ACCEPTED

profile necessity:
    CONDITIONAL
```

Final platform classification requires adaptation or behavior evidence.

## Required correction 6 — alias locks are not runtime requirements

The profile draft calls ninety-three package-provided symlinks:

```text
required aliases
```

The exact artifact inventory includes examples such as:

```text
libexpat.so
libX11.so
libXau.so
libxcb.so
libstdc++.so
libdrm.so
```

These unversioned names are commonly linker/development aliases. They can be runtime-relevant only when a consumer explicitly opens that name or another accepted runtime relation requires it.

Recording the exact package alias is valid supply evidence. Promoting it to the target is a separate claim.

Every alias must receive one class:

```text
SONAME_RUNTIME_ALIAS
PROVEN_DLOPEN_RUNTIME_ALIAS
LOADER_OR_ENTRYPOINT_ALIAS
LINKER_DEVELOPMENT_ALIAS
PACKAGE_INTERNAL_RELATIVE_ALIAS
UNRESOLVED_ALIAS
```

Target inclusion rules:

```text
SONAME_RUNTIME_ALIAS:
    include when the content target is externalized and the SONAME lookup requires it

PROVEN_DLOPEN_RUNTIME_ALIAS:
    include only with call/discovery evidence

LINKER_DEVELOPMENT_ALIAS:
    research/build profile only

UNRESOLVED_ALIAS:
    blocks target alias inclusion
```

The current ninety-three rows should be renamed `artifact_alias_rows` until classified.

## Required correction 7 — target mode and ownership are independent

Member locks preserve package modes such as:

```text
regular ELF mode:
    0700

locale data mode:
    0600

symlink metadata mode:
    0777
```

These are exact artifact facts. They are not automatically correct target modes for:

```text
content-addressed immutable objects;
world installation;
shared provider generation;
application-domain supplement;
data-capability tree.
```

The extraction/target schema must add:

```text
target_domain;
target_relative_path;
target_node_type;
target_mode_policy;
target_owner_policy;
target_mutability;
target_alias_class;
target_collision_policy;
```

Artifact mode remains an input verification field, never an implicit target policy.

## Required correction 8 — provider fragments versus deployable profiles

The six named profiles are useful groupings, but they are not deployable runtime profiles.

Current `parent_profiles` edges express composition pressure. They do not establish:

```text
complete dependencies;
target layout;
installation inheritance;
activation scope;
rollback scope;
profile-specific validation completeness.
```

Use three separate object layers:

```text
ProviderObjectAuthority
    one canonical content/source/authority identity

ProviderFragmentMembership
    many-to-many capability/profile pressure edges

ApplicationRuntimeComposition
    final included/reference objects, target domains, policies, and validation gates
```

The current six definitions should remain non-materializing `provider fragments` until an application composition is built above them.

## Required correction 9 — shared membership and artifact deduplication

The following cardinality is valid as a graph:

```text
59 unique reviewed objects
63 profile content memberships
35 profile/package artifact locks
```

It is not valid as a direct extraction plan.

Shared objects such as:

```text
libcap.so.2
libffi.so.8
libz.so.1
```

need one canonical object identity with multiple membership/dependent edges.

Likewise one artifact SHA should be acquired and verified once, even if several fragments consume members from it.

Required registries:

```text
supply-artifact-registry.tsv
provider-object-registry.tsv
provider-fragment-memberships.tsv
runtime-alias-authority.tsv
```

Do not duplicate target objects or update ownership because a content identity appears in multiple fragments.

## Required correction 10 — world core and locale data remain separate semantic domains

`world-substrate-selected` contains:

```text
6 reviewed world-core ELF identities;
12 en_US locale data identities.
```

The common glibc artifact is a valid shared supply transaction. The semantic classes remain distinct:

```text
WORLD_CORE_SUBSTRATE
DATA_CAPABILITY_PROVIDER / GLIBC_COUPLED_LOCALE
```

The future target and update model must answer separately:

```text
world core installation and rollback;
locale selection policy;
C.UTF-8 versus en_US.UTF-8;
locale generation versus exact copied members;
application/profile locale requirements.
```

Do not use one profile name to collapse their lifecycle.

## Required correction 11 — supply recognition versus clean acquisition

The current locks contain strong recognition identity:

```text
repository filename;
artifact byte size;
artifact SHA-256;
exact member paths and hashes;
recipe candidate trees.
```

Clean reconstruction additionally requires:

```text
repository Release/InRelease identity and trust policy;
artifact acquisition host/path policy;
retained artifact or immutable snapshot availability;
artifact signature/index verification chain;
artifact-to-recipe binding state;
source archive and patch identities when source rebuild is an authority claim.
```

The exact `.deb` can remain the binary authority even when source-build provenance is incomplete. These states must be represented independently.

`libwayland-glibc` correctly exposes this distinction. The same field structure should exist for every package, even where one recipe version candidate currently exists.

## Required correction 12 — unresolved authority ledger is incomplete

The current eight issues cover world, exec, GTK compatibility packages, printing, graphics, Wayland source binding, materialization, and data/loader state.

Current documents also identify unclosed ownership for:

```text
D-Bus;
GTK core;
GLib/GIO;
Pango/ATK;
fontconfig/freetype/harfbuzz;
NSS/security modules outside reviewed world members;
other selected generic capability providers outside the priority twenty-eight packages.
```

These are not all data capabilities and are not fully represented by `AUTH-003` or `AUTH-008`.

Add:

```text
AUTH-009 NON_PRIORITY_GENERIC_CAPABILITY_AUTHORITY
```

Every unreviewed selected/reference object must point to one open authority issue.

## Required correction 13 — base XCB narrative ambiguity

The current object ledger and base member lock classify:

```text
libxcb-render.so.0
libxcb-shm.so.0
```

as accepted base objects.

The narrative in `0133` lists them under graphics-provider conditional authority while omitting them from the base X11 list.

This can be resolved in either direction, but it cannot remain ambiguous.

Decision rule:

```text
if passive base process/edge evidence requires the object:
    retain in base and describe graphics membership as secondary capability pressure

if only the graphics overlay requires the object:
    remove from base and place in the graphics fragment
```

The object ledger, profile membership, capability edges, and narrative must then agree.

## Revised next state

The previous next state was:

```text
CLOSE_BASE_PROVIDER_PROFILE_GAPS_AND_DEFINE_EXTRACTION_TARGET_CONTRACT
```

This mixes three maturity levels:

```text
semantic authority closure;
target-domain schema design;
populated extraction/materialization plan.
```

Corrected next state:

```text
NORMALIZE_PROVIDER_AUTHORITY_COVERAGE_AND_LOCK_SEMANTICS
```

Required order:

```text
P0. correct terminology and global denominator;
P1. split supply, adaptation, semantic authority, necessity, and final-source states;
P2. classify artifact aliases and target-independent modes;
P3. create canonical artifact/object registries and fragment membership edges;
P4. add missing non-priority generic authority issues;
P5. resolve base XCB narrative and profile-fragment boundaries;
P6. define target-domain/layout SCHEMA and invariants only;
P7. close world, application payload, D-Bus/generic, font, pixbuf/icon/MIME, and conditional capability authority;
P8. populate target paths and extraction rows only after the owning authority is accepted;
P9. run an intervention-lift audit before authoring a materializer.
```

A target schema can be designed now. A populated target manifest cannot.

## Revised status vocabulary

Use:

```text
PRIORITY_PROVIDER_EVIDENCE_PASS
EXACT_MEMBER_SUPPLY_LOCK_PASS
PACKAGE_WIDE_RUNTIME_REJECTION_PASS
PROVIDER_SEMANTIC_AUTHORITY_PARTIAL
PROVIDER_FRAGMENT_DRAFT_PASS
GLOBAL_AUTHORITY_COVERAGE_OPEN
TARGET_LAYOUT_SCHEMA_ALLOWED
TARGET_LAYOUT_POPULATION_BLOCKED
SUCCESSOR_MATERIALIZATION_BLOCKED
CURRENT_ACTIVATION_BLOCKED
```

Avoid:

```text
base runtime profile complete
required aliases
96 application-local generation identities
accepted final generic provider
extractable provider profile
```

unless later evidence actually closes those claims.

## Direction decision

```text
continue repository-side work:
    YES

continue exact supply locking:
    YES

preserve current ledgers as bounded evidence:
    YES

immediately populate target paths:
    NO

write extraction/materializer commands:
    NO

run device package or runtime transactions:
    NO

materialize successor:
    NO

activate current:
    NO
```

## Stop line

Do not:

```text
treat 59/59 as the complete selected/reference authority denominator;
call the 96 first-generation contents application-local;
treat a Termux package source as automatic platform semantic authority;
treat exact Termux artifact supply as final generic-provider source choice;
copy all package-provided aliases into a target;
preserve artifact modes as target modes by default;
consume parent_profiles as installation inheritance;
duplicate shared objects or artifacts per provider fragment;
collapse glibc locale data into world core lifecycle;
write populated target paths before authority ownership is accepted;
add D-Bus or other non-priority generic capabilities without a named authority issue;
materialize, activate, patch RPATH, mutate loader state, or run package transactions.
```

## Next repository outputs

Create or normalize:

```text
review/authority-coverage-ledger.tsv
review/non-priority-generic-authority-ledger.tsv
profiles/supply-artifact-registry.tsv
profiles/provider-object-registry.tsv
profiles/provider-fragment-memberships.tsv
profiles/runtime-alias-authority.tsv
profiles/target-layout-schema.tsv
profiles/target-layout-invariants.md
```

These outputs remain design/authority records. They do not authorize extraction or materialization.
