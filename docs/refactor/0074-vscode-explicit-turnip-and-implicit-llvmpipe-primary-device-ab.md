# 0074 — VS Code Primary-Device A/B: Explicit Turnip vs Implicit llvmpipe

## Status

The symmetric Chrome DevTools Protocol GPU identity controls now identify the primary Vulkan device under both provider-policy modes.

The compared controls keep the same:

```text
VS Code payload
Electron/Chromium build
GL_GPU=1
ANGLE Vulkan feature flags
CDP SystemInfo.getInfo observer
GPU-process map correlation
```

The provider-policy dimension is:

```text
explicit-freedreno:
    VK_DRIVER_FILES=<Freedreno ICD>
    VK_ICD_FILENAMES=<Freedreno ICD>

implicit-discovery:
    VK_DRIVER_FILES unset
    VK_ICD_FILENAMES unset
```

Primary selected-device result:

```text
explicit-freedreno:
    Turnip Adreno 730

implicit-discovery:
    LVP llvmpipe
```

This closes the selected-device level of the VS Code provider-policy A/B.

## Implicit receipt

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    vscode-cdp-implicit-20260711-150155
```

Machine classification:

```text
probe_status=PASS
primary_index=0
primary=true
classification=LVP_LLVMPIPE
selected_provider=LVP
selected_device_family=llvmpipe
provider_path_relation=PRESENT
device_node_relation=NOT_APPLICABLE
correlation_state=PASS
```

Primary device identity:

```text
vendorString:
    Google Inc. (Mesa)

deviceString:
    ANGLE (Mesa, Vulkan 1.4.305
    (llvmpipe (LLVM 19.1.7 128 bits) (0x00000000)),
    llvmpipe-0.0.1)

driverVendor:
    Mesa

driverVersion:
    0.0.1
```

Feature invariants:

```text
displayType=ANGLE_VULKAN
glImplementationParts=(gl=egl-angle,angle=vulkan)
skiaBackendType=GaneshVulkan
vulkan=enabled_on
```

Mapped provider objects:

```text
app-local libEGL.so
app-local libGLESv2.so
app-local libvulkan.so.1
rootfs libVkLayer_MESA_device_select.so
rootfs libgbm.so.1.0.0
rootfs libvulkan_gfxstream.so
rootfs libvulkan_lvp.so
```

Selected-provider conclusion:

```text
LVP / llvmpipe is primary selected.
Gfxstream is mapped but is not the primary selected device in this run.
```

## Explicit receipt

The exact explicit evidence-root pathname remains held in the live-device shell variable:

```text
$VS_CDP_EXPLICIT_OUT
```

It will be persisted by the final identity-comparison receipt.

Machine classification:

```text
probe_status=PASS
primary_index=0
primary=true
classification=FREEDRENO_TURNIP
selected_provider=FREEDRENO_TURNIP
selected_device_family=Adreno
provider_path_relation=PRESENT
device_node_relation=PRESENT
correlation_state=PASS
```

Primary device identity:

```text
vendorString:
    Google Inc. (Qualcomm)

deviceString:
    ANGLE (Qualcomm, Vulkan 1.4.354
    (Turnip Adreno (TM) 730 (0x07030001)),
    turnip Mesa driver-538.1.4)

driverVendor:
    Mesa
```

Feature invariants:

```text
displayType=ANGLE_VULKAN
glImplementationParts=(gl=egl-angle,angle=vulkan)
skiaBackendType=GaneshVulkan
vulkan=enabled_on
```

Mapped provider/device objects:

```text
app-local libEGL.so
app-local libGLESv2.so
app-local libvulkan.so.1
provider-store libvulkan_freedreno.so
rootfs libVkLayer_MESA_device_select.so
rootfs libgbm.so.1.0.0
/dev/kgsl-3d0
```

Selected-provider conclusion:

```text
Freedreno/Turnip is primary selected.
The selected device family is Adreno 730.
The same GPU process maps the Freedreno provider and KGSL device node.
```

## Strongest supported causal statement

The completed experiment supports:

```text
same VS Code consumer
same ANGLE Vulkan feature mode
same CDP primary-device observer
same workload class

explicit Freedreno policy
    -> Turnip Adreno 730 primary device
    -> Freedreno provider mapped
    -> KGSL mapped

implicit discovery
    -> llvmpipe primary device
    -> LVP provider mapped
    -> no KGSL relation
