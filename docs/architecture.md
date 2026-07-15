# Architecture

This document describes both:

```text
current validated operational realization
    and
active target semantic architecture
```

They are related but not identical.

Current paths, launch helpers, environment variables, and the broad farm may remain useful during migration. They are not permanent architecture merely because they are validated.

Top-down authority:

```text
main: docs/constitution/PROJECT.md
main: docs/constitution/PRINCIPLES.md
provenance: docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
provenance: docs/system-foundation/12-document-consistency-audit-and-execution-order.md
```

Historical post-graphics audit that motivated the current refactor:

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
```

## 1. Project system boundary

The project keeps Android and Termux native.

A glibc application world is composed beside the normal bionic world rather than turning the host into a conventional Linux distribution or using PRoot as the normal application runtime.

```text
Android kernel + device hardware
        |
        +-- KGSL / Adreno 730
        |
        +-- Termux native user space (bionic)
        |       |
        |       +-- Termux:X11 + XFCE session
        |       +-- native applications
        |       +-- native uv-base environment
        |       +-- bionic Mesa / Turnip
        |
        +-- glibc application processes
                |
                +-- package-manager-owned glibc substrate
                +-- protected substrate, selected compatibility providers and rootfs-derived candidates
                +-- application-local payloads
                +-- managed graphics providers
                +-- VS Code, Obsidian, Conda, future workloads
```

The system is heterogeneous by design, but each process must remain inside one coherent ABI world.

## 2. Target semantic objects

The architecture is modeled through:

```text
World
Application Domain
Capability
Provider
Bridge
Artifact Source / Supply Adapter
Validation Gate
```

Examples:

```text
world.bionic
world.glibc

app.vscode
app.obsidian
app.pymol

provider.graphics.vulkan.glibc
provider.graphics.opengl.glibc
provider.fonts.glibc
provider.locale.glibc
provider.tls.glibc

bridge.x11
bridge.url-open

toolchain.glibc-target
```

Current repository directories do not map one-to-one to these objects.

In particular:

```text
modules/gl
    = transitional physical deployment grouping
    != one final semantic owner
```

## 3. Two execution worlds, one display bridge

```text
                    Termux:X11 Android surface
                              ^
                       termux-x11 :1
                              ^
              +---------------+---------------+
              |                               |
         bionic world                    glibc world
         XFCE / native apps              foreign applications
         bionic Mesa/Turnip              glibc providers
```

Both worlds reach the same display service and physical GPU through ABI-appropriate client/provider stacks.

They must not load each other's low-level runtime libraries.

The display relation is a bridge contract, not evidence that both worlds should share one environment or library set.

## 4. Current world baseline

### Bionic/session world

The current desktop session:

- uses `DISPLAY=:1` over the local Unix socket;
- uses the session runtime directory policy;
- exports the bionic Turnip ICD for bionic clients;
- exports a bionic Zink bridge policy for native OpenGL consumers;
- starts the X server under a cleaned environment without client GPU overrides.

### glibc application baseline

Current glibc launchers source the live realization of:

```text
modules/gl/overlay/home/gl/env
    -> ~/gl/env
```

The file currently combines several responsibilities:

```text
runtime-directory policy
X11 default
passive rootfs data paths
font/locale policy
GSettings/accessibility policy
Electron-family sandbox policy
D-Bus clearing
TLS trust policy
graphics boundary sanitation
```

Only the following graphics behavior has been promoted as a durable semantic contract:

```text
remove inherited bionic Vulkan provider policy
remove inherited bionic Zink/Gallium policy
select no glibc graphics provider
select no OpenGL bridge
```

The file path and its remaining accumulated policies are not final architecture.

The highest-priority ownership concern is:

```text
ELECTRON_DISABLE_SANDBOX=1
```

which is Electron-family/security policy currently applied at world scope.

## 5. Current graphics composition

The scoped graphics-policy transaction is closed.

Accepted semantic decomposition:

```text
world-boundary sanitation
Vulkan provider selection
OpenGL-to-Vulkan bridge selection
application GPU/CPU feature mode
application-state authority
selected-device evidence
```

### Managed glibc hardware Vulkan provider

Current realization:

```text
~/gl/policy/vulkan/freedreno.sh
```

It exports a coherent pair of Vulkan loader variables selecting the managed glibc Freedreno/Turnip ICD.

Durable contract:

```text
hardware provider selection is explicit and consumer-scoped
```

The profile path and environment implementation are replaceable.

### OpenGL/Zink consumer

Current realization:

```text
gl-run
    -> explicit provider
    -> MESA_LOADER_DRIVER_OVERRIDE=zink
    -> target program
