# 0068 — VS Code Vendor Loader Identity and GPU Observer Contract Gate

## Status

The VS Code app-local Vulkan loader identity probe produced a useful result and also exposed two implementation defects in the first probe revision.

The evidence establishes:

```text
VS Code app-local libvulkan.so.1:
    vendor payload-local object
    distinct from gl-farm/rootfs loader
    distinct from prefix glibc loader
    exports Vulkan loader entry points
    contains VK_LOADER_DEBUG marker
    contains Vulkan Loader Version marker
```

The remaining question is no longer whether the object is loader-shaped or whether it contains desktop-loader debug markers.

The next bounded question is:

```text
does the actual VS Code GPU subprocess retain the expected Vulkan policy/debug environment,
and where do its stdout/stderr file descriptors point?
```

A short GPU observer-contract probe has been added for that purpose.

## Evidence root

Identity evidence:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-loader-identity-20260711-142945
```

Control evidence reused by the identity probe:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-explicit-adopted-20260711-134601
```

## Vendor payload provenance

The preserved original VS Code onboarding report records that the official Microsoft VS Code ARM64 tarball directory itself contains:

```text
libEGL.so
libGLESv2.so
libvk_swiftshader.so
libvulkan.so.1
vk_swiftshader_icd.json
```

Therefore the mapped:

```text
$HOME/gl/apps/vscode/libvulkan.so.1
```

is a vendor payload-local component, not an object materialized by the current broad farm, Debian rootfs provider path, or Termux glibc prefix.

This conclusion is independently consistent with the direct byte/build identity comparison below.

## Identity result

### App-local loader

Observed:

```text
path:
    $HOME/gl/apps/vscode/libvulkan.so.1

bytes:
    2763681

sha256:
    73c73d9e073e35a028fd292d599677932f95064fbd023daf30b7c2ffebf19baa

build ID:
    0b47c698f41a28029da43eca0312000455ef43fc

SONAME:
    libvulkan.so.1
```

### Rootfs/farm loader

The gl-farm alias resolves to:

```text
rootfs/usr/lib/aarch64-linux-gnu/libvulkan.so.1.4.309
```

Observed identity:

```text
bytes:
    592496

sha256:
    22b6ce3145007566e3e47ce1f379135ba9b83e734cba2edc2d0c3e1b28ffeea7

build ID:
    e01027e682625cfe6a4a43a5113694d8fb332a99
```

### Prefix glibc loader

Observed:

```text
path:
    $PREFIX/glibc/lib/libvulkan.so.1.3.301

bytes:
    695400

sha256:
    60079bc90956c55ae10b9bd18ab60f42f92bcf0c8e22768b7ae3be7518f4549f

build ID:
    f1f5d6c50e12491ac1c4a165e2c88cfa5eb74ff8
```

## Identity conclusion

The app-local object is byte- and build-identity distinct from both compared desktop-loader candidates:

```text
APP_LOCAL vs GL_FARM_ALIAS:
    SHA: DIFFERENT
    build ID: DIFFERENT

APP_LOCAL vs PREFIX_GLIBC_LIB:
    SHA: DIFFERENT
    build ID: DIFFERENT

APP_LOCAL vs ROOTFS_MULTIARCH:
    SHA: DIFFERENT
    build ID: DIFFERENT
```

Therefore do not assume that the standalone rootfs or prefix loader's exact logging behavior is automatically identical to the VS Code vendor payload-local loader.

The semantic class is now more precise:

```text
consumer-local Vulkan loader component
```

not:

```text
world-global Vulkan loader selected from the farm
```

## Loader capability markers

The raw string dump from the app-local object contains:

```text
VK_LOADER_DEBUG
Vulkan Loader Version %d.%d.%d
[Vulkan Loader]
```

It also contains loader implementation diagnostics such as:

```text
loader_scanned_icd_add
loader_create_instance_chain
terminator_CreateInstance
```

and exports loader-facing Vulkan entry points including:

```text
vkGetInstanceProcAddr
vkCreateInstance
vkEnumerateInstanceExtensionProperties
vkEnumerateInstanceLayerProperties
```

Therefore the earlier possible branch:

```text
app-local object lacks desktop-loader debug markers
```

is rejected.

## Probe defects found by the raw output

The first identity probe revision wrote:

```text
has_vk_loader_debug_string=NO
has_vulkan_loader_banner_string=NO
```

while the raw string report from the same object visibly contained both markers.

Root cause in the helper:

```text
set -o pipefail
strings ... | grep -q ...
```

With an early successful `grep -q` exit, the producer may receive SIGPIPE, causing the overall pipeline status under `pipefail` to become non-zero and yielding a false negative.

The helper has been corrected to avoid early-exit `grep -q` in that pipeline.

A second defect was also found.

