# 0019 — Selected-Closure Pilot Decision Criteria

## Status

This document defines Stage 4 pilot selection and acceptance criteria.

It does not implement a resolver, materializer, provider store, or lifecycle framework.

The broad farm remains active as a research/control reference while the pilot tests whether a smaller selected provider closure is a valid architectural object.

## 1. Pilot objective

The pilot must discriminate between two models.

### Control model

```text
Debian rootfs
    -> broad scan
    -> basename-selected symlink farm
    -> active glibc loader state
    -> workload
```

### Candidate model

```text
bounded workload/provider target
    -> static dependency discovery
    -> protect world-owned substrate objects
    -> preserve valid application-local locality
    -> enrich with runtime evidence
    -> select concrete provider bytes
    -> record provenance
    -> validate in candidate-specific context
```

The goal is not to prove that every application can immediately abandon the broad farm.

The goal is to determine whether selected closure materialization can provide:

```text
smaller semantic scope
explicit identity
actual byte ownership
real rollback domain
provable provider selection
reproducible provenance
```

## 2. Recommended first real target

Recommended target:

```text
selected D-Bus client/provider chain
```

centered on the observed Debian provider:

```text
libdbus-1.so.3
```

with a bounded direct D-Bus probe rather than VS Code as the first workload.

## 3. Why D-Bus is a strong discriminating target

The recent ABI incident already exposed a real boundary:

```text
provider libdbus
    requires substrate ABI symbol
```

This makes the target useful for testing:

```text
world-owned exclusion
provider transitive closure
substrate/provider compatibility
actual loader selection
provenance capture
candidate isolation
```

The target is smaller and easier to reason about than VS Code or Obsidian, while still exercising a real provider chain and the exact class of failure seen in production.

## 4. Why VS Code is not the first pilot

VS Code currently combines:

```text
large Electron payload
application-local libraries/resources
X11
fonts
TLS
URL-open bridge
ANGLE/Vulkan graphics composition
shared providers
application-specific flags
```

Using it first would make a resolver failure difficult to distinguish from application-domain policy or graphics-path failure.

VS Code should remain an important downstream workload gate after the provider mechanism is proven on a bounded target.

## 5. Required pilot phases

### Phase A — control capture

Record the broad-farm baseline:

```text
entrypoint identity
active substrate identity
resolved libdbus path
resolved transitive provider paths
Build IDs or cryptographic hashes
package owner/version provenance
loader trace
/proc/<pid>/maps when the probe remains alive long enough
probe output/exit status
```

### Phase B — static ELF closure

Starting from the pilot entrypoint and/or selected provider root:

```text
read DT_NEEDED
resolve one dependency edge at a time
record selected source path
recurse until closure
```

The resolver must keep a decision log for every edge:

```text
consumer
DT_NEEDED name
candidate paths considered
selected path
selection reason
owner class
provenance
```

### Phase C — world-owned protected exclusion

The selected provider closure must not materialize or override world-owned objects.

Initial protected classes should be derived from observed substrate ownership, not only from one basename regex.

Examples include:

```text
glibc loader
libc family
world-owned low-level runtime objects
other explicitly protected substrate files discovered by authority inventory
```

The pilot must record rejected provider candidates and the world-owner reason.

### Phase D — application-local locality preservation

The resolver must not replace a valid application-local `$ORIGIN` dependency merely because a same-SONAME shared provider exists elsewhere.

Because the D-Bus pilot may not exercise enough `$ORIGIN` topology, add a small resolver-conformance fixture:

```text
fixture/bin/probe
fixture/lib/libapp-local.so

probe RUNPATH:
    $ORIGIN/../lib
```

Acceptance condition:

```text
resolver preserves intended app-local selection
shared candidate with same SONAME does not silently override locality
```

This fixture validates an invariant; it is not a second production pilot.

### Phase E — runtime evidence enrichment

Static closure is not sufficient for:

```text
dlopen/plugin loading
configuration-selected providers
conditional runtime loading
NSS-style mechanisms
schema/data dependencies
other non-DT_NEEDED runtime discovery
```

