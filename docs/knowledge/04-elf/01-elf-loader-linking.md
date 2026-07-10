# 8. ELF, Dynamic Loaders, Shared Libraries, and Relocation

ELF is the bridge between build-time artifacts and runtime memory. In this project, many “application compatibility” problems are really questions about ELF metadata, loader selection, library search policy, and ABI coherence.

## 8.1 What ELF is

ELF stands for Executable and Linkable Format. It is used for objects such as:

```text
relocatable object files (.o)
executables
shared objects (.so)
core files
```

An ELF file has several views. Two are especially important:

```text
sections
    -> linker/debugging organization

segments / program headers
    -> runtime loading organization
```

Do not treat section names and runtime mappings as the same abstraction.

## 8.2 Sections versus segments

Typical sections include:

```text
.text
.rodata
.data
.bss
.dynsym
.dynstr
.rela.*
.debug_*
```

Runtime-relevant program-header entries include concepts such as:

```text
PT_LOAD
PT_INTERP
PT_DYNAMIC
```

The kernel and dynamic loader care about program-header/runtime mapping information. Linkers and debugging tools also use section-level organization.

Inspect:

```sh
readelf -S app    # sections
readelf -l app    # program headers/segments
```

## 8.3 The ELF interpreter

A dynamically linked executable can declare an interpreter path.

Conceptually:

```text
execve(app)
    -> kernel reads ELF
    -> PT_INTERP says which dynamic loader to use
    -> loader maps dependencies and relocates program
    -> startup code eventually reaches main
```

Typical worlds differ:

```text
Android/bionic
    -> Android dynamic linker path

glibc AArch64 Linux
    -> ld-linux-aarch64.so.1-style loader path
```

The exact path encoded in the file is decisive. A file can exist and have execute permission yet fail with “No such file or directory” if its ELF interpreter path cannot be resolved.

## 8.4 `DT_NEEDED`

The dynamic section can declare required shared-object names:

```text
app
  DT_NEEDED libfoo.so.1
  DT_NEEDED libc.so.6
```

Inspect:

```sh
readelf -d app | grep NEEDED
```

This is a graph edge, not a full path. The loader must resolve the name according to its search policy and runtime context.

## 8.5 SONAME and library filenames

A common library layout is:

```text
libfoo.so           -> linker/development name
libfoo.so.1         -> ABI major / SONAME-facing name
libfoo.so.1.2.3     -> concrete implementation file
```

The shared object can contain:

```text
SONAME: libfoo.so.1
```

An application linked against it may record:

```text
DT_NEEDED: libfoo.so.1
```

This separates ABI identity from the exact implementation filename.

## 8.6 RPATH, RUNPATH, and `$ORIGIN`

The loader needs search policy.

A relocatable bundle can use a path relative to the object location:

```text
$ORIGIN/../lib
```

Example topology:

```text
app-root/
├── bin/app
└── lib/libfoo.so.1
```

If `bin/app` carries an appropriate `$ORIGIN`-relative search path, the bundle can move as a unit without encoding one absolute home-directory path.

The exact precedence semantics of RPATH and RUNPATH differ, so inspect the actual tag rather than treating the names as interchangeable.

## 8.7 Why broad `LD_LIBRARY_PATH` is risky

An environment-wide search path can affect every compatible dynamic process inheriting it.

In a mixed bionic/glibc Termux environment, this can cause one ABI world to discover incompatible objects from another world.

A more deterministic strategy is:

```text
application-local $ORIGIN paths
    + coherent loader configuration
    + narrowly scoped launch policy
```

rather than:

```text
global LD_LIBRARY_PATH containing everything
```

## 8.8 Symbols: definitions and requirements

One object can define a symbol:

```text
libfoo.so
    defines foo_init
```

Another can require it:

```text
app
    UND foo_init
```

Inspect:

```sh
readelf -Ws app
nm -D app
```

