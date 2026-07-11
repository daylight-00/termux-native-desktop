#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/promoted-vscode-gpu-identity-$(date +%Y%m%d-%H%M%S)}
ENV_PROBE_OUT="$OUT/environment"
CDP_PROBE_OUT="$OUT/probe"
LAUNCHER=${LAUNCHER:-$HOME/.local/bin/code}
APP=${APP:-$HOME/gl/apps/vscode}
EXPECTED_ICD=${EXPECTED_ICD:-$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json}

for command in git bash awk grep mkdir date readlink cat pgrep sleep tr sed; do
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

[ -r "$EXPECTED_ICD" ] || {
    printf 'managed glibc Freedreno manifest is not readable: %s\n' "$EXPECTED_ICD" >&2
    exit 1
}

if [ "${LIBGL_ALWAYS_SOFTWARE+x}" = x ]; then
    printf 'LIBGL_ALWAYS_SOFTWARE must be unset\n' >&2
    exit 2
fi

existing=$(pgrep -af "$APP/" || true)
if [ -n "$existing" ]; then
    printf 'existing VS Code processes detected; close them before the GPU gate:\n' >&2
    printf '%s\n' "$existing" >&2
    exit 1
fi

mkdir -p "$OUT"
branch=$(git -C "$REPO" branch --show-current)
head_sha=$(git -C "$REPO" rev-parse HEAD)
printf '%s\n' "$branch" >"$OUT/branch.txt"
printf '%s\n' "$head_sha" >"$OUT/head.txt"
printf '%s\n' "$LAUNCHER" >"$OUT/launcher-path.txt"
printf '%s\n' "$expected_launcher" >"$OUT/launcher-target.txt"
printf '%s\n' "$EXPECTED_ICD" >"$OUT/expected-icd.txt"

# Phase 1: prove the actual promoted launcher sanitizes deliberately injected
# bionic/session graphics policy, selects the exact glibc Freedreno provider,
# and does not carry a Zink/Gallium override into ANGLE processes.
VK_DRIVER_FILES=/bionic/freedreno.json \
VK_ICD_FILENAMES=/bionic/freedreno.json \
MESA_LOADER_DRIVER_OVERRIDE=llvmpipe \
GALLIUM_DRIVER=llvmpipe \
APP="$APP" \
LAUNCHER="$LAUNCHER" \
OUT="$ENV_PROBE_OUT" \
CONTROL_GL_GPU=1 \
VULKAN_POLICY_MODE=explicit-freedreno \
VK_LOADER_DEBUG_VALUE=all \
DURATION_SECONDS=${ENV_DURATION_SECONDS:-15} \
POLL_SLEEP_SECONDS=${POLL_SLEEP_SECONDS:-0.1} \
bash "$SCRIPT_DIR/probe-vscode-policy-env-boundary.sh" \
    >"$OUT/environment-probe.log" 2>&1

# The environment probe owns its launch tree and cleans it on exit. Refuse to
# start the CDP phase if cleanup did not complete; never merge two app trees.
for ((attempt = 0; attempt < 50; attempt++)); do
    existing=$(pgrep -af "$APP/" || true)
    [ -z "$existing" ] && break
    sleep 0.1
done
existing=$(pgrep -af "$APP/" || true)
if [ -n "$existing" ]; then
    printf 'VS Code processes remained after environment probe cleanup:\n' >&2
    printf '%s\n' "$existing" >&2
    printf 'FAIL\n' >"$OUT/validation.status"
    exit 1
fi

# Phase 2: independently prove Chromium's selected primary provider/device and
# correlate that identity with mapped provider and KGSL paths.
APP="$APP" \
LAUNCHER="$LAUNCHER" \
OUT="$CDP_PROBE_OUT" \
CONTROL_GL_GPU=1 \
VULKAN_POLICY_MODE=explicit-freedreno \
DURATION_SECONDS=${DURATION_SECONDS:-30} \
POLL_SLEEP_SECONDS=${POLL_SLEEP_SECONDS:-0.1} \
bash "$SCRIPT_DIR/probe-vscode-cdp-gpu-identity.sh" \
    >"$OUT/probe.log" 2>&1

