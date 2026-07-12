# 0124 — Selected Obsidian Provider-Authority Source Recipe Evidence Collector

## Status

```text
corrected N3 normalized decision surface:
    PASS / ACCEPTED

source recipe evidence collector:
    READY_FOR_DEVICE EXECUTION

binary artifact acquisition:
    NOT STARTED

provider authority decisions:
    NOT ACCEPTED

provider-authority intervention:
    ACTIVE

successor manifest/materialization/current activation:
    BLOCKED
```

This stage correlates the accepted corrected N3 package-pressure surface with the installed dpkg/APT metadata and a clean full clone of the Termux glibc package source repository.

It does not install, upgrade, remove, download, build, or execute a provider.

## Authority

Read under:

```text
docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md
docs/refactor/0117-provider-authority-intervention-adoption-and-execution-order.md
docs/refactor/0118-selected-obsidian-provider-authority-census-schema-and-evidence-plan.md
docs/refactor/0120-selected-obsidian-provider-authority-n2-device-receipt-review.md
docs/refactor/0122-selected-obsidian-provider-authority-n3-receipt-review-and-normalization-correction.md
docs/refactor/0123-selected-obsidian-provider-authority-corrected-n3-receipt-pass-and-source-comparison-entry.md
```

The accepted ordering remains:

```text
semantic responsibility
    -> source recipe and patch evidence
    -> exact binary artifact evidence
    -> provider choice
    -> locked supply identity
    -> update/revalidation contract
    -> successor composition
```

## External source input

The authoritative source repository input is:

```text
https://github.com/termux-pacman/glibc-packages.git
```

The collector does not clone or fetch it. The user prepares one full clean clone outside the project checkout:

```text
$HOME/Downloads/termux-pacman-glibc-packages-source
```

This external clone is evidence input only. It is not project runtime state, a promoted provider, or a submodule.

Required source-clone guards:

```text
origin is the approved termux-pacman repository
full non-shallow clone
clean tracked and untracked state
git fsck connectivity PASS
exact HEAD/tree/parents/commit time recorded
all refs recorded by SHA-256
no source fetch during collection
before/after repository state unchanged
```

A current clone HEAD is not assumed to have built the installed packages. Historical recipe matching is performed across all locally available refs.

## Installed-state guard

The collector requires the live package state to remain identical to the accepted N2 guard embedded through corrected N3:

```text
dpkg status SHA-256:
    unchanged

dpkg info metadata manifest:
    unchanged

installed package identities:
    exact match for all 86 N3 package-pressure rows
```

Any drift is a hard failure. The collector does not reinterpret a changed package state as equivalent evidence.

## Priority packages

The collector retains all 86 installed packages as context and performs recipe-history comparison for the 26 packages with accepted selected/reference or direct-consumer pressure, plus two explicit architecture-context packages.

```text
T0 world/platform boundary:
    glibc
    termux-exec-glibc
    libx11-glibc
    libxau-glibc
    libxcb-glibc
    libxdmcp-glibc
    libxext-glibc
    libxrandr-glibc
    libxrender-glibc
    libxshmfence-glibc

T0 bootstrap context:
    glibc-runner

T1 selected/runtime pressure:
    brotli-glibc
    e2fsprogs-glibc
    gcc-libs-glibc
    krb5-glibc
    libblkid-glibc
    libbz2-glibc
    libcap-glibc
    libdrm-glibc
    libexpat-glibc
    libffi-glibc
    libgmp-glibc
    libidn2-glibc
    libunistring-glibc
    libwayland-glibc
    pcre2-glibc
    zlib-glibc
    zstd-glibc
```

Priority is an investigation order. It is not runtime inclusion or final authority.

## Recipe-history comparison

The collector builds the package-to-recipe map from:

```text
gpkg/*/build.sh
gpkg/**/*.subpackage.sh
```

For each priority package it records:

```text
installed version and architecture
current recipe version
main and subpackage recipe paths
all historical commits whose static recipe version matches the installed version
unique recipe tree identities
source URL declaration
source SHA-256 declaration
dependency/build-dependency/recommendation declarations
commit/tree/time/subject
```

History search covers the complete recipe directory. This is required because patch or auxiliary-file changes can create a different recipe tree without changing `build.sh` or the package version.

Distinct matching recipe trees remain unresolved candidates until build or binary evidence identifies the actual artifact lineage.

## Recipe tree embedding

For each unique candidate recipe tree, the collector inventories:

```text
build.sh
subpackage recipes
patches/diffs
auxiliary C/C++/assembly/header/script/JSON/text inputs
other recipe files
```

It records Git blob identity, mode, size, content SHA-256, role, and embedded state.

Regular files up to 5 MiB are embedded, subject to a 100 MiB receipt limit. Larger files remain manifest-only evidence.

Embedding source recipe files does not authorize their runtime use.

## APT repository metadata

Without `apt update`, package download, or installation, the collector reads the already-present state under:

```text
$PREFIX/etc/apt
$PREFIX/var/lib/apt/lists
$PREFIX/var/cache/apt/archives
```

