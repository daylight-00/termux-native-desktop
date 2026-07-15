# glibc Application Layer

This guide describes the current operational glibc application world and the active migration boundary toward explicit world/provider/bridge/application objects.

Detailed provenance remains under:

```text
experiments/glibc/
experiments/gpu/
docs/refactor/
```

Historical architecture audit that motivated the current ownership model:

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
```

## Goal

Run conventional Linux arm64/glibc application distributions from native Termux without using PRoot as the application runtime.

Current operational locations:

```text
application payloads    $HOME/gl/apps/<name>/
compatibility farm      $HOME/gl/lib/
glibc substrate         $PREFIX/glibc/
Debian warehouse        $PREFIX/var/lib/proot-distro/containers/debian/rootfs
Mesa workspace          ${XDG_STATE_HOME:-$HOME/.local/state}/termux-native-desktop/workspaces/mesa/
Mesa provider store     ${XDG_STATE_HOME:-$HOME/.local/state}/termux-native-desktop/providers/mesa/
legacy Mesa paths       $HOME/gl/build and $HOME/gl/opt compatibility symlinks
```

PRoot is retained for package installation, dependency discovery, passive artifacts/data, and debugging controls. Runtime applications execute outside PRoot.

## Architecture status

The current farm/env/launcher model is validated operationally.

It is not the final target architecture.

Target semantic objects include:

```text
world.glibc
provider capabilities
bridge contracts
application domains
supply adapters
validation gates
```

Current `modules/gl`, `~/gl/env`, `gl-run`, and `gl-farm` are transitional realizations and may be split or replaced.

## Current library boundary

Operational lookup model:

```text
application-local $ORIGIN
    -> $PREFIX/glibc/lib and protected Termux glibc providers
    -> $HOME/gl/lib compatibility farm
```

Load-bearing rules:

- never expose a glibc `LD_LIBRARY_PATH` to the bionic Termux shell;
- libc-family objects come from the package-manager-owned Termux glibc substrate;
- Android/Termux-sensitive glibc X11/xcb providers must win where local Termux:X11 transport requires them;
- application-local `$ORIGIN` locality must be preserved where valid;
- transitive dependencies currently use glibc loader configuration/cache rather than broad `LD_LIBRARY_PATH` injection;
- package/prefix location is provenance evidence, not automatic semantic ownership.

## Current bootstrap baseline

The current established environment was built through:

1. Termux X11/glibc prerequisites;
2. package-manager-owned glibc substrate and Termux-aware glibc X11/xcb providers;
3. Debian PRoot warehouse;
4. broad compatibility farm generation;
5. loader configuration/cache;
6. module/package launcher deployment.

Representative historical commands:

```sh
pkg install x11-repo tur-repo termux-x11-nightly patchelf file curl proot-distro
pkg install glibc-repo glibc libx11-glibc libxcb-glibc
proot-distro install debian
```

These commands describe the current input lineage. They do not mean every new application should expand the broad farm by default.

## Broad farm status

Current `gl-farm`:

```text
scans broad Debian rootfs library directories
excludes protected libc-family names
materializes symlinks
checks contamination
refreshes loader cache
```

Architectural status:

```text
current compatibility/research/control baseline
    !=
accepted final production provider model
```

The D-Bus pilot proved a smaller object class:

```text
selected provider-owned bytes
provenance receipt
candidate-specific actual selection
protected substrate boundary
zero broad-farm/rootfs leakage
```

The real application-domain boundary remains under investigation through the selected Obsidian closure pilot.

## Application onboarding: two tracks

### Current compatibility onboarding

For an existing conventional tarball/AppDir while preserving current runtime behavior:

1. record upstream source identity and license/redistribution boundary;
2. unpack under an application-owned payload path;
3. preserve application-local `$ORIGIN` locality;
4. classify ELF objects and interpreter requirements;
5. use the Debian warehouse as an oracle/supply source;
6. use current farm/provider paths only as the established compatibility baseline;
7. create a package/application-owned launcher;
8. separate CPU/basic startup, graphics provider selection, and selected-device evidence;
9. isolate application-owned validation state;
10. record revalidation triggers.

### Target architecture onboarding

Before a new major workload is promoted, define:

```text
application domain
world
app-local closure
required capabilities
provider bindings
bridges
mutable-state authority
validation gates
supply/provenance
```

Then decide whether dependencies are:

```text
world substrate
intentional shared provider
selected supplemental provider closure
application-local payload
data provider
runtime-generated state
```

Do not begin by copying libraries or adding global environment variables.

## Graphics policy boundary

The scoped graphics-policy transaction is closed.

The glibc baseline removes inherited bionic/session values for:

```text
VK_ICD_FILENAMES
VK_DRIVER_FILES
MESA_LOADER_DRIVER_OVERRIDE
GALLIUM_DRIVER
```

The baseline does not choose a glibc graphics provider or OpenGL bridge.

Current managed hardware profile:

```text
$HOME/gl/policy/vulkan/freedreno.sh
```

Durable contract:

```text
hardware Vulkan provider selection is explicit and consumer-scoped
```

Current OpenGL adapter:

```text
gl-run
    -> managed provider
    -> Zink bridge
