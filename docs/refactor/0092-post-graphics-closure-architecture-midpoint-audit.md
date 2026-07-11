# 0092 — Post-Graphics-Closure Architecture Midpoint Audit

## Status

This is the architecture midpoint audit after closure of the scoped graphics-policy promotion transaction.

Audited repository state:

```text
commit:
    07b2f9a6f8f985fb3f152abd77c0ad3f04237cc9

runtime-source baseline:
    5ed76ec9c7409a141da02a28b5297b8b71965467

final Obsidian CPU receipt source:
    5ab13fd6c2af5843abf7bbff3a8a26f46a8e84b5
```

The six commits after the final Obsidian CPU receipt changed only:

```text
STATUS.md
docs/architecture.md
docs/glibc-layer.md
docs/gpu.md
docs/refactor/0090-current-obsidian-cpu-policy-and-survival-pass.md
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

No `modules/`, `packages/`, `tests/`, `tools/`, or experiment recipe source changed after the final CPU receipt.

This audit does not request or prescribe another graphics workload run. It evaluates whether the project is converging toward the system-foundation design, where bottom-up experiments are constrained by top-down object, ownership, lifecycle, and evidence rules.

## Executive verdict

The project is **architecturally on track**, and the graphics-policy transaction was closed legitimately.

The work followed the project philosophy in several important ways:

```text
minimum manipulation
    -> no package-manager switch for hooks
    -> no gl-sync/gl-status framework by inertia
    -> no blind periodic reruns

maximum discriminating effect
    -> one bounded D-Bus selected-closure pilot
    -> one real Electron application-domain pilot
    -> same-feature-mode provider-policy comparisons
    -> selected-device evidence rather than map-presence inference

preserve semantics, not accidental objects
    -> application launchers moved to package owners
    -> provider selection separated from bridge selection
    -> graphics feature mode separated from provider policy
    -> false-negative evidence models corrected instead of hidden
```

However, the closure creates a new risk: a successfully validated transitional implementation can now become structurally privileged merely because it passed many gates.

The immediate top-down pressure is therefore:

```text
accept the semantic contract
    !=
accept every current command, path, variable, directory, or broad provider model
```

The next project phase must not jump directly from graphics closure to PyMOL implementation.

Before PyMOL is used as the next application proof, the project must address or explicitly decide:

```text
1. the unfinished Obsidian selected-closure/locality question;
2. the semantic split of the remaining gl umbrella and global environment;
3. atomic activation for project-authored runtime leaves;
4. the glibc substrate upgrade/recovery contract beyond the 2.42 hold;
5. canonical documentation/index synchronization;
6. which closed experiment validators remain active contract gates;
7. the separation between current adapters and durable invariants.
```

## Audit basis

The audit reads the following document classes together.

### Top-down architecture authority

```text
main:
    docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
    docs/system-foundation/12-document-consistency-audit-and-execution-order.md
