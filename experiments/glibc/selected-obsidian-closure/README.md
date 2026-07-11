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
PHASE_B6_CORRECTED_SOURCE_CLOSURE_NEXT
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
    complete source/compiler reproduction still open
```

## Closed read-only phases

### Phase B1

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

Physical target:

```text
one receipt-owned application-domain generation
    -> deduplicated selected external ELF set
    -> typed capability manifests
    -> separate data subtrees/manifests
    -> later one-pointer atomic activation
```

### Phase B5

Receipt:

```text
selected-obsidian-phase-b5-data-capability-provenance-20260711-214050
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

captured schema source files:
    36

captured schema unowned source files:
    0
```

Phase B5 closes locale and selected-font ownership. It proves ownership of the 36 captured schema inputs, but not complete schema-source closure.

## First Phase B6 diagnostic

Receipt:

```text
selected-obsidian-phase-b6-gsettings-schema-reproduction-20260711-220355
```

Archive SHA-256:

```text
553e52f917a6cc72e805ac8b94bb5fd7d8ecc36809d6c6b5e2e6b226a901b30a
```

Captured head:

```text
68f3de93413dddb861e34d899bc06c49c3363c49
```

```text
analysis.status:
    PASS

reported next-state:
    REVIEW_SCHEMA_COMPILER_VERSION_DIFFERENCE

accepted interpretation:
    REVIEW_SCHEMA_SOURCE_MANIFEST_GAP

compiler:
    $PREFIX/bin/glib-compile-schemas

compiler package/version:
    glib 2.88.2

compiler SHA-256:
    5f8cfe28f5eed9e5b9400260ec0127cae5c3f881437915df3fcdca33cbe5d165
```

Default mode returned zero and generated a non-identical aggregate, but stderr reported ten undefined-enum errors and stated that ten complete schema files were ignored.

Strict mode returned one and stopped at the first undefined enum.

Therefore:

```text
default compile:
    not clean

generated hash difference:
    not a compiler-version-only comparison

complete source closure:
    still open
```

The Phase B5 filter used only:

```text
*.gschema.xml
*.gschema.override
```

and omitted definition XML whose names do not use the `.gschema.xml` suffix.

## Corrected Phase B6

Recipe:

```text
recipe/reproduce-retained-control-gsettings-schema-corrected.sh
```

It does not rerun Phase B5. It creates a receipt-local overlay of the completed B5 receipt, replaces only the schema source manifest with complete directory discovery, and invokes the existing reproduction recipe.

Corrected behavior:

```text
discover all *.xml and *.gschema.override inputs;
record the delta from the 36-file B5 manifest;
record hash and dpkg owner for newly discovered inputs;
compile only in receipt-local directories;
run default and --strict modes;
reject return code zero when stderr reports schema errors;
compare only clean outputs with the retained aggregate;
install no package and mutate no promoted runtime.
```

Possible next states:

```text
READY_FOR_COMPLETE_DATA_MANIFEST
    clean byte-identical output

REVIEW_SCHEMA_COMPILER_VERSION_DIFFERENCE
    clean compile succeeds but output differs

REVIEW_SCHEMA_COMPILATION_ERRORS
    compiler is runnable but no clean compile succeeds

ACQUIRE_SCHEMA_COMPILER_ORACLE
    no runnable compiler candidate
```

### Canonical command

```bash
cd "$HOME/projects/termux-native-desktop"

git fetch origin
git merge --ff-only origin/docs/post-graphics-architecture-audit

B5_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b5-data-capability-provenance-20260711-214050"
out="selected-obsidian-phase-b6-gsettings-schema-reproduction-corrected-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"

B5_OUT="$B5_OUT" \
OUT="$OUT" \
bash \
  experiments/glibc/selected-obsidian-closure/recipe/reproduce-retained-control-gsettings-schema-corrected.sh

tar czf ~/Downloads/$out.tgz $OUT
```

Inspect at minimum:

```text
analysis.status
next-state.txt
summary.tsv
schema-source-manifest-delta.tsv
schema-source-verification.tsv
schema-compiler-candidates.tsv
schema-reproduction-attempts.tsv
attempts/*/stderr.txt
claim-boundary.txt
```

## Candidate flow

```text
B1 identity/locality
    -> B2 static/runtime partition
    -> B3 dynamic capability grouping
    -> B4 static ownership model
    -> B5 data identity/partial source ownership
    -> corrected B6 complete source/compiler reproduction
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
rerun Phase B1-B5;
accept the first B6 default aggregate;
interpret return code zero as clean success without stderr inspection;
classify the first B6 hash difference as compiler-version-only;
install another schema compiler before corrected source discovery;
copy opaque gschemas.compiled without complete source/compiler provenance;
materialize candidate bytes before corrected Phase B6 interpretation;
implement activation before the complete generation manifest;
rerun closed graphics gates;
start PyMOL by extending the broad farm.
```
