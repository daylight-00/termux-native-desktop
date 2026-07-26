#!/usr/bin/env bash
root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
checker="$root/tools/docs/check-selected-target-manifest-review"
"$checker"

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cp -a "$root/." "$tmp/repo"
python3 - "$tmp/repo/experiments/glibc/selected-obsidian-provider-authority/review/selected-target-manifest.tsv" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text()
s=s.replace('lib/libXcomposite.so.1\tSYMLINK','lib/libXcomposite.so.1.0.0\tSYMLINK',1)
p.write_text(s)
PY
if "$tmp/repo/tools/docs/check-selected-target-manifest-review" >/dev/null 2>&1; then
  echo 'negative collision mutation unexpectedly passed' >&2
  exit 1
fi
cp "$root/experiments/glibc/selected-obsidian-provider-authority/review/selected-target-manifest.tsv" "$tmp/repo/experiments/glibc/selected-obsidian-provider-authority/review/selected-target-manifest.tsv"
python3 - "$tmp/repo/experiments/glibc/selected-obsidian-provider-authority/review/selected-target-manifest.tsv" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text().replace('PROVISIONAL_BLOCKED\tUNPOPULATED_SCHEMA_ONLY','ACCEPTED_FINAL\tAUTHORIZED',1)
p.write_text(s)
PY
if "$tmp/repo/tools/docs/check-selected-target-manifest-review" >/dev/null 2>&1; then
  echo 'negative population-authority mutation unexpectedly passed' >&2
  exit 1
fi
echo 'selected-target-manifest-review-smoke: PASS'
