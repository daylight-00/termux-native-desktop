# Desktop session launch

**Status:** passed in live use; tracked launcher source recovery pending  
**Provenance:** first-hand summary from field hardening

## Question

How should a one-command XFCE session be started under Termux:X11 so that the X server remains clean of client GPU overrides, the bionic and glibc worlds coexist, and restart cycles do not leave harmful stale state?

## Field failures that shaped the launcher

- launch contexts with unset `TMPDIR` caused immediate failure under `set -u`; the launcher added a guarded default;
- the X server must not inherit client-specific Mesa/Vulkan overrides;
- TCP X11 was only a workaround for the old Debian-libxcb pilot path and is no longer the intended transport once glibc-repo X11/xcb libraries are used;
- session-level bionic GPU selection and glibc-application GPU selection are intentionally different contracts;
- stale D-Bus PID state required explicit cleanup discipline;
- browser termination on restart became opt-in rather than unconditional;
- Picom remains off by default and XFWM compositing policy avoids accidental double composition.

## Result

The live session model is stable enough for the current workstation and supports the mixed bionic/glibc desktop architecture.

## Artifact status

The experiment record refers to `setup/session/startxfce-x11`, but that canonical source file is not present in the current GitHub tree. Because earlier reports contain older representative scripts, the missing launcher must be recovered from the on-device source rather than reconstructed from history.

See `setup/session/README.md`.
