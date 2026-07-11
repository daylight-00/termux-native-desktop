#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
B1_OUT=${B1_OUT:?set B1_OUT to a completed Phase B1 retained-control locality audit directory}
OUT=${OUT:-${PREFIX:-/tmp}/tmp/selected-obsidian-closure/phase-b2-static-runtime-closure-$(date +%Y%m%d-%H%M%S)}
ENTRYPOINT=${ENTRYPOINT:-$HOME/gl/apps/obsidian/obsidian}

for command in git bash awk grep sort uniq mkdir cp wc date cat basename head tail mv tr; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

tracked_dirty=$(git -C "$REPO" status --porcelain --untracked-files=no)
if [ -n "$tracked_dirty" ]; then
    printf 'tracked working-tree changes detected; Phase B2 analysis requires exact HEAD:\n' >&2
    printf '%s\n' "$tracked_dirty" >&2
    exit 2
fi

branch=$(git -C "$REPO" branch --show-current)
head_sha=$(git -C "$REPO" rev-parse HEAD)

REQUIRED_FILES=(
    audit.status
    summary.tsv
    candidate-input-identities.tsv
    elf-objects.tsv
    elf-needed.tsv
    name-providers.tsv
    unresolved-needed.tsv
    ambiguous-needed.tsv
    process-semantic-usage.tsv
    input/semantic-objects.tsv
)

