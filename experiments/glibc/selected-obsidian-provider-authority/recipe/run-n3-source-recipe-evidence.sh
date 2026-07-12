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
SOURCE_REPO_INPUT=${SOURCE_REPO:-$DOWNLOADS/termux-pacman-glibc-packages-source}
SOURCE_REPO_EXPECTED_HEAD=${SOURCE_REPO_EXPECTED_HEAD:-fd2ae25e04f3ea26d6c7b4678020814889331d86}
SOURCE_REPO_APPROVED_ORIGIN=${SOURCE_REPO_APPROVED_ORIGIN:-https://github.com/termux-pacman/glibc-packages.git}
OUT=${OUT:-$BASE/selected-obsidian-provider-authority-n3-source-recipe-evidence-$STAMP}
ARCHIVE=${ARCHIVE:-$DOWNLOADS/selected-obsidian-provider-authority-n3-source-recipe-evidence-results-$STAMP.tgz}
TEMP_SOURCE_REPO=$BASE/source-repository-normalized-view-$STAMP

cleanup() {
    if [ -e "$TEMP_SOURCE_REPO" ] || [ -L "$TEMP_SOURCE_REPO" ]; then
        rm -rf "$TEMP_SOURCE_REPO"
    fi
}
trap cleanup EXIT

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
case "$SOURCE_REPO_INPUT" in
    "$REPO"|"$REPO"/*)
        printf 'SOURCE_REPO must remain outside the project checkout: %s\n' "$SOURCE_REPO_INPUT" >&2
        exit 2
        ;;
esac

if [ ! -d "$N3_OUT" ] || [ -L "$N3_OUT" ]; then
    printf 'missing or unsafe corrected N3 output root: %s\n' "$N3_OUT" >&2
    exit 2
fi
if [ ! -d "$SOURCE_REPO_INPUT" ] || [ -L "$SOURCE_REPO_INPUT" ]; then
    printf 'missing or unsafe source repository directory: %s\n' "$SOURCE_REPO_INPUT" >&2
    exit 2
fi
if [ ! -e "$SOURCE_REPO_INPUT/.git" ]; then
    printf 'missing source repository Git marker: %s/.git\n' "$SOURCE_REPO_INPUT" >&2
    exit 2
fi
if [ -e "$TEMP_SOURCE_REPO" ] || [ -L "$TEMP_SOURCE_REPO" ]; then
    printf 'refusing existing temporary source view: %s\n' "$TEMP_SOURCE_REPO" >&2
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

SOURCE_REPO_CANONICAL=$(cd "$SOURCE_REPO_INPUT" && pwd -P)
source_git() {
    git -c safe.directory="$SOURCE_REPO_CANONICAL" -C "$SOURCE_REPO_INPUT" "$@"
}

SOURCE_REPO_INPUT_HEAD=$(source_git rev-parse --verify HEAD) || {
    printf 'unable to resolve SOURCE_REPO HEAD even with scoped safe.directory:\n' >&2
    printf '  logical:  %s\n' "$SOURCE_REPO_INPUT" >&2
    printf '  physical: %s\n' "$SOURCE_REPO_CANONICAL" >&2
    exit 2
}
if [ "$SOURCE_REPO_INPUT_HEAD" != "$SOURCE_REPO_EXPECTED_HEAD" ]; then
    printf 'source repository HEAD mismatch:\n' >&2
    printf '  observed: %s\n' "$SOURCE_REPO_INPUT_HEAD" >&2
    printf '  expected: %s\n' "$SOURCE_REPO_EXPECTED_HEAD" >&2
    exit 2
fi
if [ "$(source_git rev-parse --is-bare-repository)" != false ]; then
    printf 'SOURCE_REPO must be a non-bare checkout\n' >&2
    exit 2
fi
if [ "$(source_git rev-parse --is-shallow-repository)" != false ]; then
    printf 'SOURCE_REPO must be a full non-shallow checkout\n' >&2
    exit 2
fi
SOURCE_REPO_INPUT_DIRTY=$(source_git status --porcelain --untracked-files=all)
if [ -n "$SOURCE_REPO_INPUT_DIRTY" ]; then
    printf 'SOURCE_REPO input must be clean, including untracked files:\n%s\n' "$SOURCE_REPO_INPUT_DIRTY" >&2
    exit 2
fi
source_git fsck --connectivity-only --no-dangling >/dev/null
SOURCE_REPO_INPUT_REFS_BEFORE=$(source_git for-each-ref --format='%(refname)%00%(objectname)%00%(objecttype)%00' | sha256sum | awk '{print $1}')
SOURCE_REPO_PERSISTENT_ORIGIN=$(source_git remote get-url origin 2>/dev/null || true)
case "$SOURCE_REPO_PERSISTENT_ORIGIN" in
    "$SOURCE_REPO_APPROVED_ORIGIN"|git@github.com:termux-pacman/glibc-packages.git|ssh://git@github.com/termux-pacman/glibc-packages.git|"") ;;
    *)
        printf 'unexpected persistent SOURCE_REPO origin: %s\n' "$SOURCE_REPO_PERSISTENT_ORIGIN" >&2
        exit 2
        ;;
esac

mkdir -p "$BASE" "$DOWNLOADS"

# Android shared storage can legitimately trip Git's dubious-ownership guard.
# Trust is scoped to these commands only; no global/local config is changed.
git -c safe.directory="$SOURCE_REPO_CANONICAL" \
    clone --no-hardlinks "$SOURCE_REPO_CANONICAL" "$TEMP_SOURCE_REPO" >/dev/null

git -C "$TEMP_SOURCE_REPO" remote set-url origin "$SOURCE_REPO_APPROVED_ORIGIN"
if [ "$(git -C "$TEMP_SOURCE_REPO" rev-parse --verify HEAD)" != "$SOURCE_REPO_EXPECTED_HEAD" ]; then
    printf 'temporary source view lost the pinned HEAD\n' >&2
    exit 2
fi
if [ "$(git -C "$TEMP_SOURCE_REPO" rev-parse --is-shallow-repository)" != false ]; then
    printf 'temporary source view unexpectedly became shallow\n' >&2
    exit 2
fi
if [ -n "$(git -C "$TEMP_SOURCE_REPO" status --porcelain --untracked-files=all)" ]; then
    printf 'temporary source view is not clean\n' >&2
    exit 2
fi
git -C "$TEMP_SOURCE_REPO" fsck --connectivity-only --no-dangling >/dev/null

SOURCE_REPO=$TEMP_SOURCE_REPO
export N3_OUT SOURCE_REPO OUT PREFIX
python3 "$SCRIPT_DIR/collect-n3-source-recipe-evidence.py"

SOURCE_REPO_INPUT_HEAD_AFTER=$(source_git rev-parse --verify HEAD)
SOURCE_REPO_INPUT_REFS_AFTER=$(source_git for-each-ref --format='%(refname)%00%(objectname)%00%(objecttype)%00' | sha256sum | awk '{print $1}')
SOURCE_REPO_INPUT_DIRTY_AFTER=$(source_git status --porcelain --untracked-files=all)
if [ "$SOURCE_REPO_INPUT_HEAD_AFTER" != "$SOURCE_REPO_INPUT_HEAD" ] || \
   [ "$SOURCE_REPO_INPUT_REFS_AFTER" != "$SOURCE_REPO_INPUT_REFS_BEFORE" ] || \
   [ -n "$SOURCE_REPO_INPUT_DIRTY_AFTER" ]; then
    printf 'SOURCE_REPO input changed during collection\n' >&2
    exit 1
fi

printf 'field\tvalue\n' > "$OUT/source-repository-origin-guard.tsv"
printf 'input_logical_path\t%s\n' "$SOURCE_REPO_INPUT" >> "$OUT/source-repository-origin-guard.tsv"
printf 'input_physical_path\t%s\n' "$SOURCE_REPO_CANONICAL" >> "$OUT/source-repository-origin-guard.tsv"
printf 'effective_path\t%s\n' "$TEMP_SOURCE_REPO" >> "$OUT/source-repository-origin-guard.tsv"
printf 'expected_head\t%s\n' "$SOURCE_REPO_EXPECTED_HEAD" >> "$OUT/source-repository-origin-guard.tsv"
printf 'observed_head\t%s\n' "$SOURCE_REPO_INPUT_HEAD" >> "$OUT/source-repository-origin-guard.tsv"
printf 'origin_mode\tISOLATED_SHARED_STORAGE_SAFE_DIRECTORY_CLONE\n' >> "$OUT/source-repository-origin-guard.tsv"
printf 'persistent_origin_before\t%s\n' "${SOURCE_REPO_PERSISTENT_ORIGIN:--}" >> "$OUT/source-repository-origin-guard.tsv"
printf 'effective_origin\t%s\n' "$SOURCE_REPO_APPROVED_ORIGIN" >> "$OUT/source-repository-origin-guard.tsv"
printf 'input_refs_sha256_before\t%s\n' "$SOURCE_REPO_INPUT_REFS_BEFORE" >> "$OUT/source-repository-origin-guard.tsv"
printf 'input_refs_sha256_after\t%s\n' "$SOURCE_REPO_INPUT_REFS_AFTER" >> "$OUT/source-repository-origin-guard.tsv"
printf 'safe_directory_scope\tCOMMAND_ONLY\n' >> "$OUT/source-repository-origin-guard.tsv"
printf 'input_git_config_mutation\tNO\n' >> "$OUT/source-repository-origin-guard.tsv"
printf 'input_metadata_mutation\tNO\n' >> "$OUT/source-repository-origin-guard.tsv"
printf 'network_fetch_performed\tNO\n' >> "$OUT/source-repository-origin-guard.tsv"

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
printf 'SOURCE_REPO_INPUT=%s\n' "$SOURCE_REPO_INPUT"
printf 'SOURCE_REPO_INPUT_PHYSICAL=%s\n' "$SOURCE_REPO_CANONICAL"
printf 'SOURCE_REPO_EXPECTED_HEAD=%s\n' "$SOURCE_REPO_EXPECTED_HEAD"
printf 'SOURCE_REPO_ORIGIN_MODE=ISOLATED_SHARED_STORAGE_SAFE_DIRECTORY_CLONE\n'
printf 'ARCHIVE=%s\n' "$ARCHIVE"
printf 'ARCHIVE_SHA256=%s\n' "$ARCHIVE_SHA256"
