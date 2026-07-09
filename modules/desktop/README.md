# Desktop module

`startxfce-x11` is the recovered canonical launcher for the current Termux:X11 + XFCE session.

The module manages the Bionic side of the desktop:

- clean restart and explicit `stop` teardown;
- `TMPDIR` guard for non-interactive launch contexts;
- local Unix-socket X11 on `DISPLAY=:1` with TCP disabled;
- Bionic Turnip ICD selection for native clients;
- session-wide Bionic Zink policy for OpenGL clients;
- a clean X-server process with client GPU overrides removed;
- stale D-Bus PID cleanup;
- opt-in browser termination through `KILL_BROWSER=1`;
- XFWM compositor disablement and optional Picom path;
- renderer sanity logging.

The corresponding architecture and troubleshooting guide is `docs/desktop-session.md`.

## Source and live target

```text
modules/desktop/overlay/home/.local/bin/startxfce-x11
    -> $HOME/.local/bin/startxfce-x11
```

`tools/deploy` installs the live leaf symlink.

The historical discovery and hardening record remains under `experiments/desktop/session-launch/`.
