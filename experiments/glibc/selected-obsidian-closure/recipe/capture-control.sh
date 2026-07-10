#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

APP=${APP:-$HOME/gl/apps/obsidian}
LAUNCHER=${LAUNCHER:-$HOME/gl/bin/obsidian-app}
ROOTFS=${ROOTFS:-$PREFIX/var/lib/proot-distro/containers/debian/rootfs}
OUT=${OUT:-$PREFIX/tmp/selected-obsidian-control-$(date +%Y%m%d-%H%M%S)}
STARTUP_TIMEOUT_SECONDS=${STARTUP_TIMEOUT_SECONDS:-30}
STABLE_SETTLE_SECONDS=${STABLE_SETTLE_SECONDS:-5}

for command in pgrep readelf sha256sum file dpkg-query proot-distro; do
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

existing=$(pgrep -af "$APP/(obsidian|chrome_crashpad_handler)" || true)
if [ -n "$existing" ]; then
    printf 'existing Obsidian AppDir processes detected; close them before control capture:\n' >&2
    printf '%s\n' "$existing" >&2
    exit 1
fi

mkdir -p "$OUT/maps"

printf 'app: %s\n' "$APP" | tee "$OUT/app-path.txt"
printf 'launcher: %s\n' "$LAUNCHER" | tee "$OUT/launcher-path.txt"
printf 'mode: CPU path (GL_GPU=0)\n' | tee "$OUT/mode.txt"

printf '\n===== launch Obsidian control =====\n'
printf 'Observe the CPU-path window during the startup interval.\n'

GL_GPU=0 \
"$LAUNCHER" \
    >"$OUT/launch.stdout" \
    2>"$OUT/launch.stderr" &
LAUNCH_PID=$!
printf '%s\n' "$LAUNCH_PID" >"$OUT/launch.pid"
printf 'launch pid: %s\n' "$LAUNCH_PID"

cleanup_pids=()
cleanup() {
    local pid
    for pid in "${cleanup_pids[@]:-}"; do
        [ -n "$pid" ] || continue
        kill -TERM "$pid" 2>/dev/null || true
    done
    sleep 1
    for pid in "${cleanup_pids[@]:-}"; do
        [ -n "$pid" ] || continue
        kill -KILL "$pid" 2>/dev/null || true
    done
}
trap cleanup EXIT

classify_cmdline() {
    local cmdline=$1
    case "$cmdline" in
        *chrome_crashpad_handler*) printf 'crashpad\n' ;;
        *--type=renderer*) printf 'renderer\n' ;;
        *--type=utility*) printf 'utility\n' ;;
        *--type=gpu-process*) printf 'gpu\n' ;;
        *--type=zygote*) printf 'zygote\n' ;;
        *) printf 'main\n' ;;
    esac
}

stable=0
for _ in $(seq 1 $((STARTUP_TIMEOUT_SECONDS * 2))); do
    mapfile -t current_pids < <(
        pgrep -f "$APP/(obsidian|chrome_crashpad_handler)" 2>/dev/null \
            | sort -n \
            || true
    )

    have_main=0
    have_renderer=0
    have_utility=0

    for pid in "${current_pids[@]:-}"; do
        [ -r "/proc/$pid/cmdline" ] || continue
        cmdline=$(tr '\0' ' ' <"/proc/$pid/cmdline")
        class=$(classify_cmdline "$cmdline")
        case "$class" in
            main) have_main=1 ;;
            renderer) have_renderer=1 ;;
            utility) have_utility=1 ;;
        esac
    done

    if [ "$have_main" -eq 1 ] && [ "$have_renderer" -eq 1 ] && [ "$have_utility" -eq 1 ]; then
        stable=1
        break
    fi

    sleep 0.5
done

if [ "$stable" -ne 1 ]; then
    printf 'required process classes did not stabilize before timeout\n' >&2
    printf '\n===== stderr =====\n' >&2
    sed -n '1,200p' "$OUT/launch.stderr" >&2 || true
    exit 1
fi

sleep "$STABLE_SETTLE_SECONDS"

