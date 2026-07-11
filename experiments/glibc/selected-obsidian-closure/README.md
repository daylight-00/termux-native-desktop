# Selected Obsidian AppDir Closure Pilot

## Status

```text
ACTIVE_ARCHITECTURE_DISCRIMINATION
PARENT_QUESTION_NOT_CLOSED
PHASE_B1_PASS
PHASE_B2_PASS
PHASE_B3_CAPABILITY_GROUPING_NEXT
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
```

## Current decision

```text
selected Obsidian closure:
    CONTINUE

fresh control capture:
    NOT REQUIRED FOR IDENTITY DRIFT

candidate materialization:
    BLOCKED UNTIL CAPABILITY OWNERSHIP DECISION

atomic activation:
    DEFER UNTIL MANAGED OBJECT SET IS DECIDED

PyMOL runtime mutation:
    DEFER
```

## Phase B1 — retained identity/locality

Canonical receipt:

```text
$PREFIX/tmp/selected-obsidian-closure/
    selected-obsidian-phase-b1-retained-control-locality-20260711-192919
```

Archive SHA-256:

```text
aa5081f3b5ec8d7fee5e33db631abe0fd695d1291eeddcb54d3777ca72f3e383
```

Result:

```text
semantic objects                          161
candidate-relevant identity matches      136 / 136
ELF objects                               113
DT_NEEDED edges                           531
semantic review                              0
hash mismatches                              0
missing candidate paths                      0
APP_LOCAL/external lookup collisions         0
unresolved dependency names                  0
ambiguous dependency names                   0
```

No workload was launched and no promoted state was mutated.

### Locality invariant

App-local ELF:

```text
obsidian
libEGL.so
libGLESv2.so
libffmpeg.so
libvulkan.so.1
```

All retain:

```text
$ORIGIN
    -> $PREFIX/glibc/lib
    -> $HOME/gl/lib
```

No mapped external object has a colliding lookup name.

Therefore:

```text
preserve $ORIGIN first;
reject future colliding selected providers unless replacement is an explicit,
separately validated application contract;
do not accept $HOME/gl/lib as final candidate authority.
```

## Phase B2 — static/runtime partition

Canonical receipt:

```text
$PREFIX/tmp/selected-obsidian-closure/
    selected-obsidian-phase-b2-static-runtime-closure-20260711-195310
```

Archive SHA-256:

```text
70847e572fc338f20b3369e4b8af71aa0f3033b47857bd956e9b55289ca2e65a
```

Captured head:

```text
26546a015708765cd8a624a8bb4976a8db191d2a
```

Result:

```text
ELF objects                                 113
resolved DT_NEEDED edges                    531
entrypoint-static closure                    95
all-app-local static closure                 98
mapped-only dynamic/discovery                15
non-ELF data capabilities                    17
unresolved edges                              0
ambiguous edges                               0
duplicate provider lookup names               0
```

The independent graph reconstruction matched every count and partition row.

### Static partition

```text
ENTRYPOINT_STATIC_CLOSURE
    APP_LOCAL_ELF                         2
    WORLD_SUBSTRATE_ELF                   6
    PROVIDER_PREFIX_ELF                  32
    PROVIDER_ROOTFS_ELF                  54
    PROVIDER_GRAPHICS_GBM_ELF             1

AUX_APP_LOCAL_STATIC_CLOSURE
    APP_LOCAL_ELF                         3
```

Auxiliary app-local roots:

```text
libEGL.so
libGLESv2.so
libvulkan.so.1
```

Their dependency providers are already in the entrypoint-static closure.

## Dynamic root refinement

The 15 mapped-only objects reduce to five roots under the mapped-only dependency graph:

```text
libvulkan_freedreno.so
libVkLayer_MESA_device_select.so
libfreeblpriv3.so
libnssckbi.so
libsoftokn3.so
```

The remaining ten objects are support dependencies.

### Graphics direction

`libvulkan_freedreno.so` reaches itself plus:

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

`libVkLayer_MESA_device_select.so` reaches itself plus:

```text
libxcb-dri3.so.0
```

`libxcb-dri3.so.0` is shared by the two graphics roots.

### NSS/security direction

```text
libfreeblpriv3.so
libnssckbi.so
libsoftokn3.so
    -> libsqlite3.so.0
```

These are main-process dynamic modules/support and are not part of the graphics capability.

## Data capabilities

```text
locale data:
    12
    glibc 2.42 prefix

font data:
    4
    Debian packages

GSettings schema:
    1
    generated rootfs aggregate
```

Data is not an ELF closure member.

`gschemas.compiled` has stable byte identity but `UNOWNED/UNKNOWN` package provenance. Reproducible selected use requires explicit schema input/compilation provenance or deliberate rootfs-backed authority.

## B2 packaging boundary

The authoritative device verified B1 `input/semantic-objects.tsv`, but the B2 tgz did not embed that nested source file.

```text
B2 calculations and outputs:
    VALID

B2 archive alone:
    not sufficient to regenerate data-capabilities.tsv

retained B1 + B2 archive chain:
    sufficient for independent verification
```

This is a packaging-only boundary. It does not justify a runtime rerun.

## Phase B3 — capability-grouping input

Recipe:

```text
recipe/derive-retained-control-capability-groups.sh
```

It consumes only files actually embedded in the Phase B2 output and emits:

```text
dynamic-root-candidates.tsv
dynamic-root-closure.tsv
dynamic-root-members.tsv
shared-dynamic-support.tsv
entrypoint-direct-providers.tsv
partition-package-summary.tsv
data-capability-summary.tsv
suggested-dynamic-family-summary.tsv
summary.tsv
claim-boundary.txt
next-state.txt
analysis.status
```

It launches no process and mutates no promoted state.

Suggested family labels are decision inputs, not final ownership.

### Canonical command

```bash
cd "$HOME/projects/termux-native-desktop"

git fetch origin
git merge --ff-only origin/docs/post-graphics-architecture-audit

B2_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b2-static-runtime-closure-20260711-195310"
out="selected-obsidian-phase-b3-capability-grouping-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"

B2_OUT="$B2_OUT" \
OUT="$OUT" \
bash \
  experiments/glibc/selected-obsidian-closure/recipe/derive-retained-control-capability-groups.sh

tar czf ~/Downloads/$out.tgz $OUT
```

Expected next state:

```text
READY_FOR_CAPABILITY_OWNERSHIP_DECISION
```

## Claim boundary

Phase B3 may prove:

```text
dynamic discovery-root count;
root-specific dependency closure;
shared dynamic support;
entrypoint direct provider set;
partition/package distribution;
data capability distribution.
```

It does not prove:

```text
exact dlopen caller or search path;
final capability ownership;
that all entrypoint-static objects form one object;
candidate materialization or selection;
control/candidate equivalence.
```

## Candidate flow

```text
retained control
    -> Phase B1 identity/locality
    -> Phase B2 static/runtime partition
    -> Phase B3 capability-grouping inputs
    -> capability/data ownership decision
    -> selected provider materialization
    -> candidate-specific CPU launch
    -> actual selection/maps proof
    -> app-local preservation
    -> protected substrate proof
    -> zero broad-farm/rootfs provider leakage
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
copy all 113 ELF objects into one candidate/lib;
treat all 95 static objects as one semantic provider;
treat all 15 mapped-only objects as independent roots;
drop dynamic support objects;
merge graphics and NSS/security closures;
merge locale/font/schema data into ELF closure;
materialize candidate bytes before ownership is decided;
rerun closed graphics gates;
start PyMOL by expanding the unresolved broad closure.
```
