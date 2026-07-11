# 0083 — Expanded Graphics-Policy Pre-Deploy and Live Installation PASS

## Status

The current-head regression sequence passed its expanded no-mutation pre-deploy gate and expanded live installation receipt after the bionic Zink/Gallium sanitation correction.

Captured repository state:

```text
branch:
    refactor/module-package-layout

head:
    5ed76ec9c7409a141da02a28b5297b8b71965467
```

Pre-deploy evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    promoted-graphics-policy-predeploy-20260711-162231
```

Live installation evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    live-graphics-policy-installation-20260711-162316
```

Both receipts ended with:

```text
gate_failures=0
status=PASS
```

## Expanded pre-deploy receipt

Passed source and deployment gates:

```text
shell_syntax                                 PASS
policy_scope_smoke                           PASS
deploy_smoke                                 PASS
live_deploy_dry_run                          PASS
baseline_clears_vk_driver_files              PASS
baseline_clears_bionic_opengl_bridge         PASS
baseline_does_not_export_vk_driver_files     PASS
baseline_does_not_export_vk_icd_filenames    PASS
baseline_does_not_export_mesa_loader_override PASS
baseline_does_not_export_gallium_driver      PASS
profile_exports_vk_driver_files              PASS
profile_exports_vk_icd_filenames             PASS
gl_run_sources_profile                       PASS
gl_run_adds_zink_explicitly                  PASS
vscode_sources_profile                       PASS
obsidian_app_sources_profile                 PASS
dry_run_plans_profile                        PASS
dry_run_plans_gl_env                         PASS
dry_run_plans_vscode                         PASS
dry_run_plans_obsidian_app                   PASS
```

The repository policy-scope smoke also reported:

```text
vulkan policy scope smoke: PASS
```

The smoke name is historical. Its current contract covers both Vulkan provider scope and OpenGL bridge/Gallium sanitation.

## Expanded live baseline receipt

The live receipt deliberately injected bionic/session-style graphics policy:

```text
VK_DRIVER_FILES=/bionic/freedreno.json
VK_ICD_FILENAMES=/bionic/freedreno.json
MESA_LOADER_DRIVER_OVERRIDE=zink
GALLIUM_DRIVER=llvmpipe
```

Observed after sourcing the live `~/gl/env`:

```text
VK_DRIVER_FILES=<unset>
VK_ICD_FILENAMES=<unset>
MESA_LOADER_DRIVER_OVERRIDE=<unset>
GALLIUM_DRIVER=<unset>
```

This proves that the live glibc boundary now removes both policy classes:

```text
bionic Vulkan provider selection
bionic OpenGL bridge/Gallium selection
```

The result is stronger than checking only source text because it exercises the actual live symlink and shell behavior.

## Expanded explicit-profile receipt

Observed after sourcing the live baseline and the explicit Freedreno profile:

```text
VK_DRIVER_FILES=
    $HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/
        freedreno_icd.aarch64.json

VK_ICD_FILENAMES=
    the same exact path

MESA_LOADER_DRIVER_OVERRIDE=<unset>
GALLIUM_DRIVER=<unset>
profile_internal=<unset>
```

This proves that the explicit Vulkan profile:

```text
selects the intended glibc provider
sets both loader variables together
does not also select an OpenGL bridge
does not select a Gallium driver
does not leak its implementation variable
```

Therefore ANGLE/Vulkan consumers can use the explicit provider without inheriting or acquiring the Zink bridge.

## Passed live installation gates

```text
live_gl_env                              PASS
live_freedreno_profile                   PASS
live_gl_run                              PASS
live_vscode_launcher                     PASS
live_obsidian_cli                        PASS
live_obsidian_gui                        PASS
freedreno_manifest_readable              PASS
baseline_vk_driver_files_absent          PASS
baseline_vk_icd_filenames_absent         PASS
baseline_mesa_loader_override_absent     PASS
baseline_gallium_driver_absent           PASS
profile_vk_driver_files_exact            PASS
profile_vk_icd_filenames_exact           PASS
profile_loader_variable_pair_equal       PASS
profile_mesa_loader_override_absent      PASS
profile_gallium_driver_absent            PASS
profile_internal_variable_private        PASS
```

## Live target identity

All six live runtime entry points remained exact symlinks into the canonical checkout:

```text
$HOME/gl/env
$HOME/gl/policy/vulkan/freedreno.sh
$HOME/gl/bin/gl-run
$HOME/.local/bin/code
$HOME/gl/bin/obsidian
$HOME/gl/bin/obsidian-app
```

No deployment mutation was required for this correction because no new leaf was introduced. Pulling the changed `gl/env` source activated the correction through the existing symlink.

## Closed contract layers

The following current-head layers are now closed:

```text
source syntax:
    PASS

repository scope regression:
    PASS

deploy model smoke and dry-run:
    PASS

live managed targets:
    PASS

live bionic Vulkan-provider sanitation:
    PASS

live bionic OpenGL bridge/Gallium sanitation:
    PASS

live explicit Freedreno provider selection:
    PASS

explicit profile bridge neutrality:
    PASS
```

## Remaining regression sequence

The correction changed the shared baseline used by all promoted glibc consumers. Actual workloads must therefore be revalidated at one coherent post-correction source state.

Required order:

```text
1. promoted gl-run actual renderer
2. promoted VS Code GPU primary identity
3. promoted VS Code CPU policy/argv/environment
4. promoted Obsidian GPU
5. promoted Obsidian CPU
```

The first two are regression checks for previously passed workloads. The CPU and Obsidian gates add new promotion evidence.

## Expected gl-run regression

The sanitized baseline should remove any inherited session bridge policy before `gl-run` explicitly adds its own:

```text
baseline
    -> no VK provider
    -> no Zink/Gallium override

gl-run
    -> explicit Freedreno provider
    -> MESA_LOADER_DRIVER_OVERRIDE=zink
    -> GALLIUM_DRIVER remains absent
```

Expected actual renderer:

```text
zink ... Turnip Adreno (TM) 730
```

## Expected VS Code GPU regression

The GPU branch should remain:

```text
explicit Freedreno provider
ANGLE Vulkan
no Zink/Gallium override
Turnip / Adreno 730 primary device
managed provider path present
/dev/kgsl-3d0 present
```

The current CDP validator proves selected provider/device and feature mode, but does not yet capture process environment fields. The subsequent CPU validator captures those environment fields directly. A future GPU environment assertion may be added only if the current regression exposes ambiguity.

## Claim boundary

These receipts prove environment composition and managed-target identity.

They do not prove actual graphics workload behavior after the sanitation correction. That is why the actual-renderer and CDP regressions remain required.

## Current gate state

```text
expanded pre-deploy:
    PASS

expanded live installation:
    PASS

current-head promoted gl-run renderer:
    NEXT

current-head promoted VS Code GPU identity:
    AFTER GL-RUN

promoted VS Code CPU policy:
    AFTER GPU

promoted Obsidian GPU/CPU:
    PENDING

scoped graphics-policy promotion closure:
    PENDING
```

## Stop line

Do not:

```text
rerun tools/deploy without an observed target mismatch
restart the desktop session
skip the gl-run or VS Code GPU regressions
run Electron probes concurrently
classify environment receipts as renderer proof
mark the transaction complete
```

Proceed with the current-head promoted `gl-run` renderer regression.
