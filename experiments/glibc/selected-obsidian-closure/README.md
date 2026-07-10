# Selected Obsidian AppDir Closure Pilot

## Status

Active architecture-discrimination experiment.

Current stage:

```text
control capture harness: ready
control CPU-path process/maps capture: pending
static/locality classification: pending
candidate materialization: not yet allowed
```

## Question

Can a real Electron AppDir application consume a selected external provider closure while preserving valid application-local `$ORIGIN` locality and protected substrate ownership?

## Why this target

The historical Obsidian AppImage experiment already established a mixed resolution model:

```text
APP_LOCAL
    bundled Electron/AppDir libraries selected from $ORIGIN

PREFIX
    Android-sensitive X11/xcb and other prefix providers

ROOTFS/FARM CONTROL
    GTK, NSS, GIO, font, desktop, and other general compatibility providers
```

This makes Obsidian a stronger discriminator than another synthetic low-level probe.

## First scope

CPU-path GUI startup only.

The first control launch sets:

```text
GL_GPU=0
```

so the closure experiment remains separate from ANGLE/Vulkan/Turnip provider-selection questions.

## Control capture contract

The harness launches the existing promoted Obsidian GUI entrypoint and captures a stable Electron process set.

Required process classes:

```text
main
renderer
utility
```

Additional classes such as:

```text
zygote
gpu
crashpad
```

are captured when observed but do not change the first required gate.

For each stable process the harness records:

```text
PID
process class
full command line
/proc/<pid>/maps
```

It then aggregates absolute mapped file paths and classifies them initially as:

```text
APP_LOCAL
PREFIX_GLIBC
ROOTFS_PROVIDER
OTHER_ABSOLUTE
```

This path classification is only the first evidence partition. Semantic ownership is determined later using package ownership and locality contracts.

## Important locality invariant

The experiment must preserve valid AppDir-local selection.

A selected external provider candidate must not shadow an object intentionally supplied by the Obsidian payload through `$ORIGIN` unless explicit replacement is part of the application contract and independently validated.

## Procedure

```bash
bash experiments/glibc/selected-obsidian-closure/recipe/capture-control.sh
```

The script refuses to run if an existing Obsidian AppDir process is already active, so experiment-owned processes can be captured and terminated without affecting an unrelated session.

## Evidence outputs

Expected files:

```text
launch.stdout
launch.stderr
processes.tsv
maps/<pid>.maps
mapped-objects.tsv
unique-objects.tsv
object-identities.tsv
class-counts.tsv
```

## Stop line

Do not yet:

```text
rewrite Obsidian RPATH
change the promoted launcher
copy external providers into a candidate
replace the broad farm
merge APP_LOCAL and selected external provider bytes
```

First capture and understand the real control process graph and mapped object sets.
