#!/data/data/com.termux/files/usr/bin/bash
# build-mesa.sh — Mesa (Turnip KGSL + Zink) glibc build for the gl layer.
#
# Host tools:  bionic (Meson/Ninja via the immutable project under ~/gl/build)
# Mutable state: $XDG_STATE_HOME/termux-native-desktop/workspaces/mesa
# Target:      Termux glibc ($PREFIX/glibc), Adreno 7xx via KGSL
# Output:      $XDG_STATE_HOME/termux-native-desktop/providers/mesa/candidates/
#
# Usage:
#   ./build-mesa.sh                    # latest stable tag of $SERIES
#   MESA_TAG=mesa-26.1.4 ./build-mesa.sh
#   JOBS=6 ./build-mesa.sh             # thermal throttling
#   SERIES=26.2 ./build-mesa.sh
#
# CRITICAL, do not change back (see docs/gpu.md §3):
#   -Dfreedreno-kmds=msm,kgsl  — kgsl alone drops libdrm from the turnip ICD
#   and the investigated X11 present path then died with SIGBUS (BUS_ADRALN@0x1).
set -euo pipefail

GL="$HOME/gl"
TC="$GL/toolchain"
STATE_BASE="${TND_STATE_BASE:-${XDG_STATE_HOME:-$HOME/.local/state}/termux-native-desktop}"
WORKSPACE="${TND_MESA_WORKSPACE:-$STATE_BASE/workspaces/mesa}"
PROVIDER_ROOT="${TND_MESA_PROVIDER_ROOT:-$STATE_BASE/providers/mesa}"
WORK="$WORKSPACE/mesa"
VENV="$WORKSPACE/.venv"
SERIES="${SERIES:-26.1}"
JOBS="${JOBS:-$(nproc)}"

# ------------------------------------------------------------------ host env
# NEVER export LD_LIBRARY_PATH in this (bionic) shell. Wrappers scope it.
unset LD_LIBRARY_PATH LD_PRELOAD || true

for t in glibc-gcc glibc-g++ glibc-pkg-config glibc-exec; do
  [ -x "$TC/$t" ] || { echo "missing toolchain wrapper: $TC/$t"; exit 1; }
done

# Python build deps remain declarative under the immutable release, while the
# generated environment is stored in XDG state.
[ -f "$GL/build/pyproject.toml" ] || { echo "missing build project: $GL/build/pyproject.toml"; exit 1; }
mkdir -p "$WORKSPACE" "$PROVIDER_ROOT/candidates" "$GL/opt"
( cd "$GL/build" && UV_PROJECT_ENVIRONMENT="$VENV" uv sync )
export PATH="$VENV/bin:$PATH"

CCACHE=""
command -v ccache >/dev/null && CCACHE="'ccache', "

# ------------------------------------------------- toolchain smoke test gate
echo "== toolchain smoke test =="
ST=$(mktemp -d)
cat > "$ST/t.cc" <<'SRC'
#include <iostream>
#include <thread>
int main(){ std::thread t([]{ std::cout << "link-ok\n"; }); t.join(); }
SRC
"$TC/glibc-g++" -O2 -o "$ST/t" "$ST/t.cc" -lpthread
[ "$("$TC/glibc-exec" "$ST/t")" = "link-ok" ] || { echo "smoke test FAILED"; exit 1; }
rm -rf "$ST"
echo "   compiler + linker + runtime: OK"

# ------------------------------------------------------------------- source
echo "== resolving latest $SERIES tag =="
mkdir -p "$WORK"
if [ ! -d "$WORK/src/.git" ]; then
  git clone --depth 1 https://gitlab.freedesktop.org/mesa/mesa.git "$WORK/src"
fi
cd "$WORK/src"
if [ -z "${MESA_TAG:-}" ]; then
  MESA_TAG=$(git ls-remote --tags origin "refs/tags/mesa-${SERIES}.*" \
    | awk -F/ '{print $NF}' | grep -v '\^{}' | sort -V | tail -1)
fi
[ -n "$MESA_TAG" ] || { echo "no $SERIES tag found"; exit 1; }
echo "   tag: $MESA_TAG"
git fetch --depth 1 origin "refs/tags/$MESA_TAG:refs/tags/$MESA_TAG" 2>/dev/null || true
git checkout -f "$MESA_TAG"
git clean -fd src >/dev/null 2>&1 || true

VERSION="${MESA_TAG#mesa-}"

