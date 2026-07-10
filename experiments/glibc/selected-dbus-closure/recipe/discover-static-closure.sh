#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

FARM=${FARM:-$HOME/gl/lib}
ROOTFS=${ROOTFS:-$PREFIX/var/lib/proot-distro/containers/debian/rootfs}
ROOT=${ROOT:-$FARM/libdbus-1.so.3}
OUT=${OUT:-$PREFIX/tmp/selected-dbus-static-$(date +%Y%m%d-%H%M%S)}

mkdir -p "$OUT"

for command in readelf sha256sum readlink proot-distro; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

ROOT=$(readlink -f "$ROOT")
case "$ROOT" in
    "$ROOTFS"/*) ;;
    *)
        printf 'root provider is not inside configured rootfs: %s\n' "$ROOT" >&2
        exit 1
        ;;
esac

printf 'consumer\tneeded\tclassification\tselected_path\tselection_reason\n' >"$OUT/graph.tsv"
printf 'path\tpackage\tversion\tsha256\tbuild_id\n' >"$OUT/providers.tsv"
printf 'path\tsha256\tbuild_id\n' >"$OUT/world-prefix.tsv"

queue=("$ROOT")
declare -A seen=()
declare -A provider_recorded=()
declare -A world_recorded=()

build_id_of() {
    readelf -n "$1" 2>/dev/null \
        | awk '
            /Build ID:/ && id == "" { id = $3 }
            END { if (id != "") print id }
        '
}

record_provider() {
    local path=$1
    [ -n "${provider_recorded[$path]:-}" ] && return 0
    provider_recorded[$path]=1

    local inside=${path#"$ROOTFS"}
    local owner_line package version sha build_id

    owner_line=$(proot-distro login debian -- dpkg-query -S "$inside" 2>/dev/null | head -n 1 || true)
    package=$(printf '%s\n' "$owner_line" | sed -E 's/: \/.*$//')

    if [ -n "$package" ]; then
        version=$(proot-distro login debian -- \
            dpkg-query -W -f='${Version}' "$package" 2>/dev/null || true)
    else
        package=UNOWNED
        version=UNKNOWN
    fi

    sha=$(sha256sum "$path" | awk '{print $1}')
    build_id=$(build_id_of "$path")
    [ -n "$build_id" ] || build_id=NONE

    printf '%s\t%s\t%s\t%s\t%s\n' \
        "$path" "$package" "$version" "$sha" "$build_id" \
        >>"$OUT/providers.tsv"
}

record_world() {
    local path=$1
    [ -n "${world_recorded[$path]:-}" ] && return 0
    world_recorded[$path]=1

    local sha build_id
    sha=$(sha256sum "$path" | awk '{print $1}')
    build_id=$(build_id_of "$path")
    [ -n "$build_id" ] || build_id=NONE

    printf '%s\t%s\t%s\n' "$path" "$sha" "$build_id" \
        >>"$OUT/world-prefix.tsv"
}

record_provider "$ROOT"

index=0
while [ "$index" -lt "${#queue[@]}" ]; do
    consumer=${queue[$index]}
    index=$((index + 1))

    [ -n "${seen[$consumer]:-}" ] && continue
    seen[$consumer]=1

    while IFS= read -r needed; do
        [ -n "$needed" ] || continue

        if [ -e "$PREFIX/glibc/lib/$needed" ]; then
            selected=$(readlink -f "$PREFIX/glibc/lib/$needed")
            printf '%s\t%s\tWORLD_PREFIX\t%s\tprefix exact-name match\n' \
                "$consumer" "$needed" "$selected" \
                >>"$OUT/graph.tsv"
            record_world "$selected"
            continue
        fi

        if [ -e "$FARM/$needed" ]; then
            selected=$(readlink -f "$FARM/$needed")
            case "$selected" in
                "$ROOTFS"/*)
                    printf '%s\t%s\tPROVIDER_ROOTFS\t%s\tactive broad-farm control target\n' \
                        "$consumer" "$needed" "$selected" \
                        >>"$OUT/graph.tsv"
                    record_provider "$selected"
                    queue+=("$selected")
                    ;;
                *)
                    printf '%s\t%s\tREJECTED_NON_ROOTFS_CONTROL\t%s\tcontrol target outside configured rootfs\n' \
                        "$consumer" "$needed" "$selected" \
                        >>"$OUT/graph.tsv"
                    ;;
            esac
            continue
        fi

        printf '%s\t%s\tUNRESOLVED\t-\tno prefix exact-name or broad-farm control match\n' \
            "$consumer" "$needed" \
            >>"$OUT/graph.tsv"

    done < <(
        readelf -d "$consumer" 2>/dev/null \
            | sed -n 's/.*Shared library: \[\(.*\)\]/\1/p'
    )
done

printf '\n===== graph =====\n'
column -t -s $'\t' "$OUT/graph.tsv" 2>/dev/null || cat "$OUT/graph.tsv"

printf '\n===== rootfs providers =====\n'
column -t -s $'\t' "$OUT/providers.tsv" 2>/dev/null || cat "$OUT/providers.tsv"

printf '\n===== world-prefix objects =====\n'
column -t -s $'\t' "$OUT/world-prefix.tsv" 2>/dev/null || cat "$OUT/world-prefix.tsv"

if grep -q $'\tUNRESOLVED\t' "$OUT/graph.tsv"; then
    printf '\nstatic closure discovery: FAIL (unresolved edge)\n' >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
fi

if grep -q $'\tREJECTED_NON_ROOTFS_CONTROL\t' "$OUT/graph.tsv"; then
    printf '\nstatic closure discovery: FAIL (unexpected control target)\n' >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
fi

printf '\nstatic closure discovery: PASS\n'
printf 'evidence: %s\n' "$OUT"
