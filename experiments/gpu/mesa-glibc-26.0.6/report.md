# Mesa 26.0.6 glibc Build Report

## Native Turnip/KGSL for Qualcomm Adreno 730 on Termux

---

## 1. Executive Summary

This report documents the successful native build and runtime validation of **Mesa 26.0.6 Turnip**, targeting the **KGSL kernel interface** and running against the **Termux glibc runtime** on an Android aarch64 device with a **Qualcomm Adreno 730 GPU**.

The build model was intentionally hybrid:

- **Build host environment:** native Termux/Bionic
- **Build orchestration tools:** Bionic Python, Meson, Ninja, shell tools
- **Target compiler:** `gcc-glibc`
- **Target ABI/runtime:** Termux glibc
- **Target Vulkan driver:** Mesa Turnip
- **Kernel interface:** KGSL
- **Display platform:** X11 / Termux:X11
- **Architecture:** aarch64
- **GPU:** Qualcomm Adreno 730

The central design rule was:

> Run build tools in the host environment, but compile and link target artifacts entirely against the runtime world in which they will execute.

The final driver successfully enumerated the physical GPU:

```text
GPU0:
        apiVersion         = 1.4.335
        driverVersion      = 26.0.6
        vendorID           = 0x5143
        deviceID           = 0x7030001
        deviceType         = PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU
        deviceName         = Turnip Adreno (TM) 730
        driverID           = DRIVER_ID_MESA_TURNIP
        driverName         = turnip Mesa driver
        driverInfo         = Mesa 26.0.6 (git-0e095aab43)
        conformanceVersion = 1.4.0.0
```

The final installed driver exposed a KGSL implementation and contained the expected KGSL device path:

```text
../src/freedreno/vulkan/tu_knl_kgsl.cc
/dev/kgsl-3d0
tu_knl_kgsl_load
kgsl_device_init
kgsl_queue_submit
```

The build therefore achieved the primary objective:

> A glibc-linked Mesa Turnip driver running natively on Android, using KGSL to access the Adreno 730.

One limitation must be stated clearly: the surviving record conclusively proves **device enumeration and driver initialization**, but does **not preserve a final successful vanilla-present `vkcube` result for this exact custom glibc Mesa 26.0.6 build**. Earlier glibc Mesa 24.2.6 and Bionic Mesa 26.0.6 configurations did successfully run `vkcube` through ordinary X11 WSI paths, but the exact custom Mesa 26.0.6 glibc build was only conclusively preserved through `vulkaninfo` validation.

---

## 2. Project Objective

The purpose of the experiment was to build a modern Mesa Turnip driver for a glibc-based userspace running directly inside Termux, without using a PRoot Linux distribution as the execution environment.

The intended graphics path was:

```text
glibc application
    |
    v
glibc Vulkan loader
    |
    v
custom Mesa Turnip libvulkan_freedreno.so
    |
    v
KGSL
    |
    v
/dev/kgsl-3d0
    |
    v
Qualcomm Adreno 730
```

For graphical presentation under Termux:X11, the broader intended path was:

```text
Vulkan application
    |
    v
Turnip
    |
    v
Mesa WSI
    |
    v
XCB/Xlib
    |
    v
Termux:X11
```

The build was also later extended experimentally toward:

```text
OpenGL application
    |
    v
Mesa Zink
    |
    v
Turnip Vulkan
    |
    v
KGSL
```

However, the Turnip/KGSL build was fully validated first, while the Zink/GLX extension encountered additional dependency and compiler-wrapper issues and should be treated as a separate unfinished extension effort.

---

## 3. Why the Build Was Performed Natively in Termux

The selected environment was:

```text
Bionic host tools
+
Termux glibc compiler
+
Termux glibc target libraries
```

rather than building Mesa as a normal Debian package inside PRoot.

The important technical distinction is not merely whether the build process runs “inside PRoot” or “outside PRoot.” In principle, a PRoot-hosted build process could still target the Termux glibc ABI if the compiler, sysroot, pkg-config paths, linker, and libraries were carefully redirected.

However, for this project the native Termux host model had several practical advantages:

1. The target compiler and runtime libraries came from the same Termux glibc ecosystem.
2. Host-side generators could execute directly under Bionic.
3. KGSL was explicitly selected instead of the ordinary Linux DRM/MSM path.
4. The build environment became reusable for future Mesa rebuilds.
5. PRoot fork/exec overhead was avoided for a large Meson/Ninja project.
6. Host tools and target artifacts could be separated explicitly.

The build boundary was therefore:

```text
HOST WORLD:
  Termux/Bionic
  Python
  Meson
  Ninja
  shell scripts
  source generators

TARGET WORLD:
  Termux glibc
  GCC
  GNU binutils
  Vulkan headers
  libdrm
  X11/XCB libraries
  libxshmfence
  compression/XML dependencies
  final libvulkan_freedreno.so
```

---

## 4. Directory Layout

The confirmed build locations were:

```text
Source tree:
~/src/mesa-glibc-build/mesa

Build directory:
~/src/mesa-glibc-build/mesa/build-glibc-freedreno

Cross file:
~/src/mesa-glibc-build/termux-glibc-aarch64.ini

Installation prefix:
~/opt/mesa-26-glibc
```

Final installed Vulkan artifacts:

