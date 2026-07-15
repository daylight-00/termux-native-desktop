# GPU Acceleration: Turnip + Zink

**Validated target:** Adreno 730, stock Android KGSL, non-root Termux + Termux:X11.

This guide integrates the current GPU runtime contract and the reusable conclusions from the Mesa, VS Code, and Obsidian investigations. Detailed first-hand reports and raw traces remain under `experiments/gpu/`, `experiments/glibc/`, and `docs/refactor/`.

## Working paths

| Consumer | Path | Validation |
|---|---|---|
| VS Code / Electron GPU | ANGLE -> Vulkan -> Turnip -> KGSL | promoted launcher, hostile-policy sanitation, CDP primary GPU = Turnip Adreno 730, provider and KGSL mappings |
| Obsidian / Electron GPU | ANGLE -> Vulkan -> Turnip -> KGSL | receipt-local application profile, hostile-policy sanitation, CDP primary GPU = Turnip Adreno 730, WebGL/WebGL2 enabled, provider and KGSL mappings |
| VS Code / Obsidian CPU | provider-neutral baseline -> `--disable-gpu` | hostile Vulkan/Zink/Gallium inputs absent, isolated application state, renderer topology and bounded survival |
| glibc OpenGL apps | OpenGL -> Zink -> Turnip -> KGSL | promoted `gl-run` self-contained GLX context, OpenGL 4.6 |
| native Chromium / Code OSS | ANGLE Vulkan -> bionic Turnip | hardware-accelerated Chromium/Electron path |

Default Mesa WSI presentation works in the validated glibc stack without forcing `MESA_VK_WSI_DEBUG=sw`. That does **not** by itself prove complete end-to-end zero-copy presentation.

The scoped graphics-policy promotion transaction is closed in `docs/refactor/0091-scoped-graphics-policy-promotion-closure.md`.

## Build contract

The validated glibc Mesa 26.1.x configuration uses:

```text
platforms=x11
vulkan-drivers=freedreno
freedreno-kmds=msm,kgsl
gallium-drivers=zink
egl=enabled
glx=dri
llvm=disabled
```

Host orchestration remains bionic-native; artifacts target Termux glibc through the wrappers in `modules/gl/overlay/home/gl/toolchain/`.

`packages/mesa-glibc/build.sh` uses the XDG-state Mesa workspace and writes versioned candidates under the XDG-state provider store. The canonical active provider is `.../providers/mesa/current`. Legacy `~/gl/build/...` and `~/gl/opt/mesa-*` coordinates are compatibility symlinks retained for absolute-path and operator continuity; they are not canonical mutable ownership.

## Runtime contract

`modules/gl/overlay/home/gl/env` is the graphics-policy-neutral glibc baseline. It clears inherited bionic Vulkan provider variables and inherited `MESA_LOADER_DRIVER_OVERRIDE`/`GALLIUM_DRIVER`. It does not select a glibc provider or OpenGL bridge.

Consumers that deliberately require the managed hardware provider source:

```sh
source "$HOME/gl/policy/vulkan/freedreno.sh"
```

That profile sets both:

```sh
VK_ICD_FILENAMES=$ICD
VK_DRIVER_FILES=$ICD
```

For glibc OpenGL consumers:

```sh
gl-run <program> [args...]
```

`gl-run` requires the explicit Freedreno profile and then adds `MESA_LOADER_DRIVER_OVERRIDE=zink`. Vulkan-native or ANGLE-Vulkan consumers apply the provider profile directly and do not inherit or add the Zink bridge override.

VS Code and Obsidian separate application feature mode from provider and bridge selection:

```text
GL_GPU=1
    -> start from sanitized baseline
    -> source explicit Freedreno profile
    -> enable ANGLE Vulkan flags if the profile is available
    -> no MESA_LOADER_DRIVER_OVERRIDE or GALLIUM_DRIVER

GL_GPU=0
    -> start from sanitized baseline
    -> keep VK_DRIVER_FILES and VK_ICD_FILENAMES absent
    -> keep OpenGL bridge/Gallium overrides absent
    -> pass exact --disable-gpu
```

For the captured VS Code A/B, explicit Freedreno selected Turnip Adreno 730, while implicit discovery selected LVP/llvmpipe under the same `ANGLE_VULKAN`, `GaneshVulkan`, and `vulkan=enabled_on` feature state.

For official VS Code, the minimum experimentally demonstrated GPU-specific workaround was:

```text
--disable-gpu-vsync
```

The promoted Obsidian GPU branch uses the same ANGLE Vulkan feature set and exact managed glibc provider pair. Its canonical receipt also proves application-level isolation through receipt-local `XDG_CONFIG_HOME` and actual `<config>/obsidian` user-data directories.

