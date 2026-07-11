# 0082 — Bionic Zink Policy Leak and glibc Boundary Correction

## Status

The promoted VS Code GPU primary-identity gate passed at:

```text
3b8b397664507a6df62e99cfbc00916027717c8a
```

Before running the promoted CPU gate, a contract review found that the glibc baseline sanitation was incomplete.

This finding occurred before the CPU workload was launched.

Classification:

```text
CPU workload failure:
    NOT OBSERVED

promoted GPU receipt:
    VALID FOR ITS CAPTURED HEAD

current source contract:
    CORRECTED

current-HEAD promotion gates:
    REOPENED FOR REGRESSION VALIDATION
```

## Discovered policy leak

The bionic desktop session exports:

```text
VK_ICD_FILENAMES=<bionic Freedreno ICD>
VK_DRIVER_FILES=<bionic Freedreno ICD>
MESA_LOADER_DRIVER_OVERRIDE=zink
```

The first promoted `~/gl/env` correction removed only the Vulkan pair:

```text
unset VK_ICD_FILENAMES VK_DRIVER_FILES
```

It did not remove:

```text
MESA_LOADER_DRIVER_OVERRIDE
GALLIUM_DRIVER
```

Therefore a glibc process launched from the desktop could begin with:

```text
Vulkan provider policy:
    sanitized

OpenGL bridge policy:
    inherited from bionic session
```

This violated the intended semantic split:

```text
shared baseline sanitation
explicit Vulkan provider selection
OpenGL bridge selection
application feature mode
```

In particular, VS Code/Obsidian CPU branches and ANGLE-Vulkan branches could carry a session-wide Zink override even though those package launchers do not own an OpenGL/Zink composition.

## Why this is a real architecture defect

`MESA_LOADER_DRIVER_OVERRIDE=zink` is not only an informational variable. It selects a Mesa loader driver/bridge mode.

The bionic desktop owns that choice for native OpenGL clients such as optional Picom and native GL diagnostics.

The glibc world has a separate provider and library graph. Its OpenGL bridge is deliberately owned by:

```text
$HOME/gl/bin/gl-run
```

Therefore:

```text
bionic session Zink policy
    !=
glibc-world shared baseline
```

and the inherited variable must be removed before a glibc consumer composes its own policy.

`GALLIUM_DRIVER` is cleared at the same boundary because it is another direct Gallium device/driver selection input. The current session does not export it, but an inherited shell/session value would create the same semantic leak.

## Deliberate scope boundary

This correction does not attempt to sanitize every Mesa-related environment variable.

It changes only the proven provider/bridge selection set:

```text
VK_ICD_FILENAMES
VK_DRIVER_FILES
MESA_LOADER_DRIVER_OVERRIDE
GALLIUM_DRIVER
```

For example, `vblank_mode=0` is not changed in this transaction. It is a separate presentation/scheduling policy and requires its own evidence before ownership or scope is changed.

This preserves the project rule:

```text
minimum manipulation
    +
maximum semantically justified effect
```

## Corrected baseline

`modules/gl/overlay/home/gl/env` now performs:

```text
unset VK_ICD_FILENAMES VK_DRIVER_FILES
unset MESA_LOADER_DRIVER_OVERRIDE GALLIUM_DRIVER
```

New contract:

```text
glibc baseline
    -> no inherited bionic Vulkan provider
    -> no inherited bionic OpenGL bridge
    -> no inherited Gallium driver selection
```

Consumers then compose explicitly:

```text
gl-run
    -> explicit Freedreno profile
    -> MESA_LOADER_DRIVER_OVERRIDE=zink

VS Code / Obsidian GPU
    -> explicit Freedreno profile
    -> ANGLE Vulkan argv
    -> no Zink/Gallium override

VS Code / Obsidian CPU
    -> no explicit Vulkan provider
    -> no Zink/Gallium override
    -> --disable-gpu

Obsidian CLI
    -> no explicit graphics provider or bridge
```

## Source and validation changes

Baseline correction:

```text
2fad1ec05b4735c2041dae1971fdecc273102590
```

Repository policy-scope smoke expansion:

```text
aae63cabacbf7e183335d0e15991e8c943be37e8
```

The smoke now injects bionic-style values for all four policy variables and verifies:

