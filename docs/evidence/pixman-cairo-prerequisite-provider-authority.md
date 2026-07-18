# Pixman bounded Cairo prerequisite provider authority

## Decision

The exact Termux glibc member `libpixman-1.so.0.46.4` is accepted only as the pixel image compositing prerequisite directly required by exact Cairo `libcairo.so.2.11802.2`.

```text
authority root:      outside-28-root:gpkg/libpixman
recipe root:         gpkg/libpixman
recipe tree:         ba911214b3339066f757cc85e5c4d339b55a7be4
build script blob:   92b295aca84e3f68167a101ced4eceaf019b16ce
artifact:            libpixman-glibc 0.46.4
artifact SHA-256:    5becc25134aef71b8b4ed629272bd13b0be7271f01b60a48670ea938f2e83b17
artifact size:       152856
selected row:        selected:84b77925eeb02b53f18e
selected label:      libpixman-1.so.0.44.0
member:              libpixman-1.so.0.46.4
member SHA-256:      cab54c7f8e4c3a5c1980aa7564b9321114418f2d3c6fa37a3c0723f9f22e1eb2
SONAME:              libpixman-1.so.0
result archive SHA:  3df4f72452b6fb36525ea651f58a0d9d0e551d6ab1f0076653588e767fb1ad9a
```

This provider is outside the canonical 28-root claim inventory. It increases the bounded provider count without changing the 28-root, 37-object, 89-claim ADR 0005 inventory.

## Exact acquisition and consumer binding

The read-only Termux evidence run downloaded the pinned Cairo and Pixman packages from the approved repository, verified the package digests, extracted them without installation, and retained both packages and exact ELF evidence in the result archive.

Exact `libcairo.so.2.11802.2` records `DT_NEEDED=libpixman-1.so.0`. Exact Pixman records SONAME `libpixman-1.so.0`, and the package alias points to `libpixman-1.so.0.46.4`. This closes the Cairo-to-Pixman consumer edge without relying on package dependency metadata alone.

## Class B recipe boundary

The pinned one-file recipe delegates configuration to the standard Termux Meson helper. Its package-specific options disable Loongson MMI, VMX, ARM SIMD, NEON, AArch64 NEON, RISC-V vector, MMX, SSE2, SSSE3, MIPS DSPR2, and the GTK helper surface.

This selects the exact generic Pixman implementation distributed in the pinned artifact. It can change acceleration and performance characteristics, but the retained exact member, stable SONAME, alias, and Cairo binding are accepted. No byte-equivalence or performance-equivalence claim is made against an upstream default or another distribution build.

## Runtime dependency boundary

The exact Pixman ELF needs only:

```text
libm.so.6
libc.so.6
ld-linux-aarch64.so.1
```

`libpng-glibc` is declared as a build dependency but is not a Pixman runtime `DT_NEEDED` edge. No additional selected provider member is introduced by this decision.

## Concrete filename continuity

The retained package contains:

```text
libpixman-1.so.0 -> libpixman-1.so.0.46.4
```

The selected `libpixman-1.so.0.44.0` label is older reference evidence, not target-path authority. Future composition may use only the stable SONAME alias and exact accepted member; it must not synthesize the older concrete filename or promote the unversioned development alias.

## Conflict and exclusions

No accepted member or SONAME alias collision exists. Debian reference bytes, architecture-specific acceleration claims, GTK helper or test surfaces, static libraries, headers, pkg-config data, unversioned development aliases, package-wide authority, Cairo provider authority, complete rendering composition, target population, materialization, deployment, and activation remain outside this decision.

## Update and rollback

Re-review the recipe blob and tree, source version and digest, package metadata and digest, exact member digest, SONAME and alias, CPU-feature options, Cairo `DT_NEEDED`, and Pixman runtime dependencies on change.

Before materialization, rollback is revocation of the Pixman composition row and any dependent Cairo decision. After a future materialization, reverse the selector to the prior immutable generation with its matching Cairo/Pixman pair; do not rewrite the active alias in place.

## Composition effect

```text
accepted bounded provider roots overall: 26
accepted roots inside 28-root inventory: 20
open roots inside inventory:              8
accepted exact members:                  33
included members:                        32
deferred members:                         1
unresolved selected identities:          10
composition: REVIEWED_BLOCKED_INCOMPLETE
target manifest allowed: NO
activation: BLOCKED
```
