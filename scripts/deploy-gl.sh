#!/data/data/com.termux/files/usr/bin/bash
# Link repository source-of-truth paths into the live runtime tree.
# Runtime state (apps/lib/opt and build worktrees) stays outside Git tracking.
set -eu

R="$HOME/termux-native-desktop"
mkdir -p "$HOME/gl/build" "$HOME/gl/apps" "$HOME/gl/opt" "$HOME/.local/bin"

link_replace() {
    src="$1"
    dst="$2"

    if [ -d "$dst" ] && [ ! -L "$dst" ]; then
        printf 'refusing to replace real directory: %s\n' "$dst" >&2
        return 1
    fi

    ln -sfn "$src" "$dst"
}

link_optional() {
    src="$1"
    dst="$2"

    if [ ! -e "$src" ]; then
        printf 'warning: optional source not present, leaving target unchanged: %s\n' "$src" >&2
        return 0
    fi

    link_replace "$src" "$dst"
}

link_replace "$R/setup/glibc/env"       "$HOME/gl/env"
link_replace "$R/setup/glibc/bin"       "$HOME/gl/bin"
link_replace "$R/setup/glibc/shims"     "$HOME/gl/shims"
link_replace "$R/setup/glibc/toolchain" "$HOME/gl/toolchain"

for f in build-mesa.sh pyproject.toml uv.lock; do
    link_replace "$R/setup/mesa/$f" "$HOME/gl/build/$f"
done

link_optional "$R/setup/mesa/patches" "$HOME/gl/build/patches"
link_replace  "$R/setup/mesa/diag"    "$HOME/gl/build/diag"

link_replace "$R/setup/session/startxfce-x11" "$HOME/.local/bin/startxfce-x11"
link_replace "$R/setup/glibc/bin/code"         "$HOME/.local/bin/code"

printf 'deployed: repo -> live Termux paths\n'
