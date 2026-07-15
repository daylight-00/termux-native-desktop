# 5. Ideal Target Architecture

> **Lifecycle:** historical system-foundation provenance. Current constitutional authority is [`../constitution/`](../constitution/README.md); current architecture is [`../architecture/`](../architecture/README.md). Interpret this document in its recorded context; any later status, precedence, or execution-order wording below is historical to that context.

This document moves from abstract objects to an idealized concrete system. It is a target state, not a command to reorganize every path immediately.

The design goals are:

```text
coherent runtime worlds
explicit capabilities and providers
reproducible materialization
narrow policy scope
clear ownership of state
repeatable validation
cheap promotion and rollback
```

## 5.1 Top-level runtime topology

```text
Android kernel + hardware
        |
        +-- Native Host World (bionic)
        |      Termux shell/tools
        |      desktop session
        |      Termux:X11
        |      native applications
        |      bionic GPU providers
        |
        +-- Foreign Application World (glibc)
               coherent glibc substrate
               shared validated capability providers
               per-application runtime domains
```

The Debian rootfs remains outside the normal execution path:

```text
Supply/Oracle Plane
    Debian PRoot rootfs
    upstream packages/artifacts
    source builds
        |
        v
Candidate materialization
        |
        v
Validation
        |
        v
Promoted runtime
```

## 5.2 Separate source, generated runtime, mutable state, and cache

An ideal ownership model is more important than exact directory names.

Conceptually:

```text
Repository source
    -> version-controlled contracts, scripts, configuration

Generated/materialized runtime
    -> reproducible outputs derived from source + verified inputs

Mutable state
    -> application/user state not overwritten by deploy

Build/cache
    -> disposable or separately archived evidence
```

Possible conceptual paths:

```text
repo/
    contracts/
    providers/
    apps/
    validation/
    scripts/

runtime/
    worlds/
    providers/
    apps/
    manifests/

state/
    apps/<id>/...

cache/
    downloads/
    builds/
```

The current physical paths can remain during migration; the ownership model should be established first.

## 5.3 World substrate

A glibc world substrate should be minimal and coherent.

Conceptual contents:

```text
worlds/glibc/
├── loader/core runtime
├── loader configuration
├── world-base launch policy
└── world validator metadata
```

It should not contain every application-specific workaround.

World-base policy might own:

```text
runtime directory convention
preload-clearing boundary
fundamental loader coherence
world-purity validation
```

It should not own:

```text
VS Code-specific GPU flag
Electron-family sandbox policy unless truly universal to all glibc apps
application-specific PATH shims
```

## 5.4 Capability provider store

Providers should be versioned candidates with explicit promotion.

Example:

```text
providers/
├── mesa-glibc-26.1.x-buildA/
├── mesa-glibc-26.1.x-buildB/
└── mesa-glibc-current -> validated version
```

Each provider has:

```text
manifest
source/build identity
world
provided capabilities
required capabilities
runtime paths/environment fragment
validation results
```

This generalizes the versioned-prefix pattern already useful for Mesa.

## 5.5 Shared artifact pool versus resolved provider closure

The Debian rootfs and broad research farm should not be identical to the promoted shared runtime set.

Ideal flow:

```text
Debian rootfs warehouse
    -> candidate artifact index
    -> resolver/selection
    -> selected shared provider closure
    -> provenance manifest
    -> materialized runtime store
```

During transition:

```text
broad farm
    -> compatibility/research pool
```

can coexist with:

```text
resolved closure
    -> production/promotion target
```

Do not remove the productive research mechanism before the replacement is proven.

## 5.6 Application runtime layout

Each application domain should have a predictable structure.

Conceptual example:

```text
apps/vscode/
├── payload/          # transformed upstream application tree
├── manifest.toml     # source, world, capabilities, policy
├── launch            # generated or thin hand-maintained entrypoint
└── validation/       # app-specific gates or references
```

Mutable user data should not live inside the replaceable payload tree unless the upstream app contract requires and migration policy accounts for it.

## 5.7 Launch composition

The target launch process should be compositional.

```text
application manifest
    -> world base policy
    -> selected capability provider fragments
    -> application-family policy
    -> application-specific policy
    -> conflict checks
    -> exec
```

Conceptual composition:

```text
world.glibc.base
+
bridge.x11.client
+
provider.fonts.default
+
provider.tls.termux-ca
+
provider.graphics.vulkan.glibc.current
+
family.electron
+
app.vscode
```

The result is a deterministic launch contract.

## 5.8 Environment variables are outputs, not architecture

The architecture should define semantic needs first:

```text
select glibc Vulkan provider
```

The current implementation may produce:

```text
VK_ICD_FILENAMES=...
VK_DRIVER_FILES=...
```

Similarly:

```text
provide CA trust
```

may currently produce several environment variables for different consumers.

