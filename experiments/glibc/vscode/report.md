# Native Microsoft Visual Studio Code on Termux Without PRoot or Chroot
## Detailed Experimental Report: Building a glibc Compatibility Layer, Resolving Runtime Dependencies, Integrating Termux:X11, and Reaching a Working VS Code Desktop Session

---

## Abstract

This report documents the successful execution of the official Microsoft Visual Studio Code ARM64 Linux distribution directly on a native Termux environment, without PRoot, chroot, a Linux distribution container, or a conventional FHS root filesystem.

The experiment was performed on an Android ARM64 device running Termux and Termux:X11. The host user space remained the ordinary Termux environment based on Android Bionic libc. Microsoft VS Code, however, is distributed as a conventional GNU/Linux ARM64 application and expects glibc, standard Linux filesystem conventions, and a large set of GNU/Linux shared libraries.

The final working architecture was deliberately hybrid:

```text
Android
└── Termux native user space
    ├── Bionic libc
    ├── Termux:X11
    ├── XFCE
    ├── PulseAudio
    ├── Mesa / Turnip Vulkan
    └── glibc compatibility layer
        ├── glibc-runner
        ├── official Microsoft VS Code ARM64 tarball
        └── selectively extracted Debian ARM64 glibc libraries
```

The principal result is:

> The official Microsoft Visual Studio Code ARM64 Linux build was successfully executed on native Termux without PRoot or chroot.

The final session successfully reached the VS Code workbench, created application storage, started a local extension host, initialized default profile extensions, and reported a render-performance baseline.

Representative success output:

```text
[main 2026-07-02T00:21:10.398Z] [shared storage] Creating shared storage database at '/data/data/com.termux/files/home/.vscode-shared/sharedStorage/state.vscdb' (wasCreated: true)

[main 2026-07-02T00:21:10.400Z] [shared storage] Initializing fallback application storage (path: /data/data/com.termux/files/home/.vscode-ms-data/User/globalStorage/state.vscdb)

[main 2026-07-02T00:21:10.442Z] [shared storage] Fallback application storage initialized with 3 items

[9989:0702/002113.208990:INFO:CONSOLE:442] "%c INFO color: #33f Started local extension host with pid 10211."

[9989:0702/002114.439194:INFO:CONSOLE:442] "%c INFO color: #33f Completed initializing default profile extensions in extensions installation folder."

[9989:0702/002117.663253:INFO:CONSOLE:442] "%c INFO color: #33f [perf] Render performance baseline is 54ms"
```

The experiment also revealed several important architectural boundaries:

- a glibc application's library environment must be strictly isolated from native Termux/Bionic commands;
- Electron child-process behavior differs when invoked through an explicit dynamic linker;
- Termux:X11's native Unix socket path does not match the pathname expected by conventional glibc X11 clients;
- runtime `dlopen()` dependencies are not necessarily detected by static library-resolution tools;
- successful GUI startup does not imply working GPU acceleration;
- Android restrictions on Netlink, `/proc/sys`, udev, system D-Bus, and related Linux desktop facilities remain visible but are not necessarily fatal.

---

# 1. Objective

The experiment had the following requirements.

1. Use a clean native Termux installation.
2. Do not use `proot-distro`.
3. Do not use PRoot manually.
4. Do not use chroot.
5. Use Termux:X11 and XFCE for the graphical environment.
6. Preserve the normal Termux/Bionic environment.
7. Run the official Microsoft VS Code build rather than Code-OSS.
8. Avoid black-box installation scripts.
9. Keep all externally supplied GNU/Linux libraries isolated and inspectable.
10. Obtain a repeatable launch procedure.

The intended end state was:

```text
Termux native
+
Termux:X11
+
XFCE
+
glibc-runner
+
official VS Code ARM64 Linux tarball
+
minimal external glibc dependency bundle
```

---

# 2. Relevant Host Environment

The experiment was performed on ARM64.

The native graphics stack had already been validated separately.

Observed Vulkan configuration:

```text
Vulkan Instance Version: 1.4.355
```

The physical GPU was successfully enumerated as:

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
        driverInfo         = Mesa 26.0.6
        conformanceVersion = 1.4.0.0
```

The native Vulkan device was therefore:

```text
GPU: Qualcomm Adreno 730
Driver: Mesa Turnip
Mesa version: 26.0.6
```

The KGSL device was directly accessible:

```console
$ ls -al /dev/kgsl-3d0

crw-rw-rw-. 1 system system 506, 0 Sep 30  1973 /dev/kgsl-3d0
```

This graphics setup was independent of the subsequent glibc VS Code experiment, but became relevant during later GPU acceleration testing.

---

# 3. Native Termux Desktop Foundation

The desktop architecture was:

```text
Termux
└── termux-x11 :1
    └── XFCE
        ├── xfsettingsd
        ├── xfwm4
        ├── xfdesktop
        └── xfce4-panel
```

The eventual session launcher used explicit component startup instead of relying exclusively on a monolithic XFCE session launcher.

A representative version of the session script was:

```bash
#!/data/data/com.termux/files/usr/bin/bash

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
HOME="${HOME:-/data/data/com.termux/files/home}"
LOGDIR="$HOME/.cache/termux-x11-session"

mkdir -p "$LOGDIR"

pkill -f 'chromium|chrome' 2>/dev/null
pkill -f 'xfce4-session|xfwm4|xfdesktop|xfce4-panel|xfsettingsd|xfce4-power-manager|picom|compton' 2>/dev/null
pkill -f 'termux-x11' 2>/dev/null

sleep 1

# Essential isolation:
# never allow a glibc LD_LIBRARY_PATH to leak into native Termux processes.
unset LD_LIBRARY_PATH

unset MESA_LOADER_DRIVER_OVERRIDE
unset GALLIUM_DRIVER
unset LIBGL_ALWAYS_SOFTWARE
unset PULSE_SERVER

export DISPLAY=:1
export XDG_RUNTIME_DIR="${TMPDIR}"
export XDG_CONFIG_DIRS="${PREFIX}/etc/xdg"
export PATH="$HOME/.local/bin:$PATH"

FREEDRENO_ICD="$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json"

if [ -r "$FREEDRENO_ICD" ]; then
    export VK_ICD_FILENAMES="$FREEDRENO_ICD"
else
    unset VK_ICD_FILENAMES
fi

