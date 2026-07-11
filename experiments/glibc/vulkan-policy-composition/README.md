# Vulkan Policy Composition Experiment

## Status

```text
SCOPED_TRANSACTION_CLOSED
```

The architecture-discrimination experiment is complete for the accepted scoped graphics-policy contract.

Canonical closure:

```text
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

Post-closure architecture interpretation:

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
```

Do not treat the closed experiment as a reason to preserve every current helper/path as permanent architecture.

## Primary question

Can graphics policy move from unconditional shared glibc-world state into narrow consumer composition while preserving real workloads?

## Answer

Yes, for the tested target and consumers.

The accepted semantic decomposition is:

```text
bionic session policy
    -> bionic Vulkan provider
    -> bionic Zink session bridge

glibc world boundary
    -> remove inherited bionic Vulkan provider policy
    -> remove inherited bionic Zink/Gallium policy
    -> choose no graphics provider or bridge

explicit glibc hardware provider
    -> consumer-scoped Freedreno/Turnip profile

OpenGL consumer composition
    -> explicit provider
    -> Zink bridge

Electron GPU application branch
    -> application feature mode
    -> explicit provider
    -> ANGLE Vulkan argv
    -> no Zink/Gallium override

Electron CPU application branch
    -> application CPU mode
    -> provider-neutral baseline
    -> exact --disable-gpu
```

## Independent dimensions established

```text
application feature mode
provider discovery/selection policy
device-class intent
consumer-specific suitability
mapped provider participation
actual selected-provider/device evidence
application-state authority
```

These dimensions must not be collapsed into one global `GPU=0/1` or one environment variable.

## Final evidence matrix

```text
expanded source/pre-deploy transaction:
    PASS

expanded live installation:
    PASS

current OpenGL/Zink renderer:
    PASS
    zink -> Turnip -> Adreno 730

VS Code GPU:
    PASS
    primary Turnip / Adreno 730

VS Code CPU:
    PASS
    provider-neutral effective CPU mode

Obsidian GPU:
    PASS
    isolated application state
    primary Turnip / Adreno 730

Obsidian CPU:
    PASS
    isolated application state
    provider-neutral effective CPU mode
```

Detailed evidence roots, commit identities, gate counts, and claim boundaries are in `docs/refactor/0083` through `0091`.

## Consumer results

### Standalone Zink/GLX

```text
explicit Freedreno + default intent
    -> Turnip / KGSL
    -> PASS

implicit discovery + default intent
    -> llvmpipe CPU device discovered
    -> Zink rejects default CPU path
    -> FAIL before renderer identity

implicit discovery + software intent
    -> llvmpipe selected
    -> Zink / GLX / OpenGL 4.6
    -> PASS
```

Therefore:

```text
provider selection
    !=
device-class intent
```

### Electron/ANGLE Vulkan

Same-feature-mode comparisons established that explicit Freedreno and implicit discovery can preserve Electron topology/survival while changing the provider tail.

Primary selected-device probes later established:

```text
explicit profile
    -> FREEDRENO_TURNIP
    -> Adreno 730

implicit discovery control
    -> LVP / llvmpipe primary device
```

Therefore map presence alone is not selected-device proof.

## Accepted evidence model

GPU acceptance correlates:

```text
observable environment and argv
CDP primary selected-device identity
ANGLE/Vulkan feature state
managed provider mapping
KGSL device-node mapping
```

CPU acceptance requires:

```text
provider-neutral environment
exact --disable-gpu
no GPU-enablement flags
effective disabled/compositing mode
viable renderer/main topology
bounded survival
```

A process named `gpu-process` may or may not exist in CPU mode.

## Application-state authority

Promotion evidence must not depend on normal user state.

```text
VS Code
    receipt-local user-data and extensions

Obsidian
    receipt-local XDG_CONFIG_HOME
    actual receipt-local <config>/obsidian directory
```

The first Obsidian CDP attempt is preserved as a false-negative model because it observed the wrong application-owned path.

## Current realization versus durable contract

Current implementation:

```text
~/gl/env
~/gl/policy/vulkan/freedreno.sh
gl-run
GL_GPU application branches
```

Durable contract:

```text
world-boundary sanitation
consumer-scoped provider selection
consumer-owned bridge selection
application-owned feature mode
isolated state authority
selected-device evidence
```

Current path and command names remain replaceable.

## Revalidation policy

Do not blind-rerun this experiment.

Run only the affected canonical gate when its claim surface changes.

### Source/live transaction trigger

```text
gl world-boundary sanitation changes
provider profile changes
current OpenGL adapter changes
public launcher path/target changes
deployment managed-leaf set changes
```

### OpenGL renderer trigger

```text
OpenGL adapter changes
provider profile changes
Mesa/GLX/Zink/Vulkan provider-layer identity changes
glibc substrate changes
X11/GLX dependency changes
```

### Electron GPU trigger

```text
application launcher/version changes
provider profile changes
Mesa/Vulkan/ANGLE composition changes
selected-device classifier/correlation changes materially
```

### Electron CPU trigger

```text
application launcher/version changes
world sanitation changes
user-data authority changes
CPU feature/argv policy changes
```

Documentation-only changes do not require a runtime rerun unless they invalidate evidence interpretation.

## Recipe lifecycle classification

The recipe directory contains a mixture of:

```text
ACTIVE_CONTRACT_GATE
CANONICAL_EVIDENCE_HELPER
HISTORICAL_DIAGNOSTIC
SUPERSEDED_FALSE_NEGATIVE_MODEL
```

The project must classify individual tools before treating the whole recipe directory as a permanent test suite.

Until that classification is completed, the active contract gates are the final promoted validators referenced by `0091`; older probes and correction helpers are retained for provenance and interpretation.

## Claim boundaries

The closed transaction does not prove:

```text
complete end-to-end zero-copy presentation
hardware video decode
native Dawn WebGPU
long-duration normal-profile behavior
performance equivalence across providers
one universal graphics policy for every consumer
permanent validity of current helper names/paths
```

## Stop line

Do not:

```text
reopen this transaction for PyMOL, WebGPU, video, or zero-copy work;
rerun closed gates without a documented trigger;
add more global graphics policy to gl/env;
expand gl-run into lifecycle authority;
interpret mapped providers as selected devices;
treat current adapters as final semantic objects.
```

## Next architecture work

Graphics experiment expansion stops here.

The next relevant work is:

```text
post-closure contract synthesis
selected Obsidian closure resumption or explicit termination
semantic ownership split
atomic activation
substrate lifecycle
PyMOL contract proof after reusable objects are decided
```
