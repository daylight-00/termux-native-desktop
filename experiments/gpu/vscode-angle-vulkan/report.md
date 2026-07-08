# Enabling GPU Acceleration in Official Microsoft VS Code on Native Termux
## Experimental Report: From Stable CPU Rendering to Direct ANGLE Vulkan on Adreno 730

## Abstract

This report documents the process of enabling GPU acceleration in the official Microsoft VS Code ARM64 Linux build after CPU-only operation had already been stabilized on a native Termux environment.

The work was performed without `proot`, `chroot`, or a conventional Linux distribution container. The final software path was:

```text
Official Microsoft VS Code ARM64
        │
        ▼
Electron / Chromium
        │
        ▼
ANGLE Vulkan backend
        │
        ▼
glibc Vulkan loader
        │
        ▼
Mesa Turnip, KGSL backend
        │
        ▼
Qualcomm Adreno 730
        │
        ▼
Mesa X11 WSI
        │
        ▼
Termux:X11
```

The central problem was not GPU enumeration, Vulkan device creation, XCB surface creation, image usage compatibility, window dimensions, ANGLE-style Vulkan device extensions, or the fundamental ability of Turnip to create swapchains.

The direct Electron/ANGLE Vulkan path consistently reached:

```text
vkCreateXcbSurfaceKHR → VK_SUCCESS
vkCreateSwapchainKHR  → VK_ERROR_INITIALIZATION_FAILED (-3)
```

followed by GPU process restarts.

A sequence of progressively narrower experiments showed that:

1. pure Vulkan applications could create swapchains;
2. equivalent image usage combinations worked;
3. ANGLE-like device extension profiles worked;
4. the actual VS Code X11 window worked from an external Vulkan process;
5. a clean child window created inside the GPU process also worked;
6. finally, disabling Chromium GPU vsync allowed the **original window**, with **no proxy shim**, to work.

The final minimum workaround was therefore:

```text
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
--disable-gpu-vsync
```

with the appropriate glibc and Turnip runtime environment.

The proxy-window shim was crucial as a diagnostic instrument, but it was not required in the final production configuration.

---

# 1. Scope

This report starts **after CPU-only VS Code execution was already working**.

It does not attempt to document the full construction of the glibc compatibility layer, Debian library extraction, font configuration, certificate setup, or Mesa compilation process in detail. Those components are described only where they directly affected the GPU enablement effort.

The specific question investigated here was:

> Once the official glibc-linked Microsoft VS Code ARM64 build can run reliably in CPU-rendered mode, what is required to enable the maximum practical GPU acceleration path on native Termux and Termux:X11?

The target was not merely “make the window appear.” The desired progression was:

```text
CPU software rendering
        ↓
GPU process starts
        ↓
ANGLE uses Vulkan
        ↓
Turnip uses Adreno 730
        ↓
default Mesa WSI mode
        ↓
no software-presentation force
        ↓
no proxy window if avoidable
        ↓
no disabled zero-copy feature flag
        ↓
no disabled GPU rasterization flag
```

---

# 2. Experimental Platform

The relevant platform was:

```text
Host environment:
  Native Termux on Android
  No proot
  No chroot
  No conventional Linux VM/container

Display:
  Termux:X11
  X11 Ozone platform
  Final working DISPLAY=:1 local X11 connection

GPU:
  Qualcomm Adreno 730

Vulkan driver:
  Mesa Turnip
  Freedreno KGSL backend

Target application:
  Official Microsoft VS Code ARM64 Linux build

VS Code version:
  1.127.0

Architecture:
  arm64 / AArch64

Compatibility runtime:
  Termux glibc target
  glibc-runner --no-linker

Main Mesa experiment prefix:
  ~/opt/mesa-26-glibc

Main VS Code directory:
  ~/opt/VSCode-linux-arm64

Additional glibc-compatible libraries:
  ~/opt/debian-arm64-libs/usr/lib/aarch64-linux-gnu
```

The official VS Code version had previously been verified with the Electron CLI path:

```bash
ELECTRON_RUN_AS_NODE=1 \
glibc-runner --no-linker \
  "$VSCODE_DIR/code" \
  "$VSCODE_DIR/resources/app/out/cli.js" \
  --version
```

Observed output:

```text
1.127.0
4fe60c8b1cdac1c4c174f2fb180d0d758272d713
arm64
```

---

# 3. Stable CPU Baseline

Before attempting GPU acceleration, the application had been stabilized by disabling Chromium GPU use entirely.

The CPU-oriented path used flags of this general form:

