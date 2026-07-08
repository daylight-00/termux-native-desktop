# Building Mesa 26.1.4 for Native Termux/Bionic
## Rebase of the Termux Mesa 26.0.6 Package Recipe, Patch Filtering, Failure Analysis, and Final Outcome

**Environment:** Native Termux / Android bionic userspace  
**Architecture:** AArch64  
**Target GPU path:** Qualcomm Adreno 730 → KGSL → Mesa Turnip  
**OpenGL path of interest:** GLX/OpenGL → Zink → Vulkan → Turnip  
**Display environment:** Termux:X11  
**Build system:** `termux-packages` on-device package build  
**Date of the recorded build session:** 2026-07-03  
**Target Mesa version:** 26.1.4  
**Base package recipe:** Termux `packages/mesa` recipe originally targeting Mesa 26.0.6

---

## 1. Scope

This report documents the process used to build Mesa 26.1.4 for the native Termux/bionic environment by rebasing the existing Termux Mesa 26.0.6 package recipe.

The document focuses on:

- why Mesa 26.1.4 was built;
- the starting state of the existing Termux graphics stack;
- the exact package version bump;
- the first on-device `termux-packages` build attempts;
- why the initial build appeared to stop before compiling Mesa;
- the distinction between the repository checkout and the real Termux build directory;
- dependency-resolution behavior with `-I`;
- use of trace mode and explicit bionic targeting;
- bypassing dependency resolution in order to reach the Mesa source and patch stages;
- patch application failures caused by rebasing a 26.0.6 patchset onto Mesa 26.1.4;
- the confirmed patch files removed from automatic application;
- the final result and the limits of the surviving transcript.

The picom compositor experiments that motivated the version-upgrade attempt are intentionally kept out of this report except where they explain the build objective. They belong in a separate compositor report.

---

## 2. Executive Summary

The system originally had a working native Termux Mesa 26.0.6 graphics stack. OpenGL was already hardware-accelerated through:

```text
GLX / OpenGL
    ↓
Zink
    ↓
Vulkan
    ↓
Turnip
    ↓
KGSL
    ↓
Adreno 730
```

The observed renderer before the Mesa 26.1.4 build work was:

```text
OpenGL renderer string: zink Vulkan 1.4(Turnip Adreno (TM) 730 (MESA_TURNIP))
Accelerated: yes
Mesa version: 26.0.6
```

Mesa 26.1.4 was then targeted in order to test newer Mesa behavior while preserving the Termux-native Zink/Turnip/KGSL stack.

The successful strategy was not to perform an unmanaged upstream `meson install` directly into `$PREFIX`. Instead, the existing Termux `packages/mesa` recipe was rebased from Mesa 26.0.6 to 26.1.4 and built through `termux-packages`.

The important findings were:

1. A simple version/SHA bump was sufficient to reach source preparation, but not sufficient to finish the build.
2. The first apparent “non-build” was actually a dependency-resolution problem before Mesa source compilation.
3. The real on-device build tree was under:

   ```text
   $HOME/.termux-build/mesa
   ```

   not under the repository-local `./.termux-build`.
4. Explicit bionic targeting was verified in trace output:

   ```text
   TERMUX_PACKAGE_LIBRARY=bionic
   TERMUX_HOST_PLATFORM=aarch64-linux-android
   TERMUX_ARCH=aarch64
   PREFIX=/data/data/com.termux/files/usr
   ```
5. `-I` caused the build to remain in dependency handling. Trace output showed the resolver entering the `libllvm` / `libcompiler-rt` dependency chain before Mesa source processing.
6. Skipping dependency resolution with `-s` allowed the build to proceed into source extraction and patch application.
7. At least two 26.0.6-era patch files were confirmed incompatible with Mesa 26.1.4 and were removed as whole patch files from automatic application:
   - `0003-fix-for-anon-file.patch`
   - `0006-wsi-no-pthread_cancel.patch`
8. “Filtering out a patch” meant disabling/removing the entire patch file from the patch-application set. It did **not** mean deleting selected hunks from inside the patch.
9. The main Termux `packages/mesa` stack used for this build did **not** include the older historical patches named:
   - `wsi-termux-x11.patch`
   - `tu_kgsl_export_dmabuf.patch`
10. KGSL support was instead provided by the modern Mesa/Termux configuration, including `freedreno` Vulkan support and the KGSL KMD path, plus KGSL-related workarounds present in the main patchset.
11. The user later confirmed that the rebased Mesa 26.1.4 build completed successfully and worked. The exact final package filename and complete post-install diagnostic transcript were not preserved in the conversation excerpt used for this report, so they are not fabricated here.

---

## 3. Starting Point: Working Native Mesa 26.0.6

Before attempting the 26.1.4 build, the native Termux graphics environment was already operational.

A representative `glxinfo -B` result was:

