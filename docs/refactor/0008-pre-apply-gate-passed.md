# 0008 — Pre-Apply Gate Passed

## Context

After syncing commit `5a927e9`, the real Termux device reran the complete repository-level pre-apply gate.

All repository smoke tests passed:

```text
deploy smoke test: PASS
shell layout smoke test: PASS
adopt user env smoke test: PASS
```

The user-environment adoption dry-run completed successfully and planned exactly these personal-file transitions:

```text
$HOME/.bashrc
    backup -> repository-owned symlink

$HOME/uv-base/pyproject.toml
    backup -> repository-owned symlink

$HOME/uv-base/uv.lock
    backup -> repository-owned symlink

$HOME/uv-base/.uvrc
    backup -> retirement

$HOME/.config/bash/*
    repository-owned shell/module fragments
```

The runtime deployment dry-run also completed successfully.

## Reviewed deployment plan

The runtime-facing deploy phase planned:

```text
modules/desktop
    $HOME/.local/bin/startxfce-x11

modules/gl
    $HOME/.config/bash/conf.d/40-gl.sh
    $HOME/gl/env
    $HOME/gl/bin/{gl-farm,gl-run}
    $HOME/gl/shims/xdg-open
    $HOME/gl/toolchain/*

packages/vscode
    $HOME/.local/bin/code

packages/obsidian
    $HOME/gl/bin/obsidian
    $HOME/gl/bin/obsidian-app

packages/mesa-glibc
    $HOME/gl/build/build-mesa.sh
    $HOME/gl/build/pyproject.toml
    $HOME/gl/build/uv.lock
    $HOME/gl/build/patches/mesa
```

The dry-run also planned removal of the obsolete experiment-specific live symlink:

```text
$HOME/gl/build/diag
```

## Safety findings confirmed

The reviewed dry-runs showed that:

1. shell/uv-base adoption and runtime deployment are separated;
2. runtime deploy does not attempt to replace `$HOME/.bashrc` or uv-base definition files;
3. legacy directory symlinks under `$HOME/gl` are converted once in dry-run simulation;
4. package-owned launchers are deployed to their live public entry points;
5. the Mesa build compatibility surface is preserved;
6. no real file or runtime prefix was modified during preflight.

## Gate result

The repository is ready to begin live migration in two controlled phases:

```text
Phase A
    tools/adopt-user-env --apply
    -> validate new shell composition and uv-base behavior

Phase B
    tools/deploy
    -> validate gl live topology, launchers, toolchain, and session entry point
```

The phases must remain separate. Runtime deployment should not begin until Phase A validation passes.

## Next validation requirements

After `tools/adopt-user-env --apply`, validate:

```text
$HOME/.bashrc symlink target
uv-base definition symlink targets
legacy .uvrc retired
backup files present
interactive PATH order
VIRTUAL_ENV not set by promoted configuration
python resolves to uv-base when .venv exists
uva/uvr/uvs functions available
uv-base definition and runtime tests pass
```

Only then proceed to `tools/deploy`.
