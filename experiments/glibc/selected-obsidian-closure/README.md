# Selected Obsidian AppDir Closure Pilot

## Status

```text
ACTIVE_ARCHITECTURE_DISCRIMINATION
PARENT_QUESTION_NOT_CLOSED
PHASE_B1_PASS
PHASE_B2_PASS
PHASE_B3_CORRECTED_PASS
PHASE_B4_ENTRYPOINT_STATIC_MATRIX_NEXT
```

The selected application-domain candidate has **not** yet been materialized or validated.

## Parent question

Can a real Electron AppDir consume selected external provider closures while preserving valid application-local `$ORIGIN` locality and keeping world, provider, data, graphics, security, and mutable-state responsibilities separate?

Graphics startup is already closed separately. This pilot tests the broader application/provider architecture.

## Authority

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
docs/refactor/0093-post-audit-direction-validator-lifecycle-and-selected-closure-reentry.md
docs/refactor/0094-selected-obsidian-phase-b1-retained-control-locality-pass.md
docs/refactor/0095-selected-obsidian-phase-b2-static-runtime-closure-pass.md
docs/refactor/0096-selected-obsidian-phase-b3-first-run-script-failure.md
docs/refactor/0097-selected-obsidian-phase-b3-capability-grouping-pass.md
```

## Current decision

```text
selected Obsidian closure:
    CONTINUE

fresh control capture:
    NOT REQUIRED FOR IDENTITY DRIFT

candidate materialization:
    BLOCKED UNTIL STATIC/DATA CAPABILITY OWNERSHIP

atomic activation:
    DEFER UNTIL MANAGED OBJECT SET IS DECIDED

PyMOL runtime mutation:
    DEFER
```

## Phase B1 — retained identity/locality

Receipt:

```text
selected-obsidian-phase-b1-retained-control-locality-20260711-192919
```

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

Locality invariant:

```text
preserve $ORIGIN first;
reject future selected-provider lookup collisions unless replacement is an
explicit and separately validated application contract;
do not accept $HOME/gl/lib as final candidate authority.
```

## Phase B2 — static/runtime partition

Receipt:

```text
selected-obsidian-phase-b2-static-runtime-closure-20260711-195310
```

```text
ELF objects                              113
resolved DT_NEEDED edges                 531
entrypoint-static closure                 95
all-app-local static closure              98
mapped-only dynamic/discovery             15
non-ELF data capability                   17
unresolved edge                            0
ambiguous edge                             0
duplicate provider lookup                  0
```

The B2 archive omitted the nested source copy of `semantic-objects.tsv`; the separately retained B1+B2 archive chain supports full verification. No runtime rerun is justified for that packaging-only boundary.

## Phase B3 — corrected capability grouping

Failed first receipt:

```text
selected-obsidian-phase-b3-capability-grouping-20260711-203153
    INVALID
    recipe aborted during family lookup
```

Corrected receipt:

```text
selected-obsidian-phase-b3-capability-grouping-corrected-20260711-204914
```

Archive SHA-256:

```text
9700e71be0795a8a2634deb1c369d1aa0d5c0878cbd7b244091318702521ab7c
```

Captured head:

```text
2fe66ebca11104fa946848ede18df1ef57ad2d58
```

```text
mapped-only objects                       15
dynamic discovery roots                    5
unclassified dynamic roots                 0
shared mapped-only support                  1
entrypoint direct providers                34
data capability objects                    17
runtime launch                             NO
promoted runtime mutation                  NO
```

### Dynamic roots

```text
GRAPHICS_VULKAN
    libvulkan_freedreno.so
    libVkLayer_MESA_device_select.so

NSS_SECURITY
    libfreeblpriv3.so
    libnssckbi.so
    libsoftokn3.so
```

The remaining mapped-only objects are root support dependencies.

### Graphics decision

```text
minimum provider-neutral CPU candidate:
    excludes GRAPHICS_VULKAN dynamic roots

GPU feature composition:
    uses the separately closed graphics provider/feature contract
