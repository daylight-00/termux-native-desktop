# 0094 — Selected Obsidian Phase B1 Retained-Control Locality Audit Pass

## Status

Phase B1 is complete.

```text
retained control identity audit:
    PASS

next state:
    READY_FOR_LOCALITY_AND_STATIC_RUNTIME_DECISION

runtime launch:
    NO

promoted runtime mutation:
    NO
```

This receipt does not declare a candidate ready. It closes the retained-evidence identity and first-order lookup-resolution precondition for the next read-only closure analysis.

## Authoritative device receipt

Archive:

```text
selected-obsidian-phase-b1-retained-control-locality-20260711-192919.tgz
```

Archive SHA-256:

```text
aa5081f3b5ec8d7fee5e33db631abe0fd695d1291eeddcb54d3777ca72f3e383
```

Contained evidence root:

```text
/data/data/com.termux/files/usr/tmp/selected-obsidian-closure/
    selected-obsidian-phase-b1-retained-control-locality-20260711-192919
```

Retained control source:

```text
/data/data/com.termux/files/usr/tmp/
    selected-obsidian-control-survival-20260710-220652
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    0d1307fd94c8115b0d0ce3d76a3a3d48957530f9
```

The archive contained only regular files and directories under a relative Termux path. No absolute archive member, parent traversal member, symlink, device, or other special member was present.

## Input verification

All required retained inputs were present:

```text
unique-objects.tsv
mapped-objects.tsv
processes.tsv
object-identities.tsv
semantic-objects.tsv
semantic-counts.tsv
semantic-review.tsv
```

The retained root did not contain the optional historical:

```text
topology.status
survival.status
maps-capture.status
```

This is consistent with the known old control-capture transaction boundary recorded in `0033`. The final process/maps/unique-object evidence was retained, then identity enrichment and semantic classification were completed separately.

## Primary result

```text
semantic objects:
    161

captured processes:
    6

semantic review objects:
    0

verified candidate-relevant inputs:
    136

verified ELF objects:
    113

candidate input hash mismatches:
    0

candidate input missing paths:
    0

APP_LOCAL/external lookup-name collisions:
    0

unresolved DT_NEEDED edges:
    0

ambiguous DT_NEEDED edges:
    0
```

Every one of the 136 candidate-relevant current paths matched its retained captured SHA-256 identity.

Therefore the current filesystem bytes are valid inputs for analysis of this retained control receipt. No fresh control capture is required merely for identity drift.

## Semantic object distribution

```text
APP_LOCAL_DATA                              6
APP_LOCAL_ELF                               5
WORLD_SUBSTRATE_ELF                         6
PROVIDER_PREFIX_ELF                        41
PROVIDER_ROOTFS_ELF                        58
PROVIDER_GRAPHICS_GBM_ELF                   1
PROVIDER_GRAPHICS_VULKAN_DRIVER_ELF         1
PROVIDER_GRAPHICS_VULKAN_LAYER_ELF          1
PROVIDER_LOCALE_DATA                       12
PROVIDER_FONT_DATA                          4
PROVIDER_SCHEMA_DATA                        1
APP_MUTABLE_STATE                          19
RUNTIME_CACHE_FONTCONFIG                    4
RUNTIME_CACHE_MESA                          1
DEVICE_NODE_GPU                             1
```

This confirms again that the application domain is not one flat ELF closure.

It contains at least:

```text
application payload ELF/data
world substrate
prefix ELF providers
rootfs ELF providers
graphics providers/layers
locale provider data
font provider data
schema provider data
mutable application state
runtime caches
device relation
```

## App-local locality result

The five app-local ELF objects are:

```text
obsidian
libEGL.so
libGLESv2.so
libffmpeg.so
libvulkan.so.1
```

All five have current RUNPATH ordering:

```text
$ORIGIN
    -> $PREFIX/glibc/lib
    -> $HOME/gl/lib
```

The retained mapped candidate set contains:

```text
APP_LOCAL versus external lookup-name collisions:
    0
```

Therefore the current evidence establishes:

```text
no observed SONAME/lookup-name competitor for the mapped APP_LOCAL objects
```

It does not establish:

```text
that $ORIGIN precedence may be removed;
that future provider sets cannot introduce a collision;
that broad-farm search-path authority is an accepted target.
```

The locality rule remains:

```text
preserve $ORIGIN/AppDir locality first
reject any future external provider with a colliding lookup identity
unless replacement is an explicit application contract with its own evidence
```

The result converts the open locality question from:

```text
is there already an observed app-local/external collision?
```

into:

```text
no observed collision;
therefore preserve the existing locality ordering as a candidate invariant
and prove candidate selection without broad-farm shadowing.
```

## First-order static/runtime agreement

The Phase B1 receipt extracted:

```text
113 ELF objects
531 DT_NEEDED edges
113 unique provider lookup names
```

Every captured `DT_NEEDED` name resolved to exactly one captured mapped ELF candidate.

```text
unresolved:
    0

ambiguous:
    0

duplicate provider lookup names:
    0
```

This is a strong first-order agreement between:

```text
captured mapped ELF set
    and
captured ELF DT_NEEDED/name relations
```

It is not yet the final static/runtime closure decision because it does not distinguish:

