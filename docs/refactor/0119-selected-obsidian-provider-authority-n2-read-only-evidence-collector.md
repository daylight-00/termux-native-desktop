# 0119 — Selected Obsidian Provider-Authority N2 Read-Only Evidence Collector

## Status

The N2 collector is implemented and repository-ready.

```text
implementation state:
    READY_FOR_DEVICE_EXECUTION

device receipt:
    NOT YET PRODUCED

runtime implementation:
    NO

package operation:
    NO

workload launch:
    NO

generation mutation:
    NO

current activation:
    NO

promoted launcher change:
    NO

provider decision:
    NO
```

This record implements the read-only evidence phase defined by `0118`. It does not complete N2 until the device receipt passes and is independently reviewed.

## Authority

Read under:

```text
docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md
docs/refactor/0117-provider-authority-intervention-adoption-and-execution-order.md
docs/refactor/0118-selected-obsidian-provider-authority-census-schema-and-evidence-plan.md
docs/handoff/2026-07-12-selected-obsidian-provider-authority-handoff.md
```

The first immutable selected generation remains historical control evidence. The collector must not reinterpret historical B7 path/action classes as final authority.

## Implementation

```text
experiments/glibc/selected-obsidian-provider-authority/
    README.md
    schema/
        census-columns.tsv
        capability-groups.tsv
    recipe/
        collect-read-only-provider-evidence.py
        run-n2-read-only-provider-evidence.sh
```

The schema is refined with:

```text
DEVICE_RELATION row type;
semicolon-separated overlapping capability groups;
platform.device-udev.termux capability group;
shared.compiler-runtime capability group;
unassigned.prefix-surface holding group.
```

`unassigned.prefix-surface` is procedural. It is not a final semantic authority.

## Accepted historical inputs

The wrapper defaults to the retained local roots recorded by the handoff:

```text
B1_OUT:
    $PREFIX/tmp/selected-obsidian-closure/
        selected-obsidian-phase-b1-retained-control-locality-20260711-192919

B2_OUT:
    $PREFIX/tmp/selected-obsidian-closure/
        selected-obsidian-phase-b2-static-runtime-closure-20260711-195310

B9_OUT:
    $PREFIX/tmp/selected-obsidian-closure/
        selected-obsidian-phase-b9-generation-publication-corrected-20260712-003136

MAP_OUT:
    $PREFIX/tmp/selected-obsidian-closure/
        selected-obsidian-passive-map-selection-diagnostic-20260712-022611

PIXBUF_OUT:
    $PREFIX/tmp/selected-obsidian-closure/
        selected-obsidian-gtk-pixbuf-runtime-capability-inventory-20260712-014314
```

Every required input path, status, and SHA-256 is preflighted and embedded in the new receipt.

A missing local receipt is a hard failure. The collector does not reconstruct it by rerunning a workload.

## Selected/reference evidence synthesis

The collector emits exactly one evidence row for each of the 161 B9 historical semantic-disposition rows.

```text
output:
    selected-reference-object-seed.tsv

base:
    B9 semantic-object-disposition.tsv

enrichment:
    B1 ELF lookup/SONAME/RPATH/RUNPATH
    B2 resolved dependency edges
    B9 content-object plan
    passive map-selection state/classification/identity
    B9 capability memberships
```

The row preserves:

```text
historical semantic class;
historical action;
historical capability membership;
package/version/hash;
app-local $ORIGIN relation;
generation content/object relation;
passive map state;
direct consumers and needed names;
open authority-decision state.
```

It does not populate a final `semantic_class`.

## Supplemental pixbuf/icon/MIME evidence

The accepted read-only inventory is converted into:

```text
supplemental-capability-evidence.tsv
```

Rows cover:

```text
gdk-pixbuf loaders.cache;
loader modules;
icon-theme indexes;
MIME database files.
```

Every row remains:

```text
historical action:
    DIAGNOSTIC_INVENTORY_ONLY

authority decision:
    OPEN
```

The rootfs package/path observation is not promoted into final supply authority.

## Current glibc-prefix package surface

The collector inventories the full currently listed and present filesystem surface under:

```text
$PREFIX/glibc
```

It reads only:

```text
$PREFIX/var/lib/dpkg/status
$PREFIX/var/lib/dpkg/info/*.list
other package control metadata already present
filesystem metadata and regular-file bytes
ELF metadata through readelf
```

It never invokes APT, dpkg transaction commands, package scripts, or cache mutation.

Primary output:

```text
glibc-prefix-package-surface.tsv
```

Per-path evidence includes:

