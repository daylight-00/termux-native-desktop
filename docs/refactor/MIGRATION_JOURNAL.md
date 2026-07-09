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
