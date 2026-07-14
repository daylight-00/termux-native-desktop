# 12. Document Consistency Audit and Execution Order

> **Date:** 2026-07-10
> **Status:** active consistency index and execution-order guide
> **Scope:** audits the reasoning chain across the foundation set, reconciles earlier migration tactics with the architecture reassessment, and identifies which conclusions are settled versus still open.

## 12.1 Purpose

The project now has two kinds of valuable history:

```text
bottom-up discovery
    -> experiments
    -> operational mechanisms
    -> working applications
    -> incident evidence

and

top-down synthesis
    -> project essence
    -> invariants
    -> object model
    -> target architecture
    -> refactor direction
```

The risk is no longer absence of documentation. The risk is that a reader can select one correct-but-contextual document and mistake its local recommendation for the latest global direction.

This audit establishes one coherent reasoning chain and one execution order without erasing the history that produced them.

The governing distinction is:

```text
fact / evidence
    -> preserved

stable invariant
    -> normative unless strong evidence changes project definition

target model
    -> normative direction, not a claim about current implementation

migration tactic
    -> contextual and replaceable

implementation mechanism
    -> replaceable

open question
    -> must remain explicitly open until discriminating evidence exists
```

## 12.2 Executive audit result

The documentation set contains the necessary logical basis for the current direction, but before this audit the reasoning was distributed across documents with different temporal scopes.

The major conclusions are internally consistent when read with the following precedence:

```text
01 essence
    -> why the project exists

02 principles/invariants
    -> what valid implementations must preserve

03 system model
    -> which responsibility dimensions exist

04 object model
    -> which semantic objects express those responsibilities

05 ideal target architecture
    -> how those objects could become a concrete system

06 pre-refactor assessment
    -> what the earlier implementation got right and where debt existed

07 original migration strategy
    -> conservative tactic proposed before later incident/reassessment evidence

08 original roadmap
    -> original gate-based sequence, now revised for immediate execution order

09 validation/promotion doctrine
    -> enduring gate/evidence rules, extended by newer rollback and candidate-selection requirements

10 open questions
    -> unresolved implementation boundaries, interpreted in light of decisions already made in 11

11 reassessment decision
    -> latest architectural direction after ownership refactor and ABI incident

12 this audit
    -> document-role map, conflict resolution, settled/open matrix, and current execution order
```

No current conclusion requires preserving `gl-run`, `gl-farm`, a monolithic `~/gl/env`, `modules/gl` as one semantic owner, or pacman as architecture.

The preserved commitments are instead:

```text
native host authority
coherent process ABI worlds
explicit bridges
intentional provider selection
smallest valid policy scope
warehouse != promoted closure
preserve valid upstream locality
claim-oriented evidence
candidate -> validate -> promote
real rollback, not nominal rollback
provenance
```

## 12.3 Document-by-document authority map

| Document | Primary role | Authority status | Important qualification |
|---|---|---|---|
| `01-essence.md` | mission, identity, non-goals | normative | implementation-independent |
| `02-principles-and-invariants.md` | project constitution | normative | mechanisms may change |
| `03-system-model-v2.md` | responsibility planes | normative conceptual model | directories need not mirror planes |
| `04-domain-capability-bridge-model.md` | semantic object model | normative conceptual model | serialization remains open |
| `05-ideal-target-architecture.md` | target materialization model | target direction | not current-state declaration |
| `06-current-state-assessment.md` | original pre-refactor assessment | historical analytical snapshot | facade-preservation language is not a current invariant |
| `07-gap-analysis-and-refactoring-strategy.md` | original conservative migration tactic | partially superseded tactic | document 11 overrides preservation-by-default |
| `08-implementation-roadmap.md` | original phased roadmap | partially superseded sequence | document 11/12 define current immediate order |
| `09-validation-promotion-and-evidence.md` | gate/evidence doctrine | normative, extended | candidate selection and rollback domains must be proven |
| `10-open-design-questions.md` | unresolved question registry | active registry | some surrounding architecture decisions are now settled by 11 |
| `11-architecture-reassessment-and-hard-refactor-decision.md` | latest architectural decision | active direction | implementation still evidence-gated |
| `12-document-consistency-audit-and-execution-order.md` | consistency and execution index | active index | does not replace evidence records |

## 12.4 The complete logical derivation

The current direction is not a preference for cleaner directory names. It follows from the project definition.

### Step 1: mission

