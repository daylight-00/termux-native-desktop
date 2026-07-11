# 0075 — VS Code Primary-Device Receipt PASS and Policy-Ownership Audit

## Status

The final machine-readable VS Code CDP primary-device comparison receipt passed.

Comparison evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    vscode-cdp-identity-comparison-20260711-151925
```

Compared evidence roots:

```text
explicit:
    $PREFIX/tmp/tnd-vulkan-policy-composition/
        vscode-cdp-explicit-20260711-151025

implicit:
    $PREFIX/tmp/tnd-vulkan-policy-composition/
        vscode-cdp-implicit-20260711-150155
```

Receipt status:

```text
PASS
```

All 26 comparison gates passed.

This closes the VS Code provider-policy experiment at the strongest currently required level:

```text
provider composition
primary selected provider
primary selected device family
ANGLE/Vulkan feature invariants
provider-object correlation
device-node correlation for the hardware path
```

## Control identities

Observed machine receipt:

```text
explicit:
    probe_status=PASS
    identity_status=PASS
    classification=FREEDRENO_TURNIP
    selected_provider=FREEDRENO_TURNIP
    selected_device_family=Adreno

implicit:
    probe_status=PASS
    identity_status=PASS
    classification=LVP_LLVMPIPE
    selected_provider=LVP
    selected_device_family=llvmpipe
```

## Feature invariants

Both controls retained:

```text
display_type=ANGLE_VULKAN
skia_backend=GaneshVulkan
vulkan_feature_status=enabled_on
```

Therefore the selected-device delta is not explained by one side disabling Vulkan or changing away from the ANGLE Vulkan feature mode.

## Selected-device delta

Explicit policy:

```text
classification:
    FREEDRENO_TURNIP

selected provider:
    Freedreno / Turnip

selected device family:
    Adreno

renderer identity:
    ANGLE (Qualcomm, Vulkan 1.4.354
    (Turnip Adreno (TM) 730 (0x07030001)),
    turnip Mesa driver-538.1.4)

provider relation:
    libvulkan_freedreno.so PRESENT

device-node relation:
    /dev/kgsl-3d0 PRESENT
```

Implicit discovery:

```text
classification:
    LVP_LLVMPIPE

selected provider:
    LVP

selected device family:
    llvmpipe

renderer identity:
    ANGLE (Mesa, Vulkan 1.4.305
    (llvmpipe (LLVM 19.1.7 128 bits) (0x00000000)),
    llvmpipe-0.0.1)

provider relation:
    libvulkan_lvp.so PRESENT

device-node relation:
    NOT_APPLICABLE
```

## Passed gates

```text
explicit_probe_status                 PASS
explicit_identity_status              PASS
implicit_probe_status                 PASS
implicit_identity_status              PASS

explicit_classification               PASS
explicit_selected_provider            PASS
explicit_selected_device_family       PASS
explicit_provider_path_relation       PASS
explicit_device_node_relation         PASS

implicit_classification               PASS
implicit_selected_provider            PASS
implicit_selected_device_family       PASS
implicit_provider_path_relation       PASS
implicit_device_node_relation         PASS

explicit_display_type                 PASS
implicit_display_type                 PASS
display_type_invariant                PASS

explicit_skia_backend                 PASS
implicit_skia_backend                 PASS
skia_backend_invariant                PASS

explicit_vulkan_feature               PASS
implicit_vulkan_feature               PASS
vulkan_feature_invariant              PASS

selected_provider_delta               PASS
selected_device_delta                 PASS
renderer_identity_delta               PASS
```

## Strongest supported causal claim

The completed controls support:

```text
same VS Code payload
same Electron/Chromium build
same GL_GPU=1 feature mode
same ANGLE Vulkan flags
same CDP primary-device observer
same identity classifier

explicit Freedreno provider policy
    -> Turnip / Adreno 730 primary selected
    -> Freedreno provider mapped
    -> KGSL mapped

implicit discovery
    -> LVP / llvmpipe primary selected
    -> LVP provider mapped
    -> no hardware-device-node relation
```

Therefore:

```text
For the captured VS Code consumer and runtime state,
the application-main Vulkan provider-policy input
causally changes ANGLE's primary selected Vulkan provider and device.
```

The earlier `mapped != selected` concern is closed for this A/B because the selected provider is now identified through Chromium's structured primary-GPU report and correlated with process maps.

## Experiment gate closure

```text
VS Code explicit workload topology:
    PASS

VS Code explicit 60-second survival:
    PASS

VS Code implicit workload topology:
    PASS

VS Code implicit 60-second survival:
    PASS

provider-composition A/B receipt:
    PASS

primary-device A/B receipt:
    PASS

application-main provider-policy causality:
    PROVEN

VS Code provider-policy experiment:
    CLOSED FOR PROMOTION DESIGN INPUT
```

This does not mean the current promoted ownership model is already correct.

It means the consumer requirement is now established strongly enough to design the ownership migration without more VS Code provider-selection experiments.

## Current promoted responsibility structure

Static inspection already establishes the following current structure.

### Shared producer

```text
modules/gl/overlay/home/gl/env
```

currently:

```text
defines the glibc Freedreno ICD pathname
exports VK_DRIVER_FILES
exports VK_ICD_FILENAMES
clears both variables if the ICD is unavailable
```

This makes explicit Freedreno provider selection part of the shared glibc-world environment rather than a package-specific composition choice.

### Direct VS Code consumer

```text
packages/vscode/launcher/code
```

currently:

```text
sources $HOME/gl/env
checks that VK_DRIVER_FILES is nonempty
enables ANGLE Vulkan only when GL_GPU=1 and the shared pin exists
adds --use-gl=angle
adds --use-angle=vulkan
adds --disable-gpu-vsync
```

The launcher therefore directly depends on provider policy produced by the shared environment.

### Direct OpenGL/Zink consumer

```text
modules/gl/overlay/home/gl/bin/gl-run
```

currently:

```text
sources $HOME/gl/env
requires VK_DRIVER_FILES
adds MESA_LOADER_DRIVER_OVERRIDE=zink
```

This is a separate consumer class:

```text
OpenGL consumer
    -> Zink feature mode
    -> explicitly selected Vulkan provider
