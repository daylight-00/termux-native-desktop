# 0111 — Selected Obsidian Passive B10 Survival Pass and Map-Selection Failure

## Status

The passive no-input Phase B10 run passed startup topology, 100-second survival, and maps capture. The stage failed only in the exact mapped-identity analyzer.

```text
operator interaction:
    NONE

analysis.status:
    FAIL

failure stage:
    mapped_identity

topology.status:
    PASS

survival.status:
    PASS

maps-capture.status:
    PASS

current pointer changed:
    NO
```

The passive initial-window runtime claim is therefore closed for startup and 100-second survival, but the generation-selection/map contract is not closed.

## Authoritative receipt

Archive:

```text
selected-obsidian-phase-b10-passive-short-runtime-cpu-validation-20260712-015859.tgz
```

Archive SHA-256:

```text
86330e210a0171fd1bf059eec600cc92eac963b0e468538be77b8819214905af
```

Captured repository state:

```text
branch:
    docs/post-graphics-architecture-audit

head:
    3b7cc1f4f33852f273bda77d681d035a5c3be668
```

Archive structure:

```text
members:
    153

regular files:
    112

directories:
    41

absolute member paths:
    0

parent traversal:
    0

symlink/hardlink/device/special members:
    0
```

## Operator contract

```text
mode:
    PASSIVE_NO_GUI_INPUT

operator action:
    OBSERVE_ONLY

forbidden action:
    DO_NOT_CLICK_OPEN_VAULT_OR_ANY_GUI_CONTROL
```

The operator confirmed that no GUI control was touched.

## Runtime and process result

```text
runtime-root length:
    48

TMPDIR length:
    52

runtime snapshot:
    MATCH

capture exit status:
    0
```

Final stable topology:

```text
main:
    1

zygote:
    3

utility:
    1

renderer:
    1

GPU process:
    0
```

Process-contract checks:

```text
main count:
    PASS

renderer count:
    PASS

zygote count:
    PASS

GPU count:
    PASS

main exact --disable-gpu:
    PASS

renderer --disable-gpu-compositing:
    PASS
```

The survival poll recorded forty-one complete survival samples before final capture.

## Current boundary

```text
current before:
    ABSENT

current after:
    ABSENT

changed:
    NO
```

No promoted launcher or immutable generation mutation occurred.

## Map-capture result

```text
unique mapped regular objects:
    143

capture path classes:
    APP_LOCAL          12
    PREFIX_GLIBC       21
    OTHER_ABSOLUTE    110
```

Expected immutable identity model:

```text
selected objects:
    96

app-local references:
    11

protected-world references:
    18

combined expected identities:
    125
```

Observed overlap:

```text
selected object-store identities mapped:
    93 / 96

app-local expected identities mapped:
    11 / 11

protected-world expected identities mapped:
    18 / 18
```

Selected mapping by content kind:

```text
selected ELF:
    89 / 91

selected fonts:
    3 / 4

generated GSettings aggregate:
    1 / 1
```

## Missing selected paths

```text
libXdmcp.so.6.0.0 object
    0245743bb594ee1ac2c1325873d70407c790f890477d8a0fe8323bda8803f705

DejaVuSansMono-Bold.ttf object
    0d3c03d1b667192f91223660a3163325cf83132662fe4d9f7d6e596bf7a995c2

libXau.so.6.0.0 object
    1a8bc733979360f2e3327d805efe64f9306247bacb90cac9efdc0cf1e033bb89
```

The missing font is not evidence of loader-selection failure. Passive initial-window rendering did not demand that exact Bold font identity. Requiring every immutable data object to appear in `/proc/<pid>/maps` is therefore too strict.

## Selected-ELF bypass

The selected object-store copies of `libXau.so.6` and `libXdmcp.so.6` were absent, while their protected prefix source paths were mapped in every captured process:

```text
$PREFIX/glibc/lib/libXau.so.6.0.0
$PREFIX/glibc/lib/libXdmcp.so.6.0.0
```

Historical retained ELF metadata identifies four selected consumers with an absolute DT_RPATH:

```text
libxcb-render.so.0.0.0
libXrandr.so.2.2.0
libXrender.so.1.3.0
libxcb-shm.so.0.0.0

DT_RPATH:
    $PREFIX/glibc/lib
```

Three of those consumers have direct retained edges to both `libXau.so.6` and `libXdmcp.so.6`.

Because DT_RPATH can precede `LD_LIBRARY_PATH`, copied selected consumers can still select nested dependencies from the world prefix. This is the leading explanation for the two selected-object bypasses. It must be revalidated on-device with live hashes and retained edge inputs before changing the generation contract.

## Additional CPU-map findings

The passive maps contain one path previously classified as an excluded graphics feature:

```text
$PREFIX/glibc/lib/libX11-xcb.so.1.0.0
```

They also contain one app-local ELF absent from the B9 semantic manifest:

```text
$HOME/gl/apps/obsidian/libvk_swiftshader.so
```

The SwiftShader object is mapped by one zygote even though:

```text
main has exact --disable-gpu;
renderer has --disable-gpu-compositing;
GPU process count is zero.
```

This proves that process-class CPU policy and mapped graphics-object policy are distinct claims. The previous expectation of zero excluded/unmodelled graphics mappings is not satisfied.

## Clean negative boundaries

```text
broad-farm mappings:
    0

rootfs mappings:
    0

current-path mappings:
    0
```

Receipt-local mutable mappings account for seventeen additional regular files.

## Teardown stderr

After the completed PASS capture gates, stderr contains:

```text
GPU process isn't usable. Goodbye.
```

Its timestamp is after startup and the 100-second survival interval. The receipt does not establish it as an in-gate passive-runtime failure; topology, survival, and maps were already marked PASS. It must not override those gate results.

## Architecture correction

The prior analyzer combined three different requirements:

```text
all candidate content exists and is hash-correct;
all runtime-required ELF resolves through the selected ownership contract;
all selected data is necessarily mapped in one workload state.
```

Only the first two are valid invariant candidates. Demand-loaded fonts and data cannot be required to map in every passive state.

The corrected map model must distinguish:

```text
REQUIRED_SELECTED_ELF
DEMAND_LOADED_SELECTED_DATA
PROTECTED_WORLD_REFERENCE
APP_LOCAL_REFERENCE
RECEIPT_MUTABLE_STATE
CPU_ALLOWED_APP_GRAPHICS_MAPPING
CPU_FORBIDDEN_PROVIDER_MAPPING
UNMODELLED_MAPPING
```

## Direction decision

```text
passive initial-window startup:
    PASS

passive 100-second survival:
    PASS

maps capture:
    PASS

exact generation selection:
    FAIL / two selected ELF bypassed

all-selected-data-must-map rule:
    INVALID

CPU graphics map contract:
    OPEN

interactive vault-open capability:
    OPEN / known GTK pixbuf failure

activation readiness:
    NO
```

## Next action

Run a read-only map-selection diagnostic that consumes the B1, B2, B9, and passive B10 receipts. It must:

```text
rehash selected objects and mapped world substitutes;
reconstruct selected-versus-source substitution;
record DT_RPATH/DT_RUNPATH for selected consumers;
join retained dependency edges to the two bypassed providers;
record libX11-xcb and libvk_swiftshader identities;
separate demand-loaded data from required ELF;
perform no launch and no generation mutation.
```

## Stop line

Do not:

```text
claim overall B10 PASS;
activate current;
mutate the existing generation;
patch RPATH before the read-only diagnostic;
reclassify all missing data as runtime failure;
ignore libX11-xcb or libvk_swiftshader mappings;
proceed directly to atomic activation.
```
