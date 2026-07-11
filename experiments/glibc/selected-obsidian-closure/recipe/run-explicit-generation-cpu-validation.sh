#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

B9_OUT=${B9_OUT:?set B9_OUT to the completed Phase B9 receipt}
OUT=${OUT:-$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b10-explicit-generation-cpu-validation}
REPO=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
APP=${APP:-$HOME/gl/apps/obsidian}
APP_ENTRYPOINT=${APP_ENTRYPOINT:-$APP/obsidian}
ROOTFS=${ROOTFS:-$PREFIX/var/lib/proot-distro/containers/debian/rootfs}
VALIDATION_ROOT=${VALIDATION_ROOT:-}

CAPTURE_OUT="$OUT/capture"
LAUNCH_RECEIPT_DIR="$OUT/launch-contract"
RUNTIME_EVIDENCE_DIR="$OUT/runtime-evidence"
RUNTIME_ROOT_OWNED=NO
stage=initialization

snapshot_runtime_evidence() {
    [ -n "${VALIDATION_ROOT:-}" ] || return 0
    [ -d "$VALIDATION_ROOT" ] || return 0

    rm -rf "$RUNTIME_EVIDENCE_DIR"
    cp -a "$VALIDATION_ROOT" "$RUNTIME_EVIDENCE_DIR"
    diff -qr "$VALIDATION_ROOT" "$RUNTIME_EVIDENCE_DIR" >/dev/null

    {
        printf 'field\tvalue\n'
        printf 'live_runtime_root\t%s\n' "$VALIDATION_ROOT"
        printf 'archived_runtime_copy\t%s\n' "$RUNTIME_EVIDENCE_DIR"
        printf 'snapshot_state\tMATCH\n'
    } >"$OUT/runtime-snapshot.tsv"
}

cleanup_runtime_root() {
    [ "${RUNTIME_ROOT_OWNED:-NO}" = YES ] || return 0
    case "${VALIDATION_ROOT:-}" in
        "$PREFIX"/tmp/o10.*)
            rm -rf "$VALIDATION_ROOT"
            ;;
        *)
            printf 'refusing to remove unexpected runtime root: %s\n' \
                "${VALIDATION_ROOT:-UNSET}" >&2
            return 1
            ;;
    esac
}

fail() {
    local message=$1
    mkdir -p "$OUT"
    printf 'FAIL\n' >"$OUT/analysis.status"
    printf '%s\n' "$stage" >"$OUT/failure-stage.txt"
    snapshot_runtime_evidence >/dev/null 2>&1 || true
    cleanup_runtime_root >/dev/null 2>&1 || true
    printf '%s\n' "$message" >&2
    printf 'evidence: %s\n' "$OUT" >&2
    exit 1
}

summary_value() {
    local key=$1
    awk -F $'\t' -v key="$key" '
        NR > 1 && $1 == key { print $2; found=1; exit }
        END { if (!found) exit 1 }
    ' "$B9_OUT/summary.tsv"
}

write_current_state() {
    local output=$1
    local current=$2
    printf 'state\tpath\tlink_target\tresolved_target\tinode\n' >"$output"
    if [ ! -e "$current" ] && [ ! -L "$current" ]; then
        printf 'ABSENT\t%s\t-\t-\t-\n' "$current" >>"$output"
        return
    fi
    if [ -L "$current" ]; then
        local target resolved inode
        target=$(readlink "$current")
        resolved=$(realpath -m "$current")
        inode=$(stat -c '%i' "$current")
        printf 'SYMLINK\t%s\t%s\t%s\t%s\n' \
            "$current" "$target" "$resolved" "$inode" >>"$output"
        return
    fi
    local inode
    inode=$(stat -c '%i' "$current")
    printf 'NON_SYMLINK\t%s\t-\t%s\t%s\n' \
        "$current" "$(realpath -m "$current")" "$inode" >>"$output"
}

mkdir -p "$OUT"

