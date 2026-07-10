#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
MODE=${VULKAN_POLICY_MODE:-explicit-freedreno}

source "$HOME/gl/env"
source "$SCRIPT_DIR/policy-env.sh"
apply_experiment_vulkan_policy "$MODE"

export PATH="$HOME/gl/shims:$PATH"
APP=${APP:-$HOME/gl/apps/vscode}

[ -x "$APP/bin/code" ] || {
    printf 'vscode not found: %s\n' "$APP" >&2
    exit 1
}

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

export SHELL="$PREFIX/bin/bash"

printf 'experiment Vulkan policy: %s\n' "$MODE" >&2
printf 'GL_GPU=%s\n' "${GL_GPU:-1}" >&2
printf 'VK_DRIVER_FILES=%s\n' "${VK_DRIVER_FILES:-<unset>}" >&2

exec env LD_PRELOAD= bash "$APP/bin/code" \
    --disable-dev-shm-usage \
    --ozone-platform=x11 \
    "${GPU_FLAGS[@]}" \
    "$@"
