# 0121 — Selected Obsidian Provider-Authority N3 Normalization Implementation

## Status

```text
N2 read-only provider evidence:
    CLOSED / PASS

N3 normalization implementation:
    READY_FOR_DEVICE_EXECUTION

N3 device receipt:
    PENDING

provider-source comparison:
    NOT STARTED

provider-authority intervention:
    ACTIVE

successor manifest/materialization/current activation:
    BLOCKED
```

This stage creates a bounded decision surface from the accepted exhaustive N2 evidence. It does not select final providers.

## Authority

Read under:

```text
docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md
docs/refactor/0117-provider-authority-intervention-adoption-and-execution-order.md
docs/refactor/0118-selected-obsidian-provider-authority-census-schema-and-evidence-plan.md
docs/refactor/0120-selected-obsidian-provider-authority-n2-device-receipt-review.md
```

The N2 raw inventory remains immutable evidence.

## Implementation

```text
experiments/glibc/selected-obsidian-provider-authority/recipe/
    normalize-n3-provider-authority.py
    run-n3-normalized-provider-authority.sh
```

The runner consumes only the accepted N2 output root. It performs no live package, workload, generation, or `current` operation.

## Capability registry extension

N2 exposed a Termux-specific glibc adaptation object:

```text
$PREFIX/glibc/lib/libsyscall_without_fsc.so
```

It must not be hidden inside generic `world.glibc.core` accounting.

The capability registry therefore adds:

```text
platform.glibc-adaptation.termux
    Termux/Android glibc adaptation objects and world-entry shims
```

This is a provisional integration responsibility. Source recipe, patch rationale, consumers, ABI coupling, and final ownership remain open.

## Normalized decision surface

The accepted N2 census contains:

```text
raw census rows:
    26,419

raw prefix paths:
    27,279
```

The normalizer emits these decision units:

```text
capability rows:
    26

selected/reference rows:
    161

pixbuf/icon/MIME supplemental rows:
    20

additional prefix ELF rows:
    911

package aggregate rows:
    86

unowned loader-state rows:
    2

non-ELF package-surface aggregates:
    354

normalized census rows:
    1,560
```

The raw path table remains available through the embedded N2 receipt. No raw evidence is deleted or rewritten.

## Non-ELF aggregation classes

Remaining package files are grouped by package ownership and one semantic path class:

```text
HEADER
STATIC_OR_STARTFILE
BUILD_METADATA
EXECUTABLE_TOOL
CONFIGURATION
LOCALE_DATA
DOCUMENTATION
SHARED_DATA
SCRIPT_OR_LANGUAGE_MODULE
SYMLINK_ALIAS
OTHER_NON_ELF
```

Each aggregate records counts, bytes, selected/reference pressure, direct-consumer edges, and sample paths.

## Package-level pressure

The stage emits:

```text
package-authority-pressure.tsv
```

Package rows record only provisional pressure:

```text
capability group
semantic class pressure
minimum scope pressure
runtime/research profile pressure
update-owner pressure
Termux/Android adaptation pressure
classification rationale
```

Package presence is never promoted directly into final authority.

The `glibc` package aggregate remains `UNRESOLVED` because it mixes:

```text
loader/libc and tightly coupled modules
runtime tools
start files and development inputs
configuration and locale data
diagnostics
```

## Object-level glibc split

The normalizer distinguishes current glibc-package ELF pressure:

```text
loader/libc/tightly coupled library or module:
    WORLD_CORE_SUBSTRATE pressure

bin/sbin/libexec runtime utility:
    UNRESOLVED / research-maintenance pressure

crt/start file and diagnostic object:
    TOOLCHAIN_ONLY pressure

libsyscall_without_fsc.so:
    PLATFORM_INTEGRATION_PROVIDER pressure
```

This is the minimum correction required to avoid equating one package boundary with one semantic authority.

## Selected/reference classification pressure

The normalizer may assign provisional classes where the accepted evidence is already strong:

```text
valid AppDir/$ORIGIN topology:
    APPLICATION_LOCAL

application-domain selected closure:
    APPLICATION_DOMAIN_SUPPLEMENT or typed shared capability pressure

world protected identities:
    WORLD_CORE_SUBSTRATE

platform integration membership:
    PLATFORM_INTEGRATION_PROVIDER

shared runtime capabilities:
    GENERIC_SHARED_CAPABILITY_PROVIDER

data capabilities:
    DATA_CAPABILITY_PROVIDER

compiler/build surface:
    TOOLCHAIN_ONLY

oracle scenario capability:
    ORACLE_ONLY

mutable state and caches:
    MUTABLE_OR_CACHE
```

Every such row remains `PROVISIONAL`, `OPEN`, or `BLOCKED`; none becomes accepted final authority.

## Source-candidate discipline

The stage may record only evidence already present in N2:

```text
current prefix path:
    installed Termux-glibc package artifact identified

retained rootfs path:
    Debian package/version candidate identified;
    exact artifact not locked

AppDir path:
    current upstream/app-local byte identity proven
```

It does not claim source superiority.

## Outputs

```text
analysis.status
next-state.txt
claim-boundary.txt
summary.tsv
input-verification.tsv
package-authority-pressure.tsv
normalized-provider-authority-census.tsv
non-elf-surface-aggregates.tsv
unresolved-evidence-ledger.tsv
input/
```

Expected next state:

```text
READY_FOR_N3_SOURCE_RECIPE_AND_ARTIFACT_COMPARISON
```

## Read-only boundary

The stage performs:

```text
N2 receipt hashing and embedding
pure TSV normalization
provisional classification pressure
safe archive generation
```

It does not perform:

```text
APT/dpkg operation
package script execution
filesystem scan of live $PREFIX/glibc
workload launch
generation inspection or mutation
live current inspection or change
provider cleanup
successor composition
```

## Archive policy

```text
unpacked output root:
    $PREFIX/tmp/selected-obsidian-provider-authority/
        selected-obsidian-provider-authority-n3-normalized-classification-<timestamp>

TGZ archive:
    $HOME/Downloads/
        selected-obsidian-provider-authority-n3-normalized-classification-results-<timestamp>.tgz
```

## Device execution

```bash
git pull --ff-only

bash \
  experiments/glibc/selected-obsidian-provider-authority/recipe/run-n3-normalized-provider-authority.sh
```

Expected terminal marker:

```text
N3_PROVIDER_AUTHORITY_NORMALIZATION=PASS
```

The runner prints `OUT`, `ARCHIVE`, and `ARCHIVE_SHA256`.

## Development validation

The implementation passed against the accepted N2 receipt fixture:

```text
Python syntax:
    PASS

clean-git guard:
    PASS

required N2 input identity embedding:
    PASS

required census-field completeness:
    PASS

unique normalized row IDs:
    PASS

raw-to-normalized reduction:
    26,419 -> 1,560

safe TGZ under Downloads:
    PASS
```

Development validation is not the device receipt.

## Direction decision

```text
N3 normalization implementation:
    READY

next external evidence:
    DEVICE N3 NORMALIZATION RECEIPT

next analytical work after receipt PASS:
    TERMUX PACKAGE RECIPE / PATCH / SOURCE ARTIFACT COMPARISON
```

## Stop line

Do not:

```text
accept provisional classes as final provider authority
remove packages based on package-pressure output
promote every glibc-package library/module as world core without review
include maintenance utilities in runtime by installed presence
run the pixbuf discriminator as part of normalization
mutate ld.so.conf or ld.so.cache
mutate the existing generation
create current
finalize or materialize a successor
reopen closed graphics work
```
