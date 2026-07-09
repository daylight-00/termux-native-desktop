#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
HOME_TEST="$T/home"
BASH_BIN=$(command -v bash)

mkdir -p "$HOME_TEST/.config/bash/conf.d" "$HOME_TEST/gl/bin" "$HOME_TEST/uv-base/.venv/bin" "$HOME_TEST/.local/bin"

cp "$ROOT/modules/shell/overlay/home/.bashrc" "$HOME_TEST/.bashrc"
cp "$ROOT/modules/shell/overlay/home/.config/bash/interactive.sh" "$HOME_TEST/.config/bash/interactive.sh"
cp "$ROOT/modules/shell/overlay/home/.config/bash/prompt.sh" "$HOME_TEST/.config/bash/prompt.sh"
cp "$ROOT/modules/shell/overlay/home/.config/bash/aliases.sh" "$HOME_TEST/.config/bash/aliases.sh"
cp "$ROOT/modules/gl/overlay/home/.config/bash/conf.d/40-gl.sh" "$HOME_TEST/.config/bash/conf.d/40-gl.sh"
cp "$ROOT/modules/uv-base/overlay/home/.config/bash/conf.d/60-uv-base.sh" "$HOME_TEST/.config/bash/conf.d/60-uv-base.sh"
cp "$ROOT/modules/shell/overlay/home/.config/bash/conf.d/99-path-policy.sh" "$HOME_TEST/.config/bash/conf.d/99-path-policy.sh"

if ! out=$(HOME="$HOME_TEST" PATH="/usr/bin:/bin:$HOME_TEST/.local/bin:/usr/bin" "$BASH_BIN" --noprofile --norc -ic '
    unset VIRTUAL_ENV
    . "$HOME/.bashrc"
    printf "PATH=%s\n" "$PATH"
    printf "UV_BASE=%s\n" "$UV_BASE"
    printf "PYBIN=%s\n" "$PYBIN"
    type uva >/dev/null
    type uvr >/dev/null
    type uvs >/dev/null
    test -z "${VIRTUAL_ENV+x}"
' 2>"$T/shell.err"); then
    cat "$T/shell.err" >&2
    exit 1
fi

expected_prefix="$HOME_TEST/gl/bin:$HOME_TEST/uv-base/.venv/bin:$HOME_TEST/.local/bin:"
case "$out" in
    *"PATH=$expected_prefix"*) ;;
    *) printf '%s\n' "$out" >&2; echo 'PATH precedence mismatch' >&2; exit 1 ;;
esac
case "$out" in *"UV_BASE=$HOME_TEST/uv-base"*) ;; *) exit 1;; esac
case "$out" in *"PYBIN=$HOME_TEST/opt/cpython-3.14/prefix/bin/python3.14"*) ;; *) exit 1;; esac

printf 'shell layout smoke test: PASS\n'
