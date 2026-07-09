# 0003 — Migration Plan

## Safety rule

Repository ownership migration and live generated-state cleanup are separate operations.

No initial refactor commit deletes:

- `$HOME/gl/apps/*`;
- `$HOME/gl/opt/*`;
- `$HOME/gl/build/mesa/*`;
- experimental Mesa install prefixes;
- custom CPython installation;
- `uv-base/.venv`.

## Commit sequence

### Commit 1 — document refactor baseline

Add:

- `docs/design/` architecture set;
- `docs/refactor/` inventory, ownership map, plan, journal, and machine-readable path map.

No runtime path changes.

### Commit 2 — move ownership without behavior change

Move existing blobs:

- session files into `modules/desktop`;
- generic gl runtime files into `modules/gl`;
- application launchers into package-owned launcher directories;
- Mesa build definitions into `packages/mesa-glibc`;
- bisect judges into the SIGBUS experiment recipe directory.

Rewrite `tools/deploy` for new paths.

Delete legacy `setup/` and `scripts/deploy-gl.sh` entries in the same Git tree commit so repository HEAD never has ambiguous duplicate owners.

### Commit 3 — add shell and uv-base module

After live uv-base definition capture:

- add thin `.bashrc` source;
- add generic shell fragments;
- add `60-uv-base.sh`;
- add `uv-base/pyproject.toml` and `uv.lock`;
- add sync/reset/validation contract;
- document CPython artifact consumer boundary.

### Live migration

On device, after pulling the refactor branch:

1. run `tools/deploy --dry-run`;
2. inspect target replacements;
3. run `tools/deploy`;
4. verify all live links resolve to new module/package paths;
5. validate shell syntax without replacing the active shell session;
6. validate `startxfce-x11` command resolution;
7. validate `gl-run`, `gl-farm` source resolution without destructive farm rebuild unless explicitly chosen;
8. validate application launcher resolution;
9. migrate uv-base shell integration only after the tracked project definition is present.

## Rollback

Repository rollback:

```bash
git switch main
```

Live link rollback before legacy paths are removed from the local main checkout:

```bash
git -C "$HOME/termux-native-desktop" switch main
bash "$HOME/termux-native-desktop/scripts/deploy-gl.sh"
```

The legacy deploy path remains available on `main` until the refactor branch is merged.
