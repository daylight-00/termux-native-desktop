#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
FIXTURE=$(mktemp -d "$TMP_BASE/operations-model-smoke.XXXXXX")
cleanup() { chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }
trap cleanup EXIT HUP INT TERM

git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
bash "$FIXTURE/tools/docs/check-operations-model" >/dev/null

# Negative: a current catalog row cannot point back to the retired surface.
printf 'bad-session-ops\toperations\tcurrent\tcanonical\tno\tdocs/session-operations/README.md\tbad duplicate authority\n' >> "$FIXTURE/docs/catalog.tsv"
if bash "$FIXTURE/tools/docs/check-operations-model" >/dev/null 2>&1; then
  echo 'operations-model smoke: retired current catalog path was accepted' >&2
  exit 1
fi
git -C "$ROOT" show HEAD:docs/catalog.tsv > "$FIXTURE/docs/catalog.tsv"

# Negative: current workflow cannot reintroduce a mandatory narrative handoff.
printf '\nA mandatory handoff is required after every accepted transition.\n' >> "$FIXTURE/docs/operations/WORKFLOW.md"
if bash "$FIXTURE/tools/docs/check-operations-model" >/dev/null 2>&1; then
  echo 'operations-model smoke: mandatory handoff was accepted' >&2
  exit 1
fi
git -C "$ROOT" show HEAD:docs/operations/WORKFLOW.md > "$FIXTURE/docs/operations/WORKFLOW.md"

# Negative: the historical surface cannot be removed without losing routing.
rm "$FIXTURE/docs/history/session-operations-v1/README.md"
if bash "$FIXTURE/tools/docs/check-operations-model" >/dev/null 2>&1; then
  echo 'operations-model smoke: missing historical lineage was accepted' >&2
  exit 1
fi

echo 'operations-model smoke: PASS'