```text
--no-sandbox
--disable-gpu
--disable-gpu-compositing
--disable-gpu-rasterization
--disable-accelerated-2d-canvas
--disable-accelerated-video-decode
--disable-dev-shm-usage
--disable-crash-reporter
--disable-breakpad
--password-store=basic
--ozone-platform=x11
```

The corresponding application initialization reached normal states such as:

```text
StorageMainService: creating application shared storage
Started local extension host
Completed initializing default profile extensions
```

At that point the CPU-rendered application was usable, and the GPU effort could be treated as an independent optimization problem rather than as a basic application-porting problem.

This distinction was important throughout the investigation:

```text
Application runtime problem: solved first.

GPU acceleration problem: investigated separately.
```

---

# 4. First GPU Attempts: Chromium GPU Process Did Not Yet Have a Working Rendering Path

An early generic GPU mode was attempted before the full Vulkan path was established.

The logs showed errors such as:

```text
Could not dlopen libGL.so.1
eglInitialize OpenGL failed
Initialization of all EGL display types failed
Exiting GPU process due to errors during initialization
```

This demonstrated that simply allowing the Electron GPU process to start was not sufficient.

The next direction was therefore explicit Vulkan through ANGLE.

The intended Chromium/Electron configuration became:

```text
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
```

The expected rendering chain was:

```text
Electron
→ Chromium Viz
→ ANGLE
→ Vulkan loader
→ Turnip
→ Adreno 730
```

---

# 5. Establishing the Native glibc Vulkan Path

Before blaming Electron or ANGLE, the glibc Vulkan stack itself had to be shown to enumerate the real GPU.

A representative invocation was:

```bash
env -u LD_LIBRARY_PATH \
  VK_ICD_FILENAMES="$GLIBC_FREEDRENO_ICD" \
  VK_DRIVER_FILES="$GLIBC_FREEDRENO_ICD" \
  glibc-runner --no-linker \
  "$PREFIX/glibc/bin/vulkaninfo" \
  --summary
```

The stock glibc Mesa stack produced:

```text
Vulkan Instance Version: 1.3.301

GPU0:
  apiVersion    = 1.3.289
  driverVersion = 24.2.6
  deviceType    = PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU
  deviceName    = Turnip Adreno (TM) 730
  driverID      = DRIVER_ID_MESA_TURNIP
  driverName    = turnip Mesa driver
  driverInfo    = Mesa 24.2.6.termux-glibc-0
```

Later, the custom Mesa 26.0.6 glibc installation produced:

```text
deviceName    = Turnip Adreno (TM) 730
driverID      = DRIVER_ID_MESA_TURNIP
driverName    = turnip Mesa driver
driverInfo    = Mesa 26.0.6 (git-0e095aab43)
apiVersion    = 1.4.335
driverVersion = 26.0.6
```

At this stage the problem was no longer:

```text
Can a glibc process see the Adreno GPU?
```

The answer was clearly yes.

---

# 6. Direct ANGLE Vulkan Attempt

The central direct test was conceptually:

```bash
glibc-runner --no-linker "$PREFIX/glibc/bin/env" \
  LD_LIBRARY_PATH="$MSCODE_LD" \
  DISPLAY=:1 \
  XDG_RUNTIME_DIR="$TMPDIR" \
  VK_ICD_FILENAMES="$NEW_ICD" \
  VK_DRIVER_FILES="$NEW_ICD" \
  "$VSCODE_DIR/code" \
    --no-sandbox \
    --disable-dev-shm-usage \
    --disable-gpu-sandbox \
    --ozone-platform=x11 \
    --ignore-gpu-blocklist \
    --enable-features=Vulkan \
    --use-gl=angle \
    --use-angle=vulkan
```

The result was remarkably consistent:

```text
Vulkan instance creation:       works
physical device selection:      works
XCB presentation support query: works
XCB surface creation:           works
surface capability queries:     work
surface format queries:         work
swapchain creation:             fails with -3
```

The diagnostic log captured:

```text
[vk-diag] vkCreateXcbSurfaceKHR conn=0x2400160000
          window=0x2000001
          flags=0x0

[vk-diag] vkCreateXcbSurfaceKHR result=0
          surface=0x240006ab50
```

followed later by:

```text
[vk-diag] vkCreateSwapchainKHR
          device=0x240021e000
          surface=0x240006ab50
          flags=0x0
          pNext=(nil)
          minImages=3
          format=44
          colorSpace=0
          extent=1440x2400
          layers=1
          usage=0x17
          sharing=0
          preTransform=0x1
          compositeAlpha=0x1
          presentMode=2
          clipped=1
          old=(nil)

[vk-diag] vkCreateSwapchainKHR result=-3 swapchain=(nil)
```

