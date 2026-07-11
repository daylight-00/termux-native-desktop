# 0085 — VS Code Child `/proc/environ` Observability False Negative

## Status

The first strengthened promoted VS Code GPU environment/identity run ended with:

```text
gate_failures=6
validation.status=FAIL
```

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    current-vscode-gpu-environment-identity-20260711-170154
```

Captured repository state:

```text
branch:
    refactor/module-package-layout

head:
    f6a5d0e3987cf9733a0f468ac6fc55906bb072a6
```

The six failures were:

```text
zygote_gl_gpu_one
zygote_vk_driver_files_exact
zygote_vk_icd_filenames_exact
gpu_gl_gpu_one
gpu_vk_driver_files_exact
gpu_vk_icd_filenames_exact
```

Classification:

```text
VS Code launch:
    PASS

main process environment/argv:
    PASS

bionic/Zink/Gallium leak checks:
    PASS FOR OBSERVABLE ENVIRONMENT

CDP primary GPU identity:
    PASS

provider/device correlation:
    PASS

six child exact-environment gates:
    INVALID OBSERVABILITY ASSUMPTION

overall machine receipt:
    INVALID FALSE NEGATIVE
```

This is not evidence of a runtime provider failure or a graphics-policy leak.

## Direct evidence

### Observable launch chain

The environment probe captured non-empty process environments for:

```text
launch-wrapper:
    83 entries

node-cli:
    85 entries

main:
    88 entries

crashpad:
    90 entries
```

For the main process it directly observed:

```text
GL_GPU=1
VK_DRIVER_FILES=<exact managed glibc Freedreno ICD>
VK_ICD_FILENAMES=<same exact managed glibc Freedreno ICD>
VK_LOADER_DEBUG=all
```

The selected environment receipt contained no:

```text
MESA_LOADER_DRIVER_OVERRIDE
GALLIUM_DRIVER
LIBGL_ALWAYS_SOFTWARE
LD_LIBRARY_PATH
non-empty LD_PRELOAD
/bionic/ path
```

All corresponding global observable-value gates passed.

### Main argv

The actual main process contained:

```text
--disable-gpu-sandbox
--ignore-gpu-blocklist
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
--disable-gpu-vsync
```

The exact token:

```text
--disable-gpu
```

was absent.

All argv gates passed.

### Child process `/proc` observation

The two zygote processes reported:

```text
state=READ_OK
entry_count=0
selected_key_count=0
```

The GPU process reported:

```text
state=READ_OK
entry_count=1
selected_key_count=0
```

Utility and renderer processes showed the same near-empty pattern.

Therefore the failed gates did not observe wrong values. They attempted to require values from a process environment view whose content was empty or effectively empty at capture time.

A successful read syscall and an observable non-empty environment are different properties.

The validator incorrectly conflated:

```text
READ_OK
```

with:

```text
all inherited environment entries remain observable
```

### Actual GPU identity

The independent CDP phase passed completely:

```text
classification=FREEDRENO_TURNIP
selected_provider=FREEDRENO_TURNIP
selected_device_family=Adreno
provider_path_relation=PRESENT
device_node_relation=PRESENT
display_type=ANGLE_VULKAN
skia_backend=GaneshVulkan
vulkan_feature_status=enabled_on
correlation_state=PASS
```

Primary renderer:

```text
ANGLE (Qualcomm,
    Vulkan 1.4.354
    (Turnip Adreno (TM) 730),
    turnip Mesa driver-538.1.4)
```

Mapped runtime paths included:

```text
managed libvulkan_freedreno.so
/dev/kgsl-3d0
```

Thus the GPU process actually selected the intended hardware provider and device despite its near-empty `/proc/<pid>/environ` view.

## Correct observability model

The evidence supports three separate levels.

### Level 1 — exact environment values

Require exact values only where `/proc/<pid>/environ` contains a meaningful non-empty environment:

```text
launch-wrapper
node-cli
main
```

These processes directly prove the public launcher composed:

```text
GL_GPU=1
exact managed Vulkan pair
no observable inherited bionic provider path
no observable Zink/Gallium override
```

### Level 2 — child process existence and read attempt

For:

```text
zygote
gpu
```

require:

```text
process observed
/proc/<pid>/environ read attempt succeeded
```

Do not require key/value presence when the returned content is empty.

Do not interpret an empty environment view as either:

```text
variable definitely absent
```

or:

```text
variable inheritance failed
```

It only bounds the claim:

```text
child exact environment value not observable through this capture
```

### Level 3 — actual graphics identity

Use CDP primary identity plus process mappings for the GPU-effective claim:

```text
ANGLE Vulkan
Turnip/Freedreno
Adreno 730
managed provider mapped
KGSL node mapped
```

This is stronger evidence for effective selected graphics identity than requiring a policy variable to remain visible in a mutable or cleared `/proc` environment buffer.

## Validator correction

Updated:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    validate-promoted-vscode-gpu-identity.sh
```

Correction commit:

```text
3ba7cd9b78273788256f1046b02f9db10b6f6268
```

New exact-environment classes:

```text
launch-wrapper
node-cli
main
```

New child gates:

```text
zygote_process_observed
zygote_environment_read_attempt
gpu_process_observed
gpu_environment_read_attempt
```

Removed invalid requirements:

```text
zygote exact GL_GPU/VK values
gpu exact GL_GPU/VK values
```

Renamed absence/value gates to make their scope explicit:

```text
all_observable_*
observable_*_absent
```

The summary now records:

```text
zygote_max_observable_environment_entries
gpu_max_observable_environment_entries
child_environment_value_claim=NOT_MADE_WHEN_PROC_ENVIRON_EMPTY
```

## Evidence interpretation

The failed receipt remains useful and should not be deleted.

It establishes:

```text
main environment composition:
    PASS

main GPU argv:
    PASS

observable policy leak checks:
    PASS

CDP selected provider/device:
    PASS

child exact environment values:
    NOT OBSERVABLE
```

It must not be promoted as a clean machine PASS because the validator status is FAIL and the gate definitions were invalid.

A fresh run with the corrected validator is required to produce the canonical current-head receipt.

## Current gate state

```text
expanded pre-deploy:
    PASS

expanded live installation:
    PASS

current-head gl-run renderer:
    PASS

first strengthened VS Code GPU run:
    INVALID FALSE NEGATIVE

corrected VS Code GPU validator:
    READY

VS Code CPU:
    BLOCKED ON CLEAN GPU RECEIPT
```

## Stop line

Do not:

```text
classify empty child /proc/environ as a provider failure
classify empty child /proc/environ as proof of variable absence
change the promoted VS Code launcher
change the glibc baseline
repeat pre-deploy or installation gates
reuse the failed evidence root
proceed to CPU mode before a clean corrected GPU receipt
```

Sync the validator-only correction and rerun with a fresh evidence root.
