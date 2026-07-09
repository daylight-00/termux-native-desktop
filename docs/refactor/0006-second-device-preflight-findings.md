# 0006 — Second Device Preflight Findings

## Context

After syncing commit `154fd95`, the device reran repository smoke tests and both migration dry-runs.

Observed results:

```text
deploy smoke test: PASS
adopt user env smoke test: PASS
uv-base definition validation: PASS
cpython artifact validation: PASS
cpython runtime validation: PASS
```

Two further issues were found before any live mutation.

## Finding 1 — Termux test portability

`tests/repository/shell-layout-smoke.sh` replaced `PATH` with a Linux-style fixture value and then invoked `bash` by name. On Termux, Bash is installed under `$PREFIX/bin`, not `/usr/bin`, so the test failed with:

```text
bash: command not found
```

### Fix

Resolve the real Bash executable before replacing PATH:

```text
BASH_BIN=$(command -v bash)
```

Then invoke the child shell through that absolute path.

The fixture PATH remains intentionally synthetic so command-precedence behavior can still be tested independently.

## Finding 2 — adoption/deploy phase overlap

`tools/deploy --dry-run` attempted to deploy all module overlays, including `shell` and `uv-base`.

Before adoption, `$HOME/.bashrc`, `$HOME/uv-base/pyproject.toml`, and `$HOME/uv-base/uv.lock` are still real files. The generic deploy tool correctly refuses to replace such unmanaged real files, so dry-run stopped at:

```text
refusing to replace unmanaged target: $HOME/.bashrc
```

This exposed an architectural overlap between two migration phases.

### Decision

Keep personal-file adoption and runtime deployment separate:

```text
tools/adopt-user-env
    owns one-time shell + uv-base adoption
    exact hash verification
    backup
    personal-file relinking
    .uvrc retirement

tools/deploy
    owns runtime-facing deployment
    desktop module
    gl module
    package public entry points
    Mesa maintenance compatibility links
```

Because adopted shell and uv-base files are symlinks directly into the repository, normal repository updates do not require `tools/deploy` to relink them on every run.

## Finding 3 — dry-run repeated symlink conversion output

The dry-run repeatedly printed conversion of the same legacy directory symlink for every leaf below it, for example `gl/bin` and `gl/toolchain`.

Real deployment would convert each directory only once. The repeated output was a simulation-state defect.

### Fix

`tools/deploy` now records directories that dry-run has already planned as materialized. Later leaves reuse that planned state rather than printing duplicate conversion operations.

## Safety conclusion

No live files were changed during either preflight run.

The second preflight demonstrated the value of separating:

```text
repository-level tests
    -> identity validation
    -> adoption dry-run
    -> deployment dry-run
    -> apply only after review
```

## Required revalidation

After syncing the fix commit, rerun:

```bash
bash tests/repository/deploy-smoke.sh
bash tests/repository/shell-layout-smoke.sh
bash tests/repository/adopt-user-env-smoke.sh

./tools/adopt-user-env --dry-run
./tools/deploy --dry-run
```

Expected repository test results:

```text
deploy smoke test: PASS
shell layout smoke test: PASS
adopt user env smoke test: PASS
```

The deployment dry-run must complete without touching `.bashrc` or the uv-base definition files.
