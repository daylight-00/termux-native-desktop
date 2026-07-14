# 6. Virtual Memory, Mappings, Storage, and I/O

ELF loading, shared libraries, GPU buffers, file I/O, and crash addresses all become easier to understand once virtual memory and storage are treated as connected layers.

## 6.1 File versus mapped memory

An executable on storage is not executed directly “from the disk” in the naive sense.

A simplified flow:

```text
ELF file on storage
    -> kernel/loader create virtual memory mappings
    -> pages become resident as needed
    -> CPU executes instructions from mapped virtual addresses
```

A process sees a virtual address space. The kernel and hardware memory-management unit translate and protect those addresses.

## 6.2 A conceptual process address space

A simplified layout:

```text
higher addresses

stack
mmap regions
shared libraries
file-backed mappings
anonymous mappings
heap-like allocator arenas
BSS/data
read-only data
code/text

lower addresses
```

Real layouts vary. The purpose of this picture is to separate categories, not predict exact addresses.

## 6.3 Virtual addresses are process-relative views

Two processes can use the same virtual address for unrelated physical memory. Conversely, two processes can map the same underlying file-backed physical page at different virtual addresses.

Therefore:

```text
virtual address
    !=
physical address
```

This is one reason crash reports must identify the process and mapping context.

## 6.4 Pages and page faults

Memory is managed in page-sized units. The actual page size should be inspected on the target rather than assumed:

```sh
getconf PAGESIZE
```

A page fault is not synonymous with a crash. It can be a normal mechanism:

```text
process accesses valid virtual page
    -> page not resident
    -> CPU exception to kernel
    -> kernel supplies page / completes mapping work
    -> execution resumes
```

A fault becomes fatal only when the access cannot be satisfied according to the mapping and protection rules.

## 6.5 File-backed and anonymous mappings

### File-backed mapping

```text
virtual range
    -> bytes backed by file/object
```

Examples include executable code and shared libraries.

### Anonymous mapping

```text
virtual range
    -> no ordinary backing file
```

Commonly used for heaps, stacks, allocators, JIT memory, and shared-memory mechanisms depending on implementation.

Inspect mappings:

```sh
cat /proc/$PID/maps
cat /proc/$PID/smaps
```

`maps` gives the topology; `smaps` adds accounting detail.

## 6.6 ELF segments become mappings

An ELF shared object may result in multiple mappings with different permissions:

```text
r--  metadata/read-only data
r-x  executable code
r--  read-only constants/RELRO region
rw-  writable data
```

This is why a single `.so` appears across multiple lines in `/proc/<pid>/maps`.

## 6.7 Heap and `malloc`

`malloc()` is a userspace allocation API, not a direct synonym for one syscall.

An allocator can manage arenas and request larger memory regions from the kernel when needed.

Conceptually:

```text
application malloc request
    -> allocator checks managed free space
    -> may satisfy immediately
    -> may request/map more memory from kernel
```

This matters for mixed-runtime design: pointers allocated by one allocator/runtime should not be blindly freed through an incompatible allocator/runtime.

## 6.8 Stack

Each thread has a stack used for function-call state, local storage, saved registers, and temporary data according to ABI/compiler choices.

A conceptual call chain:

```text
main
  -> foo
      -> bar
          -> crash
```

can correspond to active stack frames that a debugger attempts to unwind.

The stack is not a complete execution history; returned calls are no longer active frames.

## 6.9 Storage versus RAM

At a high level:

```text
CPU registers/cache
    -> RAM
    -> persistent storage
```

Persistent storage keeps files across power loss. RAM is faster working memory. The kernel uses RAM aggressively to cache file data.

## 6.10 Page cache

A useful model for file reads is:

```text
read()
    -> filesystem/VFS
    -> page cache lookup
        -> hit: serve cached data
        -> miss: storage I/O, fill cache, serve data
```

The page cache explains why the second read of the same file may be much faster and why naive benchmarks can measure cache behavior rather than device behavior.

