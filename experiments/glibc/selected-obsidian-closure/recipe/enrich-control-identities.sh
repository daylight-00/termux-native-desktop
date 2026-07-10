#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

CONTROL_OUT=${CONTROL_OUT:?set CONTROL_OUT to a completed Obsidian control evidence directory}
ROOTFS=${ROOTFS:-$PREFIX/var/lib/proot-distro/containers/debian/rootfs}

UNIQUE="$CONTROL_OUT/unique-objects.tsv"
OUTPUT="$CONTROL_OUT/object-identities.tsv"
WORK="$CONTROL_OUT/.identity-enrichment"

[ -f "$UNIQUE" ] || {
    printf 'missing control unique-object evidence: %s\n' "$UNIQUE" >&2
    exit 1
}

for command in readelf sha256sum dpkg-query proot-distro; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

rm -rf "$WORK"
mkdir -p "$WORK"
trap 'rm -rf "$WORK"' EXIT

awk -F $'\t' 'NR > 1 && $1 == "PREFIX_GLIBC" { print $2 }' "$UNIQUE" >"$WORK/prefix-paths.txt"
awk -F $'\t' 'NR > 1 && $1 == "ROOTFS_PROVIDER" { print $2 }' "$UNIQUE" >"$WORK/rootfs-paths.txt"

: >"$WORK/prefix-owners.raw"
: >"$WORK/prefix-versions.raw"
: >"$WORK/rootfs-owners.raw"
: >"$WORK/rootfs-versions.raw"

mapfile -t prefix_paths <"$WORK/prefix-paths.txt"
if [ "${#prefix_paths[@]}" -gt 0 ]; then
    dpkg-query -S -- "${prefix_paths[@]}" \
        >"$WORK/prefix-owners.raw" 2>"$WORK/prefix-owners.stderr" \
        || true

    sed -E 's/: \/.*$//' "$WORK/prefix-owners.raw" \
        | sort -u \
        >"$WORK/prefix-packages.txt"

    mapfile -t prefix_packages <"$WORK/prefix-packages.txt"
    if [ "${#prefix_packages[@]}" -gt 0 ]; then
        dpkg-query -W -f='${binary:Package}\t${Version}\n' \
            "${prefix_packages[@]}" \
            >"$WORK/prefix-versions.raw" 2>"$WORK/prefix-versions.stderr" \
            || true
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
        >"$WORK/rootfs-owners.raw" 2>"$WORK/rootfs-owners.stderr" \
        || true

    sed -E 's/: \/.*$//' "$WORK/rootfs-owners.raw" \
        | sort -u \
        >"$WORK/rootfs-packages.txt"

    mapfile -t rootfs_packages <"$WORK/rootfs-packages.txt"
    if [ "${#rootfs_packages[@]}" -gt 0 ]; then
        proot-distro login debian -- \
            dpkg-query -W -f='${binary:Package}\t${Version}\n' \
            "${rootfs_packages[@]}" \
            >"$WORK/rootfs-versions.raw" 2>"$WORK/rootfs-versions.stderr" \
            || true
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
    } | awk '
        /Build ID:/ && id == "" { id = $3 }
        END { if (id != "") print id }
    '
}

printf 'path_class\tpath\tpackage\tversion\tsha256\tbuild_id\tstate\n' >"$OUTPUT"

count=0
while IFS=$'\t' read -r path_class path; do
    [ "$path_class" = path_class ] && continue

    package=UNKNOWN
    version=UNKNOWN

    case "$path_class" in
        APP_LOCAL)
            package=OBSIDIAN_APPDIR
            version=PAYLOAD_LOCAL
            ;;
        PREFIX_GLIBC)
            package=${PREFIX_OWNER[$path]:-UNOWNED}
            version=${PREFIX_VERSION[$package]:-UNKNOWN}
            ;;
        ROOTFS_PROVIDER)
            package=${ROOTFS_OWNER[$path]:-UNOWNED}
            version=${ROOTFS_VERSION[$package]:-UNKNOWN}
            ;;
    esac

    if [ -f "$path" ]; then
        state=PRESENT
        sha=$(sha256sum "$path" | awk '{print $1}')
        build_id=$(build_id_of "$path")
        [ -n "$build_id" ] || build_id=NONE
    else
        state=MISSING_AT_ENRICHMENT
        sha=MISSING
        build_id=MISSING
    fi

    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$path_class" "$path" "$package" "$version" \
        "$sha" "$build_id" "$state" \
        >>"$OUTPUT"

    count=$((count + 1))
done <"$UNIQUE"

expected=$(( $(wc -l <"$UNIQUE") - 1 ))
actual=$(( $(wc -l <"$OUTPUT") - 1 ))

if [ "$actual" -ne "$expected" ]; then
    printf 'identity coverage mismatch: expected %s, wrote %s\n' "$expected" "$actual" >&2
    exit 1
fi

printf 'PASS\n' >"$CONTROL_OUT/identity-enrichment.status"

printf '\nidentity enrichment: PASS\n'
printf 'objects recorded: %s\n' "$count"
printf 'coverage: %s/%s\n' "$actual" "$expected"
printf 'output: %s\n' "$OUTPUT"
