# 0002 — glibc core comes from Termux glibc-repo; everything else from Debian

Date: 2026-07-01→04

## Decision
Layer boundary: libc family + X-connection libs (libx11/libxcb) + GPU stack
= Termux glibc-repo or self-built. All other generic libraries = Debian
rootfs farm. Never mix two glibc builds.

## Context
- Termux glibc-repo's core is patched for Android paths/sockets; Debian's
  libxcb hardcodes /tmp/.X11-unix and cannot reach termux-x11.
- Debian's catalog is unbeatable for everything else; farm + denylist +
  ld.so.conf gives native resolution (RUNPATH doesn't propagate).

## Consequences
- Search order is load-bearing: glibc/lib before farm.
- Farm regeneration must be coupled with ldconfig (gl-farm does both).
- Denylist violations have a crisp signature: `invalid ELF header`.
