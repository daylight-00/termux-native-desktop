#!/data/data/com.termux/files/usr/bin/bash
# Symlink the repo's source-of-truth into the live runtime tree (~/gl).
# Edit in repo = live immediately; runtime state (apps/lib/opt) stays in ~/gl.
set -eu
R="$HOME/termux-native-desktop"
mkdir -p ~/gl/build ~/gl/apps ~/gl/opt
ln -sfn "$R/setup/glibc/env"       ~/gl/env
ln -sfn "$R/setup/glibc/bin"       ~/gl/bin
ln -sfn "$R/setup/glibc/shims"     ~/gl/shims
ln -sfn "$R/setup/glibc/toolchain" ~/gl/toolchain
for f in build-mesa.sh pyproject.toml uv.lock; do
  ln -sfn "$R/setup/mesa/$f" ~/gl/build/$f
done
ln -sfn "$R/setup/mesa/patches" ~/gl/build/patches
ln -sfn "$R/setup/mesa/diag"    ~/gl/build/diag
ln -sfn "$R/setup/session/startxfce-x11" ~/.local/bin/startxfce-x11
ln -sfn "$R/setup/glibc/bin/code"        ~/.local/bin/code
echo "deployed: repo -> ~/gl (symlinks)"