```

Durable contract:

```text
OpenGL consumer composition owns the bridge/provider requirements
```

Current Electron application branches own GPU/CPU feature mode.

The paths, helper name, and `GL_GPU` variable are current implementations, not permanent semantic objects.

## Application-state isolation

Validation must follow the application's actual state authority.

Accepted patterns:

```text
VS Code
    receipt-local user-data directory
    receipt-local extensions directory

Obsidian
    receipt-local XDG_CONFIG_HOME
    actual <config>/obsidian directory
```

Normal profiles are outside promotion evidence.

Operational daily-workstation acceptance is a separate claim class.

## Non-graphics global policy debt

The current shared baseline still contains policies with different candidate owners:

```text
DISPLAY
runtime-directory policy
rootfs XDG data
fontconfig
locale
GSettings/accessibility
Electron sandbox policy
D-Bus clearing
TLS trust variables
```

The highest-risk over-scope is:

```text
ELECTRON_DISABLE_SANDBOX=1
```

It is Electron-family/security policy, not an obvious invariant for every glibc process.

Do not move every variable at once. Use semantic ownership and discriminating evidence.

## Selected application-domain closure

The selected Obsidian pilot remains active and incomplete.

It must answer whether a real Electron AppDir can consume selected external provider bytes while preserving:

```text
app-local $ORIGIN locality
protected substrate
prefix provider roles
font/locale/schema data capability separation
candidate-specific selection
control/candidate workload equivalence
```

Canonical status:

```text
experiments/glibc/selected-obsidian-closure/README.md
```

Graphics closure does not close this parent question.

## glibc substrate state

Current device backend:

```text
APT/dpkg
```

Current containment:

```text
glibc 2.42 installed and held
exact recovery artifact preserved
known tested 2.43 compatibility failure
```

The target lifecycle must manage `world.glibc` substrate independently from provider closure.

Required future contract:

```text
substrate identity
candidate acquisition
core ABI validation
provider compatibility
application regression gates
previous artifact retention
rollback
hold release criteria
```

Do not revive a farm-centric or `gl-run`-centric lifecycle.

## Activation boundary

Repository deployment already uses immutable materialized releases and explicit activation.

```text
repository checkout
    != live release

complete release candidate
    -> validation
    -> deployment current-pointer switch
    -> post-activation status/smoke
    -> previous-pointer rollback target
```

`tools/deploy --profile workstation|full` owns project-managed public leaves. A pull or branch change does not alter those leaves until deployment activation.

Other mutable authorities remain separate:

```text
Mesa provider promotion
selected application-generation activation
compatibility-farm regeneration
loader cache/state mutation
application payload and user-data changes
```

The Mesa provider store has its own canonical `current` pointer under XDG state, while legacy `$HOME/gl/opt/mesa-glibc` remains a compatibility path. Repository rollback does not automatically roll back a provider, and provider rollback does not change the glibc substrate or selected application generation.

## Evidence interpretation

GPU acceptance requires correlated selected-device evidence.

CPU acceptance is effective-mode based.

Empty child environment reads are observability boundaries.

Mapped provider objects do not by themselves prove selection.

Closed gates are rerun only when their claim surface changes.

After experiment closure, scripts must be classified as:

```text
active contract gate
canonical evidence helper
historical diagnostic
superseded false-negative model
```

## Common failure signatures

1. **ABI contamination** — bionic processes encounter glibc libraries or vice versa.
2. **Substrate/provider incompatibility** — farm/provider rebuild cannot repair missing substrate symbols.
3. **Transitive provider failure** — direct object resolves but downstream closure does not.
4. **X11 provider mismatch** — non-Termux-aware X11/xcb provider wins.
5. **Lost `$ORIGIN`** — bundled application libraries stop resolving.
6. **Wrong graphics provider** — bionic policy crosses the boundary or explicit profile is missing.
7. **Unexpected Zink/Gallium** — bridge/device policy leaked from session or another consumer.
8. **Implicit software provider** — unset Vulkan variables allow discovery; they do not mean no Vulkan.
9. **Application-state mismatch** — probe observes a different user-data authority than the app.
10. **Activation-domain mismatch** — repository release, provider pointer, selected generation or derived loader state is changed or rolled back as though it were the same authority domain.

## Current validated workloads

- official VS Code GPU and CPU branches;
- extracted Obsidian GPU and CPU branches;
- Miniforge/Conda/Mamba plus compiled NumPy;
- glibc OpenGL 4.6 through the current Zink/Turnip composition;
- bounded D-Bus selected-provider candidate;
- same-consumer explicit Turnip versus implicit LVP/llvmpipe controls.

## Next workload rule

PyMOL may be designed now as an application-domain contract.

Runtime mutation is deferred until the project decides enough reusable objects:

```text
world.glibc
Python runtime provider
X11 bridge/provider
OpenGL provider
font/locale/data providers
native-extension ABI contract
application payload/state ownership
```

Do not onboard PyMOL by broadening `gl/env`, blindly extending the farm, or treating `gl-run` as a universal application launcher.
