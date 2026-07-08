# Native Vulkan GPU Acceleration for Chromium and Code OSS on Termux:X11

## Experimental Report

**Platform:** Native Termux userspace on Android  
**Display stack:** Termux:X11, X11 display `:1`  
**Desktop:** XFCE, ultimately run as a manual component session rather than through `xfce4-session`  
**GPU:** Qualcomm Adreno 730  
**Vulkan driver:** Mesa Turnip / Freedreno  
**Primary applications:** Chromium and Code OSS  
**Objective:** Enable real GPU acceleration through native Vulkan paths without proot/chroot, without VNC, and without globally forcing Zink.

---

## 1. Executive Summary

This experiment successfully established native Vulkan-backed GPU acceleration for Chromium and a Vulkan-targeted Electron launch path for Code OSS in a Termux + Termux:X11 environment on an Adreno 730 device.

The final working Chromium path was:

```text
Chromium
  -> ANGLE Vulkan backend
  -> Mesa Turnip Vulkan driver
  -> Adreno 730
  -> Termux:X11
```

The final confirmed Chromium state included:

```text
Canvas: Hardware accelerated
Compositing: Hardware accelerated
Rasterization: Hardware accelerated on all pages
Vulkan: Enabled
WebGL: Hardware accelerated
WebGPU: Hardware accelerated
Skia Backend: GaneshVulkan
GL implementation parts: (gl=egl-angle,angle=vulkan)
Display type: ANGLE_VULKAN
GPU process crash count: 0
```

The active renderer was:

```text
ANGLE (Qualcomm, Vulkan 1.4.335
(Turnip Adreno (TM) 730 (0x07030001)),
turnip Mesa driver-538.0.6)
```

The final Chromium launch policy was injected through the session environment:

```bash
export CHROMIUM_FLAGS="--ignore-gpu-blocklist --enable-gpu-rasterization --enable-zero-copy --enable-accelerated-video-decode --enable-features=Vulkan --use-gl=angle --use-angle=vulkan"
```

The Vulkan ICD was constrained to Freedreno/Turnip:

```bash
export VK_ICD_FILENAMES="$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json"
```

Code OSS was then accelerated through the same general architectural idea: request ANGLE Vulkan rather than relying on a desktop-wide OpenGL-over-Zink policy. Direct launch testing succeeded, command-line switch propagation succeeded, and the central Code OSS launcher was patched so that the GUI Electron binary was executed directly with the Vulkan-related switches.

The final Code OSS target path was:

```text
Code OSS
  -> Electron / Chromium graphics stack
  -> ANGLE Vulkan
  -> Mesa Turnip
  -> Adreno 730
  -> Termux:X11
```

A major finding was that **global Zink forcing is not a safe desktop-wide policy** in this environment. Globally exporting:

```bash
MESA_LOADER_DRIVER_OVERRIDE=zink
```

caused XFCE display/session instability, including a black screen and repeated `xfwm4` GLib critical errors. The final configuration therefore uses:

- native Turnip Vulkan selection globally for Vulkan-aware applications,
- ANGLE Vulkan explicitly for Chromium and Code OSS,
- no desktop-wide Zink override.

---

## 2. Scope and Design Constraints

The experiment was performed under these constraints:

1. No proot.
2. No chroot.
3. No VNC rendering path.
4. Native Termux packages where possible.
5. Termux:X11 as the display server.
6. Mesa Turnip/Freedreno as the Vulkan driver.
7. Prefer direct Vulkan paths over OpenGL-over-Zink when the application supports them.
8. Avoid global environment policies that destabilize unrelated desktop applications.
9. Preserve normal CLI behavior where practical.
10. Prefer transparent, inspectable launch mechanisms rather than opaque wrappers.

The work focused on two related but distinct application families:

- Chromium itself.
- Code OSS, which is an Electron application and therefore inherits Chromium GPU architecture, but has a different launcher chain.

---

## 3. Graphics Architecture

### 3.1 Vulkan Driver Layer

The device GPU is:

```text
Qualcomm Adreno 730
```

The Vulkan driver used is Mesa Turnip, installed through the Freedreno Vulkan ICD package.

The relevant ICD path was:

```text
/data/data/com.termux/files/usr/share/vulkan/icd.d/freedreno_icd.aarch64.json
```

The environment variable used to select this ICD was:

```bash
VK_ICD_FILENAMES=/data/data/com.termux/files/usr/share/vulkan/icd.d/freedreno_icd.aarch64.json
```

This was important because a software Vulkan ICD was also available. Selecting the Freedreno ICD explicitly prevented accidental routing to the software Vulkan implementation.

### 3.2 Zink

Zink translates OpenGL into Vulkan.

The pre-direct-Vulkan Chromium path observed in the experiment was effectively:

```text
Chromium
  -> ANGLE OpenGL backend
  -> Mesa Zink
  -> Vulkan Turnip
  -> Adreno 730
```

This path did use the real GPU, but it was not the desired final architecture. Direct Vulkan through ANGLE was preferable:

```text
Chromium
  -> ANGLE Vulkan
  -> Turnip
  -> Adreno 730
```

The difference was visible in Chromium GPU diagnostics.

