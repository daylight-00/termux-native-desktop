#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
TMP=$(mktemp -d "$TMP_BASE/gdkpixbuf-reference-provider.XXXXXX")
cleanup(){ chmod -R u+w "$TMP" 2>/dev/null || true; rm -rf "$TMP"; }
trap cleanup EXIT HUP INT TERM
bash "$ROOT/tools/docs/check-gdkpixbuf-reference-dependency-provider-authority"
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
python3 - "$TMP/experiments/glibc/selected-obsidian-provider-authority/review/gdkpixbuf-util-linux-transitive-provider-disposition.tsv" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); t=p.read_text(); p.write_text(t.replace('OPEN_EXACT_RUNTIME_BINDING_REQUIRED','ACCEPTED_BOUNDED_PROVIDER',1))
PY
if bash "$TMP/tools/docs/check-gdkpixbuf-reference-dependency-provider-authority" >/dev/null 2>&1; then
  echo 'gdkpixbuf reference provider smoke: FAIL: util-linux authority widening accepted' >&2
  exit 1
fi
rm -rf "$TMP"/*
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
python3 - "$TMP/experiments/glibc/selected-obsidian-provider-authority/review/gdkpixbuf-reference-dependency-provider-authority.tsv" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); t=p.read_text(); p.write_text(t.replace('e0504b50e14870623e10490d76b78c7a8d0037a54fe354429e2e3b5ac07ae0d5','0'*64,1))
PY
if bash "$TMP/tools/docs/check-gdkpixbuf-reference-dependency-provider-authority" >/dev/null 2>&1; then
  echo 'gdkpixbuf reference provider smoke: FAIL: exact member digest drift accepted' >&2
  exit 1
fi
printf 'gdkpixbuf reference provider smoke: PASS\n'
