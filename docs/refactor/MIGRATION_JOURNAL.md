# Migration Journal

## 2026-07-09 — Refactor initialization

### Input state

- user local checkout clean: `## main...origin/main`;
- remote base commit: `3cf41d6fc47050b06e18e956a23cefe25e4fb82a`;
- refactor branch created: `refactor/module-package-layout`;
- container network `git clone` attempt failed because `github.com` DNS could not be resolved;
- authenticated GitHub connector selected for repository reads and Git tree/commit writes;
- local working mirror created at `/mnt/data/tnd-refactor` for design documents, mapping data, generated migration material, and validation records.

### Decisions confirmed

- `startxfce-x11` -> desktop module;
- `gl/env`, `gl-run`, `gl-farm`, shim, glibc target wrappers -> gl module;
- VS Code and Obsidian launchers -> package owners;
- Mesa build definition -> Mesa package;
- Mesa bisect judges -> SIGBUS experiment recipe;
- deploy helper -> repository tool;
- no live build/install prefix cleanup in the ownership refactor.

### Pending input

Requested from device:

```text
~/uv-base/pyproject.toml content
~/uv-base/uv.lock size and SHA-256
```

### Next action

Create documentation commit, then create one grouped ownership-move commit using Git tree operations with existing blob SHAs.

## 2026-07-09 — Ownership move preparation

### Additional classification

- `setup/mesa/diag/bisect-test.sh` and `bisect-test-full.sh` are explicit `git bisect` judges and will move to the SIGBUS experiment `recipe/` directory.
- `setup/glibc/bin/code` is VS Code-specific and moves to `packages/vscode/launcher/`.
- `setup/glibc/bin/obsidian*` are Obsidian-specific and move to `packages/obsidian/launcher/`.
- generic `gl/bin` retains only layer commands (`gl-run`, `gl-farm`) in this batch.
- Mesa patch path retains the nested `patches/mesa/` shape because the promoted build script currently reads `$HOME/gl/build/patches/mesa`.

### Deploy rewrite contract

`tools/deploy` is prepared with these rules:

1. resolve repository root from the tool location rather than hard-coding `$HOME/termux-native-desktop`;
2. support `--dry-run`;
3. deploy module overlays as leaf symlinks;
4. convert legacy directory symlinks such as `~/gl/bin` into real target directories before leaf deployment;
5. refuse to overwrite unmanaged real files;
6. install application-specific public launchers from package owners;
7. preserve Mesa live build compatibility paths without keeping experiment bisect harnesses in `~/gl/build/diag`;
8. remove only obsolete symlinks, never real directories.
