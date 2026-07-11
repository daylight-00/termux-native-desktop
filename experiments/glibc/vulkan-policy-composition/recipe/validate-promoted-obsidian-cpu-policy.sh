#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/promoted-obsidian-cpu-policy-$(date +%Y%m%d-%H%M%S)}
CONFIG_HOME="$OUT/config"
USER_DATA_DIR="$CONFIG_HOME/obsidian"
LAUNCHER=${LAUNCHER:-$HOME/gl/bin/obsidian-app}
APP=${APP:-$HOME/gl/apps/obsidian}
ENTRYPOINT=${ENTRYPOINT:-$APP/obsidian}
DURATION_SECONDS=${DURATION_SECONDS:-20}
POLL_SLEEP_SECONDS=${POLL_SLEEP_SECONDS:-0.1}

for command in git bash awk grep mkdir date readlink pgrep sort tr sed sleep tail wc; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

tracked_dirty=$(git -C "$REPO" status --porcelain --untracked-files=no)
if [ -n "$tracked_dirty" ]; then
    printf 'tracked working-tree changes detected; Obsidian CPU gate requires exact HEAD:\n' >&2
    printf '%s\n' "$tracked_dirty" >&2
    exit 2
fi

case "$DURATION_SECONDS" in
    ''|*[!0-9]*|0)
        printf 'DURATION_SECONDS must be a positive integer: %s\n' "$DURATION_SECONDS" >&2
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

if [ "${LIBGL_ALWAYS_SOFTWARE+x}" = x ]; then
    printf 'LIBGL_ALWAYS_SOFTWARE must be unset before the Obsidian CPU gate\n' >&2
    exit 2
fi

existing=$(pgrep -af "$APP/|$USER_DATA_DIR" || true)
if [ -n "$existing" ]; then
    printf 'existing Obsidian processes detected; close them before the CPU gate:\n' >&2
    printf '%s\n' "$existing" >&2
    exit 1
fi

mkdir -p "$USER_DATA_DIR"
branch=$(git -C "$REPO" branch --show-current)
head_sha=$(git -C "$REPO" rev-parse HEAD)
printf '%s\n' "$branch" >"$OUT/branch.txt"
printf '%s\n' "$head_sha" >"$OUT/head.txt"
printf '%s\n' "$LAUNCHER" >"$OUT/launcher-path.txt"
printf '%s\n' "$expected_launcher" >"$OUT/launcher-target.txt"
printf '%s\n' "$CONFIG_HOME" >"$OUT/config-home.txt"
printf '%s\n' "$USER_DATA_DIR" >"$OUT/user-data-dir.txt"
printf '%s\n' "$DURATION_SECONDS" >"$OUT/duration.txt"

printf 'timestamp\tpid\tppid\tclass\targv0\tcmdline\n' >"$OUT/processes.tsv"
printf 'timestamp\tpid\tclass\tstate\tentry_count\tselected_key_count\n' >"$OUT/process-environment-summary.tsv"
printf 'timestamp\tpid\tclass\tkey\tvalue\n' >"$OUT/process-environment-selected.tsv"
printf 'sample\ttimestamp\tmain_seen\tzygote_seen\trenderer_seen\tgpu_seen\n' >"$OUT/observation-state.tsv"

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

pid_still_belongs_to_probe() {
    local pid=$1 cmdline
    cmdline=$(read_cmdline "$pid" || true)
    [ -n "$cmdline" ] || return 1
    case "$cmdline" in
        *"$APP/"*|*"$USER_DATA_DIR"*) return 0 ;;
        *) return 1 ;;
    esac
}

cleanup() {
    local pid

    for pid in "${OBSERVED_PIDS[@]:-}"; do
        if pid_still_belongs_to_probe "$pid"; then
            kill -TERM "$pid" 2>/dev/null || true
        fi
    done

    mapfile -t remaining < <(pgrep -f "$APP/|$USER_DATA_DIR" 2>/dev/null | sort -n || true)
    for pid in "${remaining[@]:-}"; do
        if pid_still_belongs_to_probe "$pid"; then
            kill -TERM "$pid" 2>/dev/null || true
        fi
    done

    sleep 1

    mapfile -t remaining < <(pgrep -f "$APP/|$USER_DATA_DIR" 2>/dev/null | sort -n || true)
    for pid in "${remaining[@]:-}"; do
        if pid_still_belongs_to_probe "$pid"; then
            kill -KILL "$pid" 2>/dev/null || true
        fi
    done
}
trap cleanup EXIT

