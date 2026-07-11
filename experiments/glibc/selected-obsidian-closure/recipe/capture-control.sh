#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

APP=${APP:-$HOME/gl/apps/obsidian}
APP_ENTRYPOINT=${APP_ENTRYPOINT:-$APP/obsidian}
CONTROL_NAME=${CONTROL_NAME:-Obsidian}
LAUNCHER=${LAUNCHER:-$HOME/gl/bin/obsidian-app}
MAIN_PROCESS_EXECUTABLE=${MAIN_PROCESS_EXECUTABLE:-}
ROOTFS=${ROOTFS:-$PREFIX/var/lib/proot-distro/containers/debian/rootfs}
OUT=${OUT:-$PREFIX/tmp/selected-obsidian-control-$(date +%Y%m%d-%H%M%S)}
CONTROL_GL_GPU=${CONTROL_GL_GPU:-0}
STARTUP_TIMEOUT_SECONDS=${STARTUP_TIMEOUT_SECONDS:-30}
TOPOLOGY_SETTLE_SECONDS=${TOPOLOGY_SETTLE_SECONDS:-5}
SURVIVAL_SECONDS=${SURVIVAL_SECONDS:-100}
POLL_SLEEP_SECONDS=${POLL_SLEEP_SECONDS:-0.5}
PROGRESS_INTERVAL_SECONDS=${PROGRESS_INTERVAL_SECONDS:-10}

for command in readelf sha256sum file dpkg-query proot-distro; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

[ -x "$APP_ENTRYPOINT" ] || {
    printf 'missing %s payload entrypoint: %s\n' "$CONTROL_NAME" "$APP_ENTRYPOINT" >&2
    exit 1
}

[ -x "$LAUNCHER" ] || {
    printf 'missing %s launcher: %s\n' "$CONTROL_NAME" "$LAUNCHER" >&2
    exit 1
}

if [ -n "$MAIN_PROCESS_EXECUTABLE" ] && [ ! -x "$MAIN_PROCESS_EXECUTABLE" ]; then
    printf 'missing %s main-process executable: %s\n' \
        "$CONTROL_NAME" "$MAIN_PROCESS_EXECUTABLE" >&2
    exit 1
fi

case "$CONTROL_GL_GPU" in
    0|1) ;;
    *)
        printf 'CONTROL_GL_GPU must be 0 or 1: %s\n' "$CONTROL_GL_GPU" >&2
        exit 2
        ;;
esac

existing=$(pgrep -af "$APP/" || true)
if [ -n "$existing" ]; then
    printf 'existing %s processes detected; close them before control capture:\n' "$CONTROL_NAME" >&2
    printf '%s\n' "$existing" >&2
    exit 1
fi

mkdir -p "$OUT/maps"
printf 'phase\tsample\tpid\tclass\tcmdline\n' >"$OUT/poll-observed.tsv"
printf 'pid\tclass\tcmdline\n' >"$OUT/last-processes.tsv"
printf 'pid\n' >"$OUT/observed-pids.tsv"
printf 'selection\ttimestamp\tphase\tsample\tpid\tppid\tcmdline\n' \
    >"$OUT/main-process-selection.tsv"

printf 'app: %s\n' "$APP" | tee "$OUT/app-path.txt"
printf 'launcher: %s\n' "$LAUNCHER" | tee "$OUT/launcher-path.txt"
if [ -n "$MAIN_PROCESS_EXECUTABLE" ]; then
    printf 'main process selection: descendant argv0=%s\n' \
        "$MAIN_PROCESS_EXECUTABLE" | tee "$OUT/main-process-contract.txt"
else
    printf 'main process selection: launch pid\n' \
        | tee "$OUT/main-process-contract.txt"
fi
printf 'mode: GL_GPU=%s\n' "$CONTROL_GL_GPU" | tee "$OUT/mode.txt"
printf 'startup timeout seconds: %s\n' "$STARTUP_TIMEOUT_SECONDS" | tee "$OUT/startup-contract.txt"
printf 'survival seconds: %s\n' "$SURVIVAL_SECONDS" | tee "$OUT/survival-contract.txt"

printf '\n===== launch %s control =====\n' "$CONTROL_NAME"
printf 'Observe the window during topology and survival gates.\n'

