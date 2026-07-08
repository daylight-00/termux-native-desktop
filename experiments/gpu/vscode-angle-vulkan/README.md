# Official VS Code: direct ANGLE Vulkan enablement

**Status:** passed  
**Dates:** 2026-07-02 to 2026-07-03 workstream; later revalidated on the current stack  
**Provenance:** first-hand session report (`report.md`)

## Question

Once official Microsoft VS Code already runs reliably as a glibc application, what is the minimum condition required to enable a direct real-GPU rendering path through ANGLE Vulkan and Turnip under Termux:X11?

## Baseline

CPU-rendered VS Code was already stable. GPU enablement was therefore isolated from application onboarding.

The initial direct path reached Vulkan instance/device/surface creation but repeatedly failed at swapchain creation with `VK_ERROR_INITIALIZATION_FAILED`, followed by GPU-process restarts.

## Investigation shape

The report progressively eliminated tempting explanations:

- pure Vulkan WSI failure;
- image-usage combinations;
- large window extent;
- ANGLE-like device-extension profiles;
- selected swapchain fields and pNext chains;
- proxy/translation-only explanations.

Controls showed that pure Vulkan worked, ANGLE-like Vulkan choices worked externally, and even the actual VS Code window could be presented to from an external probe. A child-window diagnostic then isolated a connection/window interaction strongly enough to test Chromium GPU-vsync behavior.

## Result

The production path succeeded with:

```text
Official VS Code
  -> Electron / Chromium
  -> ANGLE Vulkan
  -> glibc Vulkan runtime
  -> Mesa Turnip / KGSL
  -> Adreno 730
  -> Termux:X11
```

The minimum experimentally demonstrated GPU-specific workaround was:

```text
--disable-gpu-vsync
```

The final successful path did not require the diagnostic proxy window, forced software WSI, disabling GPU rasterization, disabling Chromium's zero-copy feature, fixed window size, or TCP X11.

## Claim boundary

The experiment proves successful direct ANGLE Vulkan rendering on the real Adreno GPU with Mesa's default WSI mode. It does **not** prove that every frame uses a particular DRI3/dmabuf route or that the entire presentation path is end-to-end zero-copy.

## Decision

Keep GPU enablement separate from glibc application onboarding. Promote only the narrow launch condition required by the experiment into the VS Code launcher.

See [`report.md`](report.md).
