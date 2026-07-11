# 0073 — VS Code Implicit Primary GPU: LVP/llvmpipe Selected

## Status

The bounded VS Code CDP GPU identity probe passed under:

```text
GL_GPU=1
VULKAN_POLICY_MODE=implicit-discovery
```

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    vscode-cdp-implicit-20260711-150155
```

The Chrome DevTools Protocol `SystemInfo.getInfo` result identified the primary GPU as:

```text
vendorString:
    Google Inc. (Mesa)

deviceString:
    ANGLE (Mesa, Vulkan 1.4.305
    (llvmpipe (LLVM 19.1.7 128 bits) (0x00000000)),
    llvmpipe-0.0.1)

driverVendor:
    Mesa

driverVersion:
    0.0.1
```

The first GPU device row was explicitly marked:

```text
index=0
primary=true
```

Therefore the implicit primary selected Vulkan device/provider is:

```text
LVP / llvmpipe
```

The simultaneously mapped `libvulkan_gfxstream.so` remains part of the implicit discovery composition but is not the primary selected device in this run.

## Probe receipt

Probe status:

```text
PASS
```

The browser command line preserved the intended feature mode:

```text
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
--disable-gpu-vsync
```

and added only bounded CDP instrumentation:

```text
--remote-debugging-address=127.0.0.1
--remote-debugging-port=0
```

The launch policy remained:

```text
experiment Vulkan policy: implicit-discovery
GL_GPU=1
VK_DRIVER_FILES=<unset>
```

## Primary GPU identity

Observed device row:

```text
index: 0
primary: true
vendorId: 0
deviceId: 0
vendorString: Google Inc. (Mesa)
deviceString: ANGLE (Mesa, Vulkan 1.4.305
              (llvmpipe (LLVM 19.1.7 128 bits) (0x00000000)),
              llvmpipe-0.0.1)
driverVendor: Mesa
driverVersion: 0.0.1
```

The device string directly identifies:

```text
llvmpipe
LLVM 19.1.7
llvmpipe-0.0.1
```

This is stronger than inferring provider choice from mapped shared objects.

## ANGLE and Vulkan state

Observed auxiliary attributes:

```text
displayType:
    ANGLE_VULKAN

glImplementationParts:
    (gl=egl-angle,angle=vulkan)

glRenderer:
    ANGLE (Mesa, Vulkan 1.4.305
    (llvmpipe (LLVM 19.1.7 128 bits) (0x00000000)),
    llvmpipe-0.0.1)

hardwareSupportsVulkan:
    true

skiaBackendType:
    GaneshVulkan
```

Observed feature state:

```text
gpu_compositing:
    enabled

rasterization:
    enabled

vulkan:
    enabled_on

webgl:
    enabled

webgpu:
    enabled
```

The result is therefore not:

```text
Vulkan feature disabled
ANGLE fell back to a non-Vulkan backend
```

It is:

```text
ANGLE Vulkan active
    -> primary Vulkan device llvmpipe
    -> LVP software provider selected
```

`hardwareSupportsVulkan=true` is Chromium's reported capability field and must not be interpreted as proof that the selected device is hardware-backed. The primary renderer string directly identifies the selected device as llvmpipe.

## Mapped-object correlation

The same GPU process mapped:

```text
$HOME/gl/apps/vscode/libEGL.so
$HOME/gl/apps/vscode/libGLESv2.so
$HOME/gl/apps/vscode/libvulkan.so.1
rootfs libVkLayer_MESA_device_select.so
rootfs libgbm.so.1.0.0
rootfs libvulkan_gfxstream.so
rootfs libvulkan_lvp.so
```

It did not map:

```text
provider-store libvulkan_freedreno.so
/dev/kgsl-3d0
```

The structured primary-device identity plus mapped-object relation yields:

```text
selected provider:
    LVP / llvmpipe

mapped but not primary-selected discovery member:
    Gfxstream

hardware provider/device relation:
    absent in implicit control
```

This closes the ambiguity left by the map-only result.

## Behavioral A/B interpretation

The completed policy A/B now has a stronger semantic form.

### Explicit intent

```text
GPU maps:
    provider-store Freedreno
    /dev/kgsl-3d0

selected primary identity:
    still to be confirmed through the same CDP observer
```

### Implicit discovery

```text
GPU maps:
    LVP
    Gfxstream

CDP primary selected identity:
    llvmpipe
```

The behavioral causal result remains:

```text
application-main provider-policy input
    -> changes downstream GPU provider/device composition
```

The implicit selected-provider result now adds:

```text
implicit discovery
    -> selects software LVP/llvmpipe as primary
```

for the captured VS Code/runtime state.

## New machine-readable identity classifier

Added:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    classify-vscode-cdp-gpu-identity.sh
```

Commit:

```text
5043f200f4e6843d6d21bae9fa2a6ad1906e5569
```

The classifier reads an existing completed CDP probe without rerunning VS Code.

It records:

```text
primary device fields
ANGLE renderer string
ANGLE display type
Skia backend
Vulkan feature status
selected provider classification
mapped provider correlation
device-node correlation where applicable
```

Recognized classifications:

```text
LVP_LLVMPIPE
GFXSTREAM
FREEDRENO_TURNIP
UNKNOWN
```

For the current implicit evidence, the expected classification is:

```text
classification=LVP_LLVMPIPE
selected_provider=LVP
selected_device_family=llvmpipe
provider_path_relation=PRESENT
correlation_state=PASS
```

## Next bounded gate

Run the same CDP GPU identity probe under:

```text
VULKAN_POLICY_MODE=explicit-freedreno
```

Keep:

```text
same VS Code payload
same GL_GPU=1 feature mode
same ANGLE/Vulkan flags
same CDP observer
same bounded duration
```

The expected evidence question is not predeclared as a required answer.

The probe should report the actual primary device identity. Useful identifying strings may include:

```text
Turnip
Adreno
Freedreno
```

If the primary identity confirms Turnip/Adreno and the same GPU process maps:

```text
libvulkan_freedreno.so
/dev/kgsl-3d0
```

then the explicit selected-provider gate can close symmetrically as:

```text
explicit selected provider:
    Freedreno/Turnip

explicit selected device family:
    Adreno
```

## Current gate state

```text
explicit control topology/survival/maps:
    PASS

implicit control topology/survival/maps:
    PASS

policy A/B comparison receipt:
    PASS

application-main policy behavioral causality:
    PROVEN

implicit mapped provider composition:
    LVP + Gfxstream

implicit primary selected provider:
    LVP / llvmpipe

implicit Gfxstream role:
    mapped discovery member, not primary selected device

explicit mapped hardware composition:
    Freedreno + KGSL

explicit primary selected provider:
    NEXT SYMMETRIC CDP GATE

promoted launcher/shared-env migration:
    STILL BLOCKED
```

## Stop line

Do not yet:

```text
claim explicit Turnip selection solely from maps;
change promoted VS Code launcher;
change shared gl/env;
remove explicit provider policy;
replace the vendor-local Vulkan loader;
force environment variables into Chromium children;
add broad tracing;
```

First run the same bounded CDP identity probe in explicit-freedreno mode and classify its existing output with the new receipt helper.
