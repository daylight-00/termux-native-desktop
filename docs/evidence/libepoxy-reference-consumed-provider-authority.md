# Bounded libepoxy provider authority for GTK 3.24.49 X11 GLX

## Decision

```text
root: gpkg/libepoxy
decision: ACCEPTED_BOUNDED_PROVIDER
accepted capability: GTK 3.24.49 X11 GLX dispatch
X11: required and bound
GLX: required and bound
EGL: not claimed by this decision
composition: not accepted
target population: not accepted
activation: not accepted
```

The exact Termux glibc `libepoxy.so.0` member is accepted only as the dispatch provider for the selected GTK 3.24.49 X11 GLX path. This is a Class B project-integration decision over a Class A reference-consumed recipe.

Canonical machine-readable record:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    libepoxy-reference-consumed-provider-authority.tsv
```

## Exact provider identity

```text
root review:  generic-root-review:2f6c3972ae083cff8dd2
recipe tree: bb827daab0491d4ff49c822f96dd4bbb80102ef0
package:      libepoxy-glibc 1.5.10
artifact id:  generic-artifact:e53dc3b7f5419f13eb09
artifact SHA: e53dc3b7f5419f13eb0948d2e16994061d2d593c1db2c535022c0d504af6a0e8
member:       data/data/com.termux/files/usr/glibc/lib/libepoxy.so.0.0.0
member SHA:   403f566468fb5212173407d041a660af0ff459841e9b0ca2274e9c28ac98c723
SONAME:       libepoxy.so.0
```

The exact concrete filename already matches the observed SONAME family. No alias or successor policy is introduced by this decision.

## Recipe and supplier boundary

The pinned package recipe contains one `build.sh` and adds no patch, hook, Meson option, install transformation, or output rewrite. Its package-specific adaptation is already confirmed Class A.

libepoxy 1.5.10 defaults are environment-sensitive:

```text
x11 = true
glx = auto
egl = auto
```

Upstream generates and installs `epoxy/glx.h` and GLX dispatch sources only when `build_glx` is true. EGL headers and dispatch are likewise conditional on `build_egl`.

The supplier pipeline copied a build framework from a floating `termux/termux-packages` `master`. The exact producing Meson host declaration is therefore not reconstructed from the pinned recipe repository. This is retained as a supplier boundary rather than converted into a blanket Class C requirement.

## GTK consumer binding

GTK 3.24.49 requires libepoxy 1.4 or newer. Its X11 GL implementation:

```text
includes <epoxy/glx.h>;
calls epoxy_has_glx();
calls epoxy_glx_version();
calls epoxy_has_glx_extension();
uses GLX dispatch for context creation, extension selection, buffer exchange and synchronization.
```

The selected closure contains the exact `libepoxy.so.0` candidate. Because the GTK 3.24.49 X11 GL source requires the generated GLX header and dispatch surface, the bounded consumer contract establishes `GLX_REQUIRED_AND_BOUND` and `X11_REQUIRED_AND_BOUND` for this provider decision.

## EGL boundary

GTK 3.24.49's selected X11 GL path is the GLX implementation reviewed above. Existing evidence does not need EGL to establish that bounded capability. Therefore:

```text
EGL_NOT_CLAIMED_BY_THIS_PROVIDER_DECISION
```

This is not a finding that EGL is absent. It means this review neither requires nor authorizes EGL capability. Any later EGL, Wayland, GLES, or non-GTK consumer scope must perform its own feature and consumer-binding review.

## Conflicts and exclusions

```text
one exact dynamic Termux glibc candidate
Debian rootfs bytes remain oracle evidence, not target provider authority
no concrete-filename or SONAME drift
EGL capability excluded from accepted scope
complete GL/graphics provider composition excluded
```

No static or development alias is added to the runtime provider decision.

## Update and rollback boundary

Re-review this row when any of the following changes:

```text
artifact version or SHA-256
exact member SHA-256 or SONAME
recipe tree
GTK source tag or X11 GL consumer binding
libepoxy GLX feature contract
selected consumer changes to EGL, Wayland, GLES, or another application
multiple non-equivalent dynamic candidates appear
```

Before materialization, rollback is revocation of this provider row. Any future materialization must use a new immutable generation; runtime rollback is reversal to the previous selected generation.

## Authority effect

This decision accepts only:

```text
exact libepoxy member
observed SONAME libepoxy.so.0
selected GTK 3.24.49 X11 GLX dispatch capability
```

It does not accept:

```text
EGL or Wayland capability
complete GL or graphics composition
provider target path or alias policy
target population
materialization
activation
producing-build equivalence
```

The next bounded no-token tranche is Pango provider authority together with its concrete-filename drift and continuity policy.
