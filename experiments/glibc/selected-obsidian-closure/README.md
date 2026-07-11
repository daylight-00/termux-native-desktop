# Selected Obsidian AppDir Closure Pilot

## Status

```text
ACTIVE_ARCHITECTURE_DISCRIMINATION
PARENT_QUESTION_NOT_CLOSED
PHASE_B1_PASS
PHASE_B2_PASS
PHASE_B3_CORRECTED_PASS
PHASE_B4_PASS
PHASE_B5_DATA_PROVENANCE_NEXT
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
```

## Current decision

```text
fresh control capture:
    NOT REQUIRED

static ELF ownership model:
    TYPED CAPABILITY MANIFESTS
    OVER ONE DEDUPLICATED APPLICATION-DOMAIN GENERATION

candidate ELF manifest design:
    READY

candidate materialization:
    BLOCKED ON DATA CAPABILITY PROVENANCE

atomic activation:
    DEFER UNTIL COMPLETE GENERATION MANIFEST

PyMOL runtime mutation:
    DEFER
```

## Phase B1 — identity and locality

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

Candidate invariant:

```text
preserve $ORIGIN first;
leave application-local ELF in the AppDir;
reject future external lookup collisions unless replacement is separately validated;
do not accept $HOME/gl/lib as final candidate authority.
```

## Phase B2 — static/runtime partition

```text
entrypoint-static closure                 95
all-app-local static closure              98
mapped-only dynamic/discovery             15
non-ELF data capability                   17
```

The B2 tgz omitted the nested source copy of `semantic-objects.tsv`. The retained B1+B2 archive chain is sufficient for complete verification. No runtime rerun is justified.

## Phase B3 — dynamic capability grouping

Corrected receipt:

```text
selected-obsidian-phase-b3-capability-grouping-corrected-20260711-204914
```

```text
mapped-only objects                       15
dynamic discovery roots                    5
unclassified dynamic roots                 0
shared mapped-only support                  1
entrypoint direct providers                34
data capability objects                    17
```

Dynamic families:

```text
GRAPHICS_VULKAN
    libvulkan_freedreno.so
    libVkLayer_MESA_device_select.so

NSS_SECURITY
    libfreeblpriv3.so
    libnssckbi.so
    libsoftokn3.so
        -> libsqlite3.so.0
```

Decision:

```text
minimum provider-neutral CPU candidate:
    exclude GRAPHICS_VULKAN dynamic roots

required CPU application capability:
    preserve NSS/NSPR static support, dynamic NSS modules, and SQLite support
```

The first failed B3 archive remains invalid and preserved separately.

## Phase B4 — entrypoint-static matrix

Receipt:

```text
selected-obsidian-phase-b4-entrypoint-static-capability-matrix-20260711-211933
```

Archive SHA-256:

```text
3829cf756dc2a6526ca59073d245a1696b60fcaada0116ad386b9c941911258a
```

Captured head:

```text
3fbe8ce5026b02f6de1e4e9e55c16dbf41beb5aa
```

```text
entrypoint direct providers               34
external direct roots                     28
external static union                     87
shared external support                   51
direct-root overlap pairs                111
external package dependency edges        144
```

Direct semantic distribution:

```text
APP_LOCAL_ELF                    1
WORLD_SUBSTRATE_ELF              5
PROVIDER_PREFIX_ELF              6
PROVIDER_ROOTFS_ELF             21
PROVIDER_GRAPHICS_GBM_ELF        1
```

### Dominant GUI closure

The GTK root has:

```text
60 external objects
63 full objects
51 external packages
```

Eighteen other external direct roots are fully contained in that closure.

### Residual static directions

```text
GBM static ABI support
compiler support
ALSA audio
CUPS printing
NSS/NSPR security
udev device observation
```

Static GBM remains in the CPU candidate because the executable directly requires it. It is separate from Vulkan provider selection and application GPU feature mode.

### Physical candidate direction

