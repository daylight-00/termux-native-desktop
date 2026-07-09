#!/data/data/com.termux/files/usr/bin/bash
# bisect-test.sh — git bisect judge for the 26.0.x -> 26.1.x Turnip WSI SIGBUS.
# Run from inside the mesa source tree (git bisect run ./bisect-test.sh).
#
# Exit codes (git bisect contract):
#   0   = good  (vkcube ran without SIGBUS)
#   1   = bad   (vkcube died with SIGBUS/crash)
#   125 = skip  (build failed -> commit untestable)
#
# Requires: an X server on $DISPLAY (vkcube creates an xcb surface).
set -u

GL="$HOME/gl"
TC="$GL/toolchain"
VENV="$GL/build/.venv"
BUILDDIR="build-bisect"
PREFIX_DIR="$GL/opt/mesa-bisect"          # throwaway install target
JOBS="${JOBS:-$(nproc)}"

unset LD_LIBRARY_PATH LD_PRELOAD || true
export PATH="$VENV/bin:$PATH"
: "${DISPLAY:=:1}"; export DISPLAY

# --- clean any state from the previous bisect step ---
rm -rf "$BUILDDIR" "$PREFIX_DIR"
git checkout -- . 2>/dev/null || true

# CRITICAL: shebang edits below must never survive into the next bisect checkout,
# or git refuses to switch commits. Restore tracked files on every exit.
restore_tree() { cd "$SRC" 2>/dev/null && git checkout -- . 2>/dev/null || true; }
SRC="$(pwd)"
trap restore_tree EXIT

# generator shebangs (regenerated per checkout)
find src -name '*.py' -exec termux-fix-shebang {} + 2>/dev/null || true

CCACHE=""
command -v ccache >/dev/null && CCACHE="'ccache', "

CROSS="$GL/build/cross-bisect.ini"
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
prefix = '$PREFIX_DIR'
libdir = 'lib'
buildtype = 'release'
c_args = ['-O2']
cpp_args = ['-O2']
c_link_args = ['-Wl,-rpath,$PREFIX_DIR/lib']
cpp_link_args = ['-Wl,-rpath,$PREFIX_DIR/lib']
EOF

# --- configure + build (minimal: turnip only, no zink -> faster bisect) ---
if ! meson setup "$BUILDDIR" --cross-file "$CROSS" \
    -Dplatforms=x11 -Dvulkan-drivers=freedreno -Dfreedreno-kmds=kgsl \
    -Dgallium-drivers= -Dllvm=disabled -Dshared-llvm=disabled \
    -Dbuild-tests=false -Dvalgrind=disabled -Dlibunwind=disabled \
    >$PREFIX/tmp/bisect-setup.log 2>&1; then
  echo "[bisect] meson setup failed -> skip"; exit 125
fi
if ! ninja -C "$BUILDDIR" -j"$JOBS" >$PREFIX/tmp/bisect-build.log 2>&1; then
  echo "[bisect] build failed -> skip"; exit 125
fi
if ! ninja -C "$BUILDDIR" install >$PREFIX/tmp/bisect-install.log 2>&1; then
  echo "[bisect] install failed -> skip"; exit 125
fi

ICD="$PREFIX_DIR/share/vulkan/icd.d/freedreno_icd.aarch64.json"
[ -r "$ICD" ] || { echo "[bisect] no ICD -> skip"; exit 125; }

# --- judge: run vkcube, force-quit after a few frames ---
# Good  = survives the timeout (124) -> no crash.
# Bad   = dies from a signal (SIGBUS=135 etc, i.e. 128+n) before timeout.
VK_ICD_FILENAMES="$ICD" VK_DRIVER_FILES="$ICD" \
  timeout -s KILL 6 "$TC/glibc-exec" "$PREFIX/glibc/bin/vkcube" --wsi xcb \
  >$PREFIX/tmp/bisect-vkcube.log 2>&1
rc=$?

echo "[bisect] vkcube rc=$rc"
if [ "$rc" -eq 124 ] || [ "$rc" -eq 137 ]; then
  # 124 = timeout fired (TERM), 137 = 128+9 KILL from timeout -> it was alive
  echo "[bisect] GOOD (survived)"; exit 0
elif [ "$rc" -ge 128 ]; then
  echo "[bisect] BAD (signal $((rc-128)))"; exit 1
else
  # clean exit (0) also means it ran fine
  [ "$rc" -eq 0 ] && { echo "[bisect] GOOD (clean exit)"; exit 0; }
  echo "[bisect] ambiguous rc=$rc -> skip"; exit 125
fi
