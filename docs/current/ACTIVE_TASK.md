# Active task: produce the `libjpeg.so.62` compatibility-provider candidate

> Task ID: `produce-libjpeg-so-62-compatibility-provider-candidate`
>
> Expected state on completion: one exact scratch-built `libjpeg.so.62` candidate and structured build/ELF evidence are returned from authoritative user Termux, or the build is explicitly blocked with bounded diagnostics; no installation, provider acceptance, target population, materialization or activation is implied.

## Objective

Produce and analyze the exact compatibility candidate specified by OJ-001:

```text
source: libjpeg-turbo 3.1.0
source SHA-256: 9564c72b1dfd1d6fe6274c5f95a8d989b59854575d4bbee44ade7bc17aa9bc93
WITH_JPEG7=OFF
WITH_JPEG8=OFF
expected member: libjpeg.so.62.4.0
expected DT_SONAME: libjpeg.so.62
```

## Why now

OJ-001 is the only remaining T0 identity contradiction. The requirement and production path are now explicit, so the smallest next step is to obtain one real SONAME-62 object before any provider-authority or broader reference-adapted review proceeds.

## Current accepted decisions

- `libjpeg.so.62` is the authoritative stable lookup requirement.
- Existing Termux and Termux-glibc package recipes enable `WITH_JPEG8` and produce the incompatible `libjpeg.so.8` family.
- No exact repository SONAME-62 package or artifact is bound.
- A source-built compatibility provider is required, but no unbuilt object has provider authority.
- Seven previously bounded providers remain accepted; composition, target population and activation remain blocked.

## In scope

- Build one scratch-only shared candidate from the exact pinned source in user Termux.
- Record source, command, environment/toolchain coordinates and output manifest.
- Verify source digest, member digest, ELF class/machine and `DT_SONAME`.
- Return candidate bytes and compact evidence in one result `.tar.zst`.
- Preserve all package databases, installed files, provider stores, target layouts and selectors.

## Out of scope

- Installing or packaging the candidate into the live Termux prefix.
- Creating `libjpeg.so.62` aliases to a SONAME-8 object.
- Accepting provider authority solely because the build succeeds.
- Complete JPEG/GTK composition, target paths, population, deployment or activation.
- Rebuilding unrelated dependencies or fulfilling historical SUP-02 requests.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/libjpeg-so-62-provider-candidate-disposition.md`
- `docs/operations/COLLABORATION.md`
- `docs/operations/EXECUTION.md`
- `docs/operations/platforms/chatgpt-web.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/libjpeg-so-62-provider-candidate-disposition.tsv`

## Pending external inputs

None at task start. The agent must prepare the bounded Termux source-build/analyzer package first.

## Next valid action

Create and sandbox-test one self-contained Termux runner that verifies the exact source, builds only in scratch, analyzes the resulting ELF, emits structured status and archives candidate bytes plus evidence without installation.

## Stop conditions

Stop without accepting a candidate if:

- the source digest differs;
- the build produces no `libjpeg.so.62` member or a different `DT_SONAME`;
- the runner would modify installed packages, the live prefix, provider stores, target layouts or selectors;
- the toolchain/build boundary cannot be recorded sufficiently to identify the produced object;
- the only available result remains `libjpeg.so.8`.

## Completion criteria

- one bounded runner package is produced and exact-simulated where possible;
- the user returns one structured result archive;
- candidate bytes, member SHA-256, ELF identity, `DT_SONAME`, source digest and build manifest are reviewable;
- provider authority remains a separate next decision;
- repository and runtime remain unchanged outside accepted review metadata and tests.
