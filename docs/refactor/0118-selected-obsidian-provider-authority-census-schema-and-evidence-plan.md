# 0118 — Selected Obsidian Provider-Authority Census Schema and Evidence Plan

## Status

This record completes N1 of the provider-authority intervention execution order.

```text
record type:
    CENSUS SCHEMA / EVIDENCE-SOURCE PLAN

provider-authority intervention:
    ACTIVE AND BINDING

runtime implementation:
    NO

package operation:
    NO

generation mutation or activation:
    NO

promoted launcher change:
    NO

result:
    N1_SCHEMA_AND_EVIDENCE_PLAN_PASS

next state:
    READY_FOR_N2_READ_ONLY_PROVIDER_EVIDENCE
```

This record does not choose final providers, finalize a successor manifest, or authorize materialization.

## Authority and claim boundary

Read this record under:

```text
main/docs/system-foundation/01-essence.md
main/docs/system-foundation/02-principles-and-invariants.md
main/docs/system-foundation/03-system-model-v2.md
main/docs/system-foundation/05-ideal-target-architecture.md
main/docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
main/docs/system-foundation/12-document-consistency-audit-and-execution-order.md

docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md
docs/refactor/0115-proot-oracle-supply-and-baseline-model.md
docs/refactor/0112-selected-obsidian-passive-map-selection-diagnostic-pass-and-contract-decision.md
docs/refactor/0117-provider-authority-intervention-adoption-and-execution-order.md
STATUS.md
experiments/glibc/selected-obsidian-closure/README.md
```

The controlling distinction is:

```text
historical selected/reference classification
    = accepted evidence about the tested control graph

provider-authority census classification
    = current provisional semantic judgment under 0116/0117

final promoted authority
    = blocked until intervention-lift audit PASS
```

No B1–B10 fact is discarded. No B7 action or path class is automatically promoted into final authority.

## N0 verification reached in this session

Repository-side facts verified through the GitHub repository authority:

```text
repository:
    daylight-00/termux-native-desktop

branch:
    docs/post-graphics-architecture-audit

branch tip:
    28bf8c1d729d4b9a2e80c574d27109a626b9d34d

expected tip comparison:
    IDENTICAL

authority and handoff:
    READ
```

The following remain device-side preflight facts before any new device experiment:

```text
tracked device worktree clean;
current remains absent;
first immutable generation still exists and is unchanged;
required local B1/B2/B7/B9/B10 receipts still exist when consumed.
```

This record does not claim those live device facts were re-observed by the assistant.

## Census design principle

The census is capability-first and object-complete.

```text
capability group
    -> semantic responsibility and reference authority
    -> object/data/cache/toolchain/oracle members
    -> candidate-source comparison
    -> provisional authority and missing evidence
```

It is not:

```text
91 unrelated ELF rows
    -> path-based source choice
```

Capability rows prevent package and pathname accidents from defining the architecture. Object rows preserve the exact identity, ABI, locality, provenance, and dependency evidence required to test each capability judgment.

## Two-layer census model

### Layer A — capability authority rows

One row represents one semantic capability or lifecycle responsibility.

Examples:

```text
world.glibc.core
platform.x11-xcb.termux
shared.dbus
shared.gtk-stack
shared.font-stack
data.fonts
data.gsettings
shared.pixbuf-codecs
data.icons
data.mime
shared.nss
shared.tls
toolchain.glibc-target
oracle.debian-scenarios
runtime.mutable-and-cache
```

A capability row owns:

```text
reference-authority question;
minimum valid scope;
application-domain demand;
candidate-source comparison;
Termux/Android adaptation question;
profile placement;
update domain and revalidation trigger;
provisional final authority;
unresolved discriminating evidence.
```

### Layer B — concrete member rows

One row represents one exact object, generated aggregate, data file, cache class, toolchain component, or oracle-only state item.

Member rows retain:

```text
current selected/reference path;
content identity and ELF identity where applicable;
package/source provenance;
B1/B2/B7/B9/B10 evidence relations;
$ORIGIN/RPATH/locality relation;
ABI/version coupling;
capability-group membership;
historical action/class;
current provisional semantic class;
source candidates and evidence gaps.
```