Zink/OpenGL route:

```text
Skia Backend: GaneshGL
GL implementation parts: (gl=egl-angle,angle=opengl)
Display type: ANGLE_OPENGL
GL_RENDERER: ANGLE (Mesa, zink Vulkan 1.4(...), OpenGL 4.6 ...)
```

Direct Vulkan route:

```text
Skia Backend: GaneshVulkan
GL implementation parts: (gl=egl-angle,angle=vulkan)
Display type: ANGLE_VULKAN
GL_RENDERER: ANGLE (Qualcomm, Vulkan 1.4.335 (... Turnip Adreno 730 ...))
```

---

## 4. Desktop Stability Work Before Application GPU Enablement

Before finalizing Chromium and Code OSS acceleration, the desktop session itself had to be stabilized.

### 4.1 Global Zink caused XFCE problems

An early strategy attempted to apply:

```bash
export MESA_LOADER_DRIVER_OVERRIDE=zink
```

to the whole XFCE session.

This caused a black screen and repeated window-manager errors.

Observed process state:

```text
u0_a534@localhost:~/.themes$ pgrep -a xfwm4
29777 xfwm4 --replace

u0_a534@localhost:~/.themes$ pgrep -a xfdesktop
29802 xfdesktop

u0_a534@localhost:~/.themes$ pgrep -a xfce4-panel
29849 xfce4-panel

u0_a534@localhost:~/.themes$ pgrep -a xfce4-session
29687 xfce4-session
```

The processes were alive, but the desktop was not usable.

The `xfwm4` log contained:

```text
(xfwm4:29777): xfwm4-WARNING **:
Failed to connect to session manager:
SESSION_MANAGER environment variable not defined

(xfwm4:29777): GLib-CRITICAL **:
g_hash_table_lookup: assertion 'hash_table != NULL' failed
```

The GLib error repeated many times.

`xfdesktop` also reported:

```text
Failed to connect to session manager:
Failed to connect to the session manager:
SESSION_MANAGER environment variable not defined

WARNING:
Failed to get system bus:
Could not connect: No such file or directory
```

### 4.2 Bare X11 test

The display stack was separated from the XFCE session layer.

The successful bare test was:

```bash
pkill -f 'xfce4-session|xfwm4|xfdesktop|xfce4-panel|xfce4-power-manager|picom|compton|xfce4-terminal' 2>/dev/null
pkill -f 'termux-x11' 2>/dev/null

export DISPLAY=:1
export XDG_RUNTIME_DIR=$TMPDIR

termux-x11 :1 >$HOME/.cache/termux-x11-bare.log 2>&1 &
sleep 2

am start --user 0 \
  -n com.termux.x11/com.termux.x11.MainActivity \
  >/dev/null 2>&1

sleep 2

xfce4-terminal --disable-server &
```

Result:

```text
Bare Termux:X11 + xfce4-terminal: SUCCESS
```

This demonstrated:

```text
Termux:X11 server: working
X11 client mapping: working
Visible application windows: working
```

### 4.3 Manual XFCE component startup

The next successful test bypassed `xfce4-session` and started XFCE components manually:

```bash
pkill -f 'xfce4-session|xfwm4|xfdesktop|xfce4-panel|xfsettingsd|xfce4-power-manager' 2>/dev/null

export DISPLAY=:1
export XDG_RUNTIME_DIR=$TMPDIR
export XDG_CONFIG_DIRS=$PREFIX/etc/xdg

eval "$(dbus-launch --sh-syntax)"

xfsettingsd >/dev/null 2>&1 &
xfwm4 --replace --compositor=off >/dev/null 2>&1 &
sleep 1
xfdesktop >/dev/null 2>&1 &
sleep 1
xfce4-panel >/dev/null 2>&1 &
```

Result:

```text
Manual XFCE startup: SUCCESS
```

This isolated the desktop problem to the session-management layer rather than to Termux:X11, the X11 applications themselves, or the GPU device.

The final desktop policy was:

```text
Termux:X11: clean environment
XFCE: manual component startup
xfwm4 compositor: disabled
Global Zink override: disabled
Turnip Vulkan ICD: selected for applications
```

---

# Part I — Chromium GPU Acceleration

## 5. Chromium Baseline

The Chromium version recorded in the GPU diagnostic files was:

```text
Chrome/149.0.7827.155
```

The operating system string was:

```text
Linux 5.10.236-android12-9-31998796-abS908NKSS9GZE5
```

### 5.1 Initial GPU state

The baseline Chromium command line was:

```text
/data/data/com.termux/files/usr/lib/chromium/chrome
--extra-plugin-dir=/data/data/com.termux/files/usr/lib/nsbrowser/plugins
--no-sandbox
--ozone-platform=x11
--flag-switches-begin
--flag-switches-end
```

Observed feature state:

```text
Canvas: Hardware accelerated
Direct Rendering Display Compositor: Disabled
Compositing: Software only. Hardware acceleration disabled
Multiple Raster Threads: Enabled
OpenGL: Enabled
Rasterization: Hardware accelerated
Raw Draw: Disabled
Skia Graphite: Disabled
TreesInViz: Enabled
Video Decode: Software only. Hardware acceleration disabled
Video Encode: Software only. Hardware acceleration disabled
Vulkan: Disabled
WebGL: Hardware accelerated but at reduced performance
WebGPU: Hardware accelerated but at reduced performance
WebGPU interop: Disabled
WebNN: Disabled
```

