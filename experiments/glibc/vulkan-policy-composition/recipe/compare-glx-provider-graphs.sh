#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

EXPLICIT_OUT=${EXPLICIT_OUT:?set EXPLICIT_OUT to the explicit-freedreno maps evidence directory}
IMPLICIT_OUT=${IMPLICIT_OUT:?set IMPLICIT_OUT to the implicit-discovery maps evidence directory}

EXPLICIT_IDENTITIES="$EXPLICIT_OUT/mapped-provider-identities.tsv"
IMPLICIT_IDENTITIES="$IMPLICIT_OUT/mapped-provider-identities.tsv"
EXPLICIT_RENDERER="$EXPLICIT_OUT/probe.stdout"
IMPLICIT_RENDERER="$IMPLICIT_OUT/probe.stdout"
OUT=${OUT:-$IMPLICIT_OUT/provider-graph-comparison}

for file in \
    "$EXPLICIT_IDENTITIES" \
    "$IMPLICIT_IDENTITIES" \
    "$EXPLICIT_RENDERER" \
    "$IMPLICIT_RENDERER"
do
    [ -f "$file" ] || {
        printf 'missing comparison input: %s\n' "$file" >&2
        exit 1
    }
done

mkdir -p "$OUT"

awk -F $'\t' 'NR > 1 { print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $6 "\t" $7 "\t" $8 }' \
    "$EXPLICIT_IDENTITIES" \
    | sort -u \
    >"$OUT/explicit-identities.tsv"

awk -F $'\t' 'NR > 1 { print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $6 "\t" $7 "\t" $8 }' \
    "$IMPLICIT_IDENTITIES" \
    | sort -u \
    >"$OUT/implicit-identities.tsv"

comm -23 \
    "$OUT/explicit-identities.tsv" \
    "$OUT/implicit-identities.tsv" \
    >"$OUT/explicit-only-identities.tsv"

comm -13 \
    "$OUT/explicit-identities.tsv" \
    "$OUT/implicit-identities.tsv" \
    >"$OUT/implicit-only-identities.tsv"

awk -F $'\t' 'NR > 1 { print $2 }' "$EXPLICIT_IDENTITIES" | sort -u >"$OUT/explicit-paths.txt"
awk -F $'\t' 'NR > 1 { print $2 }' "$IMPLICIT_IDENTITIES" | sort -u >"$OUT/implicit-paths.txt"

comm -23 "$OUT/explicit-paths.txt" "$OUT/implicit-paths.txt" >"$OUT/explicit-only-paths.txt"
comm -13 "$OUT/explicit-paths.txt" "$OUT/implicit-paths.txt" >"$OUT/implicit-only-paths.txt"

{
    printf 'side\tpath_class\tpackage\tversion\tobject_count\n'
    awk -F $'\t' '
        NR > 1 {
            key = $1 "\t" $3 "\t" $4
            count[key]++
        }
        END {
            for (k in count)
                print "explicit\t" k "\t" count[k]
        }
    ' "$EXPLICIT_IDENTITIES"

    awk -F $'\t' '
        NR > 1 {
            key = $1 "\t" $3 "\t" $4
            count[key]++
        }
        END {
            for (k in count)
                print "implicit\t" k "\t" count[k]
        }
    ' "$IMPLICIT_IDENTITIES"
} | sort >"$OUT/package-summary.tsv"

printf 'GLX provider graph comparison: PASS\n'
printf 'output: %s\n' "$OUT"

printf '\n===== explicit renderer =====\n'
cat "$EXPLICIT_RENDERER"

printf '\n===== implicit renderer =====\n'
cat "$IMPLICIT_RENDERER"

printf '\n===== explicit-only paths =====\n'
cat "$OUT/explicit-only-paths.txt"

printf '\n===== implicit-only paths =====\n'
cat "$OUT/implicit-only-paths.txt"

printf '\n===== package summary =====\n'
cat "$OUT/package-summary.tsv"
