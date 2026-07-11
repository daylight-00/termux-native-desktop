#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
B2_OUT=${B2_OUT:?set B2_OUT to a completed Phase B2 static/runtime closure directory}
OUT=${OUT:-${PREFIX:-/tmp}/tmp/selected-obsidian-closure/phase-b3-capability-grouping-$(date +%Y%m%d-%H%M%S)}

for command in git bash awk grep sort uniq mkdir cp wc date cat basename head tail mv tr sed; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

tracked_dirty=$(git -C "$REPO" status --porcelain --untracked-files=no)
if [ -n "$tracked_dirty" ]; then
    printf 'tracked working-tree changes detected; Phase B3 analysis requires exact HEAD:\n' >&2
    printf '%s\n' "$tracked_dirty" >&2
    exit 2
fi

branch=$(git -C "$REPO" branch --show-current)
head_sha=$(git -C "$REPO" rev-parse HEAD)

REQUIRED_FILES=(
    analysis.status
    summary.tsv
    resolved-edges.tsv
    candidate-elf-partition.tsv
    mapped-only-dynamic.tsv
    data-capabilities.tsv
    input/elf-objects.tsv
    input/process-semantic-usage.tsv
)

mkdir -p "$OUT/input"
printf '%s\n' "$REPO" >"$OUT/repository-root.txt"
printf '%s\n' "$branch" >"$OUT/branch.txt"
printf '%s\n' "$head_sha" >"$OUT/head.txt"
printf '%s\n' "$B2_OUT" >"$OUT/phase-b2-root.txt"
printf 'file\tstate\tpath\tembedded_path\n' >"$OUT/input-verification.tsv"
failures=0
for name in "${REQUIRED_FILES[@]}"; do
    path="$B2_OUT/$name"
    embedded="$OUT/input/$(printf '%s' "$name" | tr '/' '_')"
    if [ -f "$path" ]; then
        printf '%s\tPASS\t%s\t%s\n' "$name" "$path" "$embedded" \
            >>"$OUT/input-verification.tsv"
        cp "$path" "$embedded"
    else
        printf '%s\tFAIL\t%s\t-\n' "$name" "$path" \
            >>"$OUT/input-verification.tsv"
        failures=$((failures + 1))
    fi
done

if [ "$failures" -ne 0 ]; then
    printf 'FAIL\n' >"$OUT/analysis.status"
    printf 'missing Phase B2 inputs: %s\n' "$failures" >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
fi

b2_status=$(tr -d '\r\n' <"$B2_OUT/analysis.status")
b2_head=$(awk -F $'\t' '$1 == "head" { print $2; exit }' "$B2_OUT/summary.tsv")
entrypoint=$(awk -F $'\t' '$1 == "entrypoint" { print $2; exit }' "$B2_OUT/summary.tsv")
[ "$b2_status" = PASS ] || {
    printf 'FAIL\n' >"$OUT/analysis.status"
    printf 'Phase B2 status is not PASS: %s\n' "$b2_status" >&2
    exit 1
}
[ -n "$entrypoint" ] || {
    printf 'FAIL\n' >"$OUT/analysis.status"
    printf 'Phase B2 summary has no entrypoint\n' >&2
    exit 1
}

PARTITION="$B2_OUT/candidate-elf-partition.tsv"
EDGES="$B2_OUT/resolved-edges.tsv"
USAGE="$B2_OUT/input/process-semantic-usage.tsv"
DATA="$B2_OUT/data-capabilities.tsv"

declare -A PARTITION_BY_PATH=()
declare -A SEMANTIC_BY_PATH=()
declare -A PACKAGE_BY_PATH=()
declare -A VERSION_BY_PATH=()
declare -A DYNAMIC=()
declare -A PROCESS_CLASSES=()
declare -A INCOMING_DYNAMIC=()
declare -A ROOT_FAMILY=()

while IFS=$'\t' read -r partition semantic package version path; do
    [ "$partition" = partition ] && continue
    [ -n "$path" ] || continue
    PARTITION_BY_PATH["$path"]=$partition
    SEMANTIC_BY_PATH["$path"]=$semantic
    PACKAGE_BY_PATH["$path"]=$package
    VERSION_BY_PATH["$path"]=$version
    if [ "$partition" = MAPPED_ONLY_DYNAMIC_OR_DISCOVERY ]; then
        DYNAMIC["$path"]=1
    fi