Driver information:

```text
Skia Backend: GaneshGL

GPU0:
VENDOR=0x0000 [Google Inc. (Mesa)]

DEVICE=0x0000
[ANGLE (Mesa,
zink Vulkan 1.4
(Turnip Adreno (TM) 730 (MESA_TURNIP)),
OpenGL 4.6 (Core Profile) Mesa 26.0.6)]

DRIVER_VENDOR=Mesa
DRIVER_VERSION=26.0.6
```

Backend identity:

```text
GL implementation parts: (gl=egl-angle,angle=opengl)
Display type: ANGLE_OPENGL
```

This showed that the GPU was accessible, but Chromium was not yet running its compositor and Skia renderer through direct Vulkan.

---

## 6. First Chromium Flag Set: GPU Compositing and Rasterization

The first working performance-oriented flag set was:

```text
--ignore-gpu-blocklist
--enable-gpu-rasterization
--enable-zero-copy
--enable-accelerated-video-decode
```

After applying these flags, Chromium reported:

```text
Canvas: Hardware accelerated
Compositing: Hardware accelerated
Multiple Raster Threads: Enabled
OpenGL: Enabled
Rasterization: Hardware accelerated on all pages
Vulkan: Disabled
WebGL: Hardware accelerated
WebGPU: Hardware accelerated
WebGPU interop: Hardware accelerated
```

The active backend was still:

```text
Skia Backend: GaneshGL
GL implementation parts: (gl=egl-angle,angle=opengl)
Display type: ANGLE_OPENGL
```

The renderer remained:

```text
ANGLE
(Mesa,
 zink Vulkan 1.4
 (Turnip Adreno (TM) 730 (MESA_TURNIP)),
 OpenGL 4.6 (Core Profile) Mesa 26.0.6)
```

Intermediate result:

```text
GPU compositing: SUCCESS
GPU rasterization: SUCCESS
WebGL acceleration: SUCCESS
Direct Vulkan: NOT YET ENABLED
```

---

## 7. Direct Vulkan Attempt Without Correct ICD Environment

The Vulkan-specific switches were added:

```text
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
```

The full effective set was:

```text
--ignore-gpu-blocklist
--enable-gpu-rasterization
--enable-zero-copy
--enable-accelerated-video-decode
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
--ozone-platform=x11
```

Without the correct Vulkan ICD environment, Chromium failed to initialize the GPU path.

Observed status:

```text
Canvas: Software only. Hardware acceleration disabled
Compositing: Software only. Hardware acceleration disabled
Multiple Raster Threads: Disabled
OpenGL: Disabled
Rasterization: Software only. Hardware acceleration disabled
Vulkan: Disabled
WebGL: Disabled
WebGPU: Disabled
```

Driver state:

```text
Initialization time: 0
Skia Backend: None
GPU0: VENDOR=0x0000, DEVICE=0x0000
GL implementation parts: (gl=disabled,angle=none)
```

Problems detected included:

```text
GPU process was unable to boot:
GPU access is disabled due to frequent crashes.
Disabled Features: all
```

Logs also contained:

```text
vk_renderer.cpp:271 (VerifyExtensionsPresent):
Extension not supported: VK_KHR_surface
```

Critical finding:

> Vulkan command-line switches alone were insufficient. The Vulkan loader also had to be directed to the working Turnip/Freedreno ICD.

---

## 8. Successful Chromium Direct Vulkan Configuration

### 8.1 Vulkan ICD selection

Working environment:

```bash
VK_ICD_FILENAMES="$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json"
```

Absolute path:

```text
/data/data/com.termux/files/usr/share/vulkan/icd.d/freedreno_icd.aarch64.json
```

### 8.2 Working Chromium switch set

```text
--ignore-gpu-blocklist
--enable-gpu-rasterization
--enable-zero-copy
--enable-accelerated-video-decode
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
--ozone-platform=x11
```

### 8.3 Successful final Chromium state

Observed feature status:

```text
Canvas: Hardware accelerated
Direct Rendering Display Compositor: Disabled
Compositing: Hardware accelerated
Multiple Raster Threads: Enabled
OpenGL: Enabled
Rasterization: Hardware accelerated on all pages
Raw Draw: Disabled
Skia Graphite: Disabled
TreesInViz: Enabled
Video Decode: Software only. Hardware acceleration disabled
Video Encode: Software only. Hardware acceleration disabled
Vulkan: Enabled
WebGL: Hardware accelerated
WebGPU: Hardware accelerated
WebGPU interop: Disabled
WebNN: Disabled
```

Effective command line:

```text
/data/data/com.termux/files/usr/lib/chromium/chrome
--extra-plugin-dir=/data/data/com.termux/files/usr/lib/nsbrowser/plugins
--ignore-gpu-blocklist
--enable-gpu-rasterization
--enable-zero-copy
--enable-accelerated-video-decode
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
--no-sandbox
--ozone-platform=x11
--flag-switches-begin
--flag-switches-end
```

