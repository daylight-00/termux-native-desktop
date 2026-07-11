# 0072 — VS Code Policy Comparison Receipt PASS and CDP GPU Identity Plan

## Status

The machine-readable VS Code Vulkan policy comparison receipt passed.

Comparison evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    vscode-policy-control-comparison-20260711-145525
```

Exact compared control roots:

```text
explicit:
    $PREFIX/tmp/tnd-vulkan-policy-composition/
        vscode-explicit-adopted-20260711-134601

implicit:
    $PREFIX/tmp/tnd-vulkan-policy-composition/
        vscode-implicit-adopted-20260711-144907
```

Both controls passed:

```text
topology.status=PASS
survival.status=PASS
maps-capture.status=PASS
```

All comparison gates passed.

This closes the machine-verification step for the behavioral causal claim already described in document 0071.

## Control status receipt

Observed:

```text
control   topology   survival   maps_capture
explicit  PASS       PASS       PASS
implicit  PASS       PASS       PASS
```

The compared relation files were therefore both produced from completed workload controls after topology, survival, and final map-capture gates.

## Comparison gate receipt

Observed:

```text
explicit_gpu_freedreno_present       PASS
explicit_gpu_kgsl_present            PASS
explicit_gpu_lvp_absent              PASS
explicit_gpu_gfxstream_absent        PASS
implicit_gpu_lvp_present             PASS
implicit_gpu_gfxstream_present       PASS
implicit_gpu_freedreno_absent        PASS
implicit_gpu_kgsl_absent              PASS
bidirectional_relation_delta_present PASS
```

Receipt status:

```text
PASS
```

## Exact relation delta

### Explicit-only GPU relations

```text
gpu -> $HOME/gl/opt/mesa-glibc-26.1.4-full/lib/libvulkan_freedreno.so
gpu -> /dev/kgsl-3d0
```

### Implicit-only GPU relations

```text
gpu -> rootfs/usr/lib/aarch64-linux-gnu/libvulkan_gfxstream.so
gpu -> rootfs/usr/lib/aarch64-linux-gnu/libvulkan_lvp.so
```

### Common graphics relations

```text
gpu -> $HOME/gl/apps/vscode/libEGL.so
gpu -> $HOME/gl/apps/vscode/libGLESv2.so
gpu -> $HOME/gl/apps/vscode/libvulkan.so.1
gpu -> rootfs libVkLayer_MESA_device_select.so
gpu -> rootfs libgbm.so.1.0.0

main/zygote/renderer/utility -> rootfs libgbm.so.1.0.0
```

The common/delta split supports the architecture model:

```text
stable consumer-local graphics front half
    + policy-dependent provider/device tail
```

## Behavioral causal gate

The receipt confirms all required conditions:

```text
same consumer
same application feature mode
same workload gates
same process-adoption contract
different provider-policy input
different downstream GPU provider/device composition
```

Therefore the following claim is now both human-reviewed and machine-verified:

```text
For the captured VS Code consumer and runtime state,
changing the application-main Vulkan provider-policy input
changes the downstream GPU-process provider/device composition.
```

The ordinary Chromium child environment does not expose the original `VK_*` variables, but the behavioral downstream effect remains proven.

## Remaining selected-provider question

The implicit GPU process maps both:

```text
libvulkan_gfxstream.so
libvulkan_lvp.so
```

Map presence proves composition membership, not final physical-device selection.

The next question is:

```text
Which GPU identity does Chromium/ANGLE report as primary
under implicit-discovery mode?
```

Do not infer the answer from library names or loading order.

## Selected observer: Chrome DevTools Protocol SystemInfo

The official Chrome DevTools Protocol defines:

```text
SystemInfo.getInfo
```

as a low-level system-information query that returns a GPU information object.

Its GPU device records include:

```text
vendorId
deviceId
vendorString
deviceString
driverVendor
driverVersion
```

The protocol specifies that device element zero is the primary GPU.

The GPU information object also contains:

```text
auxAttributes
featureStatus
driverBugWorkarounds
```

This observer is preferable to the rejected alternatives because it is:

```text
consumer-level
structured
read-only after instrumentation launch
independent of GPU stdout/stderr
stronger than map-presence inference
```

Primary reference:

```text
https://chromedevtools.github.io/devtools-protocol/tot/SystemInfo/
```

## Added standard-library CDP client

Added:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    query-cdp-system-info.py
```