```

These establish:

```text
preserve validated semantics and evidence;
do not preserve command names or umbrella objects by inertia;
modules/gl is transitional;
gl-run is not an architecture invariant;
the broad farm is a research/control object;
substrate and provider lifecycles are independent;
candidate validation must prove actual selection;
package-manager choice remains below architecture.
```

### Branch architecture and evidence

```text
docs/refactor/0015-architecture-reassessment-and-hard-refactor-direction.md
docs/refactor/0017-gl-umbrella-semantic-inventory.md
docs/refactor/0018-real-device-glibc-substrate-authority.md
docs/refactor/0028-selected-dbus-candidate-validation-passed.md
docs/refactor/0029-second-selected-closure-pilot-target.md
docs/refactor/0034-obsidian-control-semantic-decomposition.md
docs/refactor/0042-0076 graphics-policy design/evidence chain
docs/refactor/0083-0091 promotion receipts and closure
```

### Current implementation

```text
modules/gl/overlay/home/gl/env
modules/gl/overlay/home/gl/bin/gl-run
modules/gl/overlay/home/gl/bin/gl-farm
modules/gl/overlay/home/gl/policy/vulkan/freedreno.sh
packages/vscode/launcher/code
packages/obsidian/launcher/obsidian
packages/obsidian/launcher/obsidian-app
tools/deploy
```

### Current integrated guides and status

```text
docs/architecture.md
docs/glibc-layer.md
docs/gpu.md
STATUS.md
```

## Philosophy scorecard

| Principle | Current result | Judgment |
|---|---|---|
| native host authority | retained | aligned |
| one coherent ABI world per process | retained and tested | aligned |
| explicit bridges/providers | graphics dimensions separated | aligned |
| minimum manipulation, maximum effect | no new package manager or universal sync framework | strongly aligned |
| evidence before promotion | multiple correlated receipts | aligned |
| claims no stronger than evidence | false negatives and observability boundaries preserved | strongly aligned |
| preserve semantics, not object identity | partially achieved | incomplete |
| warehouse != promoted closure | D-Bus pilot proved selected materialization | aligned, not yet integrated broadly |
| smallest valid policy scope | graphics improved; many non-graphics globals remain | partially aligned |
| candidate -> validate -> promote | evidence discipline strong; live activation still source-linked | incomplete |
| cheap real rollback | Mesa versioned prefix only; general runtime leaves unresolved | incomplete |
| knowledge/control plane stays current | closure docs improved; indexes and experiment READMEs drifted | currently below standard |

## What was done correctly

### 1. Graphics was decomposed into independent dimensions

The accepted current composition distinguishes:

```text
world-boundary sanitation
Vulkan provider selection
OpenGL-to-Vulkan bridge selection
application feature mode
application-state isolation
selected-device evidence
```

This is a real correction of the earlier flat `GPU=0/1` model.

The result is not merely cleaner shell code. It demonstrates that:

```text
provider discovery/selection
    !=
device-class intent
    !=
consumer suitability
    !=
application feature mode
```

### 2. Consumer-specific behavior was not forced into one global policy

The project directly observed different outcomes for:

```text
standalone Zink/GLX consumer
Electron/ANGLE Vulkan consumer
VS Code
Obsidian
CPU-mode Electron branches
```

The architecture conclusion that provider policy must remain consumer-aware is supported by discriminating evidence rather than preference.

### 3. Actual selected-provider evidence was strengthened

The project did not treat:

```text
mapped ICD object
```

as equivalent to:

```text
selected rendering provider/device
```

The accepted Electron GPU receipts correlate:

```text
observable environment/argv
CDP primary identity
ANGLE/Vulkan feature state
managed provider mapping
KGSL device mapping
```

This is consistent with the project evidence policy.

### 4. CPU mode was defined semantically

The project correctly rejected a universal rule that a process named `gpu-process` must be absent.

The accepted CPU contract is:

```text
provider-neutral environment
exact --disable-gpu
no GPU-enablement feature flags
effective disabled/compositing mode
viable renderer/main topology
bounded survival
```

This avoids accidental coupling to one Chromium/Electron internal process topology.

### 5. Application-state authority became part of validation

The first Obsidian CDP attempt exposed that a generic Chromium argument did not necessarily define the application's effective user-data authority.

The corrected receipts aligned:

```text
XDG_CONFIG_HOME
actual <config>/obsidian directory
process argv
CDP endpoint observation
```

and excluded normal user state from promotion evidence.

That correction is valuable beyond graphics: application-domain validation must identify the application's real state authority.

### 6. Revalidation became trigger-based

The closure correctly rejects blind periodic reruns.

This is a direct expression of minimum manipulation:

```text
claim surface unchanged
    -> no runtime rerun

relevant source/runtime/application/evidence contract changed
    -> run only affected gate
