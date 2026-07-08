# Termux Chromium and Code OSS WebGPU Enablement Experiments

## 1. Purpose

This report documents the WebGPU enablement experiments performed **after conventional GPU acceleration had already been successfully enabled** in both:

- Termux Chromium, and
- Termux Code OSS / Electron.

The purpose of the experiments was to determine whether the WebGPU implementation used by Chromium and Electron could expose the native Qualcomm Adreno 730 GPU through Mesa Turnip/Freedreno, instead of falling back to SwiftShader.

The experiments progressively investigated:

1. whether the WebGPU JavaScript API was exposed;
2. whether a WebGPU adapter could be obtained;
3. which adapter was actually selected;
4. whether unsafe/developer WebGPU flags changed adapter selection;
5. whether native Vulkan could be forced;
6. whether software fallback could be disabled;
7. whether the Dawn OpenGLES backend could provide an alternative path;
8. whether Chromium's WebGPU-on-Vulkan/GL interop path could be forced;
9. whether the Vulkan ICD environment reached the GPU process;
10. whether the GPU process actually loaded Turnip/Freedreno;
11. whether the problem was specific to Electron;
12. whether the same hardware could expose a native WebGPU adapter in Android Edge.

The final result is:

> **Termux Chromium and Termux Code OSS successfully use native Adreno 730 acceleration through ANGLE Vulkan and Mesa Turnip, but their Dawn WebGPU implementation does not expose the Turnip device as a native WebGPU adapter.**
>
> **WebGPU either falls back to SwiftShader or reports no available adapter when software fallback is prevented or native paths are forced.**
>
> **The same physical GPU is successfully exposed as a non-fallback Qualcomm `adreno-7xx` WebGPU adapter in Android Edge.**
>
> Therefore, the observed limitation is not an Adreno 730 hardware limitation and not a general Vulkan failure. The evidence points toward a compatibility or integration problem at the **Chromium/Dawn WebGPU ↔ Linux/X11-style Termux graphics stack ↔ Mesa Turnip/Freedreno** boundary.

---

# 2. Test Environment

## 2.1 Hardware and native graphics stack

```text
Architecture:
aarch64

GPU:
Qualcomm Adreno 730

Kernel GPU interface:
/dev/kgsl-3d0

Native Vulkan driver:
Mesa Turnip / Freedreno

Display:
Termux:X11
```

The native Vulkan ICD used throughout the experiments was:

```text
/data/data/com.termux/files/usr/share/vulkan/icd.d/freedreno_icd.aarch64.json
```

The ICD file contents were:

```json
{
    "ICD": {
        "api_version": "1.4.335",
        "library_arch": "64",
        "library_path": "/data/data/com.termux/files/usr/lib/libvulkan_freedreno.so"
    },
    "file_format_version": "1.0.1"
}
```

The Termux Chromium package used during the comparison was version `149.0.7827.155`.

Its build configuration explicitly enables the X11 Ozone platform and ANGLE Vulkan:

```text
use_ozone = true
ozone_auto_platforms = false
ozone_platform = "x11"
ozone_platform_x11 = true
angle_enable_vulkan = true
angle_enable_swiftshader = true
```

The Code OSS package uses `electron-for-code-oss`, whose Electron build similarly enables X11 Ozone and ANGLE Vulkan.

---

# 3. Starting Point: Conventional GPU Acceleration Was Already Working

The WebGPU experiments did **not** begin from a software-rendered Chromium or Electron session.

Before investigating WebGPU, conventional GPU acceleration had already been successfully established.

The intended graphics path was:

```text
Chromium / Electron
        │
        ▼
ANGLE Vulkan
        │
        ▼
Vulkan loader
        │
        ▼
Mesa Turnip / Freedreno
        │
        ▼
/dev/kgsl-3d0
        │
        ▼
Adreno 730
```

For Code OSS, the GPU process was inspected directly.

Command:

```bash
pgrep -af -- '--type=gpu-process'
```

Observed output:

```text
19371 /proc/self/exe --type=gpu-process --disable-seccomp-filter-sandbox --disable-gpu-sandbox --no-sandbox --enable-gpu-rasterization --ozone-platform=x11 --use-angle=vulkan --crashpad-handler-pid=0 --enable-crash-reporter=1b9920b0-d9a2-4bc0-bda5-c9dac5bc97ee,no_channel --user-data-dir=/data/data/com.termux/files/home/.config/Code - OSS --gpu-preferences=UAAAAAAAAAAgAAAMAAAAAAAAAAAAAGAAAgAAAAIAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAYAAAAAAAAABgAAAAAAAAAAQAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --use-gl=angle --shared-files --field-trial-handle=3,i,5685748621645750225,6978020166212001749,262144 --enable-features=DocumentPolicyIncludeJSCallStacksInCrashReports,EarlyEstablishGpuChannel,EstablishGpuChannelAsync,PdfUseShowSaveFilePicker,Vulkan --disable-features=CalculateNativeWinOcclusion,LocalNetworkAccessChecks,ScreenAIOCREnabled,SpareRendererForSitePerProcess,TraceSiteInstanceGetProcessCreation --variations-seed-version --trace-process-track-uuid=3190708993808206286
```

