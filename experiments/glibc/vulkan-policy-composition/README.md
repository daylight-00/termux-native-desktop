# Vulkan Policy Composition Experiment

## Status

```text
SCOPED_TRANSACTION_CLOSED
VALIDATOR_LIFECYCLE_CLASSIFIED
TRIGGER_BASED_REVALIDATION_ONLY
```

Canonical closure:

```text
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

Post-closure audit and direction:

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
docs/refactor/0093-post-audit-direction-validator-lifecycle-and-selected-closure-reentry.md
```

The architecture-discrimination experiment is complete for the accepted scoped graphics-policy contract.

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

Detailed evidence roots, commit identities, gate counts, false-negative corrections, and claim boundaries are in `docs/refactor/0083` through `0091`.

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

Primary selected-device probes established:

```text
explicit profile
    -> FREEDRENO_TURNIP
    -> Adreno 730

implicit discovery control
    -> LVP / llvmpipe primary device
```

Map presence alone is not selected-device proof.

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

## Active contract gates

These are the only top-level promoted graphics contract receipts.

```text
validate-promoted-vulkan-policy-transaction.sh
validate-live-vulkan-policy-installation.sh
validate-promoted-gl-run-renderer.sh
validate-promoted-vscode-gpu-identity.sh
validate-promoted-vscode-cpu-policy.sh
validate-promoted-obsidian-gpu-identity.sh
validate-promoted-obsidian-cpu-policy.sh
```

Run an active gate only when its documented claim surface changes.

## Active gate implementation dependencies

These are invoked by an active gate and are maintained with that owner gate. They are not independently scheduled.

```text
build-glx-renderer-probe.sh
glx-renderer-probe.c
probe-vscode-policy-env-boundary.sh
probe-vscode-cdp-gpu-identity.sh
classify-vscode-cdp-gpu-identity.sh
probe-electron-cdp-gpu-identity.sh
classify-cdp-gpu-identity.sh
query-cdp-system-info.py
```

## Canonical evidence helpers

These interpret or compare retained evidence. They do not independently prove the current promoted runtime.

```text
audit-promoted-vulkan-policy-ownership-v2.sh
capture-glx-probe-maps.sh
enrich-glx-probe-maps.sh
compare-glx-provider-graphs.sh
compare-obsidian-policy-controls.sh
compare-vscode-cdp-gpu-identities.sh
compare-vscode-vulkan-policy-controls.sh
summarize-obsidian-loader-debug.sh
```

## Historical diagnostics

These remain for provenance and targeted future debugging. They are not routine gates.

```text
capture-implicit-loader-debug.sh
launch-obsidian-with-policy.sh
launch-vscode-with-policy.sh
policy-env.sh
probe-driver-isolation-matrix.sh
probe-vscode-app-local-vulkan-loader.sh
probe-vscode-gpu-observer-contract.sh
probe-vscode-process-handoff.sh
run-zink-with-policy.sh
```

## Superseded false-negative models

The important superseded models are historical commits/receipts, not current runnable files.

```text
old VS Code child-environment exact-value assumption
    -> docs/refactor/0085

first Obsidian user-data/CDP path assumption
    -> docs/refactor/0088

first unsuffixed promoted ownership audit helper
    -> superseded by audit-promoted-vulkan-policy-ownership-v2.sh before use
```

Do not classify the corrected current file as superseded merely because an older commit of the same path was wrong.

## Revalidation policy

Do not blind-rerun this experiment.

### Source/live transaction trigger

```text
glibc world-boundary sanitation changes
provider profile changes
current OpenGL adapter changes
public launcher path/target changes
deployment managed-leaf set changes
```

Run:

```text
validate-promoted-vulkan-policy-transaction.sh
validate-live-vulkan-policy-installation.sh after deliberate activation
```

### OpenGL renderer trigger

```text
OpenGL adapter changes
provider profile changes
Mesa/GLX/Zink/Vulkan provider-layer identity changes
glibc substrate changes
X11/GLX dependency changes
```

Run:

```text
validate-promoted-gl-run-renderer.sh
```

### Electron GPU trigger

```text
application launcher/version changes
provider profile changes
Mesa/Vulkan/ANGLE composition changes
selected-device classifier/correlation changes materially
```

Run only the affected application GPU gate.

### Electron CPU trigger

```text
application launcher/version changes
world sanitation changes
user-data authority changes
CPU feature/argv policy changes
```

Run only the affected application CPU gate.

### Dependency/helper trigger

A change to an active gate dependency triggers its owning gate, not every graphics gate.

### Documentation/evidence trigger

```text
documentation only
    -> no runtime gate unless evidence interpretation is invalidated

evidence comparison policy only
    -> relevant canonical evidence helper over retained evidence
```

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
treat current adapters as final semantic objects;
maintain every recipe file as an active gate.
```

## Next architecture work

Graphics experiment expansion stops here.

The next active work is:

```text
selected Obsidian closure retained-evidence audit
locality-shadowing and non-graphics static/runtime closure analysis
semantic provider/application ownership decision
minimum activation design before the next promoted migration
substrate lifecycle
PyMOL proof after reusable objects are decided
```
