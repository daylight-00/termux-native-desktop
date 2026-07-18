#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
"$ROOT/tools/docs/check-fontconfig-bounded-provider-authority" >/dev/null
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"
TMP=$(mktemp -d "$TMP_BASE/fontconfig-provider-smoke.XXXXXX")
cleanup(){ chmod -R u+w "$TMP" 2>/dev/null || true; rm -rf "$TMP"; }; trap cleanup EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -x -C "$TMP"
python3 - "$TMP" <<'PY'
from pathlib import Path
import csv,sys
p=Path(sys.argv[1])/'experiments/glibc/selected-obsidian-provider-authority/review/fontconfig-bounded-provider-authority.tsv'
with p.open(newline='',encoding='utf-8') as f: reader=csv.DictReader(f,delimiter='\t'); fields=reader.fieldnames; rows=list(reader)
rows[0]['dependency_boundary']='PACKAGE_GENERATED_FONTS_CONF_ACCEPTED_AS_TARGET_POLICY;GLOBAL_CACHE_ACCEPTED;SYSTEM_FONTS_ACCEPTED;CACHE_REUSE_ACROSS_GENERATIONS_ACCEPTED'
with p.open('w',newline='',encoding='utf-8') as f: writer=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); writer.writeheader(); writer.writerows(rows)
PY
if "$TMP/tools/docs/check-fontconfig-bounded-provider-authority" >/dev/null 2>&1; then echo 'fontconfig-provider-smoke: FAIL: widened package config/global cache/system font semantics accepted' >&2; exit 1; fi
echo 'fontconfig-provider-smoke: PASS'