```text
/data/data/com.termux/files/home/opt/mesa-26-glibc/lib/libvulkan_freedreno.so

/data/data/com.termux/files/home/opt/mesa-26-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json
```

The driver embedded the following version information:

```text
Mesa 26.0.6 (git-0e095aab43)
```

This is the version string preserved by the runtime driver report. The current record does not independently preserve the output of:

```bash
git rev-parse HEAD
```

so `0e095aab43` should be treated as the revision identifier embedded in `driverInfo`, rather than as a separately verified full repository HEAD record.

---

## 5. Existing glibc Vulkan Baseline

Before the custom build, the Termux glibc package repository already provided an older Turnip stack.

The existing glibc driver reported approximately:

```text
apiVersion = 1.3.289
driverVersion = 24.2.6
deviceName = Turnip Adreno (TM) 730
driverName = turnip Mesa driver
driverInfo = Mesa 24.2.6.termux-glibc-0
```

A correct invocation pattern was necessary because directly exposing glibc libraries to the Bionic shell environment could break process startup.

A working invocation form was:

```bash
env -u LD_LIBRARY_PATH \
  VK_ICD_FILENAMES="$GLIBC_FREEDRENO_ICD" \
  VK_DRIVER_FILES="$GLIBC_FREEDRENO_ICD" \
  glibc-runner --no-linker \
  "$PREFIX/glibc/bin/vulkaninfo" --summary
```

A failed approach was to run a glibc executable with a globally exposed glibc `LD_LIBRARY_PATH` from the Bionic environment.

Observed failure:

```text
/data/data/com.termux/files/usr/glibc/bin/vulkaninfo:
error while loading shared libraries:
/data/data/com.termux/files/usr/glibc/lib/libc.so:
invalid ELF header
```

This established one of the most important operational rules of the project:

> Do not export the glibc target library path globally into the Bionic host shell.

Instead, variables intended for the glibc process should be injected after entering the glibc execution context, for example:

```bash
glibc-runner --no-linker "$PREFIX/glibc/bin/env" \
  LD_LIBRARY_PATH="..." \
  VK_DRIVER_FILES="..." \
  target-program
```

---

## 6. Build Dependencies

### 6.1 Host-side build tools

The initial package installation attempt included:

```bash
pkg install \
  git \
  python \
  meson \
  ninja \
  cmake \
  pkg-config \
  bison \
  flex \
  gettext \
  python-mako \
  python-packaging \
  python-pyyaml \
  gcc-glibc \
  vulkan-headers-glibc \
  vulkan-icd-loader-glibc \
  libdrm-glibc \
  libxcb-glibc \
  libx11-glibc \
  libxshmfence-glibc \
  zlib-glibc \
  zstd-glibc \
  expat-glibc \
  libxml2-glibc
```

Several package names were unavailable:

```text
E: Unable to locate package meson
E: Unable to locate package python-mako
E: Unable to locate package python-packaging
E: Unable to locate package python-pyyaml
E: Unable to locate package expat-glibc
```

The XML parser package name was corrected from:

```text
expat-glibc
```

to:

```text
libexpat-glibc
```

The host Python/Meson stack was ultimately supplied through a Bionic Python environment, including a virtual environment under:

```text
~/opt/.venv
```

The relevant Python packages included:

```text
meson
mako
packaging
pyyaml
```

The important architectural point was that these Python packages were **host tools**. They did not need to be glibc-linked because they generated files and orchestrated compilation rather than becoming part of the target artifacts.

### 6.2 Confirmed target library versions

The glibc-target pkg-config environment reported:

```text
vulkan     1.3.301
xcb        1.17.0
x11        1.8.11
libdrm     2.4.124
xshmfence  1.3.3
zlib       1.3.1
libzstd    1.5.7
expat      2.6.4
libxml-2.0 2.13.6
```

A custom target pkg-config wrapper existed at:

```text
~/.local/bin/glibc-pkg-config
```

Its purpose was to ensure that Meson resolved target dependencies from Termux glibc package directories rather than accidentally consuming Bionic `.pc` metadata.

Relevant target pkg-config search roots were of the form:

```text
$PREFIX/glibc/lib/pkgconfig

$PREFIX/glibc/share/pkgconfig

$PREFIX/glibc/lib/aarch64-linux-gnu/pkgconfig
```

---

## 7. Compiler and Target Toolchain

The Termux glibc toolchain included:

```text
/data/data/com.termux/files/usr/glibc/bin/aarch64-linux-gnu-gcc

/data/data/com.termux/files/usr/glibc/bin/gcc

/data/data/com.termux/files/usr/glibc/bin/g++

/data/data/com.termux/files/usr/glibc/bin/ar

/data/data/com.termux/files/usr/glibc/bin/ld
```

The glibc dynamic linker was:

```text
/data/data/com.termux/files/usr/glibc/lib/ld-linux-aarch64.so.1
```

The project used compiler wrappers so that Meson/Ninja, running as Bionic host tools, could invoke glibc toolchain binaries safely.

The surviving wrapper design evolved during the build.

A later `glibc-gcc` form was:

