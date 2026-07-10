#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
MODE=${VULKAN_POLICY_MODE:-explicit-freedreno}

source "$HOME/gl/env"
source "$SCRIPT_DIR/policy-env.sh"
apply_experiment_vulkan_policy "$MODE"

APP=${APP:-$HOME/gl/apps/obsidian}

[ -x "$APP/obsidian" ] || {
    printf 'obsidian not found: %s\n' "$APP" >&2
    exit 1
}

export APPDIR="$APP"
export PATH="$HOME/gl/shims:$APP:$APP/usr/sbin:$PATH"
export XDG_DATA_DIRS="$APP/usr/share:${XDG_DATA_DIRS:-}"

if [ -d "$APP/usr/share/glib-2.0/schemas" ]; then
    export GSETTINGS_SCHEMA_DIR="$APP/usr/share/glib-2.0/schemas"
fi

GPU_FLAGS=(--disable-gpu)
if [ "${GL_GPU:-1}" = 1 ]; then
    GPU_FLAGS=(
        --disable-gpu-sandbox
        --ignore-gpu-blocklist
        --enable-features=Vulkan
        --use-gl=angle
        --use-angle=vulkan
        --disable-gpu-vsync
    )
fi

printf 'experiment Vulkan policy: %s\n' "$MODE" >&2
printf 'GL_GPU=%s\n' "${GL_GPU:-1}" >&2
printf 'VK_DRIVER_FILES=%s\n' "${VK_DRIVER_FILES:-<unset>}" >&2

exec env LD_PRELOAD= \
    "$APP/obsidian" \
    --disable-dev-shm-usage \
    --ozone-platform=x11 \
    "${GPU_FLAGS[@]}" \
    "$@"
