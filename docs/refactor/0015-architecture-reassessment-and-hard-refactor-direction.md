# 0015 — Architecture Reassessment and Hard-Refactor Direction

## Status

This document changes the implementation direction after reviewing:

```text
main: docs/system-foundation/*
refactor branch: docs/refactor/0001-0014
actual refactored repository objects
post-refactor glibc/libdbus ABI incident
```

The detailed architectural rationale is recorded on `main` in:

```text
docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
```

This document records the branch-specific consequence.

## Executive decision

`0014-robust-gl-update-and-farm-lifecycle.md` is **partially superseded**.

Keep its principles:

```text
candidate before active mutation
pre-activation validation
identity capture and receipts
layered gates
reversible promotion where real rollback exists
separation of generation from orchestration
```

Pause its concrete implementation plan:

```text
pacman PostTransaction hook integration
gl-run auto-sync
single global compatibility fingerprint
generational broad-farm store as production target
current/previous farm as complete rollback model
large gl-sync lifecycle framework
```

The next architecture-changing work must first correct semantic object boundaries.

## Why direction changed

The previous lifecycle design assumed that existing objects should be made safer:

```text
gl-run
gl-farm
~/gl/env
modules/gl
```

The later top-down review asks a more fundamental question:

```text
Are these correct final objects?
```

The answer is: not all of them.

The repository ownership refactor remains valid, but `modules/gl` is still a semantic umbrella containing several different object classes.

Current responsibilities include:

```text
world.glibc substrate/base policy
shared-library provider materialization
OpenGL/Zink capability composition
Vulkan provider selection
fonts/locale/TLS data policy
URL-open bridge integration
glibc target toolchain integration
```

Adding fingerprints, state, activation, rollback, package-manager hooks, and application readiness to this same object would deepen the wrong boundary.

## Ownership refactor result remains accepted

Do not roll back the successful source-ownership migration.

Retain:

```text
application launchers -> package owners
Mesa build lifecycle -> packages/mesa-glibc
experiment judges -> experiment recipes
deployment workflow -> tools/
shell behavior -> shell module
uv-base definition -> uv-base module
```

The next step is semantic decomposition on top of this ownership improvement.

## `gl-run` decision

Current `gl-run` is narrow:

```text
source glibc environment
check glibc Mesa provider
set Zink OpenGL override
exec workload
```

Do not extend it into:

```text
state observer
sync gateway
provider lifecycle manager
validation orchestrator
universal glibc app launcher
```

Allowed outcomes:

```text
A. delete gl-run and compose required capabilities directly

B. retain/re-home only its narrow OpenGL/Zink capability semantics
```

The command name has no compatibility guarantee by default.

## Broad farm decision

The current broad farm remains useful as:

```text
research compatibility pool
control/reference mechanism
dependency discovery aid
transitional baseline
```

It is not accepted as the final production provider architecture.

Before building a sophisticated generation system around it, run a selected shared-provider closure pilot.

Target hypothesis:

```text
world substrate
    coherent glibc loader/core
    protected Android-sensitive libraries

shared validated providers
    intentionally selected common libraries

application-local closure
    preserve upstream $ORIGIN locality where required

supplemental selected closure
    provenance-aware Debian-derived provider artifacts
```

## Symlink generation caveat

A farm generation made of symlinks into mutable rootfs paths is not truly immutable.

```text
generation-A/lib/foo.so
    -> mutable Debian rootfs target
```

Later rootfs package mutation can change, remove, or redirect the effective generation content.

Therefore true rollback requires:

```text
generation-owned bytes
or content-addressed storage
or exact artifact retention + deterministic reconstruction
```

Do not claim immutable rollback from directory naming alone.

## Substrate and provider lifecycles must be separate

The confirmed ABI incident proves:

```text
provider libdbus requirement
    -> missing symbol in active glibc substrate
```

No farm rebuild can repair that failure.

Model independent states:

```text
READY
DIRTY_INPUT
BLOCKED_SUBSTRATE
CANDIDATE_FAILED
NEEDS_REVALIDATION
```

And preserve the distinction:

```text
provider rollback
    !=
substrate rollback
```

A previous farm cannot restore a previous glibc core.

## Identity model change

Do not begin with one combined fingerprint.

Separate:

```text
SUBSTRATE_ID
PROVIDER_INPUT_ID
MATERIALIZER_ID
VALIDATION_POLICY_ID
WORKLOAD_CONTRACT_ID
```

