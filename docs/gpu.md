# GPU Acceleration: Turnip + Zink

**Validated target:** Adreno 730, stock Android KGSL, non-root Termux + Termux:X11.

This guide integrates the current GPU runtime contract and the reusable conclusions from the Mesa/VS Code investigations. Detailed first-hand reports and raw traces remain under `experiments/gpu/`.

## Working paths

| Consumer | Path | Validation |
|---|---|---|
| VS Code / Electron | ANGLE -> Vulkan -> Turnip -> KGSL | real Adreno renderer, stable GPU process |
| glibc OpenGL apps | OpenGL -> Zink -> Turnip -> KGSL | `glxinfo -B`, OpenGL 4.6 |
| native Chromium / Code OSS | ANGLE Vulkan -> bionic Turnip | hardware-accelerated Chromium/Electron path |

Default Mesa WSI presentation works in the validated glibc stack without forcing `MESA_VK_WSI_DEBUG=sw`. That does **not** by itself prove complete end-to-end zero-copy presentation.

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

`packages/mesa-glibc/build.sh` builds into versioned prefixes under `~/gl/opt/` and only expects the stable `~/gl/opt/mesa-glibc` symlink to be promoted after verification. `tools/deploy` preserves the current live compatibility path `~/gl/build/build-mesa.sh` while the package build workflow is further normalized.

## Runtime contract

`modules/gl/overlay/home/gl/env` pins both Vulkan variables to the glibc ICD:

```sh
VK_ICD_FILENAMES=$ICD
VK_DRIVER_FILES=$ICD
```

For glibc OpenGL consumers:

```sh
gl-run <program> [args...]
```

`gl-run` adds `MESA_LOADER_DRIVER_OVERRIDE=zink` after sourcing the glibc environment. Vulkan-native and ANGLE-Vulkan consumers use the ICD pin without the Zink override.

For official VS Code, the minimum experimentally demonstrated GPU-specific workaround was:

```text
--disable-gpu-vsync
```

See `experiments/gpu/vscode-angle-vulkan/`.

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
6. Set both Vulkan ICD environment variables to avoid cross-ABI loader default scanning.

## Current boundaries

- Conventional GPU acceleration is working.
- Native Dawn WebGPU exposure through the Termux Linux/X11-style stack remains unresolved.
- Hardware video decoding remains unresolved.
- Picom is optional and not required for the core desktop path.
