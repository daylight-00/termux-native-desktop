# Selected Obsidian AppDir Closure Pilot

## Status

```text
ACTIVE_ARCHITECTURE_DISCRIMINATION
PARENT_QUESTION_NOT_CLOSED
```

The control capture, semantic decomposition, and graphics-policy sub-investigation have advanced substantially.

The selected application-domain candidate has **not** yet been materialized and validated.

Current state:

```text
control topology/survival capture:
    PASS

multiprocess maps and unique object set:
    CAPTURED

provenance enrichment:
    PASS

semantic classification:
    PASS

graphics provider/device boundary:
    DECOMPOSED

scoped graphics-policy transaction:
    CLOSED SEPARATELY

app-local locality-shadowing decision:
    OPEN

non-graphics static/runtime closure agreement:
    OPEN

selected candidate materialization:
    NOT COMPLETED

candidate-specific actual-selection proof:
    NOT COMPLETED

control/candidate application equivalence:
    NOT COMPLETED
```

The post-graphics architecture audit is:

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
```

## Parent question

Can a real Electron AppDir application consume selected external provider closures while preserving valid application-local `$ORIGIN` locality and keeping external capability classes semantically separate?

This is a stronger question than whether Obsidian launches or whether its GPU policy works.

## Why this pilot still matters

The first D-Bus pilot proved that a selected materialized provider object can exist with:

```text
actual provider bytes
provenance receipt
candidate-specific selection proof
protected substrate boundary
zero broad-farm/rootfs provider leakage
```

It did not prove that a real application domain can preserve:

```text
application-local ELF/data locality
world substrate boundaries
prefix provider roles
rootfs provider capability groups
application state
real multiprocess workload equivalence
```

Obsidian was deliberately selected to test those properties.

The graphics-policy work was a required sub-question because graphics mappings contaminated the closure interpretation. Closing graphics does not close this parent selected-closure pilot.

## Current semantic decomposition

The observed application domain composes at least:

```text
app.obsidian local payload
    APP_LOCAL_ELF
    APP_LOCAL_DATA

world.glibc substrate
    WORLD_SUBSTRATE_ELF

provider.locale.glibc
    PROVIDER_LOCALE_DATA

prefix provider capabilities
    PROVIDER_PREFIX_ELF

selected rootfs ELF provider candidates
    PROVIDER_ROOTFS_ELF

provider.fonts.glibc
    PROVIDER_FONT_DATA

provider shared-data / GSettings
    PROVIDER_SCHEMA_DATA

graphics provider/bridge tail
    consumer-scoped policy and selected-device relations

mutable application/runtime state
    APP_MUTABLE_STATE
    RUNTIME_CACHE_*
```

Physical prefix/rootfs location is provenance input, not semantic ownership.

## App-local locality invariant

Candidate composition must preserve:

```text
valid APP_LOCAL selection
    before
external selected provider closure
```

for application-supplied libraries and data intentionally selected through `$ORIGIN` or AppDir-relative behavior.

The pilot must detect and reject external provider material that shadows a valid app-local object unless an explicit application contract requires replacement and the replacement is validated.

## Control evidence already established

The control evidence includes:

```text
real Electron multiprocess topology
bounded survival
process-class maps
AppDir-local Electron/media/graphics objects
protected glibc substrate objects
prefix provider objects
broad rootfs provider objects
font/locale/schema data
mutable state/cache categories
package provenance
SHA-256 / Build ID identity where available
```

The control also established that the rootfs provider set is heterogeneous and must not be copied blindly into one flat `lib/` directory.

## Graphics sub-question closure

The graphics investigation established:

```text
world-boundary sanitation
provider selection
device-class intent
consumer-specific suitability
selected-device evidence
application GPU/CPU feature mode
application-state validation authority
```

Canonical closure:

```text
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

Graphics provider/bridge decisions should now be treated as independent capability inputs to the application domain rather than allowed to dominate non-graphics closure selection.

## Remaining required analysis

Before candidate materialization:

```text
1. update canonical classification outputs from retained evidence;
2. resolve all review/missing identity classes relevant to candidate bytes;
3. identify APP_LOCAL versus prefix/rootfs SONAME collisions;
4. perform explicit locality-shadowing analysis;
5. derive non-graphics static ELF closure;
6. compare static closure with runtime-selected multiprocess provider set;
7. separate required provider capabilities from discovery-only/mapped-only objects;
8. separate ELF providers from font/locale/schema data capabilities;
9. define candidate composition as multiple capability inputs;
10. define candidate-specific loader/search context proving actual selection.
```

Do not rerun graphics-policy workloads merely to complete these analyses unless a graphics claim surface changes.

## Candidate flow if the pilot continues

```text
retained control evidence
    -> final semantic/locality analysis
    -> selected external provider bytes materialization
    -> provenance receipt
    -> candidate-specific CPU launch
    -> actual process maps proof
    -> app-local set preservation proof
    -> protected substrate proof
    -> zero broad-farm/rootfs provider leakage
    -> control/candidate workload equivalence
```

CPU mode remains the preferred first candidate because it separates runtime-closure architecture from hardware graphics provider selection.

## Minimum candidate success

```text
Obsidian visible window opens
main/renderer/utility or accepted equivalent topology survives
validated app-local mapped set is preserved
external selected providers map from candidate-owned bytes
protected substrate maps only from allowed substrate
no broad-farm/rootfs provider leakage
font/locale/schema ownership is explicit
no unresolved relocation error
normal user profile is not used as validation authority
```

## Decision point

The project must choose explicitly:

### Continue

Complete candidate materialization and workload equivalence to decide the reusable application-domain/provider model.

### Terminate intentionally

Record:

```text
why the discriminating value no longer justifies the work;
which object-boundary questions remain unanswered;
which assumptions PyMOL or another workload must not inherit;
which evidence remains reusable.
```

Silently abandoning the pilot is not acceptable because PyMOL is otherwise likely to repeat broad-farm/global-environment assumptions.

## Stop line

Do not yet:

```text
replace the broad farm globally;
change the promoted Obsidian launcher for candidate testing;
rewrite AppDir RPATH globally;
copy every rootfs path into candidate/lib;
merge app-local and external provider bytes;
introduce a universal provider-store framework;
start PyMOL by extending the same unresolved broad closure;
interpret graphics closure as selected application closure completion.
```

## Relation to next architecture phase

The result of this pilot should inform:

```text
world.glibc substrate boundary
shared provider capability grouping
application-local closure rules
selected data-provider ownership
application-domain bindings
candidate materialization format
atomic activation requirements
PyMOL onboarding architecture
```
