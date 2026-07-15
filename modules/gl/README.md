# gl module

The `gl` module is the current **physical deployment grouping** for project-authored integration used by the managed glibc application world.

It is not one final semantic owner.

The active system-foundation model distinguishes responsibilities such as:

```text
world.glibc base
provider.shared/data capabilities
provider.graphics.vulkan.glibc
provider.graphics.opengl.glibc
bridge.url-open
family.electron policy
toolchain.glibc-target
application-domain bindings
```

The current directory groups several of those responsibilities for transitional deployment compatibility. Future refactoring may split, delete, or re-home files without preserving the `modules/gl` object identity, provided validated semantics and evidence are preserved.

## Current physical contents

```text
modules/gl/overlay/home/gl/
├── env
├── bin/
│   ├── gl-farm
│   └── gl-run
├── policy/
│   └── vulkan/
│       └── freedreno.sh
├── shims/
│   └── xdg-open
└── toolchain/
    ├── glibc-ar
    ├── glibc-exec
    ├── glibc-g++
    ├── glibc-gcc
    ├── glibc-pkg-config
    ├── glibc-ranlib
    └── glibc-strip
```

These files currently map to the same relative paths under `$HOME/gl/`.

## Current realization versus durable contract

### `env`

Current realization:

```text
shared glibc launch baseline
world-boundary graphics sanitation
runtime/data/TLS/desktop/family policy accumulation
```

Durable graphics contract:

```text
foreign bionic provider/bridge policy is removed at the glibc boundary;
the baseline does not choose a glibc graphics provider or bridge.
```

The file still contains non-graphics responsibilities with different candidate owners. In particular, `ELECTRON_DISABLE_SANDBOX=1` is Electron-family/security policy and must not be interpreted as a proven world-wide invariant.

### `policy/vulkan/freedreno.sh`

Current realization:

```text
source-only explicit managed Freedreno/Turnip provider profile
```

Durable contract:

```text
hardware Vulkan provider selection is explicit, coherent, and consumer-scoped.
```

The profile path and environment-variable implementation are replaceable.

### `gl-run`

Current realization:

```text
explicit managed Vulkan provider
    +
Zink OpenGL bridge
    +
exec target
```

Durable contract:

```text
an OpenGL consumer composition owns its Zink bridge and provider requirements.
```

`gl-run` is a transitional capability adapter, not a world lifecycle gateway or permanent command API. Do not extend it with synchronization, package management, provider generation, readiness, or universal application-launch responsibilities.

### `gl-farm`

Current realization:

```text
broad rootfs scan
libc-family denylist
symlink materialization
loader-cache refresh
```

Architectural status:

```text
research/control/compatibility mechanism
    !=
accepted final production provider architecture
```

The selected D-Bus pilot proves provenance-aware materialized provider bytes are viable. The final shared/app-local/provider boundary remains open.

### `shims/xdg-open`

Semantic owner candidate:

```text
bridge.url-open
```

### `toolchain/*`

Semantic owner candidate:

```text
toolchain.glibc-target
```

## Current responsibility separation

The validated graphics transaction preserves:

```text
world-boundary sanitation
explicit Vulkan provider selection
OpenGL-to-Vulkan bridge selection
application feature/argv mode
application-state validation authority
```

Do not collapse these into one global environment side effect.

Do not infer from this that all contents belong to one permanent module.

## Explicit non-ownership

The current module does not Git-own:

```text
$HOME/gl/apps/       upstream-supplied application bodies
$HOME/gl/lib/        generated compatibility farm
XDG-state workspaces mutable source/build state
XDG-state providers  versioned candidates and active provider pointers
$HOME/gl/build/      compatibility paths into the Mesa workspace
$HOME/gl/opt/        compatibility paths into provider candidates/current
$PREFIX/glibc/       package-manager-owned world substrate
Debian rootfs        oracle, supply backend and package/library/data warehouse
```

Application-specific launchers belong to their package/application owners, not to generic `gl/bin` ownership.

## Next ownership pressure

The repository activation boundary and Mesa local-layout separation are complete. The remaining ownership pressure is semantic rather than a missing filesystem move:

```text
1. define proportional assurance depth before resuming provider acquisition;
2. decide the semantic provider/bridge/family/application split;
3. preserve or narrow the broad farm based on accepted composition evidence;
4. move high-risk over-scoped policies only with evidence;
5. preserve current adapters only when they remain the simplest valid implementation.
```

See:

```text
docs/refactor/0017-gl-umbrella-semantic-inventory.md
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
main:docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
```
