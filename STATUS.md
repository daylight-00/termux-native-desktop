# Status

> **State:** active experiment  
> **Updated:** 2026-07-08

## Working conclusions

- **No PRoot runtime.** PRoot is retained as an install/debug-time tool and library source, but not as the normal execution environment. The decision originated from observed VS Code I/O sluggishness in the PRoot path.
- **The glibc layer is viable for real desktop applications.** Official Microsoft VS Code and an extracted Obsidian AppImage have been run as native glibc processes while the surrounding Termux desktop remains bionic-native.
- **The library boundary matters.** The working model keeps the Termux glibc core and Android-sensitive libraries ahead of a Debian-rootfs-derived library farm, with application-local libraries preserved through `$ORIGIN` where required.
- **Real GPU acceleration works in both execution worlds.** Native Chromium/Code OSS and glibc Electron applications can use ANGLE Vulkan on Turnip/Adreno. For official VS Code, the minimum experimentally demonstrated GPU-specific workaround was `--disable-gpu-vsync`.
- **The current glibc Mesa 26.1.x build policy uses `-Dfreedreno-kmds=msm,kgsl`.** In the investigated configuration, kgsl-only 26.1.x dropped the libdrm dependency and the X11 present path failed with SIGBUS; retaining `msm` restored the working dependency shape. The exact low-level crash mechanism remains intentionally unclaimed.
- **Zink is available for glibc OpenGL consumers.** OpenGL 4.6 has been observed through the Zink -> Turnip path.
- **A glibc Miniforge/Conda stack is viable.** Conda and Mamba ran, environments were created, and a compiled NumPy workload executed successfully after Termux-specific runtime adaptation.

## Open questions

- Hardware video decoding remains unresolved across the investigated MediaCodec/Vulkan, VA-API/V4L2, FFmpeg/mpv, and Chromium paths.
- Native Dawn WebGPU exposure remains unresolved: conventional Chromium/Electron GPU acceleration works, but the dedicated WebGPU investigation did not expose Turnip as a native WebGPU adapter.
- PyMOL is the next major end-to-end scientific workload target.
- The hardened `startxfce-x11` launcher described by the experiment record is not currently tracked in the GitHub tree at `setup/session/startxfce-x11`; the on-device source must be recovered rather than reconstructed from memory.

## Current focus

- [ ] recover and commit the on-device session launcher source without changing its live path contract
- [ ] run the PyMOL pilot against the current glibc/Conda/GPU stack
- [ ] continue converting session reports into concise canonical experiment records without discarding the original reports
- [ ] add repeatable validation gates where an experiment has produced a stable runtime contract

## Evidence policy

A passing application screenshot is not enough by itself. Claims are kept at the strongest level directly supported by the available evidence. For example, successful ANGLE Vulkan rendering is recorded as such; complete end-to-end zero-copy presentation is not claimed without instrumentation proving it.
