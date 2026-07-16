#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
FIXTURE=$(mktemp -d "$TMP_BASE/libjpeg-provider-authority.XXXXXX")
cleanup(){ chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }; trap cleanup EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
bash "$FIXTURE/tools/docs/check-libjpeg-so-62-loader-isolated-provider-authority" >/dev/null
TABLE=experiments/glibc/selected-obsidian-provider-authority/review/libjpeg-so-62-loader-isolated-provider-authority.tsv
restore(){ git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"; }
python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); lines=p.read_text().splitlines(); c=lines[0].split('\t'); r=lines[1].split('\t'); r[c.index('matrix_pass_count')]='5'; lines[1]='\t'.join(r); p.write_text('\n'.join(lines)+'\n')
PY
if bash "$FIXTURE/tools/docs/check-libjpeg-so-62-loader-isolated-provider-authority" >/dev/null 2>&1; then echo 'libjpeg provider smoke: partial matrix accepted' >&2; exit 1; fi
restore
python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); lines=p.read_text().splitlines(); c=lines[0].split('\t'); r=lines[1].split('\t'); r[c.index('decision')]='NOT_ACCEPTED'; lines[1]='\t'.join(r); p.write_text('\n'.join(lines)+'\n')
PY
if bash "$FIXTURE/tools/docs/check-libjpeg-so-62-loader-isolated-provider-authority" >/dev/null 2>&1; then echo 'libjpeg provider smoke: decision drift accepted' >&2; exit 1; fi
restore
python3 - "$FIXTURE/$TABLE" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); lines=p.read_text().splitlines(); c=lines[0].split('\t'); r=lines[1].split('\t'); r[c.index('authority_effect')]='COMPLETE_COMPOSITION_TARGET_AND_ACTIVATION_ACCEPTED'; lines[1]='\t'.join(r); p.write_text('\n'.join(lines)+'\n')
PY
if bash "$FIXTURE/tools/docs/check-libjpeg-so-62-loader-isolated-provider-authority" >/dev/null 2>&1; then echo 'libjpeg provider smoke: broad authority accepted' >&2; exit 1; fi
echo 'libjpeg loader-isolated provider authority smoke: PASS'
