#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
"$ROOT/tools/docs/check-selected-provider-local-supply-map-production-owner-decision-boundary-acceptance"
grep -Fq 'local_supply_map_production_remaining_transaction_count: 1' "$ROOT/docs/current/STATE.yaml"
grep -Fq 'target_population_authorized: false' "$ROOT/docs/current/STATE.yaml"
grep -Fq 'Task ID: `review-and-accept-selected-provider-local-supply-map-production-boundary`' "$ROOT/docs/current/ACTIVE_TASK.md"
echo 'local-supply map production owner decision acceptance smoke: PASS'