```text
build a credible workstation on a non-root Android phone
```

The workload set includes coding, remote development, scientific visualization, data inspection, review, and writing.

### Step 2: host constraint

```text
Android kernel/security model
    +
Termux bionic host
    remain authoritative
```

The project is not trying to boot or emulate a second machine and is not trying to turn the host into Debian.

### Step 3: compatibility problem

Desired applications span incompatible userspace assumptions.

```text
bionic-native processes
    -> Android linker + bionic ecosystem

glibc application processes
    -> glibc loader + coherent glibc ecosystem
```

Therefore one flat process/runtime environment is invalid.

### Step 4: architectural response

```text
multiple coherent worlds/domains
    +
explicit bridges
    +
ABI-appropriate capability providers
```

This leads naturally to the object model:

```text
World
Application Domain
Capability
Provider
Bridge
Artifact Source
Validation Gate
```

### Step 5: supply/runtime separation

Artifacts may come from:

```text
Debian packages
AppImages
Conda packages
wheels
source builds
Termux packages
upstream tarballs
```

but source format does not define runtime authority.

Therefore:

```text
supply adapter
    -> candidate input
    -> inspection/transformation/materialization
    -> validation
    -> promotion
```

is more fundamental than one package manager.

### Step 6: runtime closure consequence

A broad Debian rootfs or farm can be useful for research, but it does not express intended production composition.

Therefore the target distinguishes:

```text
warehouse / research compatibility pool
    !=
promoted selected provider closure
```

The exact shared-vs-local boundary remains empirical, but broad farm permanence is not assumed.

### Step 7: policy-scope consequence

A monolithic environment file that owns world base policy, fonts, locale, TLS, Vulkan selection, D-Bus behavior, and Electron policy violates the smallest-valid-scope principle.

Therefore `~/gl/env` is interpreted as a current composition result, not a final semantic object.

### Step 8: ownership-refactor consequence

The repository ownership refactor correctly separated external application launchers, package lifecycles, experiments, shell behavior, and deployment tooling.

However, the remaining `modules/gl` grouping still spans:

```text
world policy
shared-library materialization
OpenGL capability composition
Vulkan provider selection
data providers
URL bridge
target toolchain
```

Therefore the ownership refactor is retained, but semantic decomposition must continue.

### Step 9: ABI incident consequence

The libdbus/glibc failure proved:

```text
provider requirement
    can fail against
world substrate ABI
```

and:

```text
broken substrate
    +
provider/farm rebuild
    =
still broken
```

Therefore substrate identity/validation and provider materialization/validation are independent lifecycle axes.

### Step 10: automation consequence

Because different changes have different consequences, one global dirty fingerprint and one universal sync action are too coarse as a starting point.

Separate causal identities are preferred:

```text
SUBSTRATE_ID
PROVIDER_INPUT_ID
MATERIALIZER_ID
VALIDATION_POLICY_ID
WORKLOAD_CONTRACT_ID
```

Then:

```text
input/materializer change
    -> materialize candidate

validation-policy change
    -> revalidate

workload-contract change
    -> run relevant domain gates

no relevant change
    -> no-op
```

### Step 11: package-manager consequence

A package-manager hook can indicate that something probably changed. It cannot prove runtime validity.

Therefore:

```text
hook
    -> optional event hint

observed identity + receipt + gates
    -> correctness authority
```

The architecture uses a backend-neutral substrate supply adapter. Pacman is acceptable only if device evidence shows it is already or deliberately becomes the narrow authoritative substrate backend. Installing or switching package managers merely for hooks is rejected.

### Step 12: hard-refactor consequence

The project must preserve:

```text
validated semantics
evidence
provenance
rollback paths
```

It does not need to preserve:

```text
historical command names
transitional facades
umbrella directories
broad farm production status
one package-manager integration
```

Therefore hard refactoring is justified when it removes a wrong object boundary with less total complexity than maintaining the facade.

## 12.5 Resolved apparent contradictions

### 12.5.1 “Do not rewrite” versus “hard refactor now”

Earlier documents recommended stratification and strangler-style migration because they were written before the ownership refactor outcome and ABI incident were jointly assessed.

The invariant underneath those recommendations was never “preserve command names.” It was:

```text
preserve validated behavior
preserve evidence
avoid unmeasured breakage
```

Document 11 strengthens the tactic:

