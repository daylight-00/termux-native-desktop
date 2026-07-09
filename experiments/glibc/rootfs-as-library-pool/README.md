# Rootfs as a passive library pool

**Status:** passed; foundation of the current glibc layer  
**Date:** 2026-07-04  
**Provenance:** first-hand summary

## Question

Can a PRoot-distribution Debian rootfs serve as a passive library warehouse for natively executed glibc binaries—providing Debian's broad library catalog without making PRoot the runtime?

## Baseline

- Termux glibc-repo provides a working Android-adapted glibc core but a limited package catalog.
- Debian provides the required desktop/application libraries, but the PRoot runtime path had already been rejected for the normal workstation workflow.

## Hypothesis

If the project needs the library files and package metadata rather than the PRoot execution environment, the rootfs can be demoted to a passive source. A filtered symlink farm can expose general shared libraries while excluding the libc family and other incompatible core runtime pieces.

## Procedure

1. Build `~/gl/lib` as symlinks into selected rootfs library directories.
2. Exclude the libc family and related core runtime libraries with a denylist; never mix two glibc implementations.
3. Register the glibc core first and the farm second in the glibc loader configuration.
4. Couple farm regeneration with `ldconfig` refresh and contamination checks through `modules/gl/overlay/home/gl/bin/gl-farm`.

## Evidence

- VS Code's large shared-library graph resolved through the core + farm model.
- Deliberate/accidental farm contamination with a libc linker script produced the characteristic `invalid ELF header` failure, confirming that the denylist is load-bearing.
- Direct application RPATH alone did not solve transitive dependency resolution; loader-cache registration was required.

## Result

Passed. The architecture became:

```text
Termux glibc core
  -> filtered Debian-rootfs library farm
  -> application-local libraries preserved through $ORIGIN where needed
```

The exact lookup behavior is described in `docs/architecture.md` and the durable boundary choice is recorded in `docs/decisions/0002-glibc-core-from-termux-glibc-repo.md`.

## Decision

Adopted as the glibc layer foundation. PRoot remains install/debug-time infrastructure rather than the normal application runtime. `gl-farm`, the denylist, and coupled loader-cache refresh are promoted artifacts/contracts owned by the gl module.
