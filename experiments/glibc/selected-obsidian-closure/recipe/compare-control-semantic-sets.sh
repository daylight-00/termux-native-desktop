#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

BASELINE_OUT=${BASELINE_OUT:?set BASELINE_OUT to the original CPU control evidence directory}
STRICT_OUT=${STRICT_OUT:?set STRICT_OUT to the strict CPU control evidence directory}

BASE="$BASELINE_OUT/semantic-objects.tsv"
STRICT="$STRICT_OUT/semantic-objects.tsv"
OUT=${OUT:-$STRICT_OUT/control-semantic-set-comparison}

for file in "$BASE" "$STRICT"; do
    [ -f "$file" ] || {
        printf 'missing semantic evidence: %s\n' "$file" >&2
        exit 1
    }
done

mkdir -p "$OUT"

awk -F $'\t' 'NR > 1 { print $1 "\t" $3 }' "$BASE" \
    | sort -u \
    >"$OUT/baseline-class-path.tsv"

awk -F $'\t' 'NR > 1 { print $1 "\t" $3 }' "$STRICT" \
    | sort -u \
    >"$OUT/strict-class-path.tsv"

comm -23 \
    "$OUT/baseline-class-path.tsv" \
    "$OUT/strict-class-path.tsv" \
    >"$OUT/baseline-only-class-path.tsv"

comm -13 \
    "$OUT/baseline-class-path.tsv" \
    "$OUT/strict-class-path.tsv" \
    >"$OUT/strict-only-class-path.tsv"

awk -F $'\t' 'NR > 1 { print $3 }' "$BASE" \
    | sort -u \
    >"$OUT/baseline-paths.txt"

awk -F $'\t' 'NR > 1 { print $3 }' "$STRICT" \
    | sort -u \
    >"$OUT/strict-paths.txt"

comm -23 \
    "$OUT/baseline-paths.txt" \
    "$OUT/strict-paths.txt" \
    >"$OUT/baseline-only-paths.txt"

comm -13 \
    "$OUT/baseline-paths.txt" \
    "$OUT/strict-paths.txt" \
    >"$OUT/strict-only-paths.txt"

{
    printf 'path\tbaseline_class\tstrict_class\n'
    awk -F $'\t' '
        NR == FNR {
            if (FNR > 1)
                baseline[$3] = $1
            next
        }
        FNR > 1 && ($3 in baseline) && baseline[$3] != $1 {
            print $3 "\t" baseline[$3] "\t" $1
        }
    ' "$BASE" "$STRICT" \
        | sort
} >"$OUT/common-path-class-changes.tsv"

{
    printf 'semantic_class\tbaseline_only\tstrict_only\n'
    awk -F $'\t' '
        FILENAME == ARGV[1] { baseline[$1]++; next }
        FILENAME == ARGV[2] { strict[$1]++; next }
        END {
            for (c in baseline)
                all[c] = 1
            for (c in strict)
                all[c] = 1
            for (c in all)
                print c "\t" (baseline[c] + 0) "\t" (strict[c] + 0)
        }
    ' \
        "$OUT/baseline-only-class-path.tsv" \
        "$OUT/strict-only-class-path.tsv" \
        | sort
} >"$OUT/class-delta-summary.tsv"

printf '\ncontrol semantic-set comparison: PASS\n'
printf 'output: %s\n' "$OUT"

printf '\n===== class delta summary =====\n'
cat "$OUT/class-delta-summary.tsv"

printf '\n===== baseline-only paths =====\n'
cat "$OUT/baseline-only-paths.txt"

printf '\n===== strict-only paths =====\n'
cat "$OUT/strict-only-paths.txt"

printf '\n===== common-path class changes =====\n'
cat "$OUT/common-path-class-changes.tsv"