Driver information:

```text
Initialization time: 256
In-process GPU: false
Skia Backend: GaneshVulkan
Passthrough Command Decoder: true
Sandboxed: false
```

Active GPU:

```text
GPU0:
VENDOR=0x0000 [Google Inc. (Qualcomm)]

DEVICE=0x0000
[ANGLE
(Qualcomm,
 Vulkan 1.4.335
 (Turnip Adreno (TM) 730 (0x07030001)),
 turnip Mesa driver-538.0.6)]

DRIVER_VENDOR=Mesa
DRIVER_VERSION=driver
*ACTIVE*
```

ANGLE and display backend:

```text
GL implementation parts: (gl=egl-angle,angle=vulkan)
Display type: ANGLE_VULKAN
```

Renderer:

```text
GL_VENDOR: Google Inc. (Qualcomm)

GL_RENDERER:
ANGLE
(Qualcomm,
 Vulkan 1.4.335
 (Turnip Adreno (TM) 730 (0x07030001)),
 turnip Mesa driver-538.0.6)
```

GPU process stability:

```text
GPU process crash count: 0
```

Compositor state:

```text
Tile Update Mode: Zero-copy
Partial Raster: Enabled
```

---

## 9. Chromium WebGPU Observation

The successful direct Vulkan report also enumerated a native Turnip adapter in Dawn:

```text
<Integrated GPU> Vulkan backend - Turnip Adreno (TM) 730
```

Status:

```text
[WebGPU Status]
Available
```

The adapter feature list included entries such as:

```text
core-features-and-limits
depth-clip-control
depth32float-stencil8
texture-compression-bc
texture-compression-etc2
texture-compression-astc
timestamp-query
indirect-first-instance
shader-f16
subgroups
```

This means the successful Chromium configuration captured here did more than merely enable top-level GPU features: Dawn exposed the native Turnip Vulkan adapter.

---

## 10. Video Decode Result

Despite passing:

```text
--enable-accelerated-video-decode
```

the final Chromium diagnostics still reported:

```text
Video Decode: Software only. Hardware acceleration disabled
Video Encode: Software only. Hardware acceleration disabled
```

Detailed acceleration section:

```text
Video Acceleration Information
==============================
Decoding:
Encoding:
```

Therefore:

```text
GPU rendering acceleration: SUCCESS
Vulkan rendering: SUCCESS
GPU compositing: SUCCESS
GPU rasterization: SUCCESS
WebGL: SUCCESS
WebGPU: SUCCESS
Hardware video decode: NOT ACHIEVED
Hardware video encode: NOT ACHIEVED
```

This demonstrated that GPU rendering acceleration and media codec acceleration are separate subsystems.

---

## 11. Final Chromium Session Integration

Relevant session policy:

```bash
FREEDRENO_ICD="$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json"

if [ -r "$FREEDRENO_ICD" ]; then
  export VK_ICD_FILENAMES="$FREEDRENO_ICD"
else
  unset VK_ICD_FILENAMES
fi

unset MESA_LOADER_DRIVER_OVERRIDE
unset GALLIUM_DRIVER
unset LIBGL_ALWAYS_SOFTWARE

export CHROMIUM_FLAGS="--ignore-gpu-blocklist --enable-gpu-rasterization --enable-zero-copy --enable-accelerated-video-decode --enable-features=Vulkan --use-gl=angle --use-angle=vulkan"
```

The X server itself was intentionally started with GPU override variables removed:

```bash
env \
  -u VK_ICD_FILENAMES \
  -u MESA_LOADER_DRIVER_OVERRIDE \
  -u GALLIUM_DRIVER \
  -u LIBGL_ALWAYS_SOFTWARE \
  termux-x11 "$DISPLAY_NUM"
```

The separation was deliberate:

```text
Termux:X11 server process:
  clean graphics environment

Desktop applications:
  Turnip Vulkan ICD selected

Chromium:
  ANGLE Vulkan switches through CHROMIUM_FLAGS

Global Zink:
  disabled
```

The later `chrome://gpu` export confirmed that `CHROMIUM_FLAGS` appeared in Chromium's effective command line.

---

# Part II — Code OSS GPU Acceleration

## 12. Why Code OSS Required a Separate Procedure

Code OSS is an Electron application.

Although Electron embeds Chromium technologies, the Termux Code OSS package does not launch identically to the standalone Chromium package. Therefore, the successful Chromium environment variable:

```bash
CHROMIUM_FLAGS=...
```

could not simply be assumed to configure Code OSS.

The Code OSS work proceeded in three stages:

1. Direct Electron GUI launch with Vulkan switches.
2. Command-line propagation verification.
3. Permanent launch-policy integration.

---

## 13. Initial Code OSS Vulkan Test

The direct test command was:

```bash
pkill -f 'code-oss|Code|vscode' 2>/dev/null

VK_ICD_FILENAMES="$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json" \
"$PREFIX/lib/code-oss/code-oss" \
  --ignore-gpu-blocklist \
  --enable-gpu-rasterization \
  --enable-zero-copy \
  --enable-features=Vulkan \
  --use-gl=angle \
  --use-angle=vulkan \
  --ozone-platform=x11 \
  --no-sandbox
```

