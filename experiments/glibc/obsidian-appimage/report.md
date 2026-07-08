# AppImage Onboarding Experiment: Obsidian on the Native Termux glibc Layer

**Status:** Complete and verified  
**Experiment date:** 2026-07-05 to 2026-07-06  
**Target application:** Obsidian 1.12.7, arm64 AppImage  
**Device class:** arm64 Android, stock kernel, no root, Termux + Termux:X11  
**Execution model:** native glibc process on top of Termux, no proot at runtime

---

## 1. Purpose

This experiment tested whether an AppImage can be treated as a third application input format for the `gl` project, alongside upstream `tar.gz` archives and Debian packages.

The working hypothesis was:

```text
AppImage
  -> locate embedded SquashFS
  -> extract AppDir
  -> reuse the existing gl application-onboarding pipeline
```

That hypothesis was confirmed.

The final successful flow was:

```text
Obsidian AppImage
  -> calculate SquashFS offset
  -> cross-check `hsqs` magic position
  -> split embedded SquashFS payload
  -> extract with squashfs-tools-ng
  -> inventory ELF files
  -> patch interpreter and RPATH
  -> verify every ELF with glibc ldd
  -> launch Electron with the existing gl environment contract
  -> verify X11, TLS, GPU, and Obsidian CLI integration
```

The AppImage-specific work ended at AppDir extraction. Everything after that reused the existing `gl` architecture.

---

## 2. Relevant Project Runtime Model

The experiment was performed against the established native glibc layer:

```text
[application]  ~/gl/apps/<name>/
[shared farm]  ~/gl/lib/
[glibc core]   $PREFIX/glibc/
[Debian store] $PREFIX/var/lib/proot-distro/containers/debian/rootfs
```

The runtime library lookup contract remained:

```text
$ORIGIN
  -> $PREFIX/glibc/lib
  -> ~/gl/lib
```

The experiment did not use `LD_LIBRARY_PATH`.

This was important for two reasons:

1. the Termux shell is a bionic process and must not be exposed to glibc library search paths;
2. the glibc application must prefer Android-adapted core libraries such as the glibc-repo X11/xcb builds before the general Debian library farm.

All glibc process launches also cleared the inherited Termux preload environment with:

```bash
env LD_PRELOAD=
```

This became important again later for the Obsidian CLI.

---

## 3. Why AppImage Needs an Extra Front-End Adapter

The tested AppImage was a Type 2 style image with this practical layout:

```text
[ELF runtime stub][embedded SquashFS filesystem]
```

Unlike a tarball, the file does not begin with the application archive payload. A SquashFS-aware tool therefore cannot necessarily consume the whole AppImage directly.

The AppImage runtime was not used. Instead, the embedded filesystem was located and extracted without executing the AppImage runtime.

This is desirable on the project target because:

- the runtime ELF belongs to the normal Linux/glibc world;
- the default AppImage execution model expects FUSE/mount behavior that is not part of the desired unprivileged Android execution path;
- the project already has a stable model for unpacked application trees.

The effective abstraction is therefore:

```text
tar.gz    -> tar extraction        -> App Tree
.deb      -> payload extraction    -> App Tree
AppImage  -> SquashFS extraction   -> App Tree
                                      |
                                      v
                              common gl pipeline
```

---

## 4. Tooling Difference on Termux: squashfs-tools-ng

The available Termux package was:

```text
squashfs-tools-ng
```

This does not provide the classic `unsquashfs` command. Instead it provides tools such as:

```text
rdsquashfs
gensquashfs
sqfs2tar
tar2sqfs
```

The original plan used:

```bash
unsquashfs -o "$OFF" ...
```

but that command was unavailable.

The adopted approach was therefore:

```text
AppImage
  -> split at SquashFS offset
  -> raw .squashfs temporary file
  -> sqfs2tar | tar -x
```

This turned out to be simple and reliable.

---

## 5. Offset Discovery

### 5.1 Initial parsing mistake

The first ELF-header parsing attempt used `$NF` on the output of `readelf -h`. For a line such as:

```text
Start of section headers:          123456 (bytes into file)
```

