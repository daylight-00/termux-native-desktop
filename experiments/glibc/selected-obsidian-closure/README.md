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
PHASE_B9_PASS
PHASE_B10_EXPLICIT_GENERATION_CPU_VALIDATION_NEXT
```

The selected CPU generation is materialized and published but not activated.

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
docs/refactor/0104-selected-obsidian-phase-b9-first-run-hardlink-publication-failure.md
docs/refactor/0105-selected-obsidian-phase-b9-generation-directory-publication-failure.md
docs/refactor/0106-selected-obsidian-phase-b9-generation-materialization-pass.md
```

## Closed architecture

```text
application-local ELF/data:
    reference AppDir
    preserve $ORIGIN locality

protected world ELF/locale:
    reference $PREFIX/glibc
    do not copy

selected CPU ELF:
    87 external static objects
    4 required NSS/security dynamic objects

excluded GPU feature:
    11 Vulkan provider/layer/support objects

selected fonts:
    4 exact content identities

GSettings:
    37 owned sources
    native glib 2.88.2 compiler
    one byte-identical generated aggregate

mutable state and caches:
    receipt/runtime owned
    excluded from immutable generation
```

## Phase B7 manifest closure

```text
semantic objects:
    161 / 161 disposed

ELF objects:
    113 / 113 accounted

selected ELF:
    91

selected fonts:
    4

generated schema:
    1

selected lookup collisions:
    0

unclassified objects:
    0
```

## Phase B8 physical plan

```text
source identity checks:
    133 / 133 MATCH

immutable content identities:
    96

generation aliases:
    175

alias collisions:
    0

generation ID:
    obsidian-cpu-435ac66d15de2e9a3188
```

Accepted layout:

```text
$HOME/gl/selected/obsidian/
    objects/sha256/<prefix>/<sha256>
    staging/
    generations/obsidian-cpu-435ac66d15de2e9a3188/
        lib/
        share/fonts/selected/
        share/glib-2.0/schemas/
        manifests/
        receipts/
    current
```

## Phase B9 materialization

Authoritative receipt:

```text
selected-obsidian-phase-b9-generation-publication-corrected-20260712-003136
```

Archive SHA-256:

```text
ad351651e82d958c1805eed421dc9991ee573b1f79794c34aea6f079df84ec53
```

Captured head:

```text
57aa19febd6df33435afd074eb3b47c150768998
```

```text
analysis.status:
    PASS

next-state:
    READY_FOR_EXPLICIT_GENERATION_VALIDATION

publication_state:
    PUBLISHED_NEW_GENERATION

content objects:
    96

content bytes:
    70,897,301

objects reused after hash verification:
    96

generation aliases:
    175

generation validation:
    1851 / 1851 PASS

current before:
    ABSENT

current after:
    ABSENT
```

Device publication behavior:

```text
0555 generation-root probe:
    EACCES

0700 generation-root probe:
    PUBLISHED

real generation publication:
    renameat2 RENAME_NOREPLACE
    root 0700 during publication
    root restored to 0555 before validation return
```

The generation is complete and immutable but not selected by `current` or the promoted launcher.

## Phase B10 — explicit-generation CPU validation

Files:

```text
recipe/launch-obsidian-explicit-generation-cpu.sh
recipe/run-explicit-generation-cpu-validation.sh
recipe/analyze-explicit-generation-cpu.py
```

B10 must use the absolute final-generation path from the B9 receipt.

Launcher contract:

```text
LD_LIBRARY_PATH:
    <generation>/lib:$PREFIX/glibc/lib

GSETTINGS_SCHEMA_DIR:
    <generation>/share/glib-2.0/schemas

selected fonts:
    receipt-owned fontconfig input
    <generation>/share/fonts/selected only

CPU mode:
    exact --disable-gpu
    Vulkan/Mesa override variables cleared

runtime state:
    XDG config/cache/data/state/runtime under the B10 receipt
    TMPDIR under the B10 receipt

forbidden:
    current
    $HOME/gl/lib broad farm
    rootfs provider paths
```

