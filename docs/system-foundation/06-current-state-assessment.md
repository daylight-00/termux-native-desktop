# 6. Current-State Assessment

> **Lifecycle:** historical system-foundation provenance. Current constitutional authority is [`../constitution/`](../constitution/README.md); current architecture is [`../architecture/`](../architecture/README.md). Interpret this document in its recorded context; any later status, precedence, or execution-order wording below is historical to that context.

> **Historical assessment:** this document records the pre-immutable-deployment and pre-local-layout-refactor state used to derive the target architecture. It is not a current-state surface. For current state use `docs/current/BRIEF.md`, `docs/architecture.md`, Decision 0004 and `packages/mesa-glibc/README.md`.

This assessment compares the repository’s current documented and promoted model with the target architecture in this set. It is not a criticism of the bottom-up work that created the system. The current design contains several strong architectural discoveries; the goal is to identify which discoveries should be promoted into contracts and where implementation history has accumulated too much responsibility.

## 6.1 Executive assessment

The project is **architecturally viable but under-contractualized**.

The strongest parts already exist:

```text
native host authority
process ABI separation
PRoot excluded from normal execution
explicit dual GPU stacks
X11 as a cross-world bridge
no broad glibc LD_LIBRARY_PATH
experiment/evidence/decision lifecycle
versioned Mesa provider promotion pattern
```

The main structural debt is not lack of understanding. It is that understanding is distributed across:

```text
docs
shell environment
launchers
denylist logic
live path topology
historical experiment reports
```

The next phase should convert those implicit implementation contracts into explicit domain/capability/provider contracts and validation gates.

## 6.2 Strong foundation: repository lifecycle

The repository already separates:

```text
experiments/
    -> investigation and provenance

STATUS.md
    -> current conclusions and open questions

docs/decisions/
    -> durable choices

docs/*.md guides
    -> integrated operational knowledge

setup/ and scripts/
    -> promoted live artifacts
```

This is unusually strong for a fast exploratory project. Preserve it.

Recommended extension:

```text
decision
    -> explicit contract
    -> validator
    -> promoted artifact
```

The missing layer is not another report category; it is **machine- and human-readable runtime contracts plus gates**.

## 6.3 Strong foundation: process ABI world separation

The current architecture explicitly models:

```text
bionic world
    -> native session/apps/libraries

glibc world
    -> patched glibc applications and glibc providers
```

and states that individual processes should remain in one ABI world.

This should be elevated from an architecture description to a project invariant and validated dynamically.

Current evidence of this principle includes:

```text
no global LD_LIBRARY_PATH for glibc world
glibc ICD re-pinning
separate XDG runtime policy
Termux-aware glibc X11/xcb priority
preload clearing at glibc process entry
```

## 6.4 Strong foundation: PRoot has a defined non-runtime role

The project consistently treats PRoot as:

```text
install-time dependency resolver
package/library source
behavioral oracle
debugging control environment
```

while rejecting it as the normal application runtime.

This is a clear architectural boundary and should remain.

However, the runtime documentation should distinguish two levels:

```text
A. no PRoot-mediated process execution
B. no passive runtime file dependency on Debian rootfs
```

The current system clearly achieves A. It does not fully claim or achieve B.

## 6.5 Nuance: passive rootfs runtime dependency

The current shared glibc environment references Debian rootfs locations for:

```text
XDG_DATA_DIRS
FONTCONFIG_PATH
FONTCONFIG_FILE
LOCPATH
```

Therefore the runtime currently uses the rootfs not only as a package oracle/library warehouse but also as a passive data provider.

This is not inherently wrong. The issue is architectural vocabulary.

The current state should be described as:

```text
PRoot execution mediation: absent from normal app runtime
Debian rootfs passive data dependency: present for selected capabilities
```

The target design can later decide whether to keep or materialize those data providers independently.

## 6.6 Structural debt: shared `env` has multiple responsibility classes

The current `setup/glibc/env` combines at least these responsibilities:

