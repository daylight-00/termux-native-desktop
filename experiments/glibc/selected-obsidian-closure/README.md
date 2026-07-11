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
PHASE_B7_COMPLETE_CPU_MANIFEST_NEXT
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

Physical direction:

```text
one receipt-owned application-domain generation
    -> one deduplicated selected object set
    -> typed capability manifests
    -> separate data manifests/build contracts
    -> later one-pointer atomic activation
```

### Phase B5

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

captured schema sources:
    36
```

Phase B5 closed locale and selected-font ownership. Its schema suffix filter omitted one enum-definition XML.

### First Phase B6 diagnostic

```text
receipt:
    selected-obsidian-phase-b6-gsettings-schema-reproduction-20260711-220355

analysis.status:
    PASS

accepted interpretation:
    REVIEW_SCHEMA_SOURCE_MANIFEST_GAP
```

The default compiler ignored ten schema files because enum definitions were absent; strict mode failed. That hash difference was not a clean compiler-version comparison.

### Corrected Phase B6

Receipt:

```text
selected-obsidian-phase-b6-gsettings-schema-reproduction-corrected-20260711-222459
```

Archive SHA-256:

```text
4b86b884f31a87c38636b7c96b4a45de7588b89fd9b5073d02a8db4c52edf699
```

Captured head:

```text
b772acb5f6895622e73eda1a6133094885304627
```

```text
analysis.status:
    PASS

next-state:
    READY_FOR_COMPLETE_DATA_MANIFEST

B5 source files:
    36

corrected source files:
    37

added source:
    org.gnome.desktop.enums.xml

source identity:
    37 / 37 MATCH

unowned sources:
    0

undefined enum/flags references:
    0

compiler:
    $PREFIX/bin/glib-compile-schemas
    glib 2.88.2

clean successful compiles:
    2

compilation error attempts:
    0

byte-identical outputs:
    2
```

Both default and strict modes produced:

```text
457f7461585b4caf6e11de65f707077bcb2208f9916c0c588080262f43ecb938
```

which exactly matches the retained aggregate.

Data ownership and schema compiler lineage are closed for manifest synthesis.

## Phase B7 — complete CPU candidate manifest

Recipe:

```text
recipe/synthesize-selected-cpu-candidate-manifest.py
```

It consumes completed B1, corrected B3, B4, B5, and corrected B6 receipts.

It performs no materialization, process launch, package installation, or promoted mutation.

It emits:

```text
semantic-object-disposition.tsv
candidate-elf-manifest.tsv
candidate-data-manifest.tsv
capability-membership.tsv
reference-runtime-owned-manifest.tsv
schema-source-manifest.tsv
schema-build-contract.tsv
summary.tsv
claim-boundary.txt
next-state.txt
analysis.status
```

Primary lifecycle dispositions account for all retained semantic classes:

```text
MATERIALIZE_SELECTED_STATIC_ELF
MATERIALIZE_REQUIRED_DYNAMIC_ELF
EXCLUDE_CPU_BASE_GRAPHICS_FEATURE
REFERENCE_APP_LOCAL
REFERENCE_WORLD_SUBSTRATE
REFERENCE_WORLD_LOCALE
MATERIALIZE_SELECTED_FONT
GENERATE_GSETTINGS_SCHEMA
ISOLATED_MUTABLE_STATE
REGENERATE_RUNTIME_CACHE
REFERENCE_OPTIONAL_GPU_DEVICE
```

Expected structural counts:

```text
semantic_objects                         161
semantic_disposition_coverage            161
elf_objects                              113
external_static_elf_materialize           87
nss_dynamic_elf_materialize                4
total_elf_materialize                     91
graphics_dynamic_elf_excluded             11
app_local_elf_reference                     5
world_elf_reference                         6
app_local_data_reference                    6
world_locale_reference                     12
selected_font_materialize                   4
gsettings_aggregate_generate                1
schema_source_files                        37
mutable_state_objects                      19
fontconfig_cache_objects                    4
mesa_cache_objects                          1
gpu_device_objects                          1
selected_elf_lookup_collisions              0
unclassified_objects                        0
```

Expected next state:

```text
READY_FOR_CANDIDATE_MATERIALIZATION_DESIGN
```

### Canonical command

```bash
cd "$HOME/projects/termux-native-desktop"

git fetch origin
git merge --ff-only origin/docs/post-graphics-architecture-audit

B1_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b1-retained-control-locality-20260711-192919"
B3_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b3-capability-grouping-corrected-20260711-204914"
B4_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b4-entrypoint-static-capability-matrix-20260711-211933"
B5_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b5-data-capability-provenance-20260711-214050"
B6_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b6-gsettings-schema-reproduction-corrected-20260711-222459"

out="selected-obsidian-phase-b7-complete-cpu-candidate-manifest-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"

B1_OUT="$B1_OUT" \
B3_OUT="$B3_OUT" \
B4_OUT="$B4_OUT" \
B5_OUT="$B5_OUT" \
B6_OUT="$B6_OUT" \
OUT="$OUT" \
python \
  experiments/glibc/selected-obsidian-closure/recipe/synthesize-selected-cpu-candidate-manifest.py

tar czf ~/Downloads/$out.tgz $OUT
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
    -> immutable object-store and atomic activation design
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
rerun Phase B1-B6 without a source trigger;
copy opaque rootfs gschemas.compiled;
copy glibc locale into the application generation;
expand the selected font set by directory inertia;
make one provider tree per direct root or one untyped candidate blob;
copy app-local/world ELF or include Vulkan provider roots in the CPU base;
materialize candidate bytes before Phase B7 interpretation;
implement activation before object-store and rollback semantics are documented;
rerun closed graphics gates;
start PyMOL by extending the broad farm.
```
