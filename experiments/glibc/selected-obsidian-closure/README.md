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
PHASE_B8_PASS
PHASE_B9_STAGING_MATERIALIZATION_NEXT
```

The selected CPU generation has not yet been materialized, selected, or runtime-validated.

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
docs/refactor/0103-selected-obsidian-phase-b8-generation-layout-preflight-pass.md
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

## Closed evidence summary

### Phase B1–B4

```text
semantic objects                          161
ELF objects                              113
DT_NEEDED edges                          531
entrypoint-static closure                 95
mapped-only objects                       15
external static union                     87
required NSS dynamic objects               4
excluded graphics-feature objects         11
selected lookup collisions                 0
```

### Phase B5 and corrected Phase B6

```text
locale:
    12 protected-world files

selected fonts:
    4 exact package-owned files

GSettings source closure:
    37 package-owned files

compiler:
    $PREFIX/bin/glib-compile-schemas
    glib 2.88.2

aggregate reproduction:
    default byte-identical
    strict byte-identical
```

The first Phase B6 receipt remains diagnostic evidence for the incomplete 36-file source manifest.

### Phase B7

Receipt:

```text
selected-obsidian-phase-b7-complete-cpu-candidate-manifest-20260711-225234
```

```text
analysis.status:
    PASS

next-state:
    READY_FOR_CANDIDATE_MATERIALIZATION_DESIGN

semantic disposition coverage:
    161 / 161

ELF accounting:
    113 / 113

selected ELF:
    91

selected fonts:
    4

generated schema aggregates:
    1

unclassified objects:
    0
```

### Phase B8

Receipt:

```text
selected-obsidian-phase-b8-generation-layout-preflight-20260711-231228
```

Archive SHA-256:

```text
d68205e9bf99f9a0d711068c560ac5047a5560f31d109efe7aeac107002d31e8
```

Captured head:

```text
37c64a0c55fb76b71532888a1b603c4610c2aec0
```

```text
analysis.status:
    PASS

next-state:
    READY_FOR_STAGING_MATERIALIZER_IMPLEMENTATION

source identity checks:
    133

source identity failures:
    0

content identities:
    96

duplicate content hashes:
    0

generation aliases:
    175

alias collisions:
    0

candidate bytes materialized:
    NO
```

Generation identity:

```text
generation digest:
    435ac66d15de2e9a3188a31bde073ec778dfcb176190d104b513e643e7b4bc5b

generation ID:
    obsidian-cpu-435ac66d15de2e9a3188
```

The combined namespace contains:

```text
91 lookup-name aliases
79 additional source-basename aliases
4 font aliases
1 generated-schema alias
```

All alias paths and relative targets were independently verified and collision-free.

## Repository-state note

A prior `python -m py_compile` created:

```text
experiments/glibc/selected-obsidian-closure/recipe/__pycache__/
```

It is untracked and did not affect the tracked-tree gate. Remove it before the next run:

```bash
rm -rf experiments/glibc/selected-obsidian-closure/recipe/__pycache__
```

## Accepted generation layout

```text
$HOME/gl/selected/obsidian/
    objects/sha256/<first-two-hex>/<sha256>
    staging/<transaction>
    generations/obsidian-cpu-435ac66d15de2e9a3188/
        lib/
        share/fonts/selected/
        share/glib-2.0/schemas/
        manifests/
        receipts/
    current
```

`current` must remain absent or unchanged through Phase B9 and explicit-generation validation.

## Phase B9 — staging-only materialization

Recipe:

```text
recipe/materialize-selected-cpu-generation.py
```

Phase B9 is the first candidate-byte mutation, but it is not promotion.

It:

```text
consumes the completed Phase B8 receipt;
rechecks all 133 source identities immediately before copying;
rebuilds GSettings with --strict and requires empty stdout/stderr;
requires the generated aggregate to match the accepted SHA-256;
creates or hash-verifies 96 content-addressed objects;
constructs all 175 aliases in a unique staging directory;
embeds B7/B8 manifests and contracts;
validates hashes, alias targets, manifests, and permissions;
fsyncs the staged tree;
freezes the generation owner-read-only;
publishes it with one same-filesystem rename;
verifies current before and after and requires no change;
launches no process.
```

Content-object publication:

```text
new object:
    fsynced temporary file
    hash verification
    owner-read-only mode
    no-overwrite hard-link publication
    directory fsync

existing object:
    plain regular file only
    exact hash required
    owner-read-only mode required
```

Generation publication:

```text
staging/<transaction>
    -> complete validation
    -> fsync
    -> freeze read-only
    -> one rename
    -> generations/<generation-id>
```

An already-existing generation is reused only if the complete aliases, objects, embedded manifest hashes, and immutable modes validate.

Expected next state:

```text
READY_FOR_EXPLICIT_GENERATION_VALIDATION
```

### Canonical command

```bash
cd "$HOME/projects/termux-native-desktop"

git fetch origin
git merge --ff-only origin/docs/post-graphics-architecture-audit

rm -rf \
  experiments/glibc/selected-obsidian-closure/recipe/__pycache__

B8_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b8-generation-layout-preflight-20260711-231228"
out="selected-obsidian-phase-b9-staging-generation-materialization-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"

B8_OUT="$B8_OUT" \
OUT="$OUT" \
python \
  experiments/glibc/selected-obsidian-closure/recipe/materialize-selected-cpu-generation.py

tar czf ~/Downloads/$out.tgz $OUT
```

Inspect at minimum:

```text
analysis.status
failure-stage.txt
next-state.txt
summary.tsv
input-verification.tsv
source-identity-recheck.tsv
schema-generation.tsv
schema-generation.stdout.txt
schema-generation.stderr.txt
object-materialization.tsv
generation-validation.tsv
current-state-before.tsv
current-state-after.tsv
claim-boundary.txt
```

Expected structural values on the first clean run:

```text
source_identity_checks:
    133

source_identity_failures:
    0

content_objects:
    96

content_objects_created:
    96

content_objects_reused:
    0

generation_aliases:
    175

generation_validation_failures:
    0

schema_generated_cleanly:
    YES

schema_byte_identical:
    YES

current_pointer_changed:
    NO

runtime_launch_performed:
    NO

candidate_bytes_materialized:
    YES

promoted_runtime_mutated:
    NO
```

A safe rerun may instead report reused objects and:

```text
publication_state:
    REUSED_EXISTING_VALID_GENERATION
```

## Candidate flow

```text
B1 identity/locality
    -> B2 static/runtime partition
    -> B3 dynamic capability grouping
    -> B4 static ownership model
    -> B5 data identity/ownership
    -> corrected B6 schema reproduction
    -> B7 complete candidate manifest
    -> B8 source/content/alias/layout preflight
    -> B9 staging-only materialization
    -> explicit-generation loader/workload validation
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
rerun Phase B1-B8 without a source trigger;
write candidate objects into the broad farm;
create or replace current during Phase B9;
activate a partial or unvalidated generation;
copy app-local/world objects or excluded graphics objects into the CPU base;
change the promoted launcher before explicit-generation validation;
make immutable generation files or directories owner-writable;
garbage-collect objects or generations;
start PyMOL by extending the broad farm.
```
