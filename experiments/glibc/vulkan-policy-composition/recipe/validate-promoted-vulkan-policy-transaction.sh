#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/promoted-vulkan-policy-predeploy-$(date +%Y%m%d-%H%M%S)}

for command in git bash grep awk mkdir date readlink stat; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

tracked_dirty=$(git -C "$REPO" status --porcelain --untracked-files=no)
if [ -n "$tracked_dirty" ]; then
    printf 'tracked working-tree changes detected; pre-deploy gate requires exact HEAD:\n' >&2
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

run_gate() {
    local gate=$1 log=$2
    shift 2
    if "$@" >"$OUT/$log" 2>&1; then
        record_gate "$gate" PASS
    else
        record_gate "$gate" FAIL
        printf 'gate failed: %s\n' "$gate" >&2
        cat "$OUT/$log" >&2
    fi
}

run_gate shell_syntax shell-syntax.log \
    bash -n \
    "$REPO/modules/gl/overlay/home/gl/env" \
    "$REPO/modules/gl/overlay/home/gl/policy/vulkan/freedreno.sh" \
    "$REPO/modules/gl/overlay/home/gl/bin/gl-run" \
    "$REPO/packages/vscode/launcher/code" \
    "$REPO/packages/obsidian/launcher/obsidian" \
    "$REPO/packages/obsidian/launcher/obsidian-app" \
    "$REPO/tests/repository/vulkan-policy-scope-smoke.sh" \
    "$REPO/tests/repository/deploy-smoke.sh" \
    "$REPO/experiments/glibc/vulkan-policy-composition/recipe/validate-live-vulkan-policy-installation.sh" \
    "$REPO/experiments/glibc/vulkan-policy-composition/recipe/validate-promoted-gl-run-renderer.sh" \
    "$REPO/experiments/glibc/vulkan-policy-composition/recipe/probe-vscode-policy-env-boundary.sh" \
    "$REPO/experiments/glibc/vulkan-policy-composition/recipe/probe-vscode-cdp-gpu-identity.sh" \
    "$REPO/experiments/glibc/vulkan-policy-composition/recipe/classify-vscode-cdp-gpu-identity.sh" \
    "$REPO/experiments/glibc/vulkan-policy-composition/recipe/validate-promoted-vscode-gpu-identity.sh" \
    "$REPO/experiments/glibc/vulkan-policy-composition/recipe/validate-promoted-vscode-cpu-policy.sh" \
    "$REPO/experiments/glibc/vulkan-policy-composition/recipe/probe-electron-cdp-gpu-identity.sh" \
    "$REPO/experiments/glibc/vulkan-policy-composition/recipe/classify-cdp-gpu-identity.sh" \
    "$REPO/experiments/glibc/vulkan-policy-composition/recipe/validate-promoted-obsidian-gpu-identity.sh"

run_gate policy_scope_smoke policy-scope-smoke.log \
    bash "$REPO/tests/repository/vulkan-policy-scope-smoke.sh"

run_gate deploy_smoke deploy-smoke.log \
    bash "$REPO/tests/repository/deploy-smoke.sh"

run_gate live_deploy_dry_run live-deploy-dry-run.log \
    bash "$REPO/tools/deploy" --dry-run

check_contains() {
    local gate=$1 file=$2 pattern=$3
    if grep -Eq -- "$pattern" "$file"; then
        record_gate "$gate" PASS
    else
        record_gate "$gate" FAIL
        printf 'missing pattern for %s: %s\n' "$gate" "$pattern" >&2
    fi
}

check_absent() {
    local gate=$1 file=$2 pattern=$3
    if grep -Eq -- "$pattern" "$file"; then
        record_gate "$gate" FAIL
        printf 'unexpected pattern for %s: %s\n' "$gate" "$pattern" >&2
    else
        record_gate "$gate" PASS
    fi
}

ENV_FILE="$REPO/modules/gl/overlay/home/gl/env"
PROFILE_FILE="$REPO/modules/gl/overlay/home/gl/policy/vulkan/freedreno.sh"
GL_RUN_FILE="$REPO/modules/gl/overlay/home/gl/bin/gl-run"
VSCODE_FILE="$REPO/packages/vscode/launcher/code"
OBSIDIAN_APP_FILE="$REPO/packages/obsidian/launcher/obsidian-app"

