# Official VS Code: glibc application onboarding

**Status:** passed  
**Dates:** pilot 2026-07-01 to 2026-07-02; layer formalization from 2026-07-04  
**Provenance:** first-hand historical report + current canonical interpretation

## Question

Can the official Microsoft VS Code Linux arm64 distribution run as a native glibc application inside the Termux desktop, preserving the normal bionic host and avoiding a PRoot runtime?

## Baseline

- Native Code OSS exists but does not provide the desired Microsoft-licensed extension workflow.
- The PRoot VS Code path worked but showed felt I/O sluggishness.
- The initial glibc pilot had no scalable dependency-layer design.

## Hypothesis

A conventional Electron application can run if the project supplies an explicit glibc process boundary, the required shared-library world, a valid X11 path, and narrow Android-specific launch adaptations.

## Evidence and result

The first-hand report proves that official VS Code 1.127.0 arm64 reached a working workbench, local extension host, default extension initialization, storage creation, and a usable desktop session without PRoot or chroot.

The experiment also directly exposed several architectural boundaries:

- bionic and glibc library paths must be isolated;
- static dependency discovery misses runtime-loaded libraries;
- Electron child-process behavior is sensitive to the loader/invocation chain;
- GUI success and GPU success are separate milestones;
- Android restrictions around D-Bus, udev, netlink, and `/proc/sys` can be noisy without being fatal.

## Current interpretation

The preserved `report.md` describes the successful **pilot architecture**, including TCP X11 and process-local `LD_LIBRARY_PATH`. Those details are historically important but are not the current layer contract.

The later project architecture superseded them with:

- glibc-repo X11/xcb libraries and local Unix-socket X11;
- a filtered Debian-rootfs library farm;
- RPATH/loader-cache based dependency resolution rather than broad library-path injection;
- the package-owned launcher at `packages/vscode/launcher/code`, deployed to `~/.local/bin/code`.

The GPU enablement investigation is intentionally separate at `experiments/gpu/vscode-angle-vulkan/`.

## Decision

Official VS Code is the primary large-application validation target for the glibc layer. Keep the historical report intact and let this README carry the current interpretation.

See [`report.md`](report.md).