`$NF` is not the numeric offset; it is the trailing text token. In awk numeric context this became zero, producing an invalid offset.

The corrected parser extracts the numeric value from the field after the colon.

### 5.2 Correct calculation

The SquashFS offset was calculated as the end of the ELF section-header table:

```text
OFF = e_shoff + e_shentsize * e_shnum
```

The working shell sequence was:

```bash
APP=$(ls Obsidian-*arm64*.AppImage | head -1)

o=$(readelf -h "$APP" \
  | awk -F: '/Start of section headers/{print $2}' \
  | grep -oE '[0-9]+' \
  | head -1)

s=$(readelf -h "$APP" \
  | awk -F: '/Size of section headers/{print $2}' \
  | grep -oE '[0-9]+' \
  | head -1)

n=$(readelf -h "$APP" \
  | awk -F: '/Number of section headers/{print $2}' \
  | grep -oE '[0-9]+' \
  | head -1)

OFF=$((o + s*n))
echo "elf-calc offset=$OFF"
```

The actual result was:

```text
elf-calc offset=197808
```

### 5.3 Cross-check with SquashFS magic

The result was cross-checked using the SquashFS magic string:

```bash
grep -abo hsqs "$APP" | head -3
```

Observed result:

```text
197808:hsqs
```

The calculated ELF boundary and the first SquashFS magic position matched exactly:

```text
ELF-calculated offset = 197808
hsqs magic offset      = 197808
```

This was treated as the extraction gate.

---

## 6. Splitting and Extracting the SquashFS Payload

The AppImage payload was split using `tail`:

```bash
tail -c +$((OFF+1)) "$APP" \
  > "$PREFIX/tmp/obsidian.squashfs"
```

The `+1` is required because the byte offset is zero-based while `tail -c +N` starts from a one-based byte position.

The temporary image was validated:

```bash
head -c 4 "$PREFIX/tmp/obsidian.squashfs"
```

Observed output:

```text
hsqs
```

Extraction used the `squashfs-tools-ng` tar bridge:

```bash
mkdir -p ~/gl/apps/obsidian

sqfs2tar "$PREFIX/tmp/obsidian.squashfs" \
  | tar -x -C ~/gl/apps/obsidian

rm "$PREFIX/tmp/obsidian.squashfs"
```

The extracted top-level layout was:

```text
.DirIcon
AppRun
LICENSE.electron.txt
LICENSES.chromium.html
chrome-sandbox
chrome_100_percent.pak
chrome_200_percent.pak
chrome_crashpad_handler
icudtl.dat
libEGL.so
libGLESv2.so
libffmpeg.so
libvk_swiftshader.so
libvulkan.so.1
locales/
obsidian
obsidian-cli
obsidian.desktop
obsidian.png
resources/
resources.pak
snapshot_blob.bin
usr/
v8_context_snapshot.bin
vk_swiftshader_icd.json
```

This confirmed that the payload was a normal Electron AppDir-style tree.

---

## 7. ELF Inventory

The extracted tree contained 11 ELF files:

```text
chrome-sandbox
chrome_crashpad_handler
libEGL.so
libGLESv2.so
libffmpeg.so
libvk_swiftshader.so
libvulkan.so.1
obsidian
obsidian-cli
resources/app.asar.unpacked/node_modules/btime/binding.node
resources/app.asar.unpacked/node_modules/get-fonts/binding.node
```

The important entry points were:

```text
AppRun                   shell script
obsidian                 aarch64 PIE executable
obsidian-cli             aarch64 PIE executable
chrome-sandbox           aarch64 PIE executable
chrome_crashpad_handler  aarch64 PIE executable
```

The upstream main executable initially used:

```text
interpreter: /lib/ld-linux-aarch64.so.1
RPATH:      $ORIGIN
```

The existing `$ORIGIN` was important and had to be preserved when applying the project RPATH policy.

---

## 8. ELF Patching

The normal project patching rule was applied unchanged.

