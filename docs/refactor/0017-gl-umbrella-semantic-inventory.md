# 0017 — Current `gl` Umbrella Semantic Inventory

## Status

This document is the Stage 2 semantic inventory required by:

```text
main/docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
main/docs/system-foundation/12-document-consistency-audit-and-execution-order.md
docs/refactor/0015-architecture-reassessment-and-hard-refactor-direction.md
docs/refactor/0016-next-session-handoff.md
```

It records semantic ownership before any physical hard split.

The current `modules/gl` directory is treated as a transitional physical deployment grouping, not as one final semantic object.

## Inventory method

Each current mechanism is classified by:

```text
mechanism
semantic purpose
current owner
actual consumers
minimum valid scope
evidence
candidate semantic owner
migration/removal condition
```

Candidate owner classes:

```text
world
provider
bridge
toolchain
application family
specific application
validation only
supply adapter
transitional research/control
```

## 1. `modules/gl/overlay/home/gl/env`

The file is a composition result spanning several semantic objects.

### 1.1 `DISPLAY=${DISPLAY:-:1}`

```text
mechanism:
    default X11 display address

semantic purpose:
    discover the native Termux:X11 endpoint

current owner:
    modules/gl/env

actual consumers:
    VS Code launcher
    Obsidian launchers
    gl-run workloads
    any launcher sourcing ~/gl/env

minimum valid scope:
    X11 client compositions only

evidence:
    Phase B isolated environment validation observed DISPLAY=:1

candidate semantic owner:
    bridge.x11 client contract

migration/removal condition:
    move only after X11 endpoint discovery and health-check contract is explicit
```

### 1.2 `XDG_RUNTIME_DIR=$PREFIX/tmp/gl-runtime`

```text
semantic purpose:
    glibc-world runtime-directory convention

minimum valid scope:
    world or process-domain base policy

candidate semantic owner:
    world.glibc base process policy

open point:
    prove which consumers require this dedicated directory and whether one shared
    world directory is correct for all foreign application domains
```

### 1.3 `TMPDIR=$PREFIX/tmp`

```text
semantic purpose:
    temporary-file placement compatible with the Termux application sandbox

minimum valid scope:
    not yet proven world-wide

candidate semantic owner:
    provisional world.glibc policy, pending consumer audit

migration condition:
    classify actual consumers and any application-specific assumptions first
```

### 1.4 Debian rootfs path

```text
ROOTFS=$PREFIX/var/lib/proot-distro/containers/debian/rootfs
```

```text
semantic purpose:
    locate current Debian warehouse/passive-data source

candidate semantic owner:
    Debian supply adapter / passive-data provider inputs

important constraint:
    rootfs location is supply/provider input identity, not world identity
```

### 1.5 `XDG_DATA_DIRS`

```text
semantic purpose:
    expose Debian-rootfs shared data and schemas

current scope:
    all launchers sourcing env

minimum valid scope:
    selected passive shared-data provider consumers

candidate semantic owner:
    provider.shared-data.glibc

migration condition:
    inventory actual schemas/data consumed and determine whether passive rootfs
    reads remain accepted or selected data bytes are materialized
```

### 1.6 `FONTCONFIG_PATH` and `FONTCONFIG_FILE`

```text
semantic purpose:
    select fontconfig configuration from Debian rootfs

candidate semantic owner:
    provider.fonts.glibc

minimum valid scope:
    font/fontconfig consumers

migration condition:
    define font discovery/render gates and decide passive rootfs versus selected
    materialized font/fontconfig data closure
```

### 1.7 `LOCPATH`

```text
semantic purpose:
    expose Debian locale archive/data

candidate semantic owner:
    provider.locale.glibc

migration condition:
    prove runtime/version coupling between active substrate and locale data
```

### 1.8 `LC_ALL=en_US.UTF-8`

```text
semantic purpose:
    force one locale selection

current scope:
    every application sourcing env

minimum valid scope:
    unresolved

candidate owner:
    not assigned yet; likely composition/user policy rather than substrate identity

migration condition:
    determine whether any application requires forced LC_ALL and whether a less
    intrusive LANG/locale availability contract is sufficient
```

### 1.9 `GSETTINGS_BACKEND=memory`

```text
semantic purpose:
    avoid or alter persistent GSettings backend behavior

current scope:
    every application sourcing env

minimum valid scope:
    unresolved GUI-family or specific-domain scope

candidate owner:
    validation pending; application family or specific application

migration condition:
    identify the original failure it prevents and test affected applications
    independently
```

### 1.10 `NO_AT_BRIDGE=1`

```text
semantic purpose:
    disable AT-SPI accessibility bridge behavior

current scope:
    every application sourcing env

minimum valid scope:
    unresolved GUI-family or specific-domain scope

candidate owner:
    application family or specific application after evidence review

migration condition:
    identify real consumer/failure evidence; do not promote as world base policy
    without proof
```