GL_GPU="$CONTROL_GL_GPU" \
"$LAUNCHER" \
    >"$OUT/launch.stdout" \
    2>"$OUT/launch.stderr" &
LAUNCH_PID=$!
printf '%s\n' "$LAUNCH_PID" >"$OUT/launch.pid"
printf 'launch pid: %s\n' "$LAUNCH_PID"

MAIN_PID=
if [ -z "$MAIN_PROCESS_EXECUTABLE" ]; then
    MAIN_PID=$LAUNCH_PID
    printf '%s\n' "$MAIN_PID" >"$OUT/main.pid"
    printf 'launch-pid\t%s\tlaunch\t0\t%s\t-\t-\n' \
        "$(date -u +%Y-%m-%dT%H:%M:%S.%NZ)" "$MAIN_PID" \
        >>"$OUT/main-process-selection.tsv"
fi

declare -A OBSERVED_PIDS=()
OBSERVED_PIDS["$LAUNCH_PID"]=1

collect_tree_pids() {
    local root=$1
    local changed=1 status pid ppid
    declare -A member=()
    member["$root"]=1

    while [ "$changed" -eq 1 ]; do
        changed=0
        for status in /proc/[0-9]*/status; do
            [ -r "$status" ] || continue
            pid=${status#/proc/}
            pid=${pid%/status}
            [ -n "${member[$pid]:-}" ] && continue
            ppid=$(awk '/^PPid:/ { print $2; exit }' "$status" 2>/dev/null || true)
            [ -n "$ppid" ] || continue
            if [ -n "${member[$ppid]:-}" ]; then
                member["$pid"]=1
                changed=1
            fi
        done
    done

    printf '%s\n' "${!member[@]}" | sort -n
}


adopt_main_process() {
    local phase=$1 sample=$2
    local pid cmdline argv0 ppid timestamp
    local candidate_pid= candidate_ppid= candidate_cmdline=
    local candidate_count=0

    [ -n "$MAIN_PROCESS_EXECUTABLE" ] || return 0
    [ -z "$MAIN_PID" ] || return 0

    for pid in "${CURRENT_TREE[@]:-}"; do
        [ -r "/proc/$pid/cmdline" ] || continue
        cmdline=$(tr '\0' ' ' <"/proc/$pid/cmdline" 2>/dev/null || true)
        [ -n "$cmdline" ] || continue

        argv0=${cmdline%% *}
        [ "$argv0" = "$MAIN_PROCESS_EXECUTABLE" ] || continue

        case "$cmdline" in
            *" --type="*) continue ;;
        esac

        ppid=$(awk '/^PPid:/ { print $2; exit }' \
            "/proc/$pid/status" 2>/dev/null || true)
        [ -n "$ppid" ] || continue

        candidate_pid=$pid
        candidate_ppid=$ppid
        candidate_cmdline=$cmdline
        candidate_count=$((candidate_count + 1))
    done

    if [ "$candidate_count" -gt 1 ]; then
        printf 'ambiguous %s main-process descendants for argv0=%s\n' \
            "$CONTROL_NAME" "$MAIN_PROCESS_EXECUTABLE" >&2
        return 2
    fi

    [ "$candidate_count" -eq 1 ] || return 0

    MAIN_PID=$candidate_pid
    OBSERVED_PIDS["$MAIN_PID"]=1
    printf '%s\n' "$MAIN_PID" >"$OUT/main.pid"
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%S.%NZ)
    printf 'descendant-argv0\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$timestamp" "$phase" "$sample" "$MAIN_PID" \
        "$candidate_ppid" "$candidate_cmdline" \
        >>"$OUT/main-process-selection.tsv"
    printf 'adopted main pid: %s (ppid=%s, argv0=%s)\n' \
        "$MAIN_PID" "$candidate_ppid" "$MAIN_PROCESS_EXECUTABLE"
}

classify_cmdline() {
    local pid=$1 cmdline=$2
    if [ -n "$MAIN_PID" ] && [ "$pid" = "$MAIN_PID" ]; then
        printf 'main\n'
        return 0
    fi

    if [ "$pid" = "$LAUNCH_PID" ]; then
        printf 'launcher\n'
        return 0
    fi

    case "$cmdline" in
        *chrome_crashpad_handler*) printf 'crashpad\n' ;;
        *--type=renderer*) printf 'renderer\n' ;;
        *--type=utility*) printf 'utility\n' ;;
        *--type=gpu-process*) printf 'gpu\n' ;;
        *--type=zygote*) printf 'zygote\n' ;;
        *) printf 'helper\n' ;;
    esac
}

