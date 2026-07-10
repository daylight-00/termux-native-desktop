# 0042 — Vulkan Policy Producer and Consumer Inventory

## Status

The fallback-provider closure attribution is complete for the captured strict Obsidian control.

The next architecture question is no longer whether global Vulkan policy matters. The strict A/B already demonstrated that changing provider-selection environment changes the mapped provider/device composition while preserving bounded application topology and survival.

The current question is:

```text
who produces Vulkan provider-selection policy today,
who consumes it,
and what is the smallest valid future scope?
```

## Current producers

### Bionic desktop-session producer

Owner path:

```text
modules/desktop/overlay/home/.local/bin/startxfce-x11
```

Current role:

```text
bionic session graphics policy
```

It exports:

```text
VK_ICD_FILENAMES=$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json
VK_DRIVER_FILES=$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json
MESA_LOADER_DRIVER_OVERRIDE=zink
```

for bionic desktop clients.

The script explicitly documents that this policy belongs to the bionic side of the desktop session.

It also explicitly removes Vulkan and Mesa overrides from the Termux:X11 server process:

```text
termux-x11 receives:
    no MESA_LOADER_DRIVER_OVERRIDE
    no GALLIUM_DRIVER
    no VK_ICD_FILENAMES
    no VK_DRIVER_FILES
    no LIBGL_ALWAYS_SOFTWARE
```

This is already an example of narrow negative composition: the session has graphics policy, but the display server opts out.

### Glibc shared-environment producer

Owner path:

```text
modules/gl/overlay/home/gl/env
```

Current role:

```text
shared environment for glibc-world applications
```

It unconditionally re-pins Vulkan provider selection when the glibc Freedreno ICD JSON is readable:

```text
VK_ICD_FILENAMES=$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json
VK_DRIVER_FILES=$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json
```

The stated reason is shielding glibc processes from inheriting the bionic ICD exported by the desktop session.

That shielding requirement is real, but the current implementation couples two different responsibilities:

```text
remove/override incompatible inherited bionic policy

and

select a specific glibc Vulkan provider globally
```

The Obsidian A/B shows that those responsibilities must be separated.

## Current consumers

### gl-run

Owner path:

```text
modules/gl/overlay/home/gl/bin/gl-run
```

Behavior:

```text
source gl/env
require VK_DRIVER_FILES to be non-empty
set MESA_LOADER_DRIVER_OVERRIDE=zink
execute target
```

Interpretation:

```text
gl-run is a direct consumer of explicit glibc Vulkan provider policy
```

because Zink needs a Vulkan provider underneath it.

The architecture stop line still applies:

```text
do not extend gl-run into lifecycle, synchronization, provider discovery, or promotion authority
```

Its valid role is narrow launch composition.

### VS Code launcher

Owner path:

```text
packages/vscode/launcher/code
```

Behavior:

```text
source gl/env

if GL_GPU=1 and VK_DRIVER_FILES is non-empty:
    enable ANGLE/Vulkan flags
else:
    pass --disable-gpu
```

However, in the CPU branch the launcher does not remove:

```text
VK_DRIVER_FILES
VK_ICD_FILENAMES
```

Therefore the current control meaning is:

```text
CPU Chromium argv
    !=
no Vulkan provider-selection environment
```

This is the same ownership defect exposed directly by the Obsidian A/B.

### Obsidian launcher

Owner path:

```text
packages/obsidian/launcher/obsidian-app
```

Behavior is structurally the same as VS Code:

```text
source gl/env

if GL_GPU=1 and VK_DRIVER_FILES is non-empty:
    enable ANGLE/Vulkan flags
else:
    pass --disable-gpu
```

Again, `GL_GPU=0` changes argv but does not remove inherited glibc Vulkan provider-selection policy.

The strict A/B demonstrated the consequence for this concrete workload.

## Non-consumer distinction

Experiment reports and architecture documentation may mention `VK_*`, but they are not runtime consumers.

The runtime inventory should distinguish:

```text
policy producer
policy consumer
policy observer/test
documentation only
```

The current real runtime path identified from the refactor branch is:

```text
bionic session producer:
    startxfce-x11

glibc shared producer:
    gl/env

direct glibc launch consumers:
    gl-run
    VS Code launcher
    Obsidian launcher
```

## Required ownership split

The current shared glibc environment combines:

```text
world baseline
bridge policy
data-provider policy
locale policy
TLS policy
Electron policy
Vulkan provider selection
```

The semantic inventory already concluded that Vulkan variables belong to:

```text
provider.graphics.vulkan.glibc
```

The Obsidian A/B and fallback closure attribution now provide workload evidence for that conclusion.

The future contract must separate at least:

```text
1. inherited-policy sanitation
2. explicit hardware provider selection
3. explicit software provider selection
4. implicit discovery policy
5. no Vulkan participation intent
```

These are different states and must not be collapsed into one global environment side effect.

## Minimal target contract

This document defines behavior, not final filenames or directory layout.

### Baseline glibc application composition

Must guarantee:

```text
no incompatible bionic Vulkan provider path is inherited accidentally
```

but must not automatically mean:

```text
select Freedreno globally
```

### Explicit hardware Vulkan composition

Must be able to compose:

```text
Freedreno/Turnip provider identity
ICD manifest path
VK_DRIVER_FILES
VK_ICD_FILENAMES compatibility behavior if required
validation gate
actual-selection evidence
```

### Explicit software Vulkan composition

Must allow a software-provider policy to be selected deliberately rather than discovered accidentally.

Possible concrete providers are workload/environment specific and require their own validation.

### Implicit discovery composition

If retained at all, it must be an explicit policy choice.

The strict Obsidian run demonstrated that removing explicit override can discover and map:

```text
SwiftShader
Lavapipe
Gfxstream
```

Therefore `unset VK_*` is not equivalent to `no Vulkan`.

### No-Vulkan composition

If a workload truly requires evidence of no Vulkan provider participation, that is a stronger experiment and may require more than unsetting override variables.

The architecture must not claim this state until loader/discovery and runtime mapping evidence proves it.

## Migration constraints

Do not perform a blind edit such as:

```text
remove VK_* from gl/env
```

without replacing current consumers deliberately.

Required migration order:

```text
1. define narrow launch-composition primitive/contract
2. migrate gl-run to explicit hardware Vulkan composition
3. migrate VS Code GPU branch to explicit composition
4. migrate Obsidian GPU branch to explicit composition
5. make CPU branches sanitize inherited provider policy deliberately
6. validate GPU and CPU workloads separately
7. only then remove unconditional provider selection from gl/env
```

The exact physical implementation remains open.

## Non-goals

Do not use this work to introduce:

```text
gl-sync
provider auto-update
global lifecycle authority
a new monolithic graphics manager
one global compatibility fingerprint
implicit application scanning
```

The goal is smaller:

```text
move provider-selection policy to the smallest valid launch-composition scope
```

## Next gate

Before implementation:

```text
1. design a bounded experiment-local composition primitive
2. validate it with gl-run, VS Code, and Obsidian without changing gl/env
3. verify actual provider selection in GPU paths
4. verify CPU-path behavior after explicit sanitation
5. then decide the final semantic owner and physical layout
```

The Obsidian selected-closure candidate remains blocked until locality-shadowing and non-graphics static/runtime closure analysis are also complete.
