# VS Code package integration

This package owns workstation-specific integration for the official Microsoft VS Code Linux arm64 distribution.

## Current promoted state

```text
packages/vscode/launcher/code
    -> $HOME/.local/bin/code
```

The launcher:

- sources the graphics-policy-neutral `gl` runtime baseline, which clears inherited bionic Vulkan and OpenGL bridge/Gallium policy;
- uses the live payload under `$HOME/gl/apps/vscode`;
- preserves caller working-directory semantics through the vendor CLI wrapper;
- when `GL_GPU=1`, sources the explicit glibc Freedreno Vulkan profile and enables the validated ANGLE Vulkan path only if that profile is available;
- when `GL_GPU=0`, keeps both Vulkan provider variables and the Zink/Gallium overrides absent, then passes `--disable-gpu`;
- falls back to the same sanitized `--disable-gpu` path if the managed provider manifest is unavailable.

The package owns the application feature decision. The shared `gl` baseline does not select a provider or OpenGL bridge on its behalf.

Validated hardware composition:

```text
ANGLE Vulkan
    -> Freedreno / Turnip
    -> Adreno 730
    -> /dev/kgsl-3d0
```

The same-consumer implicit-discovery control selected LVP/llvmpipe, which is why the GPU branch deliberately applies the explicit provider profile.

The promoted GPU identity passed before the baseline was expanded to clear the inherited bionic Zink/Gallium policy. That evidence remains valid for the captured head, but current-HEAD GPU and CPU regression receipts are required before final promotion closure.

## Runtime payload

`$HOME/gl/apps/vscode` is an external application payload and is not tracked in Git.

The current onboarding provenance and adaptation boundaries remain documented under `experiments/glibc/vscode/` and `experiments/gpu/vscode-angle-vulkan/`.

A future package-completion pass should promote source identity, checksum, adaptation procedure, and validation scripts here without rewriting the historical experiment reports.
