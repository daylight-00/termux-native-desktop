# 14. Packaging, Distribution Formats, and Runtime Contracts

A build artifact becomes useful to others only after distribution and runtime assumptions are managed. Different package formats solve different problems.

The key question is:

> **What does this format bundle, and what does it expect the host to provide?**

## 14.1 Build, package, install, runtime

Keep the stages separate:

```text
source
    -> build
    -> artifacts
    -> package/bundle
    -> install/materialize
    -> runtime execution
```

A build can succeed while packaging is incomplete. Installation can succeed while runtime loading fails. Runtime loading can succeed while a feature-level capability is missing.

## 14.2 Tarball

A tar archive primarily preserves and transports a filesystem tree.

```text
app/
├── bin
├── lib
├── share
└── README
    -> app.tar.zst
```

A tarball does not inherently provide:

```text
dependency solving
file ownership database
upgrade transactions
uninstall policy
service integration
```

A tarball can still be an excellent distribution format for a project-controlled application-local runtime.

## 14.3 Archive format is not runtime completeness

A file named:

```text
app.tar.zst
```

says how bytes are packaged, not whether the package is self-contained.

The archive may contain one ELF binary that still requires:

```text
system glibc
GTK/Qt
fonts
D-Bus
X11
GPU drivers
CA certificates
```

Always separate:

```text
container/archive format
    from
runtime contract
```

## 14.4 Debian package

A `.deb` is intended for Debian package-system integration.

Conceptually:

```text
payload files
control metadata
package relationships
maintainer scripts/triggers
```

A Debian application package often assumes:

```text
Debian filesystem layout
Debian dependency packages
Debian glibc userspace
system data locations
service/desktop integration conventions
```

Extracting a `.deb` produces payload files, not an automatically portable application bundle.

## 14.5 System package model

```text
App A ----┐
App B ----+--> shared system libfoo
App C ----┘
```

Advantages:

```text
shared storage
central security updates
package ownership
coordinated dependency policy
```

Tradeoffs:

```text
ABI coupling
system-wide upgrade effects
version conflicts
host integration assumptions
```

## 14.6 Application-local bundle model

```text
App A/
    -> private dependency set

App B/
    -> different dependency set
```

Advantages:

```text
isolation
predictable deployment
version independence
```

Tradeoffs:

```text
duplication
security update duplication
custom update/uninstall management
```

The project needs an intentional balance between shared coherent providers and app-local closure.

## 14.7 AppImage

AppImage’s design is oriented toward distributing a desktop application in a single executable image-like artifact with application files and bundled dependencies.

It is not a VM. It still depends on the host kernel, CPU architecture, display/device environment, and other compatibility boundaries.

The project’s extraction of an AppImage can be understood as using AppImage as an **input adapter**:

```text
AppImage
    -> extract embedded application tree
    -> inspect and normalize ELF/runtime assumptions
    -> integrate with project glibc world
```

## 14.8 Flatpak

A simplified Flatpak model:

```text
application
    -> shared runtime
    -> host kernel/system integration
```

It also provides sandbox and portal concepts.

The architectural lesson useful to this project is separation among:

```text
application payload
shared runtime/provider layer
sandbox/bridge policy
host integration
```

The project does not need to become Flatpak to learn from this decomposition.

## 14.9 Snap

Snap combines packaged application images with a management ecosystem involving confinement, interfaces, revisions, and updates.

Again, the useful lesson is that package artifact format and lifecycle/control plane are separate concerns.

## 14.10 Python wheel

A wheel is a Python distribution artifact.

Pure Python wheel:

```text
Python modules
metadata
package data
```

Native wheel can additionally contain:

```text
ELF extension module
```

Then compatibility includes:

```text
Python ABI
CPU architecture
libc/platform ABI
external shared libraries
```

A wheel is not a container image. Installing it successfully does not prove its native extension closure is runnable in the target userspace.

## 14.11 `uv`/pip and native ABI

A Python resolver/installer can correctly solve Python metadata while a native extension later fails with:

```text
wrong interpreter
missing .so
symbol version mismatch
wrong architecture
```