```bash
#!/data/data/com.termux/files/usr/bin/bash
unset LD_LIBRARY_PATH
unset LD_PRELOAD

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"

export PATH="$PREFIX/glibc/bin:$PATH"

exec "$PREFIX/glibc/lib/ld-linux-aarch64.so.1" \
  --library-path "$PREFIX/glibc/lib" \
  "$PREFIX/glibc/bin/gcc" \
  -B"$PREFIX/glibc/bin/" \
  "$@"
```

The equivalent C++ wrapper was:

```bash
#!/data/data/com.termux/files/usr/bin/bash
unset LD_LIBRARY_PATH
unset LD_PRELOAD

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"

export PATH="$PREFIX/glibc/bin:$PATH"

exec "$PREFIX/glibc/lib/ld-linux-aarch64.so.1" \
  --library-path "$PREFIX/glibc/lib" \
  "$PREFIX/glibc/bin/g++" \
  -B"$PREFIX/glibc/bin/" \
  "$@"
```

Additional wrappers existed for:

```text
glibc-exec
glibc-ar
glibc-ranlib
glibc-strip
```

The exact live files should be preferred over reconstructed copies whenever available:

```text
~/.local/bin/glibc-exec
~/.local/bin/glibc-gcc
~/.local/bin/glibc-g++
~/.local/bin/glibc-ar
~/.local/bin/glibc-ranlib
~/.local/bin/glibc-strip
~/.local/bin/glibc-pkg-config
```

---

## 8. Cross File

The Meson cross-file path was:

```text
~/src/mesa-glibc-build/termux-glibc-aarch64.ini
```

The exact original contents were not preserved in the conversation record.

This distinction is important:

- the path is confirmed;
- its use in Meson setup is confirmed;
- the exact text of the file is not reconstructable with certainty from the surviving transcript.

The live original should therefore be archived directly whenever the original filesystem is still available.

The build was invoked with a structure of the form:

```bash
python -m mesonbuild.mesonmain setup \
  build-glibc-freedreno \
  --cross-file "$MESA_WORK/termux-glibc-aarch64.ini" \
  --prefix "$MESA_PREFIX" \
  ...
```

---

## 9. Initial Mesa Configuration

The build focused on Turnip/Freedreno Vulkan support.

The successful final build requirements were:

```text
platforms = x11
vulkan-drivers = freedreno
freedreno-kmds = kgsl
LLVM = disabled
tests = disabled
```

One critical mistake occurred during the first build configuration.

The Meson configuration showed:

```text
freedreno-kmds [msm]
```

The relevant output was:

```text
freedreno-kmds                 [msm]
                               [msm, kgsl, virtio, wsl]

platforms                      [x11]

vulkan-drivers                 [freedreno]
```

This build produced a Turnip library, but the driver could not enumerate the Android GPU.

Runtime failure:

```text
ERROR: [Loader Message] Code 0 :
setup_loader_term_phys_devs:
Failed to detect any valid GPUs in the current config

ERROR at
/home/builder/.termux-build/vulkan-tools-glibc/src/vulkaninfo/./vulkaninfo.h:242:
vkEnumeratePhysicalDevices failed with ERROR_INITIALIZATION_FAILED
```

This was a major diagnostic milestone.

The problem was not:

- missing ICD JSON,
- missing shared libraries,
- loader failure,
- or failure to load `libvulkan_freedreno.so`.

The Vulkan loader successfully found the driver.

Example debug output:

```text
DRIVER: Searching for driver manifest files
DRIVER: In following locations:
DRIVER:
  /data/data/com.termux/files/home/opt/mesa-26-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json

DRIVER: Found ICD manifest file
/data/data/com.termux/files/home/opt/mesa-26-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json,
version 1.0.1

DEBUG | DRIVER:
Searching for ICD drivers named
/data/data/com.termux/files/home/opt/mesa-26-glibc/lib/libvulkan_freedreno.so
```

The failure happened later, during physical-device discovery.

The correction was to configure:

```text
-Dfreedreno-kmds=kgsl
```

instead of:

```text
-Dfreedreno-kmds=msm
```

---

## 10. KGSL Reconfiguration

The intended configuration was approximately:

```bash
unset LD_LIBRARY_PATH
unset LD_PRELOAD

export PATH="$HOME/.local/bin:$PATH"
export MESA_WORK="$HOME/src/mesa-glibc-build"
export MESA_PREFIX="$HOME/opt/mesa-26-glibc"

cd "$MESA_WORK/mesa"

rm -rf build-glibc-freedreno
rm -rf "$MESA_PREFIX"
mkdir -p "$MESA_PREFIX"

python -m mesonbuild.mesonmain setup \
  build-glibc-freedreno \
  --cross-file "$MESA_WORK/termux-glibc-aarch64.ini" \
  --prefix "$MESA_PREFIX" \
  -Dplatforms=x11 \
  -Dvulkan-drivers=freedreno \
  -Dfreedreno-kmds=kgsl \
  -Dllvm=disabled \
  -Dshared-llvm=disabled \
  -Dbuild-tests=false \
  -Dvalgrind=disabled \
  -Dlibunwind=disabled
```

Some experiments used additional options for reducing unrelated Mesa components. The exact minimal successful option vector is not fully preserved.

What is firmly established is that the final functional build had:

```text
vulkan-drivers = freedreno

freedreno-kmds = kgsl

platforms = x11
```

---

## 11. Python Generator Failure