export CHROMIUM_FLAGS="--ignore-gpu-blocklist --enable-gpu-rasterization --enable-zero-copy --enable-accelerated-video-decode --enable-features=Vulkan --use-gl=angle --use-angle=vulkan"

pulseaudio --start --exit-idle-time=-1 >/dev/null 2>&1

env \
    -u LD_LIBRARY_PATH \
    -u VK_ICD_FILENAMES \
    -u MESA_LOADER_DRIVER_OVERRIDE \
    -u GALLIUM_DRIVER \
    -u LIBGL_ALWAYS_SOFTWARE \
    termux-x11 :1 -listen tcp -ac \
    >"$LOGDIR/termux-x11.log" 2>&1 &

sleep 2

am start \
    --user 0 \
    -n com.termux.x11/com.termux.x11.MainActivity \
    >/dev/null 2>&1

sleep 2

eval "$(dbus-launch --sh-syntax)"

xfsettingsd \
    >"$LOGDIR/xfsettingsd.log" 2>&1 &

sleep 1

xfwm4 \
    --replace \
    --compositor=off \
    >"$LOGDIR/xfwm4.log" 2>&1 &

sleep 1

xfdesktop \
    >"$LOGDIR/xfdesktop.log" 2>&1 &

sleep 1

xfce4-panel \
    >"$LOGDIR/xfce4-panel.log" 2>&1 &

echo "Manual XFCE session started"
echo "DISPLAY=$DISPLAY"
echo "VK_ICD_FILENAMES=${VK_ICD_FILENAMES:-<unset>}"
echo "MESA_LOADER_DRIVER_OVERRIDE=${MESA_LOADER_DRIVER_OVERRIDE:-<unset>}"
echo "CHROMIUM_FLAGS=$CHROMIUM_FLAGS"
echo "Logs: $LOGDIR"

wait
```

A crucial later addition was:

```bash
unset LD_LIBRARY_PATH
```

Without this isolation, a glibc library directory exported globally could corrupt native Bionic Termux commands.

That failure mode was directly observed later in the experiment.

---

# 4. Official Microsoft VS Code Distribution

The official ARM64 VS Code tarball was unpacked under:

```text
~/opt/VSCode-linux-arm64
```

Directory contents:

```console
$ ls

LICENSES.chromium.html
bin
chrome-sandbox
chrome_100_percent.pak
chrome_200_percent.pak
chrome_crashpad_handler
code
icudtl.dat
libEGL.so
libGLESv2.so
libffmpeg.so
libvk_swiftshader.so
libvulkan.so.1
locales
resources
resources.pak
snapshot_blob.bin
v8_context_snapshot.bin
vk_swiftshader_icd.json
```

The important executable layout was:

```text
./code      actual ARM64 ELF Electron executable
./bin/code  shell-based VS Code CLI wrapper
```

Verification:

```console
$ file ./code ./Code ./bin/code 2>/dev/null
```

Output:

```text
./code:     ELF 64-bit LSB pie executable, ARM aarch64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-aarch64.so.1, for GNU/Linux 3.7.0, BuildID[sha1]=9ef9db488fc29b4450382b3623f5d3bccc4783ee, stripped

./Code:     cannot open `./Code' (No such file or directory)

./bin/code: a sh script, ASCII text executable
```

The requested ELF interpreter was confirmed:

```console
$ readelf -l ./code | grep 'Requesting program interpreter'
```

Output:

```text
[Requesting program interpreter: /lib/ld-linux-aarch64.so.1]
```

This established the core compatibility problem:

```text
official VS Code binary
    → GNU/Linux ELF
    → glibc dynamic loader
    → /lib/ld-linux-aarch64.so.1
```

whereas native Termux provides:

```text
Android
    → Bionic libc
    → Termux prefix
    → no conventional /lib/ld-linux-aarch64.so.1
```

---

# 5. glibc-runner Inspection

`glibc-runner` was already installed.

Location:

```console
$ command -v glibc-runner
```

Output:

```text
/data/data/com.termux/files/usr/bin/glibc-runner
```

File type:

```console
$ file "$(command -v glibc-runner)"
```

Output:

```text
/data/data/com.termux/files/usr/bin/glibc-runner: a /data/data/com.termux/files/usr/bin/bash script, ASCII text executable
```

Wrapper content:

```console
$ head -n 80 "$(command -v glibc-runner)"
```

Output:

```bash
#!/data/data/com.termux/files/usr/bin/bash

# version: 2.0

source /data/data/com.termux/files/usr/opt/glibc-runner/glibc-runner.sh $@
```

Help output:

```console
$ glibc-runner --help 2>&1 | head -80
```

Output:

```text
Help message from glibc-runner v2.0

glibc-runner - launcher for working with the glibc shell or with a glibc-based binary

Options:
 --help      -h  print help message
 --info      -i  print information about the running glibc-runner shell
 --shell     -s  run the glibc-runner shell or a command from that shell
 --teg       -t  enable the use of termux-exec-glibc in the glibc-runner shell
 --configure -c  configure the binary to run on the device
 --findlib   -f  find libraries for the binary
 --no-linker -n  don't use dynamic linker to launch binary
 --debug     -d  [1|2|3|4]  launch binary or shell under strace

Example: glibc-runner [-c|-f|-n] ./binary || grun [-s|-n|-t] [gcc -v]
```

The actual runner implementation was inspected for key operations:

```console
$ grep -nE 'LD_LIBRARY_PATH|ld-linux|patchelf|linker|findlib|configure|exec|mount|proot|chroot' \
  $PREFIX/opt/glibc-runner/glibc-runner.sh
```

Observed output included:

```text
15:     export PATH_LIBTERMUX_EXEC_GLIBC="${GLIBC_PREFIX}/lib/libtermux-exec.so"

50:     _glibc-runner_check_program "patchelf"

53:     if [ "$GLIBC_RUNNER_RUN_FINDLIB" = "true" ] && [ -n "$LD_LIBRARY_PATH" ]; then

54:             LD_RPATH="$LD_LIBRARY_PATH"

59:     patchelf --set-rpath $LD_RPATH \

64:_glibc-runner_findlib() {

68:     if [ -z "$LD_LIBRARY_PATH" ]; then

71:             result=(${LD_LIBRARY_PATH//:/ })

94:     export LD_LIBRARY_PATH=$(tr -s ' ' ':' <<< "${result[@]}")

113:            exec $(_glibc-runner_debug) ${SHELL:=$GLIBC_PREFIX/bin/bash}

115:            exec $(_glibc-runner_debug) ${SHELL:=$GLIBC_PREFIX/bin/bash} -c "$command"

136:    echo "LD_LIBRARY_PATH='${LD_LIBRARY_PATH}'"

157:    echo " --configure -c  configure the binary to run on the device"

158:    echo " --findlib   -f  find libraries for the binary"

159:    echo " --no-linker -n  don't use dynamic linker to launch binary"

258:            _glibc-runner_findlib "$1"

274:                    exec $(_glibc-runner_debug) $@

276:                    exec $(_glibc-runner_debug) ld.so $@
```

