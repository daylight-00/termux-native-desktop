#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
FIXTURE=$(mktemp -d "$TMP_BASE/libjpeg-gdkpixbuf-review-smoke.XXXXXX")
cleanup(){ chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }; trap cleanup EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
CHECK="$FIXTURE/tools/docs/check-libjpeg-so-62-gdkpixbuf-consumer-binding-result-review"
TABLE=experiments/glibc/selected-obsidian-provider-authority/review/libjpeg-so-62-gdkpixbuf-consumer-binding-result-review.tsv
bash "$CHECK" "$FIXTURE" >/dev/null
restore(){ git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"; }
mutate(){ python3 - "$FIXTURE/$TABLE" "$1" "$2" <<'PY'
from pathlib import Path
import csv,sys
p=Path(sys.argv[1]); rows=list(csv.DictReader(p.open(),delimiter='\t')); rows[0][sys.argv[2]]=sys.argv[3]
with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
PY
}
mutate functional_result PASS
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'gdkpixbuf review smoke: false functional pass accepted' >&2; exit 1; fi
restore
mutate provider_authority ACCEPTED
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'gdkpixbuf review smoke: provider authority broadened' >&2; exit 1; fi
restore
mutate missing_jpeg_symbols 1
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'gdkpixbuf review smoke: static coverage drift accepted' >&2; exit 1; fi
restore
mutate runtime_loader_boundary DEBIAN_ONLY
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'gdkpixbuf review smoke: runtime boundary drift accepted' >&2; exit 1; fi
restore
sed -i 's/rerun-libjpeg-so-62-gdkpixbuf-with-loader-isolation/validate-libjpeg-so-62-compatibility-provider-consumer-binding/' "$FIXTURE/docs/current/ACTIVE_TASK.md"
if bash "$CHECK" "$FIXTURE" >/dev/null 2>&1; then echo 'gdkpixbuf review smoke: stale task accepted' >&2; exit 1; fi
echo 'libjpeg.so.62 GdkPixbuf consumer-binding result review smoke: PASS'
