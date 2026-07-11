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
PHASE_B6_SCHEMA_REPRODUCTION_NEXT
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
```

## Current architecture decision

```text
application-local ELF:
    remain in AppDir
    preserve $ORIGIN first

world substrate:
    reference protected glibc world
    do not copy into candidate

external static ELF:
    87-object deduplicated generation
    typed capability manifests

required dynamic CPU capability:
    NSS/NSPR modules and SQLite support

GPU provider capability:
    compose separately
    exclude from minimum CPU base

locale:
    WORLD_LOCALE_GLIBC
    reference prefix-managed data

fonts:
    SELECTED_FONT_DATA
    exact package-owned files

GSettings:
    SELECTED_GSETTINGS_SCHEMA_DATA
    owned source manifest
    compiler reproduction still open
```

## Phase B1 — retained identity/locality

```text
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

## Phase B2 — static/runtime partition

```text
entrypoint-static closure                 95
all-app-local static closure              98
mapped-only dynamic/discovery             15
non-ELF data capability                   17
```

## Phase B3 — dynamic grouping

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

The first failed B3 archive remains invalid and preserved. The corrected B3 receipt passed.

## Phase B4 — static ownership model

```text
entrypoint direct providers               34
external direct roots                     28
external static union                     87
shared external support                   51
direct-root overlap pairs                111
external package dependency edges        144
```

GTK is the dominant 60-object external closure. CUPS, NSS/NSPR, ALSA, udev, GBM, and compiler support remain residual typed directions.

Physical target:

```text
one receipt-owned application-domain generation
    -> deduplicated selected external ELF set
    -> typed capability manifests
    -> separate data subtrees/manifests
    -> later one-pointer atomic activation
```

## Phase B5 — data provenance

Receipt:

```text
selected-obsidian-phase-b5-data-capability-provenance-20260711-214050
```

Archive SHA-256:

```text
bea406cd8bc69a7b12e418668f16cca46ee1777430bca43f24414be68980da9f
```

Captured head:

```text
4e2fc5352d384c50bbf8370fa24fb7a377e8bab0
```

```text
analysis.status:
    PASS

next-state:
    REVIEW_DATA_PROVENANCE_GAPS

identity mismatches:
    0

missing paths:
    0

locale objects:
    12

font objects:
    4 / 4 package-owned

schema aggregate:
    1 generated/unowned byte

schema source files:
    36

schema unowned source files:
    0

schema compiler present in rootfs:
    NO
```

Schema sources:

```text
gsettings-desktop-schemas:
    32

libgtk-3-common:
    4
```

The audit closes locale ownership, font ownership, and schema source ownership. Only compiler lineage and aggregate reproduction remain open.

## Phase B6 — GSettings schema reproduction

Recipe:

```text
recipe/reproduce-retained-control-gsettings-schema.py
```

The recipe:

```text
consumes the completed B5 receipt;
rechecks all 36 source hashes;
discovers explicit/known glib-compile-schemas candidates;
records compiler path, realpath, SHA-256, package owner, and version output;
copies sources into receipt-local temporary directories;
tries default and --strict compilation modes;
records command, stdout, stderr, return code, and generated SHA-256;
compares every generated aggregate with the retained aggregate;
installs no package and mutates no promoted state.
```

Possible next states:

```text
READY_FOR_COMPLETE_DATA_MANIFEST
    at least one generated aggregate is byte-identical

REVIEW_SCHEMA_COMPILER_VERSION_DIFFERENCE
    compilation succeeds but generated bytes differ

ACQUIRE_SCHEMA_COMPILER_ORACLE
    no runnable compiler produces an aggregate
```

A `PASS` with either review/acquire state is a valid completed audit, not a script failure.

### Canonical command

```bash
cd "$HOME/projects/termux-native-desktop"

git fetch origin
git merge --ff-only origin/docs/post-graphics-architecture-audit

B5_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b5-data-capability-provenance-20260711-214050"
out="selected-obsidian-phase-b6-gsettings-schema-reproduction-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"

B5_OUT="$B5_OUT" \
OUT="$OUT" \
python \
  experiments/glibc/selected-obsidian-closure/recipe/reproduce-retained-control-gsettings-schema.py

tar czf ~/Downloads/$out.tgz $OUT
```

Optional explicit compiler candidates may be supplied without changing the script:

```bash
SCHEMA_COMPILERS="/absolute/compiler/a:/absolute/compiler/b" \
B5_OUT="$B5_OUT" \
OUT="$OUT" \
python \
  experiments/glibc/selected-obsidian-closure/recipe/reproduce-retained-control-gsettings-schema.py
```

Do not install or recover a compiler before inspecting the default Phase B6 result.

## Candidate flow

```text
B1 identity/locality
    -> B2 static/runtime partition
    -> B3 dynamic capability grouping
    -> B4 static ownership model
    -> B5 data ownership/source provenance
    -> B6 schema compiler reproduction
    -> complete CPU candidate manifest
    -> candidate materialization
    -> candidate-specific launch/maps proof
    -> boundary/leakage/equivalence acceptance
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
rerun Phase B1-B5 without a source trigger;
install a schema compiler into the rootfs merely to pass Phase B6;
copy opaque gschemas.compiled without source/compiler provenance;
copy glibc locale into the application generation;
expand the selected font set by directory inertia;
materialize candidate bytes before Phase B6 interpretation;
implement activation before the complete generation manifest;
rerun closed graphics gates;
start PyMOL by extending the broad farm.
```
