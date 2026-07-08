# Architecture

This document describes the current system model. It is intentionally a model of the working architecture, not a claim that every subsystem is finished.

## 1. System boundary

The project keeps Android and Termux native. It adds a glibc application world beside the normal bionic world rather than trying to turn the entire Termux environment into a conventional Linux distribution.

```text
Android kernel + device hardware
        |
        +-- KGSL / Adreno 730
        |
        +-- Termux native user space (bionic)
                |
                +-- Termux:X11
                +-- XFCE/session services
                +-- native Chromium / Code OSS
                +-- bionic Mesa / Turnip
                |
                +-- glibc application world
                        |
                        +-- Termux glibc core
                        +-- Debian rootfs library farm
                        +-- application-local libraries
                        +-- glibc Mesa / Turnip
                        +-- VS Code, Obsidian, Conda, ...
```

The desktop is therefore a mixed system by design, but individual process ABI boundaries are kept explicit.

## 2. Two execution worlds

### Bionic world

The Termux shell, X server integration, desktop services, and native packages run against Android bionic. Native GPU consumers use the bionic Vulkan/Mesa stack.

### glibc world

Conventional Linux applications run as glibc processes. Their launcher contract selects the glibc runtime, clears incompatible inherited preload state where required, and pins the glibc GPU stack for applications that need it.

A central invariant is:

> Do not export glibc library search paths globally into the bionic shell.

The project moved away from global or broad `LD_LIBRARY_PATH` injection. The stable layer uses ELF interpreter/RPATH handling, glibc loader configuration, and controlled launchers instead.

## 3. glibc library model

The current conceptual resolution model is:

```text
application-local libraries (`$ORIGIN`)
            +
Termux glibc core / Android-sensitive libraries
            +
filtered Debian rootfs library farm
```

The exact lookup order is load-bearing. The Termux glibc core must win for the libc family and for Android-sensitive pieces such as the X11/xcb path used by the current Unix-socket model. The Debian rootfs is valuable for its broad library catalog but must not inject a second glibc implementation into the process.

The rootfs is passive at runtime:

```text
apt / package metadata
        -> install into rootfs
        -> expose allowed shared libraries through farm
        -> refresh glibc loader cache
        -> run application natively outside PRoot
```

## 4. GPU model

There are two GPU stacks because there are two ABI worlds.

```text
bionic application
  -> ANGLE Vulkan or Vulkan consumer
  -> bionic Vulkan loader / Mesa Turnip
  -> KGSL
  -> Adreno 730


glibc application
  -> ANGLE Vulkan, Vulkan, or Zink consumer
  -> glibc Vulkan loader / glibc Mesa Turnip
  -> KGSL
  -> Adreno 730
```

The session environment can expose the bionic ICD for native desktop applications. glibc launchers re-pin the glibc ICD, so this duality is intentional rather than accidental inheritance.

Current policy also avoids a desktop-wide `MESA_LOADER_DRIVER_OVERRIDE=zink`. Native Chromium/Code OSS experiments showed that explicit ANGLE Vulkan is a better fit for Vulkan-aware Electron/Chromium consumers, while global Zink forcing destabilized unrelated desktop behavior.

## 5. Mesa build boundary

Mesa builds for the glibc world use bionic-native build orchestration tools while targeting the glibc ABI through explicit wrappers. The important separation is:

```text
host tools:      bionic Python / Meson / Ninja / shell
compiler target: Termux glibc
runtime target:  glibc Mesa + Turnip/KGSL
```

This is why `setup/glibc/toolchain/` and `setup/mesa/` belong in the same system repository even though they represent different subsystems.

For the investigated Mesa 26.1.x configuration, the current build policy includes both `msm` and `kgsl` KMD selections. The `msm` backend is not the runtime kernel path on this stock Android device; it is retained because the resulting dependency shape preserved the working X11 present path in the investigated build. See `docs/decisions/0003-mesa-kmds-msm-kgsl.md`.

## 6. Session boundary

The desktop session belongs to the bionic world and should start the X server without leaking client-specific GPU overrides into it. Desktop applications may then choose their own GPU path through process-local launch policy.

The session experiment also established an intentional split in runtime directories:

- desktop/session services use the native Termux runtime location;
- glibc applications use a separate glibc runtime directory.

The canonical session launcher source is currently missing from the tracked GitHub tree and must be recovered from the on-device source rather than reconstructed from the report.

## 7. Repository architecture

The repository mirrors the engineering lifecycle rather than the package graph:

```text
experiments/
    living investigation units

STATUS.md
    current working conclusions

docs/decisions/
    durable choices

docs/
    integrated explanations

setup/ + scripts/
    promoted artifacts used by the live device
```

The promotion path is:

```text
baseline
  -> hypothesis
  -> experiment
  -> evidence
  -> result
  -> decision
  -> promoted documentation or runtime artifact
```

An experiment can remain useful after its implementation is superseded. Its `report.md` preserves the historical path; its `README.md` records the current interpretation.
