#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

CONTROL_OUT=${CONTROL_OUT:?set CONTROL_OUT to a completed Electron CDP GPU identity probe}
OUT=${OUT:-$CONTROL_OUT}
APP_LABEL=${APP_LABEL:-Electron}

for command in awk grep tr sed mkdir; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

for file in \
    gpu-devices.tsv \
    gpu-aux-attributes.tsv \
    gpu-feature-status.tsv \
    gpu-graphics-paths.tsv \
    probe.status
do
    [ -f "$CONTROL_OUT/$file" ] || {
        printf 'missing CDP probe evidence: %s\n' "$CONTROL_OUT/$file" >&2
        exit 1
    }
done

probe_status=$(tr -d '\r\n' <"$CONTROL_OUT/probe.status")
[ "$probe_status" = PASS ] || {
    printf 'CDP probe status is not PASS: %s\n' "$probe_status" >&2
    exit 1
}

mkdir -p "$OUT"

primary_line=$(awk -F $'\t' 'NR > 1 && $2 == "true" { print NR; exit }' \
    "$CONTROL_OUT/gpu-devices.tsv")
[ -n "$primary_line" ] || {
    printf 'no primary GPU row found in %s\n' "$CONTROL_OUT/gpu-devices.tsv" >&2
    exit 1
}

column_of_primary() {
    local column=$1
    awk -F $'\t' -v line="$primary_line" -v column="$column" \
        'NR == line { print $column; exit }' "$CONTROL_OUT/gpu-devices.tsv"
}

index=$(column_of_primary 1)
primary=$(column_of_primary 2)
vendor_id=$(column_of_primary 3)
device_id=$(column_of_primary 4)
sub_sys_id=$(column_of_primary 5)
revision=$(column_of_primary 6)
vendor_string=$(column_of_primary 7)
device_string=$(column_of_primary 8)
driver_vendor=$(column_of_primary 9)
driver_version=$(column_of_primary 10)

gl_renderer=$(awk -F $'\t' '$1 == "glRenderer" { print $2; exit }' \
    "$CONTROL_OUT/gpu-aux-attributes.tsv")
display_type=$(awk -F $'\t' '$1 == "displayType" { print $2; exit }' \
    "$CONTROL_OUT/gpu-aux-attributes.tsv")
skia_backend=$(awk -F $'\t' '$1 == "skiaBackendType" { print $2; exit }' \
    "$CONTROL_OUT/gpu-aux-attributes.tsv")
hardware_supports_vulkan=$(awk -F $'\t' '$1 == "hardwareSupportsVulkan" { print $2; exit }' \
    "$CONTROL_OUT/gpu-aux-attributes.tsv")
vulkan_feature_status=$(awk -F $'\t' '$1 == "vulkan" { print $2; exit }' \
    "$CONTROL_OUT/gpu-feature-status.tsv")

identity_text=$(printf '%s\n%s\n%s\n%s\n%s\n' \
    "$vendor_string" "$device_string" "$driver_vendor" "$driver_version" "$gl_renderer" \
    | tr '[:upper:]' '[:lower:]')

classification=UNKNOWN
selected_provider=UNKNOWN
selected_device_family=UNKNOWN

case "$identity_text" in
    *llvmpipe*|*lavapipe*)
        classification=LVP_LLVMPIPE
        selected_provider=LVP
        selected_device_family=llvmpipe
        ;;
    *gfxstream*)
        classification=GFXSTREAM
        selected_provider=GFXSTREAM
        selected_device_family=gfxstream
        ;;
    *turnip*|*adreno*|*freedreno*)
        classification=FREEDRENO_TURNIP
        selected_provider=FREEDRENO_TURNIP
        selected_device_family=Adreno
        ;;
esac

has_path() {
    local pattern=$1
    grep -Eq -- "$pattern" "$CONTROL_OUT/gpu-graphics-paths.tsv"
}

provider_path_relation=UNKNOWN
device_node_relation=NOT_APPLICABLE
correlation_state=FAIL

case "$classification" in
    LVP_LLVMPIPE)
        if has_path '/libvulkan_lvp\.so$'; then
            provider_path_relation=PRESENT
            correlation_state=PASS
        else
            provider_path_relation=ABSENT
        fi
        ;;
    GFXSTREAM)
        if has_path '/libvulkan_gfxstream\.so$'; then
            provider_path_relation=PRESENT
            correlation_state=PASS
        else
            provider_path_relation=ABSENT
        fi
        ;;
    FREEDRENO_TURNIP)
        if has_path '/libvulkan_freedreno\.so$'; then
            provider_path_relation=PRESENT
        else
            provider_path_relation=ABSENT
        fi

        if has_path '^/dev/kgsl-3d0$'; then
            device_node_relation=PRESENT
        else
            device_node_relation=ABSENT
        fi

        if [ "$provider_path_relation" = PRESENT ] && \
           [ "$device_node_relation" = PRESENT ]; then
            correlation_state=PASS
        fi
        ;;
esac

printf 'field\tvalue\n' >"$OUT/cdp-gpu-identity-summary.tsv"
printf 'probe_status\t%s\n' "$probe_status" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'primary_index\t%s\n' "$index" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'primary\t%s\n' "$primary" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'vendor_id\t%s\n' "$vendor_id" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'device_id\t%s\n' "$device_id" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'sub_sys_id\t%s\n' "$sub_sys_id" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'revision\t%s\n' "$revision" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'vendor_string\t%s\n' "$vendor_string" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'device_string\t%s\n' "$device_string" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'driver_vendor\t%s\n' "$driver_vendor" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'driver_version\t%s\n' "$driver_version" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'gl_renderer\t%s\n' "$gl_renderer" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'display_type\t%s\n' "$display_type" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'skia_backend\t%s\n' "$skia_backend" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'hardware_supports_vulkan\t%s\n' "$hardware_supports_vulkan" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'vulkan_feature_status\t%s\n' "$vulkan_feature_status" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'classification\t%s\n' "$classification" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'selected_provider\t%s\n' "$selected_provider" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'selected_device_family\t%s\n' "$selected_device_family" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'provider_path_relation\t%s\n' "$provider_path_relation" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'device_node_relation\t%s\n' "$device_node_relation" >>"$OUT/cdp-gpu-identity-summary.tsv"
printf 'correlation_state\t%s\n' "$correlation_state" >>"$OUT/cdp-gpu-identity-summary.tsv"

if [ "$classification" = UNKNOWN ]; then
    printf 'UNKNOWN\n' >"$OUT/cdp-gpu-identity.status"
    printf '%s CDP GPU identity classification: UNKNOWN\n' "$APP_LABEL" >&2
    printf 'evidence: %s\n' "$CONTROL_OUT" >&2
    exit 1
fi

if [ "$correlation_state" != PASS ]; then
    printf 'FAIL\n' >"$OUT/cdp-gpu-identity.status"
    printf '%s CDP GPU identity correlation: FAIL\n' "$APP_LABEL" >&2
    cat "$OUT/cdp-gpu-identity-summary.tsv" >&2
    exit 1
fi

printf 'PASS\n' >"$OUT/cdp-gpu-identity.status"
printf '%s CDP GPU identity classification: PASS\n' "$APP_LABEL"
printf 'evidence: %s\n' "$CONTROL_OUT"
printf 'classification: %s\n' "$classification"
printf 'selected provider: %s\n' "$selected_provider"
printf 'selected device family: %s\n' "$selected_device_family"
printf '\n===== identity summary =====\n'
cat "$OUT/cdp-gpu-identity-summary.tsv"
