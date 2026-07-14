# 3. Package Managers, Bootstrap, Prefixes, and Root Filesystems

The original `pacman` question is a useful starting point because package management sits at the boundary between “a program is a file” and “a system is managed state.”

## 3.1 Installing software is more than copying a binary

A real installation can involve:

```text
executables
shared libraries
configuration
service definitions
icons and desktop files
documentation
fonts or schemas
plugin metadata
package ownership records
post-install actions
```

A package manager therefore needs to reason about both **artifacts** and **state**.

A useful model is:

```text
repository metadata
    -> dependency solution
    -> package archives
    -> filesystem transaction
    -> package database update
```

The package database answers questions that a raw tar extraction cannot:

```text
Which package owns this file?
Which version is installed?
Which packages depend on this package?
What should be removed during uninstall?
What should be upgraded together?
```

## 3.2 `apt`, `dpkg`, `pacman`, and `libalpm`

On Debian-family systems, a simplified relationship is:

```text
APT
    -> repository metadata and package selection
    -> dependency solving and acquisition
    -> drives dpkg operations

dpkg
    -> Debian package archive handling
    -> unpack/configure/remove
    -> local package state database
```

On Arch-family systems:

```text
pacman
    -> command-line package manager
    -> repository synchronization
    -> dependency handling
    -> install/remove/upgrade transactions
    -> local package database

libalpm
    -> package-management library used by pacman
```

The official pacman manual describes pacman as tracking installed packages, supporting dependencies, groups, install/remove scripts, and repository synchronization; it also identifies pacman as a frontend to `libalpm`.

## 3.3 Why installing pacman does not turn Termux into Arch Linux

A package manager is only one component of a distribution environment. Installing a `pacman` executable does not replace:

```text
repository set
package build assumptions
filesystem layout
libc ABI
toolchain conventions
service model
configuration policy
```

Likewise, installing `apt` in an unrelated prefix does not make that prefix Debian.

A distribution is an integrated contract among packages, build policy, dependency metadata, filesystem conventions, ABI expectations, and update policy.

## 3.4 Why mixing package managers in one prefix is dangerous

Suppose two managers share the same installation tree:

```text
Manager A database says:
/usr/lib/libfoo.so belongs to package A-foo

Manager B database says:
/usr/lib/libfoo.so belongs to package B-foo
```

Neither database automatically understands the other manager’s transaction.

Possible failure modes:

- one manager overwrites a file owned by the other;
- one upgrades a shared dependency without the other knowing;
- one removes a file the other still assumes exists;
- dependency databases diverge from filesystem reality.

The problem is not that two executable commands exist. The problem is **multiple authorities over one mutable filesystem state**.

## 3.5 Repository: archive storage plus metadata

A repository is not merely a directory of downloadable archives. It also exposes metadata such as:

```text
package names
versions
architectures
dependencies
conflicts
checksums/signatures
file indexes
```

`apt update` and `pacman -Sy`-style operations primarily update local repository metadata. Actual package upgrade is a different transaction.

The distinction is:

```text
refresh catalog
    !=
change installed filesystem state
```

## 3.6 Package archive versus installed state

A package archive is an input artifact. Installed state is the result of applying it under a particular package manager and environment.

For a Debian binary package, the high-level structure is:

```text
package.deb
├── debian-binary
├── control.tar.*
└── data.tar.*
```

The payload tree and control metadata are separate. Installation can also involve maintainer scripts and package-manager triggers, so “extract the payload” and “install the package” are intentionally different operations.

## 3.7 Bootstrap: the chicken-and-egg problem

A package-managed environment needs a package manager, but the package manager itself requires libraries, shell tools, certificates, configuration, and a filesystem layout.

The answer is a **bootstrap**: a minimal initial environment sufficient to grow itself.

Conceptually:

```text
small trusted initial filesystem
    -> package manager can run
    -> repositories become usable
    -> more packages are installed
    -> environment grows
```

This is the same general pattern whether discussing a Termux bootstrap archive, Debian bootstrapping, language runtime bootstraps, or compiler bootstrapping.

## 3.8 Root filesystem and `minbase`

A Debian rootfs produced by a minimal bootstrap is not equivalent to a full desktop installation.

A minimal rootfs may provide enough for:

```text
shell basics
libc/runtime
package database
APT/dpkg
essential command-line tools
```

while lacking:

```text
fonts
desktop schemas
GUI libraries
D-Bus session integration
X11 tools
media codecs
```

This explains why a minbase PRoot environment can successfully install packages while initially having no coherent desktop font environment.

## 3.9 Bootstrap versus image versus installer

These terms solve different problems.

### Bootstrap

A minimal seed from which the environment can grow.

### Rootfs archive

A serialized filesystem tree.

### Installer

A workflow that chooses, lays out, configures, and activates an environment.

### Package repository

A source of versioned package artifacts and metadata.

A project can use a rootfs archive without treating it as the runtime, or use a package repository only as a supply source.

## 3.10 The project’s package-management strategy

The project uses package managers in more than one role.

### Native host management

Termux package management owns the native bionic prefix and related packages.

### Debian supply environment

APT/dpkg inside the Debian rootfs provide:

- dependency solving;
- package metadata;
- a reproducible source of Debian-built artifacts;
- a known-good reference environment.

The final glibc application process can then run outside PRoot.

The architectural lesson is:

```text
package manager authority
    can be separated from
runtime execution authority
```

This separation is powerful but demands explicit provenance and runtime validation.

## 3.11 Oracle: a useful engineering concept

An **oracle** in this project is a known-good environment or implementation used to answer questions.

Examples:

```text
Does the app work in ordinary Debian?
Which package installs this file?
Which post-install side effects are expected?
Which plugins are loaded when feature X is used?
```

The oracle is not automatically the architecture to copy. It is a behavioral reference.

A good workflow is:

```text
known-good reference
    -> observe behavior
    -> identify required artifacts and contracts
    -> reconstruct minimal target behavior
    -> validate against reference expectations
```

## 3.12 Practical exercises

On a Debian environment:

```sh
apt-cache depends <package>
dpkg -L <package>
dpkg-query -S /path/to/file
apt-file search <filename>   # when apt-file is available/configured
```

Inspect a `.deb` without installing:

```sh
ar t package.deb
dpkg-deb --info package.deb
dpkg-deb --contents package.deb
dpkg-deb --extract package.deb extracted/
```

Questions:

1. Which information comes from repository metadata?
2. Which information comes from the archive itself?
3. Which installation effects would extraction alone miss?

## References

- Arch pacman manual: <https://man.archlinux.org/man/pacman.8.en>
- Debian Reference, package management: <https://www.debian.org/doc/manuals/debian-reference/ch02.en.html>
- Debian Policy Manual: <https://www.debian.org/doc/debian-policy/>
- `dpkg` project documentation: <https://www.dpkg.org/doc/>
- Project glibc layer guide: [`../../glibc-layer.md`](../../glibc-layer.md)
