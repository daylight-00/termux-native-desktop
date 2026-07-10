# 0021 — glibc 2.42 Downgrade Simulation Passed

## Status

A non-mutating APT transaction simulation was run after the exact `glibc=2.42` artifact had been downloaded and its binary ABI compared with the active 2.43 substrate.

The simulation shows a bounded one-package downgrade transaction.

## Current package state

```text
glibc                    2.43    aarch64
linux-api-headers-glibc  7.1     aarch64
```

APT dependency health before simulation completed without reported broken or unmet dependencies.

## Version availability

APT policy reports:

```text
glibc:
    installed 2.43
    candidate 2.43
    available 2.42

linux-api-headers-glibc:
    installed 7.1
    candidate 7.1
    available 6.18.7
```

The simulation did not request a linux-api-headers-glibc downgrade.

## Installed reverse-dependency context

The installed package graph contains multiple reverse dependencies on `glibc`, including:

```text
zlib-glibc
vulkan-icd-loader-glibc
termux-exec-glibc
tar-glibc
perl-glibc
ncurses-glibc
libxshmfence-glibc
libxcrypt-glibc
libuuid-glibc
libunistring-glibc
libsmartcols-glibc
libnghttp2-glibc
liblzma-glibc
liblz4-glibc
libjansson-glibc
libffi-glibc
libexpat-glibc
libcap-ng-glibc
libbz2-glibc
libblkid-glibc
json-c-glibc
grep-glibc
glibc-runner
gcc-libs-glibc
findutils-glibc
brotli-glibc
binutils-libs-glibc
attr-glibc
```

Despite this graph, APT found the exact 2.42 downgrade satisfiable without changing those packages.

## Simulated transaction

Command class:

```text
apt-get --simulate --verbose-versions install glibc=2.42
```

APT result:

```text
The following packages will be DOWNGRADED:
    glibc (2.43 => 2.42)

0 upgraded
0 newly installed
1 downgraded
0 to remove
0 not upgraded
```

Operation set:

```text
Inst glibc [2.43] (2.42 termux-glibc glibc:glibc [aarch64])
Conf glibc (2.42 termux-glibc glibc:glibc [aarch64])
```

No `Remv` operation appeared.

No dependency-breakage, unmet-dependency, or conflict diagnostic appeared.

## Decision consequence

The rollback blast radius is currently bounded to the `glibc` package itself according to APT simulation.

Combined with the binary A/B evidence:

```text
glibc 2.42:
    __vsyslog_chk@@GLIBC_2.17 PRESENT

glibc 2.43:
    __vsyslog_chk@@GLIBC_2.17 ABSENT
```

the exact 2.42 package is now a justified temporary incident-recovery candidate.

## Recovery policy

The recovery is not treated as a permanent architecture decision or a rejection of latest-first maintenance.

It is classified as:

```text
incident recovery:
    restore a binary artifact with the required ABI

long-term direction:
    move to a corrected current/newer substrate after equivalent gates pass
```

## Required pre-change conditions

Before active downgrade:

```text
1. preserve exact glibc_2.42_aarch64.deb outside temporary storage
2. verify artifact SHA-256
3. record current active glibc package version
4. record current active libc Build ID and SHA-256
5. keep the exact recovery gate sequence ready
```

Expected exact artifact SHA-256:

```text
59e47a50b77ba9c0c1cc7cd0dafbb1558528cb544a740858faad0263e8b9b27f
```

Expected 2.42 libc Build ID:

```text
0b0a4cdb97355daecdb91d2915f61215924104c8
```

## Required post-change gates

After package-managed downgrade:

```text
1. dpkg package identity == glibc 2.42
2. active libc Build ID == 0b0a4cdb97355daecdb91d2915f61215924104c8
3. modules/gl/tests/core-abi.sh PASS
4. modules/gl/tests/farm-libdbus-relocation.sh PASS
5. code --version succeeds
6. real VS Code GUI workload is validated separately when display/session context is ready
7. exact transaction and outputs are recorded
```

Do not rebuild the broad farm before these gates. The purpose is to isolate substrate recovery from provider mutation.

## Current incident state

```text
BLOCKED_SUBSTRATE
```

with a validated bounded recovery candidate and a ready post-change validation plan.