Therefore:

```text
language dependency resolution
    !=
native runtime resolution
```

The PyMOL design must decide the target ABI before choosing wheel-oriented distribution mechanics.

## 14.12 Conda package/environment

Conda environments can manage more than Python packages.

A prefix can contain:

```text
bin/
lib/
include/
share/
Python packages
native libraries
executables
```

This makes Conda interesting for scientific applications such as PyMOL.

But a Conda environment is not an OS or VM. It still relies on host kernel interfaces, CPU architecture, graphics/device access, and platform ABI assumptions.

## 14.13 npm package and native addons

An npm package can contain JavaScript plus scripts, resources, and native addons.

A `.node` native addon is loaded as native code into the Node process. Therefore it participates in:

```text
Node ABI/N-API compatibility
CPU architecture
ELF dynamic linking
libc and external dependencies
```

Install scripts can also download or compile binaries, meaning archive contents alone may not represent final installed state.

## 14.14 OCI container image

A container image provides layered userspace filesystem content plus runtime configuration.

A normal container still uses the host kernel:

```text
container userspace
    -> host kernel
```

This differs from both a VM and a PRoot-mediated rootfs. Container runtime behavior depends on kernel namespaces, cgroups, mounts, security policy, and runtime infrastructure.

## 14.15 Runtime contract

A runtime contract is the set of external conditions needed for a supported behavior.

Example:

```text
architecture: AArch64
world: glibc
loader: selected glibc interpreter
libraries: coherent startup + plugin closure
filesystem: resource paths
bridge: X11 endpoint
fonts: usable font provider
GPU: Vulkan ICD + Turnip/KGSL
network: DNS + TLS trust
policy: Electron sandbox/flags
```

Packaging architecture decides which parts are:

```text
bundled
shared providers
host assumptions
external services/bridges
```

## 14.16 Acquisition, transformation, distribution

For every supported application, separate three stages.

### Acquisition

```text
source tarball
official binary tarball
.deb
AppImage
Conda package
wheel
```

### Transformation

```text
build
extract
patch interpreter
normalize RUNPATH
preserve app-local libraries
adapt resources
create bridge shims
```

### Distribution

```text
installer script
tar.zst bundle
runtime manifest
release assets
repository package
```

This decomposition prevents upstream input format from dictating the final project runtime architecture.

## 14.17 Surgical packaging

“Surgical” should mean evidence-driven inclusion, not smallest-possible-by-guessing.

A disciplined loop:

```text
known-good baseline
    -> static dependency analysis
    -> runtime observation
    -> capability definition
    -> remove one candidate
    -> rerun validation
    -> record result
```

The objective is a **proven closure**, not merely a small directory.

## 14.18 Proprietary payload boundary

For licensed or proprietary applications, technical bundling ability and redistribution rights are separate.

A useful architecture can split:

```text
redistributable project runtime/support layer
    +
user-acquired licensed upstream payload
```

An installer can verify, extract, adapt, and validate a user-supplied artifact without redistributing the artifact itself.

This is particularly relevant when considering proprietary Schrödinger-distributed PyMOL payloads.

## 14.19 A project-oriented release pipeline

```text
Acquire
    -> Verify checksum/source identity
    -> Extract/build into staging
    -> Inspect ELF and resources
    -> Resolve runtime contract
    -> Transform deterministically
    -> Validate
    -> Generate manifests
    -> Package release artifact
    -> Promote
```

Keep raw inputs, staging outputs, transformed runtimes, and release artifacts distinct.

## References

- Debian Policy Manual: <https://www.debian.org/doc/debian-policy/>
- AppImage documentation: <https://docs.appimage.org/>
- Flatpak documentation: <https://docs.flatpak.org/>
- Python wheel specification: <https://packaging.python.org/en/latest/specifications/binary-distribution-format/>
- Conda package specification: <https://docs.conda.io/projects/conda-build/en/stable/resources/package-spec.html>
- Node.js C++ addons: <https://nodejs.org/api/addons.html>
- OCI image specification: <https://github.com/opencontainers/image-spec>
