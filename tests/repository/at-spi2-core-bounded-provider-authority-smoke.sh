#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"; TMP=$(mktemp -d "$TMP_BASE/atspi2-provider-smoke.XXXXXX")
cleanup(){ chmod -R u+w "$TMP" 2>/dev/null || true; rm -rf "$TMP"; }; trap cleanup EXIT HUP INT TERM
"$ROOT/tools/docs/check-at-spi2-core-bounded-provider-authority"
files=(
 docs/evidence/at-spi2-core-bounded-provider-authority.md docs/evidence/at-spi2-core-production-recipe-candidate-result-review.md
 docs/current/STATE.yaml docs/current/ACTIVE_TASK.md docs/current/BRIEF.md docs/catalog.tsv docs/evidence/README.md STATUS.md
 experiments/glibc/selected-obsidian-provider-authority/review/at-spi2-core-bounded-provider-authority.tsv
 experiments/glibc/selected-obsidian-provider-authority/review/at-spi2-core-production-recipe-candidate-result-review.tsv
 experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-members.tsv
 experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-gaps.tsv
 experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-metadata.tsv
 experiments/glibc/selected-obsidian-provider-authority/review/provider-claim-classification.tsv
 experiments/glibc/selected-obsidian-provider-authority/review/provider-claim-classification-metadata.tsv
)
make_fixture(){ local dst=$1 rel; mkdir -p "$dst"; for rel in "${files[@]}"; do mkdir -p "$dst/$(dirname "$rel")"; cp "$ROOT/$rel" "$dst/$rel"; done; }
make_fixture "$TMP/open"
python3 - "$TMP/open/experiments/glibc/selected-obsidian-provider-authority/review/at-spi2-core-bounded-provider-authority.tsv" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]);p.write_text(p.read_text().replace('ACCEPTED_BOUNDED_PROVIDER','OPEN_REVIEW_REQUIRED',1))
PY
if TND_CHECK_ROOT="$TMP/open" "$ROOT/tools/docs/check-at-spi2-core-bounded-provider-authority" >/dev/null 2>&1; then echo 'atspi2-provider-smoke: authority-open mutation accepted' >&2; exit 1; fi
make_fixture "$TMP/hash"
python3 - "$TMP/hash/experiments/glibc/selected-obsidian-provider-authority/review/at-spi2-core-bounded-provider-authority.tsv" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]);p.write_text(p.read_text().replace('e94f2980cf8580634d7ab3c4f9ad2d8713880a1e3614001aed7a63ba6388c874','0'*64,1))
PY
if TND_CHECK_ROOT="$TMP/hash" "$ROOT/tools/docs/check-at-spi2-core-bounded-provider-authority" >/dev/null 2>&1; then echo 'atspi2-provider-smoke: member-hash mutation accepted' >&2; exit 1; fi
make_fixture "$TMP/service"
python3 - "$TMP/service/experiments/glibc/selected-obsidian-provider-authority/review/at-spi2-core-bounded-provider-authority.tsv" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1]);p.write_text(p.read_text().replace('SEVEN_ACTIVATION_METADATA_FILES_DISABLED_ZERO_ACTIVE_METADATA_TWO_HELPERS_NOT_EXECUTED','ACTIVE_METADATA_AND_HELPERS_AUTHORIZED',1))
PY
if TND_CHECK_ROOT="$TMP/service" "$ROOT/tools/docs/check-at-spi2-core-bounded-provider-authority" >/dev/null 2>&1; then echo 'atspi2-provider-smoke: service widening accepted' >&2; exit 1; fi
echo 'at-spi2-core-bounded-provider-authority-smoke: PASS'
