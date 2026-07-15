# Mesa glibc package

This package owns the acquisition, build, install, provenance, and candidate lifecycle for the project-built glibc Mesa provider artifacts.

It does not own the entire graphics composition by itself.

## Current source contents

```text
packages/mesa-glibc/
├── build.sh
├── build-env/
│   ├── pyproject.toml
│   └── uv.lock
└── patches/
    └── mesa/
```

The build uses the current glibc target wrappers physically grouped under:

```text
modules/gl/overlay/home/gl/toolchain/
```

Their semantic owner is `toolchain.glibc-target`, not the Mesa provider package.

## Current validated provider build

```text
platforms=x11
vulkan-drivers=freedreno
freedreno-kmds=msm,kgsl
gallium-drivers=zink
egl=enabled
glx=dri
llvm=disabled
```

The practical local working/broken split tracked whether the tested Turnip ICD retained its libdrm dependency. The exact low-level present-SIGBUS mechanism is still open.

The `msm` backend is not claimed as the runtime kernel path on the stock Android target; KGSL remains the runtime device interface.

## Provider responsibility

This package can own project-built artifacts such as:

```text
managed Turnip/Freedreno ICD
project-built Mesa/Zink artifacts when selected
versioned installation prefix
build options and source identity
patch set
provider validation receipt
```

It does not automatically own:

```text
rootfs GLVND/GLX libraries
rootfs Gallium/Zink frontend selected by current runtime
prefix Vulkan loader/support
Mesa device-select layer
GBM providers
application-local ANGLE/Vulkan libraries
application feature mode
X11 bridge
```

Those are separate provider, bridge, or application-domain relations.

## Current cross-version graphics composition

The accepted OpenGL/Zink path currently includes:

```text
rootfs GLVND / libGL / libGLX 1.7.0
    -> rootfs Mesa GLX vendor / Gallium-Zink 25.0.7
    -> prefix Vulkan loader/support
    -> project provider-store Turnip/Freedreno 26.1.4 lineage
    -> KGSL
    -> Adreno 730
```

This tested composition works.

It is not adequately described by one `Mesa version` field.

Provider-composition identity must include independently changing layers:

```text
GLVND/GLX frontend
Gallium/Zink frontend
Vulkan loader/support
Mesa device-select/GBM layers
Turnip/Freedreno driver
kernel/device target
```

Changes to any participating layer can trigger affected graphics gates.

## Versioned install and promotion

Generated provider state remains outside Git and outside the runtime adapter tree:

```text
${XDG_STATE_HOME:-$HOME/.local/state}/termux-native-desktop/workspaces/mesa/
${XDG_STATE_HOME:-$HOME/.local/state}/termux-native-desktop/providers/mesa/candidates/
${XDG_STATE_HOME:-$HOME/.local/state}/termux-native-desktop/providers/mesa/current
```

Legacy `$HOME/gl/build/{.venv,mesa}` and `$HOME/gl/opt/mesa-*` paths are compatibility symlinks only.

The intended provider lifecycle is:

```text
source/build identity
    -> versioned candidate prefix
    -> provider/capability validation
    -> application regression where required
    -> stable active pointer
    -> retained previous validated prefix
```

A versioned directory is useful only when its provider bytes are actually retained. A pointer to mutable external bytes is not immutable rollback.

## Current stable pointer

The canonical active pointer is:

```text
${XDG_STATE_HOME:-$HOME/.local/state}/termux-native-desktop/providers/mesa/current
```

The current live consumer policy retains this compatibility path:

```text
$HOME/gl/opt/mesa-glibc
```

Promotion of this pointer must remain separate from application feature policy and from glibc substrate updates.

```text
Mesa provider rollback
    !=
glibc substrate rollback
```

## Transitional live build compatibility

The ownership refactor currently preserves:

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

These are migration compatibility paths, not architectural identities. Mutable build state and provider candidates are migrated with `tools/migrate-local-layout`; repository deployment remains independently atomic.

## Revalidation triggers

Run affected gates when:

```text
Mesa source/version/patch/build options change
managed provider prefix or stable pointer changes
Vulkan loader/support changes
rootfs GLVND/GLX/Zink/device-select/GBM layers change
glibc substrate changes
kernel/device target changes
application consumer version or feature policy changes
selected-device evidence logic changes materially
```

Do not rerun unrelated application gates when only documentation changes.

## Evidence and diagnostics

Historical bisect judges live under:

```text
experiments/gpu/mesa-26.1.4-present-sigbus/recipe/
```

They are experiment diagnostics, not deployed maintenance commands.

Current graphics contract:

```text
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

Historical architecture audit:

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
```

See also `docs/gpu.md` and `docs/decisions/0003-mesa-kmds-msm-kgsl.md`.
