#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
TMP=$(mktemp -d "$TMP_BASE/libxdamage-provider-smoke.XXXXXX")
cleanup(){ chmod -R u+w "$TMP" 2>/dev/null || true; rm -rf "$TMP"; }
trap cleanup EXIT HUP INT TERM

"$ROOT/tools/docs/check-libxdamage-bounded-provider-authority"

files=(
 docs/evidence/libxdamage-bounded-provider-authority.md
 docs/evidence/libxdamage-production-recipe-candidate-result-review.md
 docs/current/STATE.yaml docs/current/ACTIVE_TASK.md docs/current/BRIEF.md docs/catalog.tsv docs/evidence/README.md STATUS.md
 experiments/glibc/selected-obsidian-provider-authority/review/libxdamage-bounded-provider-authority.tsv
 experiments/glibc/selected-obsidian-provider-authority/review/libxdamage-production-recipe-candidate-result-review.tsv
 experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-members.tsv
 experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-gaps.tsv
 experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-metadata.tsv
 experiments/glibc/selected-obsidian-provider-authority/review/provider-claim-classification.tsv
 experiments/glibc/selected-obsidian-provider-authority/review/provider-claim-classification-metadata.tsv
 experiments/glibc/selected-obsidian-provider-authority/review/xorg-reference-consumed-provider-authority.tsv
 experiments/glibc/selected-obsidian-provider-authority/review/selected-object-authority-base.tsv
)
make_fixture(){
  local dst=$1 rel
  mkdir -p "$dst"
  for rel in "${files[@]}"; do mkdir -p "$dst/$(dirname "$rel")"; cp "$ROOT/$rel" "$dst/$rel"; done
}

make_fixture "$TMP/open"
python3 - "$TMP/open/experiments/glibc/selected-obsidian-provider-authority/review/libxdamage-bounded-provider-authority.tsv" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]); s=p.read_text(); p.write_text(s.replace('ACCEPTED_BOUNDED_PROVIDER','OPEN_REVIEW_REQUIRED',1))
PY
if TND_CHECK_ROOT="$TMP/open" "$ROOT/tools/docs/check-libxdamage-bounded-provider-authority" >/dev/null 2>&1; then
  echo 'libxdamage-provider-authority-smoke: authority-open mutation was accepted' >&2; exit 1
fi

make_fixture "$TMP/hash"
python3 - "$TMP/hash/experiments/glibc/selected-obsidian-provider-authority/review/libxdamage-bounded-provider-authority.tsv" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]); s=p.read_text(); p.write_text(s.replace('391916aff0965656e7b81ece7766e3b22068462867b1dd88a0a051b3db9c2d7c','0'*64,1))
PY
if TND_CHECK_ROOT="$TMP/hash" "$ROOT/tools/docs/check-libxdamage-bounded-provider-authority" >/dev/null 2>&1; then
  echo 'libxdamage-provider-authority-smoke: member-hash mutation was accepted' >&2; exit 1
fi

echo 'libxdamage-bounded-provider-authority-smoke: PASS'
