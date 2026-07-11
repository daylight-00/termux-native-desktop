# Desktop Session: Termux:X11 + XFCE

This document is the current operational companion to `modules/desktop/overlay/home/.local/bin/startxfce-x11`.

## One display, two ABI worlds

```text
Termux:X11 Android surface
        ^
termux-x11 :1   (bionic X server, started with a clean GPU environment)
        ^
  +-----+----------------------------+
  |                                  |
bionic world                     glibc world
XFCE / native apps               patched glibc apps
bionic Mesa/Turnip               glibc Mesa/Turnip
OpenGL: Zink -> Turnip           OpenGL: Zink -> Turnip via gl-run
Chromium: ANGLE Vulkan           VS Code: ANGLE Vulkan
```

Both worlds render to the same Adreno 730, but through separate userspace libraries. Mixing the worlds is a primary failure mode; characteristic errors include `invalid ELF header` when a process loads the other world's linker-script `libc.so` or `libm.so`.

## Environment contract

| Variable | Session / bionic | glibc applications |
|---|---|---|
| `DISPLAY` | `:1` | inherited `:1` |
| `XDG_RUNTIME_DIR` | `$TMPDIR` | `$PREFIX/tmp/gl-runtime` (0700) |
| Vulkan ICD | bionic Turnip ICD exported to session clients | inherited bionic variables cleared by `~/gl/env`; explicit consumers source `~/gl/policy/vulkan/freedreno.sh` |
| `MESA_LOADER_DRIVER_OVERRIDE` | `zink` for bionic GL clients | added by `gl-run` for glibc GL apps |
| `LD_LIBRARY_PATH` | unset | never set |
| `LD_PRELOAD` | untouched globally | cleared at glibc process entry |

The bionic session must set both `VK_ICD_FILENAMES` and `VK_DRIVER_FILES` when selecting its ICD. At the glibc boundary, `~/gl/env` clears both variables together. A glibc consumer that deliberately selects the managed hardware provider then sources the explicit profile, which sets both variables to the glibc ICD together.

Do not leave a partial pair. Do not treat `unset VK_*` as proof of no Vulkan participation: loader discovery can select software or virtual providers. The absence of an explicit pin only means that no provider was selected by policy.

The dual `XDG_RUNTIME_DIR` values are intentional. Do not unify them: the bionic session uses the Termux runtime convention, while glibc applications use a separate protected runtime directory.

## X server starts clean

The session exports GPU policy for clients, but launches `termux-x11` under `env -u` for Mesa/Vulkan client variables. The display server itself should not inherit Zink or ICD overrides.

## Local Unix socket only

The current path uses `DISPLAY=:1` with TCP disabled. glibc-repo `libX11`/`libxcb` builds understand the Termux socket layout. TCP listening was only a workaround for the earlier Debian-libxcb mismatch and should stay disabled.

## Compositing policy

- XFWM's built-in compositor is disabled at runtime and in xfconf.
- Picom is optional and off by default.
- If Picom is enabled, validate `glxinfo.log`; the expected renderer contains Zink and Turnip/Adreno.

## Usage

```sh
startxfce-x11
startxfce-x11 stop
KILL_BROWSER=1 startxfce-x11
```

Logs live under `~/.cache/termux-x11-session/`.

Android-side prerequisites:

- Termux:X11 APK and `termux-x11-nightly` package should come from the same nightly generation.
- Termux needs **Display over other apps** permission for URL intents launched from inside the desktop.

## Troubleshooting

| Symptom | Likely cause | First check |
|---|---|---|
| script exits immediately | unset `TMPDIR` under `set -u` | current launcher includes guard |
| glibc app cannot open display | Debian `libxcb` wins | glibc-repo X11/xcb must precede farm |
| `invalid ELF header` | bionic/glibc library or ICD mixing | no `LD_LIBRARY_PATH`; confirm `~/gl/env` cleared bionic `VK_*` before any provider profile |
| GL renderer is llvmpipe | explicit Freedreno profile or Zink override missing, or initialization failed | check the profile, both VK variables, and `MESA_LOADER_DRIVER_OVERRIDE=zink` |
| `VK_ERROR_INCOMPATIBLE_DRIVER` in Zink | wrong or missing explicit ICD selection | source the glibc Freedreno profile; verify both VK variables |
| URLs do not open | Android BAL policy | grant Display over other apps |

The historical session experiment record remains at `experiments/desktop/session-launch/`.