One content hash may appear in more than one path or authority relation. Rows must not be collapsed merely because bytes match.

## Canonical row identity

Every census row has:

```text
row_id
row_type
capability_group
object_or_capability
```

Allowed `row_type` values:

```text
CAPABILITY
ELF_OBJECT
APP_LOCAL_OBJECT
DATA_OBJECT
GENERATED_DATA
MUTABLE_STATE
CACHE_CLASS
TOOLCHAIN_COMPONENT
ORACLE_STATE
PACKAGE_SURFACE
```

`row_id` is a stable repository-local identifier. It must not be derived only from a mutable absolute path.

For concrete immutable files, retain separate identities for:

```text
content SHA-256;
ELF Build ID when present;
SONAME/lookup name when present;
package artifact/version provenance;
current observed path;
selected-generation object identity when present.
```

## Required authority fields

Every applicable row records the fields required by 0117:

```text
object_or_capability
current_selected_or_reference_path
current_package_or_source_provenance
semantic_class
minimum_valid_scope
application_domains
app_local_origin_relation
candidate_source_termux_glibc_package
candidate_source_exact_debian_artifact
candidate_source_upstream_or_app_local
candidate_source_project_build
candidate_source_native_termux_or_android
termux_android_adaptation_required
abi_version_coupling
profile_runtime_or_research
update_owner
revalidation_trigger
provisional_final_authority
unresolved_discriminating_evidence
```

The repository schema adds evidence-control fields so provisional language cannot be mistaken for a final decision:

```text
historical_semantic_class
historical_action
content_sha256
elf_build_id
lookup_name
soname
evidence_state
evidence_refs
evidence_claim_scope
evidence_conflict
authority_decision_state
notes
```

## Controlled values

### Semantic class

```text
WORLD_CORE_SUBSTRATE
PLATFORM_INTEGRATION_PROVIDER
GENERIC_SHARED_CAPABILITY_PROVIDER
APPLICATION_LOCAL
APPLICATION_DOMAIN_SUPPLEMENT
DATA_CAPABILITY_PROVIDER
TOOLCHAIN_ONLY
ORACLE_ONLY
MUTABLE_OR_CACHE
UNRESOLVED
```

`UNRESOLVED` is valid and preferred over a path-first guess.

### Minimum valid scope

```text
WORLD
PLATFORM_INTEGRATION
SHARED_CAPABILITY
APPLICATION_FAMILY
APPLICATION_DOMAIN
APPLICATION_LOCAL
DATA_CAPABILITY
BUILD_SUPPLY
ORACLE_SCENARIO
MUTABLE_CACHE
UNRESOLVED
```

### Evidence state

```text
OBSERVED
DERIVED
INFERRED
PROVISIONAL
CONFLICTED
MISSING
```

### Authority decision state

```text
OPEN
PROVISIONAL
ACCEPTED_FOR_INTERVENTION_REVIEW
REJECTED
BLOCKED
```

No row may become `ACCEPTED_FOR_INTERVENTION_REVIEW` solely because its current path is under `$PREFIX/glibc`, the Debian rootfs, the AppDir, or the first generation.

### Candidate-source cell state

Each candidate-source field uses a state plus evidence reference, not a bare yes/no:

```text
UNASSESSED
NO_KNOWN_CANDIDATE
CANDIDATE_IDENTIFIED
ARTIFACT_IDENTIFIED
BYTE_IDENTITY_PROVEN
BEHAVIOR_PROVEN
REQUIRES_DISCRIMINATOR
REJECTED_WITH_REASON
```

### Runtime/research profile

```text
RUNTIME
RESEARCH_BUILD_MAINTENANCE
BOTH_WITH_SEPARATE_ARTIFACTS
NEITHER
UNRESOLVED
```

### Update owner

```text
WORLD_SUBSTRATE
PROVIDER
APPLICATION
TOOLCHAIN
ORACLE_SCENARIO
MUTABLE_STATE
UNRESOLVED
```

## Historical evidence ingestion

### Selected/reference seed

The selected/reference census begins from the accepted B7 receipt, not from a fresh workload run.