A successful library-name resolution does not guarantee symbol compatibility.

Possible failure layers:

```text
library not found
    -> discovery failure

library found, symbol absent
    -> symbol provider mismatch

symbol name found, version mismatch
    -> versioned ABI incompatibility

symbol resolution succeeds, runtime object contract differs
    -> semantic ABI failure
```

## 8.9 Symbol versioning

Symbols can be associated with versions such as:

```text
GLIBC_2.xx
GLIBCXX_3.4.xx
CXXABI_x.y
```

The same apparent library filename can differ in the versioned symbol capabilities it provides.

Inspect:

```sh
readelf --version-info app
objdump -T libfoo.so
```

This is why copying “a libc.so.6” or “a libstdc++.so.6” by filename alone is not a coherent runtime strategy.

## 8.10 Relocation

At build time, final runtime addresses may be unknown. Relocation records describe adjustments that the linker or runtime loader must apply.

Conceptually:

```text
object code contains reference to symbol foo
    -> final address unknown
    -> relocation record describes how to fix reference
    -> linker/loader determines actual address
    -> reference becomes usable
```

Inspect:

```sh
readelf -r app
```

Relocation is broader than “change RUNPATH.” The project uses the word in a deployment sense too, where moving an upstream application can require normalizing:

```text
ELF interpreter
RUNPATH/RPATH
absolute symlinks
shebangs
resource paths
plugin directories
configuration
launch environment
```

## 8.11 PIC and PIE

Position-independent code supports placement at varying virtual addresses without requiring extensive text rewriting.

Conceptually:

```text
shared object
    -> can be mapped at different base addresses
    -> code uses position-independent addressing strategies
```

PIE extends similar ideas to executables, supporting address-space randomization and flexible placement.

## 8.12 Startup is earlier than `main`

The entry point is not necessarily `main`.

A simplified startup path:

```text
ELF entry
    -> loader/runtime startup
    -> relocation and constructors
    -> libc startup
    -> main
    -> exit/destructors
```

Therefore an application can crash before `main`, for example during:

```text
dynamic relocation
global constructors
plugin initialization
runtime startup
```

This is important when debugging C++ and Electron-adjacent native components.

## 8.13 `patchelf`: what it can and cannot do

`patchelf` can modify selected ELF metadata such as:

```text
interpreter
RPATH/RUNPATH-like fields
NEEDED relationships
SONAME-related metadata
```

It cannot transform the semantics of one ABI into another.

Changing:

```text
PT_INTERP from glibc loader to Android linker
```

would not make glibc symbol and runtime assumptions disappear.

Use `patchelf` as a metadata-rewriting tool inside a coherent runtime design, not as an ABI converter.

## 8.14 Project relocation checklist

For every foreign application ELF tree:

```text
1. classify every ELF object by architecture and ABI world;
2. inspect interpreter of executable files;
3. inspect NEEDED edges recursively;
4. preserve application-local $ORIGIN topology;
5. inspect symbol-version requirements;
6. verify no bionic/glibc cross-loading;
7. observe runtime dlopen behavior;
8. validate actual mappings;
9. validate feature-level behavior separately from startup.
```

## 8.15 Practical commands

```sh
file app
readelf -h app
readelf -l app
readelf -d app
readelf -Ws app
readelf -r app
readelf --version-info app

patchelf --print-interpreter app
patchelf --print-rpath app
```

For a running process:

```sh
cat /proc/$PID/maps
```

Compare what the ELF declares with what the process actually mapped.

## References

- System V ABI / ELF gABI reference: <https://refspecs.linuxfoundation.org/elf/gabi4+/contents.html>
- GNU C Library manual: <https://sourceware.org/glibc/manual/>
- `patchelf` project: <https://github.com/NixOS/patchelf>
- Arm ABI specifications: <https://github.com/ARM-software/abi-aa>
- Project glibc layer guide: [`../../glibc-layer.md`](../../glibc-layer.md)
