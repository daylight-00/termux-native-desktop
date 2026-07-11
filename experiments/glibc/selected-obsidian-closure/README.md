# Selected Obsidian AppDir Closure Pilot

## Status

```text
ACTIVE_ARCHITECTURE_DISCRIMINATION
PARENT_QUESTION_NOT_CLOSED
PHASE_B1_PASS
PHASE_B2_STATIC_RUNTIME_PARTITION_NEXT
```

The selected application-domain candidate has **not** yet been materialized or validated.

Current state:

```text
control topology/survival/maps:
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

retained-control identity/locality audit:
    PASS

app-local lookup collision:
    NONE OBSERVED

static/runtime graph partition:
    NEXT

capability grouping:
    OPEN

selected candidate materialization:
    NOT STARTED

candidate-specific selection/equivalence:
    NOT COMPLETED
```

Architecture authority:

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
docs/refactor/0093-post-audit-direction-validator-lifecycle-and-selected-closure-reentry.md
docs/refactor/0094-selected-obsidian-phase-b1-retained-control-locality-pass.md
```

## Parent question

Can a real Electron AppDir consume selected external provider closures while preserving valid application-local `$ORIGIN` locality and keeping world, provider, data, graphics, and mutable-state responsibilities separate?

This is stronger than proving that Obsidian launches or that its GPU branch works.

## Decision

The pilot continues.

```text
selected Obsidian closure:
    CONTINUE

fresh control capture:
    NOT REQUIRED FOR IDENTITY DRIFT

candidate materialization:
    BLOCKED UNTIL CAPABILITY PARTITION

atomic activation implementation:
    DEFER UNTIL MANAGED OBJECT SET IS DECIDED

PyMOL runtime mutation:
    DEFER
```

## Retained control authority

Canonical retained control root:

```text
$PREFIX/tmp/selected-obsidian-control-survival-20260710-220652
```

Phase B1 receipt:

```text
$PREFIX/tmp/selected-obsidian-closure/
    selected-obsidian-phase-b1-retained-control-locality-20260711-192919
```

Archive SHA-256:

```text
aa5081f3b5ec8d7fee5e33db631abe0fd695d1291eeddcb54d3777ca72f3e383
```

## Phase B1 result

```text
semantic objects:
    161

captured processes:
    6

candidate-relevant identity matches:
    136 / 136

ELF objects:
    113

DT_NEEDED edges:
    531

semantic review objects:
    0

hash mismatches:
    0

missing candidate paths:
    0

APP_LOCAL/external lookup collisions:
    0

unresolved dependency names:
    0

ambiguous dependency names:
    0
```

Phase B1 launched no workload and mutated no promoted runtime state.

## Locality conclusion

The app-local ELF set is:

```text
obsidian
libEGL.so
libGLESv2.so
libffmpeg.so
libvulkan.so.1
```

All five retain:

```text
RUNPATH:
    $ORIGIN
    -> $PREFIX/glibc/lib
    -> $HOME/gl/lib
```

No mapped external ELF has a colliding lookup name with the mapped app-local set.

Therefore:

```text
no current mapped collision is observed;
$ORIGIN-first locality remains a candidate invariant;
future selected providers with colliding names must be rejected unless an
explicit replacement contract is separately validated.
```

This does not accept `$HOME/gl/lib` as the target candidate authority.

## Current semantic decomposition

```text
app.obsidian payload
    APP_LOCAL_ELF
    APP_LOCAL_DATA

world.glibc
    WORLD_SUBSTRATE_ELF

prefix providers
    PROVIDER_PREFIX_ELF

rootfs ELF providers
    PROVIDER_ROOTFS_ELF

graphics providers/layers
    PROVIDER_GRAPHICS_*

locale/font/schema providers
    PROVIDER_*_DATA

mutable state/cache
    APP_MUTABLE_STATE
    RUNTIME_CACHE_*
```

Physical prefix/rootfs location is provenance, not final ownership.

## Independent graph result

The Phase B1 receipt supports the following read-only graph partition:

```text
total ELF objects:
    113

Obsidian entrypoint DT_NEEDED closure:
    95

union of all app-local ELF DT_NEEDED closures:
    98

mapped-only dynamic/discovery objects:
    15

non-ELF provider data objects:
    17
