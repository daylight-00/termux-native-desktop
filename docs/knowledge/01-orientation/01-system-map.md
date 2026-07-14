# 1. A System Map: From Intent to Hardware

The fastest way to become confused in systems work is to treat every failure as if it happened in one undifferentiated thing called “Linux.” The fastest way to become effective is to ask **which layer owns this behavior?**

This chapter establishes the map used by the rest of the knowledge layer.

## 1.1 The full path

A desktop application on this project can be viewed as a path through many layers:

```text
user intent
    -> application behavior
    -> language/runtime API
    -> shared libraries
    -> process and threads
    -> syscalls
    -> kernel subsystems
    -> device drivers
    -> hardware
```

For a graphical application, one possible path is:

```text
PyMOL
    -> Python + native extension modules
    -> OpenGL API
    -> Zink
    -> Vulkan loader
    -> Turnip userspace driver
    -> KGSL kernel interface
    -> Adreno GPU

PyMOL
    -> X11 client protocol
    -> Termux:X11 server
    -> Android surface/display path
```

These are not the same path. Rendering and presentation intersect, but a successful GPU render does not automatically prove a successful display/presentation path.

## 1.2 Five kinds of boundary

The project repeatedly crosses five different kinds of boundary. They should not be conflated.

### Language boundary

Examples:

```text
Python -> CPython C API
JavaScript -> Node native addon
C++ -> C ABI shim
```

A language package can contain native ELF objects; therefore a successful package installation does not imply ABI compatibility.

### Process boundary

Processes have separate virtual address spaces. They communicate through explicit mechanisms such as sockets, pipes, shared memory, or filesystem objects.

This boundary is useful because it can also serve as an ABI isolation boundary. A bionic process and a glibc process can exchange bytes over a socket without loading each other’s libc objects into the same address space.

### ABI boundary

An ABI defines binary-level contracts: calling convention, object layout assumptions, ELF conventions, symbol versions, libc expectations, and related details. “AArch64” answers only the CPU instruction-set question. It does not imply that two AArch64 userspaces are binary-compatible.

### Kernel boundary

A process requests kernel services through syscalls and subsystem-specific interfaces such as `ioctl`, `mmap`, sockets, and device nodes. The kernel is shared by the Termux bionic world, PRoot-mediated Debian processes, and the project’s glibc processes.

### Protocol boundary

X11, HTTP, TLS, D-Bus, SSH, and WebSocket are examples of protocols. A protocol boundary is often more stable than sharing runtime internals directly.

## 1.3 The core mental model: graphs, not lists

A runtime is not a list of files. It is a set of interacting graphs.

### Package graph

```text
package A
    -> depends on package B
    -> depends on package C
```

This tells a package manager what must be installed, not necessarily what is loaded into one process.

### ELF graph

```text
app
    -> libA.so
    -> libB.so
         -> libC.so
```

This describes static dynamic-linker relationships visible through ELF metadata. It still misses runtime `dlopen` edges.

### Process graph

```text
Electron browser process
    -> renderer process
    -> GPU process
    -> utility process
```

A crash in one child is not necessarily a crash in the application’s main process.

### IPC graph

```text
client
    -> Unix socket
    -> server
```

This graph explains why a library can load successfully while an application still fails because a bus socket, display socket, or helper service is absent.

### Filesystem/object graph

```text
pathname
    -> dentry
    -> inode
    -> open file object
    -> file descriptor
```

This explains why symlinks, bind mounts, open-but-unlinked files, device nodes, and Unix sockets cannot all be treated as ordinary copied files.

### Network graph

```text
application
    -> DNS resolver
    -> proxy policy
    -> TCP/TLS transport
    -> service endpoint
```

“Internet works” is too coarse. DNS may work while WebSocket fails and HTTPS fallback succeeds.

### Execution-state graph

```text
crash signal
    -> thread
    -> PC
    -> mapped ELF object
    -> fault address
    -> mapping
    -> fd
    -> mmap/ioctl history
```

This is the graph used in serious crash analysis.

## 1.4 Layers are not excuses to stop investigating

A layered model is valuable only if it helps cross layers when evidence demands it.

For example:

```text
symptom: Electron GPU process crashes
```

Possible investigation path:

```text
application log
    -> process identity
    -> signal
    -> PC and mapping
    -> userspace driver function
    -> buffer mapping
    -> fd identity
    -> ioctl sequence
    -> kernel/GPU interface
```

The purpose of abstraction is not to hide lower layers forever. It is to know when and where to descend.

## 1.5 A practical classification table

When an experiment fails, classify the first proven failure point.

| Layer | Typical evidence | Example question |
|---|---|---|
| Package | apt/dpkg/pacman metadata | Was the dependency installed? |
| Filesystem | path, symlink, mount, permissions | Does the expected object exist in this path view? |
| ELF | interpreter, `NEEDED`, symbols | Can this binary be loaded coherently? |
| Process | child exit, signal, thread state | Which process actually failed? |
| IPC | socket address, bus, display | Can client and server reach the same endpoint? |
| Network | DNS/TCP/TLS/proxy | Which transport layer failed? |
| GPU | ICD, driver, UAPI, WSI | Did render, buffer sharing, or presentation fail? |
| Application | feature-specific logs | Is the runtime healthy but the feature misconfigured? |

## 1.6 Project connection

The project’s deepest recurring lesson is that the phone is not “running Debian without PRoot.” Instead, one Android kernel hosts multiple userspace arrangements:

```text
Android kernel
    |
    +-- Termux bionic-native processes
    |
    +-- project-controlled glibc processes
    |
    +-- PRoot-mediated Debian processes used for supply/debug work
```

The architecture succeeds when these worlds are composed intentionally and fails when their implementation details leak into each other accidentally.

## 1.7 Study checkpoints

After this chapter, be able to explain:

1. why a package dependency graph is not a complete runtime dependency graph;
2. why a process boundary can be useful as an ABI boundary;
3. why “GPU detected” is weaker than “presentation path works”;
4. why a socket path is not equivalent to an ordinary file path;
5. why a WebSocket failure can coexist with working HTTPS.

## References

- Linux kernel VFS documentation: <https://docs.kernel.org/filesystems/vfs.html>
- Termux execution environment: <https://github.com/termux/termux-packages/wiki/Termux-execution-environment>
- Arm AAPCS64: <https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst>
- Project architecture: [`../../architecture.md`](../../architecture.md)