```text
name of display: :1
ATTENTION: default value of option vblank_mode overridden by environment.
display: :1  screen: 0
direct rendering: Yes
Extended renderer info (GLX_MESA_query_renderer):
    Vendor: Mesa (0x5143)
    Device: zink Vulkan 1.4(Turnip Adreno (TM) 730 (MESA_TURNIP)) (0x7030001)
    Version: 26.0.6
    Accelerated: yes
    Video memory: 8403MB
    Unified memory: yes
    Preferred profile: core (0x1)
    Max core profile version: 4.6
    Max compat profile version: 4.6
    Max GLES1 profile version: 1.1
    Max GLES[23] profile version: 3.2

OpenGL vendor string: Mesa
OpenGL renderer string: zink Vulkan 1.4(Turnip Adreno (TM) 730 (MESA_TURNIP))
OpenGL core profile version string: 4.6 (Core Profile) Mesa 26.0.6
OpenGL core profile shading language version string: 4.60

OpenGL version string: 4.6 (Compatibility Profile) Mesa 26.0.6
OpenGL shading language version string: 4.60

OpenGL ES profile version string: OpenGL ES 3.2 Mesa 26.0.6
OpenGL ES profile shading language version string: OpenGL ES GLSL ES 3.20
```

The same renderer was obtained both with an explicit Zink override:

```bash
MESA_LOADER_DRIVER_OVERRIDE=zink glxinfo -B
```

and without it:

```bash
glxinfo -B
```

This established that Zink was already the normal OpenGL renderer in the existing 26.0.6 native Termux environment.

That fact is important for later interpretation: the native bionic Mesa stack was not Turnip-only. Zink and Turnip coexisted successfully in the working 26.0.6 stack.

---

## 4. Why the Build Was Done

The immediate reason for trying Mesa 26.1.4 was to test a newer Mesa release in the same native Termux graphics environment.

The broader graphics stack under investigation was:

```text
Application
    │
    ├── OpenGL / GLX client
    │       ↓
    │     Zink
    │       ↓
    │     Vulkan
    │       ↓
    │     Turnip
    │
    └── Native Vulkan client
            ↓
          Turnip

Turnip
    ↓
KGSL
    ↓
Adreno 730
```

Because the existing package was integrated deeply with the Termux runtime, the chosen design constraint was:

> Preserve Termux packaging, prefix layout, bionic assumptions, Zink, Turnip, KGSL, GLX, EGL, and X11/Wayland build integration while changing the Mesa source version as narrowly as possible.

This ruled out an uncontrolled upstream install directly over `$PREFIX`.

---

## 5. Build Strategy

The selected strategy was:

1. clone or use the `termux-packages` tree;
2. modify only the Mesa package version and SHA initially;
3. build with `build-package.sh`;
4. explicitly target the bionic package library;
5. use trace mode when the build stopped before compilation;
6. bypass repository dependency resolution if necessary;
7. rebase or remove 26.0.6-era patches that no longer applied cleanly to 26.1.4;
8. produce a Termux package artifact rather than manually copying libraries into `$PREFIX`.

The working tree was:

```text
~/termux-packages
```

The Mesa package recipe was:

```text
~/termux-packages/packages/mesa/build.sh
```

---

## 6. Mesa Version Bump

The package recipe was modified to target Mesa 26.1.4.

The resulting relevant lines were:

```text
6:TERMUX_PKG_VERSION="26.1.4"
7:TERMUX_PKG_REVISION=1
8:TERMUX_PKG_SRCURL=https://archive.mesa3d.org/mesa-${TERMUX_PKG_VERSION}.tar.xz
9:TERMUX_PKG_SHA256=072705caa9adf4740f1489194b13e278ad959166863b5271fe423a86353c9ab6
```

The command used to verify the edit was:

```bash
grep -nE \
  'TERMUX_PKG_VERSION|TERMUX_PKG_SHA256|TERMUX_PKG_REVISION' \
  packages/mesa/build.sh
```

Output:

```text
6:TERMUX_PKG_VERSION="26.1.4"
7:TERMUX_PKG_REVISION=1
8:TERMUX_PKG_SRCURL=https://archive.mesa3d.org/mesa-${TERMUX_PKG_VERSION}.tar.xz
9:TERMUX_PKG_SHA256=072705caa9adf4740f1489194b13e278ad959166863b5271fe423a86353c9ab6
```

This confirmed that the package recipe itself had been changed correctly.

---

## 7. First Build Attempt

The first recorded build command was:

```bash
./build-package.sh -f -I mesa
```

The output began with Termux signing-key setup and package preparation:

```text
gpg: key B0076E490B71616B: 18 signatures not checked due to missing keys
gpg: key B0076E490B71616B: public key "Henrik Grimler <henrik@grimler.se>" imported
gpg: Total number processed: 1
gpg:               imported: 1
gpg: no ultimately trusted keys found

gpg: key 5A897D96E57CF20C: public key "Termux Releases (Termux automatic builds) <contact@termux.dev>" imported
gpg: Total number processed: 1
gpg:               imported: 1
gpg: Note: ultimately trusted key B0076E490B71616B expired
gpg: no ultimately trusted keys found

gpg: key 389CEED64573DFCA: public key "termux-pacman (security signature) <pacman@termux.dev>" imported
gpg: Total number processed: 1
gpg:               imported: 1
```

The build driver then identified the intended target:

```text
termux - building mesa for arch aarch64...
```

The system installed `termux-elf-cleaner`:

```text
The following NEW packages will be installed:
  termux-elf-cleaner

0 upgraded, 1 newly installed, 0 to remove and 20 not upgraded.
Need to get 18.1 kB of archives.
After this operation, 90.1 kB of additional disk space will be used.

Get:1 https://mirror.jeonnam.school/termux/termux-main stable/main aarch64 termux-elf-cleaner aarch64 3.0.1-1 [18.1 kB]

Selecting previously unselected package termux-elf-cleaner.
Preparing to unpack .../termux-elf-cleaner_3.0.1-1_aarch64.deb ...
Unpacking termux-elf-cleaner (3.0.1-1) ...
Setting up termux-elf-cleaner (3.0.1-1) ...
```

