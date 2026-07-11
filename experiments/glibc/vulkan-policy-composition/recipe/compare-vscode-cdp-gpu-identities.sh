#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

EXPLICIT_OUT=${EXPLICIT_OUT:?set EXPLICIT_OUT to a classified explicit-freedreno CDP probe}
IMPLICIT_OUT=${IMPLICIT_OUT:?set IMPLICIT_OUT to a classified implicit-discovery CDP probe}
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-cdp-identity-comparison-$(date +%Y%m%d-%H%M%S)}

for command in awk grep tr mkdir; do
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
        probe.status \
        cdp-gpu-identity.status \
        cdp-gpu-identity-summary.tsv \
        gpu-devices.tsv \
        gpu-aux-attributes.tsv \
        gpu-feature-status.tsv \
        gpu-graphics-paths.tsv
    do
        [ -f "$root/$file" ] || {
            printf 'missing %s CDP evidence: %s\n' "$control" "$root/$file" >&2
            exit 1
        }
    done
done

field_value() {
    local file=$1 field=$2
    awk -F $'\t' -v field="$field" '$1 == field { print $2; exit }' "$file"
}

printf 'control\tevidence_root\tprobe_status\tidentity_status\tclassification\tselected_provider\tselected_device_family\n' \
    >"$OUT/control-identities.tsv"

for control in explicit implicit; do
    case "$control" in
        explicit) root=$EXPLICIT_OUT ;;
        implicit) root=$IMPLICIT_OUT ;;
    esac

    probe_status=$(tr -d '\r\n' <"$root/probe.status")
    identity_status=$(tr -d '\r\n' <"$root/cdp-gpu-identity.status")
    summary="$root/cdp-gpu-identity-summary.tsv"
    classification=$(field_value "$summary" classification)
    selected_provider=$(field_value "$summary" selected_provider)
    selected_device_family=$(field_value "$summary" selected_device_family)

    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$control" "$root" "$probe_status" "$identity_status" \
        "$classification" "$selected_provider" "$selected_device_family" \
        >>"$OUT/control-identities.tsv"
done

EXPLICIT_SUMMARY="$EXPLICIT_OUT/cdp-gpu-identity-summary.tsv"
IMPLICIT_SUMMARY="$IMPLICIT_OUT/cdp-gpu-identity-summary.tsv"

explicit_probe=$(tr -d '\r\n' <"$EXPLICIT_OUT/probe.status")
explicit_identity=$(tr -d '\r\n' <"$EXPLICIT_OUT/cdp-gpu-identity.status")
implicit_probe=$(tr -d '\r\n' <"$IMPLICIT_OUT/probe.status")
implicit_identity=$(tr -d '\r\n' <"$IMPLICIT_OUT/cdp-gpu-identity.status")

explicit_class=$(field_value "$EXPLICIT_SUMMARY" classification)
explicit_provider=$(field_value "$EXPLICIT_SUMMARY" selected_provider)
explicit_device=$(field_value "$EXPLICIT_SUMMARY" selected_device_family)
explicit_provider_path=$(field_value "$EXPLICIT_SUMMARY" provider_path_relation)
explicit_device_node=$(field_value "$EXPLICIT_SUMMARY" device_node_relation)
explicit_display=$(field_value "$EXPLICIT_SUMMARY" display_type)
explicit_skia=$(field_value "$EXPLICIT_SUMMARY" skia_backend)
explicit_vulkan=$(field_value "$EXPLICIT_SUMMARY" vulkan_feature_status)
explicit_renderer=$(field_value "$EXPLICIT_SUMMARY" gl_renderer)

implicit_class=$(field_value "$IMPLICIT_SUMMARY" classification)
implicit_provider=$(field_value "$IMPLICIT_SUMMARY" selected_provider)
implicit_device=$(field_value "$IMPLICIT_SUMMARY" selected_device_family)
implicit_provider_path=$(field_value "$IMPLICIT_SUMMARY" provider_path_relation)
implicit_device_node=$(field_value "$IMPLICIT_SUMMARY" device_node_relation)
implicit_display=$(field_value "$IMPLICIT_SUMMARY" display_type)
implicit_skia=$(field_value "$IMPLICIT_SUMMARY" skia_backend)
implicit_vulkan=$(field_value "$IMPLICIT_SUMMARY" vulkan_feature_status)
implicit_renderer=$(field_value "$IMPLICIT_SUMMARY" gl_renderer)

printf 'gate\tstate\n' >"$OUT/comparison-gates.tsv"
FAILURES=0

record_gate() {
    local gate=$1 state=$2
    printf '%s\t%s\n' "$gate" "$state" >>"$OUT/comparison-gates.tsv"
    if [ "$state" != PASS ]; then
        FAILURES=$((FAILURES + 1))
    fi
}