## 6.11 Buffered writes and dirty data

A simplified buffered write path:

```text
application buffer
    -> write()
    -> page cache modified
    -> page marked dirty
    -> write() may return
    -> later writeback
    -> filesystem/storage
```

Therefore:

```text
write() success
    !=
guaranteed physical persistence on storage media
```

The exact durability contract depends on APIs, filesystem behavior, and lower storage layers.

## 6.12 `fsync` and durability

When durability matters, applications use explicit persistence protocols.

A common conceptual pattern for replacing a critical file is:

```text
write temporary file
    -> flush file data as required
    -> atomic rename into place
    -> flush containing directory metadata when required by durability design
```

The lesson is broader than one API: **visibility in process memory, visibility in page cache, and durable persistence are different milestones.**

## 6.13 `mmap`

`mmap` creates a virtual-memory mapping. For a file-backed mapping:

```text
file/object
    -> mapped into process virtual address range
    -> application accesses through ordinary load/store instructions
```

Mapping a 100 GB file does not mean 100 GB becomes resident in RAM immediately. Virtual mapping size and resident physical memory are different quantities.

## 6.14 Shared libraries and page sharing

Multiple processes using the same shared library can potentially share physical pages for read-only code/data while maintaining separate private writable state.

This is one of the fundamental benefits of shared-library and file-backed mapping models.

## 6.15 `fork`, copy-on-write, and `exec`

A useful conceptual sequence:

```text
parent process
    -> fork-like operation
    -> child initially shares memory pages under copy-on-write semantics
    -> one side writes: private copy created as needed
    -> child execs: old process image replaced by new executable image
```

This explains why process creation does not require eagerly copying the entire parent address space.

## 6.16 VSS, RSS, and PSS

Memory measurements answer different questions.

- **Virtual size (VSS/VSZ):** total virtual address ranges; can greatly exceed resident RAM.
- **RSS:** resident pages charged to the process, including shared pages counted fully in each process view.
- **PSS:** shared pages proportionally divided among users for accounting.

A large virtual mapping is not by itself evidence of large physical-memory use.

## 6.17 Storage location matters in Termux

Build trees and runtime prefixes should live in the private Termux filesystem area, not shared Android storage.

Reasons include:

- execution permissions and mount policy;
- symlink behavior;
- Unix metadata semantics;
- case sensitivity assumptions;
- many-small-file metadata workloads;
- security of executable content.

Use shared storage for exported artifacts, not for the live runtime tree.

## 6.18 Project connection: GPU mappings

A GPU userspace driver may interact with the kernel to allocate/import buffers and map memory.

A crash investigation can connect:

```text
SIGBUS fault address
    -> virtual mapping
    -> mmap creation
    -> backing fd
    -> device/buffer object
    -> preceding ioctl sequence
```

This is much more informative than reasoning from the signal name alone.

## 6.19 Benchmark caution

A storage or runtime benchmark must control:

```text
cold vs warm cache
input size
small-file count
sync behavior
CPU frequency/thermal state
parallelism
background activity
```

For comparing PRoot mediation with a direct glibc runtime, separate at least:

```text
CPU-heavy workload
metadata-heavy workload
small-file I/O workload
large sequential I/O workload
process-spawn workload
```

Otherwise the result cannot identify which mechanism causes the difference.

## References

- Linux kernel VFS documentation: <https://docs.kernel.org/filesystems/vfs.html>
- Linux kernel memory-management documentation: <https://docs.kernel.org/mm/>
- Linux man-pages, `mmap(2)`: <https://man7.org/linux/man-pages/man2/mmap.2.html>
- Linux man-pages, `fsync(2)`: <https://man7.org/linux/man-pages/man2/fsync.2.html>
- Android storage overview: <https://developer.android.com/training/data-storage>
- Termux execution environment: <https://github.com/termux/termux-packages/wiki/Termux-execution-environment>
