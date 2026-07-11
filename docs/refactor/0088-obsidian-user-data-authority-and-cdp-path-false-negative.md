# 0088 — Obsidian User-Data Authority and CDP Path False Negative

## Status

The first promoted Obsidian GPU validation attempt did not produce a promotion receipt.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    current-obsidian-gpu-environment-identity-20260711-174948
```

The run reached the environment phase and kept the Obsidian main process alive for the full bounded observation, but the fresh CDP phase timed out waiting for `DevToolsActivePort` in the wrong directory.

No final files were produced:

```text
summary.tsv

gates.tsv

validation.status
```

The absence of those files is expected for this incomplete attempt and must not be interpreted as either a workload PASS or a graphics-policy FAIL.

## Observed environment-phase facts

The environment phase directly observed:

```text
main
zygote
renderer
```

The main process received:

```text
GL_GPU=1
VK_DRIVER_FILES=
    $HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/
        freedreno_icd.aarch64.json
VK_ICD_FILENAMES=
    the same exact managed glibc ICD
```

The observed zygote and renderer environments also contained the same values.

No selected observable environment showed:

```text
MESA_LOADER_DRIVER_OVERRIDE
GALLIUM_DRIVER
LIBGL_ALWAYS_SOFTWARE
LD_LIBRARY_PATH
non-empty LD_PRELOAD
/bionic/ provider path
```

The main argv contained the intended GPU branch:

```text
--disable-gpu-sandbox
--ignore-gpu-blocklist
--enable-features=Vulkan
--use-gl=angle
--use-angle=vulkan
--disable-gpu-vsync
```

The application also completed normal startup work:

```text
Loaded main app package
Checking for update using Github
Success.
Latest version is 1.12.7
App is up to date.
```

These observations are useful partial evidence for provider sanitation and application startup, but they are not sufficient for promotion closure.

## The actual defect

The validator passed:

```text
--user-data-dir
    $OUT/environment/user-data
```

However, the observed renderer command line used:

```text
--user-data-dir=$HOME/.config/obsidian
```

Obsidian therefore retained application ownership of its user-data location and derived the effective directory from the normal XDG configuration root.

The fresh CDP phase then waited for:

```text
$OUT/probe/user-data/DevToolsActivePort
```

while Obsidian was using its application-derived path instead.

The result was:

```text
DevToolsActivePort did not provide a port within 30 seconds
```

This was a probe path-authority mismatch, not evidence that ANGLE/Vulkan or the GPU process failed.

## Why the attempt is invalid as a promotion receipt

The first environment phase used the normal Obsidian profile path despite the validator's intent to use isolated state.

Therefore the run does not prove:

```text
normal user profile isolation
fresh profile independence
correct CDP endpoint discovery
selected primary GPU identity
provider-map and KGSL correlation
```

The partial environment facts remain historically true for the captured process tree, but the receipt is classified as:

```text
INCOMPLETE
INVALID_FOR_PROMOTION
```

It must not be merged with a later CDP-only run because the corrected contract requires two independently isolated application trees.

## Correct ownership model

For Obsidian, the experiment must align three concepts:

```text
XDG_CONFIG_HOME
application-derived Obsidian directory
DevToolsActivePort observation path
```

The corrected phase-local layout is:

```text
environment phase:
    XDG_CONFIG_HOME=$OUT/environment/config
    actual user data=$OUT/environment/config/obsidian

CDP phase:
    XDG_CONFIG_HOME=$OUT/probe/config
    actual user data=$OUT/probe/config/obsidian
```

The two phases therefore remain isolated from:

```text
each other
$HOME/.config/obsidian
normal locks and session state
normal DevToolsActivePort state
```

## Source correction

Updated generic Electron CDP probe:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    probe-electron-cdp-gpu-identity.sh
```

It now requires or derives:

```text
CONFIG_HOME
USER_DATA_DIR
```

and launches the application with:

```text
XDG_CONFIG_HOME=$CONFIG_HOME
--user-data-dir $USER_DATA_DIR
```

It watches exactly:

```text
$USER_DATA_DIR/DevToolsActivePort
```

Updated promoted Obsidian GPU validator:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    validate-promoted-obsidian-gpu-identity.sh
```

The corrected validator additionally gates:

```text
main_xdg_config_home_exact
all_observable_xdg_config_home_exact
main_uses_isolated_user_data
renderer_uses_isolated_user_data
normal_user_data_path_absent
cdp_config_home
cdp_user_data_dir
hardware_supports_vulkan
```

The validator also records `failure-stage.txt` and `validation.status=FAIL` when the environment cleanup, CDP probe, or classifier fails before final gate evaluation.

## Runtime-source boundary

No promoted runtime source changed.

Unchanged:

```text
modules/
packages/obsidian/launcher/obsidian-app
$HOME/gl/env
$HOME/gl/policy/vulkan/freedreno.sh
```

The defect and correction belong entirely to experiment/evidence ownership.

Therefore no deployment and no desktop-session restart are required.

## Required rerun

The next valid run must:

```text
sync the corrected experiment source
pass targeted shell syntax
start with no Obsidian process
use a fresh evidence root
rerun both environment and CDP phases
```

Do not reuse or append to:

```text
current-obsidian-gpu-environment-identity-20260711-174948
```

A successful corrected run must show:

```text
environment_config_home=$OUT/environment/config
environment_user_data=$OUT/environment/config/obsidian
cdp_config_home=$OUT/probe/config
cdp_user_data=$OUT/probe/config/obsidian
normal_user_data_path_absent=PASS
CDP primary Turnip/Adreno identity
managed provider and KGSL correlation
gate_failures=0
validation.status=PASS
```

## Current gate state

```text
VS Code GPU:
    PASS

VS Code CPU:
    PASS

Obsidian GPU first attempt:
    INCOMPLETE / INVALID FOR PROMOTION

Obsidian GPU corrected validator:
    READY FOR FRESH RERUN

Obsidian CPU:
    BLOCKED ON GPU PASS

scoped graphics-policy promotion:
    PENDING
```

## Stop line

Do not:

```text
classify the CDP timeout as a GPU-policy failure
reuse the first environment evidence as the final environment phase
run only the corrected CDP phase and merge it with the old phase
allow $HOME/.config/obsidian in the corrected process receipt
rerun VS Code or gl-run gates without a runtime-source change
advance to Obsidian CPU before the corrected GPU gate passes
```