The build progressed substantially before stopping at approximately:

```text
[202/824] Generating src/freedreno/isa/ir3-isa with a custom command

FAILED:
src/freedreno/isa/ir3-isa.c
src/freedreno/isa/ir3-isa.h
```

The failing generator command involved:

```text
src/compiler/isaspec/decode.py
```

and produced:

```text
/data/data/com.termux/files/usr/bin/sh: 1:
.../decode.py: not found
```

The file itself existed. The problem was its interpreter path.

Mesa Python scripts used shebangs such as:

```text
#!/usr/bin/env python3
```

or similar host-generic paths.

These were incompatible with the execution environment as invoked by Ninja.

The scripts were patched to use the actual Termux Python executable.

A general patch procedure used was:

```bash
unset LD_LIBRARY_PATH
unset LD_PRELOAD

cd "$HOME/src/mesa-glibc-build/mesa"

export PYTHON_BIN="$(command -v python3 || command -v python)"

python - <<'PY'
from pathlib import Path
import os

root = Path(".")
python_bin = os.environ["PYTHON_BIN"]

targets = []

for p in root.rglob("*"):
    if not p.is_file():
        continue

    try:
        data = p.read_bytes()
    except Exception:
        continue

    old_new = [
        (
            b"#!/usr/bin/env python3",
            f"#!{python_bin}".encode()
        ),
        (
            b"#!/usr/bin/env python",
            f"#!{python_bin}".encode()
        ),
        (
            b"#!/usr/bin/python3",
            f"#!{python_bin}".encode()
        ),
        (
            b"#!/usr/bin/python",
            f"#!{python_bin}".encode()
        ),
    ]

    for old, new in old_new:
        if data.startswith(old):
            p.write_bytes(data.replace(old, new, 1))
            targets.append(str(p))
            break

print("patched", len(targets), "python shebangs")
PY
```

After patching, representative files contained:

```text
#!/data/data/com.termux/files/usr/bin/python3
```

Validation:

```bash
head -1 src/compiler/isaspec/decode.py
head -1 src/compiler/isaspec/encode.py
```

Output:

```text
#!/data/data/com.termux/files/usr/bin/python3

#!/data/data/com.termux/files/usr/bin/python3
```

The scripts then executed successfully:

```bash
src/compiler/isaspec/decode.py --help

src/compiler/isaspec/encode.py --help
```

This allowed Ninja to resume.

---

## 12. Build Execution

The normal build command was:

```bash
unset LD_LIBRARY_PATH
unset LD_PRELOAD

cd "$HOME/src/mesa-glibc-build/mesa"

ninja \
  -C build-glibc-freedreno \
  -j"$(nproc)"
```

A lower parallelism level was suggested for thermal or memory constraints:

```bash
ninja \
  -C build-glibc-freedreno \
  -j2
```

Installation:

```bash
ninja \
  -C build-glibc-freedreno \
  install
```

The installation prefix was:

```text
~/opt/mesa-26-glibc
```

---

## 13. Installed Artifacts

Artifact discovery:

```bash
export MESA_PREFIX="$HOME/opt/mesa-26-glibc"

find "$MESA_PREFIX" -maxdepth 6 \
  \( \
    -name '*freedreno*' \
    -o -name '*vulkan*' \
    -o -name '*icd*.json' \
  \) \
  -print
```

Observed output:

```text
/data/data/com.termux/files/home/opt/mesa-26-glibc/lib/libvulkan_freedreno.so

/data/data/com.termux/files/home/opt/mesa-26-glibc/share/vulkan

/data/data/com.termux/files/home/opt/mesa-26-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json
```

The ICD JSON was:

```json
{
    "ICD": {
        "api_version": "1.4.335",
        "library_arch": "64",
        "library_path": "/data/data/com.termux/files/home/opt/mesa-26-glibc/lib/libvulkan_freedreno.so"
    },
    "file_format_version": "1.0.1"
}
```

ELF inspection:

```bash
file \
  "$MESA_PREFIX/lib/libvulkan_freedreno.so"
```

Output:

```text
/data/data/com.termux/files/home/opt/mesa-26-glibc/lib/libvulkan_freedreno.so:
ELF 64-bit LSB shared object,
ARM aarch64,
version 1 (SYSV),
dynamically linked,
BuildID[sha1]=3182a72a85e9472abfcda01038d8fccd1e9af3d3,
with debug_info,
not stripped
```

---

## 14. Shared Library Dependency Verification

The driver was checked with glibc `ldd`:

```bash
glibc-runner --no-linker \
  "$PREFIX/glibc/bin/ldd" \
  "$MESA_PREFIX/lib/libvulkan_freedreno.so"
```

Output:

