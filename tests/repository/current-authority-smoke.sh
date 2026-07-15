#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)

bash "$ROOT/tools/docs/check-control-plane"
bash "$ROOT/tools/docs/check-current-authority"

# Negative checks prove the guard catches the major stale authority classes.
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
WORK=$(mktemp -d "$TMP_BASE/tnd-current-authority.XXXXXX")
cleanup() {
  chmod -R u+w "$WORK" 2>/dev/null || true
  rm -rf "$WORK"
}
trap cleanup EXIT HUP INT TERM

mkdir -p "$WORK/repo"
git -C "$ROOT" archive HEAD | tar -xf - -C "$WORK/repo"
cp "$WORK/repo/docs/architecture.md" "$WORK/architecture.md.original"
printf '\nCurrent deployment uses source-linked leaves.\n' >> "$WORK/repo/docs/architecture.md"
if bash "$WORK/repo/tools/docs/check-current-authority" >/dev/null 2>&1; then
  printf 'current-authority smoke: stale deployment claim was not rejected\n' >&2
  exit 1
fi

cp "$WORK/architecture.md.original" "$WORK/repo/docs/architecture.md"
printf '\nmandatory handoff\n' >> "$WORK/repo/docs/operations/WORKFLOW.md"
if bash "$WORK/repo/tools/docs/check-current-authority" >/dev/null 2>&1; then
  printf 'current-authority smoke: mandatory handoff dependency was not rejected\n' >&2
  exit 1
fi

printf 'current-authority smoke: PASS\n'
