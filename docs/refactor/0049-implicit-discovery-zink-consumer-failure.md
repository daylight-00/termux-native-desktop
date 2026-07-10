# 0049 — Implicit-Discovery Zink Consumer Failure

## Status

The GLX renderer probe was executed under:

```text
VULKAN_POLICY_MODE=implicit-discovery
VK_DRIVER_FILES unset
VK_ICD_FILENAMES unset
MESA_LOADER_DRIVER_OVERRIDE=zink
```

The probe did not reach the renderer identity gate.

Observed stderr:

```text
experiment Vulkan policy: implicit-discovery
VK_DRIVER_FILES=<unset>
MESA: error: ZINK: failed to choose pdev
glx: failed to create drisw screen
failed to load driver: zink
glXChooseFBConfig found no pbuffer-capable RGBA config
```

Result classification:

```text
policy application: PASS
implicit discovery enabled: PASS
Zink usable physical-device selection: FAIL
GLX screen creation: FAIL
GLX FBConfig gate: FAIL
renderer identity: NOT REACHED
```

## A/B interpretation

The same probe and Zink launch composition passed under explicit Freedreno policy:

```text
explicit-freedreno
    -> Zink
    -> Turnip Adreno 730
    -> GLX context
    -> OpenGL 4.6 identity
```

Under implicit discovery:

```text
implicit-discovery
    -> Zink starts
    -> no usable Vulkan physical device selected
    -> Zink screen creation fails
    -> GLX context path does not form
```

Therefore this consumer A/B establishes:

```text
explicit hardware provider policy
    is required for the tested Zink/GLX consumer path
```

in the captured environment.

The correct claim is bounded to this exact consumer and runtime state.

It does not prove that implicit Vulkan discovery is globally unusable.

The Obsidian strict control previously showed that removing explicit provider overrides can still map alternate Vulkan providers such as:

```text
SwiftShader
Lavapipe
Gfxstream
```

The new GLX result shows that:

```text
provider discovery or provider mapping
    !=
consumer-suitable physical device selection
```

## Primary contract interpretation

The Vulkan loader supports discovering one or more drivers and enumerating physical devices from them.

The `VK_DRIVER_FILES` environment variable overrides default discovery and limits the loader to the specified manifest set.

The explicit-Freedreno pass and implicit-discovery failure therefore demonstrate that provider-selection policy is not merely an optimization hint for this consumer.

It changes whether Zink can form a usable Vulkan-backed OpenGL path.

## Architecture consequence

The current architecture needs more than:

```text
Vulkan available somewhere
```

A consumer composition contract must express:

```text
consumer intent
    +
provider-selection policy
    +
provider suitability validation
    +
actual-selection evidence
```

For the tested Zink/OpenGL consumer:

```text
consumer intent:
    OpenGL through Zink

required provider policy:
    explicit Freedreno/Turnip selection

validation:
    GLX context creation
    renderer identity
    Turnip Adreno 730 identity
```

Implicit discovery is not a valid replacement for that explicit contract in this path.

## Relation to Electron consumers

The Electron consumer path must not inherit the Zink conclusion blindly.

Obsidian already demonstrated different behavior under implicit discovery:

```text
application topology and survival: PASS
alternate Vulkan providers mapped
Freedreno and KGSL absent
```

Therefore provider suitability is consumer-specific.

The next Electron experiments should test:

```text
Obsidian explicit-freedreno GPU composition
Obsidian implicit-discovery composition
VS Code explicit-freedreno GPU composition
VS Code CPU-mode with deliberate provider policy
```

without assuming that a policy valid for Zink/OpenGL is automatically required by Electron.

## Next evidence gate

Before Electron validation, capture loader-side discovery evidence for the failed implicit Zink path.

Use:

```text
VK_LOADER_DEBUG=error,warn,info,driver
```

with the same implicit-discovery probe.

Purpose:

```text
identify discovered driver manifests
identify driver loading attempts
preserve loader warnings/errors
separate loader discovery from Zink suitability failure
```

No provider-selection fix should be applied to the implicit path before that evidence is captured.