Then the package lists were refreshed:

```text
Hit:1 https://mirror.jeonnam.school/termux/termux-main stable InRelease
Hit:2 https://mirror.jeonnam.school/termux/termux-x11 x11 InRelease
Hit:3 https://packages-cf.termux.dev/apt/termux-glibc glibc InRelease
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
20 packages can be upgraded. Run 'apt list --upgradable' to see them.
```

After this, no Mesa package appeared in `output/`:

```bash
find output -type f -name 'mesa*.deb' -print
```

Output:

```text
```

At first glance this looked like Mesa had not built at all.

That interpretation was partly correct but required more precise diagnosis: the build driver had entered package preparation and dependency handling, but had not yet reached Mesa source compilation.

---

## 8. Initial Diagnostic Checks

The following environment variables were checked from the interactive shell:

```bash
echo "TERMUX_ON_DEVICE_BUILD=${TERMUX_ON_DEVICE_BUILD:-unset}"
echo "TERMUX_PACKAGE_LIBRARY=${TERMUX_PACKAGE_LIBRARY:-unset}"
```

Output:

```text
TERMUX_ON_DEVICE_BUILD=unset
TERMUX_PACKAGE_LIBRARY=unset
```

This did **not** prove that the build script had failed to recognize an on-device build. These values were merely unset in the parent interactive shell. Later trace output showed that `build-package.sh` correctly selected the native on-device path internally.

The package output directory was empty:

```bash
ls -lah output
```

Output:

```text
total 7.0K
drwx------.  2 u0_a534 u0_a534 3.4K Jul  3 16:30 .
drwx------. 13 u0_a534 u0_a534 3.4K Jul  3 16:30 ..
```

A repository-local `.termux-build` directory did not reveal the build state. The key discovery was that the actual default build top directory was under the home directory.

---

## 9. Real Build Directory Discovery

The actual build directory was found at:

```text
/data/data/com.termux/files/home/.termux-build/mesa
```

Command:

```bash
find ~/.termux-build -maxdepth 3 -type d -name '*mesa*' -print
```

Output:

```text
/data/data/com.termux/files/home/.termux-build/mesa
```

Directory listing:

```bash
ls -lah ~/.termux-build/mesa
```

Output:

```text
total 25K
drwx------. 7 u0_a534 u0_a534 3.4K Jul  3 16:35 .
drwx------. 6 u0_a534 u0_a534 3.4K Jul  3 16:35 ..
drwx------. 2 u0_a534 u0_a534 3.4K Jul  3 16:35 build
drwx------. 2 u0_a534 u0_a534 3.4K Jul  3 16:35 cache
drwx------. 2 u0_a534 u0_a534 3.4K Jul  3 16:35 massage
drwx------. 2 u0_a534 u0_a534 3.4K Jul  3 16:35 package
drwx------. 2 u0_a534 u0_a534 3.4K Jul  3 16:35 tmp
```

Tree:

```bash
find ~/.termux-build/mesa -maxdepth 2 -print
```

Output:

```text
/data/data/com.termux/files/home/.termux-build/mesa
/data/data/com.termux/files/home/.termux-build/mesa/build
/data/data/com.termux/files/home/.termux-build/mesa/package
/data/data/com.termux/files/home/.termux-build/mesa/tmp
/data/data/com.termux/files/home/.termux-build/mesa/cache
/data/data/com.termux/files/home/.termux-build/mesa/massage
```

The absence of a populated source tree at that point was another indication that the process had not yet reached normal Mesa source configuration and compilation.

---

## 10. Trace-Mode Build Investigation

Trace logging was enabled to determine exactly how far the build progressed.

The trace established the following facts.

### 10.1 Package recipe was found correctly

```text
TERMUX_PKG_BUILDER_DIR=/data/data/com.termux/files/home/termux-packages/packages/mesa
```

### 10.2 Target architecture was AArch64

```text
TERMUX_ARCH=aarch64
TERMUX_ARCH_BITS=64
TERMUX_REAL_ARCH=aarch64
```

### 10.3 Bionic was selected

```text
TERMUX_PACKAGE_LIBRARY=bionic
TERMUX_HOST_PLATFORM=aarch64-linux-android
TERMUX_REAL_HOST_PLATFORM=aarch64-linux-android
```

### 10.4 Native Termux prefix was selected

```text
prefix=/data/data/com.termux/files/usr
PREFIX=/data/data/com.termux/files/usr
```

### 10.5 Real package work directories

```text
TERMUX_PKG_CACHEDIR=/data/data/com.termux/files/home/.termux-build/mesa/cache
TERMUX_PKG_BUILDDIR=/data/data/com.termux/files/home/.termux-build/mesa/build
TERMUX_PKG_SRCDIR=/data/data/com.termux/files/home/.termux-build/mesa/src
TERMUX_PKG_PACKAGEDIR=/data/data/com.termux/files/home/.termux-build/mesa/package
TERMUX_PKG_TMPDIR=/data/data/com.termux/files/home/.termux-build/mesa/tmp
TERMUX_PKG_MASSAGEDIR=/data/data/com.termux/files/home/.termux-build/mesa/massage
```

### 10.6 Mesa recipe was sourced correctly

