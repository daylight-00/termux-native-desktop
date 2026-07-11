# Status

> **State:** active architecture/refactor after graphics-policy closure  
> **Updated:** 2026-07-11

## Working conclusions

- **No PRoot runtime.** PRoot is retained as an install/debug-time tool and library source, not as the normal execution environment.
- **The glibc layer is viable for real desktop applications.** Official VS Code and an extracted Obsidian AppImage run as glibc processes while the surrounding desktop stays bionic-native.
- **The core/farm boundary is load-bearing.** Termux glibc and Android-sensitive libraries must remain isolated from the Debian-rootfs-derived library farm; application-local libraries are preserved through `$ORIGIN` where required.
- **Real GPU acceleration works in both ABI worlds.** Native Chromium/Code OSS and glibc Electron applications can use Turnip/Adreno paths. Official VS Code's minimum demonstrated GPU-specific workaround is `--disable-gpu-vsync`.
- **Graphics policy is consumer-scoped, not a glibc-world global default.** The bionic desktop owns its Turnip ICD and session-wide Zink bridge. `~/gl/env` clears the inherited Vulkan pair plus `MESA_LOADER_DRIVER_OVERRIDE`/`GALLIUM_DRIVER` before any glibc consumer composes its own policy.
- **The promoted source separates sanitation, provider selection, bridge selection, application feature mode, and validation-state authority.** Consumers that require hardware Vulkan source `~/gl/policy/vulkan/freedreno.sh`; only `gl-run` adds Zink; VS Code and Obsidian own their `GL_GPU` branches; validation uses receipt-local application state.
- **The scoped graphics-policy promotion transaction is closed.** Expanded source/live installation, current `gl-run`, VS Code GPU/CPU, and Obsidian GPU/CPU all have authoritative zero-failure receipts. The accepted invariant set and revalidation triggers are recorded in `docs/refactor/0091-scoped-graphics-policy-promotion-closure.md`.
- **The promoted runtime source remained unchanged during workload closure.** From the expanded source/live receipt at `5ed76ec9c7409a141da02a28b5297b8b71965467` through closure, later changes were confined to `STATUS.md`, `docs/refactor/`, and experiment validators; no `modules/`, `packages/`, `tests/`, or `tools/` runtime source changed.
- **The expanded pre-deploy and live installation receipts passed.** Source syntax, repository policy regression, deploy smoke/dry-run, all managed live targets, the four-variable bionic graphics-policy sanitation set, explicit Freedreno selection, bridge neutrality, and profile-variable privacy passed with zero failures at `5ed76ec9c7409a141da02a28b5297b8b71965467`.
- **The current `gl-run` path is validated end to end.** At `147c7e2fc9b414a6be5561589293c01820d5f7f6`, hostile inherited llvmpipe bridge/Gallium policy was removed and the promoted launcher produced a glibc GLX/OpenGL 4.6 context reporting `zink Vulkan 1.4(Turnip Adreno (TM) 730)` with zero failures.
- **The current promoted VS Code GPU gate is closed.** At `bea4062df2e132639ea08c8bb94abc8235fb0a96`, all 44 environment, argv, topology, CDP identity, feature-mode, provider-map, and KGSL correlation gates passed. CDP selected Turnip/Adreno 730 under ANGLE Vulkan and GaneshVulkan.
- **The current promoted VS Code CPU gate is closed.** At `0c6a85235ee9b759addc9963a16060c806277fe3`, all 18 sanitation, argv, topology, survival, and diagnostic gates passed. The main process contained exact `--disable-gpu`; the retained internal GPU helper used `--use-gl=disabled`; the renderer used `--disable-gpu-compositing`.
- **The corrected promoted Obsidian GPU gate is closed.** At `3384bf136f3f35f7ab1d86b2005c2e7559d7e298`, all 48 environment, isolated application-profile, argv, topology, survival, CDP identity, feature-mode, provider-map, and KGSL gates passed. Main, zygote, GPU, utility, and renderer showed the exact managed GPU contract.
- **The promoted Obsidian CPU gate is closed.** At `5ab13fd6c2af5843abf7bbff3a8a26f46a8e84b5`, all 21 sanitation, isolated profile, argv, topology, survival, and diagnostic gates passed. No GPU process was observed, the renderer used `--disable-gpu-compositing`, and main/zygote/renderer remained viable for 20 seconds.
- **Application user-data authority is part of the evidence contract.** VS Code uses isolated user-data/extensions paths. Obsidian requires a receipt-local `XDG_CONFIG_HOME` plus the actual derived `<config>/obsidian` directory; `$HOME/.config/obsidian` is excluded from canonical receipts.
- **A Chromium process named `gpu-process` is not by itself an acceleration claim or CPU failure.** Acceptance is based on selected policy, effective argv/feature mode, renderer viability, and correlated provider/device evidence.
- **Child `/proc/environ` is an observability boundary.** Empty or near-empty child environment views are not interpreted as proof of absence or as a mismatch. Exact values are required only where meaningfully observable.
- **The recovered glibc substrate remains 2.42 and held.** The hold remains incident containment rather than a permanent lifecycle design.
- **Mutable checkout symlinks are also an activation path.** Pulling source changes can immediately update existing live leaves such as `~/gl/env`; the general atomic-activation problem remains open.
- **The current glibc Mesa 26.1.x build policy uses `-Dfreedreno-kmds=msm,kgsl`.** The working/broken split tracked whether the Turnip ICD retained its libdrm dependency; the exact low-level crash mechanism remains open.
- **The desktop session source is recovered and tracked.** `modules/desktop/overlay/home/.local/bin/startxfce-x11` records the two-world session contract, clean X-server startup, Unix-socket X11, bionic ICD/Zink policy, optional Picom path, and clean teardown behavior.
- **A glibc Miniforge/Conda stack is viable.** Conda, Mamba, environment creation, and a compiled NumPy workload were validated.
- **Repository ownership is being refactored explicitly.** Promoted system capabilities live under `modules/`, external payload lifecycle definitions under `packages/`, experiment-specific harnesses with their experiments, and deployment logic under `tools/`.

