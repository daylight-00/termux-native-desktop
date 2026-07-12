# Repository Refactor and Architecture Work Log

This directory is the transaction-level source of truth for the migration from the original prototype toward explicit ownership, semantic provider authority, locked supply identities, clean runtime composition, and controlled activation.

## Working rule

```text
session narrative
    != authority

repository evidence + current canonical index
    = authority
```

Historical numbered records remain intact when later audits narrow or supersede their interpretation.

## Current checkout and branch

```text
checkout:
    $HOME/projects/termux-native-desktop

active architecture branch:
    docs/post-graphics-architecture-audit
```

The historical `$HOME/termux-native-desktop` path is evidence only.

## Current authority and precedence

Top-down foundation on `main`:

```text
docs/system-foundation/01-essence.md
docs/system-foundation/02-principles-and-invariants.md
docs/system-foundation/03-system-model-v2.md
docs/system-foundation/05-ideal-target-architecture.md
docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
docs/system-foundation/12-document-consistency-audit-and-execution-order.md
```

Current branch-local authority:

```text
0116-end-to-end-architecture-audit-and-provider-authority-intervention.md
    full-project intervention and provider-source authority requirements

0115-proot-oracle-supply-and-baseline-model.md
    PRoot/rootfs as reproducible oracle and supply mechanism

0112-selected-obsidian-passive-map-selection-diagnostic-pass-and-contract-decision.md
    accepted passive runtime and map facts

0117-provider-authority-intervention-adoption-and-execution-order.md
    provider-authority workstream order

0118-selected-obsidian-provider-authority-census-schema-and-evidence-plan.md
    census schema and evidence plan

0119-selected-obsidian-provider-authority-n2-read-only-evidence-collector.md
0120-selected-obsidian-provider-authority-n2-device-receipt-review.md
    read-only provider evidence

0123-selected-obsidian-provider-authority-corrected-n3-receipt-pass-and-source-comparison-entry.md
0128-selected-obsidian-provider-authority-source-recipe-receipt-pass.md
0131-selected-obsidian-provider-authority-binary-artifact-receipt-pass.md
    normalized classification, source recipe and exact binary supply evidence

0132-evidence-storage-and-android-downloads-handoff-boundary.md
    Termux-private work state versus explicit Downloads handoff

0133-selected-obsidian-priority-provider-authority-review.md
    bounded priority package/object review

0134-selected-obsidian-provider-profile-locked-member-draft.md
    exact non-materializing provider-fragment member locks

0135-selected-obsidian-provider-profile-lock-draft-architecture-audit.md
    current correction authority for global coverage, semantic-state separation,
    alias authority, provider-fragment semantics, and target-layout ordering
```

Precedence:

```text
system-foundation
    -> constitutional intent and invariants

0116
    -> controlling provider-authority intervention

0115
    -> oracle/supply/baseline lifecycle

0112
    -> accepted bounded runtime facts

0117-0134
    -> evidence transactions and bounded draft decisions

0135
    -> current audit corrections and next-state authority

other numbered records
    -> chronological evidence and transaction history
```

## Current state

```text
repository ownership migration:
    DEPLOYED / RETAINED

ABI incident recovery:
    CLOSED FOR TESTED WORKLOAD

selected D-Bus pilot:
    PASS

scoped graphics-policy transaction:
    CLOSED

selected Obsidian B1-B8:
    CLOSED

first immutable selected generation:
    PUBLISHED / UNACTIVATED

passive startup/topology/100-second survival/maps:
    PASS

provider-authority evidence collection:
    PASS FOR BOUNDED PRIORITY SET

exact priority artifact/member supply locks:
    PASS

package-wide runtime inference:
    REJECTED

provider semantic authority:
    PARTIAL / CORRECTION REQUIRED

provider fragments:
    NON-MATERIALIZING DRAFT PASS

global authority coverage:
    OPEN

target-layout schema:
    ALLOWED TO DESIGN

target-layout population:
    BLOCKED

successor materialization:
    BLOCKED

current activation:
    BLOCKED

clean reconstruction:
    NOT PROVEN

PyMOL runtime implementation:
    DEFERRED
```

## Current provider-authority evidence

```text
priority package dispositions:
    28 / 28

bounded priority selected/reference objects:
    59 / 59

exact artifacts:
    28

artifact data members compared:
    6,887

artifact member mismatches:
    0

unique reviewed object identities:
    59

provider-fragment memberships:
    63

artifact alias rows:
    93

locked member rows:
    156

profile/artifact edges:
    35
```

These are bounded supply and review counts. They are not the complete application-domain authority denominator.

## Current correction summary

The post-`0134` audit requires:

