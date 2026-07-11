# 0093 — Post-Audit Direction, Validator Lifecycle, and Selected-Closure Re-entry

## Status

This record accepts the direction of:

```text
docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
```

Audit source:

```text
branch:
    docs/post-graphics-architecture-audit

audit commit:
    c3b6c3ac87c8246ee335212d7addca17de3c9196

audited closure base:
    07b2f9a6f8f985fb3f152abd77c0ad3f04237cc9
```

The immediate direction is revised from the earlier informal ordering.

```text
not:
    graphics closure
        -> atomic activation implementation
        -> PyMOL

now:
    graphics closure
        -> knowledge/control-plane closure
        -> resume the selected Obsidian parent pilot
        -> decide semantic provider/application boundaries
        -> define minimum activation for the next live migration
        -> apply bounded ownership changes
        -> define substrate upgrade lifecycle
        -> use PyMOL as architecture proof
```

No closed graphics workload is rerun by this decision.

## Why the direction changes

The graphics transaction proved a semantic contract:

```text
world-boundary sanitation
consumer-scoped provider selection
consumer-owned bridge selection
application-owned feature mode
isolated application-state authority
selected-provider/device correlation
claim-triggered revalidation
```

It did not prove that these current realization objects are permanent:

```text
~/gl/env
gl-run
freedreno.sh
GL_GPU
modules/gl
broad farm
checkout-linked live leaves
```

The parent selected Obsidian closure question remains the strongest unresolved architecture discriminator. It was selected to test whether a real Electron AppDir can consume selected external provider bytes while preserving valid application-local locality. Graphics was a sub-question of that pilot, not a replacement for it.

Atomic activation remains mandatory before the next multi-file promoted migration, but its managed object set cannot be designed correctly before the selected-closure result and semantic owner decisions are known.

## Knowledge/control-plane closure state

The audit branch already synchronized:

```text
README.md
STATUS.md
docs/architecture.md
docs/glibc-layer.md
docs/refactor/README.md
docs/refactor/MIGRATION_JOURNAL.md
experiments/README.md
experiments/glibc/selected-obsidian-closure/README.md
experiments/glibc/vulkan-policy-composition/README.md
modules/gl/README.md
packages/mesa-glibc/README.md
packages/obsidian/README.md
packages/vscode/README.md
```

The remaining Phase A item was individual graphics recipe lifecycle classification. This record closes that item.

## Graphics recipe lifecycle model

The post-closure recipe tree is not one permanent test suite.

The following classes are used.

### `ACTIVE_CONTRACT_GATE`

A top-level machine receipt that directly validates one accepted promoted claim. Run only when its documented claim trigger changes.

### `ACTIVE_GATE_IMPLEMENTATION_DEPENDENCY`

A probe, classifier, source fixture, or query helper invoked by an active contract gate. It is maintained with its owning gate and is not independently scheduled merely because it exists.

### `CANONICAL_EVIDENCE_HELPER`

A helper used to interpret or compare retained canonical evidence. It may be rerun over retained evidence when interpretation policy changes, but it does not by itself revalidate promoted runtime behavior.

### `HISTORICAL_DIAGNOSTIC`

A discovery-stage experiment helper retained for provenance and future debugging. It is not part of routine contract validation.

### `SUPERSEDED_FALSE_NEGATIVE_MODEL`

A historical implementation or receipt whose evidence assumption was invalid. It is preserved in commits and numbered records, but must never be reused as current authority.

This class does not require a currently tracked runnable file. In this graphics transaction, the important superseded models are historical versions/receipts rather than separate surviving scripts.

## Active contract gates

```text
experiments/glibc/vulkan-policy-composition/recipe/

validate-promoted-vulkan-policy-transaction.sh
    ACTIVE_CONTRACT_GATE
    claim:
        promoted source/pre-deploy composition is internally consistent

validate-live-vulkan-policy-installation.sh
    ACTIVE_CONTRACT_GATE
    claim:
        required live leaves and baseline/profile behavior match source contract

validate-promoted-gl-run-renderer.sh
    ACTIVE_CONTRACT_GATE
    claim:
        current OpenGL consumer selects Zink -> Turnip/Adreno under the accepted composition

validate-promoted-vscode-gpu-identity.sh
    ACTIVE_CONTRACT_GATE
    claim:
        VS Code GPU branch has sanitized policy, explicit provider, ANGLE Vulkan mode,
        and correlated Turnip/Adreno primary identity

validate-promoted-vscode-cpu-policy.sh
    ACTIVE_CONTRACT_GATE
    claim:
        VS Code CPU branch is provider-neutral and effectively GPU-disabled

validate-promoted-obsidian-gpu-identity.sh
    ACTIVE_CONTRACT_GATE
    claim:
        Obsidian GPU branch uses isolated application state and correlated
        Turnip/Adreno primary identity

validate-promoted-obsidian-cpu-policy.sh
    ACTIVE_CONTRACT_GATE
    claim:
        Obsidian CPU branch uses isolated application state and effective CPU mode
```

