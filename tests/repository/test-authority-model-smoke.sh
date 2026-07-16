#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
WORK=$(mktemp -d "$TMP_BASE/test-authority.XXXXXX")
cleanup(){ chmod -R u+w "$WORK" 2>/dev/null || true; rm -rf "$WORK"; }
trap cleanup EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -xf - -C "$WORK"
"$WORK/tools/docs/check-test-authority-model" >/dev/null
# Reintroducing a superseded stage smoke into the current runner must fail.
python3 - "$WORK/tests/run-repository" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text(); needle='      tests/repository/libjpeg-so-62-loader-isolated-provider-authority-smoke.sh\n'
p.write_text(s.replace(needle, needle+'      tests/repository/libjpeg-so-62-provider-candidate-disposition-smoke.sh\n',1))
PY
if "$WORK/tools/docs/check-test-authority-model" >/dev/null 2>&1; then
  echo 'test authority smoke: historical stage smoke re-entered current suite' >&2; exit 1
fi
git -C "$ROOT" show HEAD:tests/run-repository > "$WORK/tests/run-repository"
# A reusable component checker must not become the active-task owner.
printf '\n# docs/current/ACTIVE_TASK.md\n' >> "$WORK/tools/docs/check-gdkpixbuf-build-env"
if "$WORK/tools/docs/check-test-authority-model" >/dev/null 2>&1; then
  echo 'test authority smoke: durable checker accepted active-task coupling' >&2; exit 1
fi
printf 'test authority model smoke: PASS\n'
