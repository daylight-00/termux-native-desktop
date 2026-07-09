# 0004 — Shell and uv-base Adoption Contract

## Purpose

This document records the one-time migration from pre-refactor personal files into repository-owned shell and uv-base module state.

The migration is intentionally narrower than full deployment.

## Observed legacy state

### `.bashrc`

Observed SHA-256:

```text
3c7b8682c4debff14f68fa2a239635aed7d13ec6c11918ddee8f59040245a7cf
```

The legacy file combined:

- interactive-shell guards and history policy;
- prompt and terminal title;
- aliases;
- a stale `~/miniforge3` Conda source line;
- `~/uv-base/.uvrc` sourcing;
- gl and `.local/bin` PATH manipulation.

Live inspection established:

```text
command -v conda: no result
$HOME/miniforge3: absent
```

Therefore the old Conda source line is not preserved. This does not remove the validated glibc Miniforge work recorded under `experiments/glibc/miniforge-conda/`; that work used a separate glibc runtime boundary and prefix.

### `.uvrc`

Observed SHA-256:

```text
f851fe1147541c2f6040c5cce66852ba3d848f70b62ef3e843c8e41339a4641c
```

Its responsibilities were shell integration:

- custom CPython selection;
- uv Python-download policy;
- base project path;
- base `.venv` PATH exposure;
- `uva`, `uvr`, and `uvs` helper functions.

These responsibilities move to `60-uv-base.sh`. The legacy global relative `VIRTUAL_ENV=.venv` behavior is not preserved.

### uv-base project definition

Exact tracked identity:

```text
pyproject.toml SHA-256
2b89a3855976ca27d81f7bda0c42b7880b52e6b74fae41c83982d115576b4355

uv.lock SHA-256
79dab5fa4e9246ccfd72c28d569400013858723730f599a15ef6e6f566635a53
```

Current dependency set is empty. That is valid baseline state, not missing configuration.

## New ownership

```text
modules/shell/
    .bashrc
    generic shell fragments
    final PATH policy

modules/gl/
    40-gl.sh

modules/uv-base/
    60-uv-base.sh
    pyproject.toml
    uv.lock
    sync/reset hooks
    validation tests

packages/cpython-android-runtime/
    interpreter artifact/runtime consumer identity
```

## PATH composition

Final interactive order:

```text
$HOME/gl/bin
    >
$HOME/uv-base/.venv/bin
    >
$HOME/.local/bin
    >
remaining system PATH
```

Capability fragments declare their own variables and helpers. `99-path-policy.sh` performs the final cross-capability composition and de-duplicates managed entries.

## Adoption safety

`tools/adopt-user-env` defaults to dry-run.

`--apply` proceeds only when the four legacy files match the captured hashes. Modified files are refused rather than overwritten.

Backups are written before replacement to:

```text
${XDG_STATE_HOME:-$HOME/.local/state}/termux-native-desktop/adoption/pre-module-layout/
```

The tool is idempotent for already adopted symlinks and an already retired `.uvrc`.

## Explicit non-actions

The adoption tool does not:

- delete or recreate `$HOME/uv-base/.venv`;
- move or delete the CPython archive;
- modify `$HOME/opt/cpython-3.14/prefix`;
- migrate `$HOME/gl` directory symlinks;
- rebuild `gl-farm`;
- switch Mesa prefixes;
- activate or install Conda.

These boundaries keep user-environment adoption independent from runtime deployment and experimental cleanup.

## Repository-level validation

Two smoke tests cover the migration logic:

```text
tests/repository/shell-layout-smoke.sh
    verifies fragment composition, helper availability,
    absence of global VIRTUAL_ENV, and PATH precedence

tests/repository/adopt-user-env-smoke.sh
    verifies dry-run non-mutation, backups, adoption links,
    .uvrc retirement, and modified-file refusal
```
