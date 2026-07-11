#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/promoted-obsidian-gpu-identity-$(date +%Y%m%d-%H%M%S)}
ENV_OUT="$OUT/environment"
CDP_OUT="$OUT/probe"
ENV_CONFIG_HOME="$ENV_OUT/config"
ENV_USER_DATA="$ENV_CONFIG_HOME/obsidian"
CDP_CONFIG_HOME="$CDP_OUT/config"
CDP_USER_DATA="$CDP_CONFIG_HOME/obsidian"
LAUNCHER=${LAUNCHER:-$HOME/gl/bin/obsidian-app}
APP=${APP:-$HOME/gl/apps/obsidian}
ENTRYPOINT=${ENTRYPOINT:-$APP/obsidian}
EXPECTED_ICD=${EXPECTED_ICD:-$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json}
ENV_DURATION_SECONDS=${ENV_DURATION_SECONDS:-20}
POLL_SLEEP_SECONDS=${POLL_SLEEP_SECONDS:-0.1}

for command in git bash awk grep mkdir date readlink pgrep sort tr sed sleep tail wc; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

tracked_dirty=$(git -C "$REPO" status --porcelain --untracked-files=no)
if [ -n "$tracked_dirty" ]; then
    printf 'tracked working-tree changes detected; Obsidian GPU gate requires exact HEAD:\n' >&2
    printf '%s\n' "$tracked_dirty" >&2
    exit 2
fi

case "$ENV_DURATION_SECONDS" in
    ''|*[!0-9]*|0)
        printf 'ENV_DURATION_SECONDS must be a positive integer: %s\n' "$ENV_DURATION_SECONDS" >&2
        exit 2
        ;;
esac

[ -x "$LAUNCHER" ] || {
    printf 'missing promoted Obsidian launcher: %s\n' "$LAUNCHER" >&2
    exit 1
}

expected_launcher="$REPO/packages/obsidian/launcher/obsidian-app"
if [ ! -L "$LAUNCHER" ] || [ "$(readlink "$LAUNCHER")" != "$expected_launcher" ]; then
    printf 'promoted Obsidian launcher target mismatch: %s\n' "$LAUNCHER" >&2
    printf 'expected: %s\n' "$expected_launcher" >&2
    printf 'observed: %s\n' "$(readlink "$LAUNCHER" 2>/dev/null || printf '<not-symlink>')" >&2
    exit 1
fi

[ -x "$ENTRYPOINT" ] || {
    printf 'missing Obsidian entrypoint: %s\n' "$ENTRYPOINT" >&2
    exit 1
}

[ -r "$EXPECTED_ICD" ] || {
    printf 'managed glibc Freedreno manifest is not readable: %s\n' "$EXPECTED_ICD" >&2
    exit 1
}

if [ "${LIBGL_ALWAYS_SOFTWARE+x}" = x ]; then
    printf 'LIBGL_ALWAYS_SOFTWARE must be unset before the Obsidian GPU gate\n' >&2
    exit 2
fi

existing=$(pgrep -af "$APP/|$ENV_USER_DATA|$CDP_USER_DATA" || true)
if [ -n "$existing" ]; then
    printf 'existing Obsidian processes detected; close them before the GPU gate:\n' >&2
    printf '%s\n' "$existing" >&2
    exit 1
fi

mkdir -p "$ENV_USER_DATA" "$CDP_USER_DATA"
branch=$(git -C "$REPO" branch --show-current)
head_sha=$(git -C "$REPO" rev-parse HEAD)
printf '%s\n' "$branch" >"$OUT/branch.txt"
printf '%s\n' "$head_sha" >"$OUT/head.txt"
printf '%s\n' "$LAUNCHER" >"$OUT/launcher-path.txt"
printf '%s\n' "$expected_launcher" >"$OUT/launcher-target.txt"
printf '%s\n' "$EXPECTED_ICD" >"$OUT/expected-icd.txt"
printf '%s\n' "$ENV_CONFIG_HOME" >"$OUT/environment-config-home.txt"
printf '%s\n' "$ENV_USER_DATA" >"$OUT/environment-user-data.txt"
printf '%s\n' "$CDP_CONFIG_HOME" >"$OUT/cdp-config-home.txt"
printf '%s\n' "$CDP_USER_DATA" >"$OUT/cdp-user-data.txt"

