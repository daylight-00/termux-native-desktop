# 0116 — End-to-End Architecture Audit and Provider-Authority Intervention

## Status

This record audits the project from the original prototype and ownership refactor through the current selected-Obsidian generation work.

```text
scope:
    pre-refactor prototype
    0001 -> 0115
    system-foundation
    current selected-generation design
    PRoot/oracle/supply model
    provider-source authority
    toolchain and update lifecycle

verdict:
    PROJECT DIRECTION ON TRACK
    IMMEDIATE BOUNDED INTERVENTION REQUIRED

runtime implementation:
    NO

package operation:
    NO

generation mutation or activation:
    NO
```

The intervention does not discard the current selected generation and does not reopen closed graphics work.

It prevents the next unified generation from promoting provider choices that were inferred from the historical control environment but not yet justified against the final reference/authority model.

## Philosophy used for the audit

### Idea-directed design

The final system is not defined by the first working mechanism or the current accumulated device state.

```text
prototype
    -> evidence
    -> essence
    -> object model
    -> corrected implementation
```

A successful prototype remains evidence, not constitutional authority.

### Maximum effect from minimum sufficient conditions

The target is not minimum package count in every experiment.

The target is:

```text
minimum persistent authority
minimum promoted dependency surface
minimum hidden accumulated state
minimum policy scope
```

A large disposable oracle scenario can be justified when it answers a valuable question.

A small accidental permanent dependency is not justified merely because it already exists.

### Reference unless deliberate deviation exists

The project should prefer the relevant reference for each responsibility:

```text
Android/Termux integration
    -> native/Termux-adapted reference

ordinary glibc/Linux behavior
    -> upstream or ordinary distribution reference

application-local payload
    -> upstream application topology

package behavior and dependency observation
    -> named Debian oracle scenario

project-specific deviation
    -> explicit rationale, evidence, update scope, and rollback
```

No single repository or distribution is the universal reference for every object.

### Latest/performance preference

The project may acquire and evaluate current candidates aggressively.

```text
latest candidate acquisition
    !=
automatic active runtime replacement
```

The intended model is:

```text
rolling research/supply
    +
evidence-gated promoted runtime
```

## End-to-end audit

## Stage 0 — original prototype and discovery

The original system combined:

```text
Termux native host/session
Termux glibc packages
Debian PRoot/rootfs
broad shared-library farm
one glibc environment file
gl-run
glibc target wrappers
application-specific launchers
```

### What was valid

The prototype answered important first-order questions:

```text
Can glibc applications execute without PRoot mediation?
Can Debian artifacts be consumed passively?
Can Termux:X11 and Adreno/KGSL be reached?
Can VS Code, Obsidian, Conda, and GPU paths work?
```

The rootfs-as-library-pool experiment correctly proved:

```text
supply origin
    can be separated from
process execution authority
```

### What was provisional

The prototype accumulated accidental object boundaries:

```text
one gl umbrella
one broad farm
one shared env
one mutable rootfs
application and capability launchers in one namespace
source-linked live activation
```

These were legitimate discovery mechanisms but not final architecture.

### Audit verdict

```text
PASS AS PROTOTYPE
REJECT AS FINAL OBJECT MODEL
```

## Stage 1 — repository ownership refactor, 0001–0011

The ownership migration separated:

```text
modules
packages
experiments
tools
source definitions
generated/live state
```

It also separated application launchers from generic gl integration and preserved external payloads/build state during migration.

### What was done correctly

```text
inventory before movement
behavior-preserving source moves
repository migration separate from generated-state cleanup
hash-guarded adoption
explicit deployment validation
no destructive cleanup mixed into ownership migration
```

### Limitation

The refactor moved current physical owners before the later semantic object model was complete.

`modules/gl` therefore remained a transitional umbrella.

Later documents correctly rejected physical layout as proof of semantic ownership.

### Audit verdict

```text
PASS
KEEP THE OWNERSHIP WORK
CONTINUE SEMANTIC SPLIT
```

## Stage 2 — ABI incident and substrate authority, 0012–0025

The libdbus/glibc failure revealed that:

```text
provider compatibility
    depends on
world substrate ABI
```