```text
linux-vdso.so.1
    (0x0000007aa24c7000)

libz.so.1
    => /data/data/com.termux/files/usr/glibc/lib/libz.so.1

libzstd.so.1
    => /data/data/com.termux/files/usr/glibc/lib/libzstd.so.1

libdrm.so.2
    => /data/data/com.termux/files/usr/glibc/lib/libdrm.so.2

libxcb-dri3.so.0
    => /data/data/com.termux/files/usr/glibc/lib/libxcb-dri3.so.0

libxcb.so.1
    => /data/data/com.termux/files/usr/glibc/lib/libxcb.so.1

libX11-xcb.so.1
    => /data/data/com.termux/files/usr/glibc/lib/libX11-xcb.so.1

libxcb-present.so.0
    => /data/data/com.termux/files/usr/glibc/lib/libxcb-present.so.0

libxcb-xfixes.so.0
    => /data/data/com.termux/files/usr/glibc/lib/libxcb-xfixes.so.0

libxcb-sync.so.1
    => /data/data/com.termux/files/usr/glibc/lib/libxcb-sync.so.1

libxcb-randr.so.0
    => /data/data/com.termux/files/usr/glibc/lib/libxcb-randr.so.0

libxcb-shm.so.0
    => /data/data/com.termux/files/usr/glibc/lib/libxcb-shm.so.0

libxshmfence.so.1
    => /data/data/com.termux/files/usr/glibc/lib/libxshmfence.so.1

libexpat.so.1
    => /data/data/com.termux/files/usr/glibc/lib/libexpat.so.1

libstdc++.so.6
    => /data/data/com.termux/files/usr/glibc/lib/libstdc++.so.6

libm.so.6
    => /data/data/com.termux/files/usr/glibc/lib/libm.so.6

libgcc_s.so.1
    => /data/data/com.termux/files/usr/glibc/lib/libgcc_s.so.1

libc.so.6
    => /data/data/com.termux/files/usr/glibc/lib/libc.so.6

/data/data/com.termux/files/usr/glibc/lib/ld-linux-aarch64.so.1

libXau.so.6
    => /data/data/com.termux/files/usr/glibc/lib/libXau.so.6

libXdmcp.so.6
    => /data/data/com.termux/files/usr/glibc/lib/libXdmcp.so.6
```

There were no unresolved shared-library dependencies in this validation output.

---

## 15. Verifying KGSL Inclusion

The final installed library was inspected using:

```bash
strings \
  "$HOME/opt/mesa-26-glibc/lib/libvulkan_freedreno.so" \
  | grep -Ei \
    'kgsl|msm|turnip|/dev/kgsl' \
  | head -80
```

Relevant output:

```text
Turnip Adreno (TM) %s%s

kgsl

turnip Mesa driver

turnip-v1

turnip

kgsl_profiling_suballoc

../src/freedreno/vulkan/tu_knl_kgsl.cc

vk_kgsl_sync_import_sync_file: dup failed: %s

/dev/kgsl-3d0

tu_knl_kgsl.cc

kgsl_device_init

kgsl_device_finish

kgsl_device_get_suspend_count

kgsl_device_get_gpu_timestamp

kgsl_bo_export_dmabuf

kgsl_bo_map

kgsl_submit_create

kgsl_submit_add_entries

kgsl_submit_add_bind

kgsl_syncobj_wait

vk_kgsl_sync_wait

kgsl_submit_finish

vk_kgsl_sync_finish

vk_kgsl_sync_reset

vk_kgsl_sync_move

vk_kgsl_sync_import_sync_file

kgsl_device_check_status

kgsl_submitqueue_close

kgsl_submitqueue_new

vk_kgsl_sync_wait_many

kgsl_syncobj_merge

kgsl_sparse_vma_finish

kgsl_is_memory_type_supported

kgsl_bo_finish

kgsl_bo_user_map

vk_kgsl_sync_export_sync_file

kgsl_bo_init_dmabuf

kgsl_sparse_vma_init

kgsl_queue_submit

kgsl_bo_init

tu_knl_kgsl_load

kgsl_knl_funcs

kgsl_queue_wait_fence
```

This is strong evidence that the final driver was built with the KGSL implementation enabled.

---

## 16. Runtime Validation

The final validation command was:

```bash
unset LD_LIBRARY_PATH
unset LD_PRELOAD

MESA_PREFIX="$HOME/opt/mesa-26-glibc"

NEW_ICD="$MESA_PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json"

glibc-runner --no-linker \
  "$PREFIX/glibc/bin/env" \
  LD_LIBRARY_PATH="$MESA_PREFIX/lib:$PREFIX/glibc/lib" \
  DISPLAY=:1 \
  XDG_RUNTIME_DIR="$TMPDIR" \
  VK_ICD_FILENAMES="$NEW_ICD" \
  VK_DRIVER_FILES="$NEW_ICD" \
  "$PREFIX/glibc/bin/vulkaninfo" --summary
```

The resulting output included:

```text
==========
VULKANINFO
==========

Vulkan Instance Version: 1.3.301
```

Instance extensions included:

```text
VK_EXT_acquire_drm_display
VK_EXT_acquire_xlib_display
VK_EXT_debug_report
VK_EXT_debug_utils
VK_EXT_direct_mode_display
VK_EXT_display_surface_counter
VK_EXT_headless_surface
VK_EXT_surface_maintenance1
VK_EXT_swapchain_colorspace
VK_KHR_device_group_creation
VK_KHR_display
VK_KHR_external_fence_capabilities
VK_KHR_external_memory_capabilities
VK_KHR_external_semaphore_capabilities
VK_KHR_get_display_properties2
VK_KHR_get_physical_device_properties2
VK_KHR_get_surface_capabilities2
VK_KHR_portability_enumeration
VK_KHR_surface
VK_KHR_surface_protected_capabilities
VK_KHR_xcb_surface
VK_KHR_xlib_surface
VK_LUNARG_direct_driver_loading
```

