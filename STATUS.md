# Status

> **State:** active experiment  
> **Updated:** 2026-07-09

## Working conclusions

- **No PRoot runtime.** PRoot is retained as an install/debug-time tool and library source, not as the normal execution environment.
- **The glibc layer is viable for real desktop applications.** Official VS Code and an extracted Obsidian AppImage run as glibc processes while the surrounding desktop stays bionic-native.
- **The core/farm boundary is load-bearing.** Termux glibc and Android-sensitive libraries must remain isolated from the Debian-rootfs-derived library farm; application-local libraries are preserved through `$ORIGIN` where required.
- **Real GPU acceleration works in both ABI worlds.** Native Chromium/Code OSS and glibc Electron applications can use Turnip/Adreno paths. Official VS Code's minimum demonstrated GPU-specific workaround is `--disable-gpu-vsync`.
- **The current glibc Mesa 26.1.x build policy uses `-Dfreedreno-kmds=msm,kgsl`.** In the investigated builds, the working/broken split tracked whether the Turnip ICD retained its libdrm dependency. The exact low-level crash mechanism remains open.
- **Zink OpenGL 4.6 is available for glibc consumers.** The runtime contract is encoded in `modules/gl/overlay/home/gl/env` plus `modules/gl/overlay/home/gl/bin/gl-run`.
- **The desktop session source is recovered and tracked.** `modules/desktop/overlay/home/.local/bin/startxfce-x11` records the current two-world session contract, clean X-server startup, Unix-socket X11, bionic ICD policy, optional Picom path, and clean teardown behavior.
- **A glibc Miniforge/Conda stack is viable.** Conda, Mamba, environment creation, and a compiled NumPy workload were validated.
- **Repository ownership is being refactored explicitly.** Promoted system capabilities now live under `modules/`, external payload lifecycle definitions under `packages/`, experiment-specific harnesses with their experiments, and deployment logic under `tools/`.

## Integrated guides

- `docs/glibc-layer.md` — bootstrap, library boundary, application onboarding, traps, maintenance.
- `docs/gpu.md` — glibc Turnip/Zink build and runtime contract plus diagnostic history.
- `docs/desktop-session.md` — bionic/glibc session boundary and troubleshooting.
- `docs/architecture.md` — current whole-system model.
- `docs/refactor/` — current repository migration source of truth.

## Open questions

- Hardware video decoding remains unresolved across the investigated MediaCodec/Vulkan, VA-API/V4L2, FFmpeg/mpv, and Chromium paths.
- Native Dawn WebGPU exposure remains unresolved: conventional Chromium/Electron GPU acceleration works, but the dedicated WebGPU investigation did not expose Turnip as the desired native WebGPU adapter.
- PyMOL remains the next major end-to-end scientific workload target.
- A proper kgsl+Zink+X11 solution that removes the practical need for the `msm` backend remains worth watching upstream; the current `msm,kgsl` build is the validated local policy.

## Current focus

- [ ] complete the module/package/experiment repository ownership refactor and validate live deployment migration
- [ ] promote the existing `uv-base` definition and shell integration into tracked module ownership
- [ ] run the PyMOL pilot against the current glibc/Conda/Zink stack
- [ ] continue converting session reports into concise canonical experiment records without discarding the original reports
- [ ] add repeatable validation gates where experiments have produced stable runtime contracts
- [ ] formalize application onboarding helpers (`gl-adopt`, `gl-doctor`) only after the current manual contracts remain stable

## Evidence policy

A passing screenshot is not enough by itself. Claims stay at the strongest level directly supported by available evidence. In particular, successful default-WSI presentation and ANGLE-Vulkan rendering are recorded as such; complete end-to-end zero-copy presentation is not claimed without instrumentation that proves it.
