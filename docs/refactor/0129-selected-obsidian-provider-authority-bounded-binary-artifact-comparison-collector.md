# 0129 — Selected Obsidian Provider-Authority Bounded Binary Artifact Comparison Collector

## Status

```text
accepted source-recipe receipt:
    PASS

bounded binary artifact collector:
    READY_FOR DEVICE EXECUTION

provider authority decisions:
    NOT ACCEPTED

successor composition/materialization/current activation:
    BLOCKED
```

## Purpose

This transaction acquires only the 28 exact installed-version `.deb` artifacts identified by the accepted source-recipe receipt.

It verifies repository artifact identity and compares package payload members with the unchanged live installation without installing a package or executing package code.

## Inputs

Default accepted source receipt:

```text
$PREFIX/tmp/selected-obsidian-provider-authority/
    selected-obsidian-provider-authority-n3-source-recipe-evidence-20260712-185001
```

Accepted source receipt SHA-256 at archive level:

```text
c8160016267f3ff83b348146240f74f808ffbc93374a6f75988231ef22408cdb
```

The collector revalidates the unpacked receipt's status, next-state, captured identities, source guard, priority cardinality, exact repository records, and zero accepted authority decisions.

The live dpkg guard must still equal:

```text
dpkg status:
    aba4d9e78f68bd0fe5d841b5d1422255ecca162621c85630137651122bcc8ee2

dpkg info manifest:
    f1a32ecdf5cbe1999fbf4b2aeae28196e8a1ca215b17a4e2f4153578dce414e4
```

## Bounded download plan

```text
priority packages:
    28

expected compressed bytes:
    42,864,296

approved source:
    configured glibc-suite APT source embedded in the accepted receipt

approved HTTPS hosts:
    packages-cf.termux.dev
    packages.termux.dev
```

The collector does not run `apt`, refresh indexes, resolve newer versions, or follow an artifact redirect to an unapproved host.

Each planned artifact is bound by:

```text
package
installed version
architecture
repository Filename
expected byte size
expected SHA-256
priority tier
source recipe
candidate recipe-tree count
```

## Artifact cache and retry behavior

Raw verified `.deb` files are retained at:

```text
$HOME/Downloads/
    selected-obsidian-provider-authority-n3-exact-artifacts/
```

File names contain the package, version, architecture, and indexed SHA-256 prefix.

A rerun:

```text
reuses a file only when its complete size and SHA-256 match;
refuses an existing mismatched or unsafe path;
downloads only artifacts not already present and verified.
```

This allows a bounded retry after a transient network interruption without redownloading successful artifacts.

## Non-executing `.deb` inspection

For every verified artifact the collector checks:

```text
dpkg control Package
control Version
control Architecture
```

It obtains control and filesystem tar streams through `dpkg-deb`, but never invokes package installation or maintainer scripts.

Tar members are accepted only when they are:

```text
regular files
hardlinks
directories
symlinks
```

Absolute paths, parent traversal, unsupported special members, and unreadable hardlink content are hard failures.

Control members, including maintainer scripts, are hashed and inventoried only.

## Live filesystem comparison

For every data-tar member the collector derives its installed absolute path and uses `lstat` semantics.

```text
regular file or hardlink:
    SHA-256 comparison

symlink:
    exact link-text comparison

directory:
    type-presence comparison
```

It records rather than hides:

```text
missing live paths
content mismatches
symlink-target mismatches
type mismatches
read/hash errors
```

A divergence is evidence, not automatic transaction failure, provided the exact artifact identity and all no-mutation guards pass.

## ELF evidence

Every artifact ELF member is inspected with `readelf` for:

```text
ELF class
type
machine
SONAME
DT_NEEDED
RPATH
RUNPATH
Build ID
```

The corresponding live ELF metadata is recorded when present.

For `libwayland-glibc`, the `wayland-scanner` `DT_NEEDED` set is recorded as a discriminator for the two historical recipe trees that differ by `force-libm.patch`.

This discriminator may narrow source candidates. It does not independently prove the exact build commit.

## Outputs

A passing receipt contains:

```text
analysis.status
next-state.txt
claim-boundary.txt
summary.tsv
input-verification.tsv
input/
download-plan.tsv
downloaded-artifacts.tsv
artifact-control-fields.tsv
artifact-control-manifest.tsv
artifact-data-manifest.tsv
artifact-elf-metadata.tsv
package-artifact-comparison-summary.tsv
artifact-recipe-comparison-ledger.tsv
```

Raw `.deb` files remain in the separate Downloads artifact cache and are not copied into the receipt TGZ.

Expected next state:

```text
READY_FOR_BINARY_ARTIFACT_AND_RECIPE_AUTHORITY_REVIEW
```

## Implementation

```text
experiments/glibc/selected-obsidian-provider-authority/recipe/
    collect-n3-binary-artifact-comparison.py
    run-n3-binary-artifact-comparison.sh
```

Default receipt output:

```text
$PREFIX/tmp/selected-obsidian-provider-authority/
    selected-obsidian-provider-authority-n3-binary-artifact-comparison-<timestamp>
```

Default archive:

```text
$HOME/Downloads/
    selected-obsidian-provider-authority-n3-binary-artifact-comparison-results-<timestamp>.tgz
```

## Device execution

```bash
git pull --ff-only

bash \
  experiments/glibc/selected-obsidian-provider-authority/recipe/run-n3-binary-artifact-comparison.sh
```

Expected marker:

```text
N3_BINARY_ARTIFACT_COMPARISON=PASS
```

The wrapper prints the output root, accepted source receipt root, persistent artifact cache, receipt archive, and archive SHA-256.

## Development validation

The implementation passed:

```text
Python compile validation
shell syntax validation
synthetic .deb control identity validation
control maintainer-script inventory without execution
regular file content comparison
symlink text comparison
ELF metadata capture
28-artifact complete transaction using a preverified cache
source-receipt before/after content guard
dpkg before/after guard
zero authority decisions
```

Observed complete synthetic result:

```text
artifacts planned:
    28

artifacts verified/reused:
    28 / 28

packages with live divergence:
    0

package or maintainer-script operations:
    0

analysis.status:
    PASS
```

## Claim boundary

This stage may establish:

```text
that the exact indexed artifact bytes were acquired;
that artifact control identity matches package/version/architecture;
which package payload members are byte-identical to the live installation;
which paths differ or are missing;
which ELF metadata is present in exact artifact and live bytes;
which source-recipe ambiguity receives binary-semantic pressure.
```

It may not establish by itself:

```text
final semantic provider authority;
minimum runtime membership;
exact build worker or build commit provenance;
that every matching installed byte should be retained;
that every divergence is invalid;
successor composition, activation, or rollback closure.
```

## Stop line

Do not:

```text
run apt update or any package installation command;
download unplanned versions or packages;
execute package payloads or maintainer scripts;
modify the artifact cache after verification except by a new bounded transaction;
use artifact equality as automatic provider selection;
mutate the selected generation, loader state, current, or promoted launchers;
start successor materialization or activation.
```