Chromium then reported:

```text
vkCreateSwapchainKHR() failed: -3
Restarting GPU process due to unrecoverable error. Context was lost.
GPU process exited unexpectedly: exit_code=8704
The GPU process has crashed 1 time(s)
```

This same pattern repeated after GPU process restarts.

A later ANGLE EGL path used a more complex swapchain create request:

```text
flags=0xc
pNext=<non-null>
usage=0x97
```

but still produced:

```text
vkCreateSwapchainKHR result=-3

EGL Driver message (Error)
eglCreateWindowSurface:
Internal Vulkan error (-3)

eglCreateWindowSurface failed with error EGL_BAD_SURFACE
```

This confirmed that the failure was not confined to only one Chromium-side swapchain configuration.

---

# 7. Why the Failure Was Difficult to Diagnose

The direct failure superficially suggested many plausible causes:

```text
Turnip KGSL WSI bug
unsupported swapchain imageUsage combination
large 1440×2400 extent
wrong present mode
surface format mismatch
ANGLE device extension interaction
device creation ordering issue
external-memory/dmabuf interaction
swapchain pNext chain problem
Chromium zero-copy interaction
GPU rasterization interaction
original Electron X11 window incompatibility
Present/DRI3 state collision
```

The investigation therefore proceeded by eliminating these variables independently.

This was preferable to repeatedly changing Chromium flags without understanding the failure boundary.

---

# 8. Pure Vulkan Control Tests

The first critical observation was that pure Vulkan applications could use the same GPU and display environment.

For example, `vkcube` using XCB selected the real Turnip GPU and continued running until intentionally terminated by timeout.

The custom Mesa 26.0.6 path also supported default XCB WSI swapchain creation in diagnostic runs.

This immediately established an important distinction:

```text
Pure Vulkan application:
  works

Electron / Chromium / ANGLE Vulkan:
  fails at swapchain creation
```

Therefore the investigation moved from:

```text
"Termux:X11 Vulkan WSI is broken"
```

to:

```text
"Something specific to the Chromium/ANGLE process and window context
 causes the WSI failure."
```

---

# 9. Swapchain Image Usage Hypothesis

One early hypothesis was that ANGLE requested an image usage combination unsupported by Turnip KGSL WSI.

The successful `vkcube` case typically used:

```text
usage = 0x10
```

whereas Electron/ANGLE was observed requesting:

```text
usage = 0x17
```

and later:

```text
usage = 0x97
```

To test this directly, a minimal XCB/Vulkan swapchain probe was created and executed with:

```text
usage=0x10
usage=0x17
usage=0x97
```

The results were:

```text
usage=0x10 → vkCreateSwapchainKHR: VK_SUCCESS
usage=0x17 → vkCreateSwapchainKHR: VK_SUCCESS
usage=0x97 → vkCreateSwapchainKHR: VK_SUCCESS
```

This cleanly falsified the simple hypothesis:

```text
ANGLE swapchain usage bits are unsupported by Turnip KGSL.
```

They were supported.

---

# 10. Large Extent Hypothesis

The display dimensions seen in the failed VS Code path included:

```text
1440×2400
```

A large-window Vulkan control test was therefore performed.

Conceptually:

```bash
vkcube \
  --wsi xcb \
  --width 1440 \
  --height 2400
```

The swapchain succeeded.

Separately, a VS Code test constrained to a smaller window such as:

```text
1200×800
```

still failed in the original direct path.

Therefore:

```text
failure is not caused solely by the 1440×2400 extent
```

and neither was reducing the application window sufficient to solve it.

---

# 11. ANGLE-Like Device Extension and Device-Creation Tests

The next hypothesis was that ANGLE created Vulkan devices with a complex extension combination that changed Turnip behavior.

Observed profiles were reconstructed into a dedicated test program:

```text
basic
angle24
angle54
angle54then24
```

The most important sequence was:

```text
1. create dummy device with approximately 54 ANGLE-like extensions
2. create main device with approximately 24 ANGLE-like extensions
3. create swapchain
```

The test matrix combined each device profile with:

```text
usage 0x10
usage 0x17
usage 0x97
```

All tested combinations succeeded.

The conclusion became:

```text
not a simple device-extension-list problem

not a simple 54-extension device problem

not a simple 24-extension device problem

not the 54-device → 24-device creation order

not imageUsage alone
```

