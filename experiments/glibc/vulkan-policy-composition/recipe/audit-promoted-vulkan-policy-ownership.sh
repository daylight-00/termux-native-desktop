#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/promoted-vulkan-policy-ownership-$(date +%Y%m%d-%H%M%S)}

for command in git awk grep sort sed mkdir date; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

mkdir -p "$OUT"

branch=$(git -C "$REPO" branch --show-current)
head=$(git -C "$REPO" rev-parse HEAD)
printf '%s\n' "$REPO" >"$OUT/repository-root.txt"
printf '%s\n' "$branch" >"$OUT/branch.txt"
printf '%s\n' "$head" >"$OUT/head.txt"

scope_of_path() {
    local path=$1
    case "$path" in
        modules/*|packages/*|tools/*|tests/*)
            printf 'PROMOTED_OR_VALIDATION\n'
            ;;
        README.md|STATUS.md|docs/architecture.md|docs/glibc-layer.md|docs/gpu.md|docs/desktop-session.md|docs/PROJECT_CONTEXT.md|docs/decisions/*)
            printf 'INTEGRATED_DOCUMENTATION\n'
            ;;
        experiments/*|docs/refactor/*|docs/system-foundation/*)
            printf 'EXPERIMENT_OR_HISTORY\n'
            ;;
        *)
            printf 'OTHER_TRACKED\n'
            ;;
    esac
}

role_of_match() {
    local token=$1 text=$2
    case "$token" in
        VK_DRIVER_FILES|VK_ICD_FILENAMES)
            case "$text" in
                *export*"$token"*|*unset*"$token"*)
                    printf 'POLICY_PRODUCER_OR_CLEARER\n'
                    ;;
                *'${'"$token"*|*'$'"$token"*|*"$token="*)
                    printf 'DIRECT_POLICY_CONSUMER_OR_ASSERTION\n'
                    ;;
                *)
                    printf 'POLICY_REFERENCE\n'
                    ;;
            esac
            ;;
        'source $HOME/gl/env'|'source "$HOME/gl/env"'|'source ~/gl/env')
            printf 'TRANSITIVE_SHARED_ENV_CONSUMER\n'
            ;;
        GL_ICD|GLIBC_FREEDRENO_ICD)
            printf 'PROVIDER_LOCATION_DEFINITION\n'
            ;;
        MESA_LOADER_DRIVER_OVERRIDE)
            printf 'OPENGL_PROVIDER_MODE_COMPOSITION\n'
            ;;
        GL_GPU)
            printf 'APPLICATION_FEATURE_MODE\n'
            ;;
        *)
            printf 'REFERENCE\n'
            ;;
    esac
}

printf 'scope\trole\ttoken\tpath\tline\ttext\n' >"$OUT/all-occurrences.tsv"

scan_token() {
    local token=$1 pattern=$2
    local raw path line text scope role

    while IFS= read -r raw; do
        [ -n "$raw" ] || continue
        path=${raw%%:*}
        raw=${raw#*:}
        line=${raw%%:*}
        text=${raw#*:}
        scope=$(scope_of_path "$path")
        role=$(role_of_match "$token" "$text")
        text=$(printf '%s' "$text" | sed 's/\t/    /g')
        printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
            "$scope" "$role" "$token" "$path" "$line" "$text" \
            >>"$OUT/all-occurrences.tsv"
    done < <(git -C "$REPO" grep -n -I -E -- "$pattern" -- \
        ':!docs/refactor/0075-*' 2>/dev/null || true)
}

scan_token VK_DRIVER_FILES 'VK_DRIVER_FILES'
scan_token VK_ICD_FILENAMES 'VK_ICD_FILENAMES'
scan_token GL_ICD '(^|[^A-Za-z0-9_])GL_ICD([^A-Za-z0-9_]|$)'
scan_token GLIBC_FREEDRENO_ICD 'GLIBC_FREEDRENO_ICD'
scan_token 'source "$HOME/gl/env"' 'source[[:space:]]+"?\$HOME/gl/env"?'
scan_token 'source ~/gl/env' 'source[[:space:]]+~/?gl/env'
scan_token MESA_LOADER_DRIVER_OVERRIDE 'MESA_LOADER_DRIVER_OVERRIDE'
scan_token GL_GPU '(^|[^A-Za-z0-9_])GL_GPU([^A-Za-z0-9_]|$)'

{
    head -n 1 "$OUT/all-occurrences.tsv"
    tail -n +2 "$OUT/all-occurrences.tsv" | sort -t $'\t' -k1,1 -k4,4 -k5,5n -k3,3
} >"$OUT/all-occurrences.sorted.tsv"
mv "$OUT/all-occurrences.sorted.tsv" "$OUT/all-occurrences.tsv"

for scope in PROMOTED_OR_VALIDATION INTEGRATED_DOCUMENTATION EXPERIMENT_OR_HISTORY OTHER_TRACKED; do
    output=$(printf '%s' "$scope" | tr '[:upper:]' '[:lower:]' | tr '_' '-')
    {
        head -n 1 "$OUT/all-occurrences.tsv"
        awk -F $'\t' -v scope="$scope" 'NR > 1 && $1 == scope' "$OUT/all-occurrences.tsv"
    } >"$OUT/$output-occurrences.tsv"
done

printf 'path\tcontract\tstate\n' >"$OUT/known-contracts.tsv"
FAILURES=0

record_contract() {
    local path=$1 contract=$2 state=$3
    printf '%s\t%s\t%s\n' "$path" "$contract" "$state" >>"$OUT/known-contracts.tsv"
    if [ "$state" != PASS ]; then
        FAILURES=$((FAILURES + 1))
    fi
}

file_contains() {
    local path=$1 pattern=$2
    [ -f "$REPO/$path" ] && grep -Eq -- "$pattern" "$REPO/$path"
}

if file_contains modules/gl/overlay/home/gl/env 'export[[:space:]]+VK_DRIVER_FILES='; then
    record_contract modules/gl/overlay/home/gl/env shared_env_exports_vk_driver_files PASS
else
    record_contract modules/gl/overlay/home/gl/env shared_env_exports_vk_driver_files FAIL
fi

if file_contains modules/gl/overlay/home/gl/env 'export[[:space:]]+VK_ICD_FILENAMES='; then
    record_contract modules/gl/overlay/home/gl/env shared_env_exports_vk_icd_filenames PASS
else
    record_contract modules/gl/overlay/home/gl/env shared_env_exports_vk_icd_filenames FAIL
fi

if file_contains packages/vscode/launcher/code 'source[[:space:]]+"\$HOME/gl/env"'; then
    record_contract packages/vscode/launcher/code vscode_sources_shared_env PASS
else
    record_contract packages/vscode/launcher/code vscode_sources_shared_env FAIL
fi

if file_contains packages/vscode/launcher/code 'VK_DRIVER_FILES'; then
    record_contract packages/vscode/launcher/code vscode_directly_depends_on_shared_provider_pin PASS
else
    record_contract packages/vscode/launcher/code vscode_directly_depends_on_shared_provider_pin FAIL
fi

if file_contains packages/vscode/launcher/code -- '--use-angle=vulkan'; then
    record_contract packages/vscode/launcher/code vscode_enables_angle_vulkan PASS
else
    record_contract packages/vscode/launcher/code vscode_enables_angle_vulkan FAIL
fi

if file_contains modules/gl/overlay/home/gl/bin/gl-run 'source[[:space:]]+"\$HOME/gl/env"'; then
    record_contract modules/gl/overlay/home/gl/bin/gl-run gl_run_sources_shared_env PASS
else
    record_contract modules/gl/overlay/home/gl/bin/gl-run gl_run_sources_shared_env FAIL
fi

if file_contains modules/gl/overlay/home/gl/bin/gl-run 'VK_DRIVER_FILES'; then
    record_contract modules/gl/overlay/home/gl/bin/gl-run gl_run_requires_provider_pin PASS
else
    record_contract modules/gl/overlay/home/gl/bin/gl-run gl_run_requires_provider_pin FAIL
fi

if file_contains modules/gl/overlay/home/gl/bin/gl-run 'MESA_LOADER_DRIVER_OVERRIDE=zink'; then
    record_contract modules/gl/overlay/home/gl/bin/gl-run gl_run_adds_zink_mode PASS
else
    record_contract modules/gl/overlay/home/gl/bin/gl-run gl_run_adds_zink_mode FAIL
fi

if file_contains packages/obsidian/launcher/obsidian 'source[[:space:]]+"\$HOME/gl/env"'; then
    record_contract packages/obsidian/launcher/obsidian obsidian_sources_shared_env PASS
else
    record_contract packages/obsidian/launcher/obsidian obsidian_sources_shared_env FAIL
fi

if [ -f "$REPO/packages/obsidian/launcher/obsidian-app" ]; then
    if file_contains packages/obsidian/launcher/obsidian-app 'source[[:space:]]+"\$HOME/gl/env"'; then
        record_contract packages/obsidian/launcher/obsidian-app obsidian_app_sources_shared_env PASS
    else
        record_contract packages/obsidian/launcher/obsidian-app obsidian_app_sources_shared_env FAIL
    fi
fi

promoted_policy_refs=$(awk -F $'\t' '
    NR > 1 && $1 == "PROMOTED_OR_VALIDATION" &&
    ($3 == "VK_DRIVER_FILES" || $3 == "VK_ICD_FILENAMES" ||
     $3 == "source \"$HOME/gl/env\"" || $3 == "source ~/gl/env") { count++ }
    END { print count + 0 }
' "$OUT/all-occurrences.tsv")

promoted_files=$(awk -F $'\t' '
    NR > 1 && $1 == "PROMOTED_OR_VALIDATION" { seen[$4]=1 }
    END { for (path in seen) count++; print count + 0 }
' "$OUT/all-occurrences.tsv")

{
    printf 'metric\tvalue\n'
    printf 'repository_root\t%s\n' "$REPO"
    printf 'branch\t%s\n' "$branch"
    printf 'head\t%s\n' "$head"
    printf 'promoted_policy_reference_count\t%s\n' "$promoted_policy_refs"
    printf 'promoted_files_with_any_scanned_token\t%s\n' "$promoted_files"
    printf 'known_contract_failures\t%s\n' "$FAILURES"
} >"$OUT/audit-summary.tsv"

if [ "$FAILURES" -ne 0 ]; then
    printf 'FAIL\n' >"$OUT/audit.status"
    printf 'promoted Vulkan policy ownership audit: FAIL (%s known-contract failures)\n' "$FAILURES" >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
fi

printf 'PASS\n' >"$OUT/audit.status"

printf 'promoted Vulkan policy ownership audit: PASS\n'
printf 'repository: %s\n' "$REPO"
printf 'branch: %s\n' "$branch"
printf 'head: %s\n' "$head"
printf 'evidence: %s\n' "$OUT"
printf '\nNOTE: PASS means the static inventory and current known-contract checks completed.\n'
printf 'It does not authorize removing the shared VK_* policy.\n'

printf '\n===== audit summary =====\n'
cat "$OUT/audit-summary.tsv"

printf '\n===== known contracts =====\n'
cat "$OUT/known-contracts.tsv"

printf '\n===== promoted/validation occurrences =====\n'
cat "$OUT/promoted-or-validation-occurrences.tsv"

printf '\n===== integrated documentation occurrences =====\n'
cat "$OUT/integrated-documentation-occurrences.tsv"