## Active gate implementation dependencies

```text
build-glx-renderer-probe.sh
    owner gate:
        validate-promoted-gl-run-renderer.sh

glx-renderer-probe.c
    owner gate:
        validate-promoted-gl-run-renderer.sh

probe-vscode-policy-env-boundary.sh
    owner gate:
        validate-promoted-vscode-gpu-identity.sh

probe-vscode-cdp-gpu-identity.sh
    owner gate:
        validate-promoted-vscode-gpu-identity.sh

classify-vscode-cdp-gpu-identity.sh
    owner gate:
        validate-promoted-vscode-gpu-identity.sh

probe-electron-cdp-gpu-identity.sh
    owner gate:
        validate-promoted-obsidian-gpu-identity.sh

classify-cdp-gpu-identity.sh
    owner gate:
        validate-promoted-obsidian-gpu-identity.sh

query-cdp-system-info.py
    owner gates:
        VS Code and Obsidian CDP identity probes
```

A change to one of these helpers triggers the owning active gate, not every graphics gate.

## Canonical evidence helpers

```text
audit-promoted-vulkan-policy-ownership-v2.sh
    exact-HEAD producer/consumer ownership inventory

capture-glx-probe-maps.sh
    retained GLX process-map evidence capture helper

enrich-glx-probe-maps.sh
    retained GLX identity/provenance enrichment helper

compare-glx-provider-graphs.sh
    retained GLX provider-graph comparison helper

compare-obsidian-policy-controls.sh
    retained Obsidian same-feature-mode policy comparison helper

compare-vscode-cdp-gpu-identities.sh
    retained VS Code primary-device comparison receipt helper

compare-vscode-vulkan-policy-controls.sh
    retained VS Code provider-policy comparison helper

summarize-obsidian-loader-debug.sh
    retained implicit-loader evidence summarizer
```

These tools support evidence interpretation. They do not become runtime gates merely because their output was important during discovery.

## Historical diagnostics

```text
capture-implicit-loader-debug.sh
launch-obsidian-with-policy.sh
launch-vscode-with-policy.sh
policy-env.sh
probe-driver-isolation-matrix.sh
probe-vscode-app-local-vulkan-loader.sh
probe-vscode-gpu-observer-contract.sh
probe-vscode-process-handoff.sh
run-zink-with-policy.sh
```

These remain useful for reproducing or extending earlier investigations. They are not scheduled after closure and are not requirements for an unrelated ownership or selected-closure change.

## Superseded false-negative models

The following are preserved through numbered records and history, not retained as current authoritative recipes.

```text
old VS Code child-environment exact-value assumption
    -> docs/refactor/0085-vscode-child-proc-environ-observability-false-negative.md

first Obsidian CDP/user-data authority assumption
    -> docs/refactor/0088-obsidian-user-data-authority-and-cdp-path-false-negative.md

first unsuffixed promoted ownership audit helper
    -> superseded before use by audit-promoted-vulkan-policy-ownership-v2.sh
```

The corrected current files are not classified as false-negative models simply because older commits of the same path were wrong.

## Trigger routing

```text
source composition or managed-leaf set changes
    -> validate-promoted-vulkan-policy-transaction.sh
    -> validate-live-vulkan-policy-installation.sh after deliberate activation

OpenGL adapter or GLX/Zink/provider-layer identity changes
    -> validate-promoted-gl-run-renderer.sh

VS Code launcher/version/provider/ANGLE or identity-classifier changes
    -> relevant VS Code GPU or CPU gate only

Obsidian launcher/version/provider/state-authority or identity-classifier changes
    -> relevant Obsidian GPU or CPU gate only

active dependency helper changes
    -> its owning gate

evidence comparison policy changes only
    -> relevant CANONICAL_EVIDENCE_HELPER over retained evidence

documentation-only change
    -> no runtime gate unless evidence interpretation is invalidated
```

## Selected Obsidian closure decision

The pilot is continued, not terminated.

Reason:

```text
it remains the first real application-domain test of:
    valid $ORIGIN/AppDir locality
    protected world substrate
    prefix provider capabilities
    selected rootfs provider bytes
    data-provider separation
    multiprocess workload equivalence
```

