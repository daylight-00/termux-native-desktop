# 0084 — Current-Head gl-run Regression PASS and Strengthened VS Code GPU Gate

## Status

The promoted `gl-run` actual-renderer regression passed after the shared glibc baseline was corrected to sanitize inherited bionic OpenGL bridge/Gallium policy.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    current-gl-run-renderer-20260711-164455
```

Captured repository state:

```text
branch:
    refactor/module-package-layout

head:
    147c7e2fc9b414a6be5561589293c01820d5f7f6
```

Receipt:

```text
gate_failures=0
validation.status=PASS
```

## Source-state coherence

The checkout was fast-forwarded from the runtime-source gate head:

```text
5ed76ec9c7409a141da02a28b5297b8b71965467
```

to:

```text
147c7e2fc9b414a6be5561589293c01820d5f7f6
```

The only intervening paths were:

```text
STATUS.md
docs/refactor/0083-expanded-graphics-policy-predeploy-and-live-installation-pass.md
```

The user explicitly checked:

```text
git diff --name-status \
    5ed76ec9c7409a141da02a28b5297b8b71965467..HEAD \
    -- modules packages tests tools \
       experiments/glibc/vulkan-policy-composition/recipe
```

and observed no output.

Therefore the renderer regression ran against the same runtime and validation source that passed the expanded pre-deploy and live installation gates, with only documentation/status commits added afterward.

## Live target identity

Observed exact resolved targets:

```text
$HOME/gl/env
    -> modules/gl/overlay/home/gl/env

$HOME/gl/policy/vulkan/freedreno.sh
    -> modules/gl/overlay/home/gl/policy/vulkan/freedreno.sh

$HOME/gl/bin/gl-run
    -> modules/gl/overlay/home/gl/bin/gl-run
```

This confirms the actual promoted public path was exercised.

## glibc substrate state

Observed package state:

```text
Status:
    hold ok installed

Version:
    2.42

Architecture:
    aarch64

apt hold:
    glibc
```

The current receipt therefore belongs to the recovered and intentionally held glibc 2.42 substrate, not the earlier incompatible 2.43 state.

The hold remains incident containment, not a permanent substrate lifecycle design.

## Deliberate hostile-policy injection

The renderer validator was invoked with:

```text
MESA_LOADER_DRIVER_OVERRIDE=llvmpipe
GALLIUM_DRIVER=llvmpipe
```

`LIBGL_ALWAYS_SOFTWARE` was unset.

The expected composition was:

```text
hostile inherited bridge/device policy
    -> removed by live ~/gl/env
    -> explicit Freedreno profile selected by gl-run
    -> gl-run adds MESA_LOADER_DRIVER_OVERRIDE=zink
    -> no inherited GALLIUM_DRIVER selection remains effective
```

This is a stronger regression than launching from an already clean shell.

## Build and ABI identity

The self-contained GLX probe built successfully.

Observed interpreter:

```text
$PREFIX/glibc/lib/ld-linux-aarch64.so.1
```

Observed direct `NEEDED` entries:

```text
libc.so.6
ld-linux-aarch64.so.1
```

The probe remains a glibc workload. X11/OpenGL providers are resolved dynamically by the probe and therefore do not appear as direct build-time `NEEDED` entries.

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

Renderer stderr was empty.

## Proven corrected composition

The receipt establishes:

```text
injected llvmpipe bridge/device policy
    -> sanitized glibc baseline
    -> promoted gl-run
    -> explicit managed glibc Freedreno ICD
    -> gl-run-owned Zink bridge
    -> Turnip
    -> Adreno 730
    -> working GLX/OpenGL 4.6 context
```

If the inherited `GALLIUM_DRIVER=llvmpipe` or `MESA_LOADER_DRIVER_OVERRIDE=llvmpipe` had remained the effective selected policy, the observed renderer could not have been the required Zink/Turnip/Adreno identity.

The separate expanded live installation receipt already proved the variables themselves become unset in the baseline. This actual workload receipt proves that the resulting promoted composition remains functional.

## Current-head gl-run gate closure

The previous prior-head renderer PASS remains historical evidence.

This new receipt closes the post-correction current-source gate:

```text
expanded source/environment gates:
    PASS

current promoted gl-run renderer:
    PASS

current glibc substrate:
    2.42 held
