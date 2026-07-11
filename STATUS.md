# Status

> **State:** active promotion validation  
> **Updated:** 2026-07-11

## Working conclusions

- **No PRoot runtime.** PRoot is retained as an install/debug-time tool and library source, not as the normal execution environment.
- **The glibc layer is viable for real desktop applications.** Official VS Code and an extracted Obsidian AppImage run as glibc processes while the surrounding desktop stays bionic-native.
- **The core/farm boundary is load-bearing.** Termux glibc and Android-sensitive libraries must remain isolated from the Debian-rootfs-derived library farm; application-local libraries are preserved through `$ORIGIN` where required.
- **Real GPU acceleration works in both ABI worlds.** Native Chromium/Code OSS and glibc Electron applications can use Turnip/Adreno paths. Official VS Code's minimum demonstrated GPU-specific workaround is `--disable-gpu-vsync`.
- **Vulkan provider policy is consumer-scoped, not a glibc-world global default.** In the captured VS Code same-feature-mode A/B, explicit Freedreno selected Turnip/Adreno 730 and KGSL, while implicit discovery selected LVP/llvmpipe. Both controls retained ANGLE Vulkan, GaneshVulkan, and `vulkan=enabled_on`.
- **The promoted source now separates ABI sanitation from provider selection.** `~/gl/env` clears inherited bionic Vulkan variables; consumers that deliberately require the managed hardware provider source `~/gl/policy/vulkan/freedreno.sh`.
- **Application feature mode is separate from provider policy.** VS Code and Obsidian apply the explicit profile only in their GPU branches; CPU branches and the Obsidian CLI retain a provider-neutral glibc baseline. `gl-run` composes the explicit provider with Zink.
- **The real-device scoped-policy pre-deploy receipt passed.** Syntax, repository policy tests, deploy smoke, live dry-run, and source-contract checks all passed with zero failures at `e86dfa1516a6c978c31a81ebb849153c4232aa61`.
- **Mutable checkout symlinks are also an activation path.** Existing live leaves exposed new checkout contents immediately after `git pull`, before `tools/deploy` could install the newly introduced profile leaf. The current transaction therefore exposed a bounded activation gap: Electron launchers fell back to CPU and `gl-run` failed closed until the profile link is installed.
- **The current glibc Mesa 26.1.x build policy uses `-Dfreedreno-kmds=msm,kgsl`.** In the investigated builds, the working/broken split tracked whether the Turnip ICD retained its libdrm dependency. The exact low-level crash mechanism remains open.
- **Zink OpenGL 4.6 is available for glibc consumers.** The runtime contract is encoded in the provider-neutral baseline, the explicit Freedreno profile, and `modules/gl/overlay/home/gl/bin/gl-run`.
- **The desktop session source is recovered and tracked.** `modules/desktop/overlay/home/.local/bin/startxfce-x11` records the current two-world session contract, clean X-server startup, Unix-socket X11, bionic ICD policy, optional Picom path, and clean teardown behavior.
- **A glibc Miniforge/Conda stack is viable.** Conda, Mamba, environment creation, and a compiled NumPy workload were validated.
- **Repository ownership is being refactored explicitly.** Promoted system capabilities live under `modules/`, external payload lifecycle definitions under `packages/`, experiment-specific harnesses with their experiments, and deployment logic under `tools/`.

## Integrated guides

- `docs/glibc-layer.md` — bootstrap, library boundary, application onboarding, traps, maintenance.
- `docs/gpu.md` — glibc Turnip/Zink build and runtime contract plus provider-policy evidence.
- `docs/desktop-session.md` — bionic/glibc session boundary and troubleshooting.
- `docs/architecture.md` — current whole-system model.
- `docs/refactor/0075-vscode-primary-device-receipt-pass-and-policy-ownership-audit.md` — final VS Code selected-device receipt and ownership audit.
- `docs/refactor/0076-scoped-vulkan-policy-promotion-candidate.md` — promoted source transaction and validation plan.
- `docs/refactor/0077-predeploy-pass-and-symlink-activation-gap.md` — real-device pre-deploy receipt and mutable-symlink activation finding.
- `docs/refactor/` — full repository migration source of truth.

## Open questions

- The scoped Vulkan policy source transaction has passed pre-deploy validation but has not yet completed live profile-link installation or post-deploy environment and workload gates.
- The current source-linked deployment model lacks an atomic activation boundary for multi-file transactions that modify existing leaves and introduce new required leaves.
- Hardware video decoding remains unresolved across the investigated MediaCodec/Vulkan, VA-API/V4L2, FFmpeg/mpv, and Chromium paths.
- Native Dawn WebGPU exposure remains unresolved: conventional Chromium/Electron GPU acceleration works, but the dedicated WebGPU investigation did not expose Turnip as the desired native WebGPU adapter.
- PyMOL remains the next major end-to-end scientific workload target.
- A proper kgsl+Zink+X11 solution that removes the practical need for the `msm` backend remains worth watching upstream; the current `msm,kgsl` build is the validated local policy.

## Current focus

- [x] pass the no-mutation scoped Vulkan policy pre-deploy gate on the real Termux checkout
- [ ] install the missing managed Freedreno profile leaf through `tools/deploy`
- [ ] pass the no-GUI live installation receipt
- [ ] validate live `gl-run`, VS Code GPU/CPU, and Obsidian GPU/CPU paths
- [ ] close the scoped Vulkan promotion transaction
- [ ] evaluate an atomic activation model for future multi-file runtime migrations
- [ ] complete the remaining module/package/experiment ownership refactor and validate live deployment migration
- [ ] run the PyMOL pilot against the current glibc/Conda/Zink stack
- [ ] continue converting session reports into concise canonical experiment records without discarding the original reports
- [ ] add repeatable validation gates where experiments have produced stable runtime contracts
- [ ] formalize application onboarding helpers (`gl-adopt`, `gl-doctor`) only after the current manual contracts remain stable

## Evidence policy

A passing screenshot is not enough by itself. Claims stay at the strongest level directly supported by available evidence. In particular, successful default-WSI presentation and ANGLE-Vulkan rendering are recorded as such; complete end-to-end zero-copy presentation is not claimed without instrumentation that proves it.