printf 'timestamp\tpid\tppid\tclass\targv0\tcmdline\n' >"$ENV_OUT/processes.tsv"
printf 'timestamp\tpid\tclass\tstate\tentry_count\tselected_key_count\n' >"$ENV_OUT/process-environment-summary.tsv"
printf 'timestamp\tpid\tclass\tkey\tvalue\n' >"$ENV_OUT/process-environment-selected.tsv"
printf 'sample\ttimestamp\tmain_seen\tzygote_seen\trenderer_seen\tgpu_seen\n' >"$ENV_OUT/observation-state.tsv"

OBSERVED_PIDS=()
declare -A CAPTURED=()
MAIN_SEEN=0
ZYGOTE_SEEN=0
RENDERER_SEEN=0
GPU_SEEN=0

read_cmdline() {
    local pid=$1
    [ -r "/proc/$pid/cmdline" ] || return 1
    tr '\0' ' ' <"/proc/$pid/cmdline" 2>/dev/null | sed 's/\t/ /g'
}

read_argv0() {
    local pid=$1
    [ -r "/proc/$pid/cmdline" ] || return 1
    tr '\0' '\n' <"/proc/$pid/cmdline" 2>/dev/null | sed -n '1p'
}

classify_cmdline() {
    local cmdline=$1 argv0=$2
    case "$cmdline" in
        *--type=gpu-process*) printf 'gpu\n' ;;
        *--type=renderer*) printf 'renderer\n' ;;
        *--type=utility*) printf 'utility\n' ;;
        *--type=zygote*) printf 'zygote\n' ;;
        *chrome_crashpad_handler*) printf 'crashpad\n' ;;
        *)
            if [ "$argv0" = "$ENTRYPOINT" ] && [[ "$cmdline" != *" --type="* ]]; then
                printf 'main\n'
            else
                printf 'helper\n'
            fi
            ;;
    esac
}

pid_still_belongs_to_environment_probe() {
    local pid=$1 cmdline
    cmdline=$(read_cmdline "$pid" || true)
    [ -n "$cmdline" ] || return 1
    case "$cmdline" in
        *"$APP/"*|*"$ENV_USER_DATA"*) return 0 ;;
        *) return 1 ;;
    esac
}

cleanup_environment_probe() {
    local pid

    for pid in "${OBSERVED_PIDS[@]:-}"; do
        if pid_still_belongs_to_environment_probe "$pid"; then
            kill -TERM "$pid" 2>/dev/null || true
        fi
    done

    mapfile -t remaining < <(pgrep -f "$APP/|$ENV_USER_DATA" 2>/dev/null | sort -n || true)
    for pid in "${remaining[@]:-}"; do
        if pid_still_belongs_to_environment_probe "$pid"; then
            kill -TERM "$pid" 2>/dev/null || true
        fi
    done

    sleep 1

    mapfile -t remaining < <(pgrep -f "$APP/|$ENV_USER_DATA" 2>/dev/null | sort -n || true)
    for pid in "${remaining[@]:-}"; do
        if pid_still_belongs_to_environment_probe "$pid"; then
            kill -KILL "$pid" 2>/dev/null || true
        fi
    done
}
trap cleanup_environment_probe EXIT

