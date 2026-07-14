# 10. Filesystems, VFS, Inodes, Symlinks, Mounts, and Namespaces

Paths are not files. A pathname is a lookup request through a filesystem namespace. This distinction is essential for understanding symlinks, Unix sockets, device nodes, `/proc`, PRoot path translation, and relocation failures.

## 10.1 VFS

Linux provides a Virtual Filesystem layer that gives userspace a common interface across different filesystem implementations.

Conceptually:

```text
application
    -> open/read/write/stat
    -> VFS
    -> ext4 / f2fs / tmpfs / procfs / sysfs / FUSE / ...
```

The same syscall interface can reach very different object types and filesystem implementations.

## 10.2 Pathname resolution

A path such as:

```text
/home/user/project/file.txt
```

is resolved component by component.

A useful conceptual model:

```text
pathname component
    -> directory lookup
    -> dentry/cache relationship
    -> inode/object identity
```

The Linux kernel VFS documentation describes dentries as pathname-cache objects and inodes as filesystem objects. Multiple dentries can refer to the same inode, which is the basis of hard-link semantics.

## 10.3 Dentry versus inode

### Dentry

Represents a name relationship in directory lookup context.

### Inode

Represents filesystem object identity and metadata.

Conceptually:

```text
directory entry name A --┐
                        ├--> inode 123
hard-link name B --------┘
```

There is no inherent “original filename” among hard links. Both names refer to the same inode.

## 10.4 Directories are objects too

A directory is not merely a textual list displayed by `ls`. It is a filesystem object that participates in pathname resolution and maps names to objects according to filesystem semantics.

This is why operations such as rename, link, unlink, and mount interact with directory structure rather than simple string substitution.

## 10.5 `unlink` and open file descriptors

Removing a pathname does not necessarily destroy the underlying object immediately.

Conceptually:

```text
process opens file
    -> fd refers to open kernel file object

another process unlinks pathname
    -> directory entry removed
    -> open fd still refers to object

last reference disappears
    -> storage can finally be reclaimed
```

This explains “deleted but still open” files and why disk space can remain consumed until the owning process closes the descriptor.

Inspect:

```sh
ls -l /proc/$PID/fd
```

## 10.6 Symbolic links

A symlink is a filesystem object containing a pathname target string.

```text
link -> ../real/target
```

When pathname resolution encounters it, lookup continues according to the symlink target.

A symlink can dangle if the target path no longer resolves.

For relocatable bundles, relative symlinks are often more robust than absolute links because moving the tree preserves internal relationships.

## 10.7 Why `No such file or directory` can be misleading

Executing an apparently existing file can report an ENOENT-like error for several reasons:

```text
binary path truly missing
symlink target missing
script shebang interpreter missing
ELF PT_INTERP path missing
```

Therefore the right inspection sequence is:

```sh
ls -l path
readlink -f path
file path
head -n 1 script
readelf -l binary | grep -i interpreter
```

## 10.8 Mounts

A mount attaches a filesystem or tree into the pathname namespace.

Conceptually:

```text
root namespace tree
    /
    ├── data
    ├── proc   <- procfs mounted here
    ├── sys    <- sysfs mounted here
    └── dev    <- device-related filesystems mounted here
```

The single `/` visible to a process can be assembled from many mounted filesystems.

## 10.9 Bind mounts

A bind mount exposes an existing file or directory tree at another point in the mount namespace.

```text
/source/tree
     |
     +-- bind-mounted at /other/view
```

This does not copy bytes. It creates another mount-path view of the same underlying tree.

A symlink and a bind mount can appear similar to a user navigating paths but have different semantics and resolution behavior.

## 10.10 `chroot` versus mount namespace

### `chroot`

Changes the root directory used for pathname resolution by a process and descendants. It is not a complete isolation mechanism by itself.

### Mount namespace

Allows different process groups to see different mount trees.

```text
Process group A
    -> mount topology A

Process group B
    -> mount topology B
```

Container runtimes combine namespaces with other kernel mechanisms. PRoot provides a different userspace-mediated model and should not be equated with a kernel mount namespace.

## 10.11 `/proc`

`/proc` is a pseudo-filesystem exposing live kernel/process state.

Examples:

```text
/proc/<pid>/maps
/proc/<pid>/fd
/proc/<pid>/status
/proc/self/mountinfo
```

These are not ordinary static copies that can be meaningfully packaged as runtime data.

## 10.12 `/sys`

`sysfs` exposes kernel object relationships and attributes.

It often contains many symlinks because it represents relationships among devices, drivers, buses, and kernel objects.

A path in `/sys` is an interface into live kernel state, not just a configuration file to copy into a bundle.

## 10.13 `/dev`

Device nodes provide pathname access to kernel device interfaces.

Conceptually:

```text
open device node
    -> fd
    -> read/write/mmap/ioctl
    -> kernel driver/subsystem
```

Creating a filename that looks like a device node does not grant access to a real device. Access depends on kernel object existence, permissions, Android sandboxing, SELinux policy, and other security controls.

## 10.14 PTYs and `/dev/pts`

A pseudoterminal has master/slave endpoints.

Conceptually:

```text
terminal emulator / controlling side
    <-> PTY master
    <-> PTY slave
    <-> shell/application
```

The shell sees a terminal-like device, while another process controls the corresponding master side.

This model explains why terminal input/output and job control differ from plain pipes.

## 10.15 Object-type classification before copying

When reconstructing a runtime, classify every referenced path:

```text
regular file
symlink
directory
Unix socket
device node
procfs interface
sysfs attribute
runtime-generated cache
```

Only the first few are ordinary package payload candidates. Copying a Unix socket pathname, `/proc` entry, or device node placeholder does not reproduce the underlying service or kernel object.

## 10.16 PRoot and rootfs semantics

A rootfs directory tree provides files and paths, but a complete runtime also depends on:

```text
/proc views
/sys views
/dev access
network
IPC endpoints
permissions
kernel UAPI
service availability
```

This is why “copy the Debian rootfs” and “reproduce Debian behavior” are different goals.

PRoot can mediate pathname and process behavior to present a useful environment, but the project’s native runtime path instead reconstructs selected contracts directly.

## 10.17 Project connection: relocation and absolute paths

Relocation can fail even when ELF search paths are correct.

Examples:

```text
absolute symlink points into /usr/lib
plugin metadata points to /usr/lib/plugin
config hardcodes /etc/foo
script shebang uses unavailable interpreter
resource loader expects /usr/share/app
```

Therefore a relocation audit must include the filesystem/object graph, not only ELF metadata.

## 10.18 Practical exercises

```sh
# Inode identities and hard links
ls -li file1 file2

# Symlink chain
readlink link
readlink -f link

# Mount topology
findmnt
cat /proc/self/mountinfo

# Filesystem types
stat -f .
stat -f /storage/emulated/0 2>/dev/null || true

# Object type
file path
stat path
```

## References

- Linux kernel VFS documentation: <https://docs.kernel.org/filesystems/vfs.html>
- Linux kernel filesystems documentation: <https://docs.kernel.org/filesystems/>
- Linux man-pages, `mount_namespaces(7)`: <https://man7.org/linux/man-pages/man7/mount_namespaces.7.html>
- Linux man-pages, `proc(5)`: <https://man7.org/linux/man-pages/man5/proc.5.html>
- Termux execution environment: <https://github.com/termux/termux-packages/wiki/Termux-execution-environment>
