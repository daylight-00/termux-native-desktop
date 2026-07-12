# Repository Refactor and Architecture Work Log

This directory is the transaction-level source of truth for the migration from the original prototype toward explicit ownership, semantic composition, selected immutable providers, clean supply contracts, and controlled activation.

## Working rule

```text
session narrative
    != authority

repository evidence + current canonical index
    = authority
```

Historical records remain intact when later evidence supersedes their interpretation or implementation.

## Current checkout root

```text
$HOME/projects/termux-native-desktop
```

The historical `$HOME/termux-native-desktop` path is evidence only and must not return as a compatibility identity.

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
    -> full-project judgment, provider-source authority gap,
       toolchain/runtime separation, update domains, and immediate intervention

0115-proot-oracle-supply-and-baseline-model.md
    -> PRoot as reproducible oracle/supply mechanism rather than workstation baseline

0114-debian-baseline-correction-native-font-pressure-and-auditor-boundary.md
    -> native-font pressure and auditor-role boundary

0113-clean-state-minimum-condition-and-supply-authority-audit.md
    -> clean-product minimum conditions, supply identity, and cleanup ordering

0112-selected-obsidian-passive-map-selection-diagnostic-pass-and-contract-decision.md
    -> passive runtime/map facts and corrected map contract

0110-selected-obsidian-pixbuf-inventory-pass-and-interaction-boundary-correction.md
    -> passive/interactive split and GTK capability inventory

0106-selected-obsidian-phase-b9-generation-materialization-pass.md
    -> first immutable selected CPU generation

0092-post-graphics-closure-architecture-midpoint-audit.md
0093-post-audit-direction-validator-lifecycle-and-selected-closure-reentry.md
    -> post-graphics synthesis, validator lifecycle, and parent-pilot continuation

0091-scoped-graphics-policy-promotion-closure.md
    -> closed graphics-policy transaction

0015-0019
    -> semantic hard-refactor, substrate authority, and selected-closure criteria
```

Precedence:

```text
system-foundation
    -> project essence and constitutional invariants

0116
    -> current full-history audit and intervention authority

0115 / 0114 / 0113
    -> oracle, native-font, clean-state, and supply pressure

0112 / 0110 / 0106
    -> accepted bounded selected-generation evidence

0092 / 0093
    -> post-graphics direction

0091
    -> closed graphics contract

0015-0019
    -> semantic foundations

other numbered records
    -> chronological evidence and transaction history

0014
    -> retained candidate/validation/rollback principles only;
       concrete broad-farm/pacman/gl-run lifecycle sequence is superseded
```

## Current state

```text
repository ownership migration:
    DEPLOYED / RETAINED

ABI incident recovery:
    CLOSED FOR TESTED WORKLOAD
    newer substrate lifecycle still open

selected D-Bus provider pilot:
    PASS

scoped graphics-policy promotion:
    CLOSED

selected Obsidian phases B1-B8:
    CLOSED

first immutable selected CPU generation:
    PUBLISHED / UNACTIVATED

passive startup/topology/100-second survival/maps:
    PASS

passive map-selection diagnosis:
    PASS

interactive vault-open GTK capability:
    OPEN

PRoot oracle/supply model:
    CORRECTED

provider-source authority:
    OPEN / IMMEDIATE INTERVENTION

unified successor generation:
    BLOCKED

atomic current activation:
    NOT STARTED

clean reconstruction:
    NOT PROVEN

PyMOL runtime implementation:
    DEFERRED
```

## End-to-end chronological index

### 0001–0011 — source ownership migration

The initial refactor inventoried the legacy tree, separated modules/packages/experiments/tools, moved application launchers to package owners, preserved external/generated state, and deployed the source-ownership change with validation.

Decision:

```text
KEEP
```

Limitation:

```text
modules/gl remained a transitional physical umbrella
```

### 0012–0014 — ABI incident and first lifecycle proposal

The libdbus/glibc incident proved that provider compatibility depends on world-substrate ABI and that farm regeneration cannot repair a broken substrate.

`0014` contains useful transaction principles but its broad-farm/pacman/gl-run lifecycle is superseded.

### 0015–0019 — architecture reassessment

The project established:

```text
world/provider/bridge/application/toolchain/supply ownership
modules/gl as transitional
broad farm as research/control
backend-neutral substrate adapter
selected-closure pilot criteria
```

### 0020–0025 — package-managed glibc recovery

Exact artifact inspection, downgrade simulation, package-managed recovery, corrected core/provider gates, and real VS Code recovery closed the tested incident.

The active device backend was identified as Termux APT/dpkg without making architecture APT-specific.

### 0026–0028 — selected D-Bus provider pilot

A bounded selected provider candidate proved:

```text
immutable provider bytes
provenance
candidate-specific actual selection
protected-world exclusion
zero broad-farm/rootfs leakage
control equivalence
```

### 0029–0041 — Obsidian control and semantic decomposition

The project captured a real Electron multiprocess application domain and separated app-local, world, prefix, rootfs, data, state, and graphics relations.

### 0042–0075 — graphics architecture discrimination

The project separated provider discovery, provider selection, device intent, consumer suitability, mapped participation, and actual selected-device identity across standalone Zink, Obsidian, and VS Code controls.

### 0076–0091 — scoped graphics promotion

World-boundary sanitation, consumer-scoped provider/bridge composition, application GPU/CPU mode, isolated application state, and selected-device correlation were promoted and closed.

Current helper/path names were not accepted as permanent architecture.

### 0092–0093 — post-closure synthesis

Graphics experiment expansion stopped. Validators were classified by lifecycle, and the selected Obsidian parent pilot resumed.

### 0094–0103 — selected-Obsidian semantic closure and generation design

The project established locality, static/runtime partition, capability grouping, selected data provenance, reproducible GSettings output, complete disposition, and content-addressed generation design.

### 0104–0106 — generation materialization

Publication failures were isolated and corrected without unsafe fallback. One immutable generation with 96 content identities and 175 aliases was published but not activated.

### 0107–0112 — explicit-generation runtime validation

The project corrected launcher contamination and socket-path assumptions, proved passive topology/survival/maps, isolated the GTK interactive gap, and replaced an exact mapped-object count with class-based acceptance.

### 0113–0115 — clean-state and PRoot model correction

The project distinguished clean-product minimality from current-state minimality and redefined PRoot/rootfs as oracle/supply scenarios rather than workstation baselines.

The current Debian-derived font set remains transition evidence, not final font authority.

### 0116 — end-to-end provider-authority intervention

The project is on track, but the next unified generation is blocked because the complete selected/reference set has not yet been resolved against the final provider authority hierarchy.

Key correction:

```text
working selected path
    !=
