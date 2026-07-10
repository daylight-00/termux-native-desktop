# 0030 — Obsidian Control Capture First Timeout

## Status

The first selected-Obsidian control capture attempt timed out before the harness observed all required process classes:

```text
main
renderer
utility
```

The attempt did not produce the normal control evidence tables because the first harness version emitted those files only after the required-class stabilization gate passed.

This is classified as a **capture-harness observability failure**, not yet as an Obsidian workload failure.

## Device attempt

Evidence root allocated by the failed attempt:

```text
$PREFIX/tmp/selected-obsidian-control-20260710-212731
```

Observed harness result:

```text
required process classes did not stabilize before timeout
```

Observed stderr:

```text
Failed to read /proc/sys/fs/inotify/max_user_watches
Failed to connect to /run/dbus/system_bus_socket
LaunchProcess: failed to execvp: xdg-settings
```

These messages are not treated as sufficient proof of workload failure. Historical Obsidian onboarding evidence recorded the same classes of non-blocking startup messages while the application continued successfully.

## Harness defect

The first capture harness had two observability weaknesses.

### 1. Too-narrow process discovery expression

It searched only command lines matching:

```text
$APP/(obsidian|chrome_crashpad_handler)
```

The next version uses the full AppDir path prefix:

```text
$APP/
```

so every process whose command line references an executable or helper inside the payload can be observed before semantic process filtering.

### 2. Lost topology on timeout

The first version kept process-class observations only in shell variables while polling. If the required class set never became complete, it exited before writing:

```text
processes.tsv
class-counts.tsv
unique-objects.tsv
```

Therefore the failed run could not answer the critical diagnostic question:

```text
which process classes were actually observed?
```

The corrected harness now records:

```text
poll-observed.tsv
last-processes.tsv
```

throughout startup polling and prints the final observed topology before timeout failure.

## Interpretation rule

The next rerun must distinguish:

```text
A. discovery-pattern problem
B. application process-topology difference
C. process class appears only transiently
D. actual CPU-path startup failure
```

No candidate materialization or closure classification should proceed until the control process topology is captured reliably.

## Historical evidence policy

The failed attempt is preserved as evidence that control harnesses must preserve diagnostic state on failed gates.

The historical Obsidian workload evidence remains valid independently; this timeout does not supersede it.