```text
CPU/CLI baseline:
    all four absent

ANGLE GPU branches:
    explicit VK pair present
    Zink/Gallium variables absent

gl-run:
    explicit VK pair present
    MESA_LOADER_DRIVER_OVERRIDE=zink
    GALLIUM_DRIVER absent
```

Live installation receipt expansion:

```text
dc1907ed4745906b4b2661f1214b5d445b604422
```

Pre-deploy gate expansion:

```text
6a30e700f09866bc38245c270807da50b23e9c7f
```

The pre-deploy gate now checks:

```text
baseline clears Vulkan pair
baseline clears Zink/Gallium pair
baseline does not export any of the four
profile exports only the Vulkan pair
gl-run adds Zink explicitly
all current validator scripts pass bash syntax
```

Desktop session contract comment correction:

```text
14decde7e43ea46dffa6eb18dd3d9b2163174d68
```

## Documentation synchronization

Updated:

```text
modules/gl/README.md
docs/architecture.md
docs/desktop-session.md
docs/gpu.md
docs/glibc-layer.md
packages/vscode/README.md
packages/obsidian/README.md
```

These documents now distinguish:

```text
bionic provider/bridge policy
boundary sanitation
explicit glibc provider profile
consumer-owned Zink bridge
application feature mode
```

## Activation behavior

The live path:

```text
$HOME/gl/env
```

is already a symlink into the mutable checkout.

Therefore pulling the correction changes the live baseline immediately.

No new runtime leaf is introduced, so `tools/deploy` is not required for this correction.

No desktop-session restart is required. Existing processes keep their original environment; newly launched glibc processes use the corrected baseline.

This again demonstrates that checkout update is an activation event in the current source-linked deployment model.

## Effect on previous receipts

The earlier promoted receipts remain valid facts about their exact captured heads:

```text
promoted gl-run renderer:
    PASS at f536bb89d47db76b62a9db620e07c4c658313d65

promoted VS Code GPU identity:
    PASS at 3b8b397664507a6df62e99cfbc00916027717c8a
```

They are not deleted or relabeled as failures.

However the shared baseline changed after those captures. Final promotion must be based on one coherent current source state.

Therefore the following gates reopen:

```text
pre-deploy/source regression
live installation environment
promoted gl-run renderer
promoted VS Code GPU identity
promoted VS Code CPU policy
```

## Required current-HEAD sequence

```text
1. sync exact branch/HEAD
2. run expanded no-mutation pre-deploy gate
3. run expanded live installation receipt
4. rerun promoted gl-run renderer
5. rerun promoted VS Code GPU identity
6. run promoted VS Code CPU policy gate
7. only then proceed to Obsidian GPU/CPU
```

Do not run `tools/deploy` between steps 2 and 3 unless the live symlink inventory unexpectedly differs. The existing links already point at the corrected checkout files.

## Expected expanded installation receipt

Baseline input deliberately includes:

```text
VK_DRIVER_FILES=/bionic/freedreno.json
VK_ICD_FILENAMES=/bionic/freedreno.json
MESA_LOADER_DRIVER_OVERRIDE=zink
GALLIUM_DRIVER=llvmpipe
```

Expected after `source ~/gl/env`:

```text
VK_DRIVER_FILES=<unset>
VK_ICD_FILENAMES=<unset>
MESA_LOADER_DRIVER_OVERRIDE=<unset>
GALLIUM_DRIVER=<unset>
```

Expected after the explicit Freedreno profile:

```text
VK_DRIVER_FILES=<exact managed glibc ICD>
VK_ICD_FILENAMES=<same exact managed glibc ICD>
MESA_LOADER_DRIVER_OVERRIDE=<unset>
GALLIUM_DRIVER=<unset>
profile_internal=<unset>
```

## Current gate state

```text
historical promoted gl-run receipt:
    PASS AT PRIOR HEAD

historical promoted VS Code GPU receipt:
    PASS AT PRIOR HEAD

current baseline sanitation source:
    CORRECTED

current regression gates:
    NOT YET RUN

promoted VS Code CPU gate:
    READY AFTER GPU REGRESSION PASS

Obsidian promoted gates:
    BLOCKED
```

## Stop line

Do not:

```text
run the CPU gate before current-HEAD predeploy/install/GPU regression
restart XFCE merely for this environment-source change
run tools/deploy by habit when no new leaf is required
remove or rewrite prior-head evidence
expand sanitation to unrelated Mesa variables without evidence
mark the scoped policy transaction complete
```

First run the expanded current-HEAD regression sequence.
