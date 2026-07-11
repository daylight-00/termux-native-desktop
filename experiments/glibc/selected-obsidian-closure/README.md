# Selected Obsidian AppDir Closure Pilot

## Status

```text
ACTIVE_ARCHITECTURE_DISCRIMINATION
PARENT_QUESTION_NOT_CLOSED
PHASE_B1_PASS
PHASE_B2_PASS
PHASE_B3_CORRECTED_PASS
PHASE_B4_PASS
PHASE_B5_PASS_WITH_REVIEW
PHASE_B6_FIRST_RUN_DIAGNOSTIC_ONLY
PHASE_B6_CORRECTED_PASS
PHASE_B7_PASS
PHASE_B8_GENERATION_LAYOUT_PREFLIGHT_NEXT
```

The selected CPU application-domain candidate has not yet been materialized or validated.

## Authority

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
docs/refactor/0093-post-audit-direction-validator-lifecycle-and-selected-closure-reentry.md
docs/refactor/0094-selected-obsidian-phase-b1-retained-control-locality-pass.md
docs/refactor/0095-selected-obsidian-phase-b2-static-runtime-closure-pass.md
docs/refactor/0096-selected-obsidian-phase-b3-first-run-script-failure.md
docs/refactor/0097-selected-obsidian-phase-b3-capability-grouping-pass.md
docs/refactor/0098-selected-obsidian-phase-b4-entrypoint-static-matrix-pass.md
docs/refactor/0099-selected-obsidian-phase-b5-data-provenance-review.md
docs/refactor/0100-selected-obsidian-phase-b6-source-manifest-gap.md
docs/refactor/0101-selected-obsidian-phase-b6-corrected-schema-reproduction-pass.md
docs/refactor/0102-selected-obsidian-phase-b7-complete-cpu-manifest-pass.md
```

## Current architecture decision

```text
application-local ELF/data:
    reference AppDir
    preserve $ORIGIN first

world glibc ELF/locale:
    reference protected world
    do not copy

external static ELF:
    materialize 87 deduplicated objects
    typed capability memberships

required CPU dynamic ELF:
    materialize 4 NSS/security objects

GPU feature dynamic ELF:
    exclude 11 objects from minimum CPU base
    compose separately

fonts:
    materialize 4 exact selected files

GSettings:
    generate one aggregate from 37 owned sources
    compiler = native Termux glib 2.88.2

mutable state and caches:
    exclude from immutable generation
    recreate under runtime ownership
```

## Closed read-only evidence

### Phase B1

```text
semantic objects                          161
candidate identity matches              136 / 136
ELF objects                              113
DT_NEEDED edges                          531
semantic review                            0
hash mismatch                              0
missing path                               0
APP_LOCAL/external lookup collision        0
unresolved dependency                      0
ambiguous dependency                       0
```

### Phase B2

```text
entrypoint-static closure                 95
all-app-local static closure              98
mapped-only dynamic/discovery             15
non-ELF data capability                   17
```

### Corrected Phase B3

```text
GRAPHICS_VULKAN roots:
    libvulkan_freedreno.so
    libVkLayer_MESA_device_select.so

NSS_SECURITY roots:
    libfreeblpriv3.so
    libnssckbi.so
    libsoftokn3.so
        -> libsqlite3.so.0
```

### Phase B4

```text
entrypoint direct providers               34
external direct roots                     28
external static union                     87
shared external support                   51
direct-root overlap pairs                111
external package dependency edges        144
```

### Phase B5 and corrected Phase B6

```text
locale:
    12 world-owned glibc files

fonts:
    4 exact package-owned selected files

GSettings sources:
    37 package-owned files

compiler:
    $PREFIX/bin/glib-compile-schemas
    glib 2.88.2

clean byte-identical aggregate reproductions:
    default
    strict
```

The first B6 run remains a diagnostic receipt for the incomplete 36-file suffix-filtered source set.

## Phase B7 — complete CPU manifest

Receipt:

```text
selected-obsidian-phase-b7-complete-cpu-candidate-manifest-20260711-225234
```

Archive SHA-256:

```text
6afcbf799f1c73bbc1a058176f30eada84502d29e5507c9ed6b1c7bdb9d495b8
```

Captured head:

```text
ef8eaaaf7af467a7732bb7a00383585cb43d654d
```

```text
analysis.status:
    PASS

next-state:
    READY_FOR_CANDIDATE_MATERIALIZATION_DESIGN

semantic objects:
    161 / 161 disposed

ELF objects:
    113 / 113 accounted

selected static ELF:
    87

required NSS dynamic ELF:
    4

selected ELF total:
    91

excluded graphics feature ELF:
    11

app-local ELF reference:
    5

world ELF reference:
    6

