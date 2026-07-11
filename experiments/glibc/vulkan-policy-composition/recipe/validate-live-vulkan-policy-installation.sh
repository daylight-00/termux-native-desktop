#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/live-vulkan-policy-installation-$(date +%Y%m%d-%H%M%S)}

for command in git bash grep awk mkdir date readlink cat; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

tracked_dirty=$(git -C "$REPO" status --porcelain --untracked-files=no)
if [ -n "$tracked_dirty" ]; then
    printf 'tracked working-tree changes detected; live receipt requires exact HEAD:\n' >&2
    printf '%s\n' "$tracked_dirty" >&2
    exit 2
fi

mkdir -p "$OUT"
branch=$(git -C "$REPO" branch --show-current)
head_sha=$(git -C "$REPO" rev-parse HEAD)
printf '%s\n' "$REPO" >"$OUT/repository-root.txt"
printf '%s\n' "$branch" >"$OUT/branch.txt"
printf '%s\n' "$head_sha" >"$OUT/head.txt"

printf 'gate\tstate\n' >"$OUT/gates.tsv"
failures=0

record_gate() {
    local gate=$1 state=$2
    printf '%s\t%s\n' "$gate" "$state" >>"$OUT/gates.tsv"
    if [ "$state" != PASS ]; then
        failures=$((failures + 1))
    fi
}

check_symlink_target() {
    local gate=$1 live=$2 expected=$3
    local observed

    if [ ! -L "$live" ]; then
        record_gate "$gate" FAIL
        printf '%s is not a symlink: %s\n' "$gate" "$live" >&2
        return
    fi

    observed=$(readlink "$live")
    if [ "$observed" = "$expected" ]; then
        record_gate "$gate" PASS
    else
        record_gate "$gate" FAIL
        printf '%s target mismatch: expected=%s observed=%s\n' \
            "$gate" "$expected" "$observed" >&2
    fi
}

check_symlink_target live_gl_env \
    "$HOME/gl/env" \
    "$REPO/modules/gl/overlay/home/gl/env"
check_symlink_target live_freedreno_profile \
    "$HOME/gl/policy/vulkan/freedreno.sh" \
    "$REPO/modules/gl/overlay/home/gl/policy/vulkan/freedreno.sh"
check_symlink_target live_gl_run \
    "$HOME/gl/bin/gl-run" \
    "$REPO/modules/gl/overlay/home/gl/bin/gl-run"
check_symlink_target live_vscode_launcher \
    "$HOME/.local/bin/code" \
    "$REPO/packages/vscode/launcher/code"
check_symlink_target live_obsidian_cli \
    "$HOME/gl/bin/obsidian" \
    "$REPO/packages/obsidian/launcher/obsidian"
check_symlink_target live_obsidian_gui \
    "$HOME/gl/bin/obsidian-app" \
    "$REPO/packages/obsidian/launcher/obsidian-app"

EXPECTED_ICD="$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json"
if [ -r "$EXPECTED_ICD" ]; then
    record_gate freedreno_manifest_readable PASS
else
    record_gate freedreno_manifest_readable FAIL
    printf 'managed glibc Freedreno manifest is not readable: %s\n' "$EXPECTED_ICD" >&2
fi

BASELINE_RECEIPT="$OUT/baseline-environment.tsv"
env \
    HOME="$HOME" \
    PREFIX="$PREFIX" \
    VK_DRIVER_FILES=/bionic/freedreno.json \
    VK_ICD_FILENAMES=/bionic/freedreno.json \
    MESA_LOADER_DRIVER_OVERRIDE=zink \
    GALLIUM_DRIVER=llvmpipe \
    bash -c '
        set -u
        source "$HOME/gl/env"
        printf "field\tvalue\n"
        printf "VK_DRIVER_FILES\t%s\n" "${VK_DRIVER_FILES-<unset>}"
        printf "VK_ICD_FILENAMES\t%s\n" "${VK_ICD_FILENAMES-<unset>}"
        printf "MESA_LOADER_DRIVER_OVERRIDE\t%s\n" "${MESA_LOADER_DRIVER_OVERRIDE-<unset>}"
        printf "GALLIUM_DRIVER\t%s\n" "${GALLIUM_DRIVER-<unset>}"
    ' >"$BASELINE_RECEIPT"

baseline_driver=$(awk -F $'\t' '$1 == "VK_DRIVER_FILES" { print $2; exit }' "$BASELINE_RECEIPT")
baseline_icd=$(awk -F $'\t' '$1 == "VK_ICD_FILENAMES" { print $2; exit }' "$BASELINE_RECEIPT")
baseline_mesa=$(awk -F $'\t' '$1 == "MESA_LOADER_DRIVER_OVERRIDE" { print $2; exit }' "$BASELINE_RECEIPT")
baseline_gallium=$(awk -F $'\t' '$1 == "GALLIUM_DRIVER" { print $2; exit }' "$BASELINE_RECEIPT")

[ "$baseline_driver" = '<unset>' ] && \
    record_gate baseline_vk_driver_files_absent PASS || \
    record_gate baseline_vk_driver_files_absent FAIL
[ "$baseline_icd" = '<unset>' ] && \
    record_gate baseline_vk_icd_filenames_absent PASS || \
    record_gate baseline_vk_icd_filenames_absent FAIL
[ "$baseline_mesa" = '<unset>' ] && \
    record_gate baseline_mesa_loader_override_absent PASS || \
    record_gate baseline_mesa_loader_override_absent FAIL
