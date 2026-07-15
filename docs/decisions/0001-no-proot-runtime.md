# 0001 — No proot at runtime

Date: 2026-06-30 (pilot), reaffirmed 2026-07-04 (project start)

## Status

Accepted.

## Decision
proot is banned as a runtime; it is an install-time dependency resolver and
debug control group only.

## Context
proot-based Termux desktops are the mainstream approach, but proot's ptrace
syscall interposition costs I/O: VS Code exhibited felt sluggishness in the
pilot. The project's core question is a *tradeoff-free* native desktop.

## Consequences
- Need a native way to run glibc binaries → gl layer (0002, rootfs-as-
  library-pool experiment).
- Debian rootfs is retained, but passive: library warehouse + apt oracle.
