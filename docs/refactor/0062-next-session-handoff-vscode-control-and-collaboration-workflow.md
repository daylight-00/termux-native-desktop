# 0062 — Next Session Handoff: VS Code Control and Collaboration Workflow

## Purpose

This document is the next-session handoff for the live architecture-refactor work on:

```text
repository:
    daylight-00/termux-native-desktop

branch:
    refactor/module-package-layout

canonical device checkout:
    $HOME/projects/termux-native-desktop
```

It records both:

```text
1. the current technical state and immediate VS Code failure boundary
2. the collaboration workflow between the user, the live Termux device, GitHub, and the assistant environment
```

The second part is essential. The work has progressed through a deliberate evidence loop rather than through speculative large refactors.

---

# 1. Authority and architecture precedence

Do not reconstruct the architecture from chat memory alone.

Use repository documents as source of truth.

Authority order:

```text
main/docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
main/docs/system-foundation/12-document-consistency-audit-and-execution-order.md
branch docs/refactor/0015-architecture-reassessment-and-hard-refactor-direction.md
branch docs/refactor/0016-next-session-handoff.md
branch docs/refactor/0017 onward as evidence and design records
```

The current work is still architecture discrimination, not implementation-by-inertia.

Current stop line:

```text
do not implement:
    gl-sync
    gl-status
    gl-run auto-sync or lifecycle authority
    pacman hooks as lifecycle authority
    one global compatibility fingerprint
    broad-farm generational activation
    new global gl environment policy
```

Allowed work:

```text
read-only inspection
identity capture
recovery and regression validation
semantic inventory
contract design
small discriminating experiments
bounded selected-closure pilots
minimum lifecycle only after semantic ownership is proven
```

---

# 2. User philosophy that must shape technical decisions

The user is explicitly wary of bottom-up accidental objects becoming architectural constraints.

Key principles:

```text
minimum manipulation, maximum effect

first understand the system and ideal model top-down,
then refactor toward proven semantic objects

if an old object such as gl-run is intrinsically limiting,
do not preserve it merely because it exists

however, do not destroy working runtime paths before evidence establishes the replacement boundary
```

The preferred pattern is:

```text
observe
    -> classify
    -> design the smallest discriminating experiment
    -> capture evidence
    -> record exact result and claim boundary
    -> only then change architecture
```

Do not jump from one successful workload to a global policy.

Consumer-specific behavior is now directly proven.

---

# 3. Collaboration workflow: device, assistant environment, GitHub

## 3.1 The user runs real-device commands

The authoritative runtime experiments execute on the user's Termux device.

Typical device prompt:

```text
u0_a534@localhost:~/projects/termux-native-desktop$
```

The assistant does not pretend that its own execution environment reproduces the live Android/Termux/glibc/Termux:X11 runtime.

The normal loop is:

```text
assistant:
    inspect repository state
    reason from prior evidence
    write or repair narrow experiment helpers
    write decision/evidence documents
    commit those changes to the refactor branch
    provide exact device commands

user:
    git fetch
    git merge --ff-only origin/refactor/module-package-layout
    run commands on the real device
    paste complete stdout/stderr and evidence paths

assistant:
    classify the exact failure/success boundary
    avoid overclaiming
    update helpers only when evidence shows a defect
    record result in docs/refactor
    commit
    provide the next bounded command
```

This loop is intentional and should continue.

## 3.2 GitHub usage

Repository reads and writes are performed through the authenticated GitHub connector from the assistant environment.

Do not assume a normal clone is available inside the assistant sandbox.

The branch is updated with normal non-force history.

Rules:

```text
never force-push

prefer small intentional commits

do not rewrite or squash evidence history merely for tidiness

when one helper failure reveals a portability or evidence-hygiene issue,
fix the helper and preserve the failed result as part of the experiment history
```

The user then synchronizes with:

```bash
cd "$HOME/projects/termux-native-desktop"
git fetch origin
git merge --ff-only origin/refactor/module-package-layout
```

The assistant must not tell the user to reset hard to a rewritten branch.

## 3.3 Assistant sandbox / local design material