[ "$baseline_gallium" = '<unset>' ] && \
    record_gate baseline_gallium_driver_absent PASS || \
    record_gate baseline_gallium_driver_absent FAIL

PROFILE_RECEIPT="$OUT/freedreno-profile-environment.tsv"
env \
    HOME="$HOME" \
    PREFIX="$PREFIX" \
    VK_DRIVER_FILES=/bionic/freedreno.json \
    VK_ICD_FILENAMES=/bionic/freedreno.json \
    MESA_LOADER_DRIVER_OVERRIDE=zink \
    GALLIUM_DRIVER=llvmpipe \
    bash -c '
        set -u
        source "$HOME/gl/env"
        source "$HOME/gl/policy/vulkan/freedreno.sh"
        printf "field\tvalue\n"
        printf "VK_DRIVER_FILES\t%s\n" "${VK_DRIVER_FILES-<unset>}"
        printf "VK_ICD_FILENAMES\t%s\n" "${VK_ICD_FILENAMES-<unset>}"
        printf "MESA_LOADER_DRIVER_OVERRIDE\t%s\n" "${MESA_LOADER_DRIVER_OVERRIDE-<unset>}"
        printf "GALLIUM_DRIVER\t%s\n" "${GALLIUM_DRIVER-<unset>}"
        printf "profile_internal\t%s\n" "${_TND_GLIBC_FREEDRENO_ICD-<unset>}"
    ' >"$PROFILE_RECEIPT"

profile_driver=$(awk -F $'\t' '$1 == "VK_DRIVER_FILES" { print $2; exit }' "$PROFILE_RECEIPT")
profile_icd=$(awk -F $'\t' '$1 == "VK_ICD_FILENAMES" { print $2; exit }' "$PROFILE_RECEIPT")
profile_mesa=$(awk -F $'\t' '$1 == "MESA_LOADER_DRIVER_OVERRIDE" { print $2; exit }' "$PROFILE_RECEIPT")
profile_gallium=$(awk -F $'\t' '$1 == "GALLIUM_DRIVER" { print $2; exit }' "$PROFILE_RECEIPT")
profile_internal=$(awk -F $'\t' '$1 == "profile_internal" { print $2; exit }' "$PROFILE_RECEIPT")

[ "$profile_driver" = "$EXPECTED_ICD" ] && \
    record_gate profile_vk_driver_files_exact PASS || \
    record_gate profile_vk_driver_files_exact FAIL
[ "$profile_icd" = "$EXPECTED_ICD" ] && \
    record_gate profile_vk_icd_filenames_exact PASS || \
    record_gate profile_vk_icd_filenames_exact FAIL
[ "$profile_driver" = "$profile_icd" ] && \
    record_gate profile_loader_variable_pair_equal PASS || \
    record_gate profile_loader_variable_pair_equal FAIL
[ "$profile_mesa" = '<unset>' ] && \
    record_gate profile_mesa_loader_override_absent PASS || \
    record_gate profile_mesa_loader_override_absent FAIL
[ "$profile_gallium" = '<unset>' ] && \
    record_gate profile_gallium_driver_absent PASS || \
    record_gate profile_gallium_driver_absent FAIL
[ "$profile_internal" = '<unset>' ] && \
    record_gate profile_internal_variable_private PASS || \
    record_gate profile_internal_variable_private FAIL

printf 'path\tstate\ttarget\n' >"$OUT/live-targets.tsv"
for path in \
    "$HOME/gl/env" \
    "$HOME/gl/policy/vulkan/freedreno.sh" \
    "$HOME/gl/bin/gl-run" \
    "$HOME/.local/bin/code" \
    "$HOME/gl/bin/obsidian" \
    "$HOME/gl/bin/obsidian-app"
do
    if [ -L "$path" ]; then
        printf '%s\tSYMLINK\t%s\n' "$path" "$(readlink "$path")" \
            >>"$OUT/live-targets.tsv"
    elif [ -e "$path" ]; then
        printf '%s\tNON_SYMLINK\t-\n' "$path" \
            >>"$OUT/live-targets.tsv"
    else
        printf '%s\tABSENT\t-\n' "$path" \
            >>"$OUT/live-targets.tsv"
    fi
done

{
    printf 'metric\tvalue\n'
    printf 'repository_root\t%s\n' "$REPO"
    printf 'branch\t%s\n' "$branch"
    printf 'head\t%s\n' "$head_sha"
    printf 'expected_icd\t%s\n' "$EXPECTED_ICD"
    printf 'gate_failures\t%s\n' "$failures"
} >"$OUT/summary.tsv"

if [ "$failures" -ne 0 ]; then
    printf 'FAIL\n' >"$OUT/installation.status"
    printf 'live graphics policy installation receipt: FAIL (%s gates)\n' \
        "$failures" >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
fi

printf 'PASS\n' >"$OUT/installation.status"
printf 'live graphics policy installation receipt: PASS\n'
printf 'repository: %s\n' "$REPO"
printf 'branch: %s\n' "$branch"
printf 'head: %s\n' "$head_sha"
printf 'evidence: %s\n' "$OUT"
printf '\nNo GUI or rendering workload was launched.\n'

printf '\n===== summary =====\n'
cat "$OUT/summary.tsv"
printf '\n===== gates =====\n'
cat "$OUT/gates.tsv"
printf '\n===== baseline environment =====\n'
cat "$OUT/baseline-environment.tsv"
printf '\n===== Freedreno profile environment =====\n'
cat "$OUT/freedreno-profile-environment.tsv"
printf '\n===== live targets =====\n'
cat "$OUT/live-targets.tsv"