capture_environment() {
    local timestamp=$1 pid=$2 class=$3 raw entry_count selected_count line key value
    raw="$OUT/.environ-$pid.raw"

    if [ ! -r "/proc/$pid/environ" ]; then
        printf '%s\t%s\t%s\tUNREADABLE\t0\t0\n' \
            "$timestamp" "$pid" "$class" \
            >>"$OUT/process-environment-summary.tsv"
        return
    fi

    if ! tr '\0' '\n' <"/proc/$pid/environ" >"$raw" 2>/dev/null; then
        printf '%s\t%s\t%s\tREAD_FAILED\t0\t0\n' \
            "$timestamp" "$pid" "$class" \
            >>"$OUT/process-environment-summary.tsv"
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
            >>"$OUT/process-environment-selected.tsv"
        selected_count=$((selected_count + 1))
    done < <(
        grep -E '^(GL_GPU|XDG_CONFIG_HOME|VK_DRIVER_FILES|VK_ICD_FILENAMES|LD_LIBRARY_PATH|LD_PRELOAD|LIBGL_ALWAYS_SOFTWARE|MESA_LOADER_DRIVER_OVERRIDE|GALLIUM_DRIVER)=' "$raw" \
            | sort || true
    )

    printf '%s\t%s\t%s\tREAD_OK\t%s\t%s\n' \
        "$timestamp" "$pid" "$class" "$entry_count" "$selected_count" \
        >>"$OUT/process-environment-summary.tsv"
}

# Deliberately inject incompatible bionic provider and bridge/device policy.
# The promoted CPU branch must sanitize all values before applying GL_GPU=0.
VK_DRIVER_FILES=/bionic/freedreno.json \
VK_ICD_FILENAMES=/bionic/freedreno.json \
MESA_LOADER_DRIVER_OVERRIDE=llvmpipe \
GALLIUM_DRIVER=llvmpipe \
XDG_CONFIG_HOME="$CONFIG_HOME" \
GL_GPU=0 "$LAUNCHER" \
    --user-data-dir "$USER_DATA_DIR" \
    >"$OUT/launch.stdout" \
    2>"$OUT/launch.stderr" &
LAUNCH_PID=$!
printf '%s\n' "$LAUNCH_PID" >"$OUT/launch.pid"
OBSERVED_PIDS+=("$LAUNCH_PID")

started=$SECONDS
deadline=$((started + DURATION_SECONDS))
sample=0

while (( SECONDS < deadline )); do
    sample=$((sample + 1))
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%S.%NZ)
    mapfile -t app_pids < <(pgrep -f "$APP/|$USER_DATA_DIR" 2>/dev/null | sort -n || true)

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
                >>"$OUT/processes.tsv"
            capture_environment "$timestamp" "$pid" "$class"
        fi
    done

    printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$sample" "$timestamp" "$MAIN_SEEN" "$ZYGOTE_SEEN" "$RENDERER_SEEN" "$GPU_SEEN" \
        >>"$OUT/observation-state.tsv"

    sleep "$POLL_SLEEP_SECONDS"
done

live_main=0
while IFS=$'\t' read -r _ pid _ class _; do
    [ "$class" = main ] || continue
    if pid_still_belongs_to_probe "$pid"; then
        live_main=1
        break
    fi
done < <(tail -n +2 "$OUT/processes.tsv")

printf 'gate\tstate\n' >"$OUT/gates.tsv"
failures=0

record_gate() {
    local gate=$1 state=$2
    printf '%s\t%s\n' "$gate" "$state" >>"$OUT/gates.tsv"
    [ "$state" = PASS ] || failures=$((failures + 1))
}

process_observed() {
    local class=$1
    awk -F $'\t' -v c="$class" \
        'NR > 1 && $4 == c { found=1 } END { exit found ? 0 : 1 }' "$OUT/processes.tsv"
}

environment_read_attempt_succeeded() {
    local class=$1
    awk -F $'\t' -v c="$class" \
        'NR > 1 && $3 == c && $4 == "READ_OK" { found=1 }
         END { exit found ? 0 : 1 }' "$OUT/process-environment-summary.tsv"
}