```text
entrypoint-reachable static closure
auxiliary app-local roots
runtime dlopen/discovery-only mappings
ELF providers versus data capabilities
exact dynamic caller or search path
```

## Independent graph inspection

A separate read-only graph reconstruction over the uploaded receipt found:

```text
total ELF objects:
    113

reachable from the Obsidian entrypoint through DT_NEEDED:
    95

reachable from the union of all APP_LOCAL ELF roots:
    98

mapped but not reachable from any APP_LOCAL DT_NEEDED graph:
    15
```

Entrypoint static closure composition:

```text
APP_LOCAL_ELF:
    2

WORLD_SUBSTRATE_ELF:
    6

PROVIDER_PREFIX_ELF:
    32

PROVIDER_ROOTFS_ELF:
    54

PROVIDER_GRAPHICS_GBM_ELF:
    1
```

The three additional objects in the all-app-local closure are the auxiliary app-local graphics ELF roots:

```text
libEGL.so
libGLESv2.so
libvulkan.so.1
```

Their dependencies were already contained in the entrypoint closure.

## Mapped-only dynamic/discovery set

The 15 objects outside every app-local `DT_NEEDED` graph are:

### Graphics/provider tail — zygote

```text
libvulkan_freedreno.so
libVkLayer_MESA_device_select.so
```

### Prefix X11/DRI/support tail — mostly zygote

```text
libX11-xcb.so.1
libstdc++.so.6
libxcb-dri3.so.0
libxcb-present.so.0
libxcb-randr.so.0
libxcb-sync.so.1
libxcb-xfixes.so.0
libxshmfence.so.1
libzstd.so.1
```

`libX11-xcb.so.1` was observed in main and zygote. The other objects in this group were observed in zygote.

### NSS/security database tail — main

```text
libfreeblpriv3.so
libnssckbi.so
libsoftokn3.so
libsqlite3.so.0
```

These were observed in the main process.

This set is not optional merely because it is outside the static graph. It requires dynamic capability attribution before candidate materialization.

Likely capability directions, still to be proven rather than assumed:

```text
graphics Vulkan/provider discovery
X11/DRI runtime extension discovery
NSS/security module and database support
```

## Data capability set

The retained control contains 17 non-ELF provider data objects:

```text
locale data:
    12

font data:
    4

GSettings schema data:
    1
```

These must not be copied into an ELF `lib/` closure by inertia.

They require separate owner decisions:

```text
rootfs-backed provider retained deliberately;
selected data closure materialized;
or application-local ownership.
```

## Provenance gaps

Two candidate-relevant objects remain semantically classified but do not have ordinary package provenance in the retained identity table:

```text
managed Turnip/Freedreno driver:
    /data/data/com.termux/files/home/gl/opt/mesa-glibc-26.1.4-full/lib/
        libvulkan_freedreno.so
    package=UNKNOWN
    version=UNKNOWN

compiled GSettings schema:
    .../usr/share/glib-2.0/schemas/gschemas.compiled
    package=UNOWNED
    version=UNKNOWN
```

The first belongs to the separately closed graphics provider lineage and must remain a distinct graphics capability input.

The second is generated aggregate data and requires an explicit data-provider provenance/materialization contract before a selected application candidate can claim reproducibility.

Neither gap invalidates Phase B1 identity stability because both current files matched their captured SHA-256 values.

## Claim boundary

Phase B1 proves:

```text
retained evidence is complete for the declared inputs;
semantic review set is empty;
candidate-relevant bytes have not drifted;
all captured DT_NEEDED names have one captured provider candidate;
no mapped APP_LOCAL/external lookup-name collision exists;
read-only follow-up analysis can proceed without a new workload run.
```

Phase B1 does not prove:

```text
candidate materialization is ready;
all mapped-only objects are optional;
exact dlopen callers are known;
provider capability grouping is decided;
data ownership is decided;
broad-farm search paths may remain in the target;
candidate-specific selection or workload equivalence.
```

## Direction decision

```text
fresh control recapture:
    NOT REQUIRED

candidate materialization:
    STILL BLOCKED

locality invariant:
    PRESERVE APP_LOCAL $ORIGIN FIRST

next action:
    READ-ONLY STATIC/UNTIME GRAPH PARTITION
```

The next analysis must explicitly partition:

```text
entrypoint static closure
auxiliary app-local static roots
mapped-only dynamic/discovery providers
non-ELF data capabilities
```

## Phase B2 implementation

Added:

```text
experiments/glibc/selected-obsidian-closure/recipe/
    analyze-retained-control-static-runtime-closure.sh
```

The script consumes the completed Phase B1 directory and emits:

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

It performs no process launch and no promoted runtime mutation.

Its success state is:

```text
READY_FOR_CAPABILITY_GROUPING_DECISION
```

## Stop line

Do not:

```text
materialize all 113 ELF objects as one candidate lib directory;
drop the 15 dynamic/discovery objects because they are not statically reachable;
merge the 17 data objects into the ELF closure;
remove $ORIGIN from AppDir RUNPATH;
accept $HOME/gl/lib as the target candidate authority;
rerun graphics gates;
run a fresh Obsidian control merely to repeat the retained evidence;
start PyMOL or atomic activation implementation from this incomplete provider partition.
```
