#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

source "$HOME/gl/env"

APP=${APP:-$HOME/gl/apps/obsidian}

export APPDIR="$APP"
export PATH="$HOME/gl/shims:$APP:$APP/usr/sbin:$PATH"
export XDG_DATA_DIRS="$APP/usr/share:${XDG_DATA_DIRS:-}"

if [ -d "$APP/usr/share/glib-2.0/schemas" ]; then
    export GSETTINGS_SCHEMA_DIR="$APP/usr/share/glib-2.0/schemas"
fi

# Experimental difference from the promoted launcher:
# remove Vulkan provider-selection policy after sourcing gl/env.
unset VK_DRIVER_FILES VK_ICD_FILENAMES

exec env LD_PRELOAD= \
    "$APP/obsidian" \
    --disable-dev-shm-usage \
    --ozone-platform=x11 \
    --disable-gpu \
    "$@"
