# Desktop session launch

**Status:** passed in live use; canonical launcher recovered and promoted  
**Provenance:** first-hand summary from field hardening + recovered launcher source

## Question

How should a one-command XFCE session be started under Termux:X11 so that the X server remains clean of client GPU overrides, the bionic and glibc worlds coexist, and restart cycles do not leave harmful stale state?

## Field failures that shaped the launcher

- launch contexts with unset `TMPDIR` caused immediate failure under `set -u`; the launcher now supplies a guarded default;
- the X server must not inherit client-specific Mesa/Vulkan overrides;
- TCP X11 was only a workaround for the old Debian-libxcb pilot path and is no longer the intended transport once glibc-repo X11/xcb libraries are used;
- session-level bionic GPU selection and glibc-application GPU selection are intentionally different contracts;
- stale D-Bus PID state required explicit cleanup discipline;
- browser termination on restart became opt-in rather than unconditional;
- Picom remains off by default and XFWM compositing policy avoids accidental double composition.

## Result

The live session model is stable enough for the current workstation and supports the mixed bionic/glibc desktop architecture.

## Promoted artifacts

- `setup/session/startxfce-x11` — recovered canonical launcher.
- `docs/desktop-session.md` — integrated two-world environment contract and troubleshooting guide.
- `scripts/deploy-gl.sh` — live symlink deployment contract.
