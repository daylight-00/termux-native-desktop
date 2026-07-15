# Runpath-free `libjpeg.so.62` compatibility-provider candidate result review

## Decision

```text
requirement: OJ-001
result archive SHA-256:
    5fe0e57a28e09c4765b7da68ace947f7a3b2af6ea26ae06c95a4ad6a102d19aa
candidate member: libjpeg.so.62.4.0
candidate SHA-256:
    a537840ef9da6135cb3284bc3b3e0d1fb4f624180a416c2a3964b94714eb7fe5
ELF: ELF64 little-endian AArch64 DYN
DT_SONAME: libjpeg.so.62
DT_RPATH: absent
DT_RUNPATH: absent
candidate decision: CANDIDATE_IDENTITY_ACCEPTED_PROVIDER_REVIEW_REQUIRED
provider authority: not accepted
composition: not reached
target population: blocked
materialization and activation: not performed
```

The corrected scratch build closes the object-production defect from the first candidate. It is the first exact runpath-free SONAME-62 object bound to the pinned source and recorded Termux glibc AArch64 toolchain. This review accepts its identity as a candidate and advances to a separate consumer-binding and functional-equivalence review.

Canonical machine-readable review:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    libjpeg-so-62-runpath-free-compatibility-provider-candidate-result-review.tsv
```

## Verified production facts

```text
source: libjpeg-turbo 3.1.0
source SHA-256:
    9564c72b1dfd1d6fe6274c5f95a8d989b59854575d4bbee44ade7bc17aa9bc93
WITH_JPEG7: OFF
WITH_JPEG8: OFF
ENABLE_SHARED: ON
ENABLE_STATIC: OFF
CMAKE_SKIP_RPATH: ON
CMake: 4.4.0
Ninja: 1.13.2
glibc GCC: 14.2.1 20250228
candidate size: 770664 bytes
Build ID: 11997794a0ec6e169ad9886a44d464d79a6255fd
symbol versions:
    LIBJPEG_6.2
    LIBJPEGTURBO_6.2
DT_NEEDED:
    libc.so.6
    ld-linux-aarch64.so.1
```

The result archive internal manifest, exact candidate digest, ELF header, dynamic section and symbol-version records were independently rechecked. The protected Termux glibc prefix, compatibility tree, provider store and deployment state were unchanged.

## Candidate identity decision

The following candidate identity is accepted for the next review state:

```text
source/build coordinates as recorded above
concrete member libjpeg.so.62.4.0
SHA-256 a537840ef9da6135cb3284bc3b3e0d1fb4f624180a416c2a3964b94714eb7fe5
DT_SONAME libjpeg.so.62
no DT_RPATH
no DT_RUNPATH
LIBJPEG_6.2 and LIBJPEGTURBO_6.2 definitions
```

This does not yet establish functional equivalence for the selected GTK consumer. ADR 0005 Class C assurance still requires a bounded consumer and behavior check for the project-produced artifact.

## Next bounded review

The bounded consumer is the retained Debian oracle member:

```text
package: libgdk-pixbuf-2.0-0:arm64 2.42.12+dfsg-4+deb13u1
member: libgdk_pixbuf-2.0.so.0.4200.12
member SHA-256:
    16d15168c69d4ad61862462da9fe811b5be3bef898b940a4023e15b039f5b43c
required dependency: libjpeg.so.62
capability: electron.gui.gtk3 image decoding
```

The next analyzer must remain scratch-only and:

```text
verify the exact consumer identity and DT_NEEDED binding;
prove every undefined JPEG symbol required by the consumer is exported by the candidate;
load the consumer with the candidate selected first in a bounded diagnostic path;
decode a fixed JPEG fixture and record dimensions/channels;
record the actually mapped candidate path;
record competing SONAME-62 objects without selecting them;
perform no installation, target population or activation.
```

## Conflict and exclusion boundary

The Termux `libjpeg.so.8` family remains an incompatible separate ABI and is excluded. The Debian rootfs `libjpeg.so.62.3.0` remains oracle/reference bytes and is not selected as target authority. The runpath-bearing first scratch candidate remains rejected. The corrected candidate may be selected only by its exact digest in the diagnostic and any later immutable generation.

## Update and rollback boundary

Re-review is mandatory if source/version/digest, build options, CMake/toolchain coordinates, member digest, SONAME, dynamic tags, symbol versions, bounded consumer identity, undefined-symbol set, conflict set or functional result changes.

Before materialization, rollback is revocation of this candidate row. Any later materialization must use a new immutable generation; rollback must reverse the generation selector rather than modify the candidate or aliases in place.

## Authority effect

This review accepts only the corrected candidate identity and closes the runpath-free production gap. It does not accept provider authority, complete GTK/image composition, target membership, installation, materialization, deployment or activation.
