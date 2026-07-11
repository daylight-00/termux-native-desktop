# 0059 — Bounded Obsidian Implicit Loader Selection Debug Plan

## Status

The Obsidian same-feature-mode GPU policy A/B is closed at topology, survival, semantic-set, and process-class mapping levels.

The remaining Electron-specific graphics question is:

```text
implicit-discovery control maps both:
    libvulkan_lvp.so
    libvulkan_gfxstream.so

which provider, if either, becomes the selected renderer path?
```

Map presence alone cannot answer this.

## Minimum-manipulation strategy

Before adding tracing layers, rebuilding ANGLE, introducing RenderDoc, or modifying promoted launchers, first test whether the existing Electron/AppDir Vulkan loader emits enough physical-device and driver-selection evidence under loader debug logging.

The experiment uses only:

```text
existing Obsidian experiment launcher
existing capture-control harness
same GL_GPU=1 feature mode
same implicit-discovery provider policy
VK_LOADER_DEBUG=all inherited directly by the process tree
bounded survival window
```

No extra launcher wrapper is required.

The capture process exports:

```text
VK_LOADER_DEBUG=all
```

before invoking the existing experiment launcher. The launcher then execs the Obsidian payload, and the GPU-process descendants inherit the diagnostic environment.

No promoted runtime policy changes.

## Added helper

### Debug summarizer

```text
experiments/glibc/vulkan-policy-composition/recipe/summarize-obsidian-loader-debug.sh
```

It extracts, when present:

```text
loader version
ICD manifest discovery
ICD driver names
Mesa device-select insertion
physical-device ordering
physical-device copies
ICD removal events
llvmpipe / Turnip / Adreno references
LVP / Gfxstream references
```

The helper summarizes logs only. It does not infer renderer selection.

## Success criteria

### Strong success

The loader log exposes a discriminating chain such as:

```text
ICDs discovered
    -> physical devices enumerated
    -> device order established
    -> non-viable ICDs removed
    -> one surviving physical-device/provider identity
```

If only one viable provider/device remains and the Electron GPU process survives, that can support a stronger bounded provider-selection inference, subject to exact log semantics.

### Partial success

The log exposes:

```text
ICD discovery
physical-device list
removal events
```

but leaves multiple viable devices/providers unresolved.

In that case the result narrows the next probe but does not close selected renderer identity.

### Negative result

The AppDir loader emits no useful loader debug diagnostics.

In that case do not infer selection from maps. Escalate deliberately to the next least-invasive consumer-specific mechanism.

## Claim boundary

The loader-debug experiment must not equate:

```text
manifest discovery
object mapping
physical-device enumeration
surviving device list
selected renderer
rendering command submission
```

These are separate evidence levels.

## Planned execution

Use a new evidence root and the existing topology harness:

```text
CONTROL_GL_GPU=1
VULKAN_POLICY_MODE=implicit-discovery
LIBGL_ALWAYS_SOFTWARE unset
VK_LOADER_DEBUG=all
short bounded survival window
```

The existing experiment launcher remains:

```text
experiments/glibc/vulkan-policy-composition/recipe/launch-obsidian-with-policy.sh
```

Then run the debug summarizer over `launch.stderr`.

The experiment is diagnostic only and does not require semantic enrichment unless the resulting mapped set differs unexpectedly from the already closed implicit GPU control.
