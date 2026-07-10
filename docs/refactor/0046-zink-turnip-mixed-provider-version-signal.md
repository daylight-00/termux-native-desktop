# 0046 — Zink/Turnip Mixed-Provider Version Signal

## Status

The explicit-Freedreno GLX probe passed and reported:

```text
GLX_VERSION=1.4
GL_VENDOR=Mesa
GL_RENDERER=zink Vulkan 1.4(Turnip Adreno (TM) 730 (MESA_TURNIP))
GL_VERSION=4.6 (Compatibility Profile) Mesa 25.0.7-2
```

At the same time, the explicit Vulkan policy selected:

```text
$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json
```

which belongs to the current Mesa provider-store lineage rather than the Debian/rootfs Mesa 25.0.7 package line.

## Interpretation boundary

The renderer string proves a working Zink -> Vulkan -> Turnip path.

The OpenGL version string reports:

```text
Mesa 25.0.7-2
```

while the explicit ICD policy points at the separately managed glibc Mesa provider store.

This is a strong signal that the OpenGL/Zink frontend and Vulkan driver provider may come from different physical provider/version domains.

Do not promote that inference to a physical-path claim from version strings alone.

The next evidence must inspect the actual mapped object paths of the running probe.

## Probe hold support

The self-contained GLX probe now accepts:

```text
PROBE_HOLD_SECONDS=<0..600>
```

After it creates and makes the GLX context current and prints renderer identity, it can remain alive for a bounded interval.

This allows read-only capture of:

```text
/proc/<pid>/maps
```

while the GLX/Zink/Vulkan composition is active.

## Maps capture helper

Added:

```text
experiments/glibc/vulkan-policy-composition/recipe/capture-glx-probe-maps.sh
```

The helper:

```text
launches the probe under one VULKAN_POLICY_MODE
waits until GL_RENDERER is emitted
captures /proc/<pid>/maps
normalizes mapped absolute paths through realpath
prints graphics-related mapped paths
waits for normal probe completion
```

Evidence output includes:

```text
probe.stdout
probe.stderr
maps.txt
mapped-paths.raw.txt
mapped-paths.real.txt
graphics-related-paths.txt
pid
```

## Question

The immediate question is:

```text
which physical objects provide:
    libGL / GLX dispatch
    Zink frontend
    Vulkan loader/layer
    Turnip driver
    DRM/device support
```

for the passed explicit-Freedreno probe?

The answer matters because the broader architecture already shows that one semantic capability can cross physical supply roots.

If the probe maps, for example, a rootfs Mesa/Zink frontend and a provider-store Turnip driver, that would be concrete evidence that:

```text
provider.graphics.opengl.glibc
    and
provider.graphics.vulkan.glibc
```

can compose across independently supplied Mesa component lineages.

That would not automatically prove arbitrary cross-version compatibility; it would prove only the tested composition.

## Next order

```text
1. rebuild the probe with hold support
2. capture explicit-freedreno probe maps
3. classify physical provider paths
4. only then run the implicit-discovery GLX A/B
5. compare renderer identity and provider maps
```

Electron adapter validation remains after the GLX consumer composition is fully characterized.
