# 0002 — Historical broad glibc-provider sourcing rule

Date: 2026-07-01→04

## Status

**Superseded as a universal ownership and sourcing rule.**

The original protected-world observations remain valid evidence, especially the need for a coherent Termux glibc substrate and Termux-aware X11/xcb behavior. The conclusion that every other generic library should come from one Debian farm is no longer current architecture.

Current interpretation is governed by `docs/architecture.md`, `docs/glibc-layer.md`, the provider-authority records beginning at `docs/refactor/0116-...`, and the active assurance-depth policy task.

## Historical decision

The original rule was:

```text
libc family + selected X-connection libraries + GPU stack
    -> Termux glibc-repo or project build

all other generic libraries
    -> Debian rootfs compatibility farm
```

It also prohibited mixing independent glibc implementations inside one process world.

## Historical context

- The Termux glibc substrate and selected X11/xcb packages carried Android/Termux path or socket adaptations needed for Termux:X11.
- The Debian catalog provided a fast compatibility warehouse during application onboarding.
- Broad `LD_LIBRARY_PATH` propagation was unsafe, so the farm and loader cache provided transitive discovery.

## Current replacement

Provider authority is now decided by semantic role and evidence rather than one source-wide rule:

```text
protected world/substrate
platform-adapted provider
generic shared provider
application-local payload
application supplement
build-only or research artifact
```

Debian rootfs remains a valuable oracle, dependency solver, warehouse and candidate source. Observed rootfs origin is not by itself clean supply, final provider authority or target-layout permission.

## Retained consequences

- Never mix incompatible glibc worlds in one process.
- Search order and loader composition remain load-bearing.
- Termux/Android adaptation must be preserved where required.
- The broad farm remains a transitional compatibility and research mechanism, not the accepted final provider architecture.
