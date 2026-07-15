#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
FIXTURE=$(mktemp -d "$TMP_BASE/libepoxy-provider-smoke.XXXXXX")
cleanup(){ chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }; trap cleanup EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
bash "$FIXTURE/tools/docs/check-libepoxy-reference-consumed-provider-authority" >/dev/null
TABLE=experiments/glibc/selected-obsidian-provider-authority/review/libepoxy-reference-consumed-provider-authority.tsv
restore(){ git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"; }
mutate(){ python3 - "$FIXTURE/$TABLE" "$1" "$2" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); field=sys.argv[2]; value=sys.argv[3]; lines=p.read_text().splitlines(); c=lines[0].split('\t'); r=lines[1].split('\t'); r[c.index(field)]=value; lines[1]='\t'.join(r); p.write_text('\n'.join(lines)+'\n')
PY
}
mutate observed_soname libepoxy.so.999
if bash "$FIXTURE/tools/docs/check-libepoxy-reference-consumed-provider-authority" >/dev/null 2>&1; then echo 'libepoxy smoke: SONAME drift accepted' >&2; exit 1; fi
restore
mutate feature_selection_contract 'X11_REQUIRED_AND_BOUND;GLX_NOT_REQUIRED;EGL_ACCEPTED'
if bash "$FIXTURE/tools/docs/check-libepoxy-reference-consumed-provider-authority" >/dev/null 2>&1; then echo 'libepoxy smoke: feature contract broadening accepted' >&2; exit 1; fi
restore
mutate consumer_binding_basis 'PACKAGE_PRESENT_IN_CLOSURE_ONLY'
if bash "$FIXTURE/tools/docs/check-libepoxy-reference-consumed-provider-authority" >/dev/null 2>&1; then echo 'libepoxy smoke: weak consumer binding accepted' >&2; exit 1; fi
restore
mutate authority_effect 'COMPLETE_GL_COMPOSITION_TARGET_AND_ACTIVATION_ACCEPTED'
if bash "$FIXTURE/tools/docs/check-libepoxy-reference-consumed-provider-authority" >/dev/null 2>&1; then echo 'libepoxy smoke: authority broadening accepted' >&2; exit 1; fi
restore
sed -i '2d' "$FIXTURE/$TABLE"
if bash "$FIXTURE/tools/docs/check-libepoxy-reference-consumed-provider-authority" >/dev/null 2>&1; then echo 'libepoxy smoke: missing review row accepted' >&2; exit 1; fi
echo 'libepoxy reference-consumed provider authority smoke: PASS'
