#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
CHECK="$ROOT/tools/docs/check-selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-review"
SOURCE="$ROOT/experiments/glibc/selected-obsidian-provider-authority/implementation/selected_provider_local_supply_evidence_live_input_adapter_execution_authorization_candidate.py"
FIXTURE="$ROOT/experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-live-input-adapter-execution-authorization-implementation-synthetic-fixture.json"
TMP_ROOT=${TMPDIR:-"$ROOT/.tmp"}
mkdir -p "$TMP_ROOT"
SMOKE_JSON=$(mktemp "$TMP_ROOT/lsliae-rewrite-smoke.XXXXXX.json")
trap 'rm -f "$SMOKE_JSON"' EXIT

python3 "$CHECK"
python3 "$SOURCE" --repo-root "$ROOT" --fixture "$FIXTURE" --case success >/dev/null
set +e
python3 "$SOURCE" --repo-root "$ROOT" --fixture "$FIXTURE" --case synthetic-rewrite-detected >"$SMOKE_JSON"
rc=$?
set -e
[ "$rc" -eq 2 ]
python3 - "$SMOKE_JSON" <<'PY'
import json
import sys
from pathlib import Path
r = json.loads(Path(sys.argv[1]).read_text())
assert r['failure_id'] == 'LSLIAE-FAIL-016'
assert r['current_provider_read_count'] == 0
assert r['current_write_count'] == 0
assert r['current_live_authority_count'] == 0
assert r['provider_paths_opened'] == []
assert r['writes_performed'] == []
PY
