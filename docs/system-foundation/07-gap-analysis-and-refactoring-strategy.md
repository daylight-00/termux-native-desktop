# 7. Gap Analysis and Refactoring Strategy

> **Lifecycle:** historical system-foundation provenance. Current constitutional authority is [`../constitution/`](../constitution/README.md); current architecture is [`../architecture/`](../architecture/README.md). Interpret this document in its recorded context; any later status, precedence, or execution-order wording below is historical to that context.

The project is being actively refactored. The safest architectural strategy is therefore not a large rename/rewrite, but a sequence that first **freezes semantics, makes contracts visible, adds gates, and then moves implementation behind those contracts**.

This document uses a strangler-style migration: old working paths remain the baseline while new structure takes responsibility gradually.

## 7.1 Gap matrix

| Area | Current strength | Gap | Target |
|---|---|---|---|
| ABI worlds | clearly understood | mostly policy/document enforced | named world contracts + dynamic purity gate |
| Environment | working shared env | mixed responsibility scope | composable world/provider/family/app policy |
| Library pool | broad compatibility farm | not resolved/proven closure | warehouse index + manifest-selected closure |
| Application onboarding | documented procedure | not declarative/reusable | application-domain contracts |
| GPU providers | strong versioned pattern | provider metadata implicit | general provider manifest + gate/promotion model |
| Bridges | X11 and shims work | bridge contracts scattered | bridge registry and health checks |
| Runtime data | rootfs paths work | passive dependency implicit | explicit data-provider capability, optional materialization |
| Deployment | source/live links simple | fixed path and immediate coupling | staged materialization + reversible promotion where needed |
| Validation | evidence culture strong | gates not uniformly executable | named repeatable validators |

## 7.2 Refactoring rule 1: preserve validated behavior before changing structure

Before moving files or splitting environments, record the current behavior of:

```text
native desktop session
VS Code CPU/basic GUI
VS Code GPU path
Obsidian startup
Conda environment creation
compiled NumPy workload
glibc Vulkan device selection
glibc Zink OpenGL renderer
```

For each baseline:

```text
command/action
expected output or evidence
binary/provider identity
known required environment
failure signature
```

This becomes the regression baseline.

## 7.3 Refactoring rule 2: add contracts before abstractions

Do not immediately create a framework.

First create human-readable contract records:

```text
world.glibc
capability.display.x11.glibc
capability.graphics.vulkan.glibc
capability.graphics.opengl.glibc
app.vscode
app.obsidian
```

Only after repeated use should these become machine-readable manifests.

This avoids encoding the wrong schema too early.

## 7.4 Refactoring rule 3: convert current files into compatibility facades

Examples:

### `setup/glibc/env`

Current role:

```text
all-in-one launch environment
```

Migration role:

```text
compatibility facade
    -> internally source/combine responsibility fragments over time
    -> external callers continue sourcing same path during migration
```

### `gl-farm`

Current role:

```text
runtime library pool
```

Migration role:

```text
research compatibility pool
    -> new resolved-closure path introduced alongside it
    -> apps move only after gates pass
```

### app launchers

Current role:

```text
full launch policy
```

Migration role:

```text
thin compatibility entrypoint
    -> call composer or source structured fragments
    -> preserve CLI semantics
```

## 7.5 Refactoring rule 4: do not combine cleanup with behavior change

Bad change:

```text
rename directories
split env
change Mesa version
change font provider
rewrite launcher
```

in one commit.

Better sequence:

```text
1. add baseline gate;
2. move responsibility without changing behavior;
3. prove equivalence;
4. change provider/behavior separately;
5. prove new claim.
```

This keeps bisectability and evidence value.

## 7.6 Phase A: semantic inventory

Create a matrix of all current environment and launcher behavior.

For each setting:

```text
name
current owner file
semantic purpose
scope that actually needs it
known evidence
consumers
candidate future owner
```

Example:

```text
VK_DRIVER_FILES
current: glibc/env
purpose: select glibc Vulkan provider
scope: glibc Vulkan consumers/provider capability
future owner: provider.graphics.vulkan.glibc
```

Example:

```text
ELECTRON_DISABLE_SANDBOX
current: glibc/env
purpose: Electron sandbox compatibility
scope: Electron-family apps, pending verification
future owner: family.electron
```

The word “pending verification” matters: do not move based only on intuition; run A/B tests.

## 7.7 Phase B: baseline validators

Start with cheap, high-value gates.

### World purity

```text
launch app
capture /proc/<pid>/maps and children as needed
classify known forbidden cross-world mappings
fail on contamination
```

### X11

```text
launch minimal glibc X client
confirm connection and expected transport/provider
```

### Vulkan

```text
confirm selected ICD path
enumerate physical device
record driver/device identity
```

### Zink

```text
run glxinfo -B under gl-run
assert renderer path matches expected evidence
```