```bash
LOADER="$PREFIX/glibc/lib/ld-linux-aarch64.so.1"
RPATH='$ORIGIN:'"$PREFIX/glibc/lib:$HOME/gl/lib"

find "$APPDIR" -type f | while IFS= read -r f; do
  case "$(file -b "$f")" in
    *"ELF 64-bit"*executable*|*"ELF 64-bit"*"pie executable"*)
      patchelf \
        --set-interpreter "$LOADER" \
        --set-rpath "$RPATH" \
        "$f"
      ;;

    *"ELF 64-bit"*"shared object"*)
      patchelf \
        --set-rpath "$RPATH" \
        "$f"
      ;;
  esac
done
```

The verified main executable state became:

```text
interpreter:
/data/data/com.termux/files/usr/glibc/lib/ld-linux-aarch64.so.1

rpath:
$ORIGIN:/data/data/com.termux/files/usr/glibc/lib:/data/data/com.termux/files/home/gl/lib
```

The same interpreter contract applied to the executable ELF files, including `obsidian-cli`.

---

## 9. Dependency Verification

Every ELF in the extracted application tree was scanned with the glibc `ldd` while clearing `LD_PRELOAD`:

```bash
while IFS= read -r f; do
  env LD_PRELOAD= \
    "$PREFIX/glibc/bin/ldd" "$f" 2>&1 \
    | grep 'not found' || true
done < "$PREFIX/tmp/obsidian-elf-list.txt"
```

Final result:

```text
ALL ELF DEPENDENCIES RESOLVED
```

No additional Debian package installation or farm refresh was needed.

The main executable resolved the expected library classes correctly:

- application-local Electron libraries from `$ORIGIN`;
- glibc core libraries from `$PREFIX/glibc/lib`;
- Android-sensitive X11/xcb libraries from the glibc core;
- general GTK, NSS, GIO, font, and desktop libraries from `~/gl/lib`.

Examples observed:

```text
libffmpeg.so  -> ~/gl/apps/obsidian/libffmpeg.so
libX11.so.6   -> $PREFIX/glibc/lib/libX11.so.6
libxcb.so.1   -> $PREFIX/glibc/lib/libxcb.so.1
libgtk-3.so.0 -> ~/gl/lib/libgtk-3.so.0
libnss3.so    -> ~/gl/lib/libnss3.so
```

This was an important confirmation that the existing core/farm boundary rules worked for the AppImage payload without modification.

---

## 10. Why the Upstream AppRun Was Not Used

The extracted `AppRun` script configured the AppDir environment and eventually executed:

```text
$APPDIR/obsidian
```

However, it also exported:

```bash
export LD_LIBRARY_PATH="${APPDIR}/usr/lib:${LD_LIBRARY_PATH}"
```

This violates a central project rule.

For this environment, `LD_LIBRARY_PATH` is not used because it can cross-contaminate the bionic shell and glibc execution worlds and can break the intended core-before-farm library ordering.

Therefore the upstream `AppRun` was bypassed.

Only the useful environment semantics were reproduced in the project launcher:

- `APPDIR`;
- application PATH additions;
- AppDir XDG data directory;
- GSettings schema directory when present.

The `LD_LIBRARY_PATH` behavior was intentionally omitted.

---

## 11. First Launch Failure: `/dev/shm`

The first execution test used:

```bash
$APPDIR/obsidian --version
```

The important discovery was that `--version` did not behave like a trivial non-GUI version probe. The Electron application initialized far enough to load the main package and then failed in Chromium shared-memory setup.

Observed failure:

```text
FATAL: base/memory/platform_shared_memory_region_posix.cc:219
This is frequently caused by incorrect permissions on /dev/shm.
```

This confirmed that the application must follow the existing Electron launch contract:

```text
--disable-dev-shm-usage
```

After adding that flag, the application launched successfully.

Other messages observed at startup were known or non-blocking:

```text
Failed to read /proc/sys/fs/inotify/max_user_watches
Failed to connect to /run/dbus/system_bus_socket
LaunchProcess: failed to execvp: xdg-settings
```

The application continued past them, loaded `resources/obsidian.asar`, checked GitHub for updates, and reported success.

Observed successful application log sequence:

```text
Loaded main app package .../resources/obsidian.asar
Checking for update using Github
Success.
Latest version is 1.12.7
App is up to date.
```

This verified:

- glibc execution;
- X11 window creation;
- Electron initialization;
- TLS certificate environment;
- outbound network access.

---

## 12. CPU-Mode Validation

The first graphical validation deliberately disabled GPU acceleration to separate basic application startup from the Vulkan stack.

The CPU-path launch shape was:

```bash
source "$HOME/gl/env"

exec env LD_PRELOAD= \
  "$APPDIR/obsidian" \
  --disable-dev-shm-usage \
  --ozone-platform=x11 \
  --disable-gpu
```

The window opened successfully.

This isolated the basic onboarding path from GPU-specific failures.

---

## 13. GPU Enablement and Verification

The final GPU launch reused the same Chromium/Electron flags that had already been proven in the project GPU work:

```text
--disable-gpu-sandbox
--ignore-gpu-blocklist
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
--disable-gpu-vsync
```

The application launched successfully with no GPU-process crash loop and no SIGBUS/present failure signature.

The renderer was then queried from the running Obsidian process using the Obsidian CLI `eval` command.

The WebGL2 query returned:

```json
{
  "webgl2": true,
  "vendor": "Google Inc. (Qualcomm)",
  "renderer": "ANGLE (Qualcomm, Vulkan 1.4.354 (Turnip Adreno (TM) 730 (0x07030001)), turnip Mesa driver)",
  "version": "WebGL 2.0 (OpenGL ES 3.0 Chromium)"
}
```

This is direct evidence for the final rendering path:

```text
Obsidian / Chromium
  -> WebGL2
  -> ANGLE
  -> Vulkan 1.4.354
  -> Turnip
  -> Adreno 730
  -> KGSL
```

The result rules out:

- SwiftShader;
- llvmpipe;
- CPU WebGL fallback;
- OpenGL fallback;
- a crashing Electron GPU process.

---

## 14. Obsidian CLI Discovery

The AppImage contained a separate ELF:

```text
obsidian-cli
```

Initial testing showed:

```text
The CLI is unable to find Obsidian. Please make sure Obsidian is running and try again.
```

This established that the CLI is a client that connects to a running Obsidian process rather than the GUI entry point.

The application settings contained an option to enable the CLI and register it on PATH. Enabling it created:

```text
~/.local/bin/obsidian
```

A byte-for-byte comparison showed:

```text
~/.local/bin/obsidian
==
~/gl/apps/obsidian/obsidian-cli
```

The registered copy preserved the already patched ELF state because Obsidian copied the patched bundled CLI binary:

```text
interpreter:
$PREFIX/glibc/lib/ld-linux-aarch64.so.1

rpath:
$ORIGIN:$PREFIX/glibc/lib:$HOME/gl/lib

missing dependencies:
none
```

This means the CLI registration mechanism itself is compatible with the project.

---

## 15. CLI Failure Caused by Termux LD_PRELOAD

Running the registered CLI directly from the normal Termux shell failed:

```bash
~/.local/bin/obsidian version
```

Observed error:

```text
error while loading shared libraries:
/data/data/com.termux/files/usr/glibc/lib/libc.so: invalid ELF header
```

The shell environment contained:

```text
LD_PRELOAD=/data/data/com.termux/files/usr/lib/libtermux-exec-ld-preload.so
```

The same CLI worked immediately when launched under the project environment contract:

```bash
(
  source "$HOME/gl/env"
  env LD_PRELOAD= \
    "$HOME/.local/bin/obsidian" version
)
```

Observed result:

```text
1.12.7 (installer 1.12.7)
```

This proved that the CLI binary was valid and that the failure was solely caused by inherited Termux preload state.

The practical rule is therefore:

```text
Every glibc ELF entry point, including helper CLIs,
must be launched through the gl environment and with LD_PRELOAD cleared.
```

---

## 16. Final GUI and CLI Command Separation

A naming conflict exists if both the project GUI launcher and the upstream CLI registration use the command name `obsidian`.

The final command model separates them:

