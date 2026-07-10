# 0045 — Explicit Freedreno Zink Consumer Validation Passed

## Status

The first cross-consumer validation of the scoped Vulkan policy composition experiment passed.

Test path:

```text
VULKAN_POLICY_MODE=explicit-freedreno
    ↓
policy-env.sh
    ↓
VK_DRIVER_FILES=<glibc Freedreno ICD>
VK_ICD_FILENAMES=<glibc Freedreno ICD>
    ↓
run-zink-with-policy.sh
    ↓
MESA_LOADER_DRIVER_OVERRIDE=zink
    ↓
self-contained GLX renderer probe
```

## Probe build result

The probe built successfully through the existing glibc GCC wrapper.

Observed interpreter:

```text
$PREFIX/glibc/lib/ld-linux-aarch64.so.1
```

Observed dynamic NEEDED set:

```text
libc.so.6
ld-linux-aarch64.so.1
```

This confirms that the probe itself does not carry direct link-time dependencies on X11, GLX, or OpenGL provider libraries.

Those runtime providers are opened dynamically by the probe.

## Runtime result

Observed policy identity:

```text
experiment Vulkan policy: explicit-freedreno
VK_DRIVER_FILES=$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json
```

Observed GLX/OpenGL identity:

```text
GLX_VERSION=1.4
GL_VENDOR=Mesa
GL_RENDERER=zink Vulkan 1.4(Turnip Adreno (TM) 730 (MESA_TURNIP))
GL_VERSION=4.6 (Compatibility Profile) Mesa 25.0.7-2
```

Result:

```text
GLX context creation: PASS
OpenGL identity query: PASS
Zink renderer identity: PASS
Turnip Adreno 730 provider identity: PASS
explicit launch-scoped provider policy: PASS
```

## Architecture conclusion

The experiment establishes the first concrete consumer proof for the scoped Vulkan policy contract.

A launch-scoped composition can provide:

```text
explicit glibc Freedreno ICD selection
    +
Zink OpenGL composition
```

and preserve the core behavior currently consumed by `gl-run`.

The current evidence therefore supports:

```text
Vulkan provider-selection policy
    need not be an unconditional world baseline side effect
```

for this bounded Zink/OpenGL consumer path.

This does not yet justify changing promoted `gl/env` or `gl-run`.

## Relation to gl-run

The promoted `gl-run` currently:

```text
sources gl/env
requires VK_DRIVER_FILES
sets MESA_LOADER_DRIVER_OVERRIDE=zink
executes the target
```

The experiment validates that the provider-selection responsibility can be supplied immediately before the Zink launch composition instead of being assumed from unconditional shared environment state.

The valid future direction is therefore:

```text
narrow provider policy composition
    +
narrow Zink/OpenGL composition
```

not:

```text
gl-run becomes provider lifecycle authority
```

The existing architecture stop line remains unchanged.

## Claim boundary

The successful renderer identity proves:

```text
a GLX context was created
an OpenGL context became current
Mesa reported Zink as the renderer
Zink reported Turnip Adreno 730 provider identity
```

It does not by itself prove:

```text
long-duration stability
frame presentation behavior
all Vulkan loader manifest accesses
all mapped provider objects
device-node mapping details
```

Those are separate validation layers when needed.

## Next gate

Use the same binary and same Zink wrapper with:

```text
VULKAN_POLICY_MODE=implicit-discovery
```

The purpose is not to prove `no Vulkan`.

The purpose is to observe whether the OpenGL consumer:

```text
succeeds with an alternate renderer
fails because discovered providers are unsuitable for Zink
selects a software Vulkan provider
selects another provider path
```

Only after that A/B should the experiment proceed to the Electron adapters.