```

### 7. Package-manager and lifecycle overreach was avoided

The branch confirmed APT/dpkg as the current substrate backend and did not introduce pacman merely for event hooks.

It also did not implement:

```text
gl-sync
gl-status
gl-run auto-sync
one global dirty fingerprint
generational broad-farm production activation
```

This preserved architecture freedom.

## What the graphics closure actually establishes

The closure accepts the following **semantic contract**:

```text
1. bionic session graphics policy must not leak into glibc consumers;
2. glibc baseline sanitation must not select a graphics provider or bridge;
3. hardware Vulkan provider selection is explicit and consumer-scoped;
4. OpenGL/Zink bridge selection belongs to an OpenGL consumer composition;
5. Electron GPU/CPU feature mode belongs to the application domain/family policy;
6. validation state is isolated from normal user state;
7. hardware GPU acceptance requires selected-device correlation;
8. CPU acceptance is effective-mode based;
9. revalidation is claim-triggered.
```

It does **not** make the following immutable architecture objects:

```text
~/gl/env path
gl-run command name
~/gl/policy/vulkan/freedreno.sh path
GL_GPU variable name
modules/gl directory
filtered broad farm
direct checkout symlink activation
one particular Electron argv spelling forever
```

Those are current realizations of the accepted contract.

## Semantic invariant versus current adapter

The closure and integrated guides currently mix semantic language with concrete adapter/path names. The following distinction is now normative.

| Durable semantic contract | Current realization | Architectural status |
|---|---|---|
| sanitize foreign session graphics policy at world boundary | `~/gl/env` unsets four variables | accepted behavior; path/file not invariant |
| explicit managed glibc Vulkan provider | `freedreno.sh` exports both Vulkan loader variables | accepted provider contract; profile path not invariant |
| OpenGL consumer owns Zink bridge | `gl-run` sources provider and exports Zink override | accepted capability composition; command identity transitional |
| Electron app owns GPU/CPU mode | `GL_GPU` branch and argv | accepted ownership; variable name/argv may evolve |
| app validation owns isolated state | receipt-local VS Code/Obsidian paths | accepted evidence contract; harness paths not runtime architecture |
| selected-device proof requires correlation | CDP + mappings + KGSL | accepted gate semantics; probe implementation replaceable |

Future documents must use semantic terms as the primary claim and concrete paths as the current implementation note.

## Major gap 1 — the parent Obsidian selected-closure question is unfinished

The graphics work originated inside a stronger application-domain pilot.

The declared second selected-closure pilot asked whether a real Electron AppDir could consume selected external provider closures while preserving:

```text
valid application-local $ORIGIN locality
protected world substrate
prefix provider capabilities
selected rootfs provider closure
real GUI workload equivalence
```

The target candidate flow was:

```text
control capture
    -> process/maps evidence
    -> static closure
    -> semantic classification
    -> locality-shadowing check
    -> selected provider-byte materialization
    -> candidate-specific launch
    -> actual maps proof
    -> control/candidate equivalence
```

The branch completed substantial control capture, semantic classification, graphics provider decomposition, and selected-device work.

It did not complete the declared candidate materialization/equivalence step for Obsidian.

Current canonical experiment state still says candidate materialization is blocked, and the locality-shadowing/non-graphics static/runtime closure question has not been closed by `0091`.

Therefore the next focus must include one of two explicit decisions:

```text
A. resume and complete the bounded Obsidian selected-closure pilot;

or

B. terminate the pilot intentionally with a documented reason,
   preserving which architectural questions remain unanswered.
```

Silently skipping from graphics closure to PyMOL would lose the architecture-discrimination reason the Obsidian pilot was selected.

## Major gap 2 — the `gl` umbrella remains semantically broad

The ownership refactor succeeded physically, but `modules/gl` still contains:

```text
world baseline
passive data-provider policy
font/locale policy
Electron family/security policy
D-Bus policy
TLS policy
shared-library farm
OpenGL capability adapter
URL bridge
target toolchain
```

The graphics split reduces one part of the problem but does not validate `modules/gl` as a final object.

`modules/gl/README.md` currently states that the module owns the managed glibc application layer. That wording is too broad relative to the active system-foundation decision.

The module must be documented as:

```text
transitional physical deployment grouping
    !=