```

## Why the VS Code GPU gate was strengthened

The next regression must prove two different facts:

```text
1. environment/argv composition
2. selected provider/device identity
```

CDP primary-device evidence proves the second fact but does not expose every process environment variable.

Because the baseline correction specifically removed inherited:

```text
MESA_LOADER_DRIVER_OVERRIDE
GALLIUM_DRIVER
```

the promoted GPU gate was strengthened before rerun.

## Environment-boundary probe expansion

Updated:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    probe-vscode-policy-env-boundary.sh
```

Commit:

```text
0268c860c1e341eb433ecb02c8d3cbed85c6e726
```

The selected environment receipt now includes:

```text
GL_GPU
VK_DRIVER_FILES
VK_ICD_FILENAMES
MESA_LOADER_DRIVER_OVERRIDE
GALLIUM_DRIVER
LIBGL_ALWAYS_SOFTWARE
LD_LIBRARY_PATH
LD_PRELOAD
VK_LOADER_DEBUG
```

The probe directly reads `/proc/<pid>/environ` for observed main, zygote, and GPU processes.

## Combined promoted VS Code GPU validator

Updated:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    validate-promoted-vscode-gpu-identity.sh
```

Commit:

```text
438be69fa7bf46df50cc77a2783c10e18143c0f3
```

The validator now performs two independent application launches.

### Phase 1 — environment and argv

It deliberately injects:

```text
VK_DRIVER_FILES=/bionic/freedreno.json
VK_ICD_FILENAMES=/bionic/freedreno.json
MESA_LOADER_DRIVER_OVERRIDE=llvmpipe
GALLIUM_DRIVER=llvmpipe
```

It then requires readable main, zygote, and GPU process environments with:

```text
GL_GPU=1
VK_DRIVER_FILES=<exact managed glibc ICD>
VK_ICD_FILENAMES=<same exact managed glibc ICD>
MESA_LOADER_DRIVER_OVERRIDE absent
GALLIUM_DRIVER absent
LIBGL_ALWAYS_SOFTWARE absent
LD_LIBRARY_PATH absent
LD_PRELOAD absent or empty
no /bionic/ path retained
```

The main process must contain the exact GPU branch flags:

```text
--disable-gpu-sandbox
--ignore-gpu-blocklist
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
--disable-gpu-vsync
```

It must not contain the exact token:

```text
--disable-gpu
```

The exact-token check does not confuse `--disable-gpu-sandbox` with `--disable-gpu`.

### Launch-tree boundary

The environment probe owns and cleans its process tree.

Before beginning the CDP phase, the combined validator waits for process cleanup and fails if any VS Code application process remains.

This prevents two launch trees from contaminating one evidence set.

### Phase 2 — selected primary identity

The second launch reuses the established CDP probe and classifier.

It requires:

```text
classification=FREEDRENO_TURNIP
selected_provider=FREEDRENO_TURNIP
selected_device_family=Adreno
provider_path_relation=PRESENT
device_node_relation=PRESENT
display_type=ANGLE_VULKAN
skia_backend=GaneshVulkan
vulkan_feature_status=enabled_on
renderer contains Turnip and Adreno
```

## Claim boundary

The current `gl-run` receipt proves effective working renderer composition under hostile inherited policy.

It does not directly dump every final `gl-run` process environment variable. Exact baseline-variable absence is established by the expanded installation receipt and repository smoke; the actual renderer establishes the effective outcome.

The strengthened VS Code validator separately captures environment/argv and selected-device identity because both are material to the post-correction promotion claim.

## Current gate state

```text
expanded pre-deploy:
    PASS

expanded live installation:
    PASS

current-head promoted gl-run renderer:
    PASS

strengthened current-head VS Code GPU environment/identity:
    NEXT

promoted VS Code CPU policy:
    BLOCKED ON GPU PASS

promoted Obsidian GPU/CPU:
    PENDING

scoped graphics-policy promotion closure:
    PENDING
```

## Stop line

Do not:

```text
reuse the earlier VS Code GPU evidence root
run an existing VS Code instance during the combined gate
skip the environment phase and rely only on CDP
merge two application launch trees
proceed to CPU mode before the strengthened GPU gate passes
```

Sync the validator-only commits, run a targeted shell-syntax check, and execute the combined promoted VS Code GPU gate with a fresh evidence root.