```

Therefore:

```text
For this captured VS Code/runtime state,
the application-main Vulkan provider-policy input
causally changes the primary Vulkan device selected by ANGLE.
```

This is stronger than the earlier map-composition-only claim.

## What remains unchanged

Both controls report:

```text
ANGLE_VULKAN
GaneshVulkan
vulkan=enabled_on
hardwareSupportsVulkan=true
```

The difference is not explained by one control disabling Vulkan or switching away from ANGLE Vulkan.

The changed result is the selected provider/device:

```text
Turnip Adreno 730
    versus
LVP llvmpipe
```

## Driver-version field caution

The explicit CDP device row reported:

```text
driverVendor=Mesa
driverVersion=driver
```

The useful precise identity is carried by the renderer/device string:

```text
turnip Mesa driver-538.1.4
```

Do not rewrite the structured `driverVersion` field as `538.1.4`; preserve the distinction between the raw CDP columns and the descriptive renderer string.

## Identity classifier parser correction

The first classifier implementation used Bash whitespace `IFS` to split a tab-separated primary-device row.

Software-device rows contain empty columns for:

```text
subSysId
revision
```

Bash whitespace splitting can collapse adjacent tab delimiters and shift later fields.

The classifier was corrected before this receipt was accepted. Each TSV column is now extracted independently with:

```text
awk -F '\t'
```

Correction commit:

```text
c770fd693527e7b3302b11450a039fd3b3bae357
```

The resulting implicit summary preserves:

```text
sub_sys_id=<empty>
revision=<empty>
vendor_string=Google Inc. (Mesa)
device_string=<llvmpipe identity>
```

## Added final primary-device comparison receipt

Added:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    compare-vscode-cdp-gpu-identities.sh
```

Commit:

```text
fb0710d0d63d6e82c6f52dfd29c4fd130e2aeb94
```

The receipt reads the two completed and classified CDP evidence roots without relaunching VS Code.

It verifies:

```text
both CDP probes PASS
both identity classifiers PASS

explicit classification=FREEDRENO_TURNIP
explicit provider path=PRESENT
explicit device node=PRESENT

implicit classification=LVP_LLVMPIPE
implicit provider path=PRESENT

both displayType=ANGLE_VULKAN
both skiaBackendType=GaneshVulkan
both vulkan feature=enabled_on

selected provider differs
selected device family differs
renderer identity differs
```

Outputs:

```text
control-identities.tsv
comparison-gates.tsv
identity-delta.tsv
comparison.status
```

## Promotion ownership boundary

The selected-device experiment answers whether explicit provider policy matters for VS Code:

```text
yes — it is required to preserve the Turnip/Adreno hardware path
in the captured runtime state.
```

It does not by itself decide where that policy must be owned in the promoted repository/runtime model.

The current promoted files still encode:

```text
modules/gl/overlay/home/gl/env:
    globally pins VK_DRIVER_FILES and VK_ICD_FILENAMES

packages/vscode/launcher/code:
    consumes the shared pin and only enables ANGLE/Vulkan flags
```

The next design question is:

```text
Should explicit Freedreno provider selection remain a shared glibc-world baseline,
or move to the smallest consumer/package launch-composition scope?
```

The project principles and the current experiment point toward the smallest valid scope, but no promoted file should change before a repository-wide ownership and consumer-assumption audit.

The audit must include at least:

```text
modules/gl/overlay/home/gl/env
modules/gl/overlay/home/gl/bin/gl-run
packages/vscode/launcher/code
packages/obsidian launch integration
all other promoted consumers of VK_DRIVER_FILES / VK_ICD_FILENAMES
architecture and operational documentation
live deployment links and validation tests
```

## Current gate state

```text
VS Code explicit topology/survival/maps:
    PASS

VS Code implicit topology/survival/maps:
    PASS

provider-composition A/B receipt:
    PASS

implicit primary selected provider:
    LVP / llvmpipe

explicit primary selected provider:
    Freedreno / Turnip

explicit primary selected device:
    Adreno 730

selected-device policy causality:
    PROVEN

final identity comparison receipt:
    NEXT MACHINE GATE

promoted provider-policy ownership migration:
    BLOCKED ON STATIC OWNERSHIP/CONSUMER AUDIT
```

## Stop line

Do not yet:

```text
remove VK_* pins from shared gl/env;
change the promoted VS Code launcher;
change the promoted Obsidian launcher;
change gl-run;
claim every glibc consumer should use explicit Freedreno;
claim every consumer should use implicit discovery;
```

First run the final identity comparison receipt, then inventory every promoted policy producer and consumer before designing the migration transaction.
