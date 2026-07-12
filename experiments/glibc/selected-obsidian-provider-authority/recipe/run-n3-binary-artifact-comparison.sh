#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
WORK_ROOT=${PROVIDER_AUTHORITY_WORK_ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)/work}

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
STAMP=${STAMP:-$(date +%Y%m%d-%H%M%S)}
SOURCE_EVIDENCE_OUT=${SOURCE_EVIDENCE_OUT:-$BASE/selected-obsidian-provider-authority-n3-source-recipe-evidence-20260712-185001}
ARTIFACT_DIR=${ARTIFACT_DIR:-$WORK_ROOT/artifacts/n3-exact-debs}
OUT=${OUT:-$WORK_ROOT/receipts/unpacked/selected-obsidian-provider-authority-n3-binary-artifact-comparison-$STAMP}
ARCHIVE=${ARCHIVE:-$WORK_ROOT/receipts/selected-obsidian-provider-authority-n3-binary-artifact-comparison-results-$STAMP.tgz}
SSL_CERT_FILE=${SSL_CERT_FILE:-$PREFIX/etc/tls/cert.pem}

case "$WORK_ROOT" in
    "$REPO"/experiments/*/work) ;;
    *)
        printf 'WORK_ROOT must use the repository experiment work convention: %s\n' "$WORK_ROOT" >&2
        exit 2
        ;;
esac
case "$ARTIFACT_DIR" in
    "$WORK_ROOT"/*) ;;
    *)
        printf 'ARTIFACT_DIR must remain under WORK_ROOT: %s\n' "$ARTIFACT_DIR" >&2
        exit 2
        ;;
esac
case "$OUT" in
    "$WORK_ROOT"/*) ;;
    *)
        printf 'OUT must remain under WORK_ROOT: %s\n' "$OUT" >&2
        exit 2
        ;;
esac
case "$ARCHIVE" in
    "$WORK_ROOT"/*) ;;
    *)
        printf 'ARCHIVE must remain under WORK_ROOT: %s\n' "$ARCHIVE" >&2
        exit 2
        ;;
esac

if [ ! -f "$SSL_CERT_FILE" ]; then
    printf 'missing Termux CA bundle: %s\n' "$SSL_CERT_FILE" >&2
    exit 2
fi
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

mkdir -p "$ARTIFACT_DIR" "$(dirname "$OUT")" "$(dirname "$ARCHIVE")"

export SOURCE_EVIDENCE_OUT ARTIFACT_DIR OUT PREFIX SSL_CERT_FILE
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
printf 'WORK_ROOT=%s\n' "$WORK_ROOT"
printf 'OUT=%s\n' "$OUT"
printf 'SOURCE_EVIDENCE_OUT=%s\n' "$SOURCE_EVIDENCE_OUT"
printf 'ARTIFACT_DIR=%s\n' "$ARTIFACT_DIR"
printf 'SSL_CERT_FILE=%s\n' "$SSL_CERT_FILE"
printf 'ARCHIVE=%s\n' "$ARCHIVE"
printf 'ARCHIVE_SHA256=%s\n' "$ARCHIVE_SHA256"
