# 11. Architecture Reassessment and Hard-Refactor Decision

> **Lifecycle:** historical system-foundation provenance. Current constitutional authority is [`../constitution/`](../constitution/README.md); current architecture is [`../architecture/`](../architecture/README.md). Interpret this document in its recorded context; any later status, precedence, or execution-order wording below is historical to that context.

> **Date:** 2026-07-10
> **Recorded status at authoring:** active architectural direction
> **Scope:** reconciles the system-foundation model with the concurrent `refactor/module-package-layout` work and the post-refactor glibc/libdbus ABI incident.

## 11.1 Why this reassessment exists

The project was discovered bottom-up, then deliberately re-examined top-down. That transition creates a specific risk: an implementation object that was useful during discovery can become structurally privileged merely because later work is built around it.

Examples include:

```text
one OpenGL launch helper
    -> becomes generic runtime gateway

one broad library farm
    -> becomes permanent production provider model

one shared environment file
    -> becomes architecture by accumulation

one package-manager hook
    -> becomes lifecycle authority
```

The purpose of this document is to prevent that path dependence.

The governing principle is:

> **Preserve validated semantics, evidence, and rollback paths. Do not preserve command names, compatibility facades, directory identities, or transitional runtime objects merely because they already exist.**

This strengthens the earlier migration language in `06-current-state-assessment.md`, `07-gap-analysis-and-refactoring-strategy.md`, and `08-implementation-roadmap.md`. Where those documents can be read as preferring preservation of current facades by default, this document takes precedence: preservation is a tactic, not an invariant.

## 11.2 Evidence considered

This reassessment combines four evidence sets.

### System-foundation model

The project is defined as a heterogeneous userspace composition system built from:

```text
World
Application Domain
Capability
Provider
Bridge
Artifact Source
Validation Gate
```

See:

- `01-essence.md`
- `02-principles-and-invariants.md`
- `03-system-model-v2.md`
- `04-domain-capability-bridge-model.md`
- `05-ideal-target-architecture.md`

### Repository ownership refactor

The branch `refactor/module-package-layout` correctly separated:

```text
modules/
    project-authored system capability/integration ownership

packages/
    external payload lifecycle ownership

experiments/
    investigation, evidence, and provenance

tools/
    repository/operator workflow
```

This ownership refactor is retained.

### Actual refactored `gl` object

The refactored `modules/gl` still groups:

```text
world substrate policy
shared-library materialization
OpenGL/Zink launch policy
URL-open bridge integration
glibc target toolchain wrappers
```

That grouping is useful as a transitional deployment namespace, but it is not one coherent final semantic object.

### ABI incident

The post-refactor VS Code failure was reduced to an independent core/provider ABI mismatch:

```text
Debian-derived libdbus
    requires __vsyslog_chk@GLIBC_2.17

current Termux glibc core
    does not export that symbol
```

The failure reproduces without VS Code through relocation testing. This proves that substrate and provider compatibility is a first-class contract and that rebuilding a farm cannot repair a broken substrate ABI.

See the refactor branch documents:

- `docs/refactor/0012-post-refactor-vscode-libdbus-abi-regression.md`
- `docs/refactor/0013-vscode-libdbus-root-cause-confirmed.md`
- `docs/refactor/0014-robust-gl-update-and-farm-lifecycle.md`

## 11.3 Executive decision

After incident recovery and regression-gate capture, pause implementation of the `0014` lifecycle plan in its current form.

Do not yet implement:

```text
pacman hooks as lifecycle architecture
gl-run auto-sync
generational broad-farm activation
single global compatibility fingerprint
current/previous farm as complete rollback model
```

First:

```text
reconcile foundation and refactor models
    -> hard-split semantic responsibilities
    -> decide glibc substrate authority
    -> pilot a selected provider closure
    -> then implement the smallest lifecycle required by the corrected objects
```

## 11.4 The directory refactor is retained

The ownership refactor corrected real mistakes and should not be rolled back.

The following conceptual moves are sound:

```text
VS Code launcher
    -> VS Code package owner

Obsidian launchers
    -> Obsidian package owner

Mesa build lifecycle
    -> Mesa package owner

Mesa bisect judges
    -> experiment recipe

deployment workflow
    -> repository tool

shell behavior
    -> shell owner

uv-base definition
    -> uv-base owner
```

The remaining work is not to undo those moves. It is to continue from source ownership into runtime semantic ownership.

## 11.5 Why `modules/gl` is not a valid final semantic object

The current `modules/gl` groups responsibilities that belong to different object classes.

### Shared environment

The current environment composes:

```text
world runtime-directory policy
DISPLAY default
passive rootfs data paths
font provider policy
locale provider policy
GSettings/accessibility policy
Electron sandbox policy
D-Bus clearing policy
TLS trust policy
Vulkan provider selection
```

This is a composition result, not one base object.

### `gl-run`

The current helper is narrow:

```text
source glibc environment
verify selected Mesa/Vulkan provider
set Zink override
exec target
```

Its semantic meaning is close to:

```text
provider.graphics.opengl.glibc
```

It is not a world lifecycle manager.

### `gl-farm`

The current farm combines:

```text
warehouse scanning
selection by broad directory scan
libc-family protection denylist
basename collision policy
symlink materialization
active mutation
loader-cache mutation
```

This is a transitional compatibility mechanism. It is not yet a proven final provider architecture.

### URL shim

The URL-opening shim is naturally:

```text
bridge.url-open
```

### Toolchain wrappers

The compiler/binutils wrappers are naturally:

```text
toolchain.glibc-target
```

### Decision

`modules/gl` may remain temporarily as a physical deployment grouping, but it must not become the owner of all future:

```text
state
fingerprints
provider generation
validation framework
activation
rollback
package-manager hooks
application readiness
```

## 11.6 `gl-run`: do not extend it

A narrow OpenGL/Zink helper must not grow into:

```text
identity observer
    + dirty-state checker
    + sync gateway
    + provider lifecycle manager
    + validation orchestrator
    + universal app launcher
```

That would turn an early helper into a structural center merely through historical accident.

Decision:

```text
Option A: delete gl-run and compose capabilities in application launch plans

or

Option B: retain/re-home only its narrow OpenGL/Zink capability semantics
```

Backward compatibility with the `gl-run` command is not an architectural invariant.

## 11.7 The broad farm is a transitional research object

The ideal target already distinguishes:

```text
Debian rootfs warehouse
    -> candidate artifact index
    -> resolver/selection
    -> selected shared provider closure
    -> provenance manifest
    -> materialized runtime store
```

from:

```text
broad farm
    -> research/compatibility pool
```

The broad farm was valuable because it accelerated discovery. It should remain available as a control, fallback, or research mechanism while replacement paths are validated.

However, do not first invest in making the broad farm the permanent transactional production unit.

A likely target is hybrid:

```text
world substrate
    coherent glibc loader/core and protected Android-sensitive libraries

shared validated providers
    intentionally selected common libraries

application-local closure
    upstream-local libraries preserved where required

supplemental application/provider closure
    selected Debian-derived artifacts materialized from provenance-aware inputs
```

## 11.8 Symlink generations are not automatically immutable

A generation directory can contain symlinks into a mutable Debian rootfs:

```text
generation-A/lib/libdbus-1.so.3
    -> rootfs/usr/lib/.../libdbus-1.so.3.38.3
```

If apt/dpkg later replaces or removes that target, the generation directory may still exist while its effective content changes or disappears.

Therefore:

```text
immutable generation path
    !=
immutable generation bytes
```

True rollback requires one of:

```text
A. generation-owned provider bytes
B. content-addressed provider storage
C. exact preserved package artifacts plus deterministic reconstruction
```

For this project, selected-closure materialization of actual provider bytes is a strong candidate because it gives real identity and rollback without copying the entire broad warehouse.

## 11.9 Substrate and provider closure are independent lifecycle axes

The ABI incident shows:

```text
world substrate
    <- compatibility contract ->
provider closure
```

A provider rebuild cannot repair a missing symbol in the substrate.

The lifecycle model must distinguish states such as:

```text
READY

DIRTY_INPUT
    materialization input changed

BLOCKED_SUBSTRATE
    core/world substrate violates contract

CANDIDATE_FAILED
    provider candidate fails compatibility or workload gates

NEEDS_REVALIDATION
    bytes unchanged but validation/workload contract changed
```

Provider rollback and substrate rollback are different operations.

```text
provider rollback
    !=
substrate rollback
```

Keeping a previous farm does not restore a previous glibc core after the package manager has replaced it.

## 11.10 Separate causal identities instead of one dirty fingerprint

A single combined compatibility fingerprint makes different causes trigger the same action.

Prefer separate identities.

### Substrate identity

```text
loader identity
core runtime file identity
protected world-owned libraries
explicit ABI contract gates
```

### Provider-input identity

Track the actual inputs used to materialize selected providers.

For a transitional farm observer:

```text
selected pathname
resolved target
content hash or Build ID
package owner/version as provenance when useful
```

### Materializer identity

```text
selection rules
protected/core rules
collision policy
materializer source identity
```

### Validation-policy identity

```text
gate definitions
regression set
world-purity classifier policy
```

### Workload-contract identity

```text
registered application entrypoints
application gates
capability expectations
```

Then actions can be targeted:

```text
materialization input changed
    -> rebuild candidate

only validation policy changed
    -> revalidate current materialization

only workload contract changed
    -> run new domain gates

nothing changed
    -> no action
```

## 11.11 Candidate validation must prove candidate selection

A candidate validation test is invalid if loader configuration silently selects the active provider instead.

The invariant is:

> **Evidence must identify the actual provider objects used by the candidate validation process.**

Candidate gates must therefore prove:

```text
candidate path/context selected
actual loaded object identity captured
active loader state did not silently substitute the old provider
```

Possible mechanisms can be tested later:

```text
candidate-specific search context
candidate-specific loader configuration/cache
explicit search plan for validation process
```

The architecture requires proof of selection, not one predetermined mechanism.

## 11.12 Pacman: separate supply authority from event convenience

The architectural question is not whether pacman is good or bad.

The question is:

> **What authority does the package manager have in the desired system?**

The external `termux-pacman/glibc-packages` project produces pacman-format glibc packages and repository metadata. The current project documentation, however, also contains historical bootstrap commands using `pkg install ...`. The current refactor documents do not by themselves prove which package database is authoritative for the live device substrate.

Therefore the actual device authority must be captured before architecture is coupled to pacman.

### Rejected use

Do not install or switch a package manager merely to obtain:

```text
PostTransaction dirty marker
```

A hook is an optimization hint, not a correctness mechanism.

### Accepted use

If pacman already is or is deliberately selected as the narrow authoritative glibc substrate backend, it may own:

```text
package acquisition
package identity/version observation
update transaction
exact package artifact/cache access
optional change-event hint
```

It must not own:

```text
provider compatibility
world purity
application closure
capability validation
promotion decision
```

## 11.13 Backend-neutral substrate authority model

Use the following architecture:

```text
world.glibc
    |
    +-- substrate source adapter
            observe identity
            update when explicitly requested/policy allows
            retrieve exact artifact when supported
```

Possible implementations:

```text
pacman adapter
another existing package backend adapter
verified exact-artifact adapter
project build adapter, only if justified
```

The architecture remains backend-neutral.

### Model A: rolling package-manager substrate

Useful when a package manager already authoritatively owns the substrate and reuse is cheaper than replacement.

### Model B: backend-neutral package-manager supply adapter

Recommended near-term architectural model. The control plane consumes observed identity and available artifacts without hard-coding one package manager.

### Model C: project-pinned exact substrate artifacts

Consider when reproducibility and real pre-activation validation outweigh package-manager lifecycle reuse.

### Model D: project-built substrate