has_exact_environment_value() {
    local class=$1 key=$2 expected=$3
    awk -F $'\t' -v c="$class" -v k="$key" -v e="$expected" \
        'NR > 1 && $3 == c && $4 == k && $5 == e { found=1 }
         END { exit found ? 0 : 1 }' "$OUT/process-environment-selected.tsv"
}

all_observable_values_equal() {
    local key=$1 expected=$2
    awk -F $'\t' -v k="$key" -v e="$expected" \
        'NR > 1 && $4 == k { seen=1; if ($5 != e) bad=1 }
         END { exit seen && !bad ? 0 : 1 }' "$OUT/process-environment-selected.tsv"
}

cmdline_class_contains() {
    local class=$1 pattern=$2
    awk -F $'\t' -v c="$class" -v p="$pattern" \
        'NR > 1 && $4 == c && index($6, p) { found=1 }
         END { exit found ? 0 : 1 }' "$OUT/processes.tsv"
}

for class in main zygote renderer; do
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

if has_exact_environment_value main GL_GPU 0; then
    record_gate main_gl_gpu_zero PASS
else
    record_gate main_gl_gpu_zero FAIL
fi

if has_exact_environment_value main XDG_CONFIG_HOME "$CONFIG_HOME"; then
    record_gate main_xdg_config_home_exact PASS
else
    record_gate main_xdg_config_home_exact FAIL
fi

if all_observable_values_equal GL_GPU 0; then
    record_gate all_observable_gl_gpu_values_zero PASS
else
    record_gate all_observable_gl_gpu_values_zero FAIL
fi

if all_observable_values_equal XDG_CONFIG_HOME "$CONFIG_HOME"; then
    record_gate all_observable_xdg_config_home_exact PASS
else
    record_gate all_observable_xdg_config_home_exact FAIL
fi

if grep -Eq $'\t(VK_DRIVER_FILES|VK_ICD_FILENAMES)\t' "$OUT/process-environment-selected.tsv"; then
    record_gate observable_explicit_vulkan_policy_absent FAIL
else
    record_gate observable_explicit_vulkan_policy_absent PASS
fi

if grep -Eq $'\t(MESA_LOADER_DRIVER_OVERRIDE|GALLIUM_DRIVER|LIBGL_ALWAYS_SOFTWARE|LD_LIBRARY_PATH)\t' \
    "$OUT/process-environment-selected.tsv"; then
    record_gate observable_graphics_and_library_overrides_absent FAIL
else
    record_gate observable_graphics_and_library_overrides_absent PASS
fi

if awk -F $'\t' 'NR > 1 && $4 == "LD_PRELOAD" && $5 != "" { bad=1 }
    END { exit bad ? 0 : 1 }' "$OUT/process-environment-selected.tsv"; then
    record_gate observable_ld_preload_nonempty_absent FAIL
else
    record_gate observable_ld_preload_nonempty_absent PASS
fi

if grep -F '/bionic/' "$OUT/process-environment-selected.tsv" >/dev/null; then
    record_gate observable_injected_bionic_paths_absent FAIL
else
    record_gate observable_injected_bionic_paths_absent PASS
fi

main_cmdlines="$OUT/main-cmdlines.txt"
awk -F $'\t' 'NR > 1 && $4 == "main" { print $6 }' "$OUT/processes.tsv" >"$main_cmdlines"

if grep -Eq '(^|[[:space:]])--disable-gpu([[:space:]]|$)' "$main_cmdlines"; then
    record_gate main_has_exact_disable_gpu PASS
else
    record_gate main_has_exact_disable_gpu FAIL
fi

if grep -E -- '--use-angle=vulkan|--use-gl=angle|--enable-features=Vulkan|--disable-gpu-vsync|--ignore-gpu-blocklist|--disable-gpu-sandbox' \
    "$main_cmdlines" >/dev/null; then
    record_gate main_has_no_gpu_enable_flags FAIL
else
    record_gate main_has_no_gpu_enable_flags PASS
fi

if cmdline_class_contains main "--user-data-dir $USER_DATA_DIR" || \
   cmdline_class_contains main "--user-data-dir=$USER_DATA_DIR"; then
    record_gate main_uses_isolated_user_data PASS
