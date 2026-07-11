#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/promoted-vscode-gpu-identity-$(date +%Y%m%d-%H%M%S)}
PROBE_OUT="$OUT/probe"
LAUNCHER=${LAUNCHER:-$HOME/.local/bin/code}
APP=${APP:-$HOME/gl/apps/vscode}

for command in git bash awk grep mkdir date readlink cat; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

tracked_dirty=$(git -C "$REPO" status --porcelain --untracked-files=no)
if [ -n "$tracked_dirty" ]; then
    printf 'tracked working-tree changes detected; GPU identity gate requires exact HEAD:\n' >&2
    printf '%s\n' "$tracked_dirty" >&2
    exit 2
fi

[ -x "$LAUNCHER" ] || {
    printf 'missing promoted VS Code launcher: %s\n' "$LAUNCHER" >&2
    exit 1
}

expected_launcher="$REPO/packages/vscode/launcher/code"
if [ ! -L "$LAUNCHER" ] || [ "$(readlink "$LAUNCHER")" != "$expected_launcher" ]; then
    printf 'promoted launcher target mismatch: %s\n' "$LAUNCHER" >&2
    printf 'expected: %s\n' "$expected_launcher" >&2
    printf 'observed: %s\n' "$(readlink "$LAUNCHER" 2>/dev/null || printf '<not-symlink>')" >&2
    exit 1
fi

if [ "${LIBGL_ALWAYS_SOFTWARE+x}" = x ]; then
    printf 'LIBGL_ALWAYS_SOFTWARE must be unset\n' >&2
    exit 2
fi

mkdir -p "$OUT"
branch=$(git -C "$REPO" branch --show-current)
head_sha=$(git -C "$REPO" rev-parse HEAD)
printf '%s\n' "$branch" >"$OUT/branch.txt"
printf '%s\n' "$head_sha" >"$OUT/head.txt"
printf '%s\n' "$LAUNCHER" >"$OUT/launcher-path.txt"
printf '%s\n' "$expected_launcher" >"$OUT/launcher-target.txt"

APP="$APP" \
LAUNCHER="$LAUNCHER" \
OUT="$PROBE_OUT" \
CONTROL_GL_GPU=1 \
VULKAN_POLICY_MODE=explicit-freedreno \
DURATION_SECONDS=${DURATION_SECONDS:-30} \
POLL_SLEEP_SECONDS=${POLL_SLEEP_SECONDS:-0.1} \
bash "$SCRIPT_DIR/probe-vscode-cdp-gpu-identity.sh" \
    >"$OUT/probe.log" 2>&1

CONTROL_OUT="$PROBE_OUT" OUT="$PROBE_OUT" \
    bash "$SCRIPT_DIR/classify-vscode-cdp-gpu-identity.sh" \
    >"$OUT/classifier.log" 2>&1

summary="$PROBE_OUT/cdp-gpu-identity-summary.tsv"
classification=$(awk -F $'\t' '$1 == "classification" { print $2; exit }' "$summary")
provider=$(awk -F $'\t' '$1 == "selected_provider" { print $2; exit }' "$summary")
device=$(awk -F $'\t' '$1 == "selected_device_family" { print $2; exit }' "$summary")
provider_path=$(awk -F $'\t' '$1 == "provider_path_relation" { print $2; exit }' "$summary")
device_node=$(awk -F $'\t' '$1 == "device_node_relation" { print $2; exit }' "$summary")
display_type=$(awk -F $'\t' '$1 == "display_type" { print $2; exit }' "$summary")
skia_backend=$(awk -F $'\t' '$1 == "skia_backend" { print $2; exit }' "$summary")
vulkan_status=$(awk -F $'\t' '$1 == "vulkan_feature_status" { print $2; exit }' "$summary")
renderer=$(awk -F $'\t' '$1 == "gl_renderer" { print $2; exit }' "$summary")

printf 'gate\tstate\n' >"$OUT/gates.tsv"
failures=0

record_gate() {
    local gate=$1 observed=$2 expected=$3
    if [ "$observed" = "$expected" ]; then
        printf '%s\tPASS\n' "$gate" >>"$OUT/gates.tsv"
    else
        printf '%s\tFAIL\n' "$gate" >>"$OUT/gates.tsv"
        printf '%s expected=%s observed=%s\n' "$gate" "$expected" "$observed" >&2
        failures=$((failures + 1))
    fi
}

record_gate probe_status "$(tr -d '\r\n' <"$PROBE_OUT/probe.status")" PASS
record_gate identity_status "$(tr -d '\r\n' <"$PROBE_OUT/cdp-gpu-identity.status")" PASS
record_gate classification "$classification" FREEDRENO_TURNIP
record_gate selected_provider "$provider" FREEDRENO_TURNIP
record_gate selected_device_family "$device" Adreno
record_gate provider_path_relation "$provider_path" PRESENT
record_gate device_node_relation "$device_node" PRESENT
record_gate display_type "$display_type" ANGLE_VULKAN
record_gate skia_backend "$skia_backend" GaneshVulkan
record_gate vulkan_feature_status "$vulkan_status" enabled_on

if printf '%s\n' "$renderer" | grep -Eiq 'Turnip.*Adreno|Adreno.*Turnip'; then
    printf 'renderer_identity\tPASS\n' >>"$OUT/gates.tsv"
else
    printf 'renderer_identity\tFAIL\n' >>"$OUT/gates.tsv"
    failures=$((failures + 1))
fi

{
    printf 'field\tvalue\n'
    printf 'branch\t%s\n' "$branch"
    printf 'head\t%s\n' "$head_sha"
    printf 'launcher\t%s\n' "$LAUNCHER"
    printf 'launcher_target\t%s\n' "$expected_launcher"
    printf 'classification\t%s\n' "$classification"
    printf 'selected_provider\t%s\n' "$provider"
    printf 'selected_device_family\t%s\n' "$device"
    printf 'renderer\t%s\n' "$renderer"
    printf 'gate_failures\t%s\n' "$failures"
} >"$OUT/summary.tsv"

if [ "$failures" -ne 0 ]; then
    printf 'FAIL\n' >"$OUT/validation.status"
    printf 'promoted VS Code GPU identity validation: FAIL (%s gates)\n' "$failures" >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
fi

printf 'PASS\n' >"$OUT/validation.status"
printf 'promoted VS Code GPU identity validation: PASS\n'
printf 'evidence: %s\n' "$OUT"
printf '\n===== summary =====\n'
cat "$OUT/summary.tsv"
printf '\n===== gates =====\n'
cat "$OUT/gates.tsv"
printf '\n===== GPU devices =====\n'
cat "$PROBE_OUT/gpu-devices.tsv"
printf '\n===== GPU graphics paths =====\n'
cat "$PROBE_OUT/gpu-graphics-paths.tsv"
