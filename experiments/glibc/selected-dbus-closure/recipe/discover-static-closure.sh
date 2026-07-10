#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

FARM=${FARM:-$HOME/gl/lib}
ROOTFS=${ROOTFS:-$PREFIX/var/lib/proot-distro/containers/debian/rootfs}
ROOT=${ROOT:-$FARM/libdbus-1.so.3}
OUT=${OUT:-$PREFIX/tmp/selected-dbus-static-$(date +%Y%m%d-%H%M%S)}
PROTECTED_WORLD_PACKAGES=${PROTECTED_WORLD_PACKAGES:-glibc}

mkdir -p "$OUT"

for command in readelf sha256sum readlink proot-distro dpkg-query; do
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
printf 'path\tpackage\tversion\tsha256\tbuild_id\n' >"$OUT/prefix-providers.tsv"
printf 'path\tpackage\tversion\tsha256\tbuild_id\n' >"$OUT/world-prefix.tsv"

queue=("$ROOT")
declare -A seen=()
declare -A provider_recorded=()
declare -A prefix_provider_recorded=()
declare -A world_recorded=()

build_id_of() {
    readelf -n "$1" 2>/dev/null \
        | awk '
            /Build ID:/ && id == "" { id = $3 }
            END { if (id != "") print id }
        '
}

host_owner_of() {
    local path=$1
    dpkg-query -S "$path" 2>/dev/null \
        | awk -F': ' 'NR == 1 { print $1 }'
}

host_version_of() {
    local package=$1
    dpkg-query -W -f='${Version}' "$package" 2>/dev/null || true
}

is_protected_world_package() {
    local package=$1 protected
    for protected in $PROTECTED_WORLD_PACKAGES; do
        [ "$package" = "$protected" ] && return 0
    done
    return 1
}

record_rootfs_provider() {
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

record_prefix_provider() {
    local path=$1
    [ -n "${prefix_provider_recorded[$path]:-}" ] && return 0
    prefix_provider_recorded[$path]=1

    local package version sha build_id
    package=$(host_owner_of "$path")
    [ -n "$package" ] || package=UNOWNED
    version=$(host_version_of "$package")
    [ -n "$version" ] || version=UNKNOWN
    sha=$(sha256sum "$path" | awk '{print $1}')
    build_id=$(build_id_of "$path")
    [ -n "$build_id" ] || build_id=NONE

    printf '%s\t%s\t%s\t%s\t%s\n' \
        "$path" "$package" "$version" "$sha" "$build_id" \
        >>"$OUT/prefix-providers.tsv"
}

record_world() {
    local path=$1 package=$2
    [ -n "${world_recorded[$path]:-}" ] && return 0
    world_recorded[$path]=1

    local version sha build_id
    version=$(host_version_of "$package")
    [ -n "$version" ] || version=UNKNOWN
    sha=$(sha256sum "$path" | awk '{print $1}')
    build_id=$(build_id_of "$path")
    [ -n "$build_id" ] || build_id=NONE

    printf '%s\t%s\t%s\t%s\t%s\n' \
        "$path" "$package" "$version" "$sha" "$build_id" \
        >>"$OUT/world-prefix.tsv"
}

record_rootfs_provider "$ROOT"

index=0
while [ "$index" -lt "${#queue[@]}" ]; do
    consumer=${queue[$index]}
    index=$((index + 1))

    [ -n "${seen[$consumer]:-}" ] && continue
    seen[$consumer]=1

    while IFS= read -r needed; do
        [ -n "$needed" ] || continue

        farm_selected=
        prefix_selected=
        prefix_package=

        if [ -e "$FARM/$needed" ]; then
            farm_selected=$(readlink -f "$FARM/$needed")
        fi

        if [ -e "$PREFIX/glibc/lib/$needed" ]; then
            prefix_selected=$(readlink -f "$PREFIX/glibc/lib/$needed")
            prefix_package=$(host_owner_of "$prefix_selected")
        fi

        if [ -n "$farm_selected" ]; then
            if [ -n "$prefix_selected" ] && \
               [ -n "$prefix_package" ] && \
               is_protected_world_package "$prefix_package"; then
                printf '%s\t%s\tREJECTED_SHADOWS_WORLD\t%s\tfarm-first control would shadow protected package %s at %s\n' \
                    "$consumer" "$needed" "$farm_selected" "$prefix_package" "$prefix_selected" \
                    >>"$OUT/graph.tsv"
                continue
            fi

            case "$farm_selected" in
                "$ROOTFS"/*)
                    printf '%s\t%s\tPROVIDER_ROOTFS\t%s\tfarm-first control target\n' \
                        "$consumer" "$needed" "$farm_selected" \
                        >>"$OUT/graph.tsv"
                    record_rootfs_provider "$farm_selected"
                    queue+=("$farm_selected")
                    ;;
                *)
                    printf '%s\t%s\tREJECTED_NON_ROOTFS_CONTROL\t%s\tcontrol target outside configured rootfs\n' \
                        "$consumer" "$needed" "$farm_selected" \
                        >>"$OUT/graph.tsv"
                    ;;
            esac
            continue
        fi

        if [ -n "$prefix_selected" ]; then
            if [ -n "$prefix_package" ] && is_protected_world_package "$prefix_package"; then
                printf '%s\t%s\tWORLD_SUBSTRATE\t%s\tprotected package owner %s\n' \
                    "$consumer" "$needed" "$prefix_selected" "$prefix_package" \
                    >>"$OUT/graph.tsv"
                record_world "$prefix_selected" "$prefix_package"
            else
                printf '%s\t%s\tPROVIDER_PREFIX\t%s\tprefix provider owner %s\n' \
                    "$consumer" "$needed" "$prefix_selected" "${prefix_package:-UNOWNED}" \
                    >>"$OUT/graph.tsv"
                record_prefix_provider "$prefix_selected"
                queue+=("$prefix_selected")
            fi
            continue
        fi

        printf '%s\t%s\tUNRESOLVED\t-\tno farm-first control target or prefix exact-name match\n' \
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

printf '\n===== prefix providers =====\n'
column -t -s $'\t' "$OUT/prefix-providers.tsv" 2>/dev/null || cat "$OUT/prefix-providers.tsv"

printf '\n===== protected world substrate objects =====\n'
column -t -s $'\t' "$OUT/world-prefix.tsv" 2>/dev/null || cat "$OUT/world-prefix.tsv"

if grep -q $'\tUNRESOLVED\t' "$OUT/graph.tsv"; then
    printf '\nstatic closure discovery: FAIL (unresolved edge)\n' >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
fi

if grep -qE $'\t(REJECTED_NON_ROOTFS_CONTROL|REJECTED_SHADOWS_WORLD)\t' "$OUT/graph.tsv"; then
    printf '\nstatic closure discovery: FAIL (rejected control selection)\n' >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
fi

printf '\nstatic closure discovery: PASS\n'
printf 'evidence: %s\n' "$OUT"
