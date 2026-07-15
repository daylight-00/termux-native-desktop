#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
FIXTURE=$(mktemp -d "$TMP_BASE/constitution-smoke.XXXXXX")
cleanup() { chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }
trap cleanup EXIT HUP INT TERM

git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
bash "$FIXTURE/tools/docs/check-constitution" >/dev/null

# Negative: a legacy constitutional source cannot regain canonical catalog authority.
python3 - "$FIXTURE/docs/catalog.tsv" <<'PY2'
from pathlib import Path
import sys
p=Path(sys.argv[1])
text=p.read_text().replace(
    'project-context\tconstitution\thistorical\thistory\tno\tdocs/PROJECT_CONTEXT.md',
    'project-context\tconstitution\tcurrent\tcanonical\tno\tdocs/PROJECT_CONTEXT.md',
)
p.write_text(text)
PY2
if bash "$FIXTURE/tools/docs/check-constitution" >/dev/null 2>&1; then
  echo 'constitution smoke: legacy source incorrectly accepted as canonical' >&2
  exit 1
fi

# Negative: accepted ADR cannot silently return to proposed state.
git -C "$ROOT" show HEAD:docs/catalog.tsv > "$FIXTURE/docs/catalog.tsv"
sed -i 's/- \*\*Status:\*\* accepted/- **Status:** proposed/' "$FIXTURE/docs/decisions/0005-proportional-assurance-depth.md"
if bash "$FIXTURE/tools/docs/check-constitution" >/dev/null 2>&1; then
  echo 'constitution smoke: proposed ADR incorrectly accepted' >&2
  exit 1
fi

echo 'constitution smoke: PASS'
