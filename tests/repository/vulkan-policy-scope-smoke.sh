#!/usr/bin/env bash
set -euo pipefail

REPO=$(cd "$(dirname "$0")/../.." && pwd)
ROOT=$(mktemp -d)
trap 'rm -rf "$ROOT"' EXIT

HOME_TEST="$ROOT/home"
PREFIX_TEST="$ROOT/prefix"
mkdir -p \
  "$HOME_TEST/gl/policy/vulkan" \
  "$HOME_TEST/gl/bin" \
  "$HOME_TEST/gl/apps/vscode/bin" \
  "$HOME_TEST/gl/apps/obsidian" \
  "$HOME_TEST/.local/bin" \
  "$PREFIX_TEST/tmp"

cp "$REPO/modules/gl/overlay/home/gl/env" "$HOME_TEST/gl/env"
cp "$REPO/modules/gl/overlay/home/gl/policy/vulkan/freedreno.sh" \
  "$HOME_TEST/gl/policy/vulkan/freedreno.sh"
cp "$REPO/modules/gl/overlay/home/gl/bin/gl-run" "$HOME_TEST/gl/bin/gl-run"

fail() {
  printf 'vulkan policy scope smoke: FAIL: %s\n' "$*" >&2
  exit 1
}

assert_line() {
  local file=$1 line=$2
  grep -Fx -- "$line" "$file" >/dev/null || {
    printf 'missing line in %s: %s\n' "$file" "$line" >&2
    cat "$file" >&2
    fail "assert_line"
  }
}

assert_no_line() {
  local file=$1 line=$2
  if grep -Fx -- "$line" "$file" >/dev/null; then
    cat "$file" >&2
    fail "unexpected line: $line"
  fi
}

cat >"$ROOT/capture-consumer.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
{
  printf 'VK_DRIVER_FILES=%s\n' "${VK_DRIVER_FILES-<unset>}"
  printf 'VK_ICD_FILENAMES=%s\n' "${VK_ICD_FILENAMES-<unset>}"
  printf 'MESA_LOADER_DRIVER_OVERRIDE=%s\n' "${MESA_LOADER_DRIVER_OVERRIDE-<unset>}"
  for arg in "$@"; do
    printf 'arg=%s\n' "$arg"
  done
} >"$CAPTURE"
EOF
chmod +x "$ROOT/capture-consumer.sh"

cp "$ROOT/capture-consumer.sh" "$HOME_TEST/gl/apps/vscode/bin/code"
cp "$ROOT/capture-consumer.sh" "$HOME_TEST/gl/apps/obsidian/obsidian"
cp "$ROOT/capture-consumer.sh" "$HOME_TEST/.local/bin/obsidian"

ICD="$HOME_TEST/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json"
mkdir -p "$(dirname "$ICD")"
printf '{}\n' >"$ICD"

run_vscode() {
  local mode=$1 capture=$2
  HOME="$HOME_TEST" \
  PREFIX="$PREFIX_TEST" \
  GL_GPU="$mode" \
  VK_DRIVER_FILES=/bionic/freedreno.json \
  VK_ICD_FILENAMES=/bionic/freedreno.json \
  CAPTURE="$capture" \
  bash "$REPO/packages/vscode/launcher/code" >/dev/null 2>&1
}

run_obsidian_app() {
  local mode=$1 capture=$2
  HOME="$HOME_TEST" \
  PREFIX="$PREFIX_TEST" \
  GL_GPU="$mode" \
  VK_DRIVER_FILES=/bionic/freedreno.json \
  VK_ICD_FILENAMES=/bionic/freedreno.json \
  CAPTURE="$capture" \
  bash "$REPO/packages/obsidian/launcher/obsidian-app" >/dev/null 2>&1
}

