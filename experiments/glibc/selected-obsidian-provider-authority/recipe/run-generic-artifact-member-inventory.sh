#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
WORK_ROOT=${PROVIDER_AUTHORITY_WORK_ROOT:-$REPO/experiments/glibc/selected-obsidian-provider-authority/work}
HANDOFF_DIR=${HANDOFF_DIR:-$HOME/Downloads}
STAMP=${STAMP:-$(date -u +%Y%m%dT%H%M%SZ)}
PREFIX=${PREFIX:?PREFIX is required}
SSL_CERT_FILE=${SSL_CERT_FILE:-$PREFIX/etc/tls/cert.pem}
ARTIFACT_DIR=${ARTIFACT_DIR:-$WORK_ROOT/artifacts/generic-artifact-member-inventory}
OUT=${OUT:-$WORK_ROOT/receipts/unpacked/selected-obsidian-generic-artifact-member-inventory-$STAMP}
CREATE_ARCHIVE=${CREATE_ARCHIVE:-1}
ARCHIVE=${ARCHIVE:-$HANDOFF_DIR/selected-obsidian-generic-artifact-member-inventory-$STAMP.tar.zst}
BASE=$REPO/experiments/glibc/selected-obsidian-provider-authority
COMPARISON_ARTIFACTS=${COMPARISON_ARTIFACTS:-$BASE/review/generic-artifact-member-comparison-artifacts.tsv}
COMPARISON_EDGES=${COMPARISON_EDGES:-$BASE/review/generic-artifact-member-comparison-edges.tsv}
COMPARISON_METADATA=${COMPARISON_METADATA:-$BASE/review/generic-artifact-member-comparison-metadata.tsv}
REPOSITORY_METADATA=${REPOSITORY_METADATA:-$BASE/profiles/supply-repository-metadata-registry.tsv}

for command in git python3 find tar zstd sha256sum awk date dirname basename mkdir rm dpkg-deb; do
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
case "$CREATE_ARCHIVE" in
    0|1) ;;
    *) printf 'CREATE_ARCHIVE must be 0 or 1\n' >&2; exit 2 ;;
esac
case "$WORK_ROOT" in
    "$REPO"/experiments/*/work) ;;
    *) printf 'WORK_ROOT must use the repository experiment work convention: %s\n' "$WORK_ROOT" >&2; exit 2 ;;
esac
case "$ARTIFACT_DIR" in
    "$WORK_ROOT"/*) ;;
    *) printf 'ARTIFACT_DIR must remain under WORK_ROOT: %s\n' "$ARTIFACT_DIR" >&2; exit 2 ;;
esac
case "$OUT" in
    "$WORK_ROOT"/*|"$HANDOFF_DIR"/*) ;;
    *) printf 'OUT must remain under WORK_ROOT or HANDOFF_DIR: %s\n' "$OUT" >&2; exit 2 ;;
esac
if [ -L "$ARTIFACT_DIR" ]; then
    printf 'refusing symlink ARTIFACT_DIR: %s\n' "$ARTIFACT_DIR" >&2
    exit 2
fi
if [ -e "$OUT" ] || [ -L "$OUT" ]; then
    printf 'refusing existing output: %s\n' "$OUT" >&2
    exit 2
fi
if [ ! -f "$SSL_CERT_FILE" ]; then
    printf 'missing Termux CA bundle: %s\n' "$SSL_CERT_FILE" >&2
    exit 2
fi
for input in "$COMPARISON_ARTIFACTS" "$COMPARISON_EDGES" "$COMPARISON_METADATA" "$REPOSITORY_METADATA"; do
    [ -f "$input" ] && [ ! -L "$input" ] || {
        printf 'missing or unsafe canonical input: %s\n' "$input" >&2
        exit 2
    }
done
if [ "$CREATE_ARCHIVE" = 1 ] && { [ -e "$ARCHIVE" ] || [ -L "$ARCHIVE" ] || [ -e "$ARCHIVE.sha256" ]; }; then
    printf 'refusing existing archive path: %s\n' "$ARCHIVE" >&2
    exit 2
fi

mkdir -p "$ARTIFACT_DIR" "$(dirname "$OUT")" "$HANDOFF_DIR"
export PROJECT_REPO="$REPO" PREFIX SSL_CERT_FILE ARTIFACT_DIR OUT \
    COMPARISON_ARTIFACTS COMPARISON_EDGES COMPARISON_METADATA REPOSITORY_METADATA
python3 "$SCRIPT_DIR/collect-generic-artifact-member-inventory.py"

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

printf '\nGENERIC_ARTIFACT_MEMBER_INVENTORY=PASS\n'
printf 'OUT=%s\n' "$OUT"
printf 'ARTIFACT_DIR=%s\n' "$ARTIFACT_DIR"
printf 'CREATE_ARCHIVE=%s\n' "$CREATE_ARCHIVE"
printf 'ARCHIVE=%s\n' "${ARCHIVE:--}"
printf 'ARCHIVE_SHA256=%s\n' "$ARCHIVE_SHA256"
