# Project Context

> **Status:** active experiment  
> **Primary target:** Samsung Galaxy S22 Ultra, stock Android kernel, non-root Termux + Termux:X11  
> **Project start:** 2026-07-04, after pilot work beginning 2026-06-27

## Why this project exists

The immediate constraint is unusual but concrete: a mobile phone is the only personal wireless computing device available in the user's current work environment, and access to a conventional PC became restricted after a workplace move in June 2026.

The work that still has to happen is not mobile-app work. It includes coding, browsing complex project trees, using remote development workflows, visualizing proteins, inspecting CSV files, managing cluster jobs, reviewing diffs, and writing LaTeX manuscripts. A terminal-only workflow is useful but insufficient; the work benefits from spatial project navigation and rapid movement between several desktop tools.

The phone itself is capable enough to drive an external display, keyboard, and mouse through Samsung DeX and a multiport hub. The breakthrough was realizing that Termux:X11 could provide a Linux-like desktop environment on top of that physical setup.

The project therefore asks a practical engineering question:

> How far can a single non-root Android phone be pushed toward a real research/development workstation while preserving native performance and avoiding avoidable tradeoffs?

## Why the mainstream paths were not enough

### PRoot desktop

PRoot-based desktops are the common Termux approach and remain useful reference systems. In this project, however, the normal runtime path was rejected after VS Code showed felt I/O sluggishness under PRoot. The project does not reject PRoot as a tool: a distribution rootfs is still valuable as a package/dependency oracle, a passive library warehouse, and a debugging control environment.

The boundary is intentional:

```text
PRoot at runtime:        rejected
PRoot for install/debug: retained
```

### Pure bionic-native desktop

A native Termux desktop is fast and integrates naturally with the Android/Termux environment, but application availability is limited by the bionic ABI. Many mainstream commercial Linux desktop applications do not publish bionic builds. Code OSS exists natively, but the desired Microsoft-licensed extension workflow was not available; attempts to replace that workflow with open remote-development alternatives became separate experiments and did not solve the original need.

## Evolution of the idea

### glibc workstream

The first hypothesis was simple: if conventional glibc binaries can run from native Termux, then PRoot may not be necessary as the application runtime.

A Conda/Miniforge pilot showed that a glibc application stack could be adapted. Official Microsoft VS Code then became the first large desktop application target. The initial pilot used manually gathered Debian libraries and exposed several boundaries: glibc and bionic library paths must not contaminate each other, static dependency discovery misses runtime-loaded libraries, X11 transport details matter, and successful GUI startup is separate from successful GPU acceleration.

The manual-library approach did not scale. The next idea was to keep a Debian rootfs but demote it from runtime environment to library source. That became the current layer model: Termux glibc provides the core runtime and Android-sensitive libraries; a filtered farm exposes general libraries from the Debian rootfs; applications retain local libraries where appropriate.

### GPU workstream

GPU work quickly became as important as the glibc layer itself.

Native Chromium and Code OSS established a working ANGLE Vulkan -> Turnip -> Adreno path. A glibc Mesa 26.0.6 build then showed that the same GPU could be exposed to glibc applications. Official VS Code GPU enablement required a long narrowing process around an Electron/ANGLE swapchain failure; the final operational condition was much simpler than the diagnostic path: direct ANGLE Vulkan with `--disable-gpu-vsync`.

Later Mesa 26.1.x work exposed a separate X11 present SIGBUS in the investigated kgsl-only build. Comparing working and failing driver dependency shapes led to the current `msm,kgsl` build policy.

The project also explored native bionic Mesa updates, Picom GLX behavior, video acceleration, WebGPU, and Zink. Some of these paths succeeded, some remain unresolved, and some were abandoned. They stay in the repository because the negative results define useful boundaries.

## Engineering preferences

The project follows a few strong preferences:

1. Prefer the newest practical and highest-performing path; build components locally when necessary.
2. Start from upstream, reference, or mainstream implementations whenever possible.
3. Keep custom behavior narrow and explicit.
4. When a non-reference implementation or tweak becomes necessary, understand and record why.
5. Avoid black-box setup mechanisms.
6. Preserve the chain from baseline to hypothesis, experiment, evidence, decision, and promoted artifact.
7. Optimize first for understanding and reproducibility, not for turning the work into a general installation framework.

This repository is therefore closer to a technical research notebook plus a live system source tree than to an end-user distribution.

## Repository as workplace and output

The project is still being discovered. A repository that only publishes a cleaned final answer would lose the information needed to continue the work; a repository that only dumps transcripts would be difficult to understand or review.

The structure intentionally supports both roles:

```text
README / PROJECT_CONTEXT / architecture
    stable orientation and current system model

STATUS
    current conclusions and unresolved questions

experiments/<track>/<experiment>/README.md
    concise canonical record of the experiment

experiments/<track>/<experiment>/report.md
    detailed session-derived report, preserved as provenance

experiments/<track>/<experiment>/evidence/
    raw logs, traces, and small captured facts when worth keeping

setup/ and scripts/
    artifacts promoted from successful experiments into the live system

docs/decisions/
    durable choices whose rationale should survive individual experiments
```

A detailed report may describe an intermediate architecture that was later superseded. In that case it is not rewritten to pretend the final design existed earlier. The experiment `README.md` records the current interpretation and explicitly identifies what the historical report proves and what has since changed.

## Project boundary

`termux-native-desktop` is the system project. Its glibc, GPU, desktop/session, and workstation-workflow experiments belong together because they co-evolve around one end-to-end target.

`cpython-android-cli` remains a companion repository. It originated from the need for a good Python workflow on this workstation, but it asks an independent technical question: how to adapt the official Android CPython runtime into a normal Termux CLI interpreter and integrate it with uv. This repository may consume or reference that result without absorbing its experiment history.
