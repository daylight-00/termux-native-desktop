# termux-native-desktop

An active systems-engineering project for turning a single non-root Android phone into a practical research and development workstation.

> **Goal:** run a high-performance native Termux desktop environment without a PRoot runtime, while retaining access to mainstream glibc applications and real Adreno GPU acceleration.

This repository is both the working laboratory and the curated technical record. It is not an installer framework, package manager, or black-box setup script.

## Project question

Can a stock, non-root Android phone provide a desktop environment suitable for real technical work—coding, remote development, project navigation, scientific visualization, data inspection, Git review, and manuscript writing—without accepting a containerized runtime as the normal execution path?

The project currently answers that question through three tightly coupled workstreams:

```text
native desktop/session
        |
        +-- bionic-native applications and services
        |
        +-- glibc application layer
        |      +-- Termux glibc core
        |      +-- Debian rootfs as a passive library pool
        |      +-- application-local libraries
        |
        +-- GPU acceleration
               +-- bionic Mesa/Turnip
               +-- glibc Mesa/Turnip
               +-- ANGLE Vulkan and Zink consumers
```

PRoot remains useful as an install-time dependency resolver, library source, and debugging control environment. It is intentionally excluded from the normal application runtime.

## Repository map

- `docs/` — project context, architecture, integrated operational guides, timeline, and durable decisions.
- `experiments/` — the living workbench. Each experiment keeps a concise canonical `README.md`; session-derived full reports live beside it as `report.md`; raw captures go in `evidence/` when useful.
- `setup/` — promoted runtime configuration and launch artifacts used by the live device.
- `scripts/` — repository/deployment helpers.
- `STATUS.md` — current conclusions, unresolved questions, and immediate work.

The intended information flow is:

```text
question
  -> experiment
  -> evidence
  -> working conclusion (STATUS.md)
  -> durable decision (docs/decisions/)
  -> integrated guide or promoted runtime artifact
```

## Documentation guide

- [`docs/PROJECT_CONTEXT.md`](docs/PROJECT_CONTEXT.md) — motivation and scope.
- [`docs/architecture.md`](docs/architecture.md) — current system model.
- [`docs/glibc-layer.md`](docs/glibc-layer.md) — glibc layer bootstrap, boundaries, onboarding, traps, maintenance.
- [`docs/gpu.md`](docs/gpu.md) — Turnip/Zink build and runtime contract plus diagnostic history.
- [`docs/desktop-session.md`](docs/desktop-session.md) — Termux:X11/XFCE two-world session contract.
- [`experiments/README.md`](experiments/README.md) — experiment index and provenance contract.

## Companion project

[`cpython-android-cli`](https://github.com/daylight-00/cpython-android-cli) is maintained separately. It was motivated by this workstation, but its research question—adapting the official Android CPython runtime for normal Termux CLI use with uv integration—is independently coherent.

## Status

This is an active experiment, not a finished distribution. Working paths are kept alongside failed and abandoned investigations when those failures define useful boundaries. See [`STATUS.md`](STATUS.md).