The trace entered:

```text
termux_step_start_build():3 source /data/data/com.termux/files/home/termux-packages/packages/mesa/build.sh
```

The version was recognized as:

```text
TERMUX_PKG_FULLVERSION=26.1.4
TERMUX_PKG_FULLVERSION+=-1
```

Thus the package identity became:

```text
26.1.4-1
```

---

## 11. Mesa Feature Configuration Observed in the Trace

The trace captured the package's Meson configuration block:

```text
--cmake-prefix-path /data/data/com.termux/files/usr
-Dgbm=enabled
-Dopengl=true
-Degl=enabled
-Degl-native-platform=x11
-Dgles1=disabled
-Dgles2=enabled
-Dglx=dri
-Dllvm=enabled
-Dshared-llvm=enabled
-Dplatforms=x11,wayland
-Dgallium-drivers=llvmpipe,softpipe,virgl,zink
-Dgallium-rusticl=true
-Dglvnd=enabled
-Dxmlconfig=disabled
```

This is one of the most important preserved results.

It confirms that the package build was not merely a Vulkan-only Turnip build. The bionic package recipe enabled:

- desktop OpenGL;
- EGL;
- GLES2;
- DRI-backed GLX;
- LLVM;
- X11 and Wayland platforms;
- Zink;
- software Gallium drivers;
- VirGL;
- Rusticl;
- GLVND integration.

For AArch64, the Termux Mesa package path also enabled the Freedreno Vulkan driver and KGSL KMD support in the package recipe used by this work:

```text
-Dvulkan-drivers=swrast,freedreno
-Dfreedreno-kmds=msm,kgsl
```

This means the intended native bionic architecture was:

```text
OpenGL client
    ↓
GLX/EGL
    ↓
Zink
    ↓
Vulkan
    ↓
Turnip/Freedreno Vulkan
    ↓
KGSL
    ↓
Adreno GPU
```

and, for direct Vulkan clients:

```text
Vulkan client
    ↓
Turnip
    ↓
KGSL
    ↓
Adreno GPU
```

---

## 12. Why the First Build Did Not Reach Mesa Compilation

The decisive trace section was:

```text
termux_step_get_dependencies
```

With `-I`, the script entered repository dependency handling:

```text
termux_step_get_dependencies():3 termux_download_repo_file
termux_download_repo_file():121 apt update
```

The resolver then generated the package build order:

```text
./scripts/buildorder.py -i \
  /data/data/com.termux/files/home/termux-packages/packages/mesa \
  packages root-packages x11-packages
```

The trace then entered the LLVM dependency chain:

```text
termux_step_get_dependencies():8 \
  termux_check_package_in_building_packages_list packages/libllvm
```

and subsequently:

```text
termux_extract_dep_info libcompiler-rt packages/libllvm
```

At this stage, the trace was still analyzing or resolving build dependencies. Mesa source extraction had not yet become the main operation.

This explained the original symptom:

```text
termux - building mesa for arch aarch64...
...
apt update
...
(no Mesa compile)
(no .deb in output/)
```

The build had not silently compiled and failed. It was stopped before normal source build activity.

---

## 13. Dependency Strategy Change

For the purpose of this experiment, the immediate goal was to reach the Mesa 26.1.4 source and determine whether the 26.0.6 Termux patchset could be rebased.

Therefore, the build strategy was changed from repository-driven dependency installation to a build using the already prepared local environment while skipping dependency checks.

The important option was:

```text
-s
```

The practical rebuild pattern became:

```bash
cd ~/termux-packages

rm -rf ~/.termux-build/mesa
rm -f output/mesa*.deb

./build-package.sh \
  --library bionic \
  -Q \
  -f \
  -r \
  -s \
  -j2 \
  mesa 2>&1 | tee ~/mesa-build-skipdeps.log

echo "EXIT=${PIPESTATUS[0]}"
find output -type f -name 'mesa*.deb' -print
```

The significant choices were:

- `--library bionic`  
  Explicitly target the native Termux/bionic package library.

- `-Q`  
  Enable shell trace/debug output.

- `-f`  
  Force rebuilding.

- `-r`  
  Remove/recreate source and build state as required for a clean reattempt.

- `-s`  
  Skip dependency checking so the process could reach the Mesa source and patch stages.

- `-j2`  
  Use conservative parallelism suitable for an on-device build.

The exact final successful invocation may have omitted `-Q` after diagnosis; the surviving transcript proves the trace/debug invocation and the successful rebase outcome, but does not preserve one canonical final command line verbatim. The command above accurately represents the diagnosed build path used during the rebase work.

---

## 14. First Patch Rebase Failure: `anon_file.c`

After dependency handling was bypassed, the build reached the Mesa source patch stage.

The first preserved patch failure was:

```text
+./build-package.sh termux_step_patch_package():22 sed \
  -e 's%\@TERMUX_APP_PACKAGE\@%com.termux%g' \
  -e 's%\@TERMUX_BASE_DIR\@%/data/data/com.termux/files%g' \
  -e 's%\@TERMUX_CACHE_DIR\@%/data/data/com.termux/cache%g' \
  -e 's%\@TERMUX_HOME\@%/data/data/com.termux/files/home%g' \
  -e 's%\@TERMUX_PREFIX\@%/data/data/com.termux/files/usr%g' \
  -e 's%\@TERMUX_PREFIX_CLASSICAL\@%/data/data/com.termux/files/usr%g' \
  -e 's%\@TERMUX_ENV__S_TERMUX\@%TERMUX__%g' \
  -e 's%\@TERMUX_ENV__S_TERMUX_APP\@%TERMUX_APP__%g' \
  -e 's%\@TERMUX_ENV__S_TERMUX_API_APP\@%TERMUX_API_APP__%g' \
  -e 's%\@TERMUX_ENV__S_TERMUX_ROOTFS\@%TERMUX_ROOTFS__%g' \
  -e 's%\@TERMUX_ENV__S_TERMUX_EXEC\@%TERMUX_EXEC__%g' \
  /data/data/com.termux/files/home/termux-packages/packages/mesa/0003-fix-for-anon-file.patch

+./build-package.sh termux_step_patch_package():34 patch --silent -p1

1 out of 1 hunk FAILED -- saving rejects to file src/util/anon_file.c.rej
```

The process exited with:

```text
EXIT=1
```

and no package was produced:

```bash
find output -type f -name 'mesa*.deb' -print
```

Output:

```text
```

### Interpretation

`0003-fix-for-anon-file.patch` had been written against the older Mesa source layout and no longer applied cleanly to Mesa 26.1.4.

Its role was Termux-specific path adaptation for anonymous-file/runtime-directory fallback behavior.

### Rebase decision

The patch was removed from automatic application as a **whole patch file**.

Conceptually:

```text
0003-fix-for-anon-file.patch
    ↓
0003-fix-for-anon-file.patch.disabled
```

or equivalently moved outside the patch auto-application set.

No internal hunk editing was used.

This distinction matters:

```text
NOT DONE:
- remove only the rejected hunk;
- apply the patch partially;
- manually accept some patch hunks and reject others.

DONE:
- remove the entire patch file from automatic application.
```

---

## 15. Second Patch Rebase Failure: Wayland WSI / `pthread_cancel`

After the first incompatible patch was removed and the build was retried, a second source-level patch failure occurred:

```text
+./build-package.sh termux_step_patch_package():34 patch --silent -p1

1 out of 1 hunk FAILED -- saving rejects to file src/vulkan/wsi/wsi_common_wayland.c.rej
```

The build again exited:

```text
EXIT=1
```

and again no `.deb` appeared:

```text
```

The patch associated with this source file in the 26.0.6-era Termux package stack was:

```text
0006-wsi-no-pthread_cancel.patch
```

### Interpretation

The 26.1.4 Wayland WSI source had changed sufficiently that the old patch context no longer matched.

The old patch's purpose was tied to Android/bionic thread cancellation behavior, replacing or avoiding a normal `pthread_cancel()`-based path.

### Rebase decision

This patch was also excluded as a **whole patch file** from automatic application.

Thus the two confirmed removals during the 26.1.4 rebase were:

```text
0003-fix-for-anon-file.patch
0006-wsi-no-pthread_cancel.patch
```

Again, these were file-level exclusions, not hunk-level filters.

---

## 16. Patchset Provenance and What Was Not in It

The 26.1.4 bionic build was based on the main Termux `packages/mesa` patchset used with the 26.0.6 package recipe.

The base inventory discussed during the investigation was:

```text
0000-disable-android-detection.patch
0001-disable-multithreading-for-llvmpipe.patch
0002-fix-for-getprogname.patch
0003-fix-for-anon-file.patch
0004-do-not-check-xlocale.patch
0005-virgl-socket-path.patch
0006-wsi-no-pthread_cancel.patch
0007-use-mtx_t-operations-in-turnip.patch
0008-workaround-fortify-check.patch
0009-disable-resource_create_front-for-vtest.patch

0011-lld-undefined-version.diff
0012-always-use-software-for-swrast.patch
0013-detect-sve-sve2-support.patch
0014-replace-turnip-wait_timestamp_safe-assert.patch
0015-define-reallocarray.patch
0016-unofficial_support_adreno_710_720_722.patch
0017-preserve-egl-support-in-zink.patch
0018-disable-general-layout-in-zink-for-turnip.patch
0019-UBWC_5-and-UBWC_6-support.patch
0020-unofficial-support-adreno-830.patch
0021-unofficial-support-adreno-810-825-829.patch
```

### Confirmed removed during the 26.1.4 rebase

```text
0003-fix-for-anon-file.patch
0006-wsi-no-pthread_cancel.patch
```

### Important historical patches that were not part of this main package recipe

The build did **not** rely on separate historical patches named:

```text
wsi-termux-x11.patch
tu_kgsl_export_dmabuf.patch
```

Those belong to a different historical DRI3/Termux:X11 packaging lineage and should not be confused with the main `packages/mesa` recipe used here.

The modern package path used:

```text
-Dvulkan-drivers=swrast,freedreno
-Dfreedreno-kmds=msm,kgsl
```

and retained KGSL-related handling through the modern Turnip/KGSL code path and package patchset, including:

```text
0014-replace-turnip-wait_timestamp_safe-assert.patch
```

The absence of `tu_kgsl_export_dmabuf.patch` therefore does not mean KGSL was disabled.

---

## 17. Patch Selection Philosophy

The rebase exposed an important rule for future Mesa upgrades:

> Do not assume that every patch from an older Termux Mesa package must be mechanically forward-ported.

The patches fall into several categories.

### 17.1 Bionic/Android compatibility patches

Examples:

```text
0002-fix-for-getprogname.patch
0003-fix-for-anon-file.patch
0006-wsi-no-pthread_cancel.patch
0008-workaround-fortify-check.patch
0015-define-reallocarray.patch
```

These should be evaluated against:

- whether upstream Mesa changed;
- whether the Android/bionic limitation still exists;
- whether the patch's behavior is still needed;
- whether a normal runtime environment variable can replace a hardcoded path workaround.

### 17.2 Graphics-stack behavior patches

Examples:

```text
0007-use-mtx_t-operations-in-turnip.patch
0014-replace-turnip-wait_timestamp_safe-assert.patch
0017-preserve-egl-support-in-zink.patch
0018-disable-general-layout-in-zink-for-turnip.patch
0019-UBWC_5-and-UBWC_6-support.patch
```

These are more directly related to Turnip, KGSL, Zink, EGL, image layouts, or GPU behavior and therefore deserve more careful preservation or rebase testing.

### 17.3 Device-support patches

Examples:

```text
0016-unofficial_support_adreno_710_720_722.patch
0020-unofficial-support-adreno-830.patch
0021-unofficial-support-adreno-810-825-829.patch
```

These are device-family-specific and may be irrelevant to an Adreno 730 system, even though keeping them in the package recipe may still be appropriate for a general-purpose Termux package.

---

## 18. Final Outcome

The later session state confirmed:

> The Mesa 26.1.4 bionic build was ultimately completed successfully and worked.

The successful build should therefore be understood as:

```text
Termux main Mesa 26.0.6 package recipe
    ↓
Version bump to 26.1.4
    ↓
On-device bionic build path
    ↓
Dependency-stage diagnosis
    ↓
Skip dependency resolution for the rebase experiment
    ↓
Rebase/filter incompatible patch files
    ↓
Build completion
    ↓
Operational Mesa 26.1.4 native bionic stack
```

However, the surviving conversation excerpt does **not** preserve:

- the exact final `output/mesa_*.deb` filename;
- the final `dpkg -i` line;
- a complete post-install `glxinfo -B` transcript explicitly showing Mesa 26.1.4;
- a final `vulkaninfo --summary` transcript from the newly installed bionic 26.1.4 package;
- the exact final list of every patch file present in the local directory at the instant of the successful build.

Therefore this report deliberately does not invent those outputs.

What is preserved and certain is:

- the version bump;
- the bionic/AArch64 target;
- the package recipe configuration;
- the real build directory;
- the dependency-stage behavior;
- the two exact patch failures;
- the two confirmed file-level patch exclusions;
- the fact that the final rebased build later succeeded and was operational.

---

## 19. Reproducible Build Procedure

The following procedure captures the working approach derived from the session.

### 19.1 Prepare the package tree

```bash
cd ~/termux-packages
```

Verify the Mesa recipe:

```bash
grep -nE \
  'TERMUX_PKG_VERSION|TERMUX_PKG_SHA256|TERMUX_PKG_REVISION' \
  packages/mesa/build.sh
```

Expected target:

```text
TERMUX_PKG_VERSION="26.1.4"
TERMUX_PKG_REVISION=1
TERMUX_PKG_SHA256=072705caa9adf4740f1489194b13e278ad959166863b5271fe423a86353c9ab6
```

### 19.2 Clean the Mesa build tree

```bash
rm -rf ~/.termux-build/mesa
rm -f output/mesa*.deb
```

### 19.3 Run an explicit bionic trace build

For diagnosis:

```bash
./build-package.sh \
  --library bionic \
  -Q \
  -f \
  -r \
  -s \
  -j2 \
  mesa 2>&1 | tee ~/mesa-build-debug.log
```

Preserve the real build exit status:

```bash
echo "EXIT=${PIPESTATUS[0]}"
```

Check output artifacts:

```bash
find output -type f -name 'mesa*.deb' -print
```

### 19.4 Inspect a patch reject

If the build reports:

```text
... saving rejects to file path/to/source.c.rej
```

identify the matching patch:

```bash
cd ~/termux-packages/packages/mesa
grep -RIl 'source.c' *.patch
```

For this specific rebase, the two confirmed incompatible patches were:

```text
0003-fix-for-anon-file.patch
0006-wsi-no-pthread_cancel.patch
```

Disable the whole patch file rather than partially applying it.

Example pattern:

```bash
mv 0003-fix-for-anon-file.patch \
   0003-fix-for-anon-file.patch.disabled

mv 0006-wsi-no-pthread_cancel.patch \
   0006-wsi-no-pthread_cancel.patch.disabled
```

Then clean and rebuild.

### 19.5 Verify runtime environment

Useful checks after installation include:

```bash
glxinfo -B
```

```bash
vulkaninfo --summary
```

```bash
ls -l "$PREFIX/share/vulkan/icd.d"
```

```bash
find "$PREFIX/lib" -maxdepth 2 \
  \( -name 'libvulkan_freedreno.so*' \
  -o -name 'libGLX_mesa.so*' \
  -o -name 'libEGL_mesa.so*' \) \
  -print
```

For OpenGL-over-Vulkan verification:

```bash
MESA_LOADER_DRIVER_OVERRIDE=zink glxinfo -B
```

The desired renderer pattern is:

```text
zink Vulkan ... Turnip Adreno ...
Accelerated: yes
```

---

## 20. Important Distinction: Bionic Build vs. Later glibc Build Investigation