```

Durable contract:

```text
an OpenGL consumer composition owns its Zink bridge and provider requirements
```

`gl-run` is not a lifecycle manager or permanent universal launcher.

### Electron GPU mode

Current VS Code and Obsidian GPU branches own:

```text
application feature mode
explicit managed Vulkan provider
ANGLE Vulkan argv
no Zink/Gallium override
```

Canonical GPU acceptance correlates:

```text
observable environment/argv
CDP primary selected device
ANGLE/Vulkan feature identity
managed provider mapping
KGSL device mapping
```

Both validated GPU branches selected:

```text
FREEDRENO_TURNIP
Adreno 730
ANGLE_VULKAN
GaneshVulkan
managed libvulkan_freedreno.so
/dev/kgsl-3d0
```

### Electron CPU mode

Accepted CPU semantics:

```text
provider-neutral sanitized baseline
exact --disable-gpu
no GPU-enablement flags
effective disabled/compositing behavior
viable renderer/main topology
bounded survival
```

A process named `gpu-process` may or may not exist. Process naming is not the invariant.

## 6. Current graphics provider graph

The validated OpenGL/Zink composition is cross-version:

```text
rootfs GLVND / GLX / Gallium-Zink frontend 25.0.7
    -> prefix Vulkan loader/support
    -> provider-store Turnip/Freedreno 26.1.4 lineage
    -> KGSL
    -> Adreno 730
```

The tested composition works.

It must be identified as a composition of independently changing layers rather than one generic `Mesa version`.

Changes to any participating layer can trigger revalidation.

The investigated Mesa build policy currently uses:

```text
-Dfreedreno-kmds=msm,kgsl
```

The practical working/broken split tracked the retained libdrm dependency. The exact low-level present-SIGBUS mechanism remains open.

## 7. Application-state authority

A clean launch is not automatically an isolated launch.

Canonical validation authority:

```text
VS Code
    receipt-local user-data
    receipt-local extensions

Obsidian
    receipt-local XDG_CONFIG_HOME
    actual receipt-local <config>/obsidian directory
```

The first Obsidian CDP attempt failed because the probe observed the wrong application-owned endpoint path while normal state remained authoritative.

Normal settings, extensions, vaults, plugins, locks, and long-duration behavior are outside architecture-promotion receipts.

Operational user acceptance is a separate claim class.

## 8. Current library/provider realization

The current operational lookup model remains:

```text
application-local $ORIGIN
    -> protected Termux glibc core / Android-sensitive providers
    -> filtered Debian-rootfs-derived farm
