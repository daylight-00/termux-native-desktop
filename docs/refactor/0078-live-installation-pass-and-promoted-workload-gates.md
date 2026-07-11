# 0078 — Live Vulkan Installation PASS and Promoted Workload Gates

## Status

The scoped Vulkan policy transaction has been deployed to the live Termux paths and passed its no-GUI installation receipt.

Deploy result:

```text
PASS
```

Installation evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    live-vulkan-policy-installation-20260711-154958
```

Repository state:

```text
branch:
    refactor/module-package-layout

head:
    e89bbe7a9c284759fa3ce61567f3ab474df792b3
```

Installation receipt:

```text
gate_failures=0
installation.status=PASS
```

## Live managed targets

All required runtime leaves are exact managed symlinks into the canonical checkout:

```text
$HOME/gl/env
$HOME/gl/policy/vulkan/freedreno.sh
$HOME/gl/bin/gl-run
$HOME/.local/bin/code
$HOME/gl/bin/obsidian
$HOME/gl/bin/obsidian-app
```

The previously absent profile leaf now exists and resolves to:

```text
$HOME/projects/termux-native-desktop/
    modules/gl/overlay/home/gl/policy/vulkan/freedreno.sh
```

This closes the temporary activation gap recorded in `0077` for the current deployed checkout state.

It does not solve the general atomic-activation problem of mutable checkout symlinks.

## Live environment contract

### Provider-neutral glibc baseline

The live baseline was invoked with deliberately injected bionic-style provider values.

Observed after sourcing `~/gl/env`:

```text
VK_DRIVER_FILES=<unset>
VK_ICD_FILENAMES=<unset>
```

Therefore the live baseline performs the intended ABI-boundary sanitation.

### Explicit Freedreno profile

Observed after sourcing the baseline and explicit profile:

```text
VK_DRIVER_FILES=
    $HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/
        freedreno_icd.aarch64.json

VK_ICD_FILENAMES=
    the same exact path

profile_internal=<unset>
```

The managed provider manifest was readable.

The live receipt therefore proves:

```text
inherited bionic provider removed
explicit glibc provider selected only by profile
loader variable pair equal
profile implementation variable private
```

## Passed installation gates

```text
live_gl_env                         PASS
live_freedreno_profile              PASS
live_gl_run                         PASS
live_vscode_launcher                PASS
live_obsidian_cli                   PASS
live_obsidian_gui                   PASS
freedreno_manifest_readable         PASS
baseline_vk_driver_files_absent     PASS
baseline_vk_icd_filenames_absent    PASS
profile_vk_driver_files_exact       PASS
profile_vk_icd_filenames_exact      PASS
profile_loader_variable_pair_equal  PASS
profile_internal_variable_private   PASS
```

## Gate closure

The following layers are now closed:

```text
provider-policy causal experiment
    PASS

ownership audit
    PASS

promoted source transaction
    IMPLEMENTED

real-device pre-deploy receipt
    PASS

live deployment
    PASS

live symlink and environment installation receipt
    PASS
```

The remaining work is consumer behavior validation against the promoted launchers.

## Promoted workload order

Use the smallest independent workload first:

```text
1. promoted gl-run self-contained GLX renderer
2. promoted VS Code GPU CDP primary identity
3. promoted VS Code CPU launcher policy/argv
4. promoted Obsidian GPU workload
5. promoted Obsidian CPU workload
```

Do not run all Electron controls simultaneously. Each probe requires the target application's processes to be absent at launch and cleans up only processes belonging to its own application tree.

## Promoted gl-run renderer gate

Added:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    validate-promoted-gl-run-renderer.sh
```

Commit:

```text
41561547b5f5d5e730d5a17e2fc6dc0c213edf35
```

The helper:

```text
requires a clean exact-HEAD checkout
builds the existing self-contained glibc GLX pbuffer consumer
runs that consumer through the live promoted gl-run
captures GL vendor, renderer, and version
requires a glibc interpreter
requires Zink renderer identity
requires Turnip or Adreno renderer identity
```

It does not create a window or run an event loop.

Expected semantic result:

```text
OpenGL consumer
    -> promoted gl-run
    -> explicit live Freedreno profile
    -> Zink
    -> Turnip / Adreno
```

## Promoted VS Code GPU identity gate

Added:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    validate-promoted-vscode-gpu-identity.sh
```

Commit:

```text
ac7613b0f4f057b0419b884a3367679a47c75322
```

The helper reuses the already validated CDP observer and identity classifier but changes the launch authority to:

```text
$HOME/.local/bin/code
```

It verifies that the live launcher is an exact symlink to the package-owned launcher before starting the workload.

Required result:

```text
probe_status=PASS
identity_status=PASS
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

This is a promotion-equivalence gate:

```text
experiment adapter result
    ==
promoted package launcher result
```

for the selected provider/device contract.

## Claim boundary

The live installation receipt alone proves environment composition, not rendering behavior.

The GLX gate proves a functioning OpenGL context and renderer identity, not long-duration presentation.

The VS Code CDP gate proves Chromium's primary GPU identity plus provider/device mappings, not complete zero-copy presentation or every renderer frame.

## Current state

```text
scoped policy installation:
    PASS

activation gap for current checkout:
    CLOSED BY DEPLOY

promoted gl-run renderer:
    NEXT

promoted VS Code GPU identity:
    AFTER GL-RUN

promoted VS Code CPU contract:
    PENDING

promoted Obsidian GPU/CPU:
    PENDING

atomic activation lifecycle redesign:
    OPEN, DEFERRED UNTIL CURRENT MIGRATION CLOSES
```

## Stop line

Do not yet:

```text
mark scoped policy promotion complete
remove the historical experiment adapters
change the bionic session policy
redesign tools/deploy
run multiple Electron probes concurrently
```

First pass the promoted GLX renderer and promoted VS Code GPU identity gates sequentially.
