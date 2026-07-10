#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

STRICT_OUT=${STRICT_OUT:?set STRICT_OUT to the strict CPU control evidence directory}
SEMANTIC="$STRICT_OUT/semantic-objects.tsv"
OUT=${OUT:-$STRICT_OUT/fallback-provider-closures}
ROOTFS=${ROOTFS:-$PREFIX/var/lib/proot-distro/containers/debian/rootfs}

APP_SWIFTSHADER=${APP_SWIFTSHADER:-$HOME/gl/apps/obsidian/libvk_swiftshader.so}
ROOTFS_LVP=${ROOTFS_LVP:-$ROOTFS/usr/lib/aarch64-linux-gnu/libvulkan_lvp.so}
ROOTFS_GFXSTREAM=${ROOTFS_GFXSTREAM:-$ROOTFS/usr/lib/aarch64-linux-gnu/libvulkan_gfxstream.so}

[ -f "$SEMANTIC" ] || {
    printf 'missing semantic evidence: %s\n' "$SEMANTIC" >&2
    exit 1
}

for command in readelf awk sort comm sha256sum; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

rm -rf "$OUT"
mkdir -p "$OUT/dynamic"

UNIVERSE="$OUT/elf-universe.tsv"
INDEX="$OUT/soname-index.tsv"
GRAPH="$OUT/graph.tsv"
REACHABLE="$OUT/reachable.tsv"
ATTRIBUTION="$OUT/strict-only-attribution.tsv"

printf 'semantic_class\tpath_class\tpath\tpackage\tversion\tbuild_id\n' >"$UNIVERSE"
awk -F $'\t' '
    NR > 1 && $7 != "NONE" && $7 != "MISSING" && $7 != "NOT_APPLICABLE" && $8 == "PRESENT" {
        print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $7
    }
' "$SEMANTIC" >>"$UNIVERSE"

printf 'soname\tpath\tsemantic_class\tpath_class\tpackage\tversion\tbuild_id\n' >"$INDEX"

while IFS=$'\t' read -r semantic_class path_class path package version build_id; do
    [ "$semantic_class" = semantic_class ] && continue
    [ -f "$path" ] || continue

    key=$(printf '%s' "$path" | sha256sum | awk '{print $1}')
    dynamic="$OUT/dynamic/$key.txt"
    readelf -d "$path" >"$dynamic" 2>/dev/null || true

    soname=$(awk '
        /\(SONAME\)/ {
            line = $0
            sub(/^.*\[/, "", line)
            sub(/\].*$/, "", line)
            print line
            exit
        }
    ' "$dynamic")

    [ -n "$soname" ] || soname=$(basename "$path")

    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$soname" "$path" "$semantic_class" "$path_class" \
        "$package" "$version" "$build_id" \
        >>"$INDEX"
done <"$UNIVERSE"

sort -u "$INDEX" -o "$INDEX"

printf 'root_label\tconsumer\tneeded\tresolution\tselected_path\tselected_class\n' >"$GRAPH"
printf 'root_label\tpath\tsemantic_class\n' >"$REACHABLE"

trace_root() {
    local label=$1 root=$2
    local current dynamic needed match_count selected selected_class
    local -a queue=()
    local -A seen=()

    [ -f "$root" ] || {
        printf 'missing fallback root %s: %s\n' "$label" "$root" >&2
        return 1
    }

    queue+=("$root")

    while [ "${#queue[@]}" -gt 0 ]; do
        current=${queue[0]}
        queue=("${queue[@]:1}")

        [ -n "${seen[$current]:-}" ] && continue
        seen["$current"]=1

        selected_class=$(awk -F $'\t' -v p="$current" 'NR > 1 && $2 == p { print $3; exit }' "$INDEX")
        [ -n "$selected_class" ] || selected_class=UNKNOWN
        printf '%s\t%s\t%s\n' "$label" "$current" "$selected_class" >>"$REACHABLE"

        key=$(printf '%s' "$current" | sha256sum | awk '{print $1}')
        dynamic="$OUT/dynamic/$key.txt"
        if [ ! -f "$dynamic" ]; then
            readelf -d "$current" >"$dynamic" 2>/dev/null || true
        fi

        while IFS= read -r needed; do
            [ -n "$needed" ] || continue

            match_count=$(awk -F $'\t' -v n="$needed" 'NR > 1 && $1 == n { count++ } END { print count + 0 }' "$INDEX")

            case "$match_count" in
                0)
                    printf '%s\t%s\t%s\tUNRESOLVED\t\t\n' \
                        "$label" "$current" "$needed" \
                        >>"$GRAPH"
                    ;;
                1)
                    selected=$(awk -F $'\t' -v n="$needed" 'NR > 1 && $1 == n { print $2; exit }' "$INDEX")
                    selected_class=$(awk -F $'\t' -v n="$needed" 'NR > 1 && $1 == n { print $3; exit }' "$INDEX")
                    printf '%s\t%s\t%s\tMAPPED_UNIQUE\t%s\t%s\n' \
                        "$label" "$current" "$needed" "$selected" "$selected_class" \
                        >>"$GRAPH"
                    queue+=("$selected")
                    ;;
                *)
                    printf '%s\t%s\t%s\tAMBIGUOUS_MAPPED_SONAME\t\t\n' \
                        "$label" "$current" "$needed" \
                        >>"$GRAPH"
                    ;;
            esac
        done < <(
            awk '
                /\(NEEDED\)/ {
                    line = $0
                    sub(/^.*\[/, "", line)
                    sub(/\].*$/, "", line)
                    print line
                }
            ' "$dynamic"
        )
    done
}