selected ELF lookup collisions:
    0

unclassified objects:
    0
```

The 48 non-ELF semantic objects are also completely disposed:

```text
app-local data reference                  6
world locale reference                   12
selected fonts materialize                4
GSettings aggregate generate              1
mutable state isolate                     19
fontconfig cache regenerate               4
Mesa cache regenerate                      1
optional GPU device reference              1
```

Candidate input files:

```text
candidate-elf-manifest.tsv
candidate-data-manifest.tsv
capability-membership.tsv
reference-runtime-owned-manifest.tsv
schema-source-manifest.tsv
schema-build-contract.tsv
semantic-object-disposition.tsv
```

The copied-byte input boundary is:

```text
91 ELF + 4 fonts = 95 unique source hashes
```

The generated schema aggregate adds one immutable content identity.

## Physical generation direction

The next design uses:

```text
$HOME/gl/selected/obsidian/
    objects/sha256/<prefix>/<sha256>
    staging/<transaction>
    generations/<generation-id>/
        lib/
        share/fonts/selected/
        share/glib-2.0/schemas/
        manifests/
        receipts/
    current -> generations/<generation-id>
```

This is a design direction, not an existing promoted layout.

Required invariants:

```text
content objects are immutable and hash-addressed;
generation aliases are relative and receipt-owned;
staging, generations, and current are on one filesystem;
a generation is complete before publication;
candidate validation uses an explicit generation path before activation;
current changes with one temporary-symlink atomic rename;
rollback points current at a previous immutable generation;
referenced generations are never garbage-collected.
```

## Phase B8 — generation-layout preflight

Recipe:

```text
recipe/design-selected-cpu-generation-layout.py
```

It consumes only the completed Phase B7 receipt and performs no materialization or workload launch.

It:

```text
embeds the B7 manifests;
rechecks current identity for 91 ELF, 4 fonts, 37 schema sources, and the schema compiler;
derives content-addressed object paths;
derives one generation ID from the accepted content/build contract;
builds the combined ELF lookup/SONAME/source-basename alias namespace;
adds selected-font and generated-schema aliases;
rejects alias collisions;
records relative symlink targets;
records staging, activation, rollback, and explicit-launch contracts.
```

Expected structural values for the retained receipt:

```text
source identity checks:
    133

source identity failures:
    0

copied ELF content objects:
    91

copied font content objects:
    4

generated schema content objects:
    1

content plan rows:
    96

unique content hashes:
    96

duplicate content hashes:
    0

ELF aliases:
    170

font aliases:
    4

schema aliases:
    1

total generation aliases:
    175

generation alias collisions:
    0
```

Expected next state:

```text
READY_FOR_STAGING_MATERIALIZER_IMPLEMENTATION
```

### Canonical command

```bash
cd "$HOME/projects/termux-native-desktop"

git fetch origin
git merge --ff-only origin/docs/post-graphics-architecture-audit

B7_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b7-complete-cpu-candidate-manifest-20260711-225234"
out="selected-obsidian-phase-b8-generation-layout-preflight-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"

B7_OUT="$B7_OUT" \
OUT="$OUT" \
python \
  experiments/glibc/selected-obsidian-closure/recipe/design-selected-cpu-generation-layout.py

tar czf ~/Downloads/$out.tgz $OUT
```

Optional non-default design base:

```bash
GENERATION_BASE="/absolute/same-filesystem/base" \
B7_OUT="$B7_OUT" \
OUT="$OUT" \
python \
  experiments/glibc/selected-obsidian-closure/recipe/design-selected-cpu-generation-layout.py
```

The default remains:

```text
$HOME/gl/selected/obsidian
```

## Candidate flow

```text
B1 identity/locality
    -> B2 static/runtime partition
    -> B3 dynamic capability grouping
    -> B4 static ownership model
    -> B5 data identity/ownership
    -> corrected B6 schema reproduction
    -> B7 complete semantic/candidate manifest
    -> B8 source/alias/generation-layout preflight
    -> staging-only materializer and immutable-generation validator
    -> explicit-generation launch/maps proof
    -> atomic current activation and rollback
    -> promoted candidate equivalence acceptance
```

## Evidence handoff

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run stage
tar czf ~/Downloads/$out.tgz $OUT
```

## Stop line

Do not:

```text
rerun Phase B1-B7 without a source trigger;
copy selected bytes directly into a live farm;
activate a partial or unvalidated generation;
use lookup, SONAME, basename, font, or schema aliases without collision analysis;
copy app-local/world objects or excluded graphics feature objects into the CPU base;
change the promoted launcher before explicit-generation validation;
implement garbage collection before rollback/reference semantics;
rerun closed graphics gates;
start PyMOL by extending the broad farm.
```
