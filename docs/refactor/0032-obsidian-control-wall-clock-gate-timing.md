# 0032 — Obsidian Control Wall-Clock Gate Timing Correction

## Status

The first topology/survival-gated Obsidian control harness implemented time limits as a fixed number of samples:

```text
startup samples  = STARTUP_TIMEOUT_SECONDS * 2
survival samples = SURVIVAL_SECONDS * 2
```

with a `0.5s` sleep after each sample.

This did not make the gates wall-clock bounded because every sample also executed descendant-tree discovery over `/proc`.

Observed consequence:

```text
SURVIVAL_SECONDS=100
```

did not imply a roughly 100-second survival gate; actual duration was:

```text
sum(observe_tree costs) + 100 seconds of sleeps
```

and could be substantially longer.

## Correction

Both startup and survival gates now use Bash elapsed-time deadlines based on `SECONDS`:

```text
deadline = SECONDS + requested_seconds
while SECONDS < deadline:
    observe
    evaluate
    sleep
```

The resulting semantics are:

```text
STARTUP_TIMEOUT_SECONDS
    wall-clock budget for topology acquisition

SURVIVAL_SECONDS
    wall-clock budget for survival observation
```

One in-progress observation may extend slightly past the nominal deadline, but repeated observation cost no longer accumulates outside the requested time budget.

## Progress visibility

The survival gate now emits bounded progress records at coarse intervals so a long-running but healthy experiment is distinguishable from a stalled harness.

## Interpretation

The user-observed long-running gate was a harness timing defect, not evidence that Obsidian itself had hung.

The active Obsidian closure claim remains blocked on the corrected control run:

```text
TOPOLOGY_GATE PASS
SURVIVAL_GATE PASS
CONTROL_MAP_CAPTURE PASS
```
