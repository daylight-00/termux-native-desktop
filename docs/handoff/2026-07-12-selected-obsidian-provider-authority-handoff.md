# Selected Obsidian Provider-Authority Intervention — Session Handoff

## Purpose

This document is the onboarding entrypoint for the next session continuing the `termux-native-desktop` selected-Obsidian architecture work.

It preserves:

```text
accepted device evidence;
current architecture authority;
provider-authority intervention boundaries;
important receipt identities;
collaboration and archive workflow;
allowed and blocked next work;
unresolved questions and pass gates.
```

It does not supersede numbered architecture records.

## Repository context

```text
repository:
    daylight-00/termux-native-desktop

working checkout on device:
    $HOME/projects/termux-native-desktop

active branch:
    docs/post-graphics-architecture-audit

native device operator:
    user

assistant default role:
    architecture auditor, evidence designer, receipt verifier, and repository document/recipe author
```

The user runs authoritative Termux/device commands. The assistant does not claim to operate the device.

## Mandatory onboarding order

Read these before changing direction, recipes, or claims:

```text
main/docs/system-foundation/01-essence.md
main/docs/system-foundation/02-principles-and-invariants.md
main/docs/system-foundation/03-system-model-v2.md
main/docs/system-foundation/05-ideal-target-architecture.md
main/docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
main/docs/system-foundation/12-document-consistency-audit-and-execution-order.md

docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md
docs/refactor/0115-proot-oracle-supply-and-baseline-model.md
docs/refactor/0112-selected-obsidian-passive-map-selection-diagnostic-pass-and-contract-decision.md
docs/refactor/0117-provider-authority-intervention-adoption-and-execution-order.md
STATUS.md
experiments/glibc/selected-obsidian-closure/README.md
```

Current precedence:

```text
system-foundation
    -> constitutional intent

0116
    -> controlling intervention

0115
    -> PRoot/oracle/supply and baseline model

0112
    -> accepted passive runtime/map evidence

0117
    -> current execution order

STATUS and selected-closure README
    -> active routing and stop lines
```

## Current architecture judgment

```text
project direction:
    ON TRACK

intervention:
    ACTIVE AND BINDING

first selected generation:
    VALID IMMUTABLE EXPERIMENT EVIDENCE

passive runtime:
    PASS

final clean provider composition:
    NOT PROVEN

successor manifest/materialization:
    BLOCKED

current activation:
    BLOCKED
```

The first generation must be preserved. It must not be treated as failed, deleted, mutated, or promoted into final provider authority.

## Immutable generation state

```text
generation ID:
    obsidian-cpu-435ac66d15de2e9a3188

generation directory:
    $HOME/gl/selected/obsidian/generations/obsidian-cpu-435ac66d15de2e9a3188

content objects:
    96

selected ELF:
    91

selected fonts:
    4

generated GSettings aggregate:
    1

aliases:
    175

materialized bytes:
    70,897,301

structural validation:
    1851 / 1851 PASS

current pointer:
    ABSENT

promoted launcher change:
    NONE
```

The generation is immutable and unactivated.

## Accepted passive runtime evidence

The operator completed a no-input passive run.

```text
startup/topology:
    PASS

100-second survival:
    PASS

maps capture:
    PASS

main:
    1

renderer:
    1

zygote:
    3

GPU process:
    0

main exact --disable-gpu:
    PASS

renderer --disable-gpu-compositing:
    PASS

broad-farm mapping:
    0

rootfs-provider mapping:
    0

current-path mapping:
    0
```

This proves the selected composition can execute passively outside PRoot. It does not prove final provider-source authority.

## Accepted passive map decisions

### Xau and Xdmcp

Observed world paths:

```text
$PREFIX/glibc/lib/libXau.so.6.0.0
$PREFIX/glibc/lib/libXdmcp.so.6.0.0
```

Facts:

```text
world-selected bytes match duplicate selected-object hashes;
four selected consumers retain absolute DT_RPATH=$PREFIX/glibc/lib;
six retained dependency edges explain the substitutions;
RPATH patching is rejected;
existing generation mutation is rejected;
duplicate materialization must not recur by inertia.
```

Intervention qualification:

```text
prefix selection is not sufficient to call them WORLD_CORE_SUBSTRATE.
```