capture_environment() {
    local timestamp=$1 pid=$2 class=$3 raw entry_count selected_count line key value
    raw="$ENV_OUT/.environ-$pid.raw"

    if [ ! -r "/proc/$pid/environ" ]; then
        printf '%s\t%s\t%s\tUNREADABLE\t0\t0\n' \
            "$timestamp" "$pid" "$class" \
            >>"$ENV_OUT/process-environment-summary.tsv"
        return
    fi

    if ! tr '\0' '\n' <"/proc/$pid/environ" >"$raw" 2>/dev/null; then
        printf '%s\t%s\t%s\tREAD_FAILED\t0\t0\n' \
            "$timestamp" "$pid" "$class" \
            >>"$ENV_OUT/process-environment-summary.tsv"
        return
    fi

    entry_count=$(awk 'NF { count++ } END { print count + 0 }' "$raw")
    selected_count=0
    while IFS= read -r line; do
        [ -n "$line" ] || continue
        key=${line%%=*}
        value=${line#*=}
        printf '%s\t%s\t%s\t%s\t%s\n' \
            "$timestamp" "$pid" "$class" "$key" "$value" \
            >>"$ENV_OUT/process-environment-selected.tsv"
        selected_count=$((selected_count + 1))
    done < <(
        grep -E '^(GL_GPU|XDG_CONFIG_HOME|VK_DRIVER_FILES|VK_ICD_FILENAMES|LD_LIBRARY_PATH|LD_PRELOAD|LIBGL_ALWAYS_SOFTWARE|MESA_LOADER_DRIVER_OVERRIDE|GALLIUM_DRIVER)=' "$raw" \
            | sort || true
    )

    printf '%s\t%s\t%s\tREAD_OK\t%s\t%s\n' \
        "$timestamp" "$pid" "$class" "$entry_count" "$selected_count" \
        >>"$ENV_OUT/process-environment-summary.tsv"
}

VK_DRIVER_FILES=/bionic/freedreno.json \
VK_ICD_FILENAMES=/bionic/freedreno.json \
MESA_LOADER_DRIVER_OVERRIDE=llvmpipe \
GALLIUM_DRIVER=llvmpipe \
XDG_CONFIG_HOME="$ENV_CONFIG_HOME" \
GL_GPU=1 "$LAUNCHER" \
    --user-data-dir "$ENV_USER_DATA" \
    >"$ENV_OUT/launch.stdout" \
    2>"$ENV_OUT/launch.stderr" &
ENV_LAUNCH_PID=$!
printf '%s\n' "$ENV_LAUNCH_PID" >"$ENV_OUT/launch.pid"
OBSERVED_PIDS+=("$ENV_LAUNCH_PID")

started=$SECONDS
deadline=$((started + ENV_DURATION_SECONDS))
sample=0

while (( SECONDS < deadline )); do
    sample=$((sample + 1))
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%S.%NZ)
    mapfile -t app_pids < <(pgrep -f "$APP/|$ENV_USER_DATA" 2>/dev/null | sort -n || true)

    for pid in "${app_pids[@]:-}"; do
        [ -n "$pid" ] || continue
        cmdline=$(read_cmdline "$pid" || true)
        [ -n "$cmdline" ] || continue
        argv0=$(read_argv0 "$pid" || true)
        [ -n "$argv0" ] || continue
        OBSERVED_PIDS+=("$pid")

        class=$(classify_cmdline "$cmdline" "$argv0")
        ppid=$(awk '/^PPid:/ { print $2; exit }' "/proc/$pid/status" 2>/dev/null || true)

        case "$class" in
            main) MAIN_SEEN=1 ;;
            zygote) ZYGOTE_SEEN=1 ;;
            renderer) RENDERER_SEEN=1 ;;
            gpu) GPU_SEEN=1 ;;
        esac

        capture_key="$pid:$class"
        if [ -z "${CAPTURED[$capture_key]:-}" ]; then
            CAPTURED["$capture_key"]=1
            printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
                "$timestamp" "$pid" "${ppid:-UNKNOWN}" "$class" "$argv0" "$cmdline" \
                >>"$ENV_OUT/processes.tsv"
            capture_environment "$timestamp" "$pid" "$class"
        fi
    done

    printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$sample" "$timestamp" "$MAIN_SEEN" "$ZYGOTE_SEEN" "$RENDERER_SEEN" "$GPU_SEEN" \
        >>"$ENV_OUT/observation-state.tsv"

    sleep "$POLL_SLEEP_SECONDS"