```

Its requirements cannot be inferred solely from the VS Code ANGLE result, even though earlier Zink experiments also establish explicit-provider requirements.

### Transitive Obsidian consumers

```text
packages/obsidian/launcher/obsidian
packages/obsidian/launcher/obsidian-app
```

source the shared environment and therefore inherit the provider pin even when they do not directly reference the `VK_*` variable names.

This distinguishes:

```text
direct policy consumer
```

from:

```text
transitive shared-environment consumer
```

Both must be considered before moving policy ownership.

### Integrated documentation assumptions

Current integrated architecture documentation says that every glibc launcher sources the shared environment and that the shared environment pins both Vulkan provider variables.

The architecture documentation also describes the shared pin as the glibc application policy that overrides the bionic session policy.

Therefore a code-only change would leave the integrated model inconsistent.

## Ownership question

The now-proven VS Code requirement is:

```text
VS Code ANGLE Vulkan needs explicit Freedreno provider selection
to preserve the Turnip/Adreno hardware path in the captured runtime state.
```

The remaining design question is not whether VS Code needs the policy.

It is:

```text
Which semantic object should own that policy?
```

Candidate ownership domains include:

```text
shared glibc-world baseline
shared source-only provider-profile helper
OpenGL/Zink bridge composition
each application package launcher
```

The project principles favor the smallest scope that preserves validated consumer contracts, but no candidate is selected until the current branch's complete producer/consumer inventory is captured.

## Branch-authoritative audit

GitHub code-search results are not sufficient for this audit because the refactor branch is far ahead of and diverged from the default branch, while code-search results can refer to the default-branch historical layout.

The authoritative audit must run against the live checkout's tracked files and exact HEAD.

Added corrected helper:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    audit-promoted-vulkan-policy-ownership-v2.sh
```

Commit:

```text
92cc5e9cd04708dad31634560ae1625ae713613d
```

The helper:

```text
requires no tracked working-tree modifications
records branch and exact HEAD
uses git grep over the current checkout
classifies promoted, integrated-doc, experiment/history, and other scopes
classifies policy producers, direct references, and transitive shared-env consumers
checks known current contracts
produces a machine-readable occurrence inventory
performs no runtime or promoted-file mutation
```

The earlier helper:

```text
audit-promoted-vulkan-policy-ownership.sh
```

commit:

```text
7c83b56928213ec914b8321d52af27139e0b76e0
```

is superseded before use because its VS Code ANGLE-flag contract check passed an extra positional argument to the checker and could validate the wrong pattern.

Do not use the unsuffixed helper.

## Audit tokens

The v2 audit scans:

```text
VK_DRIVER_FILES
VK_ICD_FILENAMES
GL_ICD
GLIBC_FREEDRENO_ICD
source $HOME/gl/env
source ~/gl/env
MESA_LOADER_DRIVER_OVERRIDE
GL_GPU
```

These cover:

```text
provider-policy producers and clearers
provider-policy direct references
provider path definitions
transitive shared-env consumers
OpenGL/Zink composition
application GPU feature-mode gates
```

## Audit outputs

```text
repository-root.txt
branch.txt
head.txt
all-occurrences.tsv
promoted-or-validation-occurrences.tsv
integrated-documentation-occurrences.tsv
experiment-or-history-occurrences.tsv
other-tracked-occurrences.tsv
known-contracts.tsv
audit-summary.tsv
audit.status
```

A PASS means:

```text
the exact-HEAD inventory completed
and the currently known contracts were found
```

A PASS does not authorize removing the shared `VK_*` policy.

## Next decision branches

### Small promoted surface

If the exact-HEAD inventory shows that promoted consumers are limited to:

```text
shared gl env
VS Code launcher
gl-run
Obsidian launchers
```

then a bounded migration transaction can be designed around an explicit provider-profile helper and consumer-local application of that profile.

### Additional direct consumers

If more promoted launchers or tests directly consume `VK_*`, each must be assigned an explicit policy contract before shared pin removal.

### Additional transitive consumers

If more promoted launchers source `~/gl/env` without naming `VK_*`, they must not be assumed provider-neutral. Their validated feature mode and expected provider behavior must be identified first.

### Documentation-only references

Historical experiment references do not become migration blockers merely because they contain old variable names. Integrated operational and architecture documentation must change with the promoted transaction; historical evidence must remain unchanged.

## Current gate state

```text
VS Code primary-device comparison receipt:
    PASS

VS Code selected-provider/device causality:
    PROVEN

VS Code experiment requirement:
    CLOSED

promoted policy producer/consumer inventory:
    NEXT GATE

provider-policy ownership decision:
    BLOCKED ON INVENTORY

promoted mutation:
    NOT STARTED
```

## Stop line

Do not yet:

```text
remove the shared VK_* exports
move the ICD path into only the VS Code launcher
change gl-run
change either Obsidian launcher
update integrated architecture claims
run deployment
```

First run the v2 static audit and preserve its exact branch/HEAD receipt.
