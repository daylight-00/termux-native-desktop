#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}
mkdir -p "$TMP_BASE"
FIXTURE=$(mktemp -d "$TMP_BASE/web-chat-capability-contract-smoke.XXXXXX")
cleanup() { chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }
trap cleanup EXIT HUP INT TERM

restore_file() {
  git -C "$ROOT" show "HEAD:$1" > "$FIXTURE/$1"
}

run_check() {
  bash "$FIXTURE/tools/docs/check-web-chat-capability-contract" "$FIXTURE" >/dev/null
}

git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
run_check

# Negative: DNS fallback cannot remain in the sandbox or omit verified transfer.
python3 - "$FIXTURE/docs/operations/platforms/chatgpt-web-limitations.tsv" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1])
s=p.read_text()
s=s.replace('issue one exact user-Termux acquisition/analyzer wrapper with URL digest bounded analysis and result tar.zst',
            'keep retrying from the sandbox')
p.write_text(s)
PY
if run_check 2>/dev/null; then
  echo 'web-chat capability smoke: invalid DNS fallback was accepted' >&2
  exit 1
fi
restore_file docs/operations/platforms/chatgpt-web-limitations.tsv

# Negative: duplicate IDs are forbidden.
tail -n 1 "$FIXTURE/docs/operations/platforms/chatgpt-web-limitations.tsv" >> "$FIXTURE/docs/operations/platforms/chatgpt-web-limitations.tsv"
if run_check 2>/dev/null; then
  echo 'web-chat capability smoke: duplicate limitation ID was accepted' >&2
  exit 1
fi
restore_file docs/operations/platforms/chatgpt-web-limitations.tsv

# Negative: the default agent contract must route the limitation registry.
sed -i '/chatgpt-web-limitations.tsv/d' "$FIXTURE/AGENTS.md"
if run_check 2>/dev/null; then
  echo 'web-chat capability smoke: missing AGENTS registry route was accepted' >&2
  exit 1
fi
restore_file AGENTS.md

# Negative: the runtime-first-upload fallback cannot demote Drive for future artifacts.
python3 - "$FIXTURE/docs/operations/platforms/chatgpt-web-limitations.tsv" <<'PY'
from pathlib import Path
import csv,sys
p=Path(sys.argv[1])
with p.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f,delimiter='\t'))
for row in rows:
    if row['limitation_id']=='WEB-DRIVE-RUNTIME-FIRST-UPLOAD-001':
        row['preferred_fallback']='use user-visible sandbox links for all current and future artifacts'
with p.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if run_check 2>/dev/null; then
  echo 'web-chat capability smoke: permanent Drive demotion was accepted' >&2
  exit 1
fi
restore_file docs/operations/platforms/chatgpt-web-limitations.tsv

# Negative: runtime reset behavior must not be narrowed to new-chat first turn.
python3 - "$FIXTURE/docs/operations/platforms/chatgpt-web-limitations.tsv" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1])
s=p.read_text().replace(
 'the first upload attempted after the web-chat runtime is initialized or reset blocks local-path-to-file-reference rewrite even in an existing chat',
 'the first assistant turn of a new chat blocks local-path rewrite')
p.write_text(s)
PY
if run_check 2>/dev/null; then
  echo 'web-chat capability smoke: new-chat-only Drive model was accepted' >&2
  exit 1
fi
restore_file docs/operations/platforms/chatgpt-web-limitations.tsv

# Negative: device evidence cannot be reassigned to the sandbox.
python3 - "$FIXTURE/docs/operations/platforms/chatgpt-web-limitations.tsv" <<'PY'
from pathlib import Path
p=Path(__import__('sys').argv[1])
s=p.read_text().replace(
 'WEB-DEVICE-001\tandroid-device\tAndroid package loader GPU filesystem deployment or runtime fact is required\tinfer from sandbox state or label a synthetic test authoritative\tissue the smallest self-contained Termux runner and review its structured result\tuser-termux',
 'WEB-DEVICE-001\tandroid-device\tAndroid package loader GPU filesystem deployment or runtime fact is required\tinfer from sandbox state or label a synthetic test authoritative\tuse a synthetic sandbox test\tsandbox')
p.write_text(s)
PY
if run_check 2>/dev/null; then
  echo 'web-chat capability smoke: sandbox device authority was accepted' >&2
  exit 1
fi

echo 'web-chat capability contract smoke: PASS'
