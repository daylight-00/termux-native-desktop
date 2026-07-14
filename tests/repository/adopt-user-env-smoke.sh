#!/usr/bin/env bash
set -euo pipefail
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/repo/tools"
cp "$(cd "$(dirname "$0")/../.." && pwd)/tools/adopt-user-env" "$T/repo/tools/adopt-user-env"
cat >"$T/repo/tools/deploy" <<'STUB'
#!/usr/bin/env bash
printf '%s\n' "$*"
STUB
chmod +x "$T/repo/tools/adopt-user-env" "$T/repo/tools/deploy"
[ "$(bash "$T/repo/tools/adopt-user-env" --dry-run)" = '--dry-run --profile full' ]
[ "$(bash "$T/repo/tools/adopt-user-env" --apply)" = '--apply --profile full' ]
if bash "$T/repo/tools/adopt-user-env" --bad >/dev/null 2>&1; then
  echo 'bad argument was accepted' >&2
  exit 1
fi
printf 'adopt user env smoke test: PASS\n'
