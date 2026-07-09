# Session setup

`startxfce-x11` is the recovered canonical launcher for the current Termux:X11 + XFCE session.

The script manages the bionic side of the desktop:

- clean restart and explicit `stop` teardown;
- `TMPDIR` guard for non-interactive launch contexts;
- local Unix-socket X11 on `DISPLAY=:1` with TCP disabled;
- bionic Turnip ICD selection for native clients;
- session-wide bionic Zink policy for OpenGL clients;
- a clean X-server process with client GPU overrides removed;
- stale D-Bus PID cleanup;
- opt-in browser termination through `KILL_BROWSER=1`;
- XFWM compositor disablement and optional Picom path;
- renderer sanity logging.

The corresponding architecture and troubleshooting guide is `docs/desktop-session.md`.

The live link contract remains:

```text
setup/session/startxfce-x11
    -> ~/.local/bin/startxfce-x11
```

`scripts/deploy-gl.sh` installs that link together with the other promoted runtime paths.
