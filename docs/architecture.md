# Architecture

This document describes the current integrated system model. Detailed historical paths and failed alternatives remain in `experiments/`; operational contracts live in the focused guides under `docs/`.

## 1. System boundary

The project keeps Android and Termux native. A glibc application world is added beside the normal bionic world instead of turning the whole environment into a conventional Linux distribution.

```text
Android kernel + device hardware
        |
        +-- KGSL / Adreno 730
        |
        +-- Termux native user space (bionic)
                |
                +-- Termux:X11 + XFCE session
                +-- native Chromium / Code OSS
                +-- native uv-base personal environment
                +-- bionic Mesa / Turnip
                |
                +-- glibc application world
                        |
                        +-- Termux glibc core
                        +-- filtered Debian rootfs library farm
                        +-- application-local libraries
                        +-- glibc Mesa / Turnip
                        +-- VS Code, Obsidian, Conda, ...
```

The system is mixed by design, but each process stays inside one ABI world.

## 2. Two execution worlds, one display

The recovered session launcher and session guide make the boundary explicit:

```text
                    Termux:X11 app (Android surface)
                              ^
                       termux-x11 :1
                              ^
              +---------------+---------------+
              |                               |
         bionic world                    glibc world
         XFCE / native apps              patched glibc apps
         bionic Mesa/Turnip              glibc Mesa/Turnip
```

Both worlds render to the same X display and physical GPU through their own userspace driver stacks. They must not load each other's libraries.

See `docs/desktop-session.md`.

## 3. Environment contract

### Bionic/session world

The desktop session:

- uses `DISPLAY=:1` over the local Unix socket;
- uses `$TMPDIR` as its session `XDG_RUNTIME_DIR`;
- exports the bionic Turnip ICD for bionic clients;
- exports `MESA_LOADER_DRIVER_OVERRIDE=zink` for bionic OpenGL clients in the current recovered launcher;
- starts the X server itself under a cleaned environment with client GPU overrides removed.

The X server therefore stays clean even though bionic GL clients inherit the session GPU contract.

### Native personal environment

The native `uv-base` environment is separate from both the system Python and the glibc Conda ecosystem. Its durable definition is intended to be tracked while `.venv` remains disposable generated state. It provides the default personal Python environment and selected PyPI-distributed tools without mutating the infrastructure Python installation.

### glibc application world

Every glibc launcher sources `modules/gl/overlay/home/gl/env` through the live `~/gl/env` link. That baseline:

- uses a separate `$PREFIX/tmp/gl-runtime` runtime directory;
- removes inherited `VK_ICD_FILENAMES` and `VK_DRIVER_FILES` so a glibc process cannot accidentally consume the bionic session ICD;
- removes inherited `MESA_LOADER_DRIVER_OVERRIDE` and `GALLIUM_DRIVER` so the bionic session's OpenGL bridge/device policy cannot become a glibc default;
- does not select a glibc Vulkan provider or OpenGL bridge globally;
- points TLS consumers at the Termux certificate bundle;
- does not set `LD_LIBRARY_PATH`;
- leaves the bionic session isolated from glibc library lookup state.

Consumers that deliberately require the managed hardware Vulkan provider source:

```text
$HOME/gl/policy/vulkan/freedreno.sh
```

That source-only profile exports both loader variables to the managed glibc Freedreno ICD. VS Code and Obsidian apply it only in their GPU branches. `gl-run` requires it and then adds `MESA_LOADER_DRIVER_OVERRIDE=zink` for OpenGL consumers.

The architecture therefore keeps these dimensions separate:

```text
bionic-session graphics-policy sanitation
Vulkan provider selection
OpenGL-to-Vulkan bridge selection
application GPU feature mode
application-state isolation
```

## 4. glibc library model

The conceptual resolution order is:

```text
application-local libraries ($ORIGIN)
            +
Termux glibc core / Android-sensitive libraries
            +
filtered Debian rootfs library farm
```

The exact lookup behavior is load-bearing:

- the Termux glibc core must win for the libc family;
- glibc-repo X11/xcb libraries must win over Debian variants because the local Termux:X11 socket path is Android/Termux-specific;
- the Debian rootfs is a passive library/package source at runtime;
- transitive dependencies are handled through glibc loader configuration and `ldconfig`, not by broad `LD_LIBRARY_PATH` injection.

See `docs/glibc-layer.md` and `docs/decisions/0002-glibc-core-from-termux-glibc-repo.md`.

## 5. GPU model

There are two userspace GPU stacks because there are two ABI worlds.

```text
bionic app
  -> ANGLE Vulkan / Vulkan / Zink consumer
  -> bionic Vulkan loader + Mesa Turnip
  -> KGSL
  -> Adreno 730


glibc app with explicit hardware profile
  -> ANGLE Vulkan / Vulkan / Zink consumer
  -> glibc Vulkan loader + glibc Mesa Turnip
  -> KGSL
  -> Adreno 730
```

