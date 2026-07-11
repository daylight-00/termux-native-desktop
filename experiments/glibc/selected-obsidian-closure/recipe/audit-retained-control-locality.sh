#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
CONTROL_OUT=${CONTROL_OUT:?set CONTROL_OUT to the retained enriched Obsidian control evidence directory}
OUT=${OUT:-$PREFIX/tmp/selected-obsidian-closure/retained-control-locality-audit-$(date +%Y%m%d-%H%M%S)}

for command in git bash awk grep sed sort uniq readelf sha256sum basename dirname mkdir cp wc date head tail mv cat; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

tracked_dirty=$(git -C "$REPO" status --porcelain --untracked-files=no)
if [ -n "$tracked_dirty" ]; then
    printf 'tracked working-tree changes detected; retained-evidence audit requires exact HEAD:\n' >&2
    printf '%s\n' "$tracked_dirty" >&2
    exit 2
fi

REQUIRED_FILES=(
    unique-objects.tsv
    mapped-objects.tsv
    processes.tsv
    object-identities.tsv
    semantic-objects.tsv
    semantic-counts.tsv
    semantic-review.tsv
)

mkdir -p "$OUT/input" "$OUT/work"
printf 'file\tstate\tpath\n' >"$OUT/input-verification.tsv"
input_failures=0
for name in "${REQUIRED_FILES[@]}"; do
    path="$CONTROL_OUT/$name"
    if [ -f "$path" ]; then
        printf '%s\tPASS\t%s\n' "$name" "$path" >>"$OUT/input-verification.tsv"
        cp "$path" "$OUT/input/$name"
    else
        printf '%s\tFAIL\t%s\n' "$name" "$path" >>"$OUT/input-verification.tsv"
        input_failures=$((input_failures + 1))
    fi
done

for name in topology.status survival.status maps-capture.status identity-enrichment.status; do
    path="$CONTROL_OUT/$name"
    if [ -f "$path" ]; then
        cp "$path" "$OUT/input/$name"
    fi
done

branch=$(git -C "$REPO" branch --show-current)
head_sha=$(git -C "$REPO" rev-parse HEAD)
printf '%s\n' "$REPO" >"$OUT/repository-root.txt"
printf '%s\n' "$branch" >"$OUT/branch.txt"
printf '%s\n' "$head_sha" >"$OUT/head.txt"
printf '%s\n' "$CONTROL_OUT" >"$OUT/control-evidence-root.txt"

if [ "$input_failures" -ne 0 ]; then
    printf 'FAIL\n' >"$OUT/audit.status"
    printf 'retained control input verification failed: %s missing files\n' "$input_failures" >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
fi

SEMANTIC="$CONTROL_OUT/semantic-objects.tsv"
MAPPED="$CONTROL_OUT/mapped-objects.tsv"
PROCESSES="$CONTROL_OUT/processes.tsv"
REVIEW="$CONTROL_OUT/semantic-review.tsv"

review_count=$(( $(wc -l <"$REVIEW") - 1 ))
[ "$review_count" -ge 0 ] || review_count=0

is_candidate_identity_class() {
    case "$1" in
        APP_LOCAL_ELF|APP_LOCAL_DATA|APP_LOCAL_GRAPHICS_VULKAN_SWIFTSHADER_ELF|\
        WORLD_SUBSTRATE_ELF|PROVIDER_PREFIX_ELF|PROVIDER_ROOTFS_ELF|\
        PROVIDER_FONT_DATA|PROVIDER_SCHEMA_DATA|PROVIDER_LOCALE_DATA|\
        PROVIDER_GRAPHICS_*) return 0 ;;
        *) return 1 ;;
    esac
}

is_elf_class() {
    case "$1" in
        *_ELF) return 0 ;;
        *) return 1 ;;
    esac
}

printf 'semantic_class\tpath_class\tpath\tpackage\tversion\tcaptured_sha256\tcurrent_sha256\tidentity_state\n' \
    >"$OUT/candidate-input-identities.tsv"