This was an important turning point. The external Vulkan environment could reproduce many of ANGLE's observed Vulkan choices without reproducing the failure.

---

# 12. Attempts to Repair the Swapchain Request from Inside the Process

Several preload experiments were made to determine whether a specific field of `VkSwapchainCreateInfoKHR` was responsible.

The experiments included variations such as:

```text
clear flags
remove pNext
force VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT
change minImageCount
force FIFO present mode
force opaque composite alpha
strip optional swapchain-related extensions
hide selected external-memory and dmabuf extensions
remove device feature pNext chains
filter advertised device extensions
```

A representative retry shim performed:

```c
fixed.flags = 0;
fixed.pNext = NULL;
fixed.imageUsage = VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT;
```

The pattern remained:

```text
original result=-3
retry-minimal result=-3
```

A stronger experiment skipped the original failing call entirely and submitted the reduced create structure first. It still failed.

Therefore the problem was not a side effect of a failed first call, and not simply one malformed swapchain field.

---

# 13. Zink Detour

An OpenGL-over-Vulkan path through Zink was also investigated.

An initial attempt with:

```text
--use-gl=desktop
```

failed because the Chromium build accepted only the relevant ANGLE implementation path.

A later configuration used:

```text
--use-gl=angle
--use-angle=gl
MESA_LOADER_DRIVER_OVERRIDE=zink
GALLIUM_DRIVER=zink
LIBGL_KOPPER_DRI2=1
```

The GPU process avoided the original direct Vulkan `-3` crash pattern, but produced:

```text
MESA: error: zink: could not create swapchain
eglGetMscRateANGLE: glXGetMscRateOML failed
```

The visible result was a gray or blank window in one configuration.

With software compositing added, the application could appear, but this was no longer the desired pure direct Vulkan path.

Zink therefore served as a useful fallback experiment but did not become the final solution.

---

# 14. `MESA_VK_WSI_DEBUG=sw`: First Functional Vulkan Rendering Path

A decisive experiment used:

```text
MESA_VK_WSI_DEBUG=sw
```

with the direct ANGLE Vulkan configuration.

Conceptually:

```bash
glibc-runner --no-linker "$PREFIX/glibc/bin/env" \
  MESA_VK_WSI_DEBUG=sw \
  LD_LIBRARY_PATH="$MSCODE_LD" \
  DISPLAY=:1 \
  VK_ICD_FILENAMES="$NEW_ICD" \
  VK_DRIVER_FILES="$NEW_ICD" \
  "$VSCODE_DIR/code" \
    --enable-features=Vulkan \
    --use-gl=angle \
    --use-angle=vulkan
```

The application window displayed properly.

The relevant application output included:

```text
Started local extension host
```

with no observed:

```text
vkCreateSwapchainKHR() failed
EGL_BAD_SURFACE
GPU process crash
GrContext creation failed
SharedImageStub failure
```

This was a major isolation result.

It demonstrated that:

```text
ANGLE Vulkan could operate
Turnip could render
the Adreno GPU path was usable
the application could display normally
```

when the default presentation path was replaced by Mesa's software-copy WSI mode.

The important interpretation was:

> `MESA_VK_WSI_DEBUG=sw` did not mean the application had reverted to full CPU rendering.

The rendering path remained Vulkan/Turnip/GPU-backed; the forced software component was in the final WSI presentation/copy path.

At that point the working path was:

```text
VS Code
→ Electron
→ ANGLE Vulkan
→ Turnip
→ Adreno 730
→ software-copy WSI presentation
→ Termux:X11
```

This was functional, but not yet the desired final configuration.

---

# 15. Foreign-Window Probe

The next critical experiment used the **actual VS Code X11 window** in an external Vulkan probe.

The window attributes observed were:

```text
window     = 0x1e00007
root       = 0x511
depth      = 24
width      = 1440
height     = 2400
visual     = 0x21
colormap   = 0x20
map_state  = 2
```

The external test deliberately reproduced an ANGLE-like device sequence:

```text
mode=angle54then24
usage=0x97
format=44
present=2
images=3
```

The important output was:

```text
device ext profile=angle54-dummy kept=54

vkCreateDevice[angle54-dummy]:
  0 VK_SUCCESS

device ext profile=angle24-main kept=24

vkCreateDevice[angle24-main]:
  0 VK_SUCCESS

SurfaceCaps:
  0 VK_SUCCESS
  minImages=3
  maxImages=0
  curExtent=1440x2400
  usage=0x8009f

CreateSwapchain:
  minImages=3
  format=44
  colorSpace=0
  extent=1440x2400
  usage=0x97
  present=2

vkCreateSwapchainKHR:
  0 VK_SUCCESS
```

