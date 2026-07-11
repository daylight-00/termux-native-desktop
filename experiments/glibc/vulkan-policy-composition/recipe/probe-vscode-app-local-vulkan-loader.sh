#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

APP=${APP:-$HOME/gl/apps/vscode}
TARGET=${TARGET:-$APP/libvulkan.so.1}
CONTROL_OUT=${CONTROL_OUT:-}
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-loader-identity-$(date +%Y%m%d-%H%M%S)}
ROOTFS=${ROOTFS:-$PREFIX/var/lib/proot-distro/containers/debian/rootfs}

for command in readelf sha256sum strings readlink stat awk grep sed sort; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

[ -f "$TARGET" ] || {
    printf 'missing VS Code app-local Vulkan loader: %s\n' "$TARGET" >&2
    exit 1
}

mkdir -p "$OUT"

build_id_of() {
    {
        readelf -n "$1" 2>/dev/null || true
    } | awk '/Build ID:/ && id == "" { id = $3 } END { if (id != "") print id }'
}

soname_of() {
    {
        readelf -d "$1" 2>/dev/null || true
    } | sed -n -E 's/^.*\(SONAME\).*\[(.*)\].*$/\1/p' | head -n 1
}

bool_string() {
    local path=$1
    local needle=$2
    if strings -a "$path" 2>/dev/null | grep -Fq -- "$needle"; then
        printf 'YES\n'
    else
        printf 'NO\n'
    fi
}

printf 'label\trequested_path\tresolved_path\tbytes\tsha256\tbuild_id\tsoname\thas_vk_loader_debug_string\thas_vulkan_loader_banner_string\n' \
    >"$OUT/candidate-identities.tsv"

add_candidate() {
    local label=$1
    local requested=$2
    local resolved bytes sha build_id soname has_debug has_banner

    [ -e "$requested" ] || return 0

    resolved=$(readlink -f "$requested")
    [ -f "$resolved" ] || return 0

    bytes=$(stat -c '%s' "$resolved")
    sha=$(sha256sum "$resolved" | awk '{print $1}')
    build_id=$(build_id_of "$resolved")
    [ -n "$build_id" ] || build_id=NONE
    soname=$(soname_of "$resolved")
    [ -n "$soname" ] || soname=NONE
    has_debug=$(bool_string "$resolved" 'VK_LOADER_DEBUG')
    has_banner=$(bool_string "$resolved" 'Vulkan Loader Version')

    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$label" "$requested" "$resolved" "$bytes" "$sha" "$build_id" "$soname" "$has_debug" "$has_banner" \
        >>"$OUT/candidate-identities.tsv"
}

add_candidate APP_LOCAL "$TARGET"
add_candidate GL_FARM_ALIAS "$HOME/gl/lib/libvulkan.so.1"
add_candidate PREFIX_GLIBC_LIB "$PREFIX/glibc/lib/libvulkan.so.1"
add_candidate PREFIX_GLIBC_LIB64 "$PREFIX/glibc/lib64/libvulkan.so.1"
add_candidate PREFIX_GLIBC_MULTIARCH "$PREFIX/glibc/lib/aarch64-linux-gnu/libvulkan.so.1"
add_candidate ROOTFS_MULTIARCH "$ROOTFS/usr/lib/aarch64-linux-gnu/libvulkan.so.1"
add_candidate ROOTFS_LIB "$ROOTFS/usr/lib/libvulkan.so.1"

app_sha=$(awk -F $'\t' '$1 == "APP_LOCAL" { print $5 }' "$OUT/candidate-identities.tsv")
app_build_id=$(awk -F $'\t' '$1 == "APP_LOCAL" { print $6 }' "$OUT/candidate-identities.tsv")

printf 'label\tresolved_path\tsha_relation_to_app\tbuild_id_relation_to_app\n' \
    >"$OUT/app-comparisons.tsv"

awk -F $'\t' 'NR > 1 { print $1 "\t" $3 "\t" $5 "\t" $6 }' "$OUT/candidate-identities.tsv" \
    | while IFS=$'\t' read -r label resolved sha build_id; do
        if [ "$sha" = "$app_sha" ]; then
            sha_relation=SAME
        else
            sha_relation=DIFFERENT
        fi

        if [ "$build_id" != NONE ] && [ "$app_build_id" != NONE ] && [ "$build_id" = "$app_build_id" ]; then
            build_relation=SAME
        else
            build_relation=DIFFERENT_OR_UNAVAILABLE
        fi

        printf '%s\t%s\t%s\t%s\n' \
            "$label" "$resolved" "$sha_relation" "$build_relation" \
            >>"$OUT/app-comparisons.tsv"
    done

readelf -d "$TARGET" >"$OUT/app-local-dynamic-section.txt" 2>&1 || true
readelf -n "$TARGET" >"$OUT/app-local-notes.txt" 2>&1 || true
readelf -Ws "$TARGET" >"$OUT/app-local-dynamic-symbols.txt" 2>&1 || true

{
    strings -a "$TARGET" 2>/dev/null \
        | grep -E 'VK_LOADER_DEBUG|Vulkan Loader Version|\[Vulkan Loader\]|vkGetInstanceProcAddr|vkCreateInstance' \
        | sort -u \
        || true
} >"$OUT/app-local-loader-debug-strings.txt"

{
    readelf -Ws "$TARGET" 2>/dev/null \
        | grep -E 'vkGetInstanceProcAddr|vkCreateInstance|vkEnumerateInstanceExtensionProperties|vkEnumerateInstanceLayerProperties' \
        || true
} >"$OUT/app-local-loader-entrypoints.txt"

printf 'observer_signal_source\tline\n' >"$OUT/control-observer-signal-lines.tsv"
if [ -n "$CONTROL_OUT" ]; then
    for stream in stdout stderr; do
        log="$CONTROL_OUT/launch.$stream"
        [ -f "$log" ] || continue
        grep -nE 'Vulkan Loader Version|Found ICD manifest file|Searching for ICD drivers named|Insert instance layer|terminator_CreateInstance|linux_read_sorted_physical_devices|Original order:|Sorted order:|Copying old device|Removing driver|Using ".*" with driver:|llvmpipe|Turnip|Adreno|gfxstream|freedreno|libvulkan_lvp|libvulkan_gfxstream' "$log" \
            | while IFS= read -r line; do
                printf '%s\t%s\n' "$stream" "$line"
            done \
            || true
    done
fi

printf 'VS Code app-local Vulkan loader identity probe: PASS\n'
printf 'target: %s\n' "$TARGET"
printf 'output: %s\n' "$OUT"

printf '\n===== candidate identities =====\n'
cat "$OUT/candidate-identities.tsv"

printf '\n===== app comparisons =====\n'
cat "$OUT/app-comparisons.tsv"

printf '\n===== app-local loader debug strings =====\n'
cat "$OUT/app-local-loader-debug-strings.txt"

printf '\n===== app-local loader entrypoints =====\n'
cat "$OUT/app-local-loader-entrypoints.txt"

printf '\n===== control observer signal lines =====\n'
cat "$OUT/control-observer-signal-lines.tsv"