Intended path:

```text
Code OSS
  -> Electron
  -> ANGLE Vulkan
  -> Turnip
  -> Adreno 730
```

The user reported that the direct launch test succeeded.

---

## 14. Code OSS Command-Line Propagation Check

Verification command:

```bash
pgrep -af 'code-oss|Code|vscode'
```

Success criterion:

```text
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
```

The user reported that this step succeeded.

Therefore, the experiment established at minimum:

```text
Code OSS direct GUI launch: SUCCESS
Vulkan-related switch propagation: SUCCESS
```

---

## 15. `code-oss --status` Produced No Useful GPU Output

Attempted diagnostic command:

```bash
code-oss --status | sed -n '/GPU Status/,$p' | head -80
```

Result:

```text
No output
```

This did **not** prove a GPU failure. It only showed that this diagnostic method was not useful in this Termux Code OSS setup.

```text
No diagnostic output != software rendering
```

---

## 16. Inspection of the Packaged Code OSS Launcher

The real launcher was located with:

```bash
CODE_LAUNCHER="$(readlink -f "$(command -v code-oss)")"
echo "$CODE_LAUNCHER"
```

Output:

```text
/data/data/com.termux/files/usr/lib/code-oss/bin/code-oss
```

The launcher was inspected:

```bash
sed -n '1,160p' "$CODE_LAUNCHER"
```

Observed launcher:

```sh
#!/data/data/com.termux/files/usr/bin/env sh
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.

# when run in remote terminal, use the remote cli
if [ -n "$VSCODE_IPC_HOOK_CLI" ]; then
        REMOTE_CLI="$(which -a 'code-oss' | grep /remote-cli/)"
        if [ -n "$REMOTE_CLI" ]; then
                "$REMOTE_CLI" "$@"
                exit $?
        fi
fi

# test that VSCode wasn't installed inside WSL
if grep -qi Microsoft /dev/null && [ -z "$DONT_PROMPT_WSL_INSTALL" ]; then
        echo "To use Code - OSS with the Windows Subsystem for Linux, please install Code - OSS in Windows and uninstall the Linux version in WSL. You can then use the \`code-oss\` command in a WSL terminal just as you would in a normal command prompt." 1>&2
        printf "Do you want to continue anyway? [y/N] " 1>&2
        read -r YN
        YN=$(printf '%s' "$YN" | tr '[:upper:]' '[:lower:]')
        case "$YN" in
                y | yes )
                ;;
                * )
                        exit 1
                ;;
        esac
        echo "To no longer see this prompt, start Code - OSS with the environment variable DONT_PROMPT_WSL_INSTALL defined." 1>&2
fi

# If root, ensure that --user-data-dir or --file-write is specified
if [ "$(id -u)" = "0" ]; then
        for i in "$@"
        do
                case "$i" in
                        --user-data-dir | --user-data-dir=* | --file-write | tunnel | serve-web )
                                CAN_LAUNCH_AS_ROOT=1
                        ;;
                esac
        done
        if [ -z $CAN_LAUNCH_AS_ROOT ]; then
                echo "You are trying to start Code - OSS as a super user which isn't recommended. If this was intended, please add the argument \`--no-sandbox\` and specify an alternate user data directory using the \`--user-data-dir\` argument." 1>&2
                exit 1
        fi
fi

if [ ! -L "$0" ]; then
        # if path is not a symlink, find relatively
        VSCODE_PATH="$(dirname "$0")/.."
else
        if command -v readlink >/dev/null; then
                # if readlink exists, follow the symlink and find relatively
                VSCODE_PATH="$(dirname "$(readlink -f "$0")")/.."
        else
                # else use the standard install location
                VSCODE_PATH="/data/data/com.termux/files/usr/lib/code-oss"
        fi
fi

ELECTRON="$VSCODE_PATH/code-oss"
CLI="$VSCODE_PATH/resources/app/out/cli.js"
ELECTRON_RUN_AS_NODE=1 "$ELECTRON" "$CLI" "$@"
exit $?
```

The key tail was:

```sh
ELECTRON="$VSCODE_PATH/code-oss"
CLI="$VSCODE_PATH/resources/app/out/cli.js"
ELECTRON_RUN_AS_NODE=1 "$ELECTRON" "$CLI" "$@"
exit $?
```

This showed that the normal `code-oss` command initially entered the Electron binary in Node mode and ran the Code OSS CLI JavaScript entry point.

---

## 17. Launcher Backup

Before modification:

```bash
CODE_LAUNCHER="$(readlink -f "$(command -v code-oss)")"

cp "$CODE_LAUNCHER" \
   "$CODE_LAUNCHER.bak.$(date +%Y%m%d-%H%M%S)"
```

---

## 18. Code OSS Launcher Patch

The patch replaced:

```sh
ELECTRON_RUN_AS_NODE=1 "$ELECTRON" "$CLI" "$@"
exit $?
```

with a direct GUI Electron launch carrying the GPU switches.

Patch command:

