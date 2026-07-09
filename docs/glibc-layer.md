# glibc Application Layer

This guide integrates the recovered `gl` layer README with the current repository structure. Detailed experiment provenance remains under `experiments/glibc/` and `experiments/gpu/`.

## Goal

Run conventional Linux arm64/glibc application distributions from native Termux without using PRoot as the application runtime.

```text
application   ~/gl/apps/<name>/
library farm ~/gl/lib/
glibc core   $PREFIX/glibc/
warehouse    $PREFIX/var/lib/proot-distro/containers/debian/rootfs
```

PRoot is retained for package installation, dependency discovery, and debugging controls. Runtime applications execute outside PRoot.

## Library boundary

The conceptual lookup model is:

```text
$ORIGIN
  -> $PREFIX/glibc/lib
  -> ~/gl/lib
```

Important rules:

- never expose a glibc `LD_LIBRARY_PATH` to the bionic Termux shell;
- libc-family libraries come from the Termux glibc core, never the Debian farm;
- glibc-repo X11/xcb libraries must win over Debian variants for local Termux:X11 socket access;
- application-local libraries must keep `$ORIGIN` in RPATH where required;
- transitive dependencies are handled through glibc loader configuration and `ldconfig`.

## Bootstrap outline

1. Install Termux X11/glibc prerequisites, including glibc-repo X11/xcb packages.
2. Install a Debian PRoot distribution as the package/library warehouse.
3. Populate required general libraries inside the rootfs.
4. Run `gl-farm` to rebuild `~/gl/lib` from allowed rootfs libraries.
5. Register core then farm in the glibc loader configuration and refresh `ldconfig`.
6. Deploy module overlays and package-owned launchers through `tools/deploy`.

A representative core setup includes:

```sh
pkg install x11-repo tur-repo termux-x11-nightly patchelf file curl proot-distro
pkg install glibc-repo glibc libx11-glibc libxcb-glibc
proot-distro install debian
```

The rootfs path may vary across proot-distro generations; the current project contract uses `containers/debian/rootfs`.

## Library farm

`modules/gl/overlay/home/gl/bin/gl-farm`:

- rebuilds `~/gl/lib` as symlinks into selected Debian rootfs library directories;
- excludes the libc family through a denylist;
- performs a contamination check;
- refreshes the glibc loader cache.

Farm regeneration and `ldconfig` refresh are one operation.

## Application onboarding

For a conventional tarball or extracted application tree:

1. unpack under `~/gl/apps/<name>/`;
2. use the Debian rootfs as a dependency oracle when additional libraries are needed;
3. rebuild the farm if the rootfs library set changes;
4. patch executable interpreters to the Termux glibc loader;
5. patch RPATH while preserving `$ORIGIN`;
6. verify every ELF with the glibc `ldd` path;
7. create a package-owned launcher that sources `~/gl/env` and clears incompatible preload state at process entry;
8. validate CPU/basic GUI startup before treating GPU enablement as a separate milestone.

AppImage is supported as an input adapter by extracting the embedded SquashFS payload first, then reusing the same onboarding pipeline. See `experiments/glibc/obsidian-appimage/`.

## Common failure signatures

1. **`LD_LIBRARY_PATH` contamination** — bionic processes encounter glibc linker scripts and fail with ELF-header errors.
2. **Transitive dependency failure** — direct RPATH lookup succeeds, but downstream dependencies fail until loader configuration/cache is correct.
3. **X display failure** — Debian `libxcb` wins over the Termux-aware glibc-repo build.
4. **Lost `$ORIGIN`** — bundled application libraries such as Electron-local `.so` files stop resolving after careless RPATH replacement.
5. **Electron sandbox ordering** — sandbox checks can occur before `argv.json`; the project uses launch environment/CLI policy instead.
6. **URL intents silently blocked** — Android background-activity policy requires Termux's Display over other apps permission.
7. **Wrong Vulkan ICD** — a glibc process inherits or default-scans the bionic ICD; always pin both Vulkan ICD variables in the glibc environment.

## Current promoted owners

```text
modules/gl/overlay/home/gl/env
modules/gl/overlay/home/gl/bin/gl-farm
modules/gl/overlay/home/gl/bin/gl-run
modules/gl/overlay/home/gl/shims/xdg-open
modules/gl/overlay/home/gl/toolchain/*

modules/desktop/overlay/home/.local/bin/startxfce-x11

packages/vscode/launcher/code
packages/obsidian/launcher/obsidian
packages/obsidian/launcher/obsidian-app
packages/mesa-glibc/build.sh
packages/mesa-glibc/build-env/*
packages/mesa-glibc/patches/

tools/deploy
```

Runtime state remains outside Git tracking: application trees, the farm, Mesa install prefixes, build worktrees, generated uv environments, and the installed glibc core.

## Validated workloads

- official Microsoft VS Code arm64 tarball;
- Obsidian arm64 AppImage after extraction/onboarding;
- Miniforge/Conda/Mamba with environment creation and compiled NumPy workload;
- glibc OpenGL 4.6 through Zink -> Turnip;
- ANGLE Vulkan -> Turnip for official VS Code.

The next major scientific workload target is PyMOL.
