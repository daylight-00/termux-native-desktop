#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

PROBE=${PROBE:-$PREFIX/tmp/tnd-vulkan-policy-composition/glx-renderer-probe}
ROOTFS=${ROOTFS:-$PREFIX/var/lib/proot-distro/containers/debian/rootfs}
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/driver-isolation-matrix-$(date +%Y%m%d-%H%M%S)}
LOADER_DEBUG=${VK_LOADER_DEBUG:-error,warn,info,driver}

PROVIDER_STORE_FREEDRENO=${PROVIDER_STORE_FREEDRENO:-$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json}
ROOTFS_LVP=${ROOTFS_LVP:-$ROOTFS/usr/share/vulkan/icd.d/lvp_icd.json}
ROOTFS_FREEDRENO=${ROOTFS_FREEDRENO:-$ROOTFS/usr/share/vulkan/icd.d/freedreno_icd.json}

[ -x "$PROBE" ] || {
    printf 'missing probe binary: %s\n' "$PROBE" >&2
    exit 1
}

for manifest in \
    "$PROVIDER_STORE_FREEDRENO" \
    "$ROOTFS_LVP" \
    "$ROOTFS_FREEDRENO"
do
    [ -r "$manifest" ] || {
        printf 'missing or unreadable manifest: %s\n' "$manifest" >&2
        exit 1
    }
done

mkdir -p "$OUT"
printf 'case\tmanifest\texit_status\trenderer_gate\n' >"$OUT/summary.tsv"

run_case() {
    local label=$1
    local manifest=$2
    local case_dir="$OUT/$label"
    local status renderer_gate

    mkdir -p "$case_dir"

    set +e
    CASE_MANIFEST="$manifest" \
    PROBE="$PROBE" \
    LOADER_DEBUG="$LOADER_DEBUG" \
    bash -c '
        set -euo pipefail

        source "$HOME/gl/env"

        unset VK_DRIVER_FILES VK_ICD_FILENAMES
        export VK_DRIVER_FILES="$CASE_MANIFEST"
        export VK_ICD_FILENAMES="$CASE_MANIFEST"
        export VK_LOADER_DEBUG="$LOADER_DEBUG"

        printf "isolated driver manifest: %s\n" "$CASE_MANIFEST" >&2
        printf "VK_DRIVER_FILES=%s\n" "$VK_DRIVER_FILES" >&2

        exec env LD_PRELOAD= MESA_LOADER_DRIVER_OVERRIDE=zink "$PROBE"
    ' >"$case_dir/probe.stdout" 2>"$case_dir/probe.stderr"
    status=$?
    set -e

    printf '%s\n' "$status" >"$case_dir/exit-status"

    if grep -q '^GL_RENDERER=' "$case_dir/probe.stdout"; then
        renderer_gate=PASS
    else
        renderer_gate=NOT_REACHED
    fi

    awk '/Vulkan Loader/ || /Found ICD manifest/ || /Searching for ICD drivers named/ || /physical_devices/ || /Original order:/ || /Sorted order:/ || /Removing driver/ || /failed to choose pdev/ || /failed to create drisw screen/ || /failed to load driver/ || /^GL_RENDERER=/ { print }' \
        "$case_dir/probe.stderr" "$case_dir/probe.stdout" \
        >"$case_dir/selection-summary.txt"

    printf '%s\t%s\t%s\t%s\n' \
        "$label" "$manifest" "$status" "$renderer_gate" \
        >>"$OUT/summary.tsv"
}

run_case provider-store-freedreno "$PROVIDER_STORE_FREEDRENO"
run_case rootfs-lvp "$ROOTFS_LVP"
run_case rootfs-freedreno "$ROOTFS_FREEDRENO"

printf 'isolated Vulkan driver matrix: PASS\n'
printf 'output: %s\n' "$OUT"

printf '\n===== summary =====\n'
cat "$OUT/summary.tsv"

for label in provider-store-freedreno rootfs-lvp rootfs-freedreno; do
    printf '\n===== %s stdout =====\n' "$label"
    cat "$OUT/$label/probe.stdout"

    printf '\n===== %s selection summary =====\n' "$label"
    cat "$OUT/$label/selection-summary.txt"
done
