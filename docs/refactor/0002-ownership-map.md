# 0002 — Ownership Map

## Governing distinctions

```text
module
    owns a system capability and its project-authored integration files

package
    owns acquisition/build/adaptation/install/validation lifecycle for an external payload

experiment
    owns discovery-specific harnesses, evidence, and provenance

tool
    owns repository operator workflow
```

## Confirmed ownership decisions

### Desktop module

```text
setup/session/README.md
    -> modules/desktop/README.md

setup/session/startxfce-x11
    -> modules/desktop/overlay/home/.local/bin/startxfce-x11
```

### gl module

```text
setup/glibc/env
    -> modules/gl/overlay/home/gl/env

setup/glibc/bin/gl-run
    -> modules/gl/overlay/home/gl/bin/gl-run

setup/glibc/bin/gl-farm
    -> modules/gl/overlay/home/gl/bin/gl-farm

setup/glibc/shims/xdg-open
    -> modules/gl/overlay/home/gl/shims/xdg-open

setup/glibc/toolchain/*
    -> modules/gl/overlay/home/gl/toolchain/*
```

The toolchain remains a gl maintenance capability rather than becoming Mesa package-private state.

### Application packages

```text
setup/glibc/bin/code
    -> packages/vscode/launcher/code

setup/glibc/bin/obsidian
    -> packages/obsidian/launcher/obsidian

setup/glibc/bin/obsidian-app
    -> packages/obsidian/launcher/obsidian-app
```

These are application-specific launchers, not generic gl layer commands.

### Mesa package

```text
setup/mesa/build-mesa.sh
    -> packages/mesa-glibc/build.sh

setup/mesa/pyproject.toml
    -> packages/mesa-glibc/build-env/pyproject.toml

setup/mesa/uv.lock
    -> packages/mesa-glibc/build-env/uv.lock

setup/mesa/patches/mesa/.gitkeep
    -> packages/mesa-glibc/patches/mesa/.gitkeep
```

The first migration preserves behavior and blob identity; build-path redesign is a later change.

### Mesa SIGBUS experiment

```text
setup/mesa/diag/bisect-test.sh
    -> experiments/gpu/mesa-26.1.4-present-sigbus/recipe/bisect-test.sh

setup/mesa/diag/bisect-test-full.sh
    -> experiments/gpu/mesa-26.1.4-present-sigbus/recipe/bisect-test-full.sh
```

The scripts explicitly implement `git bisect` judge contracts and therefore belong with experiment reproduction material.

### Repository tool

```text
scripts/deploy-gl.sh
    -> tools/deploy
```

The implementation is rewritten for module overlays and package launcher entry points.

## Deferred ownership

`uv-base` tracked project files and generated lock identity will be added after the live `pyproject.toml` and `uv.lock` are captured.

The custom CPython runtime consumer package will be created after its artifact identity and transfer/install contract are documented.
