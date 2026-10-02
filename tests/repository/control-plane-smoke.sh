#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)

bash "$ROOT/tools/docs/check-control-plane"

printf 'control-plane smoke: PASS\n'
