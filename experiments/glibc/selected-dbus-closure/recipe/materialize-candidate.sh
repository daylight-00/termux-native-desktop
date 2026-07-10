#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

STATIC_OUT=${STATIC_OUT:?set STATIC_OUT to the successful ownership-aware static evidence directory}
CANDIDATE=${CANDIDATE:-$PREFIX/tmp/selected-dbus-candidate-$(date +%Y%m%d-%H%M%S)}

PROVIDERS="$STATIC_OUT/providers.tsv"
GRAPH="$STATIC_OUT/graph.tsv"
WORLD="$STATIC_OUT/world-prefix.tsv"

for file in "$PROVIDERS" "$GRAPH" "$WORLD"; do
    [ -f "$file" ] || {
        printf 'missing required static evidence: %s\n' "$file" >&2
        exit 1
    }
done

[ ! -e "$CANDIDATE" ] || {
    printf 'candidate already exists: %s\n' "$CANDIDATE" >&2
    exit 1
}

PARENT=$(dirname "$CANDIDATE")
NAME=$(basename "$CANDIDATE")
STAGE="$PARENT/.${NAME}.stage.$$"

mkdir -p "$PARENT"
rm -rf "$STAGE"
mkdir -p "$STAGE/lib" "$STAGE/meta"

cleanup() {
    rm -rf "$STAGE"
}
trap cleanup EXIT

build_id_of() {
    readelf -n "$1" 2>/dev/null \
        | awk '
            /Build ID:/ && id == "" { id = $3 }
            END { if (id != "") print id }
        '
}

soname_of() {
    readelf -d "$1" 2>/dev/null \
        | sed -n 's/.*Library soname: \[\(.*\)\]/\1/p'
}

cp "$GRAPH" "$STAGE/meta/graph.tsv"
cp "$PROVIDERS" "$STAGE/meta/source-providers.tsv"
cp "$WORLD" "$STAGE/meta/world-substrate.tsv"

printf 'source_path\tpackage\tversion\tsource_sha256\tsource_build_id\tsoname\tcandidate_file\tcandidate_sha256\tcandidate_build_id\n' \
    >"$STAGE/receipt.tsv"

printf 'soname\ttarget\n' >"$STAGE/soname-links.tsv"

count=0
while IFS=$'\t' read -r source package version source_sha source_build; do
    [ "$source" = path ] && continue
    [ -n "$source" ] || continue

    [ -f "$source" ] || {
        printf 'source provider missing: %s\n' "$source" >&2
        exit 1
    }

    actual_source_sha=$(sha256sum "$source" | awk '{print $1}')
    [ "$actual_source_sha" = "$source_sha" ] || {
        printf 'source hash drift: %s\n' "$source" >&2
        printf 'expected: %s\nactual:   %s\n' "$source_sha" "$actual_source_sha" >&2
        exit 1
    }

    actual_source_build=$(build_id_of "$source")
    [ -n "$actual_source_build" ] || actual_source_build=NONE
    [ "$actual_source_build" = "$source_build" ] || {
        printf 'source Build ID drift: %s\n' "$source" >&2
        printf 'expected: %s\nactual:   %s\n' "$source_build" "$actual_source_build" >&2
        exit 1
    }

    soname=$(soname_of "$source")
    [ -n "$soname" ] || {
        printf 'provider has no SONAME: %s\n' "$source" >&2
        exit 1
    }

    base=$(basename "$source")
    candidate_file="lib/$base"
    destination="$STAGE/$candidate_file"

    cp "$source" "$destination"

    candidate_sha=$(sha256sum "$destination" | awk '{print $1}')
    candidate_build=$(build_id_of "$destination")
    [ -n "$candidate_build" ] || candidate_build=NONE

    [ "$candidate_sha" = "$source_sha" ] || {
        printf 'candidate byte mismatch after copy: %s\n' "$destination" >&2
        exit 1
    }

    [ "$candidate_build" = "$source_build" ] || {
        printf 'candidate Build ID mismatch after copy: %s\n' "$destination" >&2
        exit 1
    }

    link="$STAGE/lib/$soname"
    if [ "$soname" != "$base" ]; then
        if [ -e "$link" ] || [ -L "$link" ]; then
            existing=$(readlink "$link" 2>/dev/null || true)
            [ "$existing" = "$base" ] || {
                printf 'conflicting SONAME target: %s -> %s, expected %s\n' \
                    "$link" "$existing" "$base" >&2
                exit 1
            }
        else
            ln -s "$base" "$link"
        fi
    fi

    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$source" "$package" "$version" "$source_sha" "$source_build" \
        "$soname" "$candidate_file" "$candidate_sha" "$candidate_build" \
        >>"$STAGE/receipt.tsv"

    printf '%s\t%s\n' "$soname" "$base" >>"$STAGE/soname-links.tsv"
    count=$((count + 1))
done <"$PROVIDERS"

[ "$count" -gt 0 ] || {
    printf 'no providers materialized\n' >&2
    exit 1
}

candidate_id=$(
    cat \
        "$STAGE/receipt.tsv" \
        "$STAGE/meta/graph.tsv" \
        "$STAGE/meta/world-substrate.tsv" \
        | sha256sum \
        | awk '{print $1}'
)

printf '%s\n' "$candidate_id" >"$STAGE/candidate-id"
printf '%s\n' "$STATIC_OUT" >"$STAGE/meta/source-static-evidence-path.txt"

mv "$STAGE" "$CANDIDATE"
trap - EXIT

printf '\n===== candidate =====\n'
printf 'path: %s\n' "$CANDIDATE"
printf 'id:   %s\n' "$candidate_id"
printf 'providers: %s\n' "$count"

printf '\n===== candidate files =====\n'
find "$CANDIDATE/lib" -maxdepth 1 -mindepth 1 -printf '%f\t%y\t%l\n' | sort

printf '\n===== receipt =====\n'
cat "$CANDIDATE/receipt.tsv"

printf '\ncandidate materialization: PASS\n'