else
    record_gate main_uses_isolated_user_data FAIL
fi

if cmdline_class_contains renderer "--user-data-dir=$USER_DATA_DIR" || \
   cmdline_class_contains renderer "--user-data-dir $USER_DATA_DIR"; then
    record_gate renderer_uses_isolated_user_data PASS
else
    record_gate renderer_uses_isolated_user_data FAIL
fi

if grep -F "$HOME/.config/obsidian" "$OUT/processes.tsv" >/dev/null; then
    record_gate normal_user_data_path_absent FAIL
else
    record_gate normal_user_data_path_absent PASS
fi

[ "$live_main" = 1 ] && record_gate main_survived_observation PASS || record_gate main_survived_observation FAIL

if grep -Eiq 'FATAL|GPU process isn.t usable|SIGBUS|Bus error' "$OUT/launch.stderr"; then
    record_gate no_fatal_diagnostic FAIL
else
    record_gate no_fatal_diagnostic PASS
fi

zygote_max_entries=$(awk -F $'\t' '$3 == "zygote" && $5 + 0 > max { max=$5 + 0 } END { print max + 0 }' "$OUT/process-environment-summary.tsv")
renderer_max_entries=$(awk -F $'\t' '$3 == "renderer" && $5 + 0 > max { max=$5 + 0 } END { print max + 0 }' "$OUT/process-environment-summary.tsv")
gpu_max_entries=$(awk -F $'\t' '$3 == "gpu" && $5 + 0 > max { max=$5 + 0 } END { print max + 0 }' "$OUT/process-environment-summary.tsv")

{
    printf 'field\tvalue\n'
    printf 'branch\t%s\n' "$branch"
    printf 'head\t%s\n' "$head_sha"
    printf 'launcher\t%s\n' "$LAUNCHER"
    printf 'launcher_target\t%s\n' "$expected_launcher"
    printf 'config_home\t%s\n' "$CONFIG_HOME"
    printf 'user_data_dir\t%s\n' "$USER_DATA_DIR"
    printf 'duration_seconds\t%s\n' "$DURATION_SECONDS"
    printf 'main_seen\t%s\n' "$MAIN_SEEN"
    printf 'zygote_seen\t%s\n' "$ZYGOTE_SEEN"
    printf 'renderer_seen\t%s\n' "$RENDERER_SEEN"
    printf 'gpu_seen_observational\t%s\n' "$GPU_SEEN"
    printf 'zygote_max_observable_environment_entries\t%s\n' "$zygote_max_entries"
    printf 'renderer_max_observable_environment_entries\t%s\n' "$renderer_max_entries"
    printf 'gpu_max_observable_environment_entries\t%s\n' "$gpu_max_entries"
    printf 'child_environment_value_claim\tNOT_MADE_WHEN_PROC_ENVIRON_EMPTY\n'
    printf 'captured_processes\t%s\n' "$(awk 'NR > 1 { count++ } END { print count + 0 }' "$OUT/processes.tsv")"
    printf 'gate_failures\t%s\n' "$failures"
} >"$OUT/summary.tsv"

if [ "$failures" -ne 0 ]; then
    printf 'FAIL\n' >"$OUT/validation.status"
    printf 'promoted Obsidian CPU policy validation: FAIL (%s gates)\n' "$failures" >&2
    printf 'evidence: %s\n' "$OUT" >&2
    cat "$OUT/summary.tsv" >&2
    exit 1
fi

printf 'PASS\n' >"$OUT/validation.status"
printf 'promoted Obsidian CPU policy validation: PASS\n'
printf 'evidence: %s\n' "$OUT"
printf '\n===== summary =====\n'
cat "$OUT/summary.tsv"
printf '\n===== gates =====\n'
cat "$OUT/gates.tsv"
printf '\n===== process identities =====\n'
cat "$OUT/processes.tsv"
printf '\n===== environment observation summary =====\n'
cat "$OUT/process-environment-summary.tsv"
printf '\n===== selected observable environment =====\n'
cat "$OUT/process-environment-selected.tsv"
printf '\n===== main cmdline =====\n'
cat "$OUT/main-cmdlines.txt"
printf '\n===== launch stderr =====\n'
sed -n '1,200p' "$OUT/launch.stderr" || true