printf 'semantic_class\tpath\tpackage\tversion\tbasename\tsoname\tlookup_name\trpath\trunpath\n' \
    >"$OUT/elf-objects.tsv"
printf 'consumer_semantic_class\tconsumer_path\tneeded\n' >"$OUT/elf-needed.tsv"
printf 'lookup_name\tsemantic_class\tpath\n' >"$OUT/name-providers.tsv"
printf 'semantic_class\tpath\tstate\treason\n' >"$OUT/analysis-exclusions.tsv"

identity_mismatches=0
identity_missing=0
verified_candidate_inputs=0
verified_elf_objects=0

while IFS=$'\t' read -r semantic_class path_class path package version captured_sha build_id state; do
    [ "$semantic_class" = semantic_class ] && continue
    [ -n "$semantic_class" ] || continue

    if ! is_candidate_identity_class "$semantic_class"; then
        printf '%s\t%s\t%s\tnot-candidate-input\n' \
            "$semantic_class" "$path" "$state" >>"$OUT/analysis-exclusions.tsv"
        continue
    fi

    current_sha=MISSING
    identity_state=MISSING_CURRENT_PATH
    if [ -f "$path" ]; then
        current_sha=$(sha256sum "$path" | awk '{print $1}')
        if [ "$captured_sha" = "$current_sha" ]; then
            identity_state=MATCH
            verified_candidate_inputs=$((verified_candidate_inputs + 1))
        else
            identity_state=HASH_MISMATCH
            identity_mismatches=$((identity_mismatches + 1))
        fi
    else
        identity_missing=$((identity_missing + 1))
    fi

    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$semantic_class" "$path_class" "$path" "$package" "$version" \
        "$captured_sha" "$current_sha" "$identity_state" \
        >>"$OUT/candidate-input-identities.tsv"

    if ! is_elf_class "$semantic_class"; then
        continue
    fi
    if [ "$identity_state" != MATCH ]; then
        printf '%s\t%s\t%s\tidentity-not-reproducible\n' \
            "$semantic_class" "$path" "$state" >>"$OUT/analysis-exclusions.tsv"
        continue
    fi

    dynamic="$OUT/work/dynamic-$verified_elf_objects.txt"
    if ! readelf -d "$path" >"$dynamic" 2>"$dynamic.stderr"; then
        printf '%s\t%s\t%s\treadelf-dynamic-failed\n' \
            "$semantic_class" "$path" "$state" >>"$OUT/analysis-exclusions.tsv"
        continue
    fi

    base=$(basename "$path")
    soname=$(awk '/\(SONAME\)/ { line=$0; sub(/^.*\[/, "", line); sub(/\].*$/, "", line); print line; exit }' "$dynamic")
    rpath=$(awk '/\(RPATH\)/ { line=$0; sub(/^.*\[/, "", line); sub(/\].*$/, "", line); print line; exit }' "$dynamic")
    runpath=$(awk '/\(RUNPATH\)/ { line=$0; sub(/^.*\[/, "", line); sub(/\].*$/, "", line); print line; exit }' "$dynamic")
    [ -n "$soname" ] || soname=-
    [ -n "$rpath" ] || rpath=-
    [ -n "$runpath" ] || runpath=-
    lookup_name=$base
    [ "$soname" = - ] || lookup_name=$soname

    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$semantic_class" "$path" "$package" "$version" "$base" \
        "$soname" "$lookup_name" "$rpath" "$runpath" \
        >>"$OUT/elf-objects.tsv"
    printf '%s\t%s\t%s\n' "$lookup_name" "$semantic_class" "$path" \
        >>"$OUT/name-providers.tsv"

    awk -v c="$semantic_class" -v p="$path" '
        /\(NEEDED\)/ {
            line=$0
            sub(/^.*\[/, "", line)
            sub(/\].*$/, "", line)
            print c "\t" p "\t" line
        }
    ' "$dynamic" >>"$OUT/elf-needed.tsv"

    verified_elf_objects=$((verified_elf_objects + 1))
