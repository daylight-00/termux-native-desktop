# glibc-cross-toolchain

Status: **passed** — prerequisite for all Mesa work

## Question

Can we compile *for* the Termux glibc target while running build tools on
bionic (meson/ninja/python), without a real cross-sysroot?

## Baseline

gcc-glibc exists as a package, but naive invocation picks the wrong
(bionic) ld, mangles quoted arguments, and glibc tools can't be exec'd
directly from bionic shells.

## Procedure / Evidence

- `modules/gl/overlay/home/gl/toolchain/glibc-{gcc,g++,ar,ranlib,strip,exec}`: the explicit-loader pattern (`ld-linux --library-path $PREFIX/glibc/lib <tool> -B$PREFIX/glibc/bin/`). Field-verified details: `"$@"` quoting (unquoted split args — real failure), `-B` pinning binutils (wrong native ld otherwise).
- `glibc-pkg-config` pinned to exactly 3 glibc pkgconfig dirs — leaking bionic `.pc` files poisons dependency resolution.
- Host Python deps as a **uv project** (`packages/mesa-glibc/build-env/pyproject.toml` + `uv.lock`): meson, mako, packaging, pyyaml. Reproducible, no global pip state. Interpreter from `cpython-android-cli` companion project.
- Smoke-test gate in `packages/mesa-glibc/build.sh`: compile & run hello via `glibc-exec` before configuring Mesa. Earlier misses fixed en route: bison/flex missing; CPython `_ssl` rpath patch.

## Result / Decision

Passed; built Mesa 26.x repeatedly plus every bisect step. Promoted to `modules/gl/overlay/home/gl/toolchain/`. Rule: build artifacts **where they will live** because prefix RPATH is baked at link time.

## Dating note

Originally assembled during the Mesa 26.0.6 build (2026-07-02, prior session — where the quoting / wrong-ld / `--fix-cortex-a53-835769` issues were fought). Restored from backup tar and formalized into the promoted gl toolchain during the 26.1.4 work (07-04→05), adding the uv build project and smoke-test gate. The repository path later moved during the module/package ownership refactor; this canonical README records the current owner while preserving that history.