A later glibc experiment found that, for one Mesa 26.1.4 kit configuration:

```text
turnip-only build        → GOOD
zink-enabled full build  → SIGBUS in Vulkan present path
```

That result should **not** be retroactively generalized to the native bionic stack.

The native bionic Mesa 26.0.6 environment already proved that:

```text
Zink enabled
+
Turnip enabled
+
KGSL enabled
+
GLX/OpenGL acceleration
```

could coexist successfully.

Therefore:

```text
Incorrect generalization:
"Zink and Turnip can never coexist."

More accurate conclusion:
"A specific glibc Mesa 26.1.4 full-build configuration produced a bad runtime result,
while the native bionic package lineage demonstrates that Zink + Turnip coexistence
is possible."
```

This distinction matters when comparing the bionic rebase with the later glibc kit work.

---

## 21. Lessons Learned

### 21.1 Use the package system for a system graphics stack

Mesa is not one isolated shared object. A native graphics stack includes tightly related components such as:

```text
libEGL_mesa
libGLX_mesa
Gallium drivers
Zink
Turnip Vulkan ICD
ICD JSON files
GLVND integration
GBM
DRI/WSI support
LLVM-dependent components
```

For the native Termux/bionic environment, rebuilding through `termux-packages` was safer than overlaying selected upstream libraries into `$PREFIX`.

### 21.2 `-I` can hide the real build stage

A build that prints:

```text
termux - building mesa for arch aarch64...
```

has not necessarily started Mesa compilation.

Trace output must be used to distinguish:

```text
dependency resolution
source download
patch application
Meson configure
Ninja compile
package creation
```

### 21.3 The real on-device build tree matters

The build state was under:

```text
~/.termux-build/mesa
```

not:

```text
~/termux-packages/.termux-build/mesa
```

Looking in the wrong directory initially obscured the actual build state.

### 21.4 A package version bump is not the same as a patchset rebase

Changing:

```text
26.0.6 → 26.1.4
```

was trivial.

The real work was validating every downstream patch against the new source.

The first two confirmed failures were:

```text
src/util/anon_file.c
src/vulkan/wsi/wsi_common_wayland.c
```

### 21.5 Patch filtering must be documented precisely

In this work:

```text
"filtered out"
```

means:

```text
the complete patch file was removed from automatic application
```

not:

```text
selected hunks were deleted from inside the patch.
```

This precision is necessary when later comparing bionic and glibc patch stacks.

### 21.6 Do not automatically port bionic workarounds into glibc

Examples such as:

```text
Termux prefix /tmp fallback
Android/bionic pthread cancellation workarounds
fortify workarounds
Android API compatibility shims
```

may be unnecessary or harmful in a glibc build.

By contrast, graphics behavior patches involving:

```text
Turnip
KGSL
Zink
EGL
image layouts
UBWC
WSI buffer handling
```

should be evaluated on graphics-stack behavior rather than libc identity alone.

---

## 22. Raw Transcript Appendix

This appendix preserves the most important command/output fragments from the build session.

### 22.1 Initial build

```bash
./build-package.sh -f -I mesa
```

Output excerpt:

```text
termux - building mesa for arch aarch64...
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done

The following NEW packages will be installed:
  termux-elf-cleaner

0 upgraded, 1 newly installed, 0 to remove and 20 not upgraded.
Need to get 18.1 kB of archives.
After this operation, 90.1 kB of additional disk space will be used.

Get:1 https://mirror.jeonnam.school/termux/termux-main stable/main aarch64 termux-elf-cleaner aarch64 3.0.1-1 [18.1 kB]
Fetched 18.1 kB in 0s (50.0 kB/s)

Selecting previously unselected package termux-elf-cleaner.
Preparing to unpack .../termux-elf-cleaner_3.0.1-1_aarch64.deb ...
Unpacking termux-elf-cleaner (3.0.1-1) ...
Setting up termux-elf-cleaner (3.0.1-1) ...

Hit:1 https://mirror.jeonnam.school/termux/termux-main stable InRelease
Hit:2 https://mirror.jeonnam.school/termux/termux-x11 x11 InRelease
Hit:3 https://packages-cf.termux.dev/apt/termux-glibc glibc InRelease

Reading package lists... Done
Building dependency tree... Done
Reading state information... Done

20 packages can be upgraded. Run 'apt list --upgradable' to see them.
```

Artifact check:

```bash
find output -type f -name 'mesa*.deb' -print
```

Output:

```text
```

---

### 22.2 Version verification

```bash
grep -nE \
  'TERMUX_PKG_VERSION|TERMUX_PKG_SHA256|TERMUX_PKG_REVISION' \
  packages/mesa/build.sh
```

Output:

```text
6:TERMUX_PKG_VERSION="26.1.4"
7:TERMUX_PKG_REVISION=1
8:TERMUX_PKG_SRCURL=https://archive.mesa3d.org/mesa-${TERMUX_PKG_VERSION}.tar.xz
9:TERMUX_PKG_SHA256=072705caa9adf4740f1489194b13e278ad959166863b5271fe423a86353c9ab6
```

---

### 22.3 Interactive-shell environment check

```bash
echo "TERMUX_ON_DEVICE_BUILD=${TERMUX_ON_DEVICE_BUILD:-unset}"
echo "TERMUX_PACKAGE_LIBRARY=${TERMUX_PACKAGE_LIBRARY:-unset}"
```