```text
safe preservation is optional
when object identity is correct or replacement risk is high

hard replacement is allowed
when the object boundary is wrong and gates protect semantics
```

Thus there is no contradiction at the invariant level.

### 12.5.2 “Keep broad farm during migration” versus “do not build lifecycle around farm”

Both are true:

```text
keep farm as control/reference/research baseline
```

but:

```text
do not assume farm is the final production provider unit
```

The selected-closure pilot decides the long-term boundary.

### 12.5.3 “Reversible promotion” versus symlink farm generations

A stable pointer is reversible only if the pointed-to content identity remains stable.

```text
versioned directory
    + symlinks to mutable rootfs
    != true immutable generation
```

Real rollback requires generation-owned bytes, content-addressed storage, or exact artifact retention plus deterministic reconstruction.

### 12.5.4 “Package manager open question” versus backend-neutral substrate adapter decision

Two questions are distinct.

Settled architecture:

```text
world.glibc
    -> backend-neutral substrate supply adapter
```

Still open implementation:

```text
which backend is authoritative on the real device?
```

A future project-wide package manager is a separate question again and remains open.

### 12.5.5 “gl-run is narrow and useful” versus “delete or re-home gl-run”

The observation remains correct: current `gl-run` has narrow OpenGL/Zink semantics.

The later conclusion is about ownership:

```text
narrow semantics may survive
historical command/object identity need not
```

Therefore do not extend `gl-run` into lifecycle authority. Either compose the capability directly or re-home only the narrow behavior.

## 12.6 Settled decisions

The following are current project decisions, not open questions.

| Subject | Decision |
|---|---|
| native host authority | keep Android/Termux bionic host authoritative |
| PRoot normal execution | rejected |
| PRoot supply/oracle role | accepted |
| process ABI purity | invariant |
| cross-world communication | explicit bridges required |
| provider selection | intentional and validated |
| global foreign loader mutation | rejected |
| application model | domains consume capabilities |
| ownership refactor | keep and continue |
| `modules/gl` as final semantic owner | rejected |
| monolithic `~/gl/env` as final architecture | rejected; decompose by semantic scope |
| extending `gl-run` into lifecycle gateway | rejected |
| broad farm as established production target | rejected/not established; transitional only |
| candidate -> validate -> promote | retained |
| one global dirty fingerprint as first design | rejected |
| pacman for hook convenience | rejected |
| substrate architecture | backend-neutral supply adapter |
| package hooks | optional optimization only |
| candidate validation | must prove actual candidate/provider selection |
| symlink generation naming as proof of immutability | rejected |
| provider rollback == substrate rollback | rejected |
| hard semantic refactor at current project stage | recommended |
| PyMOL on legacy umbrella model | postpone |
| PyMOL as architecture composition proof | recommended |

## 12.7 Questions still open

The following must not be silently converted into implementation assumptions.

### Runtime data providers

For each of fonts, fontconfig config, locale, schemas, and shared data:

```text
keep passive rootfs provider?
materialize selected data closure?
which files are version-coupled to libraries?
```

### Shared-library boundary

The likely target is hybrid, but empirical evidence must decide:

```text
which low-level providers are intentionally shared?
which libraries remain app-local?
what becomes supplemental selected closure?
```

### Manifest serialization

Markdown first. TOML/YAML/JSON/custom formats remain implementation questions until fields stabilize.

### Launch composition mechanism

Still open:

```text
generated launch plan
runtime interpretation
hybrid
```

The semantic ownership split must precede this choice.

### Exact substrate backend

Still requires real-device evidence:

```text
which package database owns installed glibc?
how is it updated today?
can exact previous artifacts be retrieved?
what install/config semantics matter?
```

### Selected-closure pilot target

Choose a bounded workload/provider based on discriminating value, not convenience alone.

### PyMOL acquisition/provider strategy

Conda, source build, wheel-oriented, hybrid, and licensed-payload paths remain supply/provider questions after the application contract is written.

### Generalization scope

Device/SoC/Android-version generalization must follow evidence rather than be assumed from one target.

## 12.8 Current execution order

This section is the current order for architecture-changing work.

### Stage 0 — recover the ABI incident and freeze evidence

Allowed now:

```text
repair or replace the broken glibc substrate
run the core ABI regression gate
run the libdbus relocation regression gate
run the VS Code real workload gate
preserve outputs and identities
```

Do not mix recovery with unrelated environment/farm restructuring.