### World-base policy

```text
DISPLAY default
XDG_RUNTIME_DIR
TMPDIR
preload/bus cleanup behavior
```

### Passive data provider policy

```text
XDG_DATA_DIRS
fontconfig paths
locale path
```

### Desktop/session compatibility policy

```text
GSettings backend
accessibility bridge setting
```

### Application-family/security policy

```text
Electron sandbox environment
```

### TLS provider policy

```text
SSL_CERT_FILE
NODE_EXTRA_CA_CERTS
GIT_SSL_CAINFO
CURL_CA_BUNDLE
REQUESTS_CA_BUNDLE
```

### GPU provider policy

```text
VK_ICD_FILENAMES
VK_DRIVER_FILES
```

Every setting may have a valid history, but the file is becoming a **composition output disguised as a base environment**.

Recommended interpretation during refactor:

```text
keep current file stable as compatibility facade
    -> document responsibility fragments
    -> extract conceptual modules
    -> migrate consumers gradually
```

Do not split it physically before validation covers the current behavior.

## 6.7 Structural debt: broad farm is a research pool, not a resolved closure

The current `gl-farm` behavior is approximately:

```text
scan broad Debian library directories
    -> link almost all *.so*
    -> exclude libc-family names via denylist
    -> first basename wins
    -> run contamination check
    -> refresh ldconfig cache
```

This is a pragmatic compatibility mechanism. It enabled fast exploration and avoided manual copying.

But long-term issues include:

```text
breadth exceeds proven runtime need
basename collision policy is simple and order-dependent
provenance is indirect
app/provider-specific intent is not represented
new Debian packages can broaden the pool globally
```

Recommended target:

```text
rootfs warehouse
    -> candidate index
    -> manifest-driven selected closure
    -> materialized shared provider store
```

Migration rule: keep the broad farm available until resolved closures prove equivalent or better for validated workloads.

## 6.8 Structural debt: deploy path and repository location coupling

The current deployment script assumes a specific repository path under `$HOME` and creates live symlinks into:

```text
~/gl
~/.local/bin
```

It also distinguishes tracked source from untracked runtime state such as apps, farm, Mesa prefixes, and builds. That conceptual distinction is good.

The remaining issue is that source topology and live runtime topology are tightly coupled through direct symlinks and fixed paths.

Risks as the project grows:

```text
repo relocation is harder
generated runtime and source ownership can blur
promotion semantics differ by component
live edits can immediately affect runtime
parallel refactor can change source under live links
```

Recommended target:

```text
source-of-truth
    -> explicit deploy/materialize transaction
    -> versioned or staged candidate
    -> validate
    -> promote stable runtime pointer
```

Not every small script needs copying/versioning, but provider/application payloads should not rely on incidental repository placement.

## 6.9 Structural debt: app launchers own too much knowledge

The VS Code launcher currently composes:

```text
glibc base environment
shim PATH
application location
GPU enable/disable policy
ANGLE Vulkan flags
VS Code-specific GPU-vsync workaround
SHELL integration
shared-memory workaround
X11/Ozone selection
```

This is understandable for the first complex app. As more Electron apps arrive, copying launchers would create divergence.

Target decomposition:

```text
world.glibc.base
provider/bridge fragments
family.electron policy
app.vscode policy
```

The current launcher should remain the behavioral baseline until equivalent composed launch behavior is validated.

## 6.10 Strong foundation: `gl-run` is already capability-scoped

`gl-run` is a good example of narrow scope:

```text
source glibc environment
verify glibc Mesa provider exists
add Zink override only for OpenGL consumers
exec target
```

It explicitly states that Vulkan-native applications do not need this override.

This is close to the capability-provider model:

```text
graphics.opengl/glibc policy
    -> compose Zink over selected Vulkan provider
```

The future architecture should generalize this pattern without unnecessarily abstracting the simple wrapper.

## 6.11 Strong foundation: Mesa versioned provider promotion