Output:

```text
TERMUX_ON_DEVICE_BUILD=unset
TERMUX_PACKAGE_LIBRARY=unset
```

---

### 22.4 Output directory

```bash
ls -lah output
```

Output:

```text
total 7.0K
drwx------.  2 u0_a534 u0_a534 3.4K Jul  3 16:30 .
drwx------. 13 u0_a534 u0_a534 3.4K Jul  3 16:30 ..
```

---

### 22.5 Real build directory

```bash
find ~/.termux-build -maxdepth 3 -type d -name '*mesa*' -print
```

Output:

```text
/data/data/com.termux/files/home/.termux-build/mesa
```

```bash
ls -lah ~/.termux-build/mesa
```

Output:

```text
total 25K
drwx------. 7 u0_a534 u0_a534 3.4K Jul  3 16:35 .
drwx------. 6 u0_a534 u0_a534 3.4K Jul  3 16:35 ..
drwx------. 2 u0_a534 u0_a534 3.4K Jul  3 16:35 build
drwx------. 2 u0_a534 u0_a534 3.4K Jul  3 16:35 cache
drwx------. 2 u0_a534 u0_a534 3.4K Jul  3 16:35 massage
drwx------. 2 u0_a534 u0_a534 3.4K Jul  3 16:35 package
drwx------. 2 u0_a534 u0_a534 3.4K Jul  3 16:35 tmp
```

---

### 22.6 Trace proof of bionic/AArch64 selection

```text
TERMUX_PACKAGE_LIBRARY=bionic
TERMUX_ARCH=aarch64
TERMUX_ARCH_BITS=64
TERMUX_HOST_PLATFORM=aarch64-linux-android
TERMUX_REAL_HOST_PLATFORM=aarch64-linux-android
PREFIX=/data/data/com.termux/files/usr
```

---

### 22.7 Trace proof of package paths

```text
TERMUX_PKG_BUILDER_DIR=/data/data/com.termux/files/home/termux-packages/packages/mesa
TERMUX_PKG_CACHEDIR=/data/data/com.termux/files/home/.termux-build/mesa/cache
TERMUX_PKG_BUILDDIR=/data/data/com.termux/files/home/.termux-build/mesa/build
TERMUX_PKG_SRCDIR=/data/data/com.termux/files/home/.termux-build/mesa/src
TERMUX_PKG_PACKAGEDIR=/data/data/com.termux/files/home/.termux-build/mesa/package
TERMUX_PKG_TMPDIR=/data/data/com.termux/files/home/.termux-build/mesa/tmp
TERMUX_PKG_MASSAGEDIR=/data/data/com.termux/files/home/.termux-build/mesa/massage
```

---

### 22.8 Trace proof of major Mesa feature configuration

```text
--cmake-prefix-path /data/data/com.termux/files/usr
-Dgbm=enabled
-Dopengl=true
-Degl=enabled
-Degl-native-platform=x11
-Dgles1=disabled
-Dgles2=enabled
-Dglx=dri
-Dllvm=enabled
-Dshared-llvm=enabled
-Dplatforms=x11,wayland
-Dgallium-drivers=llvmpipe,softpipe,virgl,zink
-Dgallium-rusticl=true
-Dglvnd=enabled
-Dxmlconfig=disabled
```

---

### 22.9 Trace proof of dependency-stage stop

```text
termux_step_get_dependencies
termux_download_repo_file
apt update
./scripts/buildorder.py -i \
  /data/data/com.termux/files/home/termux-packages/packages/mesa \
  packages root-packages x11-packages

termux_check_package_in_building_packages_list packages/libllvm
termux_extract_dep_info libcompiler-rt packages/libllvm
```

---

### 22.10 `anon_file.c` patch rejection

```text
+./build-package.sh termux_step_patch_package():34 patch --silent -p1
1 out of 1 hunk FAILED -- saving rejects to file src/util/anon_file.c.rej
```

Exit:

```text
EXIT=1
```

---

### 22.11 Wayland WSI patch rejection

```text
+./build-package.sh termux_step_patch_package():34 patch --silent -p1
1 out of 1 hunk FAILED -- saving rejects to file src/vulkan/wsi/wsi_common_wayland.c.rej
```

Exit:

```text
EXIT=1
```

---

## 23. Final State Summary

The Mesa build effort established a reproducible native Termux/bionic rebase workflow:

```text
Working Mesa 26.0.6 Termux package
    ↓
Change package version and source checksum to 26.1.4
    ↓
Run native `termux-packages` build
    ↓
Diagnose pre-build dependency handling with trace mode
    ↓
Confirm explicit bionic / AArch64 target
    ↓
Use real build root under ~/.termux-build
    ↓
Skip dependency resolution for controlled source/patch testing
    ↓
Reach Mesa 26.1.4 source patch stage
    ↓
Remove incompatible patch files:
    - 0003-fix-for-anon-file.patch
    - 0006-wsi-no-pthread_cancel.patch
    ↓
Continue patchset rebase
    ↓
Complete the Mesa 26.1.4 bionic build
    ↓
Confirm operational result
```

The central engineering lesson is that the successful 26.1.4 build was not a raw upstream build. It was a controlled rebase of the Termux-native Mesa packaging model, preserving the bionic prefix, GLX/EGL integration, Zink, Turnip, and KGSL configuration while selectively removing downstream patches that no longer applied to the newer Mesa source.