Skipping it would force PyMOL or another application to inherit unresolved broad-farm and global-environment assumptions.

## Phase B1 — retained control locality input audit

The first re-entry action is read-only analysis of the retained enriched control evidence.

Added recipe:

```text
experiments/glibc/selected-obsidian-closure/recipe/
    audit-retained-control-locality.sh
```

The recipe performs no process launch and no promoted mutation.

It verifies:

```text
required retained evidence files exist;
semantic review set is empty;
candidate-relevant current bytes still match captured SHA-256 identities;
ELF SONAME / DT_NEEDED / RPATH / RUNPATH facts can still be reproduced;
APP_LOCAL versus external provider name collisions are explicit;
DT_NEEDED names have zero, one, or multiple captured runtime candidates;
process-class use of semantic objects is preserved;
provider package/capability counts are emitted.
```

Primary outputs:

```text
input-verification.tsv
candidate-input-identities.tsv
elf-objects.tsv
elf-needed.tsv
name-providers.tsv
locality-collisions.tsv
needed-resolution.tsv
unresolved-needed.tsv
ambiguous-needed.tsv
process-semantic-usage.tsv
provider-package-summary.tsv
summary.tsv
claim-boundary.txt
next-state.txt
audit.status
```

A `PASS` means:

```text
retained evidence remains identity-reproducible enough for the next locality and
static/runtime decision step
```

It does not mean:

```text
locality policy is decided;
static closure is complete;
a selected candidate is ready;
control/candidate equivalence is proven.
```

Collision, unresolved-edge, and ambiguous-edge rows are decision inputs, not automatic audit failures.

## Phase B1 decision branches

```text
PASS + identity stable
    -> inspect locality collisions
    -> classify unresolved and ambiguous DT_NEEDED edges
    -> decide whether retained maps are sufficient for edge attribution
    -> define the bounded non-graphics closure analysis

FAIL due hash mismatch or missing candidate input
    -> do not silently analyze current bytes as captured bytes
    -> determine whether exact captured artifacts exist
    -> otherwise perform one explicitly justified fresh CPU control capture

FAIL due semantic review rows
    -> resolve classifier/identity ownership before closure materialization
```

No candidate bytes are materialized in Phase B1.

## Evidence handoff convention

Future device evidence is transferred as a stage-specific compressed archive.

Every command block that creates an evidence directory must define:

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
```

The final command must be:

```bash
tar czf ~/Downloads/$out.tgz $OUT
```

Do not use ambiguous names such as:

```text
results.tgz
output.tgz
evidence.tgz
```

The archive name identifies the exact stage, while the contained receipt remains the evidence authority.

The archive is a transport object. It is not automatically promoted into repository evidence and it does not replace the original device evidence root.

## Revised execution order

```text
A. knowledge/control-plane closure
    CLOSED by canonical synchronization plus this validator classification

B. selected Obsidian closure parent pilot
    ACTIVE
    first action: retained control locality input audit

C. semantic owner decision
    BLOCKED on selected-closure result

D. minimum atomic activation design
    BLOCKED until the next promoted object set is known
    mandatory before applying the next multi-file live migration

E. bounded ownership change
    candidate first move remains Electron sandbox policy out of world baseline

F. glibc substrate upgrade/recovery lifecycle
    after world/provider object boundaries are explicit

G. PyMOL runtime implementation
    deferred

PyMOL contract design
    allowed in parallel without runtime mutation
```

## Stop line

Do not:

```text
rerun closed graphics gates without a trigger;
materialize an Obsidian candidate before Phase B1 evidence is interpreted;
use current rootfs bytes when they no longer match retained captured identities;
treat SONAME collision as proof of wrong selection without process/loader evidence;
treat absence from the captured mapped set as universal proof of irrelevance;
mutate the promoted Obsidian launcher for the candidate experiment;
start atomic activation implementation around the current gl umbrella;
start PyMOL by expanding gl/env or the broad farm;
forget to create the stage-specific tgz handoff archive.
```

## Decision

```text
post-audit direction:
    ADJUSTED

graphics transaction:
    CLOSED / TRIGGER-BASED GATES ONLY

knowledge/control-plane Phase A:
    CLOSED

selected Obsidian parent pilot:
    CONTINUE

next device action:
    READ-ONLY RETAINED CONTROL LOCALITY INPUT AUDIT

atomic activation implementation:
    DEFER UNTIL SEMANTIC OBJECT SET IS DECIDED

PyMOL runtime mutation:
    DEFER
```