## Integrated guides

- `docs/glibc-layer.md` — bootstrap, library boundary, application onboarding, accepted graphics-policy compositions, evidence interpretation, and traps.
- `docs/gpu.md` — glibc Turnip/Zink build and runtime contract, Electron GPU/CPU evidence model, and revalidation policy.
- `docs/desktop-session.md` — bionic/glibc session boundary and troubleshooting.
- `docs/architecture.md` — current whole-system model, graphics-policy closure, application-state authority, and evidence lifecycle.
- `docs/refactor/0083-expanded-graphics-policy-predeploy-and-live-installation-pass.md` — current promoted source/live installation receipt.
- `docs/refactor/0084-current-head-gl-run-regression-pass-and-strengthened-vscode-gpu-gate.md` — hostile-policy `gl-run` renderer PASS.
- `docs/refactor/0085-vscode-child-proc-environ-observability-false-negative.md` — corrected child environment observability model.
- `docs/refactor/0086-current-vscode-gpu-environment-and-primary-identity-pass.md` — canonical VS Code GPU receipt.
- `docs/refactor/0087-current-vscode-cpu-policy-and-survival-pass.md` — canonical VS Code CPU receipt.
- `docs/refactor/0088-obsidian-user-data-authority-and-cdp-path-false-negative.md` — invalid first Obsidian CDP path model and correction.
- `docs/refactor/0089-current-obsidian-gpu-environment-and-primary-identity-pass.md` — canonical Obsidian GPU receipt.
- `docs/refactor/0090-current-obsidian-cpu-policy-and-survival-pass.md` — canonical Obsidian CPU receipt.
- `docs/refactor/0091-scoped-graphics-policy-promotion-closure.md` — final accepted invariant set, evidence matrix, claim boundaries, and trigger-based revalidation policy.
- `docs/refactor/` — full repository migration source of truth.

## Open questions

- The current source-linked deployment model lacks an atomic activation boundary for multi-file transactions that modify existing leaves and introduce new required leaves.
- The recovered `glibc 2.42` hold needs a deliberate upgrade/recovery lifecycle rather than indefinite incident containment.
- Ownership of other inherited Mesa/session variables such as `vblank_mode` has not been changed; each requires separate evidence.
- Hardware video decoding remains unresolved across the investigated MediaCodec/Vulkan, VA-API/V4L2, FFmpeg/mpv, and Chromium paths.
- Native Dawn WebGPU exposure remains unresolved: conventional Chromium/Electron GPU acceleration works, but the dedicated WebGPU investigation did not expose Turnip as the desired native WebGPU adapter.
- Complete end-to-end zero-copy presentation is not proven.
- Normal-profile long-duration VS Code and Obsidian behavior with user extensions, vaults, and plugins is outside the promotion receipts.
- PyMOL remains the next major end-to-end scientific workload target.
- A proper kgsl+Zink+X11 solution that removes the practical need for the `msm` backend remains worth watching upstream; the current `msm,kgsl` build is the validated local policy.

## Current focus

- [x] pass the expanded current-head no-mutation pre-deploy gate
- [x] pass the expanded live graphics-policy installation receipt
- [x] pass the promoted `gl-run` Zink/Turnip renderer gate
- [x] pass the promoted VS Code GPU environment/identity gate
- [x] pass the promoted VS Code CPU policy/survival gate
- [x] pass the corrected promoted Obsidian GPU environment/identity gate
- [x] pass the promoted Obsidian CPU policy/survival gate
- [x] close the scoped graphics-policy promotion transaction
- [ ] evaluate and design an atomic activation model for future multi-file runtime migrations
- [ ] complete the remaining module/package/experiment ownership refactor and validate live deployment migration
- [ ] define a deliberate glibc upgrade/recovery lifecycle beyond the current package hold
- [ ] run the PyMOL pilot against the current glibc/Conda/Zink stack
- [ ] continue converting session reports into concise canonical experiment records without discarding original reports
- [ ] add repeatable validation gates where experiments have produced stable runtime contracts
- [ ] formalize application onboarding helpers (`gl-adopt`, `gl-doctor`) only after the current manual contracts remain stable

## Evidence policy

A passing screenshot is not enough by itself. Claims stay at the strongest level directly supported by correlated evidence. Empty or near-empty child `/proc/<pid>/environ` output is an observability boundary, not a graphics-policy value. A mapped provider library is not selected-device proof without primary identity correlation. Application-derived user-data paths must be made receipt-local through the application's actual configuration authority before isolation is claimed. Successful default-WSI presentation and ANGLE-Vulkan rendering do not prove complete end-to-end zero-copy presentation. Closed gates are rerun only when their source/runtime/application/evidence claim surface changes.
