#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
MODE=${VULKAN_POLICY_MODE:-explicit-freedreno}

[ "$#" -gt 0 ] || {
    printf 'usage: VULKAN_POLICY_MODE=MODE %s COMMAND [ARGS...]\n' "$0" >&2
    exit 2
}

source "$HOME/gl/env"
source "$SCRIPT_DIR/policy-env.sh"
apply_experiment_vulkan_policy "$MODE"

printf 'experiment Vulkan policy: %s\n' "$MODE" >&2
printf 'VK_DRIVER_FILES=%s\n' "${VK_DRIVER_FILES:-<unset>}" >&2

exec env LD_PRELOAD= MESA_LOADER_DRIVER_OVERRIDE=zink "$@"
