#!/data/data/com.termux/files/usr/bin/bash
# build-mesa.sh — Mesa (Turnip KGSL + Zink) glibc build for the gl layer.
#
# Host tools:   bionic (meson/ninja/python via uv venv)
# Target:       Termux glibc ($PREFIX/glibc), Adreno 7xx via KGSL
# Output:       ~/gl/opt/mesa-glibc-<version>/  (+ stable symlink after verify)
#
# Usage:
#   ./build-mesa.sh              # latest 26.1.x tag
#   MESA_TAG=mesa-26.1.3 ./build-mesa.sh
#   JOBS=6 ./build-mesa.sh       # override parallelism (thermal throttling)
set -euo pipefail

GL="$HOME/gl"
TC="$GL/toolchain"
WORK="$GL/build/mesa"
VENV="$GL/build/.venv"
SERIES="${SERIES:-26.1}"
JOBS="${JOBS:-$(nproc)}"

# ---------------------------------------------------------------- 0. host env
# NEVER export LD_LIBRARY_PATH here (bionic shell). Wrappers handle scoping.
unset LD_LIBRARY_PATH LD_PRELOAD || true

for t in glibc-gcc glibc-g++ glibc-pkg-config glibc-exec; do
  [ -x "$TC/$t" ] || { echo "missing toolchain wrapper: $TC/$t"; exit 1; }
done

if [ ! -x "$VENV/bin/meson" ]; then
  echo "== creating build venv (uv) =="
  uv venv "$VENV"
  uv pip install --python "$VENV/bin/python" meson mako packaging pyyaml
fi
export PATH="$VENV/bin:$PATH"

CCACHE=""
command -v ccache >/dev/null && CCACHE="'ccache', "

# ------------------------------------------------------- 1. toolchain smoke test
# Gate from the previous run: -B linker fix was never verified through a full
# build. Prove compile+link+run works before touching Mesa.
echo "== toolchain smoke test =="
ST=$(mktemp -d)
cat > "$ST/t.cc" <<'EOF'
#include <iostream>
#include <thread>
int main(){ std::thread t([]{ std::cout << "link-ok\n"; }); t.join(); }
EOF
"$TC/glibc-g++" -O2 -o "$ST/t" "$ST/t.cc" -lpthread
out=$("$TC/glibc-exec" "$ST/t")
[ "$out" = "link-ok" ] || { echo "smoke test FAILED"; exit 1; }
rm -rf "$ST"
echo "   compiler + linker + runtime: OK"

# ---------------------------------------------------------------- 2. source
echo "== resolving latest $SERIES tag =="
mkdir -p "$WORK"
if [ ! -d "$WORK/src/.git" ]; then
  git clone --depth 1 https://gitlab.freedesktop.org/mesa/mesa.git "$WORK/src"
fi
cd "$WORK/src"
if [ -z "${MESA_TAG:-}" ]; then
  # ls-remote avoids the shallow-clone tag-refspec problem entirely
  MESA_TAG=$(git ls-remote --tags origin "refs/tags/mesa-${SERIES}.*" \
    | awk -F/ '{print $NF}' | grep -v '\^{}' | sort -V | tail -1)
fi
[ -n "$MESA_TAG" ] || { echo "no $SERIES tag found"; exit 1; }
echo "   tag: $MESA_TAG"
git fetch --depth 1 origin "refs/tags/$MESA_TAG:refs/tags/$MESA_TAG"
git checkout -f "$MESA_TAG"

VERSION="${MESA_TAG#mesa-}"
DESTDIR="$GL/opt/mesa-glibc-$VERSION"
BUILDDIR="$WORK/build-$VERSION"

# Known issue from previous run: generator scripts fail on #!/usr/bin/env shebangs.
echo "== fixing generator shebangs =="
find src -name '*.py' -exec termux-fix-shebang {} + 2>/dev/null || true

# ---------------------------------------------------------------- 3. cross file
# Generated per build so the -Wl,-rpath and prefix always match the versioned dir.
CROSS="$WORK/cross-$VERSION.ini"
cat > "$CROSS" <<EOF
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
EOF

# ---------------------------------------------------------------- 4. configure
# Verified base (Turnip KGSL) + separately-verified Zink extension, one build.
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

# ---------------------------------------------------------------- 5. build + install
echo "== ninja -j$JOBS =="
ninja -C "$BUILDDIR" -j"$JOBS"
ninja -C "$BUILDDIR" install

echo
echo "== installed: $DESTDIR =="
echo
echo "Verify in layers, then promote the stable symlink:"
echo "  1) VK_ICD_FILENAMES=$DESTDIR/share/vulkan/icd.d/freedreno_icd.aarch64.json \\"
echo "       $TC/glibc-exec \$PREFIX/glibc/bin/vulkaninfo --summary   # expect: Turnip Adreno 730"
echo "  2) Zink/EGL, then GLX checks (see docs)"
echo "  3) ln -sfn '$DESTDIR' '$GL/opt/mesa-glibc'   # launcher picks it up via GL_GPU=1"
