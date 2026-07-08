# Chromium / Code OSS native WebGPU adapter investigation

**Status:** desired native adapter path unsuccessful  
**Provenance:** first-hand session report (`report.md`)

## Question

After normal Chromium/Electron acceleration already works through ANGLE Vulkan and Turnip, can Dawn expose the same Adreno 730 / Turnip device as a native WebGPU adapter?

## Baseline

Conventional GPU acceleration was already proven:

```text
Chromium / Electron compositor
  -> ANGLE Vulkan
  -> Turnip
  -> KGSL
  -> Adreno 730
```

WebGPU adapter selection was therefore treated as a separate question rather than as a proxy for general GPU health.

## Result

The tested Termux Chromium and Code OSS paths did not expose Turnip as the desired native WebGPU adapter. WebGPU either selected SwiftShader or returned no adapter when software fallback was prevented/native paths were forced.

A useful control was that the same physical GPU could be exposed as a non-fallback Qualcomm `adreno-7xx` WebGPU adapter in Android Edge. This rules out the simple explanation that the hardware itself cannot support the workload.

## Current interpretation

The evidence points to a compatibility/integration boundary involving Chromium/Dawn's Linux/X11-style path and the Termux Mesa Turnip/Freedreno environment. The experiment does not claim a single proven low-level root cause.

## Decision

Do not advertise native WebGPU support for the current Termux desktop stack. Keep conventional ANGLE Vulkan acceleration as a separate successful result.

See [`report.md`](report.md).
