# glibc Application Layer

This guide integrates the recovered `gl` layer README with the current repository structure. Detailed experiment provenance remains under `experiments/glibc/`, `experiments/gpu/`, and `docs/refactor/`.

## Goal

Run conventional Linux arm64/glibc application distributions from native Termux without using PRoot as the application runtime.

```text
application   ~/gl/apps/<name>/
library farm ~/gl/lib/
glibc core   $PREFIX/glibc/
warehouse    $PREFIX/var/lib/proot-distro/containers/debian/rootfs
```

PRoot is retained for package installation, dependency discovery, and debugging controls. Runtime applications execute outside PRoot.

## Library boundary

The conceptual lookup model is:

```text
$ORIGIN
  -> $PREFIX/glibc/lib
  -> ~/gl/lib
```

Important rules:

- never expose a glibc `LD_LIBRARY_PATH` to the bionic Termux shell;
- libc-family libraries come from the Termux glibc core, never the Debian farm;
- glibc-repo X11/xcb libraries must win over Debian variants for local Termux:X11 socket access;
- application-local libraries must keep `$ORIGIN` in RPATH where required;
- transitive dependencies are handled through glibc loader configuration and `ldconfig`.

## Bootstrap outline

1. Install Termux X11/glibc prerequisites, including glibc-repo X11/xcb packages.
2. Install a Debian PRoot distribution as the package/library warehouse.
3. Populate required general libraries inside the rootfs.
4. Run `gl-farm` to rebuild `~/gl/lib` from allowed rootfs libraries.
5. Register core then farm in the glibc loader configuration and refresh `ldconfig`.
6. Deploy module overlays and package-owned launchers through `tools/deploy`.

A representative core setup includes:

```sh
pkg install x11-repo tur-repo termux-x11-nightly patchelf file curl proot-distro
pkg install glibc-repo glibc libx11-glibc libxcb-glibc
proot-distro install debian
```

The rootfs path may vary across proot-distro generations; the current project contract uses `containers/debian/rootfs`.

## Library farm

`modules/gl/overlay/home/gl/bin/gl-farm`:

- rebuilds `~/gl/lib` as symlinks into selected Debian rootfs library directories;
- excludes the libc family through a denylist;
- performs a contamination check;
- refreshes the glibc loader cache.

Farm regeneration and `ldconfig` refresh are one operation.

## Application onboarding

For a conventional tarball or extracted application tree:

1. unpack under `~/gl/apps/<name>/`;
2. use the Debian rootfs as a dependency oracle when additional libraries are needed;
3. rebuild the farm if the rootfs library set changes;
4. patch executable interpreters to the Termux glibc loader;
5. patch RPATH while preserving `$ORIGIN`;
6. verify every ELF with the glibc `ldd` path;
7. create a package-owned launcher that sources `~/gl/env` and clears incompatible preload state at process entry;
8. if the workload deliberately requires the managed hardware Vulkan provider, source `~/gl/policy/vulkan/freedreno.sh` in that launch branch;
9. add an OpenGL bridge only in the consumer that owns it, such as `gl-run` for Zink;
10. validate CPU/basic GUI startup separately from GPU enablement and selected-provider evidence;
11. make application-owned configuration and user-data paths receipt-local before claiming isolated validation.

AppImage is supported as an input adapter by extracting the embedded SquashFS payload first, then reusing the same onboarding pipeline. See `experiments/glibc/obsidian-appimage/`.

## Graphics policy boundary

`~/gl/env` is the shared glibc baseline. It clears four classes of inherited bionic/session graphics policy:

```text
VK_ICD_FILENAMES
VK_DRIVER_FILES
MESA_LOADER_DRIVER_OVERRIDE
GALLIUM_DRIVER
```

The first pair is an ABI-critical Vulkan provider selection. The second pair is OpenGL bridge/Gallium device policy. None is a valid glibc-world global default merely because it is valid for the surrounding bionic desktop session.

The baseline does not choose a glibc Vulkan provider or OpenGL bridge.

The source-only profile:

```text
~/gl/policy/vulkan/freedreno.sh
```

selects the managed glibc Freedreno ICD by exporting both Vulkan loader variables together. It is applied only by consumers that deliberately require that provider.

Current accepted compositions:

```text
gl-run
    -> source gl/env
    -> inherited bionic provider/bridge policy absent
    -> source explicit Freedreno profile
    -> MESA_LOADER_DRIVER_OVERRIDE=zink

VS Code GPU branch
    -> source gl/env
    -> inherited bionic provider/bridge policy absent
    -> source explicit Freedreno profile
    -> ANGLE Vulkan flags
    -> no Zink/Gallium override

Obsidian GUI GPU branch
    -> source gl/env
    -> inherited bionic provider/bridge policy absent
    -> source explicit Freedreno profile
    -> ANGLE Vulkan flags
    -> no Zink/Gallium override

VS Code / Obsidian CPU branches
    -> source gl/env
    -> GL_GPU=0
    -> no explicit Vulkan provider
    -> no OpenGL bridge/Gallium override
    -> exact --disable-gpu

Obsidian CLI
    -> source gl/env
    -> no explicit Vulkan provider
    -> no OpenGL bridge/Gallium override
```

This separates ABI/session sanitation, provider selection, bridge selection, and application feature mode.

