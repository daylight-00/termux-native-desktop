#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"; TMP=$(mktemp -d "$TMP_BASE/gtk3-core-provider-smoke.XXXXXX")
cleanup(){ chmod -R u+w "$TMP" 2>/dev/null || true; rm -rf "$TMP"; }; trap cleanup EXIT HUP INT TERM
"$ROOT/tools/docs/check-gtk3-core-bounded-provider-authority"
files=(docs/evidence/gtk3-core-bounded-provider-authority.md docs/evidence/gtk3-core-production-recipe-candidate-result-review.md docs/current/STATE.yaml docs/current/ACTIVE_TASK.md docs/current/BRIEF.md docs/catalog.tsv docs/evidence/README.md STATUS.md experiments/glibc/selected-obsidian-provider-authority/review/gtk3-core-bounded-provider-authority.tsv experiments/glibc/selected-obsidian-provider-authority/review/gtk3-core-production-recipe-candidate-result-review.tsv experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-members.tsv experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-gaps.tsv experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-metadata.tsv experiments/glibc/selected-obsidian-provider-authority/review/provider-claim-classification.tsv experiments/glibc/selected-obsidian-provider-authority/review/provider-claim-classification-metadata.tsv)
make_fixture(){ local dst=$1 rel; mkdir -p "$dst"; for rel in "${files[@]}"; do mkdir -p "$dst/$(dirname "$rel")"; cp "$ROOT/$rel" "$dst/$rel"; done; }
make_fixture "$TMP/open"
python3 - "$TMP/open/experiments/glibc/selected-obsidian-provider-authority/review/gtk3-core-bounded-provider-authority.tsv" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]);p.write_text(p.read_text().replace('ACCEPTED_BOUNDED_PROVIDER','OPEN_REVIEW_REQUIRED',1))
PY
if TND_CHECK_ROOT="$TMP/open" "$ROOT/tools/docs/check-gtk3-core-bounded-provider-authority" >/dev/null 2>&1; then echo 'gtk3-core-provider-smoke: authority-open mutation accepted' >&2; exit 1; fi
make_fixture "$TMP/hash"
python3 - "$TMP/hash/experiments/glibc/selected-obsidian-provider-authority/review/gtk3-core-bounded-provider-authority.tsv" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]);p.write_text(p.read_text().replace('0404b91acdaa3a2558e3a11214918692f64d0ba3cebaae4722e3aa4a61f31bc6','0'*64,1))
PY
if TND_CHECK_ROOT="$TMP/hash" "$ROOT/tools/docs/check-gtk3-core-bounded-provider-authority" >/dev/null 2>&1; then echo 'gtk3-core-provider-smoke: member-hash mutation accepted' >&2; exit 1; fi
make_fixture "$TMP/widen"
python3 - "$TMP/widen/experiments/glibc/selected-obsidian-provider-authority/review/gtk3-core-bounded-provider-authority.tsv" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]);p.write_text(p.read_text().replace('ONLY_TWO_RUNTIME_MEMBERS_AND_SONAME_ALIASES_ACCEPTED','PACKAGE_WIDE_AUTHORITY_ACCEPTED',1))
PY
if TND_CHECK_ROOT="$TMP/widen" "$ROOT/tools/docs/check-gtk3-core-bounded-provider-authority" >/dev/null 2>&1; then echo 'gtk3-core-provider-smoke: package-wide widening accepted' >&2; exit 1; fi
echo 'gtk3-core-bounded-provider-authority-smoke: PASS'
