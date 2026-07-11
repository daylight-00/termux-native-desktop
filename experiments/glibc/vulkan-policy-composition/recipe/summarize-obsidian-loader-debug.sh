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

PATTERN='Vulkan Loader Version|Found ICD manifest file|Searching for ICD drivers named|Insert instance layer|terminator_CreateInstance|linux_read_sorted_physical_devices|Original order:|Sorted order:|Copying old device|Removing driver|llvmpipe|Turnip|Adreno|gfxstream|freedreno|libvulkan_lvp|libvulkan_gfxstream'

{
    grep -E "$PATTERN" "$LOG" || true
} >"$OUT/loader-driver-summary.txt"

{
    grep -E 'linux_read_sorted_physical_devices|Original order:|Sorted order:|Copying old device|llvmpipe|Turnip|Adreno' \
        "$LOG" \
        || true
} >"$OUT/physical-device-summary.txt"

{
    grep -E 'Removing driver|terminator_CreateInstance' \
        "$LOG" \
        || true
} >"$OUT/driver-removal-summary.txt"

{
    printf 'metric\tcount\n'
    printf 'loader_version_lines\t%s\n' "$(grep -c 'Vulkan Loader Version' "$LOG" || true)"
    printf 'icd_manifest_lines\t%s\n' "$(grep -c 'Found ICD manifest file' "$LOG" || true)"
    printf 'physical_device_sort_lines\t%s\n' "$(grep -c 'linux_read_sorted_physical_devices' "$LOG" || true)"
    printf 'driver_removal_lines\t%s\n' "$(grep -c 'Removing driver' "$LOG" || true)"
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

printf '\n===== physical-device summary =====\n'
cat "$OUT/physical-device-summary.txt"

printf '\n===== driver-removal summary =====\n'
cat "$OUT/driver-removal-summary.txt"

printf '\n===== loader/driver summary =====\n'
cat "$OUT/loader-driver-summary.txt"
