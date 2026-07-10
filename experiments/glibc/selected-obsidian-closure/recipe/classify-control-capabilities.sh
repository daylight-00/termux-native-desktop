#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

CONTROL_OUT=${CONTROL_OUT:?set CONTROL_OUT to an enriched Obsidian control evidence directory}
INPUT="$CONTROL_OUT/object-identities.tsv"
OUTPUT="$CONTROL_OUT/semantic-objects.tsv"
COUNTS="$CONTROL_OUT/semantic-counts.tsv"
REVIEW="$CONTROL_OUT/semantic-review.tsv"

[ -f "$INPUT" ] || {
    printf 'missing identity evidence: %s\n' "$INPUT" >&2
    exit 1
}

printf 'semantic_class\tpath_class\tpath\tpackage\tversion\tsha256\tbuild_id\tstate\n' >"$OUTPUT"

classify() {
    local path_class=$1 path=$2 package=$3 build_id=$4 state=$5

    if [ "$state" = MISSING_AT_ENRICHMENT ]; then
        printf 'MISSING_AT_ENRICHMENT\n'
        return 0
    fi

    case "$path_class" in
        APP_LOCAL)
            if [ "$build_id" = NONE ]; then
                printf 'APP_LOCAL_DATA\n'
            else
                printf 'APP_LOCAL_ELF\n'
            fi
            ;;

        PREFIX_GLIBC)
            if [ "$package" = glibc ] && [[ "$path" == */locale/* ]]; then
                printf 'PROVIDER_LOCALE_DATA\n'
            elif [ "$package" = glibc ] && [ "$build_id" != NONE ]; then
                printf 'WORLD_SUBSTRATE_ELF\n'
            elif [ "$build_id" != NONE ]; then
                printf 'PROVIDER_PREFIX_ELF\n'
            else
                printf 'PROVIDER_PREFIX_DATA_REVIEW\n'
            fi
            ;;

        ROOTFS_PROVIDER)
            if [[ "$path" == */usr/share/fonts/* ]]; then
                printf 'PROVIDER_FONT_DATA\n'
            elif [[ "$path" == */usr/share/glib-2.0/schemas/* ]]; then
                printf 'PROVIDER_SCHEMA_DATA\n'
            elif [ "$build_id" != NONE ]; then
                printf 'PROVIDER_ROOTFS_ELF\n'
            else
                printf 'PROVIDER_ROOTFS_DATA_REVIEW\n'
            fi
            ;;

        OTHER_ABSOLUTE)
            case "$path" in
                "$HOME/.cache/fontconfig/"*) printf 'RUNTIME_CACHE_FONTCONFIG\n' ;;
                "$HOME/.cache/mesa_shader_cache/"*) printf 'RUNTIME_CACHE_MESA\n' ;;
                "$HOME/.config/obsidian/"*) printf 'APP_MUTABLE_STATE\n' ;;
                *)
                    if [ "$build_id" != NONE ]; then
                        printf 'OTHER_ABSOLUTE_ELF_REVIEW\n'
                    else
                        printf 'OTHER_RUNTIME_DATA_REVIEW\n'
                    fi
                    ;;
            esac
            ;;

        *)
            printf 'UNCLASSIFIED_PATH_CLASS\n'
            ;;
    esac
}

while IFS=$'\t' read -r path_class path package version sha build_id state; do
    [ "$path_class" = path_class ] && continue
    [ -n "$state" ] || state=PRESENT

    semantic_class=$(classify "$path_class" "$path" "$package" "$build_id" "$state")

    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$semantic_class" "$path_class" "$path" "$package" "$version" \
        "$sha" "$build_id" "$state" \
        >>"$OUTPUT"
done <"$INPUT"

{
    printf 'semantic_class\tobject_count\n'
    awk -F $'\t' 'NR > 1 { count[$1]++ } END { for (c in count) print c "\t" count[c] }' \
        "$OUTPUT" \
        | sort
} >"$COUNTS"

{
    printf 'semantic_class\tpath_class\tpath\tpackage\tversion\tsha256\tbuild_id\tstate\n'
    awk -F $'\t' '
        NR > 1 && (
            $1 ~ /REVIEW$/ ||
            $1 == "MISSING_AT_ENRICHMENT" ||
            $1 == "UNCLASSIFIED_PATH_CLASS"
        ) { print }
    ' "$OUTPUT"
} >"$REVIEW"

printf '\nsemantic classification: PASS\n'
printf 'counts: %s\n' "$COUNTS"
printf 'review set: %s\n' "$REVIEW"

printf '\n===== semantic counts =====\n'
cat "$COUNTS"

review_count=$(( $(wc -l <"$REVIEW") - 1 ))
printf '\nreview objects: %s\n' "$review_count"