This eliminated a major class of explanations.

The actual VS Code window itself was capable of supporting the requested swapchain from another process/connection.

The emerging matrix was:

| Context | Original VS Code window | Clean child window |
|---|---:|---:|
| External process / connection | Success | Not required |
| GPU process connection | Failure | To be tested |

This led directly to the proxy-window experiment.

---

# 16. Proxy Child-Window Experiment

A Vulkan preload shim intercepted:

```text
vkCreateXcbSurfaceKHR
```

Instead of passing ANGLE's original Electron window directly to Mesa, it:

1. inspected the original window;
2. created a mapped child window using the same XCB connection;
3. used `XCB_COPY_FROM_PARENT`;
4. passed the child window to the real `vkCreateXcbSurfaceKHR`.

The original window was logged as:

```text
Window[original]:
  depth=24
  visual=0x21
  colormap=0x20
  map_state=2
  override_redirect=0
```

The proxy window was:

```text
Window[proxy]:
  depth=24
  visual=0x21
  colormap=0x20
  map_state=2
  override_redirect=0
```

Thus the proxy did **not** solve the issue by choosing a fundamentally different visual, depth, or colormap.

In the proxy-full run, the log showed:

```text
original surface request
conn=0x1c00154000
window=0x2000001
```

followed by creation of:

```text
proxy child=0x2400002
parent=0x2000001
```

and then:

```text
vkCreateXcbSurfaceKHR result=0
```

followed by:

```text
vkCreateSwapchainKHR
surface=0x1c0006aa30
flags=0x0
pNext=(nil)
minImages=3
format=44
extent=1200x800
usage=0x17

vkCreateSwapchainKHR result=0
```

A separate proxy run also demonstrated swapchain recreation:

```text
initial:
  extent=1440x3006
  old=(nil)
  result=0

recreate:
  extent=1200x800
  old=0x3c00798000
  result=0
```

The application window was visibly normal.

This was the first success in default Mesa WSI mode without `MESA_VK_WSI_DEBUG=sw`.

---

# 17. Re-Enabling Chromium Features

The first proxy success had intentionally retained conservative Chromium flags:

```text
--disable-zero-copy
--disable-gpu-rasterization
```

These were then removed incrementally.

## Stage A: remove `--disable-zero-copy`

The proxy path still succeeded.

Observed behavior:

```text
surface creation: success
swapchain creation: success
swapchain recreation: success
no EGL_BAD_SURFACE
no GPU process crash
normal visible application window
```

## Stage B: remove `--disable-gpu-rasterization`

The proxy-full configuration also succeeded.

The resulting configuration had:

```text
MESA_VK_WSI_DEBUG=sw absent
--disable-zero-copy absent
--disable-gpu-rasterization absent
proxy child window enabled
ANGLE Vulkan enabled
```

The proxy was therefore a fully functional high-performance candidate.

However, it was still undesirable as the final design because:

```text
LD_PRELOAD affected the glibc process tree
child-window lifecycle required maintenance
destroy handling needed cleanup
input-event behavior required long-term testing
window resize synchronization required care
the shim created an additional compatibility layer
```

The next goal was therefore to determine whether the condition avoided by the proxy could be removed directly.

---

# 18. Reinterpretation of the Failure Matrix

After the foreign-window and proxy tests, the experimental matrix was:

| Process/connection context | Window | Result |
|---|---|---|
| external Vulkan probe | original VS Code window | `VK_SUCCESS` |
| Electron GPU path | original VS Code window | `VK_ERROR_INITIALIZATION_FAILED` |
| Electron GPU path | clean child window | `VK_SUCCESS` |

This implied that neither the window alone nor the GPU process connection alone was sufficient to cause failure.

The failure depended on their interaction:

```text
GPU process connection × original Electron window
```

The direct failure log provided another important clue.

The same X11 window ID appeared across several failed attempts, but the XCB connection addresses changed:

```text
window=0x2000001
conn=0x2400160000

window=0x2000001
conn=0x3400160000

window=0x2000001
conn=0x1c0015c000
```

Those were associated with GPU process crash/restart cycles rather than obvious repeated surface creation on one unchanged connection.

This weakened the simple hypothesis:

```text
ANGLE creates two Vulkan surfaces on the same window
within one unchanged connection.
```

