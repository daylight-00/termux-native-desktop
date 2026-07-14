#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
WORK=$(mktemp -d "$TMP_BASE/tnd-control-plane.XXXXXX")
cleanup() {
  chmod -R u+w "$WORK" 2>/dev/null || true
  rm -rf "$WORK"
}
trap cleanup EXIT HUP INT TERM

bash "$ROOT/tools/docs/check-control-plane"

# Candidate tests run before publication, so the current candidate may not yet
# be refs/heads/main in the authoring repository. Reproduce the accepted state
# in a temporary local clone, then prove that a user-created --all bundle alone
# can initialize a clean main checkout without a network remote.
[ -z "$(git -C "$ROOT" status --porcelain --untracked-files=no)" ] || {
  printf 'control-plane smoke: tracked worktree must be clean for bundle test\n' >&2
  exit 1
}

CANDIDATE_HEAD=$(git -C "$ROOT" rev-parse HEAD)
CANDIDATE_TREE=$(git -C "$ROOT" rev-parse HEAD^{tree})

git clone --no-hardlinks "$ROOT" "$WORK/source" >/dev/null 2>&1
git -C "$WORK/source" checkout -B main "$CANDIDATE_HEAD" >/dev/null 2>&1
git -C "$WORK/source" bundle create "$WORK/repository.bundle" --all
git -C "$WORK/source" bundle verify "$WORK/repository.bundle" >/dev/null

git clone "$WORK/repository.bundle" "$WORK/clone" >/dev/null 2>&1
git -C "$WORK/clone" checkout main >/dev/null 2>&1

[ "$(git -C "$WORK/clone" rev-parse HEAD)" = "$CANDIDATE_HEAD" ]
[ "$(git -C "$WORK/clone" rev-parse HEAD^{tree})" = "$CANDIDATE_TREE" ]
[ -z "$(git -C "$WORK/clone" status --porcelain)" ]

bash "$WORK/clone/tools/docs/check-control-plane" >/dev/null

grep -Fq 'docs/current/BRIEF.md' "$WORK/clone/START_HERE.md"
grep -Fq 'docs/current/ACTIVE_TASK.md' "$WORK/clone/START_HERE.md"
grep -Fq 'user-provided-full-git-bundle' "$WORK/clone/docs/current/STATE.yaml"

printf 'control-plane smoke: PASS\n'
