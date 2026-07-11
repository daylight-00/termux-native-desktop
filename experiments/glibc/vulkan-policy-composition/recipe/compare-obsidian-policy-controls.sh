#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

EXPLICIT_OUT=${EXPLICIT_OUT:?set EXPLICIT_OUT to the Obsidian explicit-freedreno GPU evidence directory}
IMPLICIT_OUT=${IMPLICIT_OUT:?set IMPLICIT_OUT to the Obsidian implicit-discovery GPU evidence directory}
OUT=${OUT:-$IMPLICIT_OUT/obsidian-policy-control-comparison}

EXPLICIT_SEMANTIC="$EXPLICIT_OUT/semantic-objects.tsv"
IMPLICIT_SEMANTIC="$IMPLICIT_OUT/semantic-objects.tsv"
EXPLICIT_PROCESSES="$EXPLICIT_OUT/processes.tsv"
IMPLICIT_PROCESSES="$IMPLICIT_OUT/processes.tsv"
EXPLICIT_MAPPED="$EXPLICIT_OUT/mapped-objects.tsv"
IMPLICIT_MAPPED="$IMPLICIT_OUT/mapped-objects.tsv"

for file in \
    "$EXPLICIT_SEMANTIC" \
    "$IMPLICIT_SEMANTIC" \
    "$EXPLICIT_PROCESSES" \
    "$IMPLICIT_PROCESSES" \
    "$EXPLICIT_MAPPED" \
    "$IMPLICIT_MAPPED"
do
    [ -f "$file" ] || {
        printf 'missing comparison input: %s\n' "$file" >&2
        exit 1
    }
done

mkdir -p "$OUT"

is_graphics_path_awk='$4 ~ /\/libvulkan_freedreno\.so$/ || $4 ~ /\/libvulkan_lvp\.so$/ || $4 ~ /\/libvulkan_gfxstream\.so$/ || $4 ~ /\/libvk_swiftshader\.so$/ || $4 ~ /\/libVkLayer_MESA_device_select\.so$/ || $4 ~ /\/libgbm\.so(\.|$)/ || $4 ~ /\/libvulkan\.so\.1$/ || $4 ~ /\/libEGL\.so$/ || $4 ~ /\/libGLESv2\.so$/ || $4 == "/dev/kgsl-3d0"'

class_counts() {
    local input=$1
    awk -F $'\t' '
        NR > 1 { count[$2]++ }
        END { for (c in count) print c "\t" count[c] }
    ' "$input" | sort
}

semantic_pairs() {
    local input=$1
    awk -F $'\t' 'NR > 1 { print $1 "\t" $3 }' "$input" | sort -u
}

graphics_relations() {
    local input=$1
    awk -F $'\t' "NR > 1 && ($is_graphics_path_awk) { print \$2 \"\\t\" \$4 }" \
        "$input" \
        | sort -u
}

class_counts "$EXPLICIT_PROCESSES" >"$OUT/explicit-process-class-counts.tsv"
class_counts "$IMPLICIT_PROCESSES" >"$OUT/implicit-process-class-counts.tsv"

semantic_pairs "$EXPLICIT_SEMANTIC" >"$OUT/explicit-semantic-class-path.tsv"
semantic_pairs "$IMPLICIT_SEMANTIC" >"$OUT/implicit-semantic-class-path.tsv"

comm -23 \
    "$OUT/explicit-semantic-class-path.tsv" \
    "$OUT/implicit-semantic-class-path.tsv" \
    >"$OUT/explicit-only-semantic-class-path.tsv"

comm -13 \
    "$OUT/explicit-semantic-class-path.tsv" \
    "$OUT/implicit-semantic-class-path.tsv" \
    >"$OUT/implicit-only-semantic-class-path.tsv"

graphics_relations "$EXPLICIT_MAPPED" >"$OUT/explicit-graphics-relations.tsv"
graphics_relations "$IMPLICIT_MAPPED" >"$OUT/implicit-graphics-relations.tsv"

comm -23 \
    "$OUT/explicit-graphics-relations.tsv" \
    "$OUT/implicit-graphics-relations.tsv" \
    >"$OUT/explicit-only-graphics-relations.tsv"

comm -13 \
    "$OUT/explicit-graphics-relations.tsv" \
    "$OUT/implicit-graphics-relations.tsv" \
    >"$OUT/implicit-only-graphics-relations.tsv"

printf 'Obsidian policy control comparison: PASS\n'
printf 'output: %s\n' "$OUT"

printf '\n===== explicit process class counts =====\n'
cat "$OUT/explicit-process-class-counts.tsv"

printf '\n===== implicit process class counts =====\n'
cat "$OUT/implicit-process-class-counts.tsv"

printf '\n===== explicit-only semantic class/path =====\n'
cat "$OUT/explicit-only-semantic-class-path.tsv"

printf '\n===== implicit-only semantic class/path =====\n'
cat "$OUT/implicit-only-semantic-class-path.tsv"

printf '\n===== explicit graphics relations =====\n'
cat "$OUT/explicit-graphics-relations.tsv"

printf '\n===== implicit graphics relations =====\n'
cat "$OUT/implicit-graphics-relations.tsv"

printf '\n===== explicit-only graphics relations =====\n'
cat "$OUT/explicit-only-graphics-relations.tsv"

printf '\n===== implicit-only graphics relations =====\n'
cat "$OUT/implicit-only-graphics-relations.tsv"