Important conclusion:

> `glibc-runner` was not used as a PRoot or chroot substitute. It was used as a controlled glibc execution layer and dynamic-linker wrapper.

---

# 6. Initial Dependency Resolution

The first attempt to identify dependencies was:

```console
$ glibc-runner --findlib ./code
```

Initial output:

```text
Message from glibc-runner: searching for libraries...
Error from glibc-runner: could not find 'libglib-2.0.so.0'
```

A direct launch produced the same root cause:

```console
$ DISPLAY=:1 \
  XDG_RUNTIME_DIR=$TMPDIR \
  glibc-runner ./code \
    --no-sandbox \
    --disable-gpu \
    --disable-dev-shm-usage \
    --password-store=basic
```

Output:

```text
./code: error while loading shared libraries: libglib-2.0.so.0: cannot open shared object file: No such file or directory
```

The glibc repository contained:

```console
$ pkg search glib | grep -Ei 'glib-glib'
```

Output:

```text
glib-glibc/glibc 2.82.2-2 aarch64
glib-glibc-static/glibc 2.82.2-2 aarch64
  Static libraries for glib-glibc
```

Installation:

```bash
pkg install glib-glibc
```

After that:

```console
$ glibc-runner --findlib ./code
```

Output:

```text
Message from glibc-runner: searching for libraries...
Error from glibc-runner: could not find 'libnspr4.so'
```

Search results showed only native Termux/Bionic packages:

```console
$ pkg search nspr
```

Output:

```text
libnspr/stable,now 4.39 aarch64 [installed,automatic]
  Netscape Portable Runtime (NSPR)

libnspr-static/stable 4.39 aarch64
  Static libraries for libnspr
```

There was no corresponding `libnspr-glibc` package.

Likewise:

```console
$ pkg search nss
```

showed:

```text
libnss/stable,now 3.125 aarch64 [installed,automatic]
  Network Security Services (NSS)
```

but no isolated glibc equivalent.

This led to the next architecture decision.

---

# 7. Creation of an Isolated Debian ARM64 glibc Library Root

Rather than mix Bionic Termux libraries into the glibc process, a separate library root was created:

```text
~/opt/debian-arm64-libs
```

Working directory:

```text
~/tmp/debpkgs
```

Initialization:

```bash
mkdir -p ~/opt/debian-arm64-libs
mkdir -p ~/tmp/debpkgs
```

The Debian ARM64 package index was downloaded:

```bash
cd ~/tmp/debpkgs

curl -L \
  https://deb.debian.org/debian/dists/trixie/main/binary-arm64/Packages.gz \
  -o Packages.gz
```

A package extraction helper was created.

Representative implementation:

```bash
#!/data/data/com.termux/files/usr/bin/bash

set -e

MIRROR="https://deb.debian.org/debian"
PKG="$1"

META="$HOME/tmp/debpkgs/Packages.gz"
OUT="$HOME/tmp/debpkgs"
ROOT="$HOME/opt/debian-arm64-libs"

if [ -z "$PKG" ]; then
    echo "usage: extract-deb-pkg <debian-package-name>" >&2
    exit 1
fi

FILE="$(
    zcat "$META" |
    awk -v pkg="$PKG" '
        BEGIN {
            RS=""
            FS="\n"
        }

        $0 ~ "(^|\n)Package: " pkg "(\n|$)" {
            for (i = 1; i <= NF; i++) {
                if ($i ~ /^Filename: /) {
                    sub(/^Filename: /, "", $i)
                    print $i
                    exit
                }
            }
        }
    '
)"

if [ -z "$FILE" ]; then
    echo "package not found in metadata: $PKG" >&2
    exit 1
fi

DEB="$OUT/${PKG}.deb"

echo "Package: $PKG"
echo "File: $FILE"

env -u LD_LIBRARY_PATH \
    curl -L "$MIRROR/$FILE" -o "$DEB"

echo "Extracting to $ROOT"

env -u LD_LIBRARY_PATH \
    dpkg-deb -x "$DEB" "$ROOT"
```

This script performed:

```text
Debian Packages.gz
        │
        ▼
resolve package filename
        │
        ▼
download .deb
        │
        ▼
dpkg-deb -x
        │
        ▼
~/opt/debian-arm64-libs
```

It did not install packages into Termux.

---

# 8. Debian Contents Index and Library-to-Package Mapping

A Debian `Contents-arm64.gz` index was used to map filenames such as:

```text
libatk-1.0.so.0
```

to packages.

The initial incorrect URL downloaded only a 300-byte file and returned no result.

Correct download:

```bash
curl -fL \
  https://deb.debian.org/debian/dists/trixie/main/Contents-arm64.gz \
  -o Contents-arm64.gz
```

Search:

```console
$ zgrep -m 10 'libatk-1.0.so.0' Contents-arm64.gz
```

Output:

```text
usr/lib/aarch64-linux-gnu/libatk-1.0.so.0               libs/libatk1.0-0t64
usr/lib/aarch64-linux-gnu/libatk-1.0.so.0.25611.1       libs/libatk1.0-0t64
```

Therefore:

```bash
~/tmp/debpkgs/extract-deb-pkg libatk1.0-0t64
```

---

# 9. Automated Dependency Resolution

Manual resolution quickly became impractical, so an automated resolver was created.

Its intended loop was:

```text
glibc-runner --findlib
        │
        ▼
parse missing libXXX.so
        │
        ▼
Contents-arm64.gz
        │
        ▼
resolve Debian package
        │
        ▼
Packages.gz
        │
        ▼
resolve .deb path
        │
        ▼
download and extract
        │
        └─────────────── repeat
```

Representative resolver:

```bash
#!/data/data/com.termux/files/usr/bin/bash

set -u

SUITE="${SUITE:-trixie}"
MIRROR="${MIRROR:-https://deb.debian.org/debian}"

WORK="$HOME/tmp/debpkgs"
ROOT="$HOME/opt/debian-arm64-libs"
VSCODE_DIR="$HOME/opt/VSCode-linux-arm64"
BIN="$VSCODE_DIR/code"

PACKAGES="$WORK/Packages.gz"
CONTENTS="$WORK/Contents-arm64.gz"
LOG="$WORK/resolve-vscode-glibc-deps.log"

mkdir -p "$WORK" "$ROOT"

log() {
    printf '%s\n' "$*" | tee -a "$LOG"
}

find_pkg_for_lib() {
    local lib="$1"

    zgrep -m 20 "/$lib" "$CONTENTS" 2>/dev/null |
        awk '{print $NF}' |
        tr ',' '\n' |
        sed 's|.*/||' |
        sort -u |
        head -1
}

find_deb_file_for_pkg() {
    local pkg="$1"

    zcat "$PACKAGES" |
    awk -v pkg="$pkg" '
        BEGIN {
            RS=""
            FS="\n"
        }

        $0 ~ "(^|\n)Package: " pkg "(\n|$)" {
            for (i = 1; i <= NF; i++) {
                if ($i ~ /^Filename: /) {
                    sub(/^Filename: /, "", $i)
                    print $i
                    exit
                }
            }
        }
    '
}

extract_missing_lib() {
    sed -n \
        -e "s/.*could not find '\([^']*\)'.*/\1/p" \
        -e "s/.*error while loading shared libraries: \([^: ]*\):.*/\1/p" |
        head -1
}
```

The second error pattern was added later because the first implementation recognized only:

```text
could not find 'libXXX.so'
```

but not:

```text
error while loading shared libraries: libXXX.so: cannot open shared object file
```

A real failure exposed this bug.

Observed output:

```text
Extracting package: libatspi2.0-0t64

===== pass 2 =====

Message from glibc-runner: searching for libraries...
Message from glibc-runner: searching libraries was successful

/data/data/com.termux/files/home/opt/VSCode-linux-arm64/code:
error while loading shared libraries: libsystemd.so.0:
cannot open shared object file: No such file or directory

No missing library reported by glibc-runner --findlib.
Dependency resolution loop finished.
```

The parser was then expanded to handle both formats.

Eventually, the resolver reached:

```text
===== pass 30 =====

Message from glibc-runner: searching for libraries...
Message from glibc-runner: searching libraries was successful

[0701/234414.096865:ERROR:base/i18n/icu_util.cc:232]
Invalid file descriptor to ICU data received.

No missing library reported by glibc-runner --findlib.
Dependency resolution loop finished.
```

This was a major transition point:

> All statically visible shared library dependencies had been resolved sufficiently for Electron to begin startup.

The remaining problem was no longer a simple missing library.

---

# 10. ICU File Descriptor Failure

Initial execution after dependency resolution produced:

```text
[ERROR:base/i18n/icu_util.cc:232]
Invalid file descriptor to ICU data received.
```

The important observation was that this happened when `glibc-runner` invoked the executable through its dynamic-linker mode.

Inspection of the runner showed:

```text
exec ... ld.so $@
```

as one execution path.

Electron and Chromium re-exec child processes and pass file descriptors internally. The working hypothesis was that explicit dynamic-linker invocation interfered with this process model.

The next experiment used:

```bash
glibc-runner --no-linker
```

---

# 11. `--no-linker` and the Bundled Library Path

First `--no-linker` attempt:

```console
$ DISPLAY=:1 \
  XDG_RUNTIME_DIR=$TMPDIR \
  LD_LIBRARY_PATH="$DEB_LIBS" \
  glibc-runner --no-linker ./code \
    --no-sandbox \
    --disable-gpu \
    --disable-dev-shm-usage \
    --password-store=basic
```

Output:

```text
./code: error while loading shared libraries:
libffmpeg.so: cannot open shared object file:
No such file or directory
```

However, `libffmpeg.so` was already present in the VS Code directory:

```text
~/opt/VSCode-linux-arm64/libffmpeg.so
```

The issue was therefore not absence, but search path composition.

The corrected runtime path became:

```bash
VSCODE_DIR="$HOME/opt/VSCode-linux-arm64"

DEB_LIBS="$HOME/opt/debian-arm64-libs/usr/lib/aarch64-linux-gnu"

MSCODE_LD="$VSCODE_DIR:$DEB_LIBS"
```

This was an important rule:

```text
LD_LIBRARY_PATH =
    VS Code bundled libraries
    +
    isolated Debian ARM64 libraries
```

not merely:

```text
Debian libraries
```

---

# 12. The Critical LD_LIBRARY_PATH Isolation Failure

At one point, the glibc library path was exported globally.

This caused a native Termux command to fail:

```text
CANNOT LINK EXECUTABLE "dpkg-deb":
library "libc.so.6" not found:
needed by
/data/data/com.termux/files/home/opt/debian-arm64-libs/usr/lib/aarch64-linux-gnu/libbz2.so.1.0.4
in namespace (default)
```

Cause:

```text
dpkg-deb
    = native Termux/Bionic executable

global LD_LIBRARY_PATH
    = Debian glibc library directory

native Bionic loader
    → finds Debian libbz2 first
    → Debian libbz2 requires libc.so.6
    → Bionic process cannot satisfy glibc ABI
```

Recovery:

```bash
unset LD_LIBRARY_PATH
unset DEB_LIBS
hash -r
```

The extraction scripts were made safer:

```bash
env -u LD_LIBRARY_PATH curl ...
```

and:

```bash
env -u LD_LIBRARY_PATH dpkg-deb -x ...
```

This became one of the most important conclusions of the experiment:

> Never globally export the glibc application library path in a native Termux shell.

The safe pattern is:

```bash
env LD_LIBRARY_PATH="$MSCODE_LD" \
    glibc-runner ...
```

The unsafe pattern is:

```bash
export LD_LIBRARY_PATH="$MSCODE_LD"
```

in a shell that also executes Termux/Bionic tools.

---

# 13. Termux:X11 Socket Path Incompatibility

Native Termux X11 worked:

```console
$ echo "DISPLAY=$DISPLAY"
DISPLAY=:1

$ echo "TMPDIR=$TMPDIR"
TMPDIR=/data/data/com.termux/files/usr/tmp
```

The X11 socket existed here:

```console
$ ls -al "$TMPDIR/.X11-unix"
```

Output:

```text
total 7
drwxrwxrwt.  2 u0_a534 u0_a534 3452 Jul  1 23:30 .
drwx------. 24 u0_a534 u0_a534 3452 Jul  2 08:51 ..
srwxrwxrwx.  1 u0_a534 u0_a534    0 Jul  1 23:30 X1
```

There was no conventional socket here:

```text
/tmp/.X11-unix/X1
```

Native verification:

```console
$ DISPLAY=:1 xdpyinfo >/dev/null && echo "native X11 OK"
```

Output:

```text
native X11 OK
```

But the glibc Electron application reported:

```text
Missing X server or $DISPLAY
```

even when:

```text
DISPLAY=:1
```

was provided.

This showed that the conventional glibc X11 stack was looking for the FHS-style Unix socket path rather than the Termux-specific socket location.

The workaround was to run Termux:X11 with TCP listening:

```bash
termux-x11 :1 -listen tcp -ac
```

and run the glibc client with:

```bash
DISPLAY=127.0.0.1:1
```

This eliminated the:

```text
Missing X server or $DISPLAY
```

failure.

This architecture was retained in the final desktop script.

---

# 14. Fontconfig Failure

Once X11 worked, the next blocker was:

```text
Fontconfig error:
Cannot load default config file: File not found
```

The native Termux font configuration existed:

```console
$ ls -al $PREFIX/etc/fonts/fonts.conf
```

Output:

```text
-rw-------. 1 u0_a534 u0_a534 2746 Jun  2 22:29
/data/data/com.termux/files/usr/etc/fonts/fonts.conf
```

The initial environment used:

```bash
export FONTCONFIG_PATH="$PREFIX/etc/fonts"
export FONTCONFIG_FILE="$PREFIX/etc/fonts/fonts.conf"
```

This moved startup further, but generated many compatibility warnings because the glibc-side Fontconfig libraries parsed Termux-specific Fontconfig configuration files.

Representative warnings:

```text
Fontconfig warning:
"/data/data/com.termux/files/usr/etc/fonts/conf.d/48-guessfamily.conf",
line 19: invalid attribute 'xsi:nil'

Fontconfig warning:
invalid constant used : monospace

Fontconfig warning:
invalid constant used : sans-serif

Fontconfig warning:
invalid constant used : emoji
```

A minimal VS Code-specific Fontconfig configuration was therefore created.

Example:

```bash
mkdir -p ~/.config/mscode-fontconfig
mkdir -p ~/.cache/mscode-fontconfig
```

Configuration:

```xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">

<fontconfig>

  <dir>/system/fonts</dir>
  <dir>/product/fonts</dir>
  <dir>/system_ext/fonts</dir>

  <dir>/data/data/com.termux/files/usr/share/fonts</dir>
  <dir>/data/data/com.termux/files/home/.local/share/fonts</dir>

  <cachedir>/data/data/com.termux/files/home/.cache/mscode-fontconfig</cachedir>

  <alias>
    <family>sans-serif</family>
    <prefer>
      <family>Roboto</family>
      <family>Noto Sans</family>
    </prefer>
  </alias>

  <alias>
    <family>monospace</family>
    <prefer>
      <family>Roboto Mono</family>
      <family>Noto Sans Mono</family>
      <family>Droid Sans Mono</family>
    </prefer>
  </alias>

</fontconfig>
```

Runtime variables:

```bash
FONTCONFIG_PATH="$HOME/.config/mscode-fontconfig"
FONTCONFIG_FILE="$HOME/.config/mscode-fontconfig/fonts.conf"
```

---

# 15. VS Code CLI Validation

The official `bin/code` wrapper was inspected.

Relevant ending:

```bash
ELECTRON="$VSCODE_PATH/code"
CLI="$VSCODE_PATH/resources/app/out/cli.js"

ELECTRON_RUN_AS_NODE=1 "$ELECTRON" "$CLI" "$@"
```

This demonstrated that the CLI uses Electron as a Node runtime.

A direct CLI test was performed:

```bash
env ELECTRON_RUN_AS_NODE=1 \
LD_LIBRARY_PATH="$LD_LIBRARY_PATH" \
FONTCONFIG_PATH="$FONTCONFIG_PATH" \
FONTCONFIG_FILE="$FONTCONFIG_FILE" \
glibc-runner --no-linker "$VSCODE_DIR/code" \
  "$VSCODE_DIR/resources/app/out/cli.js" \
  --version
```

Output:

```text
1.127.0
4fe60c8b1cdac1c4c174f2fb180d0d758272d713
arm64
```

This proved that:

```text
glibc-runner           working
glibc dependency set   sufficient for CLI
official VS Code CLI   working
Electron Node mode     working
architecture           ARM64
VS Code version         1.127.0
```

---

# 16. Runtime dlopen Dependency: `libX11-xcb.so.1`

Static dependency resolution eventually succeeded, but GUI execution still terminated with SIGTRAP.

A `glibc-runner --debug` trace revealed:

```text
openat(
  AT_FDCWD,
  "/data/data/com.termux/files/home/opt/VSCode-linux-arm64/libX11-xcb.so.1",
  O_RDONLY|O_CLOEXEC
) = -1 ENOENT
```

Then:

```text
openat(
  AT_FDCWD,
  "/data/data/com.termux/files/home/opt/debian-arm64-libs/usr/lib/aarch64-linux-gnu/libX11-xcb.so.1",
  O_RDONLY|O_CLOEXEC
) = -1 ENOENT
```

Then:

```text
openat(
  AT_FDCWD,
  "/data/data/com.termux/files/usr/glibc/lib/libX11-xcb.so.1",
  O_RDONLY|O_CLOEXEC
) = -1 ENOENT
```

Finally:

```text
--- SIGTRAP {
    si_signo=SIGTRAP,
    si_code=TRAP_BRKPT,
    si_addr=0x57cb559bd8
} ---

+++ killed by SIGTRAP +++
```

This revealed a limitation of `--findlib`:

> Dependencies loaded dynamically with `dlopen()` may not appear as ELF `DT_NEEDED` entries and therefore may escape static dependency resolution.

The missing runtime library was supplied by the Debian package:

```text
libx11-xcb1
```

Extraction:

```bash
~/tmp/debpkgs/extract-deb-pkg libx11-xcb1
```

This moved the GUI startup significantly further.

---

# 17. Runtime Main-Process Errors

After additional runtime dependencies were resolved, VS Code reached its actual JavaScript main process.