check_contains baseline_clears_vk_driver_files "$ENV_FILE" \
    'unset[[:space:]]+VK_ICD_FILENAMES[[:space:]]+VK_DRIVER_FILES'
check_contains baseline_clears_bionic_opengl_bridge "$ENV_FILE" \
    'unset[[:space:]]+MESA_LOADER_DRIVER_OVERRIDE[[:space:]]+GALLIUM_DRIVER'
check_absent baseline_does_not_export_vk_driver_files "$ENV_FILE" \
    'export[[:space:]]+VK_DRIVER_FILES='
check_absent baseline_does_not_export_vk_icd_filenames "$ENV_FILE" \
    'export[[:space:]]+VK_ICD_FILENAMES='
check_absent baseline_does_not_export_mesa_loader_override "$ENV_FILE" \
    'export[[:space:]]+MESA_LOADER_DRIVER_OVERRIDE='
check_absent baseline_does_not_export_gallium_driver "$ENV_FILE" \
    'export[[:space:]]+GALLIUM_DRIVER='

check_contains profile_exports_vk_driver_files "$PROFILE_FILE" \
    'export[[:space:]]+VK_DRIVER_FILES='
check_contains profile_exports_vk_icd_filenames "$PROFILE_FILE" \
    'export[[:space:]]+VK_ICD_FILENAMES='

check_contains gl_run_sources_profile "$GL_RUN_FILE" \
    'policy/vulkan/freedreno\.sh'
check_contains gl_run_adds_zink_explicitly "$GL_RUN_FILE" \
    'MESA_LOADER_DRIVER_OVERRIDE=zink'
check_contains vscode_sources_profile "$VSCODE_FILE" \
    'policy/vulkan/freedreno\.sh'
check_contains obsidian_app_sources_profile "$OBSIDIAN_APP_FILE" \
    'policy/vulkan/freedreno\.sh'

check_contains dry_run_plans_profile "$OUT/live-deploy-dry-run.log" \
    'gl/policy/vulkan/freedreno\.sh'
check_contains dry_run_plans_gl_env "$OUT/live-deploy-dry-run.log" \
    'gl/env'
check_contains dry_run_plans_vscode "$OUT/live-deploy-dry-run.log" \
    '\.local/bin/code'
check_contains dry_run_plans_obsidian_app "$OUT/live-deploy-dry-run.log" \
    'gl/bin/obsidian-app'

printf 'path\tstate\ttarget\n' >"$OUT/current-live-targets.tsv"
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
            >>"$OUT/current-live-targets.tsv"
    elif [ -e "$path" ]; then
        printf '%s\tNON_SYMLINK\t-\n' "$path" \
            >>"$OUT/current-live-targets.tsv"
    else
        printf '%s\tABSENT\t-\n' "$path" \
            >>"$OUT/current-live-targets.tsv"
    fi
done

{
    printf 'metric\tvalue\n'
    printf 'repository_root\t%s\n' "$REPO"
    printf 'branch\t%s\n' "$branch"
    printf 'head\t%s\n' "$head_sha"
    printf 'gate_failures\t%s\n' "$failures"
} >"$OUT/summary.tsv"

if [ "$failures" -ne 0 ]; then
    printf 'FAIL\n' >"$OUT/predeploy.status"
    printf 'promoted graphics policy pre-deploy gate: FAIL (%s gates)\n' \
        "$failures" >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
fi

printf 'PASS\n' >"$OUT/predeploy.status"
printf 'promoted graphics policy pre-deploy gate: PASS\n'
printf 'repository: %s\n' "$REPO"
printf 'branch: %s\n' "$branch"
printf 'head: %s\n' "$head_sha"
printf 'evidence: %s\n' "$OUT"
printf '\nNo live deployment was performed.\n'

printf '\n===== summary =====\n'
cat "$OUT/summary.tsv"
printf '\n===== gates =====\n'
cat "$OUT/gates.tsv"
printf '\n===== current live targets =====\n'
cat "$OUT/current-live-targets.tsv"