Commit:

```text
7eb86ad7275c6bdd5577d355df500c0942ea0f47
```

The helper uses only the Python standard library.

It implements the bounded subset required for the probe:

```text
WebSocket opening handshake
masked client text frames
server frame decoding
ping/pong handling
fragmented text-message assembly
CDP request/response correlation
SystemInfo.getInfo
```

Outputs:

```text
system-info.json
gpu-devices.tsv
gpu-aux-attributes.tsv
gpu-feature-status.tsv
browser-command-line.txt
```

The helper fails if the protocol result contains no GPU object or no GPU devices.

## Added VS Code CDP GPU identity probe

Added:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    probe-vscode-cdp-gpu-identity.sh
```

Commit:

```text
bffe6b1f65631de106c88a32227815fb5261eed8
```

The probe:

```text
1. rejects preexisting VS Code processes;
2. preserves GL_GPU=1 and the existing ANGLE/Vulkan flags;
3. supports explicit-freedreno or implicit-discovery policy mode;
4. adds only remote-debugging instrumentation flags;
5. uses the existing VS Code user-data directory by default;
6. preserves and restores a preexisting DevToolsActivePort file;
7. waits for both the browser CDP endpoint and a GPU process;
8. calls SystemInfo.getInfo over the browser WebSocket endpoint;
9. records structured GPU identity and feature state;
10. captures the same GPU process's graphics-related mapped paths for correlation;
11. terminates only matching VS Code processes during cleanup.
```

Default instrumentation flags:

```text
--remote-debugging-address=127.0.0.1
--remote-debugging-port=0
```

The selected port and browser WebSocket path are read from:

```text
$HOME/.config/Code/DevToolsActivePort
```

The probe copies the active-port evidence into its output directory and restores any file that existed before the probe.

## Probe outputs

```text
DevToolsActivePort
websocket-url.txt
gpu.pid
system-info.json
gpu-devices.tsv
gpu-aux-attributes.tsv
gpu-feature-status.tsv
browser-command-line.txt
gpu.maps
gpu-graphics-paths.tsv
launch.stdout
launch.stderr
probe.status
```

## First run scope

Run the next probe in:

```text
VULKAN_POLICY_MODE=implicit-discovery
```

The purpose is to classify the currently open implicit selected-device question.

Possible useful results include device/renderer strings identifying:

```text
Lavapipe / llvmpipe
Gfxstream
another software or virtual device
```

Do not predeclare an expected result.

## Decision branches

### Outcome A — primary device identifies Lavapipe/llvmpipe

Then close:

```text
implicit selected provider:
    LVP / llvmpipe
```

while retaining Gfxstream as a mapped but unselected composition member unless contrary evidence appears.

### Outcome B — primary device identifies Gfxstream

Then close:

```text
implicit selected provider:
    Gfxstream
```

while retaining LVP as mapped but unselected unless contrary evidence appears.

### Outcome C — device information is generic or ambiguous

Use the complete:

```text
auxAttributes
featureStatus
browser command line
mapped graphics paths
```

before deciding whether one additional narrow observer is required.

Do not guess from a generic `Vulkan` or `ANGLE` label alone.

### Outcome D — remote debugging endpoint is unavailable

Treat this as observer incompatibility, not a workload/provider failure.

Preserve the partial evidence and choose the next consumer-level observer without changing provider composition.

## Current gate state

```text
explicit control topology/survival/maps:
    PASS

implicit control topology/survival/maps:
    PASS

machine-readable A/B receipt:
    PASS

application-main policy behavioral causality:
    PROVEN

explicit GPU -> Freedreno/KGSL:
    PASS

implicit GPU -> Gfxstream/LVP composition:
    PASS

implicit selected primary GPU/provider:
    NEXT GATE

promoted launcher/shared-env migration:
    STILL BLOCKED
```

## Stop line

Do not yet:

```text
claim LVP selected from maps alone;
claim Gfxstream selected from maps alone;
change promoted launcher;
change shared gl/env;
replace the vendor-local Vulkan loader;
force environment variables into Chromium children;
add broad tracing;
```

First run the bounded implicit CDP GPU identity probe.