Primary B7 seed files:

```text
semantic-object-disposition.tsv
candidate-elf-manifest.tsv
candidate-data-manifest.tsv
capability-membership.tsv
reference-runtime-owned-manifest.tsv
schema-source-manifest.tsv
schema-build-contract.tsv
```

Interpretation rule:

```text
B7 semantic_class / primary_action / primary_capability
    -> historical_semantic_class / historical_action / evidence membership

not

B7 classification
    -> final provider authority
```

### Identity and locality enrichment

Use B1 evidence for:

```text
semantic path set;
package/version/SHA-256 identity;
APP_LOCAL path and $ORIGIN-first locality;
lookup-name collision result;
retained mapped-process observations.
```

Use B2 evidence for:

```text
resolved DT_NEEDED edges;
entrypoint-static closure;
all-app-local static closure;
mapped-only dynamic roots and support closure;
non-ELF data separation.
```

### Materialization and runtime enrichment

Use B9 evidence for:

```text
content-addressed object identity;
alias identity;
generation membership;
copy-time source identity;
generated GSettings identity.
```

Use passive B10 and the passive map-selection diagnostic for:

```text
actual mapped path and content identity;
process-class observation;
selected/world/app-local map class;
Xau/Xdmcp exact RPATH-bound substitution evidence;
demand-loaded selected data behavior;
negative broad-farm/rootfs/current mapping evidence.
```

Use the pixbuf inventory only for bounded capability evidence:

```text
cache format and embedded path facts;
loader-module inventory;
icon-theme inventory;
MIME inventory;
current B9 manifest absence.
```

It is not a provider-authority decision.

## Current glibc-prefix evidence

`0018` already proves:

```text
current package backend:
    Termux APT/dpkg

active glibc package ownership:
    dpkg-owned

exact-artifact acquisition path:
    APT candidate capability

architecture:
    backend-neutral above the adapter
```

It does not provide the complete semantic partition now required across every relevant package and object under or feeding `$PREFIX/glibc`.

N2 therefore requires a new read-only inventory. No package operation is allowed.

Required package-surface capture:

```text
installed package name/version/architecture/status;
package file lists for relevant `$PREFIX/glibc` paths;
file-to-package ownership;
conffiles, maintainer scripts, and trigger metadata when present;
symlink text and resolved target;
regular-file SHA-256;
ELF architecture, interpreter, SONAME, NEEDED, RPATH/RUNPATH, Build ID;
non-ELF data/config/cache classification;
current consumers among selected/reference objects;
current profile pressure: runtime, research, or unresolved.
```

The inventory must distinguish:

```text
package presence
package ownership
runtime demand
semantic responsibility
final authority
```

These are separate claims.

## Initial capability groups

The initial group registry is repository data under:

```text
experiments/glibc/selected-obsidian-provider-authority/schema/
    capability-groups.tsv
```

The groups are deliberately broader than individual packages and narrower than one universal shared-library pool:

```text
world loader/libc/tightly coupled runtime;
Termux-aware X11/xcb and host integration;
D-Bus;
GTK/GLib/GIO/Pango/ATK;
fontconfig/freetype/harfbuzz;
font data and fallback contract;
locale data;
GSettings schemas;
gdk-pixbuf and image codecs;
icon themes;
MIME database;
NSS/security;
TLS and CA trust;
audio;
printing;
compression and archive libraries;
GLVND/Mesa frontend and closed graphics relations;
application-local Electron/Obsidian payload;
application-domain supplements;
toolchain/sysroot/wrappers;
oracle-only package/scenario state;
mutable state and caches.
```

Capability membership may overlap. Every concrete row still has one provisional primary semantic class and one update owner.

## Merge and conflict rules

### Path and content are independent

```text
same bytes at selected and world paths
    -> preserve both path relations and one content identity
    -> do not infer semantic class from loader choice alone
```

This applies directly to Xau/Xdmcp.

### Application locality is first-class

An app-local row records:

```text
$ORIGIN/RUNPATH order;
lookup-name competitors;
upstream topology;
replacement rationale if any.
```

Valid app-local topology is preserved unless explicit replacement evidence exists.