done <"$PARTITION"

while IFS=$'\t' read -r pid process_class semantic path; do
    [ "$pid" = pid ] && continue
    [ -n "$path" ] || continue
    key="$path|$process_class"
    case ",${PROCESS_CLASSES[$path]:-}," in
        *",$process_class,"*) : ;;
        *) PROCESS_CLASSES["$path"]="${PROCESS_CLASSES[$path]:+${PROCESS_CLASSES[$path]},}$process_class" ;;
    esac
done <"$USAGE"

while IFS=$'\t' read -r consumer provider needed; do
    [ "$consumer" = consumer_path ] && continue
    if [ -n "${DYNAMIC[$consumer]:-}" ] && [ -n "${DYNAMIC[$provider]:-}" ]; then
        INCOMING_DYNAMIC["$provider"]=$(( ${INCOMING_DYNAMIC[$provider]:-0} + 1 ))
    fi
done <"$EDGES"

suggest_family() {
    local path=$1 semantic=${SEMANTIC_BY_PATH[$path]} package=${PACKAGE_BY_PATH[$path]}
    case "$semantic" in
        PROVIDER_GRAPHICS_VULKAN_DRIVER_ELF|PROVIDER_GRAPHICS_VULKAN_LAYER_ELF)
            printf 'GRAPHICS_VULKAN\n'
            ;;
        PROVIDER_ROOTFS_ELF)
            case "$package" in
                libnss3:*) printf 'NSS_SECURITY\n' ;;
                *) printf 'REVIEW\n' ;;
            esac
            ;;
        *)
            printf 'REVIEW\n'
            ;;
    esac
}

printf 'root_path\troot_basename\tsuggested_family\tsemantic_class\tpackage\tversion\tprocess_classes\tmapped_only_closure_count\tfull_closure_count\n' \
    >"$OUT/dynamic-root-candidates.tsv"
printf 'root_path\troot_basename\tsuggested_family\tmember_relation\tmember_partition\tmember_semantic_class\tmember_package\tmember_version\tmember_process_classes\tmember_path\n' \
    >"$OUT/dynamic-root-closure.tsv"
printf 'root_path\tmember_path\n' >"$OUT/dynamic-root-members.tsv"

root_count=0
review_root_count=0
for root in "${!DYNAMIC[@]}"; do
    if [ "${INCOMING_DYNAMIC[$root]:-0}" -ne 0 ]; then
        continue
    fi

    root_count=$((root_count + 1))
    family=$(suggest_family "$root")
    ROOT_FAMILY["$root"]=$family
    [ "$family" != REVIEW ] || review_root_count=$((review_root_count + 1))

    declare -A seen=()
    queue=("$root")
    seen["$root"]=1
    index=0
    while [ "$index" -lt "${#queue[@]}" ]; do
        current=${queue[$index]}
        index=$((index + 1))
        while IFS=$'\t' read -r consumer provider needed; do
            [ "$consumer" = consumer_path ] && continue
            [ "$consumer" = "$current" ] || continue
            if [ -z "${seen[$provider]:-}" ]; then
                seen["$provider"]=1
                queue+=("$provider")
            fi
        done <"$EDGES"
    done

    mapped_count=0
    full_count=0
    for member in "${!seen[@]}"; do
        full_count=$((full_count + 1))
        if [ -n "${DYNAMIC[$member]:-}" ]; then
            mapped_count=$((mapped_count + 1))
        fi
    done

    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$root" "$(basename "$root")" "$family" \
        "${SEMANTIC_BY_PATH[$root]}" "${PACKAGE_BY_PATH[$root]}" \
        "${VERSION_BY_PATH[$root]}" "${PROCESS_CLASSES[$root]:--}" \
        "$mapped_count" "$full_count" \
        >>"$OUT/dynamic-root-candidates.tsv"

    for member in "${!seen[@]}"; do
        if [ "$member" = "$root" ]; then
            relation=ROOT
        elif [ -n "${DYNAMIC[$member]:-}" ]; then
            relation=MAPPED_ONLY_SUPPORT
        else
            relation=STATIC_SUPPORT
        fi
        printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
            "$root" "$(basename "$root")" "$family" "$relation" \
            "${PARTITION_BY_PATH[$member]}" "${SEMANTIC_BY_PATH[$member]}" \
            "${PACKAGE_BY_PATH[$member]}" "${VERSION_BY_PATH[$member]}" \
            "${PROCESS_CLASSES[$member]:--}" "$member" \
            >>"$OUT/dynamic-root-closure.tsv"
        if [ -n "${DYNAMIC[$member]:-}" ]; then
            printf '%s\t%s\n' "$root" "$member" >>"$OUT/dynamic-root-members.tsv"
        fi
    done
    unset seen queue