observe_tree() {
    local phase=$1 sample=$2 pid cmdline class root
    root=$LAUNCH_PID
    [ -n "$MAIN_PID" ] && root=$MAIN_PID
    mapfile -t CURRENT_TREE < <(collect_tree_pids "$root")
    adopt_main_process "$phase" "$sample"

    for pid in "${CURRENT_TREE[@]:-}"; do
        [ -r "/proc/$pid/cmdline" ] || continue
        cmdline=$(tr '\0' ' ' <"/proc/$pid/cmdline")
        class=$(classify_cmdline "$pid" "$cmdline")
        OBSERVED_PIDS["$pid"]=1
        printf '%s\t%s\t%s\t%s\t%s\n' \
            "$phase" "$sample" "$pid" "$class" "$cmdline" \
            >>"$OUT/poll-observed.tsv"
    done

    {
        printf 'pid\tclass\tcmdline\n'
        for pid in "${CURRENT_TREE[@]:-}"; do
            [ -r "/proc/$pid/cmdline" ] || continue
            cmdline=$(tr '\0' ' ' <"/proc/$pid/cmdline")
            class=$(classify_cmdline "$pid" "$cmdline")
            printf '%s\t%s\t%s\n' "$pid" "$class" "$cmdline"
        done
    } >"$OUT/last-processes.tsv"
}

cleanup() {
    local pid
    for pid in "${!OBSERVED_PIDS[@]}"; do
        kill -TERM "$pid" 2>/dev/null || true
    done
    sleep 1
    for pid in "${!OBSERVED_PIDS[@]}"; do
        kill -KILL "$pid" 2>/dev/null || true
    done
}
trap cleanup EXIT

stable=0
sample=0
startup_started=$SECONDS
startup_deadline=$((startup_started + STARTUP_TIMEOUT_SECONDS))

while (( SECONDS < startup_deadline )); do
    sample=$((sample + 1))
    observe_tree startup "$sample"

    have_main=0
    have_renderer=0
    have_zygote=0

    while IFS=$'\t' read -r pid class cmdline; do
        [ "$pid" = pid ] && continue
        case "$class" in
            main) have_main=1 ;;
            renderer) have_renderer=1 ;;
            zygote) have_zygote=1 ;;
        esac
    done <"$OUT/last-processes.tsv"

    if [ "$have_main" -eq 1 ] && \
       [ "$have_renderer" -eq 1 ] && \
       [ "$have_zygote" -eq 1 ]; then
        stable=1
        break
    fi

    sleep "$POLL_SLEEP_SECONDS"
done

if [ "$stable" -ne 1 ]; then
    printf 'required process classes did not stabilize before wall-clock timeout\n' >&2
    printf '\n===== final observed process topology =====\n' >&2
    cat "$OUT/last-processes.tsv" >&2 || true
    printf '\npartial evidence: %s\n' "$OUT" >&2
    exit 1
fi

printf '\ntopology gate: PASS\n'
printf 'required classes: main renderer zygote\n'
printf 'main pid: %s\n' "$MAIN_PID"
printf 'elapsed seconds: %s\n' "$((SECONDS - startup_started))"
printf 'PASS\n' >"$OUT/topology.status"

sleep "$TOPOLOGY_SETTLE_SECONDS"

printf '\n===== survival gate =====\n'
printf 'seconds: %s\n' "$SURVIVAL_SECONDS"

survival_started=$SECONDS
survival_deadline=$((survival_started + SURVIVAL_SECONDS))
next_progress=$((survival_started + PROGRESS_INTERVAL_SECONDS))
survival_sample=0

while (( SECONDS < survival_deadline )); do
    if [ ! -d "/proc/$MAIN_PID" ]; then
        printf 'FAIL main process exited\n' >"$OUT/survival.status"
        printf 'survival gate: FAIL (main process exited)\n' >&2
        printf '\n===== stderr =====\n' >&2
        sed -n '1,240p' "$OUT/launch.stderr" >&2 || true
        exit 1
    fi

    survival_sample=$((survival_sample + 1))
    observe_tree survival "$survival_sample"

    if (( SECONDS >= next_progress )); then
        elapsed=$((SECONDS - survival_started))
        remaining=$((survival_deadline - SECONDS))
        (( remaining < 0 )) && remaining=0
        printf 'survival progress: %ss elapsed, %ss remaining\n' "$elapsed" "$remaining"
        next_progress=$((SECONDS + PROGRESS_INTERVAL_SECONDS))
    fi

    sleep "$POLL_SLEEP_SECONDS"