stage=repository_state
tracked=$(git -C "$REPO" status --porcelain --untracked-files=no)
[ -z "$tracked" ] || fail "tracked working-tree changes detected"

git -C "$REPO" branch --show-current >"$OUT/branch.txt"
git -C "$REPO" rev-parse HEAD >"$OUT/head.txt"
printf '%s\n' "$REPO" >"$OUT/repository-root.txt"
printf '%s\n' "$B9_OUT" >"$OUT/phase-b9-root.txt"

stage=phase_b9_status
[ -f "$B9_OUT/analysis.status" ] || fail "missing Phase B9 analysis.status"
[ "$(cat "$B9_OUT/analysis.status")" = PASS ] || fail "Phase B9 status is not PASS"
[ -f "$B9_OUT/next-state.txt" ] || fail "missing Phase B9 next-state"
[ "$(cat "$B9_OUT/next-state.txt")" = READY_FOR_EXPLICIT_GENERATION_VALIDATION ] \
    || fail "Phase B9 is not ready for explicit validation"
[ -f "$B9_OUT/summary.tsv" ] || fail "missing Phase B9 summary"

GENERATION_DIR=$(summary_value generation_dir)
GENERATION_ID=$(summary_value generation_id)
GENERATION_BASE=${GENERATION_DIR%/generations/*}
CURRENT="$GENERATION_BASE/current"

printf '%s\n' "$GENERATION_DIR" >"$OUT/generation-dir.txt"
printf '%s\n' "$GENERATION_ID" >"$OUT/generation-id.txt"

stage=generation_preflight
[ -d "$GENERATION_DIR" ] && [ ! -L "$GENERATION_DIR" ] \
    || fail "published generation is not a plain directory"
[ -d "$GENERATION_DIR/lib" ] || fail "missing generation lib directory"
[ -d "$GENERATION_DIR/share/fonts/selected" ] || fail "missing generation font directory"
[ -f "$GENERATION_DIR/share/glib-2.0/schemas/gschemas.compiled" ] \
    || fail "missing generation schema aggregate"
case "$(stat -c '%A' "$GENERATION_DIR")" in
    ??-*) ;;
    *) fail "generation root is owner-writable" ;;
esac

write_current_state "$OUT/current-state-before.tsv" "$CURRENT"
before_state=$(awk -F $'\t' 'NR == 2 { print $1 }' "$OUT/current-state-before.tsv")
[ "$before_state" = ABSENT ] || fail "initial explicit validation requires current to be absent"

stage=runtime_root
if [ -z "$VALIDATION_ROOT" ]; then
    VALIDATION_ROOT=$(mktemp -d "$PREFIX/tmp/o10.XXXXXXXX") \
        || fail "failed to allocate short receipt-owned runtime root"
    RUNTIME_ROOT_OWNED=YES
else
    [ -d "$VALIDATION_ROOT" ] && [ ! -L "$VALIDATION_ROOT" ] \
        || fail "provided VALIDATION_ROOT is not a plain directory"
fi

FONTCONFIG_ROOT="$VALIDATION_ROOT/f"
FONTCONFIG_FILE="$FONTCONFIG_ROOT/fonts.conf"
XDG_CONFIG_HOME="$VALIDATION_ROOT/c"
XDG_CACHE_HOME="$VALIDATION_ROOT/k"
XDG_DATA_HOME="$VALIDATION_ROOT/d"
XDG_STATE_HOME="$VALIDATION_ROOT/s"
XDG_RUNTIME_DIR="$VALIDATION_ROOT/x"
TMPDIR="$VALIDATION_ROOT/t"
LAUNCHER_SOURCE="$REPO/experiments/glibc/selected-obsidian-closure/recipe/launch-obsidian-explicit-generation-cpu.sh"
LAUNCHER_RUNTIME="$VALIDATION_ROOT/b/launch.sh"

validation_root_length=${#VALIDATION_ROOT}
tmpdir_length=${#TMPDIR}
config_home_length=${#XDG_CONFIG_HOME}

{
    printf 'field\tvalue\n'
    printf 'validation_root\t%s\n' "$VALIDATION_ROOT"
    printf 'validation_root_length\t%s\n' "$validation_root_length"
    printf 'tmpdir\t%s\n' "$TMPDIR"
    printf 'tmpdir_length\t%s\n' "$tmpdir_length"
    printf 'xdg_config_home\t%s\n' "$XDG_CONFIG_HOME"
    printf 'xdg_config_home_length\t%s\n' "$config_home_length"
    printf 'runtime_root_ownership\t%s\n' "$RUNTIME_ROOT_OWNED"
    printf 'unix_socket_path_headroom_contract\tTMPDIR_LE_64\n'
} >"$OUT/runtime-root-contract.tsv"

[ "$tmpdir_length" -le 64 ] \
    || fail "receipt-owned TMPDIR is too long for the socket-path headroom contract"

stage=runtime_setup
mkdir -p \
    "$CAPTURE_OUT" \
    "$LAUNCH_RECEIPT_DIR" \
    "$FONTCONFIG_ROOT/cache" \
    "$XDG_CONFIG_HOME" \
    "$XDG_CACHE_HOME" \
    "$XDG_DATA_HOME" \
    "$XDG_STATE_HOME" \
    "$XDG_RUNTIME_DIR" \
    "$TMPDIR" \
    "$(dirname "$LAUNCHER_RUNTIME")"

cp "$LAUNCHER_SOURCE" "$LAUNCHER_RUNTIME"
chmod 500 "$LAUNCHER_RUNTIME"
{
    printf 'field\tvalue\n'
    printf 'source\t%s\n' "$LAUNCHER_SOURCE"
    printf 'runtime_copy\t%s\n' "$LAUNCHER_RUNTIME"
    printf 'source_sha256\t%s\n' "$(sha256sum "$LAUNCHER_SOURCE" | awk '{ print $1 }')"
    printf 'runtime_sha256\t%s\n' "$(sha256sum "$LAUNCHER_RUNTIME" | awk '{ print $1 }')"
} >"$OUT/launch-script-identity.tsv"

cmp -s "$LAUNCHER_SOURCE" "$LAUNCHER_RUNTIME" \
    || fail "receipt-local launcher copy differs from repository source"

chmod 700 \
    "$VALIDATION_ROOT" \
    "$XDG_CONFIG_HOME" \
    "$XDG_CACHE_HOME" \
    "$XDG_DATA_HOME" \
    "$XDG_STATE_HOME" \
    "$XDG_RUNTIME_DIR" \
    "$TMPDIR"

cat >"$FONTCONFIG_FILE" <<EOF
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <dir>$GENERATION_DIR/share/fonts/selected</dir>
  <cachedir>$FONTCONFIG_ROOT/cache</cachedir>
  <config>
    <rescan>
      <int>0</int>
    </rescan>
  </config>
</fontconfig>
EOF

printf 'field\tvalue\n' >"$OUT/runtime-contract.tsv"
printf 'generation_dir\t%s\n' "$GENERATION_DIR" >>"$OUT/runtime-contract.tsv"
printf 'validation_root\t%s\n' "$VALIDATION_ROOT" >>"$OUT/runtime-contract.tsv"
printf 'fontconfig_file\t%s\n' "$FONTCONFIG_FILE" >>"$OUT/runtime-contract.tsv"
printf 'xdg_config_home\t%s\n' "$XDG_CONFIG_HOME" >>"$OUT/runtime-contract.tsv"
printf 'xdg_cache_home\t%s\n' "$XDG_CACHE_HOME" >>"$OUT/runtime-contract.tsv"
printf 'xdg_data_home\t%s\n' "$XDG_DATA_HOME" >>"$OUT/runtime-contract.tsv"
printf 'xdg_state_home\t%s\n' "$XDG_STATE_HOME" >>"$OUT/runtime-contract.tsv"
printf 'xdg_runtime_dir\t%s\n' "$XDG_RUNTIME_DIR" >>"$OUT/runtime-contract.tsv"
printf 'tmpdir\t%s\n' "$TMPDIR" >>"$OUT/runtime-contract.tsv"

stage=capture
if \
    GENERATION_DIR="$GENERATION_DIR" \
    VALIDATION_ROOT="$VALIDATION_ROOT" \
    LAUNCH_RECEIPT_DIR="$LAUNCH_RECEIPT_DIR" \
    FONTCONFIG_FILE="$FONTCONFIG_FILE" \
    XDG_CONFIG_HOME="$XDG_CONFIG_HOME" \
    XDG_CACHE_HOME="$XDG_CACHE_HOME" \
    XDG_DATA_HOME="$XDG_DATA_HOME" \
    XDG_STATE_HOME="$XDG_STATE_HOME" \
    XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR" \
    TMPDIR="$TMPDIR" \
    APP="$APP" \
    APP_ENTRYPOINT="$APP_ENTRYPOINT" \
    ROOTFS="$ROOTFS" \
    OUT="$CAPTURE_OUT" \
    CONTROL_NAME="Obsidian explicit generation CPU" \
    LAUNCHER="$LAUNCHER_RUNTIME" \
    CONTROL_GL_GPU=0 \
    STARTUP_TIMEOUT_SECONDS=45 \
    TOPOLOGY_SETTLE_SECONDS=5 \
    SURVIVAL_SECONDS=100 \
    POLL_SLEEP_SECONDS=0.5 \
    PROGRESS_INTERVAL_SECONDS=10 \
    bash \
      "$REPO/experiments/glibc/selected-obsidian-closure/recipe/capture-control.sh"
then
    capture_rc=0
else
    capture_rc=$?
    stage=current_guard_after_capture_failure
    write_current_state "$OUT/current-state-after.tsv" "$CURRENT"
    cmp -s "$OUT/current-state-before.tsv" "$OUT/current-state-after.tsv" \
        || fail "current changed during failed explicit-generation capture"
    printf '%s\n' "$capture_rc" >"$OUT/capture-exit-status.txt"
    stage=runtime_evidence_snapshot
    snapshot_runtime_evidence || fail "failed to snapshot short runtime root"
    cleanup_runtime_root || fail "failed to remove short runtime root after snapshot"
    stage=capture
    fail "explicit-generation capture failed"
fi
printf '%s\n' "$capture_rc" >"$OUT/capture-exit-status.txt"

stage=current_guard
write_current_state "$OUT/current-state-after.tsv" "$CURRENT"
cmp -s "$OUT/current-state-before.tsv" "$OUT/current-state-after.tsv" \
    || fail "current changed during explicit-generation capture"

stage=runtime_evidence_snapshot
snapshot_runtime_evidence || fail "failed to snapshot short runtime root"

stage=analysis
if \
    B9_OUT="$B9_OUT" \
    CAPTURE_OUT="$CAPTURE_OUT" \
    OUT="$OUT" \
    VALIDATION_ROOT="$VALIDATION_ROOT" \
    LAUNCH_RECEIPT_DIR="$LAUNCH_RECEIPT_DIR" \
    APP="$APP" \
    ROOTFS="$ROOTFS" \
    python \
      "$REPO/experiments/glibc/selected-obsidian-closure/recipe/analyze-explicit-generation-cpu.py"
then
    analysis_rc=0
else
    analysis_rc=$?
    cleanup_runtime_root >/dev/null 2>&1 || true
    [ -f "$OUT/analysis.status" ] || printf 'FAIL\n' >"$OUT/analysis.status"
    [ -f "$OUT/failure-stage.txt" ] || printf '%s\n' "$stage" >"$OUT/failure-stage.txt"
    exit "$analysis_rc"
fi

stage=runtime_root_cleanup
cleanup_runtime_root || fail "failed to remove short runtime root after successful analysis"
printf 'PASS\n' >"$OUT/runtime-cleanup.status"

printf '\nselected Obsidian Phase B10 explicit generation validation: PASS\n'
printf 'evidence: %s\n' "$OUT"
