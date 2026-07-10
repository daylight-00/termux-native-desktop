# 0043 — Scoped Vulkan Policy Composition Experiment

## Status

A cross-consumer experiment has been added under:

```text
experiments/glibc/vulkan-policy-composition/
```

The experiment exists to validate launch-scoped provider-selection policy before changing:

```text
modules/gl/overlay/home/gl/env
modules/gl/overlay/home/gl/bin/gl-run
packages/vscode/launcher/code
packages/obsidian/launcher/obsidian-app
```

No promoted runtime path has been changed by this experiment.

## Evidence basis

The Obsidian A/B established:

```text
explicit Freedreno override
    -> Freedreno driver mapping
    -> KGSL device mapping

explicit override removed
    -> alternate provider composition
    -> SwiftShader root
    -> Lavapipe root + 8 strict-only dependencies
    -> Gfxstream root
```

The alternate strict-only set was attributed 11/11 with:

```text
unresolved edges: 0
ambiguous mapped SONAME edges: 0
```

The producer/consumer inventory established:

```text
bionic session producer:
    startxfce-x11

glibc shared producer:
    gl/env

real glibc consumers:
    gl-run
    VS Code launcher
    Obsidian launcher
```

## Experiment contract

The experiment exposes exactly two provider-policy modes.

### explicit-freedreno

```text
VK_DRIVER_FILES=<glibc Freedreno ICD>
VK_ICD_FILENAMES=<glibc Freedreno ICD>
```

This represents explicit hardware-provider selection.

### implicit-discovery

```text
VK_DRIVER_FILES unset
VK_ICD_FILENAMES unset
```

This represents loader discovery behavior.

It is intentionally not called `no-vulkan` because evidence already proves that unsetting explicit overrides can map alternate Vulkan providers.

## Control dimensions

The experiment separates:

```text
GL_GPU
    application feature/argv mode

VULKAN_POLICY_MODE
    provider-selection policy
```

The current promoted Electron launchers use `VK_DRIVER_FILES` presence as part of their GPU-flag condition. The experimental adapters do not make policy identity and application feature mode the same variable.

## Experiment-local files

```text
README.md

recipe/policy-env.sh
    source-only policy function

recipe/run-zink-with-policy.sh
    Zink/OpenGL consumer adapter

recipe/launch-vscode-with-policy.sh
    VS Code adapter

recipe/launch-obsidian-with-policy.sh
    Obsidian adapter
```

The common helper is intentionally small. It does not:

```text
discover providers
update providers
materialize provider bytes
promote provider state
change the broad farm
change gl-run lifecycle semantics
```

It only applies one explicit experiment policy to the current process environment.

## Validation objective

The experiment must determine whether the provider-selection responsibility can be moved to launch composition while preserving current consumer behavior.

Required validations:

```text
Zink/OpenGL:
    explicit-freedreno policy
    renderer identity
    workload success

Obsidian:
    explicit-freedreno policy
    actual Freedreno/KGSL relation

    implicit-discovery policy
    alternate-provider relation

VS Code:
    explicit-freedreno GPU path
    actual provider selection evidence

    CPU argv mode with deliberate policy choice
    no hidden dependence on global gl/env provider selection
```

## Claim boundary

This experiment does not yet prove a final owner name, final directory layout, or public CLI.

It tests the behavior contract:

```text
provider policy can be composed narrowly
without being unconditional world baseline
```

The final implementation may use a different physical layout after evidence is complete.

## Stop line

Do not yet:

```text
remove VK_* from gl/env
rewrite promoted launchers
rename gl-run
introduce a graphics manager
add provider lifecycle automation
```

First validate the experiment adapters against the actual consumers.

## Next order

```text
1. policy environment identity check
2. Zink/OpenGL explicit-freedreno validation
3. Obsidian adapter equivalence validation
4. VS Code adapter validation with actual-selection evidence
5. record failures/differences
6. only then design promoted migration transaction
```
