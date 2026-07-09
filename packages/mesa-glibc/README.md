# Mesa glibc package

This package owns the accepted Mesa acquisition/build/install lifecycle for the glibc application layer.

## Current promoted contents

```text
packages/mesa-glibc/
├── build.sh
├── build-env/
│   ├── pyproject.toml
│   └── uv.lock
└── patches/
    └── mesa/
```

The build uses the common glibc target wrappers owned by `modules/gl/overlay/home/gl/toolchain/`.

The validated current configuration includes:

```text
platforms=x11
vulkan-drivers=freedreno
freedreno-kmds=msm,kgsl
gallium-drivers=zink
```

## Transitional live compatibility paths

The first ownership refactor intentionally preserves the existing live build-script contract:

```text
packages/mesa-glibc/build.sh
    -> $HOME/gl/build/build-mesa.sh

packages/mesa-glibc/build-env/pyproject.toml
    -> $HOME/gl/build/pyproject.toml

packages/mesa-glibc/build-env/uv.lock
    -> $HOME/gl/build/uv.lock

packages/mesa-glibc/patches/mesa
    -> $HOME/gl/build/patches/mesa
```

This compatibility mapping allows repository ownership to change before the build script's internal work-directory model is redesigned.

## Generated state outside Git

```text
$HOME/gl/build/mesa/src/
$HOME/gl/build/mesa/build-*/
$HOME/gl/build/mesa/cross-*.ini
$HOME/gl/opt/mesa-*/
```

The old bisect judge scripts are experiment-specific and now live under:

```text
experiments/gpu/mesa-26.1.4-present-sigbus/recipe/
```

See `docs/gpu.md` and `docs/decisions/0003-mesa-kmds-msm-kgsl.md`.