done

live_main=0
while IFS=$'\t' read -r _ pid _ class _; do
    [ "$class" = main ] || continue
    if pid_still_belongs_to_environment_probe "$pid"; then
        live_main=1
        break
    fi
done < <(tail -n +2 "$ENV_OUT/processes.tsv")

cleanup_environment_probe
trap - EXIT

for ((attempt = 0; attempt < 50; attempt++)); do
    existing=$(pgrep -af "$APP/|$ENV_USER_DATA" || true)
    [ -z "$existing" ] && break
    sleep 0.1
done
existing=$(pgrep -af "$APP/|$ENV_USER_DATA" || true)
if [ -n "$existing" ]; then
    printf 'Obsidian processes remained after environment probe cleanup:\n' >&2
    printf '%s\n' "$existing" >&2
    printf 'environment_cleanup\n' >"$OUT/failure-stage.txt"
    printf 'FAIL\n' >"$OUT/validation.status"
    exit 1
fi

if ! APP="$APP" \
ENTRYPOINT="$ENTRYPOINT" \
LAUNCHER="$LAUNCHER" \
APP_LABEL=Obsidian \
CONFIG_HOME="$CDP_CONFIG_HOME" \
USER_DATA_DIR="$CDP_USER_DATA" \
OUT="$CDP_OUT" \
CONTROL_GL_GPU=1 \
VULKAN_POLICY_MODE=explicit-freedreno \
DURATION_SECONDS=${DURATION_SECONDS:-30} \
POLL_SLEEP_SECONDS="$POLL_SLEEP_SECONDS" \
bash "$SCRIPT_DIR/probe-electron-cdp-gpu-identity.sh" \
    >"$OUT/probe.log" 2>&1; then
    printf 'cdp_probe\n' >"$OUT/failure-stage.txt"
    printf 'FAIL\n' >"$OUT/validation.status"
    printf 'promoted Obsidian GPU CDP probe failed\n' >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
fi

if ! CONTROL_OUT="$CDP_OUT" OUT="$CDP_OUT" APP_LABEL=Obsidian \
    bash "$SCRIPT_DIR/classify-cdp-gpu-identity.sh" \
    >"$OUT/classifier.log" 2>&1; then
    printf 'classification\n' >"$OUT/failure-stage.txt"
    printf 'FAIL\n' >"$OUT/validation.status"
    printf 'promoted Obsidian GPU identity classification failed\n' >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
fi

identity_summary="$CDP_OUT/cdp-gpu-identity-summary.tsv"
environment_selected="$ENV_OUT/process-environment-selected.tsv"
environment_summary="$ENV_OUT/process-environment-summary.tsv"
processes="$ENV_OUT/processes.tsv"

classification=$(awk -F $'\t' '$1 == "classification" { print $2; exit }' "$identity_summary")
provider=$(awk -F $'\t' '$1 == "selected_provider" { print $2; exit }' "$identity_summary")
device=$(awk -F $'\t' '$1 == "selected_device_family" { print $2; exit }' "$identity_summary")
provider_path=$(awk -F $'\t' '$1 == "provider_path_relation" { print $2; exit }' "$identity_summary")
device_node=$(awk -F $'\t' '$1 == "device_node_relation" { print $2; exit }' "$identity_summary")
display_type=$(awk -F $'\t' '$1 == "display_type" { print $2; exit }' "$identity_summary")
skia_backend=$(awk -F $'\t' '$1 == "skia_backend" { print $2; exit }' "$identity_summary")
hardware_supports_vulkan=$(awk -F $'\t' '$1 == "hardware_supports_vulkan" { print $2; exit }' "$identity_summary")
vulkan_status=$(awk -F $'\t' '$1 == "vulkan_feature_status" { print $2; exit }' "$identity_summary")
renderer=$(awk -F $'\t' '$1 == "gl_renderer" { print $2; exit }' "$identity_summary")
zygote_max_entries=$(awk -F $'\t' '$3 == "zygote" && $5 + 0 > max { max=$5 + 0 } END { print max + 0 }' "$environment_summary")
gpu_max_entries=$(awk -F $'\t' '$3 == "gpu" && $5 + 0 > max { max=$5 + 0 } END { print max + 0 }' "$environment_summary")
renderer_max_entries=$(awk -F $'\t' '$3 == "renderer" && $5 + 0 > max { max=$5 + 0 } END { print max + 0 }' "$environment_summary")