Their exact semantic authority is part of the complete provider census.

### Demand-loaded data

`DejaVuSansMono-Bold.ttf` remained present and hash-correct but was not demanded by the passive initial window.

```text
selected data presence/hash:
    REQUIRED

mapping in every scenario:
    NOT REQUIRED

mapped selected data identity:
    MUST MATCH ACCEPTED PROVIDER
```

### CPU graphics-adjacent mappings

```text
$PREFIX/glibc/lib/libX11-xcb.so.1.0.0
    observed in passive CPU runtime
    exact final semantic class still under provider audit

$HOME/gl/apps/obsidian/libvk_swiftshader.so
    app-local auxiliary mapping
    not evidence of an active GPU process
```

Closed graphics gates remain closed. Do not reopen the scoped graphics transaction merely because graphics-adjacent ELF maps under CPU mode.

## Interactive Vault-open evidence

The short-runtime Obsidian initial window appeared successfully.

The operator clicked the Vault-open control. The GTK file-chooser path then failed with:

```text
hicolor icon theme not found;
GTK fallback image-missing.png load attempted;
GdkPixbuf reported Unrecognized image file format;
gtkiconhelper assertion;
main process bailout.
```

Important evidence boundary:

```text
passive initial-window runtime:
    PASS

interactive Vault-open capability:
    FAIL / OPEN
```

The mouse click is operator evidence. It is not encoded by the process-capture receipt.

## Pixbuf/icon/MIME inventory evidence

Read-only inventory result:

```text
analysis.status:
    PASS

rootfs gdk-pixbuf loaders.cache:
    1

loader modules referenced:
    12

cache-written /usr/... module paths present natively:
    0 / 12

rootfs-prefixed referenced modules present:
    12 / 12

icon-theme indexes:
    2

MIME database files:
    5

paths absent from the B9 semantic manifest:
    20
```

The rootfs cache cannot be used unchanged because it embeds FHS `/usr/...` module paths that do not exist in the native namespace.

The inventory does not prove that all twelve modules, both icon themes, all MIME files, or Debian as a source belong in the final product.

## Important receipts

All local output roots are under:

```text
$PREFIX/tmp/selected-obsidian-closure
```

### Phase B9 publication PASS

```text
output root:
    selected-obsidian-phase-b9-generation-publication-corrected-20260712-003136

archive:
    selected-obsidian-phase-b9-generation-publication-corrected-results-20260712-003136.tgz
    or the uploaded equivalent named for the stage

archive SHA-256:
    ad351651e82d958c1805eed421dc9991ee573b1f79794c34aea6f079df84ec53

captured HEAD:
    57aa19febd6df33435afd074eb3b47c150768998
```

The authoritative local root name is the output-root name above. Confirm the actual downloaded archive name before relying on a filename variant.

### B10 first launcher-shell failure

```text
archive:
    selected-obsidian-phase-b10-explicit-generation-cpu-validation-20260712-005240.tgz

SHA-256:
    0d983e798471c1a85ae17cfe1423f40e237963ecd4e7df1a8a5c838aefe5c211

cause:
    candidate glibc LD_LIBRARY_PATH leaked into a bionic mkdir before Obsidian exec
```

Closed by exec-only candidate loader injection.

### B10 long runtime-path diagnostic

```text
output root:
    selected-obsidian-phase-b10-explicit-generation-cpu-validation-corrected-20260712-010602

archive SHA-256:
    01c14177d9ed32bb9de294aef2ccc64dba3e2afbbd1e82ed53eb705526ff3575

result:
    main began initialization but long runtime/socket paths prevented stable topology
```

Closed by short receipt-owned runtime paths.

### Short-runtime interaction-triggered receipt

```text
output root:
    selected-obsidian-phase-b10-short-runtime-cpu-validation-20260712-012415

archive SHA-256:
    529e42fbc338148f5adf36cbabc1c8a1ebc16e9408e5850dd56f5194ac92f9fe

result:
    topology PASS; operator Vault-open interaction triggered GTK pixbuf failure
```

### Pixbuf capability inventory PASS

