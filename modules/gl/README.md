# gl module

The `gl` module owns project-authored integration for the managed glibc application layer.

## Owned capability

```text
modules/gl/overlay/home/gl/
├── env
├── bin/
│   ├── gl-farm
│   └── gl-run
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

`env` defines the glibc application runtime contract. `gl-run` adds the Zink-specific OpenGL execution policy. `gl-farm` regenerates the filtered Debian-rootfs-derived shared-library view and refreshes the glibc loader cache. The toolchain wrappers expose Termux glibc target tools safely from the Bionic host shell.

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