See:

```text
experiments/gpu/vscode-angle-vulkan/
docs/refactor/0086-current-vscode-gpu-environment-and-primary-identity-pass.md
docs/refactor/0087-current-vscode-cpu-policy-and-survival-pass.md
docs/refactor/0089-current-obsidian-gpu-environment-and-primary-identity-pass.md
docs/refactor/0090-current-obsidian-cpu-policy-and-survival-pass.md
```

## Acceptance evidence model

A mapped provider library is not enough to claim selected GPU identity.

The promoted Electron GPU gates require correlation across:

```text
observable environment and argv
CDP primary device identity
ANGLE/Vulkan feature state
managed provider mapping
KGSL device-node mapping
```

The accepted VS Code and Obsidian GPU receipts both show:

```text
classification=FREEDRENO_TURNIP
selected_provider=FREEDRENO_TURNIP
selected_device_family=Adreno
display_type=ANGLE_VULKAN
skia_backend=GaneshVulkan
hardware provider mapping=PRESENT
/dev/kgsl-3d0=PRESENT
```

CPU acceptance is based on the selected policy and effective mode rather than a universal process-name rule:

```text
GL_GPU=0
no explicit Vulkan provider
no Mesa/Gallium override
exact --disable-gpu
no GPU-enablement flags
renderer viability
bounded main-process survival
```

VS Code retained an internal GPU helper with `--use-gl=disabled`; Obsidian created no GPU helper in its accepted CPU receipt. Both satisfy the same architecture contract.

## Revalidation policy

Do not blind-rerun closed workload gates.

Rerun only when the claim surface changes:

```text
gl/env, provider profile, gl-run, or public launcher changes
Mesa/glibc/Vulkan provider changes
Electron application version changes
user-data authority or feature argv changes
CDP classification/correlation logic changes materially
```

Experiment-only documentation changes do not require a runtime rerun unless they invalidate the interpretation of an existing receipt.

## Mesa 26.1.x present-SIGBUS investigation

The tested kgsl-only + Zink configuration could enumerate the GPU but failed at first X11 presentation with SIGBUS. The successful comparison builds retained a libdrm dependency, while the failing kgsl-only build did not.

The practical local fix is `-Dfreedreno-kmds=msm,kgsl`. The `msm` backend is not the runtime kernel path on this stock Android target; its inclusion produces the validated dependency shape while runtime access remains through KGSL.

The exact low-level path from the missing dependency shape to `BUS_ADRALN` is **not claimed as proven**. The repository preserves that distinction between:

- established build/dependency split;
- validated practical fix;
- still-open crash mechanism.

See `experiments/gpu/mesa-26.1.4-present-sigbus/` and `docs/decisions/0003-mesa-kmds-msm-kgsl.md`.

The two `git bisect` judge scripts are preserved with that experiment under its `recipe/` directory rather than deployed into the live maintenance build tree.

## Diagnostic lessons

1. A bisect runner must reproduce the failing build configuration, not only the failing version.
2. A/B versioned prefixes and a stable symlink make rollback and binary comparison cheap.
3. Compare ELF `NEEDED` entries before assuming a source regression.
4. Do not cargo-cult distant-version patchsets; select changes by mechanism.
5. Keep the X server clean of client GPU overrides.
6. When a policy selects an ICD explicitly, set both Vulkan loader variables together.
7. Clear inherited bionic Vulkan provider **and OpenGL bridge/Gallium** variables at the glibc boundary before applying any glibc graphics composition.
8. `unset VK_*` means implicit discovery, not proof of no Vulkan participation.
9. A session-wide bionic `MESA_LOADER_DRIVER_OVERRIDE=zink` must not be mistaken for a valid glibc-world default; only `gl-run` owns that bridge selection.
10. Electron application user-data authority must be made receipt-local before isolation is claimed; for Obsidian that includes `XDG_CONFIG_HOME` plus the derived `<config>/obsidian` directory.
11. Empty or near-empty child `/proc/<pid>/environ` is an observability boundary, not proof of absence or mismatch.

## Current boundaries

- Conventional GPU acceleration is working for promoted VS Code and Obsidian through ANGLE Vulkan -> Turnip -> Adreno 730.
- Promoted CPU branches are working from a provider-neutral baseline with exact `--disable-gpu` and bounded renderer/main survival.
- Native Dawn WebGPU exposure through the Termux Linux/X11-style stack remains unresolved.
- Hardware video decoding remains unresolved.
- Complete end-to-end zero-copy presentation is not claimed.
- Picom is optional and not required for the core desktop path.
