# Modules

`modules/` owns project-authored system capabilities and their target-relative integration files.

A module answers:

> What capability does the workstation provide, and what project-owned files make that capability work?

Current module owners:

- `shell/` — thin personal Bash bootstrap, generic interactive behavior, aliases, prompt, and final cross-capability PATH ordering.
- `desktop/` — Termux:X11 + XFCE session lifecycle.
- `uv-base/` — native disposable personal base environment definition, shell integration, sync/reset hooks, and validation.
- `gl/` — glibc application-layer runtime and maintenance integration, including its shell fragment.

## Overlay contract

Target-relative files live under:

```text
modules/<name>/overlay/home/...    -> $HOME/...
modules/<name>/overlay/prefix/...  -> $PREFIX/...
```

`tools/deploy` materializes the current module selection as leaf symlinks. `tools/adopt-user-env` handles the one-time hash-guarded transition for pre-existing personal files that a normal deploy must not overwrite.

A module does not own generated runtime state merely because that state appears beneath one of its live directories. For example:

- the `gl` module does not Git-own the library farm, external app payload trees, Mesa install prefixes, or build worktrees;
- the `uv-base` module does not Git-own `.venv` or the CPython artifact/install tree;
- the shell module does not own glibc Conda runtime state.