### Capability and package are independent

One package may supply several semantic capabilities. One capability may have candidates from several package/artifact sources.

No census group is keyed solely by package name.

### Data, generated output, mutable state, and caches remain separate

Do not combine:

```text
font files;
fontconfig configuration;
fontconfig cache;
pixbuf loader modules;
pixbuf loaders.cache;
icon data;
MIME data;
GSettings source schemas;
gschemas.compiled;
user/application state.
```

Each has a separate source, generation, update, and rollback question.

### Conflicts remain visible

When historical documents use an older class name such as `WORLD_SUBSTRATE_ELF` or `PROVIDER_ROOTFS_ELF`, retain it under `historical_semantic_class` and record the current 0116 class separately.

Do not rewrite historical evidence to make the new model appear inevitable.

## N2 evidence-source priority

Use the minimum sufficient source in this order:

```text
1. embedded accepted receipts;
2. repository canonical summaries and exact accepted hashes;
3. current read-only device identity inventory;
4. additional bounded discriminator only when existing evidence cannot decide.
```

Do not rerun a workload merely to reproduce an already accepted identity or graph fact.

## N2 output sets

The read-only evidence phase should emit four explicit sets:

```text
selected-reference-object-seed.tsv
    every B7 selected/reference/data/cache/state row with B1/B2/B9/B10 evidence

glibc-prefix-package-surface.tsv
    package and object inventory without semantic promotion

provider-authority-census.tsv
    capability and object rows using the canonical schema

unresolved-evidence-ledger.tsv
    one discriminating question, current evidence, missing evidence, and permitted next action per open decision
```

The first N2 pass may leave many authority fields `UNRESOLVED` or `PROVISIONAL`.

## Initial unresolved evidence ledger

The following remain open at N1 completion:

```text
complete relevant Termux glibc-prefix package/object surface;
which prefix X11/xcb packages contain material Termux/Android adaptation;
source candidate inventory for each generic capability;
exact Debian artifact identities independent of the mutable rootfs;
ABI/version coupling inside GTK/GLib/font/pixbuf/NSS/TLS/audio/printing/compression groups;
minimum interactive Vault-open pixbuf loader/cache/icon/MIME requirement;
final native-space font provider and Korean/CJK/math/fallback coverage;
application-local replacement pressure, if any;
locked supply artifacts for accepted providers;
minimum runtime versus research package/state boundary;
five-domain update and revalidation matrix;
content/provenance/composition/install/validation identity separation.
```

## Bounded pixbuf relation

The controlled pixbuf discriminator may proceed after this schema is stable, but it remains independent of N2 census ingestion.

Required fixed boundaries:

```text
same immutable unactivated generation;
no package installation;
no generation mutation;
no current creation or change;
no promoted launcher change;
short receipt-owned runtime paths;
rootfs inputs diagnostic-only;
closed graphics gates closed.
```

Required sequence remains:

```text
D0 reproduce current failure;
D1 receipt-local relocated cache effect;
D2 exact loader-module effect when distinct;
D3 icon-theme effect;
D4 MIME effect;
D5 combinations only after single-variable evidence.
```

A PASS populates evidence fields. It does not populate final authority by itself.

## Intervention stop line

Do not:

```text
finalize a successor manifest;
materialize a successor generation;
create or change current;
mutate the first generation;
patch RPATH;
install packages for census or pixbuf work;
classify all `$PREFIX/glibc` files as world core;
classify all Debian-selected objects as final providers;
replace app-local objects by lookup-name convenience;
merge compiler/toolchain/oracle state into the minimum runtime profile;
promote the current font or pixbuf inventory by inertia;
reopen closed graphics work.
```

## Direction decision

```text
N0 repository onboarding:
    PASS

N1 census schema and evidence-source plan:
    PASS

selected/reference evidence seed:
    B7-FIRST WITH B1/B2/B9/B10 ENRICHMENT

glibc-prefix evidence:
    NEW READ-ONLY INVENTORY REQUIRED

provider decisions:
    OPEN / PROVISIONAL ONLY

next action:
    N2 READ-ONLY PROVIDER EVIDENCE
```