Do not create one copied provider tree per direct root. Do not create one untyped flat blob.

Use:

```text
one receipt-owned application-domain generation
    -> one deduplicated selected external ELF set
    -> typed capability manifests
    -> app-local payload referenced in place
    -> world substrate referenced but not copied
    -> graphics provider feature composed separately
    -> data capabilities stored separately from ELF
```

## Minimum CPU ELF direction

```text
include:
    87 selected external static ELF objects
    required NSS/security dynamic roots and support

exclude:
    APP_LOCAL ELF copies
    WORLD_SUBSTRATE copies
    Turnip dynamic provider root
    Mesa Vulkan device-selection layer root
    GPU-feature-only dynamic support
```

## Data blocker

Retained data set:

```text
PROVIDER_LOCALE_DATA:
    12

PROVIDER_FONT_DATA:
    4

PROVIDER_SCHEMA_DATA:
    1
```

`gschemas.compiled` has stable identity but `UNOWNED/UNKNOWN` aggregate provenance.

## Phase B5 — data capability provenance

Recipe:

```text
recipe/audit-retained-control-data-capabilities.py
```

It consumes the Phase B2 data receipt and performs no workload launch or promoted mutation.

It verifies:

```text
current/captured SHA-256 identity for all 17 data objects;
rootfs file ownership from dpkg .list files;
font package ownership;
GSettings XML and override source manifest;
GSettings source package ownership;
glib-compile-schemas binary identity and ownership;
proposed locale/font/schema ownership directions.
```

Outputs:

```text
data-object-verification.tsv
schema-source-manifest.tsv
schema-compiler-verification.tsv
data-ownership-decision-input.tsv
summary.tsv
claim-boundary.txt
next-state.txt
analysis.status
```

Proposed directions, subject to the receipt:

```text
PROVIDER_LOCALE_DATA
    -> WORLD_LOCALE_GLIBC
    -> reference prefix-managed data

PROVIDER_FONT_DATA
    -> SELECTED_FONT_DATA
    -> materialize exact package-owned files

PROVIDER_SCHEMA_DATA
    -> SELECTED_GSETTINGS_SCHEMA_DATA
    -> rebuild from owned source manifest and compiler provenance
```

### Canonical command

```bash
cd "$HOME/projects/termux-native-desktop"

git fetch origin
git merge --ff-only origin/docs/post-graphics-architecture-audit

B2_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b2-static-runtime-closure-20260711-195310"
out="selected-obsidian-phase-b5-data-capability-provenance-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"

B2_OUT="$B2_OUT" \
OUT="$OUT" \
python \
  experiments/glibc/selected-obsidian-closure/recipe/audit-retained-control-data-capabilities.py

tar czf ~/Downloads/$out.tgz $OUT
```

Possible next states:

```text
READY_FOR_DATA_OWNERSHIP_DECISION
REVIEW_DATA_PROVENANCE_GAPS
```

A PASS with `REVIEW_DATA_PROVENANCE_GAPS` is a valid completed audit containing unresolved provenance rows; it is not a script failure.

## Candidate flow

```text
Phase B1 identity/locality
    -> Phase B2 static/runtime partition
    -> Phase B3 dynamic grouping
    -> Phase B4 static overlap and ownership model
    -> Phase B5 data provenance
    -> complete CPU candidate manifest
    -> candidate materialization
    -> candidate-specific launch/maps proof
    -> app-local and world-substrate boundary proof
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
rerun Phase B1-B4 without a source trigger;
make one copied provider tree per direct root;
make one untyped 87-object blob;
copy app-local or world substrate ELF into the candidate;
include Vulkan provider dynamic roots in the minimum CPU candidate;
drop NSS dynamic modules, SQLite support, or static GBM;
merge locale/font/schema data into ELF closure;
materialize candidate bytes before Phase B5 interpretation;
implement activation before the complete generation manifest;
start PyMOL by expanding the broad farm.
```