Use only if evidence justifies owning the build and maintenance burden. One upstream packaging defect alone is not enough reason to duplicate the full packaging project.

## 11.14 Event hooks versus observed identity

A hook can report:

```text
something probably changed
```

It cannot prove:

```text
current runtime composition is valid
```

Therefore:

```text
hook / dirty marker
    -> optional optimization hint

observed actual substrate/provider identity
    compared with active receipt
    -> correctness authority
```

This also catches direct/manual mutations that bypass package hooks.

## 11.15 Correct semantic objects

The umbrella model should be replaced conceptually by:

```text
world.glibc
    loader/core substrate contract
    protected world-owned libraries
    base process policy
    world-purity gates

provider.shared-libs.glibc
provider.graphics.vulkan.glibc
provider.graphics.opengl.glibc
provider.fonts.glibc
provider.locale.glibc
provider.tls.glibc

bridge.x11
bridge.url-open

toolchain.glibc-target

app.vscode
app.obsidian
app.pymol
```

The live `$HOME/gl` namespace may remain. A live path namespace is not the same thing as one semantic owner.

## 11.16 Hard-refactor boundary

### Preserve

```text
experiment evidence
ABI incident documents
application/package ownership separation
Mesa package ownership
shell and uv-base decomposition
deployment safety tests
application payloads
validated provider builds
workload baselines
```

### May be replaced or deleted

```text
modules/gl as semantic umbrella
monolithic ~/gl/env contract
gl-run public API
gl-farm as production architecture
pacman-hook dependency
single global compatibility fingerprint
```

### Transitional use is allowed

```text
broad farm
current environment
current launchers
```

only as controlled baselines until equivalent target contracts pass gates.

A compatibility facade should have:

```text
owner
purpose
consumers
removal condition
latest removal milestone
```

Otherwise it tends to become permanent through accidental dependency.

## 11.17 Correction to the earlier strangler-style migration language

The earlier migration strategy intentionally emphasized gradual transition. That remains useful when the old object is expensive to replace safely.

The stronger rule is now:

```text
preserve validated semantics
preserve evidence
preserve rollback path

but

do not preserve accidental object identity by default
```

A facade is justified only when:

```text
facade cost
    <
coordinated replacement cost
```

Internal experimental helpers have no compatibility guarantee unless a real consumer contract justifies one.

## 11.18 Minimal control-plane design

Do not begin by building a large `gl-sync` framework.

Start with a minimal semantic flow:

```text
observe substrate identity
observe provider materialization inputs
read active receipt

if unchanged:
    no-op

if substrate changed:
    run substrate gates
    failure -> BLOCKED_SUBSTRATE

if provider inputs/materializer changed:
    materialize candidate selected closure

validate candidate in candidate-specific context
run registered capability/domain gates

pass:
    promote provider candidate
    record receipt

fail:
    leave previous promoted provider untouched
```

Correctness does not require package hooks, a universal `gl-run`, or a project-wide package manager.

## 11.19 Recommended physical direction

The semantic model comes first. One possible repository shape is:

```text
worlds/
└── glibc/
    ├── contract.md
    ├── substrate/
    ├── policy/
    └── tests/

providers/
├── shared-libs-glibc/
├── mesa-glibc/
├── opengl-zink-glibc/
├── fonts-glibc/
├── locale-glibc/
└── tls-glibc/

bridges/
├── x11/
└── url-open/

toolchains/
└── glibc-target/

packages/ or apps/
├── vscode/
├── obsidian/
└── pymol/
```

A lower-disruption physical layout can retain `modules/` while splitting semantic owners. The path choice is secondary to responsibility separation.

## 11.20 Recommended sequencing

### Stage 0: recover and freeze the incident evidence

Do now:

```text
repair or replace broken glibc substrate
keep core ABI regression gate
keep libdbus relocation regression gate
prove VS Code workload recovery
preserve evidence
```

Do not yet:

```text
install/switch pacman for hooks
add gl-run auto-sync
build generational broad-farm store
claim previous farm is full world rollback
```

### Stage 1: reconcile foundation and refactor work

