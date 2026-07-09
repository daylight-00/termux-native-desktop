# 0010 — Phase B Runtime Deployment Plan

## Purpose

Phase B migrates the runtime-facing live topology after Phase A has already adopted the personal shell and uv-base definition.

This phase is intentionally limited to:

```text
modules/desktop
modules/gl
package-owned public launchers
Mesa maintenance compatibility links
```

It does not change:

```text
$HOME/.bashrc
$HOME/uv-base/pyproject.toml
$HOME/uv-base/uv.lock
$HOME/uv-base/.venv
$HOME/opt/cpython-3.14/prefix
$HOME/gl/apps/*
$HOME/gl/opt/*
$HOME/gl/lib/*
```

## Apply step

```bash
tools/deploy
```

Expected topology conversion:

```text
legacy directory symlinks
    $HOME/gl/bin
    $HOME/gl/shims
    $HOME/gl/toolchain

become real directories containing repository-owned leaf symlinks.
```

The Mesa build compatibility path similarly converts:

```text
$HOME/gl/build/patches
```

from the legacy repository-directory symlink into a live directory containing:

```text
$HOME/gl/build/patches/mesa
    -> packages/mesa-glibc/patches/mesa
```

The obsolete live experiment symlink:

```text
$HOME/gl/build/diag
```

is removed.

## Validation layers

### 1. Topology validation

Verify:

- `gl/bin`, `gl/shims`, and `gl/toolchain` are real directories;
- expected leaf entries are symlinks to module/package owners;
- Mesa compatibility links point to `packages/mesa-glibc`;
- obsolete `gl/build/diag` is absent;
- application payloads and installed Mesa prefixes remain present and untouched.

### 2. Syntax and resolution validation

Run shell syntax checks on:

```text
startxfce-x11
gl-run
gl-farm
xdg-open
glibc target wrappers
VS Code launcher
Obsidian launchers
Mesa build script
```

Validate command resolution from a clean interactive shell without launching heavyweight GUI applications.

### 3. Lightweight runtime validation

Source `~/gl/env` in an isolated child shell and inspect:

```text
DISPLAY
XDG_RUNTIME_DIR
VK_ICD_FILENAMES
VK_DRIVER_FILES
LD_LIBRARY_PATH absence
```

Validate one known-safe glibc toolchain invocation such as the target compiler version query if the compiler exists.

### 4. Deferred workload validation

Only after topology and lightweight runtime validation pass:

```text
gl-run glxinfo -B
official VS Code launcher
Obsidian launcher
desktop session launcher
```

These workload tests may require an active X session and therefore are not part of the structural migration apply gate.

## Rollback boundary

Phase B changes only symlink topology and one obsolete experiment symlink.

The legacy repository paths remain recoverable from `main`, and runtime payloads/build products are not deleted.

If Phase B fails before validation completes:

1. record the failing path and command output;
2. do not run gl-farm or rebuild Mesa;
3. do not remove runtime payloads or prefixes;
4. restore legacy links from the pre-refactor `main` deploy path if required;
5. document the incident before modifying migration logic.
