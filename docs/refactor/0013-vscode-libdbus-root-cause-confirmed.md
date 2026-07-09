# 0013 — VS Code / libdbus Root Cause Confirmed

## Confirmed failure chain

The device captured the active runtime identity after the first VS Code workload failure.

```text
Termux glibc package: 2.43
libc: $PREFIX/glibc/lib/libc.so.6
farm libdbus: Debian rootfs libdbus-1.so.3.38.3
libdbus Build ID: f7d07c8924acc61f4014b2998e2180c90c660f32
VS Code payload version: 1.127.0
```

The active `libdbus-1.so.3` requires:

```text
__vsyslog_chk@GLIBC_2.17
```

The installed Termux glibc 2.43 `libc.so.6` exports:

```text
syslog@@GLIBC_2.17
vsyslog@@GLIBC_2.17
__syslog_chk@@GLIBC_2.17
```

but does **not** export:

```text
__vsyslog_chk@GLIBC_2.17
```

## VS Code excluded as root cause

The same relocation failure reproduces without VS Code:

```text
$PREFIX/glibc/bin/ldd -r <resolved farm libdbus>
    undefined symbol: __vsyslog_chk, version GLIBC_2.17
```

Loader selection for the VS Code executable confirms:

```text
libdbus-1.so.3 -> $HOME/gl/lib/libdbus-1.so.3
libc.so.6      -> $PREFIX/glibc/lib/libc.so.6
```

Therefore the primary failure boundary is:

```text
Debian farm libdbus
    requires __vsyslog_chk@GLIBC_2.17
        -> Termux glibc core does not export it
```

The VS Code update may have changed workload behavior or timing, but it is not required to reproduce the ABI failure and is not the root cause.

## Source-level defect

The Termux glibc package replaces upstream `misc/syslog.c` with a custom Android-log implementation.

The custom implementation currently defines:

```c
void __vsyslog_chk(int pri, int flag, const char *fmt, va_list ap) {
    __vsyslog_internal(pri, fmt, ap, (flag > 0) ? PRINTF_FORTIFY : 0);
}
```

The upstream glibc implementation uses the long-double/export alias contract:

```c
void
___vsyslog_chk (...)
{
    ...
}
ldbl_hidden_def (___vsyslog_chk, __vsyslog_chk)
ldbl_strong_alias (___vsyslog_chk, __vsyslog_chk)
```

The custom source already follows this pattern for `__syslog_chk` but not for `__vsyslog_chk`.

This asymmetry exactly matches the installed dynamic symbol table: `__syslog_chk` is exported while `__vsyslog_chk` is absent.

## Important historical qualification

The same custom source content was already present in the glibc 2.42 package source snapshot. Therefore the evidence does not prove that the source-level defect was introduced by the 2.43 version bump itself.

The accurate conclusion is:

> The custom implementation violates the upstream alias/export pattern, and the currently installed 2.43 build exposes the violation as a missing dynamic ABI symbol.

Explaining why the previous working environment did not fail requires an old installed libc binary or package artifact for comparison. Do not infer that from source history alone.

## Proposed upstream fix shape

Change the custom Android-log implementation to mirror upstream export glue:

```c
void ___vsyslog_chk(int pri, int flag, const char *fmt, va_list ap) {
    __vsyslog_internal(pri, fmt, ap, (flag > 0) ? PRINTF_FORTIFY : 0);
}
ldbl_hidden_def(___vsyslog_chk, __vsyslog_chk)
ldbl_strong_alias(___vsyslog_chk, __vsyslog_chk)
```

Then rebuild glibc and require these gates before installation acceptance:

```text
readelf dynsym contains __vsyslog_chk@GLIBC_2.17
farm libdbus ldd -r has no undefined symbols
VS Code CLI probe succeeds
```

## Workstation regression gates

Two read-only tests are added:

```text
modules/gl/tests/core-abi.sh
    verifies the required glibc core export

modules/gl/tests/farm-libdbus-relocation.sh
    verifies the real farm libdbus relocates against the active core
```

These tests make external runtime drift visible independently of VS Code.

## Recovery policy

Preferred order:

1. inspect whether a known previous glibc package artifact is available locally;
2. if available, inspect its `libc.so.6` symbol table before installing or downgrading;
3. otherwise build a corrected glibc package with the alias/export fix;
4. use a targeted compatibility shim only as a reversible diagnostic or emergency workaround, not as the architectural fix;
5. do not rebuild `gl-farm` or reinstall VS Code to address this root cause.
