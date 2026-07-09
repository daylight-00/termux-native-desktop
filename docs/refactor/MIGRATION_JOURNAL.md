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

## 2026-07-09 — Deploy smoke validation

### Faults found before live use

A repository-level smoke test reproduced the legacy live layout and found two deploy implementation bugs before device migration:

1. Bash function variables such as `dst` were global, so `link_leaf` lost its destination after calling `ensure_dir`.
2. dry-run needed to tolerate targets visible only through a legacy directory symlink that would be converted during real deployment.

### Fix

- all function-scoped variables are declared `local`;
- `has_symlink_ancestor` distinguishes dry-run legacy-view leaves from unmanaged direct targets;
- the Mesa `patches/mesa` compatibility path handles the same simulated legacy-parent case.

### Validation

Local repository-level test:

```text
tests/repository/deploy-smoke.sh
deploy smoke test: PASS
```

The test verifies:

- dry-run does not mutate legacy links;
- real deployment converts legacy directory symlinks to target directories;
- module leaf links are installed;
- package launchers are installed at their public entry points;
- Mesa maintenance compatibility links are installed;
- obsolete experiment `diag` symlink is removed without deleting a real directory.

## 2026-07-09 — Recorded branch commits

The refactor branch history at this point is:

```text
2211dde643ccb8db1971cc7f179a500502b7c709
    docs: establish refactor source of truth

be7802558e8b55a428abb2bf76e6041ed08e8e80
    repo: split modules packages and experiment recipes

636533cf9ab9ee27ae2d3c16d262a370751a2c0d
    test: harden deploy migration path

00638d56297b1ce9d9b87499497649805b4ce2df
    docs: align integrated guides with new owners

9401429a22a5dfb887fbf89f6fcf9be370b9dfbb
    docs: align canonical experiment records with promoted owners
```

### Current state

- repository ownership paths are split;
- deploy migration has a passing repository-level smoke test;
- integrated guides use current owner paths;
- canonical experiment README files use current promoted paths;
- historical reports remain unchanged;
- live device migration has not yet been run;
- `uv-base` module promotion is pending capture of the live project definition and lock identity.
