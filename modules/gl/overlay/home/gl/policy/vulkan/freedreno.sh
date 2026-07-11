# Source-only glibc Vulkan provider profile: explicit Freedreno/Turnip.
#
# Contract:
#   source "$HOME/gl/env" first to establish the glibc-world baseline and clear
#   inherited bionic Vulkan policy, then source this file only for consumers
#   that deliberately select the hardware Vulkan provider.
#
# Return status:
#   0  provider manifest is readable and both loader variables were exported
#   1  provider manifest is unavailable and both loader variables were cleared

_TND_GLIBC_FREEDRENO_ICD="$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json"

if [ -r "$_TND_GLIBC_FREEDRENO_ICD" ]; then
    export VK_ICD_FILENAMES="$_TND_GLIBC_FREEDRENO_ICD"
    export VK_DRIVER_FILES="$_TND_GLIBC_FREEDRENO_ICD"
    unset _TND_GLIBC_FREEDRENO_ICD
    return 0 2>/dev/null || exit 0
fi

unset VK_ICD_FILENAMES VK_DRIVER_FILES _TND_GLIBC_FREEDRENO_ICD
return 1 2>/dev/null || exit 1
