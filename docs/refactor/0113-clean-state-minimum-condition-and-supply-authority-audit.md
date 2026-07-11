# 0113 — Clean-State Minimum-Condition and Supply-Authority Audit

## Status

This is a top-down architecture audit of the accumulated selected-Obsidian work after the passive map-selection contract decision.

Audited repository state:

```text
commit:
    6c00ac7f9ca46bc2159c51689904e154146f0d2a

latest numbered decision:
    0112-selected-obsidian-passive-map-selection-diagnostic-pass-and-contract-decision.md
```

Scope:

```text
0093 -> 0112
selected Obsidian Phase B1-B10
content-addressed generation design/materialization
passive runtime and map contract
open GTK pixbuf/icon/MIME capability
clean-state reconstruction and rootfs supply authority
```

This audit does not rerun a workload, mutate the published generation, change `current`, install or remove a package, or modify promoted runtime source.

## Philosophy refinement

The project already used:

```text
minimum manipulation
    -> do not transform bytes or add infrastructure without evidence
```

The additional governing principle is:

```text
maximum effect from the minimum sufficient conditions
```

This principle is evaluated against the **desired clean system**, not merely the currently accumulated live device state.

The distinction is important:

```text
minimum change to the current dirty state
    !=
minimum required state for a clean reconstruction
```

An installed package, path, cache, font, provider, or helper may be easy to keep because it is already present. That does not make it a required clean-system dependency.

## Clean-state definition

The final implementation should be judged against a declared clean baseline.

### Host baseline

```text
fresh Termux application state
    +
only explicitly declared Termux repositories/packages
    +
repository checkout and external artifacts with recorded identity
```

### glibc world baseline

```text
explicit package-manager-owned world substrate
    +
explicit shared world providers/bridges
    +
no undeclared shell/environment accumulation
```

### Debian warehouse baseline

One of the following must be chosen explicitly:

```text
A. reproducible minimal rootfs base
   + declared package delta

B. disposable package-resolution/extraction warehouse
   that is not retained after selected artifacts are materialized

C. exact retained package artifacts
   extracted without installing a persistent expanded rootfs
```

The current installed rootfs is evidence and a supply oracle. It is not yet a clean-state specification.

### Application-domain baseline

```text
application payload identity
    +
protected world references
    +
selected immutable provider/data generation
    +
application-owned mutable state
    +
explicit bridges and feature policy
```

### Clean acceptance

A final accepted application domain should be reproducible and runnable without accidental authority from:

```text
broad farm
undeclared rootfs packages
rootfs absolute runtime paths
normal user state
historic experiment caches
current checkout mutation
```

## Executive verdict

The selected-Obsidian work remains **architecturally productive and mostly aligned**.

The strongest cumulative improvement is:

```text
broad rootfs/farm runtime
    ->
explicit app-local references
+ protected world references
+ selected immutable provider/data bytes
+ receipt-owned mutable state
+ class-based runtime acceptance
```

The next pixbuf diagnostic is a valid discriminator **only if it remains diagnostic** and does not make the currently installed rootfs the final source/runtime authority.

However, the selected generation is not yet clean-state reproducible.

The major current gap is:

```text
runtime authority:
    mostly selected and explicit

supply authority:
    still absolute paths in the currently expanded rootfs/prefix
```

The project must close this gap before:

```text
rootfs font/package cleanup;
unified replacement generation publication;
`current` activation;
claiming clean setup reproducibility.
```

## Cumulative progress judgment

### Phase B1 — locality and retained identity

Accepted result:

```text
161 semantic objects
136 candidate-relevant paths hash-stable
0 APP_LOCAL/external lookup collisions
0 unresolved or ambiguous captured DT_NEEDED edges
```

The decision to preserve `$ORIGIN`/AppDir locality is correct.

The absence of a collision in one receipt is not permission to remove locality precedence. Future candidates must continue to reject external collisions.

### Phase B2 — static/runtime partition

Accepted result:

```text
113 ELF objects
95 entrypoint-static closure
98 all-app-local static closure
15 mapped-only dynamic/discovery objects
17 non-ELF data objects
```

Separating mapped-only dynamic roots and non-ELF capabilities from static closure is correct.

### Phase B3/B4 — capability and entrypoint grouping

Accepted result:

