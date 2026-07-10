# Systems Knowledge Layer

This documentation set grew out of a simple question: **what is `pacman` in Termux?**

Answering that question honestly required progressively opening larger boxes. A package manager led to packages and repositories; packages led to prefixes, root filesystems, loaders, ABIs, and shared libraries; those led to processes, virtual memory, filesystems, syscalls, IPC, networking, drivers, build systems, packaging, and debugging. The resulting map is not a general-purpose operating-systems textbook. It is a project-oriented learning path for understanding the mechanisms that repeatedly appear in `termux-native-desktop`.

The organizing principle is cumulative: each chapter introduces only enough abstraction to make the next layer meaningful, then connects the concept back to the project.

## Reading order

### 1. Orientation

1. [`01-orientation/01-system-map.md`](01-orientation/01-system-map.md) — the complete stack from user intent to hardware.
2. [`01-orientation/02-termux-android-runtime-topology.md`](01-orientation/02-termux-android-runtime-topology.md) — Android, Termux, bionic, glibc, PRoot, and the project topology.

### 2. Packages and environments

3. [`02-packages/01-package-management-bootstrap-rootfs.md`](02-packages/01-package-management-bootstrap-rootfs.md) — package managers, repositories, bootstrap, prefix, rootfs, and minbase.
4. [`02-packages/02-packages-installation-and-runtime-closures.md`](02-packages/02-packages-installation-and-runtime-closures.md) — `.deb`, installation state, package graphs, ELF graphs, and runtime closures.

### 3. Execution and machine foundations

5. [`03-execution/01-process-syscall-fd.md`](03-execution/01-process-syscall-fd.md) — processes, threads, syscalls, file descriptors, signals, and scheduler interaction.
6. [`03-execution/02-virtual-memory-and-storage.md`](03-execution/02-virtual-memory-and-storage.md) — address spaces, mappings, page faults, page cache, writeback, `mmap`, and persistence.
7. [`03-execution/03-cpu-aarch64-and-abi.md`](03-execution/03-cpu-aarch64-and-abi.md) — instructions, registers, calls, AArch64 calling convention, syscall ABI, and the meaning of ABI.

### 4. ELF and dynamic linking

8. [`04-elf/01-elf-loader-linking.md`](04-elf/01-elf-loader-linking.md) — ELF structure, interpreter, `DT_NEEDED`, RPATH/RUNPATH, symbols, relocations, and `patchelf`.
9. [`04-elf/02-dynamic-linking-deep-dive.md`](04-elf/02-dynamic-linking-deep-dive.md) — GOT/PLT, lazy binding, interposition, `dlopen`, `dlsym`, scopes, and runtime coherence.

### 5. Filesystems, IPC, display, and networking

10. [`05-system-services/01-filesystem-vfs-mounts.md`](05-system-services/01-filesystem-vfs-mounts.md) — pathname resolution, dentry, inode, symlink, mount, namespaces, `/proc`, `/sys`, and `/dev`.
11. [`05-system-services/02-ipc-dbus-x11-process-graphs.md`](05-system-services/02-ipc-dbus-x11-process-graphs.md) — pipes, Unix sockets, D-Bus, X11, Wayland, child processes, and launcher contracts.
12. [`05-system-services/03-networking-tls-proxies.md`](05-system-services/03-networking-tls-proxies.md) — sockets, TCP/UDP, DNS, TLS, proxies, WebSockets, and the Codex/tinyproxy lesson.

### 6. Build and distribution

13. [`06-build/01-compilers-build-systems-toolchains.md`](06-build/01-compilers-build-systems-toolchains.md) — preprocessing, compilation, linking, Meson/Ninja/CMake, `pkg-config`, sysroots, and cross compilation.
14. [`06-build/02-packaging-distribution-and-runtime-contracts.md`](06-build/02-packaging-distribution-and-runtime-contracts.md) — tarballs, `.deb`, AppImage, Flatpak, wheel, Conda, npm, OCI, and runtime contracts.

### 7. Kernel, GPU, debugging, and measurement

15. [`07-platform/01-kernel-drivers-gpu.md`](07-platform/01-kernel-drivers-gpu.md) — scheduler, interrupts, drivers, `ioctl`, DMA, IOMMU, dma-buf, Mesa/Turnip, KGSL, and WSI.
16. [`07-platform/02-debugging-performance-and-experiment-design.md`](07-platform/02-debugging-performance-and-experiment-design.md) — signals, registers, stack unwinding, DWARF, core dumps, `strace`, GDB, `perf`, and controlled experiments.

## How to use this set

A useful study loop is:

```text
read a chapter
    -> inspect one real object on the device
    -> predict what a tool will show
    -> run the tool
    -> compare prediction with observation
    -> update the mental model
```

Examples:

```sh
# Package / executable identity
command -v bash
file "$(command -v bash)"

# ELF structure
readelf -h "$(command -v bash)"
readelf -l "$(command -v bash)"
readelf -d "$(command -v bash)"

# Runtime mappings and file descriptors
cat /proc/$$/maps
ls -l /proc/$$/fd

# Filesystem topology
findmnt
cat /proc/self/mountinfo
```

The chapters intentionally distinguish three levels of certainty:

- **mechanism** — what the underlying system model permits or requires;
- **project observation** — what has been demonstrated in this repository;
- **hypothesis** — a plausible explanation that still requires evidence.

That distinction is essential in a project where a practical workaround can be validated before the exact low-level mechanism is proven.

## References

Primary and project-relevant references are collected in [`REFERENCES.md`](REFERENCES.md). Individual chapters also include a focused reference section.
