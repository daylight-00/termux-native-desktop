#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

APP=${APP:-$HOME/gl/apps/obsidian}
LAUNCHER=${LAUNCHER:-$HOME/gl/bin/obsidian-app}
ROOTFS=${ROOTFS:-$PREFIX/var/lib/proot-distro/containers/debian/rootfs}
OUT=${OUT:-$PREFIX/tmp/selected-obsidian-control-$(date +%Y%m%d-%H%M%S)}
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

[ -x "$APP/obsidian" ] || {
    printf 'missing Obsidian payload entrypoint: %s\n' "$APP/obsidian" >&2
    exit 1
}

[ -x "$LAUNCHER" ] || {
    printf 'missing Obsidian launcher: %s\n' "$LAUNCHER" >&2
    exit 1
}

existing=$(pgrep -af "$APP/" || true)
if [ -n "$existing" ]; then
    printf 'existing Obsidian AppDir processes detected; close them before control capture:\n' >&2
    printf '%s\n' "$existing" >&2
    exit 1
fi

mkdir -p "$OUT/maps"
printf 'phase\tsample\tpid\tclass\tcmdline\n' >"$OUT/poll-observed.tsv"
printf 'pid\tclass\tcmdline\n' >"$OUT/last-processes.tsv"
printf 'pid\n' >"$OUT/observed-pids.tsv"

printf 'app: %s\n' "$APP" | tee "$OUT/app-path.txt"
printf 'launcher: %s\n' "$LAUNCHER" | tee "$OUT/launcher-path.txt"
printf 'mode: CPU path (GL_GPU=0)\n' | tee "$OUT/mode.txt"
printf 'startup timeout seconds: %s\n' "$STARTUP_TIMEOUT_SECONDS" | tee "$OUT/startup-contract.txt"
printf 'survival seconds: %s\n' "$SURVIVAL_SECONDS" | tee "$OUT/survival-contract.txt"

printf '\n===== launch Obsidian control =====\n'
printf 'Observe the CPU-path window during topology and survival gates.\n'

GL_GPU=0 \
"$LAUNCHER" \
    >"$OUT/launch.stdout" \
    2>"$OUT/launch.stderr" &
LAUNCH_PID=$!
printf '%s\n' "$LAUNCH_PID" >"$OUT/launch.pid"
printf 'launch pid: %s\n' "$LAUNCH_PID"

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

classify_cmdline() {
    local pid=$1 cmdline=$2
    if [ "$pid" = "$LAUNCH_PID" ]; then
        printf 'main\n'
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
    local phase=$1 sample=$2 pid cmdline class
    mapfile -t CURRENT_TREE < <(collect_tree_pids "$LAUNCH_PID")

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
printf 'elapsed seconds: %s\n' "$((SECONDS - startup_started))"

sleep "$TOPOLOGY_SETTLE_SECONDS"

printf '\n===== survival gate =====\n'
printf 'seconds: %s\n' "$SURVIVAL_SECONDS"

survival_started=$SECONDS
survival_deadline=$((survival_started + SURVIVAL_SECONDS))
next_progress=$((survival_started + PROGRESS_INTERVAL_SECONDS))
survival_sample=0

while (( SECONDS < survival_deadline )); do
    if [ ! -d "/proc/$LAUNCH_PID" ]; then
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
    printf 'survival gate: FAIL (FATAL diagnostic observed)\n' >&2
    printf '\n===== fatal diagnostics =====\n' >&2
    grep 'FATAL:' "$OUT/launch.stderr" >&2 || true
    exit 1
fi

[ -d "/proc/$LAUNCH_PID" ] || {
    printf 'survival gate: FAIL (main process absent at final gate)\n' >&2
    exit 1
}

printf 'survival gate: PASS\n'
printf 'elapsed seconds: %s\n' "$((SECONDS - survival_started))"

observe_tree final 1
mapfile -t capture_pids < <(collect_tree_pids "$LAUNCH_PID")

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

printf 'path_class\tpath\tpackage\tversion\tsha256\tbuild_id\n' >"$OUT/object-identities.tsv"

build_id_of() {
    readelf -n "$1" 2>/dev/null | awk '/Build ID:/ && id == "" { id = $3 } END { if (id != "") print id }'
}

while IFS=$'\t' read -r path_class path; do
    [ "$path_class" = path_class ] && continue
    [ -f "$path" ] || continue

    package=UNKNOWN
    version=UNKNOWN

    case "$path_class" in
        PREFIX_GLIBC)
            package=$(dpkg-query -S "$path" 2>/dev/null | awk -F': ' 'NR == 1 { print $1 }' || true)
            [ -n "$package" ] || package=UNOWNED
            if [ "$package" != UNOWNED ]; then
                version=$(dpkg-query -W -f='${Version}' "$package" 2>/dev/null || true)
                [ -n "$version" ] || version=UNKNOWN
            fi
            ;;
        ROOTFS_PROVIDER)
            inside=${path#"$ROOTFS"}
            owner_line=$(proot-distro login debian -- dpkg-query -S "$inside" 2>/dev/null | head -n 1 || true)
            package=$(printf '%s\n' "$owner_line" | sed -E 's/: \/.*$//')
            [ -n "$package" ] || package=UNOWNED
            if [ "$package" != UNOWNED ]; then
                version=$(proot-distro login debian -- dpkg-query -W -f='${Version}' "$package" 2>/dev/null || true)
                [ -n "$version" ] || version=UNKNOWN
            fi
            ;;
        APP_LOCAL)
            package=OBSIDIAN_APPDIR
            version=PAYLOAD_LOCAL
            ;;
    esac

    sha=$(sha256sum "$path" | awk '{print $1}')
    build_id=$(build_id_of "$path")
    [ -n "$build_id" ] || build_id=NONE

    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$path_class" "$path" "$package" "$version" "$sha" "$build_id" >>"$OUT/object-identities.tsv"
done <"$OUT/unique-objects.tsv"

{
    printf 'path_class\tunique_object_count\n'
    awk -F $'\t' 'NR > 1 { count[$1]++ } END { for (c in count) print c "\t" count[c] }' "$OUT/unique-objects.tsv" | sort
} >"$OUT/class-counts.tsv"

{
    printf 'class\tsamples\n'
    awk -F $'\t' 'NR > 1 { count[$4]++ } END { for (c in count) print c "\t" count[c] }' "$OUT/poll-observed.tsv" | sort
} >"$OUT/process-class-observation-counts.tsv"

printf '%s\n' "${!OBSERVED_PIDS[@]}" | sort -n >>"$OUT/observed-pids.tsv"

printf '\n===== class counts =====\n'
cat "$OUT/class-counts.tsv"

printf '\n===== process observation counts =====\n'
cat "$OUT/process-class-observation-counts.tsv"

printf '\ncontrol capture: PASS\n'
printf 'evidence: %s\n' "$OUT"
