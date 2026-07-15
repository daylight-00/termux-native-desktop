# Active task: rebuild the `libjpeg.so.62` compatibility-provider candidate without runpath

> Task ID: `rebuild-libjpeg-so-62-compatibility-provider-candidate-without-runpath`
>
> Expected state on completion: one new scratch-built `libjpeg.so.62.4.0` object from the exact pinned source is returned with no `DT_RPATH` or `DT_RUNPATH`, or the corrected build is explicitly blocked with bounded diagnostics. Provider authority, target population, materialization and activation remain separate and unaccepted.

## Objective

Repeat the successful OJ-001 source build with the smallest correction required by the first candidate review:

```text
source: libjpeg-turbo 3.1.0
source SHA-256: 9564c72b1dfd1d6fe6274c5f95a8d989b59854575d4bbee44ade7bc17aa9bc93
WITH_JPEG7=OFF
WITH_JPEG8=OFF
ENABLE_SHARED=ON
ENABLE_STATIC=OFF
CMAKE_SKIP_RPATH=ON
expected member: libjpeg.so.62.4.0
expected DT_SONAME: libjpeg.so.62
required DT_RPATH/DT_RUNPATH state: absent
```

## Why now

The first real candidate was produced successfully and has the expected source, AArch64 ELF, concrete member, digest, SONAME and `LIBJPEG_6.2` symbol version. It is rejected because its dynamic section contains a 175-character colon-only `DT_RUNPATH` created by the scratch build configuration. The smallest valid next step is a new unmodified build with RPATH generation disabled, not in-place editing of the first ELF.

## Current accepted decisions

- `libjpeg.so.62` remains the authoritative lookup requirement.
- `libjpeg.so.8` remains an incompatible substitute and no alias bridge is permitted.
- First candidate `1d32a4b12ef3a6032626af13b69a64c45a0a0a9bb4090e0b61d9312811208d88` proves the pinned build path can produce `libjpeg.so.62.4.0` but is rejected for provider review because `DT_RUNPATH` is present.
- CMake 4.4.0 was installed separately by the user before the first runner; the runner did not mutate package state.
- Seven previously bounded providers remain accepted. Complete composition, target population and activation remain blocked.

## In scope

- Build one new scratch-only shared candidate with `CMAKE_SKIP_RPATH=ON`.
- Preserve the exact source digest, ABI options and glibc AArch64 toolchain boundary.
- Verify member digest, ELF class/machine/type, SONAME, dynamic dependency set and versioned symbols.
- Fail if either `DT_RPATH` or `DT_RUNPATH` is present.
- Return the new candidate bytes and compact structured evidence in one result `.tar.zst`.
- Preserve package databases, installed files, provider stores, target layouts and selectors.

## Out of scope

- Editing, stripping or patching the first candidate in place.
- Installing or packaging either candidate into the live prefix.
- Creating `libjpeg.so.62` aliases to a SONAME-8 object.
- Accepting provider authority merely because the corrected build succeeds.
- Complete JPEG/GTK composition, target paths, population, deployment or activation.
- Rebuilding unrelated dependencies or fulfilling historical SUP-02 requests.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/libjpeg-so-62-provider-candidate-disposition.md`
- `docs/evidence/libjpeg-so-62-compatibility-provider-candidate-result-review.md`
- `docs/operations/COLLABORATION.md`
- `docs/operations/EXECUTION.md`
- `docs/operations/platforms/chatgpt-web.md`

## Pending external inputs

None at task start. The agent must prepare the corrected bounded Termux source-build/analyzer package.

## Next valid action

Create and synthetic-test one self-contained Termux runner that repeats the exact pinned scratch build with `CMAKE_SKIP_RPATH=ON`, rejects any `DT_RPATH` or `DT_RUNPATH`, and returns the new bytes plus source/build/ELF evidence without installation.

## Stop conditions

Stop without accepting a corrected candidate if:

- the source digest differs;
- the build produces no `libjpeg.so.62.4.0` member or a different `DT_SONAME`;
- any `DT_RPATH` or `DT_RUNPATH` remains;
- the toolchain/build boundary cannot be recorded sufficiently;
- protected live state changes;
- the only available output remains `libjpeg.so.8` or the first rejected candidate bytes.

## Completion criteria

- one corrected runner package is produced and synthetic-tested;
- the user returns one structured result archive;
- new candidate bytes, digest, ELF identity, SONAME, dynamic tags, source digest and build manifest are reviewable;
- the result explicitly proves no `DT_RPATH` or `DT_RUNPATH`;
- provider authority remains a separate next decision;
- repository and runtime remain unchanged outside accepted review metadata and tests.