one final semantic owner
```

## Major gap 3 — global non-graphics policies remain in `gl/env`

The following remain global in the shared baseline:

```text
DISPLAY
XDG_RUNTIME_DIR / TMPDIR
XDG_DATA_DIRS
FONTCONFIG_PATH / FONTCONFIG_FILE
LOCPATH / LC_ALL
GSETTINGS_BACKEND=memory
NO_AT_BRIDGE=1
ELECTRON_DISABLE_SANDBOX=1
D-Bus address clearing
TLS environment variables
```

These do not all have the same minimum valid scope.

The highest-risk item is:

```text
ELECTRON_DISABLE_SANDBOX=1
```

It is an Electron-family security policy currently applied to every glibc application that sources the baseline.

This violates the target ownership model unless evidence proves that every glibc process must receive it.

Required architectural treatment:

```text
family.electron policy
    -> package/family launcher scope
    -> explicit security rationale
    -> application-version/packaging revalidation trigger
```

Other environment responsibilities also require owner decisions, but they should not be split blindly. Use the semantic inventory and discriminating tests where necessary.

Suggested priority:

```text
1. Electron sandbox policy;
2. X11/display bridge policy;
3. D-Bus client/session policy;
4. font/locale/shared-data providers;
5. TLS trust provider;
6. GSettings/accessibility policy;
7. runtime-directory policy.
```

The order is based on scope/security impact, not convenience.

## Major gap 4 — the broad farm remains the operational default

The D-Bus pilot proved a materialized selected-provider object with:

```text
actual provider bytes
provenance receipt
candidate-specific selection proof
zero broad-farm/rootfs provider leakage
protected substrate boundary
```

Yet current onboarding documentation still presents:

```text
install packages in rootfs
    -> rebuild broad farm
    -> register via ldconfig
```

as the normal application path.

This is acceptable as a description of the current operational baseline, but not as the implied target for new applications.

Before PyMOL onboarding, documentation must distinguish:

```text
legacy/current compatibility onboarding
    from
architecture-target application-domain composition
```

A new major workload should not automatically expand the broad farm or `gl/env`.

## Major gap 5 — activation is not a transaction

Current leaf deployment uses source-linked symlinks.

For existing live leaves:

```text
git update/pull
    -> live behavior changes immediately
```

The graphics migration already observed a partial activation window where existing consumer source changed before a newly required profile leaf existed.

Fail-closed or CPU fallback behavior reduced impact in that case, but the model still violates:

```text
candidate
    -> validate
    -> promote
```

Atomic activation is therefore not optional cleanup.

Before the next multi-file semantic migration, define the minimum project-authored activation boundary.

The design must not expand into a universal package manager by inertia.

Minimum requirements:

```text
candidate tree or release identity
complete managed-leaf set
pre-activation static validation
single active pointer/atomic directory transition where practical
post-activation smoke
known previous active identity
rollback that restores actual bytes/targets
```

The design may remain simple, but source checkout mutation must no longer be equivalent to activation for multi-file runtime contracts.

## Major gap 6 — the glibc 2.42 hold is containment, not lifecycle

The project correctly recovered the tested workload by restoring glibc 2.42 and preserving an exact artifact.

The current state is:

```text
working substrate:
    glibc 2.42

known-broken tested update:
    glibc 2.43

package hold:
    active containment
```

The missing lifecycle contract includes:

```text
substrate identity
candidate package/artifact acquisition
core ABI gates
provider compatibility gates
application-domain regression gates
exact previous artifact retention
rollback mechanism
hold release criteria
latest corrected/newer substrate acceptance
```

Do not solve this by reviving a broad `gl-sync` design prematurely.

The object to manage is `world.glibc` substrate, not the farm and not `gl-run`.

## Major gap 7 — data capabilities are still passive broad rootfs dependencies

The Obsidian semantic decomposition identified distinct data/provider classes:

```text
PROVIDER_LOCALE_DATA
PROVIDER_FONT_DATA
PROVIDER_SCHEMA_DATA
mutable runtime/cache state
```

Current `gl/env` still exposes broad rootfs paths for data and configuration.

This creates hidden lifecycle coupling:

```text
rootfs package/update state
    -> fonts/locale/schema behavior
    -> application behavior