# ------------------------------------------------- optional local patches
# Any *.patch in $GL/build/patches/mesa is applied in filename order and the
# install prefix gets a "-tx" suffix so patched and vanilla builds coexist.
PATCHDIR="$GL/build/patches/mesa"
PATCHSET=""
if ls "$PATCHDIR"/*.patch >/dev/null 2>&1; then
  PATCHSET="-tx"
  for p in "$PATCHDIR"/*.patch; do
    echo "== applying $(basename "$p") =="
    git apply --3way "$p" || { echo "PATCH FAILED: $p"; exit 1; }
  done
fi

DESTDIR="$PROVIDER_ROOT/candidates/mesa-glibc-$VERSION$PATCHSET"
COMPAT_DEST="$GL/opt/mesa-glibc-$VERSION$PATCHSET"
BUILDDIR="$WORK/build-$VERSION$PATCHSET"

if [ -e "$COMPAT_DEST" ] && [ ! -L "$COMPAT_DEST" ]; then
  echo "legacy provider path is still a directory; run tools/migrate-local-layout first: $COMPAT_DEST" >&2
  exit 1
fi
if [ -L "$COMPAT_DEST" ]; then
  compat_resolved=$(readlink -f "$COMPAT_DEST" 2>/dev/null || true)
  expected_resolved=$(readlink -f "$DESTDIR" 2>/dev/null || printf '%s' "$DESTDIR")
  [ "$compat_resolved" = "$expected_resolved" ] || {
    echo "legacy provider compatibility path points elsewhere: $COMPAT_DEST" >&2
    exit 1
  }
fi
ln -sfn "$DESTDIR" "$COMPAT_DEST"

# Known issue: generator scripts fail on #!/usr/bin/env shebangs.
find src -name '*.py' -exec termux-fix-shebang {} + 2>/dev/null || true

# ---------------------------------------------------------------- cross file
CROSS="$WORK/cross-$VERSION$PATCHSET.ini"
cat > "$CROSS" <<CROSSEOF
[binaries]
c = [${CCACHE}'$TC/glibc-gcc']
cpp = [${CCACHE}'$TC/glibc-g++']
ar = '$TC/glibc-ar'
ranlib = '$TC/glibc-ranlib'
strip = '$TC/glibc-strip'
pkg-config = '$TC/glibc-pkg-config'
exe_wrapper = '$TC/glibc-exec'
[host_machine]
system = 'linux'
cpu_family = 'aarch64'
cpu = 'aarch64'
endian = 'little'
[properties]
needs_exe_wrapper = true
[built-in options]
prefix = '$DESTDIR'
libdir = 'lib'
buildtype = 'release'
c_args = ['-O2']
cpp_args = ['-O2']
c_link_args = ['-Wl,-rpath,$DESTDIR/lib']
cpp_link_args = ['-Wl,-rpath,$DESTDIR/lib']
CROSSEOF
# ---------------------------------------------------------------- configure
echo "== meson setup =="
meson setup "$BUILDDIR" \
  --cross-file "$CROSS" \
  -Dplatforms=x11 \
  -Dvulkan-drivers=freedreno \
  -Dfreedreno-kmds=msm,kgsl \
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
# ------------------------------------------------------------- build/install
echo "== ninja -j$JOBS =="
ninja -C "$BUILDDIR" -j"$JOBS"
ninja -C "$BUILDDIR" install

# sanity: the validated msm,kgsl configuration should retain libdrm
if ! readelf -d "$DESTDIR/lib/libvulkan_freedreno.so" | grep -q libdrm; then
  echo "WARNING: libvulkan_freedreno.so is NOT linked against libdrm."
  echo "         The investigated kgsl-only configuration failed at present. Check -Dfreedreno-kmds. (docs/gpu.md §3)"
fi

echo
echo "== installed: $DESTDIR =="
echo "Verify, then promote atomically:"
echo "  ICD=$DESTDIR/share/vulkan/icd.d/freedreno_icd.aarch64.json"
echo "  VK_ICD_FILENAMES=\$ICD VK_DRIVER_FILES=\$ICD \\"
echo "    $TC/glibc-exec \$PREFIX/glibc/bin/vkcube --wsi xcb    # default-WSI presentation check"
echo "  ln -sfn '$DESTDIR' '$PROVIDER_ROOT/current'"
echo "  ln -sfn '$PROVIDER_ROOT/current' '$GL/opt/mesa-glibc'"
