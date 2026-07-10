# 9. Dynamic Linking Deep Dive: GOT, PLT, Binding, `dlopen`, and Symbol Scope

Finding the right `.so` file is only the beginning. A coherent process requires correct symbol providers, version compatibility, controlled lookup scopes, and safe object ownership boundaries.

## 9.1 The address problem

Suppose an application calls `printf`, but `printf` lives in libc.

ASLR and position-independent loading mean libc can be mapped at different virtual addresses across runs.

Therefore the executable cannot simply assume one permanent absolute address.

Dynamic linking solves this through a combination of:

```text
symbol tables
relocation records
GOT
PLT
runtime symbol lookup
```

## 9.2 GOT

The Global Offset Table is, conceptually, a table of runtime-resolved addresses used by position-independent code.

A simplified picture:

```text
application code
    -> GOT slot
    -> runtime address of object/function
```

The loader can relocate table entries according to actual process mappings.

## 9.3 PLT

The Procedure Linkage Table provides call stubs/trampolines for external function calls.

Simplified:

```text
call site
    -> foo@PLT
    -> GOT/resolution path
    -> actual foo implementation
```

The exact instruction sequence is architecture-specific. On AArch64, disassembly may involve branch and address-construction instructions rather than the x86-style patterns found in many tutorials.

## 9.4 Lazy versus immediate binding

### Immediate/eager model

```text
startup
    -> resolve required function bindings
    -> main
```

### Lazy model

```text
startup
    -> leave some function bindings unresolved
    -> first call to foo
    -> runtime resolver finds provider
    -> binding state updated
    -> later calls use resolved target
```

The tradeoff is startup cost versus deferred first-use work and earlier versus later detection of missing bindings.

## 9.5 Symbol lookup is ordered

Suppose several loaded objects define `foo`:

```text
main
libA.so -> foo
libB.so -> foo
plugin  -> foo
```

The dynamic linker does not choose randomly. Lookup follows a defined scope/order relationship influenced by loading topology and flags.

Therefore:

```text
correct filename found
    !=
correct symbol provider selected
```

## 9.6 Symbol interposition

Interposition means one symbol definition can replace or precede another in lookup for eligible calls.

A common conceptual use:

```text
application malloc
    -> tracing wrapper malloc
    -> real next malloc
```

This can support:

```text
logging
profiling
compatibility shims
debug allocators
function wrapping
```

But not every internal call in every library necessarily passes through an externally interposable dynamic symbol path.

## 9.7 `LD_PRELOAD`

`LD_PRELOAD` requests early loading of one or more shared objects, often so their symbols participate early in lookup.

Example conceptual use:

```sh
LD_PRELOAD=/path/to/libhook.so ./app
```

This is powerful and dangerous in a mixed environment.

Global export can affect unrelated children:

```text
shell
├── git
├── ssh
├── Python
└── Electron helpers
```

A project rule should be to use preload narrowly and clear incompatible inherited preload state at foreign-runtime boundaries.

## 9.8 `LD_LIBRARY_PATH` versus `LD_PRELOAD`

They solve different problems.

```text
LD_LIBRARY_PATH
    -> where library names may be searched

LD_PRELOAD
    -> which additional objects are loaded early and can affect lookup
```

Both can produce process-wide side effects when inherited broadly.

## 9.9 `dlopen`

Applications can load shared objects at runtime:

```c
handle = dlopen("plugin.so", flags);
```

Conceptually:

```text
running process
    -> locate object
    -> map object
    -> load dependencies
    -> resolve/relocate according to mode
    -> run initialization
    -> return handle
```

This is why static `DT_NEEDED` inspection cannot prove complete runtime closure.

Examples of runtime-loaded components:

```text
Qt platform plugins
GTK modules
Vulkan ICD drivers
image codecs
TLS backends
Python extension modules
Node native addons
application plugins
```

## 9.10 `dlsym`

`dlsym` performs runtime name-based symbol lookup.

Conceptually:

```text
handle + "symbol-name"
    -> dynamic linker lookup
    -> address result
```

Special lookup concepts such as “default scope” and “next provider after this wrapper” are useful in plugin systems and interposition wrappers.

