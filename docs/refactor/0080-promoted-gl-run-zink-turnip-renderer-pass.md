# 0080 — Promoted gl-run Zink/Turnip Renderer PASS

## Status

The corrected promoted `gl-run` renderer validator passed on the real Termux/Android device.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    promoted-gl-run-renderer-20260711-160030
```

Repository state:

```text
branch:
    refactor/module-package-layout

head:
    f536bb89d47db76b62a9db620e07c4c658313d65
```

Receipt:

```text
gate_failures=0
validation.status=PASS
```

## Prerequisite receipt

```text
promoted_gl_run          PASS  $HOME/gl/bin/gl-run
glx_probe_build_helper   PASS  build-glx-renderer-probe.sh
glx_probe_source         PASS  glx-renderer-probe.c
```

This confirms that the corrected validator used the intended live promoted launcher and the historical self-contained GLX consumer artifacts.

## Build identity

The self-contained GLX consumer built successfully.

Observed interpreter:

```text
$PREFIX/glibc/lib/ld-linux-aarch64.so.1
```

Observed direct `NEEDED` entries:

```text
libc.so.6
ld-linux-aarch64.so.1
```

The probe deliberately resolves the runtime X11 and OpenGL providers with `dlopen`, so those libraries do not appear in the direct build-time `NEEDED` set.

This confirms the workload process is a glibc consumer rather than a bionic diagnostic binary.

## Actual renderer receipt

Observed:

```text
GLX_VERSION=1.4
GL_VENDOR=Mesa
GL_RENDERER=zink Vulkan 1.4(Turnip Adreno (TM) 730 (MESA_TURNIP))
GL_VERSION=4.6 (Compatibility Profile) Mesa 25.0.7-2
```

Passed gates:

```text
gl_vendor_present              PASS
gl_renderer_present            PASS
gl_version_present             PASS
renderer_is_zink               PASS
renderer_is_turnip_adreno      PASS
probe_interpreter_is_glibc     PASS
```

## Proven promoted composition

The receipt establishes the following actual runtime path:

```text
self-contained glibc OpenGL/GLX consumer
    -> live $HOME/gl/bin/gl-run
    -> provider-neutral $HOME/gl/env
    -> explicit $HOME/gl/policy/vulkan/freedreno.sh
    -> MESA_LOADER_DRIVER_OVERRIDE=zink
    -> Mesa GLX/Gallium Zink front half
    -> Vulkan Turnip/Freedreno provider
    -> Adreno 730
```

The renderer string identifies both:

```text
OpenGL bridge:
    Zink

selected hardware Vulkan provider/device family:
    Turnip / Adreno 730
```

This closes the promoted `gl-run` provider-composition and working-context gate.

## Mixed provider-version interpretation

The reported OpenGL version string contains:

```text
Mesa 25.0.7-2
```

while the renderer identifies the managed Turnip provider tail used by the current promoted stack.

This is consistent with the already documented cross-version graphics composition:

```text
rootfs/application-facing GLX + Gallium/Zink front half
    -> managed Vulkan loader/support plane
    -> provider-store Turnip/Freedreno tail
```

The result must not be simplified to one monolithic Mesa build merely because one version appears in `GL_VERSION`.

The version string identifies the reporting OpenGL front half. The provider identity and prior maps identify the hardware Vulkan tail.

## Claim boundary

This receipt proves:

```text
successful GLX display connection
pbuffer-capable framebuffer selection
OpenGL context creation
current context activation
non-null GL identity
Zink renderer selection
Turnip/Adreno renderer identity
successful clean process exit
```

It does not by itself prove:

```text
long-duration stability
window presentation
frame pacing
zero-copy presentation
all loader manifest accesses
all process maps or device-node accesses
```

Those broader claims remain bounded by their separate experiments.

## Promotion gate transition

```text
live scoped policy installation:
    PASS

promoted gl-run environment composition:
    PASS

promoted gl-run actual renderer:
    PASS

promoted VS Code GPU primary identity:
    NEXT
```

The Zink/OpenGL consumer now has both experiment-adapter and promoted-launcher evidence.

## Promoted VS Code validator review

Before execution, the promoted VS Code GPU validator was checked against the existing CDP probe and classifier contracts.

Launch authority:

```text
$HOME/.local/bin/code
    -> packages/vscode/launcher/code
```

The validator requires that exact symlink target.

The existing CDP probe accepts an overridden launcher and invokes it with bounded remote-debugging arguments. The promoted package launcher passes those arguments through the vendor CLI wrapper.

The classifier requires:

```text
gpu-devices.tsv
gpu-aux-attributes.tsv
gpu-feature-status.tsv
gpu-graphics-paths.tsv
probe.status
```

which the CDP probe emits.

The validator reads classifier fields with the exact current names:

```text
classification
selected_provider
selected_device_family
provider_path_relation
device_node_relation
display_type
skia_backend
vulkan_feature_status
gl_renderer
```

No additional static contract mismatch was found before the promoted GPU run.

## Next validation contract

The promoted VS Code GPU gate must prove:

```text
actual live package launcher used
CDP probe PASS
identity classifier PASS
FREEDRENO_TURNIP selected
Adreno device family selected
provider path present
KGSL node present
ANGLE_VULKAN retained
GaneshVulkan retained
Vulkan feature enabled_on
renderer contains Turnip and Adreno
```

This is the direct promotion-equivalence test between the previously validated experiment adapter and the actual package-owned launcher.

## Stop line

Do not yet:

```text
mark scoped Vulkan policy promotion complete
skip directly to CPU-only validation
run an implicit control through the promoted launcher
run VS Code and Obsidian probes concurrently
remove the experiment adapter evidence
```

First validate the promoted VS Code GPU primary identity.