```text
package keys, names, versions, architectures, status;
owned or unowned state;
present or package-listed-missing state;
file type, mode, size;
symlink target and resolved path;
SHA-256 for every current regular file;
ELF class, data, type, machine, interpreter;
SONAME, NEEDED, RPATH, RUNPATH, Build ID;
selected/reference relation;
retained direct consumer edges;
profile pressure only;
evidence state.
```

`profile_pressure` is a search aid, not runtime/research placement.

## Package lifecycle evidence

The collector emits:

```text
package-control-surface.tsv
glibc-prefix-package-summary.tsv
```

Control metadata includes presence, executable state, SHA-256, and size for:

```text
.list
.md5sums
.conffiles
.preinst
.postinst
.prerm
.postrm
.triggers
.shlibs
.symbols
```

This distinguishes raw bytes from package lifecycle/control state without executing that state.

## Immutable and transaction guards

Before census synthesis:

```text
current must be ABSENT;
all B9 content objects must match accepted SHA-256;
$PREFIX/glibc must be a plain directory;
Termux dpkg status/info state must exist;
tracked repository worktree must be clean.
```

During and after collection:

```text
current before == current after;
dpkg status SHA-256 before == after;
dpkg info metadata manifest before == after;
generation object hashes match;
output remains outside generation, rootfs, AppDir, and glibc-prefix trees.
```

Any mismatch is a hard failure.

## Census skeleton

The collector emits:

```text
provider-authority-census.tsv
```

It contains:

```text
capability rows from capability-groups.tsv;
161 selected/reference evidence member rows;
supplemental pixbuf/icon/MIME rows;
non-directory glibc-prefix package/object rows not already represented.
```

All new semantic decisions remain:

```text
semantic_class:
    UNRESOLVED

minimum_valid_scope:
    UNRESOLVED

profile_runtime_or_research:
    UNRESOLVED

update_owner:
    UNRESOLVED

provisional_final_authority:
    UNRESOLVED

authority_decision_state:
    OPEN
```

Historical class/action and package/path evidence remain visible.

## Unresolved evidence ledger

The collector emits:

```text
unresolved-evidence-ledger.tsv
```

One row per capability group records:

```text
current state;
member evidence count;
seed evidence;
missing discriminator;
next permitted action;
open authority state.
```

For pixbuf/icon/MIME, the next permitted action may be the already-authorized bounded discriminator. For other groups, the next action is read-only N3 classification and source comparison.

## Receipt and archive outputs

A passing output root includes:

```text
analysis.status
next-state.txt
claim-boundary.txt
summary.tsv
input-verification.tsv
current-state-before.tsv
current-state-after.tsv
generation-identity-check.tsv
selected-reference-object-seed.tsv
supplemental-capability-evidence.tsv
glibc-prefix-package-surface.tsv
package-control-surface.tsv
glibc-prefix-package-summary.tsv
provider-authority-census.tsv
unresolved-evidence-ledger.tsv
input/
```

The wrapper rejects:

```text
existing OUT or archive paths;
OUT/archive outside the stage evidence base;
symlink or special archive members;
absolute or parent-traversal archive names.
```

## Device execution

First fast-forward the branch:

```bash
git pull --ff-only
```

Then run:

```bash
bash \
  experiments/glibc/selected-obsidian-provider-authority/recipe/run-n2-read-only-provider-evidence.sh
```

Default evidence base:

```text
$PREFIX/tmp/selected-obsidian-provider-authority
```

Expected terminal marker:

```text
N2_PROVIDER_AUTHORITY_EVIDENCE=PASS
```

The wrapper prints:

```text
OUT
ARCHIVE
ARCHIVE_SHA256
```

Upload the printed archive without renaming it unless the upload surface requires a harmless display-name change. Retain the printed SHA-256.

## Development validation

Before repository publication, the implementation passed:

```text
Python syntax compilation:
    PASS

synthetic clean-git fixture:
    PASS

161-row selected/reference coverage gate:
    PASS

read-only dpkg-prefix inventory:
    PASS

current/dpkg before-after guards:
    PASS

safe TGZ generation and SHA-256:
    PASS
```

This is implementation validation only. It is not Termux device evidence and does not pre-judge the real receipt.

## Stop line

Do not:

```text
install or remove packages;
run APT/dpkg transactions;
execute package maintainer scripts;
mutate ldconfig or generated caches;
rerun Obsidian;
mutate the immutable generation;
create current;
change the promoted launcher;
classify prefix paths by location alone;
accept initial capability pressure as final authority;
finalize or materialize a successor;
reopen closed graphics work.
```

## Next state

A reviewed device PASS advances only to:

```text
N3:
    provisional semantic classes
    candidate-source comparison
    unresolved-evidence refinement
```

It does not lift the provider-authority intervention.
