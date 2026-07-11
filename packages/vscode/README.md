# VS Code package integration

This package owns workstation-specific integration for the official Microsoft VS Code Linux arm64 distribution.

## Current promoted launcher

```text
packages/vscode/launcher/code
    -> $HOME/.local/bin/code
```

The public path is a current integration adapter, not a permanent architecture identity.

## Current launcher contract

The launcher:

- sources the current graphics-policy-neutral glibc baseline;
- uses the external payload under `$HOME/gl/apps/vscode`;
- preserves caller working-directory semantics through the vendor CLI wrapper;
- owns the application GPU/CPU feature-mode decision;
- when `GL_GPU=1`, applies the explicit managed glibc Freedreno provider and validated ANGLE Vulkan argv;
- when `GL_GPU=0`, retains a provider/bridge-neutral baseline and passes exact `--disable-gpu`;
- fails closed to the same sanitized CPU path if the managed provider profile is unavailable.

The package owns application feature policy. The shared baseline must not select a provider or OpenGL bridge on its behalf.

## Graphics-policy validation state

```text
VS Code GPU branch:
    PASS

VS Code CPU branch:
    PASS

scoped graphics-policy transaction:
    CLOSED
```

Canonical records:

```text
docs/refactor/0085-vscode-child-proc-environ-observability-false-negative.md
docs/refactor/0086-current-vscode-gpu-environment-and-primary-identity-pass.md
docs/refactor/0087-current-vscode-cpu-policy-and-survival-pass.md
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

Validated hardware composition:

```text
ANGLE Vulkan
    -> managed Freedreno / Turnip
    -> Adreno 730
    -> /dev/kgsl-3d0
```

The same-consumer implicit-discovery control selected LVP/llvmpipe as the primary device. The GPU branch therefore applies the explicit provider profile rather than relying on default discovery.

CPU acceptance is based on effective policy/mode, not the absolute absence of a Chromium helper named `gpu-process`.

## Semantic contract versus current implementation

Durable package contract:

```text
application owns GPU/CPU feature mode
hardware provider is explicit and consumer-scoped
ANGLE Vulkan branch owns no Zink/Gallium override
CPU branch owns exact --disable-gpu
validation uses isolated application state
selected hardware GPU requires correlated evidence
```

Current implementation:

```text
GL_GPU branch
current launcher path
current Freedreno profile path
current Chromium/Electron argv
```

Those names and spellings may evolve while preserving the semantic contract.

## Application-state authority

Canonical validation uses receipt-local:

```text
--user-data-dir
--extensions-dir
```

Normal extensions, settings, locks, and long-duration user behavior are outside promotion evidence.

## Runtime payload

```text
$HOME/gl/apps/vscode
```

is an external application payload and is not tracked in Git.

Current onboarding provenance remains under:

```text
experiments/glibc/vscode/
experiments/gpu/vscode-angle-vulkan/
```

A package-completion pass still needs to promote:

```text
source identity
checksum/signature policy
acquisition/adaptation procedure
application-version trigger
canonical package-level validators
mutable-state/extension migration policy
```

## Current ownership caveat

The launcher still inherits non-graphics policy from the transitional glibc baseline.

In particular:

```text
ELECTRON_DISABLE_SANDBOX=1
```

is Electron-family/security policy rather than an obvious world-wide invariant.

Its future owner and necessity must be validated per Electron packaging/version model. Do not keep it global merely because current applications work.

## Revalidation triggers

Rerun only affected package gates when:

```text
launcher changes
VS Code/Electron version changes
application-state authority changes
GPU/CPU argv policy changes
provider profile or graphics composition changes
selected-device evidence logic changes materially
```

Documentation-only changes do not require runtime reruns unless they invalidate an existing evidence interpretation.