Representative logs:

```text
[main 2026-07-02T00:15:00.879Z]
SystemError [ERR_SYSTEM_ERROR]:
A system error occurred:
uv_interface_addresses returned Unknown system error 13
```

Stack:

```text
at networkInterfaces (node:os:218:16)

at T0 (
  file:///data/data/com.termux/files/home/opt/VSCode-linux-arm64/resources/app/out/main.js:460:4292
)

at jM (
  file:///data/data/com.termux/files/home/opt/VSCode-linux-arm64/resources/app/out/main.js:460:4698
)
```

Error object:

```text
{
  code: 'ERR_SYSTEM_ERROR',
  info: {
    errno: 13,
    code: 'Unknown system error 13',
    message: 'Unknown system error 13',
    syscall: 'uv_interface_addresses'
  }
}
```

This correlated with Chromium's Netlink error:

```text
Could not bind NETLINK socket:
Permission denied (13)
```

The application nevertheless continued.

This became an important conclusion:

> `uv_interface_addresses` failure on Android was noisy but not fatal to VS Code startup in this configuration.

---

# 18. Native Keyboard Mapping Module Investigation

The VS Code main process also logged:

```text
Error:
Cannot find module './build/Debug/keymapping'

Require stack:
- .../resources/app/node_modules/native-keymap/index.js
```

Inspection showed:

```text
resources/app/node_modules/native-keymap/build/Release/keymapping.node
```

was in fact present.

The module loader logic was:

```javascript
function NativeBinding() {
  this._tried = false;
  this._keymapping = null;
}

NativeBinding.prototype._init = function() {
  if (this._tried) {
    return;
  }

  this._tried = true;

  try {
    this._keymapping = require('./build/Release/keymapping');
  } catch (err) {
    // fallback to the debug build
    this._keymapping = require('./build/Debug/keymapping');
  }
};
```

Therefore the message:

```text
Cannot find module './build/Debug/keymapping'
```

did not necessarily mean that the release module was absent.

Instead:

```text
Release keymapping.node exists
        │
        ▼
Release load fails
        │
        ▼
catch block runs
        │
        ▼
Debug module attempted
        │
        ▼
Debug module absent
        │
        ▼
MODULE_NOT_FOUND references Debug path
```

The original exception from loading the Release native module was masked by the fallback behavior.

Despite this error, the experiment later reached a working VS Code interface.

---

# 19. NSS and SQLite Runtime Dependency

Another fatal path was:

```text
[ERROR:crypto/nss_util.cc:256]
Error initializing NSS with a persistent database
(sql:/data/data/com.termux/files/home/.pki/nssdb):

libsqlite3.so.0:
cannot open shared object file:
No such file or directory
```

Then:

```text
[ERROR:crypto/nss_util.cc:144]
Error initializing NSS without a persistent database:
NSS error code: -5925
```

Finally:

```text
[FATAL:crypto/nss_util.cc:146]
nss_error=-5925, os_error=0
```

The required Debian library package was extracted:

```bash
~/tmp/debpkgs/extract-deb-pkg libsqlite3-0
```

After resolving this and related runtime requirements, the NSS fatal path disappeared sufficiently for the application to continue startup.

---

# 20. Final Successful GUI Launch Command

The successful runtime environment used a strictly local library scope.

Representative command:

```bash
DISPLAY=127.0.0.1:1 \
XDG_RUNTIME_DIR="$TMPDIR" \
LD_LIBRARY_PATH="$MSCODE_LD" \
FONTCONFIG_PATH="$HOME/.config/mscode-fontconfig" \
FONTCONFIG_FILE="$HOME/.config/mscode-fontconfig/fonts.conf" \
NO_AT_BRIDGE=1 \
GSETTINGS_BACKEND=memory \
glibc-runner --no-linker "$VSCODE_DIR/code" \
  --no-sandbox \
  --no-zygote \
  --disable-gpu \
  --disable-dev-shm-usage \
  --password-store=basic \
  --ozone-platform=x11 \
  --user-data-dir="$HOME/.vscode-ms-data" \
  --enable-logging=stderr
```

The important aspects were:

```text
DISPLAY=127.0.0.1:1
```

because the glibc X11 client used TCP instead of the Termux-specific Unix socket path.

```text
LD_LIBRARY_PATH="$VSCODE_DIR:$DEB_LIBS"
```

because both bundled Electron libraries and extracted Debian libraries were needed.

```text
glibc-runner --no-linker
```

because normal dynamic-linker wrapping had produced the ICU file descriptor failure.

```text
--no-sandbox
```

because the conventional SUID sandbox configuration is not available in ordinary unprivileged Termux.

```text
--disable-gpu
```

was used for the first successful, stable baseline.

---

# 21. Successful Runtime Output

The successful run still emitted several warnings:

```text
Failed to connect to socket /run/dbus/system_bus_socket
```

```text
Could not bind NETLINK socket:
Permission denied (13)
```

```text
Failed to read /proc/sys/fs/inotify/max_user_watches
```

```text
Failed to initialize a udev monitor
```

```text
uv_interface_addresses returned Unknown system error 13
```

But startup continued.

Key successful messages:

```text
[main 2026-07-02T00:21:10.398Z]
[shared storage]
Creating shared storage database at
'/data/data/com.termux/files/home/.vscode-shared/sharedStorage/state.vscdb'
(wasCreated: true)
```

Then:

```text
[main 2026-07-02T00:21:10.400Z]
[shared storage]
Initializing fallback application storage

(path:
/data/data/com.termux/files/home/.vscode-ms-data/User/globalStorage/state.vscdb)
```

Then:

```text
[main 2026-07-02T00:21:10.442Z]
[shared storage]
Fallback application storage initialized with 3 items
```

Extension host:

```text
INFO Started local extension host with pid 10211.
```

Extension initialization:

```text
INFO Completed initializing default profile extensions
in extensions installation folder.

file:///data/data/com.termux/files/home/.vscode/extensions
```

Workbench render performance:

```text
INFO [perf] Render performance baseline is 54ms
```

This confirmed successful full application startup.

---

# 22. Final `mscode` Wrapper Architecture

A key usability problem was that the long command worked while an early wrapper appeared to do nothing.

A more explicit diagnostic wrapper was introduced.

Representative successful structure:

```bash
#!/data/data/com.termux/files/usr/bin/bash

set -u

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
HOME="${HOME:-/data/data/com.termux/files/home}"
TMPDIR="${TMPDIR:-$PREFIX/tmp}"

# Critical:
# do not allow an inherited glibc path to affect Termux/Bionic tools.
unset LD_LIBRARY_PATH

unset DBUS_SESSION_BUS_ADDRESS
unset DBUS_SYSTEM_BUS_ADDRESS

VSCODE_DIR="$HOME/opt/VSCode-linux-arm64"

DEB_LIBS="$HOME/opt/debian-arm64-libs/usr/lib/aarch64-linux-gnu"

MSCODE_LD="$VSCODE_DIR:$DEB_LIBS"

LOGDIR="$HOME/.cache/mscode"
mkdir -p "$LOGDIR"

LOG="$LOGDIR/mscode-last.log"

export DISPLAY=127.0.0.1:1
export XDG_RUNTIME_DIR="$TMPDIR"

export FONTCONFIG_PATH="$HOME/.config/mscode-fontconfig"
export FONTCONFIG_FILE="$HOME/.config/mscode-fontconfig/fonts.conf"

export NO_AT_BRIDGE=1
export GSETTINGS_BACKEND=memory

if [ -r "$PREFIX/etc/tls/cert.pem" ]; then
    export SSL_CERT_FILE="$PREFIX/etc/tls/cert.pem"
    export NODE_EXTRA_CA_CERTS="$PREFIX/etc/tls/cert.pem"
fi

cd "$VSCODE_DIR" || {
    echo "VS Code directory not found: $VSCODE_DIR" | tee "$LOG"
    exit 1
}

echo "=== mscode launch $(date) ===" > "$LOG"
echo "DISPLAY=$DISPLAY" >> "$LOG"
echo "XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR" >> "$LOG"
echo "LD_LIBRARY_PATH=$MSCODE_LD" >> "$LOG"
echo "FONTCONFIG_FILE=$FONTCONFIG_FILE" >> "$LOG"
echo "ARGS=$*" >> "$LOG"
echo >> "$LOG"

env LD_LIBRARY_PATH="$MSCODE_LD" \
    glibc-runner --no-linker "$VSCODE_DIR/code" \
        --no-sandbox \
        --no-zygote \
        --disable-gpu \
        --disable-dev-shm-usage \
        --password-store=basic \
        --ozone-platform=x11 \
        --user-data-dir="$HOME/.vscode-ms-data" \
        --enable-logging=stderr \
        --new-window \
        "$@" \
        2>&1 | tee -a "$LOG"
```

Usage:

```bash
mscode
```

or:

```bash
mscode .
```

The user confirmed:

> “이제 성공했어.”  
> “Now it works.”

---

# 23. Post-Success Certificate and Extension Signature Issue

After successful GUI startup, extension installation exposed another FHS assumption.

The UI reported:

```text
Cannot install 'Remote - SSH: Editing Configuration Files'
extension because Visual Studio Code cannot verify the
extension signature

Signature verification failed with 'ENOENT' error.
```

The runtime had also logged:

```text
Cannot open directory /etc/ssl/certs
to load OpenSSL certificates.
```

A VS Code-specific certificate directory was proposed.

Termux CA bundle:

```text
$PREFIX/etc/tls/cert.pem
```

Environment variables:

```bash
export SSL_CERT_FILE="$PREFIX/etc/tls/cert.pem"
export SSL_CERT_DIR="$HOME/.config/mscode-certs"
export NODE_EXTRA_CA_CERTS="$PREFIX/etc/tls/cert.pem"
export GIT_SSL_CAINFO="$PREFIX/etc/tls/cert.pem"
export CURL_CA_BUNDLE="$PREFIX/etc/tls/cert.pem"
export REQUESTS_CA_BUNDLE="$PREFIX/etc/tls/cert.pem"
```

This issue occurred after core VS Code startup had already succeeded.

---

# 24. Post-Success Performance Tuning

Multiple runtime modes were tested:

```text
safe
zygote
gpu
gpu-vulkan
```

All were reported to start successfully at the UI level.

However, log inspection showed that successful UI launch did not imply successful hardware GPU acceleration.

GPU-mode log:

```text
ANGLE Display::initialize error 12289:
Could not dlopen libGL.so.1:
libGL.so.1: cannot open shared object file:
No such file or directory
```

Then:

```text
eglInitialize OpenGL failed
with error EGL_NOT_INITIALIZED
```

Then:

```text
Initialization of all (2) EGL display types failed.
```

Then:

```text
GLDisplayEGL::Initialize failed.
```

Finally:

```text
Exiting GPU process due to errors during initialization
```

Therefore:

> The GPU-enabled mode started the VS Code application, but the GPU process itself failed initialization and the application continued through fallback behavior.

The immediate missing glibc OpenGL dependency was:

```text
libGL.so.1
```

The proposed glibc-side graphics dependency packages included:

```text
libgl1
libglx0
libglvnd0
libegl1
libgles2
libglx-mesa0
libegl-mesa0
libgbm1
libdrm2
```

This GPU work was separate from the successful baseline.

---

# 25. Important Distinction: Native Turnip vs. glibc Electron Graphics

The native graphics stack had successfully exposed:

```text
Turnip Adreno (TM) 730
```

through the Termux/Bionic Mesa stack.

However, official Microsoft VS Code was running in:

```text
glibc Electron
+
Debian glibc libraries
```

Therefore the existence of native Termux Turnip Vulkan does not automatically mean that a glibc Electron GPU process can load and use the Bionic Mesa driver stack.

This creates an ABI boundary:

```text
Termux native Mesa / Turnip
    → Bionic ABI

MS VS Code Electron
    → glibc ABI
```

A clean solution for hardware-accelerated glibc Electron therefore requires either:

1. a glibc-compatible Mesa/Turnip stack,
2. a compatible ANGLE/Vulkan path,
3. or another bridge that does not mix Bionic and glibc libraries directly.

The successful baseline intentionally used:

```text
--disable-gpu
```

---

# 26. Warnings That Remained Non-Fatal

The final working application still produced Linux desktop assumptions that Android/Termux could not satisfy.

## System D-Bus

```text
Failed to connect to socket
/run/dbus/system_bus_socket:
No such file or directory
```

## Netlink

```text
Could not bind NETLINK socket:
Permission denied (13)
```

## Network interface enumeration

```text
uv_interface_addresses returned
Unknown system error 13
```

## inotify sysctl access

