# Obsidian package integration

This package owns workstation-specific integration for the extracted Obsidian arm64 AppImage payload.

## Current promoted state

```text
packages/obsidian/launcher/obsidian
packages/obsidian/launcher/obsidian-app
```

`tools/deploy` exposes the launchers at:

```text
$HOME/gl/bin/obsidian
$HOME/gl/bin/obsidian-app
```

The GUI launcher:

- sources the graphics-policy-neutral `gl` runtime baseline, which clears inherited bionic Vulkan and OpenGL bridge/Gallium policy;
- uses the live payload under `$HOME/gl/apps/obsidian`;
- configures AppDir data/schema paths;
- avoids upstream AppRun library-path injection;
- when `GL_GPU=1`, sources the explicit glibc Freedreno Vulkan profile and enables the validated ANGLE Vulkan path only if that profile is available;
- when `GL_GPU=0`, keeps both Vulkan provider variables and the Zink/Gallium overrides absent, then passes `--disable-gpu`;
- falls back to the same sanitized `--disable-gpu` path if the managed provider manifest is unavailable.

The CLI launcher only bridges the Obsidian-registered user CLI through the glibc runtime boundary. It receives baseline graphics-policy sanitation but does not select a Vulkan provider or OpenGL bridge.

The GUI package therefore owns the feature-mode decision while the shared `gl` module provides the reusable explicit provider profile.

Because the baseline sanitation contract was expanded after the earlier Obsidian experiment captures, promoted GPU and CPU regression receipts are required before the scoped policy transaction closes.

## Runtime payload

`$HOME/gl/apps/obsidian` is an external extracted payload and is not tracked in Git.

The AppImage extraction and onboarding provenance remains under `experiments/glibc/obsidian-appimage/`. A future package-completion pass should promote source identity, checksum, extraction/adaptation procedure, and validation scripts here.