done <"$SEMANTIC"

{
    head -n 1 "$OUT/name-providers.tsv"
    tail -n +2 "$OUT/name-providers.tsv" | sort -t $'\t' -k1,1 -k2,2 -k3,3
} >"$OUT/work/name-providers.sorted.tsv"
mv "$OUT/work/name-providers.sorted.tsv" "$OUT/name-providers.tsv"

{
    head -n 1 "$OUT/elf-needed.tsv"
    tail -n +2 "$OUT/elf-needed.tsv" | sort -t $'\t' -k2,2 -k3,3
} >"$OUT/work/elf-needed.sorted.tsv"
mv "$OUT/work/elf-needed.sorted.tsv" "$OUT/elf-needed.tsv"

printf 'lookup_name\tapp_local_count\texternal_count\tapp_local_paths\texternal_paths\n' \
    >"$OUT/locality-collisions.tsv"
awk -F $'\t' '
    NR == 1 { next }
    {
        name=$1; cls=$2; path=$3
        if (cls ~ /^APP_LOCAL/) {
            app_count[name]++
            app_paths[name]=(app_paths[name] ? app_paths[name] ";" : "") path
        } else {
            ext_count[name]++
            ext_paths[name]=(ext_paths[name] ? ext_paths[name] ";" : "") path
        }
    }
    END {
        for (name in app_count) {
            if (ext_count[name] > 0) {
                print name "\t" app_count[name] "\t" ext_count[name] "\t" \
                    app_paths[name] "\t" ext_paths[name]
            }
        }
    }
' "$OUT/name-providers.tsv" | sort >>"$OUT/locality-collisions.tsv"

printf 'consumer_semantic_class\tconsumer_path\tneeded\tcandidate_count\tapp_local_count\tprefix_count\trootfs_count\tother_count\tcandidate_paths\n' \
    >"$OUT/needed-resolution.tsv"
awk -F $'\t' '
    FNR == NR {
        if (FNR == 1) next
        name=$1; cls=$2; path=$3
        count[name]++
        paths[name]=(paths[name] ? paths[name] ";" : "") path
        if (cls ~ /^APP_LOCAL/) app[name]++
        else if (cls == "PROVIDER_PREFIX_ELF" || cls == "WORLD_SUBSTRATE_ELF") prefix[name]++
        else if (cls ~ /^PROVIDER_ROOTFS/ || cls ~ /^PROVIDER_GRAPHICS/) rootfs[name]++
        else other[name]++
        next
    }
    FNR == 1 { next }
    {
        c=$1; p=$2; n=$3
        print c "\t" p "\t" n "\t" (count[n]+0) "\t" \
            (app[n]+0) "\t" (prefix[n]+0) "\t" (rootfs[n]+0) "\t" \
            (other[n]+0) "\t" (paths[n] ? paths[n] : "-")
    }
' "$OUT/name-providers.tsv" "$OUT/elf-needed.tsv" \
    | sort -t $'\t' -k2,2 -k3,3 >>"$OUT/needed-resolution.tsv"

{
    head -n 1 "$OUT/needed-resolution.tsv"
    awk -F $'\t' 'NR > 1 && $4 == 0 { print }' "$OUT/needed-resolution.tsv"
} >"$OUT/unresolved-needed.tsv"

{
    head -n 1 "$OUT/needed-resolution.tsv"
    awk -F $'\t' 'NR > 1 && $4 > 1 { print }' "$OUT/needed-resolution.tsv"
} >"$OUT/ambiguous-needed.tsv"

printf 'pid\tprocess_class\tsemantic_class\tpath\n' >"$OUT/process-semantic-usage.tsv"
awk -F $'\t' '
    FNR == NR {
        if (FNR == 1) next
        semantic[$3]=$1
        next
    }
    FNR == 1 { next }
    {
        cls=(semantic[$4] ? semantic[$4] : "UNCLASSIFIED_RUNTIME_PATH")
        print $1 "\t" $2 "\t" cls "\t" $4
    }
