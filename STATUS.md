# Status

> **State:** active promotion validation  
> **Updated:** 2026-07-11

## Working conclusions

- **No PRoot runtime.** PRoot is retained as an install/debug-time tool and library source, not as the normal execution environment.
- **The glibc layer is viable for real desktop applications.** Official VS Code and an extracted Obsidian AppImage run as glibc processes while the surrounding desktop stays bionic-native.
- **The core/farm boundary is load-bearing.** Termux glibc and Android-sensitive libraries must remain isolated from the Debian-rootfs-derived library farm; application-local libraries are preserved through `$ORIGIN` where required.
- **Real GPU acceleration works in both ABI worlds.** Native Chromium/Code OSS and glibc Electron applications can use Turnip/Adreno paths. Official VS Code's minimum demonstrated GPU-specific workaround is `--disable-gpu-vsync`.
- **Graphics policy is consumer-scoped, not a glibc-world global default.** The bionic desktop owns its Turnip ICD and session-wide Zink bridge. `~/gl/env` clears the inherited Vulkan pair plus `MESA_LOADER_DRIVER_OVERRIDE`/`GALLIUM_DRIVER` before any glibc consumer composes its own policy.
- **The promoted source separates sanitation, provider selection, bridge selection, and application feature mode.** Consumers that require hardware Vulkan source `~/gl/policy/vulkan/freedreno.sh`; only `gl-run` adds Zink; VS Code and Obsidian own their `GL_GPU` branches.
- **The expanded current-head pre-deploy and live installation receipts passed.** Source syntax, repository policy regression, deploy smoke/dry-run, all managed live targets, the four-variable bionic graphics-policy sanitation set, explicit Freedreno selection, bridge neutrality, and profile-variable privacy all passed with zero failures at `5ed76ec9c7409a141da02a28b5297b8b71965467`.
- **The earlier promoted `gl-run` and VS Code GPU receipts passed at their captured heads.** `gl-run` reported `zink Vulkan 1.4(Turnip Adreno (TM) 730)` and the public VS Code launcher reported `ANGLE_VULKAN`, `GaneshVulkan`, `FREEDRENO_TURNIP` / `Adreno`, the managed provider, and `/dev/kgsl-3d0`.
- **Those prior-head workload receipts remain valid evidence but current-head workload regressions remain open.** The shared baseline changed after those captures, so final promotion requires actual-renderer and primary-device receipts on the corrected source state.
- **Mutable checkout symlinks are also an activation path.** Pulling the current correction immediately changed `~/gl/env`; no new leaf or `tools/deploy` run was required. The general atomic-activation problem remains open.
- **The current glibc Mesa 26.1.x build policy uses `-Dfreedreno-kmds=msm,kgsl`.** In the investigated builds, the working/broken split tracked whether the Turnip ICD retained its libdrm dependency. The exact low-level crash mechanism remains open.
- **The desktop session source is recovered and tracked.** `modules/desktop/overlay/home/.local/bin/startxfce-x11` records the current two-world session contract, clean X-server startup, Unix-socket X11, bionic ICD/Zink policy, optional Picom path, and clean teardown behavior.
- **A glibc Miniforge/Conda stack is viable.** Conda, Mamba, environment creation, and a compiled NumPy workload were validated.
- **Repository ownership is being refactored explicitly.** Promoted system capabilities live under `modules/`, external payload lifecycle definitions under `packages/`, experiment-specific harnesses with their experiments, and deployment logic under `tools/`.

## Integrated guides

- `docs/glibc-layer.md` — bootstrap, library boundary, application onboarding, graphics-policy boundary, traps, maintenance.
- `docs/gpu.md` — glibc Turnip/Zink build and runtime contract plus provider/bridge evidence.
- `docs/desktop-session.md` — bionic/glibc session boundary and troubleshooting.
- `docs/architecture.md` — current whole-system model.
- `docs/refactor/0075-vscode-primary-device-receipt-pass-and-policy-ownership-audit.md` — final VS Code selected-device receipt and ownership audit.
- `docs/refactor/0076-scoped-vulkan-policy-promotion-candidate.md` — promoted source transaction and validation plan.
- `docs/refactor/0077-predeploy-pass-and-symlink-activation-gap.md` — real-device pre-deploy receipt and mutable-symlink activation finding.
- `docs/refactor/0078-live-installation-pass-and-promoted-workload-gates.md` — live installation closure and promoted workload sequence.
- `docs/refactor/0079-promoted-gl-run-validator-prerequisite-and-parser-false-negatives.md` — invalid first renderer invocation and validator correction.
- `docs/refactor/0080-promoted-gl-run-zink-turnip-renderer-pass.md` — prior-head promoted GLX/Zink/Turnip actual-renderer receipt.
- `docs/refactor/0081-promoted-vscode-turnip-primary-identity-pass-and-cpu-policy-gate.md` — prior-head promoted VS Code GPU identity and CPU gate contract.
- `docs/refactor/0082-bionic-zink-policy-leak-and-glibc-boundary-correction.md` — inherited bridge-policy defect, correction, and current-head regression order.
- `docs/refactor/0083-expanded-graphics-policy-predeploy-and-live-installation-pass.md` — current-head source/live environment closure after the sanitation correction.
- `docs/refactor/` — full repository migration source of truth.

## Open questions

- Current-head `gl-run`, VS Code GPU, VS Code CPU, and Obsidian GPU/CPU workload gates remain to close the scoped graphics-policy transaction.
- The current source-linked deployment model lacks an atomic activation boundary for multi-file transactions that modify existing leaves and introduce new required leaves.
- Ownership of other inherited Mesa/session variables such as `vblank_mode` has not been changed; each requires separate evidence.
- Hardware video decoding remains unresolved across the investigated MediaCodec/Vulkan, VA-API/V4L2, FFmpeg/mpv, and Chromium paths.
- Native Dawn WebGPU exposure remains unresolved: conventional Chromium/Electron GPU acceleration works, but the dedicated WebGPU investigation did not expose Turnip as the desired native WebGPU adapter.
- PyMOL remains the next major end-to-end scientific workload target.
- A proper kgsl+Zink+X11 solution that removes the practical need for the `msm` backend remains worth watching upstream; the current `msm,kgsl` build is the validated local policy.

## Current focus

- [x] pass the expanded current-head no-mutation pre-deploy gate
- [x] pass the expanded live graphics-policy installation receipt
- [ ] rerun the promoted `gl-run` Zink/Turnip renderer gate
- [ ] rerun promoted VS Code GPU primary identity
- [ ] validate promoted VS Code CPU policy/argv behavior
- [ ] validate promoted Obsidian GPU and CPU paths
- [ ] close the scoped graphics-policy promotion transaction
- [ ] evaluate an atomic activation model for future multi-file runtime migrations
- [ ] complete the remaining module/package/experiment ownership refactor and validate live deployment migration
- [ ] run the PyMOL pilot against the current glibc/Conda/Zink stack
- [ ] continue converting session reports into concise canonical experiment records without discarding the original reports
- [ ] add repeatable validation gates where experiments have produced stable runtime contracts
- [ ] formalize application onboarding helpers (`gl-adopt`, `gl-doctor`) only after the current manual contracts remain stable

## Evidence policy

A passing screenshot is not enough by itself. Claims stay at the strongest level directly supported by available evidence. In particular, successful default-WSI presentation and ANGLE-Vulkan rendering are recorded as such; complete end-to-end zero-copy presentation is not claimed without instrumentation that proves it.
