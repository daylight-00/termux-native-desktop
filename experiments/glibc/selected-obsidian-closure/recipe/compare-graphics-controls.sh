#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

BASELINE_OUT=${BASELINE_OUT:?set BASELINE_OUT to the original CPU control evidence directory}
STRICT_OUT=${STRICT_OUT:?set STRICT_OUT to the strict CPU control evidence directory}

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPORT="$SCRIPT_DIR/report-graphics-process-mappings.sh"

for evidence in "$BASELINE_OUT" "$STRICT_OUT"; do
    CONTROL_OUT="$evidence" bash "$REPORT" >/dev/null
done

BASE_REL="$BASELINE_OUT/graphics-class-object-relations.tsv"
STRICT_REL="$STRICT_OUT/graphics-class-object-relations.tsv"

printf '\n===== baseline graphics relations =====\n'
cat "$BASE_REL"

printf '\n===== strict CPU graphics relations =====\n'
cat "$STRICT_REL"

printf '\n===== relation diff: baseline -> strict CPU =====\n'
diff -u "$BASE_REL" "$STRICT_REL" || true

printf '\n===== graphics path presence summary =====\n'
for name in \
    libvulkan_freedreno.so \
    libVkLayer_MESA_device_select.so \
    libgbm.so \
    libvulkan.so.1 \
    libEGL.so \
    libGLESv2.so \
    /dev/kgsl-3d0
do
    baseline_count=$(grep -F -c "$name" "$BASE_REL" || true)
    strict_count=$(grep -F -c "$name" "$STRICT_REL" || true)
    printf '%s\tbaseline=%s\tstrict=%s\n' "$name" "$baseline_count" "$strict_count"
done

if [ -f "$BASELINE_OUT/semantic-counts.tsv" ] && [ -f "$STRICT_OUT/semantic-counts.tsv" ]; then
    printf '\n===== semantic-count diff =====\n'
    diff -u \
        "$BASELINE_OUT/semantic-counts.tsv" \
        "$STRICT_OUT/semantic-counts.tsv" \
        || true
fi