The relevant switches were:

```text
--type=gpu-process
--enable-gpu-rasterization
--ozone-platform=x11
--use-angle=vulkan
--use-gl=angle
--enable-features=...,Vulkan
```

This established that the Code OSS GPU process was running with the intended ANGLE Vulkan configuration.

The important distinction for the remainder of this report is:

```text
Electron/Chromium compositor acceleration:
working

ANGLE Vulkan:
working

Turnip native Vulkan:
working

WebGPU native adapter:
separate question
```

---

# 4. Initial Code OSS WebGPU Failure

Code OSS was configured to try its experimental GPU-accelerated editor renderer.

The initial visible error was:

```text
This browser supports WebGPU but it appears to be disabled
```

This distinction was important.

The VS Code WebGPU initialization code distinguishes between:

```text
navigator.gpu absent
→ browser does not support WebGPU

navigator.gpu present, but requestAdapter() fails
→ browser supports WebGPU but it appears to be disabled
```

Therefore, the initial problem was not simply the absence of the WebGPU API.

---

# 5. Experiment 1: Checking WebGPU API Exposure

The Code OSS Developer Tools console was opened.

Input:

```js
navigator.gpu
```

Observed result:

```text
GPU
```

Therefore:

```text
WebGPU JavaScript API exposure:
SUCCESS
```

The browser context contained `navigator.gpu`.

The next step was to request an adapter.

Input:

```js
await navigator.gpu.requestAdapter()
```

A `GPUAdapter` object was returned.

Inspection of the adapter showed:

```text
architecture: "swiftshader"
vendor: "google"
isFallbackAdapter: true
```

This was the first major result.

The actual WebGPU path was:

```text
Code OSS editor WebGPU
        │
        ▼
Dawn WebGPU
        │
        ▼
SwiftShader Vulkan
        │
        ▼
CPU software implementation
```

rather than:

```text
Code OSS editor WebGPU
        │
        ▼
Dawn Vulkan backend
        │
        ▼
Mesa Turnip
        │
        ▼
Adreno 730
```

Therefore:

```text
WebGPU API:
SUCCESS

WebGPU adapter creation:
SUCCESS

Native GPU adapter:
FAILURE

Selected adapter:
SwiftShader fallback
```

---

# 6. Experiment 2: Enabling Unsafe WebGPU

The first attempt to broaden WebGPU availability was to use Chromium's unsafe WebGPU switch.

A representative Code OSS launch configuration was:

```bash
pkill -f 'code-oss|vscode|Code' 2>/dev/null

VK_ICD_FILENAMES="$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json" \
"$PREFIX/lib/code-oss/code-oss" \
  --ignore-gpu-blocklist \
  --enable-gpu-rasterization \
  --enable-zero-copy \
  --enable-features=Vulkan \
  --use-gl=angle \
  --use-angle=vulkan \
  --enable-unsafe-webgpu \
  --ozone-platform=x11 \
  --no-sandbox
```

The WebGPU adapter was then queried again.

Input:

```js
adapter = await navigator.gpu.requestAdapter()
adapter.info
```

Observed adapter information:

```text
architecture: "swiftshader"
vendor: "google"
isFallbackAdapter: true
```

Result:

```text
Unsafe WebGPU API enablement:
SUCCESS

Native Turnip WebGPU:
FAILURE

Fallback:
SwiftShader
```

---

# 7. Experiment 3: Disabling the Software Rasterizer

The next hypothesis was that native Turnip might exist as a valid adapter but be losing priority to SwiftShader.

The software rasterizer was therefore disabled.

Representative launch arguments included:

```text
--enable-unsafe-webgpu
--disable-software-rasterizer
```

The adapter was queried again.

Observed result:

```text
architecture: "swiftshader"
vendor: "google"
isFallbackAdapter: true
```

At this stage, disabling the generic software rasterizer switch did not reliably eliminate the WebGPU SwiftShader fallback path.

This was an early indication that Chromium's WebGPU adapter selection and its general compositor software-rasterizer control were not equivalent mechanisms.

---

# 8. Experiment 4: Forcing Native Vulkan and High-Performance GPU Preference

Chromium contains separate mechanisms for:

- selecting the Vulkan implementation;
- influencing WebGPU power preference;
- requesting a high-performance GPU.

A native/high-performance test was performed with a configuration equivalent to:

```bash
pkill -f 'code-oss|vscode|Code' 2>/dev/null

VK_ICD_FILENAMES="$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json" \
"$PREFIX/lib/code-oss/code-oss" \
  --ignore-gpu-blocklist \
  --enable-gpu-rasterization \
  --enable-zero-copy \
  --enable-features=Vulkan,UnsafeWebGPU \
  --enable-unsafe-webgpu \
  --use-vulkan=native \
  --use-webgpu-power-preference=force-high-performance \
  --force-high-performance-gpu \
  --use-gl=angle \
  --use-angle=vulkan \
  --ozone-platform=x11 \
  --no-sandbox
```

