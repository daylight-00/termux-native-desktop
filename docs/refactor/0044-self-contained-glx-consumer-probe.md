# 0044 — Self-Contained GLX Consumer Probe

## Status

The first scoped Vulkan policy composition check passed the environment identity gate for both modes:

```text
explicit-freedreno
    VK_DRIVER_FILES=<glibc Freedreno ICD>
    VK_ICD_FILENAMES=<glibc Freedreno ICD>

implicit-discovery
    VK_DRIVER_FILES unset
    VK_ICD_FILENAMES unset
```

The next command attempted:

```text
run-zink-with-policy.sh glxinfo -B
```

but failed before any OpenGL workload ran:

```text
env: ‘glxinfo’: No such file or directory
```

Classification:

```text
policy composition: PASS
consumer command lookup: FAIL
Zink/OpenGL runtime: NOT TESTED
```

This is not evidence against the Vulkan policy composition primitive.

## Decision

Do not install `mesa-utils` merely to continue this architecture experiment.

Instead, keep a minimal OpenGL consumer inside the experiment itself.

Added files:

```text
experiments/glibc/vulkan-policy-composition/recipe/glx-renderer-probe.c
experiments/glibc/vulkan-policy-composition/recipe/build-glx-renderer-probe.sh
```

## Why a self-contained probe is preferable here

The experiment question is:

```text
can explicit Vulkan provider policy be composed narrowly and consumed by Zink/OpenGL?
```

It is not:

```text
is a particular diagnostic package installed?
```

Adding an external diagnostic package would introduce a new supply transaction and package state solely for observation.

The project already has:

```text
existing glibc GCC wrapper
existing X11 runtime provider
existing OpenGL/GLX runtime provider
existing Zink/Turnip runtime
```

A small controlled consumer is therefore the smaller manipulation.

## Probe design

The probe does not require X11 or OpenGL development headers.

It links only against the existing glibc-side C/dynamic-loader environment and resolves the actual runtime providers with:

```text
dlopen("libX11.so.6")
dlopen("libGL.so.1")
```

It then resolves the minimum Xlib/GLX/OpenGL entry points with `dlsym`.

Runtime sequence:

```text
XOpenDisplay
    ↓
glXQueryVersion
    ↓
glXChooseFBConfig
    ↓
glXCreateNewContext
    ↓
glXCreatePbuffer
    ↓
glXMakeContextCurrent
    ↓
glGetString(GL_VENDOR)
glGetString(GL_RENDERER)
glGetString(GL_VERSION)
```

The use of a GLX pbuffer keeps the consumer bounded and removes window/event-loop behavior from the test.

## Build ownership

The build recipe uses:

```text
$HOME/gl/toolchain/glibc-gcc
```

The wrapper already executes the Termux-glibc GCC under the glibc loader with scoped library-path injection.

The probe output is generated under:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
```

It is evidence/runtime scratch output, not a promoted package payload.

## Validation contract

The explicit-Freedreno Zink validation is successful only if the probe:

```text
builds as a glibc executable
opens the X display
creates a GLX context
makes the context current
prints non-null GL identity fields
reports the expected Zink/Turnip renderer identity
```

The provider-policy wrapper must still print:

```text
VULKAN_POLICY_MODE=explicit-freedreno
VK_DRIVER_FILES=<glibc Freedreno ICD>
```

before the workload result.

## Claim boundary

A successful renderer string proves the OpenGL consumer reached a functioning context and identifies the reported renderer.

It does not by itself prove:

```text
complete frame-presentation behavior
long-duration stability
all Vulkan loader manifest accesses
all device-node interactions
zero-copy presentation
```

Those require separate evidence when relevant.

## Next gate

```text
1. build the probe
2. inspect interpreter and NEEDED set
3. run it under explicit-freedreno + Zink composition
4. record renderer identity
5. only then proceed to the Electron consumer adapters
```