Physical device result:

```text
Devices:
========

GPU0:
        apiVersion         = 1.4.335
        driverVersion      = 26.0.6
        vendorID           = 0x5143
        deviceID           = 0x7030001
        deviceType         = PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU
        deviceName         = Turnip Adreno (TM) 730
        driverID           = DRIVER_ID_MESA_TURNIP
        driverName         = turnip Mesa driver
        driverInfo         = Mesa 26.0.6 (git-0e095aab43)
        conformanceVersion = 1.4.0.0
        deviceUUID         = 21fb6def-6c6e-3954-98be-b698517830b5
        driverUUID         = 3a86872e-330f-d1ae-7710-72623ff50d18
```

This proved that:

1. the glibc Vulkan loader loaded the custom ICD;
2. the ICD loaded the newly built driver;
3. the driver opened the relevant GPU path sufficiently to instantiate a physical device;
4. the device was recognized as Adreno 730;
5. the active driver was Mesa Turnip 26.0.6;
6. KGSL support was compiled into the driver.

---

## 17. X11 Display Addressing Issue

One important runtime detail was the form of the X11 `DISPLAY` variable.

Using:

```text
DISPLAY=127.0.0.1:1
```

caused problems in some XCB/WSI tests.

Using:

```text
DISPLAY=:1
```

allowed clients to connect through the Termux:X11 Unix-domain socket.

Tracing showed connection to:

```text
@"/data/data/com.termux/files/usr/tmp/.X11-unix/X1"
```

A display query reported extensions including:

```text
DRI3
MIT-SHM
Present
XFIXES
```

Therefore:

```text
DISPLAY=:1
```

became the preferred configuration for direct X11 WSI tests.

---

## 18. Historical WSI Baselines

It is important to separate three different Mesa configurations.

### 18.1 Bionic Mesa 26.0.6

Bionic `vkcube` was confirmed to use XCB and detect the GPU:

```text
Selected WSI platform: xcb

Selected GPU 0:
Turnip Adreno (TM) 730,
type: IntegratedGpu,
apiVersion: 4211023 (1.4.335),
driverVersion: 109051910 (26.0.6)
```

This was a Bionic driver, not the custom glibc driver.

### 18.2 Packaged glibc Mesa 24.2.6

glibc `vkcube` was observed successfully through Xlib:

```bash
glibc-runner --no-linker \
  "$PREFIX/glibc/bin/vkcube" \
  --wsi xlib
```

Output:

```text
Selected GPU 0:
Turnip Adreno (TM) 730,
type: IntegratedGpu
```

XCB was also tested:

```bash
timeout 10s \
  env \
  DISPLAY=:1 \
  XDG_RUNTIME_DIR="$TMPDIR" \
  VK_ICD_FILENAMES="$GLIBC_FREEDRENO_ICD" \
  VK_DRIVER_FILES="$GLIBC_FREEDRENO_ICD" \
  glibc-runner --no-linker \
  "$PREFIX/glibc/bin/vkcube" \
  --wsi xcb
```

The test selected the Adreno 730 and remained alive until timeout, which was treated as successful execution of the rendering/presentation loop.

No `MESA_VK_WSI_DEBUG=sw` override was part of these preserved successful commands.

### 18.3 Custom glibc Mesa 26.0.6

For the custom build documented here, the preserved record proves:

```text
Vulkan loader initialization: PASS

ICD loading: PASS

KGSL-enabled Turnip loading: PASS

Physical device enumeration: PASS

Adreno 730 recognition: PASS
```

However:

```text
vanilla vkcube present:
not conclusively preserved in the surviving record
```

A `vkcube --wsi xcb` test was planned after the successful build, but the result is not present in the surviving transcript.

This means the historical baseline must be stated conservatively:

> Custom glibc Mesa 26.0.6 is confirmed through physical-device enumeration, but its direct WSI present behavior is not conclusively documented.

---

## 19. Attempted Zink Extension

After the Turnip driver succeeded, the build was expanded experimentally to include Zink.

The intended configuration was:

```bash
python -m mesonbuild.mesonmain setup \
  build-glibc-freedreno \
  --cross-file "$MESA_WORK/termux-glibc-aarch64.ini" \
  --prefix "$MESA_PREFIX" \
  -Dplatforms=x11 \
  -Dvulkan-drivers=freedreno \
  -Dfreedreno-kmds=kgsl \
  -Dgallium-drivers=zink \
  -Dopengl=true \
  -Degl=enabled \
  -Dglx=dri \
  -Dgles1=disabled \
  -Dgles2=enabled \
  -Dgbm=disabled \
  -Dllvm=disabled \
  -Dshared-llvm=disabled \
  -Dbuild-tests=false \
  -Dvalgrind=disabled \
  -Dlibunwind=disabled
```

This path introduced additional X11/GLX dependencies.

One configuration failure was:

```text
meson.build:2193:22:
ERROR: Dependency "xxf86vm" not found
(tried pkg-config)
```

Earlier, another dependency failure involved:

```text
Dependency "xrandr" not found
```

Thus the Zink/GLX extension required more complete target X11 development libraries than the minimal Vulkan-only Turnip build.

---

