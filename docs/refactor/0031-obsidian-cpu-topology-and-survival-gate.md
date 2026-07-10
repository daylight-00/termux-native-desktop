# 0031 — Obsidian CPU Topology and Survival Gate

## Status

The topology-preserving Obsidian control rerun distinguished two separate facts.

### Stable topology observation

Across the startup observation window, the harness observed:

```text
main      89 samples
renderer  87 samples
zygote    266 samples
utility   0 samples
```

The final observed process set contained:

```text
main
three zygote processes
one renderer process
```

Therefore the previous required set:

```text
main + renderer + utility
```

was not supported by this actual CPU-path workload.

For the next control capture, the evidence-backed required stable classes are:

```text
main
renderer
zygote
```

`utility` remains observable and reportable if it appears, but is not a required control-topology class for this captured Obsidian CPU path.

## Separate survival signal

The same evidence directory later accumulated:

```text
FATAL: content/browser/gpu/gpu_data_manager_impl_private.cc:415
GPU process isn't usable. Goodbye.
```

This must not be collapsed into the topology question.

The experiment now separates:

```text
TOPOLOGY_GATE
    required process classes become stable

SURVIVAL_GATE
    main workload survives an explicit observation interval
    no fatal diagnostic is emitted
```

A topology capture can be valid even if a later survival gate fails.

A selected-closure candidate must not be built from a control workload whose survival behavior has not been characterized.

## Process discovery correction

The second harness still discovered processes by AppDir pathname occurrence in command lines.

That is insufficient for Electron because descendants may execute as:

```text
/proc/self/exe
```

and not retain a stable AppDir executable pathname in every command line.

The corrected harness now follows the actual descendant process tree rooted at the launch PID by reading `/proc/<pid>/status` parent-PID relationships.

This allows the harness to observe:

```text
main
zygote
renderer
utility
gpu-process
crashpad
other helpers
```

independently of executable-path spelling.

## Cleanup correction

The harness keeps the set of all descendant PIDs observed during the run.

Cleanup terminates the observed process set rather than only the final path-matched set. This reduces the chance that a `/proc/self/exe` helper or late descendant survives a failed experiment.

## Next control contract

The next control run must:

```text
1. discover descendants by PPID tree
2. require main + renderer + zygote topology
3. record all optional classes, including gpu and utility
4. pass an explicit survival interval
5. fail if the launch/main process exits
6. fail if stderr contains a FATAL diagnostic
7. only then capture final process maps and classify mapped objects
```

This is intentionally stricter than simply shortening the capture window to avoid the observed GPU fatal.

## Interpretation rule

Possible next outcomes are:

```text
A. topology PASS + survival PASS
    -> proceed with control maps and closure classification

B. topology PASS + survival FAIL
    -> investigate CPU-path launcher/runtime behavior before closure work

C. topology FAIL
    -> inspect descendant-tree evidence before changing the contract again
```

Candidate materialization remains blocked until outcome A is observed.