mapfile -t capture_pids < <(
    pgrep -f "$APP/(obsidian|chrome_crashpad_handler)" 2>/dev/null \
        | sort -n \
        || true
)

[ "${#capture_pids[@]}" -gt 0 ] || {
    printf 'no Obsidian process remained for capture\n' >&2
    exit 1
}

cleanup_pids=("${capture_pids[@]}")

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

printf '\n===== stable process set =====\n'
for pid in "${capture_pids[@]}"; do
    [ -r "/proc/$pid/cmdline" ] || continue
    [ -r "/proc/$pid/maps" ] || continue

    cmdline=$(tr '\0' ' ' <"/proc/$pid/cmdline")
    class=$(classify_cmdline "$cmdline")

    printf '%s\t%s\t%s\n' "$pid" "$class" "$cmdline" \
        >>"$OUT/processes.tsv"
    printf '%s\t%s\n' "$pid" "$class"

    cat "/proc/$pid/maps" >"$OUT/maps/$pid.maps"

    awk '$NF ~ /^\// { print $NF }' "$OUT/maps/$pid.maps" \
        | sort -u \
        | while IFS= read -r path; do
            [ -n "$path" ] || continue
            path_class=$(classify_path "$path")
            printf '%s\t%s\t%s\t%s\n' \
                "$pid" "$class" "$path_class" "$path" \
                >>"$OUT/mapped-objects.tsv"
        done
done

{
    printf 'path_class\tpath\n'
    awk -F $'\t' 'NR > 1 { print $3 "\t" $4 }' "$OUT/mapped-objects.tsv" \
        | sort -u
} >"$OUT/unique-objects.tsv"

printf 'path_class\tpath\tpackage\tversion\tsha256\tbuild_id\n' \
    >"$OUT/object-identities.tsv"

build_id_of() {
    readelf -n "$1" 2>/dev/null \
        | awk '
            /Build ID:/ && id == "" { id = $3 }
            END { if (id != "") print id }
        '
}

while IFS=$'\t' read -r path_class path; do
    [ "$path_class" = path_class ] && continue
    [ -f "$path" ] || continue

    package=UNKNOWN
    version=UNKNOWN

    case "$path_class" in
        PREFIX_GLIBC)
            package=$(dpkg-query -S "$path" 2>/dev/null \
                | awk -F': ' 'NR == 1 { print $1 }' || true)
            [ -n "$package" ] || package=UNOWNED
            if [ "$package" != UNOWNED ]; then
                version=$(dpkg-query -W -f='${Version}' "$package" 2>/dev/null || true)
                [ -n "$version" ] || version=UNKNOWN
            fi
            ;;
        ROOTFS_PROVIDER)
            inside=${path#"$ROOTFS"}
            owner_line=$(proot-distro login debian -- \
                dpkg-query -S "$inside" 2>/dev/null \
                | head -n 1 || true)
            package=$(printf '%s\n' "$owner_line" | sed -E 's/: \/.*$//')
            [ -n "$package" ] || package=UNOWNED
            if [ "$package" != UNOWNED ]; then
                version=$(proot-distro login debian -- \
                    dpkg-query -W -f='${Version}' "$package" 2>/dev/null || true)
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

    printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$path_class" "$path" "$package" "$version" "$sha" "$build_id" \
        >>"$OUT/object-identities.tsv"
done <"$OUT/unique-objects.tsv"

{
    printf 'path_class\tunique_object_count\n'
    awk -F $'\t' 'NR > 1 { count[$1]++ } END { for (c in count) print c "\t" count[c] }' \
        "$OUT/unique-objects.tsv" \
        | sort
} >"$OUT/class-counts.tsv"

printf '\n===== class counts =====\n'
cat "$OUT/class-counts.tsv"

printf '\n===== required process classes =====\n'
for required in main renderer utility; do
    if awk -F $'\t' -v c="$required" 'NR > 1 && $2 == c { found=1 } END { exit !found }' \
        "$OUT/processes.tsv"; then
        printf '%s: PASS\n' "$required"
    else
        printf '%s: FAIL\n' "$required" >&2
        exit 1
    fi
done

printf '\ncontrol capture: PASS\n'
printf 'evidence: %s\n' "$OUT"