' "$SEMANTIC" "$MAPPED" | sort -u >>"$OUT/process-semantic-usage.tsv"

{
    printf 'semantic_class\tpackage\tversion\tobject_count\n'
    awk -F $'\t' 'NR > 1 {
        key=$1 "\t" $4 "\t" $5
        count[key]++
    } END { for (key in count) print key "\t" count[key] }' "$SEMANTIC" | sort
} >"$OUT/provider-package-summary.tsv"

collision_count=$(( $(wc -l <"$OUT/locality-collisions.tsv") - 1 ))
unresolved_count=$(( $(wc -l <"$OUT/unresolved-needed.tsv") - 1 ))
ambiguous_count=$(( $(wc -l <"$OUT/ambiguous-needed.tsv") - 1 ))
process_count=$(( $(wc -l <"$PROCESSES") - 1 ))
semantic_count=$(( $(wc -l <"$SEMANTIC") - 1 ))

{
    printf 'field\tvalue\n'
    printf 'branch\t%s\n' "$branch"
    printf 'head\t%s\n' "$head_sha"
    printf 'control_evidence_root\t%s\n' "$CONTROL_OUT"
    printf 'semantic_objects\t%s\n' "$semantic_count"
    printf 'captured_processes\t%s\n' "$process_count"
    printf 'semantic_review_objects\t%s\n' "$review_count"
    printf 'verified_candidate_inputs\t%s\n' "$verified_candidate_inputs"
    printf 'verified_elf_objects\t%s\n' "$verified_elf_objects"
    printf 'candidate_input_hash_mismatches\t%s\n' "$identity_mismatches"
    printf 'candidate_input_missing_paths\t%s\n' "$identity_missing"
    printf 'app_local_external_name_collisions\t%s\n' "$collision_count"
    printf 'unresolved_needed_edges\t%s\n' "$unresolved_count"
    printf 'ambiguous_needed_edges\t%s\n' "$ambiguous_count"
    printf 'runtime_launch_performed\tNO\n'
    printf 'promoted_runtime_mutated\tNO\n'
} >"$OUT/summary.tsv"

{
    printf 'This is a read-only audit of retained control evidence.\n'
    printf 'PASS means the retained candidate-relevant bytes still match their captured hashes and the analysis completed.\n'
    printf 'It does not mean locality policy is decided, the static closure is complete, or a selected candidate is ready.\n'
    printf 'Collision, ambiguous-edge, and unresolved-edge rows are decision inputs, not automatic failures.\n'
} >"$OUT/claim-boundary.txt"

failures=0
[ "$review_count" -eq 0 ] || failures=$((failures + 1))
[ "$identity_mismatches" -eq 0 ] || failures=$((failures + 1))
[ "$identity_missing" -eq 0 ] || failures=$((failures + 1))

if [ "$failures" -ne 0 ]; then
    printf 'REFRESH_OR_IDENTITY_RECONCILIATION_REQUIRED\n' >"$OUT/next-state.txt"
    printf 'FAIL\n' >"$OUT/audit.status"
    printf 'retained Obsidian control locality input audit: FAIL (%s blocking conditions)\n' "$failures" >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
fi

printf 'READY_FOR_LOCALITY_AND_STATIC_RUNTIME_DECISION\n' >"$OUT/next-state.txt"
printf 'PASS\n' >"$OUT/audit.status"
printf 'retained Obsidian control locality input audit: PASS\n'
printf 'evidence: %s\n' "$OUT"
printf '\n===== summary =====\n'
cat "$OUT/summary.tsv"
printf '\n===== locality collisions =====\n'
cat "$OUT/locality-collisions.tsv"
printf '\n===== unresolved needed =====\n'
cat "$OUT/unresolved-needed.tsv"
printf '\n===== ambiguous needed =====\n'
cat "$OUT/ambiguous-needed.tsv"