The adapter request was:

```js
adapter = await navigator.gpu.requestAdapter({
    powerPreference: "high-performance"
})
```

Result:

```text
No available adapters.
```

Code OSS emitted:

```text
This browser supports WebGPU but it appears to be disabled
```

This result significantly changed the diagnosis.

The behavior was now:

```text
Normal/default WebGPU path:
→ SwiftShader fallback adapter

Native Vulkan / native-oriented configuration:
→ No available adapters
```

This strongly suggested that the native Turnip device was not merely lower-priority than SwiftShader.

Instead, the native adapter was apparently not available to WebGPU after Dawn's adapter enumeration and acceptance process.

---

# 9. Experiment 5: Native Vulkan with Software Fallback Prevention

Another test combined native Vulkan forcing with software fallback prevention.

Representative launch configuration:

```bash
pkill -f 'code-oss|vscode|Code' 2>/dev/null

VK_ICD_FILENAMES="$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json" \
"$PREFIX/lib/code-oss/code-oss" \
  --ignore-gpu-blocklist \
  --enable-gpu-rasterization \
  --enable-zero-copy \
  --enable-features=Vulkan,UnsafeWebGPU \
  --enable-unsafe-webgpu \
  --use-vulkan=native \
  --disable-software-rasterizer \
  --use-webgpu-power-preference=force-high-performance \
  --force-high-performance-gpu \
  --use-gl=angle \
  --use-angle=vulkan \
  --ozone-platform=x11 \
  --no-sandbox
```

Result:

```text
No available adapters.
```

The cumulative behavior was now:

```text
SwiftShader allowed:
→ SwiftShader adapter

Native-oriented / fallback-restricted configuration:
→ no adapter
```

This became one of the strongest experimental observations of the entire investigation.

---

# 10. Experiment 6: Diagnostic Logging

A diagnostic run was performed with logging enabled.

Representative input:

```bash
pkill -f 'code-oss|vscode|Code' 2>/dev/null

VK_ICD_FILENAMES="$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json" \
"$PREFIX/lib/code-oss/code-oss" \
  --ignore-gpu-blocklist \
  --enable-gpu-rasterization \
  --enable-zero-copy \
  --enable-features=Vulkan,UnsafeWebGPU \
  --enable-unsafe-webgpu \
  --use-vulkan=native \
  --use-webgpu-power-preference=force-high-performance \
  --force-high-performance-gpu \
  --use-gl=angle \
  --use-angle=vulkan \
  --ozone-platform=x11 \
  --no-sandbox \
  --enable-logging=file \
  --log-file="$HOME/.cache/code-oss-webgpu.log" \
  --v=1
```

Log filtering command:

```bash
grep -Ei 'webgpu|dawn|vulkan|swiftshader|adapter|turnip|adreno|disabled|blocklist|fallback' \
  "$HOME/.cache/code-oss-webgpu.log" | tail -200
```

Observed output:

```text
[17961:0702/003101.796175:VERBOSE1:components/viz/service/main/viz_main_impl.cc:86] VizNullHypothesis is disabled (not a warning)
[17922:0702/003111.852503:INFO:CONSOLE:493] "WebGPU is experimental on this platform. See https://github.com/gpuweb/gpuweb/wiki/Implementation-Status#implementation-status", source: vscode-file://vscode-app/data/data/com.termux/files/usr/lib/code-oss/resources/app/out/vs/workbench/workbench.desktop.main.js (493)
[17922:0702/003112.866026:INFO:CONSOLE:0] "No available adapters.", source: vscode-file://vscode-app/data/data/com.termux/files/usr/lib/code-oss/resources/app/out/vs/code/electron-browser/workbench/workbench.html (0)
[17922:0702/003113.488513:INFO:CONSOLE:414] "%c  ERR color: #f33 This browser supports WebGPU but it appears to be disabled: Error: This browser supports WebGPU but it appears to be disabled
```

The most important line was:

```text
No available adapters.
```

The logging configuration did not reveal a low-level Dawn rejection reason, but it confirmed the browser-side outcome.

---

# 11. Experiment 7: Forcing the Dawn OpenGLES Adapter

Chromium provides a `--use-webgpu-adapter` switch.

The Chromium parser accepts:

```text
default
d3d11
opengles
swiftshader
```

There is no explicit `vulkan` value for this switch.

An OpenGLES WebGPU test was therefore performed.

Representative launch configuration:

```bash
pkill -f 'code-oss|vscode|Code' 2>/dev/null

VK_ICD_FILENAMES="$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json" \
"$PREFIX/lib/code-oss/code-oss" \
  --ignore-gpu-blocklist \
  --enable-gpu-rasterization \
  --enable-zero-copy \
  --enable-features=Vulkan,UnsafeWebGPU \
  --enable-unsafe-webgpu \
  --enable-webgpu-developer-features \
  --use-webgpu-adapter=opengles \
  --use-webgpu-power-preference=force-high-performance \
  --force-high-performance-gpu \
  --use-gl=angle \
  --use-angle=vulkan \
  --ozone-platform=x11 \
  --no-sandbox \
  --enable-logging=file \
  --log-file="$HOME/.cache/code-oss-webgpu-opengles.log" \
  --v=1
```

