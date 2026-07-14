#!/usr/bin/env bash
set -euo pipefail

ROOT=$(mktemp -d)
cleanup() { chmod -R u+w "$ROOT" 2>/dev/null || true; rm -rf "$ROOT"; }
trap cleanup EXIT
REPO="$ROOT/repo"
HOME_TEST="$ROOT/home"
PREFIX_TEST="$ROOT/prefix"
STATE_TEST="$ROOT/state"
mkdir -p "$HOME_TEST" "$PREFIX_TEST"

PROJECT_ROOT=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
# Candidate gates run from linked Git worktrees, where `.git` is a control file
# rather than a directory. Copying it would make fixture commits mutate the
# candidate worktree. A local no-hardlink clone gives the fixture an independent
# object database and index without requiring a network remote.
git clone --no-hardlinks "$PROJECT_ROOT" "$REPO" >/dev/null 2>&1
chmod +x "$REPO/tools/deploy"

fail() { printf 'deploy smoke test: FAIL: %s\n' "$*" >&2; exit 1; }
assert_link() {
  local path=$1 expected=$2
  [ -L "$path" ] || fail "expected symlink: $path"
  [ "$(readlink "$path")" = "$expected" ] || fail "unexpected target: $path -> $(readlink "$path")"
}

# Build exactly the source paths named by both manifests.
cat "$REPO/config/deployment/workstation.tsv" "$REPO/config/deployment/development.tsv" |
  awk -F '\t' 'NF && $1 !~ /^#/ { print $1 "\t" $2 }' |
  while IFS=$'\t' read -r type src; do
    mkdir -p "$REPO/$(dirname "$src")"
    case "$type" in
      file) printf 'source=%s\n' "$src" >"$REPO/$src" ;;
      dir) mkdir -p "$REPO/$src"; printf 'patch\n' >"$REPO/$src/member" ;;
      *) fail "bad fixture type: $type" ;;
    esac
  done

# Executable leaves should preserve executable mode.
chmod +x \
  "$REPO/modules/desktop/overlay/home/.local/bin/startxfce-x11" \
  "$REPO/modules/gl/overlay/home/gl/bin/gl-farm" \
  "$REPO/modules/gl/overlay/home/gl/bin/gl-run" \
  "$REPO/packages/vscode/launcher/code" \
  "$REPO/packages/obsidian/launcher/obsidian" \
  "$REPO/packages/obsidian/launcher/obsidian-app"

git -C "$REPO" add .
git -C "$REPO" -c user.name=test -c user.email=test@example.invalid commit -m fixture >/dev/null

# Legacy source-linked state.
mkdir -p "$HOME_TEST/gl/bin" "$HOME_TEST/.local/bin"
ln -s "$REPO/modules/gl/overlay/home/gl/bin/gl-run" "$HOME_TEST/gl/bin/gl-run"
ln -s "$REPO/packages/vscode/launcher/code" "$HOME_TEST/.local/bin/code"

HOME="$HOME_TEST" PREFIX="$PREFIX_TEST" XDG_STATE_HOME="$STATE_TEST" \
  bash "$REPO/tools/deploy" --dry-run --profile full >"$ROOT/dry-run.log"
[ ! -e "$STATE_TEST/termux-native-desktop/deployment/current" ] || fail 'dry-run mutated state'

HOME="$HOME_TEST" PREFIX="$PREFIX_TEST" XDG_STATE_HOME="$STATE_TEST" \
  bash "$REPO/tools/deploy" --profile full >"$ROOT/deploy-1.log"

DEPLOY_STATE="$STATE_TEST/termux-native-desktop/deployment"
[ -L "$DEPLOY_STATE/current" ] || fail 'current pointer missing'
FIRST_RELEASE=$(readlink "$DEPLOY_STATE/current")
[ -d "$FIRST_RELEASE" ] || fail 'first release missing'
assert_link "$HOME_TEST/gl/bin/gl-run" "$DEPLOY_STATE/current/root/home/gl/bin/gl-run"
assert_link "$HOME_TEST/.local/bin/code" "$DEPLOY_STATE/current/root/home/.local/bin/code"
assert_link "$HOME_TEST/gl/toolchain/glibc-gcc" "$DEPLOY_STATE/current/root/home/gl/toolchain/glibc-gcc"
grep -F 'modules/gl/overlay/home/gl/bin/gl-run' "$HOME_TEST/gl/bin/gl-run" >/dev/null

# Editing and committing the checkout must not alter the active copy until redeploy.
printf 'second release\n' >"$REPO/modules/gl/overlay/home/gl/bin/gl-run"
git -C "$REPO" add modules/gl/overlay/home/gl/bin/gl-run
git -C "$REPO" -c user.name=test -c user.email=test@example.invalid commit -m second >/dev/null
! grep -F 'second release' "$HOME_TEST/gl/bin/gl-run" >/dev/null || fail 'checkout edit leaked into active release'

HOME="$HOME_TEST" PREFIX="$PREFIX_TEST" XDG_STATE_HOME="$STATE_TEST" \
  bash "$REPO/tools/deploy" --profile full >"$ROOT/deploy-2.log"
SECOND_RELEASE=$(readlink "$DEPLOY_STATE/current")
[ "$SECOND_RELEASE" != "$FIRST_RELEASE" ] || fail 'second release did not change'
[ "$(readlink "$DEPLOY_STATE/previous")" = "$FIRST_RELEASE" ] || fail 'previous pointer mismatch'
grep -F 'second release' "$HOME_TEST/gl/bin/gl-run" >/dev/null

HOME="$HOME_TEST" PREFIX="$PREFIX_TEST" XDG_STATE_HOME="$STATE_TEST" \
  bash "$REPO/tools/deploy" --rollback >"$ROOT/rollback.log"
[ "$(readlink "$DEPLOY_STATE/current")" = "$FIRST_RELEASE" ] || fail 'rollback did not restore first release'
! grep -F 'second release' "$HOME_TEST/gl/bin/gl-run" >/dev/null || fail 'rollback content mismatch'

HOME="$HOME_TEST" PREFIX="$PREFIX_TEST" XDG_STATE_HOME="$STATE_TEST" \
  bash "$REPO/tools/deploy" --status --profile full >"$ROOT/status.log"

# Workstation profile retires only managed development links.
HOME="$HOME_TEST" PREFIX="$PREFIX_TEST" XDG_STATE_HOME="$STATE_TEST" \
  bash "$REPO/tools/deploy" --profile workstation >"$ROOT/workstation.log"
[ ! -e "$HOME_TEST/gl/toolchain/glibc-gcc" ] && [ ! -L "$HOME_TEST/gl/toolchain/glibc-gcc" ] || fail 'development link remained'
[ -L "$HOME_TEST/gl/bin/gl-run" ] || fail 'workstation link disappeared'

printf 'deploy smoke test: PASS\n'
