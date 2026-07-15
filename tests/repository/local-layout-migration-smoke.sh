#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TMPDIR:-${PREFIX:+$PREFIX/tmp}}
TMP_BASE=${TMP_BASE:-$ROOT/.tmp}
mkdir -p "$TMP_BASE"
T=$(mktemp -d "$TMP_BASE/tnd-local-layout-smoke.XXXXXX")
cleanup() { chmod -R u+w "$T" 2>/dev/null || true; rm -rf "$T"; }
trap cleanup EXIT HUP INT TERM

HOME=$T/home
PREFIX=$T/prefix
XDG_STATE_HOME=$HOME/.local/state
SAFETY=$T/safety
mkdir -p "$HOME/gl/build/.venv/bin" "$HOME/gl/build/mesa/src" "$HOME/gl/opt" "$HOME/gl/apps/vscode" "$HOME/gl/selected/obsidian" "$HOME/opt" "$PREFIX/tmp"
printf 'venv\n' >"$HOME/gl/build/.venv/bin/marker"
printf 'source\n' >"$HOME/gl/build/mesa/src/marker"
printf 'cross\n' >"$HOME/gl/build/cross-full.ini"
for name in mesa-glibc-26.1.4 mesa-glibc-26.1.4-full mesa-bisect mesa-glibc-debug; do
  mkdir -p "$HOME/gl/opt/$name/lib"
  printf '%s\n' "$name" >"$HOME/gl/opt/$name/lib/marker"
done
ln -s "$HOME/gl/opt/mesa-glibc-26.1.4-full" "$HOME/gl/opt/mesa-glibc"
ln -s "$HOME/ark/build/opt/mesa-26-glibc" "$HOME/opt/mesa-26-glibc"
printf 'app\n' >"$HOME/gl/apps/vscode/marker"
printf 'selected\n' >"$HOME/gl/selected/obsidian/marker"

(
  cd "$HOME/gl"
  git init -q
  git config user.name test
  git config user.email test@example.invalid
  cat >.gitignore <<'GI'
apps/
opt/
build/mesa/
build/.venv/
GI
  printf 'legacy\n' >env
  git add .gitignore env
  git commit -qm initial
  git tag v0.2-gpu
)
EXPECTED=$(git -C "$HOME/gl" rev-parse HEAD)
ln -s "$ROOT/modules/gl/overlay/home/gl/env" "$HOME/gl/env.new"
mv -Tf "$HOME/gl/env.new" "$HOME/gl/env"

HOME=$HOME PREFIX=$PREFIX XDG_STATE_HOME=$XDG_STATE_HOME \
TND_LOCAL_LAYOUT_SAFETY_ROOT=$SAFETY TND_EXPECTED_GL_HEAD=$EXPECTED \
TND_SKIP_ACTIVE_MAPPING_CHECK=1 TND_MIGRATION_TIMESTAMP=smoke \
  bash "$ROOT/tools/migrate-local-layout" --apply >"$T/apply.out"

HOME=$HOME PREFIX=$PREFIX XDG_STATE_HOME=$XDG_STATE_HOME \
  bash "$ROOT/tools/migrate-local-layout" --status >"$T/status.out"

test ! -e "$HOME/gl/.git"
test ! -e "$HOME/gl/.gitignore"
test -L "$HOME/gl/build/.venv"
test -L "$HOME/gl/build/mesa"
test -L "$HOME/gl/build/cross-full.ini"
test -f "$XDG_STATE_HOME/termux-native-desktop/workspaces/mesa/.venv/bin/marker"
test -f "$XDG_STATE_HOME/termux-native-desktop/workspaces/mesa/mesa/src/marker"
test -L "$HOME/gl/opt/mesa-glibc-26.1.4-full"
test -L "$HOME/gl/opt/mesa-glibc-debug"
test -f "$XDG_STATE_HOME/termux-native-desktop/providers/mesa/candidates/mesa-glibc-26.1.4-full/lib/marker"
test "$(readlink "$HOME/gl/opt/mesa-glibc")" = "$XDG_STATE_HOME/termux-native-desktop/providers/mesa/current"
test "$(readlink -f "$HOME/gl/opt/mesa-glibc")" = "$(readlink -f "$XDG_STATE_HOME/termux-native-desktop/providers/mesa/current")"
test ! -e "$HOME/gl/opt/mesa-glibc.new.$$"
test ! -L "$HOME/opt/mesa-26-glibc"
test -f "$HOME/gl/apps/vscode/marker"
test -f "$HOME/gl/selected/obsidian/marker"
test -s "$SAFETY/termux-native-desktop-local-layout-smoke-gl-legacy-all-refs.bundle"
test -s "$SAFETY/termux-native-desktop-local-layout-smoke-gl-legacy-git.tar.zst"

echo 'local layout migration smoke: PASS'
