# Migration Journal

## 2026-07-09 — Refactor initialization

### Input state

- user local checkout clean: `## main...origin/main`;
- remote base commit: `3cf41d6fc47050b06e18e956a23cefe25e4fb82a`;
- refactor branch created: `refactor/module-package-layout`;
- container network `git clone` attempt failed because `github.com` DNS could not be resolved;
- authenticated GitHub connector selected for repository reads and Git tree/commit writes;
- local working mirrors under `/mnt/data/` store design documents, path maps, candidate files, and validation records.

### Decisions confirmed

- `startxfce-x11` -> desktop module;
- `gl/env`, `gl-run`, `gl-farm`, shim, glibc target wrappers -> gl module;
- VS Code and Obsidian launchers -> package owners;
- Mesa build definition -> Mesa package;
- Mesa bisect judges -> SIGBUS experiment recipe;
- deploy helper -> repository tool;
- no live build/install prefix cleanup in the ownership refactor.

## 2026-07-09 — Ownership move preparation

- `setup/mesa/diag/bisect-test*.sh` are explicit `git bisect` judges and move to the SIGBUS experiment `recipe/` directory.
- `setup/glibc/bin/code` is VS Code-specific and moves to `packages/vscode/launcher/`.
- `setup/glibc/bin/obsidian*` are Obsidian-specific and move to `packages/obsidian/launcher/`.
- generic `gl/bin` retains only layer commands (`gl-run`, `gl-farm`) in the first ownership batch.
- Mesa patch path retains the nested `patches/mesa/` shape because the promoted build script currently reads `$HOME/gl/build/patches/mesa`.

## 2026-07-09 — Deploy rewrite and smoke validation

`tools/deploy` follows these rules:

1. resolve repository root from tool location;
2. support `--dry-run`;
3. deploy module overlays as leaf symlinks;
4. convert legacy directory symlinks before leaf deployment;
5. refuse unmanaged real-file replacement;
6. install application-specific public launchers from package owners;
7. preserve Mesa live build compatibility paths;
8. remove only obsolete symlinks, never real directories.

A temporary-home smoke test reproduced the legacy live layout and found two implementation faults before device migration:

1. Bash function variables such as `dst` were global, so `link_leaf` lost its destination after calling `ensure_dir`.
2. dry-run needed to tolerate targets visible only through a legacy directory symlink that real deployment would convert first.

Fixes:

- function variables declared `local`;
- `has_symlink_ancestor` distinguishes dry-run legacy-view leaves;
- Mesa `patches/mesa` compatibility path handles the same case.

Validation:

```text
tests/repository/deploy-smoke.sh
deploy smoke test: PASS
```

## 2026-07-09 — CPython consumer identity capture

Live input established:

```text
artifact: cpython-3.14-aarch64-linux-android-for-uv.tar.gz
size: 22474527 bytes
SHA-256: 7083ad89661d73278c2165dfff7506a6de26c8ec9471d6621a5c06c3aa9a49be
installed Python: 3.14.6
program interpreter: /system/bin/linker64
install prefix: $HOME/opt/cpython-3.14/prefix
```

Decision:

- do not commit the runtime archive;
- record consumer-side identity under `packages/cpython-android-runtime/`;
- validate archive SHA-256 and installed runtime identity;
- keep producer/build history in `daylight-00/cpython-android-cli`;
- let `uv-base` consume the installed runtime rather than own the archive.

## 2026-07-09 — uv-base and shell identity capture

Device input established:

```text
uv-base pyproject SHA-256:
2b89a3855976ca27d81f7bda0c42b7880b52e6b74fae41c83982d115576b4355

uv-base lock SHA-256:
79dab5fa4e9246ccfd72c28d569400013858723730f599a15ef6e6f566635a53

legacy .bashrc SHA-256:
3c7b8682c4debff14f68fa2a239635aed7d13ec6c11918ddee8f59040245a7cf

legacy .uvrc SHA-256:
f851fe1147541c2f6040c5cce66852ba3d848f70b62ef3e843c8e41339a4641c
```

Conda live-status inspection:

```text
command -v conda: no result
$HOME/miniforge3: absent
```

Decision:

- remove the stale `~/miniforge3/etc/profile.d/conda.sh` source line from the promoted shell model;
- do not reinterpret this as removal of the separate validated glibc Miniforge experiment;
- promote exact uv-base project and lock state;
- retire `.uvrc` after backup and move its responsibilities into module-owned Bash integration;
- do not globally export `VIRTUAL_ENV`;
- enforce final command precedence as `gl/bin > uv-base/.venv/bin > .local/bin > remaining PATH`.

### Local mirror validation

```text
shell layout smoke test: PASS
adopt user env smoke test: PASS
```

The candidate project files reproduced the device identities exactly.

`tools/adopt-user-env` defaults to dry-run and performs only the personal shell/uv-base ownership transition. It does not invoke full `tools/deploy`, delete `.venv`, move the CPython archive, or alter gl/Mesa runtime state.

## 2026-07-09 — Connector write-order incidents and recovery

Several GitHub contents-API writes advanced the branch while separately created Git-tree commit objects remained unattached. No force rewrite was used.

Observed classes:

- CPython owner entry and package README were committed separately before the grouped package tree was attached;
- shell module README and shell/uv-base adoption document were committed separately before the validated full source tree was attached;
- several intermediate grouped commit objects were created but never became branch ancestors.

Recovery policy:

1. treat the actual branch tip as authoritative;
2. rebuild the intended complete tree on top of that exact tip;
3. create a new commit with that tip as parent;
4. load and call `update_ref` explicitly;
5. compare `main...refactor/module-package-layout` after each grouped phase;
6. document the incident rather than force-rewriting history.

The grouped shell/uv-base source tree was finally attached at:

```text
030cbdc4204d8073813c353491592723140ae817
    module: promote shell and uv-base ownership
```

## Branch state before live migration

Repository-level work completed so far:

- legacy promoted source ownership split into modules, packages, and experiment recipes;
- deploy rewrite and deploy smoke test;
- integrated/current docs aligned to new owners;
- module/package owner contracts documented;
- CPython consumer package recorded;
- shell module and uv-base module promoted;
- hash-guarded user-environment adoption tool added;
- shell composition and adoption smoke tests passing.

Live device migration has not yet been run.