printf 'gate\tstate\n' >"$OUT/gates.tsv"
failures=0

record_gate() {
    local gate=$1 state=$2
    printf '%s\t%s\n' "$gate" "$state" >>"$OUT/gates.tsv"
    [ "$state" = PASS ] || failures=$((failures + 1))
}

record_expected() {
    local gate=$1 observed=$2 expected=$3
    if [ "$observed" = "$expected" ]; then
        record_gate "$gate" PASS
    else
        record_gate "$gate" FAIL
        printf '%s expected=%s observed=%s\n' "$gate" "$expected" "$observed" >&2
    fi
}

process_observed() {
    local class=$1
    awk -F $'\t' -v c="$class" \
        'NR > 1 && $4 == c { found=1 } END { exit found ? 0 : 1 }' "$processes"
}

environment_read_attempt_succeeded() {
    local class=$1
    awk -F $'\t' -v c="$class" \
        'NR > 1 && $3 == c && $4 == "READ_OK" { found=1 }
         END { exit found ? 0 : 1 }' "$environment_summary"
}

has_exact_environment_value() {
    local class=$1 key=$2 expected=$3
    awk -F $'\t' -v c="$class" -v k="$key" -v e="$expected" \
        'NR > 1 && $3 == c && $4 == k && $5 == e { found=1 }
         END { exit found ? 0 : 1 }' "$environment_selected"
}

all_observable_values_equal() {
    local key=$1 expected=$2
    awk -F $'\t' -v k="$key" -v e="$expected" \
        'NR > 1 && $4 == k { seen=1; if ($5 != e) bad=1 }
         END { exit seen && !bad ? 0 : 1 }' "$environment_selected"
}

observable_key_absent() {
    local key=$1
    ! awk -F $'\t' -v k="$key" \
        'NR > 1 && $4 == k { found=1 } END { exit found ? 0 : 1 }' "$environment_selected"
}

cmdline_class_contains() {
    local class=$1 pattern=$2
    awk -F $'\t' -v c="$class" -v p="$pattern" \
        'NR > 1 && $4 == c && index($6, p) { found=1 }
         END { exit found ? 0 : 1 }' "$processes"
}

for class in main zygote renderer gpu; do
    if process_observed "$class"; then
        record_gate "${class}_observed" PASS
    else
        record_gate "${class}_observed" FAIL
    fi
    if environment_read_attempt_succeeded "$class"; then
        record_gate "${class}_environment_read_attempt" PASS
    else
        record_gate "${class}_environment_read_attempt" FAIL
    fi
done

if has_exact_environment_value main GL_GPU 1; then
    record_gate main_gl_gpu_one PASS
else
    record_gate main_gl_gpu_one FAIL
fi
if has_exact_environment_value main XDG_CONFIG_HOME "$ENV_CONFIG_HOME"; then
    record_gate main_xdg_config_home_exact PASS
else
    record_gate main_xdg_config_home_exact FAIL
fi
if has_exact_environment_value main VK_DRIVER_FILES "$EXPECTED_ICD"; then
    record_gate main_vk_driver_files_exact PASS
else
    record_gate main_vk_driver_files_exact FAIL
fi
if has_exact_environment_value main VK_ICD_FILENAMES "$EXPECTED_ICD"; then
    record_gate main_vk_icd_filenames_exact PASS