```

The project must decide per capability:

```text
keep rootfs-backed provider deliberately;
materialize selected data closure;
or allow application-local ownership.
```

This is especially important before PyMOL, whose Python/scientific/GUI stack may add more locale, font, plugin, and data dependencies.

## Major gap 8 — graphics composition contains cross-version provider layers

The validated Zink graph currently includes a cross-version composition:

```text
rootfs GLVND / Mesa GLX / Gallium-Zink frontend 25.0.7
    -> prefix Vulkan loader/support
    -> provider-store Turnip/Freedreno 26.1.4 lineage
```

The project has validated the tested composition.

It has not established a general compatibility policy for independent upgrades of:

```text
GLVND/GLX frontend
Gallium/Zink frontend
Vulkan loader/support
Turnip driver/provider
Mesa device-select/GBM layers
```

This must be captured as provider-composition identity, not reduced to one `Mesa version` field.

Revalidation triggers should include changes to any layer participating in the accepted graph.

## Major gap 9 — canonical documentation drift

The project documentation control plane is not fully synchronized.

Observed drift at the audited commit:

```text
docs/refactor/README.md
    indexes current evidence only through 0057 in its precedence text
    and does not index 0058-0091 as the closed chain

experiments/glibc/vulkan-policy-composition/README.md
    still says the experiment is active,
    VS Code is next,
    and promoted launchers/gl/env are unchanged

experiments/glibc/selected-obsidian-closure/README.md
    still says semantic classification is pending
    and candidate materialization is blocked at an earlier stage

docs/refactor/MIGRATION_JOURNAL.md
    ends before live migration and says it has not run
```

This violates the project rule that session memory is not authoritative.

The correct solution is not to erase old evidence. It is to update canonical status/index documents and preserve detailed records as history.

## Major gap 10 — validator and evidence lifecycle needs consolidation

The graphics investigation produced many one-off diagnostic scripts, false-negative correction tools, comparison helpers, and final promotion validators.

That is appropriate during discovery.

After closure, the project should classify them as:

```text
ACTIVE_CONTRACT_GATE
    rerun by explicit trigger

CANONICAL_EVIDENCE_HELPER
    supports interpretation of retained receipts

HISTORICAL_DIAGNOSTIC
    retained for provenance, not routine execution

SUPERSEDED_FALSE_NEGATIVE_MODEL
    retained as caution/evidence, never reused as authority
```

Without this classification, future maintenance may mistake every experiment tool for a permanent test suite and violate minimum manipulation.

The final active graphics contract gate set should be smaller than the complete experiment recipe set.

## Gap 11 — normal user-state operation is outside promotion evidence

The isolated receipts are valid and necessary.

They prove contract behavior independent of user configuration.

They do not prove:

```text
long-duration normal-profile stability
real VS Code extension state
real Obsidian vault/plugin behavior
upgrade behavior of existing user data
performance under normal state
```

This is not a reason to reopen the graphics transaction.

It means project documentation must distinguish:

```text
architecture/promotion validation
    from
