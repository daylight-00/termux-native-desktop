# 0131 — Selected Obsidian Provider-Authority Binary Artifact Receipt PASS

## Status

```text
corrected N3 normalized classification:
    PASS / ACCEPTED

source recipe evidence:
    PASS / ACCEPTED

bounded binary artifact comparison:
    PASS / ACCEPTED

binary supply identity for 28 priority packages:
    ESTABLISHED

semantic provider authority:
    NOT YET ACCEPTED

successor manifest/materialization/current activation:
    BLOCKED
```

## Accepted receipt

```text
archive:
    selected-obsidian-provider-authority-n3-binary-artifact-comparison-results-20260712-194542.tgz

SHA-256:
    da16d49acf54cbc8b6824e3974f08fea9ad0d6daf91687f4666d6c48d0b7567f

captured branch:
    docs/post-graphics-architecture-audit

captured HEAD:
    b7c894d59120082c3ab43f33438715486065ede9

analysis.status:
    PASS

next-state:
    READY_FOR_BINARY_ARTIFACT_AND_RECIPE_AUTHORITY_REVIEW
```

The archive was independently inspected before extraction.

```text
members:
    31

single root:
    PASS

absolute paths:
    0

parent traversal:
    0

links and special members:
    0
```

## Input continuity

All 16 embedded source-recipe receipt inputs are byte-identical to the accepted source receipt.

```text
input verification rows:
    16 / 16 PASS

source receipt manifest before/after:
    b8a4987e19a60ab96a991f8f23d91f09dbda8cade6a791400aa4481ac3666e4f
    unchanged

source repository HEAD:
    fd2ae25e04f3ea26d6c7b4678020814889331d86
```

The accepted dpkg state also remained unchanged.

```text
dpkg status SHA-256 before/after:
    aba4d9e78f68bd0fe5d841b5d1422255ecca162621c85630137651122bcc8ee2

dpkg info metadata manifest before/after:
    f1a32ecdf5cbe1999fbf4b2aeae28196e8a1ca215b17a4e2f4153578dce414e4
```

## Artifact acquisition

The transaction was bounded to the 28 priority packages established by the accepted source receipt.

```text
artifacts planned:
    28

artifacts verified:
    28

artifacts newly downloaded:
    28

artifacts reused:
    0

verified bytes:
    42,864,296

repository host:
    packages-cf.termux.dev

transport:
    HTTPS with Termux CA bundle
```

Every artifact satisfied all of:

```text
indexed repository filename match;
indexed size match;
indexed SHA-256 match;
internal Package field match;
internal Version field match;
internal Architecture field match.
```

There are 28 unique package identities, 28 unique artifact paths, and 28 unique artifact SHA-256 identities.

## Installed-artifact equivalence

The downloaded `.deb` data archives contain:

```text
data members:
    6,887

regular files:
    6,016

symlinks:
    226

directories:
    645

ELF files:
    462
```

Every member matched the current installed filesystem.

```text
regular content matches:
    6,016

symlink target matches:
    226

directory matches:
    645

missing live paths:
    0

content mismatches:
    0

symlink target mismatches:
    0

type mismatches:
    0

packages whose complete archive matches live:
    28 / 28
```

All 462 artifact ELF objects and their live counterparts passed `readelf` inspection and are byte-identical. Therefore their Build ID, SONAME, NEEDED, RPATH, and RUNPATH observations also coincide.

This closes a previously missing supply claim:

```text
for these 28 package identities,
current installed package-owned bytes
    == exact indexed repository artifact bytes
```

This does not by itself decide whether each package is semantically appropriate for the final minimum runtime.

## Control archive boundary

The 28 control archives contain 32 regular control members. They were hashed and inspected without execution.

Observed non-`control` metadata files are limited to four `conffiles` members:

```text
glibc-runner
glibc
e2fsprogs-glibc
krb5-glibc
```

No maintainer script was executed.

## `libwayland-glibc` recipe pressure

The exact artifact and live `wayland-scanner` are byte-identical and have:

```text
Build ID:
    f1e7b9ad0afba535e8e06b64577c467e905fe147

NEEDED:
    libexpat.so.1
    libxml2.so.2
    libc.so.6
    ld-linux-aarch64.so.1

libm direct NEEDED:
    absent
```

Two source recipe trees remain in the source receipt:

```text
older tree:
    d0c7dcd812e720f00a781c0410af150fbfffdae0
    commit 6117f3901366567b04fd69dcc718770fbc952695
    2024-11-13T14:07:19+03:00
    includes force-libm.patch

newer tree:
    fb5924ca0b3f42a87d0d865e11a8aa9f6163e5a2
    commit 16a5e6853837f8c67248bc72c6893aba8d2acb99
    2025-03-10T10:15:48+03:00
    omits force-libm.patch
```

Every member of the accepted `libwayland-glibc` artifact has mtime:

```text
2024-11-13T11:32:03Z
```

That timestamp is shortly after the older recipe commit and months before the newer recipe tree existed. It strongly pressures the installed artifact toward the older tree.

However, absence of a direct `libm` NEEDED entry is not sufficient by itself to prove that `force-libm.patch` was absent, because linker `--as-needed` behavior can omit an unused direct dependency. Until build-run or repository publication metadata binds the artifact SHA to a source commit/tree, the formal lineage remains:

```text
strong older-tree pressure;
not cryptographically closed.
```

## Mutation guard

The transaction performed:

```text
apt update:
    NO

package install/upgrade/remove:
    NO

maintainer-script execution:
    NO

runtime launch:
    NO

generation operation:
    NO

current operation:
    NO

authority decisions accepted:
    0
```

The only network operation was bounded download of the exact 28 pre-identified artifacts.

## Accepted claims

This receipt establishes:

```text
the exact repository artifacts corresponding to all 28 priority installed packages;
the complete control and data member inventories of those artifacts;
byte-for-byte equivalence between every artifact data member and the live installed path;
exact ELF identity for all 462 ELF members;
no drift in the accepted dpkg or source-evidence inputs.
```

It does not establish:

```text
that all 28 packages belong in the minimum workstation runtime;
that package ownership equals semantic provider authority;
that every historical recipe patch was required for the accepted artifact;
that glibc-runner, package utilities, headers, documentation, or toolchain objects are runtime authority;
that a successor composition may now be materialized or activated.
```

## Next valid state

```text
REVIEW_PRIORITY_PROVIDER_AUTHORITY_FROM_NORMALIZED_SEMANTICS_SOURCE_RECIPES_AND_EXACT_BINARY_ARTIFACTS
```

This review is repository-side analysis. It does not require another device transaction unless a specific unresolved provider decision demands new discriminating evidence.