The pilot should enrich the static graph using bounded runtime evidence such as:

```text
loader resolution trace
/proc/<pid>/maps
controlled open/openat trace when justified
application/probe-specific diagnostics
```

Only runtime-observed additions supported by evidence should enter the selected closure.

### Phase F — provider-byte materialization

The candidate must own concrete selected provider bytes or otherwise preserve exact immutable content identity.

Rejected pilot form:

```text
candidate generation directory
    -> symlinks into mutable Debian rootfs paths
```

Accepted initial form:

```text
candidate provider directory
    contains copied/materialized selected bytes
    records source path and source package identity
    records content hash and/or Build ID
```

The exact storage format remains open.

### Phase G — provenance receipt

At minimum record:

```text
pilot target identity
substrate identity
source rootfs identity/context
for every materialized provider object:
    SONAME/path
    source pathname
    package owner
    package version
    content SHA-256
    ELF Build ID when present
materializer source identity
selection policy identity
validation policy identity
```

The receipt must be human-readable first. Machine serialization can follow after fields stabilize.

### Phase H — candidate-specific validation

The candidate test must prove the candidate was selected.

Required evidence:

```text
candidate-specific loader/search context
resolved provider path points into candidate materialization
actual mapped object identity captured
mapped hash/Build ID matches receipt
active broad-farm provider was not silently substituted
```

A passing process with only configuration intent is insufficient.

## 6. Acceptance gates

### Gate 1 — bounded closure

```text
PASS:
    closure terminates in a small, explainable selected set

FAIL:
    ordinary probe requires effectively importing the broad rootfs library pool
```

### Gate 2 — world protection

```text
PASS:
    no candidate provider overrides world-owned protected substrate objects

FAIL:
    closure only works by importing another libc/loader/runtime family
```

### Gate 3 — actual candidate selection

```text
PASS:
    trace/maps prove candidate provider objects were loaded

FAIL:
    active farm/cache can satisfy the test without the candidate
```

### Gate 4 — provenance completeness

```text
PASS:
    every materialized provider byte has source and identity evidence

FAIL:
    unexplained copied libraries or unresolved symlink provenance remain
```

### Gate 5 — control equivalence

```text
PASS:
    bounded probe behavior under selected closure matches the control claim

FAIL:
    selected closure changes required behavior without understood reason
```

### Gate 6 — mutation isolation

```text
PASS:
    rootfs package mutation after candidate materialization does not change the
    candidate provider bytes

FAIL:
    candidate identity changes because external rootfs symlink targets changed
```

### Gate 7 — rollback-domain honesty

```text
PASS:
    replacing/removing candidate provider materialization does not claim to restore
    an independently changed substrate

FAIL:
    provider rollback is presented as world/substrate rollback
```

## 7. Pilot non-goals

Do not use the pilot to implement:

```text
global gl-sync
universal application resolver
project-wide package manager
pacman hooks
one global dirty fingerprint
complete broad-farm replacement
automatic update policy
```

## 8. Decision outcomes after the pilot

### Outcome A — selected shared provider is validated

Then the project may define a real object such as:

```text
provider.shared-libs.glibc/<bounded-purpose>
```

and implement only the lifecycle needed by that object.

### Outcome B — closure is application-family specific

Then ownership should move toward:

```text
family-specific supplemental provider closure
```

rather than one global shared pool.

### Outcome C — closure is application-specific

Then materialization belongs with the application domain/package.

### Outcome D — broad dynamic behavior dominates

Then retain the broad farm as a controlled compatibility mechanism for that workload class while further evidence is collected.

Do not force a selected-closure architecture when the pilot evidence rejects it.

## 9. Required relationship to incident recovery

The pilot must not begin against the currently broken substrate.

Precondition:

```text
core ABI gate PASS
libdbus relocation gate PASS
real VS Code recovery gate recorded
```

The ABI incident recovery and selected-closure pilot are separate activities:

```text
incident recovery
    restores known substrate/provider compatibility

selected-closure pilot
    tests a future provider materialization architecture
```

Mixing them would make the experiment uninterpretable.