# CPU mode must retain only the sanitized glibc baseline.
run_vscode 0 "$ROOT/vscode-cpu.tsv"
assert_line "$ROOT/vscode-cpu.tsv" 'VK_DRIVER_FILES=<unset>'
assert_line "$ROOT/vscode-cpu.tsv" 'VK_ICD_FILENAMES=<unset>'
assert_line "$ROOT/vscode-cpu.tsv" 'arg=--disable-gpu'
assert_no_line "$ROOT/vscode-cpu.tsv" 'arg=--use-angle=vulkan'

# GPU mode must deliberately select the managed glibc Freedreno profile.
run_vscode 1 "$ROOT/vscode-gpu.tsv"
assert_line "$ROOT/vscode-gpu.tsv" "VK_DRIVER_FILES=$ICD"
assert_line "$ROOT/vscode-gpu.tsv" "VK_ICD_FILENAMES=$ICD"
assert_line "$ROOT/vscode-gpu.tsv" 'arg=--use-angle=vulkan'
assert_no_line "$ROOT/vscode-gpu.tsv" 'arg=--disable-gpu'

run_obsidian_app 0 "$ROOT/obsidian-cpu.tsv"
assert_line "$ROOT/obsidian-cpu.tsv" 'VK_DRIVER_FILES=<unset>'
assert_line "$ROOT/obsidian-cpu.tsv" 'VK_ICD_FILENAMES=<unset>'
assert_line "$ROOT/obsidian-cpu.tsv" 'arg=--disable-gpu'

run_obsidian_app 1 "$ROOT/obsidian-gpu.tsv"
assert_line "$ROOT/obsidian-gpu.tsv" "VK_DRIVER_FILES=$ICD"
assert_line "$ROOT/obsidian-gpu.tsv" "VK_ICD_FILENAMES=$ICD"
assert_line "$ROOT/obsidian-gpu.tsv" 'arg=--use-angle=vulkan'

# The CLI wrapper is provider-neutral but still receives ABI sanitation.
HOME="$HOME_TEST" \
PREFIX="$PREFIX_TEST" \
VK_DRIVER_FILES=/bionic/freedreno.json \
VK_ICD_FILENAMES=/bionic/freedreno.json \
CAPTURE="$ROOT/obsidian-cli.tsv" \
bash "$REPO/packages/obsidian/launcher/obsidian" >/dev/null 2>&1
assert_line "$ROOT/obsidian-cli.tsv" 'VK_DRIVER_FILES=<unset>'
assert_line "$ROOT/obsidian-cli.tsv" 'VK_ICD_FILENAMES=<unset>'

# gl-run composes the explicit provider profile plus the Zink bridge mode.
HOME="$HOME_TEST" \
PREFIX="$PREFIX_TEST" \
VK_DRIVER_FILES=/bionic/freedreno.json \
VK_ICD_FILENAMES=/bionic/freedreno.json \
CAPTURE="$ROOT/gl-run.tsv" \
bash "$HOME_TEST/gl/bin/gl-run" "$ROOT/capture-consumer.sh" >/dev/null 2>&1
assert_line "$ROOT/gl-run.tsv" "VK_DRIVER_FILES=$ICD"
assert_line "$ROOT/gl-run.tsv" "VK_ICD_FILENAMES=$ICD"
assert_line "$ROOT/gl-run.tsv" 'MESA_LOADER_DRIVER_OVERRIDE=zink'

# Missing provider bytes must not leave the inherited bionic policy active.
rm -f "$ICD"
run_vscode 1 "$ROOT/vscode-missing-provider.tsv"
assert_line "$ROOT/vscode-missing-provider.tsv" 'VK_DRIVER_FILES=<unset>'
assert_line "$ROOT/vscode-missing-provider.tsv" 'VK_ICD_FILENAMES=<unset>'
assert_line "$ROOT/vscode-missing-provider.tsv" 'arg=--disable-gpu'

if HOME="$HOME_TEST" PREFIX="$PREFIX_TEST" \
   bash "$HOME_TEST/gl/bin/gl-run" true >/dev/null 2>&1; then
  fail 'gl-run unexpectedly succeeded without the provider manifest'
fi

printf 'vulkan policy scope smoke: PASS\n'