```text
Failed to read
/proc/sys/fs/inotify/max_user_watches
```

## udev

```text
Failed to initialize a udev monitor
```

## login1 / power management

```text
org.freedesktop.login1 not available
```

These warnings did not prevent successful workbench startup.

---

# 27. Final Filesystem Layout

The experiment ultimately used approximately this layout:

```text
$HOME/
├── .local/
│   └── bin/
│       ├── startxfce-x11
│       └── mscode
│
├── .config/
│   ├── mscode-fontconfig/
│   │   └── fonts.conf
│   │
│   └── mscode-certs/
│       └── ...
│
├── .cache/
│   ├── mscode/
│   │   └── mscode-last.log
│   │
│   └── termux-x11-session/
│       ├── termux-x11.log
│       ├── xfsettingsd.log
│       ├── xfwm4.log
│       ├── xfdesktop.log
│       └── xfce4-panel.log
│
├── opt/
│   ├── VSCode-linux-arm64/
│   │   ├── code
│   │   ├── bin/
│   │   ├── resources/
│   │   ├── libffmpeg.so
│   │   ├── libEGL.so
│   │   ├── libGLESv2.so
│   │   └── ...
│   │
│   └── debian-arm64-libs/
│       └── usr/
│           └── lib/
│               └── aarch64-linux-gnu/
│                   ├── libglib-2.0.so...
│                   ├── libnspr4.so...
│                   ├── libnss3.so...
│                   ├── libatk-1.0.so...
│                   ├── libX11-xcb.so...
│                   ├── libsqlite3.so...
│                   └── ...
│
└── tmp/
    └── debpkgs/
        ├── Packages.gz
        ├── Contents-arm64.gz
        ├── extract-deb-pkg
        ├── resolve-vscode-glibc-deps
        └── *.deb
```

---

# 28. Final Architecture

The successful system can be summarized as follows.

```text
Android Kernel
│
├── /dev/kgsl-3d0
│
└── Termux
    │
    ├── Bionic native environment
    │   ├── bash
    │   ├── XFCE
    │   ├── Termux:X11
    │   ├── PulseAudio
    │   ├── Mesa
    │   └── Turnip Vulkan
    │
    └── isolated glibc application path
        │
        ├── glibc-runner
        │
        ├── VSCode-linux-arm64
        │
        ├── Debian ARM64 shared-library bundle
        │
        ├── dedicated Fontconfig configuration
        │
        ├── dedicated CA configuration
        │
        └── mscode wrapper
```

Runtime boundary:

```text
Native Termux commands
    → no glibc LD_LIBRARY_PATH

MS VS Code process
    → env LD_LIBRARY_PATH=VSCode_DIR:Debian_glibc_libs
```

That separation was essential.

---

# 29. Major Findings

## Finding 1: PRoot is not fundamentally required

The official ARM64 Microsoft VS Code Linux distribution can be brought up on native Termux without PRoot or chroot if its glibc runtime and shared library dependencies are supplied explicitly.

---

## Finding 2: glibc-runner alone is not a full Linux userland

`glibc-runner` solved the ELF interpreter and glibc execution problem, but did not automatically provide every GUI, NSS, X11, Fontconfig, or runtime-loaded shared library required by Electron.

A supplemental library layer was necessary.

---

## Finding 3: Static dependency discovery is incomplete

`glibc-runner --findlib` was useful but insufficient.

It successfully discovered direct dependencies such as:

```text
libglib-2.0.so.0
libnspr4.so
libatk-1.0.so.0
```

but failed to identify runtime `dlopen()` dependencies such as:

```text
libX11-xcb.so.1
```

Strace/debug analysis was required.

---

## Finding 4: Explicit dynamic-linker invocation can break Electron startup

The ICU error:

```text
Invalid file descriptor to ICU data received
```

disappeared when moving to:

```text
glibc-runner --no-linker
```

This strongly suggests that Electron's child-process/file-descriptor model is sensitive to the invocation chain.

---

## Finding 5: X11 socket namespaces differ

Native Termux X11 socket:

```text
$TMPDIR/.X11-unix/X1
```

Conventional glibc expectation:

```text
/tmp/.X11-unix/X1
```

TCP X11 transport provided the working bridge:

```text
Termux:X11:
    :1 -listen tcp -ac

glibc application:
    DISPLAY=127.0.0.1:1
```

---

## Finding 6: Global `LD_LIBRARY_PATH` contamination is dangerous

A glibc library path exported into the normal Termux shell caused native Bionic executables to load incompatible Debian libraries.

Observed failure:

```text
CANNOT LINK EXECUTABLE "dpkg-deb":
library "libc.so.6" not found
```

The correct pattern is process-local environment injection.

---

## Finding 7: Android Linux-API restrictions are noisy but not necessarily fatal

These failed:

```text
system D-Bus
udev monitor
Netlink interface tracking
/proc/sys inotify query
login1 power management
```

Yet VS Code still reached a working desktop session.

---

## Finding 8: Successful GUI execution and successful GPU acceleration are separate milestones

VS Code could start in GPU experiment modes, but log inspection proved that the GPU process failed because:

```text
libGL.so.1
```

was unavailable in the glibc environment.

Therefore:

```text
UI launches successfully
≠
GPU acceleration successfully initialized
```

---

# 30. Final Result

The experiment successfully demonstrated the following:

```text
Official Microsoft Visual Studio Code
Version: 1.127.0
Architecture: arm64

Execution environment:
Native Termux

Containerization:
None

PRoot:
None

chroot:
None

Display:
Termux:X11 over TCP transport

Desktop:
XFCE

glibc execution:
glibc-runner --no-linker

External runtime libraries:
selectively extracted Debian ARM64 packages

Library isolation:
process-local LD_LIBRARY_PATH

VS Code GUI:
successful

VS Code workbench:
successful

Local extension host:
successful

Default extension initialization:
successful

Shared application storage:
successful

Reported render baseline:
54 ms
```

The experiment therefore establishes that a conventional glibc/Electron desktop application as complex as official Microsoft VS Code can be executed directly within a native Termux desktop stack, provided that ABI boundaries, dynamic library isolation, X11 transport, Fontconfig paths, certificates, and runtime-loaded dependencies are handled explicitly.

The most important practical lesson is:

> The successful architecture was not “make Termux look like Debian.” It was “keep Termux native, and isolate the glibc application sufficiently that both environments can coexist without contaminating each other.”
