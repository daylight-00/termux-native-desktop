#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BASE=${TND_TEST_TMPDIR:-$(mktemp -d)}
FIXTURE="$BASE/repo"
rm -rf "$FIXTURE"; mkdir -p "$FIXTURE"
git -C "$ROOT" archive HEAD | tar -x -C "$FIXTURE"
bash "$FIXTURE/tools/docs/check-libjpeg-so-62-gdkpixbuf-diagnostic-matrix-result-review"

expect_fail() {
  local copy=$1
  if bash "$copy/tools/docs/check-libjpeg-so-62-gdkpixbuf-diagnostic-matrix-result-review" >/dev/null 2>&1; then
    echo "expected failure: $(basename "$copy")" >&2
    exit 1
  fi
}

copy="$BASE/pass-count"; cp -a "$FIXTURE" "$copy"
sed -i '2s/\t0\t12\t0\tDIRECT_CONTROL_ENVIRONMENT_UNRESOLVED/\t1\t12\t0\tDIRECT_CONTROL_ENVIRONMENT_UNRESOLVED/' \
  "$copy/experiments/glibc/selected-obsidian-provider-authority/review/libjpeg-so-62-gdkpixbuf-diagnostic-matrix-result-review.tsv"
expect_fail "$copy"

copy="$BASE/provider-authority"; cp -a "$FIXTURE" "$copy"
sed -i '2s/\tNOT_ACCEPTED\t/\tACCEPTED\t/' \
  "$copy/experiments/glibc/selected-obsidian-provider-authority/review/libjpeg-so-62-gdkpixbuf-diagnostic-matrix-result-review.tsv"
expect_fail "$copy"

copy="$BASE/active-task"; cp -a "$FIXTURE" "$copy"
sed -i 's/rerun-libjpeg-so-62-gdkpixbuf-with-loader-isolation/accept-libjpeg-provider/' \
  "$copy/docs/current/ACTIVE_TASK.md"
expect_fail "$copy"

echo 'libjpeg diagnostic review smoke: PASS'
