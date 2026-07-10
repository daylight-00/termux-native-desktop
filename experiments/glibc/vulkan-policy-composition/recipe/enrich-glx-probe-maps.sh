#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

MAP_OUT=${MAP_OUT:?set MAP_OUT to a GLX probe maps evidence directory}
ROOTFS=${ROOTFS:-$PREFIX/var/lib/proot-distro/containers/debian/rootfs}
INPUT="$MAP_OUT/mapped-paths.real.txt"
OUTPUT="$MAP_OUT/mapped-provider-identities.tsv"
PACKAGE_SUMMARY="$MAP_OUT/mapped-package-summary.tsv"
GRAPHICS="$MAP_OUT/graphics-related-paths.expanded.txt"
WORK="$MAP_OUT/.map-enrichment"

[ -f "$INPUT" ] || {
    printf 'missing mapped path evidence: %s\n' "$INPUT" >&2
    exit 1
}

for command in readelf sha256sum dpkg-query proot-distro awk sort; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

rm -rf "$WORK"
mkdir -p "$WORK"
trap 'rm -rf "$WORK"' EXIT

: >"$WORK/prefix-paths.txt"
: >"$WORK/rootfs-paths.txt"

while IFS= read -r path; do
    case "$path" in
        "$PREFIX/glibc/"*) printf '%s\n' "$path" >>"$WORK/prefix-paths.txt" ;;
        "$ROOTFS/"*) printf '%s\n' "$path" >>"$WORK/rootfs-paths.txt" ;;
    esac
done <"$INPUT"

: >"$WORK/prefix-owners.raw"
: >"$WORK/prefix-versions.raw"
: >"$WORK/rootfs-owners.raw"
: >"$WORK/rootfs-versions.raw"

mapfile -t prefix_paths <"$WORK/prefix-paths.txt"
if [ "${#prefix_paths[@]}" -gt 0 ]; then
    dpkg-query -S -- "${prefix_paths[@]}" \
        >"$WORK/prefix-owners.raw" 2>"$WORK/prefix-owners.stderr" || true

    sed -E 's/: \/.*$//' "$WORK/prefix-owners.raw" | sort -u >"$WORK/prefix-packages.txt"
    mapfile -t prefix_packages <"$WORK/prefix-packages.txt"
    if [ "${#prefix_packages[@]}" -gt 0 ]; then
        dpkg-query -W -f='${binary:Package}\t${Version}\n' \
            "${prefix_packages[@]}" \
            >"$WORK/prefix-versions.raw" 2>"$WORK/prefix-versions.stderr" || true
    fi
fi

mapfile -t rootfs_paths <"$WORK/rootfs-paths.txt"
if [ "${#rootfs_paths[@]}" -gt 0 ]; then
    rootfs_inside=()
    for path in "${rootfs_paths[@]}"; do
        rootfs_inside+=("${path#"$ROOTFS"}")
    done

    proot-distro login debian -- \
        dpkg-query -S -- "${rootfs_inside[@]}" \
        >"$WORK/rootfs-owners.raw" 2>"$WORK/rootfs-owners.stderr" || true

    sed -E 's/: \/.*$//' "$WORK/rootfs-owners.raw" | sort -u >"$WORK/rootfs-packages.txt"
    mapfile -t rootfs_packages <"$WORK/rootfs-packages.txt"
    if [ "${#rootfs_packages[@]}" -gt 0 ]; then
        proot-distro login debian -- \
            dpkg-query -W -f='${binary:Package}\t${Version}\n' \
            "${rootfs_packages[@]}" \
            >"$WORK/rootfs-versions.raw" 2>"$WORK/rootfs-versions.stderr" || true
    fi
fi

declare -A PREFIX_OWNER=()
declare -A PREFIX_VERSION=()
declare -A ROOTFS_OWNER=()
declare -A ROOTFS_VERSION=()