### 1.11 `ELECTRON_DISABLE_SANDBOX=1`

```text
semantic purpose:
    Electron sandbox policy required by current application execution context

actual consumers:
    VS Code
    Obsidian
    other Electron-family applications only where validated

minimum valid scope:
    Electron application family

candidate semantic owner:
    family.electron

migration condition:
    replace global env ownership with deterministic Electron-family composition
```

### 1.12 D-Bus environment clearing

```text
unset DBUS_SESSION_BUS_ADDRESS DBUS_SYSTEM_BUS_ADDRESS
```

```text
semantic purpose:
    prevent inherited bus endpoint selection

current scope:
    every application sourcing env

minimum valid scope:
    unresolved bridge/domain policy

candidate owner:
    bridge.dbus policy if an explicit D-Bus bridge is intended,
    otherwise application-family/domain policy

migration condition:
    characterize actual D-Bus use, endpoint expectations, and failure mode
```

### 1.13 TLS certificate variables

Current bindings:

```text
SSL_CERT_FILE
NODE_EXTRA_CA_CERTS
GIT_SSL_CAINFO
CURL_CA_BUNDLE
REQUESTS_CA_BUNDLE
```

```text
semantic purpose:
    expose Termux CA material to foreign-world consumers

candidate semantic owner:
    provider.tls.glibc plus consumer-specific bindings

important distinction:
    one trust capability is currently represented by several consumer adapters;
    those environment variables are composition outputs, not one world policy
```

Suggested semantic split:

```text
provider.tls.glibc
    CA material identity
    trust capability contract

consumer bindings
    OpenSSL-style
    Node
    Git
    curl
    Python Requests
```

### 1.14 `VK_ICD_FILENAMES` and `VK_DRIVER_FILES`

```text
semantic purpose:
    deterministic selection of the promoted glibc Turnip/Vulkan ICD

actual consumers:
    VS Code ANGLE-Vulkan path
    Obsidian ANGLE-Vulkan path
    Vulkan consumers composed with this provider
    OpenGL/Zink provider transitively

minimum valid scope:
    provider.graphics.vulkan.glibc consumers

candidate semantic owner:
    provider.graphics.vulkan.glibc

migration condition:
    define provider identity, promotion pointer, and actual-selection gates
```

### 1.15 no global `LD_LIBRARY_PATH`

```text
semantic purpose:
    preserve ABI purity and prevent foreign runtime policy from contaminating
    Bionic children

minimum valid scope:
    world invariant / launch boundary

candidate semantic owner:
    world.glibc process-policy contract

status:
    retain the invariant, not necessarily the current file location
```

## 2. `gl-run`

Current behavior:

```text
source ~/gl/env
require selected Vulkan provider variables
set MESA_LOADER_DRIVER_OVERRIDE=zink
clear LD_PRELOAD
exec workload
```

Classification:

```text
semantic purpose:
    OpenGL-through-Zink capability composition

current owner:
    modules/gl

actual consumers:
    explicit GL workloads and documented test commands

minimum valid scope:
    graphics.opengl.glibc through Zink

candidate semantic owner:
    provider.graphics.opengl.glibc

migration/removal condition:
    either compose the same capability semantics directly in application/domain
    launch plans or re-home a narrow provider-specific helper;
    the public command name has no architectural preservation requirement
```

Explicit non-direction:

```text
do not extend gl-run into:
    substrate observer
    dirty-state checker
    sync gateway
    lifecycle manager
    universal glibc launcher
```

## 3. `gl-farm`

Current responsibilities:

```text
rootfs location
scan-directory selection
broad *.so* discovery
libc-family denylist
basename collision policy
symlink materialization
active farm destruction/replacement
contamination check
ldconfig mutation
```

Semantic decomposition:

| Current mechanism | Candidate owner |
|---|---|
| rootfs location/discovery | supply adapter |
| scan directories | supply adapter/materializer policy |
| broad library discovery | research/control mechanism |
| protected libc-family exclusions | world.glibc protected-set contract |
| basename collision policy | materializer policy |
| symlink generation | transitional materializer |
| contamination check | validation gate |
| active in-place replacement | transitional implementation; not accepted target |
| ldconfig mutation | substrate loader-state concern; must be separated from discovery/materialization |

Current classification:

```text
broad farm:
    research compatibility pool
    control/reference mechanism
    dependency discovery aid
    transitional baseline
```

It is not accepted as the permanent production provider object.

Removal/migration condition:

```text
one or more selected-closure pilots prove:
    bounded resolution
    protected world-owned exclusion
    valid app-local locality preservation
    provider-byte materialization
    provenance receipts
    candidate-specific selection proof
    workload equivalence against the broad-farm control
```

## 4. `shims/xdg-open`

Current behavior:

```text
glibc application request
    -> Bionic termux-open
    -> Android intent/default browser path
```