CONTROL_OUT="$CDP_PROBE_OUT" OUT="$CDP_PROBE_OUT" \
    bash "$SCRIPT_DIR/classify-vscode-cdp-gpu-identity.sh" \
    >"$OUT/classifier.log" 2>&1

identity_summary="$CDP_PROBE_OUT/cdp-gpu-identity-summary.tsv"
environment_selected="$ENV_PROBE_OUT/process-environment-selected.tsv"
environment_summary="$ENV_PROBE_OUT/process-environment-summary.tsv"
processes="$ENV_PROBE_OUT/processes.tsv"

classification=$(awk -F $'\t' '$1 == "classification" { print $2; exit }' "$identity_summary")
provider=$(awk -F $'\t' '$1 == "selected_provider" { print $2; exit }' "$identity_summary")
device=$(awk -F $'\t' '$1 == "selected_device_family" { print $2; exit }' "$identity_summary")
provider_path=$(awk -F $'\t' '$1 == "provider_path_relation" { print $2; exit }' "$identity_summary")
device_node=$(awk -F $'\t' '$1 == "device_node_relation" { print $2; exit }' "$identity_summary")
display_type=$(awk -F $'\t' '$1 == "display_type" { print $2; exit }' "$identity_summary")
skia_backend=$(awk -F $'\t' '$1 == "skia_backend" { print $2; exit }' "$identity_summary")
vulkan_status=$(awk -F $'\t' '$1 == "vulkan_feature_status" { print $2; exit }' "$identity_summary")
renderer=$(awk -F $'\t' '$1 == "gl_renderer" { print $2; exit }' "$identity_summary")

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

record_boolean_gate() {
    local gate=$1
    shift
    if "$@"; then
        printf '%s\tPASS\n' "$gate" >>"$OUT/gates.tsv"
    else
        printf '%s\tFAIL\n' "$gate" >>"$OUT/gates.tsv"
        failures=$((failures + 1))
    fi
}

has_exact_environment_value() {
    local class=$1 key=$2 expected=$3
    awk -F $'\t' -v c="$class" -v k="$key" -v e="$expected" \
        'NR > 1 && $3 == c && $4 == k && $5 == e { found=1 }
         END { exit found ? 0 : 1 }' \
        "$environment_selected"
}

all_environment_values_equal() {
    local key=$1 expected=$2
    awk -F $'\t' -v k="$key" -v e="$expected" \
        'NR > 1 && $4 == k { seen=1; if ($5 != e) bad=1 }
         END { exit seen && !bad ? 0 : 1 }' \
        "$environment_selected"
}

key_absent() {
    local key=$1
    ! awk -F $'\t' -v k="$key" \
        'NR > 1 && $4 == k { found=1 } END { exit found ? 0 : 1 }' \
        "$environment_selected"
}

required_environment_readable() {
    local class=$1
    awk -F $'\t' -v c="$class" \
        'NR > 1 && $3 == c && $4 == "READ_OK" { found=1 }
         END { exit found ? 0 : 1 }' \
        "$environment_summary"
}

for required_class in main zygote gpu; do
    record_boolean_gate "${required_class}_environment_readable" \
        required_environment_readable "$required_class"
    record_boolean_gate "${required_class}_gl_gpu_one" \
        has_exact_environment_value "$required_class" GL_GPU 1
    record_boolean_gate "${required_class}_vk_driver_files_exact" \
        has_exact_environment_value "$required_class" VK_DRIVER_FILES "$EXPECTED_ICD"
    record_boolean_gate "${required_class}_vk_icd_filenames_exact" \
        has_exact_environment_value "$required_class" VK_ICD_FILENAMES "$EXPECTED_ICD"
done

record_boolean_gate all_gl_gpu_values_one \
    all_environment_values_equal GL_GPU 1
record_boolean_gate all_vk_driver_files_exact \
    all_environment_values_equal VK_DRIVER_FILES "$EXPECTED_ICD"
record_boolean_gate all_vk_icd_filenames_exact \
    all_environment_values_equal VK_ICD_FILENAMES "$EXPECTED_ICD"
record_boolean_gate mesa_loader_override_absent \
    key_absent MESA_LOADER_DRIVER_OVERRIDE
record_boolean_gate gallium_driver_absent \
    key_absent GALLIUM_DRIVER
record_boolean_gate libgl_always_software_absent \
    key_absent LIBGL_ALWAYS_SOFTWARE
