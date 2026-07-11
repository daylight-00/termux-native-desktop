# 0081 — Promoted VS Code Turnip Primary Identity PASS and CPU Policy Gate

## Status

The promoted VS Code GPU identity validator passed on the real Termux/Android device using the actual public package launcher.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    promoted-vscode-gpu-identity-20260711-160546
```

Repository state:

```text
branch:
    refactor/module-package-layout

head:
    3b8b397664507a6df62e99cfbc00916027717c8a
```

Receipt:

```text
gate_failures=0
validation.status=PASS
```

## Launch authority

Observed public launcher:

```text
$HOME/.local/bin/code
```

Exact target:

```text
$HOME/projects/termux-native-desktop/
    packages/vscode/launcher/code
```

The gate therefore validates the promoted package-owned entry point rather than the earlier experiment-only launch adapter.

## Primary GPU identity

Observed CDP primary device:

```text
primary=true
vendorString=Google Inc. (Qualcomm)
deviceString=
    ANGLE (Qualcomm,
        Vulkan 1.4.354
        (Turnip Adreno (TM) 730 (0x07030001)),
        turnip Mesa driver-538.1.4)
driverVendor=Mesa
```

Classifier result:

```text
classification=FREEDRENO_TURNIP
selected_provider=FREEDRENO_TURNIP
selected_device_family=Adreno
correlation_state=PASS
```

This is selected-device evidence, not merely a mapped-library inference.

## Feature-mode invariants

Observed:

```text
displayType=ANGLE_VULKAN
glImplementationParts=(gl=egl-angle,angle=vulkan)
skiaBackendType=GaneshVulkan
hardwareSupportsVulkan=true
vulkan=enabled_on
gpu_compositing=enabled
rasterization=enabled
webgl=enabled
```

Therefore the promoted launcher retains the intended ANGLE/Vulkan and Ganesh/Vulkan feature composition.

## Provider and device correlation

Observed GPU-process graphics paths:

```text
VS Code AppDir:
    libEGL.so
    libGLESv2.so
    libvulkan.so.1

managed provider:
    $HOME/gl/opt/mesa-glibc-26.1.4-full/lib/
        libvulkan_freedreno.so

support plane:
    rootfs libVkLayer_MESA_device_select.so
    rootfs libgbm.so.1.0.0

device:
    /dev/kgsl-3d0
```

Passed correlation gates:

```text
provider_path_relation=PRESENT
device_node_relation=PRESENT
```

The primary CDP identity and process mappings agree on the same hardware-provider graph.

## Passed gates

```text
probe_status               PASS
identity_status            PASS
classification             PASS
selected_provider          PASS
selected_device_family     PASS
provider_path_relation     PASS
device_node_relation       PASS
display_type               PASS
skia_backend               PASS
vulkan_feature_status      PASS
renderer_identity          PASS
```

## Promotion-equivalence conclusion

The experiment adapter previously established:

```text
explicit Freedreno policy
    -> Turnip / Adreno 730 primary device
```

The promoted public launcher now establishes the same result:

```text
$HOME/.local/bin/code
    -> package-owned launcher
    -> provider-neutral glibc baseline
    -> explicit Freedreno profile in GL_GPU=1 branch
    -> ANGLE Vulkan
    -> Turnip / Adreno 730
    -> /dev/kgsl-3d0
```

Therefore the GPU policy behavior survived promotion from experiment adapter to the real package launcher.

## Non-fatal diagnostics

Launch stderr included:

```text
grep: /proc/version: Permission denied
Electron CLI warnings that Chromium flags are not known VS Code CLI options
```

The vendor CLI explicitly passed those arguments to Electron/Chromium, and the resulting CDP identity proves that the intended graphics flags took effect.

These warnings are not treated as gate failures.

## Claim boundary

This receipt proves:

```text
actual promoted launcher use
ANGLE/Vulkan feature mode
CDP primary selected device identity
Turnip/Freedreno selected provider identity
Adreno 730 device family
managed provider mapping
KGSL device-node mapping
```

It does not prove:

```text
complete zero-copy presentation
all individual rendered frames
hardware video decode
native Dawn WebGPU adapter exposure
long-duration application stability
```

## Next gate — promoted CPU policy

The remaining VS Code branch question is:

```text
GL_GPU=0
    -> provider-neutral process environment
    -> exact --disable-gpu argv policy
    -> no GPU-enablement argv leakage
    -> viable GUI topology and survival
```

Added:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    validate-promoted-vscode-cpu-policy.sh
```

Implementation commits:

```text
a93b1479e62a700f58388bec92a2438e6b731231
4d2cf89548690b5b09c686ce6839aec76b7f66cf
```

The second commit hardens exact-token and environment assertions.

## CPU validator design

The validator launches the actual public launcher with:

```text
GL_GPU=0
isolated user-data directory
isolated extensions directory
--disable-extensions
--new-window
```

It requires no pre-existing VS Code processes.

It observes the real process set for a bounded interval and records:

```text
process identities and argv
process class
parent PID
environment readability
selected environment variables
topology state over time
launch stdout/stderr
```

Required stable classes:

```text
main
zygote
renderer
```

A GPU process is observable if Chromium creates one, but its presence or absence is not itself a pass/fail criterion. `--disable-gpu` does not justify encoding one internal process-topology assumption as architecture policy.

## CPU environment gates

For every successfully captured environment:

```text
GL_GPU values must be 0
VK_DRIVER_FILES must be absent
VK_ICD_FILENAMES must be absent
MESA_LOADER_DRIVER_OVERRIDE must be absent
LIBGL_ALWAYS_SOFTWARE must be absent
LD_LIBRARY_PATH must be absent
LD_PRELOAD must be absent or empty
```

The main process must explicitly expose:

```text
GL_GPU=0
```

This confirms that the CPU application-feature decision reaches the promoted workload while provider selection remains absent.

## CPU argv gates

The main process must contain the exact token:

```text
--disable-gpu
```

It must not contain:

```text
--use-angle=vulkan
--use-gl=angle
--enable-features=Vulkan
--disable-gpu-vsync
--ignore-gpu-blocklist
--disable-gpu-sandbox
```

The exact-token test prevents `--disable-gpu-sandbox` from being misread as `--disable-gpu`.

## CPU survival gates

The main process must still belong to the probe at the end of the observation interval.

Launch stderr must not contain:

```text
FATAL
GPU process isn't usable
```

The validator cleans up only processes associated with the VS Code application tree or its isolated user-data directory.

## Current gate state

```text
live scoped policy installation:
    PASS

promoted gl-run renderer:
    PASS

promoted VS Code GPU identity:
    PASS

promoted VS Code CPU policy:
    NEXT

promoted Obsidian GPU/CPU:
    BLOCKED ON VS CODE CPU RESULT

scoped Vulkan promotion closure:
    PENDING
```

## Stop line

Do not:

```text
run the CPU and Obsidian probes concurrently
assert that CPU mode forbids all Chromium GPU helper processes
use a real user-data directory for the CPU gate
interpret absence of explicit VK variables as proof that no loader discovery can occur
mark the VS Code package fully validated before the CPU gate
```

Run the bounded promoted VS Code CPU policy validator next.