Local assistant files under `/mnt/data` are not automatically repository truth.

Important distinction:

```text
GitHub branch documents
    -> shared project source of truth

/mnt/data local design files
    -> assistant-side working/design material only
```

Do not promote broad local design documents into the repository unless the user explicitly asks or the current architecture process deliberately adopts them.

Do not invent sandbox links for GitHub-only files.

## 3.4 Evidence preservation

Real-device evidence roots are commonly under:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
```

and earlier selected-closure work also uses `$PREFIX/tmp/...` roots.

The preferred pattern is:

```text
one evidence directory per bounded run

preserve:
    launch stdout/stderr
    process topology
    maps
    unique object sets
    identity enrichment
    semantic classification
    comparison products
    loader-debug summaries
```

Do not rerun an expensive workload merely because a downstream classifier or summarizer changed.

When raw capture is still valid:

```text
reuse raw evidence
    -> rerun enrichment/classification/comparison only
```

This pattern was used successfully for Obsidian shader-cache reclassification and policy comparison cleanup.

---

# 4. Important evidence discipline

Always distinguish:

```text
manifest discovered
object mapped
physical device enumerated
provider remains viable
provider selected by loader
rendering command submission
pixel correctness
performance equivalence
```

These are different evidence levels.

Examples already proven:

```text
mapped ICD object
    != selected provider

GL_GPU=1
    != hardware acceleration

provider discovery policy
    != consumer device-class intent

semantic provider closure
    != one physical supply root

lookup alias path
    != physical supplied object
    != semantic ownership boundary
```

Do not collapse those distinctions in future summaries.

---

# 5. Current technical state immediately before handoff

## 5.1 Obsidian same-feature-mode Vulkan policy A/B is closed

Both tested controls use:

```text
GL_GPU=1
LIBGL_ALWAYS_SOFTWARE unset
same Electron workload family
same experiment policy adapter
same topology/survival capture semantics
```

Policy substitution:

```text
explicit-freedreno
    -> provider-store Freedreno/Turnip
    -> KGSL
    -> hardware provider tail
    -> PASS

implicit-discovery
    -> rootfs Lavapipe/LVP
    -> llvmpipe CPU physical device
    -> software provider tail
    -> PASS
```

The implicit loader-debug evidence root is:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/obsidian-implicit-loader-debug-20260711-123513
```

The Vulkan desktop loader repeatedly reports:

```text
Using "llvmpipe (LLVM 19.1.7, 128 bits)"
with driver:
$HOME/gl/lib/libvulkan_lvp.so
```

and removes Gfxstream and Freedreno from the viable set because they expose no physical devices in that control.

The precise result and claim boundary are in:

```text
docs/refactor/0060-obsidian-implicit-loader-selected-lvp-llvmpipe.md
```

Do not build a heavier Electron tracing stack merely to re-prove this selection identity.

## 5.2 Current graphics architecture lesson

The evidence supports:

```text
stable consumer-facing graphics front half
    +
consumer-specific provider-policy composition
    +
policy-dependent provider tail
```

Cross-consumer behavior:

```text
standalone Zink:
    explicit-freedreno/default intent
        -> Turnip/KGSL
        -> PASS

    implicit-discovery/default intent
        -> llvmpipe discovered
        -> CPU pdev rejected
        -> FAIL

    implicit-discovery/software intent
        -> LVP/llvmpipe
        -> PASS

Obsidian Electron:
    GL_GPU=1 + explicit-freedreno
        -> hardware Freedreno/KGSL tail
        -> PASS

    GL_GPU=1 + implicit-discovery
        -> LVP/llvmpipe selected
        -> PASS
```

Therefore VS Code must be tested as a separate consumer.

---

# 6. Current active gate: VS Code explicit-freedreno GPU control

The plan is documented in:

```text
docs/refactor/0061-vscode-explicit-gpu-policy-consumer-validation-plan.md
```

The experiment launcher is:

```text
experiments/glibc/vulkan-policy-composition/recipe/launch-vscode-with-policy.sh
```

The capture harness was narrowly parameterized to accept:

```text
APP_ENTRYPOINT
CONTROL_NAME
```

while preserving Obsidian defaults.

No topology, survival, PPID-tree, or map-capture algorithm was intentionally changed by that parameterization.

---

# 7. Latest VS Code control result: topology capture failed before graphics interpretation

The user ran the explicit-freedreno VS Code control twice against the same evidence-root variable.

Observed command shape:

```text
APP=$HOME/gl/apps/vscode
APP_ENTRYPOINT=$APP/bin/code
CONTROL_NAME="VS Code"
LAUNCHER=experiments/.../launch-vscode-with-policy.sh
CONTROL_GL_GPU=1
VULKAN_POLICY_MODE=explicit-freedreno
VK_LOADER_DEBUG=all
SURVIVAL_SECONDS=60
```

Evidence root shown by the failed capture:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-explicit-gpu-20260711-130033
```

Both attempts reached:

```text
===== launch VS Code control =====
launch pid: <pid>
```

and then failed with:

```text
required process classes did not stabilize before wall-clock timeout

===== final observed process topology =====
pid    class    cmdline
```

The final topology table was header-only.

Therefore the correct current classification is:

```text
VS Code explicit graphics gate:
    NOT RUN / NOT INTERPRETABLE

failure boundary:
    launcher/process ownership topology before stable descendant capture

not yet evidence of:
    Vulkan failure
    Turnip failure
    ANGLE failure
    GPU-process failure
```

Do not interpret the current failure as graphics-policy failure.

---

# 8. Leading hypothesis, but not yet a fact

A plausible explanation is that:

```text
launch-vscode-with-policy.sh
    -> bash $APP/bin/code
    -> CLI wrapper may spawn/connect to Electron application process
    -> original launch PID may exit quickly
    -> real Electron processes may detach or be reparented
    -> PPID-rooted capture tree loses ownership
```

This is only a hypothesis.

It must be tested before modifying the harness.

Do not immediately replace PPID traversal with a broad global process scan.

---

# 9. First investigation order for the next session

Start by inspecting the existing partial evidence and wrapper semantics.

## Step 1 — Inspect partial evidence before rerunning

Use the known failed root:

```bash
VS_EXPLICIT_OUT="$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-explicit-gpu-20260711-130033"

printf '\n===== launch stdout =====\n'
cat "$VS_EXPLICIT_OUT/launch.stdout" 2>/dev/null || true

printf '\n===== launch stderr =====\n'
cat "$VS_EXPLICIT_OUT/launch.stderr" 2>/dev/null || true

printf '\n===== poll observations =====\n'
cat "$VS_EXPLICIT_OUT/poll-observed.tsv" 2>/dev/null || true

printf '\n===== last processes =====\n'
cat "$VS_EXPLICIT_OUT/last-processes.tsv" 2>/dev/null || true
```

The exact output should be analyzed before any new capture-helper patch.

## Step 2 — Inspect `bin/code` process behavior directly

Read the live payload wrapper and identify whether it:

```text
execs Electron in place
forks a child
uses a Node CLI process
connects to an existing instance
spawns and returns
detaches/reparents descendants
```

Useful device inspection may include:

```bash
APP="$HOME/gl/apps/vscode"

file "$APP/bin/code"
sed -n '1,260p' "$APP/bin/code"
```

If `bin/code` delegates to another script/module, inspect only the relevant path necessary to understand process ownership.

Do not copy the entire VS Code payload into the repository.

## Step 3 — Run a short read-only process-topology probe

The next discriminating experiment should determine:

```text
launch PID lifetime
child PID creation
whether descendants reparent
actual Electron main-process cmdline identity
whether `pgrep -af "$APP/"` sees processes after launch PID exits
```

Prefer a narrow diagnostic helper that records:

```text
timestamp
pid
ppid
cmdline
```

for candidate VS Code processes during the first few seconds.

Do not yet change the production launcher.

## Step 4 — Repair capture ownership semantics only after topology is known

Possible future directions, depending on evidence:

```text
A. launcher execs stable main process
    -> current failure is elsewhere; inspect stderr and immediate exit

