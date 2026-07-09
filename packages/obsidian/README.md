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

- sources the `gl` runtime environment;
- uses the live payload under `$HOME/gl/apps/obsidian`;
- configures AppDir data/schema paths;
- avoids upstream AppRun library-path injection;
- selects the validated ANGLE Vulkan path when available.

The CLI launcher bridges the Obsidian-registered user CLI through the glibc runtime boundary.

## Runtime payload

`$HOME/gl/apps/obsidian` is an external extracted payload and is not tracked in Git.

The AppImage extraction and onboarding provenance remains under `experiments/glibc/obsidian-appimage/`. A future package-completion pass should promote source identity, checksum, extraction/adaptation procedure, and validation scripts here.
