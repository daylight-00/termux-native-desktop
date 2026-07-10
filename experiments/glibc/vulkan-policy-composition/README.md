# Vulkan Policy Composition Experiment

## Status

Active architecture-discrimination experiment.

## Question

Can Vulkan provider-selection policy be moved from unconditional shared glibc environment state into narrow launch composition without changing the promoted launchers yet?

## Evidence basis

The Obsidian selected-closure pilot demonstrated:

```text
baseline:
    explicit Freedreno override
    Freedreno driver mapped
    KGSL device mapped

strict policy-isolation run:
    explicit VK_* override removed
    SwiftShader mapped
    Lavapipe root + 8 strict-only dependencies mapped
    Gfxstream mapped
    Freedreno absent
    KGSL absent
```

All 11 strict-only paths were attributed to the three alternate provider roots with zero unresolved or ambiguous mapped-universe SONAME edges.

## Current policy problem

The shared glibc environment currently combines two separate responsibilities:

```text
shield glibc applications from inherited bionic ICD policy

and

select the glibc Freedreno provider globally
```

Real consumers are:

```text
gl-run
VS Code launcher
Obsidian launcher
```

The bionic desktop session has its own separate provider policy and is not the target of this experiment.

## Experiment modes

This experiment intentionally implements only two modes.

### explicit-freedreno

```text
VK_DRIVER_FILES=<glibc Freedreno ICD>
VK_ICD_FILENAMES=<glibc Freedreno ICD>
```

Intent:

```text
explicit hardware-provider selection
```

### implicit-discovery

```text
VK_DRIVER_FILES unset
VK_ICD_FILENAMES unset
```

Intent:

```text
allow loader discovery behavior
```

This mode is **not** called `no-vulkan` because direct evidence shows that removing the explicit override can map alternate Vulkan providers.

## Separation of controls

The experiment keeps these dimensions separate:

```text
GL_GPU
    application argv / feature-mode choice

VULKAN_POLICY_MODE
    provider-selection policy choice
```

The promoted launchers currently couple GPU feature flags to the presence of `VK_DRIVER_FILES`. Experimental adapters do not use that coupling.

## Files

```text
recipe/policy-env.sh
    shared experiment-local policy function

recipe/run-zink-with-policy.sh
    gl-run-equivalent Zink/OpenGL adapter

recipe/launch-vscode-with-policy.sh
    VS Code adapter

recipe/launch-obsidian-with-policy.sh
    Obsidian adapter
```

## Non-goals

Do not use this experiment to implement:

```text
provider updates
provider promotion
provider discovery database
gl-sync
gl-run lifecycle expansion
global environment migration
final directory layout
```

The only goal is to validate that explicit provider policy can be composed at launch scope.

## Validation order

```text
1. environment identity check
2. Zink/OpenGL consumer validation
3. Obsidian explicit-freedreno control
4. Obsidian implicit-discovery control comparison
5. VS Code explicit-freedreno GPU validation
6. VS Code CPU/implicit policy behavior check
```

Promoted launchers and `gl/env` remain unchanged during this experiment.