The refactor branch and foundation documents were created on diverged histories. Before further architecture-changing implementation:

```text
bring both models into one review context
record superseded assumptions
make document precedence explicit
```

### Stage 2: semantic hard refactor of `gl`

Inventory every file and environment variable currently owned by the `gl` umbrella and assign it to:

```text
world
provider
bridge
toolchain
application family
specific application
validation only
```

Then split ownership.

### Stage 3: settle substrate authority

Capture actual device facts:

```text
who owns installed $PREFIX/glibc files
which package database records them
how glibc is updated today
whether exact previous artifacts can be retrieved
which install/config semantics direct extraction would lose
```

Then choose the backend implementation of the neutral substrate adapter.

### Stage 4: selected shared-provider closure pilot

Keep the broad farm as a control/reference while one bounded target is materialized through:

```text
static ELF closure
    -> world-owned protected library exclusion
    -> app-local locality preservation
    -> dynamic runtime evidence enrichment
    -> selected provider-byte materialization
    -> provenance receipt
    -> candidate validation
```

Only after the pilot should the project decide how much broad farm remains in the promoted runtime.

### Stage 5: implement only the minimum lifecycle

After object boundaries are correct, implement:

```text
observe
receipt
candidate materialize
candidate validate
promote
rollback
```

Event hooks remain optional.

### Stage 6: use PyMOL as architectural proof

PyMOL should test whether the architecture composes existing contracts:

```text
world.glibc
python.runtime provider
display.x11 bridge/provider
graphics.opengl provider
fonts provider
native-extension ABI contract
```

If onboarding requires copying old launchers, adding more global environment state, or adding app-specific farm exceptions, the hard refactor is incomplete.

## 11.21 Decision table

| Subject | Decision |
|---|---|
| ownership directory refactor | keep and continue |
| `modules/` / `packages/` distinction | keep as useful source-ownership taxonomy |
| `modules/gl` as final semantic object | reject |
| monolithic `~/gl/env` | decompose |
| `gl-run` | do not extend; delete or re-home narrow OpenGL semantics |
| broad `gl-farm` | transitional research/compatibility mechanism |
| candidate -> validate -> promote principle | keep |
| `0014` implementation plan as written | pause and supersede/revise |
| install/switch pacman for hook convenience | reject |
| pacman as selected narrow substrate backend | acceptable after real authority is established |
| architecture coupled to pacman | reject |
| hard refactor now | recommended |
| PyMOL on existing umbrella architecture | postpone |
| PyMOL as new-architecture proof | strongly recommended |

## 11.22 Final principle

The immediate design question is not:

```text
How do we make gl-farm safer?
```

It is:

```text
Do we want gl-farm to remain a production object at all?
```

Likewise, the pacman question is not:

```text
Can a hook detect updates?
```

It is:

```text
Who owns glibc substrate supply authority,
and what is the smallest mechanism that preserves identity, validation, and rollback requirements?
```

Once the semantic boundaries are correct, package-manager choice, event hooks, command names, and path layout become implementation decisions instead of architecture.

## Project references

- [`01-essence.md`](01-essence.md)
- [`02-principles-and-invariants.md`](02-principles-and-invariants.md)
- [`03-system-model-v2.md`](03-system-model-v2.md)
- [`04-domain-capability-bridge-model.md`](04-domain-capability-bridge-model.md)
- [`05-ideal-target-architecture.md`](05-ideal-target-architecture.md)
- [`06-current-state-assessment.md`](06-current-state-assessment.md)
- [`07-gap-analysis-and-refactoring-strategy.md`](07-gap-analysis-and-refactoring-strategy.md)
- [`08-implementation-roadmap.md`](08-implementation-roadmap.md)
- [`09-validation-promotion-and-evidence.md`](09-validation-promotion-and-evidence.md)
- [`10-open-design-questions.md`](10-open-design-questions.md)
- refactor branch: `refactor/module-package-layout`
- refactor review point: `0f3b218` (`docs: design robust gl update and farm lifecycle`)
