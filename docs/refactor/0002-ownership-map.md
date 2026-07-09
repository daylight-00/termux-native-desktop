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

The gl module also owns its Bash integration fragment:

```text
modules/gl/overlay/home/.config/bash/conf.d/40-gl.sh
    -> $HOME/.config/bash/conf.d/40-gl.sh
```

### Shell module

The personal interactive Bash configuration is system behavior and is now module-owned:

```text
$HOME/.bashrc
    -> modules/shell/overlay/home/.bashrc

$HOME/.config/bash/interactive.sh
    -> modules/shell/overlay/home/.config/bash/interactive.sh

$HOME/.config/bash/prompt.sh
    -> modules/shell/overlay/home/.config/bash/prompt.sh

$HOME/.config/bash/aliases.sh
    -> modules/shell/overlay/home/.config/bash/aliases.sh

$HOME/.config/bash/conf.d/99-path-policy.sh
    -> modules/shell/overlay/home/.config/bash/conf.d/99-path-policy.sh
```

The shell module owns generic shell personality and final command precedence. Capability-specific shell fragments remain owned by the relevant capability module.

### uv-base module

The native disposable base environment is represented by:

```text
modules/uv-base/overlay/home/uv-base/pyproject.toml
    -> $HOME/uv-base/pyproject.toml

modules/uv-base/overlay/home/uv-base/uv.lock
    -> $HOME/uv-base/uv.lock

modules/uv-base/overlay/home/.config/bash/conf.d/60-uv-base.sh
    -> $HOME/.config/bash/conf.d/60-uv-base.sh
```

Generated state remains outside Git:

```text
$HOME/uv-base/.venv
```

The legacy `$HOME/uv-base/.uvrc` is retired after hash-guarded backup because its contents are shell integration rather than uv-native project configuration.

### CPython Android runtime consumer package

```text
packages/cpython-android-runtime/
```

owns:

- producer repository identity;
- artifact filename, exact byte size, target, Python version, and SHA-256;
- intended install prefix;
- installed runtime validation.

It does not own the archive in Git or the producer project's build history.

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

### Repository tools

```text
scripts/deploy-gl.sh
    -> tools/deploy
```

Additional one-time migration tooling:

```text
tools/adopt-user-env
```

The adoption tool hash-verifies and backs up the pre-refactor personal shell and uv-base definition before replacing them with repository-owned links.