expect_equal() {
    local gate=$1 observed=$2 expected=$3
    if [ "$observed" = "$expected" ]; then
        record_gate "$gate" PASS
    else
        record_gate "$gate" FAIL
        printf '%s expected=%s observed=%s\n' "$gate" "$expected" "$observed" >&2
    fi
}

expect_different() {
    local gate=$1 left=$2 right=$3
    if [ "$left" != "$right" ]; then
        record_gate "$gate" PASS
    else
        record_gate "$gate" FAIL
        printf '%s expected different values, both=%s\n' "$gate" "$left" >&2
    fi
}

expect_equal explicit_probe_status "$explicit_probe" PASS
expect_equal explicit_identity_status "$explicit_identity" PASS
expect_equal implicit_probe_status "$implicit_probe" PASS
expect_equal implicit_identity_status "$implicit_identity" PASS

expect_equal explicit_classification "$explicit_class" FREEDRENO_TURNIP
expect_equal explicit_selected_provider "$explicit_provider" FREEDRENO_TURNIP
expect_equal explicit_selected_device_family "$explicit_device" Adreno
expect_equal explicit_provider_path_relation "$explicit_provider_path" PRESENT
expect_equal explicit_device_node_relation "$explicit_device_node" PRESENT

expect_equal implicit_classification "$implicit_class" LVP_LLVMPIPE
expect_equal implicit_selected_provider "$implicit_provider" LVP
expect_equal implicit_selected_device_family "$implicit_device" llvmpipe
expect_equal implicit_provider_path_relation "$implicit_provider_path" PRESENT
expect_equal implicit_device_node_relation "$implicit_device_node" NOT_APPLICABLE

expect_equal explicit_display_type "$explicit_display" ANGLE_VULKAN
expect_equal implicit_display_type "$implicit_display" ANGLE_VULKAN
expect_equal display_type_invariant "$explicit_display" "$implicit_display"

expect_equal explicit_skia_backend "$explicit_skia" GaneshVulkan
expect_equal implicit_skia_backend "$implicit_skia" GaneshVulkan
expect_equal skia_backend_invariant "$explicit_skia" "$implicit_skia"

expect_equal explicit_vulkan_feature "$explicit_vulkan" enabled_on
expect_equal implicit_vulkan_feature "$implicit_vulkan" enabled_on
expect_equal vulkan_feature_invariant "$explicit_vulkan" "$implicit_vulkan"

expect_different selected_provider_delta "$explicit_provider" "$implicit_provider"
expect_different selected_device_delta "$explicit_device" "$implicit_device"
expect_different renderer_identity_delta "$explicit_renderer" "$implicit_renderer"

{
    printf 'field\texplicit\timplicit\n'
    printf 'classification\t%s\t%s\n' "$explicit_class" "$implicit_class"
    printf 'selected_provider\t%s\t%s\n' "$explicit_provider" "$implicit_provider"
    printf 'selected_device_family\t%s\t%s\n' "$explicit_device" "$implicit_device"
    printf 'display_type\t%s\t%s\n' "$explicit_display" "$implicit_display"
    printf 'skia_backend\t%s\t%s\n' "$explicit_skia" "$implicit_skia"
    printf 'vulkan_feature_status\t%s\t%s\n' "$explicit_vulkan" "$implicit_vulkan"
    printf 'provider_path_relation\t%s\t%s\n' "$explicit_provider_path" "$implicit_provider_path"
    printf 'device_node_relation\t%s\t%s\n' "$explicit_device_node" "$implicit_device_node"
    printf 'gl_renderer\t%s\t%s\n' "$explicit_renderer" "$implicit_renderer"
} >"$OUT/identity-delta.tsv"

if [ "$FAILURES" -ne 0 ]; then
    printf 'FAIL\n' >"$OUT/comparison.status"
    printf 'VS Code CDP GPU identity comparison: FAIL (%s gates)\n' "$FAILURES" >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
fi

printf 'PASS\n' >"$OUT/comparison.status"

printf 'VS Code CDP GPU identity comparison: PASS\n'
printf 'explicit evidence: %s\n' "$EXPLICIT_OUT"
printf 'implicit evidence: %s\n' "$IMPLICIT_OUT"
printf 'comparison evidence: %s\n' "$OUT"

printf '\n===== control identities =====\n'
cat "$OUT/control-identities.tsv"

printf '\n===== comparison gates =====\n'
cat "$OUT/comparison-gates.tsv"

printf '\n===== identity delta =====\n'
cat "$OUT/identity-delta.tsv"
