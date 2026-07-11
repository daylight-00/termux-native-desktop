#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

CONTROL_OUT=${CONTROL_OUT:?set CONTROL_OUT to an Electron loader-debug evidence directory}
STDOUT_LOG="$CONTROL_OUT/launch.stdout"
STDERR_LOG="$CONTROL_OUT/launch.stderr"
OUT="$CONTROL_OUT/loader-selection-debug"

logs=()
[ -f "$STDOUT_LOG" ] && logs+=("$STDOUT_LOG")
[ -f "$STDERR_LOG" ] && logs+=("$STDERR_LOG")

[ "${#logs[@]}" -gt 0 ] || {
    printf 'missing loader-debug launch streams under: %s\n' "$CONTROL_OUT" >&2
    exit 1
}

mkdir -p "$OUT"

combined=$(mktemp)
trap 'rm -f "$combined"' EXIT
: >"$combined"
for log in "${logs[@]}"; do
    cat "$log" >>"$combined"
    printf '\n' >>"$combined"
done

PATTERN='Vulkan Loader Version|Found ICD manifest file|Searching for ICD drivers named|Insert instance layer|terminator_CreateInstance|linux_read_sorted_physical_devices|Original order:|Sorted order:|Copying old device|Removing driver|Using ".*" with driver:|llvmpipe|Turnip|Adreno|gfxstream|freedreno|libvulkan_lvp|libvulkan_gfxstream'

{
    printf 'stream\tpath\tbytes\tloader_signal_lines\tselected_driver_lines\n'
    for stream in stdout stderr; do
        case "$stream" in
            stdout) log=$STDOUT_LOG ;;
            stderr) log=$STDERR_LOG ;;
        esac

        if [ -f "$log" ]; then
            bytes=$(wc -c <"$log" | tr -d ' ')
            signal_count=$(grep -cE "$PATTERN" "$log" || true)
            selected_count=$(grep -cE 'Using ".*" with driver:' "$log" || true)
            printf '%s\t%s\t%s\t%s\t%s\n' \
                "$stream" "$log" "$bytes" "$signal_count" "$selected_count"
        else
            printf '%s\t%s\t0\t0\t0\n' "$stream" "$log"
        fi
    done
} >"$OUT/input-streams.tsv"

{
    grep -E "$PATTERN" "$combined" || true
} >"$OUT/loader-driver-summary.txt"

{
    grep -E 'Using ".*" with driver:' "$combined" \
        | sort -u \
        || true
} >"$OUT/selected-driver-lines.txt"

{
    grep -E '\[[0-9]+\] ' "$combined" \
        | sed -E 's/^.*\[[0-9]+\] //' \
        | sort -u \
        || true
} >"$OUT/physical-device-identities.txt"

{
    grep -E 'Removing driver .* due to not having any physical devices' "$combined" \
        | sed -E 's/^.*Removing driver ([^ ]+) due to not having any physical devices.*$/\1/' \
        | sort -u \
        || true
} >"$OUT/removed-drivers.txt"

{
    grep -E 'Found ICD manifest file ' "$combined" \
        | sed -E 's/^.*Found ICD manifest file ([^,]+),.*$/\1/' \
        | sort -u \
        || true
} >"$OUT/discovered-icd-manifests.txt"

{
    grep -E 'Using ".*" with driver:' "$combined" \
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
    grep -E 'terminator_CreateInstance' "$combined" \
        | sort -u \
        || true
} >"$OUT/driver-instance-warnings.txt"

{
    printf 'metric\tcount\n'
    printf 'loader_version_lines\t%s\n' "$(grep -c 'Vulkan Loader Version' "$combined" || true)"
    printf 'icd_manifest_lines\t%s\n' "$(grep -c 'Found ICD manifest file' "$combined" || true)"
    printf 'physical_device_sort_lines\t%s\n' "$(grep -c 'linux_read_sorted_physical_devices' "$combined" || true)"
    printf 'driver_removal_lines\t%s\n' "$(grep -c 'Removing driver' "$combined" || true)"
    printf 'selected_driver_lines\t%s\n' "$(grep -cE 'Using ".*" with driver:' "$combined" || true)"
    printf 'llvmpipe_lines\t%s\n' "$(grep -c 'llvmpipe' "$combined" || true)"
    printf 'turnip_lines\t%s\n' "$(grep -cE 'Turnip|Adreno' "$combined" || true)"
    printf 'gfxstream_lines\t%s\n' "$(grep -cE 'gfxstream|libvulkan_gfxstream' "$combined" || true)"
    printf 'lvp_lines\t%s\n' "$(grep -cE 'libvulkan_lvp|lvp_icd' "$combined" || true)"
} >"$OUT/loader-debug-counts.tsv"

printf 'Electron loader debug summary: PASS\n'
printf 'control evidence: %s\n' "$CONTROL_OUT"
printf 'output: %s\n' "$OUT"

printf '\n===== input streams =====\n'
cat "$OUT/input-streams.tsv"

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