The two broad observer signal lines were printed to the terminal but were not redirected into:

```text
control-observer-signal-lines.tsv
```

The output file therefore retained only its header.

That redirection defect has also been corrected.

Correction commit:

```text
630469029d75dc438e3a5eb6aebd5a5f74c14c77
```

## Exact meaning of the two earlier stderr broad matches

The terminal output already exposed the two lines:

```text
experiment Vulkan policy: explicit-freedreno
VK_DRIVER_FILES=.../freedreno_icd.aarch64.json
```

These are experiment launcher/policy echo lines, not Vulkan loader selection diagnostics.

Therefore the corrected interpretation of the stored control remains:

```text
VK_LOADER_DEBUG provider-selection log:
    absent from captured launch stdout/stderr
```

while the independent process map result remains:

```text
GPU process maps app-local Vulkan loader:
    PASS

GPU process maps provider-store Freedreno ICD object:
    PASS

GPU process maps /dev/kgsl-3d0:
    PASS
```

## Why the next question is environment plus stdio contract

The vendor payload-local object contains the expected debug markers, yet the captured streams contain no loader diagnostics.

The smallest remaining discrimination is between:

```text
A. VK_LOADER_DEBUG or provider policy was not present in the GPU subprocess environment

B. the GPU subprocess had the environment, but stdout/stderr were redirected or detached

C. both environment and observable stdio were present, but the vendor-local loader did not emit the expected diagnostics in this execution path
```

These cases require different next actions and should not be conflated.

## New bounded GPU observer-contract probe

Added:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    probe-vscode-gpu-observer-contract.sh
```

Commit:

```text
d019e80bfcd77412d4be7bd8340db79613448cda
```

The probe follows the existing bounded VS Code process-handoff probe style.

It:

```text
1. rejects preexisting VS Code application processes;
2. runs only explicit-freedreno GPU feature mode;
3. injects VK_LOADER_DEBUG=all at launch;
4. observes the bounded app process set;
5. finds the GPU process by --type=gpu-process;
6. captures selected /proc/<gpu>/environ keys;
7. captures /proc/<gpu>/fd/{0,1,2} targets;
8. records launch stdout/stderr;
9. terminates only matching observed application processes at probe cleanup.
```

Default bounded duration:

```text
15 seconds
```

The probe does not change promoted launchers, shared `gl/env`, provider materialization, or provider promotion state.

## Evidence outputs

```text
gpu-environment.tsv
gpu-stdio-fds.tsv
gpu-process-selection.tsv
observation-state.tsv
launch.stdout
launch.stderr
probe.status
```

Relevant environment keys include:

```text
VK_LOADER_DEBUG
VK_DRIVER_FILES
VK_ICD_FILENAMES
TND_EXPERIMENT_VULKAN_POLICY
LD_LIBRARY_PATH
LD_PRELOAD
LIBGL_ALWAYS_SOFTWARE
MESA_LOADER_DRIVER_OVERRIDE
```

## Decision branches

### Branch A — environment missing in GPU process

Then the consumer process model sanitizes or reconstructs environment state before the GPU process.

Next work:

```text
identify the exact process boundary where policy/debug variables are lost
```

Do not blame loader logging.

### Branch B — environment present, stdout/stderr detached or redirected

Then `VK_LOADER_DEBUG` may be functioning but the capture channel is wrong for this subprocess.

Next work:

```text
use the actual GPU-process fd target or a minimally redirected child-local observer
```

Do not rerun a long GUI control merely to repeat the same blind capture.

### Branch C — environment present and stdio points to captured launch streams

Then the remaining explanation moves to vendor-local loader behavior or the exact Vulkan initialization path.

Next work must be one consumer-specific bounded selection observer, potentially reusing the earlier VS Code Vulkan diagnostic instrumentation lineage, rather than broad invasive tracing.

## Current gate state

```text
VS Code explicit control workload:
    PASS

GPU -> provider-store Freedreno:
    PASS

GPU -> KGSL:
    PASS

vendor payload-local Vulkan loader identity:
    ESTABLISHED

distinct from farm/rootfs loader:
    PASS

distinct from prefix glibc loader:
    PASS

loader debug markers in app-local object:
    PRESENT

captured VK_LOADER_DEBUG selection output:
    ABSENT

GPU environment/stdio observer contract:
    NEXT BOUNDED GATE

loader selected-provider identity:
    OPEN

implicit-discovery VS Code control:
    STILL BLOCKED
```

## Stop line

Do not yet:

```text
run VS Code implicit-discovery control
repeat the 60-second explicit control blindly
change promoted VS Code launcher
change shared gl/env
replace the vendor-local loader
force a different loader into VS Code
infer selected provider solely from map presence
add invasive tracing
```

First close the GPU subprocess environment and stdio observation contract.
