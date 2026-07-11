# gl module

The `gl` module owns project-authored integration for the managed glibc application layer.

## Owned capability

```text
modules/gl/overlay/home/gl/
├── env
├── bin/
│   ├── gl-farm
│   └── gl-run
├── policy/
│   └── vulkan/
│       └── freedreno.sh
├── shims/
│   └── xdg-open
└── toolchain/
    ├── glibc-ar
    ├── glibc-exec
    ├── glibc-g++
    ├── glibc-gcc
    ├── glibc-pkg-config
    ├── glibc-ranlib
    └── glibc-strip
```

These files map to the same relative paths under `$HOME/gl/`.

`env` defines the provider-neutral glibc application baseline. It removes inherited bionic Vulkan provider variables as ABI sanitation, but does not select a glibc Vulkan provider.

`policy/vulkan/freedreno.sh` is a source-only explicit hardware-provider profile. Consumers source it only when they deliberately require the managed glibc Freedreno/Turnip Vulkan path.

`gl-run` composes that explicit Vulkan provider profile with the Zink-specific OpenGL bridge mode. `gl-farm` regenerates the filtered Debian-rootfs-derived shared-library view and refreshes the glibc loader cache. The toolchain wrappers expose Termux glibc target tools safely from the Bionic host shell.

This separation preserves four distinct responsibilities:

```text
shared glibc baseline sanitation
explicit Vulkan provider selection
OpenGL-to-Vulkan bridge selection
application feature/argv mode
```

Do not collapse them back into one shared environment side effect.

## Explicit non-ownership

The module does not Git-own:

```text
$HOME/gl/apps/       external application payloads
$HOME/gl/lib/        generated compatibility farm
$HOME/gl/opt/        installed/versioned runtime prefixes
$HOME/gl/build/      source checkouts and generated build work
$PREFIX/glibc/       Termux package-manager-owned core runtime
Debian rootfs        supply backend and package/library warehouse
```

Application-specific launchers belong to their packages, not to `gl/bin` source ownership.

See `docs/glibc-layer.md` and `docs/refactor/0002-ownership-map.md`.