and that farm regeneration cannot repair a broken substrate.

### Strong decisions

```text
substrate lifecycle separated from provider lifecycle
pacman not installed for hook convenience
actual device backend observed as APT/dpkg
exact previous artifact inspected before downgrade
recovery isolated from unrelated refactor
core/provider/application gates separated
```

This phase strongly follows minimum manipulation and evidence-before-promotion.

### Remaining gap

The current Termux glibc package prefix was identified as package-managed authority, but the **entire package set under or feeding `$PREFIX/glibc` was not yet semantically partitioned** into:

```text
world core substrate
platform-integration provider
generic capability provider
compiler/runtime support
toolchain-only package
```

Physical prefix ownership must not become automatic semantic substrate ownership.

### Audit verdict

```text
PASS FOR INCIDENT RECOVERY
PROVIDER-AUTHORITY CLASSIFICATION STILL OPEN
```

## Stage 3 — selected D-Bus pilot, 0026–0028

The pilot proved a real selected provider object:

```text
concrete immutable bytes
provenance
candidate-specific selection
protected-world exclusion
zero broad-farm/rootfs leakage
bounded workload equivalence
```

It did not overgeneralize the result into a universal provider store.

### Audit verdict

```text
STRONG PASS
```

## Stage 4 — Obsidian/graphics investigation, 0029–0091

The project decomposed:

```text
application-local payload
world substrate
prefix and rootfs providers
data providers
graphics provider
graphics bridge
application feature mode
application-state authority
selected-device evidence
```

### Strong results

```text
consumer-scoped graphics policy
no global bionic graphics leakage into glibc consumers
provider selection separated from bridge selection
GPU/CPU mode owned by application domains
mapped provider distinguished from selected device
normal user state excluded from promotion evidence
closed gate lifecycle became trigger-based
```

### Remaining debt

```text
current adapters are still transitional
non-graphics policy remains over-scoped in gl/env
checkout-linked activation remains non-atomic
broad farm remains current compatibility control
```

These debts were identified rather than hidden.

### Audit verdict

```text
PASS
GRAPHICS TRANSACTION REMAINS CLOSED
```

## Stage 5 — post-closure audit and selected-pilot re-entry, 0092–0093

This phase correctly stopped graphics experiment expansion and returned to the parent application-domain question.

It also classified validators as active gates, implementation dependencies, evidence helpers, historical diagnostics, and superseded false-negative models.

### Audit verdict

```text
PASS
```

## Stage 6 — selected Obsidian B1–B10, 0094–0112

The work progressed from retained control evidence to one immutable, unactivated generation.

### Strong results

```text
$ORIGIN/AppDir locality preserved
static and runtime closure separated
dynamic/plugin and data capabilities separated
all retained objects dispositioned
GSettings aggregate reproduced from exact sources
content-addressed objects and local aliases
no-overwrite publication
validation before activation
passive startup/topology/100-second survival
zero broad-farm/rootfs/current mappings
class-based map acceptance
existing generation left immutable
```

The work successfully moved the project from broad runtime authority toward explicit selected bytes.

### Critical qualification

The B7 manifest materialized:

```text
91 ELF objects
from 71 package provenance labels
```

Those objects were selected from the observed control runtime and classified relative to the current filesystem/provider graph.

This proves a selected application-domain composition can run.

It does **not** yet prove that every chosen source/provider is the final reference-quality provider for the clean product.

Examples of unresolved source authority:

```text
Termux glibc package exists for the same capability
Debian generic package supplied the observed byte
application bundle contains an upstream-local alternative
project-built provider exists
native host data/provider could satisfy the capability
```

The Xau/Xdmcp result exposed this general issue:

```text
prefix path selected
    !=
semantic substrate ownership
```

The same audit must now be applied across the complete selected/reference set, not only those two files.

### Audit verdict

```text
PASS AS ARCHITECTURE-DISCRIMINATION GENERATION
NOT YET APPROVED AS FINAL CLEAN PROVIDER COMPOSITION
```

## Stage 7 — clean-state and PRoot/oracle correction, 0113–0115

These records correctly established:

