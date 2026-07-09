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

Every glibc launcher sources `modules/gl/overlay/home/gl/env` through the live `~/gl/env` link. That environment:

- uses a separate `$PREFIX/tmp/gl-runtime` runtime directory;
- pins both `VK_ICD_FILENAMES` and `VK_DRIVER_FILES` to the glibc Mesa ICD;
- points TLS consumers at the Termux certificate bundle;
- does not set `LD_LIBRARY_PATH`;
- leaves the bionic session isolated from glibc library lookup state.

OpenGL consumers add `MESA_LOADER_DRIVER_OVERRIDE=zink` through `gl-run`; Vulkan-native and ANGLE-Vulkan consumers do not need that override.

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


glibc app
  -> ANGLE Vulkan / Vulkan / Zink consumer
  -> glibc Vulkan loader + glibc Mesa Turnip
  -> KGSL
  -> Adreno 730
```

The current session-wide bionic GL policy and the glibc application policy are deliberately separate. The session's bionic ICD and Zink override do not define the glibc runtime; `~/gl/env` re-pins the glibc ICD, and `gl-run` adds Zink only for glibc OpenGL consumers.

For the investigated Mesa 26.1.x configuration, the validated build policy uses `-Dfreedreno-kmds=msm,kgsl`. The working/broken split tracked the presence of the libdrm dependency in the tested builds; the exact low-level crash mechanism remains open.

See `docs/gpu.md` and `docs/decisions/0003-mesa-kmds-msm-kgsl.md`.

## 6. Build boundary

Mesa builds for the glibc world use bionic-native orchestration tools while targeting the glibc ABI through explicit wrappers:

```text
host tools:      bionic Python / uv / Meson / Ninja / shell
compiler target: Termux glibc
runtime target:  glibc Mesa + Turnip/KGSL + Zink
```

This is why the glibc target wrappers live under `modules/gl/overlay/home/gl/toolchain/`, while the Mesa acquisition/build/install lifecycle lives under `packages/mesa-glibc/`.

## 7. Repository lifecycle

```text
baseline
  -> hypothesis
  -> experiment
  -> evidence
  -> result
  -> working conclusion (STATUS.md)
  -> durable decision (docs/decisions/)
  -> module / package / test / integrated guide
```

The repository mirrors that lifecycle:

- `experiments/` keeps living investigations and provenance;
- `STATUS.md` records current conclusions and open questions;
- `docs/decisions/` preserves durable choices;
- focused guides in `docs/` integrate current operational knowledge;
- `modules/` owns project-authored system capabilities and target-relative overlays;
- `packages/` owns external payload lifecycle definitions and application-specific launch integration;
- `tools/` owns repository operator and deployment commands;
- `tests/` holds cross-cutting repository and integration validation.
