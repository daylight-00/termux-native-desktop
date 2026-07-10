# 0018 — Real-Device glibc Substrate Authority

## Status

This document records Stage 3 real-device authority evidence for the active glibc substrate.

It supersedes the earlier uncertainty about whether pacman, APT/dpkg, or another backend owns the installed device substrate.

Architecture remains backend-neutral; this document identifies the current backend implementation on this device.

## 1. Observed package-manager availability

The device reports:

```text
pkg          $PREFIX/bin/pkg
apt          $PREFIX/bin/apt
apt-get      $PREFIX/bin/apt-get
dpkg         $PREFIX/bin/dpkg
dpkg-query   $PREFIX/bin/dpkg-query
pacman       absent
```

Conclusion:

```text
pacman is not the active device package-manager path
```

Do not install or switch to pacman merely to obtain lifecycle hooks.

## 2. Exact installed-file ownership

The dpkg database reports:

```text
glibc: $PREFIX/glibc/lib/libc.so.6
glibc: $PREFIX/glibc/lib/ld-linux-aarch64.so.1
```

Installed package identity:

```text
status: ii
package: glibc
version: 2.43
architecture: aarch64
```

Conclusion:

> The active glibc substrate on this device is currently owned by the dpkg database and supplied/updated through the Termux APT path.

This is current device authority evidence, not a requirement that the architecture itself become APT-specific.

## 3. Repository and available versions

`apt-cache policy glibc` reports:

```text
Installed: 2.43
Candidate: 2.43

2.43
    https://packages-cf.termux.dev/apt/termux-glibc
    glibc/stable aarch64

2.42
    https://packages-cf.termux.dev/apt/termux-glibc
    glibc/stable aarch64
```

Important consequence:

```text
exact previous version 2.42 is currently repository-addressable
```

No local cached `.deb` was observed under the APT archive cache, but repository availability means the previous artifact can currently be acquired without changing installed state.

This is stronger than the earlier package-cache assumption and should be tested before any downgrade.

## 4. Actual installation/update history

APT history records:

```text
2026-07-04 01:20:38
    apt install termux-tools x11-repo tur-repo glibc-repo

2026-07-04 01:22:14
    apt full-upgrade
    installs glibc 2.42 and the initial glibc package set

2026-07-09 18:15:49
    apt full-upgrade
    upgrades glibc 2.42 -> 2.43
```

The same July 9 transaction also upgraded unrelated native packages and `linux-api-headers-glibc`.

Conclusion:

```text
current substrate update mechanism:
    explicit user-run APT full-upgrade

not:
    pacman transaction
    project-owned substrate installer
```

## 5. Package-owned surface

`dpkg-query -L glibc` confirms the package owns a broad substrate tree under:

```text
$PREFIX/glibc/
```

including:

```text
loader/core runtime
runtime tools such as ldd and ldconfig
headers
configuration files
other substrate files recorded in glibc.list/md5sums
```

This matters because `world.glibc` substrate authority is broader than one `libc.so.6` file.

A future exact-artifact adapter must not silently reduce the substrate identity to a single ELF object.

## 6. Package control-state evidence

Observed dpkg info files:

```text
glibc.conffiles
glibc.list
glibc.md5sums
```

No package-specific files were observed for:

```text
preinst
postinst
prerm
postrm
triggers
```

Observed conffiles:

```text
$PREFIX/glibc/etc/gai.conf
$PREFIX/glibc/etc/locale.gen
```

Interpretation:

```text
direct extraction of data bytes would not reproduce:
    dpkg ownership/status database state
    dependency transaction semantics
    conffile upgrade/merge semantics
    package-level integrity/accounting state

for the currently observed glibc package specifically:
    no package-specific maintainer scripts were present in dpkg info state
```

This narrows, but does not eliminate, the semantic difference between package installation and raw extraction.

## 7. Rollback reality

### What is currently proven

```text
2.42 is still visible in the configured APT repository metadata
APT can address exact package versions
active files are dpkg-owned
```

### What is not yet proven

```text
2.42 binary exports the missing ABI symbol
installing 2.42 would preserve the full currently required dependency set
an exact downgrade simulation is conflict-free
2.42 remains indefinitely retrievable
substrate rollback restores all dependent glibc package compatibility
```

Therefore:

> Repository visibility of 2.42 means exact-artifact inspection is available now; it does not yet prove that downgrade is a valid recovery.

## 8. Immediate minimum-manipulation recovery experiment

Before rebuilding or downgrading, acquire the exact 2.42 artifact without installation and inspect it.

Required experiment:

```text
APT exact-version download
    -> extract to temporary directory
    -> inspect libc Build ID
    -> inspect dynsym/version export for __vsyslog_chk@GLIBC_2.17
    -> compare against active 2.43
```

Decision:

```text
if 2.42 binary exports the required symbol:
    evaluate a simulated exact-version downgrade and dependency impact

if 2.42 binary also lacks the symbol:
    downgrade is not a justified recovery path
    proceed to corrected 2.43 artifact/package validation
```

The source-level defect was already present in the 2.42 source snapshot, so binary inspection is mandatory before inferring that 2.42 is known-good.

## 9. Current backend-neutral architecture mapping

```text
world.glibc
    substrate contract
        |
        +-- current adapter implementation: apt/dpkg-termux-glibc
                observe installed identity through dpkg
                observe available versions through APT metadata
                acquire exact artifact through APT
                update through explicit APT transaction
```

The adapter must expose facts, not take over higher-level correctness policy.

It may own:

```text
installed package identity observation
exact artifact acquisition
update/downgrade transaction execution when explicitly selected
package-file ownership/provenance observation
```

It must not own:

```text
provider compatibility
world purity claim
application closure
capability validation
promotion decision
```

## 10. Current incident state

Current state remains:

```text
BLOCKED_SUBSTRATE
```

because:

```text
active glibc 2.43
    does not export __vsyslog_chk@GLIBC_2.17

active Debian-derived libdbus
    requires __vsyslog_chk@GLIBC_2.17
```

Required recovery completion gate:

```text
1. substrate artifact corrected/replaced
2. core ABI regression gate PASS
3. libdbus relocation regression gate PASS
4. real VS Code workload probe PASS
5. recovery identities and outputs recorded
```

Do not restructure the farm or application launch architecture as part of this recovery.
