#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)

for command in git python3 tar sha256sum find grep awk date dirname basename mkdir rm dpkg-deb readelf; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

tracked_dirty=$(git -C "$REPO" status --porcelain --untracked-files=no)
if [ -n "$tracked_dirty" ]; then
    printf 'tracked working-tree changes detected; artifact evidence requires exact HEAD:\n%s\n' "$tracked_dirty" >&2
    exit 2
fi

BASE=${EVIDENCE_BASE:-$PREFIX/tmp/selected-obsidian-provider-authority}
DOWNLOADS=${DOWNLOADS_DIR:-$HOME/Downloads}
STAMP=${STAMP:-$(date +%Y%m%d-%H%M%S)}
SOURCE_EVIDENCE_OUT=${SOURCE_EVIDENCE_OUT:-$BASE/selected-obsidian-provider-authority-n3-source-recipe-evidence-20260712-185001}
ARTIFACT_DIR=${ARTIFACT_DIR:-$DOWNLOADS/selected-obsidian-provider-authority-n3-exact-artifacts}
OUT=${OUT:-$BASE/selected-obsidian-provider-authority-n3-binary-artifact-comparison-$STAMP}
ARCHIVE=${ARCHIVE:-$DOWNLOADS/selected-obsidian-provider-authority-n3-binary-artifact-comparison-results-$STAMP.tgz}

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
case "$ARTIFACT_DIR" in
    "$DOWNLOADS"/*) ;;
    *)
        printf 'ARTIFACT_DIR must remain under DOWNLOADS_DIR: %s\n' "$ARTIFACT_DIR" >&2
        exit 2
        ;;
esac

if [ ! -d "$SOURCE_EVIDENCE_OUT" ] || [ -L "$SOURCE_EVIDENCE_OUT" ]; then
    printf 'missing or unsafe accepted source evidence root: %s\n' "$SOURCE_EVIDENCE_OUT" >&2
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
if [ -L "$ARTIFACT_DIR" ]; then
    printf 'refusing symlink ARTIFACT_DIR: %s\n' "$ARTIFACT_DIR" >&2
    exit 2
fi

mkdir -p "$BASE" "$DOWNLOADS" "$ARTIFACT_DIR"

export SOURCE_EVIDENCE_OUT ARTIFACT_DIR OUT PREFIX
python3 "$SCRIPT_DIR/collect-n3-binary-artifact-comparison.py"

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

printf '\nN3_BINARY_ARTIFACT_COMPARISON=PASS\n'
printf 'OUT=%s\n' "$OUT"
printf 'SOURCE_EVIDENCE_OUT=%s\n' "$SOURCE_EVIDENCE_OUT"
printf 'ARTIFACT_DIR=%s\n' "$ARTIFACT_DIR"
printf 'ARCHIVE=%s\n' "$ARCHIVE"
printf 'ARCHIVE_SHA256=%s\n' "$ARCHIVE_SHA256"
