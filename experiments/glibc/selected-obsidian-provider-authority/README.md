# Selected Obsidian Provider-Authority Census

## Status

```text
N0_REPOSITORY_ONBOARDING_PASS
N1_CENSUS_SCHEMA_AND_EVIDENCE_PLAN_PASS
N2_READ_ONLY_PROVIDER_EVIDENCE_PASS
N3_CORRECTED_NORMALIZED_CLASSIFICATION_PASS
N3_SOURCE_RECIPE_EVIDENCE_PASS
N3_BINARY_ARTIFACT_COMPARISON_PASS
PRIORITY_PROVIDER_AUTHORITY_REVIEW_ACTIVE
SUCCESSOR_MANIFEST_BLOCKED
SUCCESSOR_MATERIALIZATION_BLOCKED
CURRENT_ACTIVATION_BLOCKED
```

This workstream implements the provider-authority intervention required by `docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md`.

## Closed evidence transactions

### N2 — read-only provider evidence

```text
archive:
    selected-obsidian-provider-authority-n2-read-only-evidence-results-20260712-155013.tgz

SHA-256:
    e1eec5b68286cd6f888241afb50d9eabe00a8765269ecf20eb57bc0d7fe270d0
```

Accepted surface:

```text
27,279 current glibc-prefix paths
86 installed package identities
958 prefix ELF objects
161 selected/reference rows
20 supplemental pixbuf/icon/MIME rows
2 unowned loader-state paths
```

### Corrected N3 — normalized decision surface

```text
archive:
    selected-obsidian-provider-authority-n3-normalized-classification-results-20260712-165805.tgz

SHA-256:
    4dd86c4af956b447ed1829d6b5d604f43d10a17e5b3dcb3ddff3e9b48c377a9c
```

Accepted normalization:

```text
raw census rows:
    26,419

normalized rows:
    1,551

accepted authority decisions:
    0
```

### N3 source-recipe evidence

```text
archive:
    selected-obsidian-provider-authority-n3-source-recipe-evidence-results-20260712-185001.tgz

SHA-256:
    c8160016267f3ff83b348146240f74f808ffbc93374a6f75988231ef22408cdb
```

Accepted source comparison:

```text
priority packages:
    28

recipe mappings:
    28 / 28

unique installed-version recipe trees:
    27

multiple-tree lineage:
    libwayland-glibc 1.23.1
```

### N3 exact binary-artifact comparison

```text
archive:
    selected-obsidian-provider-authority-n3-binary-artifact-comparison-results-20260712-194542.tgz

SHA-256:
    da16d49acf54cbc8b6824e3974f08fea9ad0d6daf91687f4666d6c48d0b7567f
```

Accepted binary supply result:

```text
exact indexed .deb artifacts:
    28 / 28

verified bytes:
    42,864,296

artifact data members:
    6,887

regular content matches:
    6,016

symlink target matches:
    226

directory matches:
    645

ELF byte matches:
    462

missing paths or mismatches:
    0
```

For all 28 priority package identities, the live package-owned filesystem is byte-equivalent to the exact indexed repository artifacts. This is supply identity, not semantic provider authority.

## Repository layout

```text
schema/
    census-columns.tsv
    capability-groups.tsv

recipe/
    collect-read-only-provider-evidence.py
    run-n2-read-only-provider-evidence.sh

    collect-n3-normalized-provider-authority.py
    run-n3-normalized-provider-authority.sh

    collect-n3-source-recipe-evidence.py
    run-n3-source-recipe-evidence.sh

    collect-n3-binary-artifact-comparison.py
    collect-n3-binary-artifact-comparison.parts/
    run-n3-binary-artifact-comparison.sh

work/                       # ignored by Git
    source/
    artifacts/
    receipts/unpacked/
    tmp/
```

## Storage boundary

```text
work/ and other Termux-private stage paths:
    source repositories
    raw artifact caches
    unpacked receipts
    temporary transaction state

$HOME/Downloads:
    final handoff TGZ files and explicitly requested exports only
```

Downloads is the Termux/Android-user handoff boundary, not the project workspace.

## Current authority review inputs

The current review combines:

```text
normalized semantic class and minimum-scope pressure
selected/reference consumers and dependency edges
historical source recipes, patches, and auxiliary files
exact repository artifact identity
complete artifact-to-live byte equivalence
application-local and native/provider alternatives
runtime versus research profile
update and revalidation ownership
```

Priority package groups:

```text
world/platform:
    glibc
    termux-exec-glibc
    glibc-runner

X11/XCB platform pressure:
    libx11-glibc
    libxau-glibc
    libxcb-glibc
    libxdmcp-glibc
    libxext-glibc
    libxrandr-glibc
    libxrender-glibc
    libxshmfence-glibc

generic shared capability pressure:
    brotli-glibc
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

maintenance/toolchain pressure:
    e2fsprogs-glibc
    gcc-libs-glibc
```

## `libwayland-glibc` lineage note

Two recipe trees exist for version 1.23.1:

```text
d0c7dcd812e720f00a781c0410af150fbfffdae0
    includes force-libm.patch
    commit date 2024-11-13

fb5924ca0b3f42a87d0d865e11a8aa9f6163e5a2
    omits force-libm.patch
    commit date 2025-03-10
```

The exact accepted artifact has uniform member timestamp `2024-11-13T11:32:03Z`, strongly favoring the older tree. Its `wayland-scanner` does not have a direct `libm` NEEDED entry, but linker `--as-needed` behavior means that fact alone does not close lineage.

## Semantic classes

```text
WORLD_CORE_SUBSTRATE
PLATFORM_INTEGRATION_PROVIDER
GENERIC_SHARED_CAPABILITY_PROVIDER
APPLICATION_LOCAL
APPLICATION_DOMAIN_SUPPLEMENT
DATA_CAPABILITY_PROVIDER
TOOLCHAIN_ONLY
ORACLE_ONLY
MUTABLE_OR_CACHE
UNRESOLVED
```

## Claim discipline

```text
path identity != content identity
package ownership != semantic authority
exact artifact identity != runtime necessity
working runtime != final provider choice
loader selection != final authority
package boundary != capability boundary
application-local $ORIGIN topology is first-class evidence
runtime and research profiles remain separate
```

## Next valid state

```text
REVIEW_PRIORITY_PROVIDER_AUTHORITY_FROM_NORMALIZED_SEMANTICS_SOURCE_RECIPES_AND_EXACT_BINARY_ARTIFACTS
```

This is repository-side analysis. A new device transaction is required only when a specific authority decision still lacks discriminating evidence.

## Stop line

Do not:

```text
install, remove, upgrade, or downgrade packages
run package maintainer scripts
mutate loader caches
mutate the selected generation
create or change current
change promoted launchers
patch RPATH
promote every exact package artifact into the minimum runtime
reopen closed graphics gates
materialize or activate a successor before provider-authority review closes
```
