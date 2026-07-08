# Mesa 26.1.4 for native Termux / bionic

**Status:** passed; bionic-world daily-driver lineage  
**Date:** 2026-07-03  
**Provenance:** first-hand build report + later first-hand runtime inspection

## Question

Can the existing Termux Mesa 26.0.6 package recipe be rebased to Mesa 26.1.4 on-device while preserving the native Zink/Turnip/KGSL graphics stack?

## Procedure and findings

The experiment used the `termux-packages` build system rather than an unmanaged direct install into `$PREFIX`.

The preserved report records:

- version/SHA rebase from the 26.0.6 recipe;
- distinction between dependency-resolution stalls and actual Mesa compilation;
- the real on-device build tree under `$HOME/.termux-build/mesa`;
- explicit bionic target configuration;
- whole-file exclusion of `0003-fix-for-anon-file.patch` and `0006-wsi-no-pthread_cancel.patch` from the old patchset;
- confirmation that historical `wsi-termux-x11.patch` and `tu_kgsl_export_dmabuf.patch` were not part of this package lineage;
- final build success as confirmed by the operator.

The report is careful that the exact final package filename and complete post-install diagnostic transcript were not preserved in that session record.

## Later validation

Subsequent first-hand checks observed accelerated Zink/Turnip operation and a `msm,kgsl` configuration whose resulting driver dependency shape became a key counter-example during the glibc Mesa 26.1.4 SIGBUS investigation.

## Decision

Keep this build lineage as the bionic-world graphics baseline and as an architectural comparison point for glibc Mesa work. The `msm,kgsl` lesson was promoted into `docs/decisions/0003-mesa-kmds-msm-kgsl.md`.

See [`report.md`](report.md).