else
    record_gate main_vk_icd_filenames_exact FAIL
fi

for spec in \
    "GL_GPU|1|all_observable_gl_gpu_values_one" \
    "XDG_CONFIG_HOME|$ENV_CONFIG_HOME|all_observable_xdg_config_home_exact" \
    "VK_DRIVER_FILES|$EXPECTED_ICD|all_observable_vk_driver_files_exact" \
    "VK_ICD_FILENAMES|$EXPECTED_ICD|all_observable_vk_icd_filenames_exact"
do
    IFS='|' read -r key expected gate <<<"$spec"
    if all_observable_values_equal "$key" "$expected"; then
        record_gate "$gate" PASS
    else
        record_gate "$gate" FAIL
    fi
done

for spec in \
    "MESA_LOADER_DRIVER_OVERRIDE|observable_mesa_loader_override_absent" \
    "GALLIUM_DRIVER|observable_gallium_driver_absent" \
    "LIBGL_ALWAYS_SOFTWARE|observable_libgl_always_software_absent" \
    "LD_LIBRARY_PATH|observable_ld_library_path_absent"
do
    IFS='|' read -r key gate <<<"$spec"
    if observable_key_absent "$key"; then
        record_gate "$gate" PASS
    else
        record_gate "$gate" FAIL
    fi
done

if awk -F $'\t' 'NR > 1 && $4 == "LD_PRELOAD" && $5 != "" { bad=1 }
    END { exit bad ? 0 : 1 }' "$environment_selected"; then
    record_gate observable_ld_preload_nonempty_absent FAIL
else
    record_gate observable_ld_preload_nonempty_absent PASS
fi

if grep -F '/bionic/' "$environment_selected" >/dev/null; then
    record_gate observable_injected_bionic_paths_absent FAIL
else
    record_gate observable_injected_bionic_paths_absent PASS
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
        record_gate "main_has_${gate}" PASS
    else
        record_gate "main_has_${gate}" FAIL
    fi
done

if grep -Eq '(^|[[:space:]])--disable-gpu([[:space:]]|$)' "$main_cmdlines"; then
    record_gate main_exact_disable_gpu_absent FAIL
else
    record_gate main_exact_disable_gpu_absent PASS
fi

if cmdline_class_contains main "--user-data-dir $ENV_USER_DATA" || \
   cmdline_class_contains main "--user-data-dir=$ENV_USER_DATA"; then
    record_gate main_uses_isolated_user_data PASS
else
    record_gate main_uses_isolated_user_data FAIL
fi

if cmdline_class_contains renderer "--user-data-dir=$ENV_USER_DATA" || \
   cmdline_class_contains renderer "--user-data-dir $ENV_USER_DATA"; then
    record_gate renderer_uses_isolated_user_data PASS
else
    record_gate renderer_uses_isolated_user_data FAIL
fi

if grep -F "$HOME/.config/obsidian" "$processes" >/dev/null; then
    record_gate normal_user_data_path_absent FAIL
else
    record_gate normal_user_data_path_absent PASS
fi

[ "$live_main" = 1 ] && record_gate main_survived_observation PASS || record_gate main_survived_observation FAIL

if grep -Eiq 'FATAL|GPU process isn.t usable|SIGBUS|Bus error' "$ENV_OUT/launch.stderr"; then
    record_gate no_fatal_gpu_diagnostic FAIL
else
    record_gate no_fatal_gpu_diagnostic PASS
fi

