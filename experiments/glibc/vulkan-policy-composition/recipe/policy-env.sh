# Source-only helper for the Vulkan policy composition experiment.
# This file does not source ~/gl/env itself; callers choose when shared baseline
# composition occurs, then apply one explicit provider-policy mode.

apply_experiment_vulkan_policy() {
    local mode=${1:?usage: apply_experiment_vulkan_policy MODE}
    local freedreno_icd=${GLIBC_FREEDRENO_ICD:-$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json}

    case "$mode" in
        explicit-freedreno)
            [ -r "$freedreno_icd" ] || {
                printf 'unreadable glibc Freedreno ICD: %s\n' "$freedreno_icd" >&2
                return 1
            }
            export VK_DRIVER_FILES="$freedreno_icd"
            export VK_ICD_FILENAMES="$freedreno_icd"
            ;;

        implicit-discovery)
            unset VK_DRIVER_FILES VK_ICD_FILENAMES
            ;;

        *)
            printf 'unsupported VULKAN_POLICY_MODE: %s\n' "$mode" >&2
            printf 'supported: explicit-freedreno | implicit-discovery\n' >&2
            return 2
            ;;
    esac

    export TND_EXPERIMENT_VULKAN_POLICY="$mode"
}

print_experiment_vulkan_policy() {
    printf 'VULKAN_POLICY_MODE=%s\n' "${TND_EXPERIMENT_VULKAN_POLICY:-<unset>}"
    printf 'VK_DRIVER_FILES=%s\n' "${VK_DRIVER_FILES:-<unset>}"
    printf 'VK_ICD_FILENAMES=%s\n' "${VK_ICD_FILENAMES:-<unset>}"
}
