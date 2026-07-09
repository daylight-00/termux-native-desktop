# VS Code package integration

This package owns workstation-specific integration for the official Microsoft VS Code Linux arm64 distribution.

## Current promoted state

```text
packages/vscode/launcher/code
    -> $HOME/.local/bin/code
```

The launcher:

- sources the `gl` runtime environment;
- uses the live payload under `$HOME/gl/apps/vscode`;
- preserves caller working-directory semantics through the vendor CLI wrapper;
- selects the validated ANGLE Vulkan path when glibc GPU support is available;
- retains CPU fallback through `GL_GPU=0`.

## Runtime payload

`$HOME/gl/apps/vscode` is an external application payload and is not tracked in Git.

The current onboarding provenance and adaptation boundaries remain documented under `experiments/glibc/vscode/` and `experiments/gpu/vscode-angle-vulkan/`.

A future package-completion pass should promote source identity, checksum, adaptation procedure, and validation scripts here without rewriting the historical experiment reports.