```text
graphics Vulkan dynamic family
NSS/security dynamic family
heterogeneous entrypoint-static capabilities
data capabilities separate from ELF
```

The project correctly avoided naming one large static set a universal shared provider merely because it was reachable.

### Phase B5/B6 — data provenance

Particularly strong results:

```text
locale tied to world glibc
four exact font files identified with package provenance
37 exact schema source files
native Termux glib-compile-schemas identity
byte-identical GSettings aggregate reproduction
no rootfs compiler package installation
```

Using the already available native compiler instead of installing `libglib2.0-bin` into the rootfs is an exemplary maximum-effect/minimum-condition decision.

### Phase B7 — complete semantic disposition

Accepted result:

```text
all 161 paths classified
all 113 ELF paths accounted
91 selected ELF candidates
4 selected fonts
1 generated schema
mutable/cache/device classes excluded or referenced
```

This is a complete accounting of the retained control.

It is not yet proof that every selected item is a minimum clean-system requirement.

### Phase B8/B9 — immutable materialization

Accepted result:

```text
content-addressed object store
same-filesystem staging
generation-local relative aliases
no-overwrite publication
explicit validation before activation
96 hash-correct content objects
175 collision-free aliases
1851/1851 structural checks
`current` unchanged
```

The materializer failures were handled correctly:

```text
hard-link EACCES
    -> no-overwrite renameat2 object publication

frozen-root directory rename EACCES
    -> explicit probe, narrow root thaw, no-overwrite publication, refreeze/fsync
```

The failure receipts were preserved and did not trigger broad redesign or unsafe fallback.

### Phase B10 — runtime and map semantics

Accepted result:

```text
exec-only candidate loader injection
short transaction-owned socket/runtime paths
passive main/renderer/zygote topology
100-second passive survival
no GPU process
zero broad-farm/rootfs/current mappings
class-based map acceptance
```

The correction from one exact object count to semantic classes is important.

```text
all selected content exists and is hash-correct
    !=
all selected data must map in every scenario
```

### Interactive capability

Still open:

```text
vault-open GTK file chooser
pixbuf loader/cache
icon-theme data
MIME database
```

The plan to test a relocated loader cache first and add icon data only as a separate discriminator is directionally correct.

## Strong alignment with project philosophy

### 1. No broad production mutation

The work remained under experiment ownership.

```text
modules/
packages/
tests/
tools/
promoted launchers
current pointer
```

were not changed by the selected-generation investigation.

### 2. One variable at a time

Observed failures were separated into:

```text
launcher-shell ABI contamination
Unix socket path length
passive versus interactive input
GTK pixbuf/icon handling
map identity versus ownership selection
```

This avoided compensating for multiple causes at once.

### 3. Existing generation immutability

The project did not patch or rewrite the published generation after discovering:

```text
Xau/Xdmcp world selection
missing demand-loaded Bold font map
libX11-xcb CPU mapping
app-local SwiftShader mapping
```

The next generation will incorporate corrected semantics as one new object.

### 4. RPATH patch rejected

The decision not to patch selected consumers is operationally sound:

```text
actual selected/world bytes identical
actual loader path understood
world reference already allowed
ELF transformation would create new identities and validation work
```

The no-patch decision is accepted.

### 5. No package install to close evidence gaps

The schema gap was solved from native compiler capability instead of expanding the rootfs.

The pixbuf stage also currently forbids installing packages or copying the whole rootfs data tree.

## Critical gap 1 — installed rootfs paths are still supply authority

The current materializer rechecks absolute source paths before every generation build.

The checked sources include:

```text
selected ELF paths
selected rootfs font paths
rootfs GSettings source paths
native schema compiler path
```

The B9 materializer refuses to proceed if any accepted source path is missing, even when the corresponding content-addressed object already exists and is hash-correct.

Consequences:

```text
existing generation runtime:
    can survive source removal because bytes are already in the object store

next generation synthesis/materialization:
    still depends on the currently installed source tree

clean Termux reset:
    cannot reproduce the generation from the repository alone
```

This is not a defect in the experiment receipt. It is an unclosed supply-layer contract.

### Required correction

Introduce a supply manifest separate from runtime semantic disposition.

For every externally acquired input, capture one of:

```text
exact package artifact SHA-256 + package metadata;
content-addressed retained source object;
reproducible source/build artifact identity;
explicit world-package identity managed by the substrate backend.
```

The materializer should consume a staged acquisition root or content object, not depend forever on the mutable installed warehouse pathname.

## Critical gap 2 — rootfs base and mutation delta are unknown

The current documents identify package ownership of selected files, but they do not establish:

```text
original minbase package set
manual package additions
automatic dependency additions
install dates/commands
packages installed only for font experiments
packages installed for VS Code/Obsidian closure
packages now unused by any accepted supply manifest
```

This prevents a safe answer to:

```text
which packages can be purged now?
what is the original state?
what must a clean setup install?
```

The rootfs is broader than a font issue. Fonts are the visible example of a general warehouse mutation-ledger gap.

### Required immediate evidence

Before any removal, capture read-only:

```text
full dpkg package/version/status manifest
apt manual marks
apt automatic marks
apt history logs
dpkg logs
package policy/origin for selected font/schema/pixbuf packages
reverse installed dependencies
font/config/cache path inventory
selected file owner/version/hash mapping
```

If apt history is incomplete or rotated, the package state can still be captured, but exact original intent may remain partially unknown. That uncertainty must be documented rather than guessed.

## Critical gap 3 — selected fonts are sufficient observations, not proven minimum conditions

The current selected font set is:

```text
NotoSansCJK-Regular.ttc
DejaVuMathTeXGyre.ttf
DejaVuSansMono.ttf
DejaVuSansMono-Bold.ttf
```

The project proved:

```text
all four bytes exist and have package provenance;
three were mapped in the passive selected-generation run;
the Bold file was not demanded in that passive scenario.
```

It did not prove:

```text
all four are required for the clean workstation contract;
no smaller set provides the desired UI/language/editor coverage;
the original control mapping was unaffected by previous rootfs font installation;
one passive scenario represents interactive vault/file-chooser font needs.
```

### Correct minimum-condition question

First define desired effects:

```text
Latin UI text
monospace/code text
bold monospace when actually required
Korean/CJK coverage
math glyph coverage
fallback behavior
```

Then derive the smallest selected file set that satisfies those declared effects across required scenarios.

```text
mapped once
    != required

not mapped once
    != unnecessary
```

The current four-font set is a valid provisional selected provider. It is not yet the final minimum clean-state font contract.

## Critical gap 4 — generation identity conflates causal axes

The current generation digest includes:

```text
B7 repository head
absolute generation base
content rows including absolute source paths/package/version
schema source absolute paths/owners
compiler absolute path and identity
```

This has two problems.

### Path/provenance over-coupling

The same immutable bytes and alias namespace can receive a different generation ID merely because:

```text
installation base changes
source extraction path changes
package provenance representation changes
compiler path changes while compiler bytes remain identical
```

### Composition under-representation

The ID does not directly and completely identify:

```text
application payload bytes
protected world substrate/provider bytes
world locale identity
launcher/policy identity
validation policy identity
open interactive capability status
```

Therefore the current ID is neither:

```text
pure immutable-content identity
```

nor:

```text
complete application-domain composition identity
```

### Required identity split

Use separate causal identities.

```text
content generation identity
    selected object hashes
    generated artifact hashes
    alias namespace / relative layout contract

supply/provenance identity
    package artifacts, source inputs, compiler/build receipts

runtime composition identity
    content generation
    application payload
    protected world identities
    launcher/feature/bridge policy

installation/activation identity
    deployment base
    active current target
    previous target

validation-policy identity
    gate definitions and scenario requirements
```

Do not redesign or rename the already published B9 generation. Apply this split to the unified successor design before activation.

## Critical gap 5 — rollback is scoped more narrowly than the application domain

The current pointer contract can roll back:

```text
selected provider/data generation
```

It cannot roll back:

```text
glibc substrate
protected world X11/provider packages
application payload
launcher source
user state
```

This is acceptable only when named accurately.

```text
generation rollback
    !=
application-domain rollback
```

Activation receipts must bind the selected generation to the external composition identities it was validated against.

## Critical gap 6 — Xau/Xdmcp no-patch decision is correct, class name is too strong

The evidence proves:

```text
loader selects $PREFIX/glibc/lib paths
selected/world bytes are identical
selection follows exact absolute RPATH edges
```