```text
output root:
    selected-obsidian-gtk-pixbuf-runtime-capability-inventory-20260712-014314

archive SHA-256:
    e9f5fc256dbbe74e6b060fb8ebfde8745959321d20a58f8d7bd4181d19be3be6

captured HEAD:
    a1ba53e48146dc5eeb68901bea7725a2bfcbf56e
```

### Passive no-input B10

```text
output root:
    selected-obsidian-phase-b10-passive-short-runtime-cpu-validation-20260712-015859

archive SHA-256:
    86330e210a0171fd1bf059eec600cc92eac963b0e468538be77b8819214905af

captured HEAD:
    3b7cc1f4f33852f273bda77d681d035a5c3be668

capture gates:
    topology PASS
    survival PASS
    maps PASS

stage analyzer:
    FAIL only under the superseded exact mapped-object contract
```

### Passive map-selection diagnostic PASS

```text
output root:
    selected-obsidian-passive-map-selection-diagnostic-20260712-022611

archive SHA-256:
    78c6cf04963ce02f25924b900d9122bc22abcb22d2c38e0b7ca4b583d68d8bbb

captured HEAD:
    7147e42bd204b85080e645498637ca2e8415d852

analysis.status:
    PASS

next-state at the time:
    READY_FOR_CPU_MAP_CONTRACT_REDESIGN
```

`0116` now supersedes the earlier direct route from this result to successor composition.

## Earlier local receipt roots used by diagnostics

```text
B1_OUT:
    $PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b1-retained-control-locality-20260711-192919

B2_OUT:
    $PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b2-static-runtime-closure-20260711-195310

B9_OUT:
    $PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b9-generation-publication-corrected-20260712-003136

PASSIVE_B10_OUT:
    $PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b10-passive-short-runtime-cpu-validation-20260712-015859
```

Do not assume a local receipt still exists. Preflight every required path and status before a new diagnostic.

## Provider-authority intervention

### Primary required work

Perform a census over:

```text
all selected Obsidian runtime objects;
all retained/reference Obsidian runtime objects;
all relevant current $PREFIX/glibc packages and objects;
app-local providers and $ORIGIN relationships;
data capabilities;
toolchain-only and oracle-only state.
```

Required classes:

```text
WORLD_CORE_SUBSTRATE
PLATFORM_INTEGRATION_PROVIDER
GENERIC_SHARED_CAPABILITY_PROVIDER
APPLICATION_LOCAL
APPLICATION_DOMAIN_SUPPLEMENT
DATA_CAPABILITY_PROVIDER
TOOLCHAIN_ONLY
ORACLE_ONLY
MUTABLE_OR_CACHE
```

Required decision fields:

```text
object/capability name;
current selected/reference path;
package/source provenance;
semantic class;
minimum valid scope;
application domains;
app-local $ORIGIN relation;
Termux-glibc candidate;
exact Debian artifact candidate;
upstream/app-local candidate;
project-build candidate;
native Termux/Android candidate;
Termux/Android adaptation need;
ABI/version coupling;
runtime or research profile;
update owner and trigger;
provisional final authority;
missing discriminating evidence.
```

Decision order:

```text
semantic role
    -> reference authority
    -> source comparison
    -> app-local topology preservation
    -> provider and supply artifact
    -> update/revalidation scope
    -> successor include/reference decision
```

## Permitted bounded experiment

One controlled interactive Vault-open pixbuf diagnostic may continue.

It must keep:

```text
the same immutable unactivated generation;
no package installation;
no generation mutation;
no current creation or change;
no promoted launcher change;
short receipt-owned runtime paths;
rootfs pixbuf inputs as diagnostic-only;
closed graphics gates closed.
```

Required discrimination:

```text
cache effect;
loader-module effect;
icon-theme effect;
MIME effect;
combinations only after single-variable evidence.
```

Do not use the rootfs `loaders.cache` unchanged. A diagnostic cache must be receipt-local and contain the actual native absolute module paths used for that diagnostic.

A diagnostic PASS does not choose final provider authority or successor membership.

## Blocked work

Do not perform any of the following before the intervention is explicitly lifted:

```text
final successor-manifest declaration;
unified successor generation materialization;
current activation;
existing-generation mutation;
RPATH patching;
provider cleanup based only on prefix/rootfs location;
clean runtime package-list finalization;
native font provider promotion;
pixbuf/icon/MIME provider promotion;
glibc-runner baseline inclusion;
compiler/toolchain inclusion in minimum runtime;
closed graphics-gate reopening.
```