Different causes should trigger different actions.

Examples:

```text
provider input changed
    -> materialize candidate

materializer rules changed
    -> materialize candidate

only validation policy changed
    -> revalidate

only workload contract changed
    -> run new domain gates

nothing changed
    -> no-op
```

## Candidate validation requirement

Future candidate tests must prove they used the candidate.

The current relocation regression test defaults to active `$HOME/gl/lib` state. That is correct for the incident regression, but a candidate lifecycle must establish:

```text
candidate context selected
actual loaded object identity captured
active loader/cache state did not silently substitute old provider
```

Configuration intent is not enough.

## Pacman decision

Do not install or switch package-manager infrastructure merely for hooks.

A package event can say:

```text
something probably changed
```

Correctness authority must come from:

```text
observed actual runtime identities
    compared with
active receipt
```

If pacman is already or deliberately becomes the narrow authoritative glibc substrate backend, it may own:

```text
package acquisition
package identity/version
update transaction
artifact/cache access
optional event hint
```

It must not own:

```text
provider compatibility
world purity
application closure
capability validation
promotion policy
```

Architecture remains backend-neutral.

## Semantic hard-refactor target

Conceptually split the current umbrella into:

```text
world.glibc

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

The physical `$HOME/gl` namespace may remain. A live namespace is not one semantic owner.

## Immediate sequencing

### Stage 0 — incident recovery only

Do now:

```text
repair or replace broken glibc substrate
run core ABI regression gate
run libdbus relocation regression gate
run VS Code real workload gate
preserve evidence
```

Do not yet:

```text
install/switch pacman for hooks
add gl-run auto-sync
build broad-farm generation lifecycle
claim current/previous farm is world rollback
```

### Stage 1 — reconcile documents and branch reality

Use together:

```text
main: docs/system-foundation/
refactor branch: docs/refactor/
```

Treat `docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md` and this document as the current direction where earlier migration tactics conflict.

### Stage 2 — semantic inventory and hard split

Inventory every file and every environment variable currently under the `gl` umbrella.

Assign each to exactly one primary semantic owner:

```text
world
provider
bridge
toolchain
application family
specific application
validation only
```

Do not begin physical movement until the ownership table is explicit.

### Stage 3 — settle substrate authority

Capture real device facts:

```text
who owns installed $PREFIX/glibc files
which package database records them
current update path
exact previous artifact availability
install/config semantics that direct extraction would lose
```

Then choose the backend implementation of a neutral substrate adapter.

### Stage 4 — selected closure pilot

Keep broad farm as a control/reference and pilot one bounded closure through:

```text
static ELF closure
protected world-owned exclusion
app-local locality preservation
dynamic evidence enrichment
selected provider-byte materialization
provenance receipt
candidate validation
```

### Stage 5 — minimum lifecycle only

After semantic objects are correct:

```text
observe
receipt
candidate materialize
candidate validate
promote
rollback
```

Hooks remain optional optimizations.

### Stage 6 — PyMOL as architecture proof

Do not onboard PyMOL by copying legacy launcher/global-env patterns.

Use it to prove composition of:

```text
world.glibc
python.runtime
display.x11
graphics.opengl
fonts
native-extension ABI contract
```

## Branch implementation stop line

Until the semantic inventory and substrate authority decision are complete, do not add architecture-changing implementation for:

```text
gl-sync
gl-status
auto-sync in gl-run
pacman hooks
broad-farm generation activation
new global gl env policy
```

Read-only observation, evidence capture, incident recovery, and regression gates are allowed.

## Decision summary

```text
ownership refactor
    KEEP

modules/gl as final semantic object
    REJECT

gl-run extension
    REJECT

broad farm as production architecture
    NOT ESTABLISHED; KEEP TRANSITIONAL ONLY

candidate -> validate -> promote principle
    KEEP

0014 implementation plan
    PARTIALLY SUPERSEDED

pacman for hook convenience
    REJECT

backend-neutral substrate adapter
    ACCEPT

semantic hard refactor now
    RECOMMENDED

PyMOL as architecture proof
    RECOMMENDED
```

## Source-of-truth relationship

When reading the current project direction:

```text
main/docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
    -> full architectural rationale

this document
    -> refactor-branch implementation consequence

0014
    -> retained transaction/validation insights, but not current implementation sequence

0012 + 0013
    -> incident evidence and root-cause record
```
