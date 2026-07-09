#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
REPO="$T/repo"
HOME_TEST="$T/home"
mkdir -p "$REPO" "$HOME_TEST/uv-base"

cp -a "$SOURCE_ROOT/modules" "$REPO/modules"
mkdir -p "$REPO/tools"
cp "$SOURCE_ROOT/tools/adopt-user-env" "$REPO/tools/adopt-user-env"
chmod +x "$REPO/tools/adopt-user-env"

cat > "$HOME_TEST/.bashrc" <<'OLD_BASHRC'
case $- in
    *i*) ;;
      *) return;;
esac
HISTCONTROL=ignoreboth
shopt -s histappend
HISTSIZE=1000
HISTFILESIZE=2000
shopt -s checkwinsize

PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
PS1="\[\e]0;\u@\h: \w\a\]$PS1"

[ -f ~/miniforge3/etc/profile.d/conda.sh ] && \
    . ~/miniforge3/etc/profile.d/conda.sh

alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

alias dush='du ./* -sh'
alias con='conda activate venv'

source $HOME/uv-base/.uvrc

# gl layer commands first; upstream per-user tools second.
case ":$PATH:" in
  *":$HOME/gl/bin:"*) ;;
  *) PATH="$HOME/gl/bin:$PATH" ;;
esac

case ":$PATH:" in
  *":$HOME/.local/bin:"*) ;;
  *) PATH="$HOME/.local/bin:$PATH" ;;
esac

# Ensure gl wrappers take precedence over upstream registered binaries.
PATH="$HOME/gl/bin:$HOME/.local/bin:$(printf '%s' "$PATH" | \
  tr ':' '\n' | \
  grep -v -Fx "$HOME/gl/bin" | \
  grep -v -Fx "$HOME/.local/bin" | \
  paste -sd ':' -)"

export PATH
OLD_BASHRC

expected_bashrc_sha=3c7b8682c4debff14f68fa2a239635aed7d13ec6c11918ddee8f59040245a7cf
fixture_bashrc_sha=$(sha256sum "$HOME_TEST/.bashrc" | awk '{print $1}')
[ "$fixture_bashrc_sha" = "$expected_bashrc_sha" ] || {
    echo "legacy .bashrc fixture drift" >&2
    echo "expected: $expected_bashrc_sha" >&2
    echo "actual:   $fixture_bashrc_sha" >&2
    exit 1
}

printf 'fixture uvrc for adoption smoke test\n' > "$HOME_TEST/uv-base/.uvrc"
cp "$REPO/modules/uv-base/overlay/home/uv-base/pyproject.toml" "$HOME_TEST/uv-base/pyproject.toml"
cp "$REPO/modules/uv-base/overlay/home/uv-base/uv.lock" "$HOME_TEST/uv-base/uv.lock"

fixture_uvrc_sha=$(sha256sum "$HOME_TEST/uv-base/.uvrc" | awk '{print $1}')
sed -i "s/f851fe1147541c2f6040c5cce66852ba3d848f70b62ef3e843c8e41339a4641c/$fixture_uvrc_sha/" "$REPO/tools/adopt-user-env"

HOME="$HOME_TEST" bash "$REPO/tools/adopt-user-env" --dry-run >"$T/dry.log"
[ ! -L "$HOME_TEST/.bashrc" ]
[ -f "$HOME_TEST/uv-base/.uvrc" ]

HOME="$HOME_TEST" bash "$REPO/tools/adopt-user-env" --apply >"$T/apply.log"
[ -L "$HOME_TEST/.bashrc" ]
[ -L "$HOME_TEST/uv-base/pyproject.toml" ]
[ -L "$HOME_TEST/uv-base/uv.lock" ]
[ ! -e "$HOME_TEST/uv-base/.uvrc" ]
[ -f "$HOME_TEST/.local/state/termux-native-desktop/adoption/pre-module-layout/home/.bashrc" ]
[ -f "$HOME_TEST/.local/state/termux-native-desktop/adoption/pre-module-layout/home/uv-base/.uvrc" ]
[ -L "$HOME_TEST/.config/bash/conf.d/40-gl.sh" ]
[ -L "$HOME_TEST/.config/bash/conf.d/60-uv-base.sh" ]
[ -L "$HOME_TEST/.config/bash/conf.d/99-path-policy.sh" ]

HOME_BAD="$T/home-bad"
mkdir -p "$HOME_BAD/uv-base"
printf 'modified\n' > "$HOME_BAD/.bashrc"
printf 'fixture uvrc for adoption smoke test\n' > "$HOME_BAD/uv-base/.uvrc"
cp "$REPO/modules/uv-base/overlay/home/uv-base/pyproject.toml" "$HOME_BAD/uv-base/pyproject.toml"
cp "$REPO/modules/uv-base/overlay/home/uv-base/uv.lock" "$HOME_BAD/uv-base/uv.lock"
if HOME="$HOME_BAD" bash "$REPO/tools/adopt-user-env" --apply >"$T/bad.log" 2>&1; then
    echo 'modified file was incorrectly adopted' >&2
    exit 1
fi

printf 'adopt user env smoke test: PASS\n'
