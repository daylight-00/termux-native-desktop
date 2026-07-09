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

## 2026-07-09 — Ownership move preparation

### Additional classification

- `setup/mesa/diag/bisect-test.sh` and `bisect-test-full.sh` are explicit `git bisect` judges and move to the SIGBUS experiment `recipe/` directory.
- `setup/glibc/bin/code` is VS Code-specific and moves to `packages/vscode/launcher/`.
- `setup/glibc/bin/obsidian*` are Obsidian-specific and move to `packages/obsidian/launcher/`.
- generic `gl/bin` retains only layer commands (`gl-run`, `gl-farm`) in this batch.
- Mesa patch path retains the nested `patches/mesa/` shape because the promoted build script currently reads `$HOME/gl/build/patches/mesa`.

### Deploy rewrite contract

`tools/deploy` follows these rules:

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

4ab6703ba43f566bd27d37e9efd45355c4f0164b
    docs: define module and package owner contracts

5d241dc8ce401c7f95a6a0c8f5324f1686337c73
    connector file-update commit adding the CPython owner entry to packages/README.md

fa63b263c3fab871f895cc3ad742aad3c65e0ef7
    connector file-update commit adding the CPython package README
```

### Connector write-order incidents

Two contents-API writes advanced the branch while separately created Git-tree commit objects remained unattached. The unattached objects were not merged or force-applied. Recovery strategy: use the actual branch tip as the base for the next Git tree, add the missing CPython package files and journal updates there, and continue without force-rewriting history.

New guard procedure for all subsequent writes:

1. fetch or otherwise resolve the current branch tip;
2. build the next tree from that exact tip;
3. create one commit with that tip as parent;
4. call `update_ref` explicitly;
5. compare branch against `main` before the next write.

## 2026-07-09 — CPython consumer identity capture

Live input established:

```text
artifact: cpython-3.14-aarch64-linux-android-for-uv.tar.gz
SHA-256:  7083ad89661d73278c2165dfff7506a6de26c8ec9471d6621a5c06c3aa9a49be
visible size: 22 MiB
installed Python: 3.14.6
program interpreter: /system/bin/linker64
install prefix: $HOME/opt/cpython-3.14/prefix
```

Decision:

- do not commit the runtime archive;
- record its consumer-side identity under `packages/cpython-android-runtime/`;
- validate the transferred archive by SHA-256;
- validate the installed runtime by Python version and ELF interpreter;
- keep the producer/build history in `daylight-00/cpython-android-cli`;
- let `uv-base` consume the installed runtime rather than own the archive.

### Current state

- repository ownership paths are split;
- deploy migration has a passing repository-level smoke test;
- integrated guides and canonical experiment READMEs use current owner paths;
- historical reports remain unchanged;
- CPython consumer contract is represented as a package owner;
- live device migration has not yet been run;
- `uv-base` module promotion is pending exact `uv.lock` content plus shell/Conda live-status guards.