```bash
python - <<'PY'
from pathlib import Path

launcher = Path("/data/data/com.termux/files/usr/lib/code-oss/bin/code-oss")
text = launcher.read_text()

old = '''ELECTRON_RUN_AS_NODE=1 "$ELECTRON" "$CLI" "$@"
exit $?
'''

new = '''# ------------------------------------------------------------
# Termux native GPU acceleration policy
# ------------------------------------------------------------

CODE_OSS_GPU_FLAGS="
  --ignore-gpu-blocklist
  --enable-gpu-rasterization
  --enable-zero-copy
  --enable-features=Vulkan
  --use-gl=angle
  --use-angle=vulkan
  --ozone-platform=x11
  --no-sandbox
"

exec "$ELECTRON" $CODE_OSS_GPU_FLAGS "$@"
'''

if old not in text:
    raise SystemExit(
        "Target block not found. "
        "Launcher layout may have changed; not patched."
    )

launcher.write_text(text.replace(old, new))
PY
```

After the patch, the GUI launch path became conceptually:

```text
Before:
code-oss shell launcher
  -> Electron in Node mode
  -> cli.js
  -> GUI launch mediation

After:
code-oss shell launcher
  -> Electron GUI directly
  -> Vulkan-related Chromium/Electron switches
  -> ANGLE Vulkan target path
```

The user reported that the modified launch method succeeded.

---

## 19. Code OSS Result and Evidence Level

The Code OSS experiment established:

```text
Direct Electron GUI launch with Vulkan-related switches: SUCCESS
Command-line switch propagation: SUCCESS
Patched central launcher startup: SUCCESS
```

The final target architecture was:

```text
Code OSS
  -> Electron / Chromium graphics stack
  -> ANGLE Vulkan
  -> Turnip
  -> Adreno 730
  -> Termux:X11
```

However, the diagnostic evidence captured in this session was not as complete as Chromium's `chrome://gpu` export.

Specifically:

- Chromium had full backend, renderer, Skia, ANGLE, Vulkan, WebGPU, and GPU crash-count output.
- Code OSS had successful launch behavior and command-line switch propagation.
- `code-oss --status` returned no useful GPU section.
- No equivalent final Code OSS renderer dump was captured in this conversation.

Therefore, the strongest conservative statement is:

> Code OSS successfully launched using the Vulkan-targeted Electron switch set, the relevant switches were observed in the process command line, and the launcher modification succeeded. A Chromium-style detailed renderer dump was not captured for Code OSS in this session.

---

## 20. Why the Central Launcher Was Modified

After success, the question arose whether simply placing the flags in the `.desktop` file would have been enough.

Yes. For menu-only GUI launching, a `.desktop` `Exec=` modification is sufficient.

The central launcher was modified for centralization.

### `.desktop`-only policy

```text
Menu launch:
  Vulkan flags applied

Terminal:
  code .
  code-oss
  vscode
  original launcher behavior
```

### Central launcher policy

```text
Menu launch:
  Vulkan flags applied

Terminal:
  code .
  code-oss
  vscode
  same Vulkan policy applied
```

Trade-off: direct replacement of the launcher's final CLI path may affect non-GUI CLI behavior such as:

```text
code --status
code --list-extensions
code --install-extension
remote CLI integration
```

Therefore:

For primarily GUI use:

```text
Recommended:
restore stock launcher
put Vulkan flags in a user-local .desktop file
```

For a single centralized GPU policy across GUI and terminal-launched editor sessions:

```text
Keep central launcher modification
```

---

## 21. Optional `.desktop` Alternative for Code OSS

A safer GUI-only approach is:

```bash
mkdir -p ~/.local/share/applications
```

Copy the package desktop file:

```bash
cp "$PREFIX/share/applications/code-oss.desktop" \
   "$HOME/.local/share/applications/code-oss.desktop"
```

Replace the `Exec=` line:

```bash
sed -i \
's|^Exec=.*|Exec=/data/data/com.termux/files/usr/lib/code-oss/code-oss --ignore-gpu-blocklist --enable-gpu-rasterization --enable-zero-copy --enable-features=Vulkan --use-gl=angle --use-angle=vulkan --ozone-platform=x11 --no-sandbox %F|' \
"$HOME/.local/share/applications/code-oss.desktop"
```

Refresh desktop database:

```bash
update-desktop-database \
  "$HOME/.local/share/applications" \
  2>/dev/null
```

Resulting split:

```text
Code OSS menu launch:
  direct Electron GUI
  Vulkan target switches

Code OSS CLI:
  stock Termux launcher
  original CLI semantics
```

---

# Part III — Final Combined GPU Policy

## 22. Final Architecture

```text
                     +-------------------+
                     |   Termux:X11 :1   |
                     +---------+---------+
                               |
              +----------------+----------------+
              |                                 |
      +-------v-------+                 +-------v-------+
      |   Chromium    |                 |    Code OSS   |
      +-------+-------+                 +-------+-------+
              |                                 |
      ANGLE Vulkan                       Electron/ANGLE
              |                              Vulkan
              +---------------+-----------------+
                              |
                        Mesa Turnip
                              |
                         Adreno 730
```

