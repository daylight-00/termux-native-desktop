#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
bash "$ROOT/tools/docs/check-libselinux-direct-consumer-necessity-review"