record_expected cdp_probe_status "$(tr -d '\r\n' <"$CDP_OUT/probe.status")" PASS
record_expected identity_status "$(tr -d '\r\n' <"$CDP_OUT/cdp-gpu-identity.status")" PASS
record_expected cdp_config_home "$(sed 's/^config home: //' "$CDP_OUT/config-home.txt")" "$CDP_CONFIG_HOME"
record_expected cdp_user_data_dir "$(sed 's/^user data dir: //' "$CDP_OUT/user-data-dir.txt")" "$CDP_USER_DATA"
record_expected classification "$classification" FREEDRENO_TURNIP
record_expected selected_provider "$provider" FREEDRENO_TURNIP
record_expected selected_device_family "$device" Adreno
record_expected provider_path_relation "$provider_path" PRESENT
record_expected device_node_relation "$device_node" PRESENT
record_expected display_type "$display_type" ANGLE_VULKAN
record_expected skia_backend "$skia_backend" GaneshVulkan
record_expected hardware_supports_vulkan "$hardware_supports_vulkan" true
record_expected vulkan_feature_status "$vulkan_status" enabled_on

if printf '%s\n' "$renderer" | grep -Eiq 'Turnip.*Adreno|Adreno.*Turnip'; then
    record_gate renderer_identity PASS
else
    record_gate renderer_identity FAIL
fi

{
    printf 'field\tvalue\n'
    printf 'branch\t%s\n' "$branch"
    printf 'head\t%s\n' "$head_sha"
    printf 'launcher\t%s\n' "$LAUNCHER"
    printf 'launcher_target\t%s\n' "$expected_launcher"
    printf 'expected_icd\t%s\n' "$EXPECTED_ICD"
    printf 'environment_config_home\t%s\n' "$ENV_CONFIG_HOME"
    printf 'environment_user_data\t%s\n' "$ENV_USER_DATA"
    printf 'cdp_config_home\t%s\n' "$CDP_CONFIG_HOME"
    printf 'cdp_user_data\t%s\n' "$CDP_USER_DATA"
    printf 'classification\t%s\n' "$classification"
    printf 'selected_provider\t%s\n' "$provider"
    printf 'selected_device_family\t%s\n' "$device"
    printf 'renderer\t%s\n' "$renderer"
    printf 'main_seen\t%s\n' "$MAIN_SEEN"
    printf 'zygote_seen\t%s\n' "$ZYGOTE_SEEN"
    printf 'renderer_seen\t%s\n' "$RENDERER_SEEN"
    printf 'gpu_seen\t%s\n' "$GPU_SEEN"
    printf 'zygote_max_observable_environment_entries\t%s\n' "$zygote_max_entries"
    printf 'renderer_max_observable_environment_entries\t%s\n' "$renderer_max_entries"
    printf 'gpu_max_observable_environment_entries\t%s\n' "$gpu_max_entries"
    printf 'child_environment_value_claim\tNOT_MADE_WHEN_PROC_ENVIRON_EMPTY\n'
    printf 'environment_probe\t%s\n' "$ENV_OUT"
    printf 'cdp_probe\t%s\n' "$CDP_OUT"
    printf 'gate_failures\t%s\n' "$failures"
} >"$OUT/summary.tsv"

if [ "$failures" -ne 0 ]; then
    printf 'gate_evaluation\n' >"$OUT/failure-stage.txt"
    printf 'FAIL\n' >"$OUT/validation.status"
    printf 'promoted Obsidian GPU environment/identity validation: FAIL (%s gates)\n' "$failures" >&2
    printf 'evidence: %s\n' "$OUT" >&2
    cat "$OUT/summary.tsv" >&2
    exit 1
fi

printf 'PASS\n' >"$OUT/validation.status"
printf 'promoted Obsidian GPU environment/identity validation: PASS\n'
printf 'evidence: %s\n' "$OUT"
printf '\n===== summary =====\n'
cat "$OUT/summary.tsv"
printf '\n===== gates =====\n'
cat "$OUT/gates.tsv"
printf '\n===== selected observable environment =====\n'
cat "$environment_selected"
printf '\n===== environment process identities =====\n'
cat "$processes"
printf '\n===== GPU devices =====\n'
cat "$CDP_OUT/gpu-devices.tsv"
printf '\n===== GPU graphics paths =====\n'
cat "$CDP_OUT/gpu-graphics-paths.tsv"