```

Entrypoint static closure composition:

```text
APP_LOCAL_ELF                 2
WORLD_SUBSTRATE_ELF           6
PROVIDER_PREFIX_ELF          32
PROVIDER_ROOTFS_ELF          54
PROVIDER_GRAPHICS_GBM_ELF     1
```

Auxiliary app-local static roots:

```text
libEGL.so
libGLESv2.so
libvulkan.so.1
```

## Mapped-only dynamic/discovery set

The 15 objects outside every app-local `DT_NEEDED` graph are not automatically optional.

Observed directions:

```text
Vulkan/provider tail:
    libvulkan_freedreno.so
    libVkLayer_MESA_device_select.so

X11/DRI/support tail:
    libX11-xcb.so.1
    libstdc++.so.6
    libxcb-dri3.so.0
    libxcb-present.so.0
    libxcb-randr.so.0
    libxcb-sync.so.1
    libxcb-xfixes.so.0
    libxshmfence.so.1
    libzstd.so.1

NSS/security database tail:
    libfreeblpriv3.so
    libnssckbi.so
    libsoftokn3.so
    libsqlite3.so.0
```

The next analysis reports these separately so capability ownership can be decided without flattening them into the entrypoint static closure.

## Data capabilities

The retained control contains:

```text
locale data:
    12

font data:
    4

GSettings schema data:
    1
```

These are not ELF closure members.

Each capability must be deliberately:

```text
kept rootfs-backed;
materialized as selected data;
or owned by the application domain.
```

## Phase B2

Recipe:

```text
recipe/analyze-retained-control-static-runtime-closure.sh
```

It consumes the completed Phase B1 directory and emits:

```text
resolved-edges.tsv
entrypoint-static-closure.tsv
all-app-local-static-closure.tsv
candidate-elf-partition.tsv
mapped-only-dynamic.tsv
data-capabilities.tsv
closure-class-counts.tsv
summary.tsv
claim-boundary.txt
next-state.txt
analysis.status
```

It launches no process and mutates no promoted runtime state.

Successful next state:

```text
READY_FOR_CAPABILITY_GROUPING_DECISION
```

### Canonical command

```bash
cd "$HOME/projects/termux-native-desktop"

git fetch origin
git merge --ff-only origin/docs/post-graphics-architecture-audit

B1_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b1-retained-control-locality-20260711-192919"
out="selected-obsidian-phase-b2-static-runtime-closure-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"

B1_OUT="$B1_OUT" \
OUT="$OUT" \
bash \
  experiments/glibc/selected-obsidian-closure/recipe/analyze-retained-control-static-runtime-closure.sh

tar czf ~/Downloads/$out.tgz $OUT
```

## Phase B2 interpretation boundary

A PASS means:

```text
captured DT_NEEDED graph was reproducibly partitioned;
entrypoint-static, auxiliary app-local, mapped-only, and data sets are explicit;
capability grouping analysis can proceed.
```

It does not mean:

```text
exact dlopen callers are proven;
dynamic providers are optional;
capability ownership is decided;
candidate bytes may be materialized;
search-path selection or workload equivalence is proven.
```

## Candidate flow after capability grouping

```text
retained control evidence
    -> Phase B1 identity/locality audit
    -> Phase B2 static/runtime partition
    -> capability grouping and data ownership decision
    -> selected provider bytes materialization
    -> provenance receipt
    -> candidate-specific CPU launch
    -> actual selection/maps proof
    -> app-local preservation proof
    -> protected substrate proof
    -> zero broad-farm/rootfs provider leakage
    -> control/candidate equivalence
```

CPU mode remains the preferred first candidate because it separates runtime-closure architecture from hardware graphics selection.

## Evidence handoff

Every evidence-producing stage defines stage-specific `out` and `OUT` and ends with:

```bash
tar czf ~/Downloads/$out.tgz $OUT
```

The archive is a transport object. The contained receipt and original device evidence root remain authoritative.

## Stop line

Do not:

```text
replace the broad farm globally;
change the promoted Obsidian launcher for candidate testing;
rewrite AppDir RPATH globally;
copy all 113 ELF objects into one candidate/lib;
drop the 15 mapped-only objects because they are outside static reachability;
merge locale/font/schema data into the ELF closure;
remove $ORIGIN or accept $HOME/gl/lib as final candidate authority;
introduce a universal provider-store framework;
materialize a candidate before Phase B2 interpretation;
rerun closed graphics gates;
start PyMOL by extending the unresolved broad closure.
```
