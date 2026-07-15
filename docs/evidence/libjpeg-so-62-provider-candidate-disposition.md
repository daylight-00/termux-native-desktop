# `libjpeg.so.62` provider-candidate disposition

## Decision

```text
requirement: OJ-001
required lookup identity: libjpeg.so.62
existing Termux glibc candidate: libjpeg.so.8 family rejected
exact repository SONAME-62 candidate: not found
first scratch candidate: produced and rejected for colon-only DT_RUNPATH
canonical disposition: COMPATIBILITY_PROVIDER_CANDIDATE_REBUILD_REQUIRED_NO_RUNPATH
provider authority: not accepted
composition: not reached
target population: blocked
materialization and activation: not performed
```

The stable `libjpeg.so.62` requirement remains authoritative. The selected `libjpeg-turbo-glibc 3.1.0` artifact cannot satisfy it because the supplier recipe explicitly enables the backward-incompatible libjpeg v8 ABI and produces the `libjpeg.so.8` family.

Canonical machine-readable record:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    libjpeg-so-62-provider-candidate-disposition.tsv
```

## Rejected repository candidate

```text
package:       libjpeg-turbo-glibc 3.1.0
artifact id:   generic-artifact:e672a721d7a949048cab
artifact SHA:  e672a721d7a949048cab5c7073ef0a0c05f627b8fc691ecc2d0adea6a5a5689e
recipe root:   gpkg/libjpeg-turbo
recipe tree:   cb58a7c1d7f4a1f89d036e4c80da596c0c61234c
configuration: -DWITH_JPEG8=ON
observed family:
    libjpeg.so
    libjpeg.so.8
    libjpeg.so.8.3.2
```

This is an exact artifact candidate for the v8 ABI family only. A package-name match, source-family match, unversioned development name, or symlink cannot convert its ABI into `libjpeg.so.62`.

## Repository candidate search result

The canonical evidence, the pinned and current Termux-glibc recipe, and the current standard Termux recipe expose the same material fact: the packaged runtime enables `WITH_JPEG8` and no separate SONAME-62 package definition or bound artifact is present.

Therefore OJ-001 is not resolved by provider discovery. It is resolved by selecting an explicit compatibility-provider production path.

## Pinned compatibility-provider specification

Use the already pinned upstream source:

```text
source: libjpeg-turbo 3.1.0
source SHA-256:
9564c72b1dfd1d6fe6274c5f95a8d989b59854575d4bbee44ade7bc17aa9bc93
```

The smallest valid build delta is:

```text
WITH_JPEG7=OFF
WITH_JPEG8=OFF
shared library enabled
no installation
no alias creation
no target population
no activation
```

Upstream 3.1.0 then selects:

```text
JPEG_LIB_VERSION = 62
SO_MAJOR_VERSION = 62
SO_AGE = 4
SO_MINOR_VERSION = 0
expected concrete member = libjpeg.so.62.4.0
expected DT_SONAME = libjpeg.so.62
```

The older oracle name `libjpeg.so.62.3.0` is not the required concrete filename. It is retained only as reference provenance. Candidate acceptance depends on the stable SONAME, exact new member digest, source and build coordinates, and bounded consumer/conflict review.

## Why this is not an alias bridge

Creating `libjpeg.so.62 -> libjpeg.so.8.3.2` would misrepresent two backward-incompatible ABI families and is prohibited. The required object is a real v6b-compatible shared library produced from upstream's native v6b ABI mode.

## First scratch candidate result

The first bounded Termux build completed successfully and returned:

```text
member: libjpeg.so.62.4.0
SHA-256:
    1d32a4b12ef3a6032626af13b69a64c45a0a0a9bb4090e0b61d9312811208d88
ELF: ELF64 little-endian AArch64 DYN
DT_SONAME: libjpeg.so.62
symbol versions: LIBJPEG_6.2; LIBJPEGTURBO_6.2
protected live state: unchanged
```

That object is rejected for provider review because it contains a 175-character colon-only `DT_RUNPATH`. The canonical result review is [`libjpeg-so-62-compatibility-provider-candidate-result-review.md`](libjpeg-so-62-compatibility-provider-candidate-result-review.md).

## Next bounded action

The next transaction prepares one corrected user-Termux source-build and ELF analyzer wrapper. It must:

```text
acquire the exact pinned source and verify SHA-256
build in scratch with the explicit v6b ABI options
set CMAKE_SKIP_RPATH=ON
perform no package installation or target mutation
record the complete configure/build command and relevant toolchain coordinates
verify the concrete member, SHA-256, ELF class/machine and DT_SONAME
reject any DT_RPATH or DT_RUNPATH
archive the candidate bytes and structured evidence in one .tar.zst
```

The corrected returned object remains a candidate until a later provider-authority review accepts its consumer binding, conflict/exclusion set, update boundary and rollback boundary.

## Update and rollback boundary

Reissue the candidate specification when any of these changes:

```text
source version or source digest
WITH_JPEG7/WITH_JPEG8 or shared-library options
build framework or toolchain coordinates
output concrete member, digest or DT_SONAME
consumer requirement or selected capability
competing provider candidates or collision set
```

Before materialization, rollback is revocation of the candidate specification or candidate row. Any later materialization must use an immutable generation and reverse the selector to a prior complete generation rather than rewrite aliases in place.

## Authority effect

This decision accepts only:

```text
libjpeg.so.62 remains the required lookup identity
libjpeg.so.8 remains an invalid substitute
no exact repository candidate is available
the first pinned-source build is rejected for runpath and a runpath-free rebuild is required
```

It does not accept provider authority, complete image/GTK composition, a target path, alias policy, installation, materialization, deployment or activation.
