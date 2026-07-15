# Active task: rerun the libjpeg/GdkPixbuf controls with loader isolation

> Task ID: `rerun-libjpeg-so-62-gdkpixbuf-with-loader-isolation`
>
> Expected state on completion: direct candidate/oracle decode is measured through a direct Termux-glibc loader and an ELF-only scratch runtime shim; broader GdkPixbuf controls use the same bounded core world. Provider authority remains a later decision.

## Objective

Replace the invalid 12-cell launcher environment with a smaller valid comparison that cannot expose glibc paths to a Bionic shell.

## Why now

The first 12-cell matrix cannot answer the provider question because its launcher started a Bionic shell under a foreign `LD_LIBRARY_PATH` and exposed raw linker-script paths. Repeating the same launcher would only reproduce analyzer defects.

## Known facts

- Candidate identity `a537840e…` remains accepted.
- Static GdkPixbuf binding requires 22 JPEG symbols; none are missing.
- The first functional call exited 139.
- The first diagnostic matrix also failed for the Debian oracle because its launcher/runtime construction was invalid.
- Zero matrix passes do not reject the candidate or oracle.

## In scope

- ELF-only scratch shim for the Termux glibc core runtime.
- Direct loader invocation with `LD_PRELOAD` and `LD_LIBRARY_PATH` unset.
- Direct `djpeg` candidate/oracle controls without Debian dependency paths.
- GdkPixbuf candidate/oracle file and memory controls with core-first ordering.
- Exact loader lists, stage markers, maps and structured classification.
- One result archive; individual cell crashes remain evidence rows.

## Out of scope

- Package installation or rootfs mutation.
- The `glibc-exec` shell wrapper for diagnostic execution.
- Treating raw `$PREFIX/glibc/lib` as a runtime farm.
- Provider acceptance, target population, deployment or activation.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/libjpeg-so-62-runpath-free-compatibility-provider-candidate-result-review.md`
- `docs/evidence/libjpeg-so-62-gdkpixbuf-consumer-binding-result-review.md`
- `docs/evidence/libjpeg-so-62-gdkpixbuf-diagnostic-matrix-result-review.md`
- `docs/operations/EXECUTION.md`
- `docs/operations/platforms/chatgpt-web.md`

## Pending external inputs

None.

## Next valid action

Run one self-contained loader-isolated diagnostic runner. The user-facing command surface is limited to `rclone copyto` and `bash runner.sh`.

## Stop conditions

Stop if candidate, oracle, consumer, repository, or protected-state identity drifts; if the core shim contains a non-ELF target; or if the diagnostic would require package installation, rootfs mutation, provider installation, target population, deployment, or activation.

## Completion criteria

- direct candidate and oracle cells use no Debian library path;
- no Bionic process starts with a glibc `LD_LIBRARY_PATH`;
- runtime shim entries resolve only to ELF objects;
- direct and GdkPixbuf results are independently recorded;
- provider authority remains separate.
