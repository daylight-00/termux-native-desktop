# Selected Obsidian AppDir Closure Pilot

## Status

```text
PHASE_B1_B8_CLOSED
PHASE_B9_PASS
PASSIVE_B10_STARTUP_PASS
PASSIVE_B10_100_SECOND_SURVIVAL_PASS
PASSIVE_B10_MAPS_CAPTURE_PASS
PASSIVE_MAP_SELECTION_DIAGNOSTIC_PASS
CPU_MAP_CONTRACT_DECIDED
INTERACTIVE_VAULT_OPEN_CAPABILITY_OPEN
CONTROLLED_PIXBUF_DIAGNOSTIC_PERMITTED
PROVIDER_AUTHORITY_AUDIT_REQUIRED
UNIFIED_SUCCESSOR_GENERATION_BLOCKED
CURRENT_ACTIVATION_BLOCKED
```

The first immutable generation remains published, preserved, and unactivated.

Current authority:

```text
docs/refactor/0112-selected-obsidian-passive-map-selection-diagnostic-pass-and-contract-decision.md
docs/refactor/0113-clean-state-minimum-condition-and-supply-authority-audit.md
docs/refactor/0115-proot-oracle-supply-and-baseline-model.md
docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md
```

## Parent question

Can a real Electron AppDir consume explicit external provider/data capabilities while preserving:

```text
valid AppDir/$ORIGIN locality
minimal coherent world substrate
reference-quality provider selection
application-owned state
passive and interactive workload behavior
locked supply provenance
clean reconstruction
```

The pilot has proven the materialization and passive-runtime mechanism.

It has not yet proven that every currently selected source is the final provider authority.

## Accepted cumulative results

### Semantic analysis

```text
semantic objects:
    161

ELF objects:
    113

entrypoint static closure:
    95

all-app-local static closure:
    98

mapped-only dynamic/discovery objects:
    15

non-ELF data objects:
    17

APP_LOCAL/external lookup collisions:
    0

unresolved/ambiguous captured DT_NEEDED edges:
    0 / 0
```

### First selected generation

```text
selected ELF:
    91

package provenance labels across selected ELF:
    71

selected fonts:
    4

generated GSettings aggregate:
    1

content objects:
    96

aliases:
    175

materialized bytes:
    70,897,301

structural validation:
    1851 / 1851 PASS

current:
    ABSENT
```

The generation is valid immutable experiment evidence.

It is not yet the final clean provider composition.

### Passive explicit-generation runtime

```text
startup/topology:
    PASS

100-second survival:
    PASS

maps capture:
    PASS

main / renderer / zygote / GPU:
    1 / 1 / 3 / 0

broad-farm mappings:
    0

rootfs-provider mappings:
    0

current mappings:
    0
```

## Accepted map decisions

### Xau/Xdmcp

Observed world paths:

```text
$PREFIX/glibc/lib/libXau.so.6.0.0
$PREFIX/glibc/lib/libXdmcp.so.6.0.0
```

They are byte-identical to the duplicate selected objects and selected through exact retained absolute RPATH edges.

Accepted operational decision:

```text
RPATH patch:
    NO

existing generation mutation:
    NO

successor duplicate materialization:
    NO

world reference:
    exact hash/edge contract
```

Semantic owner remains provisional. Prefix location does not prove glibc-substrate ownership.

### Demand-loaded data

`DejaVuSansMono-Bold.ttf` was present and hash-correct but not mapped by the passive initial window.

```text
selected-data presence/hash:
    REQUIRED

mapping in every scenario:
    NOT REQUIRED

if mapped:
    accepted provider identity required
```

### CPU graphics-adjacent mappings

```text
libX11-xcb.so.1.0.0
    CPU/X11 world-support relation; exact final class still audited

app-local libvk_swiftshader.so
    allowed auxiliary mapping
    not GPU-enable evidence
```

## Why the successor is blocked

The first generation preserved the observed control composition.

That was necessary to prove:

```text
selected byte ownership
immutable publication
explicit loader selection
workload viability
rootfs/farm runtime exclusion
```

The next generation must answer a stronger question:

```text
Is each selected/reference object supplied by the correct final authority?
```

Unresolved alternatives include:

```text
Termux-adapted glibc package provider
Debian exact package artifact
upstream/application-local provider
project-built provider
native host/data provider
```

A working path or mapped path is not a final source decision.

## Required provider-authority audit

For every selected/reference runtime object and relevant current glibc-prefix package, record:

```text
object/capability
current path and provenance
semantic class
minimum valid scope
candidate provider sources
Termux/Android adaptation rationale
app-local relation
ABI/version relation
dependent domains
runtime profile or research profile
update owner/trigger
provisional final authority
```

Required classes:

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

Source-choice order:

```text
semantic role
    -> relevant reference
    -> candidate comparison
    -> provider choice
    -> locked supply artifact
    -> update/revalidation contract
    -> successor composition
```

## PRoot and supply model

```text
PRoot/rootfs:
    oracle and supply scenario mechanism

not:
    workstation baseline
    permanent runtime provider
    automatic final source authority
```

The first generation currently depends on live absolute source paths during materialization.

The successor must consume locked package/artifact/source receipts rather than relying permanently on one accumulated rootfs instance.

## Font status

Current selected Debian-derived fonts:

```text
NotoSansCJK-Regular.ttc
DejaVuMathTeXGyre.ttf
DejaVuSansMono.ttf
DejaVuSansMono-Bold.ttf
```

Status:

```text
first-generation transition evidence:
    VALID

final native-font contract:
    NOT ACCEPTED
```

The final provider must be selected against declared effects and explicit fontconfig/cache ownership without Debian-rootfs font authority.

## Controlled pixbuf diagnostic permission

One interactive vault-open diagnostic may continue because it answers a still-open capability question.

Required boundaries:

```text
named diagnostic/oracle capability experiment
same immutable unactivated generation
short receipt-owned runtime paths
no package install
no generation mutation
no current activation
no promoted launcher change
rootfs loader modules/cache treated as diagnostic inputs only
separate cache/module/icon/MIME effects
```

A pass with the broad diagnostic inventory does not authorize all modules or data in the successor.

## Successor pass conditions

The successor block can be lifted only when:

```text
provider authority is explicit for the selected/reference set;
world core is distinguished from platform/generic prefix providers;
fonts and pixbuf/icon/MIME capabilities are bounded;
runtime and research/toolchain profiles are declared;
locked supply inputs replace mutable rootfs source authority;
content/provenance/composition/install/validation identities are separated;
update and rollback scopes are explicit.
```

## Stop line

Do not:

```text
materialize or activate the unified successor before provider-authority review;
treat all prefix objects as world substrate;
treat all Debian-selected objects as final providers;
patch RPATH;
mutate or delete the first generation;
materialize Xau/Xdmcp duplicates again;
require every selected data object to map;
copy all pixbuf/icon/MIME inventory paths;
retain the Debian font set by inertia;
use the rootfs loaders.cache unchanged;
add broad-farm/rootfs paths to an acceptance run;
install packages for the pixbuf test;
create current;
claim clean reconstruction from the current rootfs;
carry phase-specific wrappers or receipt counts into final deployed tooling.
```
