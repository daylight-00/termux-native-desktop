# 2. Android, Termux, PRoot, bionic, and glibc

The project becomes much easier to understand after separating **kernel**, **userspace**, **filesystem view**, and **libc ABI**.

## 2.1 One kernel, several userspace topologies

A stock Termux process is not a VM guest. It executes against the Android host kernel. Termux packages are built for Android and normally link against bionic. The Termux execution-environment documentation explicitly describes this native execution model and the package paths rooted under the application’s private data directory.

The project adds a second userspace runtime possibility without replacing the kernel:

```text
Android Linux kernel
        |
        +-- bionic-native Termux process
        |       loader: Android linker
        |       libc: bionic
        |
        +-- glibc process
        |       loader: glibc dynamic linker
        |       libc: glibc
        |
        +-- PRoot-mediated Debian process
                filesystem/syscall mediation
                Debian glibc userspace assumptions
```

These paths share the kernel but differ in how userspace libraries and paths are assembled.

## 2.2 Termux is more than a shell

A common beginner model is:

```text
Termux = terminal app + bash
```

A better model is:

```text
Termux app sandbox
    -> private application data directory
    -> package prefix
    -> binaries, libraries, headers, configuration, package database
    -> shells and user applications
```

Typical paths are:

```text
$HOME   = /data/data/com.termux/files/home
$PREFIX = /data/data/com.termux/files/usr
```

`$PREFIX` is an installation prefix inside the Android app’s filesystem space. It is not a complete independent root filesystem in the same sense as a Debian rootfs.

## 2.3 Prefix versus rootfs

A **prefix** is a base path under which a software ecosystem installs files:

```text
$PREFIX/bin
$PREFIX/lib
$PREFIX/etc
$PREFIX/share
```

A **rootfs** is the tree an environment treats as `/`:

```text
/
├── bin
├── etc
├── lib
├── usr
└── var
```

A prefix coexists inside a larger filesystem namespace. A rootfs defines the environment’s root pathname view.

This distinction matters because many desktop Linux applications contain assumptions such as:

```text
/etc/ssl/...
/usr/share/...
/lib/ld-linux-aarch64.so.1
```

A project-controlled glibc process can run without a Debian process runtime while still needing deliberate answers for those pathname assumptions.

## 2.4 bionic and glibc are userspace runtimes, not kernels

Both bionic and glibc ultimately request services from the same Android/Linux kernel. Their difference is not “different kernels”; it is userspace ABI and runtime behavior.

Conceptually:

```text
bionic application
    -> bionic APIs/wrappers/runtime
    -> syscalls
    -> Android kernel

glibc application
    -> glibc APIs/wrappers/runtime
    -> syscalls
    -> Android kernel
```

The same AArch64 instruction set does not erase differences in:

- ELF interpreter;
- libc symbols and symbol versions;
- resolver behavior and configuration assumptions;
- dynamic-loader behavior;
- path conventions;
- extension/plugin ecosystem assumptions.

## 2.5 What PRoot changes

PRoot does not boot another kernel. It provides a userspace mechanism for presenting a different root filesystem and translating/mediating relevant process behavior.

For this project, the useful conceptual distinction is:

```text
PRoot as normal runtime
    -> application path includes mediation

PRoot as oracle/warehouse
    -> apt/dpkg solve and install into rootfs
    -> project inspects or exposes selected artifacts
    -> final app process runs outside PRoot
```

The second use is architecturally different from treating PRoot as the application runtime.

## 2.6 A subtle but important distinction: process-free versus filesystem-free

A runtime can be free of PRoot **process mediation** while still depending on files physically stored in a Debian rootfs.

For example:

```text
glibc app process
    -> executes outside PRoot
    -> reads a font config from Debian rootfs path
```

This means:

```text
no PRoot execution dependency
```

but not necessarily:

```text
no Debian rootfs filesystem dependency
```

The distinction is useful when designing a future self-contained runtime closure.

## 2.7 Android shared storage is not a Unix development workspace

Termux private application storage and Android shared/emulated storage serve different purposes.

A simplified model:

```text
Termux private storage
    -> executable code
    -> symlinks
    -> Unix permission-sensitive build trees
    -> package/runtime state

Android shared storage
    -> user-visible documents and media
    -> app-to-user exchange
    -> Android-mediated access model
```

The Termux project documentation warns that shared/external storage has execution and special-file limitations and should not be treated as the normal location for Termux package trees or development environments.

For this project, use `$HOME`/`$PREFIX` for repositories, build trees, runtimes, symlinks, and ELF artifacts; use shared storage for exported reports, archives, screenshots, and user-facing exchange.

## 2.8 The project topology

The current project architecture can be modeled as:

```text
Android kernel + hardware
        |
        +-- native host plane
        |      Termux bionic userspace
        |      Termux:X11 + desktop session
        |      native tools and apps
        |
        +-- foreign application runtime domains
        |      glibc loader/core
        |      selected shared providers
        |      app-local runtime closures
        |
        +-- supply/debug plane
               Debian PRoot rootfs
               package metadata and dependency solver
               known-good behavioral controls
```

This model is stronger than saying “Termux plus Debian libraries,” because it identifies which part is authoritative, which part supplies artifacts, and which part executes applications.

## 2.9 Practical inspection exercises

```sh
printf 'HOME=%s\nPREFIX=%s\n' "$HOME" "$PREFIX"

file "$(command -v bash)"
readelf -l "$(command -v bash)" | grep -i interpreter

# Compare with a known glibc binary from the project runtime.
file "$HOME/gl/apps/vscode/code" 2>/dev/null || true

# Inspect current process maps.
cat /proc/$$/maps | head
```

Questions to answer:

1. Which ELF interpreter is encoded in each binary?
2. Which libc world appears in the mappings?
3. Which paths are private Termux paths and which are shared Android storage paths?

## References

- Termux execution environment: <https://github.com/termux/termux-packages/wiki/Termux-execution-environment>
- Android data and file storage overview: <https://developer.android.com/training/data-storage>
- Android bionic source and documentation entry point: <https://android.googlesource.com/platform/bionic/>
- PRoot project: <https://proot-me.github.io/>
- Project context: [`../../PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md)
- Project architecture: [`../../architecture.md`](../../architecture.md)