```

Load-bearing rules:

- libc-family objects come from the package-manager-owned glibc substrate;
- Termux-aware glibc X11/xcb providers win where Android/Termux transport behavior requires them;
- valid application-local `$ORIGIN` locality must be preserved;
- broad `LD_LIBRARY_PATH` injection is rejected;
- the current farm/cache model resolves many transitive providers.

This is the current compatibility baseline, not the accepted final production provider architecture.

The D-Bus pilot proved that a selected materialized provider closure can own:

```text
actual provider bytes
provenance
candidate-specific selection proof
protected substrate boundary
zero broad-farm/rootfs leakage
```

The selected Obsidian pilot is still incomplete. It must resume or be terminated explicitly before the project claims a reusable real application-domain closure model.

## 9. Data-provider realization

Current glibc applications can read broad rootfs-backed:

```text
fonts
fontconfig configuration
locale data
GSettings schemas
other XDG shared data
```

These are passive data-provider dependencies, not PRoot process execution.

Their final ownership remains open per capability:

```text
intentional rootfs-backed provider
selected materialized data closure
application-local provider
```

## 10. Supply and substrate

The real device currently uses APT/dpkg as the glibc substrate backend.

Architecture remains backend-neutral.

Current containment:

```text
glibc 2.42 installed and held
exact recovery artifact retained
known tested 2.43 state incompatible with current provider requirement
```

The hold is not a lifecycle design.

A future substrate contract must define:

```text
identity
candidate acquisition
core ABI gates
provider compatibility
application regression gates
previous artifact retention
rollback
hold release criteria
```

Do not solve this by making the farm or `gl-run` the lifecycle owner.

## 11. Deployment and activation

The repository checkout is authoring state, not live runtime authority.

`tools/deploy` materializes complete immutable releases under:

```text
${XDG_STATE_HOME:-$HOME/.local/state}/termux-native-desktop/deployment/releases/<tree>-<profile>/
```

Managed public leaves resolve through one stable deployment `current` pointer. A repository checkout, pull or branch change has no live effect until a complete candidate release is built, validated and activated. The deployment retains a `previous` pointer and supports pointer rollback.

```text
checkout change
    -> candidate immutable release
    -> pre-activation validation
    -> atomic current-pointer switch
    -> post-activation status/smoke
    -> retained previous release
```

Physical profiles are `workstation` and `full`; they are deployment groupings, not final semantic ownership claims.

Generated state remains outside repository releases:

```text
application payloads and user data
selected application generations
Mesa workspace
Mesa provider candidates and active provider pointer
compatibility farm and other derived runtime state
```

Mesa mutable build state and versioned provider candidates now live under the XDG-state workspace/provider store. Legacy `$HOME/gl/build` and `$HOME/gl/opt` locations are compatibility paths only.

Repository deployment rollback and provider rollback are separate authority domains. Neither implies application-generation activation or provider-authority acceptance.

## 12. Evidence lifecycle

The repository lifecycle is:

```text
question
    -> experiment
    -> evidence
    -> interpretation correction
    -> contract
    -> canonical gate
    -> promotion
    -> trigger-based revalidation
```

Closed investigations should classify tools as:

```text
ACTIVE_CONTRACT_GATE
CANONICAL_EVIDENCE_HELPER
HISTORICAL_DIAGNOSTIC
SUPERSEDED_FALSE_NEGATIVE_MODEL
```

Not every experiment helper is a permanent active test.

Current graphics closure:

```text
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

Historical architecture audit:

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
```

## 13. Next architecture order

```text
1. keep the current documentation and agent control plane internally consistent;
2. consolidate durable document authority and explicitly classify current, superseded and historical material;
3. define proportional assurance depth for reference-supplied, adapted, independently reproduced and novel providers;
4. decide whether and how the paused provider-authority workstream resumes;
5. define ApplicationRuntimeComposition only after owning authorities are accepted;
6. populate target rows only after composition acceptance;
7. implement extraction/materialization only after the intervention-lift audit permits it;
8. use later workloads such as PyMOL to test the resulting reusable objects rather than expanding global compatibility by inertia.
```

Immutable repository activation and XDG-state Mesa ownership are already implemented. Do not reopen them as missing architecture work unless a new failure demonstrates a contract gap.

Do not resume SUP-02 production, populate a provider target or start PyMOL by expanding the broad farm or global environment before the assurance and ownership decisions above.

## 14. Repository ownership map

Current source ownership:

```text
modules/
    project-authored physical integration and overlays

packages/
    external payload lifecycle and application launch integration

experiments/
    architecture discrimination, evidence, and provenance

tools/
    repository/operator workflows

tests/
    cross-cutting repository/integration gates
```

This is a source ownership taxonomy.

Runtime semantic ownership remains the World/Provider/Bridge/Application/Toolchain model above.
