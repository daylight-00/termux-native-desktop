# 0009 — Phase A User-Environment Adoption Passed

## Context

After the pre-apply gate passed, the real Termux device executed:

```text
tools/adopt-user-env --apply
```

The operation completed successfully.

## Adopted topology

```text
$HOME/.bashrc
    -> $HOME/termux-native-desktop/modules/shell/overlay/home/.bashrc

$HOME/uv-base/pyproject.toml
    -> $HOME/termux-native-desktop/modules/uv-base/overlay/home/uv-base/pyproject.toml

$HOME/uv-base/uv.lock
    -> $HOME/termux-native-desktop/modules/uv-base/overlay/home/uv-base/uv.lock

$HOME/uv-base/.uvrc
    retired after backup
```

Shell fragments were linked under:

```text
$HOME/.config/bash/
$HOME/.config/bash/conf.d/
```

with owners split across the shell, gl, and uv-base modules.

## Backup verification

Backups were created under:

```text
$HOME/.local/state/termux-native-desktop/adoption/pre-module-layout/
```

Verified SHA-256 values:

```text
legacy .bashrc
3c7b8682c4debff14f68fa2a239635aed7d13ec6c11918ddee8f59040245a7cf

legacy uv-base pyproject.toml
2b89a3855976ca27d81f7bda0c42b7880b52e6b74fae41c83982d115576b4355

legacy uv-base uv.lock
79dab5fa4e9246ccfd72c28d569400013858723730f599a15ef6e6f566635a53

legacy .uvrc
f851fe1147541c2f6040c5cce66852ba3d848f70b62ef3e843c8e41339a4641c
```

These match the identities captured before migration.

## uv-base validation

The live tracked definition passed:

```text
uv-base definition validation: PASS
```

The existing generated environment also passed:

```text
uv-base runtime validation: PASS
```

The environment continued to provide:

```text
Python 3.14.6
```

## Clean child-shell validation

A clean child Bash removed inherited legacy variables before sourcing the promoted `.bashrc`.

Observed environment:

```text
PATH=$HOME/gl/bin:$HOME/uv-base/.venv/bin:$HOME/.local/bin:$PREFIX/bin
PYBIN=$HOME/opt/cpython-3.14/prefix/bin/python3.14
UV_BASE=$HOME/uv-base
python=$HOME/uv-base/.venv/bin/python
```

Validated behavior:

```text
PATH precedence: PASS
default Python resolution: PASS
VIRTUAL_ENV global export: absent
```

The shell helpers were present as functions:

```text
uva
uvr
uvs
```

## Result

Phase A passed completely.

The personal shell and uv-base definition are now repository-owned while the generated `.venv` remains live disposable state.

The stale `~/miniforge3` auto-source behavior and global relative `VIRTUAL_ENV=.venv` behavior are no longer part of the promoted shell configuration.

## Next phase

Proceed to Phase B only:

```text
tools/deploy
    -> convert legacy gl directory symlinks
    -> install module-owned leaf links
    -> install package-owned public entry points
    -> preserve Mesa maintenance compatibility links
    -> remove obsolete live experiment diag symlink
```

Phase B validation must check topology and command resolution before launching heavyweight GUI workloads.
