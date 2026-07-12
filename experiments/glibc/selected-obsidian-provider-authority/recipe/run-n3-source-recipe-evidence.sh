#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)

for command in git python3 tar sha256sum find grep awk date dirname basename mkdir rm; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

tracked_dirty=$(git -C "$REPO" status --porcelain --untracked-files=no)
if [ -n "$tracked_dirty" ]; then
    printf 'tracked working-tree changes detected; source evidence requires exact HEAD:\n%s\n' "$tracked_dirty" >&2
    exit 2
fi

BASE=${EVIDENCE_BASE:-$PREFIX/tmp/selected-obsidian-provider-authority}
DOWNLOADS=${DOWNLOADS_DIR:-$HOME/Downloads}
STAMP=${STAMP:-$(date +%Y%m%d-%H%M%S)}
N3_OUT=${N3_OUT:-$BASE/selected-obsidian-provider-authority-n3-normalized-classification-20260712-165805}
SOURCE_REPO=${SOURCE_REPO:-$DOWNLOADS/termux-pacman-glibc-packages-source}
OUT=${OUT:-$BASE/selected-obsidian-provider-authority-n3-source-recipe-evidence-$STAMP}
ARCHIVE=${ARCHIVE:-$DOWNLOADS/selected-obsidian-provider-authority-n3-source-recipe-evidence-results-$STAMP.tgz}

case "$OUT" in
    "$BASE"/*) ;;
    *)
        printf 'OUT must remain under EVIDENCE_BASE: %s\n' "$OUT" >&2
        exit 2
        ;;
esac
case "$ARCHIVE" in
    "$DOWNLOADS"/*) ;;
    *)
        printf 'ARCHIVE must remain under DOWNLOADS_DIR: %s\n' "$ARCHIVE" >&2
        exit 2
        ;;
esac
case "$SOURCE_REPO" in
    "$REPO"|"$REPO"/*)
        printf 'SOURCE_REPO must remain outside the project checkout: %s\n' "$SOURCE_REPO" >&2
        exit 2
        ;;
esac

if [ ! -d "$N3_OUT" ] || [ -L "$N3_OUT" ]; then
    printf 'missing or unsafe corrected N3 output root: %s\n' "$N3_OUT" >&2
    exit 2
fi
if [ ! -d "$SOURCE_REPO/.git" ]; then
    printf 'missing full source repository clone: %s\n' "$SOURCE_REPO" >&2
    printf 'clone https://github.com/termux-pacman/glibc-packages.git there first\n' >&2
    exit 2
fi
if [ -e "$OUT" ] || [ -L "$OUT" ]; then
    printf 'refusing existing OUT: %s\n' "$OUT" >&2
    exit 2
fi
if [ -e "$ARCHIVE" ] || [ -L "$ARCHIVE" ]; then
    printf 'refusing existing ARCHIVE: %s\n' "$ARCHIVE" >&2
    exit 2
fi

mkdir -p "$BASE" "$DOWNLOADS"

export N3_OUT SOURCE_REPO OUT PREFIX
python3 "$SCRIPT_DIR/collect-n3-source-recipe-evidence.py"

special=$(find "$OUT" \( -type l -o \( ! -type f ! -type d \) \) -print -quit)
if [ -n "$special" ]; then
    printf 'unsafe archive member type under OUT: %s\n' "$special" >&2
    exit 1
fi

OUT_PARENT=$(dirname "$OUT")
OUT_NAME=$(basename "$OUT")
tar -C "$OUT_PARENT" -czf "$ARCHIVE" "$OUT_NAME"

if tar -tzf "$ARCHIVE" | grep -E '(^/|(^|/)\.\.(/|$))' >/dev/null; then
    rm -f "$ARCHIVE"
    printf 'archive safety validation failed\n' >&2
    exit 1
fi

ARCHIVE_SHA256=$(sha256sum "$ARCHIVE" | awk '{print $1}')

printf '\nN3_SOURCE_RECIPE_EVIDENCE=PASS\n'
printf 'OUT=%s\n' "$OUT"
printf 'SOURCE_REPO=%s\n' "$SOURCE_REPO"
printf 'ARCHIVE=%s\n' "$ARCHIVE"
printf 'ARCHIVE_SHA256=%s\n' "$ARCHIVE_SHA256"