## 9.11 `RTLD_LOCAL` and `RTLD_GLOBAL`

A dynamically loaded object can participate in different symbol-visibility scopes.

Simplified mental model:

```text
RTLD_LOCAL
    -> object group available for its own resolution context
    -> symbols not broadly exported into later global lookup

RTLD_GLOBAL
    -> symbols can participate in later global resolution
```

Global loading can create contamination when plugins expect private dependency versions but encounter already-visible symbols from another component.

## 9.12 Directory isolation is not namespace isolation

Suppose:

```text
app/lib/libfoo.so.1
plugin/lib/libfoo.so.1
```

Simply storing them in different directories does not guarantee that one process will maintain independent symbol universes.

The dynamic loader considers object identity, SONAME relationships, loading history, dependency graphs, and symbol scopes.

Therefore:

```text
directory separation
    !=
linker namespace separation
```

This is a major reason plugin dependency conflicts are hard.

## 9.13 Link namespaces

glibc exposes mechanisms such as `dlmopen` that can construct separate link-map namespaces.

Conceptual view:

```text
one process address space
├── namespace A
│   ├── main
│   └── dependency set A
└── namespace B
    ├── plugin
    └── dependency set B
```

This can isolate symbol-resolution domains, but it is not process isolation.

The process still shares broad process-level resources such as:

```text
address space
credentials
file descriptor table
signals
kernel process identity
```

Cross-namespace object ownership can still be unsafe.

## 9.14 Semantic ABI boundaries

Consider values crossing a library boundary.

Relatively simple:

```text
integer
fixed-size byte buffer
file descriptor
well-defined plain C struct
```

Potentially dangerous across incompatible runtimes:

```text
FILE *
allocator-owned pointer
pthread_mutex_t
locale object
C++ STL container
C++ exception
RTTI object
```

Why? These can encode private runtime representation and ownership semantics.

A `FILE *` created by one libc is not merely an integer fd. It represents a userspace stdio object with buffering and internal state.

## 9.15 Why two libc implementations in one process are dangerous

libc is not just a bag of independent functions. It owns or coordinates:

```text
allocator state
thread/runtime internals
TLS
stdio objects
locale state
exit handlers
resolver behavior
dynamic-loader relationships
```

Accidental cross-calls or object ownership transfer can create failures even when every symbol name resolves.

This supports the project invariant:

```text
each process remains in one coherent ABI world
```

and cross-world integration occurs through explicit bridges.

## 9.16 Runtime coherence checklist

When a library graph appears to resolve, ask:

```text
1. Which loader is in control?
2. Which libc family is mapped?
3. Are duplicate low-level runtimes present?
4. Which provider supplies each versioned symbol?
5. What does the plugin system dlopen later?
6. Which objects are RTLD_GLOBAL?
7. Do allocator/runtime-owned objects cross boundaries?
8. Do child processes inherit dangerous loader variables?
```

## 9.17 Tool layering

```text
readelf
    -> declared ELF structure

loader diagnostics
    -> search and binding behavior

/proc/<pid>/maps
    -> actual mapped objects

strace
    -> file/open/mmap/exec/connect kernel-boundary events

GDB
    -> process memory, registers, call stacks, symbols
```

Use all layers together when necessary.

## 9.18 Project connection

The glibc runtime should be understood as a **coherent dynamic-linking universe**, not a directory containing `libc.so.6`.

A robust world includes:

```text
selected ELF interpreter
coherent low-level runtime set
deterministic search topology
controlled app-local libraries
runtime plugin closure
controlled symbol scope
child-process environment policy
```

The design objective is not “make `ldd` green.” It is “make every process runtime graph coherent.”

## References

- GNU C Library manual: <https://sourceware.org/glibc/manual/>
- POSIX `dlopen`: <https://pubs.opengroup.org/onlinepubs/9699919799/functions/dlopen.html>
- POSIX `dlsym`: <https://pubs.opengroup.org/onlinepubs/9699919799/functions/dlsym.html>
- glibc linker namespace notes: <https://sourceware.org/glibc/wiki/LinkerNamespaces>
- ELF gABI reference: <https://refspecs.linuxfoundation.org/elf/gabi4+/contents.html>
