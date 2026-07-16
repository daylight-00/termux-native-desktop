# `libjpeg.so.62` provider-candidate disposition

## Decision

```text
requirement: OJ-001
required lookup identity: libjpeg.so.62
existing Termux glibc candidate: libjpeg.so.8 family rejected
exact repository SONAME-62 candidate: not found
first scratch candidate: rejected for colon-only DT_RUNPATH
corrected scratch candidate: runpath-free identity accepted
corrected candidate SHA-256:
    a537840ef9da6135cb3284bc3b3e0d1fb4f624180a416c2a3964b94714eb7fe5
canonical disposition: RUNPATH_FREE_COMPATIBILITY_PROVIDER_ACCEPTED_BOUNDED_GDKPIXBUF_JPEG_SCOPE
provider authority: accepted for exact GdkPixbuf 2.42.12 JPEG file and memory decode
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

## Corrected scratch candidate result

The second bounded build returned:

```text
member: libjpeg.so.62.4.0
SHA-256:
    a537840ef9da6135cb3284bc3b3e0d1fb4f624180a416c2a3964b94714eb7fe5
ELF: ELF64 little-endian AArch64 DYN
DT_SONAME: libjpeg.so.62
DT_RPATH: absent
DT_RUNPATH: absent
symbol versions: LIBJPEG_6.2; LIBJPEGTURBO_6.2
protected live state: unchanged
```

Its canonical review is [`libjpeg-so-62-runpath-free-compatibility-provider-candidate-result-review.md`](libjpeg-so-62-runpath-free-compatibility-provider-candidate-result-review.md). The object identity is accepted as a candidate; provider authority remains open.

## Next bounded action

Perform one read-only consumer-binding and functional-equivalence diagnostic using the exact retained `libgdk_pixbuf-2.0.so.0.4200.12` oracle consumer. The diagnostic must verify its `DT_NEEDED` binding and undefined JPEG symbol set, load the corrected candidate from scratch, decode a fixed JPEG fixture, record the mapped candidate path and competing SONAME-62 objects, and perform no installation or target mutation.

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
the first pinned-source build is rejected for runpath; the corrected runpath-free candidate identity is accepted for bounded provider review
```

It does not accept provider authority, complete image/GTK composition, a target path, alias policy, installation, materialization, deployment or activation.

## First bounded consumer result

The exact consumer identity, `DT_NEEDED=libjpeg.so.62`, and all 22 required JPEG symbols were verified. The fixed JPEG call then exited with `SIGSEGV` before decode or mapped-path output. This does not revoke candidate identity and does not accept provider authority. The next action is the bounded runtime/API diagnostic matrix recorded in [`libjpeg-so-62-gdkpixbuf-consumer-binding-result-review.md`](libjpeg-so-62-gdkpixbuf-consumer-binding-result-review.md).

## Loader-isolated provider decision

The corrected direct-loader matrix closed the remaining bounded functional gap:

```text
result archive SHA-256:
4e546ac1ef2a92f3301dd51ca2328d6901a05e309da78b6d08b26211d9b621e3

direct candidate/oracle output SHA-256:
8cef10ed9b5f2e4ffde1fdedc4b722d4738d86ac5d204554328c30ef34ecbdc6

GdkPixbuf candidate file:   PASS
GdkPixbuf candidate memory: PASS
GdkPixbuf oracle file:      PASS
GdkPixbuf oracle memory:    PASS
```

The exact project-produced candidate is therefore accepted as a bounded provider for the selected GdkPixbuf 2.42.12 JPEG file and memory decode capability. See [`libjpeg-so-62-loader-isolated-provider-authority.md`](libjpeg-so-62-loader-isolated-provider-authority.md). This does not decide complete composition, target membership, materialization or activation.