## Profile model

### Minimum workstation runtime profile

Must eventually contain only:

```text
native host/session;
minimal coherent glibc world core;
accepted platform/generic providers;
application-local payloads;
accepted application supplements;
accepted data providers;
runtime validation/status/rollback surface;
user mutable state.
```

It does not contain PRoot, GCC, toolchain packages, oracle packages, broad rootfs state, or `glibc-runner` by availability alone.

### Research/build/maintenance profile

May contain:

```text
PRoot;
pinned oracle seed and named scenarios;
APT/dpkg acquisition metadata;
gcc-glibc and explicit target wrappers;
binutils/sysroots/headers;
Python/Meson/Ninja;
artifact inspection and validators;
historical evidence receipts.
```

## Update domains that must be documented

```text
world substrate;
provider;
application;
toolchain;
oracle scenario.
```

Each needs independent identity, dependents, gates, promotion, rollback scope, and revalidation triggers.

Latest candidate acquisition may remain aggressive. Active runtime changes remain evidence-gated.

## Recommended next-session execution order

### N0 — onboarding

```text
pull docs/post-graphics-architecture-audit;
verify a clean tracked worktree;
read the mandatory authority set and this handoff;
confirm current remains absent before any runtime experiment;
confirm the first generation and required receipts still exist when needed.
```

### N1 — census schema and evidence-source plan

Create repository documentation and, if useful, a read-only analyzer schema for:

```text
glibc-prefix package/object semantic partition;
selected/reference Obsidian provider-authority matrix;
generic capability source comparison;
unresolved evidence ledger.
```

Do not make final provider decisions from path or package presence alone.

### N2 — read-only provider evidence

Prefer existing receipts first:

```text
B1 ELF inventory;
B2 retained edges;
B7/B9 semantic and content plans;
passive maps;
pixbuf inventory;
package ownership/version receipts already captured.
```

Only then design additional read-only device inventory for evidence not already present.

No package operations are allowed for census collection.

### N3 — bounded pixbuf diagnostic

May proceed in parallel or after the census schema is stable.

Treat every diagnostic input as an experiment variable and capture exact hashes, paths, process result, file-chooser behavior, and current before/after state.

### N4 — profiles and update matrix

Write:

```text
minimum workstation runtime profile;
research/build/maintenance profile;
world/provider/application/toolchain/oracle update matrix.
```

### N5 — intervention-lift preparation

Prepare, but do not execute:

```text
authority-driven successor-manifest plan;
locked supply-artifact plan;
identity separation for content/provenance/composition/install/validation;
unresolved evidence list.
```

The successor block is lifted only by an explicit audit PASS.

## Collaboration workflow

### Division of work

```text
user:
    executes authoritative Termux/device commands;
    observes GUI interactions;
    uploads stage-specific TGZ receipts;

assistant:
    reads current repository authority;
    designs bounded recipes and exact commands when permitted;
    safely inspects uploaded archives;
    independently verifies receipts against prior evidence;
    updates repository documentation and recipes;
    states precise claim boundaries and next commands.
```

### Receipt inspection discipline

For every uploaded archive:

```text
1. compute archive size and SHA-256;
2. inspect tar members without following symlinks;
3. reject/flag absolute member paths, parent traversal, devices, and unexpected special members;
4. read regular files directly from the archive where possible;
5. inspect analysis.status, failure-stage, next-state, summary, branch, and head;
6. verify current before/after evidence;
7. inspect stderr/stdout without treating warnings as fatal automatically;
8. independently reconstruct critical counts and hashes from prior receipts;
9. distinguish machine evidence from operator observation;
10. document only the claims actually reached.
```

Chromium runtime receipts can contain application-created `SingletonSocket` symlinks with absolute targets. Treat these as metadata and never follow them while inspecting an archive.

### Failure handling

```text
no blind reruns;
identify the first discriminating failure;
determine whether it is recipe, environment, workload, contract, or authority-model failure;
preserve earlier PASS claims;
change one variable where practical;
write a diagnostic record before expanding scope.
```

