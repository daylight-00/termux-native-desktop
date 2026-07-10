#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

CONTROL_OUT=${CONTROL_OUT:?set CONTROL_OUT to an Obsidian control evidence directory}
INPUT="$CONTROL_OUT/mapped-objects.tsv"
RAW="$CONTROL_OUT/graphics-process-mappings.tsv"
UNIQUE="$CONTROL_OUT/graphics-class-object-relations.tsv"

[ -f "$INPUT" ] || {
    printf 'missing mapped-object evidence: %s\n' "$INPUT" >&2
    exit 1
}

is_graphics_path_awk='$4 ~ /\/libvulkan_freedreno\.so$/ || $4 ~ /\/libVkLayer_MESA_device_select\.so$/ || $4 ~ /\/libgbm\.so(\.|$)/ || $4 ~ /\/libvulkan\.so\.1$/ || $4 ~ /\/libEGL\.so$/ || $4 ~ /\/libGLESv2\.so$/ || $4 == "/dev/kgsl-3d0"'

awk -F $'\t' "NR == 1 || ($is_graphics_path_awk) { print }" \
    "$INPUT" \
    >"$RAW"

{
    printf 'class\tpath\n'
    awk -F $'\t' "NR > 1 && ($is_graphics_path_awk) { key = \$2 \"\\t\" \$4; seen[key] = 1 } END { for (k in seen) print k }" \
        "$INPUT" \
        | sort
} >"$UNIQUE"

printf '\ngraphics process mapping report: PASS\n'
printf 'raw mappings: %s\n' "$RAW"
printf 'unique class/object relations: %s\n' "$UNIQUE"

printf '\n===== raw mappings =====\n'
cat "$RAW"

printf '\n===== unique class/object relations =====\n'
cat "$UNIQUE"