Expected immutable mapped identities:

```text
selected object-store identities:
    96
    ├─ ELF       91
    ├─ fonts      4
    └─ schema     1

app-local identities:
    11

protected-world identities:
    18

expected immutable mapped total:
    125
```

Receipt-local runtime mappings and non-GPU device mappings are recorded separately. Every other external path is a failure.

Process gates:

```text
main:
    exactly 1

renderer:
    at least 1
    every renderer has --disable-gpu-compositing

zygote:
    at least 1

GPU process:
    0

survival:
    100 seconds
```

Expected next state:

```text
READY_FOR_ATOMIC_ACTIVATION_IMPLEMENTATION
```

### Canonical command

```bash
cd "$HOME/projects/termux-native-desktop"

rm -rf \
  experiments/glibc/selected-obsidian-closure/recipe/__pycache__

git fetch origin
git merge --ff-only origin/docs/post-graphics-architecture-audit

B9_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b9-generation-publication-corrected-20260712-003136"
out="selected-obsidian-phase-b10-explicit-generation-cpu-validation-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"

if B9_OUT="$B9_OUT" \
   OUT="$OUT" \
   bash \
     experiments/glibc/selected-obsidian-closure/recipe/run-explicit-generation-cpu-validation.sh
then
  analysis_rc=0
else
  analysis_rc=$?
fi

printf '\n===== analysis exit status =====\n'
printf '%s\n' "$analysis_rc"

for f in \
  "$OUT/analysis.status" \
  "$OUT/failure-stage.txt" \
  "$OUT/next-state.txt" \
  "$OUT/summary.tsv" \
  "$OUT/process-contract.tsv" \
  "$OUT/missing-expected-mapped-paths.tsv" \
  "$OUT/unexpected-mapped-paths.tsv" \
  "$OUT/mapped-identity-verification.tsv" \
  "$OUT/mapped-path-classification.tsv" \
  "$OUT/current-state-before.tsv" \
  "$OUT/current-state-after.tsv" \
  "$OUT/launch-contract/launch-environment.tsv" \
  "$OUT/launch-contract/argv.txt" \
  "$OUT/capture/class-counts.tsv" \
  "$OUT/capture/processes.tsv" \
  "$OUT/capture/launch.stderr" \
  "$OUT/claim-boundary.txt"
do
  [ -e "$f" ] || continue
  printf '\n===== %s =====\n' "$f"
  cat "$f"
done

tar czf ~/Downloads/$out.tgz $OUT
```

### Syntax-only preflight

This avoids Python bytecode creation:

```bash
python - <<'PY'
import ast
from pathlib import Path

root = Path(
    "experiments/glibc/selected-obsidian-closure/recipe"
)

for name in (
    "analyze-explicit-generation-cpu.py",
):
    path = root / name
    ast.parse(path.read_text(), filename=str(path))
    print(f"{name}: syntax PASS")
PY

bash -n \
  experiments/glibc/selected-obsidian-closure/recipe/launch-obsidian-explicit-generation-cpu.sh

bash -n \
  experiments/glibc/selected-obsidian-closure/recipe/run-explicit-generation-cpu-validation.sh
```

## Candidate flow

```text
B1 identity/locality
    -> B2 static/runtime partition
    -> B3 dynamic capability grouping
    -> B4 static ownership model
    -> B5 data ownership
    -> corrected B6 schema reproduction
    -> B7 complete candidate manifest
    -> B8 content/alias/layout preflight
    -> B9 immutable generation materialization
    -> B10 explicit-generation CPU validation
    -> atomic current activation and rollback
    -> activated-candidate equivalence acceptance
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
rerun Phase B1-B9 without a source or validation trigger;
create current before B10 passes;
use the broad farm in the B10 loader path;
allow rootfs provider leakage;
include the excluded graphics feature in CPU mode;
mutate the published generation;
change the promoted launcher;
garbage-collect the generation or object store;
start PyMOL by extending the broad farm.
```