Classification:

```text
semantic purpose:
    cross-world URL opening

minimum valid scope:
    applications requiring URL-open integration

candidate semantic owner:
    bridge.url-open

migration condition:
    document producer/consumer, transport/action, permissions, failure behavior,
    and health check; then re-home or compose explicitly
```

## 5. glibc target toolchain wrappers

Files:

```text
glibc-ar
glibc-exec
glibc-g++
glibc-gcc
glibc-pkg-config
glibc-ranlib
glibc-strip
```

Observed real consumer:

```text
packages/mesa-glibc/build.sh
```

The Mesa build requires the wrappers, runs a compiler/linker/runtime smoke gate,
and writes them into the Meson cross file as target tools and exe wrapper.

Classification:

```text
semantic purpose:
    execute glibc target compiler/binutils/runtime tools from the Bionic host
    without globally contaminating the host process environment

minimum valid scope:
    build/supply workflows targeting world.glibc

candidate semantic owner:
    toolchain.glibc-target

migration condition:
    move ownership only after all build consumers are inventoried and the Mesa
    build path is updated atomically with wrapper locations
```

## 6. Regression gates

### `core-abi.sh`

```text
claim:
    active world.glibc substrate exports __vsyslog_chk@GLIBC_2.17

candidate semantic owner:
    validation gate for world.glibc substrate ABI
```

The test is incident-specific but valuable as a regression contract.

### `farm-libdbus-relocation.sh`

```text
claim:
    active selected/broad-farm libdbus relocates against the active glibc substrate
    without undefined symbols

candidate semantic owner:
    validation gate for substrate/provider compatibility
```

Important qualification:

```text
this test validates active state by default;
future candidate validation must prove the candidate context was selected and
must record actual resolved/mapped provider identity
```

## 7. Shell namespace integration

Current shell fragment:

```text
GL_BIN=$HOME/gl/bin
```

The final shell PATH policy places this namespace before uv-base and `.local/bin`.

Current contents exposed beneath the namespace include semantically different
commands such as:

```text
OpenGL helper
farm research/materialization helper
Obsidian application entrypoints
```

Classification:

```text
$HOME/gl/bin:
    transitional public command namespace facade

not:
    one semantic owner
```

Migration condition:

```text
establish final public-entrypoint ownership and compatibility cost before deciding
whether the namespace remains as a convenience facade or disappears
```

## 8. Application consumers

### VS Code

Current launcher consumes:

```text
~/gl/env composition
URL-open shim PATH
VS Code payload
Vulkan provider selection
Electron-family sandbox behavior
VS Code-specific ANGLE/Vulkan and GPU-vsync flags
```

Proposed ownership:

```text
app.vscode
    payload identity and entrypoint
    vendor CLI behavior
    VS Code-specific flags
    workload gates

family.electron
    only policies proven common to Electron applications

providers/bridges
    X11
    Vulkan
    fonts
    TLS
    URL-open
```

### Obsidian

Current GUI launcher additionally owns valid AppDir-local composition:

```text
APPDIR
AppDir PATH entries
AppDir XDG data
AppDir GSettings schema directory
```

These are application-domain/locality concerns and should remain with
`app.obsidian` unless evidence supports a broader family policy.

## 9. Proposed semantic split

```text
world.glibc
    loader/core substrate contract
    protected world-owned library set
    base process policy
    world ABI/purity gates

provider.shared-libs.glibc
    selected shared provider closure, if pilot validates the object

provider.graphics.vulkan.glibc
    promoted Mesa/Turnip Vulkan provider
    ICD selection
    provider gates

provider.graphics.opengl.glibc
    Zink composition
    OpenGL gates

provider.fonts.glibc
    font/fontconfig capability

provider.locale.glibc
    locale data capability

provider.tls.glibc
    CA trust material plus explicit consumer bindings

provider.shared-data.glibc
    schemas/data only where selected and evidenced

bridge.x11
    endpoint discovery and connectivity contract

bridge.url-open
    current xdg-open -> termux-open integration

toolchain.glibc-target
    compiler/binutils/pkg-config/exe-wrapper boundary

app.vscode
    VS Code domain

app.obsidian
    Obsidian domain

app.pymol
    future architecture proof, not legacy umbrella extension

Debian supply adapter
    package/file provenance
    warehouse observation
    selected artifact acquisition

broad farm
    research/control/reference mechanism
```

## 10. Physical-move decision

No physical semantic hard split is performed by this document.

The next justified steps are:

```text
1. recover or replace the broken substrate and freeze recovery evidence
2. finish substrate-authority evidence and backend contract
3. define and run one bounded selected-closure pilot
4. use pilot evidence to decide which shared-provider objects are real
5. only then move physical ownership and add the minimum lifecycle those objects need
```

The repository tree must follow proven semantic ownership, not the other way around.
