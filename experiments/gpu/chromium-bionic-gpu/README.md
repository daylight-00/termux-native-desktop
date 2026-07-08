# Native Chromium / Code OSS GPU acceleration

**Status:** passed for conventional GPU acceleration  
**Date:** 2026-07-01 workstream  
**Provenance:** first-hand session report (`report.md`)

## Question

Can native bionic Chromium and Code OSS use the real Adreno GPU through an explicit Vulkan path under Termux:X11, without making Zink a desktop-wide override?

## Result

Yes. The successful application path is:

```text
Chromium / Code OSS
  -> ANGLE Vulkan
  -> Mesa Turnip
  -> KGSL
  -> Adreno 730
  -> Termux:X11
```

The report records hardware-accelerated Chromium compositor/raster/WebGL state, Vulkan enablement, ANGLE Vulkan selection, Turnip renderer identity, and zero GPU-process crash count in the tested configuration.

## Important boundary

A global `MESA_LOADER_DRIVER_OVERRIDE=zink` policy destabilized the XFCE desktop/session. The resulting project policy is:

- explicitly select the Turnip ICD for native Vulkan consumers;
- request ANGLE Vulkan for Chromium/Electron consumers;
- do not force Zink globally across the desktop.

The dedicated WebGPU question is separate. A `chrome://gpu` feature label is not treated as proof of a native Dawn WebGPU adapter; see `../webgpu/` for the targeted adapter investigation.

## Decision

Use explicit per-application GPU policy rather than a desktop-wide translation override.

See [`report.md`](report.md).