```text
current state minimality
    !=
clean-product minimality

PRoot/rootfs
    = oracle and supply mechanism
    != workstation baseline

VS Code/font/pixbuf installs
    = named scenario states
    != promoted dependency authority
```

They also identified installed-rootfs absolute source paths as an unclosed supply contract.

### Audit verdict

```text
PASS
```

## End-to-end architecture that now follows

## 1. Native host authority

```text
Android kernel/security model
Termux bionic host
Termux:X11/session
native orchestration and integration
```

This is the highest authority.

## 2. Minimal protected glibc world substrate

This class contains only objects inseparable from establishing one coherent glibc world:

```text
dynamic loader
libc core and tightly coupled runtime
world loader/configuration identity
world ABI and purity contract
```

The current Termux glibc package is the leading reference because it is the device-adapted substrate already proven on this host.

Repository membership or prefix location alone does not expand this class.

## 3. Platform-integration providers

These are not libc substrate but directly encode Termux/Android integration:

```text
Termux-aware X11/xcb client providers
Android/Termux path-sensitive providers
explicit host bridges
```

A Termux-adapted package is preferred when its adaptation is relevant and evidenced.

These objects need their own update and validation scope.

## 4. Generic capability providers

Examples:

```text
D-Bus
GTK
fontconfig/freetype
pixbuf/image codecs
TLS
compression
printing
audio
GLVND/Mesa frontend
NSS/security
```

Possible sources:

```text
Termux glibc package
exact Debian package artifact
upstream artifact
project build
```

The source is selected only after the semantic capability and reference criteria are defined.

Existence in `glibc-repo` does not automatically make an object world substrate.

Existence in Debian slim or an oracle scenario does not automatically make it a promoted provider.

## 5. Application-local ownership

Upstream `$ORIGIN`/AppDir topology is preserved where valid.

Application-local objects are replaced only with explicit evidence and rationale.

## 6. Data capability providers

```text
fonts
locale
schemas
icons
MIME data
CA trust
```

These have independent source, generation, cache, and update contracts.

The final font target remains a native-space provider rather than a persistent Debian font installation.

## 7. Toolchain and build profile

Compilers, binutils, pkg-config, headers, sysroots, Meson, and build Python are Build and Supply Plane objects.

```text
workstation runtime profile
    !=
research/build profile
```

The existing `gcc-glibc` plus explicit-loader/binutils wrappers are a proven `toolchain.glibc-target` implementation for Mesa builds.

They are not a reason to install a compiler in the minimum workstation runtime profile.

Debian GCC is primarily an oracle/reference build tool unless a specific project requires its behavior.

`glibc-runner` must not enter the clean baseline merely because it is available. It remains a bootstrap/world-entry candidate until a unique responsibility not already satisfied by explicit launch composition is proven.

## 8. Oracle and supply scenarios

```text
pinned oracle seed
    -> named disposable/reconstructible scenarios
    -> evidence and exact artifacts
    -> selected candidate inputs
```

No single accumulated rootfs is the final baseline.

## 9. Update domains

### World substrate update

```text
candidate exact artifact
    -> substrate identity/self-integrity
    -> exported ABI gates
    -> platform-provider compatibility
    -> selected-provider relocation
    -> representative application gates
    -> explicit promotion
```

### Provider update

```text
provider candidate
    -> provider ABI/behavior gate
    -> dependent application domains only
    -> promotion and retained previous provider
```

### Application update

```text
new payload
    -> app-local closure/locality
    -> capability binding delta
    -> family/launcher policy
    -> application gates
    -> promotion
```

### Toolchain update

```text
build-profile candidate
    -> compiler/linker/sysroot smoke
    -> reproducible artifact build
    -> produced-provider validation
```

It does not mutate runtime by itself.

### Oracle update

```text
new oracle scenario identity/evidence
```

It does not automatically change promoted runtime.

## Full-project scorecard

