#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

EXPLICIT_OUT=${EXPLICIT_OUT:?set EXPLICIT_OUT to the completed VS Code explicit-intent control}
IMPLICIT_OUT=${IMPLICIT_OUT:?set IMPLICIT_OUT to the completed VS Code implicit-discovery control}
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-policy-control-comparison-$(date +%Y%m%d-%H%M%S)}

for command in awk grep sort comm readlink; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

mkdir -p "$OUT"

for control in explicit implicit; do
    case "$control" in
        explicit) root=$EXPLICIT_OUT ;;
        implicit) root=$IMPLICIT_OUT ;;
    esac

    for file in \
        topology.status \
        survival.status \
        maps-capture.status \
        graphics-class-object-relations.tsv
    do
        [ -f "$root/$file" ] || {
            printf 'missing %s control evidence: %s\n' "$control" "$root/$file" >&2
            exit 1
        }
    done
done

printf 'control\tevidence_root\ttopology\tsurvival\tmaps_capture\n' >"$OUT/control-status.tsv"
for control in explicit implicit; do
    case "$control" in
        explicit) root=$EXPLICIT_OUT ;;
        implicit) root=$IMPLICIT_OUT ;;
    esac

    topology=$(tr -d '\r\n' <"$root/topology.status")
    survival=$(tr -d '\r\n' <"$root/survival.status")
    maps_capture=$(tr -d '\r\n' <"$root/maps-capture.status")

    printf '%s\t%s\t%s\t%s\t%s\n' \
        "$control" "$root" "$topology" "$survival" "$maps_capture" \
        >>"$OUT/control-status.tsv"

    [ "$topology" = PASS ] || {
        printf '%s topology status is not PASS: %s\n' "$control" "$topology" >&2
        exit 1
    }
    [ "$survival" = PASS ] || {
        printf '%s survival status is not PASS: %s\n' "$control" "$survival" >&2
        exit 1
    }
    [ "$maps_capture" = PASS ] || {
        printf '%s maps-capture status is not PASS: %s\n' "$control" "$maps_capture" >&2
        exit 1
    }
done

awk -F $'\t' 'NR > 1 { print $1 "\t" $2 }' \
    "$EXPLICIT_OUT/graphics-class-object-relations.tsv" \
    | sort -u >"$OUT/explicit-relations.tsv"

awk -F $'\t' 'NR > 1 { print $1 "\t" $2 }' \
    "$IMPLICIT_OUT/graphics-class-object-relations.tsv" \
    | sort -u >"$OUT/implicit-relations.tsv"

comm -12 "$OUT/explicit-relations.tsv" "$OUT/implicit-relations.tsv" \
    >"$OUT/common-relations.tsv"
comm -23 "$OUT/explicit-relations.tsv" "$OUT/implicit-relations.tsv" \
    >"$OUT/explicit-only-relations.tsv"
comm -13 "$OUT/explicit-relations.tsv" "$OUT/implicit-relations.tsv" \
    >"$OUT/implicit-only-relations.tsv"

has_relation() {
    local file=$1 class=$2 pattern=$3
    awk -F $'\t' -v c="$class" -v p="$pattern" \
        '$1 == c && $2 ~ p { found=1 } END { exit found ? 0 : 1 }' "$file"
}

not_has_relation() {
    local file=$1 class=$2 pattern=$3
    if has_relation "$file" "$class" "$pattern"; then
        return 1
    fi
    return 0
}

printf 'gate\tstate\n' >"$OUT/comparison-gates.tsv"

record_gate() {
    local gate=$1 state=$2
    printf '%s\t%s\n' "$gate" "$state" >>"$OUT/comparison-gates.tsv"
    [ "$state" = PASS ]
}

if has_relation "$OUT/explicit-relations.tsv" gpu 'libvulkan_freedreno\.so$'; then
    record_gate explicit_gpu_freedreno_present PASS
else
    record_gate explicit_gpu_freedreno_present FAIL
fi

if has_relation "$OUT/explicit-relations.tsv" gpu '^/dev/kgsl-3d0$'; then
    record_gate explicit_gpu_kgsl_present PASS
else
    record_gate explicit_gpu_kgsl_present FAIL
fi

if not_has_relation "$OUT/explicit-relations.tsv" gpu 'libvulkan_lvp\.so$'; then
    record_gate explicit_gpu_lvp_absent PASS
else
    record_gate explicit_gpu_lvp_absent FAIL
fi

if not_has_relation "$OUT/explicit-relations.tsv" gpu 'libvulkan_gfxstream\.so$'; then
    record_gate explicit_gpu_gfxstream_absent PASS
else
    record_gate explicit_gpu_gfxstream_absent FAIL
fi

if has_relation "$OUT/implicit-relations.tsv" gpu 'libvulkan_lvp\.so$'; then
    record_gate implicit_gpu_lvp_present PASS
else
    record_gate implicit_gpu_lvp_present FAIL
fi

if has_relation "$OUT/implicit-relations.tsv" gpu 'libvulkan_gfxstream\.so$'; then
    record_gate implicit_gpu_gfxstream_present PASS
else
    record_gate implicit_gpu_gfxstream_present FAIL
fi

if not_has_relation "$OUT/implicit-relations.tsv" gpu 'libvulkan_freedreno\.so$'; then
    record_gate implicit_gpu_freedreno_absent PASS
else
    record_gate implicit_gpu_freedreno_absent FAIL
fi

if not_has_relation "$OUT/implicit-relations.tsv" gpu '^/dev/kgsl-3d0$'; then
    record_gate implicit_gpu_kgsl_absent PASS
else
    record_gate implicit_gpu_kgsl_absent FAIL
fi

if [ -s "$OUT/explicit-only-relations.tsv" ] && [ -s "$OUT/implicit-only-relations.tsv" ]; then
    record_gate bidirectional_relation_delta_present PASS
else
    record_gate bidirectional_relation_delta_present FAIL
fi

printf 'PASS\n' >"$OUT/comparison.status"

printf 'VS Code Vulkan policy control comparison: PASS\n'
printf 'explicit evidence: %s\n' "$EXPLICIT_OUT"
printf 'implicit evidence: %s\n' "$IMPLICIT_OUT"
printf 'comparison evidence: %s\n' "$OUT"

printf '\n===== control status =====\n'
cat "$OUT/control-status.tsv"

printf '\n===== comparison gates =====\n'
cat "$OUT/comparison-gates.tsv"

printf '\n===== explicit-only relations =====\n'
cat "$OUT/explicit-only-relations.tsv"

printf '\n===== implicit-only relations =====\n'
cat "$OUT/implicit-only-relations.tsv"

printf '\n===== common relations =====\n'
cat "$OUT/common-relations.tsv"