## 20. Compiler Wrapper Quoting Failure During Zink Build

The extended build later reached approximately:

```text
[925/1453]
Compiling C++ object ...
libzink.a.p/zink_draw.cpp
```

but another compilation unit failed with:

```text
<command-line>:
warning: missing terminating " character

gcc:
warning: and:
linker input file unused because linking not done

gcc:
error: and:
linker input file not found:
No such file or directory

gcc:
warning: libGLX":
linker input file unused because linking not done

gcc:
error: libGLX":
linker input file not found:
No such file or directory
```

This strongly suggested that a command-line definition containing spaces, likely text resembling:

```text
"... and libGLX"
```

had been split by the compiler wrapper.

The critical wrapper rule was therefore:

```bash
"$@"
```

must be used to preserve the original argument vector.

Using:

```bash
$*
```

or reconstructing arguments as a single string would be unsafe.

A small quote-preservation test was prepared:

```c
#ifndef TEST_NAME
#error TEST_NAME missing
#endif

#include <stdio.h>

int main(void) {
    puts(TEST_NAME);
    return 0;
}
```

Compile command:

```bash
~/.local/bin/glibc-gcc \
  '-DTEST_NAME="Mesa and libGLX"' \
  "$QT_DIR/quote-test.c" \
  -o "$QT_DIR/quote-test"
```

The first attempt incorrectly used `/tmp`, which is not the correct writable temporary directory in this Termux context.

Observed:

```text
bash: /tmp/quote-test.c:
Permission denied
```

The test was moved to:

```bash
QT_DIR="${TMPDIR:-$PREFIX/tmp}"
```

The compilation then exposed another wrapper/toolchain issue.

---

## 21. Linker Selection Failure

The quote test produced:

```text
ld: error:
unknown argument '--fix-cortex-a53-835769'

collect2:
error: ld returned 1 exit status
```

This indicated that GCC had selected an incompatible linker, most likely the host/native linker rather than the GNU linker expected by the glibc GCC toolchain.

The wrapper was modified to include:

```bash
export PATH="$PREFIX/glibc/bin:$PATH"
```

and:

```bash
-B"$PREFIX/glibc/bin/"
```

For example:

```bash
exec "$PREFIX/glibc/lib/ld-linux-aarch64.so.1" \
  --library-path "$PREFIX/glibc/lib" \
  "$PREFIX/glibc/bin/gcc" \
  -B"$PREFIX/glibc/bin/" \
  "$@"
```

The record does not preserve a later completed Zink build after these wrapper changes.

Therefore the project status must distinguish:

```text
Turnip KGSL Vulkan build:
SUCCESS

Zink + EGL + GLX extension:
PARTIAL / NOT CONCLUSIVELY COMPLETED
```

---

## 22. Patches and Source Modifications

The surviving record confirms one class of source-tree modification.

### Confirmed

Python generator shebang changes:

```text
/usr/bin/env python3
```

to the actual Termux Python path:

```text
/data/data/com.termux/files/usr/bin/python3
```

Representative files:

```text
src/compiler/isaspec/decode.py

src/compiler/isaspec/encode.py
```

### Not confirmed

The surviving record does not prove that any of the following runtime patch groups were applied:

```text
wsi-termux-x11 patches

tu_kgsl patches

anon-file patches

memfd compatibility patches

Termux package patch series
```

The final build clearly included KGSL support, but the record is consistent with enabling the upstream source backend using:

```text
-Dfreedreno-kmds=kgsl
```

rather than applying an external KGSL patch series.

A caveat remains:

> The surviving conversation does not independently prove that the source checkout was completely pristine before configuration.

If the original source tree is still available, the definitive audit should be:

```bash
cd ~/src/mesa-glibc-build/mesa

git status --short

git diff --stat

git diff

git log -1 --oneline

git rev-parse HEAD
```

Focused checks:

```bash
git diff -- \
  src/vulkan/wsi \
  src/freedreno/vulkan \
  src/util
```

---

## 23. Recommended Reproducibility Archive

The most valuable files to preserve are:

```text
~/src/mesa-glibc-build/termux-glibc-aarch64.ini

~/.local/bin/glibc-exec

~/.local/bin/glibc-gcc

~/.local/bin/glibc-g++

~/.local/bin/glibc-ar

~/.local/bin/glibc-ranlib

~/.local/bin/glibc-strip

~/.local/bin/glibc-pkg-config
```

The Meson configuration should also be archived:

```bash
python -m mesonbuild.mesonmain configure \
  ~/src/mesa-glibc-build/mesa/build-glibc-freedreno \
  > meson-configure.txt
```

Additional useful metadata:

```bash
git status --short
git diff
git rev-parse HEAD
git log -1 --oneline

python3 --version
python3 -m mesonbuild.mesonmain --version
ninja --version

~/.local/bin/glibc-gcc --version
```

The driver identity should be stored with:

```bash
glibc-runner --no-linker \
  "$PREFIX/glibc/bin/env" \
  LD_LIBRARY_PATH="$MESA_PREFIX/lib:$PREFIX/glibc/lib" \
  DISPLAY=:1 \
  XDG_RUNTIME_DIR="$TMPDIR" \
  VK_ICD_FILENAMES="$NEW_ICD" \
  VK_DRIVER_FILES="$NEW_ICD" \
  "$PREFIX/glibc/bin/vulkaninfo" --summary
```

