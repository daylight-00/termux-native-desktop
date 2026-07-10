# 4. Domain, Capability, Provider, and Bridge Model

The six-plane architecture becomes implementable when it is expressed through a small object model.

The proposed core objects are:

```text
World
Application Domain
Capability
Provider
Bridge
Artifact Source
Validation Gate
```

These are conceptual objects first. They can later become Markdown contracts, TOML/YAML manifests, shell modules, or generated launch plans.

## 4.1 World

A **World** defines a coherent userspace ABI/runtime domain.

Example worlds:

```text
world.bionic
world.glibc
```

Possible properties:

```text
id
ELF interpreter family
libc family
loader search policy
forbidden foreign families
base runtime environment
runtime directory policy
inspection commands
purity validator
```

Example conceptual contract:

```yaml
id: world.glibc
interpreter_family: glibc
libc_family: glibc
forbidden_mappings:
  - bionic-runtime-libraries
base_policy:
  clear_preload: true
validation:
  - world-purity
```

## 4.2 Application Domain

An **Application Domain** is a supported application plus its runtime contract.

It is not merely an executable path.

Properties:

```text
id/version
world
source artifact
entrypoint
app-local closure
required capabilities
family policies
specific policies
state directories
validation gates
```

Example:

```text
app.vscode
    world: glibc
    requires:
        display.x11
        graphics.angle-vulkan
        fonts.fontconfig
        tls.ca-trust
        integration.url-open
```

## 4.3 Capability

A **Capability** is a named behavior an application requires.

Good capability names describe outcomes rather than implementation files.

Better:

```text
graphics.opengl
```

than:

```text
libGL.so.1
```

because OpenGL capability may involve:

```text
libGL frontend
GLX integration
Zink
Vulkan loader
ICD metadata
Turnip
KGSL access
```

One `.so` name does not express the whole runtime contract.

## 4.4 Provider

A **Provider** implements a capability for a specific context.

Example:

```text
provider.graphics.opengl.glibc.zink
    provides: graphics.opengl
    world: glibc
    depends on:
        graphics.vulkan.glibc
        display.x11
```

Another provider could later implement the same capability differently.

Provider properties:

```text
id
world
version/build identity
provides
requires
materialization path
environment fragment
loader/search requirements
health checks
promotion pointer
rollback target
```

## 4.5 Bridge

A **Bridge** connects domains without merging ABI worlds.

Examples:

```text
bridge.x11
bridge.url-open
bridge.network
bridge.filesystem-export
```

Bridge contract fields:

```text
transport
endpoint discovery
client worlds
server/owner world
lifecycle
permissions
protocol version/expectations
health check
```

Example:

```yaml
id: bridge.x11
transport: unix-socket
server_owner: world.bionic
clients:
  - world.bionic
  - world.glibc
address_policy:
  DISPLAY: ':1'
validation:
  - x11-connect
```

## 4.6 Artifact Source

An **Artifact Source** describes where a candidate input came from.

Types:

```text
upstream-tarball
deb-package
appimage
conda-package
wheel
source-build
termux-package
```

Properties:

```text
origin
version
checksum/signature
license/redistribution status
acquisition method
extraction/build adapter
```

The source object belongs to the supply plane; it should not silently become runtime authority.

## 4.7 Validation Gate

A **Validation Gate** is a repeatable test that supports one specific claim.

Examples:

```text
gate.world-purity
    claim: no cross-ABI mapped runtime objects

gate.x11-connect
    claim: client reaches intended Termux:X11 display

gate.vulkan-adreno
    claim: intended ICD loads and Adreno device enumerates

gate.zink-opengl
    claim: OpenGL consumer reports Zink/Turnip renderer

gate.vscode-gpu-process
    claim: VS Code GPU process remains stable under defined workload
```

A gate should record:

```text
inputs
command/action
expected evidence
failure output
scope
```

## 4.8 Relationships

The model can be drawn as:

```text
Application Domain
    --belongs-to----> World
    --requires------> Capability
    --derived-from--> Artifact Source
    --validated-by--> Validation Gate

Capability
    --provided-by---> Provider

Provider
    --belongs-to----> World
    --requires------> Capability
    --uses----------> Bridge
    --validated-by--> Validation Gate

World
    --communicates-through--> Bridge
```

This graph is more expressive than a flat launcher script.

## 4.9 VS Code mapping