```text
59/59 priority coverage
    != complete selected/reference authority coverage

exact Termux artifact supply
    != automatic final provider-source authority

Termux package origin
    != automatic platform-integration semantic role

package-provided symlink
    != required runtime alias

artifact mode/path
    != target mode/path

provider fragment membership
    != deployable runtime profile

96 first-generation content identities
    != application-local identities
```

The current member locks remain valid exact supply evidence.

## Required normalized model

```text
SupplyArtifact
    exact artifact identity, acquisition/trust and recipe-binding state

ProviderObjectAuthority
    canonical content identity and semantic/provider decision states

ProviderFragmentMembership
    many-to-many capability/profile pressure edges

RuntimeAliasAuthority
    SONAME, proven dlopen, loader, development, internal or unresolved alias

ApplicationRuntimeComposition
    accepted include/reference decisions, target domains and validation gates

TargetLayout
    target paths/modes/owners populated only after authority acceptance
```

Required authority-state separation:

```text
semantic_role_state
termux_android_adaptation_state
candidate_source_comparison_state
exact_supply_artifact_state
artifact_to_recipe_binding_state
profile_necessity_state
provisional_final_provider_state
```

## Current unresolved authority groups

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

Execution order:

```text
P0 correct terminology and complete authority denominator;
P1 split semantic/adaptation/source/supply/necessity/final states;
P2 classify artifact aliases and define target-independent mode policy;
P3 create canonical artifact/object registries and fragment edges;
P4 map every unreviewed capability/object to an authority issue;
P5 resolve base XCB narrative and membership ambiguity;
P6 define target-layout schema and invariants only;
P7 close world, application, generic and data authority;
P8 populate target paths only after ownership acceptance;
P9 perform intervention-lift audit before materializer design.
```

## End-to-end chronological index

```text
0001-0011
    repository ownership migration

0012-0025
    ABI incident, substrate authority and package-managed recovery

0026-0028
    selected D-Bus provider pilot

0029-0091
    Obsidian control, semantic decomposition and closed graphics transaction

0092-0093
    post-graphics synthesis and selected-pilot re-entry

0094-0103
    selected-Obsidian semantic closure and generation design

0104-0106
    immutable generation publication

0107-0112
    explicit-generation runtime, passive survival/maps and map-contract correction

0113-0116
    clean-state, PRoot/oracle and provider-authority intervention

0117-0123
    census schema, N2 evidence and corrected N3 normalization

0124-0128
    source-recipe evidence and bounded source review

0129-0132
    exact binary artifact comparison and storage boundary

0133-0134
    bounded priority authority review and exact member-lock fragments

0135
    architecture audit of coverage, authority states, aliases and target ordering
```

## Runtime and research profiles

### Minimum workstation runtime profile

Contains only accepted promoted runtime objects, application domains, data providers, validation/status surface, rollback surface and user state.

It does not automatically contain:

```text
PRoot or a Debian rootfs;
GCC/compiler packages;
binutils/sysroots/headers;
glibc-runner;
build dependencies;
oracle-only packages;
package-wide provider surfaces.
```

### Research/build/maintenance profile

May contain:

```text
PRoot tooling and pinned oracle scenarios;
APT/dpkg acquisition and metadata tools;
gcc-glibc and explicit target wrappers;
build Python/Meson/Ninja;
artifact inspection and validators;
historical evidence receipts.
```

## Update domains

```text
world substrate update
provider update
application update
toolchain update
oracle scenario update
```

Each has independent identity, gates, dependents, promotion and rollback scope.

## Evidence handoff

Every evidence-producing stage uses a unique stage-specific output root and archive identity. Generic archive names are rejected.

```bash
out="<specific-stage-name>-$(date +%Y%m%d-%H%M%S)"
OUT="<stage-output-root>/$out"
tar czf ~/Downloads/$out.tgz $OUT
```

## Current stop lines

Do not:

```text
treat 59/59 as global authority completion;
treat all `$PREFIX/glibc` objects as world or platform authority;
treat exact artifact supply as final generic-provider choice;
copy all package aliases or artifact modes into a target;
consume provider fragments as extraction manifests;
call the 96 first-generation contents application-local;
populate target paths before ownership closes;
materialize or activate a successor;
create or change current;
install/remove/update packages or run maintainer scripts;
mutate loader state or patch RPATH;
promote conditional fragments by availability;
reopen closed graphics work;
turn audit findings into runtime implementation without explicit authorization.
```

## Refactor lineage

```text
original refactor branch:
    refactor/module-package-layout

base:
    3cf41d6fc47050b06e18e956a23cefe25e4fb82a

selected-Obsidian state audited by 0116:
    6c00ac7f9ca46bc2159c51689904e154146f0d2a

provider-profile draft audited by 0135:
    9bc7e9ffb92cf5d7b1095508e8a21438026656cd

current architecture branch:
    docs/post-graphics-architecture-audit
```