done

if grep -q 'FATAL:' "$OUT/launch.stderr"; then
    printf 'FAIL fatal diagnostic observed\n' >"$OUT/survival.status"
    printf 'survival gate: FAIL (FATAL diagnostic observed)\n' >&2
    printf '\n===== fatal diagnostics =====\n' >&2
    grep 'FATAL:' "$OUT/launch.stderr" >&2 || true
    exit 1
fi

[ -d "/proc/$MAIN_PID" ] || {
    printf 'FAIL main process absent at final gate\n' >"$OUT/survival.status"
    printf 'survival gate: FAIL (main process absent at final gate)\n' >&2
    exit 1
}

printf 'survival gate: PASS\n'
printf 'elapsed seconds: %s\n' "$((SECONDS - survival_started))"
printf 'PASS\n' >"$OUT/survival.status"

observe_tree final 1
mapfile -t capture_pids < <(collect_tree_pids "$MAIN_PID")

printf 'pid\tclass\tcmdline\n' >"$OUT/processes.tsv"
printf 'pid\tclass\tpath_class\tpath\n' >"$OUT/mapped-objects.tsv"

classify_path() {
    local path=$1
    case "$path" in
        "$APP"/*) printf 'APP_LOCAL\n' ;;
        "$PREFIX/glibc/lib"/*) printf 'PREFIX_GLIBC\n' ;;
        "$ROOTFS"/*) printf 'ROOTFS_PROVIDER\n' ;;
        *) printf 'OTHER_ABSOLUTE\n' ;;
    esac
}

printf '\n===== final process set =====\n'
for pid in "${capture_pids[@]}"; do
    [ -r "/proc/$pid/cmdline" ] || continue
    [ -r "/proc/$pid/maps" ] || continue

    cmdline=$(tr '\0' ' ' <"/proc/$pid/cmdline")
    class=$(classify_cmdline "$pid" "$cmdline")

    printf '%s\t%s\t%s\n' "$pid" "$class" "$cmdline" >>"$OUT/processes.tsv"
    printf '%s\t%s\n' "$pid" "$class"

    cat "/proc/$pid/maps" >"$OUT/maps/$pid.maps"

    awk '$NF ~ /^\// { print $NF }' "$OUT/maps/$pid.maps" | sort -u | while IFS= read -r path; do
        [ -n "$path" ] || continue
        path_class=$(classify_path "$path")
        printf '%s\t%s\t%s\t%s\n' "$pid" "$class" "$path_class" "$path" >>"$OUT/mapped-objects.tsv"
    done
done

{
    printf 'path_class\tpath\n'
    awk -F $'\t' 'NR > 1 { print $3 "\t" $4 }' "$OUT/mapped-objects.tsv" | sort -u
} >"$OUT/unique-objects.tsv"

{
    printf 'path_class\tunique_object_count\n'
    awk -F $'\t' 'NR > 1 { count[$1]++ } END { for (c in count) print c "\t" count[c] }' "$OUT/unique-objects.tsv" | sort
} >"$OUT/class-counts.tsv"

{
    printf 'class\tsamples\n'
    awk -F $'\t' 'NR > 1 { count[$4]++ } END { for (c in count) print c "\t" count[c] }' "$OUT/poll-observed.tsv" | sort
} >"$OUT/process-class-observation-counts.tsv"

printf '%s\n' "${!OBSERVED_PIDS[@]}" | sort -n >>"$OUT/observed-pids.tsv"
printf 'PASS\n' >"$OUT/maps-capture.status"

printf '\n===== class counts =====\n'
cat "$OUT/class-counts.tsv"

printf '\n===== process observation counts =====\n'
cat "$OUT/process-class-observation-counts.tsv"

printf '\ncontrol capture: PASS\n'
printf 'evidence: %s\n' "$OUT"
printf 'next: run enrich-control-identities.sh with CONTROL_OUT=%s\n' "$OUT"