done

{
    head -n 1 "$OUT/dynamic-root-candidates.tsv"
    tail -n +2 "$OUT/dynamic-root-candidates.tsv" | sort -t $'\t' -k3,3 -k2,2
} >"$OUT/dynamic-root-candidates.sorted.tsv"
mv "$OUT/dynamic-root-candidates.sorted.tsv" "$OUT/dynamic-root-candidates.tsv"

{
    head -n 1 "$OUT/dynamic-root-closure.tsv"
    tail -n +2 "$OUT/dynamic-root-closure.tsv" | sort -t $'\t' -k3,3 -k2,2 -k4,4 -k10,10
} >"$OUT/dynamic-root-closure.sorted.tsv"
mv "$OUT/dynamic-root-closure.sorted.tsv" "$OUT/dynamic-root-closure.tsv"

printf 'member_path\tmember_basename\troot_count\troots\n' >"$OUT/shared-dynamic-support.tsv"
awk -F $'\t' '
    NR == 1 { next }
    {
        root=$1; member=$2
        key=member SUBSEP root
        if (!seen[key]++) {
            count[member]++
            roots[member]=(roots[member] ? roots[member] ";" : "") root
        }
    }
    END {
        for (member in count) {
            if (count[member] > 1) {
                base=member
                sub(/^.*\//, "", base)
                print member "\t" base "\t" count[member] "\t" roots[member]
            }
        }
    }
' "$OUT/dynamic-root-members.tsv" | sort >>"$OUT/shared-dynamic-support.tsv"

printf 'needed\tsemantic_class\tpackage\tversion\tprovider_path\n' >"$OUT/entrypoint-direct-providers.tsv"
while IFS=$'\t' read -r consumer provider needed; do
    [ "$consumer" = consumer_path ] && continue
    [ "$consumer" = "$entrypoint" ] || continue
    printf '%s\t%s\t%s\t%s\t%s\n' \
        "$needed" "${SEMANTIC_BY_PATH[$provider]}" "${PACKAGE_BY_PATH[$provider]}" \
        "${VERSION_BY_PATH[$provider]}" "$provider" \
        >>"$OUT/entrypoint-direct-providers.tsv"
done <"$EDGES"
{
    head -n 1 "$OUT/entrypoint-direct-providers.tsv"
    tail -n +2 "$OUT/entrypoint-direct-providers.tsv" | sort -t $'\t' -k2,2 -k3,3 -k1,1
} >"$OUT/entrypoint-direct-providers.sorted.tsv"
mv "$OUT/entrypoint-direct-providers.sorted.tsv" "$OUT/entrypoint-direct-providers.tsv"

{
    printf 'partition\tsemantic_class\tpackage\tversion\tobject_count\n'
    awk -F $'\t' 'NR > 1 {
        key=$1 SUBSEP $2 SUBSEP $3 SUBSEP $4
        count[key]++
    } END {
        for (key in count) {
            split(key,a,SUBSEP)
            print a[1] "\t" a[2] "\t" a[3] "\t" a[4] "\t" count[key]
        }
    }' "$PARTITION" | sort
} >"$OUT/partition-package-summary.tsv"