The GPU documentation uses:

```text
versioned install prefixes
    -> validate
    -> stable mesa-glibc symlink promotion
```

and explicitly values A/B comparison and rollback.

This is one of the best patterns in the current system and should become a general provider lifecycle template.

## 6.12 Structural debt: validation is documented but not yet systematic

The repository has strong evidence discipline and explicit statements that passing screenshots do not prove stronger hidden-path claims.

Current focus also recognizes the need for repeatable validation gates.

The gap is execution:

```text
documented working conclusion
    -> not always backed by one repeatable named gate
```

Recommended next layer:

```text
validate/world-purity
validate/x11
validate/vulkan-glibc
validate/zink-glibc
validate/vscode-gpu
validate/conda-native-extension
```

Each should produce evidence artifacts suitable for experiment comparison.

## 6.13 Structural debt: current architecture mixes plane vocabulary

The current workstream model is historically clear:

```text
desktop/session
glibc layer
GPU
```

But for future design it causes cross-cutting concerns:

```text
GPU exists in both ABI worlds
session owns host lifecycle but not all app runtime
fonts/TLS/locale live inside glibc env without explicit provider category
PRoot is neither runtime world nor simple library directory
```

The six-plane model does not need to replace the current user-facing architecture document immediately. It provides a higher-order vocabulary for refactoring.

## 6.14 Current-state mapping to target objects

| Current artifact/concept | Target interpretation |
|---|---|
| `setup/glibc/env` | compatibility facade composing world + providers + policies |
| `gl-farm` | broad research candidate pool/materializer |
| `gl-run` | OpenGL capability composition wrapper |
| `code` launcher | application domain launcher with mixed policy ownership |
| Debian rootfs | supply oracle + warehouse + current passive data provider |
| `mesa-glibc` symlink | promoted provider pointer |
| `startxfce-x11` | host session lifecycle implementation |
| `experiments/` | discovery/evidence plane |
| `STATUS.md` | working conclusion registry |
| `docs/decisions/` | durable rationale plane |

## 6.15 Current risk if bottom-up expansion continues unchanged

Without contract extraction, likely evolution is:

```text
new app fails
    -> add global env setting

another app breaks
    -> launcher-specific unset

new dependency missing
    -> broaden farm/rootfs package set

provider conflict
    -> add denylist special case

new Electron app
    -> copy launcher and diverge flags
```

Each local fix can be correct. The systemic risk is invisible coupling.

## 6.16 Current opportunity

The project is at a favorable transition point because:

```text
several real applications already work
world boundaries are understood
GPU paths are validated
session source is tracked
evidence culture exists
PyMOL is not yet entangled in legacy onboarding
```

PyMOL can become the first major workload onboarded against explicit domain/capability contracts rather than copied historical procedure.

## 6.17 Assessment conclusion

The current project should not be “rewritten.” It should be **stratified**.

Preserve:

```text
working runtime behavior
experiment history
operational guides
proven provider paths
```

Extract from them:

```text
invariants
world contracts
capability contracts
application contracts
validation gates
promotion rules
```

Then migrate implementation behind those contracts gradually.

## Project references

- [`../architecture.md`](../architecture.md)
- [`../glibc-layer.md`](../glibc-layer.md)
- [`../desktop-session.md`](../desktop-session.md)
- [`../gpu.md`](../gpu.md)
- [`../../STATUS.md`](../../STATUS.md)
- [`../../modules/gl/overlay/home/gl/env`](../../modules/gl/overlay/home/gl/env)
- [`../../modules/gl/overlay/home/gl/bin/gl-farm`](../../modules/gl/overlay/home/gl/bin/gl-farm)
- [`../../modules/gl/overlay/home/gl/bin/gl-run`](../../modules/gl/overlay/home/gl/bin/gl-run)
- [`../../packages/vscode/README.md`](../../packages/vscode/README.md)
- [`../../tools/deploy`](../../tools/deploy)