mkdir -p "$OUT/input"
printf '%s\n' "$REPO" >"$OUT/repository-root.txt"
printf '%s\n' "$branch" >"$OUT/branch.txt"
printf '%s\n' "$head_sha" >"$OUT/head.txt"
printf '%s\n' "$B1_OUT" >"$OUT/phase-b1-root.txt"
printf 'file\tstate\tpath\n' >"$OUT/input-verification.tsv"
failures=0
for name in "${REQUIRED_FILES[@]}"; do
    path="$B1_OUT/$name"
    if [ -f "$path" ]; then
        printf '%s\tPASS\t%s\n' "$name" "$path" >>"$OUT/input-verification.tsv"
        case "$name" in
            */*) : ;;
            *) cp "$path" "$OUT/input/$name" ;;
        esac
    else
        printf '%s\tFAIL\t%s\n' "$name" "$path" >>"$OUT/input-verification.tsv"
        failures=$((failures + 1))
    fi
done

if [ "$failures" -ne 0 ]; then
    printf 'FAIL\n' >"$OUT/analysis.status"
    printf 'missing Phase B1 inputs: %s\n' "$failures" >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
fi

b1_status=$(tr -d '\r\n' <"$B1_OUT/audit.status")
b1_head=$(awk -F $'\t' '$1 == "head" { print $2; exit }' "$B1_OUT/summary.tsv")
[ "$b1_status" = PASS ] || {
    printf 'FAIL\n' >"$OUT/analysis.status"
    printf 'Phase B1 status is not PASS: %s\n' "$b1_status" >&2
    exit 1
}

unresolved_count=$(( $(wc -l <"$B1_OUT/unresolved-needed.tsv") - 1 ))
ambiguous_count=$(( $(wc -l <"$B1_OUT/ambiguous-needed.tsv") - 1 ))
if [ "$unresolved_count" -ne 0 ] || [ "$ambiguous_count" -ne 0 ]; then
    printf 'FAIL\n' >"$OUT/analysis.status"
    printf 'Phase B1 dependency resolution is not unique: unresolved=%s ambiguous=%s\n' \
        "$unresolved_count" "$ambiguous_count" >&2
    exit 1
fi

ELF="$B1_OUT/elf-objects.tsv"
NEEDED="$B1_OUT/elf-needed.tsv"
PROVIDERS="$B1_OUT/name-providers.tsv"
USAGE="$B1_OUT/process-semantic-usage.tsv"
SEMANTIC="$B1_OUT/input/semantic-objects.tsv"

declare -A SEMANTIC_CLASS=()
declare -A PACKAGE=()
declare -A VERSION=()
declare -A PROVIDER_BY_NAME=()
declare -A PROVIDER_NAME_COUNT=()

while IFS=$'\t' read -r semantic path package version base soname lookup rpath runpath; do
    [ "$semantic" = semantic_class ] && continue
    [ -n "$path" ] || continue
    SEMANTIC_CLASS["$path"]=$semantic
    PACKAGE["$path"]=$package
    VERSION["$path"]=$version
done <"$ELF"

while IFS=$'\t' read -r lookup semantic path; do
    [ "$lookup" = lookup_name ] && continue
    [ -n "$lookup" ] || continue
    PROVIDER_NAME_COUNT["$lookup"]=$(( ${PROVIDER_NAME_COUNT[$lookup]:-0} + 1 ))
    PROVIDER_BY_NAME["$lookup"]=$path
done <"$PROVIDERS"

printf 'lookup_name\tprovider_count\n' >"$OUT/duplicate-provider-names.tsv"
for lookup in "${!PROVIDER_NAME_COUNT[@]}"; do
    count=${PROVIDER_NAME_COUNT[$lookup]}
    if [ "$count" -gt 1 ]; then
        printf '%s\t%s\n' "$lookup" "$count" >>"$OUT/duplicate-provider-names.tsv"
    fi
done
{
    head -n 1 "$OUT/duplicate-provider-names.tsv"
    tail -n +2 "$OUT/duplicate-provider-names.tsv" | sort
} >"$OUT/duplicate-provider-names.sorted.tsv"
mv "$OUT/duplicate-provider-names.sorted.tsv" "$OUT/duplicate-provider-names.tsv"
duplicate_count=$(( $(wc -l <"$OUT/duplicate-provider-names.tsv") - 1 ))
[ "$duplicate_count" -eq 0 ] || {
    printf 'FAIL\n' >"$OUT/analysis.status"
    printf 'duplicate provider lookup names detected: %s\n' "$duplicate_count" >&2
    exit 1
}

printf 'consumer_path\tprovider_path\tneeded\n' >"$OUT/resolved-edges.tsv"
while IFS=$'\t' read -r consumer_semantic consumer_path needed; do
    [ "$consumer_semantic" = consumer_semantic_class ] && continue
    provider=${PROVIDER_BY_NAME[$needed]:-}
    if [ -z "$provider" ]; then
        printf 'missing provider for DT_NEEDED=%s consumer=%s\n' "$needed" "$consumer_path" >&2
        failures=$((failures + 1))
        continue
    fi
    printf '%s\t%s\t%s\n' "$consumer_path" "$provider" "$needed" >>"$OUT/resolved-edges.tsv"
done <"$NEEDED"

[ "$failures" -eq 0 ] || {
    printf 'FAIL\n' >"$OUT/analysis.status"
    printf 'failed to resolve %s dependency edges\n' "$failures" >&2
    exit 1
}

[ -n "${SEMANTIC_CLASS[$ENTRYPOINT]:-}" ] || {
    printf 'FAIL\n' >"$OUT/analysis.status"
    printf 'entrypoint is not present in Phase B1 ELF set: %s\n' "$ENTRYPOINT" >&2
    exit 1
}

printf '%s\n' "$ENTRYPOINT" >"$OUT/entrypoint-roots.txt"
printf 'path\n' >"$OUT/all-app-local-roots.tsv"
for path in "${!SEMANTIC_CLASS[@]}"; do
    case "${SEMANTIC_CLASS[$path]}" in
        APP_LOCAL_*) printf '%s\n' "$path" >>"$OUT/all-app-local-roots.tsv" ;;
    esac
done
{
    head -n 1 "$OUT/all-app-local-roots.tsv"
    tail -n +2 "$OUT/all-app-local-roots.tsv" | sort
} >"$OUT/all-app-local-roots.sorted.tsv"
mv "$OUT/all-app-local-roots.sorted.tsv" "$OUT/all-app-local-roots.tsv"

compute_closure() {
    local roots_file=$1 output=$2 paths_output=$3
    local -A seen=()
    local -A depth=()
    local -a queue=()
    local path current provider needed index=0 current_depth

    while IFS= read -r path; do
        [ "$path" = path ] && continue
        [ -n "$path" ] || continue
        [ -n "${SEMANTIC_CLASS[$path]:-}" ] || {
            printf 'root missing from ELF set: %s\n' "$path" >&2
            return 1
        }
        if [ -z "${seen[$path]:-}" ]; then
            seen["$path"]=1
            depth["$path"]=0
            queue+=("$path")
        fi
    done <"$roots_file"

    while [ "$index" -lt "${#queue[@]}" ]; do
        current=${queue[$index]}
        current_depth=${depth[$current]}
        index=$((index + 1))

        while IFS=$'\t' read -r consumer provider needed; do
            [ "$consumer" = consumer_path ] && continue
            [ "$consumer" = "$current" ] || continue
            if [ -z "${seen[$provider]:-}" ]; then
                seen["$provider"]=1
                depth["$provider"]=$((current_depth + 1))
                queue+=("$provider")
            fi
        done <"$OUT/resolved-edges.tsv"
    done

    printf 'depth\tsemantic_class\tpackage\tversion\tpath\n' >"$output"
    : >"$paths_output"
    for path in "${!seen[@]}"; do
        printf '%s\t%s\t%s\t%s\t%s\n' \
            "${depth[$path]}" "${SEMANTIC_CLASS[$path]}" \
            "${PACKAGE[$path]}" "${VERSION[$path]}" "$path" >>"$output"
        printf '%s\n' "$path" >>"$paths_output"
    done
    {
        head -n 1 "$output"
        tail -n +2 "$output" | sort -t $'\t' -k1,1n -k2,2 -k5,5
    } >"$output.sorted"
    mv "$output.sorted" "$output"
    sort -o "$paths_output" "$paths_output"
}

compute_closure \
    "$OUT/entrypoint-roots.txt" \
    "$OUT/entrypoint-static-closure.tsv" \
    "$OUT/entrypoint-static-paths.txt"
compute_closure \
    "$OUT/all-app-local-roots.tsv" \
    "$OUT/all-app-local-static-closure.tsv" \
    "$OUT/all-app-local-static-paths.txt"

printf 'partition\tsemantic_class\tpackage\tversion\tpath\n' >"$OUT/candidate-elf-partition.tsv"
for path in "${!SEMANTIC_CLASS[@]}"; do
    if grep -Fxq -- "$path" "$OUT/entrypoint-static-paths.txt"; then
        partition=ENTRYPOINT_STATIC_CLOSURE
    elif grep -Fxq -- "$path" "$OUT/all-app-local-static-paths.txt"; then
        partition=AUX_APP_LOCAL_STATIC_CLOSURE
    else
        partition=MAPPED_ONLY_DYNAMIC_OR_DISCOVERY
    fi
    printf '%s\t%s\t%s\t%s\t%s\n' \
        "$partition" "${SEMANTIC_CLASS[$path]}" "${PACKAGE[$path]}" \
        "${VERSION[$path]}" "$path" >>"$OUT/candidate-elf-partition.tsv"
done
{
    head -n 1 "$OUT/candidate-elf-partition.tsv"
    tail -n +2 "$OUT/candidate-elf-partition.tsv" | sort -t $'\t' -k1,1 -k2,2 -k5,5
} >"$OUT/candidate-elf-partition.sorted.tsv"
mv "$OUT/candidate-elf-partition.sorted.tsv" "$OUT/candidate-elf-partition.tsv"

printf 'semantic_class\tpath\tprocess_classes\n' >"$OUT/mapped-only-dynamic.tsv"
awk -F $'\t' '
    FNR == NR {
        if (FNR == 1) next
        if ($1 == "MAPPED_ONLY_DYNAMIC_OR_DISCOVERY") {
            semantic[$5]=$2
            wanted[$5]=1
        }
        next
    }
    FNR == 1 { next }
    ($4 in wanted) {
        key=$4 SUBSEP $2
        if (!seen[key]++) {
            classes[$4]=(classes[$4] ? classes[$4] "," : "") $2
        }
    }
    END {
        for (path in wanted) {
            if (!wanted[path]) continue
            print semantic[path] "\t" path "\t" (classes[path] ? classes[path] : "-")
        }
    }
' "$OUT/candidate-elf-partition.tsv" "$USAGE" | sort >>"$OUT/mapped-only-dynamic.tsv"

printf 'semantic_class\tpath\tpackage\tversion\tsha256\tstate\n' >"$OUT/data-capabilities.tsv"
awk -F $'\t' 'NR > 1 && $1 ~ /^PROVIDER_.*_DATA$/ {
    print $1 "\t" $3 "\t" $4 "\t" $5 "\t" $6 "\t" $8
}' "$SEMANTIC" | sort >>"$OUT/data-capabilities.tsv"

{
    printf 'partition\tsemantic_class\tobject_count\n'
    awk -F $'\t' 'NR > 1 { count[$1 SUBSEP $2]++ }
        END { for (key in count) { split(key,a,SUBSEP); print a[1] "\t" a[2] "\t" count[key] } }' \
        "$OUT/candidate-elf-partition.tsv" | sort
} >"$OUT/closure-class-counts.tsv"

entrypoint_count=$(wc -l <"$OUT/entrypoint-static-paths.txt")
all_app_count=$(wc -l <"$OUT/all-app-local-static-paths.txt")
elf_count=$(( $(wc -l <"$ELF") - 1 ))
mapped_only_count=$(( $(wc -l <"$OUT/mapped-only-dynamic.tsv") - 1 ))
data_count=$(( $(wc -l <"$OUT/data-capabilities.tsv") - 1 ))
edge_count=$(( $(wc -l <"$OUT/resolved-edges.tsv") - 1 ))

{
    printf 'field\tvalue\n'
    printf 'branch\t%s\n' "$branch"
    printf 'head\t%s\n' "$head_sha"
    printf 'phase_b1_root\t%s\n' "$B1_OUT"
    printf 'phase_b1_head\t%s\n' "$b1_head"
    printf 'entrypoint\t%s\n' "$ENTRYPOINT"
    printf 'elf_objects\t%s\n' "$elf_count"
    printf 'resolved_dt_needed_edges\t%s\n' "$edge_count"
    printf 'entrypoint_static_closure_objects\t%s\n' "$entrypoint_count"
    printf 'all_app_local_static_closure_objects\t%s\n' "$all_app_count"
    printf 'mapped_only_dynamic_or_discovery_objects\t%s\n' "$mapped_only_count"
    printf 'data_capability_objects\t%s\n' "$data_count"
    printf 'unresolved_needed_edges\t%s\n' "$unresolved_count"
    printf 'ambiguous_needed_edges\t%s\n' "$ambiguous_count"
    printf 'duplicate_provider_names\t%s\n' "$duplicate_count"
    printf 'runtime_launch_performed\tNO\n'
    printf 'promoted_runtime_mutated\tNO\n'
} >"$OUT/summary.tsv"

{
    printf 'This is a read-only graph analysis over the completed Phase B1 receipt.\n'
    printf 'ENTRYPOINT_STATIC_CLOSURE means reachable through captured DT_NEEDED/name relations.\n'
    printf 'MAPPED_ONLY_DYNAMIC_OR_DISCOVERY means observed in process maps but not reachable from any captured app-local ELF DT_NEEDED graph.\n'
    printf 'It does not by itself identify the exact dlopen caller, prove candidate search-path selection, or decide capability ownership.\n'
    printf 'Data capabilities are reported separately and are not ELF closure members.\n'
} >"$OUT/claim-boundary.txt"

printf 'READY_FOR_CAPABILITY_GROUPING_DECISION\n' >"$OUT/next-state.txt"
printf 'PASS\n' >"$OUT/analysis.status"
printf 'selected Obsidian Phase B2 static/runtime closure analysis: PASS\n'
printf 'evidence: %s\n' "$OUT"
printf '\n===== summary =====\n'
cat "$OUT/summary.tsv"
printf '\n===== closure class counts =====\n'
cat "$OUT/closure-class-counts.tsv"
printf '\n===== mapped-only dynamic/discovery =====\n'
cat "$OUT/mapped-only-dynamic.tsv"
