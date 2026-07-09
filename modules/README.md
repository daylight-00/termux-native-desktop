# Modules

`modules/` owns project-authored system capabilities and their target-relative integration files.

A module answers:

> What capability does the workstation provide, and what project-owned files make that capability work?

Current module owners:

- `desktop/` — Termux:X11 + XFCE session lifecycle.
- `gl/` — glibc application-layer runtime and maintenance integration.
- `shell/` — reserved for the tracked personal shell bootstrap and generic shell behavior; not yet promoted in the current refactor phase.
- `uv-base/` — reserved for the native disposable personal base environment; promotion waits for capture of the live project definition and lock state.

## Overlay contract

Target-relative files live under:

```text
modules/<name>/overlay/home/...    -> $HOME/...
modules/<name>/overlay/prefix/...  -> $PREFIX/...
```

`tools/deploy` materializes the current module selection as leaf symlinks.

A module does not own generated runtime state merely because that state appears beneath one of its live directories. For example, the `gl` module does not Git-own the library farm, external app payload trees, Mesa install prefixes, or build worktrees.