trace_root swiftshader "$APP_SWIFTSHADER"
trace_root lvp "$ROOTFS_LVP"
trace_root gfxstream "$ROOTFS_GFXSTREAM"

{
    head -n 1 "$GRAPH"
    tail -n +2 "$GRAPH" | sort -u
} >"$GRAPH.tmp"
mv "$GRAPH.tmp" "$GRAPH"

{
    head -n 1 "$REACHABLE"
    tail -n +2 "$REACHABLE" | sort -u
} >"$REACHABLE.tmp"
mv "$REACHABLE.tmp" "$REACHABLE"

STRICT_ONLY="$STRICT_OUT/control-semantic-set-comparison/strict-only-paths.txt"
if [ -f "$STRICT_ONLY" ]; then
    printf 'path\tswiftshader\tlvp\tgfxstream\n' >"$ATTRIBUTION"
    while IFS= read -r path; do
        [ -n "$path" ] || continue
        swiftshader=0
        lvp=0
        gfxstream=0
        grep -F -q $'swiftshader\t'"$path"$'\t' "$REACHABLE" && swiftshader=1 || true
        grep -F -q $'lvp\t'"$path"$'\t' "$REACHABLE" && lvp=1 || true
        grep -F -q $'gfxstream\t'"$path"$'\t' "$REACHABLE" && gfxstream=1 || true
        printf '%s\t%s\t%s\t%s\n' "$path" "$swiftshader" "$lvp" "$gfxstream" >>"$ATTRIBUTION"
    done <"$STRICT_ONLY"
else
    printf 'path\tswiftshader\tlvp\tgfxstream\n' >"$ATTRIBUTION"
fi

unresolved=$(awk -F $'\t' 'NR > 1 && $4 == "UNRESOLVED" { count++ } END { print count + 0 }' "$GRAPH")
ambiguous=$(awk -F $'\t' 'NR > 1 && $4 == "AMBIGUOUS_MAPPED_SONAME" { count++ } END { print count + 0 }' "$GRAPH")

printf '\nfallback provider closure discovery: PASS\n'
printf 'unresolved edges: %s\n' "$unresolved"
printf 'ambiguous mapped SONAME edges: %s\n' "$ambiguous"
printf 'output: %s\n' "$OUT"

printf '\n===== strict-only attribution =====\n'
cat "$ATTRIBUTION"

printf '\n===== unresolved or ambiguous edges =====\n'
awk -F $'\t' 'NR == 1 || $4 == "UNRESOLVED" || $4 == "AMBIGUOUS_MAPPED_SONAME" { print }' "$GRAPH"
