#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
WORK_ROOT=${PROVIDER_AUTHORITY_WORK_ROOT:-$REPO/experiments/glibc/selected-obsidian-provider-authority/work}
HANDOFF_DIR=${HANDOFF_DIR:-$HOME/Downloads}
STAMP=${STAMP:-$(date -u +%Y%m%dT%H%M%SZ)}
PREFIX=${PREFIX:?PREFIX is required}
SOURCE_REPO=${SOURCE_REPO:-$WORK_ROOT/source/termux-pacman-glibc-packages}
SOURCE_REPO_EXPECTED_HEAD=${SOURCE_REPO_EXPECTED_HEAD:-fd2ae25e04f3ea26d6c7b4678020814889331d86}
OUT=${OUT:-$WORK_ROOT/receipts/unpacked/selected-obsidian-generic-exact-candidate-evidence-$STAMP}
CREATE_ARCHIVE=${CREATE_ARCHIVE:-1}
ARCHIVE=${ARCHIVE:-$HANDOFF_DIR/selected-obsidian-generic-exact-candidate-evidence-$STAMP.tar.zst}

for command in git python3 find tar zstd sha256sum awk date dirname basename mkdir rm; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 2
    }
done

tracked_dirty=$(git -C "$REPO" status --porcelain --untracked-files=no)
if [ -n "$tracked_dirty" ]; then
    printf 'tracked repository changes detected:\n%s\n' "$tracked_dirty" >&2
    exit 2
fi
if [ -e "$OUT" ] || [ -L "$OUT" ]; then
    printf 'refusing existing output: %s\n' "$OUT" >&2
    exit 2
fi
if [ ! -d "$SOURCE_REPO" ] || [ -L "$SOURCE_REPO" ]; then
    printf 'missing or unsafe retained source checkout: %s\n' "$SOURCE_REPO" >&2
    exit 2
fi
case "$CREATE_ARCHIVE" in
    0|1) ;;
    *) printf 'CREATE_ARCHIVE must be 0 or 1\n' >&2; exit 2 ;;
esac
if [ "$CREATE_ARCHIVE" = 1 ] && { [ -e "$ARCHIVE" ] || [ -L "$ARCHIVE" ] || [ -e "$ARCHIVE.sha256" ]; }; then
    printf 'refusing existing archive path: %s\n' "$ARCHIVE" >&2
    exit 2
fi

export PROJECT_REPO="$REPO" SOURCE_REPO SOURCE_REPO_EXPECTED_HEAD PREFIX OUT
python3 "$SCRIPT_DIR/collect-generic-exact-candidate-evidence.py"

[ "$(cat "$OUT/analysis.status")" = PASS ] || {
    printf 'collector did not produce PASS status\n' >&2
    exit 1
}
special=$(find "$OUT" \( -type l -o \( ! -type f ! -type d \) \) -print -quit)
if [ -n "$special" ]; then
    printf 'unsafe evidence member type: %s\n' "$special" >&2
    exit 1
fi

ARCHIVE_SHA256=-
if [ "$CREATE_ARCHIVE" = 1 ]; then
    mkdir -p "$HANDOFF_DIR"
    out_parent=$(dirname "$OUT")
    out_name=$(basename "$OUT")
    tar -C "$out_parent" -cf - "$out_name" | zstd -T0 -19 -q -o "$ARCHIVE"
    [ -s "$ARCHIVE" ] || {
        printf 'archive was not created: %s\n' "$ARCHIVE" >&2
        exit 1
    }
    zstd -t -q "$ARCHIVE"
    if tar --zstd -tf "$ARCHIVE" | grep -E '(^/|(^|/)\.\.(/|$))' >/dev/null; then
        rm -f "$ARCHIVE"
        printf 'archive path safety validation failed\n' >&2
        exit 1
    fi
    ARCHIVE_SHA256=$(sha256sum "$ARCHIVE" | awk '{print $1}')
    printf '%s  %s\n' "$ARCHIVE_SHA256" "$(basename "$ARCHIVE")" > "$ARCHIVE.sha256"
    (cd "$(dirname "$ARCHIVE")" && sha256sum -c "$(basename "$ARCHIVE").sha256")
fi

printf '\nGENERIC_EXACT_CANDIDATE_EVIDENCE=PASS\n'
printf 'OUT=%s\n' "$OUT"
printf 'SOURCE_REPO=%s\n' "$SOURCE_REPO"
printf 'SOURCE_REPO_EXPECTED_HEAD=%s\n' "$SOURCE_REPO_EXPECTED_HEAD"
printf 'CREATE_ARCHIVE=%s\n' "$CREATE_ARCHIVE"
printf 'ARCHIVE=%s\n' "${ARCHIVE:--}"
printf 'ARCHIVE_SHA256=%s\n' "$ARCHIVE_SHA256"