### VS Code GPU

```text
launch controlled workspace
capture GPU diagnostics
verify GPU child stability over defined action sequence
```

## 7.8 Phase C: conceptual environment decomposition

Before physical split, document fragments:

```text
world/glibc-base
provider/x11-client-glibc
provider/fonts-current
provider/locale-current
provider/tls-termux-ca
provider/vulkan-glibc-current
family/electron
app/vscode
```

Then map each current variable to exactly one owner where possible.

If a variable appears to have two owners, that is a design question to resolve before implementation.

## 7.9 Phase D: physical environment decomposition behind stable entrypoints

Keep:

```text
~/gl/env
```

as a stable compatibility entrypoint initially.

Internally it can become:

```sh
source world/glibc-base.env
source providers/data-defaults.env
source providers/tls.env
source providers/vulkan-glibc.env
```

But do not source Electron policy there.

Migrate one application family at a time, validating before and after.

## 7.10 Phase E: rootfs passive-data dependency decision

Current data categories:

```text
fonts/fontconfig
XDG shared data
locale
possibly schemas/resources used by apps
```

For each:

```text
Is the rootfs path actually required?
Which files are read at runtime?
Can a selected closure be materialized?
Is the data version-coupled to libraries?
What is the update source?
```

Do not extract all `/usr/share` blindly. Build per-capability data closures based on observation and package provenance.

## 7.11 Phase F: library closure migration

Do not replace `gl-farm` in one step.

Introduce:

```text
farm mode: broad research compatibility pool
resolved mode: manifest-selected closure
```

Start with one application or provider whose dynamic closure is well understood.

Suggested first candidates:

```text
small diagnostic tools
well-bounded provider
one stable app before VS Code
```

Only migrate VS Code after the resolver/materializer has proven itself.

## 7.12 Phase G: application contracts

Create application contracts without changing launch behavior.

For VS Code, capture:

```text
source identity
world
entrypoint
local library policy
required capabilities
shim requirements
Electron family policy
VS Code-specific GPU policy
validation gates
```

Then make the existing launcher demonstrably correspond to the contract.

The first goal is explanatory equivalence, not generation.

## 7.13 Phase H: launcher composition

After two or three applications show stable repeated patterns, implement composition.

Potential stages:

```text
v1: shell fragments sourced manually
v2: manifest parser outputs env/argv plan
v3: doctor validates plan before exec
```

Avoid building a general resolver before real contracts expose the necessary semantics.

## 7.14 Phase I: staged deployment and promotion

Move from:

```text
repo path -> live symlink immediately
```

where appropriate to:

```text
repo/source
    -> deploy candidate/stage
    -> validate
    -> promote stable pointer
```

Not every shell script needs versioned promotion. Apply this to components where rollback matters:

```text
Mesa/provider prefixes
application payload transforms
resolved shared closures
critical generated configuration
```

## 7.15 Coexistence with active refactoring session

Because another session may currently change repository structure:

### Safe documentation work

```text
define semantics
record current behavior
create invariants
write target contracts
add validators that observe without mutating
```

### High-conflict work to postpone until tree stabilizes

```text
mass directory renames
changing live symlink topology
replacing deploy mechanism
moving every setup artifact
rewriting launchers simultaneously
```

The architecture should guide the refactor, not race it.

## 7.16 Migration success criteria

The refactor succeeds when:

```text
existing apps still pass baseline gates;
current workarounds have explicit owners/scopes;
new PyMOL onboarding uses reusable capability contracts;
provider changes are versioned and reversible;
rootfs runtime dependencies are visible and intentional;
world contamination is automatically detected;
new dependencies enter runtime through provenance-aware materialization;
```

not when the directory tree merely looks cleaner.

## 7.17 Anti-patterns to avoid

### Premature framework

Building a complex manifest engine before contracts stabilize.

### Big-bang farm removal

Breaking working apps before resolved closures are validated.

### Global environment relapse

Moving variables between files without reducing scope.

### Documentation drift

Writing target architecture as if it were current implementation.

### Success by startup only

Treating window appearance as full capability validation.

### Cleanup that destroys provenance

Deleting failed experiments that define important boundaries.

## 7.18 Recommended immediate next move

The highest-value next step is:

```text
1. create semantic inventory of current env/launchers;
2. write world/capability/app contracts in Markdown;
3. implement world-purity + X11 + Vulkan + Zink baseline gates;
4. only then split current environment responsibilities.
```

This produces architectural leverage without destabilizing active refactoring.

## Project references

- [`../architecture.md`](../architecture.md)
- [`../glibc-layer.md`](../glibc-layer.md)
- [`../desktop-session.md`](../desktop-session.md)
- [`../gpu.md`](../gpu.md)
- [`../../STATUS.md`](../../STATUS.md)
