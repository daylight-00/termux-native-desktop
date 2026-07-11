# 0063 — VS Code CLI Wrapper Process-Handoff Diagnosis

## Status

The two failed VS Code explicit-freedreno control attempts did start a complete Electron process topology.

The control was not rejected because VS Code failed to create Electron processes. It was rejected because the Obsidian-derived capture harness assumes that the original launch PID is the long-lived Electron main process.

That assumption is false for the live VS Code payload.

Known reused partial-evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-explicit-gpu-20260711-130033
```

Because the same evidence root was used twice and the harness opens the relevant TSV/stdout/stderr files with truncating redirections, these files represent the last attempt rather than two independently preserved runs.

## Control inputs

```text
APP=$HOME/gl/apps/vscode
APP_ENTRYPOINT=$APP/bin/code
CONTROL_NAME=VS Code
CONTROL_GL_GPU=1
VULKAN_POLICY_MODE=explicit-freedreno
LIBGL_ALWAYS_SOFTWARE unset
VK_LOADER_DEBUG=all
SURVIVAL_SECONDS=60
```

## Observed launch diagnostics

`launch.stdout` was empty.

`launch.stderr` established that the experiment policy and application feature flags were applied:

```text
experiment Vulkan policy: explicit-freedreno
GL_GPU=1
VK_DRIVER_FILES=$HOME/gl/opt/mesa-glibc/share/vulkan/icd.d/freedreno_icd.aarch64.json
```

The wrapper's WSL check produced:

```text
grep: /proc/version: Permission denied
```

and the VS Code CLI reported several options as absent from its known-option list while explicitly stating that they were still passed to Electron/Chromium.

No immediate `FATAL` diagnostic, Vulkan loader failure, or Electron crash was present in the captured stderr.

The child cmdlines later confirmed that the Vulkan/ANGLE feature flags reached the Electron processes. The warnings are therefore not classified as the topology-capture failure.

## Observed process sequence

Startup sample 1 observed only the original launch PID:

```text
pid:
    15295

harness class:
    main

cmdline:
    bash $HOME/gl/apps/vscode/bin/code
        --disable-dev-shm-usage
        --ozone-platform=x11
        --disable-gpu-sandbox
        --ignore-gpu-blocklist
        --enable-features=Vulkan
        --use-gl=angle
        --use-angle=vulkan
        --disable-gpu-vsync
```

Startup sample 2 observed:

```text
15400  helper    $HOME/gl/apps/vscode/code ...
15409  zygote   $HOME/gl/apps/vscode/code --type=zygote ...
15410  zygote   $HOME/gl/apps/vscode/code --type=zygote ...
15460  gpu      $HOME/gl/apps/vscode/code --type=gpu-process ...
15464  utility  $HOME/gl/apps/vscode/code --type=utility ...
15551  renderer $HOME/gl/apps/vscode/code --type=renderer ...
```

Thus one captured sample contained:

```text
untyped Electron main candidate
zygote
gpu process
utility process
renderer
```

The untyped `$APP/code` process was classified as `helper`, not `main`.

The later final process table was header-only.

## Live wrapper semantics

The device payload identifies `$APP/bin/code` as a shell script.

Its relevant final dispatch is:

```sh
ELECTRON="$VSCODE_PATH/code"
CLI="$VSCODE_PATH/resources/app/out/cli.js"
ELECTRON_RUN_AS_NODE=1 "$ELECTRON" "$CLI" "$@"
exit $?
```

The wrapper does not use `exec`.

It invokes the Electron binary in Node/CLI mode as a child and waits for that command's status. The CLI path can then start or connect to the actual Electron application process.

## Exact harness contract mismatch

The current capture harness defines:

```text
pid == LAUNCH_PID
    -> class main
```

Any untyped Electron process with another PID falls through to:

```text
helper
```

The topology gate requires:

```text
main + renderer + zygote
```

Therefore sample 2 contained the functional process roles required by the intent of the gate, but the actual Electron main candidate could not satisfy `have_main=1`.

The harness also uses `LAUNCH_PID` as the permanent root for:

```text
PPID-descendant discovery
survival
final map capture
cleanup ownership
```

Once the wrapper/CLI launch PID disappears and application processes cease to be its descendants, the root-only observer cannot rediscover them. A header-only final table is therefore evidence that the observer lost its root, not evidence that every VS Code process exited.

## Revised failure classification

```text
VS Code Electron process creation:
    OBSERVED

main / zygote / gpu / utility / renderer creation:
    OBSERVED

current topology-gate result:
    FALSE NEGATIVE for VS Code

first harness defect:
    actual untyped Electron main candidate is classified as helper

remaining ownership question:
    whether and how the actual Electron main survives and reparents
    after the CLI/wrapper launch PID exits

explicit graphics-selection gate:
    NOT REACHED / NOT INTERPRETABLE
```

## Supported inference

The combined wrapper and process evidence strongly supports a multi-stage handoff:

```text
experiment launcher
    -> shell bin/code wrapper
    -> Electron binary in Node/CLI mode
    -> actual Electron application main
    -> Electron process topology
```

It also shows that the Obsidian contract:

```text
launch PID == application main PID
```

cannot be reused unchanged for VS Code.

## Remaining unknown

The existing PPID-rooted evidence does not directly establish:

```text
the transient Node/CLI PID
the exact parent transition of the untyped Electron main
the post-wrapper PPID of that main
whether the main remains alive throughout a bounded interval
whether a pre-existing IPC instance participates
```

The harness did check for existing processes whose cmdline matched `$APP/` before launch, so an existing matching instance was not observed. That does not replace direct handoff evidence.

## Next discriminating experiment

A new narrow helper is added at:

```text
experiments/glibc/vulkan-policy-composition/recipe/probe-vscode-process-handoff.sh
```

The probe:

```text
uses the same explicit-freedreno experiment launcher
requires GL_GPU=1
requires LIBGL_ALWAYS_SOFTWARE to be unset
rejects a pre-existing $APP/ process
runs for 12 seconds
scans only exact $APP/ cmdline matches
records timestamp, launch-root state, PID, PPID, class, and cmdline
prints only launch-state and PID/PPID/class transitions
preserves raw samples under one explicit evidence root
cleans up only observed PIDs that still match $APP/
```

This is a bounded diagnostic identity scan. It is not a decision to replace the production capture harness with a broad global process scan.

## Decision branches

```text
main candidate remains alive after launch root disappears
and its PPID changes
    -> bounded application-main adoption is required

main candidate exits with launch root
    -> inspect CLI failure/instance behavior before adoption design

CLI connects to another instance outside the exact APP identity
    -> isolated user-data-dir or stronger instance identity is required
```

Only the observed branch will be implemented.

## Claim boundary

This result establishes:

```text
the live bin/code wrapper is a non-exec CLI wrapper
a complete Electron topology was created
the harness misclassified the actual main candidate
the launch-PID-rooted contract is invalid for this consumer
```

It does not establish:

```text
post-handoff survival
selected Vulkan provider
physical-device identity
Turnip/KGSL use
rendering submission
pixel correctness
performance
```

No promoted launcher, shared `gl/env`, or graphics-provider policy is changed by this diagnosis.