---

## 24. Key Lessons

### 24.1 Host tools and target libraries can belong to different libc worlds

The build demonstrated that it is practical to use:

```text
Bionic Meson
Bionic Ninja
Bionic Python
```

while producing:

```text
glibc-linked Mesa driver binaries
```

provided that compiler, linker, pkg-config resolution, and target libraries are correctly separated.

### 24.2 Never leak glibc `LD_LIBRARY_PATH` into the Bionic host environment

Bad pattern:

```bash
export LD_LIBRARY_PATH="$PREFIX/glibc/lib"
```

before running Bionic shell tools.

Preferred pattern:

```bash
unset LD_LIBRARY_PATH
unset LD_PRELOAD
```

for host tools, then:

```bash
glibc-runner --no-linker \
  "$PREFIX/glibc/bin/env" \
  LD_LIBRARY_PATH="..." \
  target-program
```

for target execution.

### 24.3 KGSL must be explicitly selected

The difference between:

```text
freedreno-kmds = msm
```

and:

```text
freedreno-kmds = kgsl
```

was decisive.

MSM configuration produced:

```text
Failed to detect any valid GPUs
```

KGSL configuration produced:

```text
Turnip Adreno (TM) 730
```

### 24.4 Generator scripts are host tools

Mesa source generators execute during the build.

Their shebangs must therefore resolve in the Bionic host environment, even though the generated target objects are compiled for glibc.

This distinction explains why changing Python script shebangs was valid and did not contaminate the target ABI.

### 24.5 Compiler wrappers must preserve argv exactly

The Zink experiment showed that compile definitions containing spaces can be destroyed by careless wrappers.

Correct:

```bash
"$@"
```

Incorrect patterns include argument reconstruction or unquoted expansion.

### 24.6 Linker selection must be explicit when wrapping GCC

Using glibc GCC through a custom dynamic-loader wrapper can cause GCC to find an unintended host linker.

The observed symptom was:

```text
unknown argument '--fix-cortex-a53-835769'
```

Explicit toolchain selection using:

```bash
PATH="$PREFIX/glibc/bin:$PATH"
```

and:

```bash
-B"$PREFIX/glibc/bin/"
```

was introduced to address this.

---

## 25. Final Status Matrix

| Component | Result |
|---|---|
| Mesa 26.0.6 source compilation | Success |
| glibc target linkage | Success |
| Freedreno Vulkan driver | Success |
| Turnip driver initialization | Success |
| KGSL backend inclusion | Success |
| `/dev/kgsl-3d0` backend presence | Confirmed |
| Adreno 730 detection | Success |
| Vulkan 1.4.335 device API report | Success |
| Driver version 26.0.6 | Confirmed |
| XCB instance extension | Present |
| Xlib instance extension | Present |
| Custom glibc 26.0.6 `vulkaninfo` | Success |
| Custom glibc 26.0.6 vanilla `vkcube` present | Not conclusively preserved |
| glibc Mesa 24.2.6 vanilla XCB/Xlib `vkcube` | Success |
| Bionic Mesa 26.0.6 vanilla XCB `vkcube` | Success |
| Zink build extension | Partial |
| EGL/GLX Zink final validation | Not conclusively completed |

---

## 26. Final Conclusion

The experiment successfully established a reusable native Mesa build architecture for Android/Termux in which:

```text
Bionic host tools
        +
Termux glibc compiler
        +
Termux glibc target libraries
        +
Mesa Turnip
        +
KGSL
```

produced a working glibc Vulkan driver for the Qualcomm Adreno 730.

The most important verified result was:

```text
deviceName  = Turnip Adreno (TM) 730
driverName  = turnip Mesa driver
driverInfo  = Mesa 26.0.6 (git-0e095aab43)
apiVersion  = 1.4.335
```

The central build failure was initially caused by selecting the wrong kernel backend:

```text
freedreno-kmds = msm
```

After rebuilding with:

```text
freedreno-kmds = kgsl
```

physical-device enumeration succeeded.

The most important build-system adaptations were:

```text
Bionic host Meson/Ninja/Python
glibc target GCC and libraries
target-specific pkg-config wrapper
no global glibc LD_LIBRARY_PATH
Termux Python shebang repair for Mesa generators
explicit KGSL selection
careful compiler-wrapper argv preservation
explicit linker-toolchain selection
```

The Turnip/KGSL portion of the project should be regarded as successfully completed.

The Zink/GLX portion should be regarded separately: it progressed far into compilation but introduced additional X11 dependencies and exposed compiler-wrapper quoting/linker-selection problems. Its final success is not established by the surviving record.

Finally, when comparing this build against a later Mesa 26.1.4 build that crashes during vanilla presentation, the historical evidence should be used carefully. The valid comparison baseline is:

```text
Mesa 24.2.6 glibc:
vanilla XCB/Xlib vkcube present confirmed

Mesa 26.0.6 Bionic:
vanilla XCB vkcube present confirmed

custom Mesa 26.0.6 glibc KGSL:
device enumeration confirmed,
vanilla present not conclusively preserved
```

That distinction is essential before interpreting a Mesa 26.1.4 `SIGBUS` during direct WSI presentation as a version regression.