Log query:

```bash
grep -Ei 'webgpu|dawn|vulkan|swiftshader|adapter|turnip|adreno|disabled|blocklist|fallback|opengles' \
  "$HOME/.cache/code-oss-webgpu-opengles.log" | tail -200
```

Observed output:

```text
[20854:0702/003345.233062:VERBOSE1:components/viz/service/main/viz_main_impl.cc:86] VizNullHypothesis is disabled (not a warning)
[20806:0702/003357.323191:INFO:CONSOLE:493] "WebGPU is experimental on this platform. See https://github.com/gpuweb/gpuweb/wiki/Implementation-Status#implementation-status", source: vscode-file://vscode-app/data/data/com.termux/files/usr/lib/code-oss/resources/app/out/vs/workbench/workbench.desktop.main.js (493)
[20806:0702/003358.292909:INFO:CONSOLE:0] "No available adapters.", source: vscode-file://vscode-app/data/data/com.termux/files/usr/lib/code-oss/resources/app/out/vs/code/electron-browser/workbench/workbench.html (0)
[20806:0702/003358.967658:INFO:CONSOLE:414] "%c  ERR color: #f33 This browser supports WebGPU but it appears to be disabled: Error: This browser supports WebGPU but it appears to be disabled
```

Result:

```text
Dawn OpenGLES adapter path:
FAILURE

Available adapter:
none
```

Therefore an alternative route resembling:

```text
Dawn OpenGLES
→ ANGLE
→ Vulkan
→ Turnip
```

could not be established.

---

# 12. Experiment 8: Force-Enabling WebGPU Vulkan/GL Interop

Chromium exposed the following experimental flag:

```text
Force enable WebGPU interop

Force enable the WebGPU on vulkan via GL compositing interop. – Linux

#force-enable-webgpu-interop
```

This was particularly interesting because the Termux environment already had:

```text
ANGLE Vulkan:
working

Vulkan compositing:
working

native Turnip:
working
```

The test launch configuration was:

```bash
VK_ICD_FILENAMES="$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json" \
"$PREFIX/lib/code-oss/code-oss" \
  --ignore-gpu-blocklist \
  --enable-gpu-rasterization \
  --enable-zero-copy \
  --enable-features=Vulkan,WebGPUService,ForceEnableWebGpuInterop \
  --enable-unsafe-webgpu \
  --enable-webgpu-developer-features \
  --use-vulkan=native \
  --use-webgpu-power-preference=force-high-performance \
  --force-high-performance-gpu \
  --use-gl=angle \
  --use-angle=vulkan \
  --ozone-platform=x11 \
  --no-sandbox \
  --enable-logging=file \
  --log-file="$HOME/.cache/code-oss-webgpu-interop.log" \
  --v=1
```

Log query:

```bash
grep -Ei 'webgpu|dawn|vulkan|swiftshader|adapter|turnip|adreno|disabled|blocklist|fallback|interop|opengles' \
  "$HOME/.cache/code-oss-webgpu-interop.log" | tail -250
```

Observed output:

```text
[5310:0702/005153.105450:VERBOSE1:components/viz/service/main/viz_main_impl.cc:86] VizNullHypothesis is disabled (not a warning)
[5247:0702/005204.063418:INFO:CONSOLE:0] "No available adapters.", source: vscode-file://vscode-app/data/data/com.termux/files/usr/lib/code-oss/resources/app/out/vs/code/electron-browser/workbench/workbench.html (0)
[5247:0702/005204.681353:INFO:CONSOLE:414] "%c  ERR color: #f33 This browser supports WebGPU but it appears to be disabled: Error: This browser supports WebGPU but it appears to be disabled
```

Result:

```text
Forced Vulkan/GL WebGPU interop:
FAILURE

Native adapter:
not exposed

WebGPU:
No available adapters
```

The interop flag therefore did not solve the native adapter problem.

---

# 13. Experiment 9: Confirming Vulkan ICD Propagation into the GPU Process

One possible explanation was that Code OSS received the Vulkan environment in the browser process but failed to propagate it into the GPU process.

This was tested directly.

Input:

```bash
gpu_pid=$(pgrep -n -f -- '--type=gpu-process')
```

```bash
echo "GPU PID=$gpu_pid"
```

Observed output:

```text
GPU PID=5310
```

The GPU process environment was then inspected.

Input:

```bash
tr '\0' '\n' < /proc/$gpu_pid/environ | grep -E 'VK|MESA|LD_LIBRARY_PATH'
```

Observed output:

```text
VK_ICD_FILENAMES=/data/data/com.termux/files/usr/share/vulkan/icd.d/freedreno_icd.aarch64.json
```

