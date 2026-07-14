# Knowledge Layer References

This bibliography prioritizes primary specifications, upstream project documentation, and the project’s own validated records. The knowledge chapters are explanatory syntheses; they are not substitutes for the specifications.

## Android and Termux

- Termux execution environment: <https://github.com/termux/termux-packages/wiki/Termux-execution-environment>
- Termux filesystem layout: <https://github.com/termux/termux-packages/wiki/Termux-file-system-layout>
- Android data and file storage overview: <https://developer.android.com/training/data-storage>
- Android platform source: <https://android.googlesource.com/>
- Android bionic source: <https://android.googlesource.com/platform/bionic/>
- Android NDK guides: <https://developer.android.com/ndk/guides>

## Linux kernel and userspace interface

- Linux kernel documentation: <https://docs.kernel.org/>
- VFS overview: <https://docs.kernel.org/filesystems/vfs.html>
- Memory management documentation: <https://docs.kernel.org/mm/>
- GPU documentation: <https://docs.kernel.org/gpu/>
- dma-buf documentation: <https://docs.kernel.org/driver-api/dma-buf.html>
- Linux man-pages project: <https://man7.org/linux/man-pages/>

## CPU and ABI

- Arm ABI repository: <https://github.com/ARM-software/abi-aa>
- AAPCS64: <https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst>
- Linux arm64 documentation: <https://docs.kernel.org/arch/arm64/>

## ELF and dynamic linking

- ELF gABI reference: <https://refspecs.linuxfoundation.org/elf/gabi4+/contents.html>
- GNU C Library manual: <https://sourceware.org/glibc/manual/>
- glibc linker namespaces: <https://sourceware.org/glibc/wiki/LinkerNamespaces>
- `patchelf`: <https://github.com/NixOS/patchelf>
- POSIX `dlopen`: <https://pubs.opengroup.org/onlinepubs/9699919799/functions/dlopen.html>
- POSIX `dlsym`: <https://pubs.opengroup.org/onlinepubs/9699919799/functions/dlsym.html>

## Package management

- pacman manual: <https://man.archlinux.org/man/pacman.8.en>
- Debian Reference, package management: <https://www.debian.org/doc/manuals/debian-reference/ch02.en.html>
- Debian Policy Manual: <https://www.debian.org/doc/debian-policy/>
- dpkg documentation: <https://www.dpkg.org/doc/>

## IPC and display systems

- D-Bus specification: <https://dbus.freedesktop.org/doc/dbus-specification.html>
- X.Org documentation: <https://www.x.org/wiki/Documentation/>
- Wayland documentation: <https://wayland.freedesktop.org/docs/html/>

## Networking

- RFC 9293, TCP: <https://www.rfc-editor.org/rfc/rfc9293.html>
- RFC 9110, HTTP semantics: <https://www.rfc-editor.org/rfc/rfc9110.html>
- RFC 8446, TLS 1.3: <https://www.rfc-editor.org/rfc/rfc8446.html>
- RFC 6455, WebSocket: <https://www.rfc-editor.org/rfc/rfc6455.html>
- RFC 1928, SOCKS v5: <https://www.rfc-editor.org/rfc/rfc1928.html>

## Build systems and toolchains

- LLVM documentation: <https://llvm.org/docs/>
- Meson documentation: <https://mesonbuild.com/>
- Meson cross compilation: <https://mesonbuild.com/Cross-compilation.html>
- Ninja manual: <https://ninja-build.org/manual.html>
- CMake build-system manual: <https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html>
- pkg-config guide: <https://people.freedesktop.org/~dbn/pkg-config-guide.html>

## Distribution formats

- AppImage documentation: <https://docs.appimage.org/>
- Flatpak documentation: <https://docs.flatpak.org/>
- Python wheel specification: <https://packaging.python.org/en/latest/specifications/binary-distribution-format/>
- Conda package specification: <https://docs.conda.io/projects/conda-build/en/stable/resources/package-spec.html>
- Node.js C++ addons: <https://nodejs.org/api/addons.html>
- OCI image specification: <https://github.com/opencontainers/image-spec>

## Graphics

- Mesa documentation: <https://docs.mesa3d.org/>
- Mesa source: <https://gitlab.freedesktop.org/mesa/mesa>
- Vulkan specification: <https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html>

## Debugging

- GDB manual: <https://sourceware.org/gdb/current/onlinedocs/gdb.html/>
- GNU Binutils documentation: <https://sourceware.org/binutils/docs/>
- DWARF standard: <https://dwarfstd.org/>
- Linux kernel tracing: <https://docs.kernel.org/trace/>

## Project-local references

- [`../PROJECT_CONTEXT.md`](../PROJECT_CONTEXT.md)
- [`../architecture.md`](../architecture.md)
- [`../glibc-layer.md`](../glibc-layer.md)
- [`../gpu.md`](../gpu.md)
- [`../desktop-session.md`](../desktop-session.md)
- [`../../STATUS.md`](../../STATUS.md)
- [`../../experiments/README.md`](../../experiments/README.md)