The session-wide bionic policy and glibc provider profiles are deliberately separate. `startxfce-x11` owns the bionic ICD and bionic Zink session policy. `~/gl/env` removes both the bionic Vulkan-provider pair and the bionic OpenGL bridge/Gallium policy at the glibc boundary. Individual glibc launch compositions then choose whether to apply explicit Freedreno, Zink, another validated provider/bridge policy, or no explicit graphics policy.

Accepted glibc application modes:

```text
gl-run
    explicit managed Freedreno
    + MESA_LOADER_DRIVER_OVERRIDE=zink

VS Code / Obsidian GPU
    GL_GPU=1
    explicit managed Freedreno
    ANGLE Vulkan argv
    no Zink/Gallium override

VS Code / Obsidian CPU
    GL_GPU=0
    no explicit provider
    no bridge/Gallium override
    exact --disable-gpu
```

For the captured VS Code control, explicit Freedreno selected Turnip/Adreno 730, while implicit discovery selected LVP/llvmpipe with the same ANGLE Vulkan feature mode. This is why the promoted VS Code GPU branch applies the explicit profile instead of relying on loader discovery.

The promoted VS Code and Obsidian GPU receipts both correlate:

```text
observable environment and argv
CDP primary selected device
ANGLE_VULKAN
GaneshVulkan
managed libvulkan_freedreno.so mapping
/dev/kgsl-3d0 mapping
```

Both selected:

```text
FREEDRENO_TURNIP
Adreno 730
```

A mapped provider alone is not treated as selected-device proof.

For CPU mode, process-name presence is not the architecture invariant. VS Code retained an internal GPU helper using `--use-gl=disabled`; Obsidian did not create one in its accepted CPU receipt. Both had a provider-neutral environment, exact `--disable-gpu`, no GPU-enablement flags, renderer viability, and bounded main-process survival.

For the investigated Mesa 26.1.x configuration, the validated build policy uses `-Dfreedreno-kmds=msm,kgsl`. The working/broken split tracked the presence of the libdrm dependency in the tested builds; the exact low-level crash mechanism remains open.

See `docs/gpu.md`, `docs/decisions/0003-mesa-kmds-msm-kgsl.md`, and `docs/refactor/0091-scoped-graphics-policy-promotion-closure.md`.

## 6. Application-state authority

A clean launch is not automatically an isolated launch. The application may derive its effective configuration directory independently of a generic Chromium argument.

Accepted validation authority:

```text
VS Code
    isolated --user-data-dir
    isolated --extensions-dir

Obsidian
    receipt-local XDG_CONFIG_HOME
    actual receipt-local <config>/obsidian directory
```

The first Obsidian CDP attempt failed because the probe observed the wrong `DevToolsActivePort` path while the application retained `$HOME/.config/obsidian`. The corrected model binds XDG configuration, application-derived user data, process argv, and CDP endpoint observation to the same receipt-local tree.

Normal user configuration, vaults, extensions, and locks are outside promotion evidence.

## 7. Evidence and observability model

The project distinguishes effective behavior from observability artifacts.

```text
empty or near-empty /proc/<pid>/environ
    -> observability boundary
    -> not proof of absence
    -> not a value mismatch by itself

mapped provider library
    -> provider presence evidence
    -> not selected-device proof by itself

Chromium gpu-process name
    -> internal topology observation
    -> not hardware acceleration proof by itself
```

Claims are accepted at the strongest level supported by correlated evidence, not at the strongest plausible interpretation.

The scoped graphics-policy promotion transaction is closed because all required layers have current authoritative receipts:

```text
source/pre-deploy
live installation
gl-run renderer
VS Code GPU
VS Code CPU
Obsidian GPU
Obsidian CPU
```

Revalidation is trigger-based rather than periodic or blind. The relevant gate is rerun only when its source, runtime dependency, application version, or evidence interpretation changes materially.

## 8. Build boundary

Mesa builds for the glibc world use bionic-native orchestration tools while targeting the glibc ABI through explicit wrappers:

```text
host tools:      bionic Python / uv / Meson / Ninja / shell
compiler target: Termux glibc
runtime target:  glibc Mesa + Turnip/KGSL + Zink
```

This is why the glibc target wrappers live under `modules/gl/overlay/home/gl/toolchain/`, while the Mesa acquisition/build/install lifecycle lives under `packages/mesa-glibc/`.

## 9. Repository lifecycle

```text
baseline
  -> hypothesis
  -> experiment
  -> evidence
  -> result
  -> working conclusion (STATUS.md)
  -> durable decision (docs/decisions/ and closure records)
  -> module / package / test / integrated guide
```

The repository mirrors that lifecycle:

- `experiments/` keeps living investigations and provenance;
- `STATUS.md` records current conclusions and open questions;
- `docs/decisions/` preserves durable choices;
- `docs/refactor/` preserves transaction-level evidence, false-negative corrections, and closure records;
- focused guides in `docs/` integrate current operational knowledge;
- `modules/` owns project-authored system capabilities and target-relative overlays;
- `packages/` owns external payload lifecycle definitions and application-specific launch integration;
- `tools/` owns repository operator and deployment commands;
- `tests/` holds cross-cutting repository and integration validation.