### Application

```text
id: app.vscode
world: glibc
entrypoint: upstream bin/code wrapper path
```

### Capabilities

```text
display.x11
fonts.fontconfig
tls.ca-trust
graphics.angle-vulkan
integration.url-open
```

### Providers

```text
display.x11/glibc
    -> Termux-aware glibc X11/xcb libraries

graphics.angle-vulkan/glibc
    -> Electron/ANGLE Vulkan consumer policy
    -> glibc Vulkan provider

graphics.vulkan/glibc
    -> glibc Mesa Turnip

tls.ca-trust/glibc
    -> Termux CA bundle exposure
```

### Bridges

```text
X11 Unix socket
network sockets
URL-opening shim to host integration
```

### Application-specific policy

```text
validated GPU-vsync workaround
shell integration
specific Electron launch flags
```

The important design point is that application-specific policy should not be promoted into the entire glibc world.

## 4.10 Obsidian mapping

Obsidian shares some Electron-family behavior but has a different source adapter:

```text
Artifact Source
    -> AppImage
    -> extracted SquashFS application tree
```

Application contract can reuse:

```text
world.glibc
display.x11
fonts.fontconfig
tls.ca-trust
Electron family policy where actually shared
```

while keeping app-specific differences separate.

## 4.11 PyMOL mapping

PyMOL should be modeled before implementation choice.

### Stable application requirements

Likely categories:

```text
world: glibc or explicitly chosen alternative
python.runtime
display.x11
graphics.opengl
fonts.fontconfig
scientific native-extension ABI
```

### Open provider choices

```text
python.runtime
    -> Conda environment
    -> source-built Python/prefix
    -> other validated provider

graphics.opengl
    -> Zink -> Vulkan -> Turnip
```

The application domain should not be defined as “whatever `conda install` produced.” Conda is an acquisition/materialization strategy that can implement part of the contract.

## 4.12 Capability composition

Capabilities can depend on other capabilities.

Example:

```text
graphics.opengl.glibc
    -> graphics.vulkan.glibc
    -> display.x11

graphics.vulkan.glibc
    -> GPU kernel access
    -> Vulkan ICD provider
```

This creates a typed dependency graph that can be validated at each layer.

## 4.13 Environment fragments

Instead of one global environment file owning everything, providers can conceptually contribute fragments:

```text
world.glibc.base
    -> XDG_RUNTIME_DIR, preload clearing policy

provider.fonts
    -> FONTCONFIG_PATH / data policy

provider.tls
    -> CA bundle policy

provider.vulkan.glibc
    -> ICD variables

family.electron
    -> sandbox policy if still required

app.vscode
    -> VS Code-specific GPU flags
```

A launcher composer can merge these in a deterministic order.

Initially, the composition can remain hand-written shell while the contracts are documented. Automation should follow only after semantics stabilize.

## 4.14 Conflict detection

A future resolver/doctor can detect conflicts such as:

```text
application requires world.glibc
provider belongs to world.bionic
    -> reject

app requires graphics.opengl
no provider selected
    -> fail before launch

provider A and B both claim exclusive Vulkan ICD policy
    -> explicit conflict
```

This is more robust than discovering contamination through `invalid ELF header` after process startup.

## 4.15 Minimal manifest sketch

A future machine-readable format might look like:

```toml
[app]
id = "vscode"
world = "glibc"
entrypoint = "apps/vscode/bin/code"

[requires]
capabilities = [
  "display.x11",
  "fonts.fontconfig",
  "tls.ca-trust",
  "graphics.angle-vulkan",
  "integration.url-open",
]

[policy]
family = "electron"

[validation]
gates = [
  "world-purity",
  "x11-connect",
  "vulkan-adreno",
  "vscode-gpu-process",
]
```

The exact serialization format is intentionally open. The important step is to stabilize the object model first.

## 4.16 Admission question for every new component

Before adding a file, environment variable, shim, or library, ask:

```text
Which object owns this?

World base?
Capability provider?
Bridge?
Application family?
Specific application?
Supply/build tooling?
Validation only?
```

If the answer is unclear, the component is likely crossing responsibilities.

## Project references

- [`../architecture.md`](../architecture.md)
- [`../glibc-layer.md`](../glibc-layer.md)
- [`../gpu.md`](../gpu.md)
- [`../desktop-session.md`](../desktop-session.md)
