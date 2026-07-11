# Selected Obsidian AppDir Closure Pilot

## Status

```text
ACTIVE_ARCHITECTURE_DISCRIMINATION
PARENT_QUESTION_NOT_CLOSED
PHASE_B1_RETAINED_CONTROL_AUDIT_NEXT
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

graphics validator lifecycle:
    CLASSIFIED

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

Architecture authority:

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
docs/refactor/0093-post-audit-direction-validator-lifecycle-and-selected-closure-reentry.md
```

## Parent question

Can a real Electron AppDir application consume selected external provider closures while preserving valid application-local `$ORIGIN` locality and keeping external capability classes semantically separate?

This is a stronger question than whether Obsidian launches or whether its GPU policy works.

## Decision after the post-graphics audit

The pilot continues.

It is not silently terminated and it is not skipped in favor of PyMOL.

Reason:

```text
D-Bus proved that a bounded selected provider object can exist.

Obsidian must now test whether a real multiprocess AppDir can consume selected
external providers without flattening application-local, world, provider, data,
and mutable-state ownership into one broad farm or one global environment.
```

Atomic activation remains mandatory before the next multi-file promoted migration, but activation implementation is not started around the unresolved current umbrella. The selected object set and semantic owners must be decided first.

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

The graphics-policy work was a required sub-question because graphics mappings contaminated closure interpretation. Closing graphics does not close this parent selected-closure pilot.

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

Canonical retained control root:

```text
$PREFIX/tmp/selected-obsidian-control-survival-20260710-220652
```

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

The control established that the rootfs provider set is heterogeneous and must not be copied blindly into one flat `lib/` directory.

## Graphics sub-question closure

Canonical closure:

```text
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

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

Graphics provider/bridge decisions are now independent capability inputs to the application domain. They must not dominate non-graphics closure selection.

Closed graphics gates are rerun only when their own claim surface changes.

## Phase B1 — retained control locality input audit

The next action is a read-only audit of the retained control evidence.

Recipe:

```text
recipe/audit-retained-control-locality.sh
```

It launches no process and mutates no promoted runtime state.

It verifies and emits:

```text
required retained input availability
candidate-relevant captured/current SHA-256 agreement
ELF SONAME, DT_NEEDED, RPATH, and RUNPATH facts
APP_LOCAL versus external provider name collisions
zero/one/multiple captured candidates for each DT_NEEDED name
process-class semantic object use
provider package/capability counts
explicit claim boundary and next-state decision
```

A `PASS` means the retained evidence is still identity-reproducible enough for the next locality/static-runtime decision step.

It does not mean the candidate is ready.

### Canonical command

```bash
cd "$HOME/projects/termux-native-desktop"

git fetch origin
git merge --ff-only origin/docs/post-graphics-architecture-audit

CONTROL_OUT="$PREFIX/tmp/selected-obsidian-control-survival-20260710-220652"
out="selected-obsidian-phase-b1-retained-control-locality-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"

CONTROL_OUT="$CONTROL_OUT" \
OUT="$OUT" \
bash \
  experiments/glibc/selected-obsidian-closure/recipe/audit-retained-control-locality.sh

tar czf ~/Downloads/$out.tgz $OUT
```

Do not replace the final archive name with `results.tgz` or another generic name.

## Phase B1 decision branches

```text
PASS with stable identities
    -> inspect locality-collisions.tsv
    -> inspect unresolved-needed.tsv
    -> inspect ambiguous-needed.tsv
    -> classify whether retained maps are sufficient for edge attribution
    -> define the next bounded non-graphics closure analysis

FAIL with hash mismatch or missing candidate input
    -> do not treat current bytes as captured bytes
    -> check for exact retained artifacts
    -> otherwise justify one fresh CPU control capture

FAIL with semantic review rows
    -> resolve semantic classification before materialization
```

No selected provider bytes are materialized in this phase.

## Remaining required analysis

After Phase B1:

```text
1. resolve APP_LOCAL versus prefix/rootfs SONAME collisions;
2. make the locality-shadowing decision explicit;
3. derive the bounded non-graphics static ELF closure;
4. compare static closure with runtime-selected multiprocess provider use;
5. separate required providers from discovery-only/mapped-only objects;
6. separate ELF providers from font/locale/schema data capabilities;
7. define candidate composition as multiple capability inputs;
8. define candidate-specific loader/search context proving actual selection.
```

Do not rerun graphics-policy workloads merely to complete these analyses unless a graphics claim surface changes.

## Candidate flow if the pilot continues

```text
retained control evidence
    -> identity/locality audit
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

## Evidence handoff rule

Every evidence-producing stage defines a stage-specific `out` and `OUT` and ends with:

```bash
tar czf ~/Downloads/$out.tgz $OUT
```

The tgz is a transport object. The contained receipt and original device evidence root remain authoritative.

## Stop line

Do not yet:

```text
replace the broad farm globally;
change the promoted Obsidian launcher for candidate testing;
rewrite AppDir RPATH globally;
copy every rootfs path into candidate/lib;
merge app-local and external provider bytes;
introduce a universal provider-store framework;
materialize a candidate before Phase B1 interpretation;
start PyMOL by extending the same unresolved broad closure;
interpret graphics closure as selected application closure completion.
```

## Relation to the next architecture phase

The result of this pilot should inform:

```text
world.glibc substrate boundary
shared provider capability grouping
application-local closure rules
selected data-provider ownership
application-domain bindings
candidate materialization format
atomic activation managed-leaf set
PyMOL onboarding architecture
```
