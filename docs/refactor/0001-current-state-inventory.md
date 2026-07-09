# 0001 — Current State Inventory

## Repository baseline

Branch: `main`

Base commit: `3cf41d6fc47050b06e18e956a23cefe25e4fb82a`

User-reported local Git state before refactor:

```text
## main...origin/main
```

The local checkout was clean.

## Legacy promoted source layout

```text
scripts/deploy-gl.sh

setup/glibc/
├── bin/
│   ├── code
│   ├── gl-farm
│   ├── gl-run
│   ├── obsidian
│   └── obsidian-app
├── env
├── shims/
│   └── xdg-open
└── toolchain/
    ├── glibc-ar
    ├── glibc-exec
    ├── glibc-g++
    ├── glibc-gcc
    ├── glibc-pkg-config
    ├── glibc-ranlib
    └── glibc-strip

setup/mesa/
├── build-mesa.sh
├── diag/
│   ├── bisect-test-full.sh
│   └── bisect-test.sh
├── patches/mesa/.gitkeep
├── pyproject.toml
└── uv.lock

setup/session/
├── README.md
└── startxfce-x11
```

## Live system observations

### gl applications

```text
$HOME/gl/apps/
├── obsidian/
└── vscode/
```

These are external live payloads and are not Git-owned installation trees.

### gl promoted links

```text
$HOME/gl/bin       -> repo/setup/glibc/bin
$HOME/gl/env       -> repo/setup/glibc/env
$HOME/gl/shims     -> repo/setup/glibc/shims
$HOME/gl/toolchain -> repo/setup/glibc/toolchain
```

### Mesa build area

```text
$HOME/gl/build/
├── build-mesa.sh       -> repo/setup/mesa/build-mesa.sh
├── diag                -> repo/setup/mesa/diag
├── patches             -> repo/setup/mesa/patches
├── pyproject.toml      -> repo/setup/mesa/pyproject.toml
├── uv.lock             -> repo/setup/mesa/uv.lock
├── cross-bisect.ini
├── cross-full.ini
├── cross-turnip.ini
└── mesa/
    ├── build-26.1.4/
    ├── cross-26.1.4.ini
    └── src/
```

This area mixes tracked recipe links, experiment-generated cross files, source checkout state, and generated build state.

### Mesa installed prefixes

```text
$HOME/gl/opt/
├── mesa-bisect/
├── mesa-bisect-dri3/
├── mesa-glibc -> mesa-glibc-26.1.4-full
├── mesa-glibc-26.1.4/
├── mesa-glibc-26.1.4-full/
├── mesa-glibc-26.1.4-turnip/
└── mesa-glibc-26.1.4-tx/
```

No deletion is part of the repository ownership migration. Runtime-prefix cleanup is a later, separately documented pass.

### uv-base

Observed visible content:

```text
$HOME/uv-base/
├── cpython-3.14-aarch64-linux-android-for-uv.tar.gz
├── pyproject.toml
└── uv.lock
```

Earlier direct inspection also established a hidden `.uvrc` shell integration fragment and generated `.venv` environment. Their migration is handled by the `uv-base` architecture document and a later live deployment step.

### custom CPython

```text
$HOME/opt/cpython-3.14/prefix/
```

This is an installed runtime consumed by `uv-base`; the producing project is `cpython-android-cli`.

## Main structural findings

1. `setup/` mixes capability implementation, application-specific launchers, external software build lifecycle, and experiment harnesses.
2. `gl/build` mixes operational definitions with generated and experiment state.
3. `gl/opt` contains both active runtime selection and historical/experimental prefixes.
4. `gl/bin` currently mixes generic layer commands with application-specific launchers.
5. Live symlinks directly target legacy repository paths, so repository movement and live relinking must be ordered carefully.