Attention instead shifted toward Chromium's X11 frame-timing/vsync/Present behavior on the original drawable.

The remaining hypothesis was deliberately stated cautiously:

> Some interaction in the Chromium GPU process involving the original X11 drawable and its vsync/Present-related state was interfering with Mesa Vulkan WSI swapchain initialization.

At this stage this was still a hypothesis, not yet a source-level proof.

---

# 19. The Decisive Experiment: `--disable-gpu-vsync`

The cheapest direct experiment was to remove the proxy and retain the original window, while adding only:

```text
--disable-gpu-vsync
```

The test path was:

```text
direct ANGLE Vulkan
original Electron window
no proxy LD_PRELOAD
no MESA_VK_WSI_DEBUG=sw
no --disable-zero-copy
no --disable-gpu-rasterization
--disable-gpu-vsync
```

The application started successfully.

The verification command was:

```bash
LOG="$HOME/.cache/mscode/mscode-vulkan-direct-novsync.log"

grep -ciE \
'vkCreateSwapchainKHR\(\) failed|EGL_BAD_SURFACE|GPU process exited|GPU process has crashed|GrContext creation failed|SharedImageStub' \
"$LOG"
```

Observed output:

```text
0
```

A second command:

```bash
grep -iE \
'Started local extension host|Completed initializing default profile extensions|GPU process|EGL_BAD_SURFACE|vkCreateSwapchainKHR|GrContext|SharedImage' \
"$LOG" | tail -120
```

produced:

```text
[12957:0703/024314.218831:INFO:CONSOLE:442]
"%c INFO color: #33f Started local extension host with pid 13259.",
source:
vscode-file://vscode-app/data/data/com.termux/files/home/opt/VSCode-linux-arm64/resources/app/out/vs/workbench/workbench.desktop.main.js
```

The application window was operational, and the previous failure signatures were absent.

This changed the status of every workaround:

```text
MESA_VK_WSI_DEBUG=sw
  useful diagnostic and fallback
  not required

proxy child-window shim
  critical diagnostic tool
  functional workaround
  not required for final use

swapchain mutation shims
  not required

extension filtering
  not required

Zink
  not required

--disable-zero-copy
  not required

--disable-gpu-rasterization
  not required

window-size forcing
  not required

scale-factor forcing
  not required
```

The final minimal behavioral workaround was:

```text
--disable-gpu-vsync
```

in addition to the Vulkan-selection flags.

---

# 20. Final Interpretation

The evidence supports the following interpretation.

## Established facts

The investigation directly established that:

```text
1. Turnip detects and uses Adreno 730.

2. Pure Vulkan XCB WSI works.

3. The relevant swapchain image usage combinations work externally.

4. Large swapchain extents work externally.

5. ANGLE-like device extension combinations work externally.

6. ANGLE-like multi-device creation order works externally.

7. The actual VS Code X11 window works from an external Vulkan connection.

8. A clean child window works inside the GPU process connection.

9. The original window works directly when Chromium GPU vsync is disabled.
```

## Strongest causal interpretation

The most coherent explanation is:

```text
Chromium GPU-process X11 vsync / Present timing behavior
interacts badly with the original Electron drawable in this environment,
and that interaction causes Mesa Vulkan WSI swapchain initialization to fail.

--disable-gpu-vsync prevents that conflicting path from being used,
allowing direct ANGLE Vulkan swapchain initialization on the original window.
```

However, the exact low-level call sequence was not instrumented down to individual:

```text
xcb_present_select_input
DRI3 requests
special XGE event registration
Present event IDs
drawable registration structures
```

Therefore the report does **not** claim that one specific Mesa or Chromium function was proven to be defective.

The correct level of certainty is:

> `--disable-gpu-vsync` is experimentally demonstrated to remove the failure, and the preceding matrix strongly implicates a Chromium GPU-process vsync/Present interaction with the original X11 drawable.

That is stronger than correlation by random flag testing because the conclusion was reached after controlling both the X11 window and connection context independently.

---

# 21. Final Production Configuration

The final production objective was:

```text
maximum effect
minimum special conditions
```

The GPU-specific flags retained were:

```text
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
--disable-gpu-vsync
```

No experimental geometry flags were needed.

The final path did **not** require:

```text
--window-size=...
--force-device-scale-factor=...
MESA_VK_WSI_DEBUG=sw
proxy LD_PRELOAD
--disable-zero-copy
--disable-gpu-rasterization
--disable-gpu
--disable-gpu-compositing
```

