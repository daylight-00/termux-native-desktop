# Project Timeline

This timeline is a compact navigation aid. Detailed claims belong in experiment records and their reports.

## Background

- **2026-06-19 onward** — workplace change restricts conventional PC access; the phone becomes the only personal wireless computing device available in the work setting.
- Research/career work still requires coding, project-tree navigation, remote development, protein visualization, CSV inspection, cluster-job management, diff review, and LaTeX writing.

## Idea development

- **2026-06-27** — DeX + multiport hub + wired display/keyboard/mouse suggests a phone-centered workstation; discovery of Termux:X11 makes a Linux-like native desktop plausible.
- **2026-06-30** — PRoot runtime path rejected after felt VS Code I/O sluggishness. Pure bionic application availability also proves insufficient for the desired VS Code/MS-extension workflow.
- **2026-06-30** — Code OSS remote-development alternatives investigated. Open Remote SSH reaches a deterministic remote-server download/version mismatch; the official Remote Tunnels path progresses through transport and socket creation but is rejected at final client negotiation.

## glibc track

- **2026-06-30** — Miniforge/Conda pilot establishes that a conventional compiled glibc software stack can be adapted to Termux without using PRoot as the runtime.
- **2026-07-01 to 2026-07-02** — official Microsoft VS Code pilot succeeds with an explicitly isolated glibc runtime and manually supplied Debian libraries. The experiment exposes ABI isolation, dynamic dependency, X11 transport, font, certificate, and Electron-launch boundaries.
- **2026-07-04 onward** — manual library hunting is replaced by the rootfs-as-library-pool model. PRoot becomes install/debug-time infrastructure; native glibc execution becomes the runtime model.
- **2026-07-05 to 2026-07-06** — Obsidian arm64 AppImage onboarding succeeds through SquashFS extraction, ELF adaptation, dependency verification, launch-contract reuse, GPU validation, and CLI integration.

## GPU track

- **2026-07-01** — native Chromium/Code OSS conventional GPU acceleration succeeds through ANGLE Vulkan and Turnip. Global Zink forcing is rejected as a desktop-wide policy.
- **2026-07-01 onward** — video acceleration and native WebGPU investigations branch from the working conventional GPU baseline; neither produces the desired final path.
- **2026-07-02 to 2026-07-03** — Mesa 26.0.6 is built for the glibc runtime; the real Adreno/Turnip device path is validated and the build becomes a crucial control for later work.
- **2026-07-02 to 2026-07-03** — official VS Code GPU enablement narrows an Electron/ANGLE swapchain failure to a minimal operational workaround: direct ANGLE Vulkan with `--disable-gpu-vsync`.
- **2026-07-03** — native bionic Mesa 26.1.4 is rebuilt from the Termux package recipe lineage; this working `msm,kgsl` configuration later becomes an important comparison point.
- **2026-07-03** — Picom GLX work motivates Mesa investigations but the compositor path is abandoned.
- **2026-07-04 to 2026-07-05** — glibc Mesa 26.1.4 X11 present SIGBUS is investigated through controls, traces, dependency comparison, and build-configuration changes. Current policy adopts `msm,kgsl`.

## Python workflow

- A persistent `uv-base` workflow is validated around an existing standalone CPython 3.14.6 runtime: uv does not download another interpreter, project metadata and lock state remain explicit, and the default interactive Python can change through PATH precedence without replacing the system Python.
- `cpython-android-cli` evolves as a separate companion project because its CPython Android CLI adaptation question is independently coherent.

## Repository consolidation

- **2026-07-08** — glibc, GPU, desktop/session, and workstation-workflow tracks are consolidated as one research workbench. Session-derived full reports are promoted from `temp/` into the corresponding experiment directories as `report.md`, while concise `README.md` files remain the canonical current interpretation.
