# 0012 — Post-Refactor VS Code / libdbus ABI Regression

## Context

After Phase B structural deployment passed, the first real VS Code workload probe failed:

```text
grep: /proc/version: Permission denied
$HOME/gl/apps/vscode/code:
    symbol lookup error:
    $HOME/gl/lib/libdbus-1.so.3:
    undefined symbol: __vsyslog_chk, version GLIBC_2.17
```

The structural migration itself had already passed:

- repository-owned link topology;
- runtime payload preservation;
- shell syntax;
- command resolution;
- isolated gl environment contract;
- glibc compiler wrapper execution.

Therefore this incident is tracked as a workload/runtime-drift regression, not yet as a refactor ownership regression.

## Concurrent untracked changes

Two external changes occurred around the same period and were not independently captured before the workload probe:

1. the Termux glibc package was updated;
2. VS Code's in-application update action had been used, but the resulting payload mutation/version transition was not recorded.

The diagnosis must separate those changes.

## External package context

The `termux-pacman/glibc-packages` repository bumped `gpkg/glibc` from 2.42 to 2.43 on 2026-07-08.

The package build replaces upstream `misc/syslog.c` with a custom Android-log implementation. The current custom source contains definitions for `__syslog_chk` and `__vsyslog_chk`, while the conventional glibc version map exports those fortified syslog symbols.

The device failure therefore requires direct installed-binary inspection rather than assuming the source definition was exported correctly by the installed 2.43 build.

## Current working hypotheses

### H1 — glibc 2.43 package export regression

The installed `$PREFIX/glibc/lib/libc.so.6` may not export:

```text
__vsyslog_chk@GLIBC_2.17
```

although the Debian farm `libdbus-1.so.3` requires it.

This is the highest-priority hypothesis because the failing relocation is directly between the Debian farm library and the glibc core.

### H2 — farm library drift

The Debian rootfs or `gl-farm` may now expose a newer/different `libdbus-1.so.3` than the one used during the original VS Code validation.

This requires package identity, symlink target, build ID, and symbol-version requirement capture.

### H3 — VS Code payload update changed dependency activation

The updated VS Code payload may load D-Bus earlier or along a code path not exercised by the previous payload, revealing a latent core/farm ABI mismatch.

This would make the VS Code update a trigger rather than the root ABI defect.

### H4 — VS Code payload update replaced or partially mutated the application tree

The in-application updater may have changed the payload tree in a way not represented by the package integration record. Version, mtimes, checksums, and payload-local library inventory must be captured.

## Explicit non-actions

Until identity capture is complete, do not:

- rebuild `gl-farm`;
- delete or replace `libdbus-1.so.3`;
- reinstall VS Code;
- downgrade or upgrade glibc again;
- patch the VS Code launcher;
- inject broad `LD_LIBRARY_PATH` state;
- copy a random `libdbus` into the application tree.

These actions would destroy the A/B evidence needed to distinguish core, farm, and payload drift.

## Required capture

### Core glibc identity

Capture installed package version, libc build/version strings, and exported fortified syslog symbols.

### Farm libdbus identity

Capture symlink target, Debian package owner/version, ELF build ID, DT_NEEDED, and required symbol versions.

### VS Code payload identity

Capture CLI/product version metadata, executable mtimes, payload-local D-Bus presence, and package-tree recent changes.

### Loader trace

Use the glibc loader's diagnostic or library trace path to prove which libc and libdbus are selected before attempting any fix.

## Decision status

Open. No remediation is accepted until the core/farm/app identity matrix is captured.
