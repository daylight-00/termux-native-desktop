# `libjpeg.so.62` compatibility-provider candidate result review

## Decision

```text
requirement: OJ-001
result archive SHA-256:
    e9ab2755c8d70d2c21e33b87f4ea438702e0dbaf8a8718480ea78792394369c8
candidate member: libjpeg.so.62.4.0
candidate SHA-256:
    1d32a4b12ef3a6032626af13b69a64c45a0a0a9bb4090e0b61d9312811208d88
ELF: ELF64 little-endian AArch64 DYN
DT_SONAME: libjpeg.so.62
build result: successful scratch production
candidate decision: REJECTED_REBUILD_REQUIRED_NO_RUNPATH
provider authority: not accepted
composition: not reached
target population: blocked
materialization and activation: not performed
```

The first real SONAME-62 object proves that the pinned libjpeg-turbo 3.1.0 source and the recorded glibc AArch64 toolchain can produce the expected v6b member. It is not an acceptable provider candidate because the returned build-tree ELF contains an undeclared `DT_RUNPATH` consisting of 175 colon characters.

Canonical machine-readable review:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    libjpeg-so-62-compatibility-provider-candidate-result-review.tsv
```

## Verified production facts

The result archive and its internal manifest were verified independently.

```text
source version: 3.1.0
source SHA-256:
    9564c72b1dfd1d6fe6274c5f95a8d989b59854575d4bbee44ade7bc17aa9bc93
WITH_JPEG7: OFF
WITH_JPEG8: OFF
ENABLE_SHARED: ON
ENABLE_STATIC: OFF
CMake: 4.4.0
Ninja: 1.13.2
glibc GCC: 14.2.1 20250228
candidate size: 770688 bytes
symbol versions:
    LIBJPEG_6.2
    LIBJPEGTURBO_6.2
```

The required dynamic symbols are exported under `LIBJPEG_6.2`, including `jpeg_CreateCompress`, `jpeg_CreateDecompress`, `jpeg_read_header`, `jpeg_start_decompress`, `jpeg_finish_decompress`, `jpeg_start_compress`, `jpeg_write_scanlines`, `jpeg_finish_compress`, and `jpeg_std_error`.

The runner compared protected live-state coordinates before and after the build. The Termux glibc prefix, legacy compatibility tree, provider store and deployment state were unchanged. CMake was installed separately by the user before the runner began; package-manager provisioning was not performed by the runner and is not part of the candidate artifact claim.

## Blocking defect

The ELF dynamic section contains:

```text
DT_NEEDED: libc.so.6
DT_NEEDED: ld-linux-aarch64.so.1
DT_SONAME: libjpeg.so.62
DT_RUNPATH: 175 colon characters
```

The runpath was not an intended runtime contract. It originated from a scratch build configured with `CMAKE_SKIP_RPATH=NO` and a non-live `CMAKE_INSTALL_PREFIX`. An undeclared build-tree runpath is outside the accepted provider specification even when all path components appear empty.

This review therefore does not normalize, strip in place, or accept the first object. Candidate identity includes its exact bytes and dynamic tags; changing the ELF after production would create a different candidate requiring a new digest and review.

## Required rebuild delta

The smallest correction is:

```text
same source version and SHA-256
same glibc AArch64 toolchain boundary
same WITH_JPEG7=OFF
same WITH_JPEG8=OFF
same shared-only jpeg target
add CMAKE_SKIP_RPATH=ON
require no DT_RPATH
require no DT_RUNPATH
no installation
no post-link ELF mutation
```

The corrected result must return a new exact member digest, complete dynamic-section evidence, versioned-symbol evidence and the unchanged protected-state comparison.

## Stop and acceptance boundary

The corrected candidate remains rejected if it has any `DT_RPATH` or `DT_RUNPATH`, the source or toolchain boundary drifts without review, the output identity differs from `libjpeg.so.62.4.0` / `libjpeg.so.62`, or live state changes.

A runpath-free rebuilt object will still be only a candidate. Provider authority requires a later review of consumer binding, conflict and exclusion closure, update boundary and rollback boundary.

## Authority effect

This review accepts only:

```text
the first source build completed successfully;
the returned bytes have the recorded source/build/ELF identity;
the first object is rejected because of its dynamic runpath;
a clean rebuild with RPATH generation disabled is required.
```

It does not accept provider authority, complete image/GTK composition, target membership, installation, alias policy, materialization, deployment or activation.
