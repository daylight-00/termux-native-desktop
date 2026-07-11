#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

CONTROL_OUT=${CONTROL_OUT:?set CONTROL_OUT to an Obsidian loader-debug evidence directory}
LOG="$CONTROL_OUT/launch.stderr"
OUT="$CONTROL_OUT/loader-selection-debug"

[ -f "$LOG" ] || {
    printf 'missing loader-debug stderr: %s\n' "$LOG" >&2
    exit 1
}

mkdir -p "$OUT"

PATTERN='Vulkan Loader Version|Found ICD manifest file|Searching for ICD drivers named|Insert instance layer|terminator_CreateInstance|linux_read_sorted_physical_devices|Original order:|Sorted order:|Copying old device|Removing driver|Using ".*" with driver:|llvmpipe|Turnip|Adreno|gfxstream|freedreno|libvulkan_lvp|libvulkan_gfxstream'

{
    grep -E "$PATTERN" "$LOG" || true
} >"$OUT/loader-driver-summary.txt"

{
    grep -E 'Using ".*" with driver:' "$LOG" \
        | sort -u \
        || true
} >"$OUT/selected-driver-lines.txt"

{
    grep -E '\[[0-9]+\] ' "$LOG" \
        | sed -E 's/^.*\[[0-9]+\] //' \
        | sort -u \
        || true
} >"$OUT/physical-device-identities.txt"

{
    grep -E 'Removing driver .* due to not having any physical devices' "$LOG" \
        | sed -E 's/^.*Removing driver ([^ ]+) due to not having any physical devices.*$/\1/' \
        | sort -u \
        || true
} >"$OUT/removed-drivers.txt"

{
    grep -E 'Found ICD manifest file ' "$LOG" \
        | sed -E 's/^.*Found ICD manifest file ([^,]+),.*$/\1/' \
        | sort -u \
        || true
} >"$OUT/discovered-icd-manifests.txt"

{
    grep -E 'Using ".*" with driver:' "$LOG" \
        | sed -n -E 's/^.*with driver: "(.*)"$/\1/p' \
        | sort -u \
        || true
} >"$OUT/selected-driver-reported-paths.txt"

{
    printf 'reported_driver_path\tcurrent_resolved_path\tstate\n'
    while IFS= read -r path; do
        [ -n "$path" ] || continue
        if [ -e "$path" ]; then
            printf '%s\t%s\tPRESENT\n' "$path" "$(readlink -f "$path")"
        else
            printf '%s\tNOT_AVAILABLE\tMISSING_CURRENTLY\n' "$path"
        fi
    done <"$OUT/selected-driver-reported-paths.txt"
} >"$OUT/selected-driver-path-resolution.tsv"

{
    grep -E 'terminator_CreateInstance' "$LOG" \
        | sort -u \
        || true
} >"$OUT/driver-instance-warnings.txt"

{
    printf 'metric\tcount\n'
    printf 'loader_version_lines\t%s\n' "$(grep -c 'Vulkan Loader Version' "$LOG" || true)"
    printf 'icd_manifest_lines\t%s\n' "$(grep -c 'Found ICD manifest file' "$LOG" || true)"
    printf 'physical_device_sort_lines\t%s\n' "$(grep -c 'linux_read_sorted_physical_devices' "$LOG" || true)"
    printf 'driver_removal_lines\t%s\n' "$(grep -c 'Removing driver' "$LOG" || true)"
    printf 'selected_driver_lines\t%s\n' "$(grep -c -E 'Using ".*" with driver:' "$LOG" || true)"
    printf 'llvmpipe_lines\t%s\n' "$(grep -c 'llvmpipe' "$LOG" || true)"
    printf 'turnip_lines\t%s\n' "$(grep -c -E 'Turnip|Adreno' "$LOG" || true)"
    printf 'gfxstream_lines\t%s\n' "$(grep -c -E 'gfxstream|libvulkan_gfxstream' "$LOG" || true)"
    printf 'lvp_lines\t%s\n' "$(grep -c -E 'libvulkan_lvp|lvp_icd' "$LOG" || true)"
} >"$OUT/loader-debug-counts.tsv"

printf 'Obsidian loader debug summary: PASS\n'
printf 'input: %s\n' "$LOG"
printf 'output: %s\n' "$OUT"

printf '\n===== loader debug counts =====\n'
cat "$OUT/loader-debug-counts.tsv"

printf '\n===== selected driver lines =====\n'
cat "$OUT/selected-driver-lines.txt"

printf '\n===== physical device identities =====\n'
cat "$OUT/physical-device-identities.txt"

printf '\n===== removed drivers =====\n'
cat "$OUT/removed-drivers.txt"

printf '\n===== selected driver path resolution =====\n'
cat "$OUT/selected-driver-path-resolution.tsv"

printf '\n===== driver instance warnings =====\n'
cat "$OUT/driver-instance-warnings.txt"
