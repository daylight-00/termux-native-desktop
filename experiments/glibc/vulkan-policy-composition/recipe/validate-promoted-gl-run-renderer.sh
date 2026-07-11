#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
OUT=${OUT:-$PREFIX/tmp/tnd-vulkan-policy-composition/promoted-gl-run-renderer-$(date +%Y%m%d-%H%M%S)}
BUILD_HELPER="$SCRIPT_DIR/build-glx-renderer-probe.sh"
BINARY="$OUT/glx-renderer-probe"
GL_RUN=${GL_RUN:-$HOME/gl/bin/gl-run}

for command in git bash grep awk mkdir date readelf; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

tracked_dirty=$(git -C "$REPO" status --porcelain --untracked-files=no)
if [ -n "$tracked_dirty" ]; then
    printf 'tracked working-tree changes detected; renderer gate requires exact HEAD:\n' >&2
    printf '%s\n' "$tracked_dirty" >&2
    exit 2
fi

[ -x "$GL_RUN" ] || {
    printf 'missing promoted gl-run: %s\n' "$GL_RUN" >&2
    exit 1
}

[ -x "$BUILD_HELPER" ] || {
    printf 'missing GLX probe build helper: %s\n' "$BUILD_HELPER" >&2
    exit 1
}

if [ "${LIBGL_ALWAYS_SOFTWARE+x}" = x ]; then
    printf 'LIBGL_ALWAYS_SOFTWARE must be unset\n' >&2
    exit 2
fi

mkdir -p "$OUT"
branch=$(git -C "$REPO" branch --show-current)
head_sha=$(git -C "$REPO" rev-parse HEAD)
printf '%s\n' "$branch" >"$OUT/branch.txt"
printf '%s\n' "$head_sha" >"$OUT/head.txt"
printf '%s\n' "$GL_RUN" >"$OUT/gl-run-path.txt"

OUT_DIR="$OUT" BINARY="$BINARY" \
    bash "$BUILD_HELPER" >"$OUT/build.log" 2>&1

readelf -l "$BINARY" >"$OUT/readelf-program-headers.txt"
readelf -d "$BINARY" >"$OUT/readelf-dynamic.txt"

"$GL_RUN" "$BINARY" >"$OUT/renderer.stdout" 2>"$OUT/renderer.stderr"

vendor=$(awk -F ': ' '$1 == "GL_VENDOR" { print $2; exit }' "$OUT/renderer.stdout")
renderer=$(awk -F ': ' '$1 == "GL_RENDERER" { print $2; exit }' "$OUT/renderer.stdout")
version=$(awk -F ': ' '$1 == "GL_VERSION" { print $2; exit }' "$OUT/renderer.stdout")

printf 'gate\tstate\n' >"$OUT/gates.tsv"
failures=0

record_gate() {
    local gate=$1 state=$2
    printf '%s\t%s\n' "$gate" "$state" >>"$OUT/gates.tsv"
    [ "$state" = PASS ] || failures=$((failures + 1))
}

[ -n "$vendor" ] && record_gate gl_vendor_present PASS || record_gate gl_vendor_present FAIL
[ -n "$renderer" ] && record_gate gl_renderer_present PASS || record_gate gl_renderer_present FAIL
[ -n "$version" ] && record_gate gl_version_present PASS || record_gate gl_version_present FAIL

if printf '%s\n' "$renderer" | grep -Eiq 'zink'; then
    record_gate renderer_is_zink PASS
else
    record_gate renderer_is_zink FAIL
fi

if printf '%s\n' "$renderer" | grep -Eiq 'turnip|adreno'; then
    record_gate renderer_is_turnip_adreno PASS
else
    record_gate renderer_is_turnip_adreno FAIL
fi

if grep -Eq 'Requesting program interpreter.*glibc' "$OUT/readelf-program-headers.txt"; then
    record_gate probe_interpreter_is_glibc PASS
else
    record_gate probe_interpreter_is_glibc FAIL
fi

{
    printf 'field\tvalue\n'
    printf 'branch\t%s\n' "$branch"
    printf 'head\t%s\n' "$head_sha"
    printf 'gl_run\t%s\n' "$GL_RUN"
    printf 'binary\t%s\n' "$BINARY"
    printf 'vendor\t%s\n' "$vendor"
    printf 'renderer\t%s\n' "$renderer"
    printf 'version\t%s\n' "$version"
    printf 'gate_failures\t%s\n' "$failures"
} >"$OUT/summary.tsv"

if [ "$failures" -ne 0 ]; then
    printf 'FAIL\n' >"$OUT/validation.status"
    printf 'promoted gl-run renderer validation: FAIL (%s gates)\n' "$failures" >&2
    printf 'evidence: %s\n' "$OUT" >&2
    cat "$OUT/summary.tsv" >&2
    exit 1
fi

printf 'PASS\n' >"$OUT/validation.status"
printf 'promoted gl-run renderer validation: PASS\n'
printf 'evidence: %s\n' "$OUT"
printf '\n===== summary =====\n'
cat "$OUT/summary.tsv"
printf '\n===== gates =====\n'
cat "$OUT/gates.tsv"
printf '\n===== renderer stdout =====\n'
cat "$OUT/renderer.stdout"
printf '\n===== renderer stderr =====\n'
cat "$OUT/renderer.stderr"