B. wrapper child becomes stable main descendant
    -> root handoff can be followed explicitly

C. wrapper process exits and Electron main process reparents
    -> capture harness needs a bounded application-identity adoption mechanism

D. CLI connects to another instance
    -> ensure no stale instance and select a deterministic isolated user-data-dir if needed
```

Choose only the branch supported by observed topology.

---

# 10. Preferred experiment-helper design style

Helpers should be:

```text
small
single-purpose
bounded
read-only when possible
explicit about evidence root
portable to Termux shell/tooling
careful with set -euo pipefail
```

Known lessons:

```text
1. sample-count loops are not wall-clock gates when scans are expensive
   -> use Bash SECONDS for bounded wall-clock gates

2. do not run ELF-only probes on arbitrary data files under set -e
   -> separate capture from enrichment and guard readelf

3. Android/Termux awk portability matters
   -> avoid fragile multiline parenthesized awk expressions

4. process topology gates should not require optional late classes
   -> main + renderer + zygote were the stable early Obsidian gate

5. raw exact delta and interpretation delta should be separate
   -> preserve full evidence, then emit policy-relevant filtered views
```

When a helper fails because the helper is wrong, record the failed boundary, fix the helper, and reuse valid raw evidence where possible.

---

# 11. Git and documentation discipline for the next assistant

For each meaningful result:

```text
1. inspect current branch file before editing
2. make the smallest helper change needed
3. commit helper change
4. user syncs ff-only and runs it
5. analyze output
6. write docs/refactor/00xx-... result/decision record
7. update index/status documents when the project sequence changes
```

Do not leave major conclusions only in chat.

Important distinction:

```text
experiment recipe
    records how evidence is generated

decision/result document
    records what was observed, what can be concluded, and what remains unproven
```

Keep exact paths, input modes, output roots, and claim boundaries.

---

# 12. Current immediate objective

The next session should not redesign graphics architecture from scratch.

The immediate objective is:

```text
explain why VS Code control capture loses the process tree
    -> establish deterministic VS Code process ownership capture
    -> rerun explicit-freedreno GPU control
    -> obtain topology + survival + process graphics mappings + loader selected provider
    -> only then test VS Code implicit-discovery behavior
```

After VS Code A/B is complete, compare:

```text
standalone Zink
Obsidian Electron
VS Code Electron
```

and derive the minimum graphics composition contract.

Only after the consumer comparison should promoted launcher/shared-env migration be designed.

---

# 13. Communication style with the user

The user expects a collaborative engineering loop, not generic advice.

Preferred response pattern:

```text
1. classify the pasted output precisely
2. state what it proves and what it does not prove
3. identify the next smallest discriminating question
4. inspect/update repository helper and docs when needed
5. give exact copy-pasteable device commands
6. wait for real output before advancing the architecture claim
```

Do not repeatedly ask for information already present in repository documents or prior pasted output.

Do not dump speculative alternatives when one bounded experiment can discriminate them.

Do not recommend package installation merely because a diagnostic utility is missing; prefer a self-contained probe when that gives cleaner evidence.

Do not silently change promoted runtime paths during architecture discrimination.

The user is comfortable with deep low-level reasoning, but explanations should keep:

```text
observed fact
inference
hypothesis
architecture conclusion
```

clearly separated.

---

# 14. Summary for the next session

```text
Architecture direction:
    top-down semantic ownership refactor

Current graphics result:
    provider policy is consumer-specific
    GL_GPU is feature mode, not hardware identity
    Obsidian implicit selects LVP/llvmpipe and passes

Current active target:
    VS Code explicit-freedreno GPU consumer gate

Current failure:
    capture-control loses/never establishes stable VS Code process tree
    header-only final topology
    graphics gate not reached

First task:
    inspect partial stderr/stdout/poll evidence
    inspect bin/code process behavior
    capture bounded pid/ppid/cmdline topology
    repair ownership capture minimally

Workflow:
    assistant commits small helpers/docs through GitHub connector
    user ff-only syncs and runs on real Termux device
    user pastes raw output
    assistant classifies, records, and advances one discriminating gate at a time
```