Result:

```text
VK_ICD_FILENAMES inherited by GPU process:
YES
```

This excluded a simple environment propagation failure.

---

# 14. Experiment 10: Inspecting Loaded GPU Libraries and Device Mappings

The GPU process memory mappings were inspected.

Input:

```bash
gpu_pid=$(pgrep -n -f -- '--type=gpu-process')
```

```bash
grep -Ei 'vulkan|swiftshader|freedreno|turnip|kgsl|mesa' \
  /proc/$gpu_pid/maps | sort -u
```

Observed output included:

```text
76e0f5f000-76e135f000 rw-s 00000000 00:11 1365                           /dev/kgsl-3d0
76e1948000-76e1d48000 rw-s 00000000 00:11 1365                           /dev/kgsl-3d0
76e2e46000-76e3246000 rw-s 00000000 00:11 1365                           /dev/kgsl-3d0
76e3346000-76e3746000 rw-s 00000000 00:11 1365                           /dev/kgsl-3d0
76e3746000-76e3b46000 rw-s 00000000 00:11 1365                           /dev/kgsl-3d0
76e3c46000-76e4046000 rw-s 00000000 00:11 1365                           /dev/kgsl-3d0
76e5144000-76e5544000 rw-s 00000000 00:11 1365                           /dev/kgsl-3d0
```

SwiftShader was loaded:

```text
76e5907000-76e68b4000 r-xp 00000000 fe:3a 2499028                        /data/data/com.termux/files/usr/lib/code-oss/libvk_swiftshader.so
76e68b7000-76e6976000 r--p 00fac000 fe:3a 2499028                        /data/data/com.termux/files/usr/lib/code-oss/libvk_swiftshader.so
76e6979000-76e697a000 rw-p 0106a000 fe:3a 2499028                        /data/data/com.termux/files/usr/lib/code-oss/libvk_swiftshader.so
```

Mesa shader cache mappings were present:

```text
76eac81000-76eae82000 rw-s 00000000 fe:3a 2506469                        /data/data/com.termux/files/home/.cache/mesa_shader_cache/index
76f529b000-76f549c000 rw-s 00000000 fe:3a 2506469                        /data/data/com.termux/files/home/.cache/mesa_shader_cache/index
76f881b000-76f8a1c000 rw-s 00000000 fe:3a 2506469                        /data/data/com.termux/files/home/.cache/mesa_shader_cache/index
```

Most importantly, the native Freedreno Vulkan driver was also loaded:

```text
76f8c2a000-76f98a3000 r-xp 00000000 fe:3a 2501860                        /data/data/com.termux/files/usr/lib/libvulkan_freedreno.so
76f98a6000-76f992e000 r--p 00c78000 fe:3a 2501860                        /data/data/com.termux/files/usr/lib/libvulkan_freedreno.so
76f9931000-76f9935000 rw-p 00cff000 fe:3a 2501860                        /data/data/com.termux/files/usr/lib/libvulkan_freedreno.so
```

The bundled Vulkan loader was present:

```text
76fd247000-76fd2b7000 r-xp 00000000 fe:3a 2276774                        /data/data/com.termux/files/usr/lib/code-oss/libvulkan.so.1
76fd2ba000-76fd2bc000 r--p 0006f000 fe:3a 2276774                        /data/data/com.termux/files/usr/lib/code-oss/libvulkan.so.1
76fd2bf000-76fd2c0000 rw-p 00070000 fe:3a 2276774                        /data/data/com.termux/files/usr/lib/code-oss/libvulkan.so.1
```

Numerous additional KGSL mappings were observed, for example:

```text
79fb616000-79fb636000 rw-s 00000000 00:11 1365                           /dev/kgsl-3d0
7a01ca3000-7a01cc3000 rw-s 00000000 00:11 1365                           /dev/kgsl-3d0
7a01f30000-7a01f50000 rw-s 00000000 00:11 1365                           /dev/kgsl-3d0
...
```

The complete pattern established:

```text
GPU process:
├── bundled Vulkan loader
├── libvk_swiftshader.so
├── libvulkan_freedreno.so
├── Mesa shader cache
└── /dev/kgsl-3d0 mappings
```

This was a critical result.

It demonstrated that:

```text
Native Turnip ICD discovery:
SUCCESS

Native Freedreno Vulkan library loading:
SUCCESS

KGSL GPU device access:
SUCCESS

SwiftShader availability:
YES
```

Therefore, the WebGPU failure could no longer reasonably be explained as:

```text
VK_ICD_FILENAMES missing
Vulkan ICD not found
Turnip library not loaded
KGSL device inaccessible
general Vulkan failure
```

The remaining problem was downstream of Vulkan discovery.

---

# 15. SwiftShader Presence in the Packaged Applications

The observation that SwiftShader was loaded was consistent with the package layouts.

The Termux Chromium package installs:

```text
libvulkan.so.1
libVkICD_mock_icd.so
libvk_swiftshader.so
libVkLayer_khronos_validation.so
vk_swiftshader_icd.json
```