It records:

```text
.list and Deb822 .sources configuration
source-file SHA-256
Release/InRelease metadata
Packages index identity and compression/parse state
exact installed-version records where locally indexed
repository Filename/Size/SHA256 fields
other locally indexed versions
cached .deb path/size/SHA-256 where present
```

Plain, gzip, bzip2, and xz indexes are decoded directly. LZ4 or zstd indexes are decoded only when an existing decoder command is available. Unsupported compressed indexes remain explicit unresolved evidence; the collector does not install a decoder.

An indexed filename/hash is repository metadata, not proof that the installed bytes came from that exact file.

## Outputs

A passing output includes:

```text
analysis.status
next-state.txt
claim-boundary.txt
summary.tsv
input-verification.tsv
source-repository-state.tsv
recipe-package-map.tsv
installed-package-lineage.tsv
priority-package-set.tsv
apt-source-lines.tsv
apt-index-files.tsv
apt-release-metadata.tsv
repository-package-records.tsv
cached-deb-artifacts.tsv
priority-recipe-lineage.tsv
recipe-candidate-commits.tsv
recipe-file-manifest.tsv
source-comparison-ledger.tsv
input/
recipe-trees/
```

Expected next state:

```text
READY_FOR_BOUNDED_BINARY_ARTIFACT_ACQUISITION_AND_RECIPE_REVIEW
```

This next state permits planning or executing a separately authorized download-only artifact transaction. It does not permit package installation.

## Implementation

```text
experiments/glibc/selected-obsidian-provider-authority/recipe/
    collect-n3-source-recipe-evidence.py
    run-n3-source-recipe-evidence.sh
```

Default inputs and outputs:

```text
corrected N3 root:
    $PREFIX/tmp/selected-obsidian-provider-authority/
        selected-obsidian-provider-authority-n3-normalized-classification-20260712-165805

source clone:
    $HOME/Downloads/termux-pacman-glibc-packages-source

unpacked output:
    $PREFIX/tmp/selected-obsidian-provider-authority/
        selected-obsidian-provider-authority-n3-source-recipe-evidence-<timestamp>

TGZ:
    $HOME/Downloads/
        selected-obsidian-provider-authority-n3-source-recipe-evidence-results-<timestamp>.tgz
```

## Device execution

Prepare the external source input once:

```bash
SOURCE_REPO="$HOME/Downloads/termux-pacman-glibc-packages-source"

test ! -e "$SOURCE_REPO"

git clone \
  https://github.com/termux-pacman/glibc-packages.git \
  "$SOURCE_REPO"
```

Then run from the project checkout:

```bash
git pull --ff-only

bash \
  experiments/glibc/selected-obsidian-provider-authority/recipe/run-n3-source-recipe-evidence.sh
```

Expected terminal marker:

```text
N3_SOURCE_RECIPE_EVIDENCE=PASS
```

The runner prints `OUT`, `SOURCE_REPO`, `ARCHIVE`, and `ARCHIVE_SHA256`.

## Development validation

The implementation passed a clean synthetic transaction containing:

```text
86 installed package identities
28 priority packages
plain APT Packages and Release metadata
.list and Deb822 .sources parsing
cached .deb identity capture
full clean source repository clone guards
installed-version recipe history matching
current-versus-installed recipe divergence
multiple recipe-tree candidates caused only by auxiliary-file changes
recipe-tree embedding
before/after dpkg and source-repository guards
safe TGZ generation
```

Observed fixture result:

```text
analysis.status:
    PASS

installed packages:
    86

priority packages:
    28

recipe mappings:
    28

unique recipe-tree matches:
    27

multiple recipe-tree matches:
    1

exact repository records:
    86

package/runtime/generation/current operations:
    NONE
```

Synthetic validation is implementation evidence only. It does not pre-judge the real device/source receipt.

## Claim boundary

This stage may establish:

```text
which current and historical source recipe trees are candidates for installed package versions
which Android/Termux-specific patches and auxiliary files are present in those recipe trees
which exact repository artifact metadata remains locally available
which binary artifacts are already cached
which packages need bounded artifact acquisition or lineage resolution
```

It may not establish by itself:

```text
which candidate recipe tree actually built the installed bytes
that current source HEAD is final provider authority
that every recipe patch is semantically necessary
that package boundaries equal semantic provider boundaries
that an installed package belongs in the minimum runtime profile
binary artifact identity when no exact artifact is present
source superiority among Termux, Debian, upstream, app-local, native, or project-built candidates
successor composition, activation, or rollback
```

## Stop line

Do not:

```text
run apt update, install, upgrade, remove, autoremove, or package scripts
fetch or mutate the source repository during collection
build packages or source trees
use recipe-version equality as proof of exact binary lineage
use current recipe HEAD as proof of installed package provenance
promote glibc-runner by recommendation or availability
mutate ld.so.conf or ld.so.cache
mutate the immutable selected generation
create current
finalize or materialize a successor
reopen closed graphics work
```