Desktop components do not receive a global Zink override.

```text
xfsettingsd
xfwm4
xfdesktop
xfce4-panel
```

remain independent from:

```text
MESA_LOADER_DRIVER_OVERRIDE=zink
```

---

## 23. Final XFCE Startup Script

```bash
#!/data/data/com.termux/files/usr/bin/bash

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
HOME="${HOME:-/data/data/com.termux/files/home}"
DISPLAY_NUM=":1"

LOGDIR="$HOME/.cache/termux-x11-session"
mkdir -p "$LOGDIR"

FREEDRENO_ICD="$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json"

pkill -f 'chromium|chrome' 2>/dev/null
pkill -f 'xfce4-session|xfwm4|xfdesktop|xfce4-panel|xfsettingsd|xfce4-power-manager|picom|compton' 2>/dev/null
pkill -f 'termux-x11' 2>/dev/null

sleep 1

unset VK_ICD_FILENAMES
unset MESA_LOADER_DRIVER_OVERRIDE
unset GALLIUM_DRIVER
unset LIBGL_ALWAYS_SOFTWARE
unset PULSE_SERVER

export DISPLAY="$DISPLAY_NUM"
export XDG_RUNTIME_DIR="${TMPDIR}"
export XDG_CONFIG_DIRS="$PREFIX/etc/xdg"
export PATH="$HOME/.local/bin:$PATH"

if [ -r "$FREEDRENO_ICD" ]; then
  export VK_ICD_FILENAMES="$FREEDRENO_ICD"
else
  unset VK_ICD_FILENAMES
fi

unset MESA_LOADER_DRIVER_OVERRIDE
unset GALLIUM_DRIVER
unset LIBGL_ALWAYS_SOFTWARE

export CHROMIUM_FLAGS="--ignore-gpu-blocklist --enable-gpu-rasterization --enable-zero-copy --enable-accelerated-video-decode --enable-features=Vulkan --use-gl=angle --use-angle=vulkan"

{
  echo "DISPLAY=$DISPLAY"
  echo "XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR"
  echo "XDG_CONFIG_DIRS=$XDG_CONFIG_DIRS"
  echo "VK_ICD_FILENAMES=${VK_ICD_FILENAMES:-<unset>}"
  echo "MESA_LOADER_DRIVER_OVERRIDE=${MESA_LOADER_DRIVER_OVERRIDE:-<unset>}"
  echo "GALLIUM_DRIVER=${GALLIUM_DRIVER:-<unset>}"
  echo "LIBGL_ALWAYS_SOFTWARE=${LIBGL_ALWAYS_SOFTWARE:-<unset>}"
  echo "CHROMIUM_FLAGS=$CHROMIUM_FLAGS"
} >"$LOGDIR/gpu-policy.log"

pulseaudio --start --exit-idle-time=-1 >/dev/null 2>&1

env \
  -u VK_ICD_FILENAMES \
  -u MESA_LOADER_DRIVER_OVERRIDE \
  -u GALLIUM_DRIVER \
  -u LIBGL_ALWAYS_SOFTWARE \
  termux-x11 "$DISPLAY_NUM" \
  >"$LOGDIR/termux-x11.log" 2>&1 &

sleep 2

am start --user 0 \
  -n com.termux.x11/com.termux.x11.MainActivity \
  >/dev/null 2>&1

sleep 2

eval "$(dbus-launch --sh-syntax)"

xfsettingsd >"$LOGDIR/xfsettingsd.log" 2>&1 &
sleep 1

xfwm4 --replace --compositor=off \
  >"$LOGDIR/xfwm4.log" 2>&1 &
sleep 1

xfdesktop >"$LOGDIR/xfdesktop.log" 2>&1 &
sleep 1

xfce4-panel >"$LOGDIR/xfce4-panel.log" 2>&1 &

echo "Manual XFCE session started."
echo "DISPLAY=$DISPLAY"
echo "VK_ICD_FILENAMES=${VK_ICD_FILENAMES:-<unset>}"
echo "MESA_LOADER_DRIVER_OVERRIDE=${MESA_LOADER_DRIVER_OVERRIDE:-<unset>}"
echo "Logs: $LOGDIR"

wait
```

---

## 24. Result Matrix

| Component | Initial State | Final State |
|---|---|---|
| Termux:X11 | Working | Working |
| XFCE through `xfce4-session` | Unstable in tested state | Bypassed |
| Manual XFCE components | Tested | Working |
| Global Zink override | Caused desktop instability | Disabled |
| Turnip Vulkan ICD | Available | Explicitly selected for apps |
| Chromium compositor | Initially software | Hardware accelerated |
| Chromium rasterization | Partial/limited | Hardware accelerated on all pages |
| Chromium Vulkan | Disabled | Enabled |
| Chromium Skia backend | GaneshGL | GaneshVulkan |
| Chromium ANGLE backend | ANGLE_OPENGL | ANGLE_VULKAN |
| Chromium renderer | Zink-over-Turnip OpenGL route | Direct ANGLE Vulkan over Turnip |
| Chromium WebGL | Reduced performance initially | Hardware accelerated |
| Chromium WebGPU | Reduced/indirect initially | Hardware accelerated; native Turnip Vulkan adapter visible |
| Chromium video decode | Software only | Still software only |
| Code OSS direct GPU-switch launch | Not configured | Successful |
| Code OSS Vulkan switch propagation | Not configured | Successful |
| Code OSS central launcher policy | Stock CLI-mediated route | Direct GUI Electron launch with GPU switches |
| Code OSS detailed renderer dump | Not available | Not captured in this session |