operational user acceptance
```

Application support should eventually have both classes where the project claims daily-workstation readiness.

## Documentation and naming pressure

Future integrated documentation should prefer:

```text
world-boundary graphics sanitation
explicit glibc Freedreno provider profile
OpenGL/Zink consumer composition
Electron GPU/CPU application policy
```

over path-first language such as:

```text
gl/env architecture
gl-run architecture
freedreno.sh architecture
GL_GPU architecture
```

Paths and variables remain useful operational details, but they are not the highest-level object model.

## Revised project priority

The current STATUS ordering is incomplete because it does not explicitly resume or close the selected-Obsidian-closure parent question.

Recommended order:

### Phase A — close the knowledge/control-plane transaction

```text
1. publish this architecture audit;
2. synchronize refactor index and canonical experiment READMEs;
3. classify current adapters versus semantic invariants;
4. classify active versus historical graphics validators.
```

No graphics workload rerun is required.

### Phase B — resume the architecture-discrimination parent pilot

```text
1. return to selected-obsidian-closure;
2. finish locality-shadowing analysis;
3. finish non-graphics static/runtime closure agreement;
4. decide capability grouping;
5. materialize candidate provider bytes;
6. prove candidate-specific actual selection;
7. compare control/candidate workload equivalence;
8. or explicitly terminate the pilot with reasons.
```

This remains experiment-space work; it must not mutate promoted runtime by default.

### Phase C — decide final semantic ownership split

Use the completed graphics contract and selected-closure result to decide:

```text
world.glibc base
provider.shared/data capability groups
provider.graphics.vulkan.glibc
provider.graphics.opengl.glibc
bridge.x11
bridge.url-open
family.electron policy
toolchain.glibc-target
application-domain bindings
```

Do not split directories only to mirror names. Split responsibility when evidence supports the owner.

### Phase D — define atomic activation before applying the split

The next multi-file promoted runtime migration must not use mutable checkout changes as implicit activation.

### Phase E — implement bounded ownership changes

Priority candidate:

```text
move ELECTRON_DISABLE_SANDBOX from world baseline
    to explicit Electron-family/application scope
```

because it has both scope and security significance.

Other global policy moves require their own ownership evidence.

### Phase F — establish glibc substrate upgrade/recovery lifecycle

Define exact acceptance and rollback for a corrected current/newer substrate.

### Phase G — use PyMOL as architecture proof

PyMOL should consume already-decided objects:

```text
world.glibc
python.runtime provider
display.x11 bridge/provider
graphics.opengl provider
font/locale/data providers
native-extension ABI contract
application-local payload/state
```

If PyMOL onboarding requires broadening `gl/env`, adding a new global farm exception, or treating `gl-run` as a universal launcher, stop and redirect.

## Stop lines

Do not:

```text
rerun the closed graphics gates without a documented trigger;
call gl-run/freedreno.sh/GL_GPU permanent architecture objects;
start PyMOL by copying an existing Electron launcher pattern;
expand the broad farm automatically for PyMOL;
add more policy to gl/env because it is convenient;
implement gl-sync or package-manager hooks before object/lifecycle ownership is settled;
apply another multi-file live migration before activation semantics are defined;
forget the unfinished Obsidian selected-closure question;
treat isolated profile receipts as full normal-user operational acceptance;
maintain every experiment helper as a permanent active gate.
```

## Continue / stop / redirect decisions

| Work item | Decision | Reason |
|---|---|---|
| scoped graphics-policy experiments | STOP and preserve | required claim surface is closed |
| graphics contract synthesis | CONTINUE now | convert evidence into semantic contract |
| selected Obsidian closure | RESUME or explicitly terminate | parent architecture question remains open |
| broad-farm production lifecycle | BLOCK | target provider boundary not decided |
| gl-run lifecycle expansion | BLOCK | transitional capability adapter only |
| atomic activation design | CONTINUE before next migration | current deployment violates candidate/promotion boundary |
| non-graphics env policy split | CONTINUE after activation design | significant scope debt remains |
| glibc upgrade lifecycle | CONTINUE after object boundary definition | 2.42 hold is temporary containment |
| PyMOL implementation | DEFER | must consume corrected reusable objects |
| PyMOL contract design | CONTINUE | can define requirements without mutating runtime |
| WebGPU/video/zero-copy work | SEPARATE | unrelated to closed transaction |

## Final judgment

The project has made substantial progress from a flat, workaround-driven runtime toward an evidence-backed composition architecture.

The most important successful transition is:

```text
one shared GPU switch
    ->
world sanitation
+ provider selection
+ bridge selection
+ application feature mode
+ state authority
+ evidence correlation
```

The most important unfinished transition is:

```text
one gl umbrella + broad farm
    ->
explicit world/provider/bridge/toolchain/application objects
with real candidate materialization and activation semantics
```

The project remains aligned with its philosophy only if the next stage uses the graphics closure to remove transitional privilege, not to grant it.
