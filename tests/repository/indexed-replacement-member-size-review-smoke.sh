#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"; F=$(mktemp -d "$TMP_BASE/index-size-smoke.XXXXXX"); trap 'rm -rf "$F"' EXIT
git -C "$ROOT" archive HEAD | tar -xf - -C "$F"
python3 "$F/tools/docs/check-indexed-replacement-member-size-review" >/dev/null
META="$F/experiments/glibc/selected-obsidian-provider-authority/review/selected-target-index-size-review-metadata.tsv"
sed -i 's/population_authorized\tNO/population_authorized\tYES/' "$META"
if python3 "$F/tools/docs/check-indexed-replacement-member-size-review" >/dev/null 2>&1; then echo population widening accepted >&2; exit 1; fi
git -C "$ROOT" show HEAD:experiments/glibc/selected-obsidian-provider-authority/review/selected-target-index-size-review-metadata.tsv > "$META"
SIZE="$F/experiments/glibc/selected-obsidian-provider-authority/profiles/selected-target-member-size-evidence.tsv"
python3 - "$SIZE" <<'PY2'
from pathlib import Path
import sys
p=Path(sys.argv[1]);s=p.read_text();s=s.replace('libpixman-1.so.0.46.4\tcab54c7f8e4c3a5c1980aa7564b9321114418f2d3c6fa37a3c0723f9f22e1eb2\t\tOPEN','libpixman-1.so.0.46.4\tcab54c7f8e4c3a5c1980aa7564b9321114418f2d3c6fa37a3c0723f9f22e1eb2\t152856\tEXACT');p.write_text(s)
PY2
if python3 "$F/tools/docs/check-indexed-replacement-member-size-review" >/dev/null 2>&1; then echo fabricated Pixman size accepted >&2; exit 1; fi
echo 'indexed replacement and member-size review smoke: PASS'