final reference-quality provider decision
```

## Current semantic authority model

```text
native host authority
    Android/Termux bionic and native integration

world core substrate
    glibc loader/libc/tightly coupled runtime only

platform-integration provider
    Termux/Android-sensitive glibc providers and explicit bridges

generic capability provider
    D-Bus, GTK, fontconfig, pixbuf, TLS, NSS, audio, printing, etc.

application-local
    valid upstream AppDir/$ORIGIN payload

application-domain supplement
    bounded app/family-specific selected closure

data capability provider
    fonts, locale, schemas, icons, MIME, trust data

toolchain-only
    compiler/binutils/sysroot/build tools

oracle-only
    Debian scenario packages and controls not promoted into runtime
```

Repository or filesystem location is not sufficient to assign one of these classes.

## Immediate intervention

### Allowed bounded work

The current pixbuf vault-open diagnostic may continue only as:

```text
named diagnostic/oracle capability experiment
same immutable unactivated generation
no package install
no generation mutation
no current activation
no promoted launcher change
rootfs inputs treated as diagnostic-only
```

### Blocked work

```text
unified successor manifest finalization
successor generation materialization
current activation
clean runtime package-list declaration
provider cleanup based only on prefix/rootfs path
```

### Required provider-authority audit

For every selected/reference runtime object and relevant current glibc-prefix package, record:

```text
semantic class
minimum scope
current provenance
candidate sources
Termux/Android adaptation rationale
app-local relation
ABI/version relation
dependent domains
runtime or research profile
update owner/trigger
provisional final authority
```

### Required source-choice order

```text
semantic role
    -> relevant reference
    -> candidate comparison
    -> provider choice
    -> locked supply artifact
    -> update/revalidation contract
    -> successor composition
```

## Runtime and research profiles

### Minimum workstation runtime profile

Contains only promoted runtime objects and required status/validation surface.

It does not automatically contain PRoot, GCC, `glibc-runner`, broad oracle package state, or build dependencies.

### Research/build/maintenance profile

May contain:

```text
PRoot tooling and pinned oracle scenarios
APT/dpkg metadata/acquisition tools
gcc-glibc and explicit target wrappers
build Python/Meson/Ninja
artifact inspection and validators
```

The existing glibc target wrapper toolchain remains a valid build/supply implementation. It is not a runtime-base decision.

## Update domains

```text
world substrate update
provider update
application update
toolchain update
oracle scenario update
```

Each has independent identity, gates, dependents, promotion, and rollback scope.

The project may remain latest-first in candidate acquisition while keeping active runtime evidence-gated.

## Current stop lines

Do not:

```text
materialize or activate the successor before provider authority is classified;
treat all `$PREFIX/glibc` objects as world substrate;
treat all selected Debian objects as final providers;
use glibc-repo membership as automatic semantic ownership;
use Debian slim defaults as promoted runtime defaults;
retain or install glibc-runner/GCC/fonts/pixbuf in the runtime profile by availability alone;
replace valid app-local objects without evidence;
turn the pixbuf diagnostic into final provider selection;
reopen closed graphics work;
mutate the existing generation;
create current before provider/supply/composition/activation/rollback contracts close;
turn audit findings into implementation without an explicit role change.
```

## Evidence handoff

Every evidence-producing stage uses a unique stage-specific output root and archive identity. Generic archive names are rejected.

## Refactor lineage

```text
original refactor branch:
    refactor/module-package-layout

base:
    3cf41d6fc47050b06e18e956a23cefe25e4fb82a

selected-Obsidian state audited:
    6c00ac7f9ca46bc2159c51689904e154146f0d2a

current architecture-audit branch:
    docs/clean-state-minimum-condition-audit
```

The foundation documents exist on `main`; branch-local absence never makes them irrelevant. Histories must be reconciled deliberately before final integration.