A minimal practical wrapper structure was:

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -u

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
HOME="${HOME:-/data/data/com.termux/files/home}"
TMPDIR="${TMPDIR:-$PREFIX/tmp}"

unset LD_LIBRARY_PATH
unset LD_PRELOAD
unset MESA_VK_WSI_DEBUG
unset MESA_LOADER_DRIVER_OVERRIDE
unset GALLIUM_DRIVER
unset LIBGL_DRIVERS_PATH
unset LIBGL_KOPPER_DRI2
unset __GLX_VENDOR_LIBRARY_NAME

VSCODE_DIR="$HOME/opt/VSCode-linux-arm64"
MESA_PREFIX="$HOME/opt/mesa-26-glibc"
DEB_LIBS="$HOME/opt/debian-arm64-libs/usr/lib/aarch64-linux-gnu"
ICD="$MESA_PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json"

MSCODE_LD="$PREFIX/glibc/lib:$MESA_PREFIX/lib:$VSCODE_DIR:$DEB_LIBS"

DISPLAY="${DISPLAY:-:1}"
XDG_RUNTIME_DIR="$TMPDIR"
SHELL="$PREFIX/bin/bash"

exec glibc-runner --no-linker "$PREFIX/glibc/bin/env" \
  LD_LIBRARY_PATH="$MSCODE_LD" \
  DISPLAY="$DISPLAY" \
  XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR" \
  SHELL="$SHELL" \
  VK_ICD_FILENAMES="$ICD" \
  VK_DRIVER_FILES="$ICD" \
  FONTCONFIG_PATH="$HOME/.config/mscode-fontconfig" \
  FONTCONFIG_FILE="$HOME/.config/mscode-fontconfig/fonts.conf" \
  NO_AT_BRIDGE=1 \
  GSETTINGS_BACKEND=memory \
  SSL_CERT_FILE="$PREFIX/etc/tls/cert.pem" \
  SSL_CERT_DIR="$HOME/.config/mscode-certs" \
  NODE_EXTRA_CA_CERTS="$PREFIX/etc/tls/cert.pem" \
  GIT_SSL_CAINFO="$PREFIX/etc/tls/cert.pem" \
  CURL_CA_BUNDLE="$PREFIX/etc/tls/cert.pem" \
  REQUESTS_CA_BUNDLE="$PREFIX/etc/tls/cert.pem" \
  "$VSCODE_DIR/code" \
    --no-sandbox \
    --disable-dev-shm-usage \
    --disable-gpu-sandbox \
    --password-store=basic \
    --ozone-platform=x11 \
    --ignore-gpu-blocklist \
    --enable-features=Vulkan \
    --use-gl=angle \
    --use-angle=vulkan \
    --disable-gpu-vsync \
    --user-data-dir="$HOME/.vscode-ms-data-vulkan" \
    "$@"
```

The ordering of the library path was intentional:

```text
$PREFIX/glibc/lib
$MESA_PREFIX/lib
$VSCODE_DIR
$DEB_LIBS
```

The outer native Termux shell remained free of the glibc target's `LD_LIBRARY_PATH`.

---

# 22. X11 Transport Simplification

During earlier bring-up, TCP X11 had been used as a compatibility workaround:

```text
termux-x11 :1 -listen tcp -ac
DISPLAY=127.0.0.1:1
```

This was initially useful because of uncertainty around the glibc application's access to the Termux:X11 local socket path.

Later testing established that the working glibc-runner configuration could use:

```text
DISPLAY=:1
```

directly.

Therefore the final GPU configuration did not require TCP X11.

The production arrangement could use:

```bash
termux-x11 :1
```

rather than:

```bash
termux-x11 :1 -listen tcp -ac
```

This simplification was independent of the Vulkan swapchain fix. The direct Vulkan failure occurred **after XCB surface creation succeeded**, proving that the major GPU problem was not an inability to connect to the X server.

---

# 23. Non-GPU Side Issue: Shell Environment Resolution

One unrelated warning remained visible during several GPU experiments:

```text
Unable to resolve your shell environment:
Unexpected exit code from spawned shell
(code 1, signal null)
```

This appeared independently of the Vulkan swapchain problem.

In one failed direct Vulkan run it appeared immediately before the swapchain call, but the Vulkan diagnosis showed that the actual GPU failure was the subsequent `vkCreateSwapchainKHR result=-3`; the shell warning was not itself the GPU root cause.

Likewise, successful proxy runs could create swapchains even while the same shell-environment warning was still present, further separating the two problems.

For production use, shell environment handling should therefore be cleaned separately from GPU configuration.

---

# 24. Final Experimental Progression

The complete GPU progression can be summarized as:

```text
Stage 0
CPU-only VS Code
Result: stable

