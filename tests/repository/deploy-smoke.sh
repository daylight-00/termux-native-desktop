#!/usr/bin/env bash
set -euo pipefail

ROOT=$(mktemp -d)
trap 'rm -rf "$ROOT"' EXIT
REPO="$ROOT/repo"
HOME_TEST="$ROOT/home"
PREFIX_TEST="$ROOT/prefix"
mkdir -p "$REPO/tools" "$HOME_TEST" "$PREFIX_TEST"
cp "$(cd "$(dirname "$0")/../.." && pwd)/tools/deploy" "$REPO/tools/deploy"
chmod +x "$REPO/tools/deploy"

fail() {
  printf 'deploy smoke test: FAIL: %s\n' "$*" >&2
  exit 1
}

assert_symlink() {
  local path=$1
  [ -L "$path" ] || fail "expected symlink: $path"
}

# Minimal source tree required by tools/deploy.
mkdir -p \
  "$REPO/modules/desktop/overlay/home/.local/bin" \
  "$REPO/modules/gl/overlay/home/gl/bin" \
  "$REPO/modules/gl/overlay/home/gl/policy/vulkan" \
  "$REPO/modules/gl/overlay/home/gl/shims" \
  "$REPO/modules/gl/overlay/home/gl/toolchain" \
  "$REPO/packages/vscode/launcher" \
  "$REPO/packages/obsidian/launcher" \
  "$REPO/packages/mesa-glibc/build-env" \
  "$REPO/packages/mesa-glibc/patches/mesa"

touch \
  "$REPO/modules/desktop/overlay/home/.local/bin/startxfce-x11" \
  "$REPO/modules/gl/overlay/home/gl/env" \
  "$REPO/modules/gl/overlay/home/gl/bin/gl-run" \
  "$REPO/modules/gl/overlay/home/gl/bin/gl-farm" \
  "$REPO/modules/gl/overlay/home/gl/policy/vulkan/freedreno.sh" \
  "$REPO/modules/gl/overlay/home/gl/shims/xdg-open" \
  "$REPO/modules/gl/overlay/home/gl/toolchain/glibc-exec" \
  "$REPO/packages/vscode/launcher/code" \
  "$REPO/packages/obsidian/launcher/obsidian" \
  "$REPO/packages/obsidian/launcher/obsidian-app" \
  "$REPO/packages/mesa-glibc/build.sh" \
  "$REPO/packages/mesa-glibc/build-env/pyproject.toml" \
  "$REPO/packages/mesa-glibc/build-env/uv.lock" \
  "$REPO/packages/mesa-glibc/patches/mesa/.gitkeep"

# Reproduce the legacy live layout: directory symlinks into setup-like trees.
mkdir -p "$ROOT/legacy/gl-bin" "$ROOT/legacy/shims" "$ROOT/legacy/toolchain" "$ROOT/legacy/diag"
touch "$ROOT/legacy/gl-bin/gl-run" "$ROOT/legacy/gl-bin/gl-farm"
mkdir -p "$HOME_TEST/gl/build" "$HOME_TEST/gl" "$HOME_TEST/.local/bin"
ln -s "$ROOT/legacy/gl-bin" "$HOME_TEST/gl/bin"
ln -s "$ROOT/legacy/shims" "$HOME_TEST/gl/shims"
ln -s "$ROOT/legacy/toolchain" "$HOME_TEST/gl/toolchain"
ln -s "$ROOT/legacy/diag" "$HOME_TEST/gl/build/diag"
mkdir -p "$ROOT/legacy/patches/mesa"
ln -s "$ROOT/legacy/patches" "$HOME_TEST/gl/build/patches"

# Dry-run must succeed and must not mutate the legacy symlinks.
if ! HOME="$HOME_TEST" PREFIX="$PREFIX_TEST" bash "$REPO/tools/deploy" --dry-run >"$ROOT/dry-run.log" 2>&1; then
  cat "$ROOT/dry-run.log" >&2
  fail "dry-run exited non-zero"
fi
assert_symlink "$HOME_TEST/gl/bin"
assert_symlink "$HOME_TEST/gl/build/diag"

# Real deployment converts legacy directory links and installs leaf links.
if ! HOME="$HOME_TEST" PREFIX="$PREFIX_TEST" bash "$REPO/tools/deploy" >"$ROOT/deploy.log" 2>&1; then
  cat "$ROOT/deploy.log" >&2
  fail "real deployment exited non-zero"
fi

[ -d "$HOME_TEST/gl/bin" ] && [ ! -L "$HOME_TEST/gl/bin" ] || fail "gl/bin was not materialized"
assert_symlink "$HOME_TEST/gl/bin/gl-run"
assert_symlink "$HOME_TEST/gl/bin/gl-farm"
assert_symlink "$HOME_TEST/gl/bin/obsidian"
assert_symlink "$HOME_TEST/gl/bin/obsidian-app"
assert_symlink "$HOME_TEST/gl/policy/vulkan/freedreno.sh"
assert_symlink "$HOME_TEST/.local/bin/code"
assert_symlink "$HOME_TEST/.local/bin/startxfce-x11"
assert_symlink "$HOME_TEST/gl/env"
assert_symlink "$HOME_TEST/gl/build/build-mesa.sh"
assert_symlink "$HOME_TEST/gl/build/patches/mesa"
[ ! -e "$HOME_TEST/gl/build/diag" ] && [ ! -L "$HOME_TEST/gl/build/diag" ] || fail "obsolete diag link still exists"

printf 'deploy smoke test: PASS\n'