The complete accepted transaction is recorded in:

```text
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

## Application-state isolation

Validation must not rely on the user's normal profile state.

Accepted patterns:

```text
VS Code:
    receipt-local user-data directory
    receipt-local extensions directory

Obsidian:
    XDG_CONFIG_HOME=<receipt-local config root>
    actual user data=<receipt-local config root>/obsidian
```

For Obsidian, passing only `--user-data-dir` was insufficient in the first probe because the application retained `$HOME/.config/obsidian` as its effective authority. The corrected model aligns `XDG_CONFIG_HOME`, the application-derived directory, and `DevToolsActivePort` observation.

See:

```text
docs/refactor/0088-obsidian-user-data-authority-and-cdp-path-false-negative.md
docs/refactor/0089-current-obsidian-gpu-environment-and-primary-identity-pass.md
docs/refactor/0090-current-obsidian-cpu-policy-and-survival-pass.md
```

## Evidence interpretation

Selected GPU identity is not inferred from one mapped library.

Promoted Electron GPU acceptance correlates:

```text
observable launch environment and argv
CDP primary device identity
ANGLE/Vulkan feature mode
managed provider mapping
KGSL device-node mapping
```

CPU acceptance requires:

```text
GL_GPU=0
no explicit Vulkan pair
no Mesa/Gallium bridge/device override
exact --disable-gpu
no GPU-enablement flags
viable renderer/main topology
bounded main-process survival
```

A process named `gpu-process` may or may not exist in CPU mode. VS Code retained one with `--use-gl=disabled`; Obsidian created none in its canonical CPU receipt. The contract is selected policy and effective mode, not a universal process-name rule.

Empty or near-empty child `/proc/<pid>/environ` is an observability boundary. It is not proof that a value is absent and not a mismatch by itself.

## Common failure signatures

1. **`LD_LIBRARY_PATH` contamination** — bionic processes encounter glibc linker scripts and fail with ELF-header errors.
2. **Transitive dependency failure** — direct RPATH lookup succeeds, but downstream dependencies fail until loader configuration/cache is correct.
3. **X display failure** — Debian `libxcb` wins over the Termux-aware glibc-repo build.
4. **Lost `$ORIGIN`** — bundled application libraries such as Electron-local `.so` files stop resolving after careless RPATH replacement.
5. **Electron sandbox ordering** — sandbox checks can occur before `argv.json`; the project uses launch environment/CLI policy instead.
6. **URL intents silently blocked** — Android background-activity policy requires Termux's Display over other apps permission.
7. **Wrong Vulkan ICD** — a glibc process inherits the bionic ICD or applies the wrong profile; confirm `~/gl/env` sanitizes first and the intended profile sets both loader variables.
8. **Unexpected Zink in ANGLE/CPU workload** — the bionic session's `MESA_LOADER_DRIVER_OVERRIDE` crossed the boundary; confirm the baseline clears it and `GALLIUM_DRIVER`.
9. **Unexpected llvmpipe** — explicit provider policy was absent or failed; note that implicit discovery is allowed to select software providers.
10. **CDP endpoint timeout with a live Electron app** — application-owned user-data authority and the observed `DevToolsActivePort` path disagree.

## Current promoted owners

```text
modules/gl/overlay/home/gl/env
modules/gl/overlay/home/gl/bin/gl-farm
modules/gl/overlay/home/gl/bin/gl-run
modules/gl/overlay/home/gl/policy/vulkan/freedreno.sh
modules/gl/overlay/home/gl/shims/xdg-open
modules/gl/overlay/home/gl/toolchain/*

modules/desktop/overlay/home/.local/bin/startxfce-x11

packages/vscode/launcher/code
packages/obsidian/launcher/obsidian
packages/obsidian/launcher/obsidian-app
packages/mesa-glibc/build.sh
packages/mesa-glibc/build-env/*
packages/mesa-glibc/patches/

tools/deploy
```

Runtime state remains outside Git tracking: application trees, the farm, Mesa install prefixes, build worktrees, generated uv environments, and the installed glibc core.

## Validated workloads

- official Microsoft VS Code arm64 tarball;
- Obsidian arm64 AppImage after extraction/onboarding;
- Miniforge/Conda/Mamba with environment creation and compiled NumPy workload;
- promoted glibc OpenGL 4.6 through `gl-run` -> Zink -> Turnip;
- promoted ANGLE Vulkan -> Turnip/Adreno 730 for official VS Code;
- promoted VS Code CPU branch with hostile-policy sanitation, exact `--disable-gpu`, and bounded survival;
- promoted Obsidian GPU branch with isolated application-owned user data, CDP primary Turnip/Adreno 730, WebGL, and WebGL2;
- promoted Obsidian CPU branch with isolated application-owned user data, exact `--disable-gpu`, renderer `--disable-gpu-compositing`, and bounded survival;
- same-consumer VS Code policy A/B showing explicit Turnip/Adreno versus implicit LVP/llvmpipe.

The scoped graphics-policy promotion transaction is closed. Previously accepted gates should be rerun only when their claim surface changes; see `docs/refactor/0091-scoped-graphics-policy-promotion-closure.md` for the revalidation triggers.

The next major scientific workload target is PyMOL.