{
    printf 'semantic_class\tpackage\tversion\tobject_count\n'
    awk -F $'\t' 'NR > 1 {
        key=$1 SUBSEP $3 SUBSEP $4
        count[key]++
    } END {
        for (key in count) {
            split(key,a,SUBSEP)
            print a[1] "\t" a[2] "\t" a[3] "\t" count[key]
        }
    }' "$DATA" | sort
} >"$OUT/data-capability-summary.tsv"

{
    printf 'suggested_family\troot_count\tmapped_only_member_count\n'
    awk -F $'\t' '
        FNR == NR {
            if (FNR == 1) next
            family[$1]=$3
            roots[$3]++
            next
        }
        FNR == 1 { next }
        {
            fam=family[$1]
            key=fam SUBSEP $2
            if (!seen[key]++) members[fam]++
        }
        END {
            for (fam in roots) print fam "\t" roots[fam] "\t" (members[fam]+0)
        }
    ' "$OUT/dynamic-root-candidates.tsv" "$OUT/dynamic-root-members.tsv" | sort
} >"$OUT/suggested-dynamic-family-summary.tsv"

mapped_only_count=$(( $(wc -l <"$B2_OUT/mapped-only-dynamic.tsv") - 1 ))
shared_dynamic_count=$(( $(wc -l <"$OUT/shared-dynamic-support.tsv") - 1 ))
entrypoint_direct_count=$(( $(wc -l <"$OUT/entrypoint-direct-providers.tsv") - 1 ))
data_count=$(( $(wc -l <"$DATA") - 1 ))

{
    printf 'field\tvalue\n'
    printf 'branch\t%s\n' "$branch"
    printf 'head\t%s\n' "$head_sha"
    printf 'phase_b2_root\t%s\n' "$B2_OUT"
    printf 'phase_b2_head\t%s\n' "$b2_head"
    printf 'entrypoint\t%s\n' "$entrypoint"
    printf 'mapped_only_objects\t%s\n' "$mapped_only_count"
    printf 'dynamic_discovery_roots\t%s\n' "$root_count"
    printf 'unclassified_dynamic_roots\t%s\n' "$review_root_count"
    printf 'shared_dynamic_support_objects\t%s\n' "$shared_dynamic_count"
    printf 'entrypoint_direct_providers\t%s\n' "$entrypoint_direct_count"
    printf 'data_capability_objects\t%s\n' "$data_count"
    printf 'runtime_launch_performed\tNO\n'
    printf 'promoted_runtime_mutated\tNO\n'
} >"$OUT/summary.tsv"

{
    printf 'This is a read-only capability-grouping input analysis over Phase B2.\n'
    printf 'A dynamic root is a mapped-only object with no incoming edge from another mapped-only object.\n'
    printf 'Suggested families are evidence-guided labels, not final ownership decisions.\n'
    printf 'Root closures include both mapped-only support and already-static support.\n'
    printf 'Process classes support attribution but do not prove the exact dlopen caller or search path.\n'
    printf 'The large entrypoint-static external set remains heterogeneous.\n'
} >"$OUT/claim-boundary.txt"

if [ "$root_count" -eq 0 ]; then
    printf 'NO_DYNAMIC_ROOTS_FOUND\n' >"$OUT/next-state.txt"
    printf 'FAIL\n' >"$OUT/analysis.status"
    printf 'no dynamic discovery root found\n' >&2
    exit 1
fi

if [ "$review_root_count" -ne 0 ]; then
    printf 'REVIEW_DYNAMIC_ROOT_FAMILIES\n' >"$OUT/next-state.txt"
else
    printf 'READY_FOR_CAPABILITY_OWNERSHIP_DECISION\n' >"$OUT/next-state.txt"
fi
printf 'PASS\n' >"$OUT/analysis.status"
printf 'selected Obsidian Phase B3 capability grouping input: PASS\n'
printf 'evidence: %s\n' "$OUT"
printf '\n===== summary =====\n'
cat "$OUT/summary.tsv"
printf '\n===== dynamic roots =====\n'
cat "$OUT/dynamic-root-candidates.tsv"
printf '\n===== shared dynamic support =====\n'
cat "$OUT/shared-dynamic-support.tsv"
printf '\n===== suggested dynamic families =====\n'
cat "$OUT/suggested-dynamic-family-summary.tsv"