| Area | Judgment |
|---|---|
| native host authority | aligned |
| process ABI purity | aligned and strongly evidenced |
| repository source ownership | aligned |
| semantic ownership | materially advanced, incomplete |
| PRoot runtime exclusion | aligned |
| PRoot oracle/supply model | now corrected |
| broad farm status | correctly transitional |
| selected immutable materialization | strong pass |
| provider-source authority | incomplete, immediate gap |
| app-local locality | aligned |
| graphics capability model | strong pass |
| fonts/data capabilities | incomplete; current source provisional |
| toolchain/runtime profile separation | conceptually present, clean-profile contract incomplete |
| glibc-runner necessity | unproven |
| atomic activation | open |
| world/provider/application updates | partially evidenced, not yet unified as contract |
| clean reconstruction | not proven |
| latest-first preference | safe only as candidate-first/gated-promotion model |

## Immediate intervention decision

```text
INTERVENTION REQUIRED
```

The current controlled pixbuf diagnostic remains a valid bounded experiment if it stays non-promoting.

The following work is blocked before a unified successor generation or `current` activation:

```text
final successor manifest
successor generation materialization
current activation
provider cleanup based only on physical path
clean runtime package list
```

Reason:

> The project has proven how to materialize and validate selected bytes, but has not yet proven the final provider authority for the complete selected set.

Without this intervention, the project risks converting the observed historical control closure into an immutable but still accidental application silo.

## Required provider-authority audit

For every selected/reference runtime object and every relevant package under the current glibc prefix, record:

```text
object/capability
current selected path
current package/source provenance
semantic class
minimum valid scope
candidate sources
Termux/Android adaptation or patch rationale
app-local locality relation
ABI/version relation
dependent application domains
runtime profile or research profile
update owner and trigger
final provisional authority decision
```

Required semantic classes:

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
```

## Required source decision order

```text
1. decide semantic role and minimum scope;
2. identify the relevant reference authority;
3. compare available provider candidates;
4. preserve app-local topology where valid;
5. choose provider and supply artifact;
6. define update/revalidation scope;
7. only then include/reference it in the successor composition.
```

Do not use:

```text
prefix path wins
rootfs path was mapped
package existed in the initial repository
Debian package installed successfully
```

as sufficient authority decisions.

## Bounded permission for the current pixbuf work

The current session may continue one controlled interactive vault-open diagnostic only under these boundaries:

```text
named diagnostic/oracle capability experiment
same immutable unactivated generation
no package install
no existing-generation mutation
no current activation
no promoted launcher change
rootfs loader modules/cache treated as diagnostic inputs only
result used to separate cache/module/icon/MIME effects
```

A diagnostic pass does not authorize:

```text
all discovered modules
all icon-theme files
all MIME files
current rootfs source authority
successor generation materialization
```

## Stop lines

Do not:

```text
materialize or activate the unified successor generation before the provider-authority audit;
treat all `$PREFIX/glibc` objects as world substrate;
treat all selected Debian objects as final providers;
install `glibc-runner`, GCC, fonts, pixbuf, or other packages into the clean runtime profile by availability alone;
use Debian slim defaults as promoted runtime defaults;
use glibc-repo membership as automatic semantic ownership;
replace valid application-local providers without evidence;
merge build/toolchain packages into the minimum runtime profile;
allow oracle upgrade or package installation to mutate promoted runtime automatically;
reopen closed graphics work;
turn the pixbuf diagnostic into final provider selection;
create `current` before composition/update/rollback identities are explicit.
```

## Pass conditions for lifting the intervention

The block on successor materialization can be lifted when:

```text
1. the current Termux glibc package surface is semantically partitioned;
2. every selected/reference Obsidian runtime object has a provisional authority class;
3. generic providers have an explicit source-choice rationale;
4. native font direction is represented independently from the Debian transition set;
5. pixbuf/icon/MIME capability requirements are separated and bounded;
6. runtime and research/toolchain package profiles are declared;
7. world/provider/application/toolchain/oracle update triggers are documented;
8. successor manifest synthesis uses those decisions rather than current paths alone;
9. supply artifacts are locked independently of the mutable oracle tree.
```

## Final judgment

The project has not failed its philosophy.

It has reached the exact point where top-down pressure is required:

```text
selected bytes and working generation
    ->
reference-quality provider authority and clean composition
```

The current generation should remain preserved as evidence.

The next generation must be derived from the corrected authority model, not merely from a more complete observation of the current control environment.