### Repository write workflow

Use the GitHub connector for repository reads and writes. Multiple related files may be committed with tree-based or sequential contents operations as appropriate.

Do not create a PR unless the user asks.

Keep low-level documentation current whenever a device experiment changes a claim or reveals a new boundary.

## Command and archive conventions

Always use a unique stage-specific slug.

```bash
out="<specific-stage-name>-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"
```

Required archive command:

```bash
tar czf ~/Downloads/$out.tgz $OUT
```

Conventions:

```text
out:
    lowercase archive slug

OUT:
    uppercase absolute output root

archive:
    ~/Downloads/$out.tgz
```

Never use ambiguous names such as:

```text
results.tgz
output.tgz
archive.tgz
```

When a recipe returns nonzero, still print and archive all existing evidence files.

## Environment and launcher invariants

```text
never export candidate glibc LD_LIBRARY_PATH into a bionic launcher shell;
inject the candidate loader path only in the final glibc application exec;
preserve valid application-local $ORIGIN topology;
do not use broad $HOME/gl/lib as final authority;
do not point acceptance runs at rootfs providers;
keep current absent until activation work is explicitly authorized;
use short receipt-owned runtime/socket paths for Electron/Chromium controls;
separate passive observation from interactive GUI claims.
```

## Special source decisions still open

### World core

Only loader/libc/tightly coupled runtime begins as `WORLD_CORE_SUBSTRATE` candidate.

### X11/xcb

Termux-aware or path-sensitive providers must be compared as `PLATFORM_INTEGRATION_PROVIDER` candidates rather than absorbed into core by prefix location.

### Generic capabilities

D-Bus, GTK, fontconfig, pixbuf, NSS, audio, printing, compression, TLS, and similar libraries need capability-level source rationale.

### Fonts

The current four Debian-derived fonts are transition evidence only.

The final font contract must consider:

```text
Latin;
monospace;
Bold;
Korean/CJK;
math;
fallback;
fontconfig configuration and cache ownership;
native Termux/Android/project-owned sources.
```

### Toolchain

```text
gcc-glibc plus explicit wrappers:
    accepted toolchain.glibc-target implementation

minimum workstation runtime membership:
    NO

Debian GCC:
    oracle/reference build tool by default

glibc-runner:
    excluded until unique runtime responsibility is proven
```

## Intervention-lift deliverables

Repository documentation must eventually contain:

```text
1. glibc-prefix package/object semantic partition;
2. selected/reference Obsidian provider-authority matrix;
3. generic capability source-choice rationale;
4. minimum runtime and research/build profiles;
5. five-domain update matrix;
6. separated native-font and pixbuf/icon/MIME status;
7. authority-driven successor-manifest plan;
8. unresolved evidence ledger;
9. locked supply-artifact strategy independent of mutable oracle paths.
```

## Unresolved evidence ledger

At handoff time, the following remain open:

```text
complete semantic partition of the Termux glibc package surface;
final authority for every selected/reference Obsidian object;
Termux-adaptation relevance for X11/xcb and other prefix providers;
source choice for generic GTK/GLib/fontconfig/pixbuf/NSS/audio/printing/compression capabilities;
minimum interactive Vault-open pixbuf/icon/MIME requirement;
final native font provider and coverage contract;
locked Debian/upstream/project supply artifacts independent of live rootfs paths;
minimum workstation runtime package/state declaration;
research/build/maintenance profile declaration;
five update-domain matrices;
content/provenance/composition/install/validation identity separation;
honest activation and rollback scope;
intervention-lift audit.
```

## Final stop line for the successor session

Do not:

```text
skip the provider-authority census because the first generation works;
turn a pixbuf diagnostic PASS into final provider selection;
materialize a successor generation;
create or change current;
mutate the first generation;
patch RPATH;
install packages for the bounded diagnostic;
treat prefix/rootfs/repository membership as sufficient authority;
merge compiler, oracle, or build state into the runtime profile;
reopen closed graphics work;
claim clean reconstruction from the current accumulated rootfs;
delete historical evidence before reproducible supply/scenario replacements exist.
```

The next session should preserve the successful evidence, raise the provider-authority model above historical path selection, and continue only bounded experiments that produce discriminating evidence for that model.