Stage 1
Generic Chromium GPU mode
Result: EGL/OpenGL initialization failure

Stage 2
Direct ANGLE Vulkan
Result:
  XCB surface success
  swapchain -3
  GPU process restart

Stage 3
Pure Vulkan controls
Result:
  Vulkan GPU works
  XCB WSI works
  swapchains work

Stage 4
Swapchain mutation experiments
Result:
  failure persists

Stage 5
Extension and feature filtering
Result:
  failure persists or breaks other contexts

Stage 6
Zink experiments
Result:
  partial behavior
  blank/gray or software-composited fallback
  not final solution

Stage 7
MESA_VK_WSI_DEBUG=sw
Result:
  VS Code displays successfully
  proves usable Vulkan GPU rendering path
  final presentation uses software-copy WSI mode

Stage 8
External minimal swapchain matrix
Result:
  usage 0x10 success
  usage 0x17 success
  usage 0x97 success

Stage 9
ANGLE-like device profiles
Result:
  basic success
  angle24 success
  angle54 success
  angle54→angle24 success

Stage 10
Foreign VS Code window probe
Result:
  actual VS Code window succeeds externally

Stage 11
Proxy child-window shim
Result:
  same GPU-process connection
  clean child window
  swapchain success
  visible application success

Stage 12
Re-enable zero-copy Chromium flag
Result:
  success

Stage 13
Re-enable GPU rasterization
Result:
  success

Stage 14
Remove proxy
Add --disable-gpu-vsync
Result:
  direct original-window path succeeds
  failure count = 0

Final
Direct ANGLE Vulkan
No proxy
No sw WSI force
No zero-copy disable
No GPU-raster disable
Only GPU-specific workaround:
  --disable-gpu-vsync
```

---

# 25. Final Result

The final verified operational architecture was:

```text
Official Microsoft VS Code ARM64
        │
        ▼
Electron / Chromium
        │
        │ --enable-features=Vulkan
        │ --use-gl=angle
        │ --use-angle=vulkan
        │ --disable-gpu-vsync
        ▼
ANGLE Vulkan
        │
        ▼
glibc Vulkan runtime
        │
        ▼
Mesa Turnip KGSL
        │
        ▼
Adreno 730
        │
        ▼
Mesa default WSI mode
        │
        ▼
Termux:X11 via DISPLAY=:1
```

The final solution did not require:

```text
proot
chroot
VNC
TCP X11
proxy window shim
software WSI force
GPU rasterization disable
zero-copy disable
fixed window size
fixed scale factor
```

---

# 26. Caveats

Two claims are intentionally **not** made.

First, the experiments proved success in Mesa's default WSI mode without:

```text
MESA_VK_WSI_DEBUG=sw
```

but they did not instrument every X11 request deeply enough to prove that every frame was presented through a specific DRI3/dmabuf path.

Second, the experiments did not prove complete end-to-end zero-copy presentation. Removal of `--disable-zero-copy` shows that Chromium's zero-copy feature was not explicitly disabled, but that is not equivalent to proving that every buffer transfer in the complete presentation path was zero-copy.

The appropriately restrained conclusion is:

> Direct ANGLE Vulkan acceleration on the real Adreno 730 was enabled successfully in official Microsoft VS Code under native Termux. The application ran on the original Electron X11 window without proxy substitution and without forcing Mesa's software-copy WSI mode. The minimum experimentally demonstrated GPU-specific workaround was `--disable-gpu-vsync`.

---

# 27. Main Engineering Conclusion

The most important lesson from the investigation was that the initial swapchain failure was misleading.

The problem was **not** solved by:

```text
changing Mesa image usage
changing window size
removing pNext chains
simplifying device features
removing dmabuf extensions
changing visual/depth
using an Xlib translation shim
forcing Zink
```

Instead, the successful investigation path was:

```text
prove pure Vulkan works
→ reproduce ANGLE's Vulkan choices externally
→ test the actual Electron window externally
→ hold connection constant and replace only the window
→ prove child-window success
→ infer a connection×window interaction
→ disable Chromium GPU vsync
→ remove the proxy
→ confirm zero failure signatures
```

The final result was much simpler than the diagnostic path that led to it:

```text
Maximum effect, minimum condition:

ANGLE Vulkan
+ Turnip KGSL
+ Adreno 730
+ --disable-gpu-vsync
```

That is the production conclusion of the GPU enablement work.
