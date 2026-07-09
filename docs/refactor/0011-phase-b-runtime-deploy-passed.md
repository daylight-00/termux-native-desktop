# 0011 — Phase B Runtime Deployment Passed

## Context

The real Termux device executed the Phase B runtime deployment after Phase A user-environment adoption had already passed.

Apply command:

```text
tools/deploy
```

The operation completed successfully.

## Live topology conversion

The following legacy directory symlinks were converted into real live directories:

```text
$HOME/gl/bin
$HOME/gl/shims
$HOME/gl/toolchain
$HOME/gl/build/patches
```

Repository-owned leaf symlinks were installed beneath them.

## Verified module-owned links

### Desktop

```text
$HOME/.local/bin/startxfce-x11
    -> modules/desktop/overlay/home/.local/bin/startxfce-x11
```

### gl module

```text
$HOME/.config/bash/conf.d/40-gl.sh
    -> modules/gl/overlay/home/.config/bash/conf.d/40-gl.sh

$HOME/gl/env
    -> modules/gl/overlay/home/gl/env

$HOME/gl/bin/gl-farm
    -> modules/gl/overlay/home/gl/bin/gl-farm

$HOME/gl/bin/gl-run
    -> modules/gl/overlay/home/gl/bin/gl-run

$HOME/gl/shims/xdg-open
    -> modules/gl/overlay/home/gl/shims/xdg-open

$HOME/gl/toolchain/glibc-*
    -> modules/gl/overlay/home/gl/toolchain/*
```

All expected toolchain wrappers resolved to their new module-owned sources:

```text
glibc-ar
glibc-exec
glibc-g++
glibc-gcc
glibc-pkg-config
glibc-ranlib
glibc-strip
```

## Verified package-owned entry points

```text
$HOME/.local/bin/code
    -> packages/vscode/launcher/code

$HOME/gl/bin/obsidian
    -> packages/obsidian/launcher/obsidian

$HOME/gl/bin/obsidian-app
    -> packages/obsidian/launcher/obsidian-app
```

## Verified Mesa compatibility surface

```text
$HOME/gl/build/build-mesa.sh
    -> packages/mesa-glibc/build.sh

$HOME/gl/build/pyproject.toml
    -> packages/mesa-glibc/build-env/pyproject.toml

$HOME/gl/build/uv.lock
    -> packages/mesa-glibc/build-env/uv.lock

$HOME/gl/build/patches/mesa
    -> packages/mesa-glibc/patches/mesa
```

The obsolete experiment-specific live symlink was removed:

```text
$HOME/gl/build/diag
    absent
```

## Runtime payload preservation

The structural migration preserved external runtime state:

```text
VS Code payload: present
Obsidian payload: present
active Mesa selection: present
```

No application payload or installed Mesa prefix was removed by Phase B.

## Syntax validation

Shell syntax validation passed for:

```text
startxfce-x11
gl-farm
gl-run
xdg-open
all glibc toolchain wrappers
VS Code launcher
Obsidian launchers
Mesa build script
```

## Command resolution validation

A clean interactive shell resolved:

```text
gl-run        -> $HOME/gl/bin/gl-run
gl-farm       -> $HOME/gl/bin/gl-farm
obsidian      -> $HOME/gl/bin/obsidian
obsidian-app  -> $HOME/gl/bin/obsidian-app
code          -> $HOME/.local/bin/code
startxfce-x11 -> $HOME/.local/bin/startxfce-x11
```

## Isolated gl environment validation

The gl environment contract passed:

```text
DISPLAY=:1
XDG_RUNTIME_DIR=$PREFIX/tmp/gl-runtime
VK_ICD_FILENAMES=$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json
VK_DRIVER_FILES=$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json
LD_LIBRARY_PATH contamination: absent
```

The Vulkan ICD variables matched and pointed to the active glibc Mesa selection.

## glibc toolchain validation

The target compiler wrapper executed successfully:

```text
gcc (GCC) 14.2.1 20250228 (...)
glibc-gcc wrapper: PASS
```

This validates that the post-migration toolchain leaf-link topology still reaches a functional glibc compiler invocation path.

## Result

Phase B structural validation passed completely:

```text
===== Phase B structural validation =====
PASS
```

The ownership refactor has now been applied successfully to the live device for:

```text
personal shell
uv-base definition
CPython runtime consumer contract
runtime-facing desktop integration
gl runtime integration
glibc toolchain integration
VS Code launcher ownership
Obsidian launcher ownership
Mesa maintenance compatibility paths
```

## Next workstreams

The repository-ownership migration is structurally complete. Follow-up work should be separated into three independent workstreams.

### A. Workload validation

Validate real end-to-end workloads without changing ownership topology:

```text
gl-run glxinfo -B
VS Code launcher and GUI
Obsidian launcher and GUI
desktop session restart
```

### B. Runtime residue inventory and cleanup design

Classify, but do not immediately delete:

```text
$HOME/gl/build/*
$HOME/gl/opt/*
$HOME/opt/*
$HOME/ark/*
$HOME/uv-base/cpython-*.tar.gz
```

Separate active state, historical controls, rebuildable outputs, and unique evidence before cleanup.

### C. Repository history cleanup decision

The refactor branch contains several temporary connector-generated commits (`temp`, `noop`, etc.) that are documented but noisy. Decide separately whether to:

```text
preserve exact branch history
or
create a clean squashed/curated integration branch before merging to main
```

Do not rewrite the already validated live filesystem merely to clean Git history.
