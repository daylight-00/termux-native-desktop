# Mesa 26.0.6 for the glibc runtime

**Status:** passed; retained as a historical control  
**Dates:** 2026-07-02 to 2026-07-03  
**Provenance:** first-hand build report + later cross-experiment validation records

## Question

Can Mesa Turnip be built for the Termux glibc runtime while build orchestration remains bionic-native, and can the resulting driver expose the real Adreno 730 through KGSL?

## Build model

```text
host tools:      bionic Python / Meson / Ninja / shell
compiler target: Termux glibc
GPU driver:      Turnip
kernel path:     KGSL
hardware:        Adreno 730
```

The build report records the key correction from a non-working configuration to `-Dfreedreno-kmds=kgsl` and successful real-device enumeration with Mesa 26.0.6 / Turnip.

## Evidence boundary

The preserved `report.md` directly proves build success, driver initialization, and physical-device enumeration. It explicitly notes that its surviving transcript does **not** preserve a final vanilla-present `vkcube` success for that exact build.

Later VS Code GPU-enable­ment records used the 26.0.6 stack as a control and preserve successful Vulkan WSI/swapchain probes and ANGLE-related comparison tests. Those later records are additional evidence, not retroactively part of the original build transcript.

## Later significance

The 26.0.6 driver remained useful as the known-good comparison during the Mesa 26.1.4 present-SIGBUS investigation. Later dependency inspection showed a libdrm dependency shape that differed from the failing kgsl-only 26.1.x build.

## Decision

Superseded as the main glibc driver by the later 26.1.x configuration, but retained as an important control and as the origin of the reusable bionic-host/glibc-target build model.

See [`report.md`](report.md) and the later `../vscode-angle-vulkan/` and `../mesa-26.1.4-present-sigbus/` records.