```text
obsidian-app
  -> project GUI launcher
  -> ~/gl/apps/obsidian/obsidian

obsidian
  -> project CLI wrapper
  -> ~/.local/bin/obsidian
  -> registered upstream CLI copy
```

### 16.1 GUI launcher

The GUI launcher is:

```text
~/gl/bin/obsidian-app
```

Representative implementation:

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -u -o pipefail

source "$HOME/gl/env"

APP="$HOME/gl/apps/obsidian"

export APPDIR="$APP"
export PATH="$HOME/gl/shims:$APP:$APP/usr/sbin:$PATH"
export XDG_DATA_DIRS="$APP/usr/share:${XDG_DATA_DIRS:-}"

if [ -d "$APP/usr/share/glib-2.0/schemas" ]; then
    export GSETTINGS_SCHEMA_DIR="$APP/usr/share/glib-2.0/schemas"
fi

GPU_FLAGS=(--disable-gpu)

if [ "${GL_GPU:-1}" = "1" ] && [ -n "${VK_DRIVER_FILES:-}" ]; then
    GPU_FLAGS=(
        --disable-gpu-sandbox
        --ignore-gpu-blocklist
        --enable-features=Vulkan
        --use-gl=angle
        --use-angle=vulkan
        --disable-gpu-vsync
    )
fi

exec env LD_PRELOAD= \
    "$APP/obsidian" \
    --disable-dev-shm-usage \
    --ozone-platform=x11 \
    "${GPU_FLAGS[@]}" \
    "$@"
```

### 16.2 CLI wrapper

The CLI wrapper is:

```text
~/gl/bin/obsidian
```

Representative implementation:

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -u -o pipefail

source "$HOME/gl/env"

CLI="$HOME/.local/bin/obsidian"

if [ ! -x "$CLI" ]; then
    echo "Obsidian CLI is not registered: $CLI" >&2
    echo "Enable Command line interface in Obsidian Settings > General." >&2
    exit 127
fi

exec env LD_PRELOAD= \
    "$CLI" \
    "$@"
```

This preserves upstream ownership of the registered CLI binary while keeping the project environment adaptation in a separate wrapper.

---

## 17. PATH Integration

The final intended command-resolution order is:

```text
~/gl/bin
  -> ~/.local/bin
  -> Termux system PATH
```

This ensures:

```text
obsidian
  -> ~/gl/bin/obsidian
  -> safe glibc CLI wrapper
  -> ~/.local/bin/obsidian

obsidian-app
  -> ~/gl/bin/obsidian-app
```

The XFCE session script was also adjusted so graphical terminals inherit the same precedence order.

This prevents the raw glibc CLI from being selected ahead of the environment wrapper.

---

## 18. Clean Rebuild Reproducibility Test

After the first success, the entire Obsidian-specific installation state was deleted and the experiment was repeated from the original AppImage.

Removed state included:

```text
~/gl/apps/obsidian
~/.config/obsidian
~/.cache/obsidian
~/.local/share/obsidian
~/.local/bin/obsidian
~/gl/bin/obsidian
~/gl/bin/obsidian-app
Obsidian-specific temporary logs and SquashFS files
```

The original AppImage was retained.

The automated rebuild repeated:

1. process cleanup;
2. application-state removal;
3. ELF offset calculation;
4. `hsqs` cross-check;
5. SquashFS split;
6. AppDir extraction;
7. ELF inventory;
8. interpreter and RPATH patching;
9. full ELF dependency scan.

The second run produced the same key results:

```text
ELF offset   = 197808
hsqs offset  = 197808
SquashFS magic: hsqs
ELF count: 11
ALL ELF DEPENDENCIES RESOLVED
```

The rebuilt application again:

- opened a normal window;
- loaded `resources/obsidian.asar`;
- completed GitHub update checks;
- re-registered the CLI;
- returned the same hardware renderer path through ANGLE/Vulkan/Turnip.

This clean rerun established that the onboarding result is reproducible and not dependent on hidden state from the first experiment.

---

## 19. Final Verified Results

The following were verified successfully:

```text
AppImage parsing                    PASS
ELF/SquashFS offset agreement       PASS
SquashFS extraction                 PASS
Electron AppDir structure           PASS
ELF inventory                       PASS (11 files)
Interpreter patching                PASS
RPATH ordering                      PASS
Full ELF dependency scan            PASS
CPU/X11 GUI launch                  PASS
/dev/shm workaround                 PASS
TLS/network update check            PASS
GPU process stability               PASS
WebGL2                              PASS
ANGLE                               PASS
Vulkan                              PASS
Turnip                              PASS
Adreno 730 hardware renderer        PASS
Obsidian CLI registration           PASS
CLI binary identity check           PASS
CLI wrapper with LD_PRELOAD clear   PASS
Clean rebuild reproducibility       PASS
```

---

## 20. Failure Signatures and Their Meaning

### `unsquashfs: command not found`

Cause:

```text
Termux package is squashfs-tools-ng, not classic squashfs-tools.
```

Resolution:

```text
split SquashFS payload first, then use sqfs2tar | tar -x
```

### ELF offset reported as zero

Cause:

```text
incorrect readelf parsing using the final whitespace token
```

Resolution:

```text
parse the colon-delimited numeric field and strip digits explicitly
```

### `/dev/shm` fatal during Electron startup

Cause:

```text
Chromium shared-memory initialization on the Android target environment
```

Resolution:

```text
--disable-dev-shm-usage
```

### `libc.so: invalid ELF header` from registered CLI

Cause:

```text
raw glibc CLI inherited Termux's bionic libtermux-exec LD_PRELOAD
```

Resolution:

```text
source ~/gl/env
exec env LD_PRELOAD= ...
```

### AppRun incompatible with project runtime contract

Cause:

```text
AppRun exports LD_LIBRARY_PATH
```

Resolution:

```text
bypass AppRun and launch the patched Electron ELF through a project launcher
```

---

## 21. Lessons for a Future gl-adopt AppImage Adapter

The experiment suggests a clean adapter boundary.

A future AppImage path can be modeled as:

```text
gl-adopt --appimage FILE
  |
  +-- validate architecture
  +-- calculate ELF boundary
  +-- find hsqs magic
  +-- require offset agreement
  +-- split SquashFS
  +-- extract AppDir
  +-- remove temporary image
  +-- pass resulting tree to common onboarding code
        |
        +-- ELF inventory
        +-- patchelf
        +-- dependency verification
        +-- launcher generation
```

Recommended adapter checks:

1. confirm arm64/aarch64 ELF runtime;
2. calculate `e_shoff + e_shentsize * e_shnum`;
3. search for SquashFS magic;
4. require the expected magic at the calculated offset or fail explicitly;
5. verify extracted tree contains a plausible application entry point;
6. inventory all ELF files, including `.node` native modules;
7. preserve `$ORIGIN` in every rewritten RPATH;
8. never run extracted AppRun blindly;
9. inspect AppRun for environment assumptions, especially `LD_LIBRARY_PATH`;
10. treat helper CLIs as separate glibc entry points that also need the runtime wrapper contract.

The key architectural conclusion is:

```text
AppImage is not a separate runtime problem after extraction.
It is an input-format problem.
```

For this project, AppImage successfully joins `tar.gz` and `.deb` as another front-end adapter feeding the same native glibc application pipeline.

---

## 22. Conclusion

The Obsidian arm64 AppImage was successfully onboarded into the native Termux glibc layer without proot at runtime and without using the AppImage runtime.

The AppImage-specific complexity was limited to locating and extracting the embedded SquashFS filesystem. Once converted into an ordinary application tree, the existing project rules were sufficient:

```text
$ORIGIN first
Android-adapted glibc core second
Debian library farm third
no LD_LIBRARY_PATH
clear inherited LD_PRELOAD
launch Electron with the established X11 and Vulkan flags
```

The final application ran with:

```text
Electron/Chromium
  -> ANGLE
  -> Vulkan
  -> Turnip
  -> Adreno 730
```

The official Obsidian CLI registration also worked once wrapped with the same glibc environment boundary.

The clean rebuild reproduced the result, making this a successful proof that AppImage can be promoted to a first-class input adapter for the project.
