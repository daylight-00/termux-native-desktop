# Obsidian AppImage onboarding

**Status:** passed  
**Dates:** 2026-07-05 to 2026-07-06  
**Provenance:** first-hand session report (`report.md`)

## Question

Can an arm64 AppImage be treated as another application input format for the native glibc layer, despite the target not using the normal AppImage FUSE/mount execution model?

## Hypothesis

The AppImage-specific problem ends at payload extraction:

```text
AppImage
  -> locate embedded SquashFS
  -> extract AppDir
  -> reuse the normal glibc application onboarding pipeline
```

## Procedure

1. calculate the end of the ELF section-header table;
2. cross-check that offset against the first `hsqs` SquashFS magic position;
3. split the payload and extract it with `squashfs-tools-ng` (`sqfs2tar | tar -x`);
4. inventory all ELF files;
5. patch executable interpreters and RPATH while preserving `$ORIGIN`;
6. verify every ELF dependency with the glibc `ldd` path;
7. bypass upstream `AppRun` behavior that injects `LD_LIBRARY_PATH`;
8. validate CPU-mode launch before enabling the established ANGLE Vulkan path;
9. validate Obsidian CLI integration separately from GUI launch.

## Evidence

The report records:

- exact matching ELF-calculated and SquashFS magic offsets;
- successful extraction of the AppDir tree;
- 11-ELF inventory and complete dependency resolution;
- successful X11, TLS/network, and application startup;
- WebGL2 renderer evidence showing ANGLE -> Vulkan -> Turnip -> Adreno 730;
- successful Obsidian CLI integration after resolving its discovery/launch contract.

## Result

Passed. AppImage is a viable front-end format for the same downstream glibc onboarding pipeline.

## Decision

Keep AppImage extraction as a narrow input adapter, not as a separate runtime architecture. The package-owned launchers are now `packages/obsidian/launcher/obsidian` and `packages/obsidian/launcher/obsidian-app`; `tools/deploy` exposes them at the live entry points.

See [`report.md`](report.md).
