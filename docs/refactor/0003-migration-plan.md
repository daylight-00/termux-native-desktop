# 0003 — Migration Plan

## Safety rule

Repository ownership migration and live generated-state cleanup are separate operations.

No initial refactor commit deletes:

- `$HOME/gl/apps/*`;
- `$HOME/gl/opt/*`;
- `$HOME/gl/build/mesa/*`;
- experimental Mesa install prefixes;
- custom CPython installation;
- `uv-base/.venv`;
- the CPython artifact archive.

## Repository commit sequence

### Phase 1 — document refactor baseline

Add low-level inventory, ownership map, migration plan, journal, and machine-readable path map.

No runtime path changes.

### Phase 2 — move existing promoted ownership

Move existing blobs:

- session files into `modules/desktop`;
- generic gl runtime files into `modules/gl`;
- application launchers into package-owned launcher directories;
- Mesa build definitions into `packages/mesa-glibc`;
- bisect judges into the SIGBUS experiment recipe directory.

Rewrite `tools/deploy` for new paths and add repository-level deployment smoke tests.

### Phase 3 — promote shell, uv-base, and CPython consumer contract

After live identity capture:

- add thin `.bashrc` source;
- add generic shell fragments;
- add gl and uv-base capability fragments;
- add exact `uv-base/pyproject.toml` and `uv.lock`;
- add sync/reset/validation contracts;
- record CPython artifact identity and installed runtime validation;
- add hash-guarded one-time adoption tooling;
- test PATH ordering and adoption behavior in temporary homes.

## Live migration order

Live migration is deliberately split into two operations.

### A. Adopt pre-existing personal files

```bash
tools/adopt-user-env --dry-run
tools/adopt-user-env --apply
```

This operation:

1. verifies exact SHA-256 identities for the legacy `.bashrc`, `.uvrc`, `pyproject.toml`, and `uv.lock`;
2. creates backups under `$XDG_STATE_HOME` or `$HOME/.local/state`;
3. replaces `.bashrc`, `pyproject.toml`, and `uv.lock` with repository-owned links;
4. retires `.uvrc` after backup;
5. links Bash fragments required for a functional new interactive shell.

It does **not** migrate the gl live tree and does not delete `.venv` or the CPython archive.

### B. Deploy modules and package entry points

```bash
tools/deploy --dry-run
tools/deploy
```

Then verify:

1. all live links resolve to new module/package paths;
2. a new interactive shell has PATH order `gl/bin > uv-base/.venv/bin > .local/bin > system`;
3. `VIRTUAL_ENV` is not globally exported by uv-base integration;
4. `python` resolves to the uv-base environment when `.venv` exists;
5. `startxfce-x11` resolves correctly;
6. `gl-run` and `gl-farm` source paths resolve without running destructive maintenance;
7. application launchers resolve;
8. CPython artifact and installed-runtime tests pass;
9. uv-base definition and runtime tests pass.

## Rollback

The adoption backup root is:

```text
${XDG_STATE_HOME:-$HOME/.local/state}/termux-native-desktop/adoption/pre-module-layout
```

Rollback should be explicit:

1. close newly started interactive shells;
2. remove adopted symlinks for `.bashrc`, uv-base definition files, and Bash fragments;
3. restore backed-up files with metadata preserved;
4. switch the repository checkout to `main`;
5. run the legacy deploy script from `main` if gl live links were already migrated.

The CPython installation, uv-base `.venv`, application payloads, Mesa prefixes, and build work remain untouched by adoption and therefore require no rollback in this phase.
