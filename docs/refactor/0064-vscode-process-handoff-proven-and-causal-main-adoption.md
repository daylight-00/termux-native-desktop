# 0064 — VS Code Process Handoff Proven and Causal Main Adoption

## Status

The bounded VS Code process-handoff probe directly observed the CLI-to-application-main transition.

The previously leading branch is now selected:

```text
C. launch wrapper and Node/CLI process exit
   actual Electron main reparents and remains viable
   PPID-rooted capture loses the application unless it adopts the main
```

The production capture harness is repaired with an optional causal descendant-adoption contract. No broad application-process scan is used for capture ownership.

## Evidence root

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-process-handoff-20260711-133241
```

Probe inputs:

```text
APP=$HOME/gl/apps/vscode
CONTROL_GL_GPU=1
VULKAN_POLICY_MODE=explicit-freedreno
LIBGL_ALWAYS_SOFTWARE unset
VK_LOADER_DEBUG unset
DURATION_SECONDS=12
POLL_SLEEP_SECONDS=0.1
```

The probe rejected pre-existing cmdlines matching `$APP/` before launch.

## Direct launch-root observation

The launch-root state changed as follows:

```text
sample 1
2026-07-11T04:32:41.249434278Z
launch PID 10743 alive

sample 9
2026-07-11T04:32:43.140639016Z
launch PID 10743 absent
```

The launch-root lifetime was therefore less than two seconds in this bounded run.

## Direct process chain

The probe observed:

```text
PID 10743
    class:
        launch-wrapper
    PPID:
        10724
    cmdline:
        bash $APP/bin/code ...

PID 10757
    class:
        node-cli
    PPID:
        10743
    cmdline:
        $APP/bin/../code
        $APP/bin/../resources/app/out/cli.js
        ...

PID 10844
    class:
        electron-main-candidate
    initial PPID:
        10757
    cmdline:
        $APP/code ...
```

This closes the transient path as:

```text
capture harness
    -> launch wrapper 10743
    -> Electron/Node CLI 10757
    -> Electron application main 10844
```

## Direct reparent observation

At:

```text
2026-07-11T04:32:43.140639016Z
```

the same Electron main PID was observed as:

```text
PID:
    10844

previous PPID:
    10757

new PPID:
    1

class:
    electron-main-candidate
```

This occurred in the same sample in which the launch root was observed absent.

The application topology continued to appear under PID 10844 after the reparent:

```text
gpu process:
    PID 10965
    PPID 10844

network utility:
    PID 10975
    PPID 10844

renderer:
    PID 11069
    descendant through zygote 10858

later NodeService utilities:
    PIDs 11241, 11243, 11281
    PPID 10844
```

Later extension-signature verification processes were also observed below the adopted application topology.

Therefore:

```text
launch root exits
    !=
Electron application exits
```

and:

```text
header-only LAUNCH_PID-rooted final topology
    !=
header-only application topology
```

## Crashpad boundary

The probe also observed:

```text
chrome_crashpad_handler
    PPID 1
```

before the main-process handoff completed.

Crashpad is therefore an independently reparented auxiliary process and is not a suitable application-main ownership anchor.

The required control topology remains:

```text
main
zygote
renderer
```

with GPU/utility classes captured when present.

## Exact conclusion

The earlier hypothesis is now an observed process-lifecycle fact for this payload:

```text
$APP/bin/code is a non-exec CLI wrapper

the wrapper starts Electron in Node/CLI mode

the CLI starts the actual Electron application main as a descendant

the actual main has exact argv0:
    $APP/code

the main has no --type= process-class argument

the wrapper and CLI exit

the main reparents to PID 1 and continues with its Electron topology
```

This is not an existing-instance connection in the observed run. The actual main was first captured as a causal descendant of the newly launched wrapper/CLI chain.

## Capture-harness repair

The shared control harness now accepts:

```text
MAIN_PROCESS_EXECUTABLE
```

Default:

```text
unset
    -> MAIN_PID=LAUNCH_PID
    -> historical Obsidian behavior
```

VS Code contract:

```text
MAIN_PROCESS_EXECUTABLE=$APP/code
```

When the optional contract is set, the harness:

```text
1. begins with the original LAUNCH_PID descendant tree
2. searches only that causal tree
3. requires argv0 to equal MAIN_PROCESS_EXECUTABLE exactly
4. rejects --type= child-process cmdlines
5. fails on more than one matching main candidate
6. records PID, PPID, phase, sample, timestamp, and cmdline
7. adopts the selected PID exactly once
8. uses that PID for later topology, survival, and final maps capture
```

New evidence outputs:

```text
main-process-contract.txt
main-process-selection.tsv
main.pid
```

The change is recorded in commit:

```text
95049a0310941d410bcea7e8d7a3cdeda1e849a0
```

## Why this is bounded adoption rather than global scanning

The application main is not selected from every process on the device.

The candidate must first be observed inside:

```text
collect_tree_pids(LAUNCH_PID)
```

Only after causal membership is established can exact argv0 identity be adopted.

After adoption:

```text
collect_tree_pids(MAIN_PID)
```

becomes the observation root.

Thus the ownership proof is:

```text
causal ancestry
    + exact executable identity
    + main-versus-child cmdline discrimination
```

not:

```text
first global process whose name resembles VS Code
```

## Revised gate state

```text
wrapper semantics:
    CLOSED

launch-root lifetime:
    CLOSED

CLI PID:
    OBSERVED

actual Electron main identity:
    OBSERVED

reparent transition:
    OBSERVED

need for bounded main adoption:
    PROVEN

repaired explicit graphics control:
    NOT YET RUN

Vulkan selected provider:
    NOT YET ESTABLISHED
```

## Claim boundary

This experiment establishes process ownership and topology-observer semantics.

It does not establish:

```text
60-second application survival under the repaired harness
final graphics process mappings
selected Vulkan driver
physical-device identity
Turnip/KGSL selection
rendering correctness
performance
```

Those questions belong to the repaired explicit-freedreno control.

## Next action

Run one fresh VS Code explicit-freedreno control with:

```text
APP_ENTRYPOINT=$APP/bin/code
MAIN_PROCESS_EXECUTABLE=$APP/code
CONTROL_GL_GPU=1
VULKAN_POLICY_MODE=explicit-freedreno
VK_LOADER_DEBUG=all
SURVIVAL_SECONDS=60
```

If topology, survival, and map capture pass, reuse that raw evidence for graphics mapping and loader-selection analysis. Do not rerun the workload for downstream classifier or summarizer changes.

No promoted VS Code launcher, shared `gl/env`, or provider policy is changed by this repair.
