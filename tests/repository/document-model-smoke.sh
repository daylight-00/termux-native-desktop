#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
WORK=$(mktemp -d "$TMP_BASE/tnd-document-model.XXXXXX")
cleanup() {
  chmod -R u+w "$WORK" 2>/dev/null || true
  rm -rf "$WORK"
}
trap cleanup EXIT HUP INT TERM

bash "$ROOT/tools/docs/check-document-model"

mkdir -p "$WORK/repo"
git -C "$ROOT" archive HEAD | tar -xf - -C "$WORK/repo"

# Ignored upstream source snapshots are not project documentation authority.
mkdir -p "$WORK/repo/experiments/example/work/source/upstream"
printf '%s\n' '[Security](/SECURITY.md)' \
  >"$WORK/repo/experiments/example/work/source/upstream/README.md"
bash "$WORK/repo/tools/docs/check-document-model" >/dev/null

# A broken link in repository-managed documentation must still be rejected.
printf '%s\n' '[Missing](does-not-exist.md)' >"$WORK/repo/docs/broken-link-test.md"
if bash "$WORK/repo/tools/docs/check-document-model" >/dev/null 2>&1; then
  printf 'document-model smoke: managed broken link was not rejected\n' >&2
  exit 1
fi
rm -f "$WORK/repo/docs/broken-link-test.md"

# The guard must reject historical material in the default onboarding set.
python3 - "$WORK/repo/docs/catalog.tsv" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
text = p.read_text()
text = text.replace(
    'handoff-index\thistory\thistorical\thistory\tno\t',
    'handoff-index\thistory\thistorical\thistory\tyes\t',
)
p.write_text(text)
PY
if bash "$WORK/repo/tools/docs/check-document-model" >/dev/null 2>&1; then
  printf 'document-model smoke: historical default onboarding was not rejected\n' >&2
  exit 1
fi

# Restore and prove the required-reading cap is enforced.
rm -rf "$WORK/repo"
mkdir -p "$WORK/repo"
git -C "$ROOT" archive HEAD | tar -xf - -C "$WORK/repo"
python3 - "$WORK/repo/docs/current/ACTIVE_TASK.md" <<'PY2'
from pathlib import Path
import re
import sys
p = Path(sys.argv[1])
text = p.read_text()
match = re.search(r'(^## Required reading\s*$\n)(.*?)(?=^## )', text, flags=re.M | re.S)
if not match:
    raise SystemExit('required-reading block missing')
extra = ''.join(f'- `docs/PROJECT_CONTEXT.md`\n' for _ in range(3))
text = text[:match.end(2)] + extra + text[match.end(2):]
p.write_text(text)
PY2
if bash "$WORK/repo/tools/docs/check-document-model" >/dev/null 2>&1; then
  printf 'document-model smoke: required-reading overflow was not rejected\n' >&2
  exit 1
fi

printf 'document-model smoke: PASS\n'
