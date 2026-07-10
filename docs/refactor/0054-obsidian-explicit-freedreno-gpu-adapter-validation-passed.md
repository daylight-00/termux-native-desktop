# 0054 — Obsidian Explicit-Freedreno GPU Adapter Validation Passed

## Status

The real Obsidian Electron consumer passed the scoped explicit-Freedreno GPU-path control.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/obsidian-explicit-gpu-20260711-080703
```

Launch inputs:

```text
CONTROL_GL_GPU=1
VULKAN_POLICY_MODE=explicit-freedreno
LIBGL_ALWAYS_SOFTWARE unset
```

Launcher:

```text
experiments/glibc/vulkan-policy-composition/recipe/launch-obsidian-with-policy.sh
```

Capture harness:

```text
experiments/glibc/selected-obsidian-closure/recipe/capture-control.sh
```

## Validation result

Observed:

```text
topology gate: PASS
startup stabilization elapsed: 3 seconds
survival gate: PASS
survival duration: 100 seconds
maps capture: PASS
identity enrichment: PASS
semantic classification: PASS
semantic review objects: 0
```

This establishes that scoped explicit provider policy is compatible with the tested Obsidian GPU-feature path for the captured runtime state.

## Final process topology

Observed final process set:

```text
main      1
zygote    2
gpu       1
utility   1
renderer  1
```

The actual final classes were:

```text
main
zygote
zygote
gpu
utility
renderer
```

The explicit GPU control therefore differs structurally from the earlier CPU controls by containing a live Chromium/Electron GPU process at the final capture gate.

The GPU process command line contains:

```text
--type=gpu-process
--use-gl=angle
--use-angle=vulkan
--enable-features=...Vulkan
```

The main process was launched with:

```text
--disable-gpu-sandbox
--ignore-gpu-blocklist
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
--disable-gpu-vsync
```

These argv facts establish requested feature mode. They are not, by themselves, proof of selected provider ownership or submitted rendering work.

## Semantic result

Observed semantic counts:

```text
APP_LOCAL_DATA                         6
APP_LOCAL_ELF                          5
APP_MUTABLE_STATE                     19
DEVICE_NODE_GPU                        1
PROVIDER_FONT_DATA                     3
PROVIDER_GRAPHICS_GBM_ELF              1
PROVIDER_GRAPHICS_VULKAN_DRIVER_ELF    1
PROVIDER_GRAPHICS_VULKAN_LAYER_ELF     1
PROVIDER_LOCALE_DATA                  12
PROVIDER_PREFIX_ELF                   41
PROVIDER_ROOTFS_ELF                   58
PROVIDER_SCHEMA_DATA                   1
RUNTIME_CACHE_FONTCONFIG               4
RUNTIME_CACHE_MESA                     1
WORLD_SUBSTRATE_ELF                    6
```

Review count:

```text
0
```

The semantic set therefore contains the hardware Vulkan driver class and KGSL device-node class while passing the real Electron topology and 100-second survival gates.

## Claim boundary

The current evidence proves:

```text
Obsidian GPU feature mode
    + scoped explicit-Freedreno policy
    -> stable real Electron topology
    -> live GPU process
    -> 100-second survival
    -> mapped hardware Vulkan driver class
    -> mapped KGSL device node
```

It does not yet prove:

```text
which process class maps the Freedreno driver
which process class maps KGSL
whether the GPU process is the sole owner of those mappings
whether rendering commands were submitted to the device
whether implicit discovery with the same GL_GPU=1 mode preserves the workload
```

Those questions require process-class mapping and same-feature-mode policy A/B evidence.

## Count-comparison warning

The earlier baseline CPU control captured 161 unique objects while this explicit GPU control captured 160.

The current result also shows three font-data objects rather than four in the older control.

Do not interpret raw total-count differences as policy deltas.

Runtime capture timing can change which lazily mapped data files are present at the final gate. Policy inference must use:

```text
same application feature mode
same topology/survival contract
exact path-set comparison
semantic-class comparison
process-class graphics relation comparison
```

rather than total object count alone.

## Next gate

First derive process-class graphics ownership for this explicit control using the existing reporter.

Then run the same Obsidian GPU-feature control with only:

```text
VULKAN_POLICY_MODE=implicit-discovery
```

changed.

Keep:

```text
CONTROL_GL_GPU=1
LIBGL_ALWAYS_SOFTWARE unset
same launcher adapter
same capture harness
same 100-second survival budget
```

The resulting A/B should compare:

```text
topology classes
survival result
semantic sets
hardware driver/device presence
alternate ICD presence
process-class graphics relations
```

No promoted launcher or global environment policy should change before that comparison is complete.