It does not prove that `libXau` and `libXdmcp` are glibc **substrate**.

Earlier architecture already established:

```text
prefix/package location
    != semantic substrate ownership
```

Recommended semantic class:

```text
PROTECTED_WORLD_X11_SUPPORT
```

or:

```text
REFERENCE_WORLD_PREFIX_PROVIDER
```

rather than:

```text
PROTECTED_WORLD_SUBSTRATE
```

This is a naming/ownership correction only.

Keep the accepted operational decisions:

```text
no RPATH patch
no duplicate next-generation materialization
no current-generation mutation
exact hash/edge allowlist
```

## Critical gap 7 — the pixbuf diagnostic is not the final minimum capability

Using one relocated cache that references all twelve currently installed rootfs loader modules is acceptable as a coarse diagnostic.

It must not be promoted directly as the final selected capability.

After the discriminator, the project must identify:

```text
which loader modules were actually opened/mapped
whether the cache itself is necessary
whether embedded PNG support is independent of external modules
which icon-theme index/files are required
which MIME files are required for vault selection
which generated files need reproducible source/build contracts
```

The final generation should contain the minimum reproducible capability, not the full inventory merely because it fixed the interaction.

## Critical gap 8 — experimental implementation must not become the clean operational surface

The selected-closure recipe tree intentionally contains:

```text
phase-specific analyzers
failure-specific corrected wrappers
hardcoded receipt counts
exact status-string transitions
absolute device paths
historical failed implementations
```

This is appropriate for discovery and evidence preservation.

It is not the desired final installed tooling.

After the pilot closes, classify and reduce the operational surface to something like:

```text
manifest/supply resolver
canonical materializer
canonical explicit validator
activation/rollback command
read-only status/doctor command
```

Historical phase scripts remain experiment evidence and are not deployed.

Hardcoded counts such as:

```text
161
113
96
175
1851
125
```

must remain receipt assertions, not reusable architecture constants. Final validators derive expected sets from manifests and class policy.

## Critical gap 9 — refactor index drift

At the audited commit:

```text
docs/refactor/README.md
    current state still says Phase B1 is next
    index stops its current direction at 0093
```

while canonical status and selected experiment README have advanced through `0112`.

This violates the repository rule that the current index is authority.

The index must be synchronized as part of this audit branch.

## Font-package cleanup decision

### Desired result

The clean final architecture should not require a permanently expanded Debian rootfs merely to supply fonts.

The selected generation already demonstrates the correct runtime direction:

```text
exact selected font files
receipt-owned fontconfig
no rootfs provider mappings
```

### Current safe conclusion

Do not purge the rootfs font packages yet.

Reason:

```text
1. rootfs package/manual history has not been captured;
2. next-generation materializer still requires current font source paths;
3. the open pixbuf diagnostic still uses the current rootfs as a source oracle;
4. current promoted broad-farm/rootfs-based launchers may still consume rootfs fontconfig/data;
5. exact package artifacts for clean reconstruction have not been retained as supply objects.
```

Removing the packages now would not corrupt the existing immutable generation, but it could:

```text
break source preflight for the unified successor generation;
change the current non-candidate daily runtime;
remove evidence needed to determine the exact original delta;
make rollback to the present supply state harder.
```

### Correct cleanup sequence

```text
1. capture read-only rootfs package/mutation inventory;
2. retain exact selected package artifacts or equivalent source objects;
3. complete the controlled pixbuf/icon/MIME diagnosis with no new installs;
4. define the minimum font and GTK data/plugin capabilities;
5. materialize and validate the unified successor generation;
6. prove passive and interactive acceptance with no rootfs/broad-farm runtime authority;
7. prove clean reconstruction from the locked supply manifest;
8. then purge the accidental rootfs delta or recreate the rootfs from the declared minbase baseline;
9. repeat acceptance after cleanup;
10. later repeat the entire setup after the planned Termux reset.
```

### Cleanup target

The preferred final state is not necessarily a manually purged long-lived rootfs.

A stronger design is:

```text
minimal/disposable warehouse
    -> resolve/download exact package artifacts
    -> extract selected bytes into a staged supply root
    -> materialize content-addressed providers
    -> warehouse may be removed or recreated
```