```

The retained old control mapping does not override the current accepted CPU policy receipt.

### NSS/security decision direction

The first CPU selected candidate must preserve a distinct NSS/security capability containing:

```text
libnss3 direct/static members
libnspr4 support
freebl / trust / softokn dynamic modules
libsqlite3 support required by softokn
world substrate supplied separately
```

### Entrypoint direct-provider boundary

```text
APP_LOCAL_ELF                    1
WORLD_SUBSTRATE_ELF              5
PROVIDER_PREFIX_ELF              6
PROVIDER_ROOTFS_ELF             21
PROVIDER_GRAPHICS_GBM_ELF        1
----------------------------------
total                           34
```

The 28 external direct roots are heterogeneous. They must not become one permanent Electron provider object merely because the entrypoint names them directly.

## Data capabilities

```text
locale:
    glibc 2.42
    12 objects

fonts:
    DejaVu / Noto packages
    4 objects

GSettings schema:
    generated rootfs aggregate
    1 object
    package=UNOWNED
    version=UNKNOWN
```

Data remains outside ELF closure. Schema provenance remains unresolved.

## Phase B4 — entrypoint-static capability matrix

Recipe:

```text
recipe/derive-retained-control-entrypoint-static-groups.py
```

It consumes the corrected Phase B3 output and derives:

```text
28 external direct-root closures;
root-specific external/full closure counts;
root package sets;
shared external support objects;
pairwise direct-root overlap;
external package dependency edges;
entrypoint direct semantic summary;
root-package union summaries.
```

Outputs:

```text
external-direct-root-candidates.tsv
external-direct-root-closure.tsv
external-direct-root-packages.tsv
shared-external-support.tsv
direct-root-overlap.tsv
external-package-dependency-edges.tsv
entrypoint-direct-semantic-summary.tsv
root-package-group-summary.tsv
summary.tsv
claim-boundary.txt
next-state.txt
analysis.status
```

It launches no process and mutates no promoted state.

### Canonical command

```bash
cd "$HOME/projects/termux-native-desktop"

git fetch origin
git merge --ff-only origin/docs/post-graphics-architecture-audit

B3_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b3-capability-grouping-corrected-20260711-204914"
out="selected-obsidian-phase-b4-entrypoint-static-capability-matrix-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"

B3_OUT="$B3_OUT" \
OUT="$OUT" \
python \
  experiments/glibc/selected-obsidian-closure/recipe/derive-retained-control-entrypoint-static-groups.py

tar czf ~/Downloads/$out.tgz $OUT
```

Expected structural values:

```text
entrypoint_direct_providers             34
external_direct_roots                   28
app_local_direct_roots                   1
world_direct_roots                       5
prefix_direct_roots                      6
rootfs_direct_roots                     21
graphics_gbm_direct_roots                1
```

The numbers of shared support objects, overlap pairs, and package dependency edges are computed from the authoritative device receipt and must be inspected rather than hard-gated as architecture invariants.

Expected next state:

```text
READY_FOR_STATIC_CAPABILITY_OWNERSHIP_DECISION
```

## Claim boundary

Phase B4 may prove:

```text
external direct-root closure identities;
root/package dependency overlap;
shared external support;
entrypoint direct semantic distribution;
static grouping inputs.
```

It does not prove:

```text
final capability ownership;
that package boundaries are activation boundaries;
dynamic-root caller/search paths;
candidate materialization or actual selection;
control/candidate equivalence.
```

## Candidate flow

```text
retained control
    -> Phase B1 identity/locality
    -> Phase B2 static/runtime partition
    -> Phase B3 dynamic capability grouping
    -> Phase B4 entrypoint-static overlap matrix
    -> static/data ownership decision
    -> selected CPU candidate manifest/materialization
    -> candidate-specific launch and maps proof
    -> app-local preservation
    -> protected substrate proof
    -> zero broad-farm/rootfs ELF-provider leakage
    -> control/candidate equivalence
```

## Evidence handoff

Every stage defines stage-specific `out` and `OUT` and ends with:

```bash
tar czf ~/Downloads/$out.tgz $OUT
```

## Stop line

Do not:

```text
replace the broad farm globally;
change the promoted Obsidian launcher;
rewrite AppDir RPATH;
rerun Phase B1/B2/B3 without a source trigger;
include graphics dynamic roots in the minimum CPU candidate;
drop NSS dynamic roots or sqlite support;
copy all 113 ELF objects into one candidate/lib;
treat all 95 static objects or all 34 direct providers as one semantic provider;
merge locale/font/schema data into ELF closure;
materialize candidate bytes before static/data ownership is decided;
rerun closed graphics gates;
start PyMOL by expanding the unresolved broad closure.
```