This distinction prevents the architecture from being frozen around one library version’s environment-variable interface.

## 5.9 Bridge registry

A small bridge registry should document active cross-world interactions.

Example:

```text
bridge.x11
    owner: native session
    transport: Unix socket
    clients: bionic + glibc

bridge.url-open
    owner: host integration shim
    client: glibc apps
    output: Android/Termux intent path

bridge.network
    owner: kernel/network stack
    clients: all process worlds
    policy: app/library-specific proxy and TLS configuration
```

This makes invisible integration assumptions visible.

## 5.10 Passive data providers

Fonts, schemas, locale data, and certificates should be modeled as data capabilities.

Current reality can be represented honestly:

```text
fonts provider
    -> passive files currently located in Debian rootfs
```

Future target:

```text
fonts provider
    -> materialized project-owned selected data closure
```

The architecture does not need to force immediate decoupling, but it should make the dependency visible and replaceable.

## 5.11 Supply adapters

Each input type gets an adapter, not a new runtime architecture.

Examples:

```text
adapter.tarball
adapter.deb
adapter.appimage
adapter.conda
adapter.source-build
```

Adapter responsibilities:

```text
acquire/verify
extract/build into staging
record provenance
hand candidate tree to common inspection/transformation pipeline
```

This keeps runtime onboarding consistent across upstream formats.

## 5.12 Transformation pipeline

Ideal deterministic pipeline:

```text
raw verified input
    -> stage
    -> classify files and ELF objects
    -> patch interpreter where contract requires
    -> normalize search paths while preserving $ORIGIN locality
    -> resolve selected shared providers
    -> materialize data resources
    -> generate application manifest
    -> run static validators
    -> run dynamic validators
    -> promote
```

Every transformation should be idempotent or detect already-transformed state explicitly.

## 5.13 Static validation

Examples:

```text
ELF architecture/world classification
interpreter policy
forbidden NEEDED families
RUNPATH preservation
broken symlink detection
absolute path audit
manifest completeness
provider conflict detection
```

## 5.14 Dynamic validation

Examples:

```text
actual mapping world-purity
X11 connection
font rendering/discovery
TLS request to controlled endpoint
Vulkan ICD/device enumeration
Zink OpenGL renderer verification
Electron GPU process stability
application smoke workflow
```

Validation should produce evidence artifacts, not only exit status.

## 5.15 Promotion transaction

A candidate should not become live merely because build succeeded.

```text
candidate
    -> static gates
    -> dynamic gates
    -> record validation
    -> atomically/reversibly update stable pointer
    -> post-promotion smoke gate
```

Rollback:

```text
stable pointer
    -> previous validated version
```

## 5.16 Runtime manifest

A promoted runtime should be explainable.

At minimum:

```text
artifact identity
world
source provenance
transformations
selected providers
required bridges
file checksums or inventory strategy
validation gates passed
promotion timestamp/commit identity
```

This is the basis for future `gl-doctor` behavior.

## 5.17 Doctor versus adopter

A future tool split is useful.

### `gl-adopt`

Transformation/materialization workflow:

```text
input artifact
    -> inspect
    -> transform
    -> manifest
    -> candidate runtime
```

### `gl-doctor`

Diagnosis/validation workflow:

```text
inspect world coherence
check providers
check bridges
run health gates
report contract violations
```

These should not be built until manual contracts are stable enough to encode.

## 5.18 Ideal repository information flow

```text
question
    -> experiment
    -> evidence
    -> conclusion
    -> decision/invariant update
    -> contract update
    -> validator update
    -> implementation candidate
    -> validation evidence
    -> promotion
```

This adds contracts and gates between decision and live artifact, closing the current gap between knowledge and runtime state.

## 5.19 The target system in one diagram

```text
                    Knowledge / Control
              contracts + validators + promotion
                          |        ^
                          v        |
Supply / Build ---> candidates ---> evidence
     |                    |
     v                    v
warehouse           Application Domains
Debian/source       VS Code / Obsidian / PyMOL
                          |
                          v
                 Capability Providers
              X11 / fonts / TLS / GPU / Python
                          |
                          v
                      Bridges
                X11 / socket / URL / network
                          |
                          v
                    Native Host Plane
              Termux bionic + Android kernel
                          |
                          v
                       Hardware
```

## 5.20 Success criterion

The ideal architecture is achieved not when every directory matches one diagram, but when:

```text
new app onboarding reuses stable contracts;
provider upgrades do not require app-specific reinvention;
world contamination is detected before or immediately at validation;
active runtime state is reproducible and explainable;
rollback is cheap;
experiments can continue without corrupting promoted state.
```

## Project references

- [`../architecture.md`](../architecture.md)
- [`../glibc-layer.md`](../glibc-layer.md)
- [`../gpu.md`](../gpu.md)
- [`../../STATUS.md`](../../STATUS.md)