The Electron package used by Code OSS likewise ships Vulkan and SwiftShader components.

Therefore the observed behavior was structurally consistent:

```text
Native Dawn adapter unavailable
        │
        ▼
SwiftShader available
        │
        ▼
WebGPU fallback adapter returned
```

When a test configuration prevented or bypassed that fallback behavior:

```text
No available adapters
```

was observed instead.

---

# 16. Experiment 11: Testing Termux Chromium 149

Until this stage, the main WebGPU experiments had focused on Code OSS / Electron.

A key question was therefore:

> Is this an Electron-specific problem?

Termux Chromium `149.0.7827.155` was used as an independent Chromium-family test.

The Termux package installs its command as:

```text
chromium-browser
```

rather than:

```text
chromium
```

A representative test command was:

```bash
pkill -f 'chromium|chrome' 2>/dev/null

VK_ICD="$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json"

VK_ICD_FILENAMES="$VK_ICD" \
VK_DRIVER_FILES="$VK_ICD" \
chromium-browser \
  --user-data-dir="$HOME/.config/chromium-webgpu-test" \
  --ignore-gpu-blocklist \
  --enable-gpu-rasterization \
  --enable-zero-copy \
  --enable-features=Vulkan,WebGPUService,UnsafeWebGPU,ForceEnableWebGpuInterop \
  --enable-unsafe-webgpu \
  --enable-webgpu-developer-features \
  --use-vulkan=native \
  --use-webgpu-power-preference=force-high-performance \
  --force-high-performance-gpu \
  --use-gl=angle \
  --use-angle=vulkan \
  --ozone-platform=x11 \
  --no-sandbox
```

Chromium's WebGPU-related experiments page contained:

```text
Force enable WebGPU interop

Force enable the WebGPU on vulkan via GL compositing interop. – Linux

#force-enable-webgpu-interop
```

```text
Unsafe WebGPU Support

Convenience flag for WebGPU development. Enables best-effort WebGPU support on unsupported configurations and more! Note that this flag could expose security issues to websites so only use it for your own development.

#enable-unsafe-webgpu
```

```text
WebGPU Developer Features

Enables web applications to access WebGPU features intended only for use during development.

#enable-webgpu-developer-features
```

When unsafe WebGPU was enabled, Chromium displayed a warning bar similar to:

```text
You are using an unsupported command-line flag: --enable-u...
```

This was interpreted as a warning about the unsafe/development nature of `--enable-unsafe-webgpu`, not as evidence that the switch was ignored.

The Chromium DevTools adapter test was:

```js
adapter = await navigator.gpu.requestAdapter({
    powerPreference: "high-performance"
})

adapter && adapter.info
```

Result:

```text
architecture: "swiftshader"
vendor: "google"
isFallbackAdapter: true
```

Therefore:

```text
Termux Chromium 149 native WebGPU:
FAILURE

Termux Chromium 149 WebGPU:
SwiftShader fallback
```

This was decisive.

The same high-level failure occurred in:

```text
Code OSS / Electron 142
and
Termux Chromium 149
```

Therefore the problem was unlikely to be specific to the Code OSS application layer or to one old Electron release.

---

# 17. Experiment 12: Android Edge as a Control Group

Android Edge 149 was then tested on the same physical device.

User agent:

```text
Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36 EdgA/149.0.0.0
```

WebGPU support result:

```text
This browser supports WebGPU: True
```

The native WebGPU adapter information was:

```text
Supported Adapters: #1

Power Preference: undefined

Is Fallback Adapter: false

Vendor: qualcomm

Architecture: adreno-7xx

Device: empty

Description: empty

Driver: undefined

Backend: undefined

Type: undefined

Memory Heaps: undefined

D3D Shader Model: undefined

Vulkan Driver Version: undefined

Subgroup Max Size: 128
```

Selected adapter limits included:

```text
Max Texture Dimension 1D: 16384
Max Texture Dimension 2D: 16384
Max Texture Dimension 3D: 2048
Max Texture Array Layers: 2048

Max Bind Groups: 4
Max Bind Groups Plus Vertex Buffers: 24
Max Bindings Per Bind Group: 1000

Max Dynamic Uniform Buffers Per Pipeline Layout: 10
Max Dynamic Storage Buffers Per Pipeline Layout: 8

Max Sampled Textures Per Shader Stage: 48
Max Samplers Per Shader Stage: 16
Max Storage Buffers Per Shader Stage: 16
Max Storage Textures Per Shader Stage: 8
Max Uniform Buffers Per Shader Stage: 12

Max Uniform Buffer Binding Size: 65536
Max Storage Buffer Binding Size: 134217728

Max Vertex Buffers: 8
Max Buffer Size: 1073741824
Max Vertex Attributes: 30
Max Vertex Buffer Array Stride: 2048

Max Color Attachments: 8
Max Color Attachment Bytes Per Sample: 128

Max Compute Workgroup Storage Size: 32768
Max Compute Invocations Per Workgroup: 1024
Max Compute Workgroup Size X: 1024
Max Compute Workgroup Size Y: 1024
Max Compute Workgroup Size Z: 64
Max Compute Workgroups Per Dimension: 65535
```

