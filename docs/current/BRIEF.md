# Current project brief

> Semantic state version: `2026-07-26.01`

## Purpose and operational boundary

`termux-native-desktop` develops a native Termux/glibc workstation while keeping artifact identity, adaptation, provider authority, composition, target population, and activation separate. User Termux remains authoritative for device execution and remote mutation.

## Current provider boundary

```text
claims: 95
Class A/B/C/D: 36 / 52 / 4 / 3
bounded provider roots accepted overall: 31
accepted roots inside the 28-root inventory: 21
open roots inside the 28-root inventory: 7
accepted exact members: 42
included current-scope members: 41
deferred members: 1
composition review: REVIEWED_BLOCKED_INCOMPLETE
selected identity gaps: 1
target population: blocked
activation: blocked
```

ADR 0005 classification now records 95 claims with 24 bounded provider decisions.

The exact project-produced GTK 3.24.49 pair is now accepted atomically for bounded core library linkage:

```text
libgdk-3.so.0.2417.32 -> libgdk-3.so.0
libgtk-3.so.0.2417.32 -> libgtk-3.so.0
```

The pair was built from official GTK 3.24.49 source, packaged together, verified with exact GIR/typelib evidence, and passed a display-free canonical-glibc-loader probe returning `3.24.49 GdkDisplay`. Only the two versioned runtime members and SONAME aliases are provider-authorized. Headers, pkg-config, unversioned aliases, GAIL, tools, `broadwayd`, input modules, print backends, schemas, GIR/typelib target membership, display/service execution, deployment and activation remain excluded.


Web-chat capability failures follow a stop-loss contract: run one bounded representative probe, classify the limitation, stop equivalent retries, and use the registered authority fallback.

Exact project-produced `libXdamage.so.1.1.0` retains bounded authority for GTK 3.24.49 GDK X11 damage support. The exact atomic `libatk-1.0.so.0.25611.1`, `libatk-bridge-2.0.so.0.0.0`, and `libatspi.so.0.0.1` family retains bounded GTK accessibility library-linkage authority with service metadata disabled and helpers non-executed.

## Current project phase

`libselinux.so.1` is the only unresolved selected identity. The active task is `review-libselinux-direct-consumer-necessity-and-security-boundary`. It is a read-only necessity and security-semantics review. No libSELinux build, acquisition, alias, policy load, relabeling, target population, deployment, or activation is authorized.
