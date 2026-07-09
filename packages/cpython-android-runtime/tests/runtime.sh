#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

PY=${PYBIN:-$HOME/opt/cpython-3.14/prefix/bin/python3.14}
[ -x "$PY" ] || { echo "missing runtime: $PY" >&2; exit 1; }

version=$($PY --version 2>&1)
[ "$version" = "Python 3.14.6" ] || {
  echo "unexpected version: $version" >&2
  exit 1
}

interp=$(readelf -l "$PY" | sed -n 's/.*Requesting program interpreter: \(.*\)]/\1/p')
[ "$interp" = "/system/bin/linker64" ] || {
  echo "unexpected interpreter: $interp" >&2
  exit 1
}

printf 'cpython runtime validation: PASS\n'
