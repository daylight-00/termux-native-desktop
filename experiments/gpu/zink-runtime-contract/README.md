# zink-runtime-contract

Status: **passed**

## Question

With the msm,kgsl build in place, what is the minimal correct runtime
environment for OpenGL apps on Zink→Turnip (and why did the first glxinfo
attempt fail)?

## Evidence

- `MESA_LOADER_DRIVER_OVERRIDE=zink` + **only** `VK_ICD_FILENAMES` →
  `ZINK: vkCreateInstance failed (VK_ERROR_INCOMPATIBLE_DRIVER)`.
  Modern Vulkan loaders prefer `VK_DRIVER_FILES`; with it absent the loader
  default-scans and finds the **bionic** ICD, whose .so cannot load in a
  glibc process (`libm.so: invalid ELF header`).
- With **both** VK variables + the override:
  `renderer: zink Vulkan 1.4(Turnip Adreno (TM) 730)`, OpenGL 4.6
  (Compatibility Profile) — glibc glxinfo.
- Vulkan-native apps need only the two VK variables (no override).

## Result / Decision

Contract encoded in `setup/glibc/env` (pins BOTH VK vars to the glibc ICD,
deliberately overriding the desktop session's bionic export) and in
`bin/gl-run` (adds the zink override for GL apps). Rule of thumb:
**always set both VK variables.**