---

## 25. Key Technical Findings

### 25.1 GPU access alone is not the same as full GPU acceleration

The baseline Chromium renderer already mentioned:

```text
zink Vulkan
Turnip Adreno 730
```

but GPU compositing was still software-only.

Seeing the GPU name in a renderer string is therefore insufficient; the complete feature status must also be checked.

### 25.2 Direct Vulkan flags alone are not enough

The failed Chromium attempt showed that:

```text
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
```

can still fail completely when the Vulkan loader resolves the wrong or incomplete path.

Explicit Turnip ICD selection was essential.

### 25.3 Global Zink policy is too broad

A desktop-wide:

```bash
MESA_LOADER_DRIVER_OVERRIDE=zink
```

affected more than target applications.

It also changed the rendering behavior of desktop components such as:

```text
xfwm4
xfdesktop
xfce4-panel
```

The observed black-screen behavior demonstrated why application-specific direct Vulkan paths are preferable.

### 25.4 Chromium and Code OSS need different integration points

Chromium successfully consumed:

```bash
CHROMIUM_FLAGS
```

from the session environment.

Code OSS required direct Electron launch testing and launcher-level or `.desktop`-level switch injection.

### 25.5 Rendering acceleration and video decoding are separate

The final Chromium state achieved:

```text
Vulkan: Enabled
Compositing: Hardware accelerated
Rasterization: Hardware accelerated
WebGL: Hardware accelerated
WebGPU: Hardware accelerated
```

while still reporting:

```text
Video Decode: Software only
Video Encode: Software only
```

These are separate optimization projects.

---

## 26. Recommended Final Policy

For this native Termux + Termux:X11 + Adreno 730 environment:

```text
1. Keep Termux:X11 itself on a clean environment.

2. Select the Freedreno/Turnip Vulkan ICD for Vulkan-aware applications.

3. Do not export MESA_LOADER_DRIVER_OVERRIDE=zink globally.

4. Use ANGLE Vulkan for Chromium:
   --enable-features=Vulkan
   --use-gl=angle
   --use-angle=vulkan

5. Retain:
   --ignore-gpu-blocklist
   --enable-gpu-rasterization
   --enable-zero-copy

6. Treat hardware video decode as a separate issue.

7. For Code OSS:
   either patch the central launcher for a unified policy,
   or use a user-local .desktop entry for safer GUI-only acceleration.

8. Preserve stock CLI behavior if commands such as:
   code --status
   code --install-extension
   code --list-extensions
   are important.
```

---

## 27. Rollback Procedures

### Restore Code OSS launcher

List backups:

```bash
ls -t \
  /data/data/com.termux/files/usr/lib/code-oss/bin/code-oss.bak.* \
  | head -1
```

Restore:

```bash
cp \
  "$(ls -t /data/data/com.termux/files/usr/lib/code-oss/bin/code-oss.bak.* | head -1)" \
  /data/data/com.termux/files/usr/lib/code-oss/bin/code-oss

chmod +x \
  /data/data/com.termux/files/usr/lib/code-oss/bin/code-oss
```

### Disable Chromium Vulkan policy

```bash
unset CHROMIUM_FLAGS
```

Then restart Chromium.

### Return to unrestricted Vulkan ICD enumeration

```bash
unset VK_ICD_FILENAMES
```

### Ensure no global Zink override remains

```bash
unset MESA_LOADER_DRIVER_OVERRIDE
unset GALLIUM_DRIVER
unset LIBGL_ALWAYS_SOFTWARE
```

---

## 28. Final Conclusion

The experiment demonstrated that a native Android/Termux desktop can run Chromium with a verified real Adreno 730 Vulkan stack through Mesa Turnip, and can launch Code OSS through a Vulkan-targeted Electron path using the same Turnip device.

The decisive Chromium configuration was not merely “GPU enabled.” It was a verified direct Vulkan route:

```text
Chromium
  -> ANGLE Vulkan
  -> Turnip
  -> Adreno 730
```

with:

```text
Skia Backend: GaneshVulkan
Display type: ANGLE_VULKAN
Vulkan: Enabled
GPU process crash count: 0
```

Code OSS successfully accepted the same Vulkan-oriented Electron/Chromium switches when launched directly, and the central launcher modification made that policy persistent.

The most important architectural lesson was to avoid solving the problem with a global translation layer.

The final policy was deliberately asymmetric:

```text
Desktop:
  stable, conservative, no global Zink

Chromium:
  direct ANGLE Vulkan

Code OSS:
  direct Electron GUI launch with ANGLE Vulkan target switches

Vulkan driver:
  Turnip / Freedreno

GPU:
  Adreno 730
```

This approach provided the best combination of transparency, performance, and desktop stability observed during the experiment.