Representative native adapter features included:

```text
core-features-and-limits: True
depth-clip-control: True
depth32float-stencil8: True

texture-compression-bc: True
texture-compression-bc-sliced-3d: True
texture-compression-etc2: True
texture-compression-astc: True
texture-compression-astc-sliced-3d: True

timestamp-query: True
indirect-first-instance: True
shader-f16: True

rg11b10ufloat-renderable: True
float32-blendable: True
clip-distances: True
dual-source-blending: True
subgroups: True
texture-component-swizzle: True

texture-formats-tier1: True
texture-formats-tier2: True
primitive-index: True
```

The critical comparison was:

```text
Android Edge:
vendor = qualcomm
architecture = adreno-7xx
isFallbackAdapter = false

Termux Chromium:
vendor = google
architecture = swiftshader
isFallbackAdapter = true

Code OSS:
SwiftShader fallback
or
No available adapters
```

Therefore the Adreno 730 hardware itself is demonstrably WebGPU-capable.

---

# 18. Comparative Graphics Paths

## 18.1 Android Edge

The working Android Edge path can be modeled as:

```text
Android Edge
        │
        ▼
Chromium Android platform build
        │
        ▼
Dawn WebGPU Android integration
        │
        ▼
Android Vulkan graphics stack
        │
        ▼
Qualcomm GPU driver
        │
        ▼
Adreno 7xx
```

Observed result:

```text
Native WebGPU adapter:
YES

Fallback:
NO

Vendor:
qualcomm

Architecture:
adreno-7xx
```

---

## 18.2 Termux Chromium

```text
Termux Chromium
        │
        ▼
Chromium X11/Ozone configuration
        │
        ▼
Termux:X11
        │
        ├── ANGLE Vulkan
        │       │
        │       ▼
        │   Turnip/Freedreno
        │       │
        │       ▼
        │   Adreno 730
        │
        └── Dawn WebGPU
                │
                ├── native Turnip adapter: unavailable
                │
                └── SwiftShader fallback
```

---

## 18.3 Termux Code OSS

```text
Code OSS
        │
        ▼
Electron / Chromium
        │
        ├── GPU compositor
        │       │
        │       ▼
        │   ANGLE Vulkan
        │       │
        │       ▼
        │   Turnip/Freedreno
        │       │
        │       ▼
        │   Adreno 730
        │       │
        │       └── SUCCESS
        │
        └── Editor WebGPU renderer
                │
                ▼
            Dawn WebGPU
                │
                ├── native Turnip: unavailable
                │
                ├── SwiftShader: available
                │
                └── fallback disabled: no adapter
```

---

# 19. What the Experiments Ruled Out

The accumulated experiments ruled out several simple explanations.

## 19.1 Not a general Vulkan failure

Native Vulkan was already working through Turnip.

The GPU process loaded:

```text
libvulkan_freedreno.so
```

and accessed:

```text
/dev/kgsl-3d0
```

Therefore:

```text
Vulkan device access:
working
```

---

## 19.2 Not an ANGLE Vulkan failure

Both Chromium and Code OSS were successfully running with:

```text
--use-gl=angle
--use-angle=vulkan
--enable-features=...,Vulkan
```

Therefore:

```text
ANGLE Vulkan:
working
```

---

## 19.3 Not a missing Vulkan ICD environment variable

The Code OSS GPU process environment explicitly contained:

```text
VK_ICD_FILENAMES=/data/data/com.termux/files/usr/share/vulkan/icd.d/freedreno_icd.aarch64.json
```

Therefore:

```text
ICD propagation to GPU process:
working
```

---

## 19.4 Not failure to load the native driver

The GPU process maps contained:

```text
/data/data/com.termux/files/usr/lib/libvulkan_freedreno.so
```

Therefore:

```text
native Turnip/Freedreno Vulkan driver loading:
working
```

---

## 19.5 Not an Electron-only problem

Termux Chromium 149 reproduced the same WebGPU fallback behavior.

Therefore:

```text
Electron-specific failure:
unlikely
```

---

## 19.6 Not a hardware WebGPU limitation

Android Edge exposed:

```text
vendor: qualcomm
architecture: adreno-7xx
isFallbackAdapter: false
```

Therefore:

```text
Adreno 730 WebGPU capability:
confirmed through Android browser stack
```

---

# 20. Most Likely Failure Boundary

Based on the evidence, the problem boundary can be narrowed to:

```text
Chromium / Dawn WebGPU
        ↕
Linux/X11-style Chromium platform integration
        ↕
Termux:X11 graphics environment
        ↕
Mesa Turnip/Freedreno
```

The exact subcomponent has **not** yet been proven.

Plausible candidates include:

```text
Dawn Vulkan adapter validation

required WebGPU feature or limit negotiation

shared-image interoperability

Vulkan ↔ GL compositing interoperability

shared texture memory support

external memory requirements

semaphore or sync-fd interoperability

GPU buffer sharing across the compositor/WebGPU boundary

platform classification and build-time assumptions

Termux-specific Bionic/X11 integration differences
```

These are hypotheses, not confirmed root causes.

The confirmed observation is narrower:

> **Dawn does not expose the already functional Turnip Vulkan device as a native WebGPU adapter in the tested Termux Chromium and Electron environments.**

---

# 21. Result Matrix

| Experiment | Code OSS / Electron | Chromium 149 |
|---|---|---|
| ANGLE Vulkan | Success | Success |
| Native Turnip Vulkan | Success | Success |
| `navigator.gpu` | Present | Present |
| Default WebGPU adapter | SwiftShader | SwiftShader |
| `--enable-unsafe-webgpu` | SwiftShader | SwiftShader |
| High-performance preference | No native adapter | SwiftShader or no native adapter |
| `--use-vulkan=native` | No available adapters | No native Turnip WebGPU adapter |
| Software fallback restriction | No available adapters in native-oriented tests | No native adapter |
| `--use-webgpu-adapter=opengles` | No available adapters | Not useful as native Turnip solution |
| Force WebGPU interop | No available adapters | Did not produce native Turnip adapter |
| Native ICD visible to GPU process | Yes | Native Vulkan independently verified |
| `libvulkan_freedreno.so` loaded | Yes | Native graphics stack functional |
| `/dev/kgsl-3d0` accessed | Yes | Native Vulkan path functional |
| Native WebGPU Adreno | Failure | Failure |
| SwiftShader WebGPU | Available | Available |

Android Edge control:

| Test | Android Edge 149 |
|---|---|
| WebGPU API | Available |
| Adapter | Native Qualcomm |
| Architecture | `adreno-7xx` |
| Fallback | `false` |
| Native GPU WebGPU | Success |

---

# 22. Final Conclusion

The WebGPU experiments establish a clear separation between general Chromium/Electron GPU acceleration and WebGPU device exposure.

The following paths are confirmed working:

```text
Chromium
→ ANGLE Vulkan
→ Turnip/Freedreno
→ Adreno 730
```

and:

```text
Code OSS
→ Electron GPU process
→ ANGLE Vulkan
→ Turnip/Freedreno
→ Adreno 730
```

The following path could not be established:

```text
Chromium / Electron
→ Dawn WebGPU
→ native Vulkan adapter
→ Turnip/Freedreno
→ Adreno 730
```

Instead:

```text
WebGPU default behavior
→ SwiftShader fallback
```

or, under several native-forcing/fallback-restricting configurations:

```text
WebGPU
→ No available adapters
```

The identical high-level failure in both:

```text
Code OSS / Electron 142
and
Termux Chromium 149
```

strongly suggests that the issue is **not specific to Code OSS or Electron**.

The Android Edge control experiment proves that:

```text
Adreno 730 hardware:
WebGPU-capable

Qualcomm Android graphics path:
WebGPU-capable

Termux Turnip Vulkan path:
Vulkan-capable

Termux Chromium/Electron Dawn path:
unable to expose native Turnip WebGPU adapter
```

The most defensible current conclusion is therefore:

> **On the tested Adreno 730 device, Termux native Chromium and Electron applications can achieve full conventional GPU acceleration through ANGLE Vulkan and Mesa Turnip/Freedreno, but Chromium's Dawn WebGPU implementation does not expose the Turnip device as a native WebGPU adapter. SwiftShader is used as the only functioning WebGPU adapter, while native-oriented configurations result in no available adapters. The same GPU works correctly as a native non-fallback WebGPU adapter in Android Edge, indicating that the remaining problem lies in the Chromium/Dawn integration with the Termux X11 and Mesa Turnip/Freedreno stack rather than in the hardware or Vulkan driver access itself.**

---

# 23. Practical Configuration Decision

For the tested environment, the practical configuration was therefore:

```text
XFCE:
compositor disabled for minimum overhead

Chromium:
ANGLE Vulkan enabled
Turnip/Freedreno native Vulkan
WebGPU not relied upon for native GPU execution

Code OSS:
Electron ANGLE Vulkan enabled
editor WebGPU renderer disabled
DOM-based editor rendering used

Global Zink:
not forced

Vulkan ICD:
Freedreno/Turnip explicitly selected
```

The Code OSS editor configuration should therefore avoid SwiftShader WebGPU when performance is the priority:

```json
{
  "editor.experimentalGpuAcceleration": "off"
}
```

This does **not** disable the successful Electron GPU compositor path.

The resulting practical architecture is:

```text
Code OSS application UI
→ GPU accelerated through ANGLE Vulkan / Turnip

Editor text rendering
→ DOM renderer

WebGPU
→ disabled for the editor until native Turnip adapter support becomes available
```

This preserves the successful native GPU acceleration work while avoiding a CPU-based SwiftShader WebGPU renderer.