### Stage 1 — reconcile branch and foundation context

Read together:

```text
main/docs/system-foundation/
refactor/module-package-layout:docs/refactor/
```

The branch-specific operational direction is already recorded in:

```text
docs/refactor/0015-architecture-reassessment-and-hard-refactor-direction.md
docs/refactor/0016-next-session-handoff.md
```

Do not treat absence of main-only documents from the diverged branch as architectural irrelevance.

### Stage 2 — semantic inventory and ownership split

Inventory every file, variable, helper, and path assumption under the current `gl` umbrella.

Required fields:

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

Owner categories:

```text
world
provider
bridge
toolchain
application family
specific application
validation only
supply adapter
```

Only after this table is explicit should physical ownership be changed.

### Stage 3 — establish substrate authority from real device evidence

Capture facts before choosing pacman or another backend:

```text
installed-file ownership
authoritative package database
current update path
previous exact artifact availability
real rollback ability
install/config semantics that extraction would need to preserve
```

Then select the backend implementation of the neutral substrate adapter.

### Stage 4 — selected shared-provider closure pilot

Keep the broad farm as a control/reference.

Pilot one bounded target:

```text
static ELF closure
    -> protect world-owned libraries
    -> preserve valid app-local $ORIGIN locality
    -> enrich with runtime evidence
    -> materialize selected provider bytes
    -> record provenance receipt
    -> validate in candidate-specific context
```

Candidate validation must prove actual candidate selection and actual mapped provider identity.

### Stage 5 — implement only the minimum lifecycle

After semantic objects and pilot behavior are known:

```text
observe
receipt
candidate materialize
candidate validate
promote
rollback
```

Do not begin with a large universal `gl-sync` framework.

### Stage 6 — use PyMOL as architecture proof

Compose:

```text
world.glibc
python.runtime provider
display.x11 bridge/provider
graphics.opengl provider
fonts provider
native-extension ABI contract
```

If onboarding requires copying legacy launchers, broadening global environment policy, or adding PyMOL-specific farm exceptions, return to the ownership/closure design instead of normalizing the workaround.

## 12.9 Current implementation stop line

Until the semantic inventory and substrate-authority evidence are complete, do not add architecture-changing implementation for:

```text
gl-sync
gl-status
gl-run auto-sync
pacman hooks as lifecycle authority
single global compatibility fingerprint
generational broad-farm activation
new global gl environment policy
```

Allowed work:

```text
read-only inspection
identity capture
incident recovery
regression validation
semantic inventory
human-readable contracts
small discriminating experiments
documentation reconciliation
```

## 12.10 Validation interpretation after the reassessment

The gate doctrine in document 09 remains active, with three explicit extensions.

### Actual selection proof

```text
configured path
    != proof of selected provider
```

Record actual mapped/resolved object identity.

### Candidate isolation proof

A test of a candidate must prove that active loader/cache state did not silently substitute the active provider.

### Rollback-domain proof

Before claiming rollback, identify which domain is actually restored:

```text
provider content
world substrate
application payload
configuration
```

A provider pointer rollback does not undo an independently mutated substrate.

## 12.11 Documentation maintenance rule

When new evidence changes direction:

```text
1. preserve the evidence record;
2. state which previous assumption changed;
3. classify the old statement as fact, tactic, or superseded implementation decision;
4. update the active decision document;
5. update this consistency index if precedence or execution order changes;
6. update STATUS.md;
7. update validators/contracts together with implementation when applicable.
```

Do not rewrite historical experiment or migration records to make the current architecture appear inevitable in hindsight.

## 12.12 Audit conclusion

The project now has a complete top-down reasoning chain:

```text
mission
    -> host constraint
    -> multiple coherent worlds
    -> explicit bridges and providers
    -> semantic object model
    -> selected/materialized runtime target
    -> claim-oriented validation
    -> ownership refactor evidence
    -> ABI incident evidence
    -> hard-refactor decision
    -> current execution order
```

The immediate goal is not to automate the current umbrella more aggressively.

It is to ensure the objects are correct before automation makes them expensive to replace.

## Project references

- [`README.md`](README.md)
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
- [`11-architecture-reassessment-and-hard-refactor-decision.md`](11-architecture-reassessment-and-hard-refactor-decision.md)
- refactor branch: `refactor/module-package-layout`
- branch handoff: `docs/refactor/0016-next-session-handoff.md`