record_boolean_gate ld_library_path_absent \
    key_absent LD_LIBRARY_PATH

if awk -F $'\t' 'NR > 1 && $4 == "LD_PRELOAD" && $5 != "" { bad=1 }
    END { exit bad ? 0 : 1 }' "$environment_selected"; then
    printf 'ld_preload_nonempty_absent\tFAIL\n' >>"$OUT/gates.tsv"
    failures=$((failures + 1))
else
    printf 'ld_preload_nonempty_absent\tPASS\n' >>"$OUT/gates.tsv"
fi

if grep -F '/bionic/' "$environment_selected" >/dev/null; then
    printf 'injected_bionic_paths_absent\tFAIL\n' >>"$OUT/gates.tsv"
    failures=$((failures + 1))
else
    printf 'injected_bionic_paths_absent\tPASS\n' >>"$OUT/gates.tsv"
fi

main_cmdlines="$OUT/main-cmdlines.txt"
awk -F $'\t' 'NR > 1 && $4 == "main" { print $6 }' "$processes" >"$main_cmdlines"

for flag in \
    --disable-gpu-sandbox \
    --ignore-gpu-blocklist \
    --enable-features=Vulkan \
    --use-gl=angle \
    --use-angle=vulkan \
    --disable-gpu-vsync
do
    gate=$(printf '%s' "$flag" | sed 's/^--//; s/[^A-Za-z0-9]/_/g')
    if grep -Eq "(^|[[:space:]])${flag//+/\\+}([[:space:]]|$)" "$main_cmdlines"; then
        printf 'main_has_%s\tPASS\n' "$gate" >>"$OUT/gates.tsv"
    else
        printf 'main_has_%s\tFAIL\n' "$gate" >>"$OUT/gates.tsv"
        failures=$((failures + 1))
    fi
done

if grep -Eq '(^|[[:space:]])--disable-gpu([[:space:]]|$)' "$main_cmdlines"; then
    printf 'main_exact_disable_gpu_absent\tFAIL\n' >>"$OUT/gates.tsv"
    failures=$((failures + 1))
else
    printf 'main_exact_disable_gpu_absent\tPASS\n' >>"$OUT/gates.tsv"
fi

record_gate environment_probe_status \
    "$(tr -d '\r\n' <"$ENV_PROBE_OUT/probe.status")" PASS
record_gate cdp_probe_status \
    "$(tr -d '\r\n' <"$CDP_PROBE_OUT/probe.status")" PASS
record_gate identity_status \
    "$(tr -d '\r\n' <"$CDP_PROBE_OUT/cdp-gpu-identity.status")" PASS
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
    printf 'expected_icd\t%s\n' "$EXPECTED_ICD"
    printf 'classification\t%s\n' "$classification"
    printf 'selected_provider\t%s\n' "$provider"
    printf 'selected_device_family\t%s\n' "$device"
    printf 'renderer\t%s\n' "$renderer"
    printf 'environment_probe\t%s\n' "$ENV_PROBE_OUT"
    printf 'cdp_probe\t%s\n' "$CDP_PROBE_OUT"
    printf 'gate_failures\t%s\n' "$failures"
} >"$OUT/summary.tsv"

if [ "$failures" -ne 0 ]; then
    printf 'FAIL\n' >"$OUT/validation.status"
    printf 'promoted VS Code GPU environment/identity validation: FAIL (%s gates)\n' "$failures" >&2
    printf 'evidence: %s\n' "$OUT" >&2
    cat "$OUT/summary.tsv" >&2
    exit 1
fi

printf 'PASS\n' >"$OUT/validation.status"
printf 'promoted VS Code GPU environment/identity validation: PASS\n'
printf 'evidence: %s\n' "$OUT"
printf '\n===== summary =====\n'
cat "$OUT/summary.tsv"
printf '\n===== gates =====\n'
cat "$OUT/gates.tsv"
printf '\n===== selected process environment =====\n'
cat "$environment_selected"
printf '\n===== environment process identities =====\n'
cat "$processes"
printf '\n===== GPU devices =====\n'
cat "$CDP_PROBE_OUT/gpu-devices.tsv"
printf '\n===== GPU graphics paths =====\n'
cat "$CDP_PROBE_OUT/gpu-graphics-paths.tsv"
