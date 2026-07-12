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
    printf 'tracked working-tree changes detected; N2 requires exact HEAD:\n%s\n' "$tracked_dirty" >&2
    exit 2
fi

BASE=${EVIDENCE_BASE:-$PREFIX/tmp/selected-obsidian-provider-authority}
DOWNLOADS=${DOWNLOADS_DIR:-$HOME/Downloads}
STAMP=${STAMP:-$(date +%Y%m%d-%H%M%S)}
OUT=${OUT:-$BASE/selected-obsidian-provider-authority-n2-read-only-evidence-$STAMP}
ARCHIVE=${ARCHIVE:-$DOWNLOADS/selected-obsidian-provider-authority-n2-read-only-evidence-results-$STAMP.tgz}

B1_OUT=${B1_OUT:-$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b1-retained-control-locality-20260711-192919}
B2_OUT=${B2_OUT:-$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b2-static-runtime-closure-20260711-195310}
B9_OUT=${B9_OUT:-$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b9-generation-publication-corrected-20260712-003136}
MAP_OUT=${MAP_OUT:-$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-passive-map-selection-diagnostic-20260712-022611}
PIXBUF_OUT=${PIXBUF_OUT:-$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-gtk-pixbuf-runtime-capability-inventory-20260712-014314}

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

if [ -e "$OUT" ] || [ -L "$OUT" ]; then
    printf 'refusing existing OUT: %s\n' "$OUT" >&2
    exit 2
fi
if [ -e "$ARCHIVE" ] || [ -L "$ARCHIVE" ]; then
    printf 'refusing existing ARCHIVE: %s\n' "$ARCHIVE" >&2
    exit 2
fi

mkdir -p "$BASE" "$DOWNLOADS"

export B1_OUT B2_OUT B9_OUT MAP_OUT PIXBUF_OUT OUT
python3 "$SCRIPT_DIR/collect-read-only-provider-evidence.py"

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

printf '\nN2_PROVIDER_AUTHORITY_EVIDENCE=PASS\n'
printf 'OUT=%s\n' "$OUT"
printf 'ARCHIVE=%s\n' "$ARCHIVE"
printf 'ARCHIVE_SHA256=%s\n' "$ARCHIVE_SHA256"
