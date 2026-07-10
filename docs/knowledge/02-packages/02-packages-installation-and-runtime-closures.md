# 4. From Package Dependencies to Runtime Closures

A package manager answers a distribution-management question. A dynamic loader answers a process-loading question. An application runtime answers an even larger behavioral question. Treating these as the same graph causes many relocation mistakes.

## 4.1 Four increasingly large closures

A useful sequence is:

```text
package closure
    -> ELF startup closure
    -> dynamic runtime closure
    -> end-to-end capability closure
```

### Package closure

All packages required according to package metadata.

```text
app package
    -> libgtk package
    -> libdbus package
    -> fontconfig package
```

This graph can include documentation, development files, service files, and other artifacts never mapped into the application process.

### ELF startup closure

The recursive `DT_NEEDED` graph resolved by the dynamic linker at process startup.

```text
app
    -> libA.so
        -> libB.so
    -> libc.so.6
```

This graph is smaller in one sense but still incomplete.

### Dynamic runtime closure

Add runtime discoveries:

```text
dlopened plugins
GPU drivers
image codecs
TLS providers
native language extensions
helper executables
```

### End-to-end capability closure

Add everything needed for meaningful behavior:

```text
fonts
fontconfig configuration
locale data
CA trust store
D-Bus endpoint
X11 display
Vulkan ICD metadata
GPU device access
network/proxy configuration
resources and schemas
```

This is the level at which “the application works” becomes meaningful.

## 4.2 Why `ldd` is useful and insufficient

`ldd` can help inspect a process’s expected shared-library resolution, but it is not a complete runtime manifest.

It can miss things loaded after startup:

```text
app starts
    -> reads configuration
    -> chooses backend
    -> dlopen("backend.so")
```

It also says nothing by itself about:

- fonts;
- helper executables;
- D-Bus services;
- sockets;
- certificates;
- child-process behavior;
- GPU presentation success.

Therefore:

```text
ldd clean
    !=
application runtime complete
```

## 4.3 Static discovery, dynamic observation, controlled removal

A robust runtime-minimization strategy combines three techniques.

### Static discovery

Inspect:

```text
package dependencies
ELF interpreter
DT_NEEDED
RPATH/RUNPATH
symbol versions
shebangs
absolute paths
plugin metadata
```

### Dynamic observation

Trace or inspect:

```text
open/openat
mmap
dlopen-related loader diagnostics
connect
execve
process tree
/proc/<pid>/maps
/proc/<pid>/fd
```

### Controlled removal

Remove one candidate dependency or capability at a time and rerun validation gates.

This is the difference between **surgical minimization** and accidental under-packaging.

## 4.4 Package installation effects matter

Consider an application whose package contains:

```text
/usr/bin/app
/usr/lib/libapp.so
/usr/share/app/schema.xml
```

A post-install action might additionally:

```text
compile a schema cache
refresh icon cache
update MIME database
create a symlink
register a service
```

Extracting only the payload may leave the runtime incomplete even though every visible ELF dependency exists.

The correct question is:

> What final observable state does the known-good installation produce?

not merely:

> Which files were inside the archive?

## 4.5 Application-local libraries versus shared providers

Many applications ship local libraries intentionally.

Example:

```text
app/
├── app-binary
└── lib/
    ├── libfoo.so
    └── libbar.so
```

A naive relocation step that replaces RUNPATH and removes `$ORIGIN` can cause the application to select a system/farm library instead of the bundled one.

A safer conceptual resolution model is:

```text
application-local libraries
    -> coherent shared runtime core
    -> selected shared provider pool
```

The exact ordering is load-bearing.

## 4.6 Provenance is part of the runtime closure

A runtime file without provenance becomes a future mystery.

For each promoted artifact, record at least:

```text
runtime path
source package/artifact
source version
source path
checksum
transformation
reason for inclusion
validation evidence
```

Example:

```text
runtime: lib/libfoo.so.1
source: Debian package libfoo1 1.2.3-4
source path: /usr/lib/aarch64-linux-gnu/libfoo.so.1.2.3
transform: none
reason: DT_NEEDED by libbar.so.2
validated by: app-smoke, feature-X
```

This is especially important for a mixed-source runtime assembled from upstream tarballs, Termux glibc packages, Debian artifacts, and locally built Mesa components.

## 4.7 Warehouse is not runtime closure

A broad library warehouse is useful for discovery:

```text
Debian rootfs
    -> thousands of possible libraries
```

A promoted runtime should ideally be narrower:

```text
application contract
    -> resolver
    -> selected runtime set
    -> provenance manifest
```

The project’s current broad farm is a productive research mechanism because it enables fast experiments. The long-term architecture should distinguish that candidate pool from a validated runtime closure.

## 4.8 Feature-dependent closures

There may be no single “minimal VS Code runtime.” Instead:

```text
Level 1: process starts
Level 2: window opens
Level 3: editor works
Level 4: GPU process stable
Level 5: extensions work
Level 6: remote tunnel works
Level 7: native extension works
```

Each level can add dependencies and bridges.

Likewise PyMOL may have:

```text
import-only closure
CPU rendering/test closure
X11 GUI closure
OpenGL/Zink closure
scientific plugin closure
```

A runtime contract should state the supported feature set before claiming minimality.

## 4.9 Runtime closure as a graph problem

Model the system with typed edges.

```text
Application --needs-symbol--> SharedObject
Application --dlopens-------> Plugin
Application --execs---------> Helper
Application --connects------> Service
Application --reads---------> Resource
Application --requires------> Capability
Capability  --provided-by---> Provider
```

Typed graphs prevent a common mistake: trying to solve a service problem by copying another `.so`, or trying to solve a GPU path problem by changing package metadata.

## 4.10 A project-oriented onboarding method

A strong onboarding pipeline is:

```text
1. Choose source artifact and record checksum.
2. Establish known-good reference behavior.
3. Extract or build into staging.
4. Inspect all ELF objects.
5. Normalize interpreters and search policy.
6. Preserve app-local library topology.
7. Resolve startup closure.
8. Exercise features and observe dynamic closure.
9. Define required external capabilities.
10. Build repeatable validation gates.
11. Promote only validated artifacts.
```

This pipeline is intentionally more rigorous than “copy missing libraries until the error disappears.”

## 4.11 Practical inspection commands

```sh
# Direct ELF dependencies
readelf -d ./app | grep NEEDED

# Search paths
readelf -d ./app | grep -E 'RPATH|RUNPATH'

# Symbol/version needs
readelf --version-info ./app
readelf -Ws ./app

# Actual loaded objects in a running process
cat /proc/$PID/maps

# File and process discovery
strace -f -e trace=file,process,network ./app
```

Use observations as evidence, not as a substitute for understanding the mechanism.

## References

- Debian Policy Manual: <https://www.debian.org/doc/debian-policy/>
- GNU C Library manual: <https://sourceware.org/glibc/manual/>
- ELF gABI reference: <https://refspecs.linuxfoundation.org/elf/gabi4+/contents.html>
- Project glibc layer guide: [`../../glibc-layer.md`](../../glibc-layer.md)
- Project experiments index: [`../../../experiments/README.md`](../../../experiments/README.md)