while IFS= read -r line; do
    [ -n "$line" ] || continue
    package=$(printf '%s\n' "$line" | sed -E 's/: \/.*$//')
    path=${line#*: }
    [ -n "${PREFIX_OWNER[$path]:-}" ] || PREFIX_OWNER["$path"]=$package
done <"$WORK/prefix-owners.raw"

while IFS=$'\t' read -r package version; do
    [ -n "$package" ] || continue
    PREFIX_VERSION["$package"]=$version
done <"$WORK/prefix-versions.raw"

while IFS= read -r line; do
    [ -n "$line" ] || continue
    package=$(printf '%s\n' "$line" | sed -E 's/: \/.*$//')
    inside=${line#*: }
    full="$ROOTFS$inside"
    [ -n "${ROOTFS_OWNER[$full]:-}" ] || ROOTFS_OWNER["$full"]=$package
done <"$WORK/rootfs-owners.raw"

while IFS=$'\t' read -r package version; do
    [ -n "$package" ] || continue
    ROOTFS_VERSION["$package"]=$version
done <"$WORK/rootfs-versions.raw"

build_id_of() {
    {
        readelf -n "$1" 2>/dev/null || true
    } | awk '/Build ID:/ && id == "" { id = $3 } END { if (id != "") print id }'
}

soname_of() {
    {
        readelf -d "$1" 2>/dev/null || true
    } | awk '
        /\(SONAME\)/ {
            line = $0
            sub(/^.*\[/, "", line)
            sub(/\].*$/, "", line)
            print line
            exit
        }
    '
}

printf 'path_class\tpath\tpackage\tversion\tsha256\tbuild_id\tsoname\tstate\n' >"$OUTPUT"

while IFS= read -r path; do
    [ -n "$path" ] || continue

    path_class=OTHER
    package=UNKNOWN
    version=UNKNOWN

    case "$path" in
        "$HOME/gl/opt/mesa-glibc-"*)
            path_class=MESA_STORE
            package=MESA_PROVIDER_STORE
            version=PATH_VERSIONED
            ;;
        "$PREFIX/glibc/"*)
            path_class=PREFIX_GLIBC
            package=${PREFIX_OWNER[$path]:-UNOWNED}
            version=${PREFIX_VERSION[$package]:-UNKNOWN}
            ;;
        "$ROOTFS/"*)
            path_class=ROOTFS
            package=${ROOTFS_OWNER[$path]:-UNOWNED}
            version=${ROOTFS_VERSION[$package]:-UNKNOWN}
            ;;
        /dev/*)
            path_class=DEVICE
            package=KERNEL_DEVICE
            version=NOT_APPLICABLE
            ;;
        /memfd:allocation*)
            path_class=RUNTIME_ANON_MEMORY
            package=RUNTIME_MEMORY
            version=NOT_APPLICABLE
            ;;
        "$HOME/.cache/"*)
            path_class=RUNTIME_CACHE
            package=RUNTIME_STATE
            version=NOT_APPLICABLE
            ;;
        "$PREFIX/tmp/tnd-vulkan-policy-composition/"*)
            path_class=EXPERIMENT
            package=EXPERIMENT_BUILD
            version=NOT_APPLICABLE
            ;;
    esac

    if [ "$path_class" = RUNTIME_ANON_MEMORY ]; then
        state=RUNTIME_ANONYMOUS_MAPPING
        sha=NOT_APPLICABLE
        build_id=NOT_APPLICABLE
        soname=NOT_APPLICABLE
    elif [ -f "$path" ]; then
        state=PRESENT
        sha=$(sha256sum "$path" | awk '{print $1}')
        build_id=$(build_id_of "$path")
        [ -n "$build_id" ] || build_id=NONE
        soname=$(soname_of "$path")
        [ -n "$soname" ] || soname=NONE
    elif [ -c "$path" ] || [ -b "$path" ]; then
        state=DEVICE_NODE
        sha=NOT_APPLICABLE
        build_id=NOT_APPLICABLE
        soname=NOT_APPLICABLE
    else
        state=PRESENT_NONREGULAR_OR_VANISHED
        sha=NOT_APPLICABLE
        build_id=NOT_APPLICABLE
        soname=NOT_APPLICABLE
    fi

    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$path_class" "$path" "$package" "$version" "$sha" "$build_id" "$soname" "$state" \
        >>"$OUTPUT"
done <"$INPUT"

{
    printf 'path_class\tpackage\tversion\tobject_count\n'
    awk -F $'\t' '
        NR > 1 {
            key = $1 "\t" $3 "\t" $4
            count[key]++
        }
        END {
            for (k in count)
                print k "\t" count[k]
        }
    ' "$OUTPUT" | sort
} >"$PACKAGE_SUMMARY"

awk -F $'\t' 'NR > 1 { lower = tolower($2); if ($2 ~ /libGL/ || lower ~ /libgallium/ || lower ~ /zink/ || lower ~ /vulkan/ || lower ~ /mesa/ || lower ~ /\/dri\// || lower ~ /libdrm/ || lower ~ /libgbm/ || lower ~ /xcb-dri/ || lower ~ /kgsl/) print $0 }' \
    "$OUTPUT" >"$GRAPHICS"

printf 'GLX probe map enrichment: PASS\n'
printf 'output: %s\n' "$OUTPUT"
printf 'package summary: %s\n' "$PACKAGE_SUMMARY"
printf 'expanded graphics set: %s\n' "$GRAPHICS"

printf '\n===== package summary =====\n'
cat "$PACKAGE_SUMMARY"

printf '\n===== expanded graphics set =====\n'
cat "$GRAPHICS"