This turns PRoot/Debian from an accumulated subsystem into a reproducible supply adapter.

## Required clean-state gates

Before final activation, add these architecture gates.

### Clean supply manifest gate

```text
all selected external bytes trace to exact retained/acquirable artifacts;
package artifact hashes are recorded;
source extraction paths are disposable;
no final build requires an undeclared installed rootfs package.
```

### Warehouse-offline runtime gate

```text
accepted launcher environment contains no rootfs paths;
no broad-farm/rootfs provider mapping;
no required file opens from rootfs during passive and interactive scenarios;
```

The mechanism may be file-open tracing, a controlled unavailable warehouse, or another evidence-backed method. Map absence alone is insufficient for short-lived data reads.

### Clean reconstruction gate

```text
start from declared clean host/world/warehouse state;
acquire locked inputs;
materialize the same content generation;
reproduce expected identities;
pass passive and interactive workload gates.
```

### Undeclared mutation gate

```text
compare final package/manual-state manifests with declared baseline + allowed delta;
report every undeclared installed package or persistent runtime file class.
```

## Revised immediate execution order

### Phase C0 — clean-state supply inventory

Read-only, no install/remove:

```text
capture rootfs package state and apt/dpkg history;
identify manually installed font packages;
identify dependency and reverse-dependency relations;
capture package origins/versions;
capture selected source-file ownership and hashes;
record current promoted runtime dependence on rootfs font/data paths.
```

### Phase C1 — controlled pixbuf diagnostic

Proceed with the currently planned diagnostic after C0:

```text
same immutable generation
short receipt-owned runtime paths
receipt-local relocated loader cache
exact existing rootfs modules as diagnostic-only sources
one declared vault-open interaction
no package install
no generation mutation
```

### Phase C2 — minimum capability derivation

```text
separate loader cache/modules, icon theme, and MIME effects;
record actual use;
derive the minimum reproducible set;
revisit the four-font set against declared clean-state requirements.
```

### Phase C3 — supply and identity redesign

```text
lock package/source artifacts;
separate content/provenance/composition/installation identities;
rename Xau/Xdmcp semantic ownership class;
make manifest synthesis independent of installed rootfs paths.
```

### Phase C4 — unified successor generation

```text
remove Xau/Xdmcp duplicate objects;
add only the proven minimum GTK data/plugin delta;
include the final selected font contract;
produce one new immutable generation;
leave the existing generation unchanged.
```

### Phase C5 — acceptance

```text
passive startup/topology/survival/maps;
interactive vault-open/file chooser;
class-based selected/world/app/data acceptance;
warehouse/rootfs runtime independence;
current unchanged.
```

### Phase C6 — activation and cleanup

Only after all previous phases:

```text
bind composition identities;
atomically activate current;
prove generation-scoped rollback;
remove/recreate accidental rootfs package delta;
repeat acceptance;
```

## Stop lines

Do not:

```text
purge rootfs font packages before the package/mutation inventory;
install another package to make the pixbuf diagnostic pass;
treat all twelve pixbuf modules or all icon/MIME files as final merely because a broad diagnostic passes;
retain four fonts by observation inertia without a declared coverage contract;
remove Bold merely because one passive scenario did not map it;
call Xau/Xdmcp glibc substrate solely because the prefix path won;
use the current generation digest as a complete application-domain identity;
activate current before supply and composition identities are separated;
claim clean reproducibility from the current installed rootfs;
carry phase-specific wrapper layers into the final deployed tool surface;
use exact receipt counts as architecture constants;
reset Termux before external payloads, selected objects, package artifacts, and clean bootstrap contracts are preserved.
```

## Final judgment

The cumulative work has successfully moved the project from:

```text
broad compatibility farm
```

toward:

```text
explicit immutable application-domain composition
```

The next top-down correction is to move from:

```text
selected runtime bytes copied from the current warehouse
```

to:

```text
selected runtime bytes reproducible from a minimal locked supply contract
```

The rootfs font regret is therefore not an isolated cleanup issue. It reveals the missing clean-state supply layer.

The correct response is not immediate deletion and not permanent retention. It is:

```text
inventory
    -> lock exact supply
    -> prove minimum capability
    -> reproduce selected generation
    -> remove warehouse authority
    -> clean/reset acceptance
```
